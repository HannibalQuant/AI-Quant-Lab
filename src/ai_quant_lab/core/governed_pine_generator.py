"""Deterministic governed Pine v6 generation for the bounded AI Quant Lab strategy profile."""

from __future__ import annotations

from dataclasses import dataclass

from ai_quant_lab.core.dataset_store import LocalDatasetRepository, RepositoryWriteResult
from ai_quant_lab.core.integrity import fingerprint_record
from ai_quant_lab.core.model import (
    ArtifactId,
    AuthorityBindingId,
    ExecutionState,
    ObjectVersion,
    ProvenanceId,
    RunId,
    TraceabilityRef,
    fingerprint,
)
from ai_quant_lab.core.pine_strategy_contracts import (
    PineStrategyIntakeRecord,
    PineStrategyIntakeRequest,
    PineStrategySourceArtifact,
)
from ai_quant_lab.core.pine_strategy_intake import (
    PineStrategyIntakeContext,
    intake_pine_strategy,
    verify_pine_strategy_intake_lineage,
)
from ai_quant_lab.core.research_eligibility_contracts import DeploymentAuthorizationStatus
from ai_quant_lab.core.strategy_backtest_contracts import (
    SidePermission,
    SignalTiming,
    SimulatedExecutionTiming,
    StrategyDefinition,
    StrategyModel,
)

_V1 = ObjectVersion(1)
_GENERATOR_PROFILE = "AIQL_GOVERNED_PINE_V6_CLOSE_VS_OPEN_LONG_ONLY_V1"


def _valid_title(value: object) -> bool:
    return (
        isinstance(value, str)
        and 1 <= len(value) <= 96
        and '"' not in value
        and "\\" not in value
        and "\r" not in value
        and "\n" not in value
    )


class GovernedPineGeneratorError(ValueError):
    pass


class GovernedPineGeneratorAuthorityInvalid(GovernedPineGeneratorError):
    pass


class GovernedPineGeneratorLineageMismatch(GovernedPineGeneratorError):
    pass


class GovernedPineGeneratorUnsupported(GovernedPineGeneratorError):
    pass


@dataclass(frozen=True, slots=True)
class GovernedPineGenerationRequest:
    generation_run_id: RunId
    intake_run_id: RunId
    requested_artifact_id: ArtifactId
    strategy_definition_ref: TraceabilityRef
    script_title: str
    generator_authority_ref: TraceabilityRef
    pine_intake_authority_ref: TraceabilityRef
    provenance_ref: TraceabilityRef
    contract_version: ObjectVersion = _V1

    def __post_init__(self) -> None:
        if (
            not isinstance(self.generation_run_id, RunId)
            or not isinstance(self.intake_run_id, RunId)
            or not isinstance(self.requested_artifact_id, ArtifactId)
            or self.contract_version != _V1
            or not _valid_title(self.script_title)
        ):
            raise GovernedPineGeneratorError("invalid governed Pine generation request")
        _exact_ref(self.strategy_definition_ref, ArtifactId, "strategy_definition_ref")
        _exact_ref(
            self.generator_authority_ref,
            AuthorityBindingId,
            "generator_authority_ref",
        )
        _exact_ref(
            self.pine_intake_authority_ref,
            AuthorityBindingId,
            "pine_intake_authority_ref",
        )
        _exact_ref(self.provenance_ref, ProvenanceId, "provenance_ref")


@dataclass(frozen=True, slots=True)
class GovernedPineGeneratorContext:
    pine_intake_context: PineStrategyIntakeContext
    generator_authority_ref: TraceabilityRef

    def __post_init__(self) -> None:
        _exact_ref(
            self.generator_authority_ref,
            AuthorityBindingId,
            "generator_authority_ref",
        )


@dataclass(frozen=True, slots=True)
class GovernedPineGenerationResult:
    generation_run_id: RunId
    generator_profile: str
    generation_input_fingerprint: str
    source_text: str
    source_sha256: str
    intake_request: PineStrategyIntakeRequest
    artifact: PineStrategySourceArtifact
    intake_record: PineStrategyIntakeRecord
    writes: tuple[RepositoryWriteResult, ...]
    deployment_authorization: DeploymentAuthorizationStatus
    execution_state: ExecutionState


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
        raise GovernedPineGeneratorError(
            f"{field} must be an exact fingerprint-bearing {expected_type.__name__} reference"
        )


def _exact(record: object, object_id: object, version: ObjectVersion) -> TraceabilityRef:
    return TraceabilityRef(object_id, version, fingerprint_record(record))  # type: ignore[arg-type]


def _validate_strategy(strategy: StrategyDefinition) -> None:
    if (
        strategy.model is not StrategyModel.CLOSE_VS_OPEN_LONG_ONLY
        or strategy.signal_timing is not SignalTiming.BAR_CLOSE_AFTER_AVAILABILITY
        or strategy.execution_timing is not SimulatedExecutionTiming.FIRST_ELIGIBLE_NEXT_BAR_OPEN
        or strategy.side_permission is not SidePermission.LONG_ONLY
        or strategy.allow_pyramiding
        or strategy.force_close_at_window_end
    ):
        raise GovernedPineGeneratorUnsupported(
            "generator supports only the governed close-vs-open long-only next-bar-open profile"
        )


def _cash_literal(strategy: StrategyDefinition) -> str:
    scale = strategy.capital_minor_unit_scale
    amount = strategy.fixed_notional_minor
    whole, remainder = divmod(amount, scale)
    if remainder == 0:
        return str(whole)
    width = len(str(scale)) - 1 if scale > 1 else 0
    if 10**width != scale:
        raise GovernedPineGeneratorUnsupported(
            "capital minor-unit scale must be a power of ten for canonical Pine cash literal"
        )
    fraction = f"{remainder:0{width}d}".rstrip("0")
    return f"{whole}.{fraction}"


def render_governed_pine_v6(
    strategy: StrategyDefinition,
    *,
    script_title: str,
) -> str:
    """Render canonical Pine source for the exact bounded StrategyDefinition."""
    if not _valid_title(script_title):
        raise GovernedPineGeneratorError(
            "script title must be 1..96 characters without quotes, backslashes or newlines"
        )
    _validate_strategy(strategy)
    cash = _cash_literal(strategy)
    strategy_ref = _exact(strategy, strategy.strategy_id, strategy.version)
    lines = (
        "//@version=6",
        "// AI Quant Lab governed Pine generator v1",
        f"// Generator profile: {_GENERATOR_PROFILE}",
        f"// Strategy: {strategy_ref.object_id}",
        f"// Strategy fingerprint: {strategy_ref.expected_fingerprint}",
        "strategy(",
        f'    "{script_title}",',
        "    pyramiding=0,",
        "    process_orders_on_close=false,",
        "    calc_on_every_tick=false,",
        "    default_qty_type=strategy.cash,",
        f"    default_qty_value={cash}",
        ")",
        "",
        f"thresholdBps = {strategy.threshold_bps}.0",
        "threshold = thresholdBps / 10000.0",
        "confirmedBar = barstate.isconfirmed",
        "desiredLong = confirmedBar and open > 0 and close > 0 and (close / open - 1.0) > threshold",
        "",
        "if desiredLong and strategy.position_size <= 0",
        '    strategy.entry("AIQL-L", strategy.long)',
        "else if confirmedBar and not desiredLong and strategy.position_size > 0",
        '    strategy.close("AIQL-L")',
        "",
    )
    return "\n".join(lines)


def _optimization_refs(
    context: PineStrategyIntakeContext,
) -> tuple[TraceabilityRef | None, TraceabilityRef | None, TraceabilityRef | None]:
    optimization = context.optimization
    if optimization is None:
        return None, None, None
    selected_ref = optimization.result.selected_candidate_ref
    if selected_ref is None:
        raise GovernedPineGeneratorLineageMismatch(
            "optimized generation requires an exact selected candidate"
        )
    candidate_result = next(
        (
            item
            for item in optimization.candidate_results
            if _exact(item, item.candidate_id, item.version) == selected_ref
        ),
        None,
    )
    if candidate_result is None:
        raise GovernedPineGeneratorLineageMismatch(
            "selected candidate result is absent from optimization evidence"
        )
    definition_ref = candidate_result.candidate_definition_ref
    selection_ref = _exact(
        optimization.result,
        optimization.result.selection_result_id,
        optimization.result.version,
    )
    return definition_ref, selected_ref, selection_ref


def _generation_input_fingerprint(
    request: GovernedPineGenerationRequest,
    *,
    strategy: StrategyDefinition,
    source_text: str,
) -> str:
    return fingerprint(
        {
            "generator_profile": _GENERATOR_PROFILE,
            "generation_run_id": str(request.generation_run_id),
            "intake_run_id": str(request.intake_run_id),
            "requested_artifact_id": str(request.requested_artifact_id),
            "strategy_fingerprint": fingerprint_record(strategy),
            "script_title": request.script_title,
            "generator_authority_ref": request.generator_authority_ref,
            "pine_intake_authority_ref": request.pine_intake_authority_ref,
            "provenance_ref": request.provenance_ref,
            "source_text": source_text,
        }
    )


def _build_intake_request(
    request: GovernedPineGenerationRequest,
    *,
    context: GovernedPineGeneratorContext,
    source_text: str,
) -> PineStrategyIntakeRequest:
    pine_context = context.pine_intake_context
    strategy = pine_context.strategy
    candidate_definition_ref, candidate_result_ref, selection_ref = _optimization_refs(pine_context)
    evidence = pine_context.evidence
    return PineStrategyIntakeRequest(
        request.intake_run_id,
        request.requested_artifact_id,
        source_text.encode("utf-8"),
        _exact(strategy, strategy.strategy_id, strategy.version),
        candidate_definition_ref,
        candidate_result_ref,
        selection_ref,
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
        request.pine_intake_authority_ref,
        request.provenance_ref,
    )


def _verify_generation_boundary(
    request: GovernedPineGenerationRequest,
    *,
    context: GovernedPineGeneratorContext,
) -> StrategyDefinition:
    pine_context = context.pine_intake_context
    strategy = pine_context.strategy
    strategy_ref = _exact(strategy, strategy.strategy_id, strategy.version)
    if request.generator_authority_ref != context.generator_authority_ref:
        raise GovernedPineGeneratorAuthorityInvalid(
            "generation request lacks exact governed generator authority"
        )
    if request.pine_intake_authority_ref != pine_context.pine_intake_authority_ref:
        raise GovernedPineGeneratorAuthorityInvalid(
            "generator cannot substitute or mint Pine intake authority"
        )
    if request.strategy_definition_ref != strategy_ref:
        raise GovernedPineGeneratorLineageMismatch(
            "generation request does not bind the exact StrategyDefinition"
        )
    _validate_strategy(strategy)
    return strategy


def generate_governed_pine_strategy(
    request: GovernedPineGenerationRequest,
    *,
    context: GovernedPineGeneratorContext,
    repository: LocalDatasetRepository,
) -> GovernedPineGenerationResult:
    """Generate canonical Pine and immediately submit it to the existing governed intake."""
    strategy = _verify_generation_boundary(request, context=context)
    source_text = render_governed_pine_v6(strategy, script_title=request.script_title)
    intake_request = _build_intake_request(request, context=context, source_text=source_text)
    intake = intake_pine_strategy(
        intake_request,
        context=context.pine_intake_context,
        repository=repository,
    )
    verify_pine_strategy_intake_lineage(
        artifact=intake.artifact,
        record=intake.record,
        request=intake_request,
        context=context.pine_intake_context,
    )
    input_fp = _generation_input_fingerprint(
        request,
        strategy=strategy,
        source_text=source_text,
    )
    return GovernedPineGenerationResult(
        request.generation_run_id,
        _GENERATOR_PROFILE,
        input_fp,
        source_text,
        intake.artifact.source_sha256,
        intake_request,
        intake.artifact,
        intake.record,
        tuple(intake.writes),
        DeploymentAuthorizationStatus.NOT_AUTHORIZED,
        ExecutionState.PLANNED_CLOSED,
    )


def verify_governed_pine_generation(
    request: GovernedPineGenerationRequest,
    *,
    result: GovernedPineGenerationResult,
    context: GovernedPineGeneratorContext,
) -> None:
    """Deterministically rebuild generation and verify exact persisted intake lineage."""
    strategy = _verify_generation_boundary(request, context=context)
    expected_source = render_governed_pine_v6(strategy, script_title=request.script_title)
    expected_request = _build_intake_request(
        request,
        context=context,
        source_text=expected_source,
    )
    expected_fp = _generation_input_fingerprint(
        request,
        strategy=strategy,
        source_text=expected_source,
    )
    if (
        result.generation_run_id != request.generation_run_id
        or result.generator_profile != _GENERATOR_PROFILE
        or result.generation_input_fingerprint != expected_fp
        or result.source_text != expected_source
        or result.source_sha256 != result.artifact.source_sha256
        or result.intake_request != expected_request
        or result.deployment_authorization is not DeploymentAuthorizationStatus.NOT_AUTHORIZED
        or result.execution_state is not ExecutionState.PLANNED_CLOSED
    ):
        raise GovernedPineGeneratorLineageMismatch(
            "governed Pine generation result does not match exact deterministic reconstruction"
        )
    if result.artifact.source_text != expected_source:
        raise GovernedPineGeneratorLineageMismatch(
            "generated Pine artifact source differs from canonical generator output"
        )
    try:
        verify_pine_strategy_intake_lineage(
            artifact=result.artifact,
            record=result.intake_record,
            request=result.intake_request,
            context=context.pine_intake_context,
        )
    except ValueError as exc:
        raise GovernedPineGeneratorLineageMismatch(
            "generated Pine intake lineage failed exact verification"
        ) from exc
