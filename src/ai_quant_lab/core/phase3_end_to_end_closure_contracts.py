"""Phase 3 end-to-end closure contracts for the bounded manual TradingView research path."""

from __future__ import annotations

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
from ai_quant_lab.core.tradingview_research_export_contracts import (
    TradingViewResearchExportRuntimeStatus,
)

_V1 = ObjectVersion(1)
_FP = re.compile(r"^sha256:[0-9a-f]{64}$")


class Phase3EndToEndClosureContractError(ValueError):
    pass


class Phase3EndToEndStage(StrEnum):
    REAL_CSV_ADMITTED = "REAL_CSV_ADMITTED"
    DATASET_ELIGIBLE = "DATASET_ELIGIBLE"
    EXPERIMENT_AUTHORIZED = "EXPERIMENT_AUTHORIZED"
    BACKTEST_COMPLETED = "BACKTEST_COMPLETED"
    SCIENTIFIC_VALIDATION_PASSED = "SCIENTIFIC_VALIDATION_PASSED"
    ROBUSTNESS_PASSED = "ROBUSTNESS_PASSED"
    OPTIMIZATION_SELECTED = "OPTIMIZATION_SELECTED"
    PINE_GENERATED = "PINE_GENERATED"
    PINE_INTAKE_ACCEPTED = "PINE_INTAKE_ACCEPTED"
    STATIC_SAFETY_PASSED = "STATIC_SAFETY_PASSED"
    TRADINGVIEW_EXPORT_READY = "TRADINGVIEW_EXPORT_READY"


class Phase3EndToEndState(StrEnum):
    READY_FOR_MANUAL_TRADINGVIEW_RESEARCH = "READY_FOR_MANUAL_TRADINGVIEW_RESEARCH"


def _exact(reference: TraceabilityRef, expected: type[object], field: str) -> None:
    if (
        not isinstance(reference, TraceabilityRef)
        or reference.expected_fingerprint is None
        or not isinstance(reference.object_id, expected)
    ):
        raise Phase3EndToEndClosureContractError(
            f"{field} must be an exact fingerprint-bearing {expected.__name__} reference"
        )


@dataclass(frozen=True, slots=True)
class Phase3EndToEndClosureRecord:
    closure_id: ArtifactId
    version: ObjectVersion
    closure_run_id: RunId
    source_declaration_ref: TraceabilityRef
    admission_ref: TraceabilityRef
    eligibility_ref: TraceabilityRef
    authorization_ref: TraceabilityRef
    strategy_ref: TraceabilityRef
    backtest_ref: TraceabilityRef
    scientific_validation_ref: TraceabilityRef
    robustness_ref: TraceabilityRef
    optimization_selection_ref: TraceabilityRef | None
    pine_artifact_ref: TraceabilityRef
    safety_assessment_id: ArtifactId
    safety_input_fingerprint: str
    export_ref: TraceabilityRef
    stages: tuple[Phase3EndToEndStage, ...]
    final_state: Phase3EndToEndState
    runtime_status: TradingViewResearchExportRuntimeStatus
    closure_authority_ref: TraceabilityRef
    provenance_ref: TraceabilityRef
    deployment_authorization: DeploymentAuthorizationStatus
    execution_state: ExecutionState
    contract_version: ObjectVersion = _V1

    def __post_init__(self) -> None:
        if (
            not isinstance(self.closure_id, ArtifactId)
            or self.version != _V1
            or not isinstance(self.closure_run_id, RunId)
            or self.contract_version != _V1
            or not isinstance(self.safety_assessment_id, ArtifactId)
            or not isinstance(self.safety_input_fingerprint, str)
            or _FP.fullmatch(self.safety_input_fingerprint) is None
            or self.final_state is not Phase3EndToEndState.READY_FOR_MANUAL_TRADINGVIEW_RESEARCH
            or self.runtime_status
            is not TradingViewResearchExportRuntimeStatus.NOT_VERIFIED_ON_TRADINGVIEW
            or self.deployment_authorization is not DeploymentAuthorizationStatus.NOT_AUTHORIZED
            or self.execution_state is not ExecutionState.PLANNED_CLOSED
        ):
            raise Phase3EndToEndClosureContractError("invalid Phase 3 end-to-end closure record")

        for reference, expected, field in (
            (self.source_declaration_ref, ProvenanceId, "source_declaration_ref"),
            (self.admission_ref, ArtifactId, "admission_ref"),
            (self.eligibility_ref, ArtifactId, "eligibility_ref"),
            (self.authorization_ref, ArtifactId, "authorization_ref"),
            (self.strategy_ref, ArtifactId, "strategy_ref"),
            (self.backtest_ref, ArtifactId, "backtest_ref"),
            (self.scientific_validation_ref, ValidationId, "scientific_validation_ref"),
            (self.robustness_ref, ArtifactId, "robustness_ref"),
            (self.pine_artifact_ref, ArtifactId, "pine_artifact_ref"),
            (self.export_ref, ArtifactId, "export_ref"),
            (self.closure_authority_ref, AuthorityBindingId, "closure_authority_ref"),
            (self.provenance_ref, ProvenanceId, "provenance_ref"),
        ):
            _exact(reference, expected, field)

        if self.optimization_selection_ref is not None:
            _exact(
                self.optimization_selection_ref,
                ArtifactId,
                "optimization_selection_ref",
            )

        base = (
            Phase3EndToEndStage.REAL_CSV_ADMITTED,
            Phase3EndToEndStage.DATASET_ELIGIBLE,
            Phase3EndToEndStage.EXPERIMENT_AUTHORIZED,
            Phase3EndToEndStage.BACKTEST_COMPLETED,
            Phase3EndToEndStage.SCIENTIFIC_VALIDATION_PASSED,
            Phase3EndToEndStage.ROBUSTNESS_PASSED,
        )
        tail = (
            Phase3EndToEndStage.PINE_GENERATED,
            Phase3EndToEndStage.PINE_INTAKE_ACCEPTED,
            Phase3EndToEndStage.STATIC_SAFETY_PASSED,
            Phase3EndToEndStage.TRADINGVIEW_EXPORT_READY,
        )
        expected_stages = (
            (*base, Phase3EndToEndStage.OPTIMIZATION_SELECTED, *tail)
            if self.optimization_selection_ref is not None
            else (*base, *tail)
        )
        if self.stages != expected_stages:
            raise Phase3EndToEndClosureContractError(
                "Phase 3 closure stages are not in canonical current-order sequence"
            )
