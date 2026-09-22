"""Sprint 13 independent backtest-result accounting and tamper tests."""

from __future__ import annotations

import copy
import json
from collections.abc import Callable
from dataclasses import replace
from datetime import timedelta
from decimal import ROUND_HALF_EVEN, Context, Decimal, localcontext
from pathlib import Path

import pytest
from test_real_csv_onboarding import HEADER
from test_strategy_backtest import (
    BacktestContext,
    authorized_context,
    execute_context,
)

from ai_quant_lab import EXE_01
from ai_quant_lab.core.codec import encode
from ai_quant_lab.core.experiment_runner import _select_replay_bars
from ai_quant_lab.core.integrity import fingerprint_record
from ai_quant_lab.core.model import ArtifactId, ExecutionState, ObjectVersion
from ai_quant_lab.core.strategy_backtest import (
    AccountingMismatch,
    InconsistentPositionTransition,
    verify_backtest_accounting,
)
from ai_quant_lab.core.strategy_backtest_contracts import (
    BacktestResultArtifact,
    SimulatedOrderSide,
    SimulatedPositionState,
    StrategyBacktestContractError,
)

GOLDEN = Path(__file__).parent / "golden" / "backtest_result_hardening_v1.json"


def _open_long_csv() -> str:
    rows: list[str] = []
    for index in range(6):
        open_price = 100 + index
        close_price = open_price + 1
        rows.append(
            f"2025-02-01T{index:02d}:00:00.000000Z,"
            f"2025-02-01T{index + 1:02d}:00:00.000000Z,"
            f"{open_price},{close_price + 1},{open_price - 1},{close_price},"
            f"{10 + index},final,"
            f"2025-02-01T{index + 1:02d}:00:05.000000Z\n"
        )
    return HEADER + "".join(rows)


def _verify(context: BacktestContext, artifact: BacktestResultArtifact) -> None:
    verify_backtest_accounting(
        artifact=artifact,
        specification=context[7],
        strategy=context[6],
        bars=_select_replay_bars(context[7], context[3]),
    )


def _unsafe(artifact: BacktestResultArtifact, **changes: object) -> BacktestResultArtifact:
    clone = copy.copy(artifact)
    for name, value in changes.items():
        object.__setattr__(clone, name, value)
    return clone


def _decimal_text(value: Decimal) -> str:
    if value == 0:
        return "0"
    text = format(value, "f")
    return text.rstrip("0").rstrip(".") if "." in text else text


def _replace_item(
    artifact: BacktestResultArtifact,
    collection: str,
    index: int,
    **changes: object,
) -> BacktestResultArtifact:
    values = list(getattr(artifact, collection))
    values[index] = replace(values[index], **changes)
    return _unsafe(artifact, **{collection: tuple(values)})


def _flat_result(
    tmp_path: Path, suffix: str = "sprint13-flat"
) -> tuple[BacktestContext, BacktestResultArtifact]:
    context = authorized_context(tmp_path, suffix=suffix)
    _, result = execute_context(context)
    return context, result.artifact


def _open_result(
    tmp_path: Path, suffix: str = "sprint13-open"
) -> tuple[BacktestContext, BacktestResultArtifact]:
    context = authorized_context(tmp_path, suffix=suffix, csv_text=_open_long_csv())
    _, result = execute_context(context)
    return context, result.artifact


def test_valid_flat_result_passes_independent_accounting_verification(tmp_path: Path) -> None:
    context, artifact = _flat_result(tmp_path)
    _verify(context, artifact)
    final = artifact.equity_curve[-1]
    assert artifact.open_position is SimulatedPositionState.FLAT
    assert final.position_quantity == final.position_value == final.unrealized_pnl == "0"
    assert len(artifact.trades) == artifact.trade_count == 1


def test_independent_verifier_rejects_coherent_wrong_fixed_notional(tmp_path: Path) -> None:
    context, artifact = _flat_result(tmp_path, suffix="coherent-wrong-fixed-notional")
    factor = Decimal("0.5")
    initial = Decimal(artifact.initial_capital)

    with localcontext(Context(prec=34, rounding=ROUND_HALF_EVEN)):
        orders = tuple(
            replace(order, notional=_decimal_text(Decimal(order.notional) * factor))
            for order in artifact.orders
        )
        fills = tuple(
            replace(
                fill,
                quantity=_decimal_text(Decimal(fill.quantity) * factor),
                fill_notional=_decimal_text(Decimal(fill.fill_notional) * factor),
                commission=_decimal_text(Decimal(fill.commission) * factor),
                slippage_cost=_decimal_text(Decimal(fill.slippage_cost) * factor),
            )
            for fill in artifact.fills
        )
        trades = tuple(
            replace(
                trade,
                quantity=_decimal_text(Decimal(trade.quantity) * factor),
                gross_pnl=_decimal_text(Decimal(trade.gross_pnl) * factor),
                commission=_decimal_text(Decimal(trade.commission) * factor),
                slippage_cost=_decimal_text(Decimal(trade.slippage_cost) * factor),
                net_pnl=_decimal_text(Decimal(trade.net_pnl) * factor),
            )
            for trade in artifact.trades
        )
        curve = tuple(
            replace(
                point,
                cash=_decimal_text(initial + (Decimal(point.cash) - initial) * factor),
                position_quantity=_decimal_text(Decimal(point.position_quantity) * factor),
                position_value=_decimal_text(Decimal(point.position_value) * factor),
                unrealized_pnl=_decimal_text(Decimal(point.unrealized_pnl) * factor),
                realized_pnl=_decimal_text(Decimal(point.realized_pnl) * factor),
                equity=_decimal_text(initial + (Decimal(point.equity) - initial) * factor),
            )
            for point in artifact.equity_curve
        )
        peak = initial
        max_drawdown = Decimal(0)
        for point in curve:
            equity = Decimal(point.equity)
            peak = max(peak, equity)
            max_drawdown = max(max_drawdown, Decimal(1) - equity / peak)
        coherent_tamper = _unsafe(
            artifact,
            orders=orders,
            fills=fills,
            trades=trades,
            equity_curve=curve,
            final_cash=_decimal_text(initial + (Decimal(artifact.final_cash) - initial) * factor),
            final_equity=_decimal_text(
                initial + (Decimal(artifact.final_equity) - initial) * factor
            ),
            gross_pnl=_decimal_text(Decimal(artifact.gross_pnl) * factor),
            net_pnl=_decimal_text(Decimal(artifact.net_pnl) * factor),
            total_return=_decimal_text(Decimal(artifact.total_return) * factor),
            max_drawdown=_decimal_text(max_drawdown),
        )

    expected = Decimal(context[6].fixed_notional_minor) / Decimal(
        context[6].capital_minor_unit_scale
    )
    assert expected == Decimal("100")
    assert Decimal(coherent_tamper.orders[0].notional) == Decimal("50")
    assert Decimal(coherent_tamper.fills[0].fill_notional) == Decimal("50")
    with pytest.raises(
        AccountingMismatch,
        match="BUY notional does not match governed fixed-notional sizing",
    ):
        _verify(context, coherent_tamper)


def test_valid_open_long_result_has_exact_unforced_valuation(tmp_path: Path) -> None:
    context, artifact = _open_result(tmp_path)
    _verify(context, artifact)
    final = artifact.equity_curve[-1]
    entry = artifact.fills[0]
    mark = Decimal(_select_replay_bars(context[7], context[3])[-1].close.text)
    quantity = Decimal(entry.quantity)
    assert artifact.open_position is SimulatedPositionState.LONG
    assert len(artifact.orders) == len(artifact.fills) == 1
    assert artifact.trades == () and artifact.trade_count == 0
    assert Decimal(final.position_quantity) == quantity > 0
    with localcontext(Context(prec=34, rounding=ROUND_HALF_EVEN)):
        assert Decimal(final.position_value) == quantity * mark
        assert Decimal(final.unrealized_pnl) == (mark - Decimal(entry.execution_price)) * quantity
        assert Decimal(artifact.final_equity) == Decimal(artifact.final_cash) + Decimal(
            final.position_value
        )


def _cash_tamper(artifact: BacktestResultArtifact) -> BacktestResultArtifact:
    point = artifact.equity_curve[-1]
    return _replace_item(artifact, "equity_curve", -1, cash=str(Decimal(point.cash) + 1))


def _quantity_tamper(artifact: BacktestResultArtifact) -> BacktestResultArtifact:
    return _replace_item(artifact, "equity_curve", 2, position_quantity="2")


def _position_value_tamper(artifact: BacktestResultArtifact) -> BacktestResultArtifact:
    point = artifact.equity_curve[2]
    return _replace_item(
        artifact, "equity_curve", 2, position_value=str(Decimal(point.position_value) + 1)
    )


def _unrealized_tamper(artifact: BacktestResultArtifact) -> BacktestResultArtifact:
    return _replace_item(artifact, "equity_curve", 2, unrealized_pnl="1")


def _realized_tamper(artifact: BacktestResultArtifact) -> BacktestResultArtifact:
    return _replace_item(artifact, "equity_curve", -1, realized_pnl="1")


def _equity_tamper(artifact: BacktestResultArtifact) -> BacktestResultArtifact:
    point = artifact.equity_curve[-1]
    return _replace_item(artifact, "equity_curve", -1, equity=str(Decimal(point.equity) + 1))


def _duplicate_order(artifact: BacktestResultArtifact) -> BacktestResultArtifact:
    return _replace_item(artifact, "orders", 1, order_id=artifact.orders[0].order_id)


def _duplicate_fill(artifact: BacktestResultArtifact) -> BacktestResultArtifact:
    return _replace_item(artifact, "fills", 1, fill_id=artifact.fills[0].fill_id)


def _orphan_fill(artifact: BacktestResultArtifact) -> BacktestResultArtifact:
    return _replace_item(artifact, "fills", 0, order_id=ArtifactId("orphan-order"))


def _wrong_side(artifact: BacktestResultArtifact) -> BacktestResultArtifact:
    return _replace_item(artifact, "orders", 0, side=SimulatedOrderSide.SELL)


def _wrong_bar(artifact: BacktestResultArtifact) -> BacktestResultArtifact:
    return _replace_item(artifact, "fills", 0, bar_ref=artifact.equity_curve[0].bar_ref)


def _wrong_order_fill_ref(artifact: BacktestResultArtifact) -> BacktestResultArtifact:
    return _replace_item(artifact, "orders", 0, fill_bar_ref=artifact.equity_curve[0].bar_ref)


def _timing_tamper(artifact: BacktestResultArtifact) -> BacktestResultArtifact:
    return _replace_item(
        artifact, "fills", 0, fill_time=artifact.fills[0].fill_time + timedelta(seconds=1)
    )


def _fill_execution_tamper(artifact: BacktestResultArtifact) -> BacktestResultArtifact:
    return _replace_item(artifact, "fills", 0, execution_price="1")


def _fill_commission_tamper(artifact: BacktestResultArtifact) -> BacktestResultArtifact:
    return _replace_item(artifact, "fills", 0, commission="0")


def _fill_quantity_tamper(artifact: BacktestResultArtifact) -> BacktestResultArtifact:
    return _replace_item(artifact, "fills", 0, quantity="1")


def _duplicate_trade(artifact: BacktestResultArtifact) -> BacktestResultArtifact:
    return _unsafe(artifact, trades=(artifact.trades[0], artifact.trades[0]))


def _unknown_entry(artifact: BacktestResultArtifact) -> BacktestResultArtifact:
    return _replace_item(artifact, "trades", 0, entry_fill_id=ArtifactId("unknown-entry-fill"))


def _unknown_exit(artifact: BacktestResultArtifact) -> BacktestResultArtifact:
    return _replace_item(artifact, "trades", 0, exit_fill_id=ArtifactId("unknown-exit-fill"))


def _trade_quantity_tamper(artifact: BacktestResultArtifact) -> BacktestResultArtifact:
    return _replace_item(artifact, "trades", 0, quantity="1")


def _trade_gross_tamper(artifact: BacktestResultArtifact) -> BacktestResultArtifact:
    return _replace_item(artifact, "trades", 0, gross_pnl="1")


def _trade_commission_tamper(artifact: BacktestResultArtifact) -> BacktestResultArtifact:
    return _replace_item(artifact, "trades", 0, commission="0")


def _trade_slippage_tamper(artifact: BacktestResultArtifact) -> BacktestResultArtifact:
    return _replace_item(artifact, "trades", 0, slippage_cost="0")


def _trade_net_tamper(artifact: BacktestResultArtifact) -> BacktestResultArtifact:
    return _replace_item(artifact, "trades", 0, net_pnl="1")


def _trade_count_tamper(artifact: BacktestResultArtifact) -> BacktestResultArtifact:
    return _unsafe(artifact, trade_count=artifact.trade_count + 1)


def _gross_summary_tamper(artifact: BacktestResultArtifact) -> BacktestResultArtifact:
    return _unsafe(artifact, gross_pnl="1")


def _net_summary_tamper(artifact: BacktestResultArtifact) -> BacktestResultArtifact:
    return _unsafe(artifact, net_pnl="1")


def _final_cash_tamper(artifact: BacktestResultArtifact) -> BacktestResultArtifact:
    return _unsafe(artifact, final_cash=str(Decimal(artifact.final_cash) + 1))


def _final_equity_tamper(artifact: BacktestResultArtifact) -> BacktestResultArtifact:
    return _unsafe(artifact, final_equity=str(Decimal(artifact.final_equity) + 1))


def _total_return_tamper(artifact: BacktestResultArtifact) -> BacktestResultArtifact:
    return _unsafe(artifact, total_return="1")


def _drawdown_tamper(artifact: BacktestResultArtifact) -> BacktestResultArtifact:
    return _unsafe(artifact, max_drawdown="1")


TAMPERS: tuple[tuple[str, Callable[[BacktestResultArtifact], BacktestResultArtifact]], ...] = (
    ("cash", _cash_tamper),
    ("quantity", _quantity_tamper),
    ("position_value", _position_value_tamper),
    ("unrealized_pnl", _unrealized_tamper),
    ("realized_pnl", _realized_tamper),
    ("equity", _equity_tamper),
    ("duplicate_order", _duplicate_order),
    ("duplicate_fill", _duplicate_fill),
    ("orphan_fill", _orphan_fill),
    ("wrong_side", _wrong_side),
    ("wrong_bar", _wrong_bar),
    ("wrong_order_fill_ref", _wrong_order_fill_ref),
    ("timing", _timing_tamper),
    ("fill_execution", _fill_execution_tamper),
    ("fill_commission", _fill_commission_tamper),
    ("fill_quantity", _fill_quantity_tamper),
    ("duplicate_trade", _duplicate_trade),
    ("unknown_entry", _unknown_entry),
    ("unknown_exit", _unknown_exit),
    ("trade_quantity", _trade_quantity_tamper),
    ("trade_gross", _trade_gross_tamper),
    ("trade_commission", _trade_commission_tamper),
    ("trade_slippage", _trade_slippage_tamper),
    ("trade_net", _trade_net_tamper),
    ("trade_count", _trade_count_tamper),
    ("gross_summary", _gross_summary_tamper),
    ("net_summary", _net_summary_tamper),
    ("final_cash", _final_cash_tamper),
    ("final_equity", _final_equity_tamper),
    ("total_return", _total_return_tamper),
    ("max_drawdown", _drawdown_tamper),
)


@pytest.mark.parametrize(("name", "tamper"), TAMPERS, ids=[item[0] for item in TAMPERS])
def test_independent_accounting_verifier_rejects_tampered_flat_result(
    tmp_path: Path,
    name: str,
    tamper: Callable[[BacktestResultArtifact], BacktestResultArtifact],
) -> None:
    context, artifact = _flat_result(tmp_path, suffix=f"tamper-{name}")
    with pytest.raises((AccountingMismatch, InconsistentPositionTransition)):
        _verify(context, tamper(artifact))


def test_open_long_requires_one_unresolved_buy_and_exact_mark(tmp_path: Path) -> None:
    context, artifact = _open_result(tmp_path, suffix="open-tamper")
    with pytest.raises(AccountingMismatch, match="open-position state"):
        _verify(context, _unsafe(artifact, open_position=SimulatedPositionState.FLAT))
    final = artifact.equity_curve[-1]
    bad_point = _replace_item(
        artifact,
        "equity_curve",
        -1,
        position_value=str(Decimal(final.position_value) + 1),
    )
    with pytest.raises(AccountingMismatch, match="position value"):
        _verify(context, bad_point)


def test_result_identity_and_canonical_bytes_are_stable(tmp_path: Path) -> None:
    context = authorized_context(tmp_path, suffix="stable-result")
    _, first = execute_context(context)
    _, second = execute_context(context)
    assert encode(first.artifact) == encode(second.artifact)
    assert fingerprint_record(first.artifact) == fingerprint_record(second.artifact)
    assert first.artifact.run_input_fingerprint == second.artifact.run_input_fingerprint
    assert tuple(item.order_id for item in first.artifact.orders) == tuple(
        item.order_id for item in second.artifact.orders
    )
    assert tuple(item.fill_id for item in first.artifact.fills) == tuple(
        item.fill_id for item in second.artifact.fills
    )
    assert tuple(item.trade_id for item in first.artifact.trades) == tuple(
        item.trade_id for item in second.artifact.trades
    )


def test_hardened_result_rejects_legacy_contract_version(tmp_path: Path) -> None:
    _, artifact = _flat_result(tmp_path, suffix="legacy-version")
    with pytest.raises(StrategyBacktestContractError, match="unsupported backtest result contract"):
        replace(artifact, version=ObjectVersion(1))


def test_sprint_13_golden_is_pinned_and_read_only(tmp_path: Path) -> None:
    context, artifact = _flat_result(tmp_path, suffix="sprint13-golden")
    authorization = context[9].record
    engine = context[7].engine_contract_ref
    expected = {
        "format": "backtest-result-hardening-v1",
        "strategy_fingerprint": fingerprint_record(context[6]),
        "instrument_fingerprint": fingerprint_record(context[10]),
        "authorization_fingerprint": fingerprint_record(authorization),
        "engine_fingerprint": engine.expected_fingerprint,
        "run_input_fingerprint": artifact.run_input_fingerprint,
        "order_ids": [str(item.order_id) for item in artifact.orders],
        "fill_ids": [str(item.fill_id) for item in artifact.fills],
        "trade_ids": [str(item.trade_id) for item in artifact.trades],
        "final_cash": artifact.final_cash,
        "final_equity": artifact.final_equity,
        "open_position": artifact.open_position.value,
        "trade_count": artifact.trade_count,
        "gross_pnl": artifact.gross_pnl,
        "net_pnl": artifact.net_pnl,
        "total_return": artifact.total_return,
        "max_drawdown": artifact.max_drawdown,
        "result_fingerprint": fingerprint_record(artifact),
    }
    assert json.loads(GOLDEN.read_text(encoding="utf-8")) == expected
    assert EXE_01.state is ExecutionState.PLANNED_CLOSED
