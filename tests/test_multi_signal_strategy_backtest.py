"""Sprint 25 governed multi-signal Python backtest runtime tests."""

from __future__ import annotations

import ast
import inspect
from dataclasses import replace
from datetime import UTC, datetime, timedelta
from decimal import ROUND_HALF_EVEN, Context, Decimal, localcontext
from pathlib import Path
from typing import Any

import pytest
from test_real_csv_onboarding import HEADER
from test_strategy_backtest import (
    authorized_context,
    strategy_configuration,
)

from ai_quant_lab import EXE_01
from ai_quant_lab.core import multi_signal_runtime as runtime_module
from ai_quant_lab.core.data import DecimalValue
from ai_quant_lab.core.experiment_authorization import (
    ExperimentAuthorizationRequest,
    authorize_experiment,
)
from ai_quant_lab.core.experiment_contracts import ExperimentAuthorizationDecision
from ai_quant_lab.core.experiment_runner import ExperimentRunRequest
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
from ai_quant_lab.core.multi_signal_runtime import (
    MultiSignalIndicatorPoint,
    MultiSignalMissingNextBar,
    build_multi_signal_indicators,
    multi_signal_direction,
    simulate_multi_signal_backtest,
)
from ai_quant_lab.core.research_eligibility_contracts import DeploymentAuthorizationStatus
from ai_quant_lab.core.strategy_backtest import (
    AccountingMismatch,
    BacktestLineageMismatch,
    StrategyBacktestResult,
    StrategyBacktestRunRequest,
    multi_signal_strategy_backtest_engine_ref,
    multi_signal_strategy_backtest_replay_contract,
    run_authorized_strategy_backtest,
    verify_strategy_backtest_lineage,
)
from ai_quant_lab.core.strategy_backtest_contracts import (
    MultiSignalTrendParameters,
    SidePermission,
    SignalTiming,
    SimulatedExecutionTiming,
    SimulatedOrderSide,
    SimulatedPositionState,
    StrategyDefinition,
    StrategyModel,
)

V1 = ObjectVersion(1)
V2 = ObjectVersion(2)
COMPLETED_AT = datetime(2025, 2, 3, 1, tzinfo=UTC)
PROVENANCE_REF = TraceabilityRef(
    ProvenanceId("sprint-25-multi-signal-backtest"),
    V1,
    "sha256:" + "c" * 64,
)


def parameters(
    *,
    atr_stop_mult: str = "100",
    take_profit_r: str = "100",
    break_even_trigger_r: str = "100",
    time_stop_bars: int = 100,
    ema_separation_min_pct: str = "0",
    adx_slope_length: int = 0,
    atr_pct_min: str = "0",
    atr_pct_max: str = "100",
) -> MultiSignalTrendParameters:
    return MultiSignalTrendParameters(
        2,
        3,
        4,
        2,
        "55",
        "45",
        2,
        4,
        2,
        2,
        "5",
        2,
        atr_stop_mult,
        take_profit_r,
        break_even_trigger_r,
        time_stop_bars,
        ema_separation_min_pct,
        adx_slope_length,
        atr_pct_min,
        atr_pct_max,
    )


def strategy(
    *,
    params: MultiSignalTrendParameters | None = None,
) -> StrategyDefinition:
    return StrategyDefinition(
        ArtifactId("solusdt-4h-multi-signal-runtime-v1"),
        V2,
        StrategyModel.MULTI_SIGNAL_TREND_LONG_SHORT,
        SignalTiming.BAR_CLOSE_AFTER_AVAILABILITY,
        SimulatedExecutionTiming.FIRST_ELIGIBLE_NEXT_BAR_OPEN,
        SidePermission.LONG_SHORT,
        0,
        10_000,
        "USD",
        100,
        False,
        False,
        multi_signal_strategy_backtest_engine_ref(),
        TraceabilityRef(
            ProvenanceId("sprint-25-strategy-definition"),
            V1,
            "sha256:" + "d" * 64,
        ),
        V2,
        parameters() if params is None else params,
    )


def _trend_csv() -> str:
    closes = (
        101,
        103,
        105,
        107,
        109,
        111,
        113,
        111,
        109,
        107,
        105,
        103,
        101,
        99,
        101,
        103,
        105,
        107,
        109,
        111,
        113,
        113,
        113,
    )
    rows: list[str] = []
    prior = 100
    start = datetime(2025, 2, 1, tzinfo=UTC)
    for index, close in enumerate(closes):
        opened = start + timedelta(hours=index)
        closed = opened + timedelta(hours=1)
        availability = closed + timedelta(seconds=5)
        high = max(prior, close) + 1
        low = min(prior, close) - 1
        rows.append(
            f"{opened.strftime('%Y-%m-%dT%H:%M:%S.000000Z')},"
            f"{closed.strftime('%Y-%m-%dT%H:%M:%S.000000Z')},"
            f"{prior},{high},{low},{close},{100 + index},final,"
            f"{availability.strftime('%Y-%m-%dT%H:%M:%S.000000Z')}\n"
        )
        prior = close
    return HEADER + "".join(rows)


def _multi_context(
    tmp_path: Path,
    *,
    params: MultiSignalTrendParameters | None = None,
    warmup_bars: int = 0,
    csv_text: str | None = None,
    pullback: bool = False,
) -> tuple[Any, ...]:
    base = authorized_context(
        tmp_path,
        suffix="sprint-25-multi",
        csv_text=_trend_csv() if csv_text is None else csv_text,
    )
    (
        declaration,
        repository,
        admission,
        report,
        eligibility_policy,
        eligibility,
        _legacy_strategy,
        legacy_specification,
        legacy_policy,
        _legacy_authorization,
        instrument,
    ) = base
    definition = strategy(params=params)
    engine = multi_signal_strategy_backtest_replay_contract()
    engine_ref = multi_signal_strategy_backtest_engine_ref()
    if pullback:
        from ai_quant_lab.core.strategy_backtest import (
            pullback_strategy_backtest_engine_ref,
            pullback_strategy_backtest_replay_contract,
        )

        engine = pullback_strategy_backtest_replay_contract()
        engine_ref = pullback_strategy_backtest_engine_ref()
        definition = replace(
            definition,
            model=StrategyModel.MULTI_SIGNAL_PULLBACK_LONG_SHORT,
            engine_contract_ref=engine_ref,
        )
    specification = replace(
        legacy_specification,
        experiment_id=ExperimentId("sprint-25-multi-signal-experiment"),
        research_objective=(
            "Exercise deterministic EMA/RSI/MACD/ADX long-short timing and risk controls."
        ),
        configuration=strategy_configuration(definition),
        observation_start=report.normalized_bars[0].bar_open,
        observation_end=report.normalized_bars[-1].bar_close,
        knowledge_cutoff=datetime(2025, 2, 2, tzinfo=UTC),
        engine_contract_ref=engine_ref,
        warmup_bars=warmup_bars,
    )
    policy = replace(
        legacy_policy,
        policy_id=ArtifactId("sprint-25-multi-signal-authorization-policy"),
        supported_engine_refs=(engine_ref,),
    )
    authorization = authorize_experiment(
        ExperimentAuthorizationRequest(
            ArtifactId("sprint-25-multi-signal-authorization"),
            specification,
            policy,
            datetime(2025, 2, 3, tzinfo=UTC),
            AgentId("experiment-authorizer"),
        ),
        eligibility=eligibility,
        eligibility_policy=eligibility_policy,
        admission=admission,
        declaration=declaration,
        report=report,
        repository=repository,
    )
    request = StrategyBacktestRunRequest(
        ExperimentRunRequest(
            RunId("sprint-25-multi-signal-backtest-run"),
            ArtifactId("sprint-25-multi-signal-backtest-result"),
            TraceabilityRef(
                authorization.record.authorization_id,
                authorization.record.version,
                fingerprint_record(authorization.record),
            ),
            TraceabilityRef(
                specification.experiment_id,
                specification.version,
                fingerprint_record(specification),
            ),
            TraceabilityRef(
                policy.policy_id,
                policy.version,
                fingerprint_record(policy),
            ),
            TraceabilityRef(
                eligibility.eligibility_id,
                eligibility.version,
                fingerprint_record(eligibility),
            ),
            engine_ref,
            COMPLETED_AT,
            PROVENANCE_REF,
        ),
        TraceabilityRef(
            definition.strategy_id,
            definition.version,
            fingerprint_record(definition),
        ),
    )
    return (
        declaration,
        repository,
        admission,
        report,
        eligibility_policy,
        eligibility,
        definition,
        specification,
        policy,
        authorization,
        instrument,
        engine,
        request,
    )


def _execute(context: tuple[Any, ...]) -> StrategyBacktestResult:
    (
        declaration,
        repository,
        admission,
        report,
        eligibility_policy,
        eligibility,
        definition,
        specification,
        policy,
        authorization,
        instrument,
        engine,
        request,
    ) = context
    assert authorization.record.status is ExperimentAuthorizationDecision.AUTHORIZED
    return run_authorized_strategy_backtest(
        request,
        authorization=authorization.record,
        specification=specification,
        policy=policy,
        eligibility=eligibility,
        eligibility_policy=eligibility_policy,
        admission=admission,
        declaration=declaration,
        report=report,
        engine_contract=engine,
        strategy=definition,
        instrument=instrument,
        repository=repository,
    )


def test_indicator_state_is_deterministic_and_emits_both_directions(tmp_path: Path) -> None:
    context = _multi_context(tmp_path)
    report = context[3]
    definition = context[6]
    points_a = build_multi_signal_indicators(
        report.normalized_bars,
        definition.multi_signal,
    )
    points_b = build_multi_signal_indicators(
        report.normalized_bars,
        definition.multi_signal,
    )

    assert points_a == points_b
    directions = tuple(
        multi_signal_direction(bar, point, definition.multi_signal)
        for bar, point in zip(report.normalized_bars, points_a, strict=True)
    )
    assert SimulatedPositionState.LONG in directions
    assert SimulatedPositionState.SHORT in directions
    assert all(point.atr is None or point.atr >= 0 for point in points_a)


def test_regime_filters_gate_signal_deterministically(tmp_path: Path) -> None:
    context = _multi_context(tmp_path)
    bar = replace(
        context[3].normalized_bars[-1],
        open=DecimalValue("108"),
        high=DecimalValue("111"),
        low=DecimalValue("99"),
        close=DecimalValue("110"),
    )
    point = MultiSignalIndicatorPoint(
        Decimal("110"),
        Decimal("105"),
        Decimal("100"),
        Decimal("65"),
        Decimal("2"),
        Decimal("1"),
        Decimal("30"),
        Decimal("10"),
        Decimal("25"),
        Decimal("2"),
    )
    filtered = replace(
        parameters(),
        ema_separation_min_pct="5",
        adx_slope_length=2,
        atr_pct_min="1",
        atr_pct_max="3",
    )

    assert (
        multi_signal_direction(bar, point, filtered, Decimal("20")) is SimulatedPositionState.LONG
    )
    assert (
        multi_signal_direction(
            bar,
            point,
            replace(filtered, ema_separation_min_pct="10"),
            Decimal("20"),
        )
        is SimulatedPositionState.FLAT
    )
    assert (
        multi_signal_direction(
            bar,
            point,
            replace(filtered, atr_pct_min="2"),
            Decimal("20"),
        )
        is SimulatedPositionState.FLAT
    )
    assert (
        multi_signal_direction(bar, point, filtered, Decimal("26")) is SimulatedPositionState.FLAT
    )
    assert multi_signal_direction(bar, point, filtered, None) is SimulatedPositionState.FLAT


def test_governed_backtest_executes_completed_long_and_short_cycles(tmp_path: Path) -> None:
    context = _multi_context(tmp_path)
    result = _execute(context)
    artifact = result.artifact
    fills = {fill.fill_id: fill for fill in artifact.fills}

    completed_sides = tuple(
        (fills[trade.entry_fill_id].side, fills[trade.exit_fill_id].side)
        for trade in artifact.trades
    )
    assert (SimulatedOrderSide.BUY, SimulatedOrderSide.SELL) in completed_sides
    assert (SimulatedOrderSide.SELL, SimulatedOrderSide.BUY) in completed_sides
    assert any(point.position_quantity.startswith("-") for point in artifact.equity_curve)
    assert all(
        order.signal_time < fill.fill_time
        for order, fill in zip(artifact.orders, artifact.fills, strict=True)
    )
    assert artifact.deployment_authorization is DeploymentAuthorizationStatus.NOT_AUTHORIZED
    assert artifact.execution_state is ExecutionState.PLANNED_CLOSED
    assert EXE_01.state is ExecutionState.PLANNED_CLOSED


def test_short_accounting_uses_signed_position_value_and_exact_cash_identity(
    tmp_path: Path,
) -> None:
    result = _execute(_multi_context(tmp_path))
    short_points = [
        point for point in result.artifact.equity_curve if Decimal(point.position_quantity) < 0
    ]
    assert short_points
    for point in short_points:
        assert Decimal(point.position_value) < 0
        with localcontext(Context(prec=34, rounding=ROUND_HALF_EVEN)):
            assert Decimal(point.equity) == Decimal(point.cash) + Decimal(point.position_value)


def _scripted_risk_run(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    *,
    position: SimulatedPositionState,
    params: MultiSignalTrendParameters,
    trigger_bar: int | None = None,
    trigger_high: str = "100",
    trigger_low: str = "100",
    bar_count: int = 8,
    warmup_bars: int = 0,
) -> tuple[Any, tuple[Any, ...]]:
    context = _multi_context(tmp_path, params=params, warmup_bars=warmup_bars)
    report = context[3]
    bars = tuple(
        replace(
            bar,
            open=DecimalValue("100"),
            high=DecimalValue("100"),
            low=DecimalValue("100"),
            close=DecimalValue("100"),
        )
        for bar in report.normalized_bars[:bar_count]
    )
    if trigger_bar is not None:
        changed = list(bars)
        changed[trigger_bar] = replace(
            changed[trigger_bar],
            high=DecimalValue(trigger_high),
            low=DecimalValue(trigger_low),
        )
        bars = tuple(changed)

    point = MultiSignalIndicatorPoint(
        Decimal("1"),
        Decimal("1"),
        Decimal("1"),
        None,
        Decimal("0"),
        Decimal("0"),
        None,
        None,
        None,
        Decimal("1"),
    )
    points = tuple(point for _ in bars)
    signal_bar_id = bars[warmup_bars].bar_id
    monkeypatch.setattr(
        runtime_module,
        "build_multi_signal_indicators",
        lambda _bars, _parameters: points,
    )
    monkeypatch.setattr(
        runtime_module,
        "multi_signal_direction",
        lambda bar, _point, _parameters: (
            position if bar.bar_id == signal_bar_id else SimulatedPositionState.FLAT
        ),
    )

    artifact = simulate_multi_signal_backtest(
        context[12].experiment_run,
        context[9].record,
        context[7],
        context[6],
        bars,
        "sha256:" + "9" * 64,
    )
    return artifact, bars


@pytest.mark.parametrize(
    ("position", "trigger_high", "trigger_low", "exit_side"),
    (
        (SimulatedPositionState.LONG, "100", "97", SimulatedOrderSide.SELL),
        (SimulatedPositionState.SHORT, "103", "100", SimulatedOrderSide.BUY),
    ),
)
def test_atr_stop_exits_long_and_short_on_first_eligible_later_open(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    position: SimulatedPositionState,
    trigger_high: str,
    trigger_low: str,
    exit_side: SimulatedOrderSide,
) -> None:
    artifact, bars = _scripted_risk_run(
        tmp_path,
        monkeypatch,
        position=position,
        params=parameters(
            atr_stop_mult="2",
            take_profit_r="100",
            break_even_trigger_r="100",
            time_stop_bars=100,
        ),
        trigger_bar=3,
        trigger_high=trigger_high,
        trigger_low=trigger_low,
    )

    assert len(artifact.orders) == 2
    assert artifact.orders[1].side is exit_side
    assert artifact.orders[1].source_bar_ref.object_id == bars[3].bar_id
    assert artifact.fills[1].bar_ref.object_id == bars[5].bar_id
    assert artifact.fills[1].fill_time >= artifact.orders[1].signal_time


@pytest.mark.parametrize(
    ("position", "trigger_high", "trigger_low", "exit_side"),
    (
        (SimulatedPositionState.LONG, "103", "100", SimulatedOrderSide.SELL),
        (SimulatedPositionState.SHORT, "100", "97", SimulatedOrderSide.BUY),
    ),
)
def test_take_profit_exits_long_and_short_on_first_eligible_later_open(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    position: SimulatedPositionState,
    trigger_high: str,
    trigger_low: str,
    exit_side: SimulatedOrderSide,
) -> None:
    artifact, bars = _scripted_risk_run(
        tmp_path,
        monkeypatch,
        position=position,
        params=parameters(
            atr_stop_mult="2",
            take_profit_r="1",
            break_even_trigger_r="100",
            time_stop_bars=100,
        ),
        trigger_bar=3,
        trigger_high=trigger_high,
        trigger_low=trigger_low,
    )

    assert len(artifact.orders) == 2
    assert artifact.orders[1].side is exit_side
    assert artifact.orders[1].source_bar_ref.object_id == bars[3].bar_id
    assert artifact.fills[1].bar_ref.object_id == bars[5].bar_id


@pytest.mark.parametrize(
    ("position", "trigger_high", "trigger_low", "exit_side"),
    (
        (SimulatedPositionState.LONG, "103", "100", SimulatedOrderSide.SELL),
        (SimulatedPositionState.SHORT, "100", "97", SimulatedOrderSide.BUY),
    ),
)
def test_break_even_arms_then_exits_only_on_a_later_completed_bar(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    position: SimulatedPositionState,
    trigger_high: str,
    trigger_low: str,
    exit_side: SimulatedOrderSide,
) -> None:
    artifact, bars = _scripted_risk_run(
        tmp_path,
        monkeypatch,
        position=position,
        params=parameters(
            atr_stop_mult="2",
            take_profit_r="100",
            break_even_trigger_r="1",
            time_stop_bars=100,
        ),
        trigger_bar=3,
        trigger_high=trigger_high,
        trigger_low=trigger_low,
    )

    assert len(artifact.orders) == 2
    assert artifact.orders[1].side is exit_side
    assert artifact.orders[1].source_bar_ref.object_id == bars[4].bar_id
    assert artifact.fills[1].bar_ref.object_id == bars[6].bar_id


@pytest.mark.parametrize(
    ("position", "exit_side"),
    (
        (SimulatedPositionState.LONG, SimulatedOrderSide.SELL),
        (SimulatedPositionState.SHORT, SimulatedOrderSide.BUY),
    ),
)
def test_time_stop_counts_completed_bars_from_actual_fill_bar(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    position: SimulatedPositionState,
    exit_side: SimulatedOrderSide,
) -> None:
    artifact, bars = _scripted_risk_run(
        tmp_path,
        monkeypatch,
        position=position,
        params=parameters(
            atr_stop_mult="100",
            take_profit_r="100",
            break_even_trigger_r="100",
            time_stop_bars=1,
        ),
    )

    assert artifact.fills[0].bar_ref.object_id == bars[2].bar_id
    assert artifact.orders[1].side is exit_side
    assert artifact.orders[1].source_bar_ref.object_id == bars[3].bar_id
    assert artifact.fills[1].bar_ref.object_id == bars[5].bar_id


@pytest.mark.parametrize("warmup", (0, 1))
def test_terminal_risk_exit_without_eligible_later_open_fails_closed(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    warmup: int,
) -> None:
    with pytest.raises(MultiSignalMissingNextBar):
        _scripted_risk_run(
            tmp_path,
            monkeypatch,
            position=SimulatedPositionState.LONG,
            params=parameters(
                atr_stop_mult="2",
                take_profit_r="100",
                break_even_trigger_r="100",
                time_stop_bars=100,
            ),
            trigger_bar=4,
            trigger_high="100",
            trigger_low="97",
            bar_count=5,
            warmup_bars=warmup,
        )


def test_multi_signal_result_is_deterministic_and_exactly_verifiable(tmp_path: Path) -> None:
    context = _multi_context(tmp_path)
    first = _execute(context)
    second = _execute(context)
    assert first.artifact == second.artifact
    assert first.record == second.record

    (
        _declaration,
        _repository,
        _admission,
        report,
        _eligibility_policy,
        eligibility,
        definition,
        specification,
        policy,
        authorization,
        instrument,
        engine,
        request,
    ) = context
    verify_strategy_backtest_lineage(
        record=first.record,
        artifact=first.artifact,
        request=request,
        authorization=authorization.record,
        specification=specification,
        policy=policy,
        eligibility=eligibility,
        engine_contract=engine,
        strategy=definition,
        instrument=instrument,
        report=report,
    )


def test_tampered_short_equity_fails_independent_accounting(tmp_path: Path) -> None:
    context = _multi_context(tmp_path)
    result = _execute(context)
    artifact = result.artifact
    short_index = next(
        index
        for index, point in enumerate(artifact.equity_curve)
        if Decimal(point.position_quantity) < 0
    )
    changed_points = list(artifact.equity_curve)
    changed_points[short_index] = replace(
        changed_points[short_index],
        position_value="0",
        equity=changed_points[short_index].cash,
    )

    (
        _declaration,
        _repository,
        _admission,
        report,
        _eligibility_policy,
        eligibility,
        definition,
        specification,
        policy,
        authorization,
        instrument,
        engine,
        request,
    ) = context
    with pytest.raises((ValueError, AccountingMismatch, BacktestLineageMismatch)):
        changed = replace(artifact, equity_curve=tuple(changed_points))
        verify_strategy_backtest_lineage(
            record=result.record,
            artifact=changed,
            request=request,
            authorization=authorization.record,
            specification=specification,
            policy=policy,
            eligibility=eligibility,
            engine_contract=engine,
            strategy=definition,
            instrument=instrument,
            report=report,
        )


def test_wrong_engine_profile_fails_closed(tmp_path: Path) -> None:
    context = _multi_context(tmp_path)
    changed = list(context)
    from ai_quant_lab.core.strategy_backtest import strategy_backtest_replay_contract

    changed[11] = strategy_backtest_replay_contract()
    with pytest.raises(ValueError):
        _execute(tuple(changed))


def test_multi_signal_runtime_has_no_optimizer_network_or_live_execution_capability() -> None:
    tree = ast.parse(inspect.getsource(runtime_module))
    imported = {
        alias.name.split(".")[0]
        for node in ast.walk(tree)
        if isinstance(node, (ast.Import, ast.ImportFrom))
        for alias in node.names
    }
    assert not imported.intersection(
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


def test_governed_warmup_preserves_indicator_history_and_suppresses_orders(tmp_path: Path) -> None:
    context = _multi_context(tmp_path, warmup_bars=9)
    result = _execute(context)
    bars = context[3].normalized_bars
    artifact = result.artifact
    indexes = {bar.bar_id: i for i, bar in enumerate(bars)}
    assert artifact.orders
    assert all(indexes[order.source_bar_ref.object_id] >= 9 for order in artifact.orders)
    assert all(indexes[fill.bar_ref.object_id] >= 10 for fill in artifact.fills)
    assert len(artifact.equity_curve) == len(bars)
    for point in artifact.equity_curve[:10]:
        assert Decimal(point.position_quantity) == 0
        assert Decimal(point.realized_pnl) == 0
        assert Decimal(point.unrealized_pnl) == 0
        assert Decimal(point.equity) == Decimal(context[7].capital_notional_minor) / 100
    assert context[6].multi_signal is not None
    full = build_multi_signal_indicators(bars, context[6].multi_signal)
    sliced = build_multi_signal_indicators(bars[9:], context[6].multi_signal)
    assert full[9] != sliced[0]
    expected_direction = multi_signal_direction(bars[9], full[9], context[6].multi_signal)
    first = artifact.orders[0]
    assert indexes[first.source_bar_ref.object_id] == 9
    assert first.side is (
        SimulatedOrderSide.BUY
        if expected_direction is SimulatedPositionState.LONG
        else SimulatedOrderSide.SELL
    )


@pytest.mark.parametrize("warmup", (22, 23, 1000))
def test_warmup_without_signal_and_fill_capacity_fails_closed(tmp_path: Path, warmup: int) -> None:
    from ai_quant_lab.core.strategy_backtest import StrategyBacktestError

    context = _multi_context(tmp_path, warmup_bars=warmup)
    assert len(context[3].normalized_bars) == 23
    with pytest.raises(StrategyBacktestError, match="warmup must leave"):
        _execute(context)


def test_accounting_rejects_orders_originating_in_warmup(tmp_path: Path) -> None:
    from ai_quant_lab.core.multi_signal_runtime import (
        MultiSignalAccountingError,
        verify_multi_signal_backtest_accounting,
    )

    context = _multi_context(tmp_path)
    artifact = _execute(context).artifact
    bars = context[3].normalized_bars
    first_index = next(
        i for i, bar in enumerate(bars) if bar.bar_id == artifact.orders[0].source_bar_ref.object_id
    )
    with pytest.raises(MultiSignalAccountingError, match="inside warmup"):
        verify_multi_signal_backtest_accounting(
            artifact=artifact,
            specification=replace(context[7], warmup_bars=first_index + 1),
            strategy=context[6],
            bars=bars,
        )


def test_exact_1000_bar_warmup_runs_through_governed_authorization(tmp_path: Path) -> None:
    rows = []
    prior = 100
    start = datetime(2024, 12, 22, tzinfo=UTC)
    for index in range(1004):
        close = 100 if index < 1000 else 101 + 2 * (index - 1000)
        opened = start + timedelta(hours=index)
        closed = opened + timedelta(hours=1)
        available = closed + timedelta(seconds=5)
        rows.append(
            f"{opened.strftime('%Y-%m-%dT%H:%M:%S.000000Z')},"
            f"{closed.strftime('%Y-%m-%dT%H:%M:%S.000000Z')},"
            f"{prior},{max(prior, close) + 1},{min(prior, close) - 1},{close},100,final,"
            f"{available.strftime('%Y-%m-%dT%H:%M:%S.000000Z')}\n"
        )
        prior = close
    context = _multi_context(tmp_path, warmup_bars=1000, csv_text=HEADER + "".join(rows))
    artifact = _execute(context).artifact
    bars = context[3].normalized_bars
    assert len(artifact.equity_curve) == 1004
    assert artifact.orders[0].source_bar_ref.object_id == bars[1000].bar_id
    assert artifact.fills[0].bar_ref.object_id == bars[1002].bar_id
    assert all(Decimal(point.position_quantity) == 0 for point in artifact.equity_curve[:1002])
    assert artifact.open_position is SimulatedPositionState.LONG


def test_warmup_change_requires_new_exact_authorization(tmp_path: Path) -> None:
    context = list(_multi_context(tmp_path))
    context[7] = replace(context[7], warmup_bars=9)
    from ai_quant_lab.core.experiment_runner import ExperimentRunnerLineageMismatch

    with pytest.raises(ExperimentRunnerLineageMismatch, match="exact references"):
        _execute(tuple(context))


def test_explicit_warmup_is_not_silently_promoted_to_pine(tmp_path: Path) -> None:
    from ai_quant_lab.core.governed_pine_generator import (
        GovernedPineGeneratorUnsupported,
        render_governed_pine_v6,
    )
    from ai_quant_lab.core.pine_strategy_contracts import PineIntakeStatus
    from ai_quant_lab.core.pine_strategy_intake import PineIntakeFailure, _parse_static_source

    context = _multi_context(tmp_path, warmup_bars=9)
    with pytest.raises(GovernedPineGeneratorUnsupported, match="explicit warmup"):
        render_governed_pine_v6(context[6], context[7], script_title="Warmup boundary")
    with pytest.raises(PineIntakeFailure, match="explicit warmup") as failed:
        _parse_static_source("", context[6], context[7])
    assert failed.value.status is PineIntakeStatus.UNSUPPORTED


def test_legacy_profile_still_rejects_explicit_warmup(tmp_path: Path) -> None:
    from ai_quant_lab.core.strategy_backtest import (
        UnsupportedStrategy,
        _require_scope,
        strategy_backtest_replay_contract,
    )

    context = authorized_context(tmp_path)
    with pytest.raises(UnsupportedStrategy):
        _require_scope(
            replace(context[7], warmup_bars=1),
            strategy_backtest_replay_contract(),
            context[6],
        )
