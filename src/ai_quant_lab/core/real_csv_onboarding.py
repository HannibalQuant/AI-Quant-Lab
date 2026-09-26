"""Controlled, local-only real historical CSV technical admission boundary."""

from __future__ import annotations

import re
from dataclasses import dataclass, field, replace
from decimal import Decimal

from ai_quant_lab.core.codec import REPRESENTATION_VERSION, GovernedRecord
from ai_quant_lab.core.csv_import import (
    CsvImportKernel,
    CsvImportReport,
    CsvImportRequest,
    CsvImportStatus,
    CsvInputScope,
    LocalCsvInputAdapter,
)
from ai_quant_lab.core.data import InstrumentIdentity, SourceIdentity, SourceType
from ai_quant_lab.core.dataset_store import (
    DatasetLineageVerification,
    LocalDatasetRepository,
    RepositoryWriteResult,
    verify_dataset_lineage,
)
from ai_quant_lab.core.ingestion import Clock, IngestionSourceBoundary
from ai_quant_lab.core.integrity import fingerprint_record
from ai_quant_lab.core.market_data import MarketDataSchema, TimeframeIdentity
from ai_quant_lab.core.model import (
    ArtifactId,
    GovernedId,
    ObjectVersion,
    TraceabilityRef,
    fingerprint,
)
from ai_quant_lab.core.real_csv_contracts import (
    AvailabilitySemantics,
    CsvAdmissionStatus,
    CsvTrustState,
    MissingDataPolicy,
    PriceDomain,
    RealCsvAdmissionRecord,
    RealCsvSourceDeclaration,
    ResearchEligibilityState,
    RetentionClassification,
    SourcePermissionState,
    TimestampSemantics,
)


class RealCsvOnboardingError(ValueError):
    """Exact contract mismatch; no partial admission is returned."""


@dataclass(frozen=True, slots=True)
class RealCsvOnboardingRequest:
    admission_id: ArtifactId
    declaration: RealCsvSourceDeclaration
    csv_request: CsvImportRequest
    contract_version: ObjectVersion = field(default_factory=lambda: ObjectVersion(1))

    def __post_init__(self) -> None:
        if self.contract_version != ObjectVersion(1):
            raise RealCsvOnboardingError("unsupported real CSV onboarding contract version")


@dataclass(frozen=True, slots=True)
class RealCsvOnboardingResult:
    admission: RealCsvAdmissionRecord
    report: CsvImportReport | None
    writes: tuple[RepositoryWriteResult, ...]


@dataclass(frozen=True, slots=True)
class RealCsvLineageVerification:
    file_sha256: str
    admission_fingerprint: str
    declaration_fingerprint: str
    dataset_lineage: DatasetLineageVerification


def _exact(
    record: GovernedRecord, object_id: GovernedId, version: ObjectVersion
) -> TraceabilityRef:
    return TraceabilityRef(object_id, version, fingerprint_record(record))


def _expected_mapping(schema: MarketDataSchema) -> tuple[tuple[str, str], ...]:
    values = {
        "availability_time": "availability_time",
        "bar_close": schema.close_time_field,
        "bar_open": schema.open_time_field,
        "close": schema.close_field,
        "finality": schema.finality_field,
        "high": schema.high_field,
        "low": schema.low_field,
        "open": schema.open_field,
    }
    if schema.volume_field is not None:
        values["volume"] = schema.volume_field
    return tuple(sorted(values.items()))


def _ingestion_configuration_fingerprint(request: CsvImportRequest) -> str:
    """Fingerprint semantic configuration without treating a physical path as authority."""
    ingestion = request.ingestion
    return fingerprint(
        {
            "request_id": ingestion.request_id,
            "request_version": ingestion.version,
            "adapter_ref": ingestion.adapter_ref,
            "source_ref": ingestion.source_ref,
            "instrument_ref": ingestion.instrument_ref,
            "observation_provenance_ref": ingestion.observation_provenance_ref,
            "manifest_provenance_ref": ingestion.manifest_provenance_ref,
            "lock_provenance_ref": ingestion.lock_provenance_ref,
            "raw_dataset_id": ingestion.dataset_id,
            "raw_dataset_version": ingestion.dataset_version,
            "raw_lock_id": ingestion.lock_id,
            "raw_lock_version": ingestion.lock_version,
            "dataset_cutoff": ingestion.dataset_cutoff,
            "actor_id": ingestion.actor_id,
            "source_boundary": ingestion.source_boundary,
            "schema_ref": request.schema_ref,
            "timeframe_ref": request.timeframe_ref,
            "normalized_dataset_id": request.normalized_dataset_id,
            "normalized_dataset_version": request.normalized_dataset_version,
            "normalized_lock_id": request.normalized_lock_id,
            "normalized_lock_version": request.normalized_lock_version,
            "normalization_version": request.normalization_version,
            "normalization_provenance_ref": request.normalization_provenance_ref,
            "normalized_provenance_ref": request.normalized_provenance_ref,
            "contract_version": request.contract_version,
        }
    )


def _validate_bindings(
    request: RealCsvOnboardingRequest,
    source: SourceIdentity,
    instrument: InstrumentIdentity,
    schema: MarketDataSchema,
    timeframe: TimeframeIdentity,
) -> TraceabilityRef:
    declaration = request.declaration
    expected = (
        _exact(source, source.source_id, source.version),
        _exact(instrument, instrument.instrument_id, instrument.version),
        _exact(timeframe, timeframe.timeframe_id, timeframe.version),
        _exact(schema, schema.schema_id, schema.version),
    )
    actual = (
        declaration.source_ref,
        declaration.instrument_ref,
        declaration.timeframe_ref,
        declaration.schema_ref,
    )
    if actual != expected:
        raise RealCsvOnboardingError("source declaration does not bind exact governed identities")
    if source.source_type is not SourceType.FILE_SNAPSHOT:
        raise RealCsvOnboardingError("real CSV onboarding requires file-snapshot source identity")
    if declaration.provider_name != source.provider:
        raise RealCsvOnboardingError("declared provider does not match source identity")
    if declaration.operator_id != request.csv_request.ingestion.actor_id:
        raise RealCsvOnboardingError("declared operator does not match ingestion actor")
    if (
        request.csv_request.ingestion.source_boundary
        is not IngestionSourceBoundary.CONTROLLED_FILE_SNAPSHOT
    ):
        raise RealCsvOnboardingError("real CSV requires controlled file-snapshot boundary")
    if declaration.column_mapping != _expected_mapping(schema):
        raise RealCsvOnboardingError("declared column mapping does not match parser schema")
    if declaration.volume_semantics is not schema.volume_semantic:
        raise RealCsvOnboardingError("declared volume semantics do not match parser schema")
    declaration_ref = _exact(declaration, declaration.provenance_id, declaration.version)
    provenance_refs = (
        request.csv_request.ingestion.observation_provenance_ref,
        request.csv_request.ingestion.manifest_provenance_ref,
        request.csv_request.ingestion.lock_provenance_ref,
        request.csv_request.normalization_provenance_ref,
        request.csv_request.normalized_provenance_ref,
    )
    if any(reference != declaration_ref for reference in provenance_refs):
        raise RealCsvOnboardingError("CSV pipeline does not bind exact source declaration")
    return declaration_ref


_TRADINGVIEW_LINEAGE_RE = re.compile(
    r"^tv_adapter_v1;source_sha256=([0-9a-f]{64});canonical_sha256=([0-9a-f]{64})$"
)


def _derived_tradingview_lineage(
    declaration: RealCsvSourceDeclaration,
    evaluated_file_sha256: str,
) -> None:
    derived_timestamp = (
        declaration.timestamp_semantics
        is TimestampSemantics.BAR_OPEN_UTC_CLOSE_DERIVED_FROM_TIMEFRAME
    )
    derived_availability = (
        declaration.availability_semantics is AvailabilitySemantics.DERIVED_BAR_CLOSE_UTC
    )
    if not (derived_timestamp or derived_availability):
        return
    if not (derived_timestamp and derived_availability):
        raise RealCsvOnboardingError("derived timestamp and availability semantics must be paired")
    match = _TRADINGVIEW_LINEAGE_RE.fullmatch(declaration.provenance_note)
    if match is None:
        raise RealCsvOnboardingError("derived TradingView semantics require exact adapter lineage")
    if match.group(2) != evaluated_file_sha256:
        raise RealCsvOnboardingError(
            "derived TradingView canonical hash does not match the evaluated file"
        )


def _policy_outcome(declaration: RealCsvSourceDeclaration) -> tuple[CsvAdmissionStatus, str] | None:
    if declaration.permission_state is SourcePermissionState.PROHIBITED:
        return CsvAdmissionStatus.REJECTED, "permission_prohibited"
    if declaration.permission_state is not SourcePermissionState.DECLARED_PERMITTED:
        return CsvAdmissionStatus.QUARANTINED, "permission_not_declared_permitted"
    if declaration.retention_classification is RetentionClassification.UNKNOWN:
        return CsvAdmissionStatus.INCOMPLETE, "retention_unknown"

    explicit_pair = (
        declaration.timestamp_semantics is TimestampSemantics.BAR_OPEN_AND_CLOSE_UTC
        and declaration.availability_semantics
        is AvailabilitySemantics.EXPLICIT_SOURCE_AVAILABILITY_UTC
    )
    derived_pair = (
        declaration.timestamp_semantics
        is TimestampSemantics.BAR_OPEN_UTC_CLOSE_DERIVED_FROM_TIMEFRAME
        and declaration.availability_semantics is AvailabilitySemantics.DERIVED_BAR_CLOSE_UTC
    )
    if explicit_pair or derived_pair:
        return None
    if declaration.timestamp_semantics is TimestampSemantics.AMBIGUOUS:
        return CsvAdmissionStatus.UNSUPPORTED, "timestamp_semantics_ambiguous"
    if declaration.availability_semantics is AvailabilitySemantics.UNKNOWN:
        return CsvAdmissionStatus.QUARANTINED, "availability_time_unknown"
    return CsvAdmissionStatus.QUARANTINED, "timestamp_availability_semantics_mismatch"


def _admission(
    request: RealCsvOnboardingRequest,
    declaration_ref: TraceabilityRef,
    adapter: LocalCsvInputAdapter,
    *,
    file_sha256: str,
    file_size: int,
    row_count: int,
    status: CsvAdmissionStatus,
    findings: tuple[str, ...],
    report: CsvImportReport | None,
) -> RealCsvAdmissionRecord:
    path = adapter.request.fixture_path.resolve(strict=True)
    root = adapter.request.allowed_root.resolve(strict=True)
    relative = path.relative_to(root).as_posix()
    refs: tuple[TraceabilityRef | None, ...]
    if report is None:
        refs = (None, None, None, None)
    else:
        refs = (
            _exact(
                report.ingestion.manifest,
                report.ingestion.manifest.dataset_id,
                report.ingestion.manifest.version,
            ),
            _exact(
                report.ingestion.dataset_lock,
                report.ingestion.dataset_lock.lock_id,
                report.ingestion.dataset_lock.version,
            ),
            _exact(
                report.normalized_manifest,
                report.normalized_manifest.dataset_id,
                report.normalized_manifest.version,
            ),
            _exact(
                report.normalized_lock,
                report.normalized_lock.lock_id,
                report.normalized_lock.version,
            ),
        )
    return RealCsvAdmissionRecord(
        request.admission_id,
        ObjectVersion(1),
        declaration_ref,
        path.name,
        relative,
        "sha256:" + file_sha256,
        file_size,
        adapter.clock.now(),
        adapter.request.contract_version,
        ObjectVersion(REPRESENTATION_VERSION),
        _ingestion_configuration_fingerprint(adapter.request),
        row_count,
        status,
        tuple(sorted(findings)),
        refs[0],
        refs[1],
        refs[2],
        refs[3],
        CsvTrustState.NOT_TRUSTED,
        ResearchEligibilityState.NOT_RESEARCH_ELIGIBLE,
        ObjectVersion(1),
    )


def onboard_real_csv(
    request: RealCsvOnboardingRequest,
    *,
    source: SourceIdentity,
    instrument: InstrumentIdentity,
    schema: MarketDataSchema,
    timeframe: TimeframeIdentity,
    clock: Clock,
    repository: LocalDatasetRepository,
) -> RealCsvOnboardingResult:
    """Technically admit one explicit local file; never confer trust or research authority."""
    declaration_ref = _validate_bindings(request, source, instrument, schema, timeframe)
    controlled_adapter = LocalCsvInputAdapter(
        request.csv_request.ingestion.adapter_ref,
        request.csv_request,
        schema,
        timeframe,
        clock,
        CsvInputScope.CONTROLLED_HISTORICAL,
    )
    prepared = controlled_adapter.prepare()
    _derived_tradingview_lineage(request.declaration, prepared.file_sha256)
    pinned_request = replace(request.csv_request, expected_file_sha256=prepared.file_sha256)
    controlled_adapter = replace(controlled_adapter, request=pinned_request, prepared=prepared)

    policy = _policy_outcome(request.declaration)
    if policy is not None:
        status, finding = policy
        admission = _admission(
            request,
            declaration_ref,
            controlled_adapter,
            file_sha256=prepared.file_sha256,
            file_size=prepared.file_size,
            row_count=prepared.row_count,
            status=status,
            findings=(finding,),
            report=None,
        )
        return RealCsvOnboardingResult(
            admission,
            None,
            (repository.store(request.declaration), repository.store(admission)),
        )

    event_times = tuple(candidate.event_time for candidate in prepared.candidates)
    quality_findings: list[str] = []
    if event_times != tuple(sorted(event_times)) or len(event_times) != len(set(event_times)):
        quality_findings.append("event_time_not_strictly_increasing")
    if prepared.rejected:
        quality_findings.append("csv_rows_rejected")
        quality_findings.extend(
            f"csv_row_{rejection.reason.value}_{rejection.column or 'none'}"
            for rejection in prepared.rejected
        )
    if request.declaration.price_domain is PriceDomain.POSITIVE_ONLY:
        price_fields = {
            schema.open_field,
            schema.high_field,
            schema.low_field,
            schema.close_field,
        }
        if any(
            Decimal(str(field.value)) <= 0
            for candidate in prepared.candidates
            for field in candidate.fields
            if field.name in price_fields
        ):
            quality_findings.append("nonpositive_price_outside_declared_domain")
    if quality_findings:
        admission = _admission(
            request,
            declaration_ref,
            controlled_adapter,
            file_sha256=prepared.file_sha256,
            file_size=prepared.file_size,
            row_count=prepared.row_count,
            status=CsvAdmissionStatus.QUARANTINED,
            findings=tuple(quality_findings),
            report=None,
        )
        return RealCsvOnboardingResult(
            admission,
            None,
            (repository.store(request.declaration), repository.store(admission)),
        )

    report = CsvImportKernel().import_fixture(
        pinned_request,
        controlled_adapter,
        source,
        instrument,
        schema,
        timeframe,
        clock,
    )
    if report.status is not CsvImportStatus.SUCCESS or report.incomplete_bars:
        quality_findings.append("pipeline_not_fully_accepted")
    if report.gap_findings:
        quality_findings.append("missing_intervals_recorded")
        if request.declaration.missing_data_policy is MissingDataPolicy.REJECT_GAPS:
            quality_findings.append("missing_intervals_rejected_by_policy")
    admitted = not quality_findings or quality_findings == ["missing_intervals_recorded"]
    admission = _admission(
        request,
        declaration_ref,
        controlled_adapter,
        file_sha256=prepared.file_sha256,
        file_size=prepared.file_size,
        row_count=prepared.row_count,
        status=CsvAdmissionStatus.ADMITTED if admitted else CsvAdmissionStatus.QUARANTINED,
        findings=tuple(quality_findings),
        report=report if admitted else None,
    )
    writes: list[RepositoryWriteResult] = [repository.store(request.declaration)]
    if admitted:
        writes.extend(
            repository.store(observation) for observation in report.ingestion.accepted_observations
        )
        writes.extend(
            (
                repository.store(report.ingestion.manifest),
                repository.store(report.ingestion.dataset_lock),
            )
        )
        writes.extend(repository.store(bar) for bar in report.normalized_bars)
        writes.extend(
            (
                repository.store(report.normalized_manifest),
                repository.store(report.normalized_lock),
            )
        )
    writes.append(repository.store(admission))
    return RealCsvOnboardingResult(admission, report if admitted else None, tuple(writes))


def verify_real_csv_lineage(
    *,
    admission: RealCsvAdmissionRecord,
    declaration: RealCsvSourceDeclaration,
    report: CsvImportReport,
) -> RealCsvLineageVerification:
    """Verify file/declaration/dataset linkage; this does not grant source authenticity."""
    if admission.status is not CsvAdmissionStatus.ADMITTED:
        raise RealCsvOnboardingError("only an admitted record can bind dataset lineage")
    declaration_ref = _exact(declaration, declaration.provenance_id, declaration.version)
    if admission.source_declaration_ref != declaration_ref:
        raise RealCsvOnboardingError("admission does not bind the exact source declaration")
    _derived_tradingview_lineage(declaration, report.file_sha256)
    if (
        admission.file_sha256 != "sha256:" + report.file_sha256
        or admission.file_size != report.file_size
        or admission.row_count != report.row_count
    ):
        raise RealCsvOnboardingError("admission does not bind the exact evaluated file")
    if (
        admission.parser_contract_version != report.request.contract_version
        or admission.canonical_codec_version != ObjectVersion(REPRESENTATION_VERSION)
        or admission.ingestion_configuration_fingerprint
        != _ingestion_configuration_fingerprint(report.request)
    ):
        raise RealCsvOnboardingError("admission does not bind the exact ingestion configuration")
    expected_refs = (
        _exact(
            report.ingestion.manifest,
            report.ingestion.manifest.dataset_id,
            report.ingestion.manifest.version,
        ),
        _exact(
            report.ingestion.dataset_lock,
            report.ingestion.dataset_lock.lock_id,
            report.ingestion.dataset_lock.version,
        ),
        _exact(
            report.normalized_manifest,
            report.normalized_manifest.dataset_id,
            report.normalized_manifest.version,
        ),
        _exact(
            report.normalized_lock, report.normalized_lock.lock_id, report.normalized_lock.version
        ),
    )
    if (
        admission.raw_manifest_ref,
        admission.raw_lock_ref,
        admission.normalized_manifest_ref,
        admission.normalized_lock_ref,
    ) != expected_refs:
        raise RealCsvOnboardingError("admission does not bind the exact dataset artifacts")
    if any(
        item.provenance_ref != declaration_ref
        for item in (
            report.ingestion.manifest,
            report.ingestion.dataset_lock,
            report.normalized_manifest,
            report.normalized_lock,
        )
    ):
        raise RealCsvOnboardingError("dataset artifacts do not preserve source declaration")
    lineage = verify_dataset_lineage(
        raw_manifest=report.ingestion.manifest,
        raw_lock=report.ingestion.dataset_lock,
        bars=report.normalized_bars,
        normalized_manifest=report.normalized_manifest,
        normalized_lock=report.normalized_lock,
    )
    return RealCsvLineageVerification(
        admission.file_sha256,
        fingerprint_record(admission),
        fingerprint_record(declaration),
        lineage,
    )
