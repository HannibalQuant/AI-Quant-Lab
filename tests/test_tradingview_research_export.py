"""Sprint 22 governed TradingView research export tests."""

# mypy: disable-error-code="no-untyped-def,no-untyped-call"

from __future__ import annotations

import json
from dataclasses import replace
from pathlib import Path

import pytest
from test_pine_safety_validation import build_assessment, build_generation
from test_pine_strategy_intake import PROVENANCE_REF, _direct_context, _selected_context

from ai_quant_lab.core.dataset_store import RepositoryReadStatus, repository_key
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
from ai_quant_lab.core.pine_strategy_contracts import RepaintAssessmentStatus
from ai_quant_lab.core.research_eligibility_contracts import DeploymentAuthorizationStatus
from ai_quant_lab.core.tradingview_research_export import (
    TradingViewResearchExportAuthorityInvalid,
    TradingViewResearchExportContext,
    TradingViewResearchExportLineageMismatch,
    TradingViewResearchExportRequest,
    build_tradingview_research_export,
    render_tradingview_research_manifest,
    verify_tradingview_research_export,
)
from ai_quant_lab.core.tradingview_research_export_contracts import (
    TradingViewResearchExportPackage,
    TradingViewResearchExportReadiness,
    TradingViewResearchExportRuntimeStatus,
    TradingViewResearchExportSafetyStatus,
)

pytest_plugins = ("test_pine_strategy_intake",)

V1 = ObjectVersion(1)
GOLDEN = Path(__file__).parent / "golden" / "tradingview_research_export_v1.json"
EXPORT_AUTHORITY = TraceabilityRef(
    AuthorityBindingId("tradingview-research-export-authority"),
    V1,
    "sha256:" + "7" * 64,
)


def exact(record, object_id, version):
    return TraceabilityRef(object_id, version, fingerprint_record(record))


def build_export_context(pine_context, repository, *, suffix=""):
    generation_request, generation_result, generator_context = build_generation(
        pine_context,
        repository,
        suffix=f"export-{suffix}" if suffix else "export",
    )
    safety_request, safety_context = build_assessment(
        generation_request,
        generation_result,
        generator_context,
        suffix=f"export-{suffix}" if suffix else "export",
    )
    from ai_quant_lab.core.pine_safety_validation import assess_governed_pine_static_safety

    safety_result = assess_governed_pine_static_safety(
        safety_request,
        context=safety_context,
    )
    context = TradingViewResearchExportContext(
        generation_request,
        generation_result,
        generator_context,
        safety_request,
        safety_result,
        safety_context,
        EXPORT_AUTHORITY,
    )
    request = TradingViewResearchExportRequest(
        RunId(f"tradingview-export-run-{suffix or 'optimized'}"),
        ArtifactId(f"tradingview-export-package-{suffix or 'optimized'}"),
        exact(
            generation_result.artifact,
            generation_result.artifact.pine_artifact_id,
            generation_result.artifact.version,
        ),
        generation_result.artifact.strategy_definition_ref,
        safety_result.assessment_id,
        safety_result.input_fingerprint,
        f"AIQL_{suffix or 'optimized'}_research",
        EXPORT_AUTHORITY,
        PROVENANCE_REF,
    )
    return request, context


@pytest.fixture
def export_bundle(selection_bundle):
    _old_request, pine_context, *_rest, repository = _selected_context(selection_bundle)
    request, context = build_export_context(pine_context, repository)
    execution = build_tradingview_research_export(
        request,
        context=context,
        repository=repository,
    )
    return request, context, execution, repository


def test_optimized_export_is_ready_and_immutably_stored(export_bundle):
    request, context, execution, repository = export_bundle

    verify_tradingview_research_export(
        request,
        package=execution.package,
        context=context,
    )

    package = execution.package
    assert (
        package.readiness
        is TradingViewResearchExportReadiness.READY_FOR_MANUAL_TRADINGVIEW_RESEARCH
    )
    assert package.safety_status is TradingViewResearchExportSafetyStatus.STATIC_SAFETY_PASS
    assert (
        package.runtime_status is TradingViewResearchExportRuntimeStatus.NOT_VERIFIED_ON_TRADINGVIEW
    )
    assert package.optimization_selection_ref is not None
    assert execution.pine_bytes == package.pine_source_text.encode("utf-8")
    assert execution.package_ref.expected_fingerprint == fingerprint_record(package)

    loaded = repository.load(repository_key(package), TradingViewResearchExportPackage)
    assert loaded.status is RepositoryReadStatus.FOUND_VERIFIED
    assert loaded.record == package


def test_direct_export_omits_optimization_selection(selection_bundle):
    _old_request, pine_context, repository = _direct_context(selection_bundle)
    request, context = build_export_context(pine_context, repository, suffix="direct")

    execution = build_tradingview_research_export(
        request,
        context=context,
        repository=repository,
    )

    assert execution.package.optimization_selection_ref is None
    assert (
        execution.package.readiness
        is TradingViewResearchExportReadiness.READY_FOR_MANUAL_TRADINGVIEW_RESEARCH
    )


def test_export_contains_exact_pine_and_research_evidence(export_bundle):
    _request, context, execution, _repository = export_bundle
    package = execution.package
    evidence = context.generator_context.pine_intake_context.evidence

    assert package.pine_source_text == context.generation_result.artifact.source_text
    assert package.pine_source_sha256 == context.generation_result.artifact.source_sha256
    assert package.strategy_ref == context.generation_result.artifact.strategy_definition_ref
    assert package.instrument_symbol == evidence.instrument.symbol
    assert package.timeframe_ref == evidence.eligibility.timeframe_ref
    assert package.normalized_manifest_ref == evidence.eligibility.normalized_manifest_ref
    assert package.normalized_lock_ref == evidence.eligibility.normalized_lock_ref
    assert package.backtest_ref.object_id == evidence.backtest_artifact.artifact_id
    assert (
        package.scientific_validation_ref.object_id
        == evidence.scientific_result.validation_result_id
    )
    assert package.robustness_ref.object_id == evidence.robustness_result.robustness_result_id


def test_manual_manifest_is_deterministic_and_explicit_about_runtime(export_bundle):
    _request, _context, execution, _repository = export_bundle

    first = render_tradingview_research_manifest(execution.package)
    second = render_tradingview_research_manifest(execution.package)
    manifest = json.loads(first.decode("utf-8"))

    assert first == second == execution.manifest_bytes
    assert manifest["runtime_status"] == "NOT_VERIFIED_ON_TRADINGVIEW"
    assert manifest["static_repaint_status"] == "NO_STATIC_REPAINT_HAZARD_DETECTED"
    assert manifest["artifact_repaint_assessment"] == "NOT_EVALUATED"
    assert manifest["backtest_ref"] == str(execution.package.backtest_ref.object_id)
    assert manifest["scientific_validation_ref"] == str(
        execution.package.scientific_validation_ref.object_id
    )
    assert manifest["robustness_ref"] == str(execution.package.robustness_ref.object_id)
    assert manifest["normalized_manifest_ref"] == str(
        execution.package.normalized_manifest_ref.object_id
    )
    assert manifest["normalized_lock_ref"] == str(
        execution.package.normalized_lock_ref.object_id
    )
    assert (
        manifest["generation_input_fingerprint"]
        == execution.package.generation_input_fingerprint
    )
    assert manifest["safety_input_fingerprint"] == execution.package.safety_input_fingerprint
    assert manifest["deployment_authorization"] == "NOT_AUTHORIZED"
    assert manifest["execution_state"] == "PLANNED_CLOSED"
    assert manifest["export_package_fingerprint"] == fingerprint_record(execution.package)


def test_manual_steps_name_exact_symbol_timeframe_and_file(export_bundle):
    _request, _context, execution, _repository = export_bundle
    package = execution.package
    joined = "\n".join(package.manual_steps)

    assert package.instrument_symbol in joined
    assert package.timeframe_token in joined
    assert package.pine_filename in joined
    assert "Strategy Tester" in joined
    assert "research-only" in joined


def test_strategy_parameters_are_sorted_and_exact(export_bundle):
    _request, context, execution, _repository = export_bundle
    strategy = context.generator_context.pine_intake_context.strategy
    params = dict(execution.package.strategy_parameters)

    assert tuple(name for name, _ in execution.package.strategy_parameters) == tuple(sorted(params))
    assert params["model"] == strategy.model.value
    assert params["threshold_bps"] == str(strategy.threshold_bps)
    assert params["fixed_notional_minor"] == str(strategy.fixed_notional_minor)
    assert params["signal_timing"] == strategy.signal_timing.value
    assert params["execution_timing"] == strategy.execution_timing.value


@pytest.mark.parametrize(
    "stem",
    (
        "",
        "../escape",
        "bad/name",
        "bad\\name",
        "bad name",
        ".hidden",
        "x" * 65,
    ),
)
def test_file_stem_is_bounded_and_cannot_escape_export(stem):
    with pytest.raises(ValueError):
        TradingViewResearchExportRequest(
            RunId("bad-export-run"),
            ArtifactId("bad-export-package"),
            TraceabilityRef(
                ArtifactId("pine"),
                V1,
                "sha256:" + "1" * 64,
            ),
            TraceabilityRef(
                ArtifactId("strategy"),
                V1,
                "sha256:" + "2" * 64,
            ),
            ArtifactId("safety"),
            "sha256:" + "3" * 64,
            stem,
            EXPORT_AUTHORITY,
            PROVENANCE_REF,
        )


def test_wrong_export_authority_fails_closed(export_bundle):
    request, context, _execution, repository = export_bundle
    wrong = TraceabilityRef(
        AuthorityBindingId("wrong-tradingview-export-authority"),
        V1,
        "sha256:" + "6" * 64,
    )
    request = replace(request, export_authority_ref=wrong)

    with pytest.raises(TradingViewResearchExportAuthorityInvalid):
        build_tradingview_research_export(
            request,
            context=context,
            repository=repository,
        )


def test_pine_artifact_substitution_fails_closed(export_bundle):
    request, context, _execution, repository = export_bundle
    wrong = TraceabilityRef(
        request.pine_artifact_ref.object_id,
        request.pine_artifact_ref.version,
        "sha256:" + "5" * 64,
    )
    request = replace(request, pine_artifact_ref=wrong)

    with pytest.raises(TradingViewResearchExportLineageMismatch):
        build_tradingview_research_export(
            request,
            context=context,
            repository=repository,
        )


def test_safety_fingerprint_substitution_fails_closed(export_bundle):
    request, context, _execution, repository = export_bundle
    request = replace(
        request,
        safety_input_fingerprint="sha256:" + "4" * 64,
    )

    with pytest.raises(TradingViewResearchExportLineageMismatch):
        build_tradingview_research_export(
            request,
            context=context,
            repository=repository,
        )


def test_provenance_substitution_fails_closed(export_bundle):
    request, context, _execution, repository = export_bundle
    wrong = TraceabilityRef(
        ProvenanceId("wrong-tradingview-export-provenance"),
        V1,
        "sha256:" + "3" * 64,
    )
    request = replace(request, provenance_ref=wrong)

    with pytest.raises(TradingViewResearchExportLineageMismatch):
        build_tradingview_research_export(
            request,
            context=context,
            repository=repository,
        )


def test_export_contract_rejects_source_hash_mismatch(export_bundle):
    _request, _context, execution, _repository = export_bundle

    with pytest.raises(ValueError):
        replace(
            execution.package,
            pine_source_sha256="sha256:" + "1" * 64,
        )


def test_tampered_export_package_fails_exact_verification(export_bundle):
    request, context, execution, _repository = export_bundle
    tampered = replace(
        execution.package,
        pine_source_text=execution.package.pine_source_text + "// tampered\n",
        pine_source_byte_size=len(
            (execution.package.pine_source_text + "// tampered\n").encode("utf-8")
        ),
    )

    with pytest.raises(TradingViewResearchExportLineageMismatch):
        verify_tradingview_research_export(
            request,
            package=tampered,
            context=context,
        )


def test_export_does_not_upgrade_runtime_repaint_or_execution(export_bundle):
    _request, _context, execution, _repository = export_bundle
    package = execution.package

    assert package.artifact_repaint_assessment is RepaintAssessmentStatus.NOT_EVALUATED
    assert (
        package.runtime_status is TradingViewResearchExportRuntimeStatus.NOT_VERIFIED_ON_TRADINGVIEW
    )
    assert package.deployment_authorization is DeploymentAuthorizationStatus.NOT_AUTHORIZED
    assert package.execution_state is ExecutionState.PLANNED_CLOSED


def test_export_module_has_no_tradingview_or_broker_automation():
    source = Path("src/ai_quant_lab/core/tradingview_research_export.py").read_text(
        encoding="utf-8"
    )
    forbidden = (
        "import requests",
        "import httpx",
        "import aiohttp",
        "import socket",
        "import subprocess",
        "selenium",
        "playwright",
        "webhook",
        "strategy.entry(",
        "strategy.close(",
    )
    for token in forbidden:
        assert token not in source


def test_tradingview_research_export_golden_is_pinned(export_bundle):
    _request, _context, execution, _repository = export_bundle
    package = execution.package
    expected = {
        "format": "tradingview-research-export-v1",
        "export_id": str(package.export_id),
        "package_fingerprint": fingerprint_record(package),
        "pine_artifact_ref": str(package.pine_artifact_ref.object_id),
        "strategy_ref": str(package.strategy_ref.object_id),
        "backtest_ref": str(package.backtest_ref.object_id),
        "scientific_validation_ref": str(package.scientific_validation_ref.object_id),
        "robustness_ref": str(package.robustness_ref.object_id),
        "optimization_selection_ref": (
            None
            if package.optimization_selection_ref is None
            else str(package.optimization_selection_ref.object_id)
        ),
        "instrument_symbol": package.instrument_symbol,
        "timeframe_token": package.timeframe_token,
        "generation_input_fingerprint": package.generation_input_fingerprint,
        "safety_input_fingerprint": package.safety_input_fingerprint,
        "safety_status": package.safety_status.value,
        "static_repaint_status": package.static_repaint_status,
        "artifact_repaint_assessment": package.artifact_repaint_assessment.value,
        "runtime_status": package.runtime_status.value,
        "pine_source_sha256": package.pine_source_sha256,
        "pine_source_byte_size": package.pine_source_byte_size,
        "pine_filename": package.pine_filename,
        "manifest_filename": package.manifest_filename,
        "readiness": package.readiness.value,
        "deployment_authorization": package.deployment_authorization.value,
        "execution_state": package.execution_state.value,
    }
    assert json.loads(GOLDEN.read_text(encoding="utf-8")) == expected
