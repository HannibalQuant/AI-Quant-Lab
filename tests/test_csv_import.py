"""Repository-owned synthetic CSV end-to-end, determinism, and fail-closed attacks."""

from __future__ import annotations

import hashlib
import json
from dataclasses import FrozenInstanceError, replace
from datetime import UTC, datetime
from pathlib import Path
from typing import cast

import pytest

from ai_quant_lab.core.codec import GovernedRecord, decode, encode
from ai_quant_lab.core.csv_import import (
    CsvFileFailure,
    CsvImportAssemblyFailure,
    CsvImportKernel,
    CsvImportReport,
    CsvImportRequest,
    CsvImportStatus,
    CsvRowReason,
    LocalCsvInputAdapter,
    UnsafeCsvPath,
)
from ai_quant_lab.core.data import (
    DatasetLockId,
    InstrumentClass,
    InstrumentId,
    InstrumentIdentity,
    SourceId,
    SourceIdentity,
    SourceType,
)
from ai_quant_lab.core.ingestion import (
    DatasetAssemblyError,
    DeterministicClock,
    IngestionRequest,
    IngestionRequestId,
    IngestionSession,
    IngestionSessionId,
)
from ai_quant_lab.core.integrity import IntegrityMismatch, fingerprint_record, verify_integrity
from ai_quant_lab.core.market_data import (
    AlignmentKind,
    BarTimestampMeaning,
    GapDisposition,
    MarketDataSchema,
    MarketDataSchemaId,
    TimeframeId,
    TimeframeIdentity,
    TimeframeUnit,
    VolumeSemantic,
)
from ai_quant_lab.core.model import (
    AgentId,
    ArtifactId,
    AuditEvent,
    DatasetId,
    ObjectVersion,
    ProvenanceId,
    TraceabilityRef,
    VersionedRef,
)

ROOT = Path(__file__).parent / "fixtures" / "market_data"
V1 = ObjectVersion(1)
F = "sha256:" + "a" * 64
CLOCK = DeterministicClock(datetime(2025, 1, 2, tzinfo=UTC))
CUTOFF = datetime(2025, 1, 1, 23, tzinfo=UTC)


def context(
    filename: str = "valid_1h.csv",
    *,
    root: Path = ROOT,
    session_name: str = "csv-session-one",
    count: int = 1,
    cutoff: datetime = CUTOFF,
    volume: bool = True,
    expected_sha: str | None = None,
) -> tuple[
    CsvImportRequest,
    LocalCsvInputAdapter,
    SourceIdentity,
    InstrumentIdentity,
    MarketDataSchema,
    TimeframeIdentity,
]:
    source = SourceIdentity(
        SourceId("synthetic-csv-source"),
        V1,
        "Synthetic Fixture",
        SourceType.SYNTHETIC_FIXTURE,
        "fixture-csv",
        "fixture-v1",
        None,
        V1,
    )
    instrument = InstrumentIdentity(
        InstrumentId("synthetic-csv-spot"),
        V1,
        "TESTUSD",
        InstrumentClass.SPOT,
        "TEST",
        "USD",
        None,
        None,
        V1,
    )
    tf = TimeframeIdentity(
        TimeframeId(f"{count}h"),
        V1,
        TimeframeUnit.HOUR,
        count,
        AlignmentKind.UTC_EPOCH_FIXED,
        V1,
    )
    tf_ref = TraceabilityRef(tf.timeframe_id, V1, fingerprint_record(tf))
    schema = MarketDataSchema(
        MarketDataSchemaId("synthetic-csv-ohlcv"),
        V1,
        tf_ref,
        BarTimestampMeaning.OPEN,
        "bar_open_time",
        "bar_close_time",
        "open",
        "high",
        "low",
        "close",
        "volume" if volume else None,
        "finality",
        VolumeSemantic.BASE if volume else VolumeSemantic.ABSENT,
        V1,
    )
    adapter_ref = TraceabilityRef(ArtifactId("fixture-csv-adapter"), V1, F)
    ingestion = IngestionRequest(
        IngestionRequestId("fixture-csv-request"),
        V1,
        adapter_ref,
        TraceabilityRef(source.source_id, V1, fingerprint_record(source)),
        TraceabilityRef(instrument.instrument_id, V1, fingerprint_record(instrument)),
        TraceabilityRef(ProvenanceId("fixture-raw"), V1, F),
        TraceabilityRef(ProvenanceId("fixture-manifest"), V1, F),
        TraceabilityRef(ProvenanceId("fixture-lock"), V1, F),
        DatasetId("fixture-raw-dataset"),
        V1,
        DatasetLockId("fixture-raw-lock"),
        V1,
        cutoff,
        AgentId("synthetic-fixture-producer"),
        V1,
    )
    session = IngestionSession(
        IngestionSessionId(session_name),
        V1,
        VersionedRef(ingestion.request_id, ingestion.version),
        CLOCK.now(),
    )
    request = CsvImportRequest(
        ingestion,
        session,
        root / filename,
        root,
        TraceabilityRef(schema.schema_id, V1, fingerprint_record(schema)),
        tf_ref,
        DatasetId("fixture-normalized-dataset"),
        V1,
        DatasetLockId("fixture-normalized-lock"),
        V1,
        V1,
        TraceabilityRef(ProvenanceId("fixture-normalization"), V1, F),
        TraceabilityRef(ProvenanceId("fixture-normalized"), V1, F),
        expected_sha,
    )
    return (
        request,
        LocalCsvInputAdapter(adapter_ref, request, schema, tf, CLOCK),
        source,
        instrument,
        schema,
        tf,
    )


def run(
    filename: str = "valid_1h.csv",
    *,
    root: Path = ROOT,
    session_name: str = "csv-session-one",
    count: int = 1,
    cutoff: datetime = CUTOFF,
    volume: bool = True,
    expected_sha: str | None = None,
) -> CsvImportReport:
    request, adapter, source, instrument, schema, tf = context(
        filename,
        root=root,
        session_name=session_name,
        count=count,
        cutoff=cutoff,
        volume=volume,
        expected_sha=expected_sha,
    )
    return CsvImportKernel().import_fixture(request, adapter, source, instrument, schema, tf, CLOCK)


def fixture(tmp_path: Path, data: str, name: str = "attack.csv") -> tuple[Path, str]:
    root = tmp_path / "tests" / "fixtures" / "market_data"
    root.mkdir(parents=True)
    (root / name).write_text(data, encoding="utf-8")
    return root, name


HEADER = "bar_open_time,bar_close_time,open,high,low,close,volume,finality,availability_time\n"
ROW = (
    "2025-01-01T10:00:00.000000Z,2025-01-01T11:00:00.000000Z,1,2,0,1.5,10,final,"
    "2025-01-01T11:00:05.000000Z\n"
)


def test_positive_end_to_end_and_golden_file_hash() -> None:
    report = run()
    assert report.status is CsvImportStatus.SUCCESS
    assert (report.row_count, len(report.normalized_bars), report.ingestion.accepted_count) == (
        3,
        3,
        3,
    )
    assert report.file_sha256 == hashlib.sha256((ROOT / "valid_1h.csv").read_bytes()).hexdigest()
    assert (
        report.normalized_manifest.raw_dataset_lock_ref.expected_fingerprint
        == fingerprint_record(report.ingestion.dataset_lock)
    )
    missing = [
        finding
        for finding in report.gap_findings
        if finding.disposition is GapDisposition.MECHANICAL_GAP
    ]
    assert len(missing) == 1 and missing[0].missing_intervals == 1
    assert {event.action for event in report.audit_events} >= {
        "csv.import_started",
        "csv.file_validated",
        "csv.row_accepted",
        "csv.bar_normalized",
        "csv.normalized_dataset_created",
        "csv.import_completed",
    }
    assert all(
        event.context == (("file_sha256", report.file_sha256),) for event in report.audit_events
    )
    assert decode(encode(report.audit_events[0]), AuditEvent) == report.audit_events[0]
    for item in (
        report.ingestion.manifest,
        report.ingestion.dataset_lock,
        *report.normalized_bars,
        report.normalized_manifest,
        report.normalized_lock,
    ):
        record = cast(GovernedRecord, item)
        verify_integrity(record, fingerprint_record(record))


def test_pinned_golden_vector_is_read_only() -> None:
    golden = json.loads(
        (Path(__file__).parent / "golden" / "csv_import_valid_1h_v1.json").read_text(
            encoding="utf-8"
        )
    )
    report = run()
    assert golden["file_sha256"] == report.file_sha256
    assert (golden["rows"], golden["accepted"], golden["csv_rejected"], golden["quarantined"]) == (
        report.row_count,
        report.ingestion.accepted_count,
        len(report.csv_rejections),
        report.ingestion.quarantined_count,
    )
    assert golden["raw_sha256"] == [
        fingerprint_record(x) for x in report.ingestion.accepted_observations
    ]
    assert golden["bar_sha256"] == [fingerprint_record(x) for x in report.normalized_bars]
    assert golden["raw_manifest_sha256"] == fingerprint_record(report.ingestion.manifest)
    assert golden["raw_lock_sha256"] == fingerprint_record(report.ingestion.dataset_lock)
    assert golden["normalized_manifest_sha256"] == fingerprint_record(report.normalized_manifest)
    assert golden["normalized_lock_sha256"] == fingerprint_record(report.normalized_lock)


def test_4h_and_lookahead_cutoff() -> None:
    assert len(run("valid_4h.csv", count=4).normalized_bars) == 2
    with pytest.raises(DatasetAssemblyError):
        run("cutoff_1h.csv", cutoff=datetime(2025, 1, 1, 12, tzinfo=UTC))
    eligible = run("cutoff_1h.csv", cutoff=datetime(2025, 1, 1, 12, 0, 5, tzinfo=UTC))
    assert eligible.normalized_bars[0].availability_time > eligible.normalized_bars[0].bar_close


def test_replay_reordering_and_session_separation() -> None:
    first = run()
    again = run(session_name="csv-session-two")
    reordered = run("reordered_1h.csv")
    assert first.semantic_snapshot == again.semantic_snapshot == reordered.semantic_snapshot
    assert first.file_sha256 != reordered.file_sha256
    assert first.ingestion.session.session_id != again.ingestion.session.session_id
    assert tuple(fingerprint_record(x) for x in first.normalized_bars) == tuple(
        fingerprint_record(x) for x in again.normalized_bars
    )


def test_mixed_row_rejection_is_explicit() -> None:
    report = run("mixed_1h.csv")
    assert report.status is CsvImportStatus.SUCCESS_WITH_REJECTIONS
    assert (report.row_count, len(report.csv_rejections), report.ingestion.accepted_count) == (
        3,
        1,
        2,
    )
    assert report.csv_rejections[0].reason is CsvRowReason.DECIMAL
    assert len(report.normalized_manifest.bar_refs) == 2
    assert "csv.row_rejected" in {event.action for event in report.audit_events}


@pytest.mark.parametrize(
    "invalid", ["../escape.csv", "missing.csv", "attack.txt", "https://example.com/a.csv"]
)
def test_unsafe_path_rejected(invalid: str) -> None:
    _, adapter, *_ = context(invalid)
    with pytest.raises(UnsafeCsvPath):
        adapter.prepare()


def test_absolute_outside_and_directory_rejected(tmp_path: Path) -> None:
    outside = tmp_path / "outside.csv"
    outside.write_text(HEADER + ROW, encoding="utf-8")
    req, adapter, *_ = context()
    with pytest.raises(UnsafeCsvPath):
        replace(adapter, request=replace(req, fixture_path=outside)).prepare()
    with pytest.raises(UnsafeCsvPath):
        replace(adapter, request=replace(req, fixture_path=ROOT)).prepare()


def test_symlink_escape_rejected(tmp_path: Path) -> None:
    root = tmp_path / "tests" / "fixtures" / "market_data"
    root.mkdir(parents=True)
    target = tmp_path / "outside.csv"
    target.write_text(HEADER + ROW, encoding="utf-8")
    (root / "link.csv").symlink_to(target)
    _, adapter, *_ = context("link.csv", root=root)
    with pytest.raises(UnsafeCsvPath):
        adapter.prepare()


@pytest.mark.parametrize(
    "header",
    [
        HEADER.replace("open,high", "open,open"),
        HEADER.replace("open,high", "high"),
        HEADER.replace("open,high", "Open,high"),
        HEADER.replace("open,high", "open,high,unknown"),
        HEADER.replace("open,high", ",high"),
    ],
)
def test_headers_fail_file_level(tmp_path: Path, header: str) -> None:
    root, name = fixture(tmp_path, header + ROW)
    _, adapter, *_ = context(name, root=root)
    with pytest.raises(CsvFileFailure):
        adapter.prepare()


@pytest.mark.parametrize(
    "replacement,reason",
    [
        ("NaN", CsvRowReason.DECIMAL),
        ("Infinity", CsvRowReason.DECIMAL),
        ("abc", CsvRowReason.DECIMAL),
        ("", CsvRowReason.EMPTY),
        (" 1 ", CsvRowReason.DECIMAL),
    ],
)
def test_malformed_decimal_is_row_rejection(
    tmp_path: Path, replacement: str, reason: CsvRowReason
) -> None:
    root, name = fixture(tmp_path, HEADER + ROW.replace(",1,2,0,1.5,", f",{replacement},2,0,1.5,"))
    _, adapter, *_ = context(name, root=root)
    assert adapter.prepare().rejected[0].reason is reason


@pytest.mark.parametrize(
    "changed,reason",
    [
        (ROW.replace(".000000Z", "Z", 1), CsvRowReason.TIMESTAMP),
        (ROW.replace(".000000Z", "+01:00", 1), CsvRowReason.TIMESTAMP),
        (ROW.replace("2025-01-01T10:00", "2025-13-01T10:00"), CsvRowReason.TIMESTAMP),
        (
            ROW.replace("2025-01-01T11:00:00.000000Z", "2025-01-01T10:00:00.000000Z", 1),
            CsvRowReason.INTERVAL,
        ),
        (ROW.replace(",final,", ",yes,"), CsvRowReason.FINALITY),
    ],
)
def test_timestamp_interval_and_finality_row_failures(
    tmp_path: Path, changed: str, reason: CsvRowReason
) -> None:
    root, name = fixture(tmp_path, HEADER + changed)
    _, adapter, *_ = context(name, root=root)
    assert adapter.prepare().rejected[0].reason is reason


def test_file_bytes_encoding_and_hash_fail_closed(tmp_path: Path) -> None:
    root, name = fixture(tmp_path, HEADER + ROW)
    _, adapter, *_ = context(name, root=root, expected_sha="0" * 64)
    with pytest.raises(CsvFileFailure, match="fingerprint"):
        adapter.prepare()
    (root / name).write_bytes(b"\xef\xbb\xbf" + (HEADER + ROW).encode())
    _, adapter, *_ = context(name, root=root)
    with pytest.raises(CsvFileFailure, match="BOM"):
        adapter.prepare()
    (root / name).write_bytes(b"\xff" + (HEADER + ROW).encode())
    with pytest.raises(CsvFileFailure, match="UTF-8"):
        adapter.prepare()


def test_physical_duplicate_and_conflict_are_never_winners(tmp_path: Path) -> None:
    root, name = fixture(tmp_path, HEADER + ROW + ROW)
    repeated = run(name, root=root)
    assert repeated.status is CsvImportStatus.SUCCESS_WITH_REJECTIONS
    assert (repeated.ingestion.accepted_count, repeated.ingestion.quarantined_count) == (1, 1)
    assert len(repeated.normalized_manifest.bar_refs) == 1
    different = ROW.replace(",1,2,0,1.5,", ",1,3,0,2,")
    (root / name).write_text(HEADER + ROW + different, encoding="utf-8")
    with pytest.raises(DatasetAssemblyError):
        run(name, root=root)


def test_all_rejected_or_incomplete_never_locks(tmp_path: Path) -> None:
    root, name = fixture(tmp_path, HEADER + ROW.replace(",1,2,0,1.5,", ",abc,2,0,1.5,"))
    with pytest.raises(DatasetAssemblyError):
        run(name, root=root)
    (root / name).write_text(HEADER + ROW.replace(",final,", ",incomplete,"), encoding="utf-8")
    with pytest.raises(CsvImportAssemblyFailure):
        run(name, root=root)


def test_schema_binding_and_unknown_execution_column(tmp_path: Path) -> None:
    root, name = fixture(tmp_path, HEADER.replace("open,high", "open,signal_buy,high") + ROW)
    _, adapter, *_ = context(name, root=root)
    with pytest.raises(CsvFileFailure):
        adapter.prepare()
    req, adapter, _, _, _, _ = context()
    with pytest.raises(CsvFileFailure):
        replace(
            adapter,
            request=replace(
                req, schema_ref=TraceabilityRef(MarketDataSchemaId("wrong-schema"), V1, F)
            ),
        ).prepare()


def test_tampering_and_immutable_report() -> None:
    report = run()
    with pytest.raises(FrozenInstanceError):
        report.file_size = 0  # type: ignore[misc]  # deliberately attempt frozen-record mutation
    raw = report.ingestion.accepted_observations[0]
    bar = report.normalized_bars[0]
    for original, changed in (
        (raw, replace(raw, observation_id=raw.observation_id.new())),
        (bar, replace(bar, close=bar.open)),
    ):
        with pytest.raises(IntegrityMismatch):
            verify_integrity(changed, fingerprint_record(original))


def test_file_line_endings_and_column_order_are_not_dataset_semantics(tmp_path: Path) -> None:
    content = (ROOT / "valid_1h.csv").read_text(encoding="utf-8")
    root, name = fixture(tmp_path, content.replace("\n", "\r\n"))
    crlf = run(name, root=root)
    assert crlf.file_sha256 != run().file_sha256
    assert crlf.semantic_snapshot == run().semantic_snapshot
    rows = content.splitlines()
    reordered = [line.split(",") for line in rows]
    swapped = "\n".join(",".join([cells[-1], *cells[:-1]]) for cells in reordered) + "\n"
    (root / name).write_text(swapped, encoding="utf-8")
    assert run(name, root=root).semantic_snapshot == run().semantic_snapshot


def test_missing_volume_is_not_zero(tmp_path: Path) -> None:
    root, name = fixture(
        tmp_path, HEADER.replace("volume,", "") + ROW.replace(",10,final,", ",final,")
    )
    absent = run(name, root=root, volume=False)
    zero = run()
    assert absent.normalized_bars[0].volume is None
    assert zero.normalized_bars[1].volume is not None
    assert zero.normalized_bars[1].volume.text == "0"
    (root / name).write_text(HEADER + ROW.replace(",10,final,", ",,final,"), encoding="utf-8")
    _, adapter, *_ = context(name, root=root)
    assert adapter.prepare().rejected[0].reason is CsvRowReason.EMPTY


def test_bad_geometry_rejected_after_raw_acceptance(tmp_path: Path) -> None:
    root, name = fixture(tmp_path, HEADER + ROW)
    # Distinct event row, while structural OHLC geometry fails only at normalization.
    (root / name).write_text(
        HEADER + ROW + "2025-01-01T11:00:00.000000Z,2025-01-01T12:00:00.000000Z,1,0,2,1.5,10,final,"
        "2025-01-01T12:00:05.000000Z\n",
        encoding="utf-8",
    )
    report = run(name, root=root)
    assert report.ingestion.accepted_count == 2
    assert len(report.normalization_rejections) == 1
    assert report.status is CsvImportStatus.SUCCESS_WITH_REJECTIONS
    assert len(report.normalized_manifest.bar_refs) == 1


def test_incomplete_is_excluded_from_finalized_manifest(tmp_path: Path) -> None:
    root, name = fixture(
        tmp_path,
        HEADER
        + ROW
        + "2025-01-01T11:00:00.000000Z,2025-01-01T12:00:00.000000Z,1,2,0,1.5,10,incomplete,"
        "2025-01-01T11:00:05.000000Z\n",
    )
    report = run(name, root=root)
    assert len(report.incomplete_bars) == 1
    assert len(report.normalized_manifest.bar_refs) == 1
    assert report.status is CsvImportStatus.SUCCESS_WITH_REJECTIONS


def test_tampered_manifest_and_locks() -> None:
    report = run()
    for original, changed in (
        (report.normalized_manifest, replace(report.normalized_manifest, version=ObjectVersion(2))),
        (
            report.normalized_lock,
            replace(report.normalized_lock, temporal_cutoff=datetime(2025, 1, 1, 22, tzinfo=UTC)),
        ),
        (
            report.ingestion.dataset_lock,
            replace(
                report.ingestion.dataset_lock, temporal_cutoff=datetime(2025, 1, 1, 22, tzinfo=UTC)
            ),
        ),
    ):
        with pytest.raises(IntegrityMismatch):
            verify_integrity(changed, fingerprint_record(original))


def test_resource_bounds_and_row_width(tmp_path: Path) -> None:
    root, name = fixture(tmp_path, HEADER + ROW.rstrip("\n") + ",extra\n")
    _, adapter, *_ = context(name, root=root)
    assert adapter.prepare().rejected[0].reason is CsvRowReason.WIDTH
    (root / name).write_text(
        HEADER + ROW.replace(",1,2,0,1.5,", f",{'9' * 260},2,0,1.5,"), encoding="utf-8"
    )
    assert adapter.prepare().rejected[0].reason is CsvRowReason.RESOURCE_LIMIT
    (root / name).write_bytes(b"x" * 1_000_001)
    with pytest.raises(CsvFileFailure, match="byte bound"):
        adapter.prepare()


def test_exact_contract_version_and_wrong_timeframe() -> None:
    req, adapter, source, instrument, schema, _ = context()
    with pytest.raises(CsvFileFailure):
        replace(req, contract_version=ObjectVersion(2))
    wrong = TimeframeIdentity(
        TimeframeId("4h"), V1, TimeframeUnit.HOUR, 4, AlignmentKind.UTC_EPOCH_FIXED, V1
    )
    with pytest.raises(CsvFileFailure):
        CsvImportKernel().import_fixture(req, adapter, source, instrument, schema, wrong, CLOCK)
