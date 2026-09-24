"""Bounded immutable local persistence for governed dataset records."""

from __future__ import annotations

import errno
import hmac
import os
import re
import stat
import tempfile
from contextlib import suppress
from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path
from typing import Any, Final, cast

from ai_quant_lab.core.codec import GovernedRecord, decode, encode
from ai_quant_lab.core.data import DatasetLock, DatasetLockId, DatasetManifest, RawObservation
from ai_quant_lab.core.experiment_contracts import (
    ExperimentAuthorizationPolicy,
    ExperimentAuthorizationRecord,
    ExperimentSpecification,
)
from ai_quant_lab.core.experiment_runner_contracts import (
    ExperimentReplayContract,
    ExperimentResultArtifact,
    ExperimentRunRecord,
)
from ai_quant_lab.core.integrity import IntegrityError, fingerprint_record, verify_integrity
from ai_quant_lab.core.market_data import MarketBar, NormalizedBarManifest
from ai_quant_lab.core.model import (
    DatasetId,
    InvalidSerialization,
    ObjectVersion,
    TraceabilityRef,
)
from ai_quant_lab.core.optimization_contracts import (
    OptimizationCandidateDefinition,
    OptimizationCandidateResult,
    OptimizationPlan,
    OptimizationRunRecord,
    OptimizationSearchSpace,
    OptimizationSelectionResult,
    OptimizationTrialRecord,
)
from ai_quant_lab.core.pine_python_parity_contracts import (
    ParityTolerancePolicy,
    PineExecutionEvidence,
    PinePythonParityResult,
    PinePythonParityRunRecord,
)
from ai_quant_lab.core.pine_strategy_contracts import (
    PineStrategyIntakeRecord,
    PineStrategySourceArtifact,
)
from ai_quant_lab.core.real_csv_contracts import (
    RealCsvAdmissionRecord,
    RealCsvSourceDeclaration,
)
from ai_quant_lab.core.research_eligibility_contracts import (
    ResearchDatasetEligibilityPolicy,
    ResearchDatasetEligibilityRecord,
)
from ai_quant_lab.core.robustness_validation_contracts import (
    RobustnessValidationPlan,
    RobustnessValidationResult,
    RobustnessValidationRunRecord,
)
from ai_quant_lab.core.scientific_validation_contracts import (
    ScientificValidationResult,
    ValidationPlan,
    ValidationRunRecord,
)
from ai_quant_lab.core.strategy_backtest_contracts import (
    BacktestResultArtifact,
    BacktestRunRecord,
    StrategyDefinition,
)

_FINGERPRINT: Final = re.compile(r"^sha256:[0-9a-f]{64}$")
_MAX_OBJECT_BYTES: Final = 1_000_000


type StoredDatasetObject = (
    DatasetManifest
    | DatasetLock
    | NormalizedBarManifest
    | RawObservation
    | MarketBar
    | RealCsvSourceDeclaration
    | RealCsvAdmissionRecord
    | ResearchDatasetEligibilityPolicy
    | ResearchDatasetEligibilityRecord
    | ExperimentSpecification
    | ExperimentAuthorizationPolicy
    | ExperimentAuthorizationRecord
    | ExperimentReplayContract
    | ExperimentResultArtifact
    | ExperimentRunRecord
    | StrategyDefinition
    | BacktestResultArtifact
    | BacktestRunRecord
    | ValidationPlan
    | ScientificValidationResult
    | ValidationRunRecord
    | RobustnessValidationPlan
    | RobustnessValidationResult
    | RobustnessValidationRunRecord
    | OptimizationSearchSpace
    | OptimizationPlan
    | OptimizationCandidateDefinition
    | OptimizationCandidateResult
    | OptimizationTrialRecord
    | OptimizationSelectionResult
    | OptimizationRunRecord
    | PineStrategySourceArtifact
    | PineStrategyIntakeRecord
    | ParityTolerancePolicy
    | PineExecutionEvidence
    | PinePythonParityResult
    | PinePythonParityRunRecord
)


class DatasetRepositoryError(ValueError):
    """Base failure for the bounded local dataset repository."""


class InvalidRepositoryPath(DatasetRepositoryError):
    pass


class UnsupportedStoredType(DatasetRepositoryError):
    pass


class RepositoryNotFound(DatasetRepositoryError):
    pass


class RepositoryIntegrityFailure(DatasetRepositoryError):
    pass


class RepositoryTypeMismatch(DatasetRepositoryError):
    pass


class RepositoryVersionMismatch(DatasetRepositoryError):
    pass


class RepositoryConflict(DatasetRepositoryError):
    def __init__(self, result: RepositoryWriteResult) -> None:
        super().__init__("immutable repository key already contains different bytes")
        self.result = result


class DatasetLineageMismatch(DatasetRepositoryError):
    pass


class StoredObjectType(StrEnum):
    RAW_OBSERVATION = "raw-observation"
    DATASET_MANIFEST = "dataset-manifest"
    DATASET_LOCK = "dataset-lock"
    MARKET_BAR = "market-bar"
    NORMALIZED_BAR_MANIFEST = "normalized-bar-manifest"
    REAL_CSV_SOURCE_DECLARATION = "real-csv-source-declaration"
    REAL_CSV_ADMISSION_RECORD = "real-csv-admission-record"
    RESEARCH_DATASET_ELIGIBILITY_POLICY = "research-dataset-eligibility-policy"
    RESEARCH_DATASET_ELIGIBILITY_RECORD = "research-dataset-eligibility-record"
    EXPERIMENT_SPECIFICATION = "experiment-specification"
    EXPERIMENT_AUTHORIZATION_POLICY = "experiment-authorization-policy"
    EXPERIMENT_AUTHORIZATION_RECORD = "experiment-authorization-record"
    EXPERIMENT_REPLAY_CONTRACT = "experiment-replay-contract"
    EXPERIMENT_RESULT_ARTIFACT = "experiment-result-artifact"
    EXPERIMENT_RUN_RECORD = "experiment-run-record"
    STRATEGY_DEFINITION = "strategy-definition"
    BACKTEST_RESULT_ARTIFACT = "backtest-result-artifact"
    BACKTEST_RUN_RECORD = "backtest-run-record"
    VALIDATION_PLAN = "validation-plan"
    SCIENTIFIC_VALIDATION_RESULT = "scientific-validation-result"
    VALIDATION_RUN_RECORD = "validation-run-record"
    ROBUSTNESS_VALIDATION_PLAN = "robustness-validation-plan"
    ROBUSTNESS_VALIDATION_RESULT = "robustness-validation-result"
    ROBUSTNESS_VALIDATION_RUN_RECORD = "robustness-validation-run-record"
    OPTIMIZATION_SEARCH_SPACE = "optimization-search-space"
    OPTIMIZATION_PLAN = "optimization-plan"
    OPTIMIZATION_CANDIDATE_DEFINITION = "optimization-candidate-definition"
    OPTIMIZATION_CANDIDATE_RESULT = "optimization-candidate-result"
    OPTIMIZATION_TRIAL_RECORD = "optimization-trial-record"
    OPTIMIZATION_SELECTION_RESULT = "optimization-selection-result"
    OPTIMIZATION_RUN_RECORD = "optimization-run-record"
    PINE_STRATEGY_SOURCE_ARTIFACT = "pine-strategy-source-artifact"
    PINE_STRATEGY_INTAKE_RECORD = "pine-strategy-intake-record"
    PARITY_TOLERANCE_POLICY = "parity-tolerance-policy"
    PINE_EXECUTION_EVIDENCE = "pine-execution-evidence"
    PINE_PYTHON_PARITY_RESULT = "pine-python-parity-result"
    PINE_PYTHON_PARITY_RUN_RECORD = "pine-python-parity-run-record"


class RepositoryWriteStatus(StrEnum):
    STORED_NEW = "STORED_NEW"
    ALREADY_PRESENT_IDENTICAL = "ALREADY_PRESENT_IDENTICAL"
    REJECTED_CONFLICT = "REJECTED_CONFLICT"


class RepositoryReadStatus(StrEnum):
    FOUND_VERIFIED = "FOUND_VERIFIED"


class DatasetLineageStatus(StrEnum):
    VERIFIED = "VERIFIED"


@dataclass(frozen=True, slots=True)
class RepositoryObjectKey:
    object_type: StoredObjectType
    object_version: ObjectVersion
    fingerprint: str

    def __post_init__(self) -> None:
        if not isinstance(self.object_type, StoredObjectType):
            raise InvalidRepositoryPath("repository object type is invalid")
        if not isinstance(self.object_version, ObjectVersion):
            raise InvalidRepositoryPath("repository object version is invalid")
        if not isinstance(self.fingerprint, str) or not _FINGERPRINT.fullmatch(self.fingerprint):
            raise InvalidRepositoryPath("repository fingerprint is invalid")

    @property
    def relative_path(self) -> Path:
        digest = self.fingerprint.removeprefix("sha256:")
        return Path(
            "objects",
            self.object_type.value,
            f"v{self.object_version.number}",
            f"{digest}.json",
        )

    def __str__(self) -> str:
        return self.relative_path.as_posix()


@dataclass(frozen=True, slots=True)
class RepositoryWriteResult:
    status: RepositoryWriteStatus
    repository_key: RepositoryObjectKey
    object_id: str
    object_fingerprint: str
    byte_size: int


@dataclass(frozen=True, slots=True)
class RepositoryReadResult[T: StoredDatasetObject]:
    status: RepositoryReadStatus
    repository_key: RepositoryObjectKey
    record: T
    byte_size: int


@dataclass(frozen=True, slots=True)
class DatasetLineageVerification:
    status: DatasetLineageStatus
    raw_manifest_fingerprint: str
    raw_lock_fingerprint: str
    normalized_manifest_fingerprint: str
    normalized_lock_fingerprint: str
    bar_fingerprints: tuple[str, ...]


_TYPE_TO_STORAGE: Final[dict[type[StoredDatasetObject], StoredObjectType]] = {
    RawObservation: StoredObjectType.RAW_OBSERVATION,
    DatasetManifest: StoredObjectType.DATASET_MANIFEST,
    DatasetLock: StoredObjectType.DATASET_LOCK,
    MarketBar: StoredObjectType.MARKET_BAR,
    NormalizedBarManifest: StoredObjectType.NORMALIZED_BAR_MANIFEST,
    RealCsvSourceDeclaration: StoredObjectType.REAL_CSV_SOURCE_DECLARATION,
    RealCsvAdmissionRecord: StoredObjectType.REAL_CSV_ADMISSION_RECORD,
    ResearchDatasetEligibilityPolicy: StoredObjectType.RESEARCH_DATASET_ELIGIBILITY_POLICY,
    ResearchDatasetEligibilityRecord: StoredObjectType.RESEARCH_DATASET_ELIGIBILITY_RECORD,
    ExperimentSpecification: StoredObjectType.EXPERIMENT_SPECIFICATION,
    ExperimentAuthorizationPolicy: StoredObjectType.EXPERIMENT_AUTHORIZATION_POLICY,
    ExperimentAuthorizationRecord: StoredObjectType.EXPERIMENT_AUTHORIZATION_RECORD,
    ExperimentReplayContract: StoredObjectType.EXPERIMENT_REPLAY_CONTRACT,
    ExperimentResultArtifact: StoredObjectType.EXPERIMENT_RESULT_ARTIFACT,
    ExperimentRunRecord: StoredObjectType.EXPERIMENT_RUN_RECORD,
    StrategyDefinition: StoredObjectType.STRATEGY_DEFINITION,
    BacktestResultArtifact: StoredObjectType.BACKTEST_RESULT_ARTIFACT,
    BacktestRunRecord: StoredObjectType.BACKTEST_RUN_RECORD,
    ValidationPlan: StoredObjectType.VALIDATION_PLAN,
    ScientificValidationResult: StoredObjectType.SCIENTIFIC_VALIDATION_RESULT,
    ValidationRunRecord: StoredObjectType.VALIDATION_RUN_RECORD,
    RobustnessValidationPlan: StoredObjectType.ROBUSTNESS_VALIDATION_PLAN,
    RobustnessValidationResult: StoredObjectType.ROBUSTNESS_VALIDATION_RESULT,
    RobustnessValidationRunRecord: StoredObjectType.ROBUSTNESS_VALIDATION_RUN_RECORD,
    OptimizationSearchSpace: StoredObjectType.OPTIMIZATION_SEARCH_SPACE,
    OptimizationPlan: StoredObjectType.OPTIMIZATION_PLAN,
    OptimizationCandidateDefinition: StoredObjectType.OPTIMIZATION_CANDIDATE_DEFINITION,
    OptimizationCandidateResult: StoredObjectType.OPTIMIZATION_CANDIDATE_RESULT,
    OptimizationTrialRecord: StoredObjectType.OPTIMIZATION_TRIAL_RECORD,
    OptimizationSelectionResult: StoredObjectType.OPTIMIZATION_SELECTION_RESULT,
    OptimizationRunRecord: StoredObjectType.OPTIMIZATION_RUN_RECORD,
    PineStrategySourceArtifact: StoredObjectType.PINE_STRATEGY_SOURCE_ARTIFACT,
    PineStrategyIntakeRecord: StoredObjectType.PINE_STRATEGY_INTAKE_RECORD,
    ParityTolerancePolicy: StoredObjectType.PARITY_TOLERANCE_POLICY,
    PineExecutionEvidence: StoredObjectType.PINE_EXECUTION_EVIDENCE,
    PinePythonParityResult: StoredObjectType.PINE_PYTHON_PARITY_RESULT,
    PinePythonParityRunRecord: StoredObjectType.PINE_PYTHON_PARITY_RUN_RECORD,
}


def _stored_type(record_type: type[StoredDatasetObject]) -> StoredObjectType:
    try:
        return _TYPE_TO_STORAGE[record_type]
    except KeyError as exc:
        raise UnsupportedStoredType(
            f"unsupported stored dataset type: {record_type.__name__}"
        ) from exc


def _object_id(record: StoredDatasetObject) -> str:
    if isinstance(record, RawObservation):
        return str(record.observation_id)
    if isinstance(record, DatasetLock):
        return str(record.lock_id)
    if isinstance(record, MarketBar):
        return str(record.bar_id)
    if isinstance(record, RealCsvSourceDeclaration):
        return str(record.provenance_id)
    if isinstance(record, RealCsvAdmissionRecord):
        return str(record.admission_id)
    if isinstance(record, ResearchDatasetEligibilityPolicy):
        return str(record.policy_id)
    if isinstance(record, ResearchDatasetEligibilityRecord):
        return str(record.eligibility_id)
    if isinstance(record, ExperimentSpecification):
        return str(record.experiment_id)
    if isinstance(record, ExperimentAuthorizationPolicy):
        return str(record.policy_id)
    if isinstance(record, ExperimentAuthorizationRecord):
        return str(record.authorization_id)
    if isinstance(record, ExperimentReplayContract):
        return str(record.engine_id)
    if isinstance(record, ExperimentResultArtifact):
        return str(record.artifact_id)
    if isinstance(record, ExperimentRunRecord):
        return str(record.run_id)
    if isinstance(record, StrategyDefinition):
        return str(record.strategy_id)
    if isinstance(record, BacktestResultArtifact):
        return str(record.artifact_id)
    if isinstance(record, BacktestRunRecord):
        return str(record.run_id)
    if isinstance(record, ValidationPlan):
        return str(record.validation_plan_id)
    if isinstance(record, ScientificValidationResult):
        return str(record.validation_result_id)
    if isinstance(record, ValidationRunRecord):
        return str(record.validation_run_id)
    if isinstance(record, RobustnessValidationPlan):
        return str(record.robustness_plan_id)
    if isinstance(record, RobustnessValidationResult):
        return str(record.robustness_result_id)
    if isinstance(record, RobustnessValidationRunRecord):
        return str(record.robustness_run_id)
    if isinstance(record, OptimizationSearchSpace):
        return str(record.search_space_id)
    if isinstance(record, OptimizationPlan):
        return str(record.optimization_plan_id)
    if isinstance(record, OptimizationCandidateDefinition):
        return str(record.candidate_id)
    if isinstance(record, OptimizationCandidateResult):
        return str(record.candidate_id)
    if isinstance(record, OptimizationTrialRecord):
        return str(record.trial_id)
    if isinstance(record, OptimizationSelectionResult):
        return str(record.selection_result_id)
    if isinstance(record, OptimizationRunRecord):
        return str(record.optimization_run_id)
    if isinstance(record, PineStrategySourceArtifact):
        return str(record.pine_artifact_id)
    if isinstance(record, PineStrategyIntakeRecord):
        return str(record.intake_run_id)
    if isinstance(record, ParityTolerancePolicy):
        return str(record.policy_id)
    if isinstance(record, PineExecutionEvidence):
        return str(record.evidence_id)
    if isinstance(record, PinePythonParityResult):
        return str(record.parity_result_id)
    if isinstance(record, PinePythonParityRunRecord):
        return str(record.parity_run_id)
    return str(record.dataset_id)


def repository_key(record: StoredDatasetObject) -> RepositoryObjectKey:
    """Return the immutable type/version/fingerprint address for a supported object."""
    object_type = _stored_type(type(record))
    return RepositoryObjectKey(object_type, record.version, fingerprint_record(record))


class LocalDatasetRepository:
    """Exact-key local store; persistence records neither trust nor authority."""

    def __init__(self, *, root: Path, allowed_root: Path) -> None:
        self._allowed_root = self._validate_allowed_root(allowed_root)
        self._root = self._initialize_root(root)

    @property
    def root(self) -> Path:
        return self._root

    @staticmethod
    def _require_absolute_clean(path: Path, name: str) -> None:
        if not isinstance(path, Path) or not path.is_absolute():
            raise InvalidRepositoryPath(f"{name} must be an explicit absolute Path")
        if ".." in path.parts:
            raise InvalidRepositoryPath(f"{name} cannot contain traversal")

    @classmethod
    def _validate_allowed_root(cls, allowed_root: Path) -> Path:
        cls._require_absolute_clean(allowed_root, "allowed_root")
        if allowed_root.is_symlink() or not allowed_root.is_dir():
            raise InvalidRepositoryPath("allowed_root must be an existing non-symlink directory")
        return allowed_root.resolve(strict=True)

    def _initialize_root(self, root: Path) -> Path:
        self._require_absolute_clean(root, "root")
        if root.is_symlink():
            raise InvalidRepositoryPath("repository root cannot be a symlink")
        try:
            parent = root.parent.resolve(strict=True)
            parent.relative_to(self._allowed_root)
        except (FileNotFoundError, ValueError) as exc:
            raise InvalidRepositoryPath("repository root parent is outside allowed_root") from exc
        if root.exists():
            if not root.is_dir():
                raise InvalidRepositoryPath("repository root must be a directory")
        else:
            root.mkdir(mode=0o700)
        resolved = root.resolve(strict=True)
        try:
            resolved.relative_to(self._allowed_root)
        except ValueError as exc:
            raise InvalidRepositoryPath("repository root resolves outside allowed_root") from exc
        return resolved

    def _assert_root_stable(self) -> None:
        if self._root.is_symlink() or not self._root.is_dir():
            raise InvalidRepositoryPath("repository root changed or is unsafe")
        if self._root.resolve(strict=True) != self._root:
            raise InvalidRepositoryPath("repository root resolution changed")

    @staticmethod
    def _ensure_directory(path: Path) -> None:
        with suppress(FileExistsError):
            path.mkdir(mode=0o700)
        if path.is_symlink() or not path.is_dir():
            raise InvalidRepositoryPath("repository path component is unsafe")

    def _object_directory(self, key: RepositoryObjectKey, *, create: bool) -> Path:
        self._assert_root_stable()
        paths = (
            self._root / "objects",
            self._root / "objects" / key.object_type.value,
            self._root / "objects" / key.object_type.value / f"v{key.object_version.number}",
        )
        if create:
            for path in paths:
                self._ensure_directory(path)
        else:
            for path in paths:
                if path.exists() and (path.is_symlink() or not path.is_dir()):
                    raise InvalidRepositoryPath("repository path component is unsafe")
        directory = paths[-1]
        try:
            directory.resolve(strict=create).relative_to(self._root)
        except (FileNotFoundError, ValueError) as exc:
            raise InvalidRepositoryPath("object directory escapes repository root") from exc
        return directory

    def path_for(self, key: RepositoryObjectKey) -> Path:
        """Expose the exact immutable location for audit; it grants no write authority."""
        directory = self._object_directory(key, create=False)
        digest = key.fingerprint.removeprefix("sha256:")
        filename = f"{digest}.json"
        if not re.fullmatch(r"[0-9a-f]{64}\.json", filename):
            raise InvalidRepositoryPath("repository filename is invalid")
        path = directory / filename
        try:
            path.parent.resolve(strict=False).relative_to(self._root)
        except ValueError as exc:
            raise InvalidRepositoryPath("object path escapes repository root") from exc
        return path

    @staticmethod
    def _read_exact_bytes(path: Path) -> bytes:
        if path.is_symlink():
            raise InvalidRepositoryPath("stored object cannot be a symlink")
        flags = os.O_RDONLY
        if hasattr(os, "O_NOFOLLOW"):
            flags |= os.O_NOFOLLOW
        try:
            descriptor = os.open(path, flags)
        except FileNotFoundError as exc:
            raise RepositoryNotFound("exact repository object was not found") from exc
        except OSError as exc:
            if exc.errno == errno.ELOOP:
                raise InvalidRepositoryPath("stored object cannot be a symlink") from exc
            raise InvalidRepositoryPath("stored object cannot be opened safely") from exc
        try:
            metadata = os.fstat(descriptor)
            if not stat.S_ISREG(metadata.st_mode):
                raise InvalidRepositoryPath("stored object must be a regular file")
            if metadata.st_size > _MAX_OBJECT_BYTES:
                raise RepositoryIntegrityFailure("stored object exceeds bounded byte limit")
            with os.fdopen(descriptor, "rb", closefd=False) as stream:
                data = stream.read(_MAX_OBJECT_BYTES + 1)
            if len(data) > _MAX_OBJECT_BYTES:
                raise RepositoryIntegrityFailure("stored object exceeds bounded byte limit")
            return data
        finally:
            os.close(descriptor)

    @staticmethod
    def _sync_directory(path: Path) -> None:
        if not hasattr(os, "O_DIRECTORY"):
            return
        descriptor = os.open(path, os.O_RDONLY | os.O_DIRECTORY)
        try:
            os.fsync(descriptor)
        finally:
            os.close(descriptor)

    def store(self, record: StoredDatasetObject) -> RepositoryWriteResult:
        if type(record) not in _TYPE_TO_STORAGE:
            raise UnsupportedStoredType(f"unsupported stored dataset type: {type(record).__name__}")
        key = repository_key(record)
        canonical_bytes = encode(cast(GovernedRecord, record))
        if len(canonical_bytes) > _MAX_OBJECT_BYTES:
            raise RepositoryIntegrityFailure("canonical object exceeds bounded byte limit")
        verify_integrity(cast(GovernedRecord, record), key.fingerprint)
        directory = self._object_directory(key, create=True)
        destination = directory / key.relative_path.name
        if destination.exists() or destination.is_symlink():
            existing = self._read_exact_bytes(destination)
            status = (
                RepositoryWriteStatus.ALREADY_PRESENT_IDENTICAL
                if hmac.compare_digest(existing, canonical_bytes)
                else RepositoryWriteStatus.REJECTED_CONFLICT
            )
            result = RepositoryWriteResult(
                status, key, _object_id(record), key.fingerprint, len(canonical_bytes)
            )
            if status is RepositoryWriteStatus.REJECTED_CONFLICT:
                raise RepositoryConflict(result)
            return result

        temporary_path: Path | None = None
        try:
            with tempfile.NamedTemporaryFile(
                mode="wb", dir=directory, prefix=".pending-", suffix=".json", delete=False
            ) as temporary:
                temporary_path = Path(temporary.name)
                temporary.write(canonical_bytes)
                temporary.flush()
                os.fsync(temporary.fileno())
            try:
                os.link(temporary_path, destination)
            except FileExistsError:
                existing = self._read_exact_bytes(destination)
                status = (
                    RepositoryWriteStatus.ALREADY_PRESENT_IDENTICAL
                    if hmac.compare_digest(existing, canonical_bytes)
                    else RepositoryWriteStatus.REJECTED_CONFLICT
                )
                result = RepositoryWriteResult(
                    status, key, _object_id(record), key.fingerprint, len(canonical_bytes)
                )
                if status is RepositoryWriteStatus.REJECTED_CONFLICT:
                    raise RepositoryConflict(result) from None
                return result
            self._sync_directory(directory)
        finally:
            if temporary_path is not None:
                with suppress(FileNotFoundError):
                    temporary_path.unlink()
        return RepositoryWriteResult(
            RepositoryWriteStatus.STORED_NEW,
            key,
            _object_id(record),
            key.fingerprint,
            len(canonical_bytes),
        )

    def load[T: StoredDatasetObject](
        self, key: RepositoryObjectKey, expected_type: type[T]
    ) -> RepositoryReadResult[T]:
        expected_storage_type = _stored_type(cast(type[StoredDatasetObject], expected_type))
        if key.object_type is not expected_storage_type:
            raise RepositoryTypeMismatch("requested type does not match repository key")
        path = self.path_for(key)
        data = self._read_exact_bytes(path)
        try:
            record = cast(T, decode(data, cast(Any, expected_type)))
        except InvalidSerialization as exc:
            if str(exc) == "governed record type mismatch":
                raise RepositoryTypeMismatch("stored canonical type does not match key") from exc
            raise RepositoryIntegrityFailure("stored canonical bytes are invalid") from exc
        if record.version != key.object_version:
            raise RepositoryVersionMismatch("stored object version does not match key")
        try:
            verify_integrity(cast(GovernedRecord, record), key.fingerprint)
        except IntegrityError as exc:
            raise RepositoryIntegrityFailure(
                "stored canonical content does not match repository key"
            ) from exc
        if not hmac.compare_digest(encode(cast(GovernedRecord, record)), data):
            raise RepositoryIntegrityFailure("stored bytes are not the exact canonical object")
        return RepositoryReadResult(RepositoryReadStatus.FOUND_VERIFIED, key, record, len(data))


def _exact_reference(
    object_id: DatasetId | DatasetLockId,
    version: ObjectVersion,
    record: StoredDatasetObject,
) -> TraceabilityRef:
    return TraceabilityRef(object_id, version, fingerprint_record(cast(GovernedRecord, record)))


def _bar_reference(bar: MarketBar) -> TraceabilityRef:
    return TraceabilityRef(bar.bar_id, bar.version, fingerprint_record(bar))


def verify_dataset_lineage(
    *,
    raw_manifest: DatasetManifest,
    raw_lock: DatasetLock,
    bars: tuple[MarketBar, ...],
    normalized_manifest: NormalizedBarManifest,
    normalized_lock: DatasetLock,
) -> DatasetLineageVerification:
    """Verify exact existing raw-to-normalized references without granting acceptance."""
    raw_manifest_ref = _exact_reference(raw_manifest.dataset_id, raw_manifest.version, raw_manifest)
    if raw_lock.dataset_ref != raw_manifest_ref or raw_lock.manifest_ref != raw_manifest_ref:
        raise DatasetLineageMismatch("raw lock does not bind the exact raw manifest")
    raw_lock_ref = _exact_reference(raw_lock.lock_id, raw_lock.version, raw_lock)
    if normalized_manifest.raw_dataset_lock_ref != raw_lock_ref:
        raise DatasetLineageMismatch("normalized manifest does not bind the exact raw lock")
    normalized_manifest_ref = _exact_reference(
        normalized_manifest.dataset_id,
        normalized_manifest.version,
        normalized_manifest,
    )
    if (
        normalized_lock.dataset_ref != normalized_manifest_ref
        or normalized_lock.manifest_ref != normalized_manifest_ref
    ):
        raise DatasetLineageMismatch("normalized lock does not bind the exact normalized manifest")
    if not bars:
        raise DatasetLineageMismatch("normalized lineage requires exact bars")
    expected_bar_refs = tuple(
        sorted(
            (_bar_reference(bar) for bar in bars),
            key=lambda ref: (
                str(ref.object_id),
                ref.version.number,
                ref.expected_fingerprint or "",
            ),
        )
    )
    if expected_bar_refs != normalized_manifest.bar_refs:
        raise DatasetLineageMismatch("normalized manifest bar membership is not exact")
    raw_observation_refs = set(raw_manifest.observation_refs)
    if any(bar.source_observation_ref not in raw_observation_refs for bar in bars):
        raise DatasetLineageMismatch("a bar source observation is absent from raw manifest")
    raw_source_refs = set(raw_manifest.source_refs)
    if any(bar.source_ref not in raw_source_refs for bar in bars):
        raise DatasetLineageMismatch("a bar source is absent from raw manifest")
    raw_instrument_refs = set(raw_manifest.instrument_refs)
    if any(bar.instrument_ref not in raw_instrument_refs for bar in bars):
        raise DatasetLineageMismatch("a bar instrument is absent from raw manifest")

    def exact_refs(refs: tuple[TraceabilityRef, ...]) -> tuple[TraceabilityRef, ...]:
        return tuple(
            sorted(
                set(refs),
                key=lambda ref: (
                    str(ref.object_id),
                    ref.version.number,
                    ref.expected_fingerprint or "",
                ),
            )
        )

    if exact_refs(tuple(bar.source_ref for bar in bars)) != normalized_manifest.source_refs:
        raise DatasetLineageMismatch("normalized source scope does not match bars")
    if exact_refs(tuple(bar.instrument_ref for bar in bars)) != normalized_manifest.instrument_refs:
        raise DatasetLineageMismatch("normalized instrument scope does not match bars")
    if exact_refs(tuple(bar.timeframe_ref for bar in bars)) != normalized_manifest.timeframe_refs:
        raise DatasetLineageMismatch("normalized timeframe scope does not match bars")
    if any(bar.schema_ref != normalized_manifest.schema_ref for bar in bars):
        raise DatasetLineageMismatch("normalized schema does not match bars")
    if any(bar.normalization_version != normalized_manifest.normalization_version for bar in bars):
        raise DatasetLineageMismatch("normalization version does not match bars")
    return DatasetLineageVerification(
        DatasetLineageStatus.VERIFIED,
        fingerprint_record(raw_manifest),
        fingerprint_record(raw_lock),
        fingerprint_record(normalized_manifest),
        fingerprint_record(normalized_lock),
        tuple(fingerprint_record(bar) for bar in bars),
    )
