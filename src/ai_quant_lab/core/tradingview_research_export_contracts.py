"""Governed contracts for deterministic manual TradingView research export."""

from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass
from enum import StrEnum
from typing import Final

from ai_quant_lab.core.data import DatasetLockId, InstrumentId
from ai_quant_lab.core.market_data import TimeframeId
from ai_quant_lab.core.model import (
    ArtifactId,
    AuthorityBindingId,
    DatasetId,
    ExecutionState,
    ObjectVersion,
    ProvenanceId,
    RunId,
    TraceabilityRef,
    ValidationId,
)
from ai_quant_lab.core.pine_strategy_contracts import RepaintAssessmentStatus
from ai_quant_lab.core.research_eligibility_contracts import DeploymentAuthorizationStatus

_V1 = ObjectVersion(1)
_FP: Final = re.compile(r"^sha256:[0-9a-f]{64}$")
_FILENAME: Final = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,95}$")


class TradingViewResearchExportContractError(ValueError):
    pass


class TradingViewResearchExportReadiness(StrEnum):
    READY_FOR_MANUAL_TRADINGVIEW_RESEARCH = "READY_FOR_MANUAL_TRADINGVIEW_RESEARCH"


class TradingViewResearchExportSafetyStatus(StrEnum):
    STATIC_SAFETY_PASS = "STATIC_SAFETY_PASS"


class TradingViewResearchExportRuntimeStatus(StrEnum):
    NOT_VERIFIED_ON_TRADINGVIEW = "NOT_VERIFIED_ON_TRADINGVIEW"


@dataclass(frozen=True, slots=True)
class TradingViewResearchExportPackage:
    export_id: ArtifactId
    version: ObjectVersion
    export_run_id: RunId
    pine_artifact_ref: TraceabilityRef
    strategy_ref: TraceabilityRef
    backtest_ref: TraceabilityRef
    scientific_validation_ref: TraceabilityRef
    robustness_ref: TraceabilityRef
    optimization_selection_ref: TraceabilityRef | None
    instrument_ref: TraceabilityRef
    timeframe_ref: TraceabilityRef
    normalized_manifest_ref: TraceabilityRef
    normalized_lock_ref: TraceabilityRef
    generation_input_fingerprint: str
    safety_assessment_id: ArtifactId
    safety_input_fingerprint: str
    safety_status: TradingViewResearchExportSafetyStatus
    static_repaint_status: str
    artifact_repaint_assessment: RepaintAssessmentStatus
    runtime_status: TradingViewResearchExportRuntimeStatus
    pine_source_sha256: str
    pine_source_byte_size: int
    pine_filename: str
    manifest_filename: str
    pine_source_text: str
    instrument_symbol: str
    timeframe_token: str
    strategy_parameters: tuple[tuple[str, str], ...]
    manual_steps: tuple[str, ...]
    readiness: TradingViewResearchExportReadiness
    export_authority_ref: TraceabilityRef
    provenance_ref: TraceabilityRef
    deployment_authorization: DeploymentAuthorizationStatus
    execution_state: ExecutionState
    contract_version: ObjectVersion = _V1

    def __post_init__(self) -> None:
        if (
            not isinstance(self.export_id, ArtifactId)
            or self.version != _V1
            or not isinstance(self.export_run_id, RunId)
            or self.contract_version != _V1
            or not isinstance(self.generation_input_fingerprint, str)
            or _FP.fullmatch(self.generation_input_fingerprint) is None
            or not isinstance(self.safety_assessment_id, ArtifactId)
            or not isinstance(self.safety_input_fingerprint, str)
            or _FP.fullmatch(self.safety_input_fingerprint) is None
            or self.safety_status is not TradingViewResearchExportSafetyStatus.STATIC_SAFETY_PASS
            or self.static_repaint_status != "NO_STATIC_REPAINT_HAZARD_DETECTED"
            or self.artifact_repaint_assessment is not RepaintAssessmentStatus.NOT_EVALUATED
            or self.runtime_status
            is not TradingViewResearchExportRuntimeStatus.NOT_VERIFIED_ON_TRADINGVIEW
            or not isinstance(self.pine_source_sha256, str)
            or _FP.fullmatch(self.pine_source_sha256) is None
            or isinstance(self.pine_source_byte_size, bool)
            or not isinstance(self.pine_source_byte_size, int)
            or self.pine_source_byte_size <= 0
            or not isinstance(self.pine_source_text, str)
            or not self.pine_source_text
            or len(self.pine_source_text.encode("utf-8")) != self.pine_source_byte_size
            or (
                "sha256:" + hashlib.sha256(self.pine_source_text.encode("utf-8")).hexdigest()
                != self.pine_source_sha256
            )
            or not isinstance(self.instrument_symbol, str)
            or not self.instrument_symbol
            or not isinstance(self.timeframe_token, str)
            or not self.timeframe_token
            or self.readiness
            is not TradingViewResearchExportReadiness.READY_FOR_MANUAL_TRADINGVIEW_RESEARCH
        ):
            raise TradingViewResearchExportContractError(
                "invalid TradingView research export package"
            )

        for reference, expected, field in (
            (self.pine_artifact_ref, ArtifactId, "pine_artifact_ref"),
            (self.strategy_ref, ArtifactId, "strategy_ref"),
            (self.backtest_ref, ArtifactId, "backtest_ref"),
            (self.scientific_validation_ref, ValidationId, "scientific_validation_ref"),
            (self.robustness_ref, ArtifactId, "robustness_ref"),
            (self.instrument_ref, InstrumentId, "instrument_ref"),
            (self.timeframe_ref, TimeframeId, "timeframe_ref"),
            (self.normalized_manifest_ref, DatasetId, "normalized_manifest_ref"),
            (self.normalized_lock_ref, DatasetLockId, "normalized_lock_ref"),
            (self.export_authority_ref, AuthorityBindingId, "export_authority_ref"),
            (self.provenance_ref, ProvenanceId, "provenance_ref"),
        ):
            _exact(reference, expected, field)
        if self.optimization_selection_ref is not None:
            _exact(
                self.optimization_selection_ref,
                ArtifactId,
                "optimization_selection_ref",
            )

        for value, suffix, field in (
            (self.pine_filename, ".pine", "pine_filename"),
            (self.manifest_filename, ".json", "manifest_filename"),
        ):
            if (
                not isinstance(value, str)
                or _FILENAME.fullmatch(value) is None
                or not value.endswith(suffix)
                or "/" in value
                or "\\" in value
                or ".." in value
            ):
                raise TradingViewResearchExportContractError(
                    f"{field} must be a bounded local filename"
                )

        names = tuple(name for name, _value in self.strategy_parameters)
        if (
            not self.strategy_parameters
            or names != tuple(sorted(names))
            or len(names) != len(set(names))
            or any(
                not isinstance(name, str) or not name or not isinstance(value, str) or not value
                for name, value in self.strategy_parameters
            )
        ):
            raise TradingViewResearchExportContractError(
                "strategy_parameters must be sorted unique non-empty text pairs"
            )
        if (
            not self.manual_steps
            or len(self.manual_steps) != len(set(self.manual_steps))
            or any(not isinstance(step, str) or not step.strip() for step in self.manual_steps)
        ):
            raise TradingViewResearchExportContractError(
                "manual_steps must be unique non-empty instructions"
            )
        if (
            self.deployment_authorization is not DeploymentAuthorizationStatus.NOT_AUTHORIZED
            or self.execution_state is not ExecutionState.PLANNED_CLOSED
        ):
            raise TradingViewResearchExportContractError(
                "research export cannot authorize deployment or execution"
            )


def _exact(
    reference: TraceabilityRef,
    expected_type: type[object],
    field: str,
) -> None:
    if (
        not isinstance(reference, TraceabilityRef)
        or reference.expected_fingerprint is None
        or not isinstance(reference.object_id, expected_type)
    ):
        raise TradingViewResearchExportContractError(
            f"{field} must be an exact fingerprint-bearing {expected_type.__name__} reference"
        )
