"""Deterministic governed export package for manual TradingView research."""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Final

from ai_quant_lab.core.dataset_store import LocalDatasetRepository, RepositoryWriteResult
from ai_quant_lab.core.governed_pine_generator import (
    GovernedPineGenerationRequest,
    GovernedPineGenerationResult,
    GovernedPineGeneratorContext,
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
    canonical_json,
)
from ai_quant_lab.core.pine_safety_validation import (
    PineSafetyAssessmentContext,
    PineSafetyAssessmentRequest,
    PineSafetyAssessmentResult,
    PineSafetyDecision,
    PineStaticRepaintStatus,
    verify_pine_static_safety_assessment,
)
from ai_quant_lab.core.research_eligibility_contracts import DeploymentAuthorizationStatus
from ai_quant_lab.core.tradingview_research_export_contracts import (
    TradingViewResearchExportPackage,
    TradingViewResearchExportReadiness,
    TradingViewResearchExportRuntimeStatus,
    TradingViewResearchExportSafetyStatus,
)

_V1 = ObjectVersion(1)
_FILE_STEM: Final = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_-]{0,63}$")


class TradingViewResearchExportError(ValueError):
    pass


class TradingViewResearchExportAuthorityInvalid(TradingViewResearchExportError):
    pass


class TradingViewResearchExportLineageMismatch(TradingViewResearchExportError):
    pass


class TradingViewResearchExportNotReady(TradingViewResearchExportError):
    pass


@dataclass(frozen=True, slots=True)
class TradingViewResearchExportRequest:
    export_run_id: RunId
    export_id: ArtifactId
    pine_artifact_ref: TraceabilityRef
    strategy_ref: TraceabilityRef
    safety_assessment_id: ArtifactId
    safety_input_fingerprint: str
    file_stem: str
    export_authority_ref: TraceabilityRef
    provenance_ref: TraceabilityRef
    contract_version: ObjectVersion = _V1

    def __post_init__(self) -> None:
        if (
            not isinstance(self.export_run_id, RunId)
            or not isinstance(self.export_id, ArtifactId)
            or not isinstance(self.safety_assessment_id, ArtifactId)
            or not isinstance(self.safety_input_fingerprint, str)
            or not re.fullmatch(r"sha256:[0-9a-f]{64}", self.safety_input_fingerprint)
            or not isinstance(self.file_stem, str)
            or _FILE_STEM.fullmatch(self.file_stem) is None
            or self.contract_version != _V1
        ):
            raise TradingViewResearchExportError("invalid TradingView research export request")
        _exact_ref(self.pine_artifact_ref, ArtifactId, "pine_artifact_ref")
        _exact_ref(self.strategy_ref, ArtifactId, "strategy_ref")
        _exact_ref(self.export_authority_ref, AuthorityBindingId, "export_authority_ref")
        _exact_ref(self.provenance_ref, ProvenanceId, "provenance_ref")


@dataclass(frozen=True, slots=True)
class TradingViewResearchExportContext:
    generation_request: GovernedPineGenerationRequest
    generation_result: GovernedPineGenerationResult
    generator_context: GovernedPineGeneratorContext
    safety_request: PineSafetyAssessmentRequest
    safety_result: PineSafetyAssessmentResult
    safety_context: PineSafetyAssessmentContext
    export_authority_ref: TraceabilityRef

    def __post_init__(self) -> None:
        _exact_ref(
            self.export_authority_ref,
            AuthorityBindingId,
            "export_authority_ref",
        )


@dataclass(frozen=True, slots=True)
class TradingViewResearchExportExecution:
    package: TradingViewResearchExportPackage
    package_ref: TraceabilityRef
    write: RepositoryWriteResult
    pine_bytes: bytes
    manifest_bytes: bytes


def _exact_ref(
    ref: TraceabilityRef,
    expected_type: type[object],
    field: str,
) -> None:
    if (
        not isinstance(ref, TraceabilityRef)
        or ref.expected_fingerprint is None
        or not isinstance(ref.object_id, expected_type)
    ):
        raise TradingViewResearchExportError(
            f"{field} must be an exact fingerprint-bearing {expected_type.__name__} reference"
        )


def _exact(record: object, object_id: object, version: ObjectVersion) -> TraceabilityRef:
    return TraceabilityRef(object_id, version, fingerprint_record(record))  # type: ignore[arg-type]


def _verify_boundary(
    request: TradingViewResearchExportRequest,
    *,
    context: TradingViewResearchExportContext,
) -> None:
    if request.export_authority_ref != context.export_authority_ref:
        raise TradingViewResearchExportAuthorityInvalid(
            "export request lacks exact governed export authority"
        )
    try:
        verify_governed_pine_generation(
            context.generation_request,
            result=context.generation_result,
            context=context.generator_context,
        )
        verify_pine_static_safety_assessment(
            context.safety_request,
            result=context.safety_result,
            context=context.safety_context,
        )
    except ValueError as exc:
        raise TradingViewResearchExportLineageMismatch(
            "export requires exact verified generator and safety lineage"
        ) from exc

    generation = context.generation_result
    artifact = generation.artifact
    expected_artifact_ref = _exact(artifact, artifact.pine_artifact_id, artifact.version)
    if (
        request.pine_artifact_ref != expected_artifact_ref
        or request.strategy_ref != artifact.strategy_definition_ref
        or request.safety_assessment_id != context.safety_result.assessment_id
        or request.safety_input_fingerprint != context.safety_result.input_fingerprint
        or request.provenance_ref != artifact.provenance_ref
        or context.safety_result.pine_artifact_ref != expected_artifact_ref
        or context.safety_result.strategy_definition_ref != request.strategy_ref
        or context.safety_result.source_sha256 != artifact.source_sha256
        or context.safety_result.normalized_source_sha256 != artifact.normalized_source_sha256
    ):
        raise TradingViewResearchExportLineageMismatch(
            "export request does not bind exact Pine, strategy and safety evidence"
        )
    if (
        context.safety_result.decision is not PineSafetyDecision.PASS
        or context.safety_result.static_repaint_status
        is not PineStaticRepaintStatus.NO_STATIC_REPAINT_HAZARD_DETECTED
    ):
        raise TradingViewResearchExportNotReady(
            "manual TradingView export requires static safety PASS"
        )


def _strategy_parameters(context: TradingViewResearchExportContext) -> tuple[tuple[str, str], ...]:
    strategy = context.generator_context.pine_intake_context.strategy
    values = {
        "allow_pyramiding": str(strategy.allow_pyramiding).lower(),
        "capital_currency": strategy.capital_currency,
        "capital_minor_unit_scale": str(strategy.capital_minor_unit_scale),
        "execution_timing": strategy.execution_timing.value,
        "fixed_notional_minor": str(strategy.fixed_notional_minor),
        "force_close_at_window_end": str(strategy.force_close_at_window_end).lower(),
        "model": strategy.model.value,
        "side_permission": strategy.side_permission.value,
        "signal_timing": strategy.signal_timing.value,
        "threshold_bps": str(strategy.threshold_bps),
    }
    return tuple(sorted(values.items()))


def _manual_steps(
    *,
    symbol: str,
    timeframe_token: str,
    pine_filename: str,
) -> tuple[str, ...]:
    return (
        f"Open a TradingView chart for the governed instrument symbol: {symbol}.",
        f"Set the chart timeframe to the governed timeframe token: {timeframe_token}.",
        "Open Pine Editor and create a new strategy script.",
        f"Replace the editor contents with the exact source from {pine_filename}.",
        "Save the script and add it to the chart; do not modify governed parameters.",
        "Confirm that TradingView reports no Pine compilation error.",
        "Open Strategy Tester and record the resulting orders/trades for runtime parity review.",
        "Treat the result as research-only; this export grants no deployment "
        "or live-trading authority.",
    )


def _build_package(
    request: TradingViewResearchExportRequest,
    *,
    context: TradingViewResearchExportContext,
) -> TradingViewResearchExportPackage:
    _verify_boundary(request, context=context)
    generation = context.generation_result
    artifact = generation.artifact
    pine_context = context.generator_context.pine_intake_context
    evidence = pine_context.evidence
    eligibility = evidence.eligibility
    if eligibility.normalized_manifest_ref is None or eligibility.normalized_lock_ref is None:
        raise TradingViewResearchExportLineageMismatch(
            "export requires exact normalized dataset manifest and lock"
        )

    optimization_selection_ref = generation.intake_request.optimization_selection_ref
    pine_filename = f"{request.file_stem}.pine"
    manifest_filename = f"{request.file_stem}.manifest.json"
    timeframe_token = eligibility.timeframe_ref.object_id.value
    parameters = _strategy_parameters(context)
    steps = _manual_steps(
        symbol=evidence.instrument.symbol,
        timeframe_token=timeframe_token,
        pine_filename=pine_filename,
    )
    return TradingViewResearchExportPackage(
        request.export_id,
        _V1,
        request.export_run_id,
        request.pine_artifact_ref,
        request.strategy_ref,
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
        optimization_selection_ref,
        eligibility.instrument_ref,
        eligibility.timeframe_ref,
        eligibility.normalized_manifest_ref,
        eligibility.normalized_lock_ref,
        generation.generation_input_fingerprint,
        context.safety_result.assessment_id,
        context.safety_result.input_fingerprint,
        TradingViewResearchExportSafetyStatus.STATIC_SAFETY_PASS,
        context.safety_result.static_repaint_status.value,
        artifact.repaint_assessment,
        TradingViewResearchExportRuntimeStatus.NOT_VERIFIED_ON_TRADINGVIEW,
        artifact.source_sha256,
        artifact.source_byte_size,
        pine_filename,
        manifest_filename,
        artifact.source_text,
        evidence.instrument.symbol,
        timeframe_token,
        parameters,
        steps,
        TradingViewResearchExportReadiness.READY_FOR_MANUAL_TRADINGVIEW_RESEARCH,
        request.export_authority_ref,
        request.provenance_ref,
        DeploymentAuthorizationStatus.NOT_AUTHORIZED,
        ExecutionState.PLANNED_CLOSED,
        _V1,
    )


def render_tradingview_research_manifest(
    package: TradingViewResearchExportPackage,
) -> bytes:
    """Render a deterministic human-facing manifest for the exact stored export package."""
    payload = {
        "format": "ai-quant-lab.tradingview-research-export-v1",
        "export_id": str(package.export_id),
        "export_package_fingerprint": fingerprint_record(package),
        "pine_filename": package.pine_filename,
        "pine_source_sha256": package.pine_source_sha256,
        "strategy_ref": str(package.strategy_ref.object_id),
        "backtest_ref": str(package.backtest_ref.object_id),
        "scientific_validation_ref": str(package.scientific_validation_ref.object_id),
        "robustness_ref": str(package.robustness_ref.object_id),
        "optimization_selection_ref": (
            None
            if package.optimization_selection_ref is None
            else str(package.optimization_selection_ref.object_id)
        ),
        "instrument_ref": str(package.instrument_ref.object_id),
        "timeframe_ref": str(package.timeframe_ref.object_id),
        "normalized_manifest_ref": str(package.normalized_manifest_ref.object_id),
        "normalized_lock_ref": str(package.normalized_lock_ref.object_id),
        "instrument_symbol": package.instrument_symbol,
        "timeframe_token": package.timeframe_token,
        "strategy_parameters": [list(item) for item in package.strategy_parameters],
        "generation_input_fingerprint": package.generation_input_fingerprint,
        "safety_assessment_id": str(package.safety_assessment_id),
        "safety_input_fingerprint": package.safety_input_fingerprint,
        "safety_status": package.safety_status.value,
        "static_repaint_status": package.static_repaint_status,
        "artifact_repaint_assessment": package.artifact_repaint_assessment.value,
        "runtime_status": package.runtime_status.value,
        "manual_steps": list(package.manual_steps),
        "readiness": package.readiness.value,
        "deployment_authorization": package.deployment_authorization.value,
        "execution_state": package.execution_state.value,
    }
    return (canonical_json(payload) + "\n").encode("utf-8")


def build_tradingview_research_export(
    request: TradingViewResearchExportRequest,
    *,
    context: TradingViewResearchExportContext,
    repository: LocalDatasetRepository,
) -> TradingViewResearchExportExecution:
    """Build, immutably store and return the manual TradingView research package."""
    package = _build_package(request, context=context)
    write = repository.store(package)
    package_ref = _exact(package, package.export_id, package.version)
    pine_bytes = package.pine_source_text.encode("utf-8")
    manifest_bytes = render_tradingview_research_manifest(package)
    return TradingViewResearchExportExecution(
        package,
        package_ref,
        write,
        pine_bytes,
        manifest_bytes,
    )


def verify_tradingview_research_export(
    request: TradingViewResearchExportRequest,
    *,
    package: TradingViewResearchExportPackage,
    context: TradingViewResearchExportContext,
) -> None:
    """Deterministically reconstruct the export package and require exact equality."""
    expected = _build_package(request, context=context)
    if package != expected:
        raise TradingViewResearchExportLineageMismatch(
            "TradingView research export differs from exact deterministic reconstruction"
        )
