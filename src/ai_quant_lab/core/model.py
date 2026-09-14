"""Immutable identities, versions, records, states, and canonical serialization."""

from __future__ import annotations

import dataclasses
import hashlib
import json
import math
import re
import uuid
from dataclasses import dataclass
from datetime import UTC, datetime
from enum import Enum, StrEnum
from typing import Any, ClassVar, Self


class GovernanceError(ValueError):
    """Base class for fail-closed governed input errors."""


class InvalidIdentifier(GovernanceError):
    pass


class InvalidVersion(GovernanceError):
    pass


class InvalidRecord(GovernanceError):
    pass


class InvalidSerialization(GovernanceError):
    pass


class InvalidState(GovernanceError):
    pass


_TOKEN = re.compile(r"^[a-z0-9][a-z0-9._-]{0,62}$")


@dataclass(frozen=True, slots=True, order=True)
class GovernedId:
    value: str
    namespace: ClassVar[str] = "object"

    def __post_init__(self) -> None:
        if not isinstance(self.value, str) or not _TOKEN.fullmatch(self.value):
            raise InvalidIdentifier(f"invalid {self.namespace} identifier token")

    def __str__(self) -> str:
        return f"{self.namespace}:{self.value}"

    @classmethod
    def parse(cls, text: str) -> Self:
        prefix = f"{cls.namespace}:"
        if not isinstance(text, str) or not text.startswith(prefix) or text.count(":") != 1:
            raise InvalidIdentifier(f"expected namespace {cls.namespace!r}")
        return cls(text[len(prefix) :])

    @classmethod
    def new(cls) -> Self:
        return cls(uuid.uuid4().hex)


class ArtifactId(GovernedId):
    namespace = "artifact"


class EvidenceId(GovernedId):
    namespace = "evidence"


class ProvenanceId(GovernedId):
    namespace = "provenance"


class DatasetId(GovernedId):
    namespace = "dataset"


class ExperimentId(GovernedId):
    namespace = "experiment"


class RunId(GovernedId):
    namespace = "run"


class TrialId(GovernedId):
    namespace = "trial"


class ValidationId(GovernedId):
    namespace = "validation"


class MonitoringId(GovernedId):
    namespace = "monitoring"


class CommandId(GovernedId):
    namespace = "command"


class DecisionId(GovernedId):
    namespace = "decision"


class AuditEventId(GovernedId):
    namespace = "audit-event"


class AuthorityBindingId(GovernedId):
    namespace = "authority-binding"


class AgentId(GovernedId):
    namespace = "agent"


@dataclass(frozen=True, slots=True, order=True)
class ObjectVersion:
    number: int

    def __post_init__(self) -> None:
        if isinstance(self.number, bool) or not isinstance(self.number, int) or self.number < 1:
            raise InvalidVersion("version must be a positive integer")

    @classmethod
    def parse(cls, text: str) -> ObjectVersion:
        if not isinstance(text, str) or not text.isascii() or not text.isdecimal():
            raise InvalidVersion("version must contain ASCII decimal digits")
        return cls(int(text))


@dataclass(frozen=True, slots=True)
class VersionedRef:
    object_id: GovernedId
    version: ObjectVersion

    def __post_init__(self) -> None:
        if not isinstance(self.object_id, GovernedId) or not isinstance(
            self.version, ObjectVersion
        ):
            raise InvalidVersion("exact typed identity and ObjectVersion are required")


def require_utc(value: datetime, field: str = "timestamp") -> datetime:
    if not isinstance(value, datetime) or value.tzinfo is None or value.utcoffset() is None:
        raise InvalidRecord(f"{field} must be timezone-aware")
    if value.utcoffset() != UTC.utcoffset(value):
        raise InvalidRecord(f"{field} must be normalized to UTC")
    return value


class StateAxis(StrEnum):
    ARTIFACT_LIFECYCLE = "artifact_lifecycle"
    EVIDENCE = "evidence"
    WORKFLOW = "workflow"
    VALIDATION = "validation"
    DECISION = "decision"
    MONITORING = "monitoring"
    COMMAND = "command"
    EXECUTION = "execution"


class ArtifactLifecycle(StrEnum):
    DRAFT = "draft"
    FROZEN = "frozen"
    SUPERSEDED = "superseded"
    INVALIDATED = "invalidated"
    ARCHIVED = "archived"


class EvidenceState(StrEnum):
    UNASSESSED = "unassessed"
    ADMISSIBLE = "admissible"
    INADMISSIBLE = "inadmissible"
    CONTRADICTED = "contradicted"
    QUARANTINED = "quarantined"
    INVALIDATED = "invalidated"


class FreshnessState(StrEnum):
    UNASSESSED = "unassessed"
    CURRENT = "current"
    AGING = "aging"
    STALE = "stale"
    INVALIDATED = "invalidated"


class ExecutionState(StrEnum):
    PLANNED_CLOSED = "PLANNED_CLOSED"


@dataclass(frozen=True, slots=True)
class StateAssignment:
    axis: StateAxis
    value: str

    def __post_init__(self) -> None:
        if (
            not isinstance(self.axis, StateAxis)
            or not isinstance(self.value, str)
            or not self.value
        ):
            raise InvalidState("state requires an explicit axis and value")
        if self.axis is StateAxis.EXECUTION and self.value != ExecutionState.PLANNED_CLOSED:
            raise InvalidState("EXE-01 supports only PLANNED_CLOSED")


@dataclass(frozen=True, slots=True)
class StateVector:
    assignments: tuple[StateAssignment, ...]

    def __post_init__(self) -> None:
        axes = [item.axis for item in self.assignments]
        if len(axes) != len(set(axes)):
            raise InvalidState("state axes cannot be duplicated or conflated")


Metadata = tuple[tuple[str, str], ...]


def _metadata(value: Metadata) -> None:
    keys = [key for key, _ in value]
    if any(not key for key in keys) or len(keys) != len(set(keys)) or keys != sorted(keys):
        raise InvalidRecord("metadata keys must be non-empty, unique, and sorted")


@dataclass(frozen=True, slots=True)
class ProvenanceRecord:
    provenance_id: ProvenanceId
    producer_id: AgentId
    produced_at: datetime
    process: str
    input_refs: tuple[VersionedRef, ...] = ()
    transformation_ref: VersionedRef | None = None
    metadata: Metadata = ()

    def __post_init__(self) -> None:
        require_utc(self.produced_at, "produced_at")
        if not self.process.strip():
            raise InvalidRecord("process is required")
        _metadata(self.metadata)


@dataclass(frozen=True, slots=True)
class ArtifactEnvelope:
    artifact_id: ArtifactId
    artifact_type: str
    version: ObjectVersion
    created_at: datetime
    producer_id: AgentId
    provenance_id: ProvenanceId
    contract_version: ObjectVersion
    lifecycle: ArtifactLifecycle
    content_fingerprint: str
    parent_refs: tuple[VersionedRef, ...] = ()
    metadata: Metadata = ()

    def __post_init__(self) -> None:
        require_utc(self.created_at, "created_at")
        if not self.artifact_type.strip():
            raise InvalidRecord("artifact_type is required")
        if not re.fullmatch(r"sha256:[0-9a-f]{64}", self.content_fingerprint):
            raise InvalidRecord("content_fingerprint must be canonical SHA-256")
        _metadata(self.metadata)


@dataclass(frozen=True, slots=True)
class EvidenceEnvelope:
    evidence_id: EvidenceId
    evidence_type: str
    source_artifact: VersionedRef
    provenance_id: ProvenanceId
    created_at: datetime
    scope: str
    admissibility: EvidenceState = EvidenceState.UNASSESSED
    freshness: FreshnessState = FreshnessState.UNASSESSED
    supersedes: VersionedRef | None = None
    invalidates: tuple[VersionedRef, ...] = ()
    metadata: Metadata = ()

    def __post_init__(self) -> None:
        require_utc(self.created_at, "created_at")
        if not self.evidence_type.strip() or not self.scope.strip():
            raise InvalidRecord("evidence type and scope are required")
        if not isinstance(self.source_artifact.object_id, ArtifactId):
            raise InvalidRecord("evidence requires an exact ArtifactId reference")
        _metadata(self.metadata)


class AuditResult(StrEnum):
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    FAILED = "failed"
    RECORDED = "recorded"


@dataclass(frozen=True, slots=True)
class AuditEvent:
    event_id: AuditEventId
    actor_id: AgentId
    action: str
    target: VersionedRef
    occurred_at: datetime
    result: AuditResult
    context: Metadata = ()

    def __post_init__(self) -> None:
        require_utc(self.occurred_at, "occurred_at")
        if not self.action.strip():
            raise InvalidRecord("action is required")
        _metadata(self.context)


SERIALIZATION_FORMAT = "ai-quant-lab.canonical-json"
SERIALIZATION_VERSION = 1


def _canonical(value: Any) -> Any:
    if isinstance(value, GovernedId):
        return str(value)
    if isinstance(value, datetime):
        return require_utc(value).isoformat(timespec="microseconds").replace("+00:00", "Z")
    if isinstance(value, Enum):
        return value.value
    if dataclasses.is_dataclass(value) and not isinstance(value, type):
        return {
            field.name: _canonical(getattr(value, field.name))
            for field in dataclasses.fields(value)
        }
    if isinstance(value, dict):
        if not all(isinstance(key, str) for key in value):
            raise InvalidSerialization("mapping keys must be strings")
        return {key: _canonical(item) for key, item in value.items()}
    if isinstance(value, (tuple, list)):
        return [_canonical(item) for item in value]
    if isinstance(value, float) and not math.isfinite(value):
        raise InvalidSerialization("non-finite numbers are not canonical")
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    raise InvalidSerialization(f"unsupported canonical type: {type(value).__name__}")


def canonical_json(value: Any) -> str:
    try:
        return json.dumps(
            _canonical(value),
            ensure_ascii=False,
            allow_nan=False,
            sort_keys=True,
            separators=(",", ":"),
        )
    except (TypeError, ValueError) as exc:
        raise InvalidSerialization("cannot serialize canonical JSON v1") from exc


def canonical_loads(payload: str) -> Any:
    if not isinstance(payload, str):
        raise InvalidSerialization("payload must be text")
    try:
        value = json.loads(payload)
    except (json.JSONDecodeError, TypeError) as exc:
        raise InvalidSerialization("malformed canonical JSON") from exc
    if canonical_json(value) != payload:
        raise InvalidSerialization("JSON is not canonical JSON v1")
    return value


def fingerprint(value: Any) -> str:
    return "sha256:" + hashlib.sha256(canonical_json(value).encode()).hexdigest()
