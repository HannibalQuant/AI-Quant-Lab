"""Bounded local CSV parsing; acquisition, trust and research authority are absent."""

from __future__ import annotations

import csv
import hashlib
import io
from dataclasses import dataclass, field, replace
from datetime import UTC, datetime
from enum import StrEnum
from pathlib import Path
from typing import BinaryIO

from ai_quant_lab.core.data import (
    DatasetLock,
    DatasetLockId,
    DecimalValue,
    InstrumentIdentity,
    ObservationId,
    SourceIdentity,
)
from ai_quant_lab.core.ingestion import (
    CandidateField,
    CandidateObservation,
    CandidateValueKind,
    Clock,
    IngestionKernel,
    IngestionRequest,
    IngestionResult,
    IngestionSession,
)
from ai_quant_lab.core.integrity import fingerprint_record, verify_integrity
from ai_quant_lab.core.market_data import (
    BarFinality,
    BarPairDisposition,
    BarPairFinding,
    GapFinding,
    MarketBar,
    MarketBarId,
    MarketDataError,
    MarketDataSchema,
    MarketDataSchemaId,
    NormalizedBarManifest,
    NormalizedDatasetAssemblyError,
    TimeframeId,
    TimeframeIdentity,
    assemble_normalized_dataset,
    classify_bars,
    classify_fixed_gaps,
    normalize_bar,
)
from ai_quant_lab.core.model import (
    AgentId,
    ArtifactId,
    AuditEvent,
    AuditEventId,
    AuditResult,
    DatasetId,
    ObjectVersion,
    ProvenanceId,
    TraceabilityRef,
    VersionedRef,
    require_utc,
)

MAX_FILE_BYTES = 1_000_000
MAX_ROWS = 2_000
MAX_FIELD_LENGTH = 256
MAX_LINE_BYTES = 4_096
MAX_COLUMNS = 32
TIMESTAMP_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"


class CsvImportError(ValueError):
    """Invalid local fixture import is never silently accepted."""


class UnsafeCsvPath(CsvImportError):
    """Path crossed the explicit allowed fixture boundary."""


class CsvFileFailure(CsvImportError):
    """Critical file/header/contract failure aborts the whole import."""


class CsvImportAssemblyFailure(CsvImportError):
    """Accepted records cannot form a governed finalized dataset."""


class CsvRowReason(StrEnum):
    WIDTH = "width"
    TIMESTAMP = "timestamp"
    DECIMAL = "decimal"
    FINALITY = "finality"
    INTERVAL = "interval"
    EMPTY = "empty"
    RESOURCE_LIMIT = "resource_limit"


class CsvImportStatus(StrEnum):
    SUCCESS = "success"
    SUCCESS_WITH_REJECTIONS = "success_with_rejections"
    FAILED = "failed"


class CsvInputScope(StrEnum):
    REPOSITORY_FIXTURE = "repository_fixture"
    CONTROLLED_HISTORICAL = "controlled_historical"


@dataclass(frozen=True, slots=True)
class CsvRowRejection:
    row_number: int
    reason: CsvRowReason
    column: str | None


@dataclass(frozen=True, slots=True)
class CsvNormalizationRejection:
    """Safe exact raw reference; no rejected payload or unbounded exception string."""

    raw_ref: TraceabilityRef
    reason: str = "invalid_market_bar"


@dataclass(frozen=True, slots=True)
class CsvImportRequest:
    """Exact pinned context; its local path grants no source or import authority."""

    ingestion: IngestionRequest
    session: IngestionSession
    fixture_path: Path
    allowed_root: Path
    schema_ref: TraceabilityRef
    timeframe_ref: TraceabilityRef
    normalized_dataset_id: DatasetId
    normalized_dataset_version: ObjectVersion
    normalized_lock_id: DatasetLockId
    normalized_lock_version: ObjectVersion
    normalization_version: ObjectVersion
    normalization_provenance_ref: TraceabilityRef
    normalized_provenance_ref: TraceabilityRef
    expected_file_sha256: str | None = None
    contract_version: ObjectVersion = field(default_factory=lambda: ObjectVersion(1))

    def __post_init__(self) -> None:
        if self.contract_version != ObjectVersion(1):
            raise CsvFileFailure("unsupported CSV import contract version")
        if not isinstance(self.schema_ref.object_id, MarketDataSchemaId) or not isinstance(
            self.timeframe_ref.object_id, TimeframeId
        ):
            raise CsvFileFailure("exact typed schema and timeframe references required")
        if self.expected_file_sha256 is not None and (
            len(self.expected_file_sha256) != 64
            or any(c not in "0123456789abcdef" for c in self.expected_file_sha256)
        ):
            raise CsvFileFailure("expected file digest must be lowercase SHA-256")
        for ref in (self.normalization_provenance_ref, self.normalized_provenance_ref):
            if not isinstance(ref.object_id, ProvenanceId) or ref.expected_fingerprint is None:
                raise CsvFileFailure("exact provenance references are required")
        if self.normalized_dataset_id == self.ingestion.dataset_id:
            raise CsvFileFailure("raw and normalized dataset identities must be distinct")
        if self.normalized_lock_id == self.ingestion.lock_id:
            raise CsvFileFailure("raw and normalized lock identities must be distinct")


@dataclass(frozen=True, slots=True)
class ParsedCsvFile:
    file_sha256: str
    file_size: int
    row_count: int
    candidates: tuple[CandidateObservation, ...]
    rejected: tuple[CsvRowRejection, ...]


def _stamp(value: datetime) -> str:
    require_utc(value, "CSV timestamp")
    return value.isoformat(timespec="microseconds").replace("+00:00", "Z")


def _csv_time(text: str) -> datetime:
    if not text or text.strip() != text:
        raise ValueError("timestamp whitespace/absence forbidden")
    parsed = datetime.strptime(text, TIMESTAMP_FORMAT).replace(tzinfo=UTC)
    if _stamp(parsed) != text:
        raise ValueError("timestamp must use canonical UTC microsecond Z")
    return parsed


def _reject_controlled_symlink_components(root: Path, path: Path) -> None:
    candidate = root
    if candidate.is_symlink():
        raise UnsafeCsvPath("controlled historical path contains symlink component")
    for component in path.relative_to(root).parts:
        candidate /= component
        if candidate.is_symlink():
            raise UnsafeCsvPath("controlled historical path contains symlink component")


def _safe_file(root: Path, path: Path, scope: CsvInputScope) -> BinaryIO:
    if path.as_posix().startswith(("http:", "https:", "file:")) or ".." in path.parts:
        raise UnsafeCsvPath("URL or traversal path prohibited")
    if path.suffix != ".csv":
        raise UnsafeCsvPath("only lowercase .csv files are supported")
    if scope is CsvInputScope.REPOSITORY_FIXTURE:
        if (
            root.name != "market_data"
            or root.parent.name != "fixtures"
            or root.parent.parent.name != "tests"
        ):
            raise UnsafeCsvPath("allowed root must be the explicit repository fixture tree")
    elif scope is CsvInputScope.CONTROLLED_HISTORICAL:
        if not root.is_absolute() or not path.is_absolute():
            raise UnsafeCsvPath(
                "controlled historical root and file must be explicit absolute paths"
            )
        if root.is_symlink():
            raise UnsafeCsvPath("controlled historical path contains symlink component")
        if not root.is_dir():
            raise UnsafeCsvPath(
                "controlled historical root must be an existing non-symlink directory"
            )
    else:
        raise UnsafeCsvPath("unsupported CSV input scope")
    try:
        if scope is CsvInputScope.CONTROLLED_HISTORICAL:
            _reject_controlled_symlink_components(root, path)
        resolved_root = root.resolve(strict=True)
        resolved_path = path.resolve(strict=True)
        resolved_path.relative_to(resolved_root)
        if path.is_symlink() or not resolved_path.is_file():
            raise UnsafeCsvPath("symlink or nonregular CSV file prohibited")
        return resolved_path.open("rb")
    except UnsafeCsvPath:
        raise
    except (OSError, ValueError) as exc:
        raise UnsafeCsvPath("CSV file is missing or outside allowed root") from exc


@dataclass(frozen=True, slots=True)
class LocalCsvInputAdapter:
    """Reads one explicitly scoped local CSV; never judges source trust or authority."""

    adapter_ref: TraceabilityRef
    request: CsvImportRequest
    schema: MarketDataSchema
    timeframe: TimeframeIdentity
    clock: Clock
    input_scope: CsvInputScope = CsvInputScope.REPOSITORY_FIXTURE
    prepared: ParsedCsvFile | None = None

    def _headers(self) -> set[str]:
        names = {
            self.schema.open_time_field,
            self.schema.close_time_field,
            self.schema.open_field,
            self.schema.high_field,
            self.schema.low_field,
            self.schema.close_field,
            self.schema.finality_field,
            "availability_time",
        }
        if self.schema.volume_field is not None:
            names.add(self.schema.volume_field)
        return names

    def prepare(self) -> ParsedCsvFile:
        if self.adapter_ref != self.request.ingestion.adapter_ref:
            raise CsvFileFailure("adapter request binding mismatch")
        if self.request.schema_ref != TraceabilityRef(
            self.schema.schema_id, self.schema.version, fingerprint_record(self.schema)
        ) or self.request.timeframe_ref != TraceabilityRef(
            self.timeframe.timeframe_id, self.timeframe.version, fingerprint_record(self.timeframe)
        ):
            raise CsvFileFailure("exact schema/timeframe binding mismatch")
        if self.schema.timeframe_ref != self.request.timeframe_ref:
            raise CsvFileFailure("schema binds another timeframe")
        require_utc(self.clock.now(), "CSV deterministic clock")
        if self.prepared is not None:
            return self.prepared
        with _safe_file(
            self.request.allowed_root, self.request.fixture_path, self.input_scope
        ) as stream:
            data = stream.read(MAX_FILE_BYTES + 1)
        if len(data) > MAX_FILE_BYTES:
            raise CsvFileFailure("bounded CSV file byte bound exceeded")
        digest = hashlib.sha256(data).hexdigest()
        if (
            self.request.expected_file_sha256 is not None
            and digest != self.request.expected_file_sha256
        ):
            raise CsvFileFailure("fixture byte fingerprint mismatch")
        try:
            text = data.decode("utf-8", errors="strict")
        except UnicodeError as exc:
            raise CsvFileFailure("fixture must be strict UTF-8") from exc
        if text.startswith("\ufeff"):
            raise CsvFileFailure("UTF-8 BOM is not supported")
        if "\x00" in text or any(
            ord(character) < 32 and character not in {"\r", "\n"} for character in text
        ):
            raise CsvFileFailure("NUL or unsupported control character in CSV")
        if any(len(line.encode("utf-8")) > MAX_LINE_BYTES for line in text.splitlines()):
            raise CsvFileFailure("bounded CSV line length exceeded")
        reader = csv.reader(
            io.StringIO(text, newline=""), delimiter=",", quotechar='"', strict=True
        )
        try:
            headers = next(reader)
            if (
                len(headers) > MAX_COLUMNS
                or len(headers) != len(set(headers))
                or any(not h or h.strip() != h for h in headers)
                or set(headers) != self._headers()
            ):
                raise CsvFileFailure("duplicate, missing, ambiguous or unknown CSV header")
        except (StopIteration, csv.Error) as exc:
            raise CsvFileFailure("missing or malformed CSV header") from exc
        candidates: list[CandidateObservation] = []
        rejected: list[CsvRowRejection] = []
        occurrence: dict[str, int] = {}
        row_count = 0
        try:
            for row in reader:
                row_count += 1
                if row_count > MAX_ROWS:
                    raise CsvFileFailure("bounded CSV row limit exceeded")
                line = reader.line_num
                if len(row) != len(headers):
                    rejected.append(CsvRowRejection(line, CsvRowReason.WIDTH, None))
                    continue
                if any(len(field) > MAX_FIELD_LENGTH for field in row):
                    rejected.append(CsvRowRejection(line, CsvRowReason.RESOURCE_LIMIT, None))
                    continue
                fields = dict(zip(headers, row, strict=True))
                try:
                    candidate = self._candidate(fields, occurrence)
                except _InvalidCsvRow as exc:
                    rejected.append(CsvRowRejection(line, exc.reason, exc.column))
                else:
                    candidates.append(candidate)
        except csv.Error as exc:
            raise CsvFileFailure("malformed CSV quoting invalidates fixture") from exc
        return ParsedCsvFile(digest, len(data), row_count, tuple(candidates), tuple(rejected))

    def _candidate(
        self, fields: dict[str, str], occurrence: dict[str, int]
    ) -> CandidateObservation:
        try:
            opening = _csv_time(fields[self.schema.open_time_field])
            closing = _csv_time(fields[self.schema.close_time_field])
            available = _csv_time(fields["availability_time"])
        except ValueError as exc:
            raise _InvalidCsvRow(CsvRowReason.TIMESTAMP, None) from exc
        try:
            self.timeframe.require_aligned(opening)
            if closing - opening != self.timeframe.duration or available < opening:
                raise ValueError("invalid pinned bar interval")
        except ValueError as exc:
            raise _InvalidCsvRow(CsvRowReason.INTERVAL, self.schema.open_time_field) from exc
        decimal_names = (
            self.schema.open_field,
            self.schema.high_field,
            self.schema.low_field,
            self.schema.close_field,
        )
        for name in decimal_names:
            if not fields[name]:
                raise _InvalidCsvRow(CsvRowReason.EMPTY, name)
            if fields[name].strip() != fields[name]:
                raise _InvalidCsvRow(CsvRowReason.DECIMAL, name)
            try:
                DecimalValue.from_text(fields[name])
            except ValueError as exc:
                raise _InvalidCsvRow(CsvRowReason.DECIMAL, name) from exc
        if self.schema.volume_field is not None:
            if not fields[self.schema.volume_field]:
                raise _InvalidCsvRow(CsvRowReason.EMPTY, self.schema.volume_field)
            if fields[self.schema.volume_field].strip() != fields[self.schema.volume_field]:
                raise _InvalidCsvRow(CsvRowReason.DECIMAL, self.schema.volume_field)
            try:
                DecimalValue.from_text(fields[self.schema.volume_field])
            except ValueError as exc:
                raise _InvalidCsvRow(CsvRowReason.DECIMAL, self.schema.volume_field) from exc
        if fields[self.schema.finality_field] not in {"final", "incomplete"}:
            raise _InvalidCsvRow(CsvRowReason.FINALITY, self.schema.finality_field)
        if fields[self.schema.finality_field] == BarFinality.FINAL.value and available < closing:
            raise _InvalidCsvRow(CsvRowReason.INTERVAL, "availability_time")
        raw_fields = tuple(
            CandidateField(
                name,
                CandidateValueKind.DECIMAL
                if name in decimal_names or name == self.schema.volume_field
                else CandidateValueKind.TEXT,
                value,
            )
            for name, value in sorted(fields.items())
            if name != "availability_time"
        )
        event = opening if self.schema.timestamp_meaning.value == "open" else closing
        content = "\x1f".join(f"{name}={value}" for name, value in sorted(fields.items()))
        stem = hashlib.sha256(content.encode("utf-8")).hexdigest()[:36]
        ordinal = occurrence.get(stem, 0)
        occurrence[stem] = ordinal + 1
        return CandidateObservation(
            ObservationId(f"csv-{stem}-{ordinal}"),
            ObjectVersion(1),
            self.request.ingestion.source_ref,
            self.request.ingestion.instrument_ref,
            _stamp(event),
            _stamp(available),
            _stamp(self.clock.now()),
            raw_fields,
        )

    def read(self) -> tuple[CandidateObservation, ...]:
        return (self.prepared or self.prepare()).candidates


class _InvalidCsvRow(Exception):
    def __init__(self, reason: CsvRowReason, column: str | None) -> None:
        self.reason = reason
        self.column = column


@dataclass(frozen=True, slots=True)
class CsvImportReport:
    request: CsvImportRequest
    file_sha256: str
    file_size: int
    row_count: int
    csv_rejections: tuple[CsvRowRejection, ...]
    ingestion: IngestionResult
    normalization_rejections: tuple[CsvNormalizationRejection, ...]
    normalized_bars: tuple[MarketBar, ...]
    incomplete_bars: tuple[MarketBar, ...]
    bar_findings: tuple[BarPairFinding, ...]
    gap_findings: tuple[GapFinding, ...]
    normalized_manifest: NormalizedBarManifest
    normalized_lock: DatasetLock
    audit_events: tuple[AuditEvent, ...]
    status: CsvImportStatus

    @property
    def semantic_snapshot(self) -> tuple[str, ...]:
        """Dataset equivalence deliberately excludes file bytes and session identity."""
        return (
            fingerprint_record(self.ingestion.manifest),
            fingerprint_record(self.ingestion.dataset_lock),
            fingerprint_record(self.normalized_manifest),
            fingerprint_record(self.normalized_lock),
        )


class CsvImportKernel:
    """Orchestrates existing ingestion and normalization; neither adapter nor report approves."""

    def import_fixture(
        self,
        request: CsvImportRequest,
        adapter: LocalCsvInputAdapter,
        source: SourceIdentity,
        instrument: InstrumentIdentity,
        schema: MarketDataSchema,
        timeframe: TimeframeIdentity,
        clock: Clock,
    ) -> CsvImportReport:
        if adapter.request != request or adapter.schema != schema or adapter.timeframe != timeframe:
            raise CsvFileFailure("adapter/schema/import context mismatch")
        if adapter.clock.now() != clock.now():
            raise CsvFileFailure("clock context mismatch")
        prepared = adapter.prepare()
        ingestion = IngestionKernel().ingest(
            request.ingestion,
            request.session,
            replace(adapter, prepared=prepared),
            source,
            instrument,
            clock,
        )
        normalized: list[MarketBar] = []
        incomplete: list[MarketBar] = []
        normalization_rejections: list[CsvNormalizationRejection] = []
        try:
            for raw in ingestion.accepted_observations:
                # Stable semantic identity from raw content; never from physical row number.
                bar_id = MarketBarId("bar-" + raw.observation_id.value)
                try:
                    result = normalize_bar(
                        raw,
                        schema,
                        timeframe,
                        bar_id,
                        ObjectVersion(1),
                        request.normalization_version,
                        request.normalization_provenance_ref,
                    )
                except MarketDataError:
                    normalization_rejections.append(
                        CsvNormalizationRejection(
                            TraceabilityRef(
                                raw.observation_id, raw.version, fingerprint_record(raw)
                            )
                        )
                    )
                    continue
                (incomplete if result.bar.finality.value == "incomplete" else normalized).append(
                    result.bar
                )
            findings = classify_bars(tuple(normalized))
            if any(f.disposition is BarPairDisposition.CONFLICT for f in findings):
                raise CsvImportAssemblyFailure("unresolved conflicting bars prohibit dataset")
            if any(f.disposition is BarPairDisposition.DUPLICATE for f in findings):
                raise CsvImportAssemblyFailure("duplicate bars prohibit finalized dataset")
            gaps = classify_fixed_gaps(tuple(normalized), timeframe)
            raw_lock_ref = TraceabilityRef(
                ingestion.dataset_lock.lock_id,
                ingestion.dataset_lock.version,
                fingerprint_record(ingestion.dataset_lock),
            )
            manifest, lock = assemble_normalized_dataset(
                tuple(normalized),
                request.normalized_dataset_id,
                request.normalized_dataset_version,
                clock.now(),
                request.schema_ref,
                request.normalization_version,
                raw_lock_ref,
                request.normalized_provenance_ref,
                request.normalized_lock_id,
                request.normalized_lock_version,
                request.ingestion.dataset_cutoff,
            )
            verify_integrity(manifest, fingerprint_record(manifest))
            verify_integrity(lock, fingerprint_record(lock))
        except (NormalizedDatasetAssemblyError, ValueError) as exc:
            raise CsvImportAssemblyFailure("normalized assembly failed closed") from exc
        rejected_count = len(prepared.rejected) + ingestion.rejected_count
        audit_events = _csv_audits(
            prepared,
            ingestion,
            tuple(normalized),
            tuple(normalization_rejections),
            manifest,
            request.ingestion.actor_id,
            clock,
        )
        return CsvImportReport(
            request,
            prepared.file_sha256,
            prepared.file_size,
            prepared.row_count,
            prepared.rejected,
            ingestion,
            tuple(normalization_rejections),
            tuple(normalized),
            tuple(incomplete),
            findings,
            gaps,
            manifest,
            lock,
            audit_events,
            CsvImportStatus.SUCCESS_WITH_REJECTIONS
            if rejected_count
            or incomplete
            or ingestion.quarantined_observations
            or normalization_rejections
            else CsvImportStatus.SUCCESS,
        )


def _csv_audits(
    parsed: ParsedCsvFile,
    ingestion: IngestionResult,
    bars: tuple[MarketBar, ...],
    failures: tuple[CsvNormalizationRejection, ...],
    manifest: NormalizedBarManifest,
    actor: AgentId,
    clock: Clock,
) -> tuple[AuditEvent, ...]:
    """Append-oriented attributable metadata only; audit cannot authorize anything."""
    events: list[AuditEvent] = []
    stem = parsed.file_sha256[:25]

    def add(action: str, target: VersionedRef, result: AuditResult) -> None:
        events.append(
            AuditEvent(
                AuditEventId(f"csv-{stem}-{len(events):04d}"),
                actor,
                action,
                target,
                clock.now(),
                result,
                (("file_sha256", parsed.file_sha256),),
            )
        )

    file_ref = VersionedRef(ArtifactId(f"fixture-file-{stem}"), ObjectVersion(1))
    add("csv.import_started", file_ref, AuditResult.RECORDED)
    add("csv.file_validated", file_ref, AuditResult.ACCEPTED)
    for row_rejection in parsed.rejected:
        add(
            "csv.row_rejected",
            VersionedRef(
                ArtifactId(f"fixture-row-{stem}-{row_rejection.row_number}"), ObjectVersion(1)
            ),
            AuditResult.REJECTED,
        )
    for observation in ingestion.accepted_observations:
        add(
            "csv.row_accepted",
            VersionedRef(observation.observation_id, observation.version),
            AuditResult.ACCEPTED,
        )
    for failure in failures:
        add(
            "csv.bar_normalization_rejected",
            VersionedRef(failure.raw_ref.object_id, failure.raw_ref.version),
            AuditResult.REJECTED,
        )
    for bar in bars:
        add("csv.bar_normalized", VersionedRef(bar.bar_id, bar.version), AuditResult.RECORDED)
    add(
        "csv.normalized_dataset_created",
        VersionedRef(manifest.dataset_id, manifest.version),
        AuditResult.RECORDED,
    )
    add("csv.import_completed", file_ref, AuditResult.ACCEPTED)
    return tuple(events)
