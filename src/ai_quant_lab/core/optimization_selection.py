"""Deterministic grid-search evidence and fail-closed selection for Sprint 16."""

from __future__ import annotations

from dataclasses import dataclass, replace
from decimal import ROUND_HALF_EVEN, Context, Decimal, localcontext
from itertools import product

from ai_quant_lab.core.csv_import import CsvImportReport
from ai_quant_lab.core.data import InstrumentIdentity
from ai_quant_lab.core.dataset_store import LocalDatasetRepository, RepositoryWriteResult
from ai_quant_lab.core.experiment_contracts import (
    ExperimentAuthorizationPolicy,
    ExperimentAuthorizationRecord,
    ExperimentSpecification,
)
from ai_quant_lab.core.experiment_runner_contracts import ExperimentReplayContract
from ai_quant_lab.core.integrity import fingerprint_record
from ai_quant_lab.core.model import (
    ArtifactId,
    ExecutionState,
    ExperimentId,
    ObjectVersion,
    TraceabilityRef,
    TrialId,
    fingerprint,
)
from ai_quant_lab.core.optimization_contracts import (
    CandidateEligibility,
    OptimizationCandidateDefinition,
    OptimizationCandidateResult,
    OptimizationMultiplicityPolicy,
    OptimizationPlan,
    OptimizationReasonCode,
    OptimizationRequest,
    OptimizationRunRecord,
    OptimizationRunStatus,
    OptimizationSearchSpace,
    OptimizationSelectionResult,
    OptimizationTrialRecord,
    OptimizationTrialStatus,
    SelectionDecision,
)
from ai_quant_lab.core.real_csv_contracts import RealCsvAdmissionRecord, RealCsvSourceDeclaration
from ai_quant_lab.core.research_eligibility_contracts import (
    DeploymentAuthorizationStatus,
    ResearchDatasetEligibilityPolicy,
    ResearchDatasetEligibilityRecord,
)
from ai_quant_lab.core.robustness_validation import verify_robustness_validation_lineage
from ai_quant_lab.core.robustness_validation_contracts import (
    RobustnessDecision,
    RobustnessValidationPlan,
    RobustnessValidationRequest,
    RobustnessValidationResult,
    RobustnessValidationRunRecord,
)
from ai_quant_lab.core.scientific_validation_contracts import (
    ScientificValidationDecision,
    ScientificValidationResult,
    ValidationPlan,
    ValidationRequest,
    ValidationRunRecord,
)
from ai_quant_lab.core.strategy_backtest import StrategyBacktestRunRequest
from ai_quant_lab.core.strategy_backtest_contracts import (
    BacktestResultArtifact,
    BacktestRunRecord,
    StrategyDefinition,
)


class OptimizationSelectionError(ValueError):
    pass


class OptimizationInputInvalid(OptimizationSelectionError):
    pass


class OptimizationAuthorityInvalid(OptimizationSelectionError):
    pass


class OptimizationLineageMismatch(OptimizationSelectionError):
    pass


_V1 = ObjectVersion(1)
_DECIMAL_CONTEXT = Context(prec=34, rounding=ROUND_HALF_EVEN)
_TIE_BREAK = (
    "TOTAL_RETURN_DESC",
    "MAX_DRAWDOWN_ASC",
    "TRADE_COUNT_DESC",
    "CANDIDATE_ID_ASC",
)


@dataclass(frozen=True, slots=True)
class OptimizationEvidence:
    """Exact runtime bundle; persisted refs remain authoritative, not this container."""

    robustness_request: RobustnessValidationRequest
    robustness_plan: RobustnessValidationPlan
    robustness_record: RobustnessValidationRunRecord
    robustness_result: RobustnessValidationResult
    scientific_request: ValidationRequest
    validation_plan: ValidationPlan
    validation_record: ValidationRunRecord
    scientific_result: ScientificValidationResult
    backtest_request: StrategyBacktestRunRequest
    backtest_record: BacktestRunRecord
    backtest_artifact: BacktestResultArtifact
    authorization: ExperimentAuthorizationRecord
    specification: ExperimentSpecification
    authorization_policy: ExperimentAuthorizationPolicy
    eligibility: ResearchDatasetEligibilityRecord
    eligibility_policy: ResearchDatasetEligibilityPolicy
    admission: RealCsvAdmissionRecord
    declaration: RealCsvSourceDeclaration
    engine_contract: ExperimentReplayContract
    strategy: StrategyDefinition
    instrument: InstrumentIdentity
    report: CsvImportReport


@dataclass(frozen=True, slots=True)
class OptimizationSelectionExecutionResult:
    record: OptimizationRunRecord
    result: OptimizationSelectionResult
    candidate_definitions: tuple[OptimizationCandidateDefinition, ...]
    candidate_results: tuple[OptimizationCandidateResult, ...]
    trials: tuple[OptimizationTrialRecord, ...]
    writes: tuple[RepositoryWriteResult, ...]


def _exact(record: object, object_id: object, version: ObjectVersion) -> TraceabilityRef:
    return TraceabilityRef(object_id, version, fingerprint_record(record))  # type: ignore[arg-type]


def _decimal(value: Decimal) -> str:
    if not value.is_finite():
        raise OptimizationInputInvalid("optimization produced a non-finite decimal")
    if value == 0:
        return "0"
    text = format(value, "f")
    return text.rstrip("0").rstrip(".") if "." in text else text


def _reasons(*values: OptimizationReasonCode) -> tuple[OptimizationReasonCode, ...]:
    return tuple(sorted(set(values), key=lambda item: item.value))


def enumerate_parameter_sets(
    search_space: OptimizationSearchSpace,
    maximum_trials: int,
) -> tuple[tuple[tuple[str, int], ...], ...]:
    """Enumerate the declared closed grid in canonical parameter/product order."""
    if (
        isinstance(maximum_trials, bool)
        or not isinstance(maximum_trials, int)
        or maximum_trials < 1
    ):
        raise OptimizationInputInvalid("maximum_trials must be a positive integer")
    names = tuple(item.name.value for item in search_space.parameters)
    grids = tuple(
        tuple(range(item.lower_bound, item.upper_bound + 1, item.step))
        for item in search_space.parameters
    )
    values = tuple(tuple(zip(names, combination, strict=True)) for combination in product(*grids))
    return values[:maximum_trials]


def corrected_alpha(plan: OptimizationPlan, candidate_count: int) -> str | None:
    if candidate_count < 1:
        raise OptimizationInputInvalid("candidate count must be positive")
    alpha = Decimal(plan.declared_alpha)
    if plan.multiplicity_policy is OptimizationMultiplicityPolicy.BONFERRONI:
        with localcontext(_DECIMAL_CONTEXT):
            return _decimal(alpha / Decimal(candidate_count))
    if (
        plan.multiplicity_policy is OptimizationMultiplicityPolicy.SINGLE_CANDIDATE
        and candidate_count == 1
    ):
        return _decimal(alpha)
    return None


def corrected_confidence(alpha: str) -> str:
    with localcontext(_DECIMAL_CONTEXT):
        return _decimal(Decimal(1) - Decimal(alpha))


def _candidate_suffix(
    *,
    plan: OptimizationPlan,
    search_space: OptimizationSearchSpace,
    parent_strategy: StrategyDefinition,
    source: OptimizationEvidence,
    parameters: tuple[tuple[str, int], ...],
) -> str:
    identity = fingerprint(
        {
            "optimization_plan_fingerprint": fingerprint_record(plan),
            "search_space_fingerprint": fingerprint_record(search_space),
            "parent_strategy_fingerprint": fingerprint_record(parent_strategy),
            "dataset_manifest_ref": plan.normalized_manifest_ref,
            "dataset_lock_ref": plan.normalized_lock_ref,
            "source_experiment_fingerprint": fingerprint_record(source.specification),
            "parameters": parameters,
        }
    )
    return identity.removeprefix("sha256:")[:20]


def derive_candidate(
    *,
    plan: OptimizationPlan,
    search_space: OptimizationSearchSpace,
    parent_strategy: StrategyDefinition,
    source: OptimizationEvidence,
    parameters: tuple[tuple[str, int], ...],
) -> tuple[OptimizationCandidateDefinition, StrategyDefinition]:
    suffix = _candidate_suffix(
        plan=plan,
        search_space=search_space,
        parent_strategy=parent_strategy,
        source=source,
        parameters=parameters,
    )
    values = dict(parameters)
    strategy = replace(
        parent_strategy,
        strategy_id=ArtifactId(f"optimized-strategy-{suffix}"),
        threshold_bps=values["threshold_bps"],
    )
    definition = OptimizationCandidateDefinition(
        ArtifactId(f"optimization-candidate-{suffix}"),
        _V1,
        _exact(plan, plan.optimization_plan_id, plan.version),
        _exact(parent_strategy, parent_strategy.strategy_id, parent_strategy.version),
        parameters,
        _exact(strategy, strategy.strategy_id, strategy.version),
        _V1,
    )
    return definition, strategy


def _verify_evidence(evidence: OptimizationEvidence) -> None:
    try:
        verify_robustness_validation_lineage(
            record=evidence.robustness_record,
            result=evidence.robustness_result,
            request=evidence.robustness_request,
            plan=evidence.robustness_plan,
            scientific_result=evidence.scientific_result,
            validation_record=evidence.validation_record,
            scientific_request=evidence.scientific_request,
            validation_plan=evidence.validation_plan,
            backtest_artifact=evidence.backtest_artifact,
            backtest_record=evidence.backtest_record,
            backtest_request=evidence.backtest_request,
            authorization=evidence.authorization,
            specification=evidence.specification,
            policy=evidence.authorization_policy,
            eligibility=evidence.eligibility,
            eligibility_policy=evidence.eligibility_policy,
            admission=evidence.admission,
            declaration=evidence.declaration,
            engine_contract=evidence.engine_contract,
            strategy=evidence.strategy,
            instrument=evidence.instrument,
            report=evidence.report,
        )
    except ValueError as exc:
        raise OptimizationInputInvalid(
            "optimization evidence failed exact robustness and source-lineage verification"
        ) from exc


def _verify_plan_source(
    request: OptimizationRequest,
    *,
    plan: OptimizationPlan,
    search_space: OptimizationSearchSpace,
    source: OptimizationEvidence,
) -> None:
    if request.optimization_plan_ref != _exact(plan, plan.optimization_plan_id, plan.version):
        raise OptimizationLineageMismatch("optimization request does not bind exact plan")
    if request.selection_authority_ref != plan.selection_authority_ref:
        raise OptimizationAuthorityInvalid("optimization request lacks exact selection authority")
    expected = (
        _exact(search_space, search_space.search_space_id, search_space.version),
        _exact(source.strategy, source.strategy.strategy_id, source.strategy.version),
        _exact(
            source.specification, source.specification.experiment_id, source.specification.version
        ),
        _exact(
            source.robustness_result,
            source.robustness_result.robustness_result_id,
            source.robustness_result.version,
        ),
        source.specification.normalized_manifest_ref,
        source.specification.normalized_lock_ref,
        source.specification.engine_contract_ref,
        _exact(
            source.validation_plan,
            source.validation_plan.validation_plan_id,
            source.validation_plan.version,
        ),
        _exact(
            source.robustness_plan,
            source.robustness_plan.robustness_plan_id,
            source.robustness_plan.version,
        ),
    )
    actual = (
        plan.search_space_ref,
        plan.parent_strategy_ref,
        plan.source_experiment_ref,
        plan.source_robustness_result_ref,
        plan.normalized_manifest_ref,
        plan.normalized_lock_ref,
        plan.engine_contract_ref,
        plan.validation_plan_ref,
        plan.robustness_plan_ref,
    )
    if actual != expected:
        raise OptimizationLineageMismatch("optimization plan does not bind exact source lineage")
    _verify_evidence(source)


def _expected_candidate_specification(
    source: OptimizationEvidence,
    strategy: StrategyDefinition,
    suffix: str,
) -> ExperimentSpecification:
    configuration = dict(source.specification.configuration)
    required = {
        "capital_currency",
        "capital_minor_unit_scale",
        "fixed_notional_minor",
        "strategy_fingerprint",
        "strategy_id",
        "strategy_model",
    }
    if not required.issubset(configuration):
        raise OptimizationInputInvalid("source experiment lacks governed strategy configuration")
    configuration.update(
        {
            "capital_currency": strategy.capital_currency,
            "capital_minor_unit_scale": str(strategy.capital_minor_unit_scale),
            "fixed_notional_minor": str(strategy.fixed_notional_minor),
            "strategy_fingerprint": fingerprint_record(strategy),
            "strategy_id": str(strategy.strategy_id),
            "strategy_model": strategy.model.value,
        }
    )
    return replace(
        source.specification,
        experiment_id=ExperimentId(f"optimization-experiment-{suffix}"),
        configuration=tuple(sorted(configuration.items())),
    )


def _verify_candidate_invariants(
    *,
    plan: OptimizationPlan,
    source: OptimizationEvidence,
    definition: OptimizationCandidateDefinition,
    expected_strategy: StrategyDefinition,
    evidence: OptimizationEvidence,
    corrected: str | None,
) -> None:
    if evidence.strategy != expected_strategy:
        raise OptimizationLineageMismatch("candidate strategy is not the exact governed derivation")
    suffix = str(definition.candidate_id).removeprefix("artifact:optimization-candidate-")
    expected_specification = _expected_candidate_specification(source, expected_strategy, suffix)
    if evidence.specification != expected_specification:
        raise OptimizationLineageMismatch("candidate experiment changed undeclared inputs")
    if (
        evidence.instrument != source.instrument
        or evidence.eligibility != source.eligibility
        or evidence.eligibility_policy != source.eligibility_policy
        or evidence.admission != source.admission
        or evidence.declaration != source.declaration
        or evidence.engine_contract != source.engine_contract
        or evidence.authorization_policy != source.authorization_policy
    ):
        raise OptimizationLineageMismatch("candidate changed shared dataset or engine lineage")
    expected_validation = replace(
        source.validation_plan,
        validation_plan_id=evidence.validation_plan.validation_plan_id,
        confidence_level=(
            corrected_confidence(corrected)
            if corrected is not None
            else source.validation_plan.confidence_level
        ),
    )
    if evidence.validation_plan != expected_validation:
        raise OptimizationLineageMismatch("candidate validation plan changed undeclared policy")
    expected_robustness = replace(
        source.robustness_plan,
        robustness_plan_id=evidence.robustness_plan.robustness_plan_id,
        source_scientific_validation_ref=_exact(
            evidence.scientific_result,
            evidence.scientific_result.validation_result_id,
            evidence.scientific_result.version,
        ),
    )
    if evidence.robustness_plan != expected_robustness:
        raise OptimizationLineageMismatch("candidate robustness plan changed undeclared policy")
    if (
        evidence.backtest_artifact.strategy_ref != definition.candidate_strategy_ref
        or evidence.scientific_result.strategy_ref != definition.candidate_strategy_ref
        or evidence.robustness_result.strategy_ref != definition.candidate_strategy_ref
    ):
        raise OptimizationLineageMismatch("candidate evidence does not bind exact strategy")
    if (
        evidence.specification.normalized_manifest_ref != plan.normalized_manifest_ref
        or evidence.specification.normalized_lock_ref != plan.normalized_lock_ref
        or evidence.specification.engine_contract_ref != plan.engine_contract_ref
    ):
        raise OptimizationLineageMismatch("candidate changed dataset or engine refs")
    _verify_evidence(evidence)


def _candidate_result(
    *,
    plan: OptimizationPlan,
    definition: OptimizationCandidateDefinition,
    evidence: OptimizationEvidence,
) -> OptimizationCandidateResult:
    reasons: list[OptimizationReasonCode] = []
    if evidence.scientific_result.decision is not ScientificValidationDecision.PASS:
        reasons.append(OptimizationReasonCode.SCIENTIFIC_VALIDATION_NOT_PASS)
    if evidence.robustness_result.decision is not RobustnessDecision.PASS:
        reasons.append(OptimizationReasonCode.ROBUSTNESS_NOT_PASS)
    if evidence.backtest_artifact.trade_count < plan.minimum_trade_count:
        reasons.append(OptimizationReasonCode.INSUFFICIENT_TRADES)
    if Decimal(evidence.backtest_artifact.max_drawdown) > Decimal(plan.maximum_drawdown):
        reasons.append(OptimizationReasonCode.DRAWDOWN_CEILING_EXCEEDED)
    eligibility = CandidateEligibility.REJECTED if reasons else CandidateEligibility.ELIGIBLE
    if not reasons:
        reasons.append(OptimizationReasonCode.ALL_CONSTRAINTS_PASSED)
    return OptimizationCandidateResult(
        definition.candidate_id,
        _V1,
        _exact(definition, definition.candidate_id, definition.version),
        definition.candidate_strategy_ref,
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
        evidence.backtest_artifact.total_return,
        evidence.backtest_artifact.max_drawdown,
        evidence.backtest_artifact.trade_count,
        eligibility,
        _reasons(*reasons),
        _V1,
    )


def _input_fingerprint(
    *,
    plan: OptimizationPlan,
    search_space: OptimizationSearchSpace,
    source: OptimizationEvidence,
    definitions: tuple[OptimizationCandidateDefinition, ...],
    results: tuple[OptimizationCandidateResult, ...],
) -> str:
    return fingerprint(
        {
            "optimization_plan_fingerprint": fingerprint_record(plan),
            "search_space_fingerprint": fingerprint_record(search_space),
            "parent_strategy_fingerprint": fingerprint_record(source.strategy),
            "source_experiment_fingerprint": fingerprint_record(source.specification),
            "source_robustness_fingerprint": fingerprint_record(source.robustness_result),
            "instrument_fingerprint": fingerprint_record(source.instrument),
            "normalized_manifest_ref": plan.normalized_manifest_ref,
            "normalized_lock_ref": plan.normalized_lock_ref,
            "engine_contract_ref": plan.engine_contract_ref,
            "multiplicity_policy": plan.multiplicity_policy,
            "maximum_trials": plan.maximum_trials,
            "candidate_enumeration": tuple(item.parameter_values for item in definitions),
            "candidate_definition_fingerprints": tuple(
                fingerprint_record(item) for item in definitions
            ),
            "candidate_result_fingerprints": tuple(fingerprint_record(item) for item in results),
        }
    )


def _build(
    request: OptimizationRequest,
    *,
    plan: OptimizationPlan,
    search_space: OptimizationSearchSpace,
    source: OptimizationEvidence,
    candidates: tuple[OptimizationEvidence, ...],
) -> tuple[
    OptimizationRunRecord,
    OptimizationSelectionResult,
    tuple[OptimizationCandidateDefinition, ...],
    tuple[OptimizationCandidateResult, ...],
    tuple[OptimizationTrialRecord, ...],
]:
    _verify_plan_source(request, plan=plan, search_space=search_space, source=source)
    parameter_sets = enumerate_parameter_sets(search_space, plan.maximum_trials)
    if len(candidates) != len(parameter_sets):
        raise OptimizationInputInvalid("candidate evidence count must equal bounded grid count")
    corrected = corrected_alpha(plan, len(parameter_sets))
    definitions: list[OptimizationCandidateDefinition] = []
    results: list[OptimizationCandidateResult] = []
    trials: list[OptimizationTrialRecord] = []
    for index, (parameters, evidence) in enumerate(zip(parameter_sets, candidates, strict=True)):
        definition, expected_strategy = derive_candidate(
            plan=plan,
            search_space=search_space,
            parent_strategy=source.strategy,
            source=source,
            parameters=parameters,
        )
        _verify_candidate_invariants(
            plan=plan,
            source=source,
            definition=definition,
            expected_strategy=expected_strategy,
            evidence=evidence,
            corrected=corrected,
        )
        result = _candidate_result(plan=plan, definition=definition, evidence=evidence)
        trial = OptimizationTrialRecord(
            TrialId(f"optimization-trial-{index:04d}"),
            _V1,
            request.optimization_plan_ref,
            index,
            _exact(definition, definition.candidate_id, definition.version),
            _exact(result, result.candidate_id, result.version),
            (
                OptimizationTrialStatus.COMPLETED
                if result.eligibility is CandidateEligibility.ELIGIBLE
                else OptimizationTrialStatus.REJECTED
            ),
            result.reason_codes,
            _V1,
        )
        definitions.append(definition)
        results.append(result)
        trials.append(trial)
    eligible = [item for item in results if item.eligibility is CandidateEligibility.ELIGIBLE]
    if corrected is None:
        selected = None
        decision = SelectionDecision.INCONCLUSIVE
        reason = (
            OptimizationReasonCode.MULTIPLE_CANDIDATES_REQUIRE_BONFERRONI
            if plan.multiplicity_policy is OptimizationMultiplicityPolicy.SINGLE_CANDIDATE
            else OptimizationReasonCode.UNSUPPORTED_MULTIPLICITY
        )
    elif not eligible:
        selected = None
        decision = SelectionDecision.INCONCLUSIVE
        reason = OptimizationReasonCode.NO_ELIGIBLE_CANDIDATE
    else:
        selected = min(
            eligible,
            key=lambda item: (
                -Decimal(item.total_return),
                Decimal(item.max_drawdown),
                -item.trade_count,
                str(item.candidate_id),
            ),
        )
        decision = SelectionDecision.SELECTED
        reason = OptimizationReasonCode.SELECTED_BY_DECLARED_ORDER
    candidate_results = tuple(results)
    trial_records = tuple(trials)
    selection = OptimizationSelectionResult(
        request.selection_result_id,
        _V1,
        request.optimization_plan_ref,
        tuple(_exact(item, item.candidate_id, item.version) for item in candidate_results),
        tuple(_exact(item, item.trial_id, item.version) for item in trial_records),
        len(trial_records),
        len(candidate_results),
        len(eligible),
        None if selected is None else _exact(selected, selected.candidate_id, selected.version),
        decision,
        plan.multiplicity_policy,
        corrected,
        _TIE_BREAK,
        _reasons(reason),
        request.selection_authority_ref,
        request.provenance_ref,
        DeploymentAuthorizationStatus.NOT_AUTHORIZED,
        ExecutionState.PLANNED_CLOSED,
        _V1,
    )
    candidate_definitions = tuple(definitions)
    input_fingerprint = _input_fingerprint(
        plan=plan,
        search_space=search_space,
        source=source,
        definitions=candidate_definitions,
        results=candidate_results,
    )
    record = OptimizationRunRecord(
        request.optimization_run_id,
        _V1,
        request.optimization_plan_ref,
        input_fingerprint,
        len(parameter_sets),
        len(trial_records),
        len(candidate_results),
        _exact(selection, selection.selection_result_id, selection.version),
        request.selection_authority_ref,
        request.provenance_ref,
        OptimizationRunStatus.COMPLETED,
        DeploymentAuthorizationStatus.NOT_AUTHORIZED,
        ExecutionState.PLANNED_CLOSED,
        _V1,
    )
    return record, selection, candidate_definitions, candidate_results, trial_records


def run_optimization_selection(
    request: OptimizationRequest,
    *,
    plan: OptimizationPlan,
    search_space: OptimizationSearchSpace,
    source: OptimizationEvidence,
    candidates: tuple[OptimizationEvidence, ...],
    repository: LocalDatasetRepository,
) -> OptimizationSelectionExecutionResult:
    record, result, definitions, candidate_results, trials = _build(
        request,
        plan=plan,
        search_space=search_space,
        source=source,
        candidates=candidates,
    )
    verify_optimization_selection_lineage(
        record=record,
        result=result,
        candidate_definitions=definitions,
        candidate_results=candidate_results,
        trials=trials,
        request=request,
        plan=plan,
        search_space=search_space,
        source=source,
        candidates=candidates,
    )
    records: tuple[object, ...] = (
        search_space,
        plan,
        *definitions,
        *(item.strategy for item in candidates),
        *candidate_results,
        *trials,
        result,
        record,
    )
    writes = tuple(repository.store(item) for item in records)  # type: ignore[arg-type]
    return OptimizationSelectionExecutionResult(
        record, result, definitions, candidate_results, trials, writes
    )


def verify_optimization_selection_lineage(
    *,
    record: OptimizationRunRecord,
    result: OptimizationSelectionResult,
    candidate_definitions: tuple[OptimizationCandidateDefinition, ...],
    candidate_results: tuple[OptimizationCandidateResult, ...],
    trials: tuple[OptimizationTrialRecord, ...],
    request: OptimizationRequest,
    plan: OptimizationPlan,
    search_space: OptimizationSearchSpace,
    source: OptimizationEvidence,
    candidates: tuple[OptimizationEvidence, ...],
) -> None:
    expected = _build(
        request,
        plan=plan,
        search_space=search_space,
        source=source,
        candidates=candidates,
    )
    if (
        record != expected[0]
        or result != expected[1]
        or candidate_definitions != expected[2]
        or candidate_results != expected[3]
        or trials != expected[4]
    ):
        raise OptimizationLineageMismatch(
            "optimization selection lineage is not exact and deterministic"
        )
