"""Sprint 14 governed scientific-validation foundation tests."""

from __future__ import annotations

import copy
import json
from dataclasses import replace
from datetime import UTC, datetime, timedelta
from decimal import Decimal
from pathlib import Path
from typing import Any

import pytest
from test_real_csv_onboarding import HEADER
from test_strategy_backtest import BacktestContext, authorized_context, execute_context

from ai_quant_lab import EXE_01
from ai_quant_lab.core.codec import decode, encode
from ai_quant_lab.core.dataset_store import (
    RepositoryIntegrityFailure,
    RepositoryTypeMismatch,
    RepositoryWriteStatus,
    repository_key,
)
from ai_quant_lab.core.experiment_contracts import ExperimentFamily
from ai_quant_lab.core.integrity import fingerprint_record
from ai_quant_lab.core.model import (
    ArtifactId,
    AuthorityBindingId,
    ExecutionState,
    ObjectVersion,
    ProvenanceId,
    RunId,
    TraceabilityRef,
    ValidationId,
)
from ai_quant_lab.core.research_eligibility_contracts import DeploymentAuthorizationStatus
from ai_quant_lab.core.scientific_validation import (
    ScientificValidationExecutionResult,
    ValidationAuthorityInvalid,
    ValidationInputInvalid,
    ValidationLineageMismatch,
    run_scientific_validation,
    verify_scientific_validation_lineage,
)
from ai_quant_lab.core.scientific_validation_contracts import (
    AlternativeHypothesis,
    HoldoutPolicy,
    MultiplicityPolicy,
    NullHypothesis,
    OutOfSampleEvidenceStatus,
    ScientificValidationContractError,
    ScientificValidationDecision,
    ScientificValidationResult,
    UncertaintyMethod,
    ValidationMetric,
    ValidationPlan,
    ValidationReasonCode,
    ValidationRequest,
    ValidationRunRecord,
)
from ai_quant_lab.core.strategy_backtest import (
    StrategyBacktestResult,
    StrategyBacktestRunRequest,
    strategy_backtest_replay_contract,
)
from ai_quant_lab.core.strategy_backtest_contracts import SimulatedPositionState

V1 = ObjectVersion(1)
AUTHORITY_REF = TraceabilityRef(
    AuthorityBindingId("independent-scientific-validator"), V1, "sha256:" + "a" * 64
)
PROVENANCE_REF = TraceabilityRef(
    ProvenanceId("scientific-validation-provenance"), V1, "sha256:" + "b" * 64
)
COMPLETED_AT = datetime(2025, 2, 4, tzinfo=UTC)
GOLDEN = Path(__file__).parent / "golden" / "scientific_validation_v1.json"


type ValidationBundle = tuple[
    ValidationRequest,
    StrategyBacktestRunRequest,
    StrategyBacktestResult,
    ScientificValidationExecutionResult,
    BacktestContext,
]


def exact(record: Any, object_id: Any, version: ObjectVersion) -> TraceabilityRef:
    return TraceabilityRef(object_id, version, fingerprint_record(record))


def validation_plan(
    *,
    seed: int = 73,
    min_trades: int = 4,
    holdout: HoldoutPolicy = HoldoutPolicy.NONE_DECLARED,
    multiplicity: MultiplicityPolicy = MultiplicityPolicy.SINGLE_PREDECLARED_TEST,
) -> ValidationPlan:
    return ValidationPlan(
        ArtifactId("scientific-validation-plan-v1"),
        V1,
        ExperimentFamily.STRATEGY_BACKTEST,
        (
            ValidationMetric.GROSS_PNL,
            ValidationMetric.MAX_DRAWDOWN,
            ValidationMetric.NET_PNL,
            ValidationMetric.TOTAL_RETURN,
            ValidationMetric.TRADE_COUNT,
        ),
        ValidationMetric.TOTAL_RETURN,
        NullHypothesis.EXPECTED_TOTAL_RETURN_NONPOSITIVE,
        AlternativeHypothesis.EXPECTED_TOTAL_RETURN_POSITIVE,
        min_trades,
        min_trades,
        UncertaintyMethod.TRADE_RETURN_BOOTSTRAP,
        "0.95",
        200,
        seed,
        holdout,
        multiplicity,
        AUTHORITY_REF,
        PROVENANCE_REF,
        V1,
    )


def _multi_trade_csv(outcomes: tuple[tuple[int, int], ...]) -> str:
    start = datetime(2025, 2, 1, tzinfo=UTC)
    rows: list[str] = []
    for cycle, (buy_price, sell_price) in enumerate(outcomes):
        values = (
            (100, 101),
            (101, 102),
            (buy_price, buy_price - 1),
            (buy_price, buy_price - 1),
            (sell_price, sell_price - 1),
        )
        for offset, (open_price, close_price) in enumerate(values):
            index = cycle * 5 + offset
            bar_open = start + timedelta(hours=index)
            bar_close = bar_open + timedelta(hours=1)
            available = bar_close + timedelta(seconds=5)
            rows.append(
                f"{bar_open.isoformat(timespec='microseconds').replace('+00:00', 'Z')},"
                f"{bar_close.isoformat(timespec='microseconds').replace('+00:00', 'Z')},"
                f"{open_price},{max(open_price, close_price) + 1},"
                f"{min(open_price, close_price) - 1},{close_price},{10 + index},final,"
                f"{available.isoformat(timespec='microseconds').replace('+00:00', 'Z')}\n"
            )
    return HEADER + "".join(rows)


def _context(tmp_path: Path, name: str, outcomes: tuple[tuple[int, int], ...]) -> BacktestContext:
    hours = len(outcomes) * 5
    return authorized_context(
        tmp_path,
        suffix=name,
        csv_text=_multi_trade_csv(outcomes),
        spec_mutator=lambda spec: replace(
            spec, observation_end=spec.observation_start + timedelta(hours=hours)
        ),
    )


def _request(plan: ValidationPlan, backtest: StrategyBacktestResult) -> ValidationRequest:
    record = backtest.record
    artifact = backtest.artifact
    return ValidationRequest(
        RunId("scientific-validation-run"),
        ValidationId("scientific-validation-result"),
        exact(plan, plan.validation_plan_id, plan.version),
        exact(artifact, artifact.artifact_id, artifact.version),
        exact(record, record.run_id, record.version),
        AUTHORITY_REF,
        COMPLETED_AT,
        PROVENANCE_REF,
    )


def _run(context: BacktestContext, plan: ValidationPlan) -> ValidationBundle:
    backtest_request, backtest = execute_context(context)
    request = _request(plan, backtest)
    result = run_scientific_validation(
        request,
        plan=plan,
        backtest_record=backtest.record,
        backtest_artifact=backtest.artifact,
        backtest_request=backtest_request,
        authorization=context[9].record,
        specification=context[7],
        policy=context[8],
        eligibility=context[5],
        engine_contract=strategy_backtest_replay_contract(),
        strategy=context[6],
        instrument=context[10],
        report=context[3],
        repository=context[1],
    )
    return request, backtest_request, backtest, result, context


@pytest.fixture
def pass_bundle(tmp_path: Path) -> ValidationBundle:
    return _run(_context(tmp_path, "validation-pass", ((100, 120),) * 4), validation_plan())


def test_validation_plan_is_explicit_immutable_and_authority_bound() -> None:
    plan = validation_plan()
    assert plan.primary_metric is ValidationMetric.TOTAL_RETURN
    assert plan.validator_authority_ref == AUTHORITY_REF
    assert plan.min_trade_count == plan.min_sample_size == 4
    with pytest.raises(ScientificValidationContractError):
        replace(plan, confidence_level="1")
    with pytest.raises(ScientificValidationContractError):
        replace(plan, min_trade_count=0)
    with pytest.raises(ScientificValidationContractError):
        replace(plan, primary_metric=ValidationMetric.NET_PNL)
    with pytest.raises(ScientificValidationContractError):
        replace(plan, validator_authority_ref=True)  # type: ignore[arg-type]
    with pytest.raises(ScientificValidationContractError):
        replace(plan, uncertainty_method="UNKNOWN")  # type: ignore[arg-type]


def test_wrong_authority_and_exact_input_refs_fail_closed(
    pass_bundle: ValidationBundle,
) -> None:
    request, backtest_request, backtest, _, context = pass_bundle
    wrong_authority = TraceabilityRef(
        AuthorityBindingId("experiment-proposer"), V1, "sha256:" + "d" * 64
    )
    with pytest.raises(ValidationAuthorityInvalid):
        run_scientific_validation(
            replace(request, validator_authority_ref=wrong_authority),
            plan=validation_plan(),
            backtest_record=backtest.record,
            backtest_artifact=backtest.artifact,
            backtest_request=backtest_request,
            authorization=context[9].record,
            specification=context[7],
            policy=context[8],
            eligibility=context[5],
            engine_contract=strategy_backtest_replay_contract(),
            strategy=context[6],
            instrument=context[10],
            report=context[3],
            repository=context[1],
        )
    with pytest.raises(ValidationLineageMismatch):
        run_scientific_validation(
            replace(request, backtest_result_ref=request.validation_plan_ref),
            plan=validation_plan(),
            backtest_record=backtest.record,
            backtest_artifact=backtest.artifact,
            backtest_request=backtest_request,
            authorization=context[9].record,
            specification=context[7],
            policy=context[8],
            eligibility=context[5],
            engine_contract=strategy_backtest_replay_contract(),
            strategy=context[6],
            instrument=context[10],
            report=context[3],
            repository=context[1],
        )


def test_legacy_or_tampered_backtest_input_is_rejected(pass_bundle: ValidationBundle) -> None:
    request, backtest_request, backtest, _, context = pass_bundle
    legacy = _unsafe(backtest.artifact, version=ObjectVersion(1))
    with pytest.raises(ValidationInputInvalid):
        run_scientific_validation(
            replace(request, backtest_result_ref=exact(legacy, legacy.artifact_id, legacy.version)),
            plan=validation_plan(),
            backtest_record=backtest.record,
            backtest_artifact=legacy,
            backtest_request=backtest_request,
            authorization=context[9].record,
            specification=context[7],
            policy=context[8],
            eligibility=context[5],
            engine_contract=strategy_backtest_replay_contract(),
            strategy=context[6],
            instrument=context[10],
            report=context[3],
            repository=context[1],
        )


def test_positive_confidence_bound_passes_without_deployment(
    pass_bundle: ValidationBundle,
) -> None:
    _, _, _, validation, _ = pass_bundle
    result = validation.result
    assert result.decision is ScientificValidationDecision.PASS
    assert Decimal(result.lower_bound) > 0
    assert result.reason_codes == (ValidationReasonCode.PASSED_CONFIDENCE_BOUND,)
    assert result.deployment_authorization is DeploymentAuthorizationStatus.NOT_AUTHORIZED
    assert result.execution_state is ExecutionState.PLANNED_CLOSED
    assert result.out_of_sample_evidence is OutOfSampleEvidenceStatus.NOT_ESTABLISHED
    assert EXE_01.state is ExecutionState.PLANNED_CLOSED


def test_nonpositive_upper_bound_fails(tmp_path: Path) -> None:
    _, _, _, validation, _ = _run(
        _context(tmp_path, "validation-fail", ((120, 100),) * 4), validation_plan()
    )
    assert validation.result.decision is ScientificValidationDecision.FAIL
    assert Decimal(validation.result.upper_bound) <= 0
    assert validation.result.reason_codes == (ValidationReasonCode.FAILED_NONPOSITIVE_BOUND,)


def test_interval_crossing_zero_is_inconclusive(tmp_path: Path) -> None:
    outcomes = ((100, 120), (120, 100), (100, 120), (120, 100))
    _, _, _, validation, _ = _run(
        _context(tmp_path, "validation-cross", outcomes), validation_plan()
    )
    assert Decimal(validation.result.lower_bound) <= 0 < Decimal(validation.result.upper_bound)
    assert validation.result.decision is ScientificValidationDecision.INCONCLUSIVE
    assert ValidationReasonCode.INTERVAL_OVERLAPS_ZERO in validation.result.reason_codes


@pytest.mark.parametrize(
    ("plan", "reason"),
    (
        (validation_plan(min_trades=5), ValidationReasonCode.INSUFFICIENT_TRADES),
        (
            validation_plan(multiplicity=MultiplicityPolicy.UNKNOWN),
            ValidationReasonCode.MULTIPLICITY_UNKNOWN,
        ),
        (
            validation_plan(multiplicity=MultiplicityPolicy.MULTIPLE_TESTS_UNCORRECTED),
            ValidationReasonCode.MULTIPLICITY_UNSUPPORTED,
        ),
        (
            validation_plan(holdout=HoldoutPolicy.RESERVED_HOLDOUT),
            ValidationReasonCode.HOLDOUT_REQUIRED,
        ),
    ),
)
def test_governance_context_blocks_pass(
    tmp_path: Path, plan: ValidationPlan, reason: ValidationReasonCode
) -> None:
    _, _, _, validation, _ = _run(
        _context(tmp_path, f"blocked-{reason.value.lower()}", ((100, 120),) * 4), plan
    )
    assert validation.result.decision is ScientificValidationDecision.INCONCLUSIVE
    assert reason in validation.result.reason_codes


def test_open_long_is_inconclusive_without_synthetic_exit(tmp_path: Path) -> None:
    values = tuple((100 + index, 101 + index) for index in range(6))
    start = datetime(2025, 2, 1, tzinfo=UTC)
    rows = []
    for index, (open_price, close_price) in enumerate(values):
        opened = start + timedelta(hours=index)
        closed = opened + timedelta(hours=1)
        available = closed + timedelta(seconds=5)
        rows.append(
            f"{opened.isoformat(timespec='microseconds').replace('+00:00', 'Z')},"
            f"{closed.isoformat(timespec='microseconds').replace('+00:00', 'Z')},"
            f"{open_price},{close_price + 1},{open_price - 1},{close_price},10,final,"
            f"{available.isoformat(timespec='microseconds').replace('+00:00', 'Z')}\n"
        )
    context = authorized_context(
        tmp_path, suffix="validation-open", csv_text=HEADER + "".join(rows)
    )
    _, _, backtest, validation, _ = _run(context, validation_plan(min_trades=1))
    assert backtest.artifact.open_position is SimulatedPositionState.LONG
    assert validation.result.decision is ScientificValidationDecision.INCONCLUSIVE
    assert ValidationReasonCode.OPEN_POSITION_UNRESOLVED in validation.result.reason_codes


def test_same_seed_is_byte_deterministic_and_new_seed_changes_input(tmp_path: Path) -> None:
    context = _context(tmp_path, "validation-deterministic", ((100, 120),) * 4)
    first = _run(context, validation_plan(seed=73))[3]
    second = _run(context, validation_plan(seed=73))[3]
    assert encode(first.result) == encode(second.result)
    assert encode(first.record) == encode(second.record)
    assert fingerprint_record(first.result) == fingerprint_record(second.result)
    changed = _run(context, validation_plan(seed=74))[3]
    assert first.record.validation_input_fingerprint != changed.record.validation_input_fingerprint


def test_exact_persistence_roundtrip_and_idempotency(pass_bundle: ValidationBundle) -> None:
    _, _, _, validation, context = pass_bundle
    repository = context[1]
    plan = validation_plan()
    assert repository.load(repository_key(plan), ValidationPlan).record == plan
    assert (
        repository.load(repository_key(validation.result), ScientificValidationResult).record
        == validation.result
    )
    assert (
        repository.load(repository_key(validation.record), ValidationRunRecord).record
        == validation.record
    )
    for stored in (plan, validation.result, validation.record):
        assert repository.store(stored).status is RepositoryWriteStatus.ALREADY_PRESENT_IDENTICAL


def test_persistence_corruption_and_wrong_type_fail_closed(
    pass_bundle: ValidationBundle,
) -> None:
    _, _, _, validation, context = pass_bundle
    repository = context[1]
    key = repository_key(validation.result)
    with pytest.raises(RepositoryTypeMismatch):
        repository.load(key, ValidationRunRecord)
    path = repository.path_for(key)
    path.write_bytes(path.read_bytes().replace(b'"PASS"', b'"FAIL"'))
    with pytest.raises(RepositoryIntegrityFailure):
        repository.load(key, ScientificValidationResult)


def test_codec_roundtrip_is_strict(pass_bundle: ValidationBundle) -> None:
    _, _, _, validation, _ = pass_bundle
    for record in (validation.result, validation.record):
        if isinstance(record, ScientificValidationResult):
            assert decode(encode(record), ScientificValidationResult) == record
        else:
            assert decode(encode(record), ValidationRunRecord) == record
    encoded = json.loads(encode(validation.result))
    encoded["payload"]["unexpected"] = True
    with pytest.raises(ValueError):
        decode(json.dumps(encoded).encode(), ScientificValidationResult)
    with pytest.raises(ScientificValidationContractError):
        replace(validation.result, version=ObjectVersion(2))


def _unsafe[T](record: T, **changes: object) -> T:
    clone = copy.copy(record)
    for field, value in changes.items():
        object.__setattr__(clone, field, value)
    return clone


@pytest.mark.parametrize(
    ("field", "value"),
    (
        ("estimate", "0"),
        ("lower_bound", "0"),
        ("upper_bound", "0"),
        ("sample_size", 99),
        ("trade_count", 99),
        ("confidence_level", "0.9"),
        ("decision", ScientificValidationDecision.FAIL),
        ("reason_codes", (ValidationReasonCode.FAILED_NONPOSITIVE_BOUND,)),
        (
            "validator_authority_ref",
            TraceabilityRef(AuthorityBindingId("wrong"), V1, "sha256:" + "c" * 64),
        ),
    ),
)
def test_validation_lineage_rejects_result_tamper(
    pass_bundle: ValidationBundle, field: str, value: object
) -> None:
    request, _, backtest, validation, context = pass_bundle
    context_result = validation.result
    # The verifier independently recomputes every scientific output from exact inputs.
    with pytest.raises(ValidationLineageMismatch):
        verify_scientific_validation_lineage(
            record=validation.record,
            result=_unsafe(context_result, **{field: value}),
            request=request,
            plan=validation_plan(),
            backtest_record=backtest.record,
            backtest_artifact=backtest.artifact,
            specification=context[7],
            strategy=context[6],
            instrument=context[10],
        )


def test_validation_lineage_rejects_refs_seed_and_run_binding_tamper(
    pass_bundle: ValidationBundle,
) -> None:
    request, _, backtest, validation, context = pass_bundle
    cases = (
        _unsafe(validation.result, validation_plan_ref=request.backtest_result_ref),
        _unsafe(validation.result, backtest_result_ref=request.validation_plan_ref),
        _unsafe(validation.result, backtest_run_ref=request.validation_plan_ref),
        _unsafe(validation.result, strategy_ref=request.validation_plan_ref),
    )
    for result in cases:
        with pytest.raises(ValidationLineageMismatch):
            verify_scientific_validation_lineage(
                record=validation.record,
                result=result,
                request=request,
                plan=validation_plan(),
                backtest_record=backtest.record,
                backtest_artifact=backtest.artifact,
                specification=context[7],
                strategy=context[6],
                instrument=context[10],
            )
    with pytest.raises(ValidationLineageMismatch):
        verify_scientific_validation_lineage(
            record=_unsafe(validation.record, random_seed=999),
            result=validation.result,
            request=request,
            plan=validation_plan(),
            backtest_record=backtest.record,
            backtest_artifact=backtest.artifact,
            specification=context[7],
            strategy=context[6],
            instrument=context[10],
        )


def test_scientific_validation_golden_is_pinned_and_read_only(tmp_path: Path) -> None:
    plan = validation_plan()
    _, _, backtest, validation, _ = _run(
        _context(tmp_path, "validation-golden", ((100, 120),) * 4), plan
    )
    result = validation.result
    expected = {
        "format": "scientific-validation-v1",
        "validation_plan_fingerprint": fingerprint_record(plan),
        "backtest_result_fingerprint": fingerprint_record(backtest.artifact),
        "validation_input_fingerprint": validation.record.validation_input_fingerprint,
        "seed": plan.random_seed,
        "sample_size": result.sample_size,
        "estimate": result.estimate,
        "lower_bound": result.lower_bound,
        "upper_bound": result.upper_bound,
        "confidence_level": result.confidence_level,
        "decision": result.decision.value,
        "reason_codes": [item.value for item in result.reason_codes],
        "validation_result_fingerprint": fingerprint_record(result),
    }
    assert json.loads(GOLDEN.read_text(encoding="utf-8")) == expected
