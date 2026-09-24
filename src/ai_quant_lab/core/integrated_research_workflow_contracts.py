"""Immutable contracts for the integrated Phase 3 research workflow."""

from __future__ import annotations

import re
from dataclasses import dataclass
from enum import StrEnum

from ai_quant_lab.core.model import (
    AgentId,
    ArtifactId,
    ExecutionState,
    ObjectVersion,
    RunId,
    TraceabilityRef,
)
from ai_quant_lab.core.pine_python_parity_contracts import PinePythonParityDecision
from ai_quant_lab.core.pine_strategy_contracts import RepaintAssessmentStatus
from ai_quant_lab.core.research_eligibility_contracts import DeploymentAuthorizationStatus


class IntegratedResearchWorkflowContractError(ValueError):
    pass


class IntegratedResearchWorkflowMode(StrEnum):
    DIRECT_STRATEGY = "DIRECT_STRATEGY"
    OPTIMIZED_STRATEGY = "OPTIMIZED_STRATEGY"


class AIStrategyProposalStatus(StrEnum):
    PROPOSED = "PROPOSED"
    REJECTED = "REJECTED"
    ACCEPTED_FOR_RESEARCH = "ACCEPTED_FOR_RESEARCH"


class ProposalAuthorityState(StrEnum):
    PROPOSAL_ONLY = "PROPOSAL_ONLY"


class IntegratedResearchWorkflowState(StrEnum):
    PROPOSAL_ACCEPTED = "PROPOSAL_ACCEPTED"
    EXPERIMENT_AUTHORIZED = "EXPERIMENT_AUTHORIZED"
    BACKTEST_COMPLETED = "BACKTEST_COMPLETED"
    SCIENTIFIC_VALIDATION_COMPLETED = "SCIENTIFIC_VALIDATION_COMPLETED"
    ROBUSTNESS_COMPLETED = "ROBUSTNESS_COMPLETED"
    OPTIMIZATION_COMPLETED = "OPTIMIZATION_COMPLETED"
    PINE_INTAKE_COMPLETED = "PINE_INTAKE_COMPLETED"
    PARITY_COMPLETED = "PARITY_COMPLETED"
    RESEARCH_HANDOFF_READY = "RESEARCH_HANDOFF_READY"
    RESEARCH_REJECTED = "RESEARCH_REJECTED"
    RESEARCH_INCONCLUSIVE = "RESEARCH_INCONCLUSIVE"


class ResearchHandoffReadiness(StrEnum):
    READY_FOR_HUMAN_RESEARCH_USE = "READY_FOR_HUMAN_RESEARCH_USE"
    NOT_READY = "NOT_READY"
    INCONCLUSIVE = "INCONCLUSIVE"


class WorkflowStage(StrEnum):
    PROPOSAL = "PROPOSAL"
    AUTHORIZATION = "AUTHORIZATION"
    BACKTEST = "BACKTEST"
    SCIENTIFIC_VALIDATION = "SCIENTIFIC_VALIDATION"
    ROBUSTNESS = "ROBUSTNESS"
    OPTIMIZATION = "OPTIMIZATION"
    PINE_INTAKE = "PINE_INTAKE"
    PARITY = "PARITY"
    HANDOFF = "HANDOFF"


class WorkflowStageOutcome(StrEnum):
    ACCEPTED = "ACCEPTED"
    AUTHORIZED = "AUTHORIZED"
    COMPLETED = "COMPLETED"
    PASS = "PASS"
    SELECTED = "SELECTED"
    MATCH = "MATCH"
    READY = "READY"
    FAIL = "FAIL"
    INCONCLUSIVE = "INCONCLUSIVE"


class WorkflowReasonCode(StrEnum):
    PROPOSAL_NOT_ACCEPTED = "PROPOSAL_NOT_ACCEPTED"
    EXPERIMENT_NOT_AUTHORIZED = "EXPERIMENT_NOT_AUTHORIZED"
    SCIENTIFIC_VALIDATION_FAILED = "SCIENTIFIC_VALIDATION_FAILED"
    SCIENTIFIC_VALIDATION_INCONCLUSIVE = "SCIENTIFIC_VALIDATION_INCONCLUSIVE"
    ROBUSTNESS_FAILED = "ROBUSTNESS_FAILED"
    ROBUSTNESS_INCONCLUSIVE = "ROBUSTNESS_INCONCLUSIVE"
    OPTIMIZATION_NOT_SELECTED = "OPTIMIZATION_NOT_SELECTED"
    PINE_INTAKE_FAILED = "PINE_INTAKE_FAILED"
    PARITY_MISMATCH = "PARITY_MISMATCH"
    PARITY_INCONCLUSIVE = "PARITY_INCONCLUSIVE"
    LINEAGE_MISMATCH = "LINEAGE_MISMATCH"
    AUTHORITY_MISMATCH = "AUTHORITY_MISMATCH"
    RESEARCH_HANDOFF_READY = "RESEARCH_HANDOFF_READY"


_V1 = ObjectVersion(1)
_FP = re.compile(r"sha256:[0-9a-f]{64}")


def _exact(ref: TraceabilityRef, field: str) -> None:
    if not isinstance(ref, TraceabilityRef) or ref.expected_fingerprint is None:
        raise IntegratedResearchWorkflowContractError(
            f"{field} must be an exact fingerprint-bearing reference"
        )


def _optional_exact(ref: TraceabilityRef | None, field: str) -> None:
    if ref is not None:
        _exact(ref, field)


@dataclass(frozen=True, slots=True)
class AIStrategyProposal:
    proposal_id: ArtifactId
    version: ObjectVersion
    proposing_agent_ref: TraceabilityRef
    strategy_family: str
    declared_hypothesis: str
    parameter_declarations: tuple[tuple[str, str], ...]
    strategy_definition_ref: TraceabilityRef
    status: AIStrategyProposalStatus
    proposal_authority_state: ProposalAuthorityState
    provenance_ref: TraceabilityRef
    contract_version: ObjectVersion = _V1

    def __post_init__(self) -> None:
        if (
            not isinstance(self.proposal_id, ArtifactId)
            or self.version != _V1
            or self.contract_version != _V1
            or not isinstance(self.status, AIStrategyProposalStatus)
            or self.proposal_authority_state is not ProposalAuthorityState.PROPOSAL_ONLY
            or not isinstance(self.strategy_family, str)
            or not self.strategy_family
            or not isinstance(self.declared_hypothesis, str)
            or not self.declared_hypothesis
        ):
            raise IntegratedResearchWorkflowContractError("invalid AI strategy proposal")
        names = tuple(name for name, _ in self.parameter_declarations)
        if (
            names != tuple(sorted(names))
            or len(set(names)) != len(names)
            or any(
                not isinstance(name, str) or not name or not isinstance(value, str)
                for name, value in self.parameter_declarations
            )
        ):
            raise IntegratedResearchWorkflowContractError(
                "proposal parameters must be sorted unique primitive text"
            )
        _exact(self.proposing_agent_ref, "proposing_agent_ref")
        if not isinstance(self.proposing_agent_ref.object_id, AgentId):
            raise IntegratedResearchWorkflowContractError(
                "proposing agent ref must identify AgentId"
            )
        _exact(self.strategy_definition_ref, "strategy_definition_ref")
        _exact(self.provenance_ref, "provenance_ref")


@dataclass(frozen=True, slots=True)
class IntegratedResearchWorkflowPlan:
    workflow_plan_id: ArtifactId
    version: ObjectVersion
    mode: IntegratedResearchWorkflowMode
    proposal_ref: TraceabilityRef
    proposal_strategy_ref: TraceabilityRef
    final_strategy_ref: TraceabilityRef
    normalized_manifest_ref: TraceabilityRef
    normalized_lock_ref: TraceabilityRef
    instrument_ref: TraceabilityRef
    experiment_authorization_ref: TraceabilityRef
    validation_plan_ref: TraceabilityRef
    robustness_plan_ref: TraceabilityRef
    optimization_selection_ref: TraceabilityRef | None
    pine_intake_authority_ref: TraceabilityRef
    parity_authority_ref: TraceabilityRef
    workflow_authority_ref: TraceabilityRef
    provenance_ref: TraceabilityRef
    contract_version: ObjectVersion = _V1

    def __post_init__(self) -> None:
        if (
            not isinstance(self.workflow_plan_id, ArtifactId)
            or self.version != _V1
            or self.contract_version != _V1
            or not isinstance(self.mode, IntegratedResearchWorkflowMode)
        ):
            raise IntegratedResearchWorkflowContractError("invalid integrated workflow plan")
        for field in (
            "proposal_ref",
            "proposal_strategy_ref",
            "final_strategy_ref",
            "normalized_manifest_ref",
            "normalized_lock_ref",
            "instrument_ref",
            "experiment_authorization_ref",
            "validation_plan_ref",
            "robustness_plan_ref",
            "pine_intake_authority_ref",
            "parity_authority_ref",
            "workflow_authority_ref",
            "provenance_ref",
        ):
            _exact(getattr(self, field), field)
        _optional_exact(self.optimization_selection_ref, "optimization_selection_ref")
        if (
            self.mode is IntegratedResearchWorkflowMode.DIRECT_STRATEGY
            and self.optimization_selection_ref is not None
        ):
            raise IntegratedResearchWorkflowContractError(
                "direct workflow cannot bind optimization selection"
            )
        if (
            self.mode is IntegratedResearchWorkflowMode.OPTIMIZED_STRATEGY
            and self.optimization_selection_ref is None
        ):
            raise IntegratedResearchWorkflowContractError(
                "optimized workflow requires exact selection result"
            )


@dataclass(frozen=True, slots=True)
class IntegratedResearchWorkflowRequest:
    workflow_run_id: RunId
    workflow_result_id: ArtifactId
    handoff_id: ArtifactId
    tradingview_manifest_id: ArtifactId
    workflow_plan_ref: TraceabilityRef
    proposal_ref: TraceabilityRef
    pine_artifact_ref: TraceabilityRef
    pine_intake_record_ref: TraceabilityRef
    parity_result_ref: TraceabilityRef
    workflow_authority_ref: TraceabilityRef
    provenance_ref: TraceabilityRef
    contract_version: ObjectVersion = _V1

    def __post_init__(self) -> None:
        if (
            not isinstance(self.workflow_run_id, RunId)
            or not isinstance(self.workflow_result_id, ArtifactId)
            or not isinstance(self.handoff_id, ArtifactId)
            or not isinstance(self.tradingview_manifest_id, ArtifactId)
            or self.contract_version != _V1
        ):
            raise IntegratedResearchWorkflowContractError("invalid workflow request identity")
        for field in (
            "workflow_plan_ref",
            "proposal_ref",
            "pine_artifact_ref",
            "pine_intake_record_ref",
            "parity_result_ref",
            "workflow_authority_ref",
            "provenance_ref",
        ):
            _exact(getattr(self, field), field)


@dataclass(frozen=True, slots=True)
class WorkflowStageResult:
    stage: WorkflowStage
    state: IntegratedResearchWorkflowState
    evidence_ref: TraceabilityRef
    outcome: WorkflowStageOutcome
    reason_code: WorkflowReasonCode | None
    stage_fingerprint: str

    def __post_init__(self) -> None:
        if (
            not isinstance(self.stage, WorkflowStage)
            or not isinstance(self.state, IntegratedResearchWorkflowState)
            or not isinstance(self.outcome, WorkflowStageOutcome)
            or (
                self.reason_code is not None
                and not isinstance(self.reason_code, WorkflowReasonCode)
            )
            or not isinstance(self.stage_fingerprint, str)
            or _FP.fullmatch(self.stage_fingerprint) is None
        ):
            raise IntegratedResearchWorkflowContractError("invalid workflow stage result")
        _exact(self.evidence_ref, "stage.evidence_ref")


@dataclass(frozen=True, slots=True)
class ResearchHandoffPackage:
    handoff_id: ArtifactId
    version: ObjectVersion
    workflow_run_id: RunId
    workflow_input_fingerprint: str
    proposal_ref: TraceabilityRef
    final_strategy_ref: TraceabilityRef
    selected_candidate_ref: TraceabilityRef | None
    backtest_ref: TraceabilityRef
    scientific_validation_ref: TraceabilityRef
    robustness_ref: TraceabilityRef
    optimization_selection_ref: TraceabilityRef | None
    pine_artifact_ref: TraceabilityRef
    pine_intake_ref: TraceabilityRef
    parity_result_ref: TraceabilityRef
    parity_decision: PinePythonParityDecision
    proposing_agent_ref: TraceabilityRef
    pine_generating_agent_ref: TraceabilityRef
    readiness: ResearchHandoffReadiness
    provenance_ref: TraceabilityRef
    deployment_authorization: DeploymentAuthorizationStatus
    execution_state: ExecutionState
    contract_version: ObjectVersion = _V1

    def __post_init__(self) -> None:
        if (
            not isinstance(self.handoff_id, ArtifactId)
            or self.version != _V1
            or self.contract_version != _V1
            or not isinstance(self.readiness, ResearchHandoffReadiness)
        ):
            raise IntegratedResearchWorkflowContractError("invalid research handoff")
        for field in (
            "proposal_ref",
            "final_strategy_ref",
            "backtest_ref",
            "scientific_validation_ref",
            "robustness_ref",
            "pine_artifact_ref",
            "pine_intake_ref",
            "parity_result_ref",
            "proposing_agent_ref",
            "pine_generating_agent_ref",
            "provenance_ref",
        ):
            _exact(getattr(self, field), field)
        if (
            not isinstance(self.workflow_run_id, RunId)
            or not isinstance(self.workflow_input_fingerprint, str)
            or _FP.fullmatch(self.workflow_input_fingerprint) is None
        ):
            raise IntegratedResearchWorkflowContractError("invalid handoff workflow binding")
        _optional_exact(self.selected_candidate_ref, "selected_candidate_ref")
        _optional_exact(self.optimization_selection_ref, "optimization_selection_ref")
        if (
            self.deployment_authorization is not DeploymentAuthorizationStatus.NOT_AUTHORIZED
            or self.execution_state is not ExecutionState.PLANNED_CLOSED
        ):
            raise IntegratedResearchWorkflowContractError(
                "handoff cannot grant deployment/execution"
            )
        if (
            self.readiness is ResearchHandoffReadiness.READY_FOR_HUMAN_RESEARCH_USE
            and self.parity_decision is not PinePythonParityDecision.MATCH
        ):
            raise IntegratedResearchWorkflowContractError(
                "ready research handoff requires parity MATCH"
            )


@dataclass(frozen=True, slots=True)
class TradingViewResearchHandoffManifest:
    manifest_id: ArtifactId
    version: ObjectVersion
    pine_artifact_ref: TraceabilityRef
    pine_source_sha256: str
    parity_result_ref: TraceabilityRef
    strategy_ref: TraceabilityRef
    instrument_ref: TraceabilityRef
    normalized_manifest_ref: TraceabilityRef
    normalized_lock_ref: TraceabilityRef
    repaint_assessment: RepaintAssessmentStatus
    readiness: ResearchHandoffReadiness
    deployment_authorization: DeploymentAuthorizationStatus
    execution_state: ExecutionState
    contract_version: ObjectVersion = _V1

    def __post_init__(self) -> None:
        if (
            not isinstance(self.manifest_id, ArtifactId)
            or self.version != _V1
            or self.contract_version != _V1
            or not isinstance(self.pine_source_sha256, str)
            or _FP.fullmatch(self.pine_source_sha256) is None
            or self.repaint_assessment is not RepaintAssessmentStatus.NOT_EVALUATED
        ):
            raise IntegratedResearchWorkflowContractError("invalid TradingView research manifest")
        for field in (
            "pine_artifact_ref",
            "parity_result_ref",
            "strategy_ref",
            "instrument_ref",
            "normalized_manifest_ref",
            "normalized_lock_ref",
        ):
            _exact(getattr(self, field), field)
        if (
            self.deployment_authorization is not DeploymentAuthorizationStatus.NOT_AUTHORIZED
            or self.execution_state is not ExecutionState.PLANNED_CLOSED
        ):
            raise IntegratedResearchWorkflowContractError(
                "TradingView handoff cannot grant deployment/execution"
            )


@dataclass(frozen=True, slots=True)
class IntegratedResearchWorkflowResult:
    workflow_result_id: ArtifactId
    version: ObjectVersion
    workflow_plan_ref: TraceabilityRef
    proposal_ref: TraceabilityRef
    final_strategy_ref: TraceabilityRef
    stages: tuple[WorkflowStageResult, ...]
    final_state: IntegratedResearchWorkflowState
    handoff_ref: TraceabilityRef | None
    tradingview_manifest_ref: TraceabilityRef | None
    reason_codes: tuple[WorkflowReasonCode, ...]
    input_fingerprint: str
    workflow_authority_ref: TraceabilityRef
    provenance_ref: TraceabilityRef
    deployment_authorization: DeploymentAuthorizationStatus
    execution_state: ExecutionState
    contract_version: ObjectVersion = _V1

    def __post_init__(self) -> None:
        if (
            not isinstance(self.workflow_result_id, ArtifactId)
            or self.version != _V1
            or self.contract_version != _V1
            or not isinstance(self.final_state, IntegratedResearchWorkflowState)
            or not isinstance(self.input_fingerprint, str)
            or _FP.fullmatch(self.input_fingerprint) is None
            or not self.stages
            or tuple(stage.stage for stage in self.stages)
            != tuple(dict.fromkeys(stage.stage for stage in self.stages))
            or tuple(sorted(self.reason_codes, key=lambda item: item.value)) != self.reason_codes
            or len(set(self.reason_codes)) != len(self.reason_codes)
        ):
            raise IntegratedResearchWorkflowContractError("invalid workflow result")
        for field in (
            "workflow_plan_ref",
            "proposal_ref",
            "final_strategy_ref",
            "workflow_authority_ref",
            "provenance_ref",
        ):
            _exact(getattr(self, field), field)
        _optional_exact(self.handoff_ref, "handoff_ref")
        _optional_exact(self.tradingview_manifest_ref, "tradingview_manifest_ref")
        if (
            self.deployment_authorization is not DeploymentAuthorizationStatus.NOT_AUTHORIZED
            or self.execution_state is not ExecutionState.PLANNED_CLOSED
        ):
            raise IntegratedResearchWorkflowContractError(
                "workflow cannot grant deployment/execution"
            )
        ready = self.final_state is IntegratedResearchWorkflowState.RESEARCH_HANDOFF_READY
        if ready != (self.handoff_ref is not None and self.tradingview_manifest_ref is not None):
            raise IntegratedResearchWorkflowContractError(
                "workflow handoff refs must match final readiness"
            )


@dataclass(frozen=True, slots=True)
class IntegratedResearchWorkflowRunRecord:
    workflow_run_id: RunId
    version: ObjectVersion
    workflow_plan_ref: TraceabilityRef
    proposal_ref: TraceabilityRef
    result_ref: TraceabilityRef
    input_fingerprint: str
    final_state: IntegratedResearchWorkflowState
    handoff_ref: TraceabilityRef | None
    stage_count: int
    workflow_authority_ref: TraceabilityRef
    provenance_ref: TraceabilityRef
    deployment_authorization: DeploymentAuthorizationStatus
    execution_state: ExecutionState
    contract_version: ObjectVersion = _V1

    def __post_init__(self) -> None:
        if (
            not isinstance(self.workflow_run_id, RunId)
            or self.version != _V1
            or self.contract_version != _V1
            or not isinstance(self.input_fingerprint, str)
            or _FP.fullmatch(self.input_fingerprint) is None
            or isinstance(self.stage_count, bool)
            or not isinstance(self.stage_count, int)
            or self.stage_count < 1
        ):
            raise IntegratedResearchWorkflowContractError("invalid workflow run record")
        for field in (
            "workflow_plan_ref",
            "proposal_ref",
            "result_ref",
            "workflow_authority_ref",
            "provenance_ref",
        ):
            _exact(getattr(self, field), field)
        _optional_exact(self.handoff_ref, "handoff_ref")
        if (
            self.deployment_authorization is not DeploymentAuthorizationStatus.NOT_AUTHORIZED
            or self.execution_state is not ExecutionState.PLANNED_CLOSED
        ):
            raise IntegratedResearchWorkflowContractError("workflow run cannot grant authority")
