"""Immutable contracts for the bounded Sprint 12 strategy backtest engine."""

from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import datetime
from decimal import ROUND_HALF_EVEN, Context, Decimal, InvalidOperation, localcontext
from enum import StrEnum

from ai_quant_lab.core.data import DatasetLockId
from ai_quant_lab.core.market_data import MarketBarId
from ai_quant_lab.core.model import (
    ArtifactId,
    DatasetId,
    ExecutionState,
    ExperimentId,
    ObjectVersion,
    ProvenanceId,
    RunId,
    TraceabilityRef,
    require_utc,
)
from ai_quant_lab.core.research_eligibility_contracts import (
    DeploymentAuthorizationStatus,
    ValidationStatus,
)


class StrategyBacktestContractError(ValueError):
    pass


class StrategyModel(StrEnum):
    CLOSE_VS_OPEN_LONG_ONLY = "CLOSE_VS_OPEN_LONG_ONLY"


class SignalTiming(StrEnum):
    BAR_CLOSE_AFTER_AVAILABILITY = "BAR_CLOSE_AFTER_AVAILABILITY"


class SimulatedExecutionTiming(StrEnum):
    FIRST_ELIGIBLE_NEXT_BAR_OPEN = "FIRST_ELIGIBLE_NEXT_BAR_OPEN"


class SidePermission(StrEnum):
    LONG_ONLY = "LONG_ONLY"


class SimulatedOrderSide(StrEnum):
    BUY = "BUY"
    SELL = "SELL"


class SimulatedOrderStatus(StrEnum):
    FILLED = "FILLED"


class SimulatedPositionState(StrEnum):
    FLAT = "FLAT"
    LONG = "LONG"


class BacktestRunStatus(StrEnum):
    COMPLETED = "COMPLETED"


def _exact(reference: TraceabilityRef, identifier: type, field: str) -> None:
    if (
        not isinstance(reference, TraceabilityRef)
        or not isinstance(reference.object_id, identifier)
        or reference.expected_fingerprint is None
    ):
        raise StrategyBacktestContractError(f"{field} must be an exact fingerprint reference")


def _decimal_text(value: str, field: str, *, positive: bool = False) -> None:
    if not isinstance(value, str) or not re.fullmatch(r"-?(?:0|[1-9][0-9]*)(?:\.[0-9]+)?", value):
        raise StrategyBacktestContractError(f"{field} must be canonical finite decimal text")
    try:
        parsed = Decimal(value)
    except InvalidOperation as exc:  # pragma: no cover
        raise StrategyBacktestContractError(f"{field} must be canonical decimal text") from exc
    if (
        not parsed.is_finite()
        or (parsed == 0 and value != "0")
        or ("." in value and value.endswith("0"))
        or (positive and parsed <= 0)
    ):
        raise StrategyBacktestContractError(f"{field} has invalid decimal semantics")


def _fingerprint(value: str, field: str) -> None:
    if not isinstance(value, str) or not re.fullmatch(r"sha256:[0-9a-f]{64}", value):
        raise StrategyBacktestContractError(f"{field} must be canonical SHA-256")


@dataclass(frozen=True, slots=True)
class StrategyDefinition:
    strategy_id: ArtifactId
    version: ObjectVersion
    model: StrategyModel
    signal_timing: SignalTiming
    execution_timing: SimulatedExecutionTiming
    side_permission: SidePermission
    threshold_bps: int
    fixed_notional_minor: int
    capital_currency: str
    capital_minor_unit_scale: int
    allow_pyramiding: bool
    force_close_at_window_end: bool
    engine_contract_ref: TraceabilityRef
    provenance_ref: TraceabilityRef
    contract_version: ObjectVersion

    def __post_init__(self) -> None:
        if (
            not isinstance(self.strategy_id, ArtifactId)
            or self.version != ObjectVersion(1)
            or self.model is not StrategyModel.CLOSE_VS_OPEN_LONG_ONLY
            or self.signal_timing is not SignalTiming.BAR_CLOSE_AFTER_AVAILABILITY
            or self.execution_timing is not SimulatedExecutionTiming.FIRST_ELIGIBLE_NEXT_BAR_OPEN
            or self.side_permission is not SidePermission.LONG_ONLY
            or self.contract_version != ObjectVersion(1)
        ):
            raise StrategyBacktestContractError("unsupported strategy definition")
        if (
            isinstance(self.threshold_bps, bool)
            or not isinstance(self.threshold_bps, int)
            or not 0 <= self.threshold_bps <= 10_000
            or isinstance(self.fixed_notional_minor, bool)
            or not isinstance(self.fixed_notional_minor, int)
            or self.fixed_notional_minor <= 0
            or isinstance(self.capital_minor_unit_scale, bool)
            or not isinstance(self.capital_minor_unit_scale, int)
            or self.capital_minor_unit_scale <= 0
        ):
            raise StrategyBacktestContractError("strategy numeric declarations are invalid")
        if not re.fullmatch(r"[A-Z]{3,12}", self.capital_currency):
            raise StrategyBacktestContractError(
                "capital currency must be explicit uppercase identity"
            )
        if self.allow_pyramiding or self.force_close_at_window_end:
            raise StrategyBacktestContractError(
                "Sprint 12 forbids pyramiding and implicit force-close"
            )
        _exact(self.engine_contract_ref, ArtifactId, "engine_contract_ref")
        _exact(self.provenance_ref, ProvenanceId, "provenance_ref")


@dataclass(frozen=True, slots=True)
class SimulatedOrder:
    order_id: ArtifactId
    side: SimulatedOrderSide
    notional: str
    signal_time: datetime
    submitted_time: datetime
    eligible_fill_time: datetime
    source_bar_ref: TraceabilityRef
    fill_bar_ref: TraceabilityRef
    strategy_ref: TraceabilityRef
    run_id: RunId
    run_version: ObjectVersion
    status: SimulatedOrderStatus

    def __post_init__(self) -> None:
        if (
            not isinstance(self.order_id, ArtifactId)
            or not isinstance(self.side, SimulatedOrderSide)
            or not isinstance(self.run_id, RunId)
            or self.run_version != ObjectVersion(1)
            or self.status is not SimulatedOrderStatus.FILLED
        ):
            raise StrategyBacktestContractError("invalid simulated order identity/state")
        _decimal_text(self.notional, "order.notional", positive=True)
        for name in ("signal_time", "submitted_time", "eligible_fill_time"):
            require_utc(getattr(self, name), name)
        if self.submitted_time != self.signal_time or self.eligible_fill_time < self.signal_time:
            raise StrategyBacktestContractError("simulated order timing permits lookahead")
        _exact(self.source_bar_ref, MarketBarId, "source_bar_ref")
        _exact(self.fill_bar_ref, MarketBarId, "fill_bar_ref")
        _exact(self.strategy_ref, ArtifactId, "strategy_ref")


@dataclass(frozen=True, slots=True)
class SimulatedFill:
    fill_id: ArtifactId
    order_id: ArtifactId
    side: SimulatedOrderSide
    bar_ref: TraceabilityRef
    fill_time: datetime
    reference_price: str
    execution_price: str
    quantity: str
    fill_notional: str
    commission: str
    slippage_cost: str

    def __post_init__(self) -> None:
        if not isinstance(self.fill_id, ArtifactId) or not isinstance(self.order_id, ArtifactId):
            raise StrategyBacktestContractError("invalid simulated fill identity")
        if not isinstance(self.side, SimulatedOrderSide):
            raise StrategyBacktestContractError("invalid simulated fill side")
        _exact(self.bar_ref, MarketBarId, "fill.bar_ref")
        require_utc(self.fill_time, "fill_time")
        for field in ("reference_price", "execution_price", "quantity", "fill_notional"):
            _decimal_text(getattr(self, field), f"fill.{field}", positive=True)
        for field in ("commission", "slippage_cost"):
            _decimal_text(getattr(self, field), f"fill.{field}")
            if Decimal(getattr(self, field)) < 0:
                raise StrategyBacktestContractError(f"fill.{field} cannot be negative")


@dataclass(frozen=True, slots=True)
class SimulatedTrade:
    trade_id: ArtifactId
    entry_fill_id: ArtifactId
    exit_fill_id: ArtifactId
    quantity: str
    entry_price: str
    exit_price: str
    gross_pnl: str
    commission: str
    slippage_cost: str
    net_pnl: str
    entry_time: datetime
    exit_time: datetime
    strategy_ref: TraceabilityRef
    run_id: RunId
    run_version: ObjectVersion

    def __post_init__(self) -> None:
        for value in (self.trade_id, self.entry_fill_id, self.exit_fill_id):
            if not isinstance(value, ArtifactId):
                raise StrategyBacktestContractError("invalid simulated trade identity")
        for field in ("quantity", "entry_price", "exit_price"):
            _decimal_text(getattr(self, field), f"trade.{field}", positive=True)
        for field in ("gross_pnl", "commission", "slippage_cost", "net_pnl"):
            _decimal_text(getattr(self, field), f"trade.{field}")
        if Decimal(self.commission) < 0 or Decimal(self.slippage_cost) < 0:
            raise StrategyBacktestContractError("trade costs cannot be negative")
        require_utc(self.entry_time, "entry_time")
        require_utc(self.exit_time, "exit_time")
        if self.entry_time >= self.exit_time:
            raise StrategyBacktestContractError("trade exit must follow entry")
        _exact(self.strategy_ref, ArtifactId, "trade.strategy_ref")
        if not isinstance(self.run_id, RunId) or self.run_version != ObjectVersion(1):
            raise StrategyBacktestContractError("trade run identity is invalid")


@dataclass(frozen=True, slots=True)
class EquityPoint:
    event_time: datetime
    cash: str
    position_quantity: str
    position_value: str
    unrealized_pnl: str
    realized_pnl: str
    equity: str

    def __post_init__(self) -> None:
        require_utc(self.event_time, "equity.event_time")
        for field in (
            "cash",
            "position_quantity",
            "position_value",
            "unrealized_pnl",
            "realized_pnl",
            "equity",
        ):
            _decimal_text(getattr(self, field), f"equity.{field}")


@dataclass(frozen=True, slots=True)
class BacktestResultArtifact:
    artifact_id: ArtifactId
    version: ObjectVersion
    run_id: RunId
    run_version: ObjectVersion
    run_input_fingerprint: str
    authorization_ref: TraceabilityRef
    specification_ref: TraceabilityRef
    policy_ref: TraceabilityRef
    eligibility_ref: TraceabilityRef
    normalized_manifest_ref: TraceabilityRef
    normalized_lock_ref: TraceabilityRef
    engine_contract_ref: TraceabilityRef
    strategy_ref: TraceabilityRef
    configuration_fingerprint: str
    capital_currency: str
    capital_minor_unit_scale: int
    initial_capital: str
    orders: tuple[SimulatedOrder, ...]
    fills: tuple[SimulatedFill, ...]
    trades: tuple[SimulatedTrade, ...]
    equity_curve: tuple[EquityPoint, ...]
    final_cash: str
    final_equity: str
    open_position: SimulatedPositionState
    trade_count: int
    gross_pnl: str
    net_pnl: str
    total_return: str
    max_drawdown: str
    validation_status: ValidationStatus
    deployment_authorization: DeploymentAuthorizationStatus
    execution_state: ExecutionState
    contract_version: ObjectVersion

    def __post_init__(self) -> None:
        if (
            not isinstance(self.artifact_id, ArtifactId)
            or self.version != ObjectVersion(1)
            or not isinstance(self.run_id, RunId)
            or self.run_version != ObjectVersion(1)
            or self.contract_version != ObjectVersion(1)
        ):
            raise StrategyBacktestContractError("unsupported backtest result contract")
        _fingerprint(self.run_input_fingerprint, "run_input_fingerprint")
        _fingerprint(self.configuration_fingerprint, "configuration_fingerprint")
        for reference, identifier, field in (
            (self.authorization_ref, ArtifactId, "authorization_ref"),
            (self.specification_ref, ExperimentId, "specification_ref"),
            (self.policy_ref, ArtifactId, "policy_ref"),
            (self.eligibility_ref, ArtifactId, "eligibility_ref"),
            (self.normalized_manifest_ref, DatasetId, "normalized_manifest_ref"),
            (self.normalized_lock_ref, DatasetLockId, "normalized_lock_ref"),
            (self.engine_contract_ref, ArtifactId, "engine_contract_ref"),
            (self.strategy_ref, ArtifactId, "strategy_ref"),
        ):
            _exact(reference, identifier, field)
        if not re.fullmatch(r"[A-Z]{3,12}", self.capital_currency):
            raise StrategyBacktestContractError("result capital currency is invalid")
        if self.capital_minor_unit_scale <= 0:
            raise StrategyBacktestContractError("result capital scale is invalid")
        for field in (
            "initial_capital",
            "final_cash",
            "final_equity",
            "gross_pnl",
            "net_pnl",
            "total_return",
            "max_drawdown",
        ):
            _decimal_text(getattr(self, field), f"result.{field}")
        if Decimal(self.initial_capital) <= 0 or Decimal(self.final_equity) < 0:
            raise StrategyBacktestContractError("result capital/equity is invalid")
        if Decimal(self.max_drawdown) < 0:
            raise StrategyBacktestContractError("max_drawdown must be non-negative magnitude")
        if self.trade_count != len(self.trades) or len(self.orders) != len(self.fills):
            raise StrategyBacktestContractError("backtest result cardinality is inconsistent")
        if not self.equity_curve:
            raise StrategyBacktestContractError("backtest requires an equity curve")
        if tuple(point.event_time for point in self.equity_curve) != tuple(
            sorted(point.event_time for point in self.equity_curve)
        ):
            raise StrategyBacktestContractError("equity curve must be deterministically ordered")
        if not isinstance(self.open_position, SimulatedPositionState):
            raise StrategyBacktestContractError("result position state is invalid")
        for order, fill in zip(self.orders, self.fills, strict=True):
            if (
                order.order_id != fill.order_id
                or order.side is not fill.side
                or order.fill_bar_ref != fill.bar_ref
                or order.eligible_fill_time != fill.fill_time
                or Decimal(order.notional) != Decimal(fill.fill_notional)
            ):
                raise StrategyBacktestContractError("order/fill exact linkage is inconsistent")
        fill_ids = {fill.fill_id for fill in self.fills}
        if any(
            trade.entry_fill_id not in fill_ids or trade.exit_fill_id not in fill_ids
            for trade in self.trades
        ):
            raise StrategyBacktestContractError("trade references an unknown fill")
        with localcontext(Context(prec=34, rounding=ROUND_HALF_EVEN)):
            if any(
                Decimal(point.equity) != Decimal(point.cash) + Decimal(point.position_value)
                for point in self.equity_curve
            ):
                raise StrategyBacktestContractError("equity accounting identity is inconsistent")
            if (
                Decimal(self.final_cash) != Decimal(self.equity_curve[-1].cash)
                or Decimal(self.final_equity) != Decimal(self.equity_curve[-1].equity)
                or Decimal(self.gross_pnl)
                != sum((Decimal(trade.gross_pnl) for trade in self.trades), Decimal(0))
                or Decimal(self.net_pnl)
                != sum((Decimal(trade.net_pnl) for trade in self.trades), Decimal(0))
            ):
                raise StrategyBacktestContractError("result summary does not match its ledger")
            if Decimal(self.total_return) != (
                Decimal(self.final_equity) / Decimal(self.initial_capital) - Decimal(1)
            ):
                raise StrategyBacktestContractError("total return does not match final equity")
            peak = Decimal(self.initial_capital)
            drawdown = Decimal(0)
            for point in self.equity_curve:
                point_equity = Decimal(point.equity)
                peak = max(peak, point_equity)
                drawdown = max(drawdown, Decimal(1) - point_equity / peak)
            if Decimal(self.max_drawdown) != drawdown:
                raise StrategyBacktestContractError("max drawdown does not match equity curve")
        if self.validation_status is not ValidationStatus.NOT_VALIDATED:
            raise StrategyBacktestContractError("backtest cannot grant validation")
        if self.deployment_authorization is not DeploymentAuthorizationStatus.NOT_AUTHORIZED:
            raise StrategyBacktestContractError("backtest cannot grant deployment")
        if self.execution_state is not ExecutionState.PLANNED_CLOSED:
            raise StrategyBacktestContractError("backtest cannot open live execution")


@dataclass(frozen=True, slots=True)
class BacktestRunRecord:
    run_id: RunId
    version: ObjectVersion
    authorization_ref: TraceabilityRef
    specification_ref: TraceabilityRef
    policy_ref: TraceabilityRef
    eligibility_ref: TraceabilityRef
    normalized_manifest_ref: TraceabilityRef
    normalized_lock_ref: TraceabilityRef
    engine_contract_ref: TraceabilityRef
    strategy_ref: TraceabilityRef
    configuration_fingerprint: str
    run_input_fingerprint: str
    result_ref: TraceabilityRef
    status: BacktestRunStatus
    completed_at: datetime
    provenance_ref: TraceabilityRef
    validation_status: ValidationStatus
    deployment_authorization: DeploymentAuthorizationStatus
    execution_state: ExecutionState
    contract_version: ObjectVersion

    def __post_init__(self) -> None:
        if (
            not isinstance(self.run_id, RunId)
            or self.version != ObjectVersion(1)
            or self.status is not BacktestRunStatus.COMPLETED
            or self.contract_version != ObjectVersion(1)
        ):
            raise StrategyBacktestContractError("unsupported backtest run record")
        for reference, identifier, field in (
            (self.authorization_ref, ArtifactId, "authorization_ref"),
            (self.specification_ref, ExperimentId, "specification_ref"),
            (self.policy_ref, ArtifactId, "policy_ref"),
            (self.eligibility_ref, ArtifactId, "eligibility_ref"),
            (self.normalized_manifest_ref, DatasetId, "normalized_manifest_ref"),
            (self.normalized_lock_ref, DatasetLockId, "normalized_lock_ref"),
            (self.engine_contract_ref, ArtifactId, "engine_contract_ref"),
            (self.strategy_ref, ArtifactId, "strategy_ref"),
            (self.result_ref, ArtifactId, "result_ref"),
            (self.provenance_ref, ProvenanceId, "provenance_ref"),
        ):
            _exact(reference, identifier, field)
        _fingerprint(self.configuration_fingerprint, "configuration_fingerprint")
        _fingerprint(self.run_input_fingerprint, "run_input_fingerprint")
        require_utc(self.completed_at, "completed_at")
        if self.validation_status is not ValidationStatus.NOT_VALIDATED:
            raise StrategyBacktestContractError("run cannot grant validation")
        if self.deployment_authorization is not DeploymentAuthorizationStatus.NOT_AUTHORIZED:
            raise StrategyBacktestContractError("run cannot grant deployment")
        if self.execution_state is not ExecutionState.PLANNED_CLOSED:
            raise StrategyBacktestContractError("run cannot open live execution")
