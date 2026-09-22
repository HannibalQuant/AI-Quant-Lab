"""Controlled deterministic robustness evaluation for Sprint 15."""

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
from ai_quant_lab.core.experiment_runner import _select_replay_bars
from ai_quant_lab.core.experiment_runner_contracts import ExperimentReplayContract
from ai_quant_lab.core.integrity import fingerprint_record
from ai_quant_lab.core.market_data import MarketBar
from ai_quant_lab.core.model import (
    ArtifactId,
    ExecutionState,
    ObjectVersion,
    TraceabilityRef,
    fingerprint,
)
from ai_quant_lab.core.research_eligibility_contracts import (
    DeploymentAuthorizationStatus,
    ResearchDatasetEligibilityRecord,
)
from ai_quant_lab.core.robustness_validation_contracts import (
    CostPerturbationScenario,
    CostPerturbationSummary,
    MonteCarloSummary,
    PerturbationPolicy,
    RobustnessDecision,
    RobustnessHoldoutEvidence,
    RobustnessReasonCode,
    RobustnessRunStatus,
    RobustnessValidationPlan,
    RobustnessValidationRequest,
    RobustnessValidationResult,
    RobustnessValidationRunRecord,
    TemporalPartitionEvidence,
    TemporalPartitionRole,
    WalkForwardSliceResult,
    WalkForwardSummary,
)
from ai_quant_lab.core.scientific_validation import verify_scientific_validation_lineage
from ai_quant_lab.core.scientific_validation_contracts import (
    ScientificValidationDecision,
    ScientificValidationResult,
    ValidationPlan,
    ValidationRequest,
    ValidationRunRecord,
)
from ai_quant_lab.core.strategy_backtest import StrategyBacktestRunRequest
from ai_quant_lab.core.strategy_backtest_contracts import (
    BacktestResultArtifact,
    BacktestRunRecord,
    StrategyDefinition,
)


class RobustnessValidationError(ValueError):
    pass


class RobustnessInputInvalid(RobustnessValidationError):
    pass


class RobustnessAuthorityInvalid(RobustnessValidationError):
    pass


class RobustnessLineageMismatch(RobustnessValidationError):
    pass


class RobustnessPartitionInvalid(RobustnessValidationError):
    pass


_V1 = ObjectVersion(1)
_DECIMAL_CONTEXT = Context(prec=34, rounding=ROUND_HALF_EVEN)


@dataclass(frozen=True, slots=True)
class RobustnessValidationExecutionResult:
    record: RobustnessValidationRunRecord
    result: RobustnessValidationResult
    writes: tuple[RepositoryWriteResult, ...]


def _exact(record: object, object_id: object, version: ObjectVersion) -> TraceabilityRef:
    return TraceabilityRef(object_id, version, fingerprint_record(record))  # type: ignore[arg-type]


def _decimal(value: Decimal) -> str:
    if not value.is_finite():
        raise RobustnessInputInvalid("robustness produced a non-finite decimal")
    if value == 0:
        return "0"
    text = format(value, "f")
    return text.rstrip("0").rstrip(".") if "." in text else text


def _reasons(*values: RobustnessReasonCode) -> tuple[RobustnessReasonCode, ...]:
    return tuple(sorted(set(values), key=lambda item: item.value))


def _bar_ref(bar: MarketBar) -> TraceabilityRef:
    return _exact(bar, bar.bar_id, bar.version)


def _draw_index(seed: int, iteration: int, draw: int, sample_size: int) -> int:
    digest = hashlib.sha256(f"{seed}:{iteration}:{draw}".encode("ascii")).digest()
    return int.from_bytes(digest, "big") % sample_size


def _quantile(values: list[Decimal], probability: Decimal, *, upper: bool = False) -> Decimal:
    if not values:
        return Decimal(0)
    index_value = probability * Decimal(len(values) - 1)
    rounding = ROUND_CEILING if upper else ROUND_FLOOR
    return values[int(index_value.to_integral_value(rounding=rounding))]


def _median(values: list[Decimal]) -> Decimal:
    if not values:
        return Decimal(0)
    middle = len(values) // 2
    if len(values) % 2:
        return values[middle]
    return (values[middle - 1] + values[middle]) / Decimal(2)


def _drawdown(values: tuple[Decimal, ...], starting_equity: Decimal) -> Decimal:
    if starting_equity <= 0:
        raise RobustnessInputInvalid("robustness requires positive starting equity")
    peak = starting_equity
    maximum = Decimal(0)
    for equity in values:
        peak = max(peak, equity)
        if peak > 0:
            maximum = max(maximum, Decimal(1) - equity / peak)
    return maximum


def _partition(
    *,
    prefix: str,
    role: TemporalPartitionRole,
    start: int,
    end: int,
    bars: tuple[MarketBar, ...],
) -> TemporalPartitionEvidence:
    selected = bars[start:end]
    if not selected or len(selected) != end - start:
        raise RobustnessPartitionInvalid("partition does not bind an exact bar range")
    return TemporalPartitionEvidence(
        partition_id=ArtifactId(f"{prefix}-{role.value.lower()}"),
        role=role,
        start_index=start,
        end_index=end,
        bar_refs=tuple(_bar_ref(bar) for bar in selected),
    )


def _walk_forward(
    *,
    plan: RobustnessValidationPlan,
    bars: tuple[MarketBar, ...],
    artifact: BacktestResultArtifact,
) -> WalkForwardSummary:
    point_by_ref = {point.bar_ref: point for point in artifact.equity_curve}
    slices: list[WalkForwardSliceResult] = []
    start = 0
    number = 1
    while start + plan.train_bars + plan.test_bars <= len(bars):
        train_start = start
        train_end = train_start + plan.train_bars
        test_start = train_end
        test_end = test_start + plan.test_bars
        prefix = f"robustness-slice-{number:04d}"
        train = _partition(
            prefix=prefix,
            role=TemporalPartitionRole.TRAIN,
            start=train_start,
            end=train_end,
            bars=bars,
        )
        test = _partition(
            prefix=prefix,
            role=TemporalPartitionRole.TEST,
            start=test_start,
            end=test_end,
            bars=bars,
        )
        if set(train.bar_refs) & set(test.bar_refs):
            raise RobustnessPartitionInvalid("train and test partitions overlap")
        points = tuple(point_by_ref[reference] for reference in test.bar_refs)
        before = point_by_ref[_bar_ref(bars[test_start - 1])]
        starting = Decimal(before.equity)
        ending = Decimal(points[-1].equity)
        first_time = bars[test_start].bar_open
        end_time = bars[test_end - 1].bar_close
        trades = tuple(
            trade for trade in artifact.trades if first_time <= trade.exit_time < end_time
        )
        total_return = ending / starting - Decimal(1)
        net_pnl = sum((Decimal(trade.net_pnl) for trade in trades), Decimal(0))
        maximum_drawdown = _drawdown(tuple(Decimal(point.equity) for point in points), starting)
        slice_decision = (
            RobustnessDecision.PASS
            if total_return > 0
            else RobustnessDecision.FAIL
            if total_return <= Decimal(plan.walk_forward_severe_loss_floor)
            else RobustnessDecision.INCONCLUSIVE
        )
        slices.append(
            WalkForwardSliceResult(
                ArtifactId(prefix),
                train,
                test,
                len(trades),
                _decimal(total_return),
                _decimal(net_pnl),
                _decimal(maximum_drawdown),
                slice_decision,
            )
        )
        start += plan.step_bars
        number += 1

    returns = [Decimal(item.total_return) for item in slices]
    drawdowns = [Decimal(item.max_drawdown) for item in slices]
    counts = [item.trade_count for item in slices]
    valid_windows = len(slices)
    positive_ratio = (
        Decimal(sum(value > 0 for value in returns)) / Decimal(valid_windows)
        if valid_windows
        else Decimal(0)
    )
    ordered_returns = sorted(returns)
    median_return = _median(ordered_returns)
    worst_return = min(returns, default=Decimal(0))
    aggregate = sum(returns, Decimal(0))
    maximum_drawdown = max(drawdowns, default=Decimal(0))
    minimum_trades = min(counts, default=0)

    reasons: list[RobustnessReasonCode] = []
    if valid_windows < plan.minimum_window_count:
        reasons.append(RobustnessReasonCode.INSUFFICIENT_WINDOWS)
    if minimum_trades < plan.minimum_completed_trades_per_test_slice:
        reasons.append(RobustnessReasonCode.INSUFFICIENT_TEST_TRADES)
    if reasons:
        decision = RobustnessDecision.INCONCLUSIVE
    elif positive_ratio <= Decimal(
        plan.walk_forward_fail_positive_ratio
    ) or worst_return <= Decimal(plan.walk_forward_severe_loss_floor):
        decision = RobustnessDecision.FAIL
        reasons.append(RobustnessReasonCode.WALK_FORWARD_FAILED)
    elif positive_ratio >= Decimal(
        plan.walk_forward_pass_positive_ratio
    ) and worst_return >= Decimal(plan.walk_forward_pass_worst_return_floor):
        decision = RobustnessDecision.PASS
        reasons.append(RobustnessReasonCode.ALL_ENABLED_METHODS_PASSED)
    else:
        decision = RobustnessDecision.INCONCLUSIVE
        reasons.append(RobustnessReasonCode.WALK_FORWARD_INCONCLUSIVE)
    return WalkForwardSummary(
        tuple(slices),
        valid_windows,
        _decimal(positive_ratio),
        _decimal(median_return),
        _decimal(worst_return),
        _decimal(aggregate),
        _decimal(maximum_drawdown),
        minimum_trades,
        decision,
        _reasons(*reasons),
    )


def _monte_carlo(
    *, plan: RobustnessValidationPlan, artifact: BacktestResultArtifact
) -> MonteCarloSummary:
    initial = Decimal(artifact.initial_capital)
    contributions = tuple(Decimal(trade.net_pnl) / initial for trade in artifact.trades)
    terminals: list[Decimal] = []
    drawdowns: list[Decimal] = []
    if contributions:
        for iteration in range(plan.monte_carlo_iterations):
            cumulative = Decimal(0)
            path: list[Decimal] = []
            for draw in range(len(contributions)):
                cumulative += contributions[
                    _draw_index(plan.monte_carlo_seed, iteration, draw, len(contributions))
                ]
                path.append(Decimal(1) + cumulative)
            terminals.append(cumulative)
            drawdowns.append(_drawdown(tuple(path), Decimal(1)))
    else:
        terminals.append(Decimal(0))
        drawdowns.append(Decimal(0))
    terminals.sort()
    lower = _quantile(terminals, Decimal(plan.monte_carlo_lower_quantile))
    upper = _quantile(terminals, Decimal(plan.monte_carlo_upper_quantile), upper=True)
    median = _median(terminals)
    positive_fraction = Decimal(sum(value > 0 for value in terminals)) / Decimal(len(terminals))
    if lower > 0:
        decision = RobustnessDecision.PASS
        reasons = _reasons(RobustnessReasonCode.ALL_ENABLED_METHODS_PASSED)
    elif upper <= 0:
        decision = RobustnessDecision.FAIL
        reasons = _reasons(RobustnessReasonCode.MONTE_CARLO_FAILED)
    else:
        decision = RobustnessDecision.INCONCLUSIVE
        reasons = _reasons(RobustnessReasonCode.MONTE_CARLO_INCONCLUSIVE)
    return MonteCarloSummary(
        plan.monte_carlo_policy,
        plan.monte_carlo_iterations,
        plan.monte_carlo_seed,
        _decimal(median),
        _decimal(lower),
        _decimal(upper),
        _decimal(max(drawdowns)),
        _decimal(positive_fraction),
        decision,
        reasons,
    )


def _adjusted_drawdown(
    *,
    artifact: BacktestResultArtifact,
    multiplier: Decimal,
) -> Decimal:
    extra_factor = multiplier - Decimal(1)
    adjusted: list[Decimal] = []
    for point in artifact.equity_curve:
        extra = sum(
            (
                Decimal(fill.commission) * extra_factor
                for fill in artifact.fills
                if fill.fill_time <= point.event_time
            ),
            Decimal(0),
        )
        adjusted.append(Decimal(point.equity) - extra)
    return _drawdown(tuple(adjusted), Decimal(artifact.initial_capital))


def _cost_perturbation(
    *, plan: RobustnessValidationPlan, artifact: BacktestResultArtifact
) -> CostPerturbationSummary:
    initial = Decimal(artifact.initial_capital)
    all_commission = sum((Decimal(fill.commission) for fill in artifact.fills), Decimal(0))
    trade_commission = sum((Decimal(trade.commission) for trade in artifact.trades), Decimal(0))
    scenarios: list[CostPerturbationScenario] = []
    for multiplier_text in plan.commission_multipliers:
        multiplier = Decimal(multiplier_text)
        extra_factor = multiplier - Decimal(1)
        adjusted_net = Decimal(artifact.net_pnl) - trade_commission * extra_factor
        adjusted_equity = Decimal(artifact.final_equity) - all_commission * extra_factor
        total_return = adjusted_equity / initial - Decimal(1)
        scenarios.append(
            CostPerturbationScenario(
                multiplier_text,
                _decimal(total_return),
                _decimal(adjusted_net),
                _decimal(_adjusted_drawdown(artifact=artifact, multiplier=multiplier)),
                artifact.trade_count,
            )
        )
    worst = min(Decimal(item.total_return) for item in scenarios)
    if worst <= Decimal(plan.perturbation_fail_return_threshold):
        decision = RobustnessDecision.FAIL
        reasons = _reasons(RobustnessReasonCode.COST_PERTURBATION_FAILED)
    elif all(
        Decimal(item.total_return) >= Decimal(plan.perturbation_pass_return_floor)
        for item in scenarios
    ):
        decision = RobustnessDecision.PASS
        reasons = _reasons(RobustnessReasonCode.ALL_ENABLED_METHODS_PASSED)
    else:
        decision = RobustnessDecision.INCONCLUSIVE
        reasons = _reasons(RobustnessReasonCode.COST_PERTURBATION_INCONCLUSIVE)
    return CostPerturbationSummary(
        PerturbationPolicy.COMMISSION_MULTIPLIER,
        tuple(scenarios),
        decision,
        reasons,
    )


def _input_fingerprint(
    *,
    plan: RobustnessValidationPlan,
    scientific_result: ScientificValidationResult,
    validation_record: ValidationRunRecord,
    backtest_artifact: BacktestResultArtifact,
    backtest_record: BacktestRunRecord,
    specification: ExperimentSpecification,
    strategy: StrategyDefinition,
    instrument: InstrumentIdentity,
) -> str:
    return fingerprint(
        {
            "robustness_plan_fingerprint": fingerprint_record(plan),
            "scientific_validation_result_fingerprint": fingerprint_record(scientific_result),
            "validation_run_fingerprint": fingerprint_record(validation_record),
            "backtest_result_fingerprint": fingerprint_record(backtest_artifact),
            "backtest_run_fingerprint": fingerprint_record(backtest_record),
            "experiment_fingerprint": fingerprint_record(specification),
            "strategy_fingerprint": fingerprint_record(strategy),
            "instrument_fingerprint": fingerprint_record(instrument),
            "normalized_manifest_ref": backtest_artifact.normalized_manifest_ref,
            "normalized_lock_ref": backtest_artifact.normalized_lock_ref,
            "monte_carlo_seed": plan.monte_carlo_seed,
            "partition": {
                "train_bars": plan.train_bars,
                "test_bars": plan.test_bars,
                "step_bars": plan.step_bars,
            },
            "commission_multipliers": plan.commission_multipliers,
        }
    )


def _verify_request(
    request: RobustnessValidationRequest,
    *,
    plan: RobustnessValidationPlan,
    scientific_result: ScientificValidationResult,
    validation_record: ValidationRunRecord,
    backtest_artifact: BacktestResultArtifact,
    backtest_record: BacktestRunRecord,
) -> None:
    expected = (
        _exact(plan, plan.robustness_plan_id, plan.version),
        _exact(
            scientific_result,
            scientific_result.validation_result_id,
            scientific_result.version,
        ),
        _exact(validation_record, validation_record.validation_run_id, validation_record.version),
        _exact(backtest_artifact, backtest_artifact.artifact_id, backtest_artifact.version),
        _exact(backtest_record, backtest_record.run_id, backtest_record.version),
    )
    actual = (
        request.robustness_plan_ref,
        request.scientific_validation_result_ref,
        request.validation_run_ref,
        request.backtest_result_ref,
        request.backtest_run_ref,
    )
    if actual != expected:
        raise RobustnessLineageMismatch("robustness request does not bind exact source artifacts")
    if request.robustness_authority_ref != plan.robustness_authority_ref:
        raise RobustnessAuthorityInvalid("robustness request lacks exact governed authority")
    if plan.source_scientific_validation_ref != request.scientific_validation_result_ref:
        raise RobustnessLineageMismatch("robustness plan does not bind exact validation result")


def _evaluate(
    *,
    request: RobustnessValidationRequest,
    plan: RobustnessValidationPlan,
    scientific_result: ScientificValidationResult,
    backtest_artifact: BacktestResultArtifact,
    specification: ExperimentSpecification,
    strategy: StrategyDefinition,
    report: CsvImportReport,
) -> RobustnessValidationResult:
    bars = _select_replay_bars(specification, report)
    with localcontext(_DECIMAL_CONTEXT):
        walk_forward = _walk_forward(plan=plan, bars=bars, artifact=backtest_artifact)
        monte_carlo = _monte_carlo(plan=plan, artifact=backtest_artifact)
        perturbation = _cost_perturbation(plan=plan, artifact=backtest_artifact)
    method_decisions = (
        walk_forward.decision,
        monte_carlo.decision,
        perturbation.decision,
    )
    reasons: list[RobustnessReasonCode] = []
    if scientific_result.decision is not ScientificValidationDecision.PASS:
        reasons.append(RobustnessReasonCode.SOURCE_VALIDATION_NOT_PASS)
        decision = RobustnessDecision.INCONCLUSIVE
    elif RobustnessDecision.FAIL in method_decisions:
        decision = RobustnessDecision.FAIL
        if walk_forward.decision is RobustnessDecision.FAIL:
            reasons.append(RobustnessReasonCode.WALK_FORWARD_FAILED)
        if monte_carlo.decision is RobustnessDecision.FAIL:
            reasons.append(RobustnessReasonCode.MONTE_CARLO_FAILED)
        if perturbation.decision is RobustnessDecision.FAIL:
            reasons.append(RobustnessReasonCode.COST_PERTURBATION_FAILED)
    elif all(value is RobustnessDecision.PASS for value in method_decisions):
        decision = RobustnessDecision.PASS
        reasons.append(RobustnessReasonCode.ALL_ENABLED_METHODS_PASSED)
    else:
        decision = RobustnessDecision.INCONCLUSIVE
        if walk_forward.decision is RobustnessDecision.INCONCLUSIVE:
            reasons.extend(walk_forward.reason_codes)
        if monte_carlo.decision is RobustnessDecision.INCONCLUSIVE:
            reasons.extend(monte_carlo.reason_codes)
        if perturbation.decision is RobustnessDecision.INCONCLUSIVE:
            reasons.extend(perturbation.reason_codes)
    return RobustnessValidationResult(
        request.robustness_result_id,
        _V1,
        request.robustness_plan_ref,
        request.scientific_validation_result_ref,
        request.validation_run_ref,
        request.backtest_result_ref,
        request.backtest_run_ref,
        backtest_artifact.strategy_ref,
        scientific_result.experiment_ref,
        backtest_artifact.normalized_manifest_ref,
        backtest_artifact.normalized_lock_ref,
        walk_forward,
        monte_carlo,
        perturbation,
        RobustnessHoldoutEvidence.NOT_ESTABLISHED,
        decision,
        _reasons(*reasons),
        request.robustness_authority_ref,
        request.provenance_ref,
        DeploymentAuthorizationStatus.NOT_AUTHORIZED,
        ExecutionState.PLANNED_CLOSED,
        _V1,
    )


def run_robustness_validation(
    request: RobustnessValidationRequest,
    *,
    plan: RobustnessValidationPlan,
    scientific_result: ScientificValidationResult,
    validation_record: ValidationRunRecord,
    scientific_request: ValidationRequest,
    validation_plan: ValidationPlan,
    backtest_artifact: BacktestResultArtifact,
    backtest_record: BacktestRunRecord,
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
) -> RobustnessValidationExecutionResult:
    _verify_request(
        request,
        plan=plan,
        scientific_result=scientific_result,
        validation_record=validation_record,
        backtest_artifact=backtest_artifact,
        backtest_record=backtest_record,
    )
    try:
        verify_scientific_validation_lineage(
            record=validation_record,
            result=scientific_result,
            request=scientific_request,
            plan=validation_plan,
            backtest_record=backtest_record,
            backtest_artifact=backtest_artifact,
            backtest_request=backtest_request,
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
        raise RobustnessInputInvalid(
            "robustness source scientific validation failed exact verification"
        ) from exc
    result = _evaluate(
        request=request,
        plan=plan,
        scientific_result=scientific_result,
        backtest_artifact=backtest_artifact,
        specification=specification,
        strategy=strategy,
        report=report,
    )
    input_fingerprint = _input_fingerprint(
        plan=plan,
        scientific_result=scientific_result,
        validation_record=validation_record,
        backtest_artifact=backtest_artifact,
        backtest_record=backtest_record,
        specification=specification,
        strategy=strategy,
        instrument=instrument,
    )
    record = RobustnessValidationRunRecord(
        request.robustness_run_id,
        _V1,
        request.robustness_plan_ref,
        request.scientific_validation_result_ref,
        request.validation_run_ref,
        request.backtest_result_ref,
        request.backtest_run_ref,
        input_fingerprint,
        plan.monte_carlo_seed,
        _exact(result, result.robustness_result_id, result.version),
        request.robustness_authority_ref,
        request.provenance_ref,
        RobustnessRunStatus.COMPLETED,
        DeploymentAuthorizationStatus.NOT_AUTHORIZED,
        ExecutionState.PLANNED_CLOSED,
        _V1,
    )
    verify_robustness_validation_lineage(
        record=record,
        result=result,
        request=request,
        plan=plan,
        scientific_result=scientific_result,
        validation_record=validation_record,
        scientific_request=scientific_request,
        validation_plan=validation_plan,
        backtest_artifact=backtest_artifact,
        backtest_record=backtest_record,
        backtest_request=backtest_request,
        authorization=authorization,
        specification=specification,
        policy=policy,
        eligibility=eligibility,
        engine_contract=engine_contract,
        strategy=strategy,
        instrument=instrument,
        report=report,
    )
    writes = (repository.store(plan), repository.store(result), repository.store(record))
    return RobustnessValidationExecutionResult(record, result, writes)


def verify_robustness_validation_lineage(
    *,
    record: RobustnessValidationRunRecord,
    result: RobustnessValidationResult,
    request: RobustnessValidationRequest,
    plan: RobustnessValidationPlan,
    scientific_result: ScientificValidationResult,
    validation_record: ValidationRunRecord,
    scientific_request: ValidationRequest,
    validation_plan: ValidationPlan,
    backtest_artifact: BacktestResultArtifact,
    backtest_record: BacktestRunRecord,
    backtest_request: StrategyBacktestRunRequest,
    authorization: ExperimentAuthorizationRecord,
    specification: ExperimentSpecification,
    policy: ExperimentAuthorizationPolicy,
    eligibility: ResearchDatasetEligibilityRecord,
    engine_contract: ExperimentReplayContract,
    strategy: StrategyDefinition,
    instrument: InstrumentIdentity,
    report: CsvImportReport,
) -> None:
    _verify_request(
        request,
        plan=plan,
        scientific_result=scientific_result,
        validation_record=validation_record,
        backtest_artifact=backtest_artifact,
        backtest_record=backtest_record,
    )
    try:
        verify_scientific_validation_lineage(
            record=validation_record,
            result=scientific_result,
            request=scientific_request,
            plan=validation_plan,
            backtest_record=backtest_record,
            backtest_artifact=backtest_artifact,
            backtest_request=backtest_request,
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
        raise RobustnessInputInvalid(
            "robustness source scientific validation failed exact verification"
        ) from exc
    expected = _evaluate(
        request=request,
        plan=plan,
        scientific_result=scientific_result,
        backtest_artifact=backtest_artifact,
        specification=specification,
        strategy=strategy,
        report=report,
    )
    expected_input = _input_fingerprint(
        plan=plan,
        scientific_result=scientific_result,
        validation_record=validation_record,
        backtest_artifact=backtest_artifact,
        backtest_record=backtest_record,
        specification=specification,
        strategy=strategy,
        instrument=instrument,
    )
    if (
        record.robustness_plan_ref != request.robustness_plan_ref
        or record.scientific_validation_result_ref != request.scientific_validation_result_ref
        or record.validation_run_ref != request.validation_run_ref
        or record.backtest_result_ref != request.backtest_result_ref
        or record.backtest_run_ref != request.backtest_run_ref
        or record.robustness_input_fingerprint != expected_input
        or record.monte_carlo_seed != plan.monte_carlo_seed
        or record.robustness_result_ref
        != _exact(result, result.robustness_result_id, result.version)
        or record.robustness_authority_ref != request.robustness_authority_ref
        or record.provenance_ref != request.provenance_ref
    ):
        raise RobustnessLineageMismatch("robustness run does not bind exact inputs")
    if result != expected:
        raise RobustnessLineageMismatch("robustness result is not deterministic")
