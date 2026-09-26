"""Sprint 26 bounded multi-year historical CSV scaling tests."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from pathlib import Path

import pytest
from test_real_csv_onboarding import CLOCK, context

from ai_quant_lab.core.csv_import import (
    MAX_CONTROLLED_HISTORICAL_FILE_BYTES,
    MAX_CONTROLLED_HISTORICAL_ROWS,
    CsvFileFailure,
    CsvInputScope,
    LocalCsvInputAdapter,
)

FOUR_YEAR_4H_BAR_BUDGET = 8_766


def _write_valid_rows(path: Path, count: int) -> None:
    header = "bar_open_time,bar_close_time,open,high,low,close,volume,finality,availability_time\n"
    start = datetime(2022, 1, 1, tzinfo=UTC)
    rows: list[str] = []
    for index in range(count):
        opened = start + timedelta(hours=index)
        closed = opened + timedelta(hours=1)
        available = closed + timedelta(seconds=5)
        stamp = "%Y-%m-%dT%H:%M:%S.%fZ"
        rows.append(
            f"{opened.strftime(stamp)},{closed.strftime(stamp)},"
            f"100,101,99,100,1,final,{available.strftime(stamp)}\n"
        )
    path.write_text(header + "".join(rows), encoding="utf-8")


def _adapter(tmp_path: Path, count: int, suffix: str) -> LocalCsvInputAdapter:
    root = tmp_path / f"historical-{suffix}"
    root.mkdir()
    path = root / "history.csv"
    _write_valid_rows(path, count)
    request, _source, _instrument, schema, timeframe, _repository = context(
        tmp_path,
        path=path.resolve(),
        allowed_root=root.resolve(),
        suffix=suffix,
    )
    return LocalCsvInputAdapter(
        request.csv_request.ingestion.adapter_ref,
        request.csv_request,
        schema,
        timeframe,
        CLOCK,
        CsvInputScope.CONTROLLED_HISTORICAL,
    )


def test_four_year_4h_equivalent_row_budget_is_within_bounded_limits(tmp_path: Path) -> None:
    adapter = _adapter(tmp_path, FOUR_YEAR_4H_BAR_BUDGET, "four-year")
    prepared = adapter.prepare()

    assert MAX_CONTROLLED_HISTORICAL_ROWS >= FOUR_YEAR_4H_BAR_BUDGET
    assert prepared.row_count == FOUR_YEAR_4H_BAR_BUDGET
    assert not prepared.rejected
    assert prepared.file_size > 1_000_000
    assert prepared.file_size <= MAX_CONTROLLED_HISTORICAL_FILE_BYTES


def test_scaled_row_limit_remains_fail_closed(tmp_path: Path) -> None:
    adapter = _adapter(tmp_path, MAX_CONTROLLED_HISTORICAL_ROWS + 1, "row-bound")

    with pytest.raises(CsvFileFailure, match="row limit"):
        adapter.prepare()
