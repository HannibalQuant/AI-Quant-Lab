"""Immutable contracts for bounded governed Pine strategy intake."""

from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass
from enum import StrEnum

from ai_quant_lab.core.model import (
    ArtifactId,
    AuthorityBindingId,
    ExecutionState,
    ObjectVersion,
    ProvenanceId,
    RunId,
    TraceabilityRef,
    ValidationId,
)
from ai_quant_lab.core.research_eligibility_contracts import DeploymentAuthorizationStatus


class PineStrategyContractError(ValueError):
    pass


class PineLanguageVersion(StrEnum):
    PINE_V6 = "PINE_V6"


class PineScriptKind(StrEnum):
    STRATEGY = "STRATEGY"
    INDICATOR = "INDICATOR"
    UNKNOWN = "UNKNOWN"


class PineIntakeStatus(StrEnum):
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"
    INCOMPLETE = "INCOMPLETE"
    UNSUPPORTED = "UNSUPPORTED"


class PineIntakeReasonCode(StrEnum):
    ACCEPTED_BOUNDED_STATIC_INTAKE = "ACCEPTED_BOUNDED_STATIC_INTAKE"
    AUTHORITY_REF_MISMATCH = "AUTHORITY_REF_MISMATCH"
    BINARY_CONTENT = "BINARY_CONTENT"
    EMPTY_SOURCE = "EMPTY_SOURCE"
    EVIDENCE_REF_MISMATCH = "EVIDENCE_REF_MISMATCH"
    INDICATOR_NOT_STRATEGY = "INDICATOR_NOT_STRATEGY"
    INVALID_ENCODING = "INVALID_ENCODING"
    MISSING_STATIC_SETTING = "MISSING_STATIC_SETTING"
    MISSING_VERSION = "MISSING_VERSION"
    MULTIPLE_TOP_LEVEL_DECLARATIONS = "MULTIPLE_TOP_LEVEL_DECLARATIONS"
    MULTIPLE_VERSION_DECLARATIONS = "MULTIPLE_VERSION_DECLARATIONS"
    NUL_BYTE_PRESENT = "NUL_BYTE_PRESENT"
    SCRIPT_KIND_UNKNOWN = "SCRIPT_KIND_UNKNOWN"
    SOURCE_HASH_MISMATCH = "SOURCE_HASH_MISMATCH"
    SOURCE_TOO_LARGE = "SOURCE_TOO_LARGE"
    STATIC_SETTING_MISMATCH = "STATIC_SETTING_MISMATCH"
    STATIC_TITLE_REQUIRED = "STATIC_TITLE_REQUIRED"
    STRATEGY_REF_MISMATCH = "STRATEGY_REF_MISMATCH"
    UNSUPPORTED_FEATURE = "UNSUPPORTED_FEATURE"
    UNSUPPORTED_VERSION = "UNSUPPORTED_VERSION"


class PineSemanticParityStatus(StrEnum):
    NOT_EVALUATED = "NOT_EVALUATED"


class RepaintAssessmentStatus(StrEnum):
    NOT_EVALUATED = "NOT_EVALUATED"


class PineDefaultQuantityType(StrEnum):
    STRATEGY_CASH = "strategy.cash"


_V1 = ObjectVersion(1)
_SHA256 = re.compile(r"sha256:[0-9a-f]{64}")
_DECIMAL = re.compile(r"(?:0|[1-9][0-9]*)(?:\.[0-9]+)?")


def normalize_pine_source(source_text: str) -> str:
    """Normalize transport line endings only; executable text otherwise remains exact."""
    return source_text.replace("\r\n", "\n").replace("\r", "\n")


def pine_sha256(data: bytes) -> str:
    return f"sha256:{hashlib.sha256(data).hexdigest()}"


def _exact(reference: TraceabilityRef, identifier: type, field: str) -> None:
    if (
        not isinstance(reference, TraceabilityRef)
        or not isinstance(reference.object_id, identifier)
        or reference.expected_fingerprint is None
    ):
        raise PineStrategyContractError(f"{field} must be an exact fingerprint reference")


def _optional_exact(reference: TraceabilityRef | None, identifier: type, field: str) -> None:
    if reference is not None:
        _exact(reference, identifier, field)


@dataclass(frozen=True, slots=True)
class PineStrategySourceArtifact:
    pine_artifact_id: ArtifactId
    version: ObjectVersion
    pine_language_version: PineLanguageVersion
    source_text: str
    normalized_source_text: str
    source_sha256: str
    normalized_source_sha256: str
    source_byte_size: int
    script_kind: PineScriptKind
    declared_script_title: str
    pyramiding: int
    process_orders_on_close: bool
    calc_on_every_tick: bool
    default_qty_type: PineDefaultQuantityType
    default_qty_value: str
    strategy_definition_ref: TraceabilityRef
    optimization_candidate_definition_ref: TraceabilityRef | None
    optimization_candidate_result_ref: TraceabilityRef | None
    optimization_selection_ref: TraceabilityRef | None
    source_backtest_result_ref: TraceabilityRef
    source_scientific_validation_ref: TraceabilityRef
    source_robustness_result_ref: TraceabilityRef
    provenance_ref: TraceabilityRef
    authority_ref: TraceabilityRef
    semantic_parity: PineSemanticParityStatus
    repaint_assessment: RepaintAssessmentStatus
    deployment_authorization: DeploymentAuthorizationStatus
    execution_state: ExecutionState
    contract_version: ObjectVersion

    def __post_init__(self) -> None:
        if (
            not isinstance(self.pine_artifact_id, ArtifactId)
            or self.version != _V1
            or self.contract_version != _V1
            or self.pine_language_version is not PineLanguageVersion.PINE_V6
            or self.script_kind is not PineScriptKind.STRATEGY
            or not isinstance(self.source_text, str)
            or not self.source_text
            or not isinstance(self.normalized_source_text, str)
            or not self.normalized_source_text
            or not isinstance(self.declared_script_title, str)
            or not self.declared_script_title
            or self.pyramiding != 0
            or self.process_orders_on_close
            or self.calc_on_every_tick
            or self.default_qty_type is not PineDefaultQuantityType.STRATEGY_CASH
            or not isinstance(self.default_qty_value, str)
            or not _DECIMAL.fullmatch(self.default_qty_value)
        ):
            raise PineStrategyContractError("unsupported Pine strategy source artifact")
        raw = self.source_text.encode("utf-8")
        normalized = normalize_pine_source(self.source_text)
        if self.normalized_source_text != normalized:
            raise PineStrategyContractError("normalized Pine source is not deterministic")
        if (
            isinstance(self.source_byte_size, bool)
            or not isinstance(self.source_byte_size, int)
            or self.source_byte_size != len(raw)
            or self.source_sha256 != pine_sha256(raw)
            or self.normalized_source_sha256 != pine_sha256(normalized.encode("utf-8"))
            or not _SHA256.fullmatch(self.source_sha256)
            or not _SHA256.fullmatch(self.normalized_source_sha256)
        ):
            raise PineStrategyContractError("Pine source identity does not match exact content")
        _exact(self.strategy_definition_ref, ArtifactId, "strategy_definition_ref")
        optional = (
            self.optimization_candidate_definition_ref,
            self.optimization_candidate_result_ref,
            self.optimization_selection_ref,
        )
        if any(item is None for item in optional) and any(item is not None for item in optional):
            raise PineStrategyContractError("optimization binding must be complete or absent")
        _optional_exact(
            self.optimization_candidate_definition_ref,
            ArtifactId,
            "optimization_candidate_definition_ref",
        )
        _optional_exact(
            self.optimization_candidate_result_ref,
            ArtifactId,
            "optimization_candidate_result_ref",
        )
        _optional_exact(
            self.optimization_selection_ref,
            ArtifactId,
            "optimization_selection_ref",
        )
        _exact(self.source_backtest_result_ref, ArtifactId, "source_backtest_result_ref")
        _exact(
            self.source_scientific_validation_ref,
            ValidationId,
            "source_scientific_validation_ref",
        )
        _exact(self.source_robustness_result_ref, ArtifactId, "source_robustness_result_ref")
        _exact(self.provenance_ref, ProvenanceId, "provenance_ref")
        _exact(self.authority_ref, AuthorityBindingId, "authority_ref")
        if (
            self.semantic_parity is not PineSemanticParityStatus.NOT_EVALUATED
            or self.repaint_assessment is not RepaintAssessmentStatus.NOT_EVALUATED
            or self.deployment_authorization is not DeploymentAuthorizationStatus.NOT_AUTHORIZED
            or self.execution_state is not ExecutionState.PLANNED_CLOSED
        ):
            raise PineStrategyContractError("Pine intake cannot grant downstream authority")


@dataclass(frozen=True, slots=True)
class PineStrategyIntakeRequest:
    intake_run_id: RunId
    requested_artifact_id: ArtifactId
    source_bytes: bytes
    strategy_definition_ref: TraceabilityRef
    optimization_candidate_definition_ref: TraceabilityRef | None
    optimization_candidate_result_ref: TraceabilityRef | None
    optimization_selection_ref: TraceabilityRef | None
    source_backtest_result_ref: TraceabilityRef
    source_scientific_validation_ref: TraceabilityRef
    source_robustness_result_ref: TraceabilityRef
    authority_ref: TraceabilityRef
    provenance_ref: TraceabilityRef
    contract_version: ObjectVersion = _V1

    def __post_init__(self) -> None:
        if (
            not isinstance(self.intake_run_id, RunId)
            or not isinstance(self.requested_artifact_id, ArtifactId)
            or not isinstance(self.source_bytes, bytes)
            or self.contract_version != _V1
        ):
            raise PineStrategyContractError("unsupported Pine intake request")
        _exact(self.strategy_definition_ref, ArtifactId, "strategy_definition_ref")
        optional = (
            self.optimization_candidate_definition_ref,
            self.optimization_candidate_result_ref,
            self.optimization_selection_ref,
        )
        if any(item is None for item in optional) and any(item is not None for item in optional):
            raise PineStrategyContractError(
                "optimization request binding must be complete or absent"
            )
        _optional_exact(
            self.optimization_candidate_definition_ref,
            ArtifactId,
            "optimization_candidate_definition_ref",
        )
        _optional_exact(
            self.optimization_candidate_result_ref,
            ArtifactId,
            "optimization_candidate_result_ref",
        )
        _optional_exact(
            self.optimization_selection_ref,
            ArtifactId,
            "optimization_selection_ref",
        )
        _exact(self.source_backtest_result_ref, ArtifactId, "source_backtest_result_ref")
        _exact(
            self.source_scientific_validation_ref,
            ValidationId,
            "source_scientific_validation_ref",
        )
        _exact(self.source_robustness_result_ref, ArtifactId, "source_robustness_result_ref")
        _exact(self.authority_ref, AuthorityBindingId, "authority_ref")
        _exact(self.provenance_ref, ProvenanceId, "provenance_ref")


@dataclass(frozen=True, slots=True)
class PineStrategyIntakeRecord:
    intake_run_id: RunId
    version: ObjectVersion
    requested_artifact_id: ArtifactId
    source_artifact_ref: TraceabilityRef | None
    source_sha256: str
    normalized_source_sha256: str | None
    source_byte_size: int
    input_fingerprint: str
    status: PineIntakeStatus
    reason_codes: tuple[PineIntakeReasonCode, ...]
    authority_ref: TraceabilityRef
    provenance_ref: TraceabilityRef
    deployment_authorization: DeploymentAuthorizationStatus
    execution_state: ExecutionState
    contract_version: ObjectVersion

    def __post_init__(self) -> None:
        if (
            not isinstance(self.intake_run_id, RunId)
            or self.version != _V1
            or not isinstance(self.requested_artifact_id, ArtifactId)
            or self.contract_version != _V1
            or not _SHA256.fullmatch(self.source_sha256)
            or (
                self.normalized_source_sha256 is not None
                and not _SHA256.fullmatch(self.normalized_source_sha256)
            )
            or isinstance(self.source_byte_size, bool)
            or not isinstance(self.source_byte_size, int)
            or self.source_byte_size < 0
            or not _SHA256.fullmatch(self.input_fingerprint)
            or not isinstance(self.status, PineIntakeStatus)
            or not self.reason_codes
            or tuple(sorted(self.reason_codes, key=lambda item: item.value)) != self.reason_codes
            or len(set(self.reason_codes)) != len(self.reason_codes)
        ):
            raise PineStrategyContractError("unsupported Pine intake record")
        if self.status is PineIntakeStatus.ACCEPTED:
            if (
                self.source_artifact_ref is None
                or self.normalized_source_sha256 is None
                or self.reason_codes
                != (PineIntakeReasonCode.ACCEPTED_BOUNDED_STATIC_INTAKE,)
            ):
                raise PineStrategyContractError("accepted Pine intake record is inconsistent")
            _exact(self.source_artifact_ref, ArtifactId, "source_artifact_ref")
        else:
            if self.source_artifact_ref is not None:
                raise PineStrategyContractError("failed Pine intake cannot reference a source artifact")
            if PineIntakeReasonCode.ACCEPTED_BOUNDED_STATIC_INTAKE in self.reason_codes:
                raise PineStrategyContractError("failed Pine intake cannot carry accepted reason")
        _exact(self.authority_ref, AuthorityBindingId, "authority_ref")
        _exact(self.provenance_ref, ProvenanceId, "provenance_ref")
        if (
            self.deployment_authorization is not DeploymentAuthorizationStatus.NOT_AUTHORIZED
            or self.execution_state is not ExecutionState.PLANNED_CLOSED
        ):
            raise PineStrategyContractError("Pine intake record cannot grant authority")