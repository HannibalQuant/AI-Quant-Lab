"""Sprint 23 authoritative current-order closure for the bounded Phase 3 manual TradingView path."""

from __future__ import annotations

from dataclasses import dataclass

from ai_quant_lab.core.dataset_store import LocalDatasetRepository, RepositoryWriteResult
from ai_quant_lab.core.experiment_contracts import ExperimentAuthorizationDecision
from ai_quant_lab.core.governed_pine_generator import (
    GovernedPineGenerationRequest,
    GovernedPineGenerationResult,
    GovernedPineGeneratorContext,
    generate_governed_pine_strategy,
    verify_governed_pine_generation,
)
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
from ai_quant_lab.core.optimization_contracts import SelectionDecision
from ai_quant_lab.core.phase3_end_to_end_closure_contracts import (
    Phase3EndToEndClosureRecord,
    Phase3EndToEndStage,
    Phase3EndToEndState,
)
from ai_quant_lab.core.pine_safety_validation import (
    PineSafetyAssessmentContext,
    PineSafetyAssessmentRequest,
    PineSafetyAssessmentResult,
    PineSafetyDecision,
    PineStaticRepaintStatus,
    assess_governed_pine_static_safety,
    verify_pine_static_safety_assessment,
)
from ai_quant_lab.core.pine_strategy_contracts import PineIntakeStatus
from ai_quant_lab.core.pine_strategy_intake import PineStrategyIntakeContext
from ai_quant_lab.core.real_csv_contracts import CsvAdmissionStatus
from ai_quant_lab.core.research_eligibility_contracts import (
    DeploymentAuthorizationStatus,
    ResearchDatasetEligibilityStatus,
)
from ai_quant_lab.core.robustness_validation_contracts import RobustnessDecision
from ai_quant_lab.core.scientific_validation_contracts import ScientificValidationDecision
from ai_quant_lab.core.tradingview_research_export import (
    TradingViewResearchExportContext,
    TradingViewResearchExportExecution,
    TradingViewResearchExportRequest,
    build_tradingview_research_export,
    verify_tradingview_research_export,
)
from ai_quant_lab.core.tradingview_research_export_contracts import (
    TradingViewResearchExportReadiness,
    TradingViewResearchExportRuntimeStatus,
)

_V1 = ObjectVersion(1)


class Phase3EndToEndClosureError(ValueError):
    pass


class Phase3EndToEndClosureAuthorityInvalid(Phase3EndToEndClosureError):
    pass


class Phase3EndToEndClosureNotReady(Phase3EndToEndClosureError):
    pass


class Phase3EndToEndClosureLineageMismatch(Phase3EndToEndClosureError):
    pass


@dataclass(frozen=True, slots=True)
class Phase3EndToEndClosureRequest:
    closure_run_id: RunId
    closure_id: ArtifactId
    script_title: str
    file_stem: str
    generator_authority_ref: TraceabilityRef
    safety_authority_ref: TraceabilityRef
    export_authority_ref: TraceabilityRef
    closure_authority_ref: TraceabilityRef
    provenance_ref: TraceabilityRef
    contract_version: ObjectVersion = _V1

    def __post_init__(self) -> None:
        if (
            not isinstance(self.closure_run_id, RunId)
            or not isinstance(self.closure_id, ArtifactId)
            or not isinstance(self.script_title, str)
            or not self.script_title
            or not isinstance(self.file_stem, str)
            or not self.file_stem
            or self.contract_version != _V1
        ):
            raise Phase3EndToEndClosureError("invalid Phase 3 end-to-end closure request")
        for reference, expected, field in (
            (self.generator_authority_ref, AuthorityBindingId, "generator_authority_ref"),
            (self.safety_authority_ref, AuthorityBindingId, "safety_authority_ref"),
            (self.export_authority_ref, AuthorityBindingId, "export_authority_ref"),
            (self.closure_authority_ref, AuthorityBindingId, "closure_authority_ref"),
            (self.provenance_ref, ProvenanceId, "provenance_ref"),
        ):
            _exact_ref(reference, expected, field)


@dataclass(frozen=True, slots=True)
class Phase3EndToEndClosureContext:
    pine_context: PineStrategyIntakeContext
    closure_authority_ref: TraceabilityRef

    def __post_init__(self) -> None:
        _exact_ref(
            self.closure_authority_ref,
            AuthorityBindingId,
            "closure_authority_ref",
        )


@dataclass(frozen=True, slots=True)
class Phase3EndToEndClosureExecution:
    generation_request: GovernedPineGenerationRequest
    generation_result: GovernedPineGenerationResult
    safety_request: PineSafetyAssessmentRequest
    safety_result: PineSafetyAssessmentResult
    export_request: TradingViewResearchExportRequest
    export_execution: TradingViewResearchExportExecution
    record: Phase3EndToEndClosureRecord
    record_write: RepositoryWriteResult


def _exact_ref(reference: TraceabilityRef, expected: type[object], field: str) -> None:
    if (
        not isinstance(reference, TraceabilityRef)
        or reference.expected_fingerprint is None
        or not isinstance(reference.object_id, expected)
    ):
        raise Phase3EndToEndClosureError(
            f"{field} must be an exact fingerprint-bearing {expected.__name__} reference"
        )


def _exact(record: object, object_id: object, version: ObjectVersion) -> TraceabilityRef:
    return TraceabilityRef(object_id, version, fingerprint_record(record))  # type: ignore[arg-type]


def _token(base: str, suffix: str) -> str:
    required = len(suffix) + 1
    if required >= 63:
        raise Phase3EndToEndClosureError("derived identifier suffix is too long")
    return f"{base[: 63 - required]}-{suffix}"


def _verify_upstream_ready(context: Phase3EndToEndClosureContext) -> None:
    pine = context.pine_context
    evidence = pine.evidence
    if evidence.admission.status is not CsvAdmissionStatus.ADMITTED:
        raise Phase3EndToEndClosureNotReady("Phase 3 closure requires admitted real CSV evidence")
    if evidence.eligibility.status is not ResearchDatasetEligibilityStatus.ELIGIBLE:
        raise Phase3EndToEndClosureNotReady("Phase 3 closure requires eligible dataset evidence")
    if evidence.authorization.status is not ExperimentAuthorizationDecision.AUTHORIZED:
        raise Phase3EndToEndClosureNotReady(
            "Phase 3 closure requires authorized experiment evidence"
        )
    if evidence.scientific_result.decision is not ScientificValidationDecision.PASS:
        raise Phase3EndToEndClosureNotReady("Phase 3 closure requires scientific validation PASS")
    if evidence.robustness_result.decision is not RobustnessDecision.PASS:
        raise Phase3EndToEndClosureNotReady("Phase 3 closure requires robustness PASS")

    optimization = pine.optimization
    if optimization is not None:
        if (
            optimization.result.decision is not SelectionDecision.SELECTED
            or optimization.result.selected_candidate_ref is None
        ):
            raise Phase3EndToEndClosureNotReady(
                "optimized Phase 3 closure requires a selected candidate"
            )


def _stages(context: Phase3EndToEndClosureContext) -> tuple[Phase3EndToEndStage, ...]:
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
    if context.pine_context.optimization is not None:
        return base + (Phase3EndToEndStage.OPTIMIZATION_SELECTED,) + tail
    return base + tail


def _build_record(
    request: Phase3EndToEndClosureRequest,
    *,
    context: Phase3EndToEndClosureContext,
    generation_result: GovernedPineGenerationResult,
    safety_result: PineSafetyAssessmentResult,
    export_execution: TradingViewResearchExportExecution,
) -> Phase3EndToEndClosureRecord:
    evidence = context.pine_context.evidence
    optimization = context.pine_context.optimization
    optimization_ref = (
        None
        if optimization is None
        else _exact(
            optimization.result,
            optimization.result.selection_result_id,
            optimization.result.version,
        )
    )
    package = export_execution.package
    return Phase3EndToEndClosureRecord(
        request.closure_id,
        _V1,
        request.closure_run_id,
        _exact(
            evidence.declaration, evidence.declaration.provenance_id, evidence.declaration.version
        ),
        _exact(evidence.admission, evidence.admission.admission_id, evidence.admission.version),
        _exact(
            evidence.eligibility,
            evidence.eligibility.eligibility_id,
            evidence.eligibility.version,
        ),
        _exact(
            evidence.authorization,
            evidence.authorization.authorization_id,
            evidence.authorization.version,
        ),
        _exact(evidence.strategy, evidence.strategy.strategy_id, evidence.strategy.version),
        _exact(
            evidence.backtest_artifact,
            evidence.backtest_artifact.artifact_id,
            evidence.backtest_artifact.version,
        ),
        _exact(
            evidence.scientific_result,
            evidence.scientific_result.validation_result_id,
            evidence.scientific_result.version,
        ),
        _exact(
            evidence.robustness_result,
            evidence.robustness_result.robustness_result_id,
            evidence.robustness_result.version,
        ),
        optimization_ref,
        _exact(
            generation_result.artifact,
            generation_result.artifact.pine_artifact_id,
            generation_result.artifact.version,
        ),
        safety_result.assessment_id,
        safety_result.input_fingerprint,
        _exact(package, package.export_id, package.version),
        _stages(context),
        Phase3EndToEndState.READY_FOR_MANUAL_TRADINGVIEW_RESEARCH,
        package.runtime_status,
        request.closure_authority_ref,
        request.provenance_ref,
        DeploymentAuthorizationStatus.NOT_AUTHORIZED,
        ExecutionState.PLANNED_CLOSED,
        _V1,
    )


def run_phase3_end_to_end_closure(
    request: Phase3EndToEndClosureRequest,
    *,
    context: Phase3EndToEndClosureContext,
    repository: LocalDatasetRepository,
) -> Phase3EndToEndClosureExecution:
    """Run the authoritative current-order Phase 3 path to a manual TradingView export."""
    if request.closure_authority_ref != context.closure_authority_ref:
        raise Phase3EndToEndClosureAuthorityInvalid(
            "closure request lacks exact governed closure authority"
        )
    _verify_upstream_ready(context)

    pine_context = context.pine_context
    strategy_ref = _exact(
        pine_context.strategy,
        pine_context.strategy.strategy_id,
        pine_context.strategy.version,
    )
    base = request.closure_id.value

    generator_context = GovernedPineGeneratorContext(
        pine_context,
        request.generator_authority_ref,
    )
    generation_request = GovernedPineGenerationRequest(
        RunId(_token(base, "gen-run")),
        RunId(_token(base, "intake-run")),
        ArtifactId(_token(base, "pine")),
        strategy_ref,
        request.script_title,
        request.generator_authority_ref,
        pine_context.pine_intake_authority_ref,
        request.provenance_ref,
    )
    generation_result = generate_governed_pine_strategy(
        generation_request,
        context=generator_context,
        repository=repository,
    )
    verify_governed_pine_generation(
        generation_request,
        result=generation_result,
        context=generator_context,
    )
    if generation_result.intake_record.status is not PineIntakeStatus.ACCEPTED:
        raise Phase3EndToEndClosureNotReady("generated Pine did not pass governed intake")

    artifact_ref = _exact(
        generation_result.artifact,
        generation_result.artifact.pine_artifact_id,
        generation_result.artifact.version,
    )
    safety_context = PineSafetyAssessmentContext(
        generation_request,
        generation_result,
        generator_context,
        request.safety_authority_ref,
    )
    safety_request = PineSafetyAssessmentRequest(
        RunId(_token(base, "safety-run")),
        ArtifactId(_token(base, "safety")),
        artifact_ref,
        strategy_ref,
        generation_result.generation_input_fingerprint,
        request.safety_authority_ref,
        request.provenance_ref,
    )
    safety_result = assess_governed_pine_static_safety(
        safety_request,
        context=safety_context,
    )
    verify_pine_static_safety_assessment(
        safety_request,
        result=safety_result,
        context=safety_context,
    )
    if (
        safety_result.decision is not PineSafetyDecision.PASS
        or safety_result.static_repaint_status
        is not PineStaticRepaintStatus.NO_STATIC_REPAINT_HAZARD_DETECTED
    ):
        raise Phase3EndToEndClosureNotReady("generated Pine failed the bounded static safety gate")

    export_context = TradingViewResearchExportContext(
        generation_request,
        generation_result,
        generator_context,
        safety_request,
        safety_result,
        safety_context,
        request.export_authority_ref,
    )
    export_request = TradingViewResearchExportRequest(
        RunId(_token(base, "export-run")),
        ArtifactId(_token(base, "export")),
        artifact_ref,
        strategy_ref,
        safety_result.assessment_id,
        safety_result.input_fingerprint,
        request.file_stem,
        request.export_authority_ref,
        request.provenance_ref,
    )
    export_execution = build_tradingview_research_export(
        export_request,
        context=export_context,
        repository=repository,
    )
    verify_tradingview_research_export(
        export_request,
        package=export_execution.package,
        context=export_context,
    )
    if (
        export_execution.package.readiness
        is not TradingViewResearchExportReadiness.READY_FOR_MANUAL_TRADINGVIEW_RESEARCH
        or export_execution.package.runtime_status
        is not TradingViewResearchExportRuntimeStatus.NOT_VERIFIED_ON_TRADINGVIEW
    ):
        raise Phase3EndToEndClosureNotReady(
            "TradingView export is not in the governed manual-research state"
        )

    record = _build_record(
        request,
        context=context,
        generation_result=generation_result,
        safety_result=safety_result,
        export_execution=export_execution,
    )
    write = repository.store(record)
    return Phase3EndToEndClosureExecution(
        generation_request,
        generation_result,
        safety_request,
        safety_result,
        export_request,
        export_execution,
        record,
        write,
    )


def verify_phase3_end_to_end_closure(
    request: Phase3EndToEndClosureRequest,
    *,
    execution: Phase3EndToEndClosureExecution,
    context: Phase3EndToEndClosureContext,
) -> None:
    """Verify the exact final closure without rerunning or contacting an external platform."""
    if request.closure_authority_ref != context.closure_authority_ref:
        raise Phase3EndToEndClosureAuthorityInvalid(
            "closure verification lacks exact governed closure authority"
        )
    _verify_upstream_ready(context)

    generator_context = GovernedPineGeneratorContext(
        context.pine_context,
        request.generator_authority_ref,
    )
    verify_governed_pine_generation(
        execution.generation_request,
        result=execution.generation_result,
        context=generator_context,
    )
    safety_context = PineSafetyAssessmentContext(
        execution.generation_request,
        execution.generation_result,
        generator_context,
        request.safety_authority_ref,
    )
    verify_pine_static_safety_assessment(
        execution.safety_request,
        result=execution.safety_result,
        context=safety_context,
    )
    export_context = TradingViewResearchExportContext(
        execution.generation_request,
        execution.generation_result,
        generator_context,
        execution.safety_request,
        execution.safety_result,
        safety_context,
        request.export_authority_ref,
    )
    verify_tradingview_research_export(
        execution.export_request,
        package=execution.export_execution.package,
        context=export_context,
    )
    expected_record = _build_record(
        request,
        context=context,
        generation_result=execution.generation_result,
        safety_result=execution.safety_result,
        export_execution=execution.export_execution,
    )
    if execution.record != expected_record:
        raise Phase3EndToEndClosureLineageMismatch(
            "Phase 3 end-to-end closure record differs from exact current-order reconstruction"
        )
