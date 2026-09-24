"""Direct-strategy end-to-end coverage for Sprint 19."""

# mypy: disable-error-code="no-untyped-def,no-untyped-call"

from pathlib import Path

from test_integrated_research_workflow import PINE_AGENT, WORKFLOW_AUTHORITY, exact
from test_pine_python_parity import PARITY_AUTHORITY_REF, _csv_bytes, _event_rows
from test_pine_strategy_intake import PROVENANCE_REF, _direct_context

from ai_quant_lab.core.dataset_store import LocalDatasetRepository
from ai_quant_lab.core.integrated_research_workflow import (
    IntegratedResearchWorkflowContext,
    evaluate_integrated_research_workflow,
    verify_integrated_research_workflow_lineage,
)
from ai_quant_lab.core.integrated_research_workflow_contracts import (
    AIStrategyProposal,
    AIStrategyProposalStatus,
    IntegratedResearchWorkflowMode,
    IntegratedResearchWorkflowPlan,
    IntegratedResearchWorkflowRequest,
    IntegratedResearchWorkflowState,
    ProposalAuthorityState,
    ResearchHandoffReadiness,
)
from ai_quant_lab.core.model import ArtifactId, ExecutionState, ObjectVersion, RunId, TraceabilityRef
from ai_quant_lab.core.pine_python_parity import (
    PinePythonParityContext,
    evaluate_pine_python_parity,
    import_pine_execution_csv,
)
from ai_quant_lab.core.pine_python_parity_contracts import (
    ParityTolerancePolicy,
    PinePythonParityRequest,
)
from ai_quant_lab.core.pine_strategy_intake import intake_pine_strategy
from ai_quant_lab.core.research_eligibility_contracts import DeploymentAuthorizationStatus

pytest_plugins = ("test_pine_strategy_intake",)

V1 = ObjectVersion(1)


def test_direct_strategy_full_path_reaches_research_handoff(selection_bundle, tmp_path: Path):
    pine_request, pine_context, _ = _direct_context(selection_bundle)
    pine_repository = LocalDatasetRepository(root=tmp_path / "direct-pine", allowed_root=tmp_path)
    pine = intake_pine_strategy(pine_request, context=pine_context, repository=pine_repository)
    source = pine_context.evidence

    policy = ParityTolerancePolicy(
        ArtifactId("direct-parity-tolerance"),
        V1,
        True,
        "0",
        "0",
        "0",
        "0",
        "0",
        PARITY_AUTHORITY_REF,
        PROVENANCE_REF,
    )
    pine_ref = exact(pine.artifact, pine.artifact.pine_artifact_id, pine.artifact.version)
    evidence = import_pine_execution_csv(
        _csv_bytes(_event_rows(source.backtest_artifact)),
        evidence_id=ArtifactId("direct-pine-execution-evidence"),
        pine_artifact_ref=pine_ref,
        strategy_ref=exact(source.strategy, source.strategy.strategy_id, source.strategy.version),
        instrument_ref=exact(
            source.instrument,
            source.instrument.instrument_id,
            source.instrument.version,
        ),
        normalized_manifest_ref=source.backtest_artifact.normalized_manifest_ref,
        normalized_lock_ref=source.backtest_artifact.normalized_lock_ref,
        observation_start=source.specification.observation_start,
        observation_end=source.specification.observation_end,
        provenance_ref=PROVENANCE_REF,
        authority_ref=PARITY_AUTHORITY_REF,
    )
    parity_request = PinePythonParityRequest(
        RunId("direct-parity-run"),
        ArtifactId("direct-parity-result"),
        pine_ref,
        exact(pine.record, pine.record.intake_run_id, pine.record.version),
        exact(
            source.backtest_artifact,
            source.backtest_artifact.artifact_id,
            source.backtest_artifact.version,
        ),
        exact(evidence, evidence.evidence_id, evidence.version),
        exact(source.strategy, source.strategy.strategy_id, source.strategy.version),
        exact(source.instrument, source.instrument.instrument_id, source.instrument.version),
        source.backtest_artifact.normalized_manifest_ref,
        source.backtest_artifact.normalized_lock_ref,
        source.specification.observation_start,
        source.specification.observation_end,
        exact(policy, policy.policy_id, policy.version),
        PARITY_AUTHORITY_REF,
        PROVENANCE_REF,
    )
    parity_context = PinePythonParityContext(
        pine.artifact,
        pine.record,
        pine_request,
        pine_context,
        PARITY_AUTHORITY_REF,
    )
    parity = evaluate_pine_python_parity(
        parity_request,
        evidence=evidence,
        policy=policy,
        context=parity_context,
        repository=LocalDatasetRepository(
            root=tmp_path / "direct-parity",
            allowed_root=tmp_path,
        ),
    )

    proposer = TraceabilityRef(
        source.specification.proposer_id,
        V1,
        "sha256:" + "7" * 64,
    )
    strategy_ref = exact(source.strategy, source.strategy.strategy_id, source.strategy.version)
    proposal = AIStrategyProposal(
        ArtifactId("direct-integrated-proposal"),
        V1,
        proposer,
        source.strategy.model.value,
        "Synthetic direct governed integration proposal.",
        (("threshold_bps", str(source.strategy.threshold_bps)),),
        strategy_ref,
        AIStrategyProposalStatus.ACCEPTED_FOR_RESEARCH,
        ProposalAuthorityState.PROPOSAL_ONLY,
        PROVENANCE_REF,
        V1,
    )
    plan = IntegratedResearchWorkflowPlan(
        ArtifactId("direct-integrated-plan"),
        V1,
        IntegratedResearchWorkflowMode.DIRECT_STRATEGY,
        exact(proposal, proposal.proposal_id, proposal.version),
        strategy_ref,
        strategy_ref,
        source.backtest_artifact.normalized_manifest_ref,
        source.backtest_artifact.normalized_lock_ref,
        exact(source.instrument, source.instrument.instrument_id, source.instrument.version),
        exact(
            source.authorization,
            source.authorization.authorization_id,
            source.authorization.version,
        ),
        exact(
            source.validation_plan,
            source.validation_plan.validation_plan_id,
            source.validation_plan.version,
        ),
        exact(
            source.robustness_plan,
            source.robustness_plan.robustness_plan_id,
            source.robustness_plan.version,
        ),
        None,
        pine_context.pine_intake_authority_ref,
        PARITY_AUTHORITY_REF,
        WORKFLOW_AUTHORITY,
        PROVENANCE_REF,
        V1,
    )
    request = IntegratedResearchWorkflowRequest(
        RunId("direct-integrated-run"),
        ArtifactId("direct-integrated-result"),
        ArtifactId("direct-integrated-handoff"),
        ArtifactId("direct-tradingview-handoff"),
        exact(plan, plan.workflow_plan_id, plan.version),
        exact(proposal, proposal.proposal_id, proposal.version),
        pine_ref,
        exact(pine.record, pine.record.intake_run_id, pine.record.version),
        exact(parity.result, parity.result.parity_result_id, parity.result.version),
        WORKFLOW_AUTHORITY,
        PROVENANCE_REF,
        V1,
    )
    context = IntegratedResearchWorkflowContext(
        source,
        None,
        parity_request,
        evidence,
        policy,
        parity.result,
        parity.record,
        parity_context,
        WORKFLOW_AUTHORITY,
        PINE_AGENT,
    )
    execution = evaluate_integrated_research_workflow(
        proposal,
        plan,
        request,
        context=context,
        repository=LocalDatasetRepository(
            root=tmp_path / "direct-integrated",
            allowed_root=tmp_path,
        ),
    )

    assert execution.result.final_state is IntegratedResearchWorkflowState.RESEARCH_HANDOFF_READY
    assert execution.handoff is not None
    assert execution.handoff.readiness is ResearchHandoffReadiness.READY_FOR_HUMAN_RESEARCH_USE
    assert execution.handoff.optimization_selection_ref is None
    assert execution.handoff.selected_candidate_ref is None
    assert execution.result.deployment_authorization is DeploymentAuthorizationStatus.NOT_AUTHORIZED
    assert execution.result.execution_state is ExecutionState.PLANNED_CLOSED
    verify_integrated_research_workflow_lineage(
        proposal=proposal,
        plan=plan,
        request=request,
        result=execution.result,
        handoff=execution.handoff,
        tradingview_manifest=execution.tradingview_manifest,
        record=execution.record,
        context=context,
    )
