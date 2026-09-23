"""Sprint 16 bounded grid-search and selection-governance tests."""

from __future__ import annotations

import ast
import copy
import inspect
import json
from dataclasses import replace
from pathlib import Path
from typing import Any

import pytest
from test_robustness_validation import (
    ROBUSTNESS_AUTHORITY_REF,
    ROBUSTNESS_PROVENANCE_REF,
    RobustnessBundle,
    robustness_plan,
)
from test_robustness_validation import (
    _execute as execute_robustness,
)
from test_scientific_validation import (
    AUTHORITY_REF as VALIDATION_AUTHORITY_REF,
)
from test_scientific_validation import (
    COMPLETED_AT as VALIDATION_COMPLETED_AT,
)
from test_scientific_validation import (
    PROVENANCE_REF as VALIDATION_PROVENANCE_REF,
)
from test_scientific_validation import _context, _run, exact, validation_plan
from test_strategy_backtest import PROVENANCE_REF as BACKTEST_PROVENANCE_REF

from ai_quant_lab import EXE_01
from ai_quant_lab.core import optimization_selection as optimization_module
from ai_quant_lab.core.codec import decode, encode
from ai_quant_lab.core.dataset_store import (
    LocalDatasetRepository,
    RepositoryIntegrityFailure,
    RepositoryTypeMismatch,
    RepositoryWriteStatus,
    repository_key,
)
from ai_quant_lab.core.experiment_authorization import (
    ExperimentAuthorizationRequest,
    authorize_experiment,
)
from ai_quant_lab.core.experiment_runner import ExperimentRunRequest
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
    ValidationId,
)
from ai_quant_lab.core.optimization_contracts import (
    CandidateEligibility,
    OptimizationContractError,
    OptimizationMultiplicityPolicy,
    OptimizationObjective,
    OptimizationParameter,
    OptimizationParameterName,
    OptimizationParameterType,
    OptimizationPlan,
    OptimizationReasonCode,
    OptimizationRequest,
    OptimizationRunRecord,
    OptimizationSearchMethod,
    OptimizationSearchSpace,
    OptimizationSelectionResult,
    SelectionDecision,
)
from ai_quant_lab.core.optimization_selection import (
    OptimizationEvidence,
    OptimizationInputInvalid,
    OptimizationLineageMismatch,
    OptimizationSelectionExecutionResult,
    _expected_candidate_specification,
    corrected_alpha,
    corrected_confidence,
    derive_candidate,
    enumerate_parameter_sets,
    run_optimization_selection,
    verify_optimization_selection_lineage,
)
from ai_quant_lab.core.research_eligibility_contracts import DeploymentAuthorizationStatus
from ai_quant_lab.core.robustness_validation import run_robustness_validation
from ai_quant_lab.core.robustness_validation_contracts import (
    RobustnessDecision,
    RobustnessValidationRequest,
)
from ai_quant_lab.core.scientific_validation import run_scientific_validation
from ai_quant_lab.core.scientific_validation_contracts import (
    MultiplicityPolicy,
    ScientificValidationDecision,
    ValidationRequest,
)
from ai_quant_lab.core.strategy_backtest import (
    StrategyBacktestRunRequest,
    run_authorized_strategy_backtest,
    strategy_backtest_replay_contract,
)

V1 = ObjectVersion(1)
SELECTION_AUTHORITY_REF = TraceabilityRef(
    AuthorityBindingId("optimization-selection-authority"), V1, "sha256:" + "e" * 64
)
SELECTION_PROVENANCE_REF = TraceabilityRef(
    ProvenanceId("optimization-selection-provenance"), V1, "sha256:" + "f" * 64
)
GOLDEN = Path(__file__).parent / "golden" / "optimization_selection_v1.json"


def _unsafe[T](record: T, **changes: object) -> T:
    changed = copy.copy(record)
    for field, value in changes.items():
        object.__setattr__(changed, field, value)
    return changed


def _evidence(bundle: RobustnessBundle) -> OptimizationEvidence:
    validation, robustness_request, robustness_policy, robustness = bundle
    scientific_request, backtest_request, backtest, scientific, context = validation
    return OptimizationEvidence(
        robustness_request,
        robustness_policy,
        robustness.record,
        robustness.result,
        scientific_request,
        validation_plan(),
        scientific.record,
        scientific.result,
        backtest_request,
        backtest.record,
        backtest.artifact,
        context[9].record,
        context[7],
        context[8],
        context[5],
        context[4],
        context[2],
        context[0],
        strategy_backtest_replay_contract(),
        context[6],
        context[10],
        context[3],
    )


def _source(tmp_path: Path) -> OptimizationEvidence:
    validation = _run(
        _context(tmp_path, "optimization-source", ((100, 120),) * 4),
        validation_plan(),
    )
    scientific_ref = exact(
        validation[3].result,
        validation[3].result.validation_result_id,
        validation[3].result.version,
    )
    return _evidence(execute_robustness(validation, robustness_plan(scientific_ref)))


def search_space(*, upper: int = 200, step: int = 200) -> OptimizationSearchSpace:
    return OptimizationSearchSpace(
        ArtifactId("threshold-grid-search-space-v1"),
        V1,
        (
            OptimizationParameter(
                OptimizationParameterName.THRESHOLD_BPS,
                OptimizationParameterType.INTEGER,
                0,
                upper,
                step,
                0,
            ),
        ),
        V1,
    )


def optimization_plan(
    source: OptimizationEvidence,
    space: OptimizationSearchSpace,
    *,
    multiplicity: OptimizationMultiplicityPolicy = OptimizationMultiplicityPolicy.BONFERRONI,
    maximum_trials: int = 2,
) -> OptimizationPlan:
    return OptimizationPlan(
        ArtifactId("controlled-optimization-selection-plan-v1"),
        V1,
        exact(space, space.search_space_id, space.version),
        exact(source.strategy, source.strategy.strategy_id, source.strategy.version),
        exact(
            source.specification,
            source.specification.experiment_id,
            source.specification.version,
        ),
        exact(
            source.robustness_result,
            source.robustness_result.robustness_result_id,
            source.robustness_result.version,
        ),
        source.specification.normalized_manifest_ref,
        source.specification.normalized_lock_ref,
        source.specification.engine_contract_ref,
        exact(
            source.validation_plan,
            source.validation_plan.validation_plan_id,
            source.validation_plan.version,
        ),
        exact(
            source.robustness_plan,
            source.robustness_plan.robustness_plan_id,
            source.robustness_plan.version,
        ),
        OptimizationSearchMethod.GRID_SEARCH,
        maximum_trials,
        OptimizationObjective.ROBUSTNESS_AWARE_TOTAL_RETURN,
        4,
        "0.5",
        multiplicity,
        "0.05",
        SELECTION_AUTHORITY_REF,
        SELECTION_PROVENANCE_REF,
        V1,
    )


def _request(plan: OptimizationPlan) -> OptimizationRequest:
    return OptimizationRequest(
        RunId("controlled-optimization-run"),
        ArtifactId("controlled-optimization-selection-result"),
        exact(plan, plan.optimization_plan_id, plan.version),
        SELECTION_AUTHORITY_REF,
        SELECTION_PROVENANCE_REF,
    )


def _candidate_evidence_with_repository(
    source: OptimizationEvidence,
    repository: Any,
    plan: OptimizationPlan,
    space: OptimizationSearchSpace,
    parameters: tuple[tuple[str, int], ...],
    candidate_count: int,
) -> OptimizationEvidence:
    definition, strategy = derive_candidate(
        plan=plan,
        search_space=space,
        parent_strategy=source.strategy,
        source=source,
        parameters=parameters,
    )
    suffix = str(definition.candidate_id).removeprefix("artifact:optimization-candidate-")
    specification = _expected_candidate_specification(source, strategy, suffix)
    authorization = authorize_experiment(
        ExperimentAuthorizationRequest(
            ArtifactId(f"optimization-authorization-{suffix}"),
            specification,
            source.authorization_policy,
            source.authorization.decision_time,
            source.authorization.decision_actor_id,
        ),
        eligibility=source.eligibility,
        eligibility_policy=source.eligibility_policy,
        admission=source.admission,
        declaration=source.declaration,
        report=source.report,
        repository=repository,
    ).record
    experiment_run = ExperimentRunRequest(
        RunId(f"opt-bt-{suffix}"),
        ArtifactId(f"opt-bt-result-{suffix}"),
        exact(authorization, authorization.authorization_id, authorization.version),
        exact(specification, specification.experiment_id, specification.version),
        exact(
            source.authorization_policy,
            source.authorization_policy.policy_id,
            source.authorization_policy.version,
        ),
        exact(source.eligibility, source.eligibility.eligibility_id, source.eligibility.version),
        exact(
            source.engine_contract, source.engine_contract.engine_id, source.engine_contract.version
        ),
        source.backtest_request.experiment_run.completed_at,
        BACKTEST_PROVENANCE_REF,
    )
    backtest_request = StrategyBacktestRunRequest(
        experiment_run,
        exact(strategy, strategy.strategy_id, strategy.version),
    )
    backtest = run_authorized_strategy_backtest(
        backtest_request,
        authorization=authorization,
        specification=specification,
        policy=source.authorization_policy,
        eligibility=source.eligibility,
        eligibility_policy=source.eligibility_policy,
        admission=source.admission,
        declaration=source.declaration,
        report=source.report,
        engine_contract=source.engine_contract,
        strategy=strategy,
        instrument=source.instrument,
        repository=repository,
    )
    alpha = corrected_alpha(plan, candidate_count)
    confidence = source.validation_plan.confidence_level
    if alpha is not None:
        confidence = corrected_confidence(alpha)
    validation_policy = replace(
        source.validation_plan,
        validation_plan_id=ArtifactId(f"opt-validation-plan-{suffix}"),
        confidence_level=confidence,
        multiplicity_policy=(
            MultiplicityPolicy.SINGLE_PREDECLARED_TEST
            if candidate_count == 1
            else (
                MultiplicityPolicy.MULTIPLE_TESTS_CORRECTED
                if plan.multiplicity_policy is OptimizationMultiplicityPolicy.BONFERRONI
                else MultiplicityPolicy.MULTIPLE_TESTS_UNCORRECTED
            )
        ),
    )
    validation_request = ValidationRequest(
        RunId(f"opt-validation-run-{suffix}"),
        ValidationId(f"opt-validation-result-{suffix}"),
        exact(
            validation_policy,
            validation_policy.validation_plan_id,
            validation_policy.version,
        ),
        exact(backtest.artifact, backtest.artifact.artifact_id, backtest.artifact.version),
        exact(backtest.record, backtest.record.run_id, backtest.record.version),
        VALIDATION_AUTHORITY_REF,
        VALIDATION_COMPLETED_AT,
        VALIDATION_PROVENANCE_REF,
    )
    scientific = run_scientific_validation(
        validation_request,
        plan=validation_policy,
        backtest_record=backtest.record,
        backtest_artifact=backtest.artifact,
        backtest_request=backtest_request,
        authorization=authorization,
        specification=specification,
        policy=source.authorization_policy,
        eligibility=source.eligibility,
        engine_contract=source.engine_contract,
        strategy=strategy,
        instrument=source.instrument,
        report=source.report,
        repository=repository,
    )
    robust_policy = replace(
        source.robustness_plan,
        robustness_plan_id=ArtifactId(f"opt-robustness-plan-{suffix}"),
        source_scientific_validation_ref=exact(
            scientific.result,
            scientific.result.validation_result_id,
            scientific.result.version,
        ),
    )
    robust_request = RobustnessValidationRequest(
        RunId(f"opt-robustness-run-{suffix}"),
        ArtifactId(f"opt-robustness-result-{suffix}"),
        exact(robust_policy, robust_policy.robustness_plan_id, robust_policy.version),
        exact(
            scientific.result,
            scientific.result.validation_result_id,
            scientific.result.version,
        ),
        exact(scientific.record, scientific.record.validation_run_id, scientific.record.version),
        exact(backtest.artifact, backtest.artifact.artifact_id, backtest.artifact.version),
        exact(backtest.record, backtest.record.run_id, backtest.record.version),
        ROBUSTNESS_AUTHORITY_REF,
        ROBUSTNESS_PROVENANCE_REF,
    )
    robustness = run_robustness_validation(
        robust_request,
        plan=robust_policy,
        scientific_result=scientific.result,
        validation_record=scientific.record,
        scientific_request=validation_request,
        validation_plan=validation_policy,
        backtest_artifact=backtest.artifact,
        backtest_record=backtest.record,
        backtest_request=backtest_request,
        authorization=authorization,
        specification=specification,
        policy=source.authorization_policy,
        eligibility=source.eligibility,
        eligibility_policy=source.eligibility_policy,
        admission=source.admission,
        declaration=source.declaration,
        engine_contract=source.engine_contract,
        strategy=strategy,
        instrument=source.instrument,
        report=source.report,
        repository=repository,
    )
    return OptimizationEvidence(
        robust_request,
        robust_policy,
        robustness.record,
        robustness.result,
        validation_request,
        validation_policy,
        scientific.record,
        scientific.result,
        backtest_request,
        backtest.record,
        backtest.artifact,
        authorization,
        specification,
        source.authorization_policy,
        source.eligibility,
        source.eligibility_policy,
        source.admission,
        source.declaration,
        source.engine_contract,
        strategy,
        source.instrument,
        source.report,
    )


@pytest.fixture
def selection_bundle(
    tmp_path: Path,
) -> tuple[
    OptimizationEvidence,
    OptimizationSearchSpace,
    OptimizationPlan,
    tuple[OptimizationEvidence, ...],
    OptimizationSelectionExecutionResult,
    Any,
]:
    return _selection_case(tmp_path, search_space())


def _selection_case(
    tmp_path: Path,
    space: OptimizationSearchSpace,
    *,
    multiplicity: OptimizationMultiplicityPolicy = OptimizationMultiplicityPolicy.BONFERRONI,
) -> tuple[
    OptimizationEvidence,
    OptimizationSearchSpace,
    OptimizationPlan,
    tuple[OptimizationEvidence, ...],
    OptimizationSelectionExecutionResult,
    LocalDatasetRepository,
]:
    source = _source(tmp_path)
    repository = LocalDatasetRepository(
        root=tmp_path / "vault-optimization-source", allowed_root=tmp_path
    )
    plan = optimization_plan(
        source,
        space,
        multiplicity=multiplicity,
        maximum_trials=len(enumerate_parameter_sets(space, 256)),
    )
    parameter_sets = enumerate_parameter_sets(space, plan.maximum_trials)
    candidates = tuple(
        _candidate_evidence_with_repository(
            source, repository, plan, space, parameters, len(parameter_sets)
        )
        for parameters in parameter_sets
    )
    result = run_optimization_selection(
        _request(plan),
        plan=plan,
        search_space=space,
        source=source,
        candidates=candidates,
        repository=repository,
    )
    return source, space, plan, candidates, result, repository


def test_grid_is_canonical_bounded_and_repeatable() -> None:
    space = search_space(upper=20, step=10)
    expected = (
        (("threshold_bps", 0),),
        (("threshold_bps", 10),),
        (("threshold_bps", 20),),
    )
    assert enumerate_parameter_sets(space, 3) == expected
    assert enumerate_parameter_sets(space, 2) == expected[:2]
    assert enumerate_parameter_sets(space, 3) == enumerate_parameter_sets(space, 3)


@pytest.mark.parametrize(
    "kwargs",
    (
        {"lower_bound": 2, "upper_bound": 1},
        {"step": 0},
        {"upper_bound": 10_001},
    ),
)
def test_search_parameter_bounds_fail_closed(kwargs: dict[str, int]) -> None:
    values = dict(lower_bound=0, upper_bound=10, step=10, default_value=0)
    values.update(kwargs)
    with pytest.raises(OptimizationContractError):
        OptimizationParameter(
            OptimizationParameterName.THRESHOLD_BPS,
            OptimizationParameterType.INTEGER,
            **values,
        )


def test_duplicate_search_parameter_fails_closed() -> None:
    parameter = OptimizationParameter(
        OptimizationParameterName.THRESHOLD_BPS,
        OptimizationParameterType.INTEGER,
        0,
        10,
        10,
        0,
    )
    with pytest.raises(OptimizationContractError):
        OptimizationSearchSpace(
            ArtifactId("duplicate-parameter-space"), V1, (parameter, parameter), V1
        )


def test_selection_uses_independent_candidate_evidence_and_bonferroni(
    selection_bundle: tuple[Any, ...],
) -> None:
    _, _, plan, candidates, execution, _ = selection_bundle
    assert corrected_alpha(plan, 2) == "0.025"
    assert all(item.validation_plan.confidence_level == "0.975" for item in candidates)
    assert all(
        item.validation_plan.multiplicity_policy is MultiplicityPolicy.MULTIPLE_TESTS_CORRECTED
        for item in candidates
    )
    assert execution.result.decision is SelectionDecision.SELECTED
    assert execution.result.eligible_candidates == 1
    assert execution.result.corrected_alpha == "0.025"
    assert execution.candidate_results[0].eligibility is CandidateEligibility.ELIGIBLE
    assert execution.candidate_results[1].eligibility is CandidateEligibility.REJECTED
    assert candidates[0].scientific_result.decision is ScientificValidationDecision.PASS
    assert candidates[0].robustness_result.decision is RobustnessDecision.PASS
    assert candidates[1].scientific_result.decision is ScientificValidationDecision.INCONCLUSIVE
    assert candidates[1].robustness_result.decision is not RobustnessDecision.PASS


def test_single_candidate_policy_allows_exactly_one_candidate(tmp_path: Path) -> None:
    space = OptimizationSearchSpace(
        ArtifactId("single-candidate-search-space"),
        V1,
        (
            OptimizationParameter(
                OptimizationParameterName.THRESHOLD_BPS,
                OptimizationParameterType.INTEGER,
                0,
                0,
                1,
                0,
            ),
        ),
        V1,
    )
    *_, candidates, execution, _ = _selection_case(
        tmp_path,
        space,
        multiplicity=OptimizationMultiplicityPolicy.SINGLE_CANDIDATE,
    )
    assert (
        candidates[0].validation_plan.multiplicity_policy
        is MultiplicityPolicy.SINGLE_PREDECLARED_TEST
    )
    assert candidates[0].validation_plan.confidence_level == "0.95"
    assert execution.result.decision is SelectionDecision.SELECTED
    assert execution.result.corrected_alpha == "0.05"
    assert execution.result.attempted_trials == 1


def test_no_eligible_candidates_is_inconclusive(tmp_path: Path) -> None:
    space = OptimizationSearchSpace(
        ArtifactId("no-eligible-candidate-search-space"),
        V1,
        (
            OptimizationParameter(
                OptimizationParameterName.THRESHOLD_BPS,
                OptimizationParameterType.INTEGER,
                200,
                400,
                200,
                200,
            ),
        ),
        V1,
    )
    *_, execution, _ = _selection_case(tmp_path, space)
    assert execution.result.decision is SelectionDecision.INCONCLUSIVE
    assert execution.result.selected_candidate_ref is None
    assert execution.result.eligible_candidates == 0
    assert execution.result.reason_codes == (OptimizationReasonCode.NO_ELIGIBLE_CANDIDATE,)


def test_true_tie_uses_lexicographically_lower_candidate_id(tmp_path: Path) -> None:
    space = OptimizationSearchSpace(
        ArtifactId("deterministic-tie-search-space"),
        V1,
        (
            OptimizationParameter(
                OptimizationParameterName.THRESHOLD_BPS,
                OptimizationParameterType.INTEGER,
                0,
                50,
                50,
                0,
            ),
        ),
        V1,
    )
    *_, execution, _ = _selection_case(tmp_path, space)
    assert execution.result.eligible_candidates == 2
    first, second = execution.candidate_results
    assert (first.total_return, first.max_drawdown, first.trade_count) == (
        second.total_return,
        second.max_drawdown,
        second.trade_count,
    )
    assert execution.result.selected_candidate_ref is not None
    assert str(execution.result.selected_candidate_ref.object_id) == min(
        str(first.candidate_id), str(second.candidate_id)
    )


def test_candidate_derivation_changes_only_declared_strategy_parameter(
    selection_bundle: tuple[Any, ...],
) -> None:
    source, _, _, candidates, execution, _ = selection_bundle
    for definition, candidate in zip(execution.candidate_definitions, candidates, strict=True):
        restored = replace(
            candidate.strategy,
            strategy_id=source.strategy.strategy_id,
            threshold_bps=source.strategy.threshold_bps,
        )
        assert restored == source.strategy
        assert (
            candidate.specification.normalized_manifest_ref
            == source.specification.normalized_manifest_ref
        )
        assert (
            candidate.specification.normalized_lock_ref == source.specification.normalized_lock_ref
        )
        assert (
            candidate.specification.engine_contract_ref == source.specification.engine_contract_ref
        )
        assert candidate.specification.commission_bps == source.specification.commission_bps
        assert candidate.specification.slippage_bps == source.specification.slippage_bps
        assert definition.candidate_strategy_ref.expected_fingerprint == fingerprint_record(
            candidate.strategy
        )


def test_multiple_candidates_without_bonferroni_are_inconclusive(
    selection_bundle: tuple[Any, ...],
) -> None:
    source, space, original, _, _, repository = selection_bundle
    plan = replace(
        original,
        optimization_plan_id=ArtifactId("single-policy-multiple-candidates"),
        multiplicity_policy=OptimizationMultiplicityPolicy.SINGLE_CANDIDATE,
    )
    # Candidate confidence is not corrected under the blocked policy.
    blocked_candidates = tuple(
        _candidate_evidence_with_repository(
            source,
            repository,
            plan,
            space,
            parameters,
            2,
        )
        for parameters in enumerate_parameter_sets(space, plan.maximum_trials)
    )
    result = run_optimization_selection(
        _request(plan),
        plan=plan,
        search_space=space,
        source=source,
        candidates=blocked_candidates,
        repository=repository,
    )
    assert result.result.decision is SelectionDecision.INCONCLUSIVE
    assert result.result.corrected_alpha is None
    assert result.result.reason_codes == (
        OptimizationReasonCode.MULTIPLE_CANDIDATES_REQUIRE_BONFERRONI,
    )


def test_lineage_rejects_tampered_candidate_and_trial(
    selection_bundle: tuple[Any, ...],
) -> None:
    source, space, plan, candidates, execution, _ = selection_bundle
    request = _request(plan)
    changed_result = replace(execution.candidate_results[0], total_return="999")
    with pytest.raises(OptimizationLineageMismatch):
        verify_optimization_selection_lineage(
            record=execution.record,
            result=execution.result,
            candidate_definitions=execution.candidate_definitions,
            candidate_results=(changed_result, *execution.candidate_results[1:]),
            trials=execution.trials,
            request=request,
            plan=plan,
            search_space=space,
            source=source,
            candidates=candidates,
        )
    changed_trial = replace(execution.trials[0], trial_index=99)
    with pytest.raises(OptimizationLineageMismatch):
        verify_optimization_selection_lineage(
            record=execution.record,
            result=execution.result,
            candidate_definitions=execution.candidate_definitions,
            candidate_results=execution.candidate_results,
            trials=(changed_trial, *execution.trials[1:]),
            request=request,
            plan=plan,
            search_space=space,
            source=source,
            candidates=candidates,
        )


@pytest.mark.parametrize(
    ("field", "value"),
    (
        ("decision", SelectionDecision.INCONCLUSIVE),
        ("corrected_alpha", "0.05"),
        ("multiplicity_policy", OptimizationMultiplicityPolicy.SINGLE_CANDIDATE),
        ("eligible_candidates", 0),
        ("reason_codes", (OptimizationReasonCode.NO_ELIGIBLE_CANDIDATE,)),
        (
            "selection_authority_ref",
            TraceabilityRef(AuthorityBindingId("wrong-authority"), V1, "sha256:" + "1" * 64),
        ),
    ),
)
def test_selection_summary_tamper_fails_exact_verification(
    selection_bundle: tuple[Any, ...], field: str, value: object
) -> None:
    source, space, plan, candidates, execution, _ = selection_bundle
    with pytest.raises(OptimizationLineageMismatch):
        verify_optimization_selection_lineage(
            record=execution.record,
            result=_unsafe(execution.result, **{field: value}),
            candidate_definitions=execution.candidate_definitions,
            candidate_results=execution.candidate_results,
            trials=execution.trials,
            request=_request(plan),
            plan=plan,
            search_space=space,
            source=source,
            candidates=candidates,
        )


def test_tampered_candidate_robustness_evidence_fails_before_selection(
    selection_bundle: tuple[Any, ...],
) -> None:
    source, space, plan, candidates, _, repository = selection_bundle
    changed = replace(
        candidates[0],
        robustness_result=_unsafe(
            candidates[0].robustness_result,
            decision=RobustnessDecision.FAIL,
        ),
    )
    with pytest.raises(
        OptimizationInputInvalid,
        match="failed exact robustness and source-lineage verification",
    ):
        run_optimization_selection(
            _request(plan),
            plan=plan,
            search_space=space,
            source=source,
            candidates=(changed, candidates[1]),
            repository=repository,
        )


def test_bonferroni_candidate_cannot_claim_single_test_semantics(
    selection_bundle: tuple[Any, ...],
) -> None:
    source, space, plan, candidates, execution, _ = selection_bundle
    changed_plan = replace(
        candidates[0].validation_plan,
        multiplicity_policy=MultiplicityPolicy.SINGLE_PREDECLARED_TEST,
    )
    changed = replace(candidates[0], validation_plan=changed_plan)
    with pytest.raises(
        OptimizationLineageMismatch,
        match="candidate validation plan changed undeclared policy",
    ):
        verify_optimization_selection_lineage(
            record=execution.record,
            result=execution.result,
            candidate_definitions=execution.candidate_definitions,
            candidate_results=execution.candidate_results,
            trials=execution.trials,
            request=_request(plan),
            plan=plan,
            search_space=space,
            source=source,
            candidates=(changed, candidates[1]),
        )


def test_wrong_selection_authority_fails_closed(selection_bundle: tuple[Any, ...]) -> None:
    source, space, plan, candidates, _, repository = selection_bundle
    request = replace(
        _request(plan),
        selection_authority_ref=TraceabilityRef(
            AuthorityBindingId("unverified-selection-actor"), V1, "sha256:" + "2" * 64
        ),
    )
    with pytest.raises(ValueError, match="lacks exact selection authority"):
        run_optimization_selection(
            request,
            plan=plan,
            search_space=space,
            source=source,
            candidates=candidates,
            repository=repository,
        )


def test_parent_evidence_cannot_substitute_for_candidate_evidence(
    selection_bundle: tuple[Any, ...],
) -> None:
    source, space, plan, candidates, _, repository = selection_bundle
    with pytest.raises(
        OptimizationLineageMismatch,
        match="candidate strategy is not the exact governed derivation",
    ):
        run_optimization_selection(
            _request(plan),
            plan=plan,
            search_space=space,
            source=source,
            candidates=(source, candidates[1]),
            repository=repository,
        )


def test_persistence_roundtrip_idempotency_and_corruption(
    selection_bundle: tuple[Any, ...],
) -> None:
    _, space, plan, _, execution, repository = selection_bundle
    records = (
        space,
        plan,
        execution.candidate_definitions[0],
        execution.candidate_results[0],
        execution.trials[0],
        execution.result,
        execution.record,
    )
    for record in records:
        key = repository_key(record)
        assert repository.load(key, type(record)).record == record
        assert repository.store(record).status is RepositoryWriteStatus.ALREADY_PRESENT_IDENTICAL
        assert decode(encode(record), type(record)) == record
    with pytest.raises(RepositoryTypeMismatch):
        repository.load(repository_key(execution.result), OptimizationRunRecord)
    path = repository.path_for(repository_key(execution.result))
    path.write_bytes(path.read_bytes().replace(b'"SELECTED"', b'"REJECTED"', 1))
    with pytest.raises(RepositoryIntegrityFailure):
        repository.load(repository_key(execution.result), OptimizationSelectionResult)
    payload = json.loads(encode(space))
    payload["payload"]["unexpected"] = True
    with pytest.raises(InvalidSerialization):
        decode(json.dumps(payload).encode(), OptimizationSearchSpace)
    with pytest.raises(OptimizationContractError):
        replace(space, version=ObjectVersion(2))


def test_deterministic_rerun_and_tie_break_order(
    selection_bundle: tuple[Any, ...],
) -> None:
    source, space, plan, candidates, first, repository = selection_bundle
    second = run_optimization_selection(
        _request(plan),
        plan=plan,
        search_space=space,
        source=source,
        candidates=candidates,
        repository=repository,
    )
    assert encode(first.result) == encode(second.result)
    assert encode(first.record) == encode(second.record)
    assert first.result.tie_break_order == (
        "TOTAL_RETURN_DESC",
        "MAX_DRAWDOWN_ASC",
        "TRADE_COUNT_DESC",
        "CANDIDATE_ID_ASC",
    )


def test_optimization_golden_is_pinned(selection_bundle: tuple[Any, ...]) -> None:
    _, space, plan, _, execution, _ = selection_bundle
    expected = {
        "format": "optimization-selection-v1",
        "search_space_fingerprint": fingerprint_record(space),
        "optimization_plan_fingerprint": fingerprint_record(plan),
        "candidate_count": len(execution.candidate_definitions),
        "candidate_ids": [str(item.candidate_id) for item in execution.candidate_definitions],
        "trial_count": len(execution.trials),
        "multiplicity_policy": execution.result.multiplicity_policy.value,
        "corrected_alpha": execution.result.corrected_alpha,
        "selected_candidate_ref": (
            None
            if execution.result.selected_candidate_ref is None
            else str(execution.result.selected_candidate_ref.object_id)
        ),
        "selection_decision": execution.result.decision.value,
        "reason_codes": [item.value for item in execution.result.reason_codes],
        "selection_result_fingerprint": fingerprint_record(execution.result),
    }
    assert json.loads(GOLDEN.read_text(encoding="utf-8")) == expected


def test_capability_isolation_and_execution_remains_closed() -> None:
    tree = ast.parse(inspect.getsource(optimization_module))
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
        {"ccxt", "httpx", "importlib", "optuna", "requests", "socket", "subprocess", "urllib"}
    )
    calls = {
        node.func.id
        for node in ast.walk(tree)
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
    }
    assert not calls.intersection({"eval", "exec"})
    assert EXE_01.state is ExecutionState.PLANNED_CLOSED
    assert DeploymentAuthorizationStatus.NOT_AUTHORIZED.value == "NOT_AUTHORIZED"
