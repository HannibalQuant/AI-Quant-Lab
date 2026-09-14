from dataclasses import FrozenInstanceError
from datetime import UTC, datetime

import pytest

from ai_quant_lab.core.model import (
    AgentId, ArtifactEnvelope, ArtifactId, ArtifactLifecycle, AuditEvent, AuditEventId,
    AuditResult, EvidenceEnvelope, EvidenceId, EvidenceState, FreshnessState,
    InvalidIdentifier, InvalidRecord, InvalidSerialization, InvalidVersion, ObjectVersion,
    ProvenanceId, ProvenanceRecord, VersionedRef, canonical_json, canonical_loads, fingerprint,
)


NOW = datetime(2026, 9, 14, tzinfo=UTC)
AID = ArtifactId("alpha")
AGENT = AgentId("producer")
PROV = ProvenanceId("origin")
REF = VersionedRef(AID, ObjectVersion(1))


def test_typed_identifier_round_trip() -> None:
    assert ArtifactId.parse(str(AID)) == AID
    assert str(AID) == "artifact:alpha"


@pytest.mark.parametrize("value", ["", "UPPER", "bad space", "x" * 64])
def test_invalid_identifier_rejected(value: str) -> None:
    with pytest.raises(InvalidIdentifier):
        ArtifactId(value)


def test_wrong_namespace_rejected() -> None:
    with pytest.raises(InvalidIdentifier):
        EvidenceId.parse("artifact:alpha")


@pytest.mark.parametrize("value", [0, -1, True])
def test_invalid_versions_rejected(value: int) -> None:
    with pytest.raises(InvalidVersion):
        ObjectVersion(value)


def test_version_is_not_identity_or_latest() -> None:
    assert AID != ObjectVersion(1)
    with pytest.raises(InvalidVersion):
        ObjectVersion.parse("latest")


def test_provenance_requires_utc_and_process() -> None:
    record = ProvenanceRecord(PROV, AGENT, NOW, "unit-test", (REF,))
    assert record.input_refs == (REF,)
    with pytest.raises(InvalidRecord):
        ProvenanceRecord(PROV, AGENT, datetime(2026, 1, 1), "test")
    with pytest.raises(InvalidRecord):
        ProvenanceRecord(PROV, AGENT, NOW, "")


def test_artifact_is_immutable_and_requires_fingerprint() -> None:
    item = ArtifactEnvelope(AID, "report", ObjectVersion(1), NOW, AGENT, PROV,
                            ObjectVersion(1), ArtifactLifecycle.FROZEN, fingerprint({"x": 1}))
    with pytest.raises(FrozenInstanceError):
        item.artifact_type = "changed"  # type: ignore[misc]
    with pytest.raises(InvalidRecord):
        ArtifactEnvelope(AID, "report", ObjectVersion(1), NOW, AGENT, PROV,
                         ObjectVersion(1), ArtifactLifecycle.FROZEN, "bad")


def test_evidence_is_not_result_and_requires_artifact_reference() -> None:
    item = EvidenceEnvelope(EvidenceId("proof"), "test", REF, PROV, NOW, "scope")
    assert item.admissibility is EvidenceState.UNASSESSED
    assert item.freshness is FreshnessState.UNASSESSED
    with pytest.raises(InvalidRecord):
        EvidenceEnvelope(EvidenceId("x"), "test",
                         VersionedRef(EvidenceId("wrong"), ObjectVersion(1)),
                         PROV, NOW, "scope")


def test_audit_records_but_does_not_authorize() -> None:
    event = AuditEvent(AuditEventId("event"), AGENT, "record", REF, NOW, AuditResult.RECORDED)
    assert not hasattr(event, "authority")
    assert event.result is AuditResult.RECORDED


def test_canonical_serialization_and_fingerprint_are_deterministic() -> None:
    left = {"b": [2, 1], "a": "ą"}
    right = {"a": "ą", "b": [2, 1]}
    payload = canonical_json(left)
    assert payload == canonical_json(right)
    assert fingerprint(left) == fingerprint(right)
    assert canonical_loads(payload) == left


def test_malformed_or_noncanonical_serialization_fails() -> None:
    with pytest.raises(InvalidSerialization):
        canonical_loads("{")
    with pytest.raises(InvalidSerialization):
        canonical_loads('{"b":1, "a":2}')
    with pytest.raises(InvalidSerialization):
        canonical_json({"x": float("nan")})
