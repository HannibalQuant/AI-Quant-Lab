"""Sprint 15 controlled robustness-validation tests."""

from __future__ import annotations

import ast
import copy
import inspect
import json
from dataclasses import replace
from datetime import timedelta
from decimal import ROUND_HALF_EVEN, Context, Decimal, localcontext
from pathlib import Path
from typing import Any

import pytest
from test_scientific_validation import (
    ValidationBundle,
    _context,
    _multi_trade_csv,
    _run,
    exact,
    validation_plan,
)
from test_strategy_backtest import authorized_context

from ai_quant_lab import EXE_01
from ai_quant_lab.core import robustness_validation as robustness_module
from ai_quant_lab.core.codec import decode, encode
from ai_quant_lab.core.dataset_store import (
    RepositoryIntegrityFailure,
    RepositoryTypeMismatch,
    RepositoryWriteStatus,
    repository_key,
)
from ai_quant_lab.core.experiment_contracts import CostSemantics
from ai_quant_lab.core.integrity import fingerprint_record
from ai_quant_lab.core.model import (
    ArtifactId,
    AuthorityBindingId,
    ExecutionState,
    ObjectVersion,
    ProvenanceId,
    RunId,
    TraceabilityRef,
)
from ai_quant_lab.core.research_eligibility_contracts import DeploymentAuthorizationStatus
from ai_quant_lab.core.robustness_validation import (
    RobustnessAuthorityInvalid,
    RobustnessInputInvalid,
    RobustnessLineageMismatch,
    RobustnessValidationExecutionResult,
    _compound_returns,
    run_robustness_validation,
    verify_robustness_validation_lineage,
)
from ai_quant_lab.core.robustness_validation_contracts import (
    MonteCarloPolicy,
    PerturbationPolicy,
    RobustnessDecision,
    RobustnessHoldoutEvidence,
    RobustnessMethod,
    RobustnessReasonCode,
    RobustnessValidationContractError,
    RobustnessValidationPlan,
    RobustnessValidationRequest,
    RobustnessValidationResult,
    RobustnessValidationRunRecord,
    TemporalPartitionRole,
    WalkForwardPolicy,
)
from ai_quant_lab.core.scientific_validation_contracts import ScientificValidationDecision
from ai_quant_lab.core.strategy_backtest import strategy_backtest_replay_contract

V1 = ObjectVersion(1)
ROBUSTNESS_AUTHORITY_REF = TraceabilityRef(
    AuthorityBindingId("independent-robustness-validator"), V1, "sha256:" + "c" * 64
)
ROBUSTNESS_PROVENANCE_REF = TraceabilityRef(
    ProvenanceId("robustness-validation-provenance"), V1, "sha256:" + "d" * 64
)
GOLDEN = Path(__file__).parent / "golden" / "robustness_validation_v1.json"


type RobustnessBundle = tuple[
    ValidationBundle,
    RobustnessValidationRequest,
    RobustnessValidationPlan,
    RobustnessValidationExecutionResult,
]


def robustness_plan(
    source_ref: TraceabilityRef,
    *,
    seed: int = 97,
    minimum_windows: int = 3,
    minimum_trades: int = 1,
) -> RobustnessValidationPlan:
    return RobustnessValidationPlan(
        ArtifactId("controlled-robustness-plan-v1"),
        V1,
        source_ref,
        (
            RobustnessMethod.COST_PERTURBATION,
            RobustnessMethod.ROLLING_WALK_FORWARD,
            RobustnessMethod.TRADE_BOOTSTRAP_WITH_REPLACEMENT,
        ),
        WalkForwardPolicy.ROLLING_FIXED_STRATEGY,
        5,
        5,
        5,
        minimum_windows,
        minimum_trades,
        "1",
        "0.25",
        "0",
        "-0.0001",
        MonteCarloPolicy.TRADE_BOOTSTRAP_WITH_REPLACEMENT,
        200,
        seed,
        "0.05",
        "0.95",
        PerturbationPolicy.COMMISSION_MULTIPLIER,
        ("1", "2", "3", "4"),
        "0",
        "-0.05",
        ROBUSTNESS_AUTHORITY_REF,
        ROBUSTNESS_PROVENANCE_REF,
        V1,
    )


def _request(
    plan: RobustnessValidationPlan, bundle: ValidationBundle
) -> RobustnessValidationRequest:
    _, _, backtest, scientific, _ = bundle
    return RobustnessValidationRequest(
        RunId("controlled-robustness-run"),
        ArtifactId("controlled-robustness-result"),
        exact(plan, plan.robustness_plan_id, plan.version),
        exact(
            scientific.result,
            scientific.result.validation_result_id,
            scientific.result.version,
        ),
        exact(scientific.record, scientific.record.validation_run_id, scientific.record.version),
        exact(backtest.artifact, backtest.artifact.artifact_id, backtest.artifact.version),
        exact(backtest.record, backtest.record.run_id, backtest.record.version),
        ROBUSTNESS_AUTHORITY_REF,
        ROBUSTNESS_PROVENANCE_REF,
    )


def _execute(bundle: ValidationBundle, plan: RobustnessValidationPlan) -> RobustnessBundle:
    scientific_request, backtest_request, backtest, scientific, context = bundle
    request = _request(plan, bundle)
    result = run_robustness_validation(
        request,
        plan=plan,
        scientific_result=scientific.result,
        validation_record=scientific.record,
        scientific_request=scientific_request,
        validation_plan=validation_plan(),
        backtest_artifact=backtest.artifact,
        backtest_record=backtest.record,
        backtest_request=backtest_request,
        authorization=context[9].record,
        specification=context[7],
        policy=context[8],
        eligibility=context[5],
        eligibility_policy=context[4],
        admission=context[2],
        declaration=context[0],
        engine_contract=strategy_backtest_replay_contract(),
        strategy=context[6],
        instrument=context[10],
        report=context[3],
        repository=context[1],
    )
    return bundle, request, plan, result


def _verify(
    bundle: RobustnessBundle,
    *,
    result: Any | None = None,
    record: Any | None = None,
    scientific_result: Any | None = None,
    backtest_artifact: Any | None = None,
    strategy: Any | None = None,
    instrument: Any | None = None,
) -> None:
    validation, request, plan, robustness = bundle
    scientific_request, backtest_request, backtest, scientific, context = validation
    verify_robustness_validation_lineage(
        record=robustness.record if record is None else record,
        result=robustness.result if result is None else result,
        request=request,
        plan=plan,
        scientific_result=scientific.result if scientific_result is None else scientific_result,
        validation_record=scientific.record,
        scientific_request=scientific_request,
        validation_plan=validation_plan(),
        backtest_artifact=(backtest.artifact if backtest_artifact is None else backtest_artifact),
        backtest_record=backtest.record,
        backtest_request=backtest_request,
        authorization=context[9].record,
        specification=context[7],
        policy=context[8],
        eligibility=context[5],
        eligibility_policy=context[4],
        admission=context[2],
        declaration=context[0],
        engine_contract=strategy_backtest_replay_contract(),
        strategy=context[6] if strategy is None else strategy,
        instrument=context[10] if instrument is None else instrument,
        report=context[3],
    )


def _unsafe[T](record: T, **changes: object) -> T:
    clone = copy.copy(record)
    for field, value in changes.items():
        object.__setattr__(clone, field, value)
    return clone


@pytest.fixture
def positive_bundle(tmp_path: Path) -> RobustnessBundle:
    validation = _run(
        _context(tmp_path, "robustness-positive", ((100, 120),) * 4), validation_plan()
    )
    source_ref = exact(
        validation[3].result,
        validation[3].result.validation_result_id,
        validation[3].result.version,
    )
    return _execute(validation, robustness_plan(source_ref))


def test_plan_is_explicit_bounded_immutable_and_authority_bound(
    positive_bundle: RobustnessBundle,
) -> None:
    _, _, plan, _ = positive_bundle
    assert plan.target_methods == tuple(sorted(RobustnessMethod, key=lambda item: item.value))
    assert plan.robustness_authority_ref == ROBUSTNESS_AUTHORITY_REF
    with pytest.raises(RobustnessValidationContractError):
        replace(plan, step_bars=plan.test_bars - 1)
    with pytest.raises(RobustnessValidationContractError):
        replace(plan, monte_carlo_iterations=99)
    with pytest.raises(RobustnessValidationContractError):
        replace(plan, target_methods=(RobustnessMethod.ROLLING_WALK_FORWARD,))
    with pytest.raises(RobustnessValidationContractError):
        replace(plan, commission_multipliers=("1", "0.5"))


def test_robust_positive_case_passes_without_new_authority(
    positive_bundle: RobustnessBundle,
) -> None:
    validation, _, _, robustness = positive_bundle
    assert validation[3].result.decision is ScientificValidationDecision.PASS
    assert robustness.result.decision is RobustnessDecision.PASS
    assert robustness.result.walk_forward.decision is RobustnessDecision.PASS
    assert robustness.result.monte_carlo.decision is RobustnessDecision.PASS
    assert robustness.result.cost_perturbation.decision is RobustnessDecision.PASS
    assert robustness.result.holdout_evidence is RobustnessHoldoutEvidence.NOT_ESTABLISHED
    assert (
        robustness.result.deployment_authorization is DeploymentAuthorizationStatus.NOT_AUTHORIZED
    )
    assert robustness.result.execution_state is ExecutionState.PLANNED_CLOSED
    assert EXE_01.state is ExecutionState.PLANNED_CLOSED


def test_walk_forward_partitions_are_exact_nonoverlapping_and_deterministic(
    positive_bundle: RobustnessBundle,
) -> None:
    summary = positive_bundle[3].result.walk_forward
    assert summary.valid_window_count == 3
    previous_test_refs: set[TraceabilityRef] = set()
    for item in summary.slices:
        assert item.train_partition.role is TemporalPartitionRole.TRAIN
        assert item.test_partition.role is TemporalPartitionRole.TEST
        assert item.train_partition.end_index == item.test_partition.start_index
        assert not set(item.train_partition.bar_refs) & set(item.test_partition.bar_refs)
        assert not previous_test_refs & set(item.test_partition.bar_refs)
        previous_test_refs.update(item.test_partition.bar_refs)
        assert item.trade_count == 1


def test_monte_carlo_is_trade_bootstrap_only_and_seed_deterministic(
    positive_bundle: RobustnessBundle,
    tmp_path: Path,
) -> None:
    validation, _, plan, first = positive_bundle
    second = _execute(validation, plan)[3]
    assert first.result.monte_carlo == second.result.monte_carlo
    assert first.record.robustness_input_fingerprint == second.record.robustness_input_fingerprint
    assert first.result.monte_carlo.iterations == 200
    assert first.result.monte_carlo.policy is MonteCarloPolicy.TRADE_BOOTSTRAP_WITH_REPLACEMENT

    changed_validation = _run(
        _context(tmp_path, "robustness-seed", ((100, 120),) * 4), validation_plan()
    )
    source_ref = exact(
        changed_validation[3].result,
        changed_validation[3].result.validation_result_id,
        changed_validation[3].result.version,
    )
    changed = _execute(changed_validation, robustness_plan(source_ref, seed=98))[3]
    assert first.record.robustness_input_fingerprint != changed.record.robustness_input_fingerprint


@pytest.mark.parametrize(
    ("name", "outcomes", "expected"),
    (
        ("positive", ((100, 120),) * 4, RobustnessDecision.PASS),
        ("negative", ((120, 100),) * 4, RobustnessDecision.FAIL),
        (
            "mixed",
            ((100, 120), (120, 100), (100, 120), (120, 100)),
            RobustnessDecision.INCONCLUSIVE,
        ),
    ),
)
def test_monte_carlo_decision_cases_are_explicit(
    tmp_path: Path,
    name: str,
    outcomes: tuple[tuple[int, int], ...],
    expected: RobustnessDecision,
) -> None:
    validation = _run(_context(tmp_path, f"robustness-mc-{name}", outcomes), validation_plan())
    source_ref = exact(
        validation[3].result,
        validation[3].result.validation_result_id,
        validation[3].result.version,
    )
    result = _execute(validation, robustness_plan(source_ref))[3].result
    assert result.monte_carlo.decision is expected
    assert Decimal(result.monte_carlo.lower_terminal_return) <= Decimal(
        result.monte_carlo.upper_terminal_return
    )


def test_cost_perturbations_are_declared_and_monotonic(
    positive_bundle: RobustnessBundle,
) -> None:
    scenarios = positive_bundle[3].result.cost_perturbation.scenarios
    assert tuple(item.commission_multiplier for item in scenarios) == ("1", "2", "3", "4")
    assert all(item.total_return is not None for item in scenarios)
    returns = tuple(Decimal(item.total_return or "0") for item in scenarios)
    assert returns == tuple(sorted(returns, reverse=True))
    assert len({item.trade_count for item in scenarios}) == 1
    source = positive_bundle[0][2].artifact
    base = scenarios[0]
    assert base.total_return == source.total_return
    assert base.net_pnl == source.net_pnl
    assert base.max_drawdown == source.max_drawdown
    assert base.trade_count == source.trade_count
    assert base.backtest_result_ref is not None
    assert len({item.scenario_id for item in scenarios}) == len(scenarios)


def test_cost_perturbation_is_true_deterministic_replay(
    positive_bundle: RobustnessBundle,
) -> None:
    validation, _, plan, first = positive_bundle
    second = _execute(validation, plan)[3]
    first_scenarios = first.result.cost_perturbation.scenarios
    assert first_scenarios == second.result.cost_perturbation.scenarios
    assert first_scenarios[1].backtest_result_ref != first_scenarios[0].backtest_result_ref
    assert first_scenarios[1].derived_commission_bps == 20
    assert Decimal(first_scenarios[1].total_return or "0") < Decimal(
        first_scenarios[0].total_return or "0"
    )
    assert first.result.strategy_ref == validation[2].artifact.strategy_ref
    assert first.result.normalized_manifest_ref == validation[2].artifact.normalized_manifest_ref
    assert first.result.normalized_lock_ref == validation[2].artifact.normalized_lock_ref


def test_cost_perturbation_insufficient_cash_fails_without_impossible_fill(
    tmp_path: Path,
) -> None:
    outcomes = ((100, 120),) * 4
    hours = len(outcomes) * 5
    context = authorized_context(
        tmp_path,
        suffix="robustness-insufficient-cash",
        csv_text=_multi_trade_csv(outcomes),
        spec_mutator=lambda spec: replace(
            spec,
            observation_end=spec.observation_start + timedelta(hours=hours),
            capital_notional_minor=10_010,
        ),
    )
    validation = _run(context, validation_plan())
    source_ref = exact(
        validation[3].result,
        validation[3].result.validation_result_id,
        validation[3].result.version,
    )
    result = _execute(validation, robustness_plan(source_ref))[3].result
    base, doubled, *_ = result.cost_perturbation.scenarios
    assert base.backtest_result_ref is not None
    assert base.trade_count == validation[2].artifact.trade_count
    assert doubled.derived_commission_bps == 20
    assert doubled.backtest_result_ref is None
    assert doubled.total_return is None
    assert doubled.net_pnl is None
    assert doubled.max_drawdown is None
    assert doubled.trade_count is None
    assert doubled.decision is RobustnessDecision.FAIL
    assert doubled.reason_codes == (RobustnessReasonCode.COST_PERTURBATION_EXECUTION_FAILED,)
    assert result.decision is RobustnessDecision.FAIL
    assert RobustnessReasonCode.COST_PERTURBATION_EXECUTION_FAILED in result.reason_codes


def test_declared_zero_commission_remains_zero_under_all_multipliers(
    tmp_path: Path,
) -> None:
    outcomes = ((100, 120),) * 4
    hours = len(outcomes) * 5
    context = authorized_context(
        tmp_path,
        suffix="robustness-zero-commission",
        csv_text=_multi_trade_csv(outcomes),
        spec_mutator=lambda spec: replace(
            spec,
            observation_end=spec.observation_start + timedelta(hours=hours),
            commission_semantics=CostSemantics.DECLARED_ZERO,
            commission_bps=0,
        ),
    )
    validation = _run(context, validation_plan())
    source_ref = exact(
        validation[3].result,
        validation[3].result.validation_result_id,
        validation[3].result.version,
    )
    scenarios = _execute(validation, robustness_plan(source_ref))[
        3
    ].result.cost_perturbation.scenarios
    assert {item.derived_commission_bps for item in scenarios} == {0}
    assert {item.total_return for item in scenarios} == {validation[2].artifact.total_return}
    assert all(item.backtest_result_ref is not None for item in scenarios)


@pytest.mark.parametrize(
    ("returns", "expected"),
    (
        (("0.10", "0.10"), "0.21"),
        (("0.10", "-0.10"), "-0.01"),
    ),
)
def test_walk_forward_aggregate_return_is_compounded(
    returns: tuple[str, ...], expected: str
) -> None:
    with localcontext(Context(prec=34, rounding=ROUND_HALF_EVEN)):
        actual = _compound_returns(tuple(Decimal(value) for value in returns))
    assert actual == Decimal(expected)


def test_walk_forward_compounding_rejects_equity_below_zero() -> None:
    with pytest.raises(
        RobustnessInputInvalid,
        match="walk-forward return cannot imply equity below zero",
    ):
        _compound_returns((Decimal("-1.01"),))


def test_cost_perturbation_uses_declared_fail_threshold(
    positive_bundle: RobustnessBundle,
) -> None:
    validation, _, original, _ = positive_bundle
    plan = replace(
        original,
        perturbation_pass_return_floor="0.2",
        perturbation_fail_return_threshold="0.1",
    )
    changed = _execute(validation, plan)[3].result
    assert changed.cost_perturbation.decision is RobustnessDecision.FAIL
    assert changed.decision is RobustnessDecision.FAIL


def test_insufficient_windows_is_inconclusive(tmp_path: Path) -> None:
    validation = _run(
        _context(tmp_path, "robustness-insufficient", ((100, 120),) * 4), validation_plan()
    )
    source_ref = exact(
        validation[3].result,
        validation[3].result.validation_result_id,
        validation[3].result.version,
    )
    robustness = _execute(validation, robustness_plan(source_ref, minimum_windows=4))[3]
    assert robustness.result.decision is RobustnessDecision.INCONCLUSIVE
    assert RobustnessReasonCode.INSUFFICIENT_WINDOWS in robustness.result.reason_codes


def test_fragile_walk_forward_case_fails(tmp_path: Path) -> None:
    validation = _run(
        _context(
            tmp_path,
            "robustness-fragile",
            ((100, 200), (100, 200), (100, 200), (120, 100)),
        ),
        validation_plan(),
    )
    assert validation[3].result.decision is ScientificValidationDecision.PASS
    source_ref = exact(
        validation[3].result,
        validation[3].result.validation_result_id,
        validation[3].result.version,
    )
    robustness = _execute(validation, robustness_plan(source_ref))[3]
    assert robustness.result.walk_forward.decision is RobustnessDecision.FAIL
    assert robustness.result.decision is RobustnessDecision.FAIL


def test_source_scientific_validation_and_backtest_are_reverified(
    positive_bundle: RobustnessBundle,
) -> None:
    validation, request, plan, _ = positive_bundle
    scientific_request, backtest_request, backtest, scientific, context = validation
    tampered = _unsafe(backtest.artifact, total_return="0")
    changed_request = replace(
        request,
        backtest_result_ref=exact(tampered, tampered.artifact_id, tampered.version),
    )
    with pytest.raises(
        RobustnessInputInvalid,
        match="source scientific validation failed exact verification",
    ):
        run_robustness_validation(
            changed_request,
            plan=plan,
            scientific_result=scientific.result,
            validation_record=scientific.record,
            scientific_request=scientific_request,
            validation_plan=validation_plan(),
            backtest_artifact=tampered,
            backtest_record=backtest.record,
            backtest_request=backtest_request,
            authorization=context[9].record,
            specification=context[7],
            policy=context[8],
            eligibility=context[5],
            eligibility_policy=context[4],
            admission=context[2],
            declaration=context[0],
            engine_contract=strategy_backtest_replay_contract(),
            strategy=context[6],
            instrument=context[10],
            report=context[3],
            repository=context[1],
        )


def test_wrong_authority_fails_closed(positive_bundle: RobustnessBundle) -> None:
    validation, request, plan, _ = positive_bundle
    scientific_request, backtest_request, backtest, scientific, context = validation
    wrong = TraceabilityRef(AuthorityBindingId("wrong"), V1, "sha256:" + "e" * 64)
    with pytest.raises(RobustnessAuthorityInvalid):
        run_robustness_validation(
            replace(request, robustness_authority_ref=wrong),
            plan=plan,
            scientific_result=scientific.result,
            validation_record=scientific.record,
            scientific_request=scientific_request,
            validation_plan=validation_plan(),
            backtest_artifact=backtest.artifact,
            backtest_record=backtest.record,
            backtest_request=backtest_request,
            authorization=context[9].record,
            specification=context[7],
            policy=context[8],
            eligibility=context[5],
            eligibility_policy=context[4],
            admission=context[2],
            declaration=context[0],
            engine_contract=strategy_backtest_replay_contract(),
            strategy=context[6],
            instrument=context[10],
            report=context[3],
            repository=context[1],
        )


@pytest.mark.parametrize(
    ("field", "value"),
    (
        ("decision", RobustnessDecision.FAIL),
        ("reason_codes", (RobustnessReasonCode.WALK_FORWARD_FAILED,)),
        ("robustness_plan_ref", TraceabilityRef(ArtifactId("wrong"), V1, "sha256:" + "f" * 64)),
    ),
)
def test_result_tamper_fails_closed(
    positive_bundle: RobustnessBundle, field: str, value: object
) -> None:
    original = positive_bundle[3].result
    with pytest.raises(RobustnessLineageMismatch):
        _verify(positive_bundle, result=_unsafe(original, **{field: value}))


def test_partition_monte_carlo_and_perturbation_tamper_fail_closed(
    positive_bundle: RobustnessBundle,
) -> None:
    original = positive_bundle[3].result
    first_slice = original.walk_forward.slices[0]
    changed_partition = replace(
        first_slice.test_partition,
        bar_refs=tuple(reversed(first_slice.test_partition.bar_refs)),
    )
    changed_slice = replace(first_slice, test_partition=changed_partition)
    changed_walk = replace(
        original.walk_forward,
        slices=(changed_slice, *original.walk_forward.slices[1:]),
    )
    cases = (
        _unsafe(original, walk_forward=changed_walk),
        _unsafe(original, monte_carlo=replace(original.monte_carlo, seed=999)),
        _unsafe(
            original,
            cost_perturbation=replace(
                original.cost_perturbation,
                scenarios=(
                    replace(original.cost_perturbation.scenarios[0], total_return="0"),
                    *original.cost_perturbation.scenarios[1:],
                ),
            ),
        ),
    )
    for changed in cases:
        with pytest.raises(RobustnessLineageMismatch):
            _verify(positive_bundle, result=changed)


def test_source_refs_strategy_and_instrument_tamper_fail_closed(
    positive_bundle: RobustnessBundle,
) -> None:
    validation, _, _, robustness = positive_bundle
    context = validation[4]
    with pytest.raises(RobustnessLineageMismatch):
        _verify(
            positive_bundle,
            scientific_result=_unsafe(validation[3].result, estimate="0"),
        )
    with pytest.raises(RobustnessLineageMismatch):
        _verify(
            positive_bundle, backtest_artifact=_unsafe(validation[2].artifact, final_equity="0")
        )
    with pytest.raises(RobustnessInputInvalid):
        _verify(positive_bundle, strategy=replace(context[6], strategy_id=ArtifactId("wrong")))
    with pytest.raises(RobustnessInputInvalid):
        _verify(positive_bundle, instrument=replace(context[10], symbol="WRONG"))
    assert robustness.result.strategy_ref == validation[2].artifact.strategy_ref


def test_exact_persistence_roundtrip_idempotency_and_strict_codec(
    positive_bundle: RobustnessBundle,
) -> None:
    validation, _, plan, robustness = positive_bundle
    repository = validation[4][1]
    values: tuple[tuple[Any, type[Any]], ...] = (
        (plan, RobustnessValidationPlan),
        (robustness.result, RobustnessValidationResult),
        (robustness.record, RobustnessValidationRunRecord),
    )
    for value, expected_type in values:
        assert repository.load(repository_key(value), expected_type).record == value
        assert repository.store(value).status is RepositoryWriteStatus.ALREADY_PRESENT_IDENTICAL
        assert decode(encode(value), expected_type) == value
    payload = json.loads(encode(robustness.result))
    payload["payload"]["unexpected"] = True
    with pytest.raises(ValueError):
        decode(json.dumps(payload).encode(), RobustnessValidationResult)


def test_persistence_corruption_wrong_type_and_version_fail_closed(
    positive_bundle: RobustnessBundle,
) -> None:
    validation, _, _, robustness = positive_bundle
    repository = validation[4][1]
    key = repository_key(robustness.result)
    with pytest.raises(RepositoryTypeMismatch):
        repository.load(key, RobustnessValidationRunRecord)
    path = repository.path_for(key)
    path.write_bytes(path.read_bytes().replace(b'"PASS"', b'"FAIL"', 1))
    with pytest.raises(RepositoryIntegrityFailure):
        repository.load(key, RobustnessValidationResult)
    with pytest.raises(RobustnessValidationContractError):
        replace(robustness.result, version=ObjectVersion(2))


def test_deterministic_result_bytes_refs_and_fingerprints(
    positive_bundle: RobustnessBundle,
) -> None:
    validation, _, plan, first = positive_bundle
    second = _execute(validation, plan)[3]
    assert encode(first.result) == encode(second.result)
    assert encode(first.record) == encode(second.record)
    assert fingerprint_record(first.result) == fingerprint_record(second.result)
    assert first.result.walk_forward.slices == second.result.walk_forward.slices


def test_robustness_golden_is_pinned_and_read_only(
    positive_bundle: RobustnessBundle,
) -> None:
    validation, _, plan, robustness = positive_bundle
    expected = {
        "format": "robustness-validation-v1",
        "robustness_plan_fingerprint": fingerprint_record(plan),
        "source_scientific_result_fingerprint": fingerprint_record(validation[3].result),
        "robustness_input_fingerprint": robustness.record.robustness_input_fingerprint,
        "partition_count": robustness.result.walk_forward.valid_window_count,
        "aggregate_test_return": robustness.result.walk_forward.aggregate_test_return,
        "monte_carlo_seed": robustness.result.monte_carlo.seed,
        "monte_carlo_iterations": robustness.result.monte_carlo.iterations,
        "commission_multipliers": [
            item.commission_multiplier for item in robustness.result.cost_perturbation.scenarios
        ],
        "derived_commission_bps": [
            item.derived_commission_bps for item in robustness.result.cost_perturbation.scenarios
        ],
        "scenario_ids": [
            str(item.scenario_id) for item in robustness.result.cost_perturbation.scenarios
        ],
        "median_test_return": robustness.result.walk_forward.median_test_return,
        "monte_carlo_lower_return": robustness.result.monte_carlo.lower_terminal_return,
        "worst_perturbed_return": str(
            min(
                Decimal(item.total_return or "0")
                for item in robustness.result.cost_perturbation.scenarios
            )
        ),
        "decision": robustness.result.decision.value,
        "reason_codes": [item.value for item in robustness.result.reason_codes],
        "robustness_result_fingerprint": fingerprint_record(robustness.result),
    }
    assert json.loads(GOLDEN.read_text(encoding="utf-8")) == expected


def test_engine_contract_stays_closed_and_non_plugin() -> None:
    tree = ast.parse(inspect.getsource(robustness_module))
    imported_roots = {
        (node.module or "").split(".")[0]
        for node in ast.walk(tree)
        if isinstance(node, ast.ImportFrom)
    } | {
        alias.name.split(".")[0]
        for node in ast.walk(tree)
        if isinstance(node, ast.Import)
        for alias in node.names
    }
    assert not imported_roots.intersection(
        {
            "aiohttp",
            "ccxt",
            "httpx",
            "importlib",
            "optuna",
            "requests",
            "socket",
            "subprocess",
            "urllib",
        }
    )
    calls = {
        node.func.id
        for node in ast.walk(tree)
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
    }
    assert not calls.intersection({"eval", "exec"})
    assert EXE_01.state is ExecutionState.PLANNED_CLOSED
