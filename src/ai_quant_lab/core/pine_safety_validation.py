"""Bounded static Pine safety and repaint-risk validation for generated research source."""

from __future__ import annotations

import re
from dataclasses import dataclass
from enum import StrEnum
from typing import Final

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
    fingerprint,
)
from ai_quant_lab.core.research_eligibility_contracts import DeploymentAuthorizationStatus

_V1 = ObjectVersion(1)
_SHA256: Final = re.compile(r"^sha256:[0-9a-f]{64}$")


class PineSafetyValidationError(ValueError):
    pass


class PineSafetyAuthorityInvalid(PineSafetyValidationError):
    pass


class PineSafetyLineageMismatch(PineSafetyValidationError):
    pass


class PineSafetyDecision(StrEnum):
    PASS = "PASS"
    FAIL = "FAIL"


class PineStaticRepaintStatus(StrEnum):
    NO_STATIC_REPAINT_HAZARD_DETECTED = "NO_STATIC_REPAINT_HAZARD_DETECTED"
    STATIC_REPAINT_HAZARD_DETECTED = "STATIC_REPAINT_HAZARD_DETECTED"


class PineSafetyReasonCode(StrEnum):
    CANONICAL_GENERATED_PROFILE = "CANONICAL_GENERATED_PROFILE"
    MISSING_CONFIRMED_BAR_GUARD = "MISSING_CONFIRMED_BAR_GUARD"
    EXTERNAL_DATA_REQUEST = "EXTERNAL_DATA_REQUEST"
    LEGACY_SECURITY_CALL = "LEGACY_SECURITY_CALL"
    EXPLICIT_LOOKAHEAD = "EXPLICIT_LOOKAHEAD"
    DYNAMIC_TIMEFRAME = "DYNAMIC_TIMEFRAME"
    REALTIME_BRANCH = "REALTIME_BRANCH"
    WALL_CLOCK_DEPENDENCY = "WALL_CLOCK_DEPENDENCY"
    INTRABAR_STATE = "INTRABAR_STATE"
    TICK_RECALCULATION = "TICK_RECALCULATION"
    ORDER_FILL_RECALCULATION = "ORDER_FILL_RECALCULATION"
    PROCESS_ORDERS_ON_CLOSE = "PROCESS_ORDERS_ON_CLOSE"
    ALERT_SIDE_EFFECT = "ALERT_SIDE_EFFECT"
    BAR_MAGNIFIER = "BAR_MAGNIFIER"


@dataclass(frozen=True, slots=True)
class PineStaticSafetyFinding:
    reason_code: PineSafetyReasonCode
    line: int
    evidence: str

    def __post_init__(self) -> None:
        if (
            not isinstance(self.reason_code, PineSafetyReasonCode)
            or isinstance(self.line, bool)
            or not isinstance(self.line, int)
            or self.line <= 0
            or not isinstance(self.evidence, str)
            or not self.evidence
        ):
            raise PineSafetyValidationError("invalid Pine static safety finding")


@dataclass(frozen=True, slots=True)
class PineSafetyAssessmentRequest:
    assessment_run_id: RunId
    assessment_id: ArtifactId
    pine_artifact_ref: TraceabilityRef
    strategy_definition_ref: TraceabilityRef
    generation_input_fingerprint: str
    safety_authority_ref: TraceabilityRef
    provenance_ref: TraceabilityRef
    contract_version: ObjectVersion = _V1

    def __post_init__(self) -> None:
        if (
            not isinstance(self.assessment_run_id, RunId)
            or not isinstance(self.assessment_id, ArtifactId)
            or self.contract_version != _V1
            or not isinstance(self.generation_input_fingerprint, str)
            or _SHA256.fullmatch(self.generation_input_fingerprint) is None
        ):
            raise PineSafetyValidationError("invalid Pine safety assessment request")
        _exact_ref(self.pine_artifact_ref, ArtifactId, "pine_artifact_ref")
        _exact_ref(self.strategy_definition_ref, ArtifactId, "strategy_definition_ref")
        _exact_ref(self.safety_authority_ref, AuthorityBindingId, "safety_authority_ref")
        _exact_ref(self.provenance_ref, ProvenanceId, "provenance_ref")


@dataclass(frozen=True, slots=True)
class PineSafetyAssessmentContext:
    generation_request: GovernedPineGenerationRequest
    generation_result: GovernedPineGenerationResult
    generator_context: GovernedPineGeneratorContext
    safety_authority_ref: TraceabilityRef

    def __post_init__(self) -> None:
        _exact_ref(self.safety_authority_ref, AuthorityBindingId, "safety_authority_ref")


@dataclass(frozen=True, slots=True)
class PineSafetyAssessmentResult:
    assessment_id: ArtifactId
    version: ObjectVersion
    assessment_run_id: RunId
    input_fingerprint: str
    pine_artifact_ref: TraceabilityRef
    strategy_definition_ref: TraceabilityRef
    generation_input_fingerprint: str
    source_sha256: str
    normalized_source_sha256: str
    decision: PineSafetyDecision
    static_repaint_status: PineStaticRepaintStatus
    reason_codes: tuple[PineSafetyReasonCode, ...]
    findings: tuple[PineStaticSafetyFinding, ...]
    safety_authority_ref: TraceabilityRef
    provenance_ref: TraceabilityRef
    deployment_authorization: DeploymentAuthorizationStatus
    execution_state: ExecutionState
    contract_version: ObjectVersion

    def __post_init__(self) -> None:
        if (
            not isinstance(self.assessment_id, ArtifactId)
            or self.version != _V1
            or not isinstance(self.assessment_run_id, RunId)
            or _SHA256.fullmatch(self.input_fingerprint) is None
            or _SHA256.fullmatch(self.generation_input_fingerprint) is None
            or _SHA256.fullmatch(self.source_sha256) is None
            or _SHA256.fullmatch(self.normalized_source_sha256) is None
            or not self.reason_codes
            or len(set(self.reason_codes)) != len(self.reason_codes)
            or self.contract_version != _V1
            or self.deployment_authorization is not DeploymentAuthorizationStatus.NOT_AUTHORIZED
            or self.execution_state is not ExecutionState.PLANNED_CLOSED
        ):
            raise PineSafetyValidationError("invalid Pine safety assessment result")
        _exact_ref(self.pine_artifact_ref, ArtifactId, "pine_artifact_ref")
        _exact_ref(self.strategy_definition_ref, ArtifactId, "strategy_definition_ref")
        _exact_ref(self.safety_authority_ref, AuthorityBindingId, "safety_authority_ref")
        _exact_ref(self.provenance_ref, ProvenanceId, "provenance_ref")
        if self.decision is PineSafetyDecision.PASS:
            if (
                self.static_repaint_status
                is not PineStaticRepaintStatus.NO_STATIC_REPAINT_HAZARD_DETECTED
                or self.findings
                or self.reason_codes != (PineSafetyReasonCode.CANONICAL_GENERATED_PROFILE,)
            ):
                raise PineSafetyValidationError("passing Pine safety result is inconsistent")
        else:
            expected = tuple(dict.fromkeys(item.reason_code for item in self.findings))
            if (
                self.static_repaint_status
                is not PineStaticRepaintStatus.STATIC_REPAINT_HAZARD_DETECTED
                or not self.findings
                or self.reason_codes != expected
            ):
                raise PineSafetyValidationError("failing Pine safety result is inconsistent")


def _exact_ref(ref: TraceabilityRef, expected_type: type[object], field: str) -> None:
    if (
        not isinstance(ref, TraceabilityRef)
        or ref.expected_fingerprint is None
        or not isinstance(ref.object_id, expected_type)
    ):
        raise PineSafetyValidationError(
            f"{field} must be an exact fingerprint-bearing {expected_type.__name__} reference"
        )


def _exact(record: object, object_id: object, version: ObjectVersion) -> TraceabilityRef:
    return TraceabilityRef(object_id, version, fingerprint_record(record))  # type: ignore[arg-type]


def _mask_non_code(source: str) -> str:
    chars = list(source)
    index = 0
    quote: str | None = None
    block_comment = False
    while index < len(chars):
        current = chars[index]
        following = chars[index + 1] if index + 1 < len(chars) else ""
        if block_comment:
            if current == "*" and following == "/":
                chars[index] = chars[index + 1] = " "
                index += 2
                block_comment = False
            else:
                if current != "\n":
                    chars[index] = " "
                index += 1
            continue
        if quote is not None:
            if current == "\\" and following:
                chars[index] = chars[index + 1] = " "
                index += 2
            else:
                if current == quote:
                    quote = None
                if current != "\n":
                    chars[index] = " "
                index += 1
            continue
        if current == "/" and following == "*":
            chars[index] = chars[index + 1] = " "
            block_comment = True
            index += 2
        elif current == "/" and following == "/":
            while index < len(chars) and chars[index] != "\n":
                chars[index] = " "
                index += 1
        elif current in ('"', "'"):
            quote = current
            chars[index] = " "
            index += 1
        else:
            index += 1
    return "".join(chars)


_HAZARDS: Final[tuple[tuple[PineSafetyReasonCode, re.Pattern[str]], ...]] = (
    (PineSafetyReasonCode.EXTERNAL_DATA_REQUEST, re.compile(r"\brequest\.")),
    (PineSafetyReasonCode.LEGACY_SECURITY_CALL, re.compile(r"\bsecurity\s*\(")),
    (PineSafetyReasonCode.EXPLICIT_LOOKAHEAD, re.compile(r"\bbarmerge\.lookahead_on\b")),
    (
        PineSafetyReasonCode.DYNAMIC_TIMEFRAME,
        re.compile(r"\b(?:input\.timeframe|timeframe\.[A-Za-z_][A-Za-z0-9_]*)\b"),
    ),
    (PineSafetyReasonCode.REALTIME_BRANCH, re.compile(r"\bbarstate\.isrealtime\b")),
    (PineSafetyReasonCode.WALL_CLOCK_DEPENDENCY, re.compile(r"\btimenow\b")),
    (PineSafetyReasonCode.INTRABAR_STATE, re.compile(r"\bvarip\b")),
    (
        PineSafetyReasonCode.TICK_RECALCULATION,
        re.compile(r"\bcalc_on_every_tick\s*=\s*true\b"),
    ),
    (
        PineSafetyReasonCode.ORDER_FILL_RECALCULATION,
        re.compile(r"\bcalc_on_order_fills\s*=\s*true\b"),
    ),
    (
        PineSafetyReasonCode.PROCESS_ORDERS_ON_CLOSE,
        re.compile(r"\bprocess_orders_on_close\s*=\s*true\b"),
    ),
    (
        PineSafetyReasonCode.ALERT_SIDE_EFFECT,
        re.compile(r"\balert(?:condition)?\s*\("),
    ),
    (
        PineSafetyReasonCode.BAR_MAGNIFIER,
        re.compile(r"\buse_bar_magnifier\s*=\s*true\b"),
    ),
)


def analyze_pine_static_safety(source: str) -> tuple[PineStaticSafetyFinding, ...]:
    """Return deterministic static hazard findings without claiming runtime proof."""
    if not isinstance(source, str) or not source:
        raise PineSafetyValidationError("Pine safety analysis requires non-empty source")
    masked = _mask_non_code(source)
    findings: list[PineStaticSafetyFinding] = []
    for reason, pattern in _HAZARDS:
        for match in pattern.finditer(masked):
            line = masked.count("\n", 0, match.start()) + 1
            evidence = source[match.start() : match.end()].strip()
            findings.append(PineStaticSafetyFinding(reason, line, evidence))
    if re.search(r"\bbarstate\.isconfirmed\b", masked) is None:
        findings.append(
            PineStaticSafetyFinding(
                PineSafetyReasonCode.MISSING_CONFIRMED_BAR_GUARD,
                1,
                "barstate.isconfirmed absent",
            )
        )
    findings.sort(key=lambda item: (item.line, item.reason_code.value, item.evidence))
    return tuple(findings)


def _verify_boundary(
    request: PineSafetyAssessmentRequest,
    *,
    context: PineSafetyAssessmentContext,
) -> None:
    if request.safety_authority_ref != context.safety_authority_ref:
        raise PineSafetyAuthorityInvalid(
            "Pine safety request lacks exact governed safety authority"
        )
    try:
        verify_governed_pine_generation(
            context.generation_request,
            result=context.generation_result,
            context=context.generator_context,
        )
    except ValueError as exc:
        raise PineSafetyLineageMismatch(
            "Pine safety assessment requires an exact verified generator result"
        ) from exc
    generation = context.generation_result
    artifact = generation.artifact
    expected_artifact_ref = _exact(artifact, artifact.pine_artifact_id, artifact.version)
    if (
        request.pine_artifact_ref != expected_artifact_ref
        or request.strategy_definition_ref != artifact.strategy_definition_ref
        or request.generation_input_fingerprint != generation.generation_input_fingerprint
        or request.provenance_ref != artifact.provenance_ref
    ):
        raise PineSafetyLineageMismatch(
            "Pine safety request does not bind exact generated source lineage"
        )


def _input_fingerprint(
    request: PineSafetyAssessmentRequest,
    *,
    context: PineSafetyAssessmentContext,
) -> str:
    artifact = context.generation_result.artifact
    return fingerprint(
        {
            "assessment_run_id": str(request.assessment_run_id),
            "assessment_id": str(request.assessment_id),
            "pine_artifact_fingerprint": fingerprint_record(artifact),
            "strategy_definition_ref": request.strategy_definition_ref,
            "generation_input_fingerprint": request.generation_input_fingerprint,
            "safety_authority_ref": request.safety_authority_ref,
            "provenance_ref": request.provenance_ref,
        }
    )


def _build_result(
    request: PineSafetyAssessmentRequest,
    *,
    context: PineSafetyAssessmentContext,
) -> PineSafetyAssessmentResult:
    _verify_boundary(request, context=context)
    artifact = context.generation_result.artifact
    findings = analyze_pine_static_safety(artifact.source_text)
    if findings:
        decision = PineSafetyDecision.FAIL
        repaint = PineStaticRepaintStatus.STATIC_REPAINT_HAZARD_DETECTED
        reason_codes = tuple(dict.fromkeys(item.reason_code for item in findings))
    else:
        decision = PineSafetyDecision.PASS
        repaint = PineStaticRepaintStatus.NO_STATIC_REPAINT_HAZARD_DETECTED
        reason_codes = (PineSafetyReasonCode.CANONICAL_GENERATED_PROFILE,)
    return PineSafetyAssessmentResult(
        request.assessment_id,
        _V1,
        request.assessment_run_id,
        _input_fingerprint(request, context=context),
        request.pine_artifact_ref,
        request.strategy_definition_ref,
        request.generation_input_fingerprint,
        artifact.source_sha256,
        artifact.normalized_source_sha256,
        decision,
        repaint,
        reason_codes,
        findings,
        request.safety_authority_ref,
        request.provenance_ref,
        DeploymentAuthorizationStatus.NOT_AUTHORIZED,
        ExecutionState.PLANNED_CLOSED,
        _V1,
    )


def assess_governed_pine_static_safety(
    request: PineSafetyAssessmentRequest,
    *,
    context: PineSafetyAssessmentContext,
) -> PineSafetyAssessmentResult:
    """Assess the exact generated Pine artifact under the bounded static safety profile."""
    return _build_result(request, context=context)


def verify_pine_static_safety_assessment(
    request: PineSafetyAssessmentRequest,
    *,
    result: PineSafetyAssessmentResult,
    context: PineSafetyAssessmentContext,
) -> None:
    """Reconstruct the complete assessment and require exact deterministic equality."""
    expected = _build_result(request, context=context)
    if result != expected:
        raise PineSafetyLineageMismatch(
            "Pine static safety assessment differs from exact deterministic reconstruction"
        )
