"""Closed deterministic long-only strategy simulation for Sprint 12."""

from __future__ import annotations

from dataclasses import dataclass, field
from decimal import ROUND_HALF_EVEN, Context, Decimal, localcontext

from ai_quant_lab.core.csv_import import CsvImportReport
from ai_quant_lab.core.dataset_store import LocalDatasetRepository, RepositoryWriteResult
from ai_quant_lab.core.experiment_authorization import experiment_configuration_fingerprint
from ai_quant_lab.core.experiment_contracts import (
    CostSemantics,
    ExperimentAuthorizationPolicy,
    ExperimentAuthorizationRecord,
    ExperimentFamily,
    ExperimentSpecification,
    NoLookaheadSemantics,
    PositionSizingSemantics,
)
from ai_quant_lab.core.experiment_runner import (
    ExperimentRunnerLineageMismatch,
    ExperimentRunRequest,
    ExperimentTimeWindowMismatch,
    UnsupportedExperimentRunner,
    _exact,
    _select_replay_bars,
    _verify_authorization,
)
from ai_quant_lab.core.experiment_runner_contracts import (
    ExperimentReplayContract,
    NumericSemantics,
    ReplayOrdering,
)
from ai_quant_lab.core.integrity import fingerprint_record
from ai_quant_lab.core.market_data import MarketBar
from ai_quant_lab.core.model import (
    ArtifactId,
    ExecutionState,
    ObjectVersion,
    TraceabilityRef,
    fingerprint,
)
from ai_quant_lab.core.real_csv_contracts import RealCsvAdmissionRecord, RealCsvSourceDeclaration
from ai_quant_lab.core.research_eligibility_contracts import (
    DeploymentAuthorizationStatus,
    ResearchDatasetEligibilityPolicy,
    ResearchDatasetEligibilityRecord,
    ValidationStatus,
)
from ai_quant_lab.core.strategy_backtest_contracts import (
    BacktestResultArtifact,
    BacktestRunRecord,
    BacktestRunStatus,
    EquityPoint,
    SidePermission,
    SignalTiming,
    SimulatedExecutionTiming,
    SimulatedFill,
    SimulatedOrder,
    SimulatedOrderSide,
    SimulatedOrderStatus,
    SimulatedPositionState,
    SimulatedTrade,
    StrategyDefinition,
    StrategyModel,
)


class StrategyBacktestError(ValueError):
    pass


class UnsupportedStrategy(StrategyBacktestError):
    pass


class UnsupportedSizing(StrategyBacktestError):
    pass


class InvalidExecutionPrice(StrategyBacktestError):
    pass


class InvalidFillTiming(StrategyBacktestError):
    pass


class LookaheadAttempt(StrategyBacktestError):
    pass


class MissingNextBar(StrategyBacktestError):
    pass


class InconsistentPositionTransition(StrategyBacktestError):
    pass


class InvalidCapital(StrategyBacktestError):
    pass


class UnsupportedFunding(StrategyBacktestError):
    pass


class BacktestLineageMismatch(StrategyBacktestError):
    pass


class AccountingMismatch(StrategyBacktestError):
    pass


_V1 = ObjectVersion(1)
_DECIMAL_CONTEXT = Context(prec=34, rounding=ROUND_HALF_EVEN)
_BPS = Decimal(10_000)
_METRICS = ("gross_pnl", "max_drawdown", "net_pnl", "total_return", "trade_count")
_OUTPUTS = ("equity_curve", "simulated_fills", "simulated_orders", "simulated_trades")


def strategy_backtest_replay_contract() -> ExperimentReplayContract:
    return ExperimentReplayContract(
        ArtifactId("close-vs-open-long-only-backtest-engine-v1"),
        _V1,
        ExperimentFamily.STRATEGY_BACKTEST,
        NoLookaheadSemantics.EXPLICIT_EVENT_AVAILABILITY_NEXT_EVENT,
        ReplayOrdering.BAR_OPEN_CLOSE_SOURCE_OBSERVATION_ID,
        NumericSemantics.DECIMAL128_HALF_EVEN,
        34,
        _METRICS,
        _OUTPUTS,
        _V1,
    )


def strategy_backtest_engine_ref() -> TraceabilityRef:
    contract = strategy_backtest_replay_contract()
    return _exact(contract, contract.engine_id, contract.version)


@dataclass(frozen=True, slots=True)
class StrategyBacktestRunRequest:
    experiment_run: ExperimentRunRequest
    strategy_ref: TraceabilityRef
    contract_version: ObjectVersion = field(default_factory=lambda: ObjectVersion(1))

    def __post_init__(self) -> None:
        if (
            not isinstance(self.experiment_run, ExperimentRunRequest)
            or self.contract_version != _V1
        ):
            raise StrategyBacktestError("unsupported strategy backtest request")
        if (
            not isinstance(self.strategy_ref, TraceabilityRef)
            or not isinstance(self.strategy_ref.object_id, ArtifactId)
            or self.strategy_ref.expected_fingerprint is None
        ):
            raise StrategyBacktestError("strategy backtest request requires exact strategy")


@dataclass(frozen=True, slots=True)
class StrategyBacktestResult:
    record: BacktestRunRecord
    artifact: BacktestResultArtifact
    writes: tuple[RepositoryWriteResult, ...]


@dataclass(frozen=True, slots=True)
class _PendingTransition:
    target: SimulatedPositionState
    source_bar: MarketBar
    fill_index: int


def _decimal(value: Decimal) -> str:
    if not value.is_finite():
        raise StrategyBacktestError("non-finite backtest value")
    if value == 0:
        return "0"
    text = format(value, "f")
    return text.rstrip("0").rstrip(".") if "." in text else text


def _bar_ref(bar: MarketBar) -> TraceabilityRef:
    return _exact(bar, bar.bar_id, bar.version)


def _cost(rate_semantics: CostSemantics, bps: int, notional: Decimal) -> Decimal:
    if rate_semantics is CostSemantics.DECLARED_ZERO:
        return Decimal(0)
    if rate_semantics is CostSemantics.DECLARED_BPS:
        return notional * Decimal(bps) / _BPS
    raise StrategyBacktestError("trading costs must be declared zero or declared bps")


def _execution_price(
    side: SimulatedOrderSide, reference: Decimal, semantics: CostSemantics, bps: int
) -> Decimal:
    if reference <= 0:
        raise InvalidExecutionPrice("fill reference price must be positive")
    if semantics is CostSemantics.DECLARED_ZERO:
        result = reference
    elif semantics is CostSemantics.DECLARED_BPS:
        direction = Decimal(1) if side is SimulatedOrderSide.BUY else Decimal(-1)
        result = reference * (Decimal(1) + direction * Decimal(bps) / _BPS)
    else:
        raise StrategyBacktestError("slippage must be declared zero or declared bps")
    if result <= 0:
        raise InvalidExecutionPrice("simulated execution price must be positive")
    return result


def _strategy_configuration(strategy: StrategyDefinition) -> tuple[tuple[str, str], ...]:
    return tuple(
        sorted(
            (
                ("capital_currency", strategy.capital_currency),
                ("capital_minor_unit_scale", str(strategy.capital_minor_unit_scale)),
                ("fixed_notional_minor", str(strategy.fixed_notional_minor)),
                ("strategy_fingerprint", fingerprint_record(strategy)),
                ("strategy_id", str(strategy.strategy_id)),
                ("strategy_model", strategy.model.value),
            )
        )
    )


def _require_scope(
    specification: ExperimentSpecification,
    engine_contract: ExperimentReplayContract,
    strategy: StrategyDefinition,
) -> None:
    if specification.family is not ExperimentFamily.STRATEGY_BACKTEST:
        raise UnsupportedExperimentRunner("strategy runner requires STRATEGY_BACKTEST")
    if engine_contract != strategy_backtest_replay_contract():
        raise UnsupportedExperimentRunner("unknown strategy backtest engine")
    if strategy.engine_contract_ref != _exact(
        engine_contract, engine_contract.engine_id, engine_contract.version
    ):
        raise UnsupportedStrategy("strategy does not bind exact engine")
    if specification.configuration != _strategy_configuration(strategy):
        raise UnsupportedStrategy("experiment does not bind exact strategy configuration")
    if specification.requested_metrics != _METRICS or specification.requested_outputs != _OUTPUTS:
        raise UnsupportedExperimentRunner("requested backtest result contract is unsupported")
    if specification.no_lookahead is not engine_contract.no_lookahead:
        raise LookaheadAttempt("strategy experiment has unsupported no-lookahead semantics")
    if (
        strategy.model is not StrategyModel.CLOSE_VS_OPEN_LONG_ONLY
        or strategy.signal_timing is not SignalTiming.BAR_CLOSE_AFTER_AVAILABILITY
        or strategy.execution_timing is not SimulatedExecutionTiming.FIRST_ELIGIBLE_NEXT_BAR_OPEN
        or strategy.side_permission is not SidePermission.LONG_ONLY
    ):
        raise UnsupportedStrategy("unsupported strategy semantics")
    if specification.sizing_semantics is not PositionSizingSemantics.FIXED_NOTIONAL:
        raise UnsupportedSizing("Sprint 12 supports FIXED_NOTIONAL only")
    if specification.funding_semantics is not CostSemantics.NOT_APPLICABLE:
        raise UnsupportedFunding("Sprint 12 does not model funding")
    if specification.commission_semantics not in (
        CostSemantics.DECLARED_ZERO,
        CostSemantics.DECLARED_BPS,
    ) or specification.slippage_semantics not in (
        CostSemantics.DECLARED_ZERO,
        CostSemantics.DECLARED_BPS,
    ):
        raise StrategyBacktestError("trading costs must be explicit")
    if specification.warmup_bars != 0:
        raise UnsupportedStrategy("closed threshold strategy requires zero warmup")
    if specification.capital_notional_minor <= 0:
        raise InvalidCapital("initial capital must be positive")
    if strategy.fixed_notional_minor > specification.capital_notional_minor:
        raise InvalidCapital("fixed notional exceeds initial capital")


def _desired_position(bar: MarketBar, strategy: StrategyDefinition) -> SimulatedPositionState:
    open_price = Decimal(bar.open.text)
    close_price = Decimal(bar.close.text)
    if open_price <= 0 or close_price <= 0:
        raise InvalidExecutionPrice("strategy signal prices must be positive")
    threshold = Decimal(strategy.threshold_bps) / _BPS
    return (
        SimulatedPositionState.LONG
        if close_price / open_price - Decimal(1) > threshold
        else SimulatedPositionState.FLAT
    )


def _next_fill_index(bars: tuple[MarketBar, ...], source_index: int) -> int:
    signal_time = bars[source_index].availability_time
    for index in range(source_index + 1, len(bars)):
        if bars[index].bar_open >= signal_time:
            return index
    raise MissingNextBar("position transition has no eligible next bar open")


def _run_input_fingerprint(
    request: StrategyBacktestRunRequest,
    authorization: ExperimentAuthorizationRecord,
    specification: ExperimentSpecification,
    policy: ExperimentAuthorizationPolicy,
    eligibility: ResearchDatasetEligibilityRecord,
    strategy: StrategyDefinition,
) -> str:
    base = request.experiment_run
    return fingerprint(
        {
            "run_id": str(base.run_id),
            "result_artifact_id": str(base.result_artifact_id),
            "authorization_fingerprint": fingerprint_record(authorization),
            "specification_fingerprint": fingerprint_record(specification),
            "policy_fingerprint": fingerprint_record(policy),
            "eligibility_fingerprint": fingerprint_record(eligibility),
            "strategy_fingerprint": fingerprint_record(strategy),
            "engine_contract_ref": base.engine_contract_ref,
            "configuration_fingerprint": experiment_configuration_fingerprint(specification),
            "completed_at": base.completed_at,
            "provenance_ref": base.provenance_ref,
        }
    )


def _simulate(
    request: StrategyBacktestRunRequest,
    authorization: ExperimentAuthorizationRecord,
    specification: ExperimentSpecification,
    strategy: StrategyDefinition,
    bars: tuple[MarketBar, ...],
    run_input: str,
) -> BacktestResultArtifact:
    base = request.experiment_run
    scale = Decimal(strategy.capital_minor_unit_scale)
    initial = Decimal(specification.capital_notional_minor) / scale
    fixed_notional = Decimal(strategy.fixed_notional_minor) / scale
    cash = initial
    quantity = Decimal(0)
    entry_price: Decimal | None = None
    entry_fill: SimulatedFill | None = None
    entry_commission = Decimal(0)
    entry_slippage = Decimal(0)
    realized = Decimal(0)
    position = SimulatedPositionState.FLAT
    pending: _PendingTransition | None = None
    orders: list[SimulatedOrder] = []
    fills: list[SimulatedFill] = []
    trades: list[SimulatedTrade] = []
    curve: list[EquityPoint] = []
    strategy_ref = _exact(strategy, strategy.strategy_id, strategy.version)

    with localcontext(_DECIMAL_CONTEXT):
        for index, bar in enumerate(bars):
            if pending is not None and pending.fill_index == index:
                side = (
                    SimulatedOrderSide.BUY
                    if pending.target is SimulatedPositionState.LONG
                    else SimulatedOrderSide.SELL
                )
                reference = Decimal(bar.open.text)
                execution = _execution_price(
                    side, reference, specification.slippage_semantics, specification.slippage_bps
                )
                order_number = len(orders) + 1
                order_id = ArtifactId(f"{base.run_id.value}-simulated-order-{order_number:04d}")
                fill_id = ArtifactId(f"{base.run_id.value}-simulated-fill-{order_number:04d}")
                if side is SimulatedOrderSide.BUY:
                    if position is not SimulatedPositionState.FLAT or quantity != 0:
                        raise InconsistentPositionTransition("long entry requires flat position")
                    fill_quantity = fixed_notional / execution
                    fill_notional = fill_quantity * execution
                else:
                    if position is not SimulatedPositionState.LONG or quantity <= 0:
                        raise InconsistentPositionTransition("long exit requires open long")
                    fill_quantity = quantity
                    fill_notional = fill_quantity * execution
                commission = _cost(
                    specification.commission_semantics,
                    specification.commission_bps,
                    fill_notional,
                )
                slippage = abs(execution - reference) * fill_quantity
                order = SimulatedOrder(
                    order_id,
                    side,
                    _decimal(fill_notional),
                    pending.source_bar.availability_time,
                    pending.source_bar.availability_time,
                    bar.bar_open,
                    _bar_ref(pending.source_bar),
                    _bar_ref(bar),
                    strategy_ref,
                    base.run_id,
                    _V1,
                    SimulatedOrderStatus.FILLED,
                )
                fill = SimulatedFill(
                    fill_id,
                    order_id,
                    side,
                    _bar_ref(bar),
                    bar.bar_open,
                    _decimal(reference),
                    _decimal(execution),
                    _decimal(fill_quantity),
                    _decimal(fill_notional),
                    _decimal(commission),
                    _decimal(slippage),
                )
                if fill.fill_time < order.signal_time:
                    raise InvalidFillTiming("fill precedes governed signal availability")
                orders.append(order)
                fills.append(fill)
                if side is SimulatedOrderSide.BUY:
                    if cash < fill_notional + commission:
                        raise InvalidCapital("insufficient simulated cash for fixed notional")
                    cash -= fill_notional + commission
                    quantity = fill_quantity
                    entry_price = execution
                    entry_fill = fill
                    entry_commission = commission
                    entry_slippage = slippage
                    position = SimulatedPositionState.LONG
                else:
                    assert entry_price is not None and entry_fill is not None
                    cash += fill_notional - commission
                    gross = (execution - entry_price) * fill_quantity
                    total_commission = entry_commission + commission
                    net = gross - total_commission
                    realized += net
                    trades.append(
                        SimulatedTrade(
                            ArtifactId(
                                f"{base.run_id.value}-simulated-trade-{len(trades) + 1:04d}"
                            ),
                            entry_fill.fill_id,
                            fill.fill_id,
                            _decimal(fill_quantity),
                            _decimal(entry_price),
                            _decimal(execution),
                            _decimal(gross),
                            _decimal(total_commission),
                            _decimal(entry_slippage + slippage),
                            _decimal(net),
                            entry_fill.fill_time,
                            fill.fill_time,
                            strategy_ref,
                            base.run_id,
                            _V1,
                        )
                    )
                    quantity = Decimal(0)
                    entry_price = None
                    entry_fill = None
                    entry_commission = Decimal(0)
                    entry_slippage = Decimal(0)
                    position = SimulatedPositionState.FLAT
                pending = None

            mark = Decimal(bar.close.text)
            if mark <= 0:
                raise InvalidExecutionPrice("equity mark price must be positive")
            position_value = quantity * mark
            unrealized = Decimal(0) if entry_price is None else (mark - entry_price) * quantity
            equity = cash + position_value
            if equity < 0:
                raise AccountingMismatch("simulated equity cannot be negative")
            curve.append(
                EquityPoint(
                    bar.availability_time,
                    _decimal(cash),
                    _decimal(quantity),
                    _decimal(position_value),
                    _decimal(unrealized),
                    _decimal(realized),
                    _decimal(equity),
                )
            )

            desired = _desired_position(bar, strategy)
            if pending is not None:
                if desired is not pending.target:
                    raise InconsistentPositionTransition(
                        "signal changed before pending next-event fill"
                    )
            elif desired is not position:
                pending = _PendingTransition(desired, bar, _next_fill_index(bars, index))

        if pending is not None:
            raise MissingNextBar("terminal position transition cannot be filled inside window")

        final_equity = Decimal(curve[-1].equity)
        gross_pnl = sum((Decimal(trade.gross_pnl) for trade in trades), Decimal(0))
        net_pnl = sum((Decimal(trade.net_pnl) for trade in trades), Decimal(0))
        total_return = final_equity / initial - Decimal(1)
        peak = initial
        max_drawdown = Decimal(0)
        for point in curve:
            point_equity = Decimal(point.equity)
            peak = max(peak, point_equity)
            if peak <= 0:
                raise AccountingMismatch("drawdown peak must remain positive")
            max_drawdown = max(max_drawdown, Decimal(1) - point_equity / peak)

    return BacktestResultArtifact(
        base.result_artifact_id,
        _V1,
        base.run_id,
        _V1,
        run_input,
        base.authorization_ref,
        base.specification_ref,
        base.policy_ref,
        base.eligibility_ref,
        specification.normalized_manifest_ref,
        specification.normalized_lock_ref,
        base.engine_contract_ref,
        strategy_ref,
        authorization.configuration_fingerprint,
        strategy.capital_currency,
        strategy.capital_minor_unit_scale,
        _decimal(initial),
        tuple(orders),
        tuple(fills),
        tuple(trades),
        tuple(curve),
        _decimal(cash),
        _decimal(final_equity),
        position,
        len(trades),
        _decimal(gross_pnl),
        _decimal(net_pnl),
        _decimal(total_return),
        _decimal(max_drawdown),
        ValidationStatus.NOT_VALIDATED,
        DeploymentAuthorizationStatus.NOT_AUTHORIZED,
        ExecutionState.PLANNED_CLOSED,
        _V1,
    )


def run_authorized_strategy_backtest(
    request: StrategyBacktestRunRequest,
    *,
    authorization: ExperimentAuthorizationRecord,
    specification: ExperimentSpecification,
    policy: ExperimentAuthorizationPolicy,
    eligibility: ResearchDatasetEligibilityRecord,
    eligibility_policy: ResearchDatasetEligibilityPolicy,
    admission: RealCsvAdmissionRecord,
    declaration: RealCsvSourceDeclaration,
    report: CsvImportReport,
    engine_contract: ExperimentReplayContract,
    strategy: StrategyDefinition,
    repository: LocalDatasetRepository,
) -> StrategyBacktestResult:
    base = request.experiment_run
    try:
        _verify_authorization(
            base,
            authorization=authorization,
            specification=specification,
            policy=policy,
            eligibility=eligibility,
            eligibility_policy=eligibility_policy,
            admission=admission,
            declaration=declaration,
            report=report,
            engine_contract=engine_contract,
        )
    except (ExperimentRunnerLineageMismatch, UnsupportedExperimentRunner):
        raise
    except ValueError as exc:
        raise BacktestLineageMismatch("strategy authorization lineage failed") from exc
    expected_strategy_ref = _exact(strategy, strategy.strategy_id, strategy.version)
    if request.strategy_ref != expected_strategy_ref:
        raise BacktestLineageMismatch("backtest request does not bind exact strategy")
    _require_scope(specification, engine_contract, strategy)
    bars = _select_replay_bars(specification, report)
    if base.completed_at < max(
        specification.knowledge_cutoff, max(bar.availability_time for bar in bars)
    ):
        raise ExperimentTimeWindowMismatch("backtest completion precedes governed knowledge")
    run_input = _run_input_fingerprint(
        request, authorization, specification, policy, eligibility, strategy
    )
    artifact = _simulate(request, authorization, specification, strategy, bars, run_input)
    record = BacktestRunRecord(
        base.run_id,
        _V1,
        base.authorization_ref,
        base.specification_ref,
        base.policy_ref,
        base.eligibility_ref,
        specification.normalized_manifest_ref,
        specification.normalized_lock_ref,
        base.engine_contract_ref,
        request.strategy_ref,
        authorization.configuration_fingerprint,
        run_input,
        _exact(artifact, artifact.artifact_id, artifact.version),
        BacktestRunStatus.COMPLETED,
        base.completed_at,
        base.provenance_ref,
        ValidationStatus.NOT_VALIDATED,
        DeploymentAuthorizationStatus.NOT_AUTHORIZED,
        ExecutionState.PLANNED_CLOSED,
        _V1,
    )
    verify_strategy_backtest_lineage(
        record=record,
        artifact=artifact,
        request=request,
        authorization=authorization,
        specification=specification,
        policy=policy,
        eligibility=eligibility,
        engine_contract=engine_contract,
        strategy=strategy,
        report=report,
    )
    writes = (
        repository.store(engine_contract),
        repository.store(strategy),
        repository.store(artifact),
        repository.store(record),
    )
    return StrategyBacktestResult(record, artifact, writes)


def verify_strategy_backtest_lineage(
    *,
    record: BacktestRunRecord,
    artifact: BacktestResultArtifact,
    request: StrategyBacktestRunRequest,
    authorization: ExperimentAuthorizationRecord,
    specification: ExperimentSpecification,
    policy: ExperimentAuthorizationPolicy,
    eligibility: ResearchDatasetEligibilityRecord,
    engine_contract: ExperimentReplayContract,
    strategy: StrategyDefinition,
    report: CsvImportReport,
) -> None:
    expected_input = _run_input_fingerprint(
        request, authorization, specification, policy, eligibility, strategy
    )
    expected_artifact = _simulate(
        request,
        authorization,
        specification,
        strategy,
        _select_replay_bars(specification, report),
        expected_input,
    )
    if artifact != expected_artifact:
        raise BacktestLineageMismatch("backtest result does not match exact deterministic replay")
    if record.result_ref != _exact(artifact, artifact.artifact_id, artifact.version):
        raise BacktestLineageMismatch("backtest run does not bind exact result")
    refs = (
        request.experiment_run.authorization_ref,
        request.experiment_run.specification_ref,
        request.experiment_run.policy_ref,
        request.experiment_run.eligibility_ref,
        specification.normalized_manifest_ref,
        specification.normalized_lock_ref,
        request.experiment_run.engine_contract_ref,
        request.strategy_ref,
    )
    if (
        record.authorization_ref,
        record.specification_ref,
        record.policy_ref,
        record.eligibility_ref,
        record.normalized_manifest_ref,
        record.normalized_lock_ref,
        record.engine_contract_ref,
        record.strategy_ref,
    ) != refs or (
        artifact.authorization_ref,
        artifact.specification_ref,
        artifact.policy_ref,
        artifact.eligibility_ref,
        artifact.normalized_manifest_ref,
        artifact.normalized_lock_ref,
        artifact.engine_contract_ref,
        artifact.strategy_ref,
    ) != refs:
        raise BacktestLineageMismatch("backtest artifacts do not preserve exact lineage refs")
    if (
        record.run_input_fingerprint != expected_input
        or artifact.run_input_fingerprint != expected_input
        or record.configuration_fingerprint != experiment_configuration_fingerprint(specification)
        or record.completed_at != request.experiment_run.completed_at
        or record.provenance_ref != request.experiment_run.provenance_ref
    ):
        raise BacktestLineageMismatch("backtest run inputs changed")
