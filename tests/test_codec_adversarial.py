import json
from dataclasses import replace
from datetime import UTC, datetime

import pytest

from ai_quant_lab.core.codec import decode, decode_traceability, encode
from ai_quant_lab.core.integrity import IntegrityMismatch, InvalidFingerprint, verify_integrity
from ai_quant_lab.core.model import (
    AgentId,
    ArtifactEnvelope,
    ArtifactId,
    ArtifactLifecycle,
    InvalidRecord,
    InvalidSerialization,
    ObjectVersion,
    ProvenanceId,
    ProvenanceRecord,
    TraceabilityRef,
    VersionedRef,
    canonical_json,
)

NOW = datetime(2026, 9, 14, 12, 34, 56, 123456, tzinfo=UTC)


def artifact() -> ArtifactEnvelope:
    return ArtifactEnvelope(
        ArtifactId("artifact-1"),
        "report",
        ObjectVersion(1),
        NOW,
        AgentId("actor-1"),
        ProvenanceId("provenance-1"),
        ObjectVersion(1),
        ArtifactLifecycle.FROZEN,
        "sha256:" + "b" * 64,
    )


def altered_bytes(mutator: object) -> bytes:
    data = json.loads(encode(artifact()))
    assert callable(mutator)
    mutator(data)
    return canonical_json(data).encode()


@pytest.mark.parametrize(
    "mutation",
    [
        lambda value: value.update({"$representation_version": 2}),
        lambda value: value.update({"$type": "UnknownRecord"}),
        lambda value: value.update({"unexpected": True}),
        lambda value: value["payload"].update({"unexpected": True}),
        lambda value: value["payload"].pop("artifact_id"),
        lambda value: value["payload"].update({"artifact_id": "evidence:wrong"}),
        lambda value: value["payload"].update({"version": "1"}),
        lambda value: value["payload"].update({"version": True}),
        lambda value: value["payload"].update({"created_at": "2026-09-14T12:34:56Z"}),
        lambda value: value["payload"].update({"created_at": "2026-09-14 12:34:56.123456"}),
        lambda value: value["payload"].update({"lifecycle": "unknown"}),
        lambda value: value["payload"].update({"metadata": [["key", 1]]}),
    ],
)
def test_strict_decoder_rejects_contract_violations(mutation: object) -> None:
    with pytest.raises(InvalidSerialization):
        decode(altered_bytes(mutation), ArtifactEnvelope)


def test_duplicate_keys_are_rejected() -> None:
    valid = encode(artifact()).decode()
    attack = valid.replace(
        '"$representation_version":1',
        '"$representation_version":1,"$representation_version":1',
        1,
    )
    with pytest.raises(InvalidSerialization, match="duplicate"):
        decode(attack.encode(), ArtifactEnvelope)


@pytest.mark.parametrize(
    "payload",
    [
        b"{",
        b"\xff",
        b'{"$representation_version":NaN}',
        b'{"$representation_version":Infinity}',
        b'{"$representation_version":-Infinity}',
    ],
)
def test_malformed_and_nonfinite_input_rejected(payload: bytes) -> None:
    with pytest.raises(InvalidSerialization):
        decode(payload, ArtifactEnvelope)


def test_noncanonical_whitespace_and_field_order_are_rejected() -> None:
    canonical = encode(artifact()).decode()
    with pytest.raises(InvalidSerialization):
        decode((canonical + "\n").encode(), ArtifactEnvelope)
    parsed = json.loads(canonical)
    reordered = json.dumps(parsed, ensure_ascii=False, separators=(",", ":"))
    if reordered != canonical:
        with pytest.raises(InvalidSerialization):
            decode(reordered.encode(), ArtifactEnvelope)


def test_type_confusion_is_rejected() -> None:
    with pytest.raises(InvalidSerialization, match="type mismatch"):
        decode(encode(artifact()), ProvenanceRecord)


def test_arbitrary_objects_are_not_serializable() -> None:
    with pytest.raises(InvalidSerialization, match="unsupported governed type"):
        encode(object())  # type: ignore[arg-type]


def test_integrity_mismatch_and_invalid_fingerprint_fail_closed() -> None:
    item = artifact()
    with pytest.raises(IntegrityMismatch):
        verify_integrity(item, "sha256:" + "0" * 64)
    with pytest.raises(InvalidFingerprint):
        verify_integrity(item, "not-a-fingerprint")


def test_direct_artifact_self_parent_is_rejected() -> None:
    own = VersionedRef(ArtifactId("artifact-1"), ObjectVersion(1))
    with pytest.raises(InvalidRecord, match="own exact version"):
        replace(artifact(), parent_refs=(own,))


def test_direct_provenance_self_reference_is_rejected() -> None:
    own = VersionedRef(ProvenanceId("provenance-1"), ObjectVersion(9))
    with pytest.raises(InvalidRecord, match="directly reference itself"):
        ProvenanceRecord(
            ProvenanceId("provenance-1"),
            AgentId("actor-1"),
            NOW,
            "bad-lineage",
            (own,),
        )


@pytest.mark.parametrize(
    "payload",
    [
        b"{}",
        b'{"$format":"ai-quant-lab.canonical-json","$representation_version":2,"$type":"TraceabilityRef","payload":{}}',
        b'{"$format":"ai-quant-lab.canonical-json","$representation_version":1,"$type":"TraceabilityRef","payload":{"expected_fingerprint":"bad","object_id":"artifact:x","version":1}}',
    ],
)
def test_malformed_traceability_reference_rejected(payload: bytes) -> None:
    with pytest.raises(InvalidSerialization):
        decode_traceability(payload)


def test_traceability_fingerprint_validation() -> None:
    with pytest.raises(InvalidRecord):
        TraceabilityRef(ArtifactId("x"), ObjectVersion(1), "bad")
