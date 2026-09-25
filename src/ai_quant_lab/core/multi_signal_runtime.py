"""Deterministic Sprint 25 multi-signal long/short research runtime.

This module is deliberately local-only and execution-closed.  It implements the
same confirmed-bar signal/risk semantics rendered by the governed Sprint 24 Pine
profile, while retaining the repository's first-eligible-next-bar-open timing
boundary and explicit cost model.
"""

from __future__ import annotations

from dataclasses import dataclass
from decimal import ROUND_HALF_EVEN, Context, Decimal, localcontext
from itertools import pairwise

from ai_quant_lab.core.experiment_contracts import (
    CostSemantics,
    ExperimentAuthorizationRecord,
    ExperimentSpecification,
    PositionSizingSemantics,
)
from ai_quant_lab.core.experiment_runner import ExperimentRunRequest
from ai_quant_lab.core.integrity import fingerprint_record
from ai_quant_lab.core.market_data import MarketBar
from ai_quant_lab.core.model import ArtifactId, ExecutionState, ObjectVersion, TraceabilityRef
from ai_quant_lab.core.research_eligibility_contracts import (
    DeploymentAuthorizationStatus,
    ValidationStatus,
)
from ai_quant_lab.core.strategy_backtest_contracts import (
    BacktestResultArtifact,
    EquityPoint,
    MultiSignalTrendParameters,
    SimulatedFill,
    SimulatedOrder,
    SimulatedOrderSide,
    SimulatedOrderStatus,
    SimulatedPositionState,
    SimulatedTrade,
    StrategyDefinition,
)

_V1 = ObjectVersion(1)
_V2 = ObjectVersion(2)
_DECIMAL_CONTEXT = Context(prec=34, rounding=ROUND_HALF_EVEN)
_BPS = Decimal(10_000)


class MultiSignalRuntimeError(ValueError):
    pass


class MultiSignalExecutionError(MultiSignalRuntimeError):
    pass


class MultiSignalMissingNextBar(MultiSignalRuntimeError):
    pass


class MultiSignalAccountingError(MultiSignalRuntimeError):
    pass


@dataclass(frozen=True, slots=True)
class MultiSignalIndicatorPoint:
    fast_ema: Decimal
    medium_ema: Decimal
    slow_ema: Decimal
    rsi: Decimal | None
    macd: Decimal
    macd_signal: Decimal
    plus_di: Decimal | None
    minus_di: Decimal | None
    adx: Decimal | None
    atr: Decimal | None

    @property
    def ready(self) -> bool:
        return (
            self.rsi is not None
            and self.plus_di is not None
            and self.minus_di is not None
            and self.adx is not None
            and self.atr is not None
        )


@dataclass(frozen=True, slots=True)
class _PendingTransition:
    target: SimulatedPositionState
    source_bar: MarketBar
    source_index: int
    fill_index: int


def _exact(record: object, object_id: object, version: ObjectVersion) -> TraceabilityRef:
    return TraceabilityRef(object_id, version, fingerprint_record(record))  # type: ignore[arg-type]


def _decimal(value: Decimal) -> str:
    if not value.is_finite():
        raise MultiSignalExecutionError("non-finite multi-signal runtime value")
    if value == 0:
        return "0"
    text = format(value, "f")
    return text.rstrip("0").rstrip(".") if "." in text else text


def _bar_ref(bar: MarketBar) -> TraceabilityRef:
    return _exact(bar, bar.bar_id, bar.version)


def _cost(semantics: CostSemantics, bps: int, notional: Decimal) -> Decimal:
    if semantics is CostSemantics.DECLARED_ZERO:
        return Decimal(0)
    if semantics is CostSemantics.DECLARED_BPS:
        return notional * Decimal(bps) / _BPS
    raise MultiSignalExecutionError("trading costs must be declared zero or declared bps")


def _execution_price(
    side: SimulatedOrderSide,
    reference: Decimal,
    semantics: CostSemantics,
    bps: int,
) -> Decimal:
    if reference <= 0:
        raise MultiSignalExecutionError("fill reference price must be positive")
    if semantics is CostSemantics.DECLARED_ZERO:
        result = reference
    elif semantics is CostSemantics.DECLARED_BPS:
        direction = Decimal(1) if side is SimulatedOrderSide.BUY else Decimal(-1)
        result = reference * (Decimal(1) + direction * Decimal(bps) / _BPS)
    else:
        raise MultiSignalExecutionError("slippage must be declared zero or declared bps")
    if result <= 0:
        raise MultiSignalExecutionError("simulated execution price must be positive")
    return result


def _ema(values: tuple[Decimal, ...], length: int) -> tuple[Decimal, ...]:
    alpha = Decimal(2) / Decimal(length + 1)
    result: list[Decimal] = []
    state: Decimal | None = None
    for value in values:
        state = value if state is None else alpha * value + (Decimal(1) - alpha) * state
        result.append(state)
    return tuple(result)


def _rma_optional(
    values: tuple[Decimal | None, ...],
    length: int,
) -> tuple[Decimal | None, ...]:
    result: list[Decimal | None] = []
    seed: list[Decimal] = []
    state: Decimal | None = None
    for value in values:
        if state is None:
            if value is None:
                result.append(None)
                continue
            seed.append(value)
            if len(seed) < length:
                result.append(None)
                continue
            state = sum(seed[-length:], Decimal(0)) / Decimal(length)
            result.append(state)
            continue
        if value is None:
            result.append(None)
            continue
        state = (state * Decimal(length - 1) + value) / Decimal(length)
        result.append(state)
    return tuple(result)


def build_multi_signal_indicators(
    bars: tuple[MarketBar, ...],
    parameters: MultiSignalTrendParameters,
) -> tuple[MultiSignalIndicatorPoint, ...]:
    """Build deterministic Decimal indicator state without future-bar access."""
    if not bars:
        raise MultiSignalExecutionError("multi-signal runtime requires at least one bar")

    with localcontext(_DECIMAL_CONTEXT):
        closes = tuple(Decimal(bar.close.text) for bar in bars)
        highs = tuple(Decimal(bar.high.text) for bar in bars)
        lows = tuple(Decimal(bar.low.text) for bar in bars)
        if any(value <= 0 for value in closes):
            raise MultiSignalExecutionError("multi-signal close prices must be positive")

        fast = _ema(closes, parameters.fast_ema)
        medium = _ema(closes, parameters.medium_ema)
        slow = _ema(closes, parameters.slow_ema)

        macd_fast = _ema(closes, parameters.macd_fast)
        macd_slow = _ema(closes, parameters.macd_slow)
        macd = tuple(a - b for a, b in zip(macd_fast, macd_slow, strict=True))
        macd_signal = _ema(macd, parameters.macd_signal)

        gains: list[Decimal | None] = [None]
        losses: list[Decimal | None] = [None]
        for previous, current in pairwise(closes):
            change = current - previous
            gains.append(max(change, Decimal(0)))
            losses.append(max(-change, Decimal(0)))
        average_gain = _rma_optional(tuple(gains), parameters.rsi_length)
        average_loss = _rma_optional(tuple(losses), parameters.rsi_length)
        rsi: list[Decimal | None] = []
        for up, down in zip(average_gain, average_loss, strict=True):
            if up is None or down is None:
                rsi.append(None)
            elif down == 0:
                rsi.append(Decimal(100))
            else:
                relative_strength = up / down
                rsi.append(Decimal(100) - Decimal(100) / (Decimal(1) + relative_strength))

        true_ranges: list[Decimal | None] = []
        plus_dm: list[Decimal | None] = []
        minus_dm: list[Decimal | None] = []
        previous_close: Decimal | None = None
        previous_high: Decimal | None = None
        previous_low: Decimal | None = None
        for high, low, close in zip(highs, lows, closes, strict=True):
            if high < low:
                raise MultiSignalExecutionError("multi-signal OHLC geometry is invalid")
            if previous_close is None:
                true_ranges.append(high - low)
                plus_dm.append(Decimal(0))
                minus_dm.append(Decimal(0))
            else:
                true_ranges.append(
                    max(
                        high - low,
                        abs(high - previous_close),
                        abs(low - previous_close),
                    )
                )
                assert previous_high is not None and previous_low is not None
                upward = high - previous_high
                downward = previous_low - low
                plus_dm.append(upward if upward > downward and upward > 0 else Decimal(0))
                minus_dm.append(downward if downward > upward and downward > 0 else Decimal(0))
            previous_close = close
            previous_high = high
            previous_low = low

        atr = _rma_optional(tuple(true_ranges), parameters.atr_length)
        smoothed_tr = _rma_optional(tuple(true_ranges), parameters.adx_length)
        smoothed_plus = _rma_optional(tuple(plus_dm), parameters.adx_length)
        smoothed_minus = _rma_optional(tuple(minus_dm), parameters.adx_length)

        plus_di: list[Decimal | None] = []
        minus_di: list[Decimal | None] = []
        dx: list[Decimal | None] = []
        for tr, plus, minus in zip(
            smoothed_tr,
            smoothed_plus,
            smoothed_minus,
            strict=True,
        ):
            if tr is None or plus is None or minus is None:
                plus_di.append(None)
                minus_di.append(None)
                dx.append(None)
                continue
            if tr == 0:
                plus_value = Decimal(0)
                minus_value = Decimal(0)
            else:
                plus_value = Decimal(100) * plus / tr
                minus_value = Decimal(100) * minus / tr
            plus_di.append(plus_value)
            minus_di.append(minus_value)
            denominator = plus_value + minus_value
            dx.append(
                Decimal(0)
                if denominator == 0
                else Decimal(100) * abs(plus_value - minus_value) / denominator
            )
        adx = _rma_optional(tuple(dx), parameters.adx_length)

        return tuple(
            MultiSignalIndicatorPoint(
                fast[index],
                medium[index],
                slow[index],
                rsi[index],
                macd[index],
                macd_signal[index],
                plus_di[index],
                minus_di[index],
                adx[index],
                atr[index],
            )
            for index in range(len(bars))
        )


def multi_signal_direction(
    bar: MarketBar,
    point: MultiSignalIndicatorPoint,
    parameters: MultiSignalTrendParameters,
) -> SimulatedPositionState:
    if not point.ready:
        return SimulatedPositionState.FLAT
    assert point.rsi is not None
    assert point.plus_di is not None
    assert point.minus_di is not None
    assert point.adx is not None
    close = Decimal(bar.close.text)
    long_signal = (
        point.fast_ema > point.medium_ema > point.slow_ema
        and close > point.slow_ema
        and point.rsi >= Decimal(parameters.rsi_long_min)
        and point.macd > point.macd_signal
        and point.adx >= Decimal(parameters.adx_threshold)
        and point.plus_di > point.minus_di
    )
    if long_signal:
        return SimulatedPositionState.LONG
    short_signal = (
        point.fast_ema < point.medium_ema < point.slow_ema
        and close < point.slow_ema
        and point.rsi <= Decimal(parameters.rsi_short_max)
        and point.macd < point.macd_signal
        and point.adx >= Decimal(parameters.adx_threshold)
        and point.minus_di > point.plus_di
    )
    return SimulatedPositionState.SHORT if short_signal else SimulatedPositionState.FLAT


def _next_fill_index(bars: tuple[MarketBar, ...], source_index: int) -> int:
    signal_time = bars[source_index].availability_time
    for index in range(source_index + 1, len(bars)):
        if bars[index].bar_open >= signal_time:
            return index
    raise MultiSignalMissingNextBar(
        "multi-signal position transition has no eligible next bar open"
    )


def _transition_side(
    position: SimulatedPositionState,
    target: SimulatedPositionState,
) -> SimulatedOrderSide:
    if position is SimulatedPositionState.FLAT and target is SimulatedPositionState.LONG:
        return SimulatedOrderSide.BUY
    if position is SimulatedPositionState.FLAT and target is SimulatedPositionState.SHORT:
        return SimulatedOrderSide.SELL
    if position is SimulatedPositionState.LONG and target is SimulatedPositionState.FLAT:
        return SimulatedOrderSide.SELL
    if position is SimulatedPositionState.SHORT and target is SimulatedPositionState.FLAT:
        return SimulatedOrderSide.BUY
    raise MultiSignalExecutionError("unsupported direct multi-signal position transition")


def simulate_multi_signal_backtest(
    base: ExperimentRunRequest,
    authorization: ExperimentAuthorizationRecord,
    specification: ExperimentSpecification,
    strategy: StrategyDefinition,
    bars: tuple[MarketBar, ...],
    run_input: str,
) -> BacktestResultArtifact:
    parameters = strategy.multi_signal
    if parameters is None:
        raise MultiSignalExecutionError("multi-signal strategy parameters are required")
    indicators = build_multi_signal_indicators(bars, parameters)
    scale = Decimal(strategy.capital_minor_unit_scale)
    strategy_ref = _exact(strategy, strategy.strategy_id, strategy.version)

    with localcontext(_DECIMAL_CONTEXT):
        initial = Decimal(specification.capital_notional_minor) / scale
        fixed_notional = Decimal(strategy.fixed_notional_minor) / scale
        cash = initial
        quantity = Decimal(0)
        position = SimulatedPositionState.FLAT
        entry_price: Decimal | None = None
        entry_fill: SimulatedFill | None = None
        entry_commission = Decimal(0)
        entry_slippage = Decimal(0)
        entry_atr: Decimal | None = None
        entry_bar_index: int | None = None
        break_even_armed = False
        realized = Decimal(0)
        pending: _PendingTransition | None = None

        orders: list[SimulatedOrder] = []
        fills: list[SimulatedFill] = []
        trades: list[SimulatedTrade] = []
        curve: list[EquityPoint] = []

        for index, (bar, point) in enumerate(zip(bars, indicators, strict=True)):
            if pending is not None and pending.fill_index == index:
                side = _transition_side(position, pending.target)
                reference = Decimal(bar.open.text)
                execution = _execution_price(
                    side,
                    reference,
                    specification.slippage_semantics,
                    specification.slippage_bps,
                )
                order_number = len(orders) + 1
                order_id = ArtifactId(f"{base.run_id.value}-simulated-order-{order_number:04d}")
                fill_id = ArtifactId(f"{base.run_id.value}-simulated-fill-{order_number:04d}")

                opening_position = position is SimulatedPositionState.FLAT
                if opening_position:
                    fill_quantity = fixed_notional / execution
                else:
                    if quantity == 0:
                        raise MultiSignalExecutionError(
                            "position close requires non-zero simulated quantity"
                        )
                    fill_quantity = abs(quantity)
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
                    raise MultiSignalExecutionError(
                        "multi-signal fill precedes governed signal availability"
                    )
                orders.append(order)
                fills.append(fill)

                if opening_position:
                    source_atr = indicators[pending.source_index].atr
                    if source_atr is None or source_atr <= 0:
                        raise MultiSignalExecutionError(
                            "entry requires a positive ATR known at signal time"
                        )
                    if pending.target is SimulatedPositionState.LONG:
                        if cash < fill_notional + commission:
                            raise MultiSignalExecutionError(
                                "insufficient simulated cash for fixed-notional long"
                            )
                        cash -= fill_notional + commission
                        quantity = fill_quantity
                    elif pending.target is SimulatedPositionState.SHORT:
                        cash += fill_notional - commission
                        quantity = -fill_quantity
                    else:
                        raise MultiSignalExecutionError("flat-to-flat transition is not supported")
                    position = pending.target
                    entry_price = execution
                    entry_fill = fill
                    entry_commission = commission
                    entry_slippage = slippage
                    entry_atr = source_atr
                    entry_bar_index = index
                    break_even_armed = False
                else:
                    if pending.target is not SimulatedPositionState.FLAT:
                        raise MultiSignalExecutionError("open position can only transition to flat")
                    if entry_price is None or entry_fill is None:
                        raise MultiSignalExecutionError("position close requires exact entry state")
                    absolute_quantity = abs(quantity)
                    if position is SimulatedPositionState.LONG:
                        if side is not SimulatedOrderSide.SELL:
                            raise MultiSignalExecutionError("long close must sell")
                        cash += fill_notional - commission
                        gross = (execution - entry_price) * absolute_quantity
                    elif position is SimulatedPositionState.SHORT:
                        if side is not SimulatedOrderSide.BUY:
                            raise MultiSignalExecutionError("short close must buy")
                        cash -= fill_notional + commission
                        gross = (entry_price - execution) * absolute_quantity
                    else:
                        raise MultiSignalExecutionError("flat position cannot execute a close")
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
                            _decimal(absolute_quantity),
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
                    position = SimulatedPositionState.FLAT
                    entry_price = None
                    entry_fill = None
                    entry_commission = Decimal(0)
                    entry_slippage = Decimal(0)
                    entry_atr = None
                    entry_bar_index = None
                    break_even_armed = False
                pending = None

            mark = Decimal(bar.close.text)
            if mark <= 0:
                raise MultiSignalExecutionError("equity mark price must be positive")
            position_value = quantity * mark
            unrealized = Decimal(0) if entry_price is None else (mark - entry_price) * quantity
            equity = cash + position_value
            if equity < 0:
                raise MultiSignalExecutionError("simulated equity cannot be negative")
            curve.append(
                EquityPoint(
                    bar.availability_time,
                    _bar_ref(bar),
                    _decimal(cash),
                    _decimal(quantity),
                    _decimal(position_value),
                    _decimal(unrealized),
                    _decimal(realized),
                    _decimal(equity),
                )
            )

            if pending is not None:
                continue

            direction = multi_signal_direction(bar, point, parameters)
            if position is SimulatedPositionState.FLAT:
                if direction in (
                    SimulatedPositionState.LONG,
                    SimulatedPositionState.SHORT,
                ):
                    pending = _PendingTransition(
                        direction,
                        bar,
                        index,
                        _next_fill_index(bars, index),
                    )
                continue

            if entry_price is None or entry_atr is None or entry_bar_index is None:
                raise MultiSignalExecutionError("open position lacks exact risk state")

            risk_distance = entry_atr * Decimal(parameters.atr_stop_mult)
            take_profit_r = Decimal(parameters.take_profit_r)
            break_even_r = Decimal(parameters.break_even_trigger_r)
            bars_in_trade = index - entry_bar_index
            high = Decimal(bar.high.text)
            low = Decimal(bar.low.text)

            if position is SimulatedPositionState.LONG:
                initial_stop = entry_price - risk_distance
                take_profit = entry_price + risk_distance * take_profit_r
                stop_touched = low <= initial_stop
                target_touched = high >= take_profit
                trigger_touched = high >= entry_price + risk_distance * break_even_r
                break_even_stop_touched = break_even_armed and low <= entry_price
                opposite_signal = direction is SimulatedPositionState.SHORT
            else:
                initial_stop = entry_price + risk_distance
                take_profit = entry_price - risk_distance * take_profit_r
                stop_touched = high >= initial_stop
                target_touched = low <= take_profit
                trigger_touched = low <= entry_price - risk_distance * break_even_r
                break_even_stop_touched = break_even_armed and high >= entry_price
                opposite_signal = direction is SimulatedPositionState.LONG

            exit_required = (
                stop_touched
                or target_touched
                or break_even_stop_touched
                or bars_in_trade >= parameters.time_stop_bars
                or opposite_signal
            )
            if exit_required:
                pending = _PendingTransition(
                    SimulatedPositionState.FLAT,
                    bar,
                    index,
                    _next_fill_index(bars, index),
                )
            elif trigger_touched:
                break_even_armed = True

        if pending is not None:
            raise MultiSignalMissingNextBar(
                "terminal multi-signal transition cannot be filled inside window"
            )

        final_equity = Decimal(curve[-1].equity)
        gross_pnl = sum(
            (Decimal(trade.gross_pnl) for trade in trades),
            Decimal(0),
        )
        net_pnl = sum(
            (Decimal(trade.net_pnl) for trade in trades),
            Decimal(0),
        )
        total_return = final_equity / initial - Decimal(1)
        peak = initial
        max_drawdown = Decimal(0)
        for point in curve:
            point_equity = Decimal(point.equity)
            peak = max(peak, point_equity)
            if peak <= 0:
                raise MultiSignalExecutionError("drawdown peak must remain positive")
            max_drawdown = max(
                max_drawdown,
                Decimal(1) - point_equity / peak,
            )

    return BacktestResultArtifact(
        base.result_artifact_id,
        _V2,
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
        _V2,
    )


def _match(actual: Decimal, expected: Decimal, message: str) -> None:
    if actual != expected:
        raise MultiSignalAccountingError(message)


def verify_multi_signal_backtest_accounting(
    *,
    artifact: BacktestResultArtifact,
    specification: ExperimentSpecification,
    strategy: StrategyDefinition,
    bars: tuple[MarketBar, ...],
) -> None:
    """Independently reconstruct long/short cash, positions, trades and equity."""
    if specification.sizing_semantics is not PositionSizingSemantics.FIXED_NOTIONAL:
        raise MultiSignalAccountingError("multi-signal accounting supports FIXED_NOTIONAL only")
    if not bars or len(artifact.equity_curve) != len(bars):
        raise MultiSignalAccountingError(
            "equity curve must bind every governed replay bar exactly once"
        )
    if (
        artifact.capital_currency != strategy.capital_currency
        or artifact.capital_minor_unit_scale != strategy.capital_minor_unit_scale
    ):
        raise MultiSignalAccountingError(
            "result denomination does not match exact multi-signal strategy"
        )

    bar_refs = tuple(_bar_ref(bar) for bar in bars)
    if tuple(point.bar_ref for point in artifact.equity_curve) != bar_refs:
        raise MultiSignalAccountingError(
            "equity curve bar bindings do not match governed replay order"
        )
    bars_by_ref = dict(zip(bar_refs, bars, strict=True))
    indexes = {reference: index for index, reference in enumerate(bar_refs)}
    strategy_ref = _exact(strategy, strategy.strategy_id, strategy.version)

    fills_by_order: dict[ArtifactId, SimulatedFill] = {}
    fills_by_id: dict[ArtifactId, SimulatedFill] = {}
    fills_by_bar: dict[TraceabilityRef, SimulatedFill] = {}
    for fill in artifact.fills:
        if fill.order_id in fills_by_order or fill.bar_ref in fills_by_bar:
            raise MultiSignalAccountingError("multi-signal ledger contains duplicate fill binding")
        fills_by_order[fill.order_id] = fill
        fills_by_id[fill.fill_id] = fill
        fills_by_bar[fill.bar_ref] = fill

    with localcontext(_DECIMAL_CONTEXT):
        prior_fill_time = None
        for order in artifact.orders:
            fill = fills_by_order.get(order.order_id)
            if fill is None:
                raise MultiSignalAccountingError("simulated order has no matching fill")
            source_bar = bars_by_ref.get(order.source_bar_ref)
            fill_bar = bars_by_ref.get(order.fill_bar_ref)
            if source_bar is None or fill_bar is None:
                raise MultiSignalAccountingError("order references a bar outside governed replay")
            if (
                order.side is not fill.side
                or order.strategy_ref != strategy_ref
                or order.fill_bar_ref != fill.bar_ref
                or order.signal_time != source_bar.availability_time
                or order.submitted_time != order.signal_time
                or order.eligible_fill_time != fill.fill_time
                or fill.fill_time != fill_bar.bar_open
                or indexes[order.source_bar_ref] >= indexes[order.fill_bar_ref]
            ):
                raise MultiSignalAccountingError(
                    "order/fill identity or temporal binding is inconsistent"
                )
            if prior_fill_time is not None and fill.fill_time <= prior_fill_time:
                raise MultiSignalAccountingError("fills must be strictly time ordered")
            prior_fill_time = fill.fill_time

            reference = Decimal(fill.reference_price)
            execution = Decimal(fill.execution_price)
            quantity = Decimal(fill.quantity)
            notional = Decimal(fill.fill_notional)
            if reference != Decimal(fill_bar.open.text):
                raise MultiSignalAccountingError(
                    "fill reference price does not match exact fill bar open"
                )
            expected_execution = _execution_price(
                fill.side,
                reference,
                specification.slippage_semantics,
                specification.slippage_bps,
            )
            _match(execution, expected_execution, "fill execution price is inconsistent")
            _match(notional, execution * quantity, "fill notional is inconsistent")
            _match(
                Decimal(order.notional),
                notional,
                "order notional does not match its fill",
            )
            expected_commission = _cost(
                specification.commission_semantics,
                specification.commission_bps,
                notional,
            )
            _match(
                Decimal(fill.commission),
                expected_commission,
                "fill commission is inconsistent",
            )
            _match(
                Decimal(fill.slippage_cost),
                abs(execution - reference) * quantity,
                "fill slippage cost is inconsistent",
            )

        if set(fills_by_order) != {order.order_id for order in artifact.orders}:
            raise MultiSignalAccountingError("backtest ledger contains an orphan fill")

        trade_by_pair: dict[tuple[ArtifactId, ArtifactId], SimulatedTrade] = {}
        participating: set[ArtifactId] = set()
        for trade in artifact.trades:
            entry = fills_by_id.get(trade.entry_fill_id)
            exit_fill = fills_by_id.get(trade.exit_fill_id)
            if entry is None or exit_fill is None:
                raise MultiSignalAccountingError("trade references an unknown fill")
            if trade.entry_fill_id in participating or trade.exit_fill_id in participating:
                raise MultiSignalAccountingError("a fill participates in multiple completed trades")
            if entry.side is exit_fill.side:
                raise MultiSignalAccountingError(
                    "completed trade must use opposite entry and exit sides"
                )
            participating.update((trade.entry_fill_id, trade.exit_fill_id))
            quantity = Decimal(trade.quantity)
            _match(quantity, Decimal(entry.quantity), "trade entry quantity is inconsistent")
            _match(
                quantity,
                Decimal(exit_fill.quantity),
                "trade exit quantity is inconsistent",
            )
            _match(
                Decimal(trade.entry_price),
                Decimal(entry.execution_price),
                "trade entry price is inconsistent",
            )
            _match(
                Decimal(trade.exit_price),
                Decimal(exit_fill.execution_price),
                "trade exit price is inconsistent",
            )
            gross = (
                (Decimal(exit_fill.execution_price) - Decimal(entry.execution_price)) * quantity
                if entry.side is SimulatedOrderSide.BUY
                else (Decimal(entry.execution_price) - Decimal(exit_fill.execution_price))
                * quantity
            )
            commission = Decimal(entry.commission) + Decimal(exit_fill.commission)
            slippage = Decimal(entry.slippage_cost) + Decimal(exit_fill.slippage_cost)
            _match(Decimal(trade.gross_pnl), gross, "trade gross PnL is inconsistent")
            _match(
                Decimal(trade.commission),
                commission,
                "trade commission is inconsistent",
            )
            _match(
                Decimal(trade.slippage_cost),
                slippage,
                "trade slippage cost is inconsistent",
            )
            _match(
                Decimal(trade.net_pnl),
                gross - commission,
                "trade net PnL is inconsistent",
            )
            trade_by_pair[(entry.fill_id, exit_fill.fill_id)] = trade

        initial = Decimal(specification.capital_notional_minor) / Decimal(
            strategy.capital_minor_unit_scale
        )
        fixed_notional = Decimal(strategy.fixed_notional_minor) / Decimal(
            strategy.capital_minor_unit_scale
        )
        _match(
            Decimal(artifact.initial_capital),
            initial,
            "initial capital is inconsistent",
        )
        cash = initial
        signed_quantity = Decimal(0)
        entry_fill: SimulatedFill | None = None
        realized = Decimal(0)
        used_trades: set[ArtifactId] = set()

        for bar, point in zip(bars, artifact.equity_curve, strict=True):
            fill = fills_by_bar.get(_bar_ref(bar))
            if fill is not None:
                quantity = Decimal(fill.quantity)
                notional = Decimal(fill.fill_notional)
                commission = Decimal(fill.commission)
                if signed_quantity == 0:
                    _match(
                        notional,
                        fixed_notional,
                        "entry fill does not match governed fixed notional",
                    )
                    if fill.side is SimulatedOrderSide.BUY:
                        cash -= notional + commission
                        signed_quantity = quantity
                    else:
                        cash += notional - commission
                        signed_quantity = -quantity
                    entry_fill = fill
                else:
                    if entry_fill is None:
                        raise MultiSignalAccountingError("open position has no exact entry fill")
                    if signed_quantity > 0:
                        if fill.side is not SimulatedOrderSide.SELL:
                            raise MultiSignalAccountingError("long position must close with SELL")
                    elif fill.side is not SimulatedOrderSide.BUY:
                        raise MultiSignalAccountingError("short position must close with BUY")
                    _match(
                        quantity,
                        abs(signed_quantity),
                        "exit quantity does not close exact position quantity",
                    )
                    trade = trade_by_pair.get((entry_fill.fill_id, fill.fill_id))
                    if trade is None:
                        raise MultiSignalAccountingError(
                            "completed position has no exact trade ledger entry"
                        )
                    if signed_quantity > 0:
                        cash += notional - commission
                    else:
                        cash -= notional + commission
                    realized += Decimal(trade.net_pnl)
                    used_trades.add(trade.trade_id)
                    signed_quantity = Decimal(0)
                    entry_fill = None

            mark = Decimal(bar.close.text)
            position_value = signed_quantity * mark
            entry_price = None if entry_fill is None else Decimal(entry_fill.execution_price)
            unrealized = (
                Decimal(0) if entry_price is None else (mark - entry_price) * signed_quantity
            )
            equity = cash + position_value
            if point.event_time != bar.availability_time:
                raise MultiSignalAccountingError(
                    "equity event time does not match exact governed bar"
                )
            for actual, expected, message in (
                (Decimal(point.cash), cash, "equity cash transition is inconsistent"),
                (
                    Decimal(point.position_quantity),
                    signed_quantity,
                    "equity position quantity is inconsistent",
                ),
                (
                    Decimal(point.position_value),
                    position_value,
                    "equity position value is inconsistent",
                ),
                (
                    Decimal(point.unrealized_pnl),
                    unrealized,
                    "equity unrealized PnL is inconsistent",
                ),
                (
                    Decimal(point.realized_pnl),
                    realized,
                    "equity realized PnL is inconsistent",
                ),
                (Decimal(point.equity), equity, "equity identity is inconsistent"),
            ):
                _match(actual, expected, message)

        if used_trades != {trade.trade_id for trade in artifact.trades}:
            raise MultiSignalAccountingError(
                "trade ledger does not match reconstructed position cycles"
            )
        if signed_quantity > 0:
            expected_position = SimulatedPositionState.LONG
        elif signed_quantity < 0:
            expected_position = SimulatedPositionState.SHORT
        else:
            expected_position = SimulatedPositionState.FLAT
        if artifact.open_position is not expected_position:
            raise MultiSignalAccountingError("final open-position state is inconsistent")
        unresolved = {fill.fill_id for fill in artifact.fills} - participating
        if expected_position is SimulatedPositionState.FLAT:
            if unresolved:
                raise MultiSignalAccountingError("flat result contains an unresolved position fill")
        elif entry_fill is None or unresolved != {entry_fill.fill_id}:
            raise MultiSignalAccountingError(
                "open position must have exactly one unresolved entry fill"
            )

        final_equity = cash + signed_quantity * Decimal(bars[-1].close.text)
        _match(Decimal(artifact.final_cash), cash, "final cash is inconsistent")
        _match(
            Decimal(artifact.final_equity),
            final_equity,
            "final equity is inconsistent",
        )
        gross = sum(
            (Decimal(trade.gross_pnl) for trade in artifact.trades),
            Decimal(0),
        )
        net = sum(
            (Decimal(trade.net_pnl) for trade in artifact.trades),
            Decimal(0),
        )
        _match(Decimal(artifact.gross_pnl), gross, "gross PnL summary is inconsistent")
        _match(Decimal(artifact.net_pnl), net, "net PnL summary is inconsistent")
        if artifact.trade_count != len(artifact.trades):
            raise MultiSignalAccountingError("trade count summary is inconsistent")
        _match(
            Decimal(artifact.total_return),
            final_equity / initial - Decimal(1),
            "total return summary is inconsistent",
        )
        peak = initial
        drawdown = Decimal(0)
        for point in artifact.equity_curve:
            equity = Decimal(point.equity)
            peak = max(peak, equity)
            if peak <= 0:
                raise MultiSignalAccountingError("drawdown peak must remain positive")
            drawdown = max(drawdown, Decimal(1) - equity / peak)
        _match(
            Decimal(artifact.max_drawdown),
            drawdown,
            "max drawdown summary is inconsistent",
        )
