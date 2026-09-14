from __future__ import annotations

import json
import os
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path

import pytest

from ai_quant_lab.core.codec import (
    REPRESENTATION_VERSION,
    GovernedRecord,
    decode,
    decode_traceability,
    encode,
    encode_traceability,
)
from ai_quant_lab.core.integrity import IntegrityMismatch, fingerprint_record, verify_integrity
from ai_quant_lab.core.model import (
    AgentId,
    ArtifactEnvelope,
    ArtifactId,
    ArtifactLifecycle,
    AuditEvent,
    AuditEventId,
    AuditResult,
    DatasetId,
    EvidenceEnvelope,
    EvidenceId,
    ObjectVersion,
    ProvenanceId,
    ProvenanceRecord,
    TraceabilityRef,
    VersionedRef,
)

NOW = datetime(2026, 9, 14, 12, 34, 56, 123456, tzinfo=UTC)
AGENT = AgentId("producer-001")
PROVENANCE_ID = ProvenanceId("prov-001")
ARTIFACT_ID = ArtifactId("report-001")
DATA_REF = VersionedRef(DatasetId("data-001"), ObjectVersion(2))
ARTIFACT_REF = VersionedRef(ARTIFACT_ID, ObjectVersion(1))


def records() -> tuple[ArtifactEnvelope, EvidenceEnvelope, ProvenanceRecord, AuditEvent]:
    artifact = ArtifactEnvelope(
        ARTIFACT_ID,
        "research_report",
        ObjectVersion(1),
        NOW,
        AGENT,
        PROVENANCE_ID,
        ObjectVersion(1),
        ArtifactLifecycle.FROZEN,
        "sha256:" + "a" * 64,
        (DATA_REF,),
        (("desk", "quant"),),
    )
    evidence = EvidenceEnvelope(
        EvidenceId("evidence-001"),
        "quality_report",
        ARTIFACT_REF,
        PROVENANCE_ID,
        NOW,
        "research",
        metadata=(("quality", "review"),),
    )
    provenance = ProvenanceRecord(
        PROVENANCE_ID,
        AGENT,
        NOW,
        "canonical-fixture",
        (DATA_REF,),
        metadata=(("source", "fixture"),),
    )
    audit = AuditEvent(
        AuditEventId("audit-001"),
        AGENT,
        "record",
        ARTIFACT_REF,
        NOW,
        AuditResult.RECORDED,
        (("reason", "fixture"),),
    )
    return artifact, evidence, provenance, audit


def _assert_round_trip[T: (ArtifactEnvelope, EvidenceEnvelope, ProvenanceRecord, AuditEvent)](
    record: T, record_type: type[T]
) -> None:
    decoded = decode(encode(record), record_type)
    assert decoded == record
    assert type(decoded) is record_type


def test_exact_typed_round_trips() -> None:
    artifact, evidence, provenance, audit = records()
    _assert_round_trip(artifact, ArtifactEnvelope)
    _assert_round_trip(evidence, EvidenceEnvelope)
    _assert_round_trip(provenance, ProvenanceRecord)
    _assert_round_trip(audit, AuditEvent)


def test_typed_components_survive_round_trip() -> None:
    artifact = records()[0]
    decoded = decode(encode(artifact), ArtifactEnvelope)
    assert isinstance(decoded.artifact_id, ArtifactId)
    assert isinstance(decoded.version, ObjectVersion)
    assert isinstance(decoded.parent_refs[0].object_id, DatasetId)
    assert decoded.created_at == NOW


def test_golden_vectors_are_stable() -> None:
    fixture = json.loads(Path("tests/golden/canonical_vectors_v1.json").read_text(encoding="utf-8"))
    assert fixture["representation_version"] == REPRESENTATION_VERSION
    by_name = {item["name"]: item for item in fixture["vectors"]}
    governed_records: tuple[GovernedRecord, ...] = records()
    for record, name in zip(
        governed_records, ("artifact", "evidence", "provenance", "audit"), strict=True
    ):
        assert encode(record).decode("utf-8") == by_name[name]["canonical"]
        assert fingerprint_record(record) == by_name[name]["fingerprint"]


def test_integrity_success_and_tamper_detection() -> None:
    artifact = records()[0]
    expected = fingerprint_record(artifact)
    assert verify_integrity(artifact, expected).actual_fingerprint == expected
    changed = ArtifactEnvelope(
        artifact.artifact_id,
        artifact.artifact_type,
        ObjectVersion(2),
        artifact.created_at,
        artifact.producer_id,
        artifact.provenance_id,
        artifact.contract_version,
        artifact.lifecycle,
        artifact.content_fingerprint,
        artifact.parent_refs,
        artifact.metadata,
    )
    with pytest.raises(IntegrityMismatch):
        verify_integrity(changed, expected)


def test_domain_separation_prevents_cross_type_equivalence() -> None:
    artifact, evidence, _, _ = records()
    assert encode(artifact) != encode(evidence)
    assert fingerprint_record(artifact) != fingerprint_record(evidence)


def test_traceability_reference_round_trip_is_exact() -> None:
    reference = TraceabilityRef(ARTIFACT_ID, ObjectVersion(1), fingerprint_record(records()[0]))
    assert decode_traceability(encode_traceability(reference)) == reference
    assert reference.versioned_ref == ARTIFACT_REF


def test_cross_process_hash_seed_determinism() -> None:
    script = """
from datetime import UTC, datetime
from ai_quant_lab.core.integrity import fingerprint_record
from ai_quant_lab.core.model import *
item = ArtifactEnvelope(
    ArtifactId('report-001'), 'research_report', ObjectVersion(1),
    datetime(2026, 9, 14, 12, 34, 56, 123456, tzinfo=UTC),
    AgentId('producer-001'), ProvenanceId('prov-001'), ObjectVersion(1),
    ArtifactLifecycle.FROZEN, 'sha256:' + 'a' * 64,
    (VersionedRef(DatasetId('data-001'), ObjectVersion(2)),),
    (('desk', 'quant'),),
)
print(fingerprint_record(item))
"""
    outputs = []
    for seed in ("1", "777"):
        environment = os.environ.copy()
        environment["PYTHONHASHSEED"] = seed
        outputs.append(
            subprocess.check_output(
                [sys.executable, "-c", script],
                text=True,
                env=environment,
            ).strip()
        )
    assert outputs[0] == outputs[1] == fingerprint_record(records()[0])
