"""Sprint 19 integrated research workflow tests."""

# mypy: disable-error-code="no-untyped-def,no-untyped-call,arg-type"

from __future__ import annotations

import json
from dataclasses import fields, replace
from pathlib import Path

import pytest
from test_pine_python_parity import (
    PARITY_AUTHORITY_REF,
    _csv_bytes,
    _event_rows,
    _run as run_parity,
)
from test_pine_strategy_intake import PROVENANCE_REF, _direct_context

from ai_quant_lab.core.codec import decode, encode
from ai_quant_lab.core.dataset_store import (
    LocalDatasetRepository,
    RepositoryWriteStatus,
    repository_key,
)
from ai_quant_lab.core.experiment_contracts import ExperimentAuthorizationDecision
from ai_quant_lab.core.integrated_research_workflow import (
    IntegratedResearchWorkflowAuthorityInvalid,
    IntegratedResearchWorkflowContext,
    IntegratedResearchWorkflowLineageMismatch,
    derive_final_workflow_state,
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
    WorkflowReasonCode,
)
from ai_quant_lab.core.integrity import fingerprint_record
from ai_quant_lab.core.model import (
    AgentId,
    ArtifactId,
    AuthorityBindingId,
    ExecutionState,
    ObjectVersion,
    RunId,
    TraceabilityRef,
)
from ai_quant_lab.core.optimization_contracts import SelectionDecision
from ai_quant_lab.core.pine_python_parity import (
    PinePythonParityContext,
    evaluate_pine_python_parity,
    import_pine_execution_csv,
)
from ai_quant_lab.core.pine_python_parity_contracts import (
    ParityTolerancePolicy,
    PinePythonParityDecision,
    PinePythonParityRequest,
)
from ai_quant_lab.core.pine_strategy_intake import intake_pine_strategy
from ai_quant_lab.core.research_eligibility_contracts import DeploymentAuthorizationStatus
from ai_quant_lab.core.robustness_validation_contracts import RobustnessDecision
from ai_quant_lab.core.scientific_validation_contracts import ScientificValidationDecision

pytest_plugins = ("test_pine_python_parity",)

V1 = ObjectVersion(1)
GOLDEN = Path(__file__).parent / "golden" / "integrated_research_workflow_v1.json"
WORKFLOW_AUTHORITY = TraceabilityRef(
    AuthorityBindingId("integrated-research-workflow-authority"),
    V1,
    "sha256:" + "e" * 64,
)
PINE_AGENT = TraceabilityRef(
    AgentId("pine-generation-agent"),
    V1,
    "sha256:" + "f" * 64,
)


def exact(record, object_id, version):
    return TraceabilityRef(object_id, version, fingerprint_record(record))


def unsafe(record, **changes):
    values = {field.name: getattr(record, field.name) for field in fields(record)}
    values.update(changes)
    clone = object.__new__(type(record))
    for name, value in values.items():
        object.__setattr__(clone, name, value)
    return clone


@pytest.fixture
def workflow_bundle(parity_bundle, tmp_path: Path):
    parity_execution, parity_request = run_parity(parity_bundle)
    final = parity_bundle[0]
    parity_context = parity_bundle[4]
    optimization = parity_context.pine_intake_context.optimization
    assert optimization is not None
    parent = optimization.source.strategy

    proposer = TraceabilityRef(
        final.specification.proposer_id,
        V1,
        "sha256:" + "d" * 64,
    )
    proposal = AIStrategyProposal(
        ArtifactId("integrated-ai-strategy-proposal"),
        V1,
        proposer,
        parent.model.value,
        "Synthetic governed strategy proposal for integration verification.",
        (("threshold_bps", str(parent.threshold_bps)),),
        exact(parent, parent.strategy_id, parent.version),
        AIStrategyProposalStatus.ACCEPTED_FOR_RESEARCH,
        ProposalAuthorityState.PROPOSAL_ONLY,
        PROVENANCE_REF,
        V1,
    )
    selection_ref = exact(
        optimization.result,
        optimization.result.selection_result_id,
        optimization.result.version,
    )
    plan = IntegratedResearchWorkflowPlan(
        ArtifactId("integrated-research-workflow-plan"),
        V1,
        IntegratedResearchWorkflowMode.OPTIMIZED_STRATEGY,
        exact(proposal, proposal.proposal_id, proposal.version),
        exact(parent, parent.strategy_id, parent.version),
        exact(final.strategy, final.strategy.strategy_id, final.strategy.version),
        final.backtest_artifact.normalized_manifest_ref,
        final.backtest_artifact.normalized_lock_ref,
        exact(final.instrument, final.instrument.instrument_id, final.instrument.version),
        exact(
            final.authorization,
            final.authorization.authorization_id,
            final.authorization.version,
        ),
        exact(
            final.validation_plan,
            final.validation_plan.validation_plan_id,
            final.validation_plan.version,
        ),
        exact(
            final.robustness_plan,
            final.robustness_plan.robustness_plan_id,
            final.robustness_plan.version,
        ),
        selection_ref,
        parity_context.pine_intake_context.pine_intake_authority_ref,
        parity_context.parity_authority_ref,
        WORKFLOW_AUTHORITY,
        PROVENANCE_REF,
        V1,
    )
    request = IntegratedResearchWorkflowRequest(
        RunId("integrated-research-workflow-run"),
        ArtifactId("integrated-research-workflow-result"),
        ArtifactId("integrated-research-handoff"),
        ArtifactId("integrated-tradingview-handoff"),
        exact(plan, plan.workflow_plan_id, plan.version),
        exact(proposal, proposal.proposal_id, proposal.version),
        exact(
            parity_context.pine_artifact,
            parity_context.pine_artifact.pine_artifact_id,
            parity_context.pine_artifact.version,
        ),
        exact(
            parity_context.pine_intake_record,
            parity_context.pine_intake_record.intake_run_id,
            parity_context.pine_intake_record.version,
        ),
        exact(
            parity_execution.result,
            parity_execution.result.parity_result_id,
            parity_execution.result.version,
        ),
        WORKFLOW_AUTHORITY,
        PROVENANCE_REF,
        V1,
    )
    context = IntegratedResearchWorkflowContext(
        final,
        optimization,
        parity_request,
        parity_bundle[2],
        parity_bundle[1],
        parity_execution.result,
        parity_execution.record,
        parity_context,
        WORKFLOW_AUTHORITY,
        PINE_AGENT,
    )
    repository = LocalDatasetRepository(
        root=tmp_path / "integrated-workflow",
        allowed_root=tmp_path,
    )
    return proposal, plan, request, context, repository


def run_workflow(bundle):
    proposal, plan, request, context, repository = bundle
    execution = evaluate_integrated_research_workflow(
        proposal,
        plan,
        request,
        context=context,
        repository=repository,
    )
    return execution


def test_full_optimized_pipeline_reaches_research_handoff(workflow_bundle):
    execution = run_workflow(workflow_bundle)
    assert execution.result.final_state is IntegratedResearchWorkflowState.RESEARCH_HANDOFF_READY
    assert execution.handoff is not None
    assert execution.tradingview_manifest is not None
    assert execution.handoff.readiness is ResearchHandoffReadiness.READY_FOR_HUMAN_RESEARCH_USE
    assert execution.handoff.parity_decision is PinePythonParityDecision.MATCH
    assert execution.result.deployment_authorization is DeploymentAuthorizationStatus.NOT_AUTHORIZED
    assert execution.result.execution_state is ExecutionState.PLANNED_CLOSED
    assert (
        execution.handoff.deployment_authorization is DeploymentAuthorizationStatus.NOT_AUTHORIZED
    )
    assert execution.handoff.execution_state is ExecutionState.PLANNED_CLOSED
    assert all(item.status is RepositoryWriteStatus.STORED_NEW for item in execution.writes)
    verify_integrated_research_workflow_lineage(
        proposal=workflow_bundle[0],
        plan=workflow_bundle[1],
        request=workflow_bundle[2],
        result=execution.result,
        handoff=execution.handoff,
        tradingview_manifest=execution.tradingview_manifest,
        record=execution.record,
        context=workflow_bundle[3],
    )


def test_fail_and_inconclusive_mapping_remains_distinct():
    common = dict(
        proposal_status=AIStrategyProposalStatus.ACCEPTED_FOR_RESEARCH,
        authorization=ExperimentAuthorizationDecision.AUTHORIZED,
        scientific=ScientificValidationDecision.PASS,
        robustness=RobustnessDecision.PASS,
        optimization=SelectionDecision.SELECTED,
        parity=PinePythonParityDecision.MATCH,
        pine_intake_accepted=True,
    )
    rejected, reasons = derive_final_workflow_state(
        **{**common, "scientific": ScientificValidationDecision.FAIL}
    )
    assert rejected is IntegratedResearchWorkflowState.RESEARCH_REJECTED
    assert reasons == (WorkflowReasonCode.SCIENTIFIC_VALIDATION_FAILED,)

    inconclusive, reasons = derive_final_workflow_state(
        **{**common, "scientific": ScientificValidationDecision.INCONCLUSIVE}
    )
    assert inconclusive is IntegratedResearchWorkflowState.RESEARCH_INCONCLUSIVE
    assert reasons == (WorkflowReasonCode.SCIENTIFIC_VALIDATION_INCONCLUSIVE,)

    rejected, reasons = derive_final_workflow_state(
        **{**common, "robustness": RobustnessDecision.FAIL}
    )
    assert rejected is IntegratedResearchWorkflowState.RESEARCH_REJECTED
    assert reasons == (WorkflowReasonCode.ROBUSTNESS_FAILED,)

    rejected, reasons = derive_final_workflow_state(
        **{**common, "parity": PinePythonParityDecision.MISMATCH}
    )
    assert rejected is IntegratedResearchWorkflowState.RESEARCH_REJECTED
    assert reasons == (WorkflowReasonCode.PARITY_MISMATCH,)

    inconclusive, reasons = derive_final_workflow_state(
        **{**common, "parity": PinePythonParityDecision.INCONCLUSIVE}
    )
    assert inconclusive is IntegratedResearchWorkflowState.RESEARCH_INCONCLUSIVE
    assert reasons == (WorkflowReasonCode.PARITY_INCONCLUSIVE,)

    direct, reasons = derive_final_workflow_state(**{**common, "optimization": None})
    assert direct is IntegratedResearchWorkflowState.RESEARCH_HANDOFF_READY
    assert reasons == (WorkflowReasonCode.RESEARCH_HANDOFF_READY,)


def test_wrong_workflow_authority_fails_closed(workflow_bundle):
    wrong = TraceabilityRef(
        AuthorityBindingId("wrong-integrated-workflow-authority"),
        V1,
        "sha256:" + "1" * 64,
    )
    request = replace(workflow_bundle[2], workflow_authority_ref=wrong)
    with pytest.raises(IntegratedResearchWorkflowAuthorityInvalid):
        evaluate_integrated_research_workflow(
            workflow_bundle[0],
            workflow_bundle[1],
            request,
            context=workflow_bundle[3],
            repository=workflow_bundle[4],
        )


def test_dataset_and_strategy_substitution_fail_lineage(workflow_bundle):
    wrong_lock = TraceabilityRef(
        workflow_bundle[1].normalized_lock_ref.object_id,
        workflow_bundle[1].normalized_lock_ref.version,
        "sha256:" + "2" * 64,
    )
    bad_plan = replace(workflow_bundle[1], normalized_lock_ref=wrong_lock)
    bad_request = replace(
        workflow_bundle[2],
        workflow_plan_ref=exact(bad_plan, bad_plan.workflow_plan_id, bad_plan.version),
    )
    with pytest.raises(IntegratedResearchWorkflowLineageMismatch):
        evaluate_integrated_research_workflow(
            workflow_bundle[0],
            bad_plan,
            bad_request,
            context=workflow_bundle[3],
            repository=workflow_bundle[4],
        )

    wrong_strategy = TraceabilityRef(
        workflow_bundle[1].final_strategy_ref.object_id,
        workflow_bundle[1].final_strategy_ref.version,
        "sha256:" + "3" * 64,
    )
    bad_plan = replace(workflow_bundle[1], final_strategy_ref=wrong_strategy)
    bad_request = replace(
        workflow_bundle[2],
        workflow_plan_ref=exact(bad_plan, bad_plan.workflow_plan_id, bad_plan.version),
    )
    with pytest.raises(IntegratedResearchWorkflowLineageMismatch):
        evaluate_integrated_research_workflow(
            workflow_bundle[0],
            bad_plan,
            bad_request,
            context=workflow_bundle[3],
            repository=workflow_bundle[4],
        )


def test_handoff_tamper_is_rejected(workflow_bundle):
    execution = run_workflow(workflow_bundle)
    assert execution.handoff is not None
    tampered = unsafe(
        execution.handoff,
        readiness=ResearchHandoffReadiness.NOT_READY,
    )
    with pytest.raises(IntegratedResearchWorkflowLineageMismatch):
        verify_integrated_research_workflow_lineage(
            proposal=workflow_bundle[0],
            plan=workflow_bundle[1],
            request=workflow_bundle[2],
            result=execution.result,
            handoff=tampered,
            tradingview_manifest=execution.tradingview_manifest,
            record=execution.record,
            context=workflow_bundle[3],
        )


def test_agent_traceability_is_preserved(workflow_bundle):
    execution = run_workflow(workflow_bundle)
    assert execution.handoff is not None
    assert execution.handoff.proposing_agent_ref == workflow_bundle[0].proposing_agent_ref
    assert execution.handoff.pine_generating_agent_ref == PINE_AGENT
    assert execution.handoff.proposing_agent_ref.object_id == (
        workflow_bundle[3].final_evidence.specification.proposer_id
    )


def test_codec_roundtrip_and_repository_idempotency(workflow_bundle):
    execution = run_workflow(workflow_bundle)
    assert execution.handoff is not None
    assert execution.tradingview_manifest is not None
    repository = workflow_bundle[4]
    records = (
        workflow_bundle[0],
        workflow_bundle[1],
        execution.handoff,
        execution.tradingview_manifest,
        execution.result,
        execution.record,
    )
    for record in records:
        assert decode(encode(record), type(record)) == record
        assert repository.store(record).status is RepositoryWriteStatus.ALREADY_PRESENT_IDENTICAL
        loaded = repository.load(repository_key(record), type(record))
        assert loaded.record == record


def test_no_success_path_opens_deployment_or_execution(workflow_bundle):
    execution = run_workflow(workflow_bundle)
    records = [
        execution.result,
        execution.record,
        execution.handoff,
        execution.tradingview_manifest,
    ]
    for record in records:
        assert record is not None
        assert record.deployment_authorization is DeploymentAuthorizationStatus.NOT_AUTHORIZED
        assert record.execution_state is ExecutionState.PLANNED_CLOSED


def test_integrated_workflow_golden_is_pinned(workflow_bundle):
    execution = run_workflow(workflow_bundle)
    assert execution.handoff is not None
    assert execution.tradingview_manifest is not None
    expected = {
        "format": "integrated-research-workflow-v1",
        "proposal_ref": str(execution.result.proposal_ref.object_id),
        "final_strategy_ref": str(execution.result.final_strategy_ref.object_id),
        "backtest_ref": str(execution.handoff.backtest_ref.object_id),
        "scientific_validation_ref": str(execution.handoff.scientific_validation_ref.object_id),
        "robustness_ref": str(execution.handoff.robustness_ref.object_id),
        "optimization_selection_ref": str(execution.handoff.optimization_selection_ref.object_id),
        "pine_artifact_ref": str(execution.handoff.pine_artifact_ref.object_id),
        "parity_ref": str(execution.handoff.parity_result_ref.object_id),
        "final_state": execution.result.final_state.value,
        "handoff_readiness": execution.handoff.readiness.value,
        "input_fingerprint": execution.result.input_fingerprint,
        "result_fingerprint": fingerprint_record(execution.result),
        "handoff_fingerprint": fingerprint_record(execution.handoff),
        "manifest_fingerprint": fingerprint_record(execution.tradingview_manifest),
        "run_fingerprint": fingerprint_record(execution.record),
    }
    assert json.loads(GOLDEN.read_text(encoding="utf-8")) == expected
