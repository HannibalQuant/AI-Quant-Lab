"""Sprint 23 authoritative Phase 3 end-to-end closure tests."""

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
from test_optimization_selection import selection_bundle as optimization_selection_bundle

from ai_quant_lab.core.codec import decode, encode
from ai_quant_lab.core.dataset_store import (
    RepositoryReadStatus,
    repository_key,
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
from ai_quant_lab.core.phase3_end_to_end_closure import (
    Phase3EndToEndClosureAuthorityInvalid,
    Phase3EndToEndClosureContext,
    Phase3EndToEndClosureNotReady,
    Phase3EndToEndClosureRequest,
    run_phase3_end_to_end_closure,
    verify_phase3_end_to_end_closure,
)
from ai_quant_lab.core.phase3_end_to_end_closure_contracts import (
    Phase3EndToEndClosureRecord,
    Phase3EndToEndStage,
    Phase3EndToEndState,
)
from ai_quant_lab.core.real_csv_contracts import CsvAdmissionStatus
from ai_quant_lab.core.research_eligibility_contracts import (
    DeploymentAuthorizationStatus,
    ResearchDatasetEligibilityStatus,
)
from ai_quant_lab.core.scientific_validation_contracts import ScientificValidationDecision
from ai_quant_lab.core.tradingview_research_export_contracts import (
    TradingViewResearchExportReadiness,
    TradingViewResearchExportRuntimeStatus,
)

pytest_plugins = ("test_optimization_selection", "test_pine_strategy_intake")

V1 = ObjectVersion(1)
GOLDEN = Path(__file__).parent / "golden" / "phase3_end_to_end_closure_v1.json"

GENERATOR_AUTHORITY = TraceabilityRef(
    AuthorityBindingId("sprint-23-generator-authority"),
    V1,
    "sha256:" + "9" * 64,
)
SAFETY_AUTHORITY = TraceabilityRef(
    AuthorityBindingId("sprint-23-safety-authority"),
    V1,
    "sha256:" + "8" * 64,
)
EXPORT_AUTHORITY = TraceabilityRef(
    AuthorityBindingId("sprint-23-export-authority"),
    V1,
    "sha256:" + "7" * 64,
)
CLOSURE_AUTHORITY = TraceabilityRef(
    AuthorityBindingId("sprint-23-closure-authority"),
    V1,
    "sha256:" + "6" * 64,
)


def closure_request(*, suffix: str = "optimized"):
    return Phase3EndToEndClosureRequest(
        RunId(f"phase3-e2e-closure-run-{suffix}"),
        ArtifactId(f"phase3-e2e-closure-{suffix}"),
        "AIQL Phase 3 E2E Research Strategy",
        f"AIQL_phase3_e2e_{suffix}",
        GENERATOR_AUTHORITY,
        SAFETY_AUTHORITY,
        EXPORT_AUTHORITY,
        CLOSURE_AUTHORITY,
        PROVENANCE_REF,
    )


@pytest.fixture
def closure_bundle(selection_bundle):
    _old_request, pine_context, *_rest, repository = _selected_context(selection_bundle)
    context = Phase3EndToEndClosureContext(pine_context, CLOSURE_AUTHORITY)
    request = closure_request()
    execution = run_phase3_end_to_end_closure(
        request,
        context=context,
        repository=repository,
    )
    return request, context, execution, repository


def test_real_csv_to_tradingview_export_golden_path_is_one_current_order_pipeline(
    closure_bundle,
):
    request, context, execution, repository = closure_bundle
    evidence = context.pine_context.evidence
    package = execution.export_execution.package

    verify_phase3_end_to_end_closure(
        request,
        execution=execution,
        context=context,
    )

    assert evidence.admission.status is CsvAdmissionStatus.ADMITTED
    assert evidence.eligibility.status is ResearchDatasetEligibilityStatus.ELIGIBLE
    assert evidence.declaration.acquisition_method.value == "OPERATOR_LOCAL_FILE"
    assert evidence.admission.file_size > 0
    assert evidence.admission.row_count > 0
    assert evidence.eligibility.normalized_manifest_ref is not None
    assert evidence.eligibility.normalized_lock_ref is not None

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
        package.readiness
        is TradingViewResearchExportReadiness.READY_FOR_MANUAL_TRADINGVIEW_RESEARCH
    )
    assert package.pine_source_text == execution.generation_result.source_text
    assert package.strategy_ref == execution.record.strategy_ref
    assert package.backtest_ref == execution.record.backtest_ref
    assert package.scientific_validation_ref == execution.record.scientific_validation_ref
    assert package.robustness_ref == execution.record.robustness_ref
    assert package.optimization_selection_ref == execution.record.optimization_selection_ref
    assert package.normalized_manifest_ref == evidence.eligibility.normalized_manifest_ref
    assert package.normalized_lock_ref == evidence.eligibility.normalized_lock_ref

    loaded_export = repository.load(
        repository_key(package),
        type(package),
    )
    assert loaded_export.status is RepositoryReadStatus.FOUND_VERIFIED
    assert loaded_export.record == package

    loaded_closure = repository.load(
        repository_key(execution.record),
        Phase3EndToEndClosureRecord,
    )
    assert loaded_closure.status is RepositoryReadStatus.FOUND_VERIFIED
    assert loaded_closure.record == execution.record


def test_direct_strategy_uses_same_authoritative_current_order_without_optimization(
    selection_bundle,
):
    _old_request, pine_context, repository = _direct_context(selection_bundle)
    context = Phase3EndToEndClosureContext(pine_context, CLOSURE_AUTHORITY)
    request = closure_request(suffix="direct")

    execution = run_phase3_end_to_end_closure(
        request,
        context=context,
        repository=repository,
    )

    assert Phase3EndToEndStage.OPTIMIZATION_SELECTED not in execution.record.stages
    assert execution.record.optimization_selection_ref is None
    assert execution.export_execution.package.optimization_selection_ref is None
    verify_phase3_end_to_end_closure(
        request,
        execution=execution,
        context=context,
    )


def test_failed_upstream_scientific_evidence_cannot_reach_export(selection_bundle):
    _old_request, pine_context, *_rest, repository = _selected_context(selection_bundle)
    failed_scientific = replace(
        pine_context.evidence.scientific_result,
        decision=ScientificValidationDecision.FAIL,
    )
    failed_evidence = replace(
        pine_context.evidence,
        scientific_result=failed_scientific,
    )
    failed_pine_context = replace(pine_context, evidence=failed_evidence)
    context = Phase3EndToEndClosureContext(failed_pine_context, CLOSURE_AUTHORITY)

    with pytest.raises(Phase3EndToEndClosureNotReady):
        run_phase3_end_to_end_closure(
            closure_request(suffix="failed-science"),
            context=context,
            repository=repository,
        )


def test_wrong_closure_authority_fails_before_generation(selection_bundle):
    _old_request, pine_context, *_rest, repository = _selected_context(selection_bundle)
    context = Phase3EndToEndClosureContext(pine_context, CLOSURE_AUTHORITY)
    wrong = TraceabilityRef(
        AuthorityBindingId("wrong-phase3-closure-authority"),
        V1,
        "sha256:" + "5" * 64,
    )
    request = replace(closure_request(suffix="wrong-authority"), closure_authority_ref=wrong)

    with pytest.raises(Phase3EndToEndClosureAuthorityInvalid):
        run_phase3_end_to_end_closure(
            request,
            context=context,
            repository=repository,
        )


def test_closure_record_roundtrips_through_strict_codec(closure_bundle):
    _request, _context, execution, _repository = closure_bundle

    encoded = encode(execution.record)
    decoded = decode(encoded, Phase3EndToEndClosureRecord)

    assert decoded == execution.record
    assert fingerprint_record(decoded) == fingerprint_record(execution.record)


def test_closure_keeps_tradingview_runtime_and_execution_open_questions_explicit(
    closure_bundle,
):
    _request, _context, execution, _repository = closure_bundle
    record = execution.record
    package = execution.export_execution.package

    assert (
        record.runtime_status is TradingViewResearchExportRuntimeStatus.NOT_VERIFIED_ON_TRADINGVIEW
    )
    assert (
        package.runtime_status is TradingViewResearchExportRuntimeStatus.NOT_VERIFIED_ON_TRADINGVIEW
    )
    assert record.deployment_authorization is DeploymentAuthorizationStatus.NOT_AUTHORIZED
    assert record.execution_state is ExecutionState.PLANNED_CLOSED


def test_sprint23_closure_has_no_broker_or_tradingview_automation_capability():
    source = Path("src/ai_quant_lab/core/phase3_end_to_end_closure.py").read_text(encoding="utf-8")
    forbidden = (
        "import requests",
        "import httpx",
        "import aiohttp",
        "import socket",
        "import subprocess",
        "selenium",
        "playwright",
        "webdriver",
        "strategy.entry(",
        "strategy.close(",
        "broker_api",
        "place_order(",
    )
    for token in forbidden:
        assert token not in source


def test_phase3_end_to_end_closure_golden_is_pinned(closure_bundle):
    _request, context, execution, _repository = closure_bundle
    evidence = context.pine_context.evidence
    package = execution.export_execution.package
    expected = {
        "format": "phase3-end-to-end-closure-v1",
        "closure_id": str(execution.record.closure_id),
        "closure_fingerprint": fingerprint_record(execution.record),
        "source_declaration_ref": str(execution.record.source_declaration_ref.object_id),
        "admission_ref": str(execution.record.admission_ref.object_id),
        "eligibility_ref": str(execution.record.eligibility_ref.object_id),
        "strategy_ref": str(execution.record.strategy_ref.object_id),
        "backtest_ref": str(execution.record.backtest_ref.object_id),
        "scientific_validation_ref": str(execution.record.scientific_validation_ref.object_id),
        "robustness_ref": str(execution.record.robustness_ref.object_id),
        "optimization_selection_ref": str(execution.record.optimization_selection_ref.object_id),
        "pine_artifact_ref": str(execution.record.pine_artifact_ref.object_id),
        "export_ref": str(execution.record.export_ref.object_id),
        "source_file_sha256": evidence.admission.file_sha256,
        "normalized_manifest_ref": str(package.normalized_manifest_ref.object_id),
        "normalized_lock_ref": str(package.normalized_lock_ref.object_id),
        "pine_source_sha256": package.pine_source_sha256,
        "safety_input_fingerprint": execution.record.safety_input_fingerprint,
        "stages": [stage.value for stage in execution.record.stages],
        "final_state": execution.record.final_state.value,
        "runtime_status": execution.record.runtime_status.value,
        "deployment_authorization": execution.record.deployment_authorization.value,
        "execution_state": execution.record.execution_state.value,
    }
    assert json.loads(GOLDEN.read_text(encoding="utf-8")) == expected
