"""Sprint 26 activation of the existing multi-signal research-to-Pine workflow."""

from __future__ import annotations

from pathlib import Path

import pytest
from test_optimization_selection import _multi_signal_source

from ai_quant_lab.core.dataset_store import LocalDatasetRepository
from ai_quant_lab.core.governed_pine_generator import (
    GovernedPineGenerationRequest,
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
from ai_quant_lab.core.phase3_end_to_end_closure import (
    Phase3EndToEndClosureContext,
    Phase3EndToEndClosureNotReady,
    Phase3EndToEndClosureRequest,
    run_phase3_end_to_end_closure,
)
from ai_quant_lab.core.pine_strategy_contracts import PineIntakeStatus
from ai_quant_lab.core.pine_strategy_intake import PineStrategyIntakeContext
from ai_quant_lab.core.research_eligibility_contracts import DeploymentAuthorizationStatus
from ai_quant_lab.core.scientific_validation_contracts import ScientificValidationDecision
from ai_quant_lab.core.strategy_backtest_contracts import StrategyModel

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


def test_multi_signal_evidence_generates_pine_and_final_closure_remains_fail_closed(
    tmp_path: Path,
) -> None:
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
    generator_context = GovernedPineGeneratorContext(
        pine_context,
        GENERATOR_AUTHORITY,
    )
    generation_request = GovernedPineGenerationRequest(
        RunId("sprint-26-generator-run"),
        RunId("sprint-26-intake-run"),
        ArtifactId("sprint-26-multi-signal-pine"),
        exact(evidence.strategy, evidence.strategy.strategy_id, evidence.strategy.version),
        "AIQL SOLUSDT 4H Multi Signal Research",
        GENERATOR_AUTHORITY,
        PINE_AUTHORITY,
        PROVENANCE,
    )

    generation = generate_governed_pine_strategy(
        generation_request,
        context=generator_context,
        repository=repository,
    )
    verify_governed_pine_generation(
        generation_request,
        result=generation,
        context=generator_context,
    )

    assert evidence.strategy.model is StrategyModel.MULTI_SIGNAL_TREND_LONG_SHORT
    assert (
        generation.generator_profile
        == "AIQL_GOVERNED_PINE_V6_MULTI_SIGNAL_TREND_LONG_SHORT_V1"
    )
    assert generation.intake_record.status is PineIntakeStatus.ACCEPTED
    assert 'strategy.entry("AIQL-L", strategy.long)' in generation.source_text
    assert 'strategy.entry("AIQL-S", strategy.short)' in generation.source_text
    assert generation.deployment_authorization is DeploymentAuthorizationStatus.NOT_AUTHORIZED
    assert generation.execution_state is ExecutionState.PLANNED_CLOSED

    assert evidence.scientific_result.decision is not ScientificValidationDecision.PASS

    closure_context = Phase3EndToEndClosureContext(pine_context, CLOSURE_AUTHORITY)
    closure_request = Phase3EndToEndClosureRequest(
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
    with pytest.raises(
        Phase3EndToEndClosureNotReady,
        match="scientific validation PASS",
    ):
        run_phase3_end_to_end_closure(
            closure_request,
            context=closure_context,
            repository=repository,
        )
