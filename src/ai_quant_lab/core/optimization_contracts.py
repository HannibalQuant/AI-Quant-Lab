"""Immutable contracts for bounded Sprint 16 optimization and selection governance."""

from __future__ import annotations

import re
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
from enum import StrEnum

from ai_quant_lab.core.data import DatasetLockId
from ai_quant_lab.core.model import (
    ArtifactId,
    AuthorityBindingId,
    DatasetId,
    ExecutionState,
    ExperimentId,
    ObjectVersion,
    ProvenanceId,
    RunId,
    TraceabilityRef,
    TrialId,
    ValidationId,
)
from ai_quant_lab.core.research_eligibility_contracts import DeploymentAuthorizationStatus


class OptimizationContractError(ValueError):
    pass


class OptimizationParameterType(StrEnum):
    INTEGER = "INTEGER"


class OptimizationParameterName(StrEnum):
    ADX_LENGTH = "adx_length"
    ADX_THRESHOLD_X100 = "adx_threshold_x100"
    ATR_LENGTH = "atr_length"
    ATR_STOP_MULT_X100 = "atr_stop_mult_x100"
    BREAK_EVEN_TRIGGER_R_X100 = "break_even_trigger_r_x100"
    FAST_EMA = "fast_ema"
    MACD_FAST = "macd_fast"
    MACD_SIGNAL = "macd_signal"
    MACD_SLOW = "macd_slow"
    MEDIUM_EMA = "medium_ema"
    RSI_LENGTH = "rsi_length"
    RSI_LONG_MIN_X100 = "rsi_long_min_x100"
    RSI_SHORT_MAX_X100 = "rsi_short_max_x100"
    SLOW_EMA = "slow_ema"
    TAKE_PROFIT_R_X100 = "take_profit_r_x100"
    THRESHOLD_BPS = "threshold_bps"
    TIME_STOP_BARS = "time_stop_bars"


class OptimizationSearchMethod(StrEnum):
    GRID_SEARCH = "GRID_SEARCH"


class OptimizationObjective(StrEnum):
    ROBUSTNESS_AWARE_TOTAL_RETURN = "ROBUSTNESS_AWARE_TOTAL_RETURN"


class OptimizationMultiplicityPolicy(StrEnum):
    BONFERRONI = "BONFERRONI"
    SINGLE_CANDIDATE = "SINGLE_CANDIDATE"
    UNSUPPORTED = "UNSUPPORTED"


class CandidateEligibility(StrEnum):
    ELIGIBLE = "ELIGIBLE"
    REJECTED = "REJECTED"


class OptimizationReasonCode(StrEnum):
    ALL_CONSTRAINTS_PASSED = "ALL_CONSTRAINTS_PASSED"
    DRAWDOWN_CEILING_EXCEEDED = "DRAWDOWN_CEILING_EXCEEDED"
    INSUFFICIENT_TRADES = "INSUFFICIENT_TRADES"
    MULTIPLE_CANDIDATES_REQUIRE_BONFERRONI = "MULTIPLE_CANDIDATES_REQUIRE_BONFERRONI"
    NO_ELIGIBLE_CANDIDATE = "NO_ELIGIBLE_CANDIDATE"
    ROBUSTNESS_NOT_PASS = "ROBUSTNESS_NOT_PASS"
    SCIENTIFIC_VALIDATION_NOT_PASS = "SCIENTIFIC_VALIDATION_NOT_PASS"
    SELECTED_BY_DECLARED_ORDER = "SELECTED_BY_DECLARED_ORDER"
    UNSUPPORTED_MULTIPLICITY = "UNSUPPORTED_MULTIPLICITY"


class OptimizationTrialStatus(StrEnum):
    COMPLETED = "COMPLETED"
    FAILED_CLOSED = "FAILED_CLOSED"
    REJECTED = "REJECTED"


class SelectionDecision(StrEnum):
    INCONCLUSIVE = "INCONCLUSIVE"
    REJECTED = "REJECTED"
    SELECTED = "SELECTED"


class OptimizationRunStatus(StrEnum):
    COMPLETED = "COMPLETED"


_V1 = ObjectVersion(1)
_FP = re.compile(r"sha256:[0-9a-f]{64}")


def _exact(reference: TraceabilityRef, identifier: type, field: str) -> None:
    if (
        not isinstance(reference, TraceabilityRef)
        or not isinstance(reference.object_id, identifier)
        or reference.expected_fingerprint is None
    ):
        raise OptimizationContractError(f"{field} must be an exact fingerprint reference")


def _decimal(value: str, field: str) -> Decimal:
    if not isinstance(value, str) or not re.fullmatch(r"-?(?:0|[1-9][0-9]*)(?:\.[0-9]+)?", value):
        raise OptimizationContractError(f"{field} must be canonical decimal text")
    try:
        parsed = Decimal(value)
    except InvalidOperation as exc:  # pragma: no cover
        raise OptimizationContractError(f"{field} is invalid") from exc
    if not parsed.is_finite() or (parsed == 0 and value != "0") or value.endswith(".0"):
        raise OptimizationContractError(f"{field} has invalid decimal semantics")
    return parsed


def _reasons(values: tuple[OptimizationReasonCode, ...]) -> None:
    if (
        not values
        or tuple(sorted(values, key=lambda item: item.value)) != values
        or len(set(values)) != len(values)
    ):
        raise OptimizationContractError("reason codes must be sorted and unique")


def _parameters(values: tuple[tuple[str, int], ...]) -> None:
    names = tuple(name for name, _ in values)
    supported = {item.value for item in OptimizationParameterName}
    if (
        not values
        or names != tuple(sorted(names))
        or len(set(names)) != len(names)
        or any(name not in supported for name in names)
        or any(isinstance(value, bool) or not isinstance(value, int) for _, value in values)
    ):
        raise OptimizationContractError("candidate parameters must be canonical and supported")


@dataclass(frozen=True, slots=True)
class OptimizationParameter:
    name: OptimizationParameterName
    parameter_type: OptimizationParameterType
    lower_bound: int
    upper_bound: int
    step: int
    default_value: int

    def __post_init__(self) -> None:
        if (
            not isinstance(self.name, OptimizationParameterName)
            or self.parameter_type is not OptimizationParameterType.INTEGER
            or any(
                isinstance(value, bool) or not isinstance(value, int)
                for value in (self.lower_bound, self.upper_bound, self.step, self.default_value)
            )
            or self.step <= 0
            or not self.lower_bound <= self.default_value <= self.upper_bound
            or (self.upper_bound - self.lower_bound) % self.step != 0
        ):
            raise OptimizationContractError("optimization parameter bounds are invalid")

        length_parameters = {
            OptimizationParameterName.ADX_LENGTH,
            OptimizationParameterName.ATR_LENGTH,
            OptimizationParameterName.FAST_EMA,
            OptimizationParameterName.MACD_FAST,
            OptimizationParameterName.MACD_SIGNAL,
            OptimizationParameterName.MACD_SLOW,
            OptimizationParameterName.MEDIUM_EMA,
            OptimizationParameterName.RSI_LENGTH,
            OptimizationParameterName.SLOW_EMA,
            OptimizationParameterName.TIME_STOP_BARS,
        }
        percentage_parameters = {
            OptimizationParameterName.ADX_THRESHOLD_X100,
            OptimizationParameterName.RSI_LONG_MIN_X100,
            OptimizationParameterName.RSI_SHORT_MAX_X100,
        }
        positive_scaled_parameters = {
            OptimizationParameterName.ATR_STOP_MULT_X100,
            OptimizationParameterName.BREAK_EVEN_TRIGGER_R_X100,
            OptimizationParameterName.TAKE_PROFIT_R_X100,
        }
        if self.name is OptimizationParameterName.THRESHOLD_BPS:
            valid = 0 <= self.lower_bound <= self.upper_bound <= 10_000
        elif self.name in length_parameters:
            valid = 1 <= self.lower_bound <= self.upper_bound <= 1000
        elif self.name in percentage_parameters:
            minimum = 1 if self.name is OptimizationParameterName.ADX_THRESHOLD_X100 else 0
            valid = minimum <= self.lower_bound <= self.upper_bound <= 10_000
        elif self.name in positive_scaled_parameters:
            valid = 1 <= self.lower_bound <= self.upper_bound <= 100_000
        else:  # pragma: no cover - exhaustive enum guard
            valid = False
        if not valid:
            raise OptimizationContractError("optimization parameter bounds are invalid")


@dataclass(frozen=True, slots=True)
class OptimizationSearchSpace:
    search_space_id: ArtifactId
    version: ObjectVersion
    parameters: tuple[OptimizationParameter, ...]
    contract_version: ObjectVersion

    def __post_init__(self) -> None:
        if (
            not isinstance(self.search_space_id, ArtifactId)
            or self.version != _V1
            or self.contract_version != _V1
            or not self.parameters
            or tuple(sorted(self.parameters, key=lambda item: item.name.value)) != self.parameters
            or len({item.name for item in self.parameters}) != len(self.parameters)
        ):
            raise OptimizationContractError("search space must be non-empty, sorted and unique")


@dataclass(frozen=True, slots=True)
class OptimizationPlan:
    optimization_plan_id: ArtifactId
    version: ObjectVersion
    search_space_ref: TraceabilityRef
    parent_strategy_ref: TraceabilityRef
    source_experiment_ref: TraceabilityRef
    source_robustness_result_ref: TraceabilityRef
    normalized_manifest_ref: TraceabilityRef
    normalized_lock_ref: TraceabilityRef
    engine_contract_ref: TraceabilityRef
    validation_plan_ref: TraceabilityRef
    robustness_plan_ref: TraceabilityRef
    search_method: OptimizationSearchMethod
    maximum_trials: int
    objective: OptimizationObjective
    minimum_trade_count: int
    maximum_drawdown: str
    multiplicity_policy: OptimizationMultiplicityPolicy
    declared_alpha: str
    selection_authority_ref: TraceabilityRef
    provenance_ref: TraceabilityRef
    contract_version: ObjectVersion

    def __post_init__(self) -> None:
        if (
            not isinstance(self.optimization_plan_id, ArtifactId)
            or self.version != _V1
            or self.search_method is not OptimizationSearchMethod.GRID_SEARCH
            or self.objective is not OptimizationObjective.ROBUSTNESS_AWARE_TOTAL_RETURN
            or self.contract_version != _V1
        ):
            raise OptimizationContractError("unsupported optimization plan")
        for reference, identifier, field in (
            (self.search_space_ref, ArtifactId, "search_space_ref"),
            (self.parent_strategy_ref, ArtifactId, "parent_strategy_ref"),
            (self.source_experiment_ref, ExperimentId, "source_experiment_ref"),
            (self.source_robustness_result_ref, ArtifactId, "source_robustness_result_ref"),
            (self.normalized_manifest_ref, DatasetId, "normalized_manifest_ref"),
            (self.normalized_lock_ref, DatasetLockId, "normalized_lock_ref"),
            (self.engine_contract_ref, ArtifactId, "engine_contract_ref"),
            (self.validation_plan_ref, ArtifactId, "validation_plan_ref"),
            (self.robustness_plan_ref, ArtifactId, "robustness_plan_ref"),
            (self.selection_authority_ref, AuthorityBindingId, "selection_authority_ref"),
            (self.provenance_ref, ProvenanceId, "provenance_ref"),
        ):
            _exact(reference, identifier, field)
        if (
            isinstance(self.maximum_trials, bool)
            or not isinstance(self.maximum_trials, int)
            or not 1 <= self.maximum_trials <= 256
            or isinstance(self.minimum_trade_count, bool)
            or not isinstance(self.minimum_trade_count, int)
            or self.minimum_trade_count < 1
            or not isinstance(self.multiplicity_policy, OptimizationMultiplicityPolicy)
        ):
            raise OptimizationContractError("optimization bounds are invalid")
        if not Decimal(0) <= _decimal(self.maximum_drawdown, "maximum_drawdown") <= Decimal(1):
            raise OptimizationContractError("maximum_drawdown must be between zero and one")
        if not Decimal(0) < _decimal(self.declared_alpha, "declared_alpha") < Decimal("0.5"):
            raise OptimizationContractError("declared_alpha must be between zero and 0.5")


@dataclass(frozen=True, slots=True)
class OptimizationCandidateDefinition:
    candidate_id: ArtifactId
    version: ObjectVersion
    optimization_plan_ref: TraceabilityRef
    parent_strategy_ref: TraceabilityRef
    parameter_values: tuple[tuple[str, int], ...]
    candidate_strategy_ref: TraceabilityRef
    contract_version: ObjectVersion

    def __post_init__(self) -> None:
        if (
            not isinstance(self.candidate_id, ArtifactId)
            or self.version != _V1
            or self.contract_version != _V1
        ):
            raise OptimizationContractError("unsupported candidate definition")
        _exact(self.optimization_plan_ref, ArtifactId, "optimization_plan_ref")
        _exact(self.parent_strategy_ref, ArtifactId, "parent_strategy_ref")
        _exact(self.candidate_strategy_ref, ArtifactId, "candidate_strategy_ref")
        _parameters(self.parameter_values)


@dataclass(frozen=True, slots=True)
class OptimizationRequest:
    optimization_run_id: RunId
    selection_result_id: ArtifactId
    optimization_plan_ref: TraceabilityRef
    selection_authority_ref: TraceabilityRef
    provenance_ref: TraceabilityRef
    contract_version: ObjectVersion = _V1

    def __post_init__(self) -> None:
        if (
            not isinstance(self.optimization_run_id, RunId)
            or not isinstance(self.selection_result_id, ArtifactId)
            or self.contract_version != _V1
        ):
            raise OptimizationContractError("unsupported optimization request")
        _exact(self.optimization_plan_ref, ArtifactId, "optimization_plan_ref")
        _exact(self.selection_authority_ref, AuthorityBindingId, "selection_authority_ref")
        _exact(self.provenance_ref, ProvenanceId, "provenance_ref")


@dataclass(frozen=True, slots=True)
class OptimizationCandidateResult:
    candidate_id: ArtifactId
    version: ObjectVersion
    candidate_definition_ref: TraceabilityRef
    candidate_strategy_ref: TraceabilityRef
    backtest_result_ref: TraceabilityRef
    scientific_validation_result_ref: TraceabilityRef
    robustness_result_ref: TraceabilityRef
    total_return: str
    max_drawdown: str
    trade_count: int
    eligibility: CandidateEligibility
    reason_codes: tuple[OptimizationReasonCode, ...]
    contract_version: ObjectVersion

    def __post_init__(self) -> None:
        if (
            not isinstance(self.candidate_id, ArtifactId)
            or self.version != _V1
            or self.contract_version != _V1
            or not isinstance(self.eligibility, CandidateEligibility)
            or isinstance(self.trade_count, bool)
            or not isinstance(self.trade_count, int)
            or self.trade_count < 0
        ):
            raise OptimizationContractError("unsupported candidate result")
        for reference, identifier, field in (
            (self.candidate_definition_ref, ArtifactId, "candidate_definition_ref"),
            (self.candidate_strategy_ref, ArtifactId, "candidate_strategy_ref"),
            (self.backtest_result_ref, ArtifactId, "backtest_result_ref"),
            (
                self.scientific_validation_result_ref,
                ValidationId,
                "scientific_validation_result_ref",
            ),
            (self.robustness_result_ref, ArtifactId, "robustness_result_ref"),
        ):
            _exact(reference, identifier, field)
        _decimal(self.total_return, "total_return")
        if not Decimal(0) <= _decimal(self.max_drawdown, "max_drawdown") <= Decimal(1):
            raise OptimizationContractError("candidate drawdown is invalid")
        _reasons(self.reason_codes)
        if self.eligibility is CandidateEligibility.ELIGIBLE:
            if self.reason_codes != (OptimizationReasonCode.ALL_CONSTRAINTS_PASSED,):
                raise OptimizationContractError("eligible candidate requires exact pass reason")
        elif OptimizationReasonCode.ALL_CONSTRAINTS_PASSED in self.reason_codes:
            raise OptimizationContractError("rejected candidate cannot carry pass reason")


@dataclass(frozen=True, slots=True)
class OptimizationTrialRecord:
    trial_id: TrialId
    version: ObjectVersion
    optimization_plan_ref: TraceabilityRef
    trial_index: int
    candidate_definition_ref: TraceabilityRef
    candidate_result_ref: TraceabilityRef
    status: OptimizationTrialStatus
    reason_codes: tuple[OptimizationReasonCode, ...]
    contract_version: ObjectVersion

    def __post_init__(self) -> None:
        if (
            not isinstance(self.trial_id, TrialId)
            or self.version != _V1
            or isinstance(self.trial_index, bool)
            or not isinstance(self.trial_index, int)
            or self.trial_index < 0
            or not isinstance(self.status, OptimizationTrialStatus)
            or self.contract_version != _V1
        ):
            raise OptimizationContractError("unsupported optimization trial")
        _exact(self.optimization_plan_ref, ArtifactId, "optimization_plan_ref")
        _exact(self.candidate_definition_ref, ArtifactId, "candidate_definition_ref")
        _exact(self.candidate_result_ref, ArtifactId, "candidate_result_ref")
        _reasons(self.reason_codes)


@dataclass(frozen=True, slots=True)
class OptimizationSelectionResult:
    selection_result_id: ArtifactId
    version: ObjectVersion
    optimization_plan_ref: TraceabilityRef
    candidate_result_refs: tuple[TraceabilityRef, ...]
    trial_refs: tuple[TraceabilityRef, ...]
    attempted_trials: int
    completed_trials: int
    eligible_candidates: int
    selected_candidate_ref: TraceabilityRef | None
    decision: SelectionDecision
    multiplicity_policy: OptimizationMultiplicityPolicy
    corrected_alpha: str | None
    tie_break_order: tuple[str, ...]
    reason_codes: tuple[OptimizationReasonCode, ...]
    selection_authority_ref: TraceabilityRef
    provenance_ref: TraceabilityRef
    deployment_authorization: DeploymentAuthorizationStatus
    execution_state: ExecutionState
    contract_version: ObjectVersion

    def __post_init__(self) -> None:
        if (
            not isinstance(self.selection_result_id, ArtifactId)
            or self.version != _V1
            or self.contract_version != _V1
            or not isinstance(self.decision, SelectionDecision)
            or any(
                isinstance(value, bool) or not isinstance(value, int) or value < 0
                for value in (
                    self.attempted_trials,
                    self.completed_trials,
                    self.eligible_candidates,
                )
            )
            or self.completed_trials > self.attempted_trials
            or self.eligible_candidates > self.completed_trials
        ):
            raise OptimizationContractError("unsupported selection result")
        _exact(self.optimization_plan_ref, ArtifactId, "optimization_plan_ref")
        for reference in self.candidate_result_refs:
            _exact(reference, ArtifactId, "candidate_result_ref")
        for reference in self.trial_refs:
            _exact(reference, TrialId, "trial_ref")
        if (
            len(self.candidate_result_refs) != self.completed_trials
            or len(self.trial_refs) != self.attempted_trials
        ):
            raise OptimizationContractError("selection cardinality is inconsistent")
        if self.selected_candidate_ref is not None:
            _exact(self.selected_candidate_ref, ArtifactId, "selected_candidate_ref")
        if self.decision is SelectionDecision.SELECTED:
            if self.selected_candidate_ref is None or self.eligible_candidates < 1:
                raise OptimizationContractError("selected decision requires eligible candidate")
        elif self.selected_candidate_ref is not None:
            raise OptimizationContractError("non-selected decision cannot name a candidate")
        if self.corrected_alpha is not None:
            _decimal(self.corrected_alpha, "corrected_alpha")
        if self.tie_break_order != (
            "TOTAL_RETURN_DESC",
            "MAX_DRAWDOWN_ASC",
            "TRADE_COUNT_DESC",
            "CANDIDATE_ID_ASC",
        ):
            raise OptimizationContractError("selection tie-break order is not canonical")
        _reasons(self.reason_codes)
        _exact(self.selection_authority_ref, AuthorityBindingId, "selection_authority_ref")
        _exact(self.provenance_ref, ProvenanceId, "provenance_ref")
        if self.deployment_authorization is not DeploymentAuthorizationStatus.NOT_AUTHORIZED:
            raise OptimizationContractError("selection cannot authorize deployment")
        if self.execution_state is not ExecutionState.PLANNED_CLOSED:
            raise OptimizationContractError("selection cannot open execution")


@dataclass(frozen=True, slots=True)
class OptimizationRunRecord:
    optimization_run_id: RunId
    version: ObjectVersion
    optimization_plan_ref: TraceabilityRef
    optimization_input_fingerprint: str
    declared_trials: int
    attempted_trials: int
    completed_trials: int
    selection_result_ref: TraceabilityRef
    selection_authority_ref: TraceabilityRef
    provenance_ref: TraceabilityRef
    status: OptimizationRunStatus
    deployment_authorization: DeploymentAuthorizationStatus
    execution_state: ExecutionState
    contract_version: ObjectVersion

    def __post_init__(self) -> None:
        if (
            not isinstance(self.optimization_run_id, RunId)
            or self.version != _V1
            or not isinstance(self.optimization_input_fingerprint, str)
            or not _FP.fullmatch(self.optimization_input_fingerprint)
            or any(
                isinstance(value, bool) or not isinstance(value, int) or value < 0
                for value in (self.declared_trials, self.attempted_trials, self.completed_trials)
            )
            or self.attempted_trials > self.declared_trials
            or self.completed_trials > self.attempted_trials
            or self.status is not OptimizationRunStatus.COMPLETED
            or self.contract_version != _V1
        ):
            raise OptimizationContractError("unsupported optimization run")
        _exact(self.optimization_plan_ref, ArtifactId, "optimization_plan_ref")
        _exact(self.selection_result_ref, ArtifactId, "selection_result_ref")
        _exact(self.selection_authority_ref, AuthorityBindingId, "selection_authority_ref")
        _exact(self.provenance_ref, ProvenanceId, "provenance_ref")
        if self.deployment_authorization is not DeploymentAuthorizationStatus.NOT_AUTHORIZED:
            raise OptimizationContractError("optimization run cannot authorize deployment")
        if self.execution_state is not ExecutionState.PLANNED_CLOSED:
            raise OptimizationContractError("optimization run cannot open execution")
