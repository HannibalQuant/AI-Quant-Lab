"""PB0 fixed one-bar setup, exact model boundary and governed replay tests."""

from dataclasses import replace
from decimal import Decimal
from pathlib import Path

import pytest
from test_multi_signal_strategy_backtest import _execute, _multi_context, parameters

from ai_quant_lab.core.codec import decode, encode
from ai_quant_lab.core.data import DecimalValue
from ai_quant_lab.core.multi_signal_runtime import (
    MultiSignalIndicatorPoint,
    pullback_entry_direction,
)
from ai_quant_lab.core.strategy_backtest import (
    multi_signal_strategy_backtest_engine_ref,
    multi_signal_strategy_backtest_replay_contract,
    pullback_strategy_backtest_engine_ref,
)
from ai_quant_lab.core.strategy_backtest_contracts import (
    SimulatedPositionState,
    StrategyDefinition,
)


@pytest.mark.parametrize("short", [False, True])
@pytest.mark.parametrize(
    "failed_condition", [None, "touch", "previous_close", "extreme", "warmup", "unready"]
)
def test_exact_pullback_predicates(
    tmp_path: Path, short: bool, failed_condition: str | None
) -> None:
    context = _multi_context(tmp_path)
    bars = list(context[3].normalized_bars[:2])
    # Symmetric price geometry with a synthetic ready production indicator state.
    previous = replace(
        bars[0],
        open=DecimalValue("100"),
        high=DecimalValue("101"),
        low=DecimalValue("99"),
        close=DecimalValue("100"),
    )
    close = "98" if short else "102"
    current = replace(
        bars[1],
        open=DecimalValue("100"),
        high=DecimalValue("103"),
        low=DecimalValue("97"),
        close=DecimalValue(close),
    )
    point = MultiSignalIndicatorPoint(
        Decimal("99" if short else "101"),
        Decimal("100"),
        Decimal("101" if short else "99"),
        Decimal("30" if short else "70"),
        Decimal("-1" if short else "1"),
        Decimal("0"),
        Decimal("10" if short else "30"),
        Decimal("30" if short else "10"),
        Decimal("30"),
        Decimal("1"),
    )
    prior_point = replace(point, fast_ema=Decimal("100"))
    if failed_condition == "touch":
        previous = replace(
            previous,
            high=DecimalValue("99") if short else previous.high,
            low=previous.low if short else DecimalValue("101"),
            open=DecimalValue("99" if short else "101"),
            close=DecimalValue("99" if short else "101"),
        )
    elif failed_condition == "previous_close":
        previous = replace(previous, close=DecimalValue("99" if short else "101"))
    elif failed_condition == "extreme":
        previous = replace(
            previous,
            low=DecimalValue(close) if short else previous.low,
            high=previous.high if short else DecimalValue(close),
        )
    elif failed_condition == "unready":
        prior_point = replace(prior_point, rsi=None)
    result = pullback_entry_direction(
        (previous, current),
        (prior_point, point),
        parameters(),
        1,
        1 if failed_condition == "warmup" else 0,
    )
    expected = SimulatedPositionState.SHORT if short else SimulatedPositionState.LONG
    assert result is (expected if failed_condition is None else SimulatedPositionState.FLAT)


def test_governed_pullback_identity_roundtrip_and_replay(tmp_path: Path) -> None:
    context = _multi_context(tmp_path, pullback=True)
    definition = context[6]
    assert decode(encode(definition), StrategyDefinition) == definition
    assert definition.engine_contract_ref == pullback_strategy_backtest_engine_ref()
    assert definition.engine_contract_ref != multi_signal_strategy_backtest_engine_ref()
    result = _execute(context)
    assert len(result.artifact.equity_curve) == len(context[3].normalized_bars)
    assert result.artifact.engine_contract_ref == definition.engine_contract_ref


def test_pullback_rejects_old_engine_contract(tmp_path: Path) -> None:
    context = list(_multi_context(tmp_path, pullback=True))
    context[11] = multi_signal_strategy_backtest_replay_contract()
    from ai_quant_lab.core.experiment_runner import ExperimentRunnerLineageMismatch

    with pytest.raises(ExperimentRunnerLineageMismatch):
        _execute(tuple(context))


def test_pullback_entry_and_opposite_trend_exit_accounting(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    from ai_quant_lab.core import multi_signal_runtime as runtime

    context = _multi_context(tmp_path, pullback=True)
    bars = list(context[3].normalized_bars)
    for i, bar in enumerate(bars):
        bars[i] = replace(
            bar,
            open=DecimalValue("100"),
            high=DecimalValue("103"),
            low=DecimalValue("99"),
            close=DecimalValue("102"),
        )
    bars[0] = replace(bars[0], high=DecimalValue("101"), close=DecimalValue("100"))
    bars[3] = replace(bars[3], close=DecimalValue("100"))
    bars[4] = replace(bars[4], low=DecimalValue("97"), close=DecimalValue("98"))
    long_point = MultiSignalIndicatorPoint(
        Decimal("101"),
        Decimal("100"),
        Decimal("99"),
        Decimal("70"),
        Decimal("1"),
        Decimal("0"),
        Decimal("30"),
        Decimal("10"),
        Decimal("30"),
        Decimal("10"),
    )
    points = [long_point for _ in bars]
    points[0] = replace(long_point, fast_ema=Decimal("100"))
    points[4] = replace(
        long_point,
        fast_ema=Decimal("99"),
        slow_ema=Decimal("101"),
        rsi=Decimal("30"),
        macd=Decimal("-1"),
        plus_di=Decimal("10"),
        minus_di=Decimal("30"),
    )
    monkeypatch.setattr(runtime, "build_multi_signal_indicators", lambda *_: tuple(points))
    # The opposite trend bar is not an opposite PB0 entry; exit still required.
    assert (
        runtime.pullback_entry_direction(tuple(bars), tuple(points), parameters(), 4, 0)
        is SimulatedPositionState.FLAT
    )
    a = runtime.simulate_multi_signal_backtest(
        context[12].experiment_run,
        context[9].record,
        context[7],
        context[6],
        tuple(bars),
        "sha256:" + "9" * 64,
    )
    assert a.orders[0].source_bar_ref.object_id == bars[1].bar_id
    assert a.fills[0].bar_ref.object_id == bars[3].bar_id
    assert a.orders[1].source_bar_ref.object_id == bars[4].bar_id
    assert a.fills[1].bar_ref.object_id == bars[6].bar_id
    runtime.verify_multi_signal_backtest_accounting(
        artifact=a, specification=context[7], strategy=context[6], bars=tuple(bars)
    )
    # Same prices/accounting, but unauthorized pullback setup: verifier rejects.
    points[0] = replace(points[0], rsi=None)
    with pytest.raises(runtime.MultiSignalAccountingError, match="PB0"):
        runtime.verify_multi_signal_backtest_accounting(
            artifact=a, specification=context[7], strategy=context[6], bars=tuple(bars)
        )
