"""RR4 exploratory replay; produces no governed authorization/result artifact.

Uses the pinned RR3 Decimal runtime, with one isolated entry-only guard added to
the function source in memory. Metadata containers are diagnostic namespaces.
Raw source data must remain local. Run with PYTHONPATH=src python research/rr4/run.py INPUT.
"""

import csv
import hashlib
import inspect
import io
import json
import sys
from dataclasses import fields
from datetime import UTC, datetime
from decimal import Decimal, localcontext
from pathlib import Path
from types import SimpleNamespace

from ai_quant_lab.core import multi_signal_runtime as rt
from ai_quant_lab.core.data import DecimalValue
from ai_quant_lab.core.market_data import (
    AlignmentKind,
    MarketBarId,
    TimeframeId,
    TimeframeIdentity,
    TimeframeUnit,
)
from ai_quant_lab.core.model import ArtifactId, ObjectVersion, ProvenanceId, RunId, TraceabilityRef
from ai_quant_lab.core.strategy_backtest import multi_signal_strategy_backtest_engine_ref
from ai_quant_lab.core.strategy_backtest_contracts import (
    BacktestResultArtifact,
    MultiSignalTrendParameters,
    SidePermission,
    SignalTiming,
    SimulatedExecutionTiming,
    StrategyDefinition,
    StrategyModel,
)
from ai_quant_lab.core.tradingview_csv_adapter import (
    TradingViewCsvAdapterPolicy,
    normalize_tradingview_csv,
)

D = Decimal
V1, V2 = ObjectVersion(1), ObjectVersion(2)
EXPECTED_RAW = "56d7f99aa210a9ab52aa283561b7ca2d13c4b97a91b49e5d1b8e1d15d9c3dd5b"
EXPECTED_CANONICAL = "1202586308d6aa85add15c51259ba59587badeeda0be64b1efceedb4865c4c6f"
EXPECTED_RUNTIME = "37b3a069dc51efa779200ff68a495b1d1e865e0ff2c563925a63fe89723a61fa"


def digest(text):
    return "sha256:" + hashlib.sha256(text.encode()).hexdigest()


def short_allowed(bars, index, threshold):
    if threshold is None:
        return True
    if index < 18:
        return False
    # Multiplication avoids division rounding at the exact boundary.
    return D(bars[index].close.text) * 100 <= D(bars[index - 18].close.text) * (100 - threshold)


def runtime(threshold, *, disable_short=False, unmodified=False):
    source = inspect.getsource(rt.simulate_multi_signal_backtest)
    anchor = (
        "            if position is SimulatedPositionState.FLAT:\n                if direction in ("
    )
    assert source.count(anchor) == 1
    guard = """            if position is SimulatedPositionState.FLAT:
                if (
                    direction is SimulatedPositionState.SHORT
                    and (disable_short or not short_allowed(bars, index, threshold))
                ):
                    continue
                if direction in ("""
    namespace = dict(vars(rt))
    namespace.update(threshold=threshold, disable_short=disable_short, short_allowed=short_allowed)
    namespace["_bar_ref"] = lambda bar: bar.ref
    names = [field.name for field in fields(BacktestResultArtifact)]
    namespace["BacktestResultArtifact"] = lambda *args: SimpleNamespace(
        **dict(zip(names, args, strict=True))
    )
    exec(
        compile(
            source if unmodified else source.replace(anchor, guard),
            "<rr4-entry-only-prototype>",
            "exec",
        ),
        namespace,
    )
    return namespace["simulate_multi_signal_backtest"], namespace


def main():
    assert hashlib.sha256(Path(rt.__file__).read_bytes()).hexdigest() == EXPECTED_RUNTIME
    source_path = Path(sys.argv[1]).resolve()
    out = Path(__file__).parent / "results"
    out.mkdir(exist_ok=True)
    timeframe = TimeframeIdentity(
        TimeframeId("4h"), V1, TimeframeUnit.HOUR, 4, AlignmentKind.UTC_EPOCH_FIXED, V1
    )
    normalized = normalize_tradingview_csv(
        source_path,
        allowed_root=source_path.parent,
        timeframe=timeframe,
        policy=TradingViewCsvAdapterPolicy(
            time_column="time",
            window_start=datetime(2022, 1, 3, tzinfo=UTC),
            window_end=datetime(2026, 1, 1, tzinfo=UTC),
            derive_finality_from_historical_export=True,
            availability_at_bar_close=True,
        ),
    )
    assert normalized.source_sha256 == EXPECTED_RAW
    assert normalized.canonical_sha256 == EXPECTED_CANONICAL
    rows = list(csv.DictReader(io.StringIO(normalized.canonical_csv)))
    assert len(rows) == 8754
    bars = []
    for i, row in enumerate(rows):
        opened = datetime.fromisoformat(row["bar_open_time"].replace("Z", "+00:00"))
        closed = datetime.fromisoformat(row["bar_close_time"].replace("Z", "+00:00"))
        if bars:
            assert bars[-1].bar_close == opened
        prices = {k: DecimalValue(row[k]) for k in ("open", "high", "low", "close")}
        assert (
            D(row["low"])
            <= min(D(row["open"]), D(row["close"]))
            <= max(D(row["open"]), D(row["close"]))
            <= D(row["high"])
        )
        bars.append(
            SimpleNamespace(
                **prices,
                bar_open=opened,
                bar_close=closed,
                availability_time=closed,
                ref=TraceabilityRef(
                    MarketBarId(f"rr4-diagnostic-bar-{i:05d}"),
                    V1,
                    digest(json.dumps(row, sort_keys=True)),
                ),
            )
        )
    bars = tuple(bars)
    params = MultiSignalTrendParameters(
        12,
        72,
        160,
        10,
        "61",
        "38",
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
        "0.2",
        1,
        "0.5",
        "4",
    )
    definition = StrategyDefinition(
        ArtifactId("rr3-c2-rr4-diagnostic-control"),
        V2,
        StrategyModel.MULTI_SIGNAL_TREND_LONG_SHORT,
        SignalTiming.BAR_CLOSE_AFTER_AVAILABILITY,
        SimulatedExecutionTiming.FIRST_ELIGIBLE_NEXT_BAR_OPEN,
        SidePermission.LONG_SHORT,
        0,
        10000,
        "USDT",
        100,
        False,
        False,
        multi_signal_strategy_backtest_engine_ref(),
        TraceabilityRef(ProvenanceId("rr4-diagnostic-source"), V1, "sha256:" + EXPECTED_RAW),
        V2,
        params,
    )
    summaries, trade_rows, curves = [], [], []
    results = {}
    # L0 is a post-hoc ablation requested after the original RR4 filter comparison.
    candidates = [
        ("C0", None, False),
        ("C1", D(4), False),
        ("C2", D(8), False),
        ("C3", D(12), False),
        ("L0", None, True),
    ]
    for candidate, threshold, disable_short in candidates:
        for commission in (10, 20, 30, 40):
            fn, _ = runtime(threshold, disable_short=disable_short)
            name = f"{candidate.lower()}-cost-{commission}"
            spec = SimpleNamespace(
                capital_notional_minor=100000,
                commission_semantics=rt.CostSemantics.DECLARED_BPS,
                commission_bps=commission,
                slippage_semantics=rt.CostSemantics.DECLARED_BPS,
                slippage_bps=5,
                normalized_manifest_ref=None,
                normalized_lock_ref=None,
                sizing_semantics=rt.PositionSizingSemantics.FIXED_NOTIONAL,
            )
            base = SimpleNamespace(
                run_id=RunId(f"rr4-diagnostic-{name}"),
                result_artifact_id=ArtifactId(f"rr4-diagnostic-result-{name}"),
                authorization_ref=None,
                specification_ref=None,
                policy_ref=None,
                eligibility_ref=None,
                engine_contract_ref=None,
            )
            config = digest(
                f"{candidate}:{threshold}:{disable_short}:{commission}:{EXPECTED_CANONICAL}"
            )
            result = fn(
                base,
                SimpleNamespace(configuration_fingerprint=config),
                spec,
                definition,
                bars,
                config,
            )
            # Independent existing accounting verifier, using identical OHLC row bindings.
            verifier_ns = dict(vars(rt))
            verifier_ns["_bar_ref"] = lambda bar: bar.ref
            exec(
                compile(
                    inspect.getsource(rt.verify_multi_signal_backtest_accounting),
                    "<rr4-accounting>",
                    "exec",
                ),
                verifier_ns,
            )
            verifier_ns["verify_multi_signal_backtest_accounting"](
                artifact=result, specification=spec, strategy=definition, bars=bars
            )
            fills = {f.fill_id: f for f in result.fills}
            local = []
            for t in result.trades:
                side = (
                    "LONG" if fills[t.entry_fill_id].side is rt.SimulatedOrderSide.BUY else "SHORT"
                )
                local.append(
                    dict(
                        candidate=candidate,
                        commission_bps=commission,
                        side=side,
                        entry=t.entry_time.isoformat(),
                        exit=t.exit_time.isoformat(),
                        net_usdt=t.net_pnl,
                    )
                )
            trade_rows.extend(local)
            if candidate == "C0" and commission == 10:
                original, _ = runtime(None, unmodified=True)
                original_result = original(
                    base,
                    SimpleNamespace(configuration_fingerprint=config),
                    spec,
                    definition,
                    bars,
                    config,
                )
                assert vars(original_result) == vars(result), (
                    "disabled filter changed control ledger"
                )
            windows = []
            window_details = []
            for k in range(4):
                start = 3285 + k * 1095
                end = start + 1095
                initial = D(result.equity_curve[start - 1].equity)
                end_equity = D(result.equity_curve[end - 1].equity)
                windows.append(end_equity / initial - 1)
                closed = [
                    t
                    for t in local
                    if bars[start].bar_open
                    <= datetime.fromisoformat(t["exit"])
                    < bars[end - 1].bar_close
                ]
                peak, drawdown = initial, D(0)
                for p in result.equity_curve[start:end]:
                    value = D(p.equity)
                    peak = max(peak, value)
                    drawdown = max(drawdown, 1 - value / peak)
                window_details.append(
                    dict(
                        start=bars[start].bar_open.isoformat(),
                        end_exclusive=bars[end - 1].bar_close.isoformat(),
                        trades=len(closed),
                        long_trades=sum(t["side"] == "LONG" for t in closed),
                        short_trades=sum(t["side"] == "SHORT" for t in closed),
                        long_net=float(
                            sum((D(t["net_usdt"]) for t in closed if t["side"] == "LONG"), D(0))
                        ),
                        short_net=float(
                            sum((D(t["net_usdt"]) for t in closed if t["side"] == "SHORT"), D(0))
                        ),
                        max_dd_pct=float(drawdown * 100),
                    )
                )
            compounded = D(1)
            for w in windows:
                compounded *= 1 + w
            long_pnl = sum((D(t["net_usdt"]) for t in local if t["side"] == "LONG"), D(0))
            short_pnl = sum((D(t["net_usdt"]) for t in local if t["side"] == "SHORT"), D(0))
            summary = dict(
                candidate=candidate,
                threshold_pct=None if threshold is None else str(threshold),
                commission_bps=commission,
                return_pct=float(D(result.total_return) * 100),
                max_dd_pct=float(D(result.max_drawdown) * 100),
                trades=result.trade_count,
                long_trades=sum(t["side"] == "LONG" for t in local),
                short_trades=sum(t["side"] == "SHORT" for t in local),
                long_net=float(long_pnl),
                short_net=float(short_pnl),
                worst_trade=float(min(D(t["net_usdt"]) for t in local)),
                positive_windows=sum(w > 0 for w in windows),
                worst_window_pct=float(min(windows) * 100),
                aggregate_window_pct=float((compounded - 1) * 100),
                windows_pct=[float(w * 100) for w in windows],
                window_details=window_details,
                open_position=result.open_position.value,
            )
            if candidate == "C0" and commission == 10:
                assert result.trade_count == 167
                assert abs(D(result.total_return) * 100 - D("24.8645")) < D("0.0001")
                assert abs(short_pnl - D("80.3430")) < D("0.0001")
                assert abs(long_pnl - D("168.3024")) < D("0.0001")
                assert abs(D(result.max_drawdown) * 100 - D("2.5494")) < D("0.0001")
                assert abs((compounded - 1) * 100 - D("9.7851")) < D("0.0001")
            summaries.append(summary)
            results[(candidate, commission)] = local
            if candidate == "L0":
                control_longs = [t for t in results[("C0", commission)] if t["side"] == "LONG"]

                def ledger(trades):
                    return [(t["side"], t["entry"], t["exit"], t["net_usdt"]) for t in trades]

                assert ledger(local) == ledger(control_longs), (
                    "LONG-only ablation changed the LONG ledger"
                )
                assert result.open_position is not rt.SimulatedPositionState.SHORT
            print(json.dumps(summary), flush=True)
            if commission == 10:
                curves.extend(
                    dict(candidate=candidate, time=p.event_time.isoformat(), equity=p.equity)
                    for p in result.equity_curve
                )
    comparisons = []
    control = {(t["side"], t["entry"]): t for t in results[("C0", 10)]}
    for candidate in ("C1", "C2", "C3"):
        current = {(t["side"], t["entry"]): t for t in results[(candidate, 10)]}
        removed = [t for key, t in control.items() if key not in current and t["side"] == "SHORT"]
        added = [t for key, t in current.items() if key not in control and t["side"] == "SHORT"]
        comparisons.append(
            dict(
                candidate=candidate,
                removed_short=len(removed),
                removed_winners=sum(D(t["net_usdt"]) > 0 for t in removed),
                removed_winner_pnl=float(
                    sum((D(t["net_usdt"]) for t in removed if D(t["net_usdt"]) > 0), D(0))
                ),
                removed_loss_pnl=float(
                    sum((D(t["net_usdt"]) for t in removed if D(t["net_usdt"]) < 0), D(0))
                ),
                new_short=len(added),
                new_short_pnl=float(sum((D(t["net_usdt"]) for t in added), D(0))),
            )
        )
    for filename, values in [("trades.csv", trade_rows), ("equity.csv", curves)]:
        with (out / filename).open("w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=list(values[0]))
            writer.writeheader()
            writer.writerows(values)
    evidence = dict(
        status="EXPLORATORY_RUNTIME_REPLAY_NOT_GOVERNED_PROMOTION",
        raw_sha256=EXPECTED_RAW,
        canonical_sha256=EXPECTED_CANONICAL,
        runtime_sha256=hashlib.sha256(Path(rt.__file__).read_bytes()).hexdigest(),
        summary=summaries,
        comparisons=comparisons,
    )
    (out / "results.json").write_text(json.dumps(evidence, indent=2) + "\n")


if __name__ == "__main__":
    with localcontext(rt._DECIMAL_CONTEXT):
        main()
