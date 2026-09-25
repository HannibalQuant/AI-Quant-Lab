"""Sprint 21 bounded Pine static safety and repaint-risk validation tests."""

# mypy: disable-error-code="no-untyped-def,no-untyped-call"

from __future__ import annotations

import json
from dataclasses import replace
from pathlib import Path

import pytest
from test_pine_strategy_intake import (
    AUTHORITY_REF,
    PROVENANCE_REF,
    _direct_context,
    _selected_context,
)

from ai_quant_lab.core.governed_pine_generator import (
    GovernedPineGenerationRequest,
    GovernedPineGeneratorContext,
    generate_governed_pine_strategy,
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
from ai_quant_lab.core.pine_safety_validation import (
    PineSafetyAssessmentContext,
    PineSafetyAssessmentRequest,
    PineSafetyAuthorityInvalid,
    PineSafetyDecision,
    PineSafetyLineageMismatch,
    PineSafetyReasonCode,
    PineStaticRepaintStatus,
    analyze_pine_static_safety,
    assess_governed_pine_static_safety,
    verify_pine_static_safety_assessment,
)
from ai_quant_lab.core.pine_strategy_contracts import RepaintAssessmentStatus
from ai_quant_lab.core.research_eligibility_contracts import DeploymentAuthorizationStatus

pytest_plugins = ("test_pine_strategy_intake",)

V1 = ObjectVersion(1)
GOLDEN = Path(__file__).parent / "golden" / "pine_safety_validation_v1.json"
GENERATOR_AUTHORITY = TraceabilityRef(
    AuthorityBindingId("sprint-21-generator-authority"),
    V1,
    "sha256:" + "9" * 64,
)
SAFETY_AUTHORITY = TraceabilityRef(
    AuthorityBindingId("pine-static-safety-authority"),
    V1,
    "sha256:" + "8" * 64,
)


def exact(record, object_id, version):
    return TraceabilityRef(object_id, version, fingerprint_record(record))


def build_generation(pine_context, repository, *, suffix=""):
    tail = f"-{suffix}" if suffix else ""
    strategy = pine_context.strategy
    generator_context = GovernedPineGeneratorContext(
        pine_context,
        GENERATOR_AUTHORITY,
    )
    generation_request = GovernedPineGenerationRequest(
        RunId(f"sprint-21-generation{tail}"),
        RunId(f"sprint-21-intake{tail}"),
        ArtifactId(f"sprint-21-generated-pine{tail}"),
        exact(strategy, strategy.strategy_id, strategy.version),
        "AIQL Sprint 21 Safety Candidate",
        GENERATOR_AUTHORITY,
        AUTHORITY_REF,
        PROVENANCE_REF,
    )
    generation_result = generate_governed_pine_strategy(
        generation_request,
        context=generator_context,
        repository=repository,
    )
    return generation_request, generation_result, generator_context


def build_assessment(generation_request, generation_result, generator_context, *, suffix=""):
    tail = f"-{suffix}" if suffix else ""
    artifact = generation_result.artifact
    context = PineSafetyAssessmentContext(
        generation_request,
        generation_result,
        generator_context,
        SAFETY_AUTHORITY,
    )
    request = PineSafetyAssessmentRequest(
        RunId(f"sprint-21-safety-run{tail}"),
        ArtifactId(f"sprint-21-safety-result{tail}"),
        exact(artifact, artifact.pine_artifact_id, artifact.version),
        artifact.strategy_definition_ref,
        generation_result.generation_input_fingerprint,
        SAFETY_AUTHORITY,
        PROVENANCE_REF,
    )
    return request, context


@pytest.fixture
def safety_bundle(selection_bundle):
    _old_request, pine_context, *_rest, repository = _selected_context(selection_bundle)
    generation_request, generation_result, generator_context = build_generation(
        pine_context,
        repository,
    )
    request, context = build_assessment(
        generation_request,
        generation_result,
        generator_context,
    )
    result = assess_governed_pine_static_safety(request, context=context)
    return request, context, result, repository


def test_optimized_generated_pine_passes_bounded_static_safety(safety_bundle):
    request, context, result, _repository = safety_bundle

    verify_pine_static_safety_assessment(request, result=result, context=context)

    assert result.decision is PineSafetyDecision.PASS
    assert result.static_repaint_status is PineStaticRepaintStatus.NO_STATIC_REPAINT_HAZARD_DETECTED
    assert result.reason_codes == (PineSafetyReasonCode.CANONICAL_GENERATED_PROFILE,)
    assert result.findings == ()
    assert result.source_sha256 == context.generation_result.artifact.source_sha256


def test_direct_generated_pine_passes_same_safety_boundary(selection_bundle):
    _old_request, pine_context, repository = _direct_context(selection_bundle)
    generation_request, generation_result, generator_context = build_generation(
        pine_context,
        repository,
        suffix="direct",
    )
    request, context = build_assessment(
        generation_request,
        generation_result,
        generator_context,
        suffix="direct",
    )

    result = assess_governed_pine_static_safety(request, context=context)

    assert result.decision is PineSafetyDecision.PASS
    assert result.findings == ()
    verify_pine_static_safety_assessment(request, result=result, context=context)


@pytest.mark.parametrize(
    ("snippet", "expected"),
    (
        (
            'x = request.security(syminfo.tickerid, "60", close)',
            PineSafetyReasonCode.EXTERNAL_DATA_REQUEST,
        ),
        ("x = security(syminfo.tickerid, close)", PineSafetyReasonCode.LEGACY_SECURITY_CALL),
        ("x = barmerge.lookahead_on", PineSafetyReasonCode.EXPLICIT_LOOKAHEAD),
        ("x = timeframe.period", PineSafetyReasonCode.DYNAMIC_TIMEFRAME),
        ("x = barstate.isrealtime", PineSafetyReasonCode.REALTIME_BRANCH),
        ("x = timenow", PineSafetyReasonCode.WALL_CLOCK_DEPENDENCY),
        ("varip float x = close", PineSafetyReasonCode.INTRABAR_STATE),
        ("calc_on_every_tick=true", PineSafetyReasonCode.TICK_RECALCULATION),
        ("calc_on_order_fills=true", PineSafetyReasonCode.ORDER_FILL_RECALCULATION),
        ("process_orders_on_close=true", PineSafetyReasonCode.PROCESS_ORDERS_ON_CLOSE),
        ('alert("x")', PineSafetyReasonCode.ALERT_SIDE_EFFECT),
        ("use_bar_magnifier=true", PineSafetyReasonCode.BAR_MAGNIFIER),
    ),
)
def test_static_scanner_detects_explicit_repaint_or_runtime_hazards(snippet, expected):
    source = "\n".join(
        (
            "//@version=6",
            'strategy("scan")',
            "confirmed = barstate.isconfirmed",
            snippet,
            "",
        )
    )

    findings = analyze_pine_static_safety(source)

    assert expected in tuple(item.reason_code for item in findings)


def test_static_scanner_requires_confirmed_bar_guard():
    findings = analyze_pine_static_safety('//@version=6\nstrategy("scan")\nx = close\n')

    assert tuple(item.reason_code for item in findings) == (
        PineSafetyReasonCode.MISSING_CONFIRMED_BAR_GUARD,
    )


def test_comments_and_strings_cannot_manufacture_hazards():
    source = "\n".join(
        (
            "//@version=6",
            'strategy("scan")',
            "confirmed = barstate.isconfirmed",
            "// request.security barmerge.lookahead_on varip timenow",
            'labelText = "alert( request.security timeframe.period )"',
            "/* security(syminfo.tickerid, close) */",
            "",
        )
    )

    assert analyze_pine_static_safety(source) == ()


def test_wrong_safety_authority_fails_closed(safety_bundle):
    request, context, _result, _repository = safety_bundle
    wrong = TraceabilityRef(
        AuthorityBindingId("wrong-pine-static-safety-authority"),
        V1,
        "sha256:" + "7" * 64,
    )
    request = replace(request, safety_authority_ref=wrong)

    with pytest.raises(PineSafetyAuthorityInvalid):
        assess_governed_pine_static_safety(request, context=context)


def test_pine_artifact_substitution_fails_closed(safety_bundle):
    request, context, _result, _repository = safety_bundle
    wrong = TraceabilityRef(
        request.pine_artifact_ref.object_id,
        request.pine_artifact_ref.version,
        "sha256:" + "6" * 64,
    )
    request = replace(request, pine_artifact_ref=wrong)

    with pytest.raises(PineSafetyLineageMismatch):
        assess_governed_pine_static_safety(request, context=context)


def test_strategy_substitution_fails_closed(safety_bundle):
    request, context, _result, _repository = safety_bundle
    wrong = TraceabilityRef(
        request.strategy_definition_ref.object_id,
        request.strategy_definition_ref.version,
        "sha256:" + "5" * 64,
    )
    request = replace(request, strategy_definition_ref=wrong)

    with pytest.raises(PineSafetyLineageMismatch):
        assess_governed_pine_static_safety(request, context=context)


def test_provenance_substitution_fails_closed(safety_bundle):
    request, context, _result, _repository = safety_bundle
    wrong = TraceabilityRef(
        ProvenanceId("wrong-pine-safety-provenance"),
        V1,
        "sha256:" + "2" * 64,
    )
    request = replace(request, provenance_ref=wrong)

    with pytest.raises(PineSafetyLineageMismatch):
        assess_governed_pine_static_safety(request, context=context)


def test_generation_fingerprint_substitution_fails_closed(safety_bundle):
    request, context, _result, _repository = safety_bundle
    request = replace(
        request,
        generation_input_fingerprint="sha256:" + "4" * 64,
    )

    with pytest.raises(PineSafetyLineageMismatch):
        assess_governed_pine_static_safety(request, context=context)


def test_tampered_generation_result_fails_before_safety_claim(safety_bundle):
    request, context, _result, _repository = safety_bundle
    tampered_generation = replace(
        context.generation_result,
        source_text=context.generation_result.source_text + "// modified\n",
    )
    tampered_context = replace(context, generation_result=tampered_generation)

    with pytest.raises(PineSafetyLineageMismatch):
        assess_governed_pine_static_safety(request, context=tampered_context)


def test_assessment_is_deterministic(safety_bundle):
    request, context, result, _repository = safety_bundle

    rerun = assess_governed_pine_static_safety(request, context=context)

    assert rerun == result


def test_assessment_result_tamper_fails_exact_verification(safety_bundle):
    request, context, result, _repository = safety_bundle
    tampered = replace(
        result,
        source_sha256="sha256:" + "3" * 64,
    )

    with pytest.raises(PineSafetyLineageMismatch):
        verify_pine_static_safety_assessment(
            request,
            result=tampered,
            context=context,
        )


def test_static_safety_does_not_upgrade_runtime_repaint_or_deployment_claim(safety_bundle):
    _request, context, result, _repository = safety_bundle

    assert result.decision is PineSafetyDecision.PASS
    assert (
        context.generation_result.artifact.repaint_assessment
        is RepaintAssessmentStatus.NOT_EVALUATED
    )
    assert result.deployment_authorization is DeploymentAuthorizationStatus.NOT_AUTHORIZED
    assert result.execution_state is ExecutionState.PLANNED_CLOSED


def test_safety_validator_has_no_external_execution_capability():
    source = Path("src/ai_quant_lab/core/pine_safety_validation.py").read_text(encoding="utf-8")
    forbidden = (
        "import requests",
        "import httpx",
        "import aiohttp",
        "import socket",
        "import subprocess",
        "selenium",
        "playwright",
        "strategy.entry(",
        "strategy.close(",
    )
    for token in forbidden:
        assert token not in source


def test_pine_safety_validation_golden_is_pinned(safety_bundle):
    _request, context, result, _repository = safety_bundle
    expected = {
        "format": "pine-static-safety-validation-v1",
        "assessment_id": str(result.assessment_id),
        "input_fingerprint": result.input_fingerprint,
        "pine_artifact_ref": str(result.pine_artifact_ref.object_id),
        "strategy_ref": str(result.strategy_definition_ref.object_id),
        "generation_input_fingerprint": result.generation_input_fingerprint,
        "source_sha256": result.source_sha256,
        "normalized_source_sha256": result.normalized_source_sha256,
        "decision": result.decision.value,
        "static_repaint_status": result.static_repaint_status.value,
        "reason_codes": [item.value for item in result.reason_codes],
        "finding_count": len(result.findings),
        "artifact_repaint_assessment": context.generation_result.artifact.repaint_assessment.value,
        "deployment_authorization": result.deployment_authorization.value,
        "execution_state": result.execution_state.value,
    }
    assert json.loads(GOLDEN.read_text(encoding="utf-8")) == expected
