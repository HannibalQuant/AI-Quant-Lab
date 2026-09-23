"""Sprint 17 governed Pine source intake and exact-lineage tests."""

from __future__ import annotations

import ast
import inspect
import json
from dataclasses import fields, replace
from pathlib import Path
from typing import Any

import pytest
from test_optimization_selection import _request as optimization_request
from test_optimization_selection import _selection_case, search_space

from ai_quant_lab import EXE_01
from ai_quant_lab.core import pine_strategy_intake as pine_module
from ai_quant_lab.core.codec import decode, encode
from ai_quant_lab.core.dataset_store import (
    LocalDatasetRepository,
    RepositoryIntegrityFailure,
    RepositoryTypeMismatch,
    RepositoryWriteStatus,
    repository_key,
)
from ai_quant_lab.core.integrity import fingerprint_record
from ai_quant_lab.core.model import (
    ArtifactId,
    AuthorityBindingId,
    ExecutionState,
    InvalidSerialization,
    ObjectVersion,
    ProvenanceId,
    RunId,
    TraceabilityRef,
)
from ai_quant_lab.core.pine_strategy_contracts import (
    PineIntakeReasonCode,
    PineIntakeStatus,
    PineLanguageVersion,
    PineScriptKind,
    PineSemanticParityStatus,
    PineStrategyIntakeRecord,
    PineStrategyIntakeRequest,
    PineStrategySourceArtifact,
    RepaintAssessmentStatus,
    normalize_pine_source,
    pine_sha256,
)
from ai_quant_lab.core.pine_strategy_intake import (
    PineAuthorityInvalid,
    PineIntakeFailure,
    PineLineageMismatch,
    PineOptimizationSelectionEvidence,
    PineStrategyIntakeContext,
    intake_pine_strategy,
    verify_pine_strategy_intake_lineage,
)
from ai_quant_lab.core.research_eligibility_contracts import DeploymentAuthorizationStatus

V1 = ObjectVersion(1)
AUTHORITY_REF = TraceabilityRef(
    AuthorityBindingId("governed-pine-intake-authority"), V1, "sha256:" + "a" * 64
)
PROVENANCE_REF = TraceabilityRef(
    ProvenanceId("governed-pine-intake-provenance"), V1, "sha256:" + "b" * 64
)
GOLDEN = Path(__file__).parent / "golden" / "pine_strategy_intake_v1.json"


@pytest.fixture
def selection_bundle(tmp_path: Path) -> tuple[Any, ...]:
    return _selection_case(tmp_path, search_space())


def exact(record: Any, object_id: Any, version: ObjectVersion) -> TraceabilityRef:
    return TraceabilityRef(object_id, version, fingerprint_record(record))


def _unsafe[T](record: T, **changes: object) -> T:
    values = {field.name: getattr(record, field.name) for field in fields(record)}  # type: ignore[arg-type]
    values.update(changes)
    clone = object.__new__(type(record))
    for name, value in values.items():
        object.__setattr__(clone, name, value)
    return clone


def valid_source(*, line_ending: str = "\n", title: str = "Synthetic governed strategy") -> bytes:
    lines = (
        "//@version=6",
        "strategy(",
        f'    "{title}",',
        "    pyramiding=0,",
        "    process_orders_on_close=false,",
        "    calc_on_every_tick=false,",
        "    default_qty_type=strategy.cash,",
        "    default_qty_value=100",
        ")",
        "if close > open",
        '    strategy.entry("L", strategy.long)',
        "",
    )
    return line_ending.join(lines).encode("utf-8")


def _selected_context(selection_bundle: tuple[Any, ...]) -> tuple[Any, ...]:
    source, space, plan, candidates, execution, repository = selection_bundle
    selected_ref = execution.result.selected_candidate_ref
    assert selected_ref is not None
    selected_index = next(
        index
        for index, result in enumerate(execution.candidate_results)
        if exact(result, result.candidate_id, result.version) == selected_ref
    )
    evidence = candidates[selected_index]
    definition = execution.candidate_definitions[selected_index]
    candidate_result = execution.candidate_results[selected_index]
    optimization = PineOptimizationSelectionEvidence(
        optimization_request(plan),
        plan,
        space,
        source,
        candidates,
        execution.record,
        execution.result,
        execution.candidate_definitions,
        execution.candidate_results,
        execution.trials,
    )
    context = PineStrategyIntakeContext(evidence.strategy, evidence, AUTHORITY_REF, optimization)
    request = PineStrategyIntakeRequest(
        RunId("governed-pine-intake-run"),
        ArtifactId("governed-pine-strategy-source"),
        valid_source(),
        exact(evidence.strategy, evidence.strategy.strategy_id, evidence.strategy.version),
        exact(definition, definition.candidate_id, definition.version),
        exact(candidate_result, candidate_result.candidate_id, candidate_result.version),
        exact(
            execution.result,
            execution.result.selection_result_id,
            execution.result.version,
        ),
        exact(
            evidence.backtest_artifact,
            evidence.backtest_artifact.artifact_id,
            evidence.backtest_artifact.version,
        ),
        exact(
            evidence.scientific_result,
            evidence.scientific_result.validation_result_id,
            evidence.scientific_result.version,
        ),
        exact(
            evidence.robustness_result,
            evidence.robustness_result.robustness_result_id,
            evidence.robustness_result.version,
        ),
        AUTHORITY_REF,
        PROVENANCE_REF,
    )
    return request, context, execution, definition, candidate_result, repository


def _direct_context(selection_bundle: tuple[Any, ...]) -> tuple[Any, ...]:
    source, *_, repository = selection_bundle
    context = PineStrategyIntakeContext(source.strategy, source, AUTHORITY_REF)
    request = PineStrategyIntakeRequest(
        RunId("direct-pine-intake-run"),
        ArtifactId("direct-pine-strategy-source"),
        valid_source(title="Direct governed strategy"),
        exact(source.strategy, source.strategy.strategy_id, source.strategy.version),
        None,
        None,
        None,
        exact(
            source.backtest_artifact,
            source.backtest_artifact.artifact_id,
            source.backtest_artifact.version,
        ),
        exact(
            source.scientific_result,
            source.scientific_result.validation_result_id,
            source.scientific_result.version,
        ),
        exact(
            source.robustness_result,
            source.robustness_result.robustness_result_id,
            source.robustness_result.version,
        ),
        AUTHORITY_REF,
        PROVENANCE_REF,
    )
    return request, context, repository


@pytest.fixture
def pine_bundle(selection_bundle: tuple[Any, ...]) -> tuple[Any, ...]:
    request, context, execution, definition, candidate_result, repository = _selected_context(
        selection_bundle
    )
    result = intake_pine_strategy(request, context=context, repository=repository)
    return request, context, execution, definition, candidate_result, result, repository


def test_valid_selected_candidate_pine_v6_is_accepted(pine_bundle: tuple[Any, ...]) -> None:
    request, context, _, _, _, result, _ = pine_bundle
    assert result.record.status is PineIntakeStatus.ACCEPTED
    assert result.artifact.pine_language_version is PineLanguageVersion.PINE_V6
    assert result.artifact.script_kind is PineScriptKind.STRATEGY
    assert result.artifact.declared_script_title == "Synthetic governed strategy"
    assert result.artifact.strategy_definition_ref == request.strategy_definition_ref
    assert result.artifact.default_qty_value == "100"
    verify_pine_strategy_intake_lineage(
        artifact=result.artifact,
        record=result.record,
        request=request,
        context=context,
    )


def test_direct_strategy_binding_without_optimization_is_accepted(
    selection_bundle: tuple[Any, ...],
) -> None:
    request, context, repository = _direct_context(selection_bundle)
    result = intake_pine_strategy(request, context=context, repository=repository)
    assert result.record.status is PineIntakeStatus.ACCEPTED
    assert result.artifact.optimization_candidate_definition_ref is None
    assert result.artifact.optimization_candidate_result_ref is None
    assert result.artifact.optimization_selection_ref is None
    verify_pine_strategy_intake_lineage(
        artifact=result.artifact,
        record=result.record,
        request=request,
        context=context,
    )


def test_parity_repaint_and_execution_authority_remain_closed(pine_bundle: tuple[Any, ...]) -> None:
    *_, result, _ = pine_bundle
    assert result.artifact.semantic_parity is PineSemanticParityStatus.NOT_EVALUATED
    assert result.artifact.repaint_assessment is RepaintAssessmentStatus.NOT_EVALUATED
    assert result.artifact.deployment_authorization is DeploymentAuthorizationStatus.NOT_AUTHORIZED
    assert result.artifact.execution_state is ExecutionState.PLANNED_CLOSED
    assert result.record.deployment_authorization is DeploymentAuthorizationStatus.NOT_AUTHORIZED
    assert result.record.execution_state is ExecutionState.PLANNED_CLOSED
    assert EXE_01.state is ExecutionState.PLANNED_CLOSED


def test_source_hashes_and_normalization_are_exact(pine_bundle: tuple[Any, ...]) -> None:
    request, _, _, _, _, result, _ = pine_bundle
    assert result.artifact.source_sha256 == pine_sha256(request.source_bytes)
    assert result.artifact.normalized_source_text == normalize_pine_source(
        request.source_bytes.decode("utf-8")
    )
    assert result.artifact.normalized_source_sha256 == pine_sha256(
        result.artifact.normalized_source_text.encode("utf-8")
    )
    assert result.artifact.source_byte_size == len(request.source_bytes)


def test_crlf_changes_raw_hash_but_not_normalized_hash(
    selection_bundle: tuple[Any, ...], tmp_path: Path
) -> None:
    request, context, *_ = _selected_context(selection_bundle)
    lf_repository = LocalDatasetRepository(root=tmp_path / "lf", allowed_root=tmp_path)
    crlf_repository = LocalDatasetRepository(root=tmp_path / "crlf", allowed_root=tmp_path)
    lf = intake_pine_strategy(request, context=context, repository=lf_repository).artifact
    crlf_request = replace(
        request,
        requested_artifact_id=ArtifactId("governed-pine-strategy-source-crlf"),
        source_bytes=valid_source(line_ending="\r\n"),
    )
    crlf = intake_pine_strategy(crlf_request, context=context, repository=crlf_repository).artifact
    assert lf.source_sha256 != crlf.source_sha256
    assert lf.normalized_source_sha256 == crlf.normalized_source_sha256
    assert lf.normalized_source_text == crlf.normalized_source_text


def test_one_character_change_changes_raw_normalized_and_artifact_identity(
    selection_bundle: tuple[Any, ...], tmp_path: Path
) -> None:
    request, context, *_ = _selected_context(selection_bundle)
    first = intake_pine_strategy(
        request,
        context=context,
        repository=LocalDatasetRepository(root=tmp_path / "first", allowed_root=tmp_path),
    ).artifact
    changed_request = replace(
        request,
        requested_artifact_id=ArtifactId("governed-pine-strategy-source-changed"),
        source_bytes=valid_source(title="Synthetic governed strategy!"),
    )
    changed = intake_pine_strategy(
        changed_request,
        context=context,
        repository=LocalDatasetRepository(root=tmp_path / "changed", allowed_root=tmp_path),
    ).artifact
    assert first.source_sha256 != changed.source_sha256
    assert first.normalized_source_sha256 != changed.normalized_source_sha256
    assert fingerprint_record(first) != fingerprint_record(changed)


@pytest.mark.parametrize(
    ("source", "status", "reason"),
    (
        (b"", PineIntakeStatus.REJECTED, PineIntakeReasonCode.EMPTY_SOURCE),
        (b"\xff", PineIntakeStatus.REJECTED, PineIntakeReasonCode.INVALID_ENCODING),
        (
            b'//@version=6\x00\nstrategy("x")',
            PineIntakeStatus.REJECTED,
            PineIntakeReasonCode.NUL_BYTE_PRESENT,
        ),
        (
            b'//@version=5\nstrategy("x")\n',
            PineIntakeStatus.UNSUPPORTED,
            PineIntakeReasonCode.UNSUPPORTED_VERSION,
        ),
        (
            b'strategy("x")\n',
            PineIntakeStatus.INCOMPLETE,
            PineIntakeReasonCode.MISSING_VERSION,
        ),
        (
            b'//@version=6\n//@version=6\nstrategy("x")\n',
            PineIntakeStatus.REJECTED,
            PineIntakeReasonCode.MULTIPLE_VERSION_DECLARATIONS,
        ),
    ),
)
def test_invalid_source_boundaries_fail_closed(
    selection_bundle: tuple[Any, ...],
    source: bytes,
    status: PineIntakeStatus,
    reason: PineIntakeReasonCode,
) -> None:
    request, context, *_ = _selected_context(selection_bundle)
    with pytest.raises(PineIntakeFailure) as captured:
        intake_pine_strategy(
            replace(request, source_bytes=source),
            context=context,
            repository=selection_bundle[-1],
        )
    assert captured.value.status is status
    assert captured.value.reason_codes == (reason,)


def test_oversized_source_is_rejected(selection_bundle: tuple[Any, ...]) -> None:
    request, context, *_ = _selected_context(selection_bundle)
    with pytest.raises(PineIntakeFailure) as captured:
        intake_pine_strategy(
            replace(request, source_bytes=b"a" * (256 * 1024 + 1)),
            context=context,
            repository=selection_bundle[-1],
        )
    assert captured.value.reason_codes == (PineIntakeReasonCode.SOURCE_TOO_LARGE,)


@pytest.mark.parametrize(
    ("source", "status", "reason"),
    (
        (
            b'//@version=6\nindicator("Synthetic indicator")\n',
            PineIntakeStatus.REJECTED,
            PineIntakeReasonCode.INDICATOR_NOT_STRATEGY,
        ),
        (
            b'//@version=6\n// strategy("Comment only")\n',
            PineIntakeStatus.INCOMPLETE,
            PineIntakeReasonCode.SCRIPT_KIND_UNKNOWN,
        ),
        (
            b'//@version=6\nx = "strategy(\\"String only\\")"\n',
            PineIntakeStatus.INCOMPLETE,
            PineIntakeReasonCode.SCRIPT_KIND_UNKNOWN,
        ),
        (
            b'//@version=6\nstrategy("One")\nindicator("Two")\n',
            PineIntakeStatus.REJECTED,
            PineIntakeReasonCode.MULTIPLE_TOP_LEVEL_DECLARATIONS,
        ),
    ),
)
def test_classification_ignores_comments_and_strings_and_rejects_conflicts(
    selection_bundle: tuple[Any, ...],
    source: bytes,
    status: PineIntakeStatus,
    reason: PineIntakeReasonCode,
) -> None:
    request, context, *_ = _selected_context(selection_bundle)
    with pytest.raises(PineIntakeFailure) as captured:
        intake_pine_strategy(
            replace(request, source_bytes=source),
            context=context,
            repository=selection_bundle[-1],
        )
    assert captured.value.status is status
    assert captured.value.reason_codes == (reason,)


def test_missing_or_incompatible_static_settings_fail_closed(
    selection_bundle: tuple[Any, ...],
) -> None:
    request, context, *_ = _selected_context(selection_bundle)
    missing = b'//@version=6\nstrategy("Missing settings", pyramiding=0)\n'
    with pytest.raises(PineIntakeFailure) as incomplete:
        intake_pine_strategy(
            replace(request, source_bytes=missing),
            context=context,
            repository=selection_bundle[-1],
        )
    assert incomplete.value.reason_codes == (PineIntakeReasonCode.MISSING_STATIC_SETTING,)
    mismatched = valid_source().replace(b"pyramiding=0", b"pyramiding=1")
    with pytest.raises(PineIntakeFailure) as unsupported:
        intake_pine_strategy(
            replace(
                request,
                intake_run_id=RunId("governed-pine-intake-run-mismatch"),
                source_bytes=mismatched,
            ),
            context=context,
            repository=selection_bundle[-1],
        )
    assert unsupported.value.reason_codes == (PineIntakeReasonCode.STATIC_SETTING_MISMATCH,)


def test_external_data_request_is_unsupported(selection_bundle: tuple[Any, ...]) -> None:
    request, context, *_ = _selected_context(selection_bundle)
    source = valid_source() + b'x = request.security("EXT:USD", "1D", close)\n'
    with pytest.raises(PineIntakeFailure) as captured:
        intake_pine_strategy(
            replace(request, source_bytes=source),
            context=context,
            repository=selection_bundle[-1],
        )
    assert captured.value.reason_codes == (PineIntakeReasonCode.UNSUPPORTED_FEATURE,)


def test_wrong_governed_intake_authority_fails_closed(
    selection_bundle: tuple[Any, ...],
) -> None:
    request, context, *_ = _selected_context(selection_bundle)
    wrong = replace(
        request,
        authority_ref=TraceabilityRef(
            AuthorityBindingId("wrong-pine-intake-authority"),
            V1,
            "sha256:" + "9" * 64,
        ),
    )
    with pytest.raises(PineAuthorityInvalid, match="exact governed intake authority"):
        intake_pine_strategy(wrong, context=context, repository=selection_bundle[-1])


@pytest.mark.parametrize(
    ("source", "status", "reason", "normalized_expected"),
    (
        (
            b'//@version=5\nstrategy("x")\n',
            PineIntakeStatus.UNSUPPORTED,
            PineIntakeReasonCode.UNSUPPORTED_VERSION,
            True,
        ),
        (
            b'//@version=6\nindicator("x")\n',
            PineIntakeStatus.REJECTED,
            PineIntakeReasonCode.INDICATOR_NOT_STRATEGY,
            True,
        ),
        (
            b'strategy("x")\n',
            PineIntakeStatus.INCOMPLETE,
            PineIntakeReasonCode.MISSING_VERSION,
            True,
        ),
        (
            b"\xff",
            PineIntakeStatus.REJECTED,
            PineIntakeReasonCode.INVALID_ENCODING,
            False,
        ),
    ),
)
def test_failed_static_intake_is_persisted_for_audit(
    selection_bundle: tuple[Any, ...],
    source: bytes,
    status: PineIntakeStatus,
    reason: PineIntakeReasonCode,
    normalized_expected: bool,
) -> None:
    request, context, *_ = _selected_context(selection_bundle)
    repository = selection_bundle[-1]
    with pytest.raises(PineIntakeFailure):
        intake_pine_strategy(
            replace(request, source_bytes=source),
            context=context,
            repository=repository,
        )
    key = repository_key(
        PineStrategyIntakeRecord(
            request.intake_run_id,
            V1,
            request.requested_artifact_id,
            None,
            pine_sha256(source),
            (
                pine_sha256(normalize_pine_source(source.decode("utf-8")).encode("utf-8"))
                if normalized_expected
                else None
            ),
            len(source),
            "sha256:" + "0" * 64,
            status,
            (reason,),
            AUTHORITY_REF,
            PROVENANCE_REF,
            DeploymentAuthorizationStatus.NOT_AUTHORIZED,
            ExecutionState.PLANNED_CLOSED,
            V1,
        )
    )
    loaded = repository.load(key, PineStrategyIntakeRecord).record
    assert loaded.status is status
    assert loaded.reason_codes == (reason,)
    assert loaded.source_artifact_ref is None
    assert loaded.requested_artifact_id == request.requested_artifact_id
    assert loaded.source_sha256 == pine_sha256(source)
    assert (loaded.normalized_source_sha256 is not None) is normalized_expected
    assert loaded.source_byte_size == len(source)
    assert loaded.authority_ref == AUTHORITY_REF
    assert loaded.deployment_authorization is DeploymentAuthorizationStatus.NOT_AUTHORIZED
    assert loaded.execution_state is ExecutionState.PLANNED_CLOSED


def test_rejected_intake_is_deterministic_and_idempotent(
    selection_bundle: tuple[Any, ...],
) -> None:
    request, context, *_ = _selected_context(selection_bundle)
    repository = selection_bundle[-1]
    rejected = replace(
        request,
        source_bytes=b'//@version=5\nstrategy("x")\n',
    )
    with pytest.raises(PineIntakeFailure):
        intake_pine_strategy(rejected, context=context, repository=repository)
    key = repository_key(
        PineStrategyIntakeRecord(
            rejected.intake_run_id,
            V1,
            rejected.requested_artifact_id,
            None,
            pine_sha256(rejected.source_bytes),
            pine_sha256(normalize_pine_source(rejected.source_bytes.decode("utf-8")).encode("utf-8")),
            len(rejected.source_bytes),
            "sha256:" + "0" * 64,
            PineIntakeStatus.UNSUPPORTED,
            (PineIntakeReasonCode.UNSUPPORTED_VERSION,),
            AUTHORITY_REF,
            PROVENANCE_REF,
            DeploymentAuthorizationStatus.NOT_AUTHORIZED,
            ExecutionState.PLANNED_CLOSED,
            V1,
        )
    )
    first = repository.load(key, PineStrategyIntakeRecord).record
    first_bytes = encode(first)
    with pytest.raises(PineIntakeFailure):
        intake_pine_strategy(rejected, context=context, repository=repository)
    second = repository.load(key, PineStrategyIntakeRecord).record
    assert encode(second) == first_bytes
    assert second.input_fingerprint == first.input_fingerprint
    assert repository.store(second).status is RepositoryWriteStatus.ALREADY_PRESENT_IDENTICAL


def test_wrong_strategy_fingerprint_is_rejected(selection_bundle: tuple[Any, ...]) -> None:
    request, context, *_ = _selected_context(selection_bundle)
    wrong = replace(
        request,
        strategy_definition_ref=TraceabilityRef(
            request.strategy_definition_ref.object_id, V1, "sha256:" + "1" * 64
        ),
    )
    with pytest.raises(PineLineageMismatch, match="exact StrategyDefinition"):
        intake_pine_strategy(wrong, context=context, repository=selection_bundle[-1])


def test_non_selected_candidate_cannot_claim_selected_lineage(
    selection_bundle: tuple[Any, ...],
) -> None:
    request, context, execution, *_ = _selected_context(selection_bundle)
    other_index = next(
        index
        for index, result in enumerate(execution.candidate_results)
        if exact(result, result.candidate_id, result.version)
        != execution.result.selected_candidate_ref
    )
    other_definition = execution.candidate_definitions[other_index]
    other_result = execution.candidate_results[other_index]
    changed = replace(
        request,
        optimization_candidate_definition_ref=exact(
            other_definition, other_definition.candidate_id, other_definition.version
        ),
        optimization_candidate_result_ref=exact(
            other_result, other_result.candidate_id, other_result.version
        ),
    )
    with pytest.raises(PineLineageMismatch):
        intake_pine_strategy(changed, context=context, repository=selection_bundle[-1])


def test_parent_strategy_cannot_substitute_for_selected_candidate(
    selection_bundle: tuple[Any, ...],
) -> None:
    request, context, *_ = _selected_context(selection_bundle)
    optimization = context.optimization
    assert optimization is not None
    parent_context = PineStrategyIntakeContext(
        optimization.source.strategy,
        optimization.source,
        AUTHORITY_REF,
        optimization,
    )
    parent_request = replace(
        request,
        strategy_definition_ref=exact(
            optimization.source.strategy,
            optimization.source.strategy.strategy_id,
            optimization.source.strategy.version,
        ),
    )
    with pytest.raises(PineLineageMismatch):
        intake_pine_strategy(
            parent_request,
            context=parent_context,
            repository=selection_bundle[-1],
        )


@pytest.mark.parametrize(
    "field",
    (
        "source_backtest_result_ref",
        "source_scientific_validation_ref",
        "source_robustness_result_ref",
        "optimization_candidate_definition_ref",
        "optimization_candidate_result_ref",
        "optimization_selection_ref",
    ),
)
def test_evidence_reference_tamper_is_rejected(
    selection_bundle: tuple[Any, ...], field: str
) -> None:
    request, context, *_ = _selected_context(selection_bundle)
    reference = getattr(request, field)
    assert reference is not None
    changed = replace(
        request,
        **{
            field: TraceabilityRef(
                reference.object_id,
                reference.version,
                "sha256:" + "2" * 64,
            )
        },
    )
    with pytest.raises(PineLineageMismatch):
        intake_pine_strategy(changed, context=context, repository=selection_bundle[-1])


@pytest.mark.parametrize(
    ("target", "changes"),
    (
        ("artifact", {"source_sha256": "sha256:" + "3" * 64}),
        ("artifact", {"normalized_source_sha256": "sha256:" + "4" * 64}),
        ("artifact", {"source_text": '//@version=6\nstrategy("tampered")\n'}),
        ("record", {"input_fingerprint": "sha256:" + "5" * 64}),
        ("record", {"status": PineIntakeStatus.REJECTED}),
        (
            "record",
            {
                "authority_ref": TraceabilityRef(
                    AuthorityBindingId("tampered-pine-authority"),
                    V1,
                    "sha256:" + "6" * 64,
                )
            },
        ),
    ),
)
def test_persisted_artifact_and_record_tamper_fail_lineage(
    pine_bundle: tuple[Any, ...], target: str, changes: dict[str, object]
) -> None:
    request, context, _, _, _, result, _ = pine_bundle
    artifact = result.artifact
    record = result.record
    if target == "artifact":
        artifact = _unsafe(artifact, **changes)
    else:
        record = _unsafe(record, **changes)
    with pytest.raises(PineLineageMismatch):
        verify_pine_strategy_intake_lineage(
            artifact=artifact,
            record=record,
            request=request,
            context=context,
        )


def test_canonical_roundtrip_persistence_and_idempotency(pine_bundle: tuple[Any, ...]) -> None:
    *_, result, repository = pine_bundle
    for record in (result.artifact, result.record):
        assert decode(encode(record), type(record)) == record
        assert repository.store(record).status is RepositoryWriteStatus.ALREADY_PRESENT_IDENTICAL
        loaded = repository.load(repository_key(record), type(record))
        assert loaded.record == record


def test_persisted_corruption_wrong_type_version_and_unknown_field_fail(
    pine_bundle: tuple[Any, ...],
) -> None:
    *_, result, repository = pine_bundle
    key = repository_key(result.artifact)
    path = repository.path_for(key)
    original = path.read_bytes()
    payload = json.loads(original)
    payload["payload"]["declared_script_title"] = "tampered"
    path.write_text(json.dumps(payload), encoding="utf-8")
    with pytest.raises(RepositoryIntegrityFailure):
        repository.load(key, PineStrategySourceArtifact)
    path.write_bytes(original)
    with pytest.raises(RepositoryTypeMismatch):
        repository.load(key, PineStrategyIntakeRecord)
    payload = json.loads(original)
    payload["payload"]["unknown"] = True
    with pytest.raises(InvalidSerialization):
        decode(json.dumps(payload).encode(), PineStrategySourceArtifact)
    payload = json.loads(original)
    payload["payload"]["contract_version"] = 2
    with pytest.raises(InvalidSerialization):
        decode(json.dumps(payload).encode(), PineStrategySourceArtifact)


def test_same_input_is_byte_and_fingerprint_deterministic(pine_bundle: tuple[Any, ...]) -> None:
    request, context, _, _, _, first, repository = pine_bundle
    second = intake_pine_strategy(request, context=context, repository=repository)
    assert encode(first.artifact) == encode(second.artifact)
    assert encode(first.record) == encode(second.record)
    assert fingerprint_record(first.artifact) == fingerprint_record(second.artifact)
    assert fingerprint_record(first.record) == fingerprint_record(second.record)


def test_pine_intake_golden_is_pinned(pine_bundle: tuple[Any, ...]) -> None:
    request, _, _, _, _, result, _ = pine_bundle
    artifact = result.artifact
    record = result.record
    expected = {
        "format": "pine-strategy-intake-v1",
        "raw_sha256": artifact.source_sha256,
        "normalized_sha256": artifact.normalized_source_sha256,
        "source_byte_size": artifact.source_byte_size,
        "pine_version": artifact.pine_language_version.value,
        "script_kind": artifact.script_kind.value,
        "title": artifact.declared_script_title,
        "strategy_ref": str(artifact.strategy_definition_ref.object_id),
        "candidate_ref": str(artifact.optimization_candidate_result_ref.object_id),
        "selection_ref": str(artifact.optimization_selection_ref.object_id),
        "backtest_ref": str(artifact.source_backtest_result_ref.object_id),
        "scientific_ref": str(artifact.source_scientific_validation_ref.object_id),
        "robustness_ref": str(artifact.source_robustness_result_ref.object_id),
        "semantic_parity": artifact.semantic_parity.value,
        "repaint_assessment": artifact.repaint_assessment.value,
        "intake_status": record.status.value,
        "reason_codes": [item.value for item in record.reason_codes],
        "record_requested_artifact_id": str(record.requested_artifact_id),
        "record_raw_sha256": record.source_sha256,
        "record_normalized_sha256": record.normalized_source_sha256,
        "record_source_byte_size": record.source_byte_size,
        "artifact_fingerprint": fingerprint_record(artifact),
        "intake_record_fingerprint": fingerprint_record(record),
        "input_fingerprint": record.input_fingerprint,
        "requested_artifact_id": str(request.requested_artifact_id),
    }
    assert json.loads(GOLDEN.read_text(encoding="utf-8")) == expected


def test_capability_isolation_has_no_execution_network_or_pine_runtime() -> None:
    tree = ast.parse(inspect.getsource(pine_module))
    imports = {
        (node.module or "").split(".")[0]
        for node in ast.walk(tree)
        if isinstance(node, ast.ImportFrom)
    } | {
        alias.name.split(".")[0]
        for node in ast.walk(tree)
        if isinstance(node, ast.Import)
        for alias in node.names
    }
    assert not imports.intersection(
        {
            "aiohttp",
            "ccxt",
            "httpx",
            "importlib",
            "optuna",
            "requests",
            "selenium",
            "socket",
            "subprocess",
            "urllib",
        }
    )
    calls = {
        node.func.id
        for node in ast.walk(tree)
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
    }
    assert not calls.intersection({"eval", "exec"})
    source = inspect.getsource(pine_module).lower()
    assert "tradingview" not in source
    assert "webhook" not in source
    assert EXE_01.state is ExecutionState.PLANNED_CLOSED