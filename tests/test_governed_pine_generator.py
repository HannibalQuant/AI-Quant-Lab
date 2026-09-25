"""Sprint 20 governed Pine generator tests."""

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
    GovernedPineGeneratorAuthorityInvalid,
    GovernedPineGeneratorContext,
    GovernedPineGeneratorLineageMismatch,
    generate_governed_pine_strategy,
    render_governed_pine_v6,
    verify_governed_pine_generation,
)
from ai_quant_lab.core.integrity import fingerprint_record
from ai_quant_lab.core.model import (
    ArtifactId,
    AuthorityBindingId,
    ExecutionState,
    ObjectVersion,
    RunId,
    TraceabilityRef,
)
from ai_quant_lab.core.pine_strategy_contracts import (
    PineSemanticParityStatus,
    RepaintAssessmentStatus,
)
from ai_quant_lab.core.research_eligibility_contracts import DeploymentAuthorizationStatus

pytest_plugins = ("test_pine_strategy_intake",)

V1 = ObjectVersion(1)
GOLDEN = Path(__file__).parent / "golden" / "governed_pine_generator_v1.json"
GENERATOR_AUTHORITY = TraceabilityRef(
    AuthorityBindingId("governed-pine-generator-authority"),
    V1,
    "sha256:" + "9" * 64,
)


def exact(record, object_id, version):
    return TraceabilityRef(object_id, version, fingerprint_record(record))


def generation_request(
    pine_context,
    *,
    suffix: str = "",
    title: str = "AIQL Governed Strategy",
    generator_authority: TraceabilityRef = GENERATOR_AUTHORITY,
    intake_authority: TraceabilityRef = AUTHORITY_REF,
):
    tail = f"-{suffix}" if suffix else ""
    strategy = pine_context.strategy
    return GovernedPineGenerationRequest(
        RunId(f"governed-pine-generation{tail}"),
        RunId(f"governed-pine-generated-intake{tail}"),
        ArtifactId(f"governed-pine-generated-source{tail}"),
        exact(strategy, strategy.strategy_id, strategy.version),
        title,
        generator_authority,
        intake_authority,
        PROVENANCE_REF,
    )


@pytest.fixture
def generator_bundle(selection_bundle):
    _old_request, pine_context, *_rest, repository = _selected_context(selection_bundle)
    context = GovernedPineGeneratorContext(pine_context, GENERATOR_AUTHORITY)
    request = generation_request(pine_context)
    result = generate_governed_pine_strategy(
        request,
        context=context,
        repository=repository,
    )
    return request, context, result, repository


def test_optimized_selected_strategy_generates_accepted_pine(generator_bundle):
    request, context, result, _repository = generator_bundle

    verify_governed_pine_generation(request, result=result, context=context)

    assert result.artifact.source_text == result.source_text
    assert result.artifact.strategy_definition_ref == request.strategy_definition_ref
    assert result.intake_request.optimization_candidate_definition_ref is not None
    assert result.intake_request.optimization_candidate_result_ref is not None
    assert result.intake_request.optimization_selection_ref is not None
    assert result.artifact.semantic_parity is PineSemanticParityStatus.NOT_EVALUATED
    assert result.artifact.repaint_assessment is RepaintAssessmentStatus.NOT_EVALUATED
    assert result.deployment_authorization is DeploymentAuthorizationStatus.NOT_AUTHORIZED
    assert result.execution_state is ExecutionState.PLANNED_CLOSED


def test_direct_strategy_generation_omits_optimization_binding(selection_bundle):
    _old_request, pine_context, repository = _direct_context(selection_bundle)
    context = GovernedPineGeneratorContext(pine_context, GENERATOR_AUTHORITY)
    request = generation_request(pine_context, suffix="direct", title="AIQL Direct Strategy")

    result = generate_governed_pine_strategy(
        request,
        context=context,
        repository=repository,
    )
    verify_governed_pine_generation(request, result=result, context=context)

    assert result.intake_request.optimization_candidate_definition_ref is None
    assert result.intake_request.optimization_candidate_result_ref is None
    assert result.intake_request.optimization_selection_ref is None


def test_generated_source_matches_bounded_python_strategy_semantics(generator_bundle):
    _request, context, result, _repository = generator_bundle
    strategy = context.pine_intake_context.strategy
    source = result.source_text

    assert source.startswith("//@version=6\n")
    assert "pyramiding=0" in source
    assert "process_orders_on_close=false" in source
    assert "calc_on_every_tick=false" in source
    assert "default_qty_type=strategy.cash" in source
    assert f"thresholdBps = {strategy.threshold_bps}.0" in source
    assert "threshold = thresholdBps / 10000.0" in source
    assert "confirmedBar = barstate.isconfirmed" in source
    assert "(close / open - 1.0) > threshold" in source
    assert 'strategy.entry("AIQL-L", strategy.long)' in source
    assert 'strategy.close("AIQL-L")' in source
    assert "request." not in source
    assert "security(" not in source
    assert "alert(" not in source


def test_render_is_byte_deterministic_and_strategy_sensitive(generator_bundle):
    request, context, result, _repository = generator_bundle
    strategy = context.pine_intake_context.strategy

    first = render_governed_pine_v6(strategy, script_title=request.script_title)
    second = render_governed_pine_v6(strategy, script_title=request.script_title)

    assert first == second == result.source_text
    changed = replace(strategy, threshold_bps=strategy.threshold_bps + 1)
    changed_source = render_governed_pine_v6(changed, script_title=request.script_title)
    assert changed_source != first
    assert f"thresholdBps = {changed.threshold_bps}.0" in changed_source


@pytest.mark.parametrize(
    "title",
    (
        "",
        'bad"title',
        "bad\\title",
        "bad\ntitle",
        "x" * 97,
    ),
)
def test_script_title_cannot_escape_canonical_template(generator_bundle, title):
    _request, context, _result, _repository = generator_bundle
    with pytest.raises(ValueError):
        render_governed_pine_v6(
            context.pine_intake_context.strategy,
            script_title=title,
        )


def test_wrong_generator_authority_fails_closed(selection_bundle):
    _old_request, pine_context, *_rest, repository = _selected_context(selection_bundle)
    context = GovernedPineGeneratorContext(pine_context, GENERATOR_AUTHORITY)
    wrong = TraceabilityRef(
        AuthorityBindingId("wrong-governed-pine-generator-authority"),
        V1,
        "sha256:" + "8" * 64,
    )
    request = generation_request(pine_context, generator_authority=wrong)

    with pytest.raises(GovernedPineGeneratorAuthorityInvalid):
        generate_governed_pine_strategy(
            request,
            context=context,
            repository=repository,
        )


def test_generator_cannot_mint_or_substitute_intake_authority(selection_bundle):
    _old_request, pine_context, *_rest, repository = _selected_context(selection_bundle)
    context = GovernedPineGeneratorContext(pine_context, GENERATOR_AUTHORITY)
    wrong = TraceabilityRef(
        AuthorityBindingId("wrong-pine-intake-authority"),
        V1,
        "sha256:" + "7" * 64,
    )
    request = generation_request(pine_context, intake_authority=wrong)

    with pytest.raises(GovernedPineGeneratorAuthorityInvalid):
        generate_governed_pine_strategy(
            request,
            context=context,
            repository=repository,
        )


def test_strategy_substitution_fails_closed(selection_bundle):
    _old_request, pine_context, *_rest, repository = _selected_context(selection_bundle)
    context = GovernedPineGeneratorContext(pine_context, GENERATOR_AUTHORITY)
    request = generation_request(pine_context)
    wrong = TraceabilityRef(
        request.strategy_definition_ref.object_id,
        request.strategy_definition_ref.version,
        "sha256:" + "6" * 64,
    )
    request = replace(request, strategy_definition_ref=wrong)

    with pytest.raises(GovernedPineGeneratorLineageMismatch):
        generate_governed_pine_strategy(
            request,
            context=context,
            repository=repository,
        )


def test_generation_result_tamper_fails_exact_verification(generator_bundle):
    request, context, result, _repository = generator_bundle
    tampered = replace(result, source_text=result.source_text + "// tampered\n")

    with pytest.raises(GovernedPineGeneratorLineageMismatch):
        verify_governed_pine_generation(
            request,
            result=tampered,
            context=context,
        )


def test_generated_artifact_remains_research_only(generator_bundle):
    _request, _context, result, _repository = generator_bundle
    records = (result.artifact, result.intake_record)
    for record in records:
        assert record.deployment_authorization is DeploymentAuthorizationStatus.NOT_AUTHORIZED
        assert record.execution_state is ExecutionState.PLANNED_CLOSED
    assert result.artifact.semantic_parity is PineSemanticParityStatus.NOT_EVALUATED
    assert result.artifact.repaint_assessment is RepaintAssessmentStatus.NOT_EVALUATED


def test_generator_source_has_no_external_execution_capability():
    source = Path("src/ai_quant_lab/core/governed_pine_generator.py").read_text(encoding="utf-8")
    forbidden = (
        "import requests",
        "import httpx",
        "import aiohttp",
        "import socket",
        "import subprocess",
        "selenium",
        "playwright",
        "webhook",
    )
    for token in forbidden:
        assert token not in source


def test_governed_pine_generator_golden_is_pinned(generator_bundle):
    _request, context, result, _repository = generator_bundle
    strategy = context.pine_intake_context.strategy
    expected = {
        "format": "governed-pine-generator-v1",
        "generator_profile": result.generator_profile,
        "strategy_ref": str(result.artifact.strategy_definition_ref.object_id),
        "threshold_bps": strategy.threshold_bps,
        "source_sha256": result.artifact.source_sha256,
        "normalized_source_sha256": result.artifact.normalized_source_sha256,
        "source_byte_size": result.artifact.source_byte_size,
        "generation_input_fingerprint": result.generation_input_fingerprint,
        "artifact_fingerprint": fingerprint_record(result.artifact),
        "intake_record_fingerprint": fingerprint_record(result.intake_record),
        "optimization_selection_ref": str(result.artifact.optimization_selection_ref.object_id),
        "semantic_parity": result.artifact.semantic_parity.value,
        "repaint_assessment": result.artifact.repaint_assessment.value,
        "deployment_authorization": result.artifact.deployment_authorization.value,
        "execution_state": result.artifact.execution_state.value,
    }
    assert json.loads(GOLDEN.read_text(encoding="utf-8")) == expected
