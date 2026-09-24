"""Governed orchestration for the Phase 3 end-to-end research workflow."""

from __future__ import annotations

from dataclasses import dataclass

from ai_quant_lab.core.dataset_store import LocalDatasetRepository, RepositoryWriteResult
from ai_quant_lab.core.experiment_authorization import verify_experiment_authorization_lineage
from ai_quant_lab.core.experiment_contracts import ExperimentAuthorizationDecision
from ai_quant_lab.core.integrated_research_workflow_contracts import (
    AIStrategyProposal,
    AIStrategyProposalStatus,
    IntegratedResearchWorkflowMode,
    IntegratedResearchWorkflowPlan,
    IntegratedResearchWorkflowRequest,
    IntegratedResearchWorkflowResult,
    IntegratedResearchWorkflowRunRecord,
    IntegratedResearchWorkflowState,
    ResearchHandoffPackage,
    ResearchHandoffReadiness,
    TradingViewResearchHandoffManifest,
    WorkflowReasonCode,
    WorkflowStage,
    WorkflowStageOutcome,
    WorkflowStageResult,
)
from ai_quant_lab.core.integrity import fingerprint_record
from ai_quant_lab.core.model import (
    AgentId,
    ExecutionState,
    ObjectVersion,
    TraceabilityRef,
    fingerprint,
)
from ai_quant_lab.core.optimization_contracts import SelectionDecision
from ai_quant_lab.core.optimization_selection import (
    OptimizationEvidence,
    verify_optimization_selection_lineage,
)
from ai_quant_lab.core.pine_python_parity import (
    PinePythonParityContext,
    verify_pine_python_parity_lineage,
)
from ai_quant_lab.core.pine_python_parity_contracts import (
    ParityTolerancePolicy,
    PineExecutionEvidence,
    PinePythonParityDecision,
    PinePythonParityRequest,
    PinePythonParityResult,
    PinePythonParityRunRecord,
)
from ai_quant_lab.core.pine_strategy_contracts import PineIntakeStatus, RepaintAssessmentStatus
from ai_quant_lab.core.pine_strategy_intake import PineOptimizationSelectionEvidence
from ai_quant_lab.core.research_eligibility_contracts import DeploymentAuthorizationStatus
from ai_quant_lab.core.robustness_validation import verify_robustness_validation_lineage
from ai_quant_lab.core.robustness_validation_contracts import RobustnessDecision
from ai_quant_lab.core.scientific_validation_contracts import ScientificValidationDecision

_V1 = ObjectVersion(1)


class IntegratedResearchWorkflowError(ValueError):
    pass


class IntegratedResearchWorkflowLineageMismatch(IntegratedResearchWorkflowError):
    pass


class IntegratedResearchWorkflowAuthorityInvalid(IntegratedResearchWorkflowError):
    pass


@dataclass(frozen=True, slots=True)
class IntegratedResearchWorkflowContext:
    final_evidence: OptimizationEvidence
    optimization: PineOptimizationSelectionEvidence | None
    parity_request: PinePythonParityRequest
    parity_evidence: PineExecutionEvidence
    parity_policy: ParityTolerancePolicy
    parity_result: PinePythonParityResult
    parity_record: PinePythonParityRunRecord
    parity_context: PinePythonParityContext
    workflow_authority_ref: TraceabilityRef
    pine_generating_agent_ref: TraceabilityRef


@dataclass(frozen=True, slots=True)
class IntegratedResearchWorkflowExecutionResult:
    result: IntegratedResearchWorkflowResult
    handoff: ResearchHandoffPackage | None
    tradingview_manifest: TradingViewResearchHandoffManifest | None
    record: IntegratedResearchWorkflowRunRecord
    writes: tuple[RepositoryWriteResult, ...]


def _exact(record: object, object_id: object, version: ObjectVersion) -> TraceabilityRef:
    return TraceabilityRef(object_id, version, fingerprint_record(record))  # type: ignore[arg-type]


def _stage(
    stage: WorkflowStage,
    state: IntegratedResearchWorkflowState,
    evidence_ref: TraceabilityRef,
    outcome: WorkflowStageOutcome,
    reason: WorkflowReasonCode | None = None,
) -> WorkflowStageResult:
    stage_fp = fingerprint(
        {
            "stage": stage,
            "state": state,
            "evidence_ref": evidence_ref,
            "outcome": outcome,
            "reason": reason,
        }
    )
    return WorkflowStageResult(stage, state, evidence_ref, outcome, reason, stage_fp)


def derive_final_workflow_state(
    *,
    proposal_status: AIStrategyProposalStatus,
    authorization: ExperimentAuthorizationDecision,
    scientific: ScientificValidationDecision,
    robustness: RobustnessDecision,
    optimization: SelectionDecision | None,
    parity: PinePythonParityDecision,
    pine_intake_accepted: bool,
) -> tuple[IntegratedResearchWorkflowState, tuple[WorkflowReasonCode, ...]]:
    """Mechanical decision map. It creates no scientific or deployment authority."""
    if proposal_status is not AIStrategyProposalStatus.ACCEPTED_FOR_RESEARCH:
        return (
            IntegratedResearchWorkflowState.RESEARCH_REJECTED,
            (WorkflowReasonCode.PROPOSAL_NOT_ACCEPTED,),
        )
    if authorization is not ExperimentAuthorizationDecision.AUTHORIZED:
        return (
            IntegratedResearchWorkflowState.RESEARCH_REJECTED,
            (WorkflowReasonCode.EXPERIMENT_NOT_AUTHORIZED,),
        )
    if scientific is ScientificValidationDecision.FAIL:
        return (
            IntegratedResearchWorkflowState.RESEARCH_REJECTED,
            (WorkflowReasonCode.SCIENTIFIC_VALIDATION_FAILED,),
        )
    if scientific is ScientificValidationDecision.INCONCLUSIVE:
        return (
            IntegratedResearchWorkflowState.RESEARCH_INCONCLUSIVE,
            (WorkflowReasonCode.SCIENTIFIC_VALIDATION_INCONCLUSIVE,),
        )
    if robustness is RobustnessDecision.FAIL:
        return (
            IntegratedResearchWorkflowState.RESEARCH_REJECTED,
            (WorkflowReasonCode.ROBUSTNESS_FAILED,),
        )
    if robustness is RobustnessDecision.INCONCLUSIVE:
        return (
            IntegratedResearchWorkflowState.RESEARCH_INCONCLUSIVE,
            (WorkflowReasonCode.ROBUSTNESS_INCONCLUSIVE,),
        )
    if optimization is SelectionDecision.REJECTED:
        return (
            IntegratedResearchWorkflowState.RESEARCH_REJECTED,
            (WorkflowReasonCode.OPTIMIZATION_NOT_SELECTED,),
        )
    if optimization is SelectionDecision.INCONCLUSIVE:
        return (
            IntegratedResearchWorkflowState.RESEARCH_INCONCLUSIVE,
            (WorkflowReasonCode.OPTIMIZATION_NOT_SELECTED,),
        )
    if not pine_intake_accepted:
        return (
            IntegratedResearchWorkflowState.RESEARCH_REJECTED,
            (WorkflowReasonCode.PINE_INTAKE_FAILED,),
        )
    if parity is PinePythonParityDecision.MISMATCH:
        return (
            IntegratedResearchWorkflowState.RESEARCH_REJECTED,
            (WorkflowReasonCode.PARITY_MISMATCH,),
        )
    if parity is PinePythonParityDecision.INCONCLUSIVE:
        return (
            IntegratedResearchWorkflowState.RESEARCH_INCONCLUSIVE,
            (WorkflowReasonCode.PARITY_INCONCLUSIVE,),
        )
    return (
        IntegratedResearchWorkflowState.RESEARCH_HANDOFF_READY,
        (WorkflowReasonCode.RESEARCH_HANDOFF_READY,),
    )


def _verify_authoritative_chain(
    proposal: AIStrategyProposal,
    plan: IntegratedResearchWorkflowPlan,
    request: IntegratedResearchWorkflowRequest,
    context: IntegratedResearchWorkflowContext,
) -> OptimizationEvidence:
    if (
        request.workflow_authority_ref != context.workflow_authority_ref
        or plan.workflow_authority_ref != context.workflow_authority_ref
    ):
        raise IntegratedResearchWorkflowAuthorityInvalid(
            "workflow request/plan lacks exact governed workflow authority"
        )
    if not isinstance(context.pine_generating_agent_ref.object_id, AgentId):
        raise IntegratedResearchWorkflowLineageMismatch(
            "Pine generating agent must be an exact AgentId reference"
        )
    if context.pine_generating_agent_ref.expected_fingerprint is None:
        raise IntegratedResearchWorkflowLineageMismatch(
            "Pine generating agent must be fingerprint-bearing"
        )

    final = context.final_evidence
    try:
        verify_experiment_authorization_lineage(
            record=final.authorization,
            specification=final.specification,
            policy=final.authorization_policy,
            eligibility=final.eligibility,
            eligibility_policy=final.eligibility_policy,
            admission=final.admission,
            declaration=final.declaration,
            report=final.report,
        )
        verify_robustness_validation_lineage(
            record=final.robustness_record,
            result=final.robustness_result,
            request=final.robustness_request,
            plan=final.robustness_plan,
            scientific_result=final.scientific_result,
            validation_record=final.validation_record,
            scientific_request=final.scientific_request,
            validation_plan=final.validation_plan,
            backtest_artifact=final.backtest_artifact,
            backtest_record=final.backtest_record,
            backtest_request=final.backtest_request,
            authorization=final.authorization,
            specification=final.specification,
            policy=final.authorization_policy,
            eligibility=final.eligibility,
            eligibility_policy=final.eligibility_policy,
            admission=final.admission,
            declaration=final.declaration,
            engine_contract=final.engine_contract,
            strategy=final.strategy,
            instrument=final.instrument,
            report=final.report,
        )
    except ValueError as exc:
        raise IntegratedResearchWorkflowLineageMismatch(
            "governed authorization/scientific/robustness chain failed verification"
        ) from exc

    proposal_ref = _exact(proposal, proposal.proposal_id, proposal.version)
    final_strategy_ref = _exact(final.strategy, final.strategy.strategy_id, final.strategy.version)
    instrument_ref = _exact(final.instrument, final.instrument.instrument_id, final.instrument.version)
    auth_ref = _exact(
        final.authorization,
        final.authorization.authorization_id,
        final.authorization.version,
    )
    validation_plan_ref = _exact(
        final.validation_plan,
        final.validation_plan.validation_plan_id,
        final.validation_plan.version,
    )
    robustness_plan_ref = _exact(
        final.robustness_plan,
        final.robustness_plan.robustness_plan_id,
        final.robustness_plan.version,
    )
    if (
        plan.proposal_ref != proposal_ref
        or request.proposal_ref != proposal_ref
        or request.workflow_plan_ref != _exact(plan, plan.workflow_plan_id, plan.version)
        or plan.final_strategy_ref != final_strategy_ref
        or plan.instrument_ref != instrument_ref
        or plan.experiment_authorization_ref != auth_ref
        or plan.validation_plan_ref != validation_plan_ref
        or plan.robustness_plan_ref != robustness_plan_ref
        or plan.normalized_manifest_ref != final.backtest_artifact.normalized_manifest_ref
        or plan.normalized_lock_ref != final.backtest_artifact.normalized_lock_ref
        or proposal.proposing_agent_ref.object_id != final.specification.proposer_id
    ):
        raise IntegratedResearchWorkflowLineageMismatch(
            "workflow plan does not bind exact final governed research evidence"
        )

    if plan.mode is IntegratedResearchWorkflowMode.DIRECT_STRATEGY:
        if context.optimization is not None:
            raise IntegratedResearchWorkflowLineageMismatch(
                "direct workflow cannot carry optimization selection"
            )
        if proposal.strategy_definition_ref != final_strategy_ref:
            raise IntegratedResearchWorkflowLineageMismatch(
                "direct workflow proposal strategy changed"
            )
        if plan.proposal_strategy_ref != final_strategy_ref:
            raise IntegratedResearchWorkflowLineageMismatch(
                "direct workflow plan proposal strategy is inconsistent"
            )
    else:
        optimization = context.optimization
        if optimization is None:
            raise IntegratedResearchWorkflowLineageMismatch(
                "optimized workflow requires exact selection evidence"
            )
        try:
            verify_optimization_selection_lineage(
                record=optimization.record,
                result=optimization.result,
                candidate_definitions=optimization.candidate_definitions,
                candidate_results=optimization.candidate_results,
                trials=optimization.trials,
                request=optimization.request,
                plan=optimization.plan,
                search_space=optimization.search_space,
                source=optimization.source,
                candidates=optimization.candidates,
            )
        except ValueError as exc:
            raise IntegratedResearchWorkflowLineageMismatch(
                "optimization selection failed exact verification"
            ) from exc
        selection_ref = _exact(
            optimization.result,
            optimization.result.selection_result_id,
            optimization.result.version,
        )
        parent_ref = _exact(
            optimization.source.strategy,
            optimization.source.strategy.strategy_id,
            optimization.source.strategy.version,
        )
        if (
            optimization.result.decision is not SelectionDecision.SELECTED
            or optimization.result.selected_candidate_ref is None
            or plan.optimization_selection_ref != selection_ref
            or proposal.strategy_definition_ref != parent_ref
            or plan.proposal_strategy_ref != parent_ref
        ):
            raise IntegratedResearchWorkflowLineageMismatch(
                "optimized workflow does not bind exact selected lineage"
            )
        selected = next(
            (
                item
                for item in optimization.candidate_results
                if _exact(item, item.candidate_id, item.version)
                == optimization.result.selected_candidate_ref
            ),
            None,
        )
        if selected is None or selected.candidate_strategy_ref != final_strategy_ref:
            raise IntegratedResearchWorkflowLineageMismatch(
                "optimized final strategy is not the selected candidate strategy"
            )
        if final not in optimization.candidates:
            raise IntegratedResearchWorkflowLineageMismatch(
                "optimized final evidence is absent from candidate evidence"
            )

    if (
        plan.pine_intake_authority_ref
        != context.parity_context.pine_intake_context.pine_intake_authority_ref
        or plan.parity_authority_ref != context.parity_context.parity_authority_ref
    ):
        raise IntegratedResearchWorkflowLineageMismatch(
            "workflow authority bindings do not match Pine/parity authorities"
        )

    try:
        verify_pine_python_parity_lineage(
            result=context.parity_result,
            record=context.parity_record,
            request=context.parity_request,
            evidence=context.parity_evidence,
            policy=context.parity_policy,
            context=context.parity_context,
        )
    except ValueError as exc:
        raise IntegratedResearchWorkflowLineageMismatch(
            "Pine/Python parity chain failed exact verification"
        ) from exc

    pine_artifact = context.parity_context.pine_artifact
    pine_record = context.parity_context.pine_intake_record
    if (
        request.pine_artifact_ref
        != _exact(pine_artifact, pine_artifact.pine_artifact_id, pine_artifact.version)
        or request.pine_intake_record_ref
        != _exact(pine_record, pine_record.intake_run_id, pine_record.version)
        or request.parity_result_ref
        != _exact(
            context.parity_result,
            context.parity_result.parity_result_id,
            context.parity_result.version,
        )
        or context.parity_result.strategy_ref != final_strategy_ref
        or context.parity_result.instrument_ref != instrument_ref
        or context.parity_result.normalized_manifest_ref
        != final.backtest_artifact.normalized_manifest_ref
        or context.parity_result.normalized_lock_ref
        != final.backtest_artifact.normalized_lock_ref
        or context.parity_result.python_backtest_ref
        != _exact(
            final.backtest_artifact,
            final.backtest_artifact.artifact_id,
            final.backtest_artifact.version,
        )
    ):
        raise IntegratedResearchWorkflowLineageMismatch(
            "Pine/parity identity does not match final governed strategy/dataset"
        )
    return final


def _workflow_input_fingerprint(
    proposal: AIStrategyProposal,
    plan: IntegratedResearchWorkflowPlan,
    request: IntegratedResearchWorkflowRequest,
    context: IntegratedResearchWorkflowContext,
) -> str:
    final = context.final_evidence
    return fingerprint(
        {
            "proposal": fingerprint_record(proposal),
            "plan": fingerprint_record(plan),
            "request": request,
            "strategy": fingerprint_record(final.strategy),
            "authorization": fingerprint_record(final.authorization),
            "backtest": fingerprint_record(final.backtest_artifact),
            "scientific": fingerprint_record(final.scientific_result),
            "robustness": fingerprint_record(final.robustness_result),
            "optimization": (
                None
                if context.optimization is None
                else fingerprint_record(context.optimization.result)
            ),
            "pine_artifact": fingerprint_record(context.parity_context.pine_artifact),
            "pine_intake": fingerprint_record(context.parity_context.pine_intake_record),
            "parity": fingerprint_record(context.parity_result),
            "workflow_authority": context.workflow_authority_ref,
            "pine_generating_agent": context.pine_generating_agent_ref,
        }
    )


def _build(
    proposal: AIStrategyProposal,
    plan: IntegratedResearchWorkflowPlan,
    request: IntegratedResearchWorkflowRequest,
    *,
    context: IntegratedResearchWorkflowContext,
) -> tuple[
    IntegratedResearchWorkflowResult,
    ResearchHandoffPackage | None,
    TradingViewResearchHandoffManifest | None,
    IntegratedResearchWorkflowRunRecord,
]:
    final = _verify_authoritative_chain(proposal, plan, request, context)
    input_fp = _workflow_input_fingerprint(proposal, plan, request, context)
    optimization_decision = (
        None if context.optimization is None else context.optimization.result.decision
    )
    final_state, reasons = derive_final_workflow_state(
        proposal_status=proposal.status,
        authorization=final.authorization.decision,
        scientific=final.scientific_result.decision,
        robustness=final.robustness_result.decision,
        optimization=optimization_decision,
        parity=context.parity_result.decision,
        pine_intake_accepted=(
            context.parity_context.pine_intake_record.status is PineIntakeStatus.ACCEPTED
        ),
    )

    refs = {
        "proposal": _exact(proposal, proposal.proposal_id, proposal.version),
        "authorization": _exact(
            final.authorization,
            final.authorization.authorization_id,
            final.authorization.version,
        ),
        "backtest": _exact(
            final.backtest_artifact,
            final.backtest_artifact.artifact_id,
            final.backtest_artifact.version,
        ),
        "scientific": _exact(
            final.scientific_result,
            final.scientific_result.validation_result_id,
            final.scientific_result.version,
        ),
        "robustness": _exact(
            final.robustness_result,
            final.robustness_result.robustness_result_id,
            final.robustness_result.version,
        ),
        "pine_intake": _exact(
            context.parity_context.pine_intake_record,
            context.parity_context.pine_intake_record.intake_run_id,
            context.parity_context.pine_intake_record.version,
        ),
        "parity": _exact(
            context.parity_result,
            context.parity_result.parity_result_id,
            context.parity_result.version,
        ),
    }
    stages = [
        _stage(
            WorkflowStage.PROPOSAL,
            IntegratedResearchWorkflowState.PROPOSAL_ACCEPTED,
            refs["proposal"],
            WorkflowStageOutcome.ACCEPTED,
        ),
        _stage(
            WorkflowStage.AUTHORIZATION,
            IntegratedResearchWorkflowState.EXPERIMENT_AUTHORIZED,
            refs["authorization"],
            WorkflowStageOutcome.AUTHORIZED,
        ),
        _stage(
            WorkflowStage.BACKTEST,
            IntegratedResearchWorkflowState.BACKTEST_COMPLETED,
            refs["backtest"],
            WorkflowStageOutcome.COMPLETED,
        ),
        _stage(
            WorkflowStage.SCIENTIFIC_VALIDATION,
            IntegratedResearchWorkflowState.SCIENTIFIC_VALIDATION_COMPLETED,
            refs["scientific"],
            (
                WorkflowStageOutcome.PASS
                if final.scientific_result.decision is ScientificValidationDecision.PASS
                else WorkflowStageOutcome.INCONCLUSIVE
                if final.scientific_result.decision is ScientificValidationDecision.INCONCLUSIVE
                else WorkflowStageOutcome.FAIL
            ),
        ),
        _stage(
            WorkflowStage.ROBUSTNESS,
            IntegratedResearchWorkflowState.ROBUSTNESS_COMPLETED,
            refs["robustness"],
            (
                WorkflowStageOutcome.PASS
                if final.robustness_result.decision is RobustnessDecision.PASS
                else WorkflowStageOutcome.INCONCLUSIVE
                if final.robustness_result.decision is RobustnessDecision.INCONCLUSIVE
                else WorkflowStageOutcome.FAIL
            ),
        ),
    ]
    selected_candidate_ref = None
    optimization_selection_ref = None
    if context.optimization is not None:
        optimization_selection_ref = _exact(
            context.optimization.result,
            context.optimization.result.selection_result_id,
            context.optimization.result.version,
        )
        selected_candidate_ref = context.optimization.result.selected_candidate_ref
        stages.append(
            _stage(
                WorkflowStage.OPTIMIZATION,
                IntegratedResearchWorkflowState.OPTIMIZATION_COMPLETED,
                optimization_selection_ref,
                (
                    WorkflowStageOutcome.SELECTED
                    if context.optimization.result.decision is SelectionDecision.SELECTED
                    else WorkflowStageOutcome.INCONCLUSIVE
                    if context.optimization.result.decision is SelectionDecision.INCONCLUSIVE
                    else WorkflowStageOutcome.FAIL
                ),
            )
        )
    stages.extend(
        (
            _stage(
                WorkflowStage.PINE_INTAKE,
                IntegratedResearchWorkflowState.PINE_INTAKE_COMPLETED,
                refs["pine_intake"],
                WorkflowStageOutcome.COMPLETED,
            ),
            _stage(
                WorkflowStage.PARITY,
                IntegratedResearchWorkflowState.PARITY_COMPLETED,
                refs["parity"],
                (
                    WorkflowStageOutcome.MATCH
                    if context.parity_result.decision is PinePythonParityDecision.MATCH
                    else WorkflowStageOutcome.INCONCLUSIVE
                    if context.parity_result.decision is PinePythonParityDecision.INCONCLUSIVE
                    else WorkflowStageOutcome.FAIL
                ),
            ),
        )
    )

    handoff: ResearchHandoffPackage | None = None
    manifest: TradingViewResearchHandoffManifest | None = None
    handoff_ref = None
    manifest_ref = None
    final_strategy_ref = _exact(
        final.strategy,
        final.strategy.strategy_id,
        final.strategy.version,
    )
    if final_state is IntegratedResearchWorkflowState.RESEARCH_HANDOFF_READY:
        handoff = ResearchHandoffPackage(
            request.handoff_id,
            _V1,
            request.workflow_run_id,
            input_fp,
            refs["proposal"],
            final_strategy_ref,
            selected_candidate_ref,
            refs["backtest"],
            refs["scientific"],
            refs["robustness"],
            optimization_selection_ref,
            request.pine_artifact_ref,
            request.pine_intake_record_ref,
            request.parity_result_ref,
            context.parity_result.decision,
            proposal.proposing_agent_ref,
            context.pine_generating_agent_ref,
            ResearchHandoffReadiness.READY_FOR_HUMAN_RESEARCH_USE,
            request.provenance_ref,
            DeploymentAuthorizationStatus.NOT_AUTHORIZED,
            ExecutionState.PLANNED_CLOSED,
            _V1,
        )
        handoff_ref = _exact(handoff, handoff.handoff_id, handoff.version)
        manifest = TradingViewResearchHandoffManifest(
            request.tradingview_manifest_id,
            _V1,
            request.pine_artifact_ref,
            context.parity_context.pine_artifact.source_sha256,
            request.parity_result_ref,
            final_strategy_ref,
            _exact(
                final.instrument,
                final.instrument.instrument_id,
                final.instrument.version,
            ),
            final.backtest_artifact.normalized_manifest_ref,
            final.backtest_artifact.normalized_lock_ref,
            RepaintAssessmentStatus.NOT_EVALUATED,
            ResearchHandoffReadiness.READY_FOR_HUMAN_RESEARCH_USE,
            DeploymentAuthorizationStatus.NOT_AUTHORIZED,
            ExecutionState.PLANNED_CLOSED,
            _V1,
        )
        manifest_ref = _exact(manifest, manifest.manifest_id, manifest.version)
        stages.append(
            _stage(
                WorkflowStage.HANDOFF,
                IntegratedResearchWorkflowState.RESEARCH_HANDOFF_READY,
                handoff_ref,
                WorkflowStageOutcome.READY,
                WorkflowReasonCode.RESEARCH_HANDOFF_READY,
            )
        )

    result = IntegratedResearchWorkflowResult(
        request.workflow_result_id,
        _V1,
        request.workflow_plan_ref,
        request.proposal_ref,
        final_strategy_ref,
        tuple(stages),
        final_state,
        handoff_ref,
        manifest_ref,
        tuple(sorted(reasons, key=lambda item: item.value)),
        input_fp,
        request.workflow_authority_ref,
        request.provenance_ref,
        DeploymentAuthorizationStatus.NOT_AUTHORIZED,
        ExecutionState.PLANNED_CLOSED,
        _V1,
    )
    record = IntegratedResearchWorkflowRunRecord(
        request.workflow_run_id,
        _V1,
        request.workflow_plan_ref,
        request.proposal_ref,
        _exact(result, result.workflow_result_id, result.version),
        input_fp,
        final_state,
        handoff_ref,
        len(stages),
        request.workflow_authority_ref,
        request.provenance_ref,
        DeploymentAuthorizationStatus.NOT_AUTHORIZED,
        ExecutionState.PLANNED_CLOSED,
        _V1,
    )
    return result, handoff, manifest, record


def evaluate_integrated_research_workflow(
    proposal: AIStrategyProposal,
    plan: IntegratedResearchWorkflowPlan,
    request: IntegratedResearchWorkflowRequest,
    *,
    context: IntegratedResearchWorkflowContext,
    repository: LocalDatasetRepository,
) -> IntegratedResearchWorkflowExecutionResult:
    result, handoff, manifest, record = _build(
        proposal,
        plan,
        request,
        context=context,
    )
    objects: list[object] = [proposal, plan]
    if handoff is not None:
        objects.append(handoff)
    if manifest is not None:
        objects.append(manifest)
    objects.extend((result, record))
    writes = tuple(repository.store(item) for item in objects)  # type: ignore[arg-type]
    return IntegratedResearchWorkflowExecutionResult(
        result,
        handoff,
        manifest,
        record,
        writes,
    )


def verify_integrated_research_workflow_lineage(
    *,
    proposal: AIStrategyProposal,
    plan: IntegratedResearchWorkflowPlan,
    request: IntegratedResearchWorkflowRequest,
    result: IntegratedResearchWorkflowResult,
    handoff: ResearchHandoffPackage | None,
    tradingview_manifest: TradingViewResearchHandoffManifest | None,
    record: IntegratedResearchWorkflowRunRecord,
    context: IntegratedResearchWorkflowContext,
) -> None:
    expected = _build(proposal, plan, request, context=context)
    if (
        result != expected[0]
        or handoff != expected[1]
        or tradingview_manifest != expected[2]
        or record != expected[3]
    ):
        raise IntegratedResearchWorkflowLineageMismatch(
            "integrated research workflow lineage is not exact and deterministic"
        )
