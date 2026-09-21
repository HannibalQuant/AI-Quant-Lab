"""Sprint 11 controlled deterministic experiment runner tests."""

from __future__ import annotations

import ast
import inspect
import json
from dataclasses import replace
from datetime import UTC, datetime, timedelta
from pathlib import Path

import pytest
from test_real_csv_onboarding import CLOCK, HEADER
from test_real_csv_onboarding import context as real_csv_context
from test_research_dataset_eligibility import (
    eligibility_request,
    evaluate,
)
from test_research_dataset_eligibility import (
    policy as eligibility_policy_contract,
)

from ai_quant_lab import EXE_01
from ai_quant_lab.core import experiment_runner as runner_module
from ai_quant_lab.core.codec import decode, encode
from ai_quant_lab.core.csv_import import CsvImportReport
from ai_quant_lab.core.dataset_store import (
    LocalDatasetRepository,
    RepositoryIntegrityFailure,
    RepositoryTypeMismatch,
    RepositoryWriteStatus,
    repository_key,
)
from ai_quant_lab.core.experiment_authorization import (
    ExperimentAuthorizationRequest,
    ExperimentAuthorizationResult,
    authorize_experiment,
)
from ai_quant_lab.core.experiment_contracts import (
    CostSemantics,
    ExperimentAuthorizationDecision,
    ExperimentAuthorizationPolicy,
    ExperimentAuthorizationRecord,
    ExperimentFamily,
    ExperimentLifecycleBoundary,
    ExperimentSpecification,
    NoLookaheadSemantics,
    PositionSizingSemantics,
)
from ai_quant_lab.core.experiment_runner import (
    ExperimentResultLineageMismatch,
    ExperimentRunnerLineageMismatch,
    ExperimentRunRequest,
    ExperimentRunResult,
    ExperimentTimeWindowMismatch,
    InvalidExperimentAuthorization,
    MissingRequiredBars,
    ReplayOrderingFailure,
    UnsupportedExperimentRunner,
    UnsupportedReturnDomain,
    _require_market_statistics_scope,
    _select_replay_bars,
    available_bars_at,
    market_statistics_engine_ref,
    market_statistics_replay_contract,
    run_authorized_experiment,
    verify_experiment_result_lineage,
)
from ai_quant_lab.core.experiment_runner_contracts import (
    ExperimentReplayContract,
    ExperimentResultArtifact,
    ExperimentRunRecord,
    ExperimentRunStatus,
    ResearchExperimentExecutionStatus,
)
from ai_quant_lab.core.integrity import fingerprint_record
from ai_quant_lab.core.model import (
    AgentId,
    ArtifactId,
    ExecutionState,
    ExperimentId,
    ObjectVersion,
    ProvenanceId,
    RunId,
    TraceabilityRef,
)
from ai_quant_lab.core.real_csv_contracts import (
    PriceDomain,
    RealCsvAdmissionRecord,
    RealCsvSourceDeclaration,
)
from ai_quant_lab.core.real_csv_onboarding import onboard_real_csv
from ai_quant_lab.core.research_eligibility import evaluate_research_dataset_eligibility
from ai_quant_lab.core.research_eligibility_contracts import (
    DeploymentAuthorizationStatus,
    EligibilityCalendarSemantics,
    ResearchDatasetEligibilityPolicy,
    ResearchDatasetEligibilityRecord,
    ValidationStatus,
)

V1 = ObjectVersion(1)
DECISION_TIME = datetime(2025, 2, 3, tzinfo=UTC)
COMPLETED_AT = datetime(2025, 2, 3, 1, tzinfo=UTC)
PROVENANCE_REF = TraceabilityRef(
    ProvenanceId("experiment-run-provenance"), V1, "sha256:" + "7" * 64
)

type AuthorizedContext = tuple[
    RealCsvSourceDeclaration,
    LocalDatasetRepository,
    RealCsvAdmissionRecord,
    CsvImportReport,
    ResearchDatasetEligibilityPolicy,
    ResearchDatasetEligibilityRecord,
    ExperimentSpecification,
    ExperimentAuthorizationPolicy,
    ExperimentAuthorizationResult,
]


def exact(record: object, object_id: object, version: ObjectVersion) -> TraceabilityRef:
    return TraceabilityRef(object_id, version, fingerprint_record(record))  # type: ignore[arg-type]


def specification(
    eligibility: ResearchDatasetEligibilityRecord,
    *,
    seed: int = 42,
    start: datetime = datetime(2025, 2, 1, tzinfo=UTC),
    end: datetime = datetime(2025, 2, 1, 3, tzinfo=UTC),
    mode: str = "descriptive",
) -> ExperimentSpecification:
    assert eligibility.normalized_manifest_ref is not None
    assert eligibility.normalized_lock_ref is not None
    return ExperimentSpecification(
        ExperimentId("market-statistics-experiment"),
        V1,
        exact(eligibility, eligibility.eligibility_id, eligibility.version),
        eligibility.normalized_manifest_ref,
        eligibility.normalized_lock_ref,
        ExperimentFamily.MARKET_STATISTICS,
        "Produce bounded descriptive market statistics without trading.",
        ArtifactId("market-statistics-hypothesis"),
        (("mode", mode),),
        seed,
        start,
        end,
        datetime(2025, 2, 2, tzinfo=UTC),
        NoLookaheadSemantics.EXPLICIT_EVENT_AVAILABILITY_NEXT_EVENT,
        0,
        CostSemantics.NOT_APPLICABLE,
        0,
        CostSemantics.NOT_APPLICABLE,
        0,
        CostSemantics.NOT_APPLICABLE,
        0,
        EligibilityCalendarSemantics.FIXED_UTC_CONTINUOUS,
        PositionSizingSemantics.NOT_APPLICABLE,
        0,
        market_statistics_engine_ref(),
        (
            "close_max",
            "close_min",
            "observation_count",
            "simple_return_mean",
            "simple_return_population_variance",
        ),
        ("return_series",),
        AgentId("market-statistics-proposer"),
        TraceabilityRef(ProvenanceId("market-statistics-specification"), V1, "sha256:" + "6" * 64),
        V1,
    )


def authorization_policy() -> ExperimentAuthorizationPolicy:
    return ExperimentAuthorizationPolicy(
        ArtifactId("market-statistics-authorization-policy"),
        V1,
        (ExperimentFamily.MARKET_STATISTICS,),
        NoLookaheadSemantics.EXPLICIT_EVENT_AVAILABILITY_NEXT_EVENT,
        (EligibilityCalendarSemantics.FIXED_UTC_CONTINUOUS,),
        False,
        False,
        False,
        False,
        365,
        0,
        2**31,
        (market_statistics_engine_ref(),),
        False,
        AgentId("experiment-governance-owner"),
        V1,
    )


def authorized_context(
    tmp_path: Path,
    *,
    suffix: str = "runner",
    seed: int = 42,
    start: datetime = datetime(2025, 2, 1, tzinfo=UTC),
    end: datetime = datetime(2025, 2, 1, 3, tzinfo=UTC),
    mode: str = "descriptive",
) -> AuthorizedContext:
    onboarding, repository, admitted, eligibility_policy, eligibility_result = evaluate(
        tmp_path, suffix=suffix
    )
    assert admitted.report is not None
    spec = specification(eligibility_result.record, seed=seed, start=start, end=end, mode=mode)
    policy = authorization_policy()
    authorization = authorize_experiment(
        ExperimentAuthorizationRequest(
            ArtifactId("market-statistics-authorization"),
            spec,
            policy,
            DECISION_TIME,
            AgentId("experiment-authorizer"),
        ),
        eligibility=eligibility_result.record,
        eligibility_policy=eligibility_policy,
        admission=admitted.admission,
        declaration=onboarding.declaration,
        report=admitted.report,
        repository=repository,
    )
    assert authorization.record.status is ExperimentAuthorizationDecision.AUTHORIZED
    return (
        onboarding.declaration,
        repository,
        admitted.admission,
        admitted.report,
        eligibility_policy,
        eligibility_result.record,
        spec,
        policy,
        authorization,
    )


def signed_authorized_context(
    tmp_path: Path, closes: tuple[str, str, str], *, suffix: str
) -> AuthorizedContext:
    rows: list[str] = []
    for index, close_text in enumerate(closes):
        close = int(close_text)
        rows.append(
            f"2025-02-01T{index:02d}:00:00.000000Z,"
            f"2025-02-01T{index + 1:02d}:00:00.000000Z,"
            f"{close},{close + 1},{close - 1},{close},{10 + index},final,"
            f"2025-02-01T{index + 1:02d}:00:05.000000Z\n"
        )
    csv_path = tmp_path / f"signed-{suffix}.csv"
    csv_path.write_text(HEADER + "".join(rows), encoding="utf-8")
    onboarding, source, instrument, schema, timeframe, repository = real_csv_context(
        tmp_path,
        path=csv_path,
        allowed_root=tmp_path,
        suffix=suffix,
    )
    declaration = replace(onboarding.declaration, price_domain=PriceDomain.SIGNED)
    declaration_ref = exact(declaration, declaration.provenance_id, declaration.version)
    ingestion = replace(
        onboarding.csv_request.ingestion,
        observation_provenance_ref=declaration_ref,
        manifest_provenance_ref=declaration_ref,
        lock_provenance_ref=declaration_ref,
    )
    csv_request = replace(
        onboarding.csv_request,
        ingestion=ingestion,
        normalization_provenance_ref=declaration_ref,
        normalized_provenance_ref=declaration_ref,
    )
    onboarding = replace(onboarding, declaration=declaration, csv_request=csv_request)
    admitted = onboard_real_csv(
        onboarding,
        source=source,
        instrument=instrument,
        schema=schema,
        timeframe=timeframe,
        clock=CLOCK,
        repository=repository,
    )
    assert admitted.report is not None
    eligibility_policy = eligibility_policy_contract()
    eligibility = evaluate_research_dataset_eligibility(
        eligibility_request(
            declaration,
            admitted.admission,
            eligibility_policy,
            admitted.report,
            eligibility_id=f"research-dataset-eligibility-{suffix}",
        ),
        admission=admitted.admission,
        declaration=declaration,
        report=admitted.report,
        repository=repository,
    ).record
    spec = specification(eligibility)
    policy = authorization_policy()
    authorization = authorize_experiment(
        ExperimentAuthorizationRequest(
            ArtifactId("market-statistics-authorization"),
            spec,
            policy,
            DECISION_TIME,
            AgentId("experiment-authorizer"),
        ),
        eligibility=eligibility,
        eligibility_policy=eligibility_policy,
        admission=admitted.admission,
        declaration=declaration,
        report=admitted.report,
        repository=repository,
    )
    assert authorization.record.status is ExperimentAuthorizationDecision.AUTHORIZED
    return (
        declaration,
        repository,
        admitted.admission,
        admitted.report,
        eligibility_policy,
        eligibility,
        spec,
        policy,
        authorization,
    )


def run_request(
    authorization: ExperimentAuthorizationRecord,
    specification: ExperimentSpecification,
    policy: ExperimentAuthorizationPolicy,
    eligibility: ResearchDatasetEligibilityRecord,
    *,
    completed_at: datetime = COMPLETED_AT,
) -> ExperimentRunRequest:
    engine = market_statistics_replay_contract()
    return ExperimentRunRequest(
        RunId("deterministic-market-statistics-run"),
        ArtifactId("deterministic-market-statistics-result"),
        exact(authorization, authorization.authorization_id, authorization.version),
        exact(specification, specification.experiment_id, specification.version),
        exact(policy, policy.policy_id, policy.version),
        exact(eligibility, eligibility.eligibility_id, eligibility.version),
        exact(engine, engine.engine_id, engine.version),
        completed_at,
        PROVENANCE_REF,
    )


def execute_context(
    context: AuthorizedContext,
) -> tuple[ExperimentRunRequest, ExperimentRunResult]:
    (
        declaration,
        repository,
        admission,
        report,
        eligibility_policy,
        eligibility,
        spec,
        policy,
        auth,
    ) = context
    request = run_request(auth.record, spec, policy, eligibility)
    result = run_authorized_experiment(
        request,
        authorization=auth.record,
        specification=spec,
        policy=policy,
        eligibility=eligibility,
        eligibility_policy=eligibility_policy,
        admission=admission,
        declaration=declaration,
        report=report,
        engine_contract=market_statistics_replay_contract(),
        repository=repository,
    )
    return request, result


def execute(
    tmp_path: Path,
    *,
    suffix: str = "runner",
    seed: int = 42,
    mode: str = "descriptive",
) -> tuple[AuthorizedContext, ExperimentRunRequest, ExperimentRunResult]:
    context = authorized_context(tmp_path, suffix=suffix, seed=seed, mode=mode)
    request, result = execute_context(context)
    return context, request, result


def test_authorized_market_statistics_executes_and_persists_exactly(tmp_path: Path) -> None:
    (context, request, result) = execute(tmp_path)
    repository = context[1]
    assert result.record.status is ExperimentRunStatus.COMPLETED
    assert result.record.research_execution is (
        ResearchExperimentExecutionStatus.RESEARCH_EXPERIMENT_EXECUTED
    )
    assert result.artifact.observation_count == 3
    assert result.artifact.close_min == "101"
    assert result.artifact.close_max == "103"
    assert len(result.artifact.simple_returns) == 2
    assert result.record.run_id == request.run_id
    assert (
        repository.load(repository_key(result.record), ExperimentRunRecord).record == result.record
    )
    assert (
        repository.load(repository_key(result.artifact), ExperimentResultArtifact).record
        == result.artifact
    )
    assert decode(encode(result.record), ExperimentRunRecord) == result.record
    assert decode(encode(result.artifact), ExperimentResultArtifact) == result.artifact


def test_result_never_grants_validation_deployment_or_live_execution(tmp_path: Path) -> None:
    _, _, result = execute(tmp_path)
    for record in (result.record, result.artifact):
        assert record.validation_status is ValidationStatus.NOT_VALIDATED
        assert record.deployment_authorization is DeploymentAuthorizationStatus.NOT_AUTHORIZED
        assert record.execution_state is ExecutionState.PLANNED_CLOSED
    assert EXE_01.state is ExecutionState.PLANNED_CLOSED
    assert not hasattr(result, "orders")
    assert not hasattr(result, "pnl")


def test_exact_rerun_is_byte_deterministic_and_repository_idempotent(tmp_path: Path) -> None:
    context, request, first = execute(tmp_path)
    (
        declaration,
        repository,
        admission,
        report,
        eligibility_policy,
        eligibility,
        spec,
        policy,
        auth,
    ) = context
    second = run_authorized_experiment(
        request,
        authorization=auth.record,
        specification=spec,
        policy=policy,
        eligibility=eligibility,
        eligibility_policy=eligibility_policy,
        admission=admission,
        declaration=declaration,
        report=report,
        engine_contract=market_statistics_replay_contract(),
        repository=repository,
    )
    assert first.record == second.record
    assert first.artifact == second.artifact
    assert encode(first.record) == encode(second.record)
    assert encode(first.artifact) == encode(second.artifact)
    assert all(
        write.status is RepositoryWriteStatus.ALREADY_PRESENT_IDENTICAL for write in second.writes
    )


def test_seed_changes_run_and_result_identity(tmp_path: Path) -> None:
    first_root = tmp_path / "first"
    second_root = tmp_path / "second"
    first_root.mkdir()
    second_root.mkdir()
    _, _, first = execute(first_root, suffix="seed-a", seed=42)
    _, _, second = execute(second_root, suffix="seed-b", seed=43)
    assert first.record.run_input_fingerprint != second.record.run_input_fingerprint
    assert fingerprint_record(first.artifact) != fingerprint_record(second.artifact)


def test_configuration_changes_run_and_result_identity(tmp_path: Path) -> None:
    first_root = tmp_path / "first"
    second_root = tmp_path / "second"
    first_root.mkdir()
    second_root.mkdir()
    _, _, first = execute(first_root, suffix="config-a", mode="descriptive")
    _, _, second = execute(second_root, suffix="config-b", mode="alternate-declaration")
    assert first.record.run_input_fingerprint != second.record.run_input_fingerprint
    assert fingerprint_record(first.artifact) != fingerprint_record(second.artifact)


def test_exact_subwindow_replays_only_authorized_bars(tmp_path: Path) -> None:
    context = authorized_context(
        tmp_path,
        start=datetime(2025, 2, 1, 1, tzinfo=UTC),
        end=datetime(2025, 2, 1, 3, tzinfo=UTC),
    )
    (
        declaration,
        repository,
        admission,
        report,
        eligibility_policy,
        eligibility,
        spec,
        policy,
        auth,
    ) = context
    result = run_authorized_experiment(
        run_request(auth.record, spec, policy, eligibility),
        authorization=auth.record,
        specification=spec,
        policy=policy,
        eligibility=eligibility,
        eligibility_policy=eligibility_policy,
        admission=admission,
        declaration=declaration,
        report=report,
        engine_contract=market_statistics_replay_contract(),
        repository=repository,
    )
    assert result.artifact.observation_count == 2
    assert result.artifact.first_event_time == spec.observation_start
    assert result.artifact.last_event_time == spec.observation_end


@pytest.mark.parametrize(
    "status",
    [
        ExperimentAuthorizationDecision.REJECTED,
        ExperimentAuthorizationDecision.INCOMPLETE,
        ExperimentAuthorizationDecision.UNSUPPORTED,
        ExperimentAuthorizationDecision.QUARANTINED,
    ],
)
def test_non_authorized_decisions_cannot_run(
    tmp_path: Path, status: ExperimentAuthorizationDecision
) -> None:
    context = authorized_context(tmp_path)
    (
        declaration,
        repository,
        admission,
        report,
        eligibility_policy,
        eligibility,
        spec,
        policy,
        auth,
    ) = context
    altered = replace(
        auth.record,
        status=status,
        findings=("not_authorized",),
        lifecycle=ExperimentLifecycleBoundary.NOT_AUTHORIZED,
    )
    request = run_request(altered, spec, policy, eligibility)
    with pytest.raises(InvalidExperimentAuthorization):
        run_authorized_experiment(
            request,
            authorization=altered,
            specification=spec,
            policy=policy,
            eligibility=eligibility,
            eligibility_policy=eligibility_policy,
            admission=admission,
            declaration=declaration,
            report=report,
            engine_contract=market_statistics_replay_contract(),
            repository=repository,
        )


@pytest.mark.parametrize(
    "field",
    ["authorization_ref", "specification_ref", "policy_ref", "eligibility_ref"],
)
def test_stale_or_tampered_request_reference_fails_closed(tmp_path: Path, field: str) -> None:
    context = authorized_context(tmp_path)
    (
        declaration,
        repository,
        admission,
        report,
        eligibility_policy,
        eligibility,
        spec,
        policy,
        auth,
    ) = context
    request = run_request(auth.record, spec, policy, eligibility)
    original = getattr(request, field)
    stale = TraceabilityRef(
        original.object_id,
        original.version,
        "sha256:" + "9" * 64,
    )
    if field == "authorization_ref":
        changed = replace(request, authorization_ref=stale)
    elif field == "specification_ref":
        changed = replace(request, specification_ref=stale)
    elif field == "policy_ref":
        changed = replace(request, policy_ref=stale)
    else:
        changed = replace(request, eligibility_ref=stale)
    with pytest.raises(ExperimentRunnerLineageMismatch):
        run_authorized_experiment(
            changed,
            authorization=auth.record,
            specification=spec,
            policy=policy,
            eligibility=eligibility,
            eligibility_policy=eligibility_policy,
            admission=admission,
            declaration=declaration,
            report=report,
            engine_contract=market_statistics_replay_contract(),
            repository=repository,
        )


def test_same_engine_id_with_wrong_fingerprint_fails(tmp_path: Path) -> None:
    context = authorized_context(tmp_path)
    (
        declaration,
        repository,
        admission,
        report,
        eligibility_policy,
        eligibility,
        spec,
        policy,
        auth,
    ) = context
    request = run_request(auth.record, spec, policy, eligibility)
    changed = replace(
        request,
        engine_contract_ref=TraceabilityRef(
            request.engine_contract_ref.object_id,
            request.engine_contract_ref.version,
            "sha256:" + "8" * 64,
        ),
    )
    with pytest.raises(ExperimentRunnerLineageMismatch):
        run_authorized_experiment(
            changed,
            authorization=auth.record,
            specification=spec,
            policy=policy,
            eligibility=eligibility,
            eligibility_policy=eligibility_policy,
            admission=admission,
            declaration=declaration,
            report=report,
            engine_contract=market_statistics_replay_contract(),
            repository=repository,
        )


def test_unsupported_family_and_metric_fail_closed(tmp_path: Path) -> None:
    context = authorized_context(tmp_path)
    spec = context[6]
    with pytest.raises(UnsupportedExperimentRunner):
        _require_market_statistics_scope(
            replace(spec, family=ExperimentFamily.STRATEGY_BACKTEST),
            market_statistics_replay_contract(),
        )
    with pytest.raises(UnsupportedExperimentRunner):
        _require_market_statistics_scope(
            replace(spec, requested_metrics=("sharpe",)),
            market_statistics_replay_contract(),
        )


def test_replay_rejects_out_of_order_duplicate_missing_and_unavailable_bars(tmp_path: Path) -> None:
    context = authorized_context(tmp_path)
    report, spec = context[3], context[6]
    with pytest.raises(ReplayOrderingFailure):
        _select_replay_bars(
            spec, replace(report, normalized_bars=tuple(reversed(report.normalized_bars)))
        )
    with pytest.raises(ReplayOrderingFailure):
        _select_replay_bars(
            spec,
            replace(
                report,
                normalized_bars=(report.normalized_bars[0],) * 2 + report.normalized_bars[1:],
            ),
        )
    with pytest.raises(MissingRequiredBars):
        _select_replay_bars(
            spec,
            replace(report, normalized_bars=(report.normalized_bars[0], report.normalized_bars[2])),
        )
    with pytest.raises(ExperimentTimeWindowMismatch):
        _select_replay_bars(
            spec,
            replace(
                report,
                normalized_bars=(
                    *report.normalized_bars[:-1],
                    replace(
                        report.normalized_bars[-1],
                        availability_time=spec.knowledge_cutoff + timedelta(seconds=1),
                        ingestion_time=spec.knowledge_cutoff + timedelta(seconds=1),
                    ),
                ),
            ),
        )


def test_future_bar_is_inaccessible_before_its_availability_event(tmp_path: Path) -> None:
    report = authorized_context(tmp_path)[3]
    first = report.normalized_bars[0]
    before_first_availability = first.availability_time - timedelta(microseconds=1)
    assert available_bars_at(report.normalized_bars, before_first_availability) == ()
    assert available_bars_at(report.normalized_bars, first.availability_time) == (first,)


@pytest.mark.parametrize(
    ("start", "end"),
    [
        (datetime(2025, 1, 31, 23, tzinfo=UTC), datetime(2025, 2, 1, 3, tzinfo=UTC)),
        (datetime(2025, 2, 1, 0, 30, tzinfo=UTC), datetime(2025, 2, 1, 3, tzinfo=UTC)),
        (datetime(2025, 2, 1, tzinfo=UTC), datetime(2025, 2, 1, 2, 30, tzinfo=UTC)),
    ],
)
def test_runner_rejects_outside_or_unaligned_windows(
    tmp_path: Path, start: datetime, end: datetime
) -> None:
    context = authorized_context(tmp_path)
    report, eligibility = context[3], context[5]
    altered = specification(eligibility, start=start, end=end)
    with pytest.raises((ExperimentTimeWindowMismatch, MissingRequiredBars)):
        _select_replay_bars(altered, report)


def test_runner_reverifies_complete_eligibility_lineage(tmp_path: Path) -> None:
    context = authorized_context(tmp_path)
    (
        declaration,
        repository,
        admission,
        report,
        eligibility_policy,
        eligibility,
        spec,
        policy,
        auth,
    ) = context
    changed_report = replace(report, normalized_bars=report.normalized_bars[:-1])
    with pytest.raises(ExperimentRunnerLineageMismatch):
        run_authorized_experiment(
            run_request(auth.record, spec, policy, eligibility),
            authorization=auth.record,
            specification=spec,
            policy=policy,
            eligibility=eligibility,
            eligibility_policy=eligibility_policy,
            admission=admission,
            declaration=declaration,
            report=changed_report,
            engine_contract=market_statistics_replay_contract(),
            repository=repository,
        )


def test_fabricated_authorized_record_is_reconstructed_fail_closed(tmp_path: Path) -> None:
    context = authorized_context(tmp_path)
    (
        declaration,
        repository,
        admission,
        report,
        eligibility_policy,
        eligibility,
        spec,
        policy,
        auth,
    ) = context
    fabricated = replace(auth.record, decision_time=spec.knowledge_cutoff - timedelta(seconds=1))
    with pytest.raises(ExperimentRunnerLineageMismatch):
        run_authorized_experiment(
            run_request(fabricated, spec, policy, eligibility),
            authorization=fabricated,
            specification=spec,
            policy=policy,
            eligibility=eligibility,
            eligibility_policy=eligibility_policy,
            admission=admission,
            declaration=declaration,
            report=report,
            engine_contract=market_statistics_replay_contract(),
            repository=repository,
        )


@pytest.mark.parametrize(
    "field", ["normalized_manifest_ref", "normalized_lock_ref", "configuration_fingerprint"]
)
def test_changed_authorization_dataset_or_configuration_binding_fails(
    tmp_path: Path, field: str
) -> None:
    context = authorized_context(tmp_path)
    (
        declaration,
        repository,
        admission,
        report,
        eligibility_policy,
        eligibility,
        spec,
        policy,
        auth,
    ) = context
    if field == "configuration_fingerprint":
        altered = replace(auth.record, configuration_fingerprint="sha256:" + "9" * 64)
    else:
        reference = getattr(auth.record, field)
        stale = TraceabilityRef(reference.object_id, reference.version, "sha256:" + "9" * 64)
        if field == "normalized_manifest_ref":
            altered = replace(auth.record, normalized_manifest_ref=stale)
        else:
            altered = replace(auth.record, normalized_lock_ref=stale)
    with pytest.raises(ExperimentRunnerLineageMismatch):
        run_authorized_experiment(
            run_request(altered, spec, policy, eligibility),
            authorization=altered,
            specification=spec,
            policy=policy,
            eligibility=eligibility,
            eligibility_policy=eligibility_policy,
            admission=admission,
            declaration=declaration,
            report=report,
            engine_contract=market_statistics_replay_contract(),
            repository=repository,
        )


def test_completion_cannot_precede_knowledge_cutoff(tmp_path: Path) -> None:
    context = authorized_context(tmp_path)
    (
        declaration,
        repository,
        admission,
        report,
        eligibility_policy,
        eligibility,
        spec,
        policy,
        auth,
    ) = context
    request = run_request(
        auth.record,
        spec,
        policy,
        eligibility,
        completed_at=spec.knowledge_cutoff - timedelta(seconds=1),
    )
    with pytest.raises(ExperimentTimeWindowMismatch):
        run_authorized_experiment(
            request,
            authorization=auth.record,
            specification=spec,
            policy=policy,
            eligibility=eligibility,
            eligibility_policy=eligibility_policy,
            admission=admission,
            declaration=declaration,
            report=report,
            engine_contract=market_statistics_replay_contract(),
            repository=repository,
        )


def test_result_lineage_detects_changed_result_and_run_inputs(tmp_path: Path) -> None:
    context, request, result = execute(tmp_path)
    _, _, _, report, _, eligibility, spec, policy, auth = context
    engine = market_statistics_replay_contract()
    altered_artifact = replace(result.artifact, close_max="999")
    with pytest.raises(ExperimentResultLineageMismatch):
        verify_experiment_result_lineage(
            record=replace(
                result.record,
                result_ref=exact(
                    altered_artifact,
                    altered_artifact.artifact_id,
                    altered_artifact.version,
                ),
            ),
            artifact=altered_artifact,
            request=request,
            authorization=auth.record,
            specification=spec,
            policy=policy,
            eligibility=eligibility,
            engine_contract=engine,
            report=report,
        )
    with pytest.raises(ExperimentResultLineageMismatch):
        verify_experiment_result_lineage(
            record=replace(result.record, run_input_fingerprint="sha256:" + "1" * 64),
            artifact=result.artifact,
            request=request,
            authorization=auth.record,
            specification=spec,
            policy=policy,
            eligibility=eligibility,
            engine_contract=engine,
            report=report,
        )


@pytest.mark.parametrize("kind", ["run", "result"])
def test_corrupted_persisted_run_artifacts_fail_integrity(tmp_path: Path, kind: str) -> None:
    context, _, result = execute(tmp_path)
    repository = context[1]
    record = result.record if kind == "run" else result.artifact
    expected_type = ExperimentRunRecord if kind == "run" else ExperimentResultArtifact
    key = repository_key(record)
    path = repository.path_for(key)
    path.write_bytes(path.read_bytes().replace(b'"PLANNED_CLOSED"', b'"OPEN__________"'))
    with pytest.raises(RepositoryIntegrityFailure):
        repository.load(key, expected_type)


def test_wrong_stored_type_and_contract_version_fail_closed(tmp_path: Path) -> None:
    context, _, result = execute(tmp_path)
    repository = context[1]
    with pytest.raises(RepositoryTypeMismatch):
        repository.load(repository_key(result.record), ExperimentResultArtifact)
    data = json.loads(encode(result.record))
    data["payload"]["contract_version"] = 2
    with pytest.raises(ValueError):
        decode(
            json.dumps(data, separators=(",", ":"), sort_keys=True).encode(), ExperimentRunRecord
        )


def test_replay_contract_and_result_numeric_values_are_strict(tmp_path: Path) -> None:
    contract = market_statistics_replay_contract()
    assert decode(encode(contract), ExperimentReplayContract) == contract
    _, _, result = execute(tmp_path)
    with pytest.raises(ValueError):
        replace(result.artifact, simple_returns=("NaN", "0"))
    with pytest.raises(ValueError):
        replace(result.artifact, close_max="")


def test_zero_first_close_fails_with_typed_return_domain_error(tmp_path: Path) -> None:
    context = signed_authorized_context(tmp_path, ("0", "100", "101"), suffix="zero-first")
    repository = context[1]
    with pytest.raises(
        UnsupportedReturnDomain,
        match="simple return is undefined when previous close is zero",
    ):
        execute_context(context)
    assert not (repository.root / "objects" / "experiment-result-artifact").exists()
    assert not (repository.root / "objects" / "experiment-run-record").exists()


def test_zero_later_in_series_fails_when_it_becomes_denominator(tmp_path: Path) -> None:
    context = signed_authorized_context(tmp_path, ("100", "0", "101"), suffix="zero-later")
    repository = context[1]
    with pytest.raises(
        UnsupportedReturnDomain,
        match="simple return is undefined when previous close is zero",
    ):
        execute_context(context)
    assert not (repository.root / "objects" / "experiment-result-artifact").exists()
    assert not (repository.root / "objects" / "experiment-run-record").exists()


def test_negative_previous_close_remains_supported_for_signed_domain(tmp_path: Path) -> None:
    context = signed_authorized_context(tmp_path, ("-100", "-50", "-25"), suffix="negative")
    _, result = execute_context(context)
    assert result.artifact.simple_returns == ("-0.5", "-0.5")
    assert result.record.status is ExperimentRunStatus.COMPLETED


def test_no_random_uuid_or_current_time_affects_identity(tmp_path: Path) -> None:
    _, request, result = execute(tmp_path)
    assert result.record.run_id == request.run_id
    assert result.record.completed_at == COMPLETED_AT
    assert result.artifact.last_knowledge_time == datetime(2025, 2, 1, 3, 0, 5, tzinfo=UTC)


def test_runner_has_no_network_plugin_subprocess_or_market_execution_entrypoint() -> None:
    tree = ast.parse(inspect.getsource(runner_module))
    imported_roots = {
        node.names[0].name.split(".")[0] for node in ast.walk(tree) if isinstance(node, ast.Import)
    } | {
        (node.module or "").split(".")[0]
        for node in ast.walk(tree)
        if isinstance(node, ast.ImportFrom)
    }
    assert not imported_roots.intersection(
        {"aiohttp", "ccxt", "httpx", "importlib", "requests", "socket", "subprocess", "urllib"}
    )
    call_names = {
        node.func.id
        for node in ast.walk(tree)
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
    }
    assert not call_names.intersection({"eval", "exec"})
    exported_functions = {
        name.lower() for name, value in inspect.getmembers(runner_module, inspect.isfunction)
    }
    assert not exported_functions.intersection(
        {"buy", "sell", "place_order", "route_order", "open_position", "deploy"}
    )
