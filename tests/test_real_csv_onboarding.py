"""Sprint 8 controlled real historical CSV onboarding and hostile-input tests."""

from __future__ import annotations

import hashlib
import json
import os
from dataclasses import replace
from datetime import UTC, datetime
from pathlib import Path

import pytest

from ai_quant_lab.core.codec import GovernedRecord, decode, encode
from ai_quant_lab.core.csv_import import (
    MAX_COLUMNS,
    MAX_CONTROLLED_HISTORICAL_FILE_BYTES,
    MAX_FIELD_LENGTH,
    MAX_LINE_BYTES,
    CsvFileFailure,
    CsvImportAssemblyFailure,
    CsvImportRequest,
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
from ai_quant_lab.core.dataset_store import LocalDatasetRepository, repository_key
from ai_quant_lab.core.ingestion import (
    DeterministicClock,
    IngestionRequest,
    IngestionRequestId,
    IngestionSession,
    IngestionSessionId,
    IngestionSourceBoundary,
)
from ai_quant_lab.core.integrity import fingerprint_record
from ai_quant_lab.core.market_data import (
    AlignmentKind,
    BarTimestampMeaning,
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
    DatasetId,
    GovernedId,
    ObjectVersion,
    ProvenanceId,
    TraceabilityRef,
    VersionedRef,
)
from ai_quant_lab.core.real_csv_contracts import (
    AcquisitionMethod,
    AvailabilitySemantics,
    CsvAdmissionStatus,
    CsvTrustState,
    DuplicatePolicy,
    MissingDataPolicy,
    OrderingPolicy,
    PriceDomain,
    RealCsvAdmissionRecord,
    RealCsvSourceDeclaration,
    ResearchEligibilityState,
    RetentionClassification,
    SourcePermissionState,
    TimestampSemantics,
)
from ai_quant_lab.core.real_csv_onboarding import (
    RealCsvOnboardingError,
    RealCsvOnboardingRequest,
    RealCsvOnboardingResult,
    onboard_real_csv,
    verify_real_csv_lineage,
)
from ai_quant_lab.core.tradingview_csv_adapter import (
    TradingViewCsvAdapterPolicy,
    normalize_tradingview_csv,
    write_canonical_csv,
)

V1 = ObjectVersion(1)
CLOCK = DeterministicClock(datetime(2025, 2, 2, tzinfo=UTC))
FIXTURE_ROOT = (Path(__file__).parent / "fixtures" / "real_csv").resolve()
VALID = FIXTURE_ROOT / "repository_owned_external_style_1h.csv"
HEADER = "bar_open_time,bar_close_time,open,high,low,close,volume,finality,availability_time\n"
ROW_1 = (
    "2025-02-01T00:00:00.000000Z,2025-02-01T01:00:00.000000Z,100,102,99,101,10,"
    "final,2025-02-01T01:00:05.000000Z\n"
)
ROW_2 = (
    "2025-02-01T01:00:00.000000Z,2025-02-01T02:00:00.000000Z,101,103,100,102,11,"
    "final,2025-02-01T02:00:05.000000Z\n"
)


def exact(record: GovernedRecord, object_id: GovernedId) -> TraceabilityRef:
    return TraceabilityRef(object_id, V1, fingerprint_record(record))


def context(
    tmp_path: Path,
    *,
    path: Path = VALID,
    allowed_root: Path = FIXTURE_ROOT,
    suffix: str = "one",
    permission: SourcePermissionState = SourcePermissionState.DECLARED_PERMITTED,
    retention: RetentionClassification = RetentionClassification.DECLARED_LOCAL_ONLY,
    timestamps: TimestampSemantics = TimestampSemantics.BAR_OPEN_AND_CLOSE_UTC,
    availability: AvailabilitySemantics = AvailabilitySemantics.EXPLICIT_SOURCE_AVAILABILITY_UTC,
    missing: MissingDataPolicy = MissingDataPolicy.RECORD_GAPS,
    acquired_at: datetime | None = None,
    provenance_note: str = "operator declaration is recorded, not independently authenticated",
) -> tuple[
    RealCsvOnboardingRequest,
    SourceIdentity,
    InstrumentIdentity,
    MarketDataSchema,
    TimeframeIdentity,
    LocalDatasetRepository,
]:
    source = SourceIdentity(
        SourceId(f"external-file-source-{suffix}"),
        V1,
        "Declared Local Provider",
        SourceType.FILE_SNAPSHOT,
        "operator-supplied-csv",
        "declared-v1",
        None,
        V1,
    )
    instrument = InstrumentIdentity(
        InstrumentId(f"external-spot-{suffix}"),
        V1,
        "EXTUSD",
        InstrumentClass.SPOT,
        "EXT",
        "USD",
        None,
        None,
        V1,
    )
    timeframe = TimeframeIdentity(
        TimeframeId("1h"),
        V1,
        TimeframeUnit.HOUR,
        1,
        AlignmentKind.UTC_EPOCH_FIXED,
        V1,
    )
    schema = MarketDataSchema(
        MarketDataSchemaId(f"external-ohlcv-{suffix}"),
        V1,
        exact(timeframe, timeframe.timeframe_id),
        BarTimestampMeaning.OPEN,
        "bar_open_time",
        "bar_close_time",
        "open",
        "high",
        "low",
        "close",
        "volume",
        "finality",
        VolumeSemantic.BASE,
        V1,
    )
    actor = AgentId(f"operator-{suffix}")
    declaration = RealCsvSourceDeclaration(
        ProvenanceId(f"real-csv-declaration-{suffix}"),
        V1,
        exact(source, source.source_id),
        exact(instrument, instrument.instrument_id),
        exact(timeframe, timeframe.timeframe_id),
        exact(schema, schema.schema_id),
        source.provider,
        AcquisitionMethod.OPERATOR_LOCAL_FILE,
        "declared-spot-market",
        acquired_at,
        timestamps,
        availability,
        "explicit UTC Z timestamps; no filename inference",
        (
            ("availability_time", "availability_time"),
            ("bar_close", "bar_close_time"),
            ("bar_open", "bar_open_time"),
            ("close", "close"),
            ("finality", "finality"),
            ("high", "high"),
            ("low", "low"),
            ("open", "open"),
            ("volume", "volume"),
        ),
        PriceDomain.POSITIVE_ONLY,
        "declared OHLC bar geometry",
        VolumeSemantic.BASE,
        "final rows are available no earlier than bar close",
        missing,
        DuplicatePolicy.REJECT_ALL,
        OrderingPolicy.STRICT_ASCENDING_EVENT_TIME,
        permission,
        "repository-owned fixture; no external redistribution grant",
        retention,
        "operator-declared local retention only",
        "redistribution prohibited by this workflow",
        actor,
        provenance_note,
        V1,
    )
    declaration_ref = exact(declaration, declaration.provenance_id)
    adapter_ref = TraceabilityRef(
        ArtifactId("controlled-real-csv-adapter"), V1, "sha256:" + "a" * 64
    )
    ingestion = IngestionRequest(
        IngestionRequestId(f"real-csv-request-{suffix}"),
        V1,
        adapter_ref,
        declaration.source_ref,
        declaration.instrument_ref,
        declaration_ref,
        declaration_ref,
        declaration_ref,
        DatasetId(f"real-raw-dataset-{suffix}"),
        V1,
        DatasetLockId(f"real-raw-lock-{suffix}"),
        V1,
        datetime(2025, 2, 2, tzinfo=UTC),
        actor,
        V1,
        IngestionSourceBoundary.CONTROLLED_FILE_SNAPSHOT,
    )
    session = IngestionSession(
        IngestionSessionId(f"real-csv-session-{suffix}"),
        V1,
        VersionedRef(ingestion.request_id, V1),
        CLOCK.now(),
    )
    csv_request = CsvImportRequest(
        ingestion,
        session,
        path,
        allowed_root,
        declaration.schema_ref,
        declaration.timeframe_ref,
        DatasetId(f"real-normalized-dataset-{suffix}"),
        V1,
        DatasetLockId(f"real-normalized-lock-{suffix}"),
        V1,
        V1,
        declaration_ref,
        declaration_ref,
    )
    onboarding = RealCsvOnboardingRequest(
        ArtifactId(f"real-csv-admission-{suffix}"), declaration, csv_request
    )
    store_root = tmp_path / f"vault-{suffix}"
    return (
        onboarding,
        source,
        instrument,
        schema,
        timeframe,
        LocalDatasetRepository(root=store_root, allowed_root=tmp_path),
    )


def run(
    tmp_path: Path,
    *,
    path: Path = VALID,
    allowed_root: Path = FIXTURE_ROOT,
    suffix: str = "one",
    permission: SourcePermissionState = SourcePermissionState.DECLARED_PERMITTED,
    retention: RetentionClassification = RetentionClassification.DECLARED_LOCAL_ONLY,
    timestamps: TimestampSemantics = TimestampSemantics.BAR_OPEN_AND_CLOSE_UTC,
    availability: AvailabilitySemantics = AvailabilitySemantics.EXPLICIT_SOURCE_AVAILABILITY_UTC,
    missing: MissingDataPolicy = MissingDataPolicy.RECORD_GAPS,
    acquired_at: datetime | None = None,
) -> tuple[RealCsvOnboardingRequest, LocalDatasetRepository, RealCsvOnboardingResult]:
    request, source, instrument, schema, timeframe, repository = context(
        tmp_path,
        path=path,
        allowed_root=allowed_root,
        suffix=suffix,
        permission=permission,
        retention=retention,
        timestamps=timestamps,
        availability=availability,
        missing=missing,
        acquired_at=acquired_at,
    )
    result = onboard_real_csv(
        request,
        source=source,
        instrument=instrument,
        schema=schema,
        timeframe=timeframe,
        clock=CLOCK,
        repository=repository,
    )
    return request, repository, result


def test_tradingview_adapter_output_flows_into_real_csv_onboarding_with_exact_lineage(
    tmp_path: Path,
) -> None:
    root = (tmp_path / "tradingview-integration").resolve()
    root.mkdir()
    source = root / "tradingview.csv"
    start = int(datetime(2025, 2, 1, tzinfo=UTC).timestamp())
    source.write_text(
        "time,open,high,low,close,Volume,EMA\n"
        f"{start},100,102,99,101,10,100\n"
        f"{start + 3600},101,103,100,102,11,101\n"
        f"{start + 7200},102,104,101,103,12,102\n",
        encoding="utf-8",
    )
    timeframe = TimeframeIdentity(
        TimeframeId("1h"),
        V1,
        TimeframeUnit.HOUR,
        1,
        AlignmentKind.UTC_EPOCH_FIXED,
        V1,
    )
    normalized = normalize_tradingview_csv(
        source,
        allowed_root=root,
        timeframe=timeframe,
        policy=TradingViewCsvAdapterPolicy(
            time_column="time",
            volume_column="Volume",
            timestamp_unit="unix_seconds",
            source_timezone="UTC",
            derive_bar_close_from_timeframe=True,
            derive_finality_from_historical_export=True,
            availability_at_bar_close=True,
        ),
    )
    canonical = root / "canonical.csv"
    write_canonical_csv(normalized, canonical, allowed_root=root)

    request, source_identity, instrument, schema, governed_timeframe, repository = context(
        tmp_path,
        path=canonical.resolve(),
        allowed_root=root,
        suffix="tv-adapter",
        timestamps=TimestampSemantics.BAR_OPEN_UTC_CLOSE_DERIVED_FROM_TIMEFRAME,
        availability=AvailabilitySemantics.DERIVED_BAR_CLOSE_UTC,
        provenance_note=normalized.provenance_note,
    )
    result = onboard_real_csv(
        request,
        source=source_identity,
        instrument=instrument,
        schema=schema,
        timeframe=governed_timeframe,
        clock=CLOCK,
        repository=repository,
    )

    assert result.admission.status is CsvAdmissionStatus.ADMITTED
    assert result.report is not None
    assert result.admission.file_sha256 == "sha256:" + normalized.canonical_sha256
    assert normalized.source_sha256 in request.declaration.provenance_note
    verification = verify_real_csv_lineage(
        admission=result.admission,
        declaration=request.declaration,
        report=result.report,
    )
    assert verification.file_sha256 == result.admission.file_sha256

    bad_note = (
        f"tv_adapter_v1;source_sha256={normalized.source_sha256};"
        f"canonical_sha256={'0' * 64}"
    )
    bad_request, bad_source, bad_instrument, bad_schema, bad_timeframe, bad_repository = context(
        tmp_path,
        path=canonical.resolve(),
        allowed_root=root,
        suffix="tv-adapter-bad-lineage",
        timestamps=TimestampSemantics.BAR_OPEN_UTC_CLOSE_DERIVED_FROM_TIMEFRAME,
        availability=AvailabilitySemantics.DERIVED_BAR_CLOSE_UTC,
        provenance_note=bad_note,
    )
    with pytest.raises(RealCsvOnboardingError, match="canonical hash"):
        onboard_real_csv(
            bad_request,
            source=bad_source,
            instrument=bad_instrument,
            schema=bad_schema,
            timeframe=bad_timeframe,
            clock=CLOCK,
            repository=bad_repository,
        )


def test_valid_real_csv_is_admitted_persisted_reloaded_and_lineage_verified(
    tmp_path: Path,
) -> None:
    request, repository, result = run(tmp_path)
    assert result.admission.status is CsvAdmissionStatus.ADMITTED
    assert result.admission.trust_state is CsvTrustState.NOT_TRUSTED
    assert result.admission.research_eligibility is ResearchEligibilityState.NOT_RESEARCH_ELIGIBLE
    assert result.admission.file_size == len(VALID.read_bytes())
    assert result.admission.ingestion_configuration_fingerprint.startswith("sha256:")
    assert request.declaration.declared_acquisition_time is None
    assert result.report is not None and len(result.report.normalized_bars) == 3
    assert len(result.writes) == 12
    loaded_declaration = repository.load(
        repository_key(request.declaration), RealCsvSourceDeclaration
    ).record
    loaded_admission = repository.load(
        repository_key(result.admission), RealCsvAdmissionRecord
    ).record
    assert loaded_declaration == request.declaration
    assert loaded_admission == result.admission
    assert (
        tuple(
            repository.load(repository_key(observation), type(observation)).record
            for observation in result.report.ingestion.accepted_observations
        )
        == result.report.ingestion.accepted_observations
    )
    assert (
        tuple(
            repository.load(repository_key(bar), type(bar)).record
            for bar in result.report.normalized_bars
        )
        == result.report.normalized_bars
    )
    assert decode(encode(result.admission), RealCsvAdmissionRecord) == result.admission
    verification = verify_real_csv_lineage(
        admission=loaded_admission,
        declaration=loaded_declaration,
        report=result.report,
    )
    assert verification.file_sha256 == result.admission.file_sha256


def test_declared_acquisition_time_and_deterministic_outputs_are_preserved(
    tmp_path: Path,
) -> None:
    acquired = datetime(2025, 2, 1, 4, tzinfo=UTC)
    request, source, instrument, schema, timeframe, first_repository = context(
        tmp_path, acquired_at=acquired
    )
    first = onboard_real_csv(
        request,
        source=source,
        instrument=instrument,
        schema=schema,
        timeframe=timeframe,
        clock=CLOCK,
        repository=first_repository,
    )
    second_repository = LocalDatasetRepository(
        root=tmp_path / "vault-deterministic-restart", allowed_root=tmp_path
    )
    second = onboard_real_csv(
        request,
        source=source,
        instrument=instrument,
        schema=schema,
        timeframe=timeframe,
        clock=CLOCK,
        repository=second_repository,
    )
    assert request.declaration.declared_acquisition_time == acquired
    assert first.report is not None and second.report is not None
    assert (
        first.report.ingestion.accepted_observations
        == second.report.ingestion.accepted_observations
    )
    assert first.report.ingestion.manifest == second.report.ingestion.manifest
    assert first.report.ingestion.dataset_lock == second.report.ingestion.dataset_lock
    assert first.admission == second.admission


def test_file_identity_is_content_based_while_path_identity_remains_explicit(
    tmp_path: Path,
) -> None:
    first = tmp_path / "inputs-a"
    second = tmp_path / "inputs-b"
    first.mkdir()
    second.mkdir()
    bytes_ = VALID.read_bytes()
    (first / "same.csv").write_bytes(bytes_)
    (second / "renamed.csv").write_bytes(bytes_)
    _, _, one = run(
        tmp_path, path=(first / "same.csv").resolve(), allowed_root=first.resolve(), suffix="a"
    )
    _, _, two = run(
        tmp_path,
        path=(second / "renamed.csv").resolve(),
        allowed_root=second.resolve(),
        suffix="b",
    )
    assert one.admission.file_sha256 == two.admission.file_sha256
    assert one.admission.original_filename != two.admission.original_filename
    (first / "same.csv").write_bytes(bytes_.replace(b",100,102,", b",100,103,"))
    _, _, changed = run(
        tmp_path,
        path=(first / "same.csv").resolve(),
        allowed_root=first.resolve(),
        suffix="changed",
    )
    assert changed.admission.file_sha256 != one.admission.file_sha256


def test_permission_and_time_ambiguity_never_promote_to_admitted(tmp_path: Path) -> None:
    _, _, unknown = run(tmp_path, suffix="unknown", permission=SourcePermissionState.UNKNOWN)
    _, _, restricted = run(
        tmp_path, suffix="restricted", permission=SourcePermissionState.DECLARED_RESTRICTED
    )
    _, _, prohibited = run(
        tmp_path, suffix="prohibited", permission=SourcePermissionState.PROHIBITED
    )
    _, _, retention_unknown = run(
        tmp_path, suffix="retention", retention=RetentionClassification.UNKNOWN
    )
    _, _, ambiguous = run(
        tmp_path,
        suffix="ambiguous",
        timestamps=TimestampSemantics.AMBIGUOUS,
    )
    _, _, unavailable = run(
        tmp_path,
        suffix="unavailable",
        availability=AvailabilitySemantics.UNKNOWN,
    )
    assert unknown.admission.status is CsvAdmissionStatus.QUARANTINED
    assert restricted.admission.status is CsvAdmissionStatus.QUARANTINED
    assert prohibited.admission.status is CsvAdmissionStatus.REJECTED
    assert retention_unknown.admission.status is CsvAdmissionStatus.INCOMPLETE
    assert ambiguous.admission.status is CsvAdmissionStatus.UNSUPPORTED
    assert unavailable.admission.status is CsvAdmissionStatus.QUARANTINED
    assert unavailable.report is None
    assert unavailable.admission.ingestion_time == CLOCK.now()
    assert "availability_time_unknown" in unavailable.admission.findings


@pytest.mark.parametrize(
    "attack",
    [
        "outside",
        "traversal",
        "relative",
        "symlink",
        "symlink-escape",
        "directory",
        "fifo",
        "extension",
    ],
)
def test_controlled_path_boundary_rejects_unsafe_inputs(tmp_path: Path, attack: str) -> None:
    root = tmp_path / "allowed"
    root.mkdir()
    valid = root / "input.csv"
    valid.write_bytes(VALID.read_bytes())
    path = valid.resolve()
    if attack == "outside":
        outside = tmp_path / "outside.csv"
        outside.write_bytes(VALID.read_bytes())
        path = outside.resolve()
    elif attack == "traversal":
        path = Path(str(root.resolve()) + "/../outside.csv")
    elif attack == "relative":
        path = Path("input.csv")
    elif attack == "symlink":
        path = root / "link.csv"
        path.symlink_to(valid)
    elif attack == "symlink-escape":
        outside_dir = tmp_path / "outside-directory"
        outside_dir.mkdir()
        (outside_dir / "input.csv").write_bytes(VALID.read_bytes())
        (root / "escape").symlink_to(outside_dir, target_is_directory=True)
        path = root / "escape" / "input.csv"
    elif attack == "directory":
        path = root / "directory.csv"
        path.mkdir()
    elif attack == "fifo":
        path = root / "pipe.csv"
        os.mkfifo(path)
    elif attack == "extension":
        path = root / "input.CSV"
        path.write_bytes(VALID.read_bytes())
    request, source, instrument, schema, timeframe, repository = context(
        tmp_path,
        path=path,
        allowed_root=root.resolve(),
        suffix=attack,
    )
    with pytest.raises(UnsafeCsvPath):
        onboard_real_csv(
            request,
            source=source,
            instrument=instrument,
            schema=schema,
            timeframe=timeframe,
            clock=CLOCK,
            repository=repository,
        )


def test_controlled_path_rejects_intermediate_symlink_inside_allowed_root(
    tmp_path: Path,
) -> None:
    root = tmp_path / "allowed"
    real = root / "real"
    real.mkdir(parents=True)
    (real / "input.csv").write_bytes(VALID.read_bytes())
    (root / "alias").symlink_to(real, target_is_directory=True)
    request, source, instrument, schema, timeframe, repository = context(
        tmp_path,
        path=root / "alias" / "input.csv",
        allowed_root=root.resolve(),
        suffix="intermediate-symlink",
    )
    with pytest.raises(
        UnsafeCsvPath, match="controlled historical path contains symlink component"
    ):
        onboard_real_csv(
            request,
            source=source,
            instrument=instrument,
            schema=schema,
            timeframe=timeframe,
            clock=CLOCK,
            repository=repository,
        )


def test_oversized_binary_and_control_character_inputs_fail_closed(tmp_path: Path) -> None:
    root = tmp_path / "hostile"
    root.mkdir()
    for suffix, data, match in (
        ("oversized", b"x" * (MAX_CONTROLLED_HISTORICAL_FILE_BYTES + 1), "byte bound"),
        ("utf8", b"\xff", "strict UTF-8"),
        ("nul", (HEADER + ROW_1).encode() + b"\x00", "control character"),
        ("binary", b"PK\x03\x04", "control character"),
    ):
        path = root / f"{suffix}.csv"
        path.write_bytes(data)
        request, source, instrument, schema, timeframe, repository = context(
            tmp_path,
            path=path.resolve(),
            allowed_root=root.resolve(),
            suffix=suffix,
        )
        with pytest.raises(CsvFileFailure, match=match):
            onboard_real_csv(
                request,
                source=source,
                instrument=instrument,
                schema=schema,
                timeframe=timeframe,
                clock=CLOCK,
                repository=repository,
            )


def test_line_column_and_field_resource_bounds_fail_closed(tmp_path: Path) -> None:
    root = tmp_path / "resource-bounds"
    root.mkdir()
    attacks = (
        ("line", HEADER + "x" * (MAX_LINE_BYTES + 1) + "\n", "line length"),
        (
            "columns",
            ",".join(f"column_{index}" for index in range(MAX_COLUMNS + 1)) + "\n",
            "header",
        ),
    )
    for suffix, data, match in attacks:
        path = root / f"{suffix}.csv"
        path.write_text(data, encoding="utf-8")
        request, source, instrument, schema, timeframe, repository = context(
            tmp_path,
            path=path.resolve(),
            allowed_root=root.resolve(),
            suffix=f"resource-{suffix}",
        )
        with pytest.raises(CsvFileFailure, match=match):
            onboard_real_csv(
                request,
                source=source,
                instrument=instrument,
                schema=schema,
                timeframe=timeframe,
                clock=CLOCK,
                repository=repository,
            )

    field_path = root / "field.csv"
    oversized_field = "9" * (MAX_FIELD_LENGTH + 1)
    field_path.write_text(
        HEADER + ROW_1.replace(",100,102,", f",{oversized_field},102,"),
        encoding="utf-8",
    )
    _, _, field_result = run(
        tmp_path,
        path=field_path.resolve(),
        allowed_root=root.resolve(),
        suffix="resource-field",
    )
    assert field_result.admission.status is CsvAdmissionStatus.QUARANTINED
    assert "csv_row_resource_limit_none" in field_result.admission.findings


def test_declared_gap_policy_controls_technical_admission(tmp_path: Path) -> None:
    root = tmp_path / "gaps"
    root.mkdir()
    lines = VALID.read_text(encoding="utf-8").splitlines(keepends=True)
    path = root / "gap.csv"
    path.write_text(lines[0] + lines[1] + lines[3], encoding="utf-8")
    _, _, result = run(
        tmp_path,
        path=path.resolve(),
        allowed_root=root.resolve(),
        suffix="gaps",
        missing=MissingDataPolicy.REJECT_GAPS,
    )
    assert result.admission.status is CsvAdmissionStatus.QUARANTINED
    assert result.report is None
    assert "missing_intervals_rejected_by_policy" in result.admission.findings


def test_declared_price_volume_and_timeframe_semantics_fail_closed(tmp_path: Path) -> None:
    root = tmp_path / "semantic-attacks"
    root.mkdir()

    negative_path = root / "negative.csv"
    negative_path.write_text(HEADER + ROW_1.replace(",100,102,", ",-1,102,"), encoding="utf-8")
    _, _, negative = run(
        tmp_path,
        path=negative_path.resolve(),
        allowed_root=root.resolve(),
        suffix="negative",
    )
    assert negative.admission.status is CsvAdmissionStatus.QUARANTINED
    assert "nonpositive_price_outside_declared_domain" in negative.admission.findings

    interval_path = root / "interval.csv"
    interval_path.write_text(
        HEADER + ROW_1.replace("2025-02-01T01:00:00.000000Z", "2025-02-01T02:00:00.000000Z", 1),
        encoding="utf-8",
    )
    _, _, interval = run(
        tmp_path,
        path=interval_path.resolve(),
        allowed_root=root.resolve(),
        suffix="interval",
    )
    assert interval.admission.status is CsvAdmissionStatus.QUARANTINED
    assert any(finding.startswith("csv_row_interval_") for finding in interval.admission.findings)

    request, source, instrument, schema, timeframe, repository = context(
        tmp_path, suffix="volume-mismatch"
    )
    mismatch = replace(
        request,
        declaration=replace(request.declaration, volume_semantics=VolumeSemantic.QUOTE),
    )
    with pytest.raises(RealCsvOnboardingError, match="volume semantics"):
        onboard_real_csv(
            mismatch,
            source=source,
            instrument=instrument,
            schema=schema,
            timeframe=timeframe,
            clock=CLOCK,
            repository=repository,
        )


def test_conflicting_duplicate_timestamp_is_quarantined(tmp_path: Path) -> None:
    root = tmp_path / "conflicting-duplicate"
    root.mkdir()
    path = root / "input.csv"
    conflict = ROW_1.replace(",100,102,99,101,", ",100,103,99,102,")
    path.write_text(HEADER + ROW_1 + conflict, encoding="utf-8")
    _, _, result = run(
        tmp_path,
        path=path.resolve(),
        allowed_root=root.resolve(),
        suffix="conflicting-duplicate",
    )
    assert result.admission.status is CsvAdmissionStatus.QUARANTINED
    assert "event_time_not_strictly_increasing" in result.admission.findings


@pytest.mark.parametrize(
    "name,data,expected",
    [
        ("duplicate-header", HEADER.replace("high", "open", 1) + ROW_1, CsvFileFailure),
        (
            "missing-header",
            HEADER.replace(",volume", "") + ROW_1.replace(",10,final", ",final"),
            CsvFileFailure,
        ),
        ("extra-header", HEADER.rstrip() + ",unknown\n" + ROW_1.rstrip() + ",x\n", CsvFileFailure),
        ("broken-quote", HEADER + '"unterminated\n', CsvFileFailure),
        ("bad-decimal", HEADER + ROW_1.replace(",100,", ",NaN,"), object),
        ("infinity", HEADER + ROW_1.replace(",100,", ",Infinity,"), object),
        ("bad-time", HEADER + ROW_1.replace("2025-02-01T00", "not-a-time"), object),
        ("bad-ohlc", HEADER + ROW_1.replace(",100,102,99,101,", ",100,98,99,101,"), Exception),
        ("duplicate-time", HEADER + ROW_1 + ROW_1, object),
        ("out-of-order", HEADER + ROW_2 + ROW_1, object),
    ],
)
def test_csv_corruption_never_reaches_admitted(
    tmp_path: Path, name: str, data: str, expected: type[object]
) -> None:
    root = tmp_path / name
    root.mkdir()
    path = root / "input.csv"
    path.write_text(data, encoding="utf-8")
    request, source, instrument, schema, timeframe, repository = context(
        tmp_path,
        path=path.resolve(),
        allowed_root=root.resolve(),
        suffix=name,
    )
    try:
        result = onboard_real_csv(
            request,
            source=source,
            instrument=instrument,
            schema=schema,
            timeframe=timeframe,
            clock=CLOCK,
            repository=repository,
        )
    except (CsvFileFailure, CsvImportAssemblyFailure):
        assert expected in {CsvFileFailure, Exception}
    else:
        assert result.admission.status is not CsvAdmissionStatus.ADMITTED


def test_wrong_declared_identity_and_changed_file_linkage_fail_closed(tmp_path: Path) -> None:
    request, source, instrument, schema, timeframe, repository = context(tmp_path)
    declaration = request.declaration

    def wrong_ref(reference: TraceabilityRef) -> TraceabilityRef:
        return TraceabilityRef(reference.object_id, reference.version, "sha256:" + "b" * 64)

    wrong_declarations = (
        replace(declaration, source_ref=wrong_ref(declaration.source_ref)),
        replace(declaration, instrument_ref=wrong_ref(declaration.instrument_ref)),
        replace(declaration, timeframe_ref=wrong_ref(declaration.timeframe_ref)),
        replace(declaration, schema_ref=wrong_ref(declaration.schema_ref)),
    )
    for wrong_declaration in wrong_declarations:
        with pytest.raises(RealCsvOnboardingError, match="exact governed identities"):
            onboard_real_csv(
                replace(request, declaration=wrong_declaration),
                source=source,
                instrument=instrument,
                schema=schema,
                timeframe=timeframe,
                clock=CLOCK,
                repository=repository,
            )
    vendor_source = replace(source, source_type=SourceType.DATA_VENDOR)
    vendor_request = replace(
        request,
        declaration=replace(
            declaration,
            source_ref=exact(vendor_source, vendor_source.source_id),
        ),
    )
    with pytest.raises(RealCsvOnboardingError, match="file-snapshot source identity"):
        onboard_real_csv(
            vendor_request,
            source=vendor_source,
            instrument=instrument,
            schema=schema,
            timeframe=timeframe,
            clock=CLOCK,
            repository=repository,
        )
    result = onboard_real_csv(
        request,
        source=source,
        instrument=instrument,
        schema=schema,
        timeframe=timeframe,
        clock=CLOCK,
        repository=repository,
    )
    assert result.report is not None
    tampered = replace(result.admission, file_sha256="sha256:" + "c" * 64)
    with pytest.raises(RealCsvOnboardingError, match="exact evaluated file"):
        verify_real_csv_lineage(
            admission=tampered,
            declaration=request.declaration,
            report=result.report,
        )
    wrong_configuration = replace(
        result.admission,
        ingestion_configuration_fingerprint="sha256:" + "f" * 64,
    )
    with pytest.raises(RealCsvOnboardingError, match="exact ingestion configuration"):
        verify_real_csv_lineage(
            admission=wrong_configuration,
            declaration=request.declaration,
            report=result.report,
        )
    assert result.admission.raw_manifest_ref is not None
    wrong_dataset = replace(
        result.admission,
        raw_manifest_ref=TraceabilityRef(
            result.admission.raw_manifest_ref.object_id,
            V1,
            "sha256:" + "d" * 64,
        ),
    )
    with pytest.raises(RealCsvOnboardingError, match="exact dataset artifacts"):
        verify_real_csv_lineage(
            admission=wrong_dataset,
            declaration=request.declaration,
            report=result.report,
        )
    assert result.admission.raw_lock_ref is not None
    wrong_lock = replace(
        result.admission,
        raw_lock_ref=TraceabilityRef(
            result.admission.raw_lock_ref.object_id,
            V1,
            "sha256:" + "e" * 64,
        ),
    )
    with pytest.raises(RealCsvOnboardingError, match="exact dataset artifacts"):
        verify_real_csv_lineage(
            admission=wrong_lock,
            declaration=request.declaration,
            report=result.report,
        )


def test_sprint_8_golden_evidence(tmp_path: Path) -> None:
    golden = json.loads(
        (Path(__file__).parent / "golden" / "real_csv_onboarding_v1.json").read_text(
            encoding="utf-8"
        )
    )
    assert golden["file_sha256"] == hashlib.sha256(VALID.read_bytes()).hexdigest()
    request, _, result = run(tmp_path)
    assert result.report is not None
    report = result.report
    assert golden == {
        "admission_fingerprint": fingerprint_record(result.admission),
        "admission_status": result.admission.status.value,
        "file_sha256": result.admission.file_sha256.removeprefix("sha256:"),
        "file_size": result.admission.file_size,
        "fixture": "tests/fixtures/real_csv/repository_owned_external_style_1h.csv",
        "ingestion_configuration_fingerprint": (
            result.admission.ingestion_configuration_fingerprint
        ),
        "instrument_identity": str(report.ingestion.manifest.instrument_refs[0].object_id),
        "normalized_lock_fingerprint": fingerprint_record(report.normalized_lock),
        "normalized_manifest_fingerprint": fingerprint_record(report.normalized_manifest),
        "raw_dataset_fingerprint": fingerprint_record(report.ingestion.manifest),
        "raw_dataset_lock_fingerprint": fingerprint_record(report.ingestion.dataset_lock),
        "raw_dataset_manifest_fingerprint": fingerprint_record(report.ingestion.manifest),
        "row_count": result.admission.row_count,
        "source_declaration_fingerprint": fingerprint_record(request.declaration),
        "source_identity": str(report.ingestion.manifest.source_refs[0].object_id),
        "timeframe_identity": str(report.normalized_manifest.timeframe_refs[0].object_id),
    }
