"""Governed contracts for bounded real historical CSV admission."""

from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum

from ai_quant_lab.core.model import (
    AgentId,
    ArtifactId,
    ObjectVersion,
    ProvenanceId,
    TraceabilityRef,
    require_utc,
)


class RealCsvContractError(ValueError):
    pass


class AcquisitionMethod(StrEnum):
    OPERATOR_LOCAL_FILE = "operator_local_file"


class SourcePermissionState(StrEnum):
    DECLARED_PERMITTED = "declared_permitted"
    DECLARED_RESTRICTED = "declared_restricted"
    UNKNOWN = "unknown"
    PROHIBITED = "prohibited"


class RetentionClassification(StrEnum):
    DECLARED_LOCAL_ONLY = "declared_local_only"
    DECLARED_RESTRICTED = "declared_restricted"
    UNKNOWN = "unknown"


class TimestampSemantics(StrEnum):
    BAR_OPEN_AND_CLOSE_UTC = "bar_open_and_close_utc"
    AMBIGUOUS = "ambiguous"


class AvailabilitySemantics(StrEnum):
    EXPLICIT_SOURCE_AVAILABILITY_UTC = "explicit_source_availability_utc"
    UNKNOWN = "unknown"


class MissingDataPolicy(StrEnum):
    RECORD_GAPS = "record_gaps"
    REJECT_GAPS = "reject_gaps"


class DuplicatePolicy(StrEnum):
    REJECT_ALL = "reject_all"


class OrderingPolicy(StrEnum):
    STRICT_ASCENDING_EVENT_TIME = "strict_ascending_event_time"


class CsvAdmissionStatus(StrEnum):
    ADMITTED = "ADMITTED"
    REJECTED = "REJECTED"
    QUARANTINED = "QUARANTINED"
    INCOMPLETE = "INCOMPLETE"
    UNSUPPORTED = "UNSUPPORTED"


class CsvTrustState(StrEnum):
    NOT_TRUSTED = "NOT_TRUSTED"


class ResearchEligibilityState(StrEnum):
    NOT_RESEARCH_ELIGIBLE = "NOT_RESEARCH_ELIGIBLE"


def _required(value: str, field: str, maximum: int = 512) -> None:
    if not isinstance(value, str) or not value.strip() or len(value) > maximum:
        raise RealCsvContractError(f"{field} must be bounded non-empty text")


def _optional(value: str | None, field: str) -> None:
    if value is not None:
        _required(value, field)


def _exact(reference: TraceabilityRef, field: str) -> None:
    if not isinstance(reference, TraceabilityRef) or reference.expected_fingerprint is None:
        raise RealCsvContractError(f"{field} must be an exact fingerprint-bearing reference")


@dataclass(frozen=True, slots=True)
class RealCsvSourceDeclaration:
    """Operator declaration; recording it does not prove source truth or permission."""

    provenance_id: ProvenanceId
    version: ObjectVersion
    source_ref: TraceabilityRef
    instrument_ref: TraceabilityRef
    timeframe_ref: TraceabilityRef
    schema_ref: TraceabilityRef
    provider_name: str
    acquisition_method: AcquisitionMethod
    declared_market: str
    timestamp_semantics: TimestampSemantics
    availability_semantics: AvailabilitySemantics
    timezone_rule: str
    column_mapping: tuple[tuple[str, str], ...]
    ohlc_semantics: str
    volume_semantics: str
    finality_assumptions: str
    missing_data_policy: MissingDataPolicy
    duplicate_policy: DuplicatePolicy
    ordering_policy: OrderingPolicy
    permission_state: SourcePermissionState
    license_reference: str | None
    retention_classification: RetentionClassification
    deletion_restriction: str | None
    redistribution_restriction: str | None
    operator_id: AgentId
    provenance_note: str
    contract_version: ObjectVersion

    def __post_init__(self) -> None:
        if self.version != ObjectVersion(1) or self.contract_version != ObjectVersion(1):
            raise RealCsvContractError("unsupported source declaration version")
        for name, reference in (
            ("source_ref", self.source_ref),
            ("instrument_ref", self.instrument_ref),
            ("timeframe_ref", self.timeframe_ref),
            ("schema_ref", self.schema_ref),
        ):
            _exact(reference, name)
        for name, value in (
            ("provider_name", self.provider_name),
            ("declared_market", self.declared_market),
            ("timezone_rule", self.timezone_rule),
            ("ohlc_semantics", self.ohlc_semantics),
            ("volume_semantics", self.volume_semantics),
            ("finality_assumptions", self.finality_assumptions),
            ("provenance_note", self.provenance_note),
        ):
            _required(value, name)
        _optional(self.license_reference, "license_reference")
        _optional(self.deletion_restriction, "deletion_restriction")
        _optional(self.redistribution_restriction, "redistribution_restriction")
        keys = [item[0] for item in self.column_mapping]
        if (
            not self.column_mapping
            or keys != sorted(keys)
            or len(keys) != len(set(keys))
            or any(not key or not value for key, value in self.column_mapping)
        ):
            raise RealCsvContractError("column_mapping must be non-empty, unique and sorted")


@dataclass(frozen=True, slots=True)
class RealCsvAdmissionRecord:
    """Immutable technical outcome; ADMITTED is neither trusted nor research eligible."""

    admission_id: ArtifactId
    version: ObjectVersion
    source_declaration_ref: TraceabilityRef
    original_filename: str
    bounded_relative_path: str
    file_sha256: str
    file_size: int
    ingestion_time: datetime
    parser_contract_version: ObjectVersion
    row_count: int
    status: CsvAdmissionStatus
    findings: tuple[str, ...]
    raw_manifest_ref: TraceabilityRef | None
    raw_lock_ref: TraceabilityRef | None
    normalized_manifest_ref: TraceabilityRef | None
    normalized_lock_ref: TraceabilityRef | None
    trust_state: CsvTrustState
    research_eligibility: ResearchEligibilityState
    contract_version: ObjectVersion

    def __post_init__(self) -> None:
        if self.version != ObjectVersion(1) or self.contract_version != ObjectVersion(1):
            raise RealCsvContractError("unsupported admission record version")
        _exact(self.source_declaration_ref, "source_declaration_ref")
        _required(self.original_filename, "original_filename", 255)
        _required(self.bounded_relative_path, "bounded_relative_path", 1024)
        if self.original_filename != self.original_filename.rsplit("/", 1)[-1]:
            raise RealCsvContractError("original_filename must not contain a path")
        if not re.fullmatch(r"sha256:[0-9a-f]{64}", self.file_sha256):
            raise RealCsvContractError("file_sha256 must be canonical SHA-256")
        if self.file_size < 0 or self.row_count < 0:
            raise RealCsvContractError("file_size and row_count must be non-negative")
        require_utc(self.ingestion_time, "ingestion_time")
        if self.parser_contract_version != ObjectVersion(1):
            raise RealCsvContractError("unsupported parser contract version")
        if (
            len(self.findings) != len(set(self.findings))
            or tuple(sorted(self.findings)) != self.findings
        ):
            raise RealCsvContractError("findings must be unique and sorted")
        refs = (
            self.raw_manifest_ref,
            self.raw_lock_ref,
            self.normalized_manifest_ref,
            self.normalized_lock_ref,
        )
        if self.status is CsvAdmissionStatus.ADMITTED:
            if any(reference is None for reference in refs):
                raise RealCsvContractError("admitted record requires exact dataset references")
            for index, reference in enumerate(refs):
                _exact(reference, f"dataset_ref[{index}]")  # type: ignore[arg-type]
        elif any(reference is not None for reference in refs):
            raise RealCsvContractError("non-admitted outcome cannot claim dataset references")
        if self.trust_state is not CsvTrustState.NOT_TRUSTED:
            raise RealCsvContractError("technical admission cannot grant trust")
        if self.research_eligibility is not ResearchEligibilityState.NOT_RESEARCH_ELIGIBLE:
            raise RealCsvContractError("technical admission cannot grant research eligibility")
