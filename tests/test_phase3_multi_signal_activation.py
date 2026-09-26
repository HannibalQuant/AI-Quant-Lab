"""Sprint 26 activation of the existing multi-signal research-to-Pine workflow."""

from __future__ import annotations

from pathlib import Path

from test_optimization_selection import _multi_signal_source

from ai_quant_lab.core.dataset_store import LocalDatasetRepository
from ai_quant_lab.core.model import (
    ArtifactId,
    AuthorityBindingId,
    ExecutionState,
    ObjectVersion,
    ProvenanceId,
    RunId,
    TraceabilityRef,
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
from ai_quant_lab.core.pine_strategy_intake import PineStrategyIntakeContext
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


def test_existing_multi_signal_pipeline_reaches_manual_tradingview_export(tmp_path: Path) -> None:
    evidence = _multi_signal_source(tmp_path)
    repository = LocalDatasetRepository(
        root=tmp_path / "vault-sprint-26-activation",
        allowed_root=tmp_path,
    )
    pine_context = PineStrategyIntakeContext(
        evidence.strategy,
        evidence,
        PINE_AUTHORITY,
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
        Phase3EndToEndStage.PINE_GENERATED,
        Phase3EndToEndStage.PINE_INTAKE_ACCEPTED,
        Phase3EndToEndStage.STATIC_SAFETY_PASSED,
        Phase3EndToEndStage.TRADINGVIEW_EXPORT_READY,
    )
    assert Phase3EndToEndStage.OPTIMIZATION_SELECTED not in execution.record.stages
    assert execution.record.optimization_selection_ref is None
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
