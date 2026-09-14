"""Strict typed canonical codecs for governed institutional records."""

from __future__ import annotations

import json
import re
from datetime import UTC, datetime
from typing import Any, Final, cast

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

REPRESENTATION_FORMAT: Final = "ai-quant-lab.canonical-json"
REPRESENTATION_VERSION: Final = 1
_TIMESTAMP = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{6}Z$")
_FINGERPRINT = re.compile(r"^sha256:[0-9a-f]{64}$")

type GovernedRecord = ArtifactEnvelope | EvidenceEnvelope | ProvenanceRecord | AuditEvent

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
}
_SUPPORTED_TYPES: dict[type[GovernedRecord], str] = {
    ArtifactEnvelope: "ArtifactEnvelope",
    EvidenceEnvelope: "EvidenceEnvelope",
    ProvenanceRecord: "ProvenanceRecord",
    AuditEvent: "AuditEvent",
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


_DECODERS = {
    "ArtifactEnvelope": _decode_artifact,
    "EvidenceEnvelope": _decode_evidence,
    "ProvenanceRecord": _decode_provenance,
    "AuditEvent": _decode_audit,
}


def decode[T: (ArtifactEnvelope, EvidenceEnvelope, ProvenanceRecord, AuditEvent)](
    data: bytes, expected_type: type[T]
) -> T:
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
