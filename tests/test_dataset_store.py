"""Sprint 7 immutable local dataset repository and lineage attacks."""

from __future__ import annotations

import hashlib
import json
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, replace
from datetime import UTC, datetime
from pathlib import Path

import pytest

from ai_quant_lab.core.codec import encode
from ai_quant_lab.core.data import (
    DatasetLock,
    DatasetLockId,
    DatasetManifest,
    DecimalValue,
    InstrumentId,
    ObservationId,
    SourceId,
)
from ai_quant_lab.core.dataset_store import (
    DatasetLineageMismatch,
    DatasetLineageStatus,
    InvalidRepositoryPath,
    LocalDatasetRepository,
    RepositoryConflict,
    RepositoryIntegrityFailure,
    RepositoryNotFound,
    RepositoryObjectKey,
    RepositoryReadStatus,
    RepositoryTypeMismatch,
    RepositoryVersionMismatch,
    RepositoryWriteStatus,
    StoredDatasetObject,
    StoredObjectType,
    repository_key,
    verify_dataset_lineage,
)
from ai_quant_lab.core.integrity import fingerprint_record
from ai_quant_lab.core.market_data import (
    BarFinality,
    MarketBar,
    MarketBarId,
    MarketDataSchemaId,
    NormalizedBarManifest,
    TimeframeId,
    VolumeSemantic,
)
from ai_quant_lab.core.model import DatasetId, ObjectVersion, ProvenanceId, TraceabilityRef

V1 = ObjectVersion(1)
F = "sha256:" + "a" * 64
CREATED = datetime(2025, 1, 2, tzinfo=UTC)
CUTOFF = datetime(2025, 1, 1, 23, tzinfo=UTC)
BAR_OPEN = datetime(2025, 1, 1, 10, tzinfo=UTC)
BAR_CLOSE = datetime(2025, 1, 1, 11, tzinfo=UTC)
AVAILABLE = datetime(2025, 1, 1, 11, 0, 5, tzinfo=UTC)


@dataclass(frozen=True, slots=True)
class DatasetBundle:
    raw_manifest: DatasetManifest
    raw_lock: DatasetLock
    bar: MarketBar
    normalized_manifest: NormalizedBarManifest
    normalized_lock: DatasetLock


def exact(object_id: object, fingerprint: str = F) -> TraceabilityRef:
    return TraceabilityRef(object_id, V1, fingerprint)  # type: ignore[arg-type]


def bundle() -> DatasetBundle:
    observation_ref = exact(ObservationId("synthetic-observation"))
    source_ref = exact(SourceId("synthetic-source"))
    instrument_ref = exact(InstrumentId("synthetic-instrument"))
    provenance_ref = exact(ProvenanceId("synthetic-provenance"))
    timeframe_ref = exact(TimeframeId("1h"))
    schema_ref = exact(MarketDataSchemaId("synthetic-schema"))
    raw_manifest = DatasetManifest(
        DatasetId("raw-synthetic-dataset"),
        V1,
        CREATED,
        (observation_ref,),
        (source_ref,),
        (instrument_ref,),
        BAR_OPEN,
        BAR_OPEN,
        provenance_ref,
        V1,
    )
    raw_manifest_ref = exact(raw_manifest.dataset_id, fingerprint_record(raw_manifest))
    raw_lock = DatasetLock(
        DatasetLockId("raw-synthetic-lock"),
        V1,
        raw_manifest_ref,
        raw_manifest_ref,
        CREATED,
        CUTOFF,
        provenance_ref,
    )
    bar = MarketBar(
        MarketBarId("synthetic-bar"),
        V1,
        source_ref,
        instrument_ref,
        timeframe_ref,
        schema_ref,
        V1,
        BAR_OPEN,
        BAR_CLOSE,
        AVAILABLE,
        CREATED,
        DecimalValue("100"),
        DecimalValue("102"),
        DecimalValue("99"),
        DecimalValue("101"),
        DecimalValue("10"),
        VolumeSemantic.BASE,
        BarFinality.FINAL,
        observation_ref,
        provenance_ref,
    )
    raw_lock_ref = exact(raw_lock.lock_id, fingerprint_record(raw_lock))
    normalized_manifest = NormalizedBarManifest(
        DatasetId("normalized-synthetic-dataset"),
        V1,
        CREATED,
        (exact(bar.bar_id, fingerprint_record(bar)),),
        (source_ref,),
        (instrument_ref,),
        (timeframe_ref,),
        schema_ref,
        V1,
        raw_lock_ref,
        provenance_ref,
    )
    normalized_manifest_ref = exact(
        normalized_manifest.dataset_id, fingerprint_record(normalized_manifest)
    )
    normalized_lock = DatasetLock(
        DatasetLockId("normalized-synthetic-lock"),
        V1,
        normalized_manifest_ref,
        normalized_manifest_ref,
        CREATED,
        CUTOFF,
        provenance_ref,
    )
    return DatasetBundle(raw_manifest, raw_lock, bar, normalized_manifest, normalized_lock)


def repository(tmp_path: Path, name: str = "vault") -> LocalDatasetRepository:
    return LocalDatasetRepository(root=tmp_path / name, allowed_root=tmp_path)


@pytest.mark.parametrize(
    "attribute,record_type",
    [
        ("raw_manifest", DatasetManifest),
        ("raw_lock", DatasetLock),
        ("normalized_manifest", NormalizedBarManifest),
    ],
)
def test_store_and_load_supported_dataset_objects(
    tmp_path: Path,
    attribute: str,
    record_type: type[DatasetManifest | DatasetLock | NormalizedBarManifest],
) -> None:
    store = repository(tmp_path)
    record = getattr(bundle(), attribute)
    written = store.store(record)
    loaded = store.load(written.repository_key, record_type)
    assert written.status is RepositoryWriteStatus.STORED_NEW
    assert loaded.status is RepositoryReadStatus.FOUND_VERIFIED
    assert loaded.record == record
    assert type(loaded.record) is record_type
    assert loaded.repository_key.fingerprint == fingerprint_record(record)
    assert loaded.repository_key.object_version == record.version
    assert store.path_for(loaded.repository_key).read_bytes() == encode(record)


def test_key_is_deterministic_idempotent_and_restart_safe(tmp_path: Path) -> None:
    record = bundle().raw_manifest
    first_store = repository(tmp_path)
    first = first_store.store(record)
    second = first_store.store(record)
    restarted = LocalDatasetRepository(root=first_store.root, allowed_root=tmp_path)
    loaded = restarted.load(first.repository_key, DatasetManifest)
    assert first.repository_key == repository_key(record)
    assert first.status is RepositoryWriteStatus.STORED_NEW
    assert second.status is RepositoryWriteStatus.ALREADY_PRESENT_IDENTICAL
    assert loaded.record == record
    assert loaded.byte_size == len(encode(record))


def test_object_storage_order_does_not_change_keys(tmp_path: Path) -> None:
    data = bundle()
    first = repository(tmp_path, "first")
    second = repository(tmp_path, "second")
    first_keys = (
        first.store(data.raw_manifest).repository_key,
        first.store(data.raw_lock).repository_key,
        first.store(data.normalized_manifest).repository_key,
    )
    second_by_type = {
        result.repository_key.object_type: result.repository_key
        for result in (
            second.store(data.normalized_manifest),
            second.store(data.raw_lock),
            second.store(data.raw_manifest),
        )
    }
    assert first_keys == (
        second_by_type[StoredObjectType.DATASET_MANIFEST],
        second_by_type[StoredObjectType.DATASET_LOCK],
        second_by_type[StoredObjectType.NORMALIZED_BAR_MANIFEST],
    )


def test_identical_concurrent_creation_converges(tmp_path: Path) -> None:
    store = repository(tmp_path)
    record = bundle().raw_manifest
    with ThreadPoolExecutor(max_workers=2) as executor:
        results = tuple(executor.map(lambda _: store.store(record), range(2)))
    assert {result.status for result in results} == {
        RepositoryWriteStatus.STORED_NEW,
        RepositoryWriteStatus.ALREADY_PRESENT_IDENTICAL,
    }
    assert results[0].repository_key == results[1].repository_key
    assert store.load(results[0].repository_key, DatasetManifest).record == record


def test_exact_lineage_is_verified() -> None:
    data = bundle()
    result = verify_dataset_lineage(
        raw_manifest=data.raw_manifest,
        raw_lock=data.raw_lock,
        bars=(data.bar,),
        normalized_manifest=data.normalized_manifest,
        normalized_lock=data.normalized_lock,
    )
    assert result.status is DatasetLineageStatus.VERIFIED
    assert result.raw_manifest_fingerprint == fingerprint_record(data.raw_manifest)
    assert result.raw_lock_fingerprint == fingerprint_record(data.raw_lock)
    assert result.normalized_manifest_fingerprint == fingerprint_record(data.normalized_manifest)
    assert result.normalized_lock_fingerprint == fingerprint_record(data.normalized_lock)
    assert result.bar_fingerprints == (fingerprint_record(data.bar),)


def test_corrupted_parent_lineage_fails_closed() -> None:
    data = bundle()
    bad_raw_ref = exact(data.raw_lock.lock_id, "sha256:" + "b" * 64)
    changed_manifest = replace(data.normalized_manifest, raw_dataset_lock_ref=bad_raw_ref)
    with pytest.raises(DatasetLineageMismatch, match="exact raw lock"):
        verify_dataset_lineage(
            raw_manifest=data.raw_manifest,
            raw_lock=data.raw_lock,
            bars=(data.bar,),
            normalized_manifest=changed_manifest,
            normalized_lock=data.normalized_lock,
        )


def test_corrupted_bar_membership_fails_closed() -> None:
    data = bundle()
    changed_bar = replace(data.bar, close=DecimalValue("100.5"))
    with pytest.raises(DatasetLineageMismatch, match="bar membership"):
        verify_dataset_lineage(
            raw_manifest=data.raw_manifest,
            raw_lock=data.raw_lock,
            bars=(changed_bar,),
            normalized_manifest=data.normalized_manifest,
            normalized_lock=data.normalized_lock,
        )


def overwrite(path: Path, data: bytes) -> None:
    path.write_bytes(data)


@pytest.mark.parametrize(
    "mutator",
    [
        lambda data: data[:-8],
        lambda data: b"{not-json}",
        lambda data: b"\xff" + data[1:],
        lambda data: data.replace(b'"payload":{', b'"extra":1,"payload":{', 1),
        lambda data: data.replace(b'"$type":', b'"$type":"duplicate","$type":', 1),
    ],
)
def test_corrupt_truncated_malformed_extra_duplicate_and_utf8_fail_closed(
    tmp_path: Path, mutator: object
) -> None:
    store = repository(tmp_path)
    record = bundle().raw_manifest
    key = store.store(record).repository_key
    original = encode(record)
    overwrite(store.path_for(key), mutator(original))  # type: ignore[operator]
    with pytest.raises(RepositoryIntegrityFailure):
        store.load(key, DatasetManifest)


def test_wrong_requested_type_is_distinct(tmp_path: Path) -> None:
    store = repository(tmp_path)
    key = store.store(bundle().raw_manifest).repository_key
    with pytest.raises(RepositoryTypeMismatch):
        store.load(key, DatasetLock)


def test_tampered_stored_type_is_distinct(tmp_path: Path) -> None:
    store = repository(tmp_path)
    record = bundle().raw_manifest
    key = store.store(record).repository_key
    changed = encode(record).replace(b'"$type":"DatasetManifest"', b'"$type":"DatasetLock"')
    overwrite(store.path_for(key), changed)
    with pytest.raises(RepositoryTypeMismatch):
        store.load(key, DatasetManifest)


def test_wrong_stored_version_is_distinct(tmp_path: Path) -> None:
    store = repository(tmp_path)
    record = bundle().raw_manifest
    key = store.store(record).repository_key
    changed = encode(record).replace(b',"version":1}}', b',"version":2}}')
    overwrite(store.path_for(key), changed)
    with pytest.raises(RepositoryVersionMismatch):
        store.load(key, DatasetManifest)


def test_wrong_fingerprint_path_fails_integrity(tmp_path: Path) -> None:
    store = repository(tmp_path)
    record = bundle().raw_manifest
    wrong = RepositoryObjectKey(StoredObjectType.DATASET_MANIFEST, V1, "sha256:" + "b" * 64)
    destination = store.root / wrong.relative_path
    destination.parent.mkdir(parents=True)
    destination.write_bytes(encode(record))
    with pytest.raises(RepositoryIntegrityFailure, match="repository key"):
        store.load(wrong, DatasetManifest)


def test_attempted_overwrite_with_different_bytes_is_rejected(tmp_path: Path) -> None:
    store = repository(tmp_path)
    record = bundle().raw_manifest
    result = store.store(record)
    overwrite(store.path_for(result.repository_key), b"different")
    with pytest.raises(RepositoryConflict) as failure:
        store.store(record)
    assert failure.value.result.status is RepositoryWriteStatus.REJECTED_CONFLICT
    assert store.path_for(result.repository_key).read_bytes() == b"different"


def test_not_found_wrong_key_and_unexpected_extension_are_distinct(tmp_path: Path) -> None:
    store = repository(tmp_path)
    key = repository_key(bundle().raw_manifest)
    with pytest.raises(RepositoryNotFound):
        store.load(key, DatasetManifest)
    txt = store.root / key.relative_path.with_suffix(".txt")
    txt.parent.mkdir(parents=True)
    txt.write_bytes(encode(bundle().raw_manifest))
    with pytest.raises(RepositoryNotFound):
        store.load(key, DatasetManifest)


def test_traversal_and_outside_roots_are_rejected(tmp_path: Path) -> None:
    allowed = tmp_path / "allowed"
    allowed.mkdir()
    with pytest.raises(InvalidRepositoryPath, match="traversal"):
        LocalDatasetRepository(root=allowed / ".." / "escape", allowed_root=allowed)
    outside = tmp_path / "outside"
    outside.mkdir()
    with pytest.raises(InvalidRepositoryPath, match="outside"):
        LocalDatasetRepository(root=outside / "vault", allowed_root=allowed)
    with pytest.raises(InvalidRepositoryPath, match="absolute"):
        LocalDatasetRepository(root=Path("relative-vault"), allowed_root=allowed)


def test_root_and_direct_object_symlinks_are_rejected(tmp_path: Path) -> None:
    outside = tmp_path / "outside"
    outside.mkdir()
    linked_root = tmp_path / "linked-vault"
    linked_root.symlink_to(outside, target_is_directory=True)
    with pytest.raises(InvalidRepositoryPath, match="symlink"):
        LocalDatasetRepository(root=linked_root, allowed_root=tmp_path)

    store = repository(tmp_path, "safe-vault")
    key = store.store(bundle().raw_manifest).repository_key
    path = store.path_for(key)
    path.unlink()
    target = outside / "object.json"
    target.write_bytes(encode(bundle().raw_manifest))
    path.symlink_to(target)
    with pytest.raises(InvalidRepositoryPath, match="symlink"):
        store.load(key, DatasetManifest)


def test_symlink_escape_in_object_directory_is_rejected(tmp_path: Path) -> None:
    store = repository(tmp_path)
    outside = tmp_path / "outside"
    outside.mkdir()
    objects = store.root / "objects"
    objects.mkdir()
    (objects / StoredObjectType.DATASET_MANIFEST.value).symlink_to(
        outside, target_is_directory=True
    )
    with pytest.raises(InvalidRepositoryPath, match="unsafe"):
        store.store(bundle().raw_manifest)


def test_invalid_key_and_mutable_latest_alias_are_not_supported(tmp_path: Path) -> None:
    store = repository(tmp_path)
    record = bundle().raw_manifest
    key = store.store(record).repository_key
    latest = store.root / "latest"
    latest.symlink_to(store.path_for(key))
    with pytest.raises(InvalidRepositoryPath, match="fingerprint"):
        RepositoryObjectKey(StoredObjectType.DATASET_MANIFEST, V1, "latest")
    assert store.load(key, DatasetManifest).record == record
    assert not hasattr(store, "load_latest")


def test_new_persistence_golden_is_exact() -> None:
    golden = json.loads(Path("tests/golden/dataset_store_v1.json").read_text(encoding="utf-8"))
    data = bundle()
    records: dict[str, StoredDatasetObject] = {
        "raw_manifest": data.raw_manifest,
        "raw_lock": data.raw_lock,
        "normalized_manifest": data.normalized_manifest,
        "normalized_lock": data.normalized_lock,
    }
    assert golden["format"] == "immutable-local-dataset-store-v1"
    for name, record in records.items():
        vector = golden["objects"][name]
        assert vector["fingerprint"] == fingerprint_record(record)
        assert vector["repository_key"] == str(repository_key(record))
        assert vector["canonical_byte_sha256"] == hashlib.sha256(encode(record)).hexdigest()
        assert vector["object_version"] == record.version.number


def test_historical_golden_files_are_unchanged() -> None:
    expected = {
        "canonical_vectors_v1.json": (
            "596c56ec11563c06321602688c1fe04d9d611f3010d2d3f43c1bb2b64f86f1ae"
        ),
        "csv_import_valid_1h_v1.json": (
            "46b9ddfadea3a059de2705232256621e61e83dfe77d3987a7c3584283ddaba54"
        ),
        "data_contract_vectors_v1.json": (
            "b78eb84c6c1a9753f72693d8039064731e4ef3237083bb0149a2a1a06a9fd5cf"
        ),
        "ingestion_scenarios_v1.json": (
            "146144e05a2a46cb175344bdb0339ee2a794d8ed4d2ff178af89c8813d032fb1"
        ),
        "market_bar_scenarios_v1.json": (
            "1402c6fd373645e3d6183cdd12f45a1458f4fefc25cc8356b90439d4660bb92f"
        ),
    }
    for name, digest in expected.items():
        data = (Path("tests/golden") / name).read_bytes()
        assert hashlib.sha256(data).hexdigest() == digest
