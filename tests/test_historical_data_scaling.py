"""Sprint 26 bounded multi-year historical CSV scaling tests."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from pathlib import Path

import pytest
from test_real_csv_onboarding import CLOCK, context

from ai_quant_lab.core.codec import encode
from ai_quant_lab.core.csv_import import (
    MAX_CONTROLLED_HISTORICAL_FILE_BYTES,
    MAX_CONTROLLED_HISTORICAL_ROWS,
    MAX_ROWS,
    CsvFileFailure,
    CsvInputScope,
    LocalCsvInputAdapter,
)
from ai_quant_lab.core.data import (
    DatasetLockId,
    DatasetManifest,
    InstrumentId,
    ObservationId,
    SourceId,
)
from ai_quant_lab.core.dataset_store import LocalDatasetRepository, RepositoryWriteStatus
from ai_quant_lab.core.market_data import (
    MarketBarId,
    MarketDataSchemaId,
    NormalizedBarManifest,
    TimeframeId,
)
from ai_quant_lab.core.model import DatasetId, ObjectVersion, ProvenanceId, TraceabilityRef

FOUR_YEAR_4H_BAR_BUDGET = 8_766
V1 = ObjectVersion(1)
FINGERPRINT = "sha256:" + "a" * 64


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
    assert FOUR_YEAR_4H_BAR_BUDGET > MAX_ROWS
    assert prepared.file_size <= MAX_CONTROLLED_HISTORICAL_FILE_BYTES


def test_scaled_row_limit_remains_fail_closed(tmp_path: Path) -> None:
    adapter = _adapter(tmp_path, MAX_CONTROLLED_HISTORICAL_ROWS + 1, "row-bound")

    with pytest.raises(CsvFileFailure, match="row limit"):
        adapter.prepare()


def _ref(object_id: object) -> TraceabilityRef:
    return TraceabilityRef(object_id, V1, FINGERPRINT)  # type: ignore[arg-type]


def test_four_year_manifest_storage_matches_scaled_historical_budget(tmp_path: Path) -> None:
    created = datetime(2026, 1, 2, tzinfo=UTC)
    start = datetime(2022, 1, 1, tzinfo=UTC)
    end = start + timedelta(hours=4 * (FOUR_YEAR_4H_BAR_BUDGET - 1))
    source_ref = _ref(SourceId("historical-source"))
    instrument_ref = _ref(InstrumentId("historical-instrument"))
    provenance_ref = _ref(ProvenanceId("historical-provenance"))
    timeframe_ref = _ref(TimeframeId("4h"))
    schema_ref = _ref(MarketDataSchemaId("historical-schema"))
    raw_lock_ref = _ref(DatasetLockId("historical-raw-lock"))

    raw_manifest = DatasetManifest(
        DatasetId("historical-raw-manifest"),
        V1,
        created,
        tuple(
            _ref(ObservationId(f"historical-observation-{index:05d}"))
            for index in range(FOUR_YEAR_4H_BAR_BUDGET)
        ),
        (source_ref,),
        (instrument_ref,),
        start,
        end,
        provenance_ref,
        V1,
    )
    normalized_manifest = NormalizedBarManifest(
        DatasetId("historical-normalized-manifest"),
        V1,
        created,
        tuple(
            _ref(MarketBarId(f"historical-bar-{index:05d}"))
            for index in range(FOUR_YEAR_4H_BAR_BUDGET)
        ),
        (source_ref,),
        (instrument_ref,),
        (timeframe_ref,),
        schema_ref,
        V1,
        raw_lock_ref,
        provenance_ref,
    )

    assert len(encode(raw_manifest)) > 1_000_000
    assert len(encode(normalized_manifest)) > 1_000_000
    store = LocalDatasetRepository(root=tmp_path / "manifest-vault", allowed_root=tmp_path)

    raw_write = store.store(raw_manifest)
    normalized_write = store.store(normalized_manifest)

    assert raw_write.status is RepositoryWriteStatus.STORED_NEW
    assert normalized_write.status is RepositoryWriteStatus.STORED_NEW
    assert store.load(raw_write.repository_key, DatasetManifest).record == raw_manifest
    assert (
        store.load(normalized_write.repository_key, NormalizedBarManifest).record
        == normalized_manifest
    )
