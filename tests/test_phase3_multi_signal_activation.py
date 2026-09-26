"""Sprint 26 activation of the existing multi-signal research-to-Pine workflow."""

from __future__ import annotations

from dataclasses import replace
from pathlib import Path

from test_optimization_selection import (
    _candidate_evidence_with_repository,
    _multi_signal_source,
    _request,
    optimization_plan,
)

from ai_quant_lab.core.dataset_store import LocalDatasetRepository
from ai_quant_lab.core.integrity import fingerprint_record
from ai_quant_lab.core.model import (
    ArtifactId,
    AuthorityBindingId,
    ExecutionState,
    ObjectVersion,
    ProvenanceId,
    RunId,
    TraceabilityRef,
)
from ai_quant_lab.core.optimization_contracts import (
    OptimizationMultiplicityPolicy,
    OptimizationParameter,
    OptimizationParameterName,
    OptimizationParameterType,
    OptimizationSearchSpace,
    SelectionDecision,
)
from ai_quant_lab.core.optimization_selection import (
    enumerate_parameter_sets,
    run_optimization_selection,
)
from ai_quant_lab.core.phase3_end_to_end_closure import (
    Phase3EndToEndClosureContext,
    Phase3EndToEndClosureRequest,
    run_phase3_end_to_end_closure,
    verify_phase3_end_to_end_closure,
)
from ai_quant_lab.core.phase3_end_to_end_closure_contracts import (
    Phase3EndToEndStage,
    Phase3EndToEndState,
)
from ai_quant_lab.core.pine_strategy_intake import (
    PineOptimizationSelectionEvidence,
    PineStrategyIntakeContext,
)
from ai_quant_lab.core.research_eligibility_contracts import DeploymentAuthorizationStatus
from ai_quant_lab.core.strategy_backtest_contracts import StrategyModel
from ai_quant_lab.core.tradingview_research_export_contracts import (
    TradingViewResearchExportReadiness,
    TradingViewResearchExportRuntimeStatus,
)

V1 = ObjectVersion(1)

PINE_AUTHORITY = TraceabilityRef(
    AuthorityBindingId("sprint-26-pine-intake-authority"), V1, "sha256:" + "1" * 64
)
GENERATOR_AUTHORITY = TraceabilityRef(
    AuthorityBindingId("sprint-26-generator-authority"), V1, "sha256:" + "2" * 64
)
SAFETY_AUTHORITY = TraceabilityRef(
    AuthorityBindingId("sprint-26-safety-authority"), V1, "sha256:" + "3" * 64
)
EXPORT_AUTHORITY = TraceabilityRef(
    AuthorityBindingId("sprint-26-export-authority"), V1, "sha256:" + "4" * 64
)
CLOSURE_AUTHORITY = TraceabilityRef(
    AuthorityBindingId("sprint-26-closure-authority"), V1, "sha256:" + "5" * 64
)
PROVENANCE = TraceabilityRef(
    ProvenanceId("sprint-26-research-activation"), V1, "sha256:" + "6" * 64
)


def exact(record: object, object_id: object, version: ObjectVersion) -> TraceabilityRef:
    return TraceabilityRef(object_id, version, fingerprint_record(record))  # type: ignore[arg-type]


def test_existing_multi_signal_pipeline_reaches_manual_tradingview_export(tmp_path: Path) -> None:
    source = _multi_signal_source(tmp_path)
    repository = LocalDatasetRepository(
        root=tmp_path / "vault-sprint-26-activation",
        allowed_root=tmp_path,
    )
    space = OptimizationSearchSpace(
        ArtifactId("sprint-26-multi-signal-search-space"),
        V1,
        (
            OptimizationParameter(
                OptimizationParameterName.ATR_STOP_MULT_X100,
                OptimizationParameterType.INTEGER,
                10_000,
                10_000,
                1,
                10_000,
            ),
        ),
        V1,
    )
    plan = replace(
        optimization_plan(
            source,
            space,
            multiplicity=OptimizationMultiplicityPolicy.SINGLE_CANDIDATE,
            maximum_trials=1,
        ),
        optimization_plan_id=ArtifactId("sprint-26-multi-signal-optimization-plan"),
        minimum_trade_count=1,
    )
    parameter_sets = enumerate_parameter_sets(space, plan.maximum_trials)
    candidates = (
        _candidate_evidence_with_repository(
            source,
            repository,
            plan,
            space,
            parameter_sets[0],
            1,
        ),
    )
    selection = run_optimization_selection(
        _request(plan),
        plan=plan,
        search_space=space,
        source=source,
        candidates=candidates,
        repository=repository,
    )
    assert selection.result.decision is SelectionDecision.SELECTED
    selected_ref = selection.result.selected_candidate_ref
    assert selected_ref is not None

    selected_index = next(
        index
        for index, result in enumerate(selection.candidate_results)
        if exact(result, result.candidate_id, result.version) == selected_ref
    )
    evidence = candidates[selected_index]
    optimization = PineOptimizationSelectionEvidence(
        _request(plan),
        plan,
        space,
        source,
        candidates,
        selection.record,
        selection.result,
        selection.candidate_definitions,
        selection.candidate_results,
        selection.trials,
    )
    pine_context = PineStrategyIntakeContext(
        evidence.strategy,
        evidence,
        PINE_AUTHORITY,
        optimization,
    )
    context = Phase3EndToEndClosureContext(pine_context, CLOSURE_AUTHORITY)
    request = Phase3EndToEndClosureRequest(
        RunId("sprint-26-closure-run"),
        ArtifactId("sprint-26-closure"),
        "AIQL SOLUSDT 4H Multi Signal Research",
        "AIQL_SOLUSDT_4H_multi_signal",
        GENERATOR_AUTHORITY,
        SAFETY_AUTHORITY,
        EXPORT_AUTHORITY,
        CLOSURE_AUTHORITY,
        PROVENANCE,
    )

    execution = run_phase3_end_to_end_closure(
        request,
        context=context,
        repository=repository,
    )
    verify_phase3_end_to_end_closure(
        request,
        execution=execution,
        context=context,
    )

    assert evidence.strategy.model is StrategyModel.MULTI_SIGNAL_TREND_LONG_SHORT
    assert (
        execution.generation_result.generator_profile
        == "AIQL_GOVERNED_PINE_V6_MULTI_SIGNAL_TREND_LONG_SHORT_V1"
    )
    assert 'strategy.entry("AIQL-L", strategy.long)' in execution.generation_result.source_text
    assert 'strategy.entry("AIQL-S", strategy.short)' in execution.generation_result.source_text
    assert execution.record.stages == (
        Phase3EndToEndStage.REAL_CSV_ADMITTED,
        Phase3EndToEndStage.DATASET_ELIGIBLE,
        Phase3EndToEndStage.EXPERIMENT_AUTHORIZED,
        Phase3EndToEndStage.BACKTEST_COMPLETED,
        Phase3EndToEndStage.SCIENTIFIC_VALIDATION_PASSED,
        Phase3EndToEndStage.ROBUSTNESS_PASSED,
        Phase3EndToEndStage.OPTIMIZATION_SELECTED,
        Phase3EndToEndStage.PINE_GENERATED,
        Phase3EndToEndStage.PINE_INTAKE_ACCEPTED,
        Phase3EndToEndStage.STATIC_SAFETY_PASSED,
        Phase3EndToEndStage.TRADINGVIEW_EXPORT_READY,
    )
    assert execution.record.final_state is Phase3EndToEndState.READY_FOR_MANUAL_TRADINGVIEW_RESEARCH
    assert (
        execution.export_execution.package.readiness
        is TradingViewResearchExportReadiness.READY_FOR_MANUAL_TRADINGVIEW_RESEARCH
    )
    assert (
        execution.record.runtime_status
        is TradingViewResearchExportRuntimeStatus.NOT_VERIFIED_ON_TRADINGVIEW
    )
    assert execution.record.deployment_authorization is DeploymentAuthorizationStatus.NOT_AUTHORIZED
    assert execution.record.execution_state is ExecutionState.PLANNED_CLOSED
