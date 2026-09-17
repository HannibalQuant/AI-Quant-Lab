"""Strict typed canonical codecs for governed institutional records."""

from __future__ import annotations

import json
import re
from datetime import UTC, datetime
from typing import Any, Final, cast

from ai_quant_lab.core.data import (
    DataQualityState,
    DatasetLock,
    DatasetLockId,
    DatasetLockState,
    DatasetManifest,
    DecimalValue,
    InstrumentClass,
    InstrumentId,
    InstrumentIdentity,
    ObservationId,
    RawField,
    RawObservation,
    ReconciliationDisposition,
    SourceId,
    SourceIdentity,
    SourceType,
    TemporalCoordinates,
    TemporalPolicy,
    VenueId,
    VenueIdentity,
    VenueType,
)
from ai_quant_lab.core.market_data import (
    AlignmentKind,
    BarFinality,
    BarTimestampMeaning,
    MarketBar,
    MarketBarId,
    MarketDataSchema,
    MarketDataSchemaId,
    NormalizedBarManifest,
    TimeframeId,
    TimeframeIdentity,
    TimeframeUnit,
    VolumeSemantic,
)
from ai_quant_lab.core.model import (
    AgentId,
    ArtifactEnvelope,
    ArtifactId,
    ArtifactLifecycle,
    AuditEvent,
    AuditEventId,
    AuditResult,
    AuthorityBindingId,
    CommandId,
    DatasetId,
    DecisionId,
    EvidenceEnvelope,
    EvidenceId,
    EvidenceState,
    ExperimentId,
    FreshnessState,
    GovernedId,
    InvalidSerialization,
    MonitoringId,
    ObjectVersion,
    ProvenanceId,
    ProvenanceRecord,
    RunId,
    TraceabilityRef,
    TrialId,
    ValidationId,
    VersionedRef,
    canonical_json,
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

REPRESENTATION_FORMAT: Final = "ai-quant-lab.canonical-json"
REPRESENTATION_VERSION: Final = 1
_TIMESTAMP = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{6}Z$")
_FINGERPRINT = re.compile(r"^sha256:[0-9a-f]{64}$")

type GovernedRecord = (
    ArtifactEnvelope
    | EvidenceEnvelope
    | ProvenanceRecord
    | AuditEvent
    | VenueIdentity
    | SourceIdentity
    | InstrumentIdentity
    | RawObservation
    | DatasetManifest
    | DatasetLock
    | TimeframeIdentity
    | MarketDataSchema
    | MarketBar
    | NormalizedBarManifest
    | RealCsvSourceDeclaration
    | RealCsvAdmissionRecord
)

_ID_TYPES: dict[str, type[GovernedId]] = {
    "agent": AgentId,
    "artifact": ArtifactId,
    "audit-event": AuditEventId,
    "authority-binding": AuthorityBindingId,
    "command": CommandId,
    "dataset": DatasetId,
    "decision": DecisionId,
    "evidence": EvidenceId,
    "experiment": ExperimentId,
    "monitoring": MonitoringId,
    "provenance": ProvenanceId,
    "run": RunId,
    "trial": TrialId,
    "validation": ValidationId,
    "source": SourceId,
    "venue": VenueId,
    "instrument": InstrumentId,
    "observation": ObservationId,
    "dataset-lock": DatasetLockId,
    "timeframe": TimeframeId,
    "market-data-schema": MarketDataSchemaId,
    "market-bar": MarketBarId,
}
_SUPPORTED_TYPES: dict[type[GovernedRecord], str] = {
    ArtifactEnvelope: "ArtifactEnvelope",
    EvidenceEnvelope: "EvidenceEnvelope",
    ProvenanceRecord: "ProvenanceRecord",
    AuditEvent: "AuditEvent",
    VenueIdentity: "VenueIdentity",
    SourceIdentity: "SourceIdentity",
    InstrumentIdentity: "InstrumentIdentity",
    RawObservation: "RawObservation",
    DatasetManifest: "DatasetManifest",
    DatasetLock: "DatasetLock",
    TimeframeIdentity: "TimeframeIdentity",
    MarketDataSchema: "MarketDataSchema",
    MarketBar: "MarketBar",
    NormalizedBarManifest: "NormalizedBarManifest",
    RealCsvSourceDeclaration: "RealCsvSourceDeclaration",
    RealCsvAdmissionRecord: "RealCsvAdmissionRecord",
}


def _reject_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise InvalidSerialization(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def _strict_object(value: Any, required: set[str], name: str) -> dict[str, Any]:
    if not isinstance(value, dict) or not all(isinstance(key, str) for key in value):
        raise InvalidSerialization(f"{name} must be an object")
    keys = set(value)
    if keys != required:
        missing = sorted(required - keys)
        unknown = sorted(keys - required)
        raise InvalidSerialization(f"{name} fields mismatch; missing={missing}, unknown={unknown}")
    return cast(dict[str, Any], value)


def _text(value: Any, field: str) -> str:
    if not isinstance(value, str):
        raise InvalidSerialization(f"{field} must be text")
    return value


def _optional_text(value: Any, field: str) -> str | None:
    return None if value is None else _text(value, field)


def _version(value: Any, field: str) -> ObjectVersion:
    if isinstance(value, bool) or not isinstance(value, int):
        raise InvalidSerialization(f"{field} must be a positive integer version")
    return ObjectVersion(value)


def _timestamp(value: Any, field: str) -> datetime:
    text = _text(value, field)
    if not _TIMESTAMP.fullmatch(text):
        raise InvalidSerialization(f"{field} must use UTC microsecond Z format")
    try:
        parsed = datetime.strptime(text, "%Y-%m-%dT%H:%M:%S.%fZ").replace(tzinfo=UTC)
    except ValueError as exc:
        raise InvalidSerialization(f"{field} is invalid") from exc
    return parsed


def _id(value: Any, field: str) -> GovernedId:
    text = _text(value, field)
    namespace = text.partition(":")[0]
    id_type = _ID_TYPES.get(namespace)
    if id_type is None:
        raise InvalidSerialization(f"{field} has unsupported identifier namespace")
    return id_type.parse(text)


def _typed_id(value: Any, expected: type[GovernedId], field: str) -> GovernedId:
    identifier = _id(value, field)
    if not isinstance(identifier, expected):
        raise InvalidSerialization(f"{field} requires {expected.namespace} namespace")
    return identifier


def _ref_payload(reference: VersionedRef) -> dict[str, Any]:
    return {"object_id": str(reference.object_id), "version": reference.version.number}


def _ref(value: Any, field: str) -> VersionedRef:
    item = _strict_object(value, {"object_id", "version"}, field)
    return VersionedRef(
        _id(item["object_id"], f"{field}.object_id"),
        _version(item["version"], f"{field}.version"),
    )


def _optional_ref(value: Any, field: str) -> VersionedRef | None:
    return None if value is None else _ref(value, field)


def _refs(value: Any, field: str) -> tuple[VersionedRef, ...]:
    if not isinstance(value, list):
        raise InvalidSerialization(f"{field} must be an array")
    return tuple(_ref(item, f"{field}[]") for item in value)


def _metadata(value: Any, field: str) -> tuple[tuple[str, str], ...]:
    if not isinstance(value, list):
        raise InvalidSerialization(f"{field} must be an array")
    result: list[tuple[str, str]] = []
    for item in value:
        if not isinstance(item, list) or len(item) != 2:
            raise InvalidSerialization(f"{field} entries must be two-element arrays")
        key, entry = item
        if not isinstance(key, str) or not isinstance(entry, str):
            raise InvalidSerialization(f"{field} entries must contain text")
        result.append((key, entry))
    return tuple(result)


def _strings(value: Any, field: str) -> tuple[str, ...]:
    if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
        raise InvalidSerialization(f"{field} must be an array of text")
    return tuple(value)


def _trace_ref_payload(reference: TraceabilityRef) -> dict[str, Any]:
    return {
        "object_id": str(reference.object_id),
        "version": reference.version.number,
        "expected_fingerprint": reference.expected_fingerprint,
    }


def _trace_ref(value: Any, field: str) -> TraceabilityRef:
    item = _strict_object(value, {"object_id", "version", "expected_fingerprint"}, field)
    fingerprint = item["expected_fingerprint"]
    if fingerprint is not None and (
        not isinstance(fingerprint, str) or not _FINGERPRINT.fullmatch(fingerprint)
    ):
        raise InvalidSerialization(f"{field}.expected_fingerprint is invalid")
    return TraceabilityRef(
        _id(item["object_id"], f"{field}.object_id"),
        _version(item["version"], f"{field}.version"),
        fingerprint,
    )


def _optional_trace_ref(value: Any, field: str) -> TraceabilityRef | None:
    return None if value is None else _trace_ref(value, field)


def _trace_refs(value: Any, field: str) -> tuple[TraceabilityRef, ...]:
    if not isinstance(value, list):
        raise InvalidSerialization(f"{field} must be an array")
    return tuple(_trace_ref(item, f"{field}[]") for item in value)


def _timestamp_payload(value: datetime) -> str:
    return value.isoformat(timespec="microseconds").replace("+00:00", "Z")


def _raw_value_payload(value: str | int | bool | DecimalValue | None) -> dict[str, Any]:
    if value is None:
        return {"kind": "null", "value": None}
    if isinstance(value, bool):
        return {"kind": "boolean", "value": value}
    if isinstance(value, int):
        return {"kind": "integer", "value": value}
    if isinstance(value, DecimalValue):
        return {"kind": "decimal", "value": value.text}
    if isinstance(value, str):
        return {"kind": "text", "value": value}
    raise InvalidSerialization("unsupported raw scalar")


def _raw_value(value: Any, field: str) -> str | int | bool | DecimalValue | None:
    item = _strict_object(value, {"kind", "value"}, field)
    kind = _text(item["kind"], f"{field}.kind")
    scalar = item["value"]
    if kind == "null" and scalar is None:
        return None
    if kind == "boolean" and isinstance(scalar, bool):
        return scalar
    if kind == "integer" and isinstance(scalar, int) and not isinstance(scalar, bool):
        return scalar
    if kind == "text" and isinstance(scalar, str):
        return scalar
    if kind == "decimal" and isinstance(scalar, str):
        return DecimalValue(scalar)
    raise InvalidSerialization(f"{field} has invalid typed raw value")


def _payload(record: GovernedRecord) -> dict[str, Any]:
    if isinstance(record, ArtifactEnvelope):
        return {
            "artifact_id": str(record.artifact_id),
            "artifact_type": record.artifact_type,
            "version": record.version.number,
            "created_at": record.created_at.isoformat(timespec="microseconds").replace(
                "+00:00", "Z"
            ),
            "producer_id": str(record.producer_id),
            "provenance_id": str(record.provenance_id),
            "contract_version": record.contract_version.number,
            "lifecycle": record.lifecycle.value,
            "content_fingerprint": record.content_fingerprint,
            "parent_refs": [_ref_payload(item) for item in record.parent_refs],
            "metadata": [list(item) for item in record.metadata],
        }
    if isinstance(record, EvidenceEnvelope):
        return {
            "evidence_id": str(record.evidence_id),
            "evidence_type": record.evidence_type,
            "source_artifact": _ref_payload(record.source_artifact),
            "provenance_id": str(record.provenance_id),
            "created_at": record.created_at.isoformat(timespec="microseconds").replace(
                "+00:00", "Z"
            ),
            "scope": record.scope,
            "admissibility": record.admissibility.value,
            "freshness": record.freshness.value,
            "supersedes": None if record.supersedes is None else _ref_payload(record.supersedes),
            "invalidates": [_ref_payload(item) for item in record.invalidates],
            "metadata": [list(item) for item in record.metadata],
        }
    if isinstance(record, ProvenanceRecord):
        return {
            "provenance_id": str(record.provenance_id),
            "producer_id": str(record.producer_id),
            "produced_at": record.produced_at.isoformat(timespec="microseconds").replace(
                "+00:00", "Z"
            ),
            "process": record.process,
            "input_refs": [_ref_payload(item) for item in record.input_refs],
            "transformation_ref": (
                None
                if record.transformation_ref is None
                else _ref_payload(record.transformation_ref)
            ),
            "metadata": [list(item) for item in record.metadata],
        }
    if isinstance(record, AuditEvent):
        return {
            "event_id": str(record.event_id),
            "actor_id": str(record.actor_id),
            "action": record.action,
            "target": _ref_payload(record.target),
            "occurred_at": record.occurred_at.isoformat(timespec="microseconds").replace(
                "+00:00", "Z"
            ),
            "result": record.result.value,
            "context": [list(item) for item in record.context],
        }
    if isinstance(record, VenueIdentity):
        return {
            "venue_id": str(record.venue_id),
            "version": record.version.number,
            "name": record.name,
            "venue_type": record.venue_type.value,
            "jurisdiction": record.jurisdiction,
            "contract_version": record.contract_version.number,
        }
    if isinstance(record, SourceIdentity):
        return {
            "source_id": str(record.source_id),
            "version": record.version.number,
            "provider": record.provider,
            "source_type": record.source_type.value,
            "feed": record.feed,
            "source_version": record.source_version,
            "venue_ref": (
                None if record.venue_ref is None else _trace_ref_payload(record.venue_ref)
            ),
            "contract_version": record.contract_version.number,
        }
    if isinstance(record, InstrumentIdentity):
        return {
            "instrument_id": str(record.instrument_id),
            "version": record.version.number,
            "symbol": record.symbol,
            "instrument_class": record.instrument_class.value,
            "base_asset": record.base_asset,
            "quote_asset": record.quote_asset,
            "settlement_asset": record.settlement_asset,
            "venue_ref": (
                None if record.venue_ref is None else _trace_ref_payload(record.venue_ref)
            ),
            "contract_version": record.contract_version.number,
        }
    if isinstance(record, RawObservation):
        return {
            "observation_id": str(record.observation_id),
            "version": record.version.number,
            "source_ref": _trace_ref_payload(record.source_ref),
            "instrument_ref": _trace_ref_payload(record.instrument_ref),
            "temporal": {
                "event_time": _timestamp_payload(record.temporal.event_time),
                "availability_time": _timestamp_payload(record.temporal.availability_time),
                "ingestion_time": _timestamp_payload(record.temporal.ingestion_time),
                "policy": record.temporal.policy.value,
            },
            "payload": [
                {"name": field.name, "value": _raw_value_payload(field.value)}
                for field in record.payload
            ],
            "provenance_ref": _trace_ref_payload(record.provenance_ref),
            "source_sequence": record.source_sequence,
            "quality": record.quality.value,
            "reconciliation": record.reconciliation.value,
            "supersedes": (
                None if record.supersedes is None else _trace_ref_payload(record.supersedes)
            ),
            "contract_version": record.contract_version.number,
        }
    if isinstance(record, DatasetManifest):
        return {
            "dataset_id": str(record.dataset_id),
            "version": record.version.number,
            "created_at": _timestamp_payload(record.created_at),
            "observation_refs": [_trace_ref_payload(item) for item in record.observation_refs],
            "source_refs": [_trace_ref_payload(item) for item in record.source_refs],
            "instrument_refs": [_trace_ref_payload(item) for item in record.instrument_refs],
            "event_time_start": _timestamp_payload(record.event_time_start),
            "event_time_end": _timestamp_payload(record.event_time_end),
            "provenance_ref": _trace_ref_payload(record.provenance_ref),
            "contract_version": record.contract_version.number,
            "membership_policy": record.membership_policy,
        }
    if isinstance(record, DatasetLock):
        return {
            "lock_id": str(record.lock_id),
            "version": record.version.number,
            "dataset_ref": _trace_ref_payload(record.dataset_ref),
            "manifest_ref": _trace_ref_payload(record.manifest_ref),
            "locked_at": _timestamp_payload(record.locked_at),
            "temporal_cutoff": _timestamp_payload(record.temporal_cutoff),
            "provenance_ref": _trace_ref_payload(record.provenance_ref),
            "state": record.state.value,
            "contract_version": record.contract_version.number,
        }
    if isinstance(record, TimeframeIdentity):
        return {
            "timeframe_id": str(record.timeframe_id),
            "version": record.version.number,
            "unit": record.unit.value,
            "count": record.count,
            "alignment": record.alignment.value,
            "contract_version": record.contract_version.number,
        }
    if isinstance(record, MarketDataSchema):
        return {
            "schema_id": str(record.schema_id),
            "version": record.version.number,
            "timeframe_ref": _trace_ref_payload(record.timeframe_ref),
            "timestamp_meaning": record.timestamp_meaning.value,
            "open_time_field": record.open_time_field,
            "close_time_field": record.close_time_field,
            "open_field": record.open_field,
            "high_field": record.high_field,
            "low_field": record.low_field,
            "close_field": record.close_field,
            "volume_field": record.volume_field,
            "finality_field": record.finality_field,
            "volume_semantic": record.volume_semantic.value,
            "contract_version": record.contract_version.number,
        }
    if isinstance(record, MarketBar):
        return {
            "bar_id": str(record.bar_id),
            "version": record.version.number,
            "source_ref": _trace_ref_payload(record.source_ref),
            "instrument_ref": _trace_ref_payload(record.instrument_ref),
            "timeframe_ref": _trace_ref_payload(record.timeframe_ref),
            "schema_ref": _trace_ref_payload(record.schema_ref),
            "normalization_version": record.normalization_version.number,
            "bar_open": _timestamp_payload(record.bar_open),
            "bar_close": _timestamp_payload(record.bar_close),
            "availability_time": _timestamp_payload(record.availability_time),
            "ingestion_time": _timestamp_payload(record.ingestion_time),
            "open": record.open.text,
            "high": record.high.text,
            "low": record.low.text,
            "close": record.close.text,
            "volume": None if record.volume is None else record.volume.text,
            "volume_semantic": record.volume_semantic.value,
            "finality": record.finality.value,
            "source_observation_ref": _trace_ref_payload(record.source_observation_ref),
            "provenance_ref": _trace_ref_payload(record.provenance_ref),
            "supersedes": None
            if record.supersedes is None
            else _trace_ref_payload(record.supersedes),
            "contract_version": record.contract_version.number,
        }
    if isinstance(record, NormalizedBarManifest):
        return {
            "dataset_id": str(record.dataset_id),
            "version": record.version.number,
            "created_at": _timestamp_payload(record.created_at),
            "bar_refs": [_trace_ref_payload(item) for item in record.bar_refs],
            "source_refs": [_trace_ref_payload(item) for item in record.source_refs],
            "instrument_refs": [_trace_ref_payload(item) for item in record.instrument_refs],
            "timeframe_refs": [_trace_ref_payload(item) for item in record.timeframe_refs],
            "schema_ref": _trace_ref_payload(record.schema_ref),
            "normalization_version": record.normalization_version.number,
            "raw_dataset_lock_ref": _trace_ref_payload(record.raw_dataset_lock_ref),
            "provenance_ref": _trace_ref_payload(record.provenance_ref),
            "contract_version": record.contract_version.number,
            "membership_policy": record.membership_policy,
        }
    if isinstance(record, RealCsvSourceDeclaration):
        return {
            "provenance_id": str(record.provenance_id),
            "version": record.version.number,
            "source_ref": _trace_ref_payload(record.source_ref),
            "instrument_ref": _trace_ref_payload(record.instrument_ref),
            "timeframe_ref": _trace_ref_payload(record.timeframe_ref),
            "schema_ref": _trace_ref_payload(record.schema_ref),
            "provider_name": record.provider_name,
            "acquisition_method": record.acquisition_method.value,
            "declared_market": record.declared_market,
            "declared_acquisition_time": None
            if record.declared_acquisition_time is None
            else _timestamp_payload(record.declared_acquisition_time),
            "timestamp_semantics": record.timestamp_semantics.value,
            "availability_semantics": record.availability_semantics.value,
            "timezone_rule": record.timezone_rule,
            "column_mapping": [list(item) for item in record.column_mapping],
            "price_domain": record.price_domain.value,
            "ohlc_semantics": record.ohlc_semantics,
            "volume_semantics": record.volume_semantics.value,
            "finality_assumptions": record.finality_assumptions,
            "missing_data_policy": record.missing_data_policy.value,
            "duplicate_policy": record.duplicate_policy.value,
            "ordering_policy": record.ordering_policy.value,
            "permission_state": record.permission_state.value,
            "license_reference": record.license_reference,
            "retention_classification": record.retention_classification.value,
            "deletion_restriction": record.deletion_restriction,
            "redistribution_restriction": record.redistribution_restriction,
            "operator_id": str(record.operator_id),
            "provenance_note": record.provenance_note,
            "contract_version": record.contract_version.number,
        }
    if isinstance(record, RealCsvAdmissionRecord):
        return {
            "admission_id": str(record.admission_id),
            "version": record.version.number,
            "source_declaration_ref": _trace_ref_payload(record.source_declaration_ref),
            "original_filename": record.original_filename,
            "bounded_relative_path": record.bounded_relative_path,
            "file_sha256": record.file_sha256,
            "file_size": record.file_size,
            "ingestion_time": _timestamp_payload(record.ingestion_time),
            "parser_contract_version": record.parser_contract_version.number,
            "canonical_codec_version": record.canonical_codec_version.number,
            "ingestion_configuration_fingerprint": record.ingestion_configuration_fingerprint,
            "row_count": record.row_count,
            "status": record.status.value,
            "findings": list(record.findings),
            "raw_manifest_ref": None
            if record.raw_manifest_ref is None
            else _trace_ref_payload(record.raw_manifest_ref),
            "raw_lock_ref": None
            if record.raw_lock_ref is None
            else _trace_ref_payload(record.raw_lock_ref),
            "normalized_manifest_ref": None
            if record.normalized_manifest_ref is None
            else _trace_ref_payload(record.normalized_manifest_ref),
            "normalized_lock_ref": None
            if record.normalized_lock_ref is None
            else _trace_ref_payload(record.normalized_lock_ref),
            "trust_state": record.trust_state.value,
            "research_eligibility": record.research_eligibility.value,
            "contract_version": record.contract_version.number,
        }
    raise InvalidSerialization(f"unsupported governed type: {type(record).__name__}")


def encode(record: GovernedRecord) -> bytes:
    """Encode only an explicitly supported governed record to canonical UTF-8 bytes."""
    record_type = _SUPPORTED_TYPES.get(type(record))
    if record_type is None:
        raise InvalidSerialization(f"unsupported governed type: {type(record).__name__}")
    envelope = {
        "$format": REPRESENTATION_FORMAT,
        "$representation_version": REPRESENTATION_VERSION,
        "$type": record_type,
        "payload": _payload(record),
    }
    return canonical_json(envelope).encode("utf-8")


def _decode_artifact(payload: Any) -> ArtifactEnvelope:
    item = _strict_object(
        payload,
        {
            "artifact_id",
            "artifact_type",
            "version",
            "created_at",
            "producer_id",
            "provenance_id",
            "contract_version",
            "lifecycle",
            "content_fingerprint",
            "parent_refs",
            "metadata",
        },
        "ArtifactEnvelope.payload",
    )
    return ArtifactEnvelope(
        cast(ArtifactId, _typed_id(item["artifact_id"], ArtifactId, "artifact_id")),
        _text(item["artifact_type"], "artifact_type"),
        _version(item["version"], "version"),
        _timestamp(item["created_at"], "created_at"),
        cast(AgentId, _typed_id(item["producer_id"], AgentId, "producer_id")),
        cast(ProvenanceId, _typed_id(item["provenance_id"], ProvenanceId, "provenance_id")),
        _version(item["contract_version"], "contract_version"),
        ArtifactLifecycle(_text(item["lifecycle"], "lifecycle")),
        _text(item["content_fingerprint"], "content_fingerprint"),
        _refs(item["parent_refs"], "parent_refs"),
        _metadata(item["metadata"], "metadata"),
    )


def _decode_evidence(payload: Any) -> EvidenceEnvelope:
    item = _strict_object(
        payload,
        {
            "evidence_id",
            "evidence_type",
            "source_artifact",
            "provenance_id",
            "created_at",
            "scope",
            "admissibility",
            "freshness",
            "supersedes",
            "invalidates",
            "metadata",
        },
        "EvidenceEnvelope.payload",
    )
    return EvidenceEnvelope(
        cast(EvidenceId, _typed_id(item["evidence_id"], EvidenceId, "evidence_id")),
        _text(item["evidence_type"], "evidence_type"),
        _ref(item["source_artifact"], "source_artifact"),
        cast(ProvenanceId, _typed_id(item["provenance_id"], ProvenanceId, "provenance_id")),
        _timestamp(item["created_at"], "created_at"),
        _text(item["scope"], "scope"),
        EvidenceState(_text(item["admissibility"], "admissibility")),
        FreshnessState(_text(item["freshness"], "freshness")),
        _optional_ref(item["supersedes"], "supersedes"),
        _refs(item["invalidates"], "invalidates"),
        _metadata(item["metadata"], "metadata"),
    )


def _decode_provenance(payload: Any) -> ProvenanceRecord:
    item = _strict_object(
        payload,
        {
            "provenance_id",
            "producer_id",
            "produced_at",
            "process",
            "input_refs",
            "transformation_ref",
            "metadata",
        },
        "ProvenanceRecord.payload",
    )
    return ProvenanceRecord(
        cast(ProvenanceId, _typed_id(item["provenance_id"], ProvenanceId, "provenance_id")),
        cast(AgentId, _typed_id(item["producer_id"], AgentId, "producer_id")),
        _timestamp(item["produced_at"], "produced_at"),
        _text(item["process"], "process"),
        _refs(item["input_refs"], "input_refs"),
        _optional_ref(item["transformation_ref"], "transformation_ref"),
        _metadata(item["metadata"], "metadata"),
    )


def _decode_audit(payload: Any) -> AuditEvent:
    item = _strict_object(
        payload,
        {"event_id", "actor_id", "action", "target", "occurred_at", "result", "context"},
        "AuditEvent.payload",
    )
    return AuditEvent(
        cast(AuditEventId, _typed_id(item["event_id"], AuditEventId, "event_id")),
        cast(AgentId, _typed_id(item["actor_id"], AgentId, "actor_id")),
        _text(item["action"], "action"),
        _ref(item["target"], "target"),
        _timestamp(item["occurred_at"], "occurred_at"),
        AuditResult(_text(item["result"], "result")),
        _metadata(item["context"], "context"),
    )


def _decode_venue(payload: Any) -> VenueIdentity:
    item = _strict_object(
        payload,
        {"venue_id", "version", "name", "venue_type", "jurisdiction", "contract_version"},
        "VenueIdentity.payload",
    )
    jurisdiction = item["jurisdiction"]
    if jurisdiction is not None:
        jurisdiction = _text(jurisdiction, "jurisdiction")
    return VenueIdentity(
        cast(VenueId, _typed_id(item["venue_id"], VenueId, "venue_id")),
        _version(item["version"], "version"),
        _text(item["name"], "name"),
        VenueType(_text(item["venue_type"], "venue_type")),
        jurisdiction,
        _version(item["contract_version"], "contract_version"),
    )


def _decode_source(payload: Any) -> SourceIdentity:
    item = _strict_object(
        payload,
        {
            "source_id",
            "version",
            "provider",
            "source_type",
            "feed",
            "source_version",
            "venue_ref",
            "contract_version",
        },
        "SourceIdentity.payload",
    )
    return SourceIdentity(
        cast(SourceId, _typed_id(item["source_id"], SourceId, "source_id")),
        _version(item["version"], "version"),
        _text(item["provider"], "provider"),
        SourceType(_text(item["source_type"], "source_type")),
        _text(item["feed"], "feed"),
        _text(item["source_version"], "source_version"),
        _optional_trace_ref(item["venue_ref"], "venue_ref"),
        _version(item["contract_version"], "contract_version"),
    )


def _decode_instrument(payload: Any) -> InstrumentIdentity:
    item = _strict_object(
        payload,
        {
            "instrument_id",
            "version",
            "symbol",
            "instrument_class",
            "base_asset",
            "quote_asset",
            "settlement_asset",
            "venue_ref",
            "contract_version",
        },
        "InstrumentIdentity.payload",
    )
    return InstrumentIdentity(
        cast(InstrumentId, _typed_id(item["instrument_id"], InstrumentId, "instrument_id")),
        _version(item["version"], "version"),
        _text(item["symbol"], "symbol"),
        InstrumentClass(_text(item["instrument_class"], "instrument_class")),
        _optional_text(item["base_asset"], "base_asset"),
        _optional_text(item["quote_asset"], "quote_asset"),
        _optional_text(item["settlement_asset"], "settlement_asset"),
        _optional_trace_ref(item["venue_ref"], "venue_ref"),
        _version(item["contract_version"], "contract_version"),
    )


def _decode_temporal(value: Any) -> TemporalCoordinates:
    item = _strict_object(
        value, {"event_time", "availability_time", "ingestion_time", "policy"}, "temporal"
    )
    return TemporalCoordinates(
        _timestamp(item["event_time"], "event_time"),
        _timestamp(item["availability_time"], "availability_time"),
        _timestamp(item["ingestion_time"], "ingestion_time"),
        TemporalPolicy(_text(item["policy"], "policy")),
    )


def _decode_raw_fields(value: Any) -> tuple[RawField, ...]:
    if not isinstance(value, list):
        raise InvalidSerialization("payload fields must be an array")
    fields: list[RawField] = []
    for raw in value:
        item = _strict_object(raw, {"name", "value"}, "payload[]")
        name = _text(item["name"], "payload[].name")
        fields.append(RawField(name, _raw_value(item["value"], f"payload[{name}].value")))
    return tuple(fields)


def _decode_observation(payload: Any) -> RawObservation:
    item = _strict_object(
        payload,
        {
            "observation_id",
            "version",
            "source_ref",
            "instrument_ref",
            "temporal",
            "payload",
            "provenance_ref",
            "source_sequence",
            "quality",
            "reconciliation",
            "supersedes",
            "contract_version",
        },
        "RawObservation.payload",
    )
    sequence = item["source_sequence"]
    if sequence is not None:
        sequence = _text(sequence, "source_sequence")
    return RawObservation(
        cast(ObservationId, _typed_id(item["observation_id"], ObservationId, "observation_id")),
        _version(item["version"], "version"),
        _trace_ref(item["source_ref"], "source_ref"),
        _trace_ref(item["instrument_ref"], "instrument_ref"),
        _decode_temporal(item["temporal"]),
        _decode_raw_fields(item["payload"]),
        _trace_ref(item["provenance_ref"], "provenance_ref"),
        sequence,
        DataQualityState(_text(item["quality"], "quality")),
        ReconciliationDisposition(_text(item["reconciliation"], "reconciliation")),
        _optional_trace_ref(item["supersedes"], "supersedes"),
        _version(item["contract_version"], "contract_version"),
    )


def _decode_manifest(payload: Any) -> DatasetManifest:
    item = _strict_object(
        payload,
        {
            "dataset_id",
            "version",
            "created_at",
            "observation_refs",
            "source_refs",
            "instrument_refs",
            "event_time_start",
            "event_time_end",
            "provenance_ref",
            "contract_version",
            "membership_policy",
        },
        "DatasetManifest.payload",
    )
    return DatasetManifest(
        cast(DatasetId, _typed_id(item["dataset_id"], DatasetId, "dataset_id")),
        _version(item["version"], "version"),
        _timestamp(item["created_at"], "created_at"),
        _trace_refs(item["observation_refs"], "observation_refs"),
        _trace_refs(item["source_refs"], "source_refs"),
        _trace_refs(item["instrument_refs"], "instrument_refs"),
        _timestamp(item["event_time_start"], "event_time_start"),
        _timestamp(item["event_time_end"], "event_time_end"),
        _trace_ref(item["provenance_ref"], "provenance_ref"),
        _version(item["contract_version"], "contract_version"),
        _text(item["membership_policy"], "membership_policy"),
    )


def _decode_lock(payload: Any) -> DatasetLock:
    item = _strict_object(
        payload,
        {
            "lock_id",
            "version",
            "dataset_ref",
            "manifest_ref",
            "locked_at",
            "temporal_cutoff",
            "provenance_ref",
            "state",
            "contract_version",
        },
        "DatasetLock.payload",
    )
    return DatasetLock(
        cast(DatasetLockId, _typed_id(item["lock_id"], DatasetLockId, "lock_id")),
        _version(item["version"], "version"),
        _trace_ref(item["dataset_ref"], "dataset_ref"),
        _trace_ref(item["manifest_ref"], "manifest_ref"),
        _timestamp(item["locked_at"], "locked_at"),
        _timestamp(item["temporal_cutoff"], "temporal_cutoff"),
        _trace_ref(item["provenance_ref"], "provenance_ref"),
        DatasetLockState(_text(item["state"], "state")),
        _version(item["contract_version"], "contract_version"),
    )


def _decode_timeframe(payload: Any) -> TimeframeIdentity:
    item = _strict_object(
        payload,
        {
            "timeframe_id",
            "version",
            "unit",
            "count",
            "alignment",
            "contract_version",
        },
        "TimeframeIdentity.payload",
    )
    count = item["count"]
    if isinstance(count, bool) or not isinstance(count, int):
        raise InvalidSerialization("timeframe count must be integer")
    return TimeframeIdentity(
        cast(TimeframeId, _typed_id(item["timeframe_id"], TimeframeId, "timeframe_id")),
        _version(item["version"], "version"),
        TimeframeUnit(_text(item["unit"], "unit")),
        count,
        AlignmentKind(_text(item["alignment"], "alignment")),
        _version(item["contract_version"], "contract_version"),
    )


def _decode_bar_schema(payload: Any) -> MarketDataSchema:
    fields = {
        "schema_id",
        "version",
        "timeframe_ref",
        "timestamp_meaning",
        "open_time_field",
        "close_time_field",
        "open_field",
        "high_field",
        "low_field",
        "close_field",
        "volume_field",
        "finality_field",
        "volume_semantic",
        "contract_version",
    }
    item = _strict_object(payload, fields, "MarketDataSchema.payload")
    return MarketDataSchema(
        cast(MarketDataSchemaId, _typed_id(item["schema_id"], MarketDataSchemaId, "schema_id")),
        _version(item["version"], "version"),
        _trace_ref(item["timeframe_ref"], "timeframe_ref"),
        BarTimestampMeaning(_text(item["timestamp_meaning"], "timestamp_meaning")),
        _text(item["open_time_field"], "open_time_field"),
        _text(item["close_time_field"], "close_time_field"),
        _text(item["open_field"], "open_field"),
        _text(item["high_field"], "high_field"),
        _text(item["low_field"], "low_field"),
        _text(item["close_field"], "close_field"),
        _optional_text(item["volume_field"], "volume_field"),
        _text(item["finality_field"], "finality_field"),
        VolumeSemantic(_text(item["volume_semantic"], "volume_semantic")),
        _version(item["contract_version"], "contract_version"),
    )


def _decode_market_bar(payload: Any) -> MarketBar:
    item = _strict_object(
        payload,
        {
            "bar_id",
            "version",
            "source_ref",
            "instrument_ref",
            "timeframe_ref",
            "schema_ref",
            "normalization_version",
            "bar_open",
            "bar_close",
            "availability_time",
            "ingestion_time",
            "open",
            "high",
            "low",
            "close",
            "volume",
            "volume_semantic",
            "finality",
            "source_observation_ref",
            "provenance_ref",
            "supersedes",
            "contract_version",
        },
        "MarketBar.payload",
    )
    volume = item["volume"]
    return MarketBar(
        cast(MarketBarId, _typed_id(item["bar_id"], MarketBarId, "bar_id")),
        _version(item["version"], "version"),
        _trace_ref(item["source_ref"], "source_ref"),
        _trace_ref(item["instrument_ref"], "instrument_ref"),
        _trace_ref(item["timeframe_ref"], "timeframe_ref"),
        _trace_ref(item["schema_ref"], "schema_ref"),
        _version(item["normalization_version"], "normalization_version"),
        _timestamp(item["bar_open"], "bar_open"),
        _timestamp(item["bar_close"], "bar_close"),
        _timestamp(item["availability_time"], "availability_time"),
        _timestamp(item["ingestion_time"], "ingestion_time"),
        DecimalValue(_text(item["open"], "open")),
        DecimalValue(_text(item["high"], "high")),
        DecimalValue(_text(item["low"], "low")),
        DecimalValue(_text(item["close"], "close")),
        None if volume is None else DecimalValue(_text(volume, "volume")),
        VolumeSemantic(_text(item["volume_semantic"], "volume_semantic")),
        BarFinality(_text(item["finality"], "finality")),
        _trace_ref(item["source_observation_ref"], "source_observation_ref"),
        _trace_ref(item["provenance_ref"], "provenance_ref"),
        _optional_trace_ref(item["supersedes"], "supersedes"),
        _version(item["contract_version"], "contract_version"),
    )


def _decode_normalized_manifest(payload: Any) -> NormalizedBarManifest:
    item = _strict_object(
        payload,
        {
            "dataset_id",
            "version",
            "created_at",
            "bar_refs",
            "source_refs",
            "instrument_refs",
            "timeframe_refs",
            "schema_ref",
            "normalization_version",
            "raw_dataset_lock_ref",
            "provenance_ref",
            "contract_version",
            "membership_policy",
        },
        "NormalizedBarManifest.payload",
    )
    return NormalizedBarManifest(
        cast(DatasetId, _typed_id(item["dataset_id"], DatasetId, "dataset_id")),
        _version(item["version"], "version"),
        _timestamp(item["created_at"], "created_at"),
        _trace_refs(item["bar_refs"], "bar_refs"),
        _trace_refs(item["source_refs"], "source_refs"),
        _trace_refs(item["instrument_refs"], "instrument_refs"),
        _trace_refs(item["timeframe_refs"], "timeframe_refs"),
        _trace_ref(item["schema_ref"], "schema_ref"),
        _version(item["normalization_version"], "normalization_version"),
        _trace_ref(item["raw_dataset_lock_ref"], "raw_dataset_lock_ref"),
        _trace_ref(item["provenance_ref"], "provenance_ref"),
        _version(item["contract_version"], "contract_version"),
        _text(item["membership_policy"], "membership_policy"),
    )


def _decode_real_csv_source_declaration(payload: Any) -> RealCsvSourceDeclaration:
    fields = {
        "provenance_id",
        "version",
        "source_ref",
        "instrument_ref",
        "timeframe_ref",
        "schema_ref",
        "provider_name",
        "acquisition_method",
        "declared_market",
        "declared_acquisition_time",
        "timestamp_semantics",
        "availability_semantics",
        "timezone_rule",
        "column_mapping",
        "price_domain",
        "ohlc_semantics",
        "volume_semantics",
        "finality_assumptions",
        "missing_data_policy",
        "duplicate_policy",
        "ordering_policy",
        "permission_state",
        "license_reference",
        "retention_classification",
        "deletion_restriction",
        "redistribution_restriction",
        "operator_id",
        "provenance_note",
        "contract_version",
    }
    item = _strict_object(payload, fields, "RealCsvSourceDeclaration.payload")
    return RealCsvSourceDeclaration(
        cast(ProvenanceId, _typed_id(item["provenance_id"], ProvenanceId, "provenance_id")),
        _version(item["version"], "version"),
        _trace_ref(item["source_ref"], "source_ref"),
        _trace_ref(item["instrument_ref"], "instrument_ref"),
        _trace_ref(item["timeframe_ref"], "timeframe_ref"),
        _trace_ref(item["schema_ref"], "schema_ref"),
        _text(item["provider_name"], "provider_name"),
        AcquisitionMethod(_text(item["acquisition_method"], "acquisition_method")),
        _text(item["declared_market"], "declared_market"),
        None
        if item["declared_acquisition_time"] is None
        else _timestamp(item["declared_acquisition_time"], "declared_acquisition_time"),
        TimestampSemantics(_text(item["timestamp_semantics"], "timestamp_semantics")),
        AvailabilitySemantics(_text(item["availability_semantics"], "availability_semantics")),
        _text(item["timezone_rule"], "timezone_rule"),
        _metadata(item["column_mapping"], "column_mapping"),
        PriceDomain(_text(item["price_domain"], "price_domain")),
        _text(item["ohlc_semantics"], "ohlc_semantics"),
        VolumeSemantic(_text(item["volume_semantics"], "volume_semantics")),
        _text(item["finality_assumptions"], "finality_assumptions"),
        MissingDataPolicy(_text(item["missing_data_policy"], "missing_data_policy")),
        DuplicatePolicy(_text(item["duplicate_policy"], "duplicate_policy")),
        OrderingPolicy(_text(item["ordering_policy"], "ordering_policy")),
        SourcePermissionState(_text(item["permission_state"], "permission_state")),
        _optional_text(item["license_reference"], "license_reference"),
        RetentionClassification(
            _text(item["retention_classification"], "retention_classification")
        ),
        _optional_text(item["deletion_restriction"], "deletion_restriction"),
        _optional_text(item["redistribution_restriction"], "redistribution_restriction"),
        cast(AgentId, _typed_id(item["operator_id"], AgentId, "operator_id")),
        _text(item["provenance_note"], "provenance_note"),
        _version(item["contract_version"], "contract_version"),
    )


def _decode_real_csv_admission(payload: Any) -> RealCsvAdmissionRecord:
    fields = {
        "admission_id",
        "version",
        "source_declaration_ref",
        "original_filename",
        "bounded_relative_path",
        "file_sha256",
        "file_size",
        "ingestion_time",
        "parser_contract_version",
        "canonical_codec_version",
        "ingestion_configuration_fingerprint",
        "row_count",
        "status",
        "findings",
        "raw_manifest_ref",
        "raw_lock_ref",
        "normalized_manifest_ref",
        "normalized_lock_ref",
        "trust_state",
        "research_eligibility",
        "contract_version",
    }
    item = _strict_object(payload, fields, "RealCsvAdmissionRecord.payload")
    file_size = item["file_size"]
    row_count = item["row_count"]
    if any(
        isinstance(value, bool) or not isinstance(value, int) for value in (file_size, row_count)
    ):
        raise InvalidSerialization("file_size and row_count must be integers")
    return RealCsvAdmissionRecord(
        cast(ArtifactId, _typed_id(item["admission_id"], ArtifactId, "admission_id")),
        _version(item["version"], "version"),
        _trace_ref(item["source_declaration_ref"], "source_declaration_ref"),
        _text(item["original_filename"], "original_filename"),
        _text(item["bounded_relative_path"], "bounded_relative_path"),
        _text(item["file_sha256"], "file_sha256"),
        file_size,
        _timestamp(item["ingestion_time"], "ingestion_time"),
        _version(item["parser_contract_version"], "parser_contract_version"),
        _version(item["canonical_codec_version"], "canonical_codec_version"),
        _text(
            item["ingestion_configuration_fingerprint"],
            "ingestion_configuration_fingerprint",
        ),
        row_count,
        CsvAdmissionStatus(_text(item["status"], "status")),
        _strings(item["findings"], "findings"),
        _optional_trace_ref(item["raw_manifest_ref"], "raw_manifest_ref"),
        _optional_trace_ref(item["raw_lock_ref"], "raw_lock_ref"),
        _optional_trace_ref(item["normalized_manifest_ref"], "normalized_manifest_ref"),
        _optional_trace_ref(item["normalized_lock_ref"], "normalized_lock_ref"),
        CsvTrustState(_text(item["trust_state"], "trust_state")),
        ResearchEligibilityState(_text(item["research_eligibility"], "research_eligibility")),
        _version(item["contract_version"], "contract_version"),
    )


_DECODERS = {
    "ArtifactEnvelope": _decode_artifact,
    "EvidenceEnvelope": _decode_evidence,
    "ProvenanceRecord": _decode_provenance,
    "AuditEvent": _decode_audit,
    "VenueIdentity": _decode_venue,
    "SourceIdentity": _decode_source,
    "InstrumentIdentity": _decode_instrument,
    "RawObservation": _decode_observation,
    "DatasetManifest": _decode_manifest,
    "DatasetLock": _decode_lock,
    "TimeframeIdentity": _decode_timeframe,
    "MarketDataSchema": _decode_bar_schema,
    "MarketBar": _decode_market_bar,
    "NormalizedBarManifest": _decode_normalized_manifest,
    "RealCsvSourceDeclaration": _decode_real_csv_source_declaration,
    "RealCsvAdmissionRecord": _decode_real_csv_admission,
}


def decode[
    T: (
        ArtifactEnvelope,
        EvidenceEnvelope,
        ProvenanceRecord,
        AuditEvent,
        VenueIdentity,
        SourceIdentity,
        InstrumentIdentity,
        RawObservation,
        DatasetManifest,
        DatasetLock,
        TimeframeIdentity,
        MarketDataSchema,
        MarketBar,
        NormalizedBarManifest,
        RealCsvSourceDeclaration,
        RealCsvAdmissionRecord,
    )
](data: bytes, expected_type: type[T]) -> T:
    """Strictly reconstruct an exact governed type from canonical bytes."""
    if not isinstance(data, bytes):
        raise InvalidSerialization("canonical representation must be bytes")
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise InvalidSerialization("canonical bytes must be UTF-8") from exc
    try:
        raw = json.loads(
            text,
            object_pairs_hook=_reject_duplicate_keys,
            parse_constant=lambda value: (_ for _ in ()).throw(
                InvalidSerialization(f"non-finite number: {value}")
            ),
        )
    except (json.JSONDecodeError, TypeError, ValueError) as exc:
        if isinstance(exc, InvalidSerialization):
            raise
        raise InvalidSerialization("malformed canonical JSON") from exc
    if canonical_json(raw) != text:
        raise InvalidSerialization("input is not canonical JSON")
    envelope = _strict_object(
        raw, {"$format", "$representation_version", "$type", "payload"}, "representation"
    )
    if envelope["$format"] != REPRESENTATION_FORMAT:
        raise InvalidSerialization("unknown representation format")
    if envelope["$representation_version"] != REPRESENTATION_VERSION:
        raise InvalidSerialization("unknown representation version")
    type_name = _text(envelope["$type"], "$type")
    expected_name = _SUPPORTED_TYPES.get(expected_type)
    if expected_name is None or type_name != expected_name:
        raise InvalidSerialization("governed record type mismatch")
    decoder = _DECODERS.get(type_name)
    if decoder is None:
        raise InvalidSerialization("unknown governed record type")
    try:
        record = decoder(envelope["payload"])
    except (TypeError, ValueError) as exc:
        if isinstance(exc, InvalidSerialization):
            raise
        raise InvalidSerialization(f"invalid {type_name} payload") from exc
    if type(record) is not expected_type:
        raise InvalidSerialization("decoder returned an unexpected governed type")
    return record


def encode_traceability(reference: TraceabilityRef) -> bytes:
    """Canonical representation for an exact typed reference, not a following alias."""
    envelope = {
        "$format": REPRESENTATION_FORMAT,
        "$representation_version": REPRESENTATION_VERSION,
        "$type": "TraceabilityRef",
        "payload": {
            "object_id": str(reference.object_id),
            "version": reference.version.number,
            "expected_fingerprint": reference.expected_fingerprint,
        },
    }
    return canonical_json(envelope).encode("utf-8")


def decode_traceability(data: bytes) -> TraceabilityRef:
    if not isinstance(data, bytes):
        raise InvalidSerialization("canonical representation must be bytes")
    try:
        text = data.decode("utf-8")
        raw = json.loads(text, object_pairs_hook=_reject_duplicate_keys)
    except (UnicodeDecodeError, json.JSONDecodeError, TypeError, ValueError) as exc:
        if isinstance(exc, InvalidSerialization):
            raise
        raise InvalidSerialization("malformed traceability representation") from exc
    if canonical_json(raw) != text:
        raise InvalidSerialization("input is not canonical JSON")
    envelope = _strict_object(
        raw, {"$format", "$representation_version", "$type", "payload"}, "representation"
    )
    if (
        envelope["$format"] != REPRESENTATION_FORMAT
        or envelope["$representation_version"] != REPRESENTATION_VERSION
        or envelope["$type"] != "TraceabilityRef"
    ):
        raise InvalidSerialization("unsupported traceability representation")
    payload = _strict_object(
        envelope["payload"],
        {"object_id", "version", "expected_fingerprint"},
        "TraceabilityRef.payload",
    )
    expected = payload["expected_fingerprint"]
    if expected is not None and (
        not isinstance(expected, str) or not _FINGERPRINT.fullmatch(expected)
    ):
        raise InvalidSerialization("invalid expected fingerprint")
    return TraceabilityRef(
        _id(payload["object_id"], "object_id"),
        _version(payload["version"], "version"),
        expected,
    )
