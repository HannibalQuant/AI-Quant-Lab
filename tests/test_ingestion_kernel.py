"""Bounded synthetic ingestion integration, deterministic replay, and failure tests."""

from __future__ import annotations

from dataclasses import FrozenInstanceError, replace
from datetime import UTC, datetime, timedelta

import pytest

from ai_quant_lab.core.data import (
    DataQualityState,
    DatasetLockId,
    InstrumentClass,
    InstrumentId,
    InstrumentIdentity,
    ObservationId,
    ReconciliationDisposition,
    SourceId,
    SourceIdentity,
    SourceType,
)
from ai_quant_lab.core.ingestion import (
    CandidateField,
    CandidateObservation,
    CandidateValueKind,
    CriticalIntegrityFailure,
    DatasetAssemblyError,
    DeterministicClock,
    IngestionKernel,
    IngestionRequest,
    IngestionRequestId,
    IngestionSession,
    IngestionSessionId,
    ParseError,
    ReconciliationError,
    RejectionReason,
    SyntheticInputAdapter,
)
from ai_quant_lab.core.integrity import IntegrityError, fingerprint_record, verify_integrity
from ai_quant_lab.core.model import (
    AgentId,
    ArtifactId,
    DatasetId,
    ExecutionState,
    ObjectVersion,
    ProvenanceId,
    TraceabilityRef,
    VersionedRef,
)

V1 = ObjectVersion(1)
T0 = datetime(2025, 1, 1, tzinfo=UTC)
T1 = T0 + timedelta(minutes=2)
T2 = T0 + timedelta(minutes=5)
T3 = T0 + timedelta(minutes=10)
PLACEHOLDER = "sha256:" + "a" * 64


def stamp(value: datetime) -> str:
    return value.isoformat(timespec="microseconds").replace("+00:00", "Z")


def context(
    candidates: tuple[CandidateObservation, ...] = (),
    *,
    session_id: str = "run-one",
) -> tuple[
    IngestionRequest,
    IngestionSession,
    SyntheticInputAdapter,
    SourceIdentity,
    InstrumentIdentity,
    DeterministicClock,
]:
    source = SourceIdentity(
        SourceId("synthetic-source"), V1, "Synthetic Lab", SourceType.SYNTHETIC_FIXTURE,
        "synthetic-feed", "fixture-v1", None, V1,
    )
    instrument = InstrumentIdentity(
        InstrumentId("synthetic-instrument"), V1, "TESTUSD", InstrumentClass.SPOT,
        "TEST", "USD", None, None, V1,
    )
    source_ref = TraceabilityRef(source.source_id, V1, fingerprint_record(source))
    instrument_ref = TraceabilityRef(
        instrument.instrument_id, V1, fingerprint_record(instrument)
    )
    adapter_ref = TraceabilityRef(ArtifactId("synthetic-adapter"), V1, PLACEHOLDER)
    request = IngestionRequest(
        IngestionRequestId("request-one"), V1, adapter_ref, source_ref, instrument_ref,
        TraceabilityRef(ProvenanceId("observation-input"), V1, PLACEHOLDER),
        TraceabilityRef(ProvenanceId("manifest-input"), V1, PLACEHOLDER),
        TraceabilityRef(ProvenanceId("lock-input"), V1, PLACEHOLDER),
        DatasetId("synthetic-dataset"), V1, DatasetLockId("synthetic-lock"), V1,
        T2, AgentId("synthetic-producer"), V1,
    )
    session = IngestionSession(
        IngestionSessionId(session_id), V1,
        VersionedRef(request.request_id, request.version), T2,
    )
    return (
        request, session, SyntheticInputAdapter(adapter_ref, candidates),
        source, instrument, DeterministicClock(T3),
    )


def candidate(
    name: str = "observation-one",
    *,
    event: datetime = T0,
    available: datetime = T1,
    ingested: datetime | None = T2,
    price: str = "1.00",
    correction_of: TraceabilityRef | None = None,
    quarantine_reason: str | None = None,
    sequence: str | None = "seq-one",
) -> CandidateObservation:
    request, _, _, _, _, _ = context()
    return CandidateObservation(
        ObservationId(name), V1, request.source_ref, request.instrument_ref,
        stamp(event), stamp(available), None if ingested is None else stamp(ingested),
        (CandidateField("price", CandidateValueKind.DECIMAL, price),),
        sequence, correction_of, quarantine_reason,
    )


def ingest(
    candidates: tuple[CandidateObservation, ...],
    *,
    session_id: str = "run-one",
    prior: tuple = (),
):
    request, session, _, source, instrument, clock = context(
        candidates, session_id=session_id
    )
    adapter = SyntheticInputAdapter(request.adapter_ref, candidates)
    return IngestionKernel().ingest(
        request, session, adapter, source, instrument, clock, prior_observations=prior
    )


def test_clean_end_to_end_integrity_and_knowledge_time() -> None:
    result = ingest((candidate(),))
    assert result.accepted_count == 1
    assert result.quarantined_count == result.rejected_count == 0
    observation = result.accepted_observations[0]
    assert observation.temporal.event_time == T0
    assert observation.temporal.legitimate_knowledge_time == T1
    assert observation.temporal.ingestion_time == T2
    assert observation.quality is DataQualityState.ACCEPTED
    assert result.manifest.observation_refs == result.accepted_refs
    assert result.dataset_lock.manifest_ref.expected_fingerprint == fingerprint_record(
        result.manifest
    )
    for governed in (observation, result.manifest, result.dataset_lock):
        verify_integrity(governed, fingerprint_record(governed))
    assert result.session.session_id == IngestionSessionId("run-one")
    assert result.audit_events[-1].action == "ingestion.completed"


def test_explicit_delayed_ingestion_and_injected_clock() -> None:
    delayed = ingest((candidate(ingested=T3),))
    injected = ingest((candidate(ingested=None),))
    assert delayed.accepted_observations[0].temporal.ingestion_time == T3
    assert injected.accepted_observations[0].temporal.ingestion_time == T3
    assert injected.accepted_observations[0].temporal.availability_time == T1


def test_mixed_record_failures_do_not_leak_into_dataset() -> None:
    valid = candidate()
    invalid = candidate("invalid-time", event=T2, available=T1)
    numeric = candidate("invalid-decimal", event=T1, available=T2, ingested=T3, price="NaN")
    result = ingest((valid, invalid, numeric))
    assert result.accepted_count == 1
    assert result.rejected_count == 2
    assert {record.reason for record in result.rejected} == {
        RejectionReason.INVALID_TEMPORAL_ORDER, RejectionReason.INVALID_NUMERIC
    }
    assert len(result.manifest.observation_refs) == 1
    assert all(
        reference.object_id != ObservationId("invalid-time")
        for reference in result.manifest.observation_refs
    )


def test_conflict_has_no_silent_winner_even_if_arrival_reverses() -> None:
    first = candidate("conflict-one", price="1")
    second = candidate("conflict-two", price="2")
    unique = candidate("unique-two", event=T1, available=T2, ingested=T3, sequence="seq-two")
    a = ingest((first, second, unique))
    b = ingest((unique, second, first))
    assert a.accepted_count == b.accepted_count == 1
    assert a.quarantined_count == b.quarantined_count == 2
    assert all(
        item.reconciliation is ReconciliationDisposition.CONFLICT
        for item in a.quarantined_observations
    )
    assert fingerprint_record(a.manifest) == fingerprint_record(b.manifest)


def test_byte_duplicate_and_retransmission_are_explicit() -> None:
    a = candidate("a-one")
    b = candidate("b-two")
    duplicate = ingest((b, a))
    assert duplicate.accepted_count == duplicate.quarantined_count == 1
    assert duplicate.quarantined_observations[0].reconciliation is (
        ReconciliationDisposition.BYTE_IDENTICAL_DUPLICATE
    )
    retransmit = ingest((a, candidate("b-two", ingested=T3)))
    assert retransmit.quarantined_observations[0].reconciliation is (
        ReconciliationDisposition.RETRANSMISSION
    )


def test_explicit_quarantine_excluded_from_accepted_only_membership() -> None:
    result = ingest((
        candidate(),
        candidate(
            "suspect", event=T1, available=T2, ingested=T3,
            sequence="seq-two", quarantine_reason="structural review",
        ),
    ))
    assert result.quarantined_count == 1
    assert result.quarantined_refs[0] not in result.manifest.observation_refs
    assert result.quarantined_observations[0].quality is DataQualityState.QUARANTINED


def test_correction_preserves_predecessor_and_changes_membership() -> None:
    original = ingest((candidate(),)).accepted_observations[0]
    prior_ref = TraceabilityRef(original.observation_id, original.version, fingerprint_record(original))
    correction = candidate(
        "observation-corrected", price="1.1", correction_of=prior_ref
    )
    result = ingest((candidate(), correction))
    assert result.accepted_count == 1
    assert len(result.superseded_observations) == 1
    assert result.superseded_observations[0] == original
    assert result.accepted_observations[0].supersedes == prior_ref
    assert result.accepted_observations[0].reconciliation is ReconciliationDisposition.CORRECTION
    assert prior_ref not in result.manifest.observation_refs
    with pytest.raises(FrozenInstanceError):
        original.quality = DataQualityState.INVALIDATED  # type: ignore[misc]


def test_unknown_or_self_correction_fails_closed() -> None:
    unknown = TraceabilityRef(ObservationId("missing"), V1, PLACEHOLDER)
    with pytest.raises(ReconciliationError):
        ingest((candidate(), candidate("correction", correction_of=unknown)))
    self_ref = TraceabilityRef(ObservationId("correction"), V1, PLACEHOLDER)
    with pytest.raises(ReconciliationError):
        ingest((candidate(), candidate("correction", correction_of=self_ref)))


def test_all_records_rejected_fails_without_valid_research_lock() -> None:
    with pytest.raises(DatasetAssemblyError):
        ingest((candidate(event=T2, available=T1),))


def test_replay_session_identity_is_separate_from_dataset_content() -> None:
    inputs = (
        candidate(),
        candidate("second", event=T1, available=T2, ingested=T3, sequence="seq-two"),
    )
    first = ingest(inputs)
    again = ingest(tuple(reversed(inputs)), session_id="run-two")
    assert first.session.session_id != again.session.session_id
    assert first.audit_events != again.audit_events
    assert tuple(fingerprint_record(x) for x in first.accepted_observations) == tuple(
        fingerprint_record(x) for x in again.accepted_observations
    )
    assert fingerprint_record(first.manifest) == fingerprint_record(again.manifest)
    assert fingerprint_record(first.dataset_lock) == fingerprint_record(again.dataset_lock)


def test_source_instrument_and_adapter_integrity_fail_session() -> None:
    request, session, adapter, source, instrument, clock = context((candidate(),))
    kernel = IngestionKernel()
    with pytest.raises(CriticalIntegrityFailure):
        kernel.ingest(replace(request, source_ref=TraceabilityRef(
            source.source_id, V1, PLACEHOLDER,
        )), session, adapter, source, instrument, clock)
    with pytest.raises(CriticalIntegrityFailure):
        kernel.ingest(request, session, SyntheticInputAdapter(
            TraceabilityRef(ArtifactId("other-adapter"), V1, PLACEHOLDER), (candidate(),)
        ), source, instrument, clock)
    with pytest.raises(CriticalIntegrityFailure):
        kernel.ingest(request, session, adapter, source, replace(
            instrument, version=ObjectVersion(2),
        ), clock)


def test_candidate_mismatch_float_and_execution_field_rejected() -> None:
    request, session, _, source, instrument, clock = context()
    mismatched = replace(
        candidate(), source_ref=TraceabilityRef(SourceId("other-source"), V1, PLACEHOLDER)
    )
    with pytest.raises(CriticalIntegrityFailure):
        IngestionKernel().ingest(
            request, session, SyntheticInputAdapter(request.adapter_ref, (mismatched,)),
            source, instrument, clock,
        )
    with pytest.raises(ParseError):
        CandidateField("price", CandidateValueKind.DECIMAL, 1.0)  # type: ignore[arg-type]
    with pytest.raises(ParseError):
        CandidateField("price", CandidateValueKind.DECIMAL, "Infinity")
        # Numeric validity is enforced at the parsing boundary, not candidate construction.
        ingest((candidate(price="Infinity"),))
    prohibited = replace(
        candidate("bad-signal", event=T1, available=T2, ingested=T3, sequence="seq-two"),
        fields=(CandidateField("signal_buy", CandidateValueKind.TEXT, "buy"),),
    )
    result = ingest((candidate(), prohibited))
    assert result.rejected[0].reason is RejectionReason.PROHIBITED_FIELD
    assert result.accepted_count == 1


def test_tampering_and_execution_remain_disallowed() -> None:
    result = ingest((candidate(),))
    with pytest.raises(IntegrityError):
        verify_integrity(
            replace(result.accepted_observations[0], version=ObjectVersion(2)),
            result.accepted_refs[0].expected_fingerprint or "",
        )
    with pytest.raises(IntegrityError):
        verify_integrity(
            replace(result.manifest, version=ObjectVersion(2)),
            fingerprint_record(result.manifest),
        )
    assert tuple(ExecutionState) == (ExecutionState.PLANNED_CLOSED,)
    assert not hasattr(IngestionKernel(), "place_order")
