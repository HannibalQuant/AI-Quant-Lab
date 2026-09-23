"""Sprint 18 governed Pine ↔ Python parity tests."""

from __future__ import annotations

import csv
import io
from dataclasses import replace
from datetime import timedelta
from pathlib import Path

import pytest
from test_pine_strategy_intake import PROVENANCE_REF, _selected_context

from ai_quant_lab.core.dataset_store import LocalDatasetRepository, RepositoryWriteStatus
from ai_quant_lab.core.integrity import fingerprint_record
from ai_quant_lab.core.model import (
    ArtifactId,
    AuthorityBindingId,
    ObjectVersion,
    RunId,
    TraceabilityRef,
)
from ai_quant_lab.core.pine_python_parity import (
    PineExecutionEvidenceError,
    PinePythonParityAuthorityInvalid,
    PinePythonParityContext,
    evaluate_pine_python_parity,
    import_pine_execution_csv,
    verify_pine_python_parity_lineage,
)
from ai_quant_lab.core.pine_python_parity_contracts import (
    ParityMismatchType,
    ParityTolerancePolicy,
    PinePythonParityDecision,
    PinePythonParityRequest,
)
from ai_quant_lab.core.pine_strategy_intake import intake_pine_strategy

pytest_plugins = ("test_pine_strategy_intake",)

V1 = ObjectVersion(1)
PARITY_AUTHORITY_REF = TraceabilityRef(
    AuthorityBindingId("governed-pine-python-parity-authority"),
    V1,
    "sha256:" + "c" * 64,
)


def exact(record, object_id, version):
    return TraceabilityRef(object_id, version, fingerprint_record(record))


def _event_rows(backtest):
    trade_by_fill = {}
    for trade in backtest.trades:
        trade_by_fill[trade.entry_fill_id] = str(trade.trade_id)
        trade_by_fill[trade.exit_fill_id] = str(trade.trade_id)
    rows = []
    state = "FLAT"
    for index, (order, fill) in enumerate(zip(backtest.orders, backtest.fills, strict=True)):
        action = "ENTRY" if order.side.value == "BUY" else "EXIT"
        state = "LONG" if action == "ENTRY" else "FLAT"
        rows.append(
            {
                "event_index": str(index),
                "signal_time": order.signal_time.isoformat(),
                "execution_time": fill.fill_time.isoformat(),
                "action": action,
                "side": "LONG",
                "execution_price": fill.execution_price,
                "position_after": state,
                "quantity": fill.quantity,
                "commission": fill.commission,
                "trade_id": trade_by_fill.get(fill.fill_id, ""),
            }
        )
    return rows


def _csv_bytes(rows):
    out = io.StringIO(newline="")
    writer = csv.DictWriter(
        out,
        fieldnames=(
            "event_index",
            "signal_time",
            "execution_time",
            "action",
            "side",
            "execution_price",
            "position_after",
            "quantity",
            "commission",
            "trade_id",
        ),
        lineterminator="\n",
    )
    writer.writeheader()
    writer.writerows(rows)
    return out.getvalue().encode("utf-8")


@pytest.fixture
def parity_bundle(selection_bundle, tmp_path: Path):
    pine_request, pine_context, *_ = _selected_context(selection_bundle)
    pine_repository = LocalDatasetRepository(root=tmp_path / "pine", allowed_root=tmp_path)
    pine_exec = intake_pine_strategy(pine_request, context=pine_context, repository=pine_repository)
    source = pine_context.evidence
    policy = ParityTolerancePolicy(
        ArtifactId("pine-python-parity-tolerance-v1"),
        V1,
        True,
        "0",
        "0",
        "0",
        "0",
        "0",
        PARITY_AUTHORITY_REF,
        PROVENANCE_REF,
    )