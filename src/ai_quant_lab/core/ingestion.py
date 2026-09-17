"""Deterministic bounded ingestion kernel; no acquisition, storage, or execution."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from enum import StrEnum
from typing import Protocol, runtime_checkable

from ai_quant_lab.core.data import (
    DataQualityState,
    DatasetLock,
    DatasetLockId,
    DatasetManifest,
    DecimalValue,
    InstrumentId,
    InstrumentIdentity,
    InvalidDataContract,
    ObservationId,
    RawField,
    RawObservation,
    ReconciliationDisposition,
    SourceId,
    SourceIdentity,
    SourceType,
    TemporalCoordinates,
)
from ai_quant_lab.core.integrity import IntegrityError, fingerprint_record, verify_integrity
from ai_quant_lab.core.model import (
    AgentId,
    ArtifactId,
    AuditEvent,
    AuditEventId,
    AuditResult,
    DatasetId,
    GovernedId,
    ObjectVersion,
    ProvenanceId,
    TraceabilityRef,
    VersionedRef,
    require_utc,
)


class IngestionError(InvalidDataContract):
    """Base class for bounded ingestion failures."""


class AdapterError(IngestionError):
    pass


class ParseError(IngestionError):
    pass


class TemporalGateError(IngestionError):
    pass


class QualityGateError(IngestionError):
    pass


class ReconciliationError(IngestionError):
    pass


class DatasetAssemblyError(IngestionError):
    pass


class CriticalIntegrityFailure(IngestionError):
    pass


class IngestionRequestId(GovernedId):
    namespace = "ingestion-request"


class IngestionSessionId(GovernedId):
    namespace = "ingestion-session"


class RejectionId(GovernedId):
    namespace = "ingestion-rejection"


class IngestionSessionState(StrEnum):
    STARTED = "started"
    COMPLETED = "completed"
    FAILED = "failed"


class IngestionSourceBoundary(StrEnum):
    SYNTHETIC_ONLY = "synthetic_only"
    CONTROLLED_FILE_SNAPSHOT = "controlled_file_snapshot"


class CandidateValueKind(StrEnum):
    TEXT = "text"
    INTEGER = "integer"
    BOOLEAN = "boolean"
    DECIMAL = "decimal"
    NULL = "null"


class RejectionStage(StrEnum):
    PARSE = "parse"
    TEMPORAL_GATE = "temporal_gate"
    QUALITY_GATE = "quality_gate"


class RejectionReason(StrEnum):
    INVALID_CANDIDATE = "invalid_candidate"
    INVALID_TIMESTAMP = "invalid_timestamp"
    INVALID_TEMPORAL_ORDER = "invalid_temporal_order"
    INVALID_NUMERIC = "invalid_numeric"
    PROHIBITED_FIELD = "prohibited_field"


class SessionResultStatus(StrEnum):
    COMPLETED = "completed"


@dataclass(frozen=True, slots=True)
class CandidateField:
    name: str
    kind: CandidateValueKind
    value: str | int | bool | None

    def __post_init__(self) -> None:
        if not isinstance(self.name, str) or not self.name:
            raise ParseError("candidate field name is required")
        if isinstance(self.value, float):
            raise ParseError("binary float is prohibited")
        valid = (
            (self.kind is CandidateValueKind.NULL and self.value is None)
            or (self.kind is CandidateValueKind.TEXT and isinstance(self.value, str))
            or (
                self.kind is CandidateValueKind.INTEGER
                and isinstance(self.value, int)
                and not isinstance(self.value, bool)
            )
            or (self.kind is CandidateValueKind.BOOLEAN and isinstance(self.value, bool))
            or (self.kind is CandidateValueKind.DECIMAL and isinstance(self.value, str))
        )
        if not valid:
            raise ParseError("candidate value does not match its explicit kind")


@dataclass(frozen=True, slots=True)
class CandidateObservation:
    """Pre-acceptance record. Parsing success cannot grant ACCEPTED quality."""

    observation_id: ObservationId
    version: ObjectVersion
    source_ref: TraceabilityRef
    instrument_ref: TraceabilityRef
    event_time: str
    availability_time: str
    ingestion_time: str | None
    fields: tuple[CandidateField, ...]
    source_sequence: str | None = None
    correction_of: TraceabilityRef | None = None
    quarantine_reason: str | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.observation_id, ObservationId):
            raise ParseError("candidate requires ObservationId")
        if not isinstance(self.version, ObjectVersion):
            raise ParseError("candidate requires ObjectVersion")
        if not self.fields:
            raise ParseError("candidate fields are required")
        if self.quarantine_reason is not None and not self.quarantine_reason.strip():
            raise ParseError("quarantine reason cannot be blank")


@dataclass(frozen=True, slots=True)
class IngestionRequest:
    request_id: IngestionRequestId
    version: ObjectVersion
    adapter_ref: TraceabilityRef
    source_ref: TraceabilityRef
    instrument_ref: TraceabilityRef
    observation_provenance_ref: TraceabilityRef
    manifest_provenance_ref: TraceabilityRef
    lock_provenance_ref: TraceabilityRef
    dataset_id: DatasetId
    dataset_version: ObjectVersion
    lock_id: DatasetLockId
    lock_version: ObjectVersion
    dataset_cutoff: datetime
    actor_id: AgentId
    expected_contract_version: ObjectVersion
    source_boundary: IngestionSourceBoundary = IngestionSourceBoundary.SYNTHETIC_ONLY

    def __post_init__(self) -> None:
        _require_ref(self.adapter_ref, ArtifactId, "adapter_ref")
        _require_ref(self.source_ref, SourceId, "source_ref")
        _require_ref(self.instrument_ref, InstrumentId, "instrument_ref")
        _require_ref(self.observation_provenance_ref, ProvenanceId, "observation_provenance_ref")
        _require_ref(self.manifest_provenance_ref, ProvenanceId, "manifest_provenance_ref")
        _require_ref(self.lock_provenance_ref, ProvenanceId, "lock_provenance_ref")
        require_utc(self.dataset_cutoff, "dataset_cutoff")
        if self.expected_contract_version != ObjectVersion(1):
            raise CriticalIntegrityFailure("unsupported data contract version")
        if not isinstance(self.source_boundary, IngestionSourceBoundary):
            raise CriticalIntegrityFailure("explicit ingestion source boundary is required")


@dataclass(frozen=True, slots=True)
class IngestionSession:
    session_id: IngestionSessionId
    version: ObjectVersion
    request_ref: VersionedRef
    started_at: datetime
    state: IngestionSessionState = IngestionSessionState.STARTED

    def __post_init__(self) -> None:
        require_utc(self.started_at, "started_at")
        if not isinstance(self.request_ref.object_id, IngestionRequestId):
            raise IngestionError("session requires exact ingestion request reference")


@dataclass(frozen=True, slots=True)
class RejectionRecord:
    rejection_id: RejectionId
    candidate_id: ObservationId
    candidate_version: ObjectVersion
    session_ref: VersionedRef
    stage: RejectionStage
    reason: RejectionReason
    recorded_at: datetime

    def __post_init__(self) -> None:
        require_utc(self.recorded_at, "recorded_at")
        if not isinstance(self.session_ref.object_id, IngestionSessionId):
            raise IngestionError("rejection requires exact ingestion session reference")


@dataclass(frozen=True, slots=True)
class ReconciliationRecord:
    observation_ref: TraceabilityRef
    disposition: ReconciliationDisposition
    related_refs: tuple[TraceabilityRef, ...] = ()


@dataclass(frozen=True, slots=True)
class IngestionResult:
    request_ref: VersionedRef
    session: IngestionSession
    accepted_observations: tuple[RawObservation, ...]
    quarantined_observations: tuple[RawObservation, ...]
    superseded_observations: tuple[RawObservation, ...]
    rejected: tuple[RejectionRecord, ...]
    reconciliation: tuple[ReconciliationRecord, ...]
    manifest: DatasetManifest
    dataset_lock: DatasetLock
    audit_events: tuple[AuditEvent, ...]
    status: SessionResultStatus = SessionResultStatus.COMPLETED

    @property
    def accepted_refs(self) -> tuple[TraceabilityRef, ...]:
        return tuple(_record_ref(item) for item in self.accepted_observations)

    @property
    def quarantined_refs(self) -> tuple[TraceabilityRef, ...]:
        return tuple(_record_ref(item) for item in self.quarantined_observations)

    @property
    def accepted_count(self) -> int:
        return len(self.accepted_observations)

    @property
    def quarantined_count(self) -> int:
        return len(self.quarantined_observations)

    @property
    def rejected_count(self) -> int:
        return len(self.rejected)


@runtime_checkable
class InputAdapter(Protocol):
    @property
    def adapter_ref(self) -> TraceabilityRef: ...

    def read(self) -> tuple[CandidateObservation, ...]: ...


@dataclass(frozen=True, slots=True)
class SyntheticInputAdapter:
    """Deterministic in-memory adapter, explicitly synthetic and authority-free."""

    adapter_ref: TraceabilityRef
    candidates: tuple[CandidateObservation, ...]

    def __post_init__(self) -> None:
        _require_ref(self.adapter_ref, ArtifactId, "adapter_ref")

    def read(self) -> tuple[CandidateObservation, ...]:
        return self.candidates


@runtime_checkable
class Clock(Protocol):
    def now(self) -> datetime: ...


@dataclass(frozen=True, slots=True)
class DeterministicClock:
    instant: datetime

    def __post_init__(self) -> None:
        require_utc(self.instant, "clock instant")

    def now(self) -> datetime:
        return self.instant


@dataclass(frozen=True, slots=True)
class _ParsedCandidate:
    candidate: CandidateObservation
    temporal: TemporalCoordinates
    fields: tuple[RawField, ...]


def _require_ref(
    reference: TraceabilityRef,
    identifier_type: type[GovernedId],
    field: str,
) -> None:
    if not isinstance(reference, TraceabilityRef) or not isinstance(
        reference.object_id, identifier_type
    ):
        raise CriticalIntegrityFailure(f"{field} has wrong governed identity")
    if reference.expected_fingerprint is None:
        raise CriticalIntegrityFailure(f"{field} requires exact fingerprint")


def _record_ref(record: RawObservation) -> TraceabilityRef:
    return TraceabilityRef(record.observation_id, record.version, fingerprint_record(record))


def _parse_timestamp(value: str | None, field: str, fallback: datetime | None = None) -> datetime:
    if value is None:
        if fallback is None:
            raise ParseError(f"{field} is required")
        return fallback
    if not isinstance(value, str):
        raise ParseError(f"{field} must be canonical timestamp text")
    try:
        parsed = datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%fZ").replace(tzinfo=UTC)
    except ValueError as exc:
        raise ParseError(f"{field} is invalid") from exc
    return parsed


def _parse_field(field: CandidateField) -> RawField:
    try:
        if field.kind is CandidateValueKind.DECIMAL:
            assert isinstance(field.value, str)
            value: str | int | bool | DecimalValue | None = DecimalValue.from_text(field.value)
        else:
            value = field.value
        return RawField(field.name, value)
    except InvalidDataContract as exc:
        if field.kind is CandidateValueKind.DECIMAL:
            raise ParseError("invalid decimal value") from exc
        raise QualityGateError("field violates raw-data boundary") from exc


def _parse_candidate(
    candidate: CandidateObservation,
    request: IngestionRequest,
    clock: Clock,
) -> _ParsedCandidate:
    if candidate.source_ref != request.source_ref:
        raise CriticalIntegrityFailure("candidate source binding mismatch")
    if candidate.instrument_ref != request.instrument_ref:
        raise CriticalIntegrityFailure("candidate instrument binding mismatch")
    try:
        temporal = TemporalCoordinates(
            _parse_timestamp(candidate.event_time, "event_time"),
            _parse_timestamp(candidate.availability_time, "availability_time"),
            _parse_timestamp(candidate.ingestion_time, "ingestion_time", clock.now()),
        )
    except ParseError:
        raise
    except InvalidDataContract as exc:
        raise TemporalGateError("candidate violates temporal acceptance policy") from exc
    if temporal.legitimate_knowledge_time > request.dataset_cutoff:
        raise TemporalGateError("candidate availability exceeds exact dataset cutoff")
    fields = tuple(
        sorted((_parse_field(field) for field in candidate.fields), key=lambda x: x.name)
    )
    return _ParsedCandidate(candidate, temporal, fields)


def _event_key(item: _ParsedCandidate) -> tuple[str, str, datetime, str]:
    candidate = item.candidate
    return (
        str(candidate.source_ref.object_id),
        str(candidate.instrument_ref.object_id),
        item.temporal.event_time,
        candidate.source_sequence or "",
    )


def _content_key(item: _ParsedCandidate) -> tuple[tuple[str, str], ...]:
    values: list[tuple[str, str]] = []
    for field in item.fields:
        value = field.value
        if isinstance(value, DecimalValue):
            encoded = f"decimal:{value.text}"
        else:
            encoded = f"{type(value).__name__}:{value!s}"
        values.append((field.name, encoded))
    return tuple(values)


def _make_observation(
    item: _ParsedCandidate,
    request: IngestionRequest,
    quality: DataQualityState,
    disposition: ReconciliationDisposition,
) -> RawObservation:
    return RawObservation(
        item.candidate.observation_id,
        item.candidate.version,
        request.source_ref,
        request.instrument_ref,
        item.temporal,
        item.fields,
        request.observation_provenance_ref,
        item.candidate.source_sequence,
        quality,
        disposition,
        item.candidate.correction_of,
        request.expected_contract_version,
    )


def _safe_rejection(
    candidate: CandidateObservation,
    session: IngestionSession,
    index: int,
    stage: RejectionStage,
    reason: RejectionReason,
    clock: Clock,
) -> RejectionRecord:
    return RejectionRecord(
        RejectionId(f"{session.session_id.value[:35]}-{index:04d}"),
        candidate.observation_id,
        candidate.version,
        VersionedRef(session.session_id, session.version),
        stage,
        reason,
        clock.now(),
    )


def _audit(
    session: IngestionSession,
    actor: AgentId,
    index: int,
    action: str,
    target: VersionedRef,
    result: AuditResult,
    clock: Clock,
) -> AuditEvent:
    return AuditEvent(
        AuditEventId(f"{session.session_id.value[:35]}-{index:04d}"),
        actor,
        action,
        target,
        clock.now(),
        result,
    )


class IngestionKernel:
    """Synchronous bounded kernel. It owns no source, quality, or execution authority."""

    def ingest(
        self,
        request: IngestionRequest,
        session: IngestionSession,
        adapter: InputAdapter,
        source: SourceIdentity,
        instrument: InstrumentIdentity,
        clock: Clock,
        *,
        prior_observations: tuple[RawObservation, ...] = (),
    ) -> IngestionResult:
        self._validate_session(request, session, adapter, source, instrument, clock)
        parsed: list[_ParsedCandidate] = []
        rejected: list[RejectionRecord] = []
        audits: list[AuditEvent] = [
            _audit(
                session,
                request.actor_id,
                0,
                "ingestion.started",
                VersionedRef(session.session_id, session.version),
                AuditResult.RECORDED,
                clock,
            )
        ]
        for index, candidate in enumerate(adapter.read(), start=1):
            if not isinstance(candidate, CandidateObservation):
                raise CriticalIntegrityFailure("adapter emitted unsupported candidate type")
            try:
                parsed.append(_parse_candidate(candidate, request, clock))
            except CriticalIntegrityFailure:
                raise
            except TemporalGateError:
                rejected.append(
                    _safe_rejection(
                        candidate,
                        session,
                        index,
                        RejectionStage.TEMPORAL_GATE,
                        RejectionReason.INVALID_TEMPORAL_ORDER,
                        clock,
                    )
                )
            except ParseError as exc:
                reason = (
                    RejectionReason.INVALID_NUMERIC
                    if "decimal" in str(exc)
                    else RejectionReason.INVALID_TIMESTAMP
                )
                rejected.append(
                    _safe_rejection(candidate, session, index, RejectionStage.PARSE, reason, clock)
                )
            except QualityGateError:
                rejected.append(
                    _safe_rejection(
                        candidate,
                        session,
                        index,
                        RejectionStage.QUALITY_GATE,
                        RejectionReason.PROHIBITED_FIELD,
                        clock,
                    )
                )

        identities = [(item.candidate.observation_id, item.candidate.version) for item in parsed]
        if len(identities) != len(set(identities)):
            raise CriticalIntegrityFailure(
                "one session cannot reuse an observation identity/version"
            )
        accepted, quarantined, superseded, reconciled = self._reconcile(
            request, parsed, prior_observations
        )
        if not accepted:
            raise DatasetAssemblyError("accepted_only assembly requires at least one observation")

        try:
            manifest = self._assemble_manifest(request, accepted, clock)
            manifest_fingerprint = fingerprint_record(manifest)
            dataset_ref = TraceabilityRef(
                manifest.dataset_id, manifest.version, manifest_fingerprint
            )
            lock = DatasetLock(
                request.lock_id,
                request.lock_version,
                dataset_ref,
                dataset_ref,
                clock.now(),
                request.dataset_cutoff,
                request.lock_provenance_ref,
            )
            verify_integrity(manifest, manifest_fingerprint)
        except (InvalidDataContract, IntegrityError) as exc:
            raise CriticalIntegrityFailure(
                "manifest/lock construction failed integrity gates"
            ) from exc
        for item in accepted:
            audits.append(
                _audit(
                    session,
                    request.actor_id,
                    len(audits),
                    "observation.accepted",
                    VersionedRef(item.observation_id, item.version),
                    AuditResult.ACCEPTED,
                    clock,
                )
            )
        for item in quarantined:
            audits.append(
                _audit(
                    session,
                    request.actor_id,
                    len(audits),
                    "observation.quarantined",
                    VersionedRef(item.observation_id, item.version),
                    AuditResult.RECORDED,
                    clock,
                )
            )
        for predecessor in superseded:
            audits.append(
                _audit(
                    session,
                    request.actor_id,
                    len(audits),
                    "observation.superseded_by_correction",
                    VersionedRef(predecessor.observation_id, predecessor.version),
                    AuditResult.RECORDED,
                    clock,
                )
            )
        for rejection in rejected:
            audits.append(
                _audit(
                    session,
                    request.actor_id,
                    len(audits),
                    "candidate.rejected",
                    VersionedRef(rejection.rejection_id, ObjectVersion(1)),
                    AuditResult.REJECTED,
                    clock,
                )
            )
        audits.extend(
            (
                _audit(
                    session,
                    request.actor_id,
                    len(audits),
                    "dataset.manifest_created",
                    VersionedRef(manifest.dataset_id, manifest.version),
                    AuditResult.RECORDED,
                    clock,
                ),
                _audit(
                    session,
                    request.actor_id,
                    len(audits) + 1,
                    "dataset.locked",
                    VersionedRef(lock.lock_id, lock.version),
                    AuditResult.RECORDED,
                    clock,
                ),
            )
        )
        audits.append(
            _audit(
                session,
                request.actor_id,
                len(audits),
                "ingestion.completed",
                VersionedRef(session.session_id, session.version),
                AuditResult.ACCEPTED,
                clock,
            )
        )
        completed = IngestionSession(
            session.session_id,
            session.version,
            session.request_ref,
            session.started_at,
            IngestionSessionState.COMPLETED,
        )
        return IngestionResult(
            VersionedRef(request.request_id, request.version),
            completed,
            tuple(accepted),
            tuple(quarantined),
            tuple(superseded),
            tuple(rejected),
            tuple(reconciled),
            manifest,
            lock,
            tuple(audits),
        )

    @staticmethod
    def _validate_session(
        request: IngestionRequest,
        session: IngestionSession,
        adapter: InputAdapter,
        source: SourceIdentity,
        instrument: InstrumentIdentity,
        clock: Clock,
    ) -> None:
        require_utc(clock.now(), "clock now")
        if session.request_ref != VersionedRef(request.request_id, request.version):
            raise CriticalIntegrityFailure("session/request mismatch")
        if session.state is not IngestionSessionState.STARTED:
            raise CriticalIntegrityFailure("session is not in STARTED state")
        if adapter.adapter_ref != request.adapter_ref:
            raise CriticalIntegrityFailure("adapter binding mismatch")
        if source.source_type is SourceType.SYNTHETIC_FIXTURE:
            if request.source_boundary is not IngestionSourceBoundary.SYNTHETIC_ONLY:
                raise AdapterError("synthetic source requires synthetic-only boundary")
        elif not (
            source.source_type is SourceType.FILE_SNAPSHOT
            and request.source_boundary is IngestionSourceBoundary.CONTROLLED_FILE_SNAPSHOT
        ):
            raise AdapterError("source type is outside the explicit ingestion boundary")
        try:
            verify_integrity(source, request.source_ref.expected_fingerprint or "")
            verify_integrity(instrument, request.instrument_ref.expected_fingerprint or "")
        except IntegrityError as exc:
            raise CriticalIntegrityFailure("source or instrument integrity failure") from exc
        if (
            request.source_ref.object_id != source.source_id
            or request.source_ref.version != source.version
        ):
            raise CriticalIntegrityFailure("source definition mismatch")
        if (
            request.instrument_ref.object_id != instrument.instrument_id
            or request.instrument_ref.version != instrument.version
        ):
            raise CriticalIntegrityFailure("instrument definition mismatch")

    @staticmethod
    def _reconcile(
        request: IngestionRequest,
        parsed: list[_ParsedCandidate],
        prior: tuple[RawObservation, ...],
    ) -> tuple[
        list[RawObservation],
        list[RawObservation],
        list[RawObservation],
        list[ReconciliationRecord],
    ]:
        accepted: list[RawObservation] = []
        quarantined: list[RawObservation] = []
        superseded: list[RawObservation] = []
        records: list[ReconciliationRecord] = []
        prior_by_ref = {_record_ref(item): item for item in prior}
        prior_by_identity = {(item.observation_id, item.version): item for item in prior}
        corrections: list[_ParsedCandidate] = []
        normal: list[_ParsedCandidate] = []
        for item in parsed:
            if item.candidate.quarantine_reason is not None:
                record = _make_observation(
                    item,
                    request,
                    DataQualityState.QUARANTINED,
                    ReconciliationDisposition.UNRESOLVED,
                )
                quarantined.append(record)
                records.append(
                    ReconciliationRecord(_record_ref(record), ReconciliationDisposition.UNRESOLVED)
                )
            elif item.candidate.correction_of is not None:
                corrections.append(item)
            else:
                normal.append(item)

        groups: dict[tuple[str, str, datetime, str], list[_ParsedCandidate]] = {}
        for item in normal:
            groups.setdefault(_event_key(item), []).append(item)
        for group in groups.values():
            group.sort(key=lambda item: str(item.candidate.observation_id))
            content = {_content_key(item) for item in group}
            temporal = {
                (
                    item.temporal.event_time,
                    item.temporal.availability_time,
                    item.temporal.ingestion_time,
                )
                for item in group
            }
            if len(content) > 1:
                related = tuple(
                    TraceabilityRef(item.candidate.observation_id, item.candidate.version, None)
                    for item in group
                )
                for item in group:
                    record = _make_observation(
                        item,
                        request,
                        DataQualityState.QUARANTINED,
                        ReconciliationDisposition.CONFLICT,
                    )
                    quarantined.append(record)
                    records.append(
                        ReconciliationRecord(
                            _record_ref(record),
                            ReconciliationDisposition.CONFLICT,
                            related,
                        )
                    )
                continue
            winner = _make_observation(
                group[0],
                request,
                DataQualityState.ACCEPTED,
                ReconciliationDisposition.UNIQUE,
            )
            accepted.append(winner)
            records.append(
                ReconciliationRecord(_record_ref(winner), ReconciliationDisposition.UNIQUE)
            )
            duplicate_disposition = (
                ReconciliationDisposition.BYTE_IDENTICAL_DUPLICATE
                if len(temporal) == 1
                else ReconciliationDisposition.RETRANSMISSION
            )
            for item in group[1:]:
                duplicate = _make_observation(
                    item, request, DataQualityState.QUARANTINED, duplicate_disposition
                )
                quarantined.append(duplicate)
                records.append(
                    ReconciliationRecord(
                        _record_ref(duplicate),
                        duplicate_disposition,
                        (_record_ref(winner),),
                    )
                )

        accepted_refs = {(item.observation_id, item.version): item for item in accepted}
        for item in sorted(corrections, key=lambda value: str(value.candidate.observation_id)):
            correction_of = item.candidate.correction_of
            assert correction_of is not None
            prior_record = prior_by_ref.get(correction_of)
            if not isinstance(correction_of.object_id, ObservationId):
                raise CriticalIntegrityFailure("correction reference requires ObservationId")
            batch_key = (correction_of.object_id, correction_of.version)
            batch_record = accepted_refs.get(batch_key)
            if batch_key in prior_by_identity and prior_record is None:
                raise CriticalIntegrityFailure("correction target fingerprint mismatch")
            target = prior_record or batch_record
            if target is None:
                raise ReconciliationError("correction target is not an exact known observation")
            if (
                target.source_ref != request.source_ref
                or target.instrument_ref != request.instrument_ref
            ):
                raise CriticalIntegrityFailure(
                    "correction target belongs to a different source/instrument"
                )
            if target.quality is not DataQualityState.ACCEPTED:
                raise ReconciliationError(
                    "non-accepted predecessor cannot be corrected into acceptance"
                )
            if correction_of.expected_fingerprint != fingerprint_record(target):
                raise CriticalIntegrityFailure("correction target fingerprint mismatch")
            correction = _make_observation(
                item,
                request,
                DataQualityState.ACCEPTED,
                ReconciliationDisposition.CORRECTION,
            )
            if batch_record is not None:
                accepted.remove(batch_record)
                superseded.append(batch_record)
            accepted.append(correction)
            accepted_refs[(correction.observation_id, correction.version)] = correction
            records.append(
                ReconciliationRecord(
                    _record_ref(correction),
                    ReconciliationDisposition.CORRECTION,
                    (correction_of,),
                )
            )

        accepted.sort(key=lambda item: (item.temporal.event_time, str(item.observation_id)))
        quarantined.sort(key=lambda item: str(item.observation_id))
        records.sort(key=lambda item: str(item.observation_ref.object_id))
        superseded.sort(key=lambda item: str(item.observation_id))
        return accepted, quarantined, superseded, records

    @staticmethod
    def _assemble_manifest(
        request: IngestionRequest,
        observations: list[RawObservation],
        clock: Clock,
    ) -> DatasetManifest:
        if any(item.quality is not DataQualityState.ACCEPTED for item in observations):
            raise DatasetAssemblyError("accepted_only membership cannot contain quarantine")
        refs = tuple(
            sorted(
                (_record_ref(item) for item in observations),
                key=lambda item: (
                    str(item.object_id),
                    item.version.number,
                    item.expected_fingerprint or "",
                ),
            )
        )
        return DatasetManifest(
            request.dataset_id,
            request.dataset_version,
            clock.now(),
            refs,
            (request.source_ref,),
            (request.instrument_ref,),
            min(item.temporal.event_time for item in observations),
            max(item.temporal.event_time for item in observations),
            request.manifest_provenance_ref,
            request.expected_contract_version,
        )
