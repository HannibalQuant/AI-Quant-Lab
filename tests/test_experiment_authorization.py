"""Sprint 10 controlled experiment authorization foundation tests."""

from __future__ import annotations

from dataclasses import replace
from datetime import UTC, datetime
from pathlib import Path

import pytest
from test_research_dataset_eligibility import evaluate

from ai_quant_lab import EXE_01
from ai_quant_lab.core.codec import decode, encode
from ai_quant_lab.core.dataset_store import (
    RepositoryIntegrityFailure,
    repository_key,
)
from ai_quant_lab.core.experiment_authorization import (
    ExperimentAuthorizationRequest,
    authorize_experiment,
    experiment_configuration_fingerprint,
)
from ai_quant_lab.core.experiment_contracts import (
    CostSemantics,
    ExperimentAuthorizationDecision,
    ExperimentAuthorizationPolicy,
    ExperimentAuthorizationRecord,
    ExperimentContractError,
    ExperimentFamily,
    ExperimentLifecycleBoundary,
    ExperimentSpecification,
    NoLookaheadSemantics,
    PositionSizingSemantics,
)
from ai_quant_lab.core.integrity import fingerprint_record
from ai_quant_lab.core.model import (
    AgentId,
    ArtifactId,
    ExecutionState,
    ExperimentId,
    ObjectVersion,
    ProvenanceId,
    TraceabilityRef,
)
from ai_quant_lab.core.research_eligibility_contracts import (
    DeploymentAuthorizationStatus,
    EligibilityCalendarSemantics,
    ValidationStatus,
)

V1 = ObjectVersion(1)
DECISION_TIME = datetime(2025, 2, 3, tzinfo=UTC)
ENGINE_REF = TraceabilityRef(ArtifactId("experiment-engine-contract-v1"), V1, "sha256:" + "1" * 64)
PROVENANCE_REF = TraceabilityRef(ProvenanceId("experiment-spec-provenance"), V1, "sha256:" + "2" * 64)


def specification(eligibility, *, seed: int = 42, commission=CostSemantics.DECLARED_BPS,
                  slippage=CostSemantics.DECLARED_BPS,
                  funding=CostSemantics.NOT_APPLICABLE,
                  no_lookahead=NoLookaheadSemantics.EXPLICIT_EVENT_AVAILABILITY_NEXT_EVENT,
                  sizing=PositionSizingSemantics.FIXED_NOTIONAL) -> ExperimentSpecification:
    assert eligibility.normalized_manifest_ref is not None
    assert eligibility.normalized_lock_ref is not None
    return ExperimentSpecification(
        ExperimentId("controlled-experiment"),
        V1,
        TraceabilityRef(
            eligibility.eligibility_id,
            eligibility.version,
            fingerprint_record(eligibility),
        ),
        eligibility.normalized_manifest_ref,
        eligibility.normalized_lock_ref,
        ExperimentFamily.MARKET_STATISTICS,
        "Measure deterministic market statistics under governed temporal assumptions.",
        ArtifactId("hypothesis-market-statistics"),
        (("lookback_bars", "24"), ("mode", "descriptive")),
        seed,
        datetime(2025, 2, 1, tzinfo=UTC),
        datetime(2025, 2, 1, 3, tzinfo=UTC),
        datetime(2025, 2, 2, tzinfo=UTC),
        no_lookahead,
        24,
        commission,
        10 if commission is CostSemantics.DECLARED_BPS else 0,
        slippage,
        5 if slippage is CostSemantics.DECLARED_BPS else 0,
        funding,
        0,
        EligibilityCalendarSemantics.FIXED_UTC_CONTINUOUS,
        sizing,
        100_000,
        ENGINE_REF,
        ("max_drawdown", "total_return"),
        ("diagnostics", "return_series"),
        AgentId("experiment-proposer"),
        PROVENANCE_REF,
        V1,
    )


def authorization_policy(*, require_actor: bool = False) -> ExperimentAuthorizationPolicy:
    return ExperimentAuthorizationPolicy(
        ArtifactId("experiment-authorization-policy"),
        V1,
        (ExperimentFamily.MARKET_STATISTICS,),
        NoLookaheadSemantics.EXPLICIT_EVENT_AVAILABILITY_NEXT_EVENT,
        (EligibilityCalendarSemantics.FIXED_UTC_CONTINUOUS,),
        True,
        True,
        False,
        True,
        365,
        0,
        2**31,
        (ENGINE_REF,),
        require_actor,
        AgentId("experiment-governance-owner"),
        V1,
    )


def authorize(tmp_path: Path, *, spec_mutator=None, policy_mutator=None, actor_verified=False):
    onboarding, repository, admitted, eligibility_policy, decision = evaluate(
        tmp_path, suffix="experiment"
    )
    assert admitted.report is not None
    spec = specification(decision.record)
    policy = authorization_policy()
    if spec_mutator is not None:
        spec = spec_mutator(spec)
    if policy_mutator is not None:
        policy = policy_mutator(policy)
    request = ExperimentAuthorizationRequest(
        ArtifactId("experiment-authorization"),
        spec,
        policy,
        DECISION_TIME,
        AgentId("experiment-authorizer"),
        actor_verified,
    )
    result = authorize_experiment(
        request,
        eligibility=decision.record,
        eligibility_policy=eligibility_policy,
        admission=admitted.admission,
        declaration=onboarding.declaration,
        report=admitted.report,
        repository=repository,
    )
    return repository, decision.record, spec, policy, result


def test_exact_eligible_dataset_can_authorize_declaration_only(tmp_path: Path) -> None:
    repository, eligibility, spec, policy, result = authorize(tmp_path)
    record = result.record
    assert record.status is ExperimentAuthorizationDecision.AUTHORIZED
    assert record.lifecycle is ExperimentLifecycleBoundary.AUTHORIZED_NOT_EXECUTED
    assert record.validation_status is ValidationStatus.NOT_VALIDATED
    assert record.deployment_authorization is DeploymentAuthorizationStatus.NOT_AUTHORIZED
    assert record.execution_state is ExecutionState.PLANNED_CLOSED
    assert EXE_01.state is ExecutionState.PLANNED_CLOSED
    assert len(result.writes) == 3
    assert repository.load(repository_key(spec), ExperimentSpecification).record == spec
    assert repository.load(repository_key(policy), ExperimentAuthorizationPolicy).record == policy
    assert repository.load(repository_key(record), ExperimentAuthorizationRecord).record == record
    assert decode(encode(spec), ExperimentSpecification) == spec
    assert decode(encode(policy), ExperimentAuthorizationPolicy) == policy
    assert decode(encode(record), ExperimentAuthorizationRecord) == record
    assert not hasattr(result, "pnl")
    assert not hasattr(result, "trade_ledger")


def test_authorization_is_deterministic_and_idempotent(tmp_path: Path) -> None:
    onboarding, repository, admitted, eligibility_policy, decision = evaluate(
        tmp_path, suffix="deterministic"
    )
    assert admitted.report is not None
    spec = specification(decision.record)
    policy = authorization_policy()
    request = ExperimentAuthorizationRequest(
        ArtifactId("experiment-authorization"),
        spec,
        policy,
        DECISION_TIME,
        AgentId("experiment-authorizer"),
    )
    first = authorize_experiment(
        request,
        eligibility=decision.record,
        eligibility_policy=eligibility_policy,
        admission=admitted.admission,
        declaration=onboarding.declaration,
        report=admitted.report,
        repository=repository,
    )
    second = authorize_experiment(
        request,
        eligibility=decision.record,
        eligibility_policy=eligibility_policy,
        admission=admitted.admission,
        declaration=onboarding.declaration,
        report=admitted.report,
        repository=repository,
    )
    assert first.record == second.record
    assert fingerprint_record(first.record) == fingerprint_record(second.record)
    assert all(write.status.value == "ALREADY_PRESENT_IDENTICAL" for write in second.writes)


def test_seed_and_configuration_change_identity(tmp_path: Path) -> None:
    _, eligibility, first, _, _ = authorize(tmp_path)
    second = replace(first, random_seed=43)
    third = replace(first, configuration=(("lookback_bars", "48"), ("mode", "descriptive")))
    assert fingerprint_record(first) != fingerprint_record(second)
    assert fingerprint_record(first) != fingerprint_record(third)
    assert experiment_configuration_fingerprint(first) != experiment_configuration_fingerprint(second)


def test_noneligible_or_wrong_dataset_cannot_authorize(tmp_path: Path) -> None:
    onboarding, repository, admitted, eligibility_policy, decision = evaluate(
        tmp_path, suffix="wrong-dataset"
    )
    assert admitted.report is not None
    spec = specification(decision.record)
    wrong_eligibility = replace(
        decision.record,
        status=decision.record.status.INCOMPLETE,
        findings=("forced_incomplete",),
        research_boundary=decision.record.research_boundary.NOT_ADMITTED_TO_RESEARCH,
    )
    request = ExperimentAuthorizationRequest(
        ArtifactId("experiment-authorization"),
        spec,
        authorization_policy(),
        DECISION_TIME,
        AgentId("experiment-authorizer"),
    )
    with pytest.raises(ValueError):
        authorize_experiment(
            request,
            eligibility=wrong_eligibility,
            eligibility_policy=eligibility_policy,
            admission=admitted.admission,
            declaration=onboarding.declaration,
            report=admitted.report,
            repository=repository,
        )
    with pytest.raises(ValueError):
        authorize_experiment(
            replace(request, specification=replace(spec, normalized_lock_ref=TraceabilityRef(
                spec.normalized_lock_ref.object_id, V1, "sha256:" + "9" * 64
            ))),
            eligibility=decision.record,
            eligibility_policy=eligibility_policy,
            admission=admitted.admission,
            declaration=onboarding.declaration,
            report=admitted.report,
            repository=repository,
        )


@pytest.mark.parametrize(
    ("mutator", "expected"),
    [
        (lambda s: replace(s, no_lookahead=NoLookaheadSemantics.UNKNOWN), ExperimentAuthorizationDecision.INCOMPLETE),
        (lambda s: replace(s, commission_semantics=CostSemantics.UNKNOWN, commission_bps=0), ExperimentAuthorizationDecision.INCOMPLETE),
        (lambda s: replace(s, slippage_semantics=CostSemantics.UNKNOWN, slippage_bps=0), ExperimentAuthorizationDecision.INCOMPLETE),
        (lambda s: replace(s, sizing_semantics=PositionSizingSemantics.UNKNOWN), ExperimentAuthorizationDecision.INCOMPLETE),
        (lambda s: replace(s, engine_contract_ref=TraceabilityRef(ArtifactId("unsupported-engine"), V1, "sha256:" + "3" * 64)), ExperimentAuthorizationDecision.UNSUPPORTED),
        (lambda s: replace(s, random_seed=2**31 + 1), ExperimentAuthorizationDecision.REJECTED),
    ],
)
def test_policy_fail_closed_for_unknown_or_unsupported_semantics(
    tmp_path: Path, mutator, expected
) -> None:
    _, _, _, _, result = authorize(tmp_path, spec_mutator=mutator)
    assert result.record.status is expected
    assert result.record.status is not ExperimentAuthorizationDecision.AUTHORIZED
    assert result.record.findings


def test_actor_identity_alone_does_not_satisfy_verified_authority(tmp_path: Path) -> None:
    _, _, _, _, result = authorize(
        tmp_path,
        policy_mutator=lambda p: replace(p, require_verified_actor_authority=True),
        actor_verified=False,
    )
    assert result.record.status is ExperimentAuthorizationDecision.INCOMPLETE
    assert "authorization_actor_unverified" in result.record.findings


def test_explicit_zero_cost_is_distinct_from_unknown(tmp_path: Path) -> None:
    _, _, zero_spec, _, zero = authorize(
        tmp_path,
        spec_mutator=lambda s: replace(
            s, commission_semantics=CostSemantics.DECLARED_ZERO, commission_bps=0
        ),
    )
    assert zero.record.status is ExperimentAuthorizationDecision.AUTHORIZED
    _, _, unknown_spec, _, unknown = authorize(
        tmp_path,
        spec_mutator=lambda s: replace(
            s, commission_semantics=CostSemantics.UNKNOWN, commission_bps=0
        ),
    )
    assert unknown.record.status is ExperimentAuthorizationDecision.INCOMPLETE
    assert fingerprint_record(zero_spec) != fingerprint_record(unknown_spec)


def test_invalid_temporal_and_configuration_contracts_fail_at_construction(tmp_path: Path) -> None:
    _, eligibility, spec, _, _ = authorize(tmp_path)
    with pytest.raises(ExperimentContractError):
        replace(spec, observation_start=spec.observation_end)
    with pytest.raises(ExperimentContractError):
        replace(spec, observation_start=datetime(2025, 2, 1))
    with pytest.raises(ExperimentContractError):
        replace(spec, configuration=(("z", "1"), ("a", "2")))
    with pytest.raises(ExperimentContractError):
        replace(spec, random_seed=-1)


def test_corrupted_persisted_authorization_fails_integrity(tmp_path: Path) -> None:
    repository, _, _, _, result = authorize(tmp_path)
    path = repository.path_for(repository_key(result.record))
    path.write_bytes(path.read_bytes().replace(b'"AUTHORIZED"', b'"INCOMPLETE"'))
    with pytest.raises(RepositoryIntegrityFailure):
        repository.load(repository_key(result.record), ExperimentAuthorizationRecord)
