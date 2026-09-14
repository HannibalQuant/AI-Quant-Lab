from __future__ import annotations

import json
from dataclasses import FrozenInstanceError
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any, cast

import pytest

from ai_quant_lab.core.codec import GovernedRecord, decode, encode
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
    InvalidDataContract,
    InvalidDecimal,
    InvalidTemporalOrder,
    ObservationId,
    RawField,
    RawObservation,
    ReconciliationDisposition,
    SourceId,
    SourceIdentity,
    SourceType,
    TemporalCoordinates,
    VenueId,
    VenueIdentity,
    VenueType,
)
from ai_quant_lab.core.governance import PRECONDITIONS, PreconditionStatus
from ai_quant_lab.core.integrity import IntegrityMismatch, fingerprint_record, verify_integrity
from ai_quant_lab.core.model import (
    AgentId,
    AuditEvent,
    AuditEventId,
    AuditResult,
    DatasetId,
    InvalidSerialization,
    ObjectVersion,
    ProvenanceId,
    TraceabilityRef,
)

T0 = datetime(2026, 1, 2, 9, 30, tzinfo=UTC)
T1 = T0 + timedelta(milliseconds=250)
T2 = T1 + timedelta(seconds=2)
FP_A = "sha256:" + "a" * 64
FP_B = "sha256:" + "b" * 64
FP_C = "sha256:" + "c" * 64


def ref(identifier: object, fingerprint: str = FP_A) -> TraceabilityRef:
    return TraceabilityRef(identifier, ObjectVersion(1), fingerprint)  # type: ignore[arg-type]


def governed_data_records() -> tuple[
    VenueIdentity,
    SourceIdentity,
    InstrumentIdentity,
    RawObservation,
    DatasetManifest,
    DatasetLock,
]:
    venue = VenueIdentity(
        VenueId("venue-001"),
        ObjectVersion(1),
        "Synthetic Venue",
        VenueType.SYNTHETIC,
        "ZZ",
        ObjectVersion(1),
    )
    source = SourceIdentity(
        SourceId("source-001"),
        ObjectVersion(1),
        "Synthetic Provider",
        SourceType.SYNTHETIC_FIXTURE,
        "trades",
        "fixture-v1",
        ref(venue.venue_id),
        ObjectVersion(1),
    )
    instrument = InstrumentIdentity(
        InstrumentId("sol-usd-spot-001"),
        ObjectVersion(1),
        "SOLUSD",
        InstrumentClass.SPOT,
        "SOL",
        "USD",
        "USD",
        ref(venue.venue_id),
        ObjectVersion(1),
    )
    observation = RawObservation(
        ObservationId("observation-001"),
        ObjectVersion(1),
        ref(source.source_id),
        ref(instrument.instrument_id),
        TemporalCoordinates(T0, T1, T2),
        (RawField("price", DecimalValue.from_text("123.4500")), RawField("size", 2)),
        ref(ProvenanceId("data-prov-001")),
        "42",
        DataQualityState.ACCEPTED,
        ReconciliationDisposition.UNIQUE,
    )
    manifest = DatasetManifest(
        DatasetId("dataset-001"),
        ObjectVersion(1),
        T2,
        (ref(observation.observation_id, fingerprint_record(observation)),),
        (ref(source.source_id, fingerprint_record(source)),),
        (ref(instrument.instrument_id, fingerprint_record(instrument)),),
        T0,
        T0,
        ref(ProvenanceId("manifest-prov-001")),
        ObjectVersion(1),
    )
    manifest_fp = fingerprint_record(manifest)
    lock = DatasetLock(
        DatasetLockId("lock-001"),
        ObjectVersion(1),
        ref(manifest.dataset_id, manifest_fp),
        ref(manifest.dataset_id, manifest_fp),
        T2 + timedelta(seconds=1),
        T1,
        ref(ProvenanceId("lock-prov-001")),
        DatasetLockState.LOCKED,
        ObjectVersion(1),
    )
    return venue, source, instrument, observation, manifest, lock


@pytest.mark.parametrize("index", range(6))
def test_data_records_have_exact_typed_round_trip(index: int) -> None:
    record = governed_data_records()[index]
    decoded = decode(encode(record), cast(Any, type(record)))
    assert decoded == record
    assert type(decoded) is type(record)


def test_source_and_venue_do_not_collapse() -> None:
    venue, source, instrument, *_ = governed_data_records()
    other = SourceIdentity(
        SourceId("source-002"),
        source.version,
        source.provider,
        source.source_type,
        source.feed,
        source.source_version,
        ref(VenueId("venue-002")),
        source.contract_version,
    )
    assert source != other
    assert str(source.source_id) != str(venue.venue_id)
    assert instrument.symbol == "SOLUSD"


def test_temporal_dimensions_and_legitimate_knowledge_time_remain_distinct() -> None:
    temporal = governed_data_records()[3].temporal
    assert temporal.event_time < temporal.availability_time < temporal.ingestion_time
    assert temporal.legitimate_knowledge_time == temporal.availability_time
    assert temporal.legitimate_knowledge_time != temporal.event_time


def test_temporal_contract_rejects_naive_and_reverse_order() -> None:
    with pytest.raises(ValueError):
        TemporalCoordinates(datetime(2026, 1, 1), T1, T2)
    with pytest.raises(InvalidTemporalOrder):
        TemporalCoordinates(T1, T0, T2)


@pytest.mark.parametrize("text", ["1", "1.0", "1.00", "1e0"])
def test_decimal_equivalence_policy_is_scale_insensitive(text: str) -> None:
    assert DecimalValue.from_text(text) == DecimalValue("1")


@pytest.mark.parametrize("text", ["NaN", "Infinity", "-Infinity", "bad"])
def test_decimal_rejects_non_finite_or_malformed_values(text: str) -> None:
    with pytest.raises(InvalidDecimal):
        DecimalValue.from_text(text)


def test_raw_payload_rejects_binary_float_arbitrary_and_derived_semantics() -> None:
    with pytest.raises(InvalidDataContract):
        RawField("price", 1.25)  # type: ignore[arg-type]
    with pytest.raises(InvalidDataContract):
        RawField("price", object())  # type: ignore[arg-type]
    for name in ("signal", "feature_rsi", "strategy_state", "order_side"):
        with pytest.raises(InvalidDataContract):
            RawField(name, "forbidden")


def test_accepted_observation_cannot_hide_unresolved_or_conflicting_data() -> None:
    base = governed_data_records()[3]
    for disposition in (
        ReconciliationDisposition.UNRESOLVED,
        ReconciliationDisposition.CONFLICT,
    ):
        with pytest.raises(InvalidDataContract):
            RawObservation(
                base.observation_id,
                base.version,
                base.source_ref,
                base.instrument_ref,
                base.temporal,
                base.payload,
                base.provenance_ref,
                quality=DataQualityState.ACCEPTED,
                reconciliation=disposition,
            )


def test_correction_is_new_immutable_history() -> None:
    original = governed_data_records()[3]
    correction = RawObservation(
        ObservationId("observation-002"),
        ObjectVersion(1),
        original.source_ref,
        original.instrument_ref,
        original.temporal,
        (RawField("price", DecimalValue("124")),),
        original.provenance_ref,
        quality=DataQualityState.SUSPECT,
        reconciliation=ReconciliationDisposition.CORRECTION,
        supersedes=ref(original.observation_id, fingerprint_record(original)),
    )
    assert correction.supersedes is not None
    assert correction.supersedes.object_id == original.observation_id
    assert original.payload[0].value == DecimalValue("123.45")
    with pytest.raises(FrozenInstanceError):
        original.quality = DataQualityState.INVALIDATED  # type: ignore[misc]


def test_direct_self_supersession_is_rejected() -> None:
    base = governed_data_records()[3]
    with pytest.raises(InvalidDataContract):
        RawObservation(
            base.observation_id,
            base.version,
            base.source_ref,
            base.instrument_ref,
            base.temporal,
            base.payload,
            base.provenance_ref,
            reconciliation=ReconciliationDisposition.CORRECTION,
            supersedes=ref(base.observation_id, fingerprint_record(base)),
        )


def test_quarantine_preserves_record_and_does_not_grant_acceptance() -> None:
    base = governed_data_records()[3]
    quarantined = RawObservation(
        base.observation_id,
        base.version,
        base.source_ref,
        base.instrument_ref,
        base.temporal,
        base.payload,
        base.provenance_ref,
        base.source_sequence,
        DataQualityState.QUARANTINED,
        ReconciliationDisposition.UNRESOLVED,
    )
    assert quarantined.quality is DataQualityState.QUARANTINED
    assert quarantined.observation_id == base.observation_id
    assert quarantined.payload == base.payload
    assert quarantined.provenance_ref == base.provenance_ref


def test_manifest_membership_is_exact_and_reproducible() -> None:
    manifest = governed_data_records()[4]
    clone = decode(encode(manifest), DatasetManifest)
    assert fingerprint_record(clone) == fingerprint_record(manifest)
    changed_ref = ref(ObservationId("observation-999"), FP_B)
    changed = DatasetManifest(
        manifest.dataset_id,
        ObjectVersion(2),
        manifest.created_at,
        (changed_ref,),
        manifest.source_refs,
        manifest.instrument_refs,
        manifest.event_time_start,
        manifest.event_time_end,
        manifest.provenance_ref,
        manifest.contract_version,
    )
    assert fingerprint_record(changed) != fingerprint_record(manifest)


def test_manifest_rejects_duplicates_and_mutable_query_membership() -> None:
    manifest = governed_data_records()[4]
    with pytest.raises(InvalidDataContract):
        DatasetManifest(
            manifest.dataset_id,
            manifest.version,
            manifest.created_at,
            manifest.observation_refs * 2,
            manifest.source_refs,
            manifest.instrument_refs,
            manifest.event_time_start,
            manifest.event_time_end,
            manifest.provenance_ref,
            manifest.contract_version,
        )
    with pytest.raises(InvalidDataContract):
        DatasetManifest(
            manifest.dataset_id,
            manifest.version,
            manifest.created_at,
            manifest.observation_refs,
            manifest.source_refs,
            manifest.instrument_refs,
            manifest.event_time_start,
            manifest.event_time_end,
            manifest.provenance_ref,
            manifest.contract_version,
            "all_sol_latest",
        )


def test_dataset_lock_binds_exact_manifest_and_cutoff() -> None:
    lock = governed_data_records()[5]
    assert lock.dataset_ref.expected_fingerprint == lock.manifest_ref.expected_fingerprint
    with pytest.raises(InvalidTemporalOrder):
        DatasetLock(
            lock.lock_id,
            lock.version,
            lock.dataset_ref,
            lock.manifest_ref,
            lock.locked_at,
            lock.locked_at + timedelta(seconds=1),
            lock.provenance_ref,
        )
    with pytest.raises(InvalidDataContract):
        DatasetLock(
            lock.lock_id,
            lock.version,
            lock.dataset_ref,
            TraceabilityRef(DatasetId("other"), ObjectVersion(1), FP_A),
            lock.locked_at,
            lock.temporal_cutoff,
            lock.provenance_ref,
        )


def test_integrity_detects_observation_manifest_and_lock_tampering() -> None:
    for record in governed_data_records()[3:]:
        expected = fingerprint_record(record)
        raw = json.loads(encode(record))
        raw["payload"]["contract_version"] = 2
        tampered = json.dumps(
            raw, ensure_ascii=False, allow_nan=False, sort_keys=True, separators=(",", ":")
        ).encode()
        changed = decode(tampered, cast(Any, type(record)))
        with pytest.raises(IntegrityMismatch):
            verify_integrity(changed, expected)


def test_data_decoder_rejects_unknown_field_type_and_representation_version() -> None:
    observation = governed_data_records()[3]
    raw = json.loads(encode(observation))
    raw["payload"]["unexpected"] = True
    canonical = json.dumps(raw, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()
    with pytest.raises(InvalidSerialization):
        decode(canonical, RawObservation)
    with pytest.raises(InvalidSerialization):
        decode(encode(observation), DatasetManifest)
    raw = json.loads(encode(observation))
    raw["$representation_version"] = 99
    canonical = json.dumps(raw, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()
    with pytest.raises(InvalidSerialization):
        decode(canonical, RawObservation)


def test_audit_can_reference_data_but_cannot_authorize_it() -> None:
    observation = governed_data_records()[3]
    audit = AuditEvent(
        AuditEventId("data-audit-001"),
        AgentId("data-steward-001"),
        "observation.accepted",
        observation.source_ref.versioned_ref,
        T2,
        AuditResult.RECORDED,
    )
    assert audit.target == observation.source_ref.versioned_ref
    assert not hasattr(audit, "authority")
    assert not hasattr(audit, "authorization")


def test_golden_data_vectors_are_stable() -> None:
    fixture = json.loads(Path("tests/golden/data_contract_vectors_v1.json").read_text())
    by_name = {item["name"]: item for item in fixture["vectors"]}
    records: tuple[GovernedRecord, ...] = governed_data_records()
    names = ("venue", "source", "instrument", "observation", "manifest", "lock")
    for record, name in zip(records, names, strict=True):
        assert encode(record).decode() == by_name[name]["canonical"]
        assert fingerprint_record(record) == by_name[name]["fingerprint"]


def test_ip11_is_partial_while_ip05_and_ip12_are_not_falsely_closed() -> None:
    by_id = {item.precondition_id: item for item in PRECONDITIONS}
    assert by_id["IP-05"].status is PreconditionStatus.PARTIALLY_RESOLVED
    assert by_id["IP-11"].status is PreconditionStatus.PARTIALLY_RESOLVED
    assert by_id["IP-12"].status is PreconditionStatus.OPEN
