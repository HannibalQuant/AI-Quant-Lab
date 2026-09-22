"""Deterministic, authority-separated scientific validation foundation for Sprint 14."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from decimal import ROUND_CEILING, ROUND_FLOOR, ROUND_HALF_EVEN, Context, Decimal, localcontext

from ai_quant_lab.core.csv_import import CsvImportReport
from ai_quant_lab.core.data import InstrumentIdentity
from ai_quant_lab.core.dataset_store import LocalDatasetRepository, RepositoryWriteResult
from ai_quant_lab.core.experiment_contracts import (
    ExperimentAuthorizationPolicy,
    ExperimentAuthorizationRecord,
    ExperimentSpecification,
)
from ai_quant_lab.core.experiment_runner_contracts import ExperimentReplayContract
from ai_quant_lab.core.integrity import fingerprint_record
from ai_quant_lab.core.model import ExecutionState, ObjectVersion, TraceabilityRef, fingerprint
from ai_quant_lab.core.research_eligibility_contracts import (
    DeploymentAuthorizationStatus,
    ResearchDatasetEligibilityRecord,
)
from ai_quant_lab.core.scientific_validation_contracts import (
    HoldoutEvidenceStatus,
    HoldoutPolicy,
    MultiplicityPolicy,
    OutOfSampleEvidenceStatus,
    ScientificValidationBoundary,
    ScientificValidationDecision,
    ScientificValidationResult,
    UncertaintyMethod,
    ValidationMetric,
    ValidationPlan,
    ValidationReasonCode,
    ValidationRequest,
    ValidationRunRecord,
    ValidationRunStatus,
)
from ai_quant_lab.core.strategy_backtest import (
    StrategyBacktestRunRequest,
    verify_strategy_backtest_lineage,
)
from ai_quant_lab.core.strategy_backtest_contracts import (
    BacktestResultArtifact,
    BacktestRunRecord,
    SimulatedPositionState,
    StrategyDefinition,
)


class ScientificValidationError(ValueError):
    pass


class ValidationInputInvalid(ScientificValidationError):
    pass


class ValidationAuthorityInvalid(ScientificValidationError):
    pass


class ValidationLineageMismatch(ScientificValidationError):
    pass


class UnsupportedValidationMethod(ScientificValidationError):
    pass


_V1 = ObjectVersion(1)
_DECIMAL_CONTEXT = Context(prec=34, rounding=ROUND_HALF_EVEN)


@dataclass(frozen=True, slots=True)
class ScientificValidationExecutionResult:
    record: ValidationRunRecord
    result: ScientificValidationResult
    writes: tuple[RepositoryWriteResult, ...]


def _exact(record: object, object_id: object, version: ObjectVersion) -> TraceabilityRef:
    return TraceabilityRef(object_id, version, fingerprint_record(record))  # type: ignore[arg-type]


def _decimal(value: Decimal) -> str:
    if not value.is_finite():
        raise ValidationInputInvalid("validation produced a non-finite decimal")
    if value == 0:
        return "0"
    text = format(value, "f")
    return text.rstrip("0").rstrip(".") if "." in text else text


def _reason_codes(*values: ValidationReasonCode) -> tuple[ValidationReasonCode, ...]:
    return tuple(sorted(set(values), key=lambda item: item.value))


def _validation_input_fingerprint(
    *,
    plan: ValidationPlan,
    artifact: BacktestResultArtifact,
    record: BacktestRunRecord,
    specification: ExperimentSpecification,
    strategy: StrategyDefinition,
    instrument: InstrumentIdentity,
) -> str:
    return fingerprint(
        {
            "validation_plan_fingerprint": fingerprint_record(plan),
            "backtest_result_fingerprint": fingerprint_record(artifact),
            "backtest_run_fingerprint": fingerprint_record(record),
            "experiment_fingerprint": fingerprint_record(specification),
            "strategy_fingerprint": fingerprint_record(strategy),
            "instrument_fingerprint": fingerprint_record(instrument),
            "method": plan.uncertainty_method.value,
            "bootstrap_iterations": plan.bootstrap_iterations,
            "confidence_level": plan.confidence_level,
            "random_seed": plan.random_seed,
        }
    )


def _draw_index(seed: int, iteration: int, draw: int, sample_size: int) -> int:
    digest = hashlib.sha256(f"{seed}:{iteration}:{draw}".encode("ascii")).digest()
    return int.from_bytes(digest, "big") % sample_size


def _bootstrap_interval(
    values: tuple[Decimal, ...], *, seed: int, iterations: int, confidence: Decimal
) -> tuple[Decimal, Decimal]:
    if not values:
        return Decimal(0), Decimal(0)
    statistics: list[Decimal] = []
    for iteration in range(iterations):
        statistics.append(
            sum(
                (
                    values[_draw_index(seed, iteration, draw, len(values))]
                    for draw in range(len(values))
                ),
                Decimal(0),
            )
        )
    statistics.sort()
    last = Decimal(iterations - 1)
    tail = (Decimal(1) - confidence) / Decimal(2)
    lower_index = int((tail * last).to_integral_value(rounding=ROUND_FLOOR))
    upper_index = int(((Decimal(1) - tail) * last).to_integral_value(rounding=ROUND_CEILING))
    return statistics[lower_index], statistics[upper_index]


def _evaluate(
    *,
    request: ValidationRequest,
    plan: ValidationPlan,
    artifact: BacktestResultArtifact,
    record: BacktestRunRecord,
    specification: ExperimentSpecification,
    strategy: StrategyDefinition,
) -> ScientificValidationResult:
    if artifact.version != ObjectVersion(2) or artifact.contract_version != ObjectVersion(2):
        raise ValidationInputInvalid("scientific validation requires hardened backtest result v2")
    if plan.uncertainty_method is not UncertaintyMethod.TRADE_RETURN_BOOTSTRAP:
        raise UnsupportedValidationMethod("unsupported scientific uncertainty method")

    with localcontext(_DECIMAL_CONTEXT):
        initial = Decimal(artifact.initial_capital)
        if initial <= 0:
            raise ValidationInputInvalid("validation requires positive initial capital")
        trade_returns = tuple(Decimal(trade.net_pnl) / initial for trade in artifact.trades)
        lower, upper = _bootstrap_interval(
            trade_returns,
            seed=plan.random_seed,
            iterations=plan.bootstrap_iterations,
            confidence=Decimal(plan.confidence_level),
        )
        estimate = Decimal(artifact.total_return)

    blockers: list[ValidationReasonCode] = []
    if artifact.trade_count < plan.min_trade_count or len(trade_returns) < plan.min_sample_size:
        blockers.append(ValidationReasonCode.INSUFFICIENT_TRADES)
    if artifact.open_position is SimulatedPositionState.LONG:
        blockers.append(ValidationReasonCode.OPEN_POSITION_UNRESOLVED)
    if plan.holdout_policy is HoldoutPolicy.RESERVED_HOLDOUT:
        blockers.append(ValidationReasonCode.HOLDOUT_REQUIRED)
    if plan.multiplicity_policy is MultiplicityPolicy.UNKNOWN:
        blockers.append(ValidationReasonCode.MULTIPLICITY_UNKNOWN)
    elif plan.multiplicity_policy is MultiplicityPolicy.MULTIPLE_TESTS_UNCORRECTED:
        blockers.append(ValidationReasonCode.MULTIPLICITY_UNSUPPORTED)

    if blockers:
        decision = ScientificValidationDecision.INCONCLUSIVE
        reasons = _reason_codes(*blockers)
    elif lower > 0:
        decision = ScientificValidationDecision.PASS
        reasons = _reason_codes(ValidationReasonCode.PASSED_CONFIDENCE_BOUND)
    elif upper <= 0:
        decision = ScientificValidationDecision.FAIL
        reasons = _reason_codes(ValidationReasonCode.FAILED_NONPOSITIVE_BOUND)
    else:
        decision = ScientificValidationDecision.INCONCLUSIVE
        reasons = _reason_codes(ValidationReasonCode.INTERVAL_OVERLAPS_ZERO)

    holdout_status = (
        HoldoutEvidenceStatus.NONE_DECLARED
        if plan.holdout_policy is HoldoutPolicy.NONE_DECLARED
        else HoldoutEvidenceStatus.REQUIRED_NOT_PROVEN
    )
    return ScientificValidationResult(
        request.validation_result_id,
        _V1,
        request.validation_plan_ref,
        request.backtest_result_ref,
        request.backtest_run_ref,
        _exact(specification, specification.experiment_id, specification.version),
        _exact(strategy, strategy.strategy_id, strategy.version),
        artifact.normalized_manifest_ref,
        artifact.normalized_lock_ref,
        ValidationMetric.TOTAL_RETURN,
        _decimal(estimate),
        _decimal(lower),
        _decimal(upper),
        plan.confidence_level,
        plan.uncertainty_method,
        len(trade_returns),
        artifact.trade_count,
        holdout_status,
        plan.multiplicity_policy,
        decision,
        reasons,
        request.validator_authority_ref,
        request.provenance_ref,
        ScientificValidationBoundary.SCIENTIFIC_METHOD_APPLIED,
        OutOfSampleEvidenceStatus.NOT_ESTABLISHED,
        DeploymentAuthorizationStatus.NOT_AUTHORIZED,
        ExecutionState.PLANNED_CLOSED,
        _V1,
    )


def _verify_request(
    request: ValidationRequest,
    *,
    plan: ValidationPlan,
    artifact: BacktestResultArtifact,
    record: BacktestRunRecord,
) -> None:
    if request.validation_plan_ref != _exact(plan, plan.validation_plan_id, plan.version):
        raise ValidationLineageMismatch("validation request does not bind exact plan")
    if request.backtest_result_ref != _exact(artifact, artifact.artifact_id, artifact.version):
        raise ValidationLineageMismatch("validation request does not bind exact backtest result")
    if request.backtest_run_ref != _exact(record, record.run_id, record.version):
        raise ValidationLineageMismatch("validation request does not bind exact backtest run")
    if request.validator_authority_ref != plan.validator_authority_ref:
        raise ValidationAuthorityInvalid("validation request lacks exact governed authority")


def run_scientific_validation(
    request: ValidationRequest,
    *,
    plan: ValidationPlan,
    backtest_record: BacktestRunRecord,
    backtest_artifact: BacktestResultArtifact,
    backtest_request: StrategyBacktestRunRequest,
    authorization: ExperimentAuthorizationRecord,
    specification: ExperimentSpecification,
    policy: ExperimentAuthorizationPolicy,
    eligibility: ResearchDatasetEligibilityRecord,
    engine_contract: ExperimentReplayContract,
    strategy: StrategyDefinition,
    instrument: InstrumentIdentity,
    report: CsvImportReport,
    repository: LocalDatasetRepository,
) -> ScientificValidationExecutionResult:
    _verify_request(request, plan=plan, artifact=backtest_artifact, record=backtest_record)
    try:
        verify_strategy_backtest_lineage(
            record=backtest_record,
            artifact=backtest_artifact,
            request=backtest_request,
            authorization=authorization,
            specification=specification,
            policy=policy,
            eligibility=eligibility,
            engine_contract=engine_contract,
            strategy=strategy,
            instrument=instrument,
            report=report,
        )
    except ValueError as exc:
        raise ValidationInputInvalid("backtest input failed exact verification") from exc
    result = _evaluate(
        request=request,
        plan=plan,
        artifact=backtest_artifact,
        record=backtest_record,
        specification=specification,
        strategy=strategy,
    )
    input_fingerprint = _validation_input_fingerprint(
        plan=plan,
        artifact=backtest_artifact,
        record=backtest_record,
        specification=specification,
        strategy=strategy,
        instrument=instrument,
    )
    validation_record = ValidationRunRecord(
        request.validation_run_id,
        _V1,
        request.validation_plan_ref,
        request.backtest_result_ref,
        request.backtest_run_ref,
        input_fingerprint,
        plan.random_seed,
        _exact(result, result.validation_result_id, result.version),
        request.validator_authority_ref,
        request.completed_at,
        request.provenance_ref,
        ValidationRunStatus.COMPLETED,
        DeploymentAuthorizationStatus.NOT_AUTHORIZED,
        ExecutionState.PLANNED_CLOSED,
        _V1,
    )
    verify_scientific_validation_lineage(
        record=validation_record,
        result=result,
        request=request,
        plan=plan,
        backtest_record=backtest_record,
        backtest_artifact=backtest_artifact,
        specification=specification,
        strategy=strategy,
        instrument=instrument,
    )
    writes = (
        repository.store(plan),
        repository.store(result),
        repository.store(validation_record),
    )
    return ScientificValidationExecutionResult(validation_record, result, writes)


def verify_scientific_validation_lineage(
    *,
    record: ValidationRunRecord,
    result: ScientificValidationResult,
    request: ValidationRequest,
    plan: ValidationPlan,
    backtest_record: BacktestRunRecord,
    backtest_artifact: BacktestResultArtifact,
    specification: ExperimentSpecification,
    strategy: StrategyDefinition,
    instrument: InstrumentIdentity,
) -> None:
    _verify_request(request, plan=plan, artifact=backtest_artifact, record=backtest_record)
    expected_result = _evaluate(
        request=request,
        plan=plan,
        artifact=backtest_artifact,
        record=backtest_record,
        specification=specification,
        strategy=strategy,
    )
    expected_input = _validation_input_fingerprint(
        plan=plan,
        artifact=backtest_artifact,
        record=backtest_record,
        specification=specification,
        strategy=strategy,
        instrument=instrument,
    )
    if result != expected_result:
        raise ValidationLineageMismatch("scientific validation result is not deterministic")
    if (
        record.validation_plan_ref != request.validation_plan_ref
        or record.backtest_result_ref != request.backtest_result_ref
        or record.backtest_run_ref != request.backtest_run_ref
        or record.validator_authority_ref != request.validator_authority_ref
        or record.validation_input_fingerprint != expected_input
        or record.random_seed != plan.random_seed
        or record.completed_at != request.completed_at
        or record.provenance_ref != request.provenance_ref
        or record.validation_result_ref
        != _exact(result, result.validation_result_id, result.version)
    ):
        raise ValidationLineageMismatch("validation run does not bind exact deterministic inputs")
