"""Sprint 24 multi-signal long/short model and governed Pine rendering tests."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import replace

import pytest

from ai_quant_lab.core.codec import decode, encode
from ai_quant_lab.core.governed_pine_generator import render_governed_pine_v6
from ai_quant_lab.core.model import (
    ArtifactId,
    ObjectVersion,
    ProvenanceId,
    TraceabilityRef,
)
from ai_quant_lab.core.strategy_backtest_contracts import (
    MultiSignalTrendParameters,
    SidePermission,
    SignalTiming,
    SimulatedExecutionTiming,
    StrategyBacktestContractError,
    StrategyDefinition,
    StrategyModel,
)

V1 = ObjectVersion(1)
V2 = ObjectVersion(2)
ENGINE_REF = TraceabilityRef(
    ArtifactId("multi-signal-trend-research-engine-contract-v1"),
    V1,
    "sha256:" + "a" * 64,
)
PROVENANCE_REF = TraceabilityRef(
    ProvenanceId("sprint-24-multi-signal-strategy"),
    V1,
    "sha256:" + "b" * 64,
)


def parameters() -> MultiSignalTrendParameters:
    return MultiSignalTrendParameters(
        34,
        120,
        236,
        8,
        "55",
        "45",
        7,
        49,
        17,
        14,
        "20",
        14,
        "2.5",
        "2",
        "1",
        18,
    )


def strategy() -> StrategyDefinition:
    return StrategyDefinition(
        ArtifactId("solusdt-4h-multi-signal-trend-v1"),
        V2,
        StrategyModel.MULTI_SIGNAL_TREND_LONG_SHORT,
        SignalTiming.BAR_CLOSE_AFTER_AVAILABILITY,
        SimulatedExecutionTiming.FIRST_ELIGIBLE_NEXT_BAR_OPEN,
        SidePermission.LONG_SHORT,
        0,
        10_000,
        "USDT",
        100,
        False,
        False,
        ENGINE_REF,
        PROVENANCE_REF,
        V2,
        parameters(),
    )


def test_multi_signal_strategy_contract_is_strict_and_codec_roundtrips() -> None:
    definition = strategy()

    assert definition.version == V2
    assert definition.contract_version == V2
    assert definition.side_permission is SidePermission.LONG_SHORT
    assert definition.multi_signal == parameters()
    assert decode(encode(definition), StrategyDefinition) == definition


def test_multi_signal_pine_contains_long_short_indicators_and_risk_controls() -> None:
    source = render_governed_pine_v6(
        strategy(),
        script_title="AIQL SOLUSDT 4H Multi Signal",
    )

    required = (
        "//@version=6",
        "AIQL_GOVERNED_PINE_V6_MULTI_SIGNAL_TREND_LONG_SHORT_V1",
        "ta.ema(close, fastEmaLength)",
        "ta.rsi(close, rsiLength)",
        "ta.macd(close, macdFastLength, macdSlowLength, macdSignalLength)",
        "ta.dmi(adxLength, adxLength)",
        "ta.atr(atrLength)",
        'strategy.entry("AIQL-L", strategy.long)',
        'strategy.entry("AIQL-S", strategy.short)',
        'strategy.close("AIQL-L")',
        'strategy.close("AIQL-S")',
        "atrStopMult = 2.5",
        "takeProfitR = 2",
        "breakEvenTriggerR = 1",
        "timeStopBars = 18",
        "process_orders_on_close=false",
        "calc_on_every_tick=false",
    )
    for token in required:
        assert token in source
    assert "request." not in source
    assert "security(" not in source
    assert "lookahead" not in source.lower()


def test_multi_signal_render_is_byte_deterministic_and_parameter_sensitive() -> None:
    definition = strategy()
    first = render_governed_pine_v6(definition, script_title="AIQL SOL 4H")
    second = render_governed_pine_v6(definition, script_title="AIQL SOL 4H")

    assert first == second
    changed = replace(
        definition,
        multi_signal=replace(parameters(), atr_stop_mult="3"),
    )
    changed_source = render_governed_pine_v6(changed, script_title="AIQL SOL 4H")
    assert changed_source != first
    assert "atrStopMult = 3" in changed_source


@pytest.mark.parametrize(
    "mutator",
    (
        lambda p: replace(p, fast_ema=p.medium_ema),
        lambda p: replace(p, rsi_short_max=p.rsi_long_min),
        lambda p: replace(p, macd_fast=p.macd_slow),
        lambda p: replace(p, adx_threshold="0"),
        lambda p: replace(p, atr_stop_mult="0"),
        lambda p: replace(p, take_profit_r="-1"),
        lambda p: replace(p, break_even_trigger_r="0"),
        lambda p: replace(p, time_stop_bars=0),
    ),
)
def test_invalid_multi_signal_parameters_fail_closed(
    mutator: Callable[[MultiSignalTrendParameters], MultiSignalTrendParameters],
) -> None:
    with pytest.raises(StrategyBacktestContractError):
        mutator(parameters())


def test_multi_signal_profile_cannot_silently_downgrade_to_long_only() -> None:
    with pytest.raises(StrategyBacktestContractError):
        replace(strategy(), side_permission=SidePermission.LONG_ONLY)
    with pytest.raises(StrategyBacktestContractError):
        replace(strategy(), multi_signal=None)
    with pytest.raises(StrategyBacktestContractError):
        replace(strategy(), threshold_bps=1)


def test_legacy_strategy_serialization_shape_remains_unchanged() -> None:
    legacy = StrategyDefinition(
        ArtifactId("legacy-shape-check"),
        V1,
        StrategyModel.CLOSE_VS_OPEN_LONG_ONLY,
        SignalTiming.BAR_CLOSE_AFTER_AVAILABILITY,
        SimulatedExecutionTiming.FIRST_ELIGIBLE_NEXT_BAR_OPEN,
        SidePermission.LONG_ONLY,
        10,
        10_000,
        "USDT",
        100,
        False,
        False,
        ENGINE_REF,
        PROVENANCE_REF,
        V1,
    )
    encoded = encode(legacy)
    assert b'"multi_signal"' not in encoded
    assert decode(encoded, StrategyDefinition) == legacy
