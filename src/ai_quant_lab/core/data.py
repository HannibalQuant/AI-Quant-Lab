"""Immutable governed market-data foundation contracts; no acquisition or engine behavior."""

from __future__ import annotations

import re
from dataclasses import dataclass
from dataclasses import field as dataclass_field
from datetime import datetime
from decimal import Decimal, InvalidOperation
from enum import StrEnum

from ai_quant_lab.core.model import (
    DatasetId,
    GovernedId,
    InvalidRecord,
    ObjectVersion,
    ProvenanceId,
    TraceabilityRef,
    require_utc,
)

_TOKEN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:/-]{0,127}$")
_FIELD = re.compile(r"^[a-z][a-z0-9_]{0,62}$")
_DERIVED_FIELD_PREFIXES = (
    "feature",
    "indicator",
    "signal",
    "strategy",
    "decision",
    "order",
    "position",
)
_SHA256 = re.compile(r"^sha256:[0-9a-f]{64}$")


class InvalidDataContract(InvalidRecord):
    pass


class InvalidTemporalOrder(InvalidDataContract):
    pass


class InvalidDecimal(InvalidDataContract):
    pass


class SourceId(GovernedId):
    namespace = "source"


class VenueId(GovernedId):
    namespace = "venue"


class InstrumentId(GovernedId):
    namespace = "instrument"


class ObservationId(GovernedId):
    namespace = "observation"


class DatasetLockId(GovernedId):
    namespace = "dataset-lock"


class SourceType(StrEnum):
    DIRECT_VENUE = "direct_venue"
    DATA_VENDOR = "data_vendor"
    INDEX_PROVIDER = "index_provider"
    BROKER_FEED = "broker_feed"
    FILE_SNAPSHOT = "file_snapshot"
    SYNTHETIC_FIXTURE = "synthetic_fixture"
    OTHER = "other"


class VenueType(StrEnum):
    EXCHANGE = "exchange"
    BROKER = "broker"
    OTC = "otc"
    INDEX_PROVIDER = "index_provider"
    DATA_VENDOR = "data_vendor"
    SYNTHETIC = "synthetic"
    OTHER = "other"


class InstrumentClass(StrEnum):
    SPOT = "spot"
    FUTURE = "future"
    PERPETUAL = "perpetual"
    FX = "fx"
    EQUITY = "equity"
    INDEX = "index"
    COMMODITY = "commodity"
    OTHER = "other"


class TemporalPolicy(StrEnum):
    STRICT_KNOWLEDGE_ORDER = "event_lte_availability_lte_ingestion"


class DataQualityState(StrEnum):
    ACCEPTED = "accepted"
    SUSPECT = "suspect"
    QUARANTINED = "quarantined"
    INVALIDATED = "invalidated"


class ReconciliationDisposition(StrEnum):
    UNIQUE = "unique"
    BYTE_IDENTICAL_DUPLICATE = "byte_identical_duplicate"
    SAME_EVENT_DUPLICATE = "same_event_duplicate"
    RETRANSMISSION = "retransmission"
    CORRECTION = "correction"
    CONFLICT = "conflict"
    UNRESOLVED = "unresolved"


class DatasetLockState(StrEnum):
    LOCKED = "locked"
    INVALIDATED = "invalidated"


def _required_text(value: str, field: str) -> None:
    if not isinstance(value, str) or not value.strip() or len(value) > 128:
        raise InvalidDataContract(f"{field} must be non-empty bounded text")


def _token(value: str, field: str) -> None:
    if not isinstance(value, str) or not _TOKEN.fullmatch(value):
        raise InvalidDataContract(f"{field} must be a bounded source token")


def _exact_ref(
    reference: TraceabilityRef,
    identifier_type: type[GovernedId],
    field: str,
    *,
    require_fingerprint: bool = False,
) -> None:
    if not isinstance(reference, TraceabilityRef) or not isinstance(
        reference.object_id, identifier_type
    ):
        raise InvalidDataContract(f"{field} requires exact {identifier_type.namespace} reference")
    if require_fingerprint and reference.expected_fingerprint is None:
        raise InvalidDataContract(f"{field} requires an expected fingerprint")


@dataclass(frozen=True, slots=True)
class VenueIdentity:
    venue_id: VenueId
    version: ObjectVersion
    name: str
    venue_type: VenueType
    jurisdiction: str | None
    contract_version: ObjectVersion

    def __post_init__(self) -> None:
        _required_text(self.name, "name")
        if self.jurisdiction is not None:
            _token(self.jurisdiction, "jurisdiction")


@dataclass(frozen=True, slots=True)
class SourceIdentity:
    source_id: SourceId
    version: ObjectVersion
    provider: str
    source_type: SourceType
    feed: str
    source_version: str
    venue_ref: TraceabilityRef | None
    contract_version: ObjectVersion

    def __post_init__(self) -> None:
        _required_text(self.provider, "provider")
        _token(self.feed, "feed")
        _token(self.source_version, "source_version")
        if self.venue_ref is not None:
            _exact_ref(self.venue_ref, VenueId, "venue_ref")


@dataclass(frozen=True, slots=True)
class InstrumentIdentity:
    instrument_id: InstrumentId
    version: ObjectVersion
    symbol: str
    instrument_class: InstrumentClass
    base_asset: str | None
    quote_asset: str | None
    settlement_asset: str | None
    venue_ref: TraceabilityRef | None
    contract_version: ObjectVersion

    def __post_init__(self) -> None:
        _token(self.symbol, "symbol")
        for field, value in (
            ("base_asset", self.base_asset),
            ("quote_asset", self.quote_asset),
            ("settlement_asset", self.settlement_asset),
        ):
            if value is not None:
                _token(value, field)
        if self.venue_ref is not None:
            _exact_ref(self.venue_ref, VenueId, "venue_ref")


@dataclass(frozen=True, slots=True)
class TemporalCoordinates:
    event_time: datetime
    availability_time: datetime
    ingestion_time: datetime
    policy: TemporalPolicy = TemporalPolicy.STRICT_KNOWLEDGE_ORDER

    def __post_init__(self) -> None:
        require_utc(self.event_time, "event_time")
        require_utc(self.availability_time, "availability_time")
        require_utc(self.ingestion_time, "ingestion_time")
        if not self.event_time <= self.availability_time <= self.ingestion_time:
            raise InvalidTemporalOrder(
                "accepted observations require event_time <= availability_time <= ingestion_time"
            )

    @property
    def legitimate_knowledge_time(self) -> datetime:
        return self.availability_time


@dataclass(frozen=True, slots=True)
class DecimalValue:
    """Canonical finite base-10 value; scale differences are intentionally equivalent."""

    text: str

    def __post_init__(self) -> None:
        if not isinstance(self.text, str) or self.text != self._canonicalize(self.text):
            raise InvalidDecimal("decimal text must be finite and canonical")

    @classmethod
    def from_text(cls, text: str) -> DecimalValue:
        if not isinstance(text, str):
            raise InvalidDecimal("decimal input must be text")
        return cls(cls._canonicalize(text))

    @staticmethod
    def _canonicalize(text: str) -> str:
        try:
            value = Decimal(text)
        except (InvalidOperation, ValueError) as exc:
            raise InvalidDecimal("malformed decimal") from exc
        if not value.is_finite():
            raise InvalidDecimal("decimal must be finite")
        if value.is_zero():
            return "0"
        normalized = format(value.normalize(), "f")
        if "." in normalized:
            normalized = normalized.rstrip("0").rstrip(".")
        return normalized


type RawScalar = str | int | bool | DecimalValue | None


@dataclass(frozen=True, slots=True)
class RawField:
    name: str
    value: RawScalar

    def __post_init__(self) -> None:
        if not isinstance(self.name, str) or not _FIELD.fullmatch(self.name):
            raise InvalidDataContract("raw field name is invalid")
        if self.name in _DERIVED_FIELD_PREFIXES or self.name.startswith(
            tuple(f"{prefix}_" for prefix in _DERIVED_FIELD_PREFIXES)
        ):
            raise InvalidDataContract("raw payload cannot contain derived or execution semantics")
        if isinstance(self.value, float) or not (
            self.value is None or isinstance(self.value, (str, int, bool, DecimalValue))
        ):
            raise InvalidDataContract("raw values allow text, integer, boolean, decimal, or null")


@dataclass(frozen=True, slots=True)
class RawObservation:
    observation_id: ObservationId
    version: ObjectVersion
    source_ref: TraceabilityRef
    instrument_ref: TraceabilityRef
    temporal: TemporalCoordinates
    payload: tuple[RawField, ...]
    provenance_ref: TraceabilityRef
    source_sequence: str | None = None
    quality: DataQualityState = DataQualityState.SUSPECT
    reconciliation: ReconciliationDisposition = ReconciliationDisposition.UNRESOLVED
    supersedes: TraceabilityRef | None = None
    contract_version: ObjectVersion = dataclass_field(default_factory=lambda: ObjectVersion(1))

    def __post_init__(self) -> None:
        _exact_ref(self.source_ref, SourceId, "source_ref", require_fingerprint=True)
        _exact_ref(self.instrument_ref, InstrumentId, "instrument_ref", require_fingerprint=True)
        _exact_ref(self.provenance_ref, ProvenanceId, "provenance_ref", require_fingerprint=True)
        if not self.payload:
            raise InvalidDataContract("raw payload cannot be empty")
        names = [field.name for field in self.payload]
        if names != sorted(names) or len(names) != len(set(names)):
            raise InvalidDataContract("raw fields must be unique and sorted")
        if self.source_sequence is not None:
            _token(self.source_sequence, "source_sequence")
        if self.supersedes is not None:
            _exact_ref(self.supersedes, ObservationId, "supersedes", require_fingerprint=True)
            if (
                self.supersedes.object_id == self.observation_id
                and self.supersedes.version == self.version
            ):
                raise InvalidDataContract("observation cannot supersede itself")
        if self.reconciliation is ReconciliationDisposition.CORRECTION and self.supersedes is None:
            raise InvalidDataContract("a correction requires an exact superseded observation")
        if self.quality is DataQualityState.ACCEPTED and self.reconciliation in {
            ReconciliationDisposition.CONFLICT,
            ReconciliationDisposition.UNRESOLVED,
        }:
            raise InvalidDataContract("unresolved/conflicting observations cannot be accepted")


@dataclass(frozen=True, slots=True)
class DatasetManifest:
    dataset_id: DatasetId
    version: ObjectVersion
    created_at: datetime
    observation_refs: tuple[TraceabilityRef, ...]
    source_refs: tuple[TraceabilityRef, ...]
    instrument_refs: tuple[TraceabilityRef, ...]
    event_time_start: datetime
    event_time_end: datetime
    provenance_ref: TraceabilityRef
    contract_version: ObjectVersion
    membership_policy: str = "accepted_only"

    def __post_init__(self) -> None:
        require_utc(self.created_at, "created_at")
        require_utc(self.event_time_start, "event_time_start")
        require_utc(self.event_time_end, "event_time_end")
        if self.event_time_start > self.event_time_end:
            raise InvalidTemporalOrder("manifest event time range is reversed")
        if not self.observation_refs or not self.source_refs or not self.instrument_refs:
            raise InvalidDataContract("manifest membership and scope references are required")
        for field, refs, identifier_type in (
            ("observation_refs", self.observation_refs, ObservationId),
            ("source_refs", self.source_refs, SourceId),
            ("instrument_refs", self.instrument_refs, InstrumentId),
        ):
            for reference in refs:
                _exact_ref(reference, identifier_type, field, require_fingerprint=True)
            keys = [
                (str(reference.object_id), reference.version.number, reference.expected_fingerprint)
                for reference in refs
            ]
            if keys != sorted(keys) or len(keys) != len(set(keys)):
                raise InvalidDataContract(f"{field} must be exact, unique, and sorted")
        _exact_ref(self.provenance_ref, ProvenanceId, "provenance_ref", require_fingerprint=True)
        if self.membership_policy != "accepted_only":
            raise InvalidDataContract("only explicit accepted_only membership is supported")


@dataclass(frozen=True, slots=True)
class DatasetLock:
    lock_id: DatasetLockId
    version: ObjectVersion
    dataset_ref: TraceabilityRef
    manifest_ref: TraceabilityRef
    locked_at: datetime
    temporal_cutoff: datetime
    provenance_ref: TraceabilityRef
    state: DatasetLockState = DatasetLockState.LOCKED
    contract_version: ObjectVersion = dataclass_field(default_factory=lambda: ObjectVersion(1))

    def __post_init__(self) -> None:
        _exact_ref(self.dataset_ref, DatasetId, "dataset_ref", require_fingerprint=True)
        _exact_ref(self.manifest_ref, DatasetId, "manifest_ref", require_fingerprint=True)
        _exact_ref(self.provenance_ref, ProvenanceId, "provenance_ref", require_fingerprint=True)
        require_utc(self.locked_at, "locked_at")
        require_utc(self.temporal_cutoff, "temporal_cutoff")
        if self.temporal_cutoff > self.locked_at:
            raise InvalidTemporalOrder("dataset cutoff cannot be later than lock time")
        if (
            self.dataset_ref.object_id != self.manifest_ref.object_id
            or self.dataset_ref.version != self.manifest_ref.version
        ):
            raise InvalidDataContract("dataset and manifest references must bind the same snapshot")
