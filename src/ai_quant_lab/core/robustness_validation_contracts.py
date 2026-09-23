"""Immutable contracts for bounded Sprint 15 robustness validation."""

from __future__ import annotations

import re
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
from enum import StrEnum

from ai_quant_lab.core.data import DatasetLockId
from ai_quant_lab.core.experiment_contracts import CostSemantics
from ai_quant_lab.core.market_data import MarketBarId
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
    ValidationId,
)
from ai_quant_lab.core.research_eligibility_contracts import DeploymentAuthorizationStatus


class RobustnessValidationContractError(ValueError):
    pass


class RobustnessMethod(StrEnum):
    COST_PERTURBATION = "COST_PERTURBATION"
    ROLLING_WALK_FORWARD = "ROLLING_WALK_FORWARD"
    TRADE_BOOTSTRAP_WITH_REPLACEMENT = "TRADE_BOOTSTRAP_WITH_REPLACEMENT"


class TemporalPartitionRole(StrEnum):
    HOLDOUT = "HOLDOUT"
    TEST = "TEST"
    TRAIN = "TRAIN"


class WalkForwardPolicy(StrEnum):
    ROLLING_FIXED_STRATEGY = "ROLLING_FIXED_STRATEGY"


class MonteCarloPolicy(StrEnum):
    TRADE_BOOTSTRAP_WITH_REPLACEMENT = "TRADE_BOOTSTRAP_WITH_REPLACEMENT"


class PerturbationPolicy(StrEnum):
    COMMISSION_MULTIPLIER = "COMMISSION_MULTIPLIER"


class RobustnessDecision(StrEnum):
    FAIL = "FAIL"
    INCONCLUSIVE = "INCONCLUSIVE"
    PASS = "PASS"


class RobustnessReasonCode(StrEnum):
    ALL_ENABLED_METHODS_PASSED = "ALL_ENABLED_METHODS_PASSED"
    COST_PERTURBATION_EXECUTION_FAILED = "COST_PERTURBATION_EXECUTION_FAILED"
    COST_PERTURBATION_FAILED = "COST_PERTURBATION_FAILED"
    COST_PERTURBATION_INCONCLUSIVE = "COST_PERTURBATION_INCONCLUSIVE"
    INSUFFICIENT_TEST_TRADES = "INSUFFICIENT_TEST_TRADES"
    INSUFFICIENT_WINDOWS = "INSUFFICIENT_WINDOWS"
    MONTE_CARLO_FAILED = "MONTE_CARLO_FAILED"
    MONTE_CARLO_INCONCLUSIVE = "MONTE_CARLO_INCONCLUSIVE"
    SOURCE_VALIDATION_NOT_PASS = "SOURCE_VALIDATION_NOT_PASS"
    WALK_FORWARD_FAILED = "WALK_FORWARD_FAILED"
    WALK_FORWARD_INCONCLUSIVE = "WALK_FORWARD_INCONCLUSIVE"


class RobustnessRunStatus(StrEnum):
    COMPLETED = "COMPLETED"


class RobustnessHoldoutEvidence(StrEnum):
    NOT_ESTABLISHED = "NOT_ESTABLISHED"


_V1 = ObjectVersion(1)
_FP = re.compile(r"sha256:[0-9a-f]{64}")


def _exact(reference: TraceabilityRef, identifier: type, field: str) -> None:
    if (
        not isinstance(reference, TraceabilityRef)
        or not isinstance(reference.object_id, identifier)
        or reference.expected_fingerprint is None
    ):
        raise RobustnessValidationContractError(
            f"{field} must be an exact fingerprint-bearing reference"
        )


def _decimal(value: str, field: str) -> Decimal:
    if not isinstance(value, str) or not re.fullmatch(r"-?(?:0|[1-9][0-9]*)(?:\.[0-9]+)?", value):
        raise RobustnessValidationContractError(f"{field} must be canonical decimal text")
    try:
        parsed = Decimal(value)
    except InvalidOperation as exc:  # pragma: no cover
        raise RobustnessValidationContractError(f"{field} is invalid") from exc
    if not parsed.is_finite() or (parsed == 0 and value != "0") or value.endswith(".0"):
        raise RobustnessValidationContractError(f"{field} has invalid decimal semantics")
    return parsed


def _sorted_unique(values: tuple[StrEnum, ...], field: str) -> None:
    if (
        not values
        or tuple(sorted(values, key=lambda item: item.value)) != values
        or len(set(values)) != len(values)
    ):
        raise RobustnessValidationContractError(f"{field} must be sorted and unique")


@dataclass(frozen=True, slots=True)
class RobustnessValidationPlan:
    robustness_plan_id: ArtifactId
    version: ObjectVersion
    source_scientific_validation_ref: TraceabilityRef
    target_methods: tuple[RobustnessMethod, ...]
    walk_forward_policy: WalkForwardPolicy
    train_bars: int
    test_bars: int
    step_bars: int
    minimum_window_count: int
    minimum_completed_trades_per_test_slice: int
    walk_forward_pass_positive_ratio: str
    walk_forward_fail_positive_ratio: str
    walk_forward_pass_worst_return_floor: str
    walk_forward_severe_loss_floor: str
    monte_carlo_policy: MonteCarloPolicy
    monte_carlo_iterations: int
    monte_carlo_seed: int
    monte_carlo_lower_quantile: str
    monte_carlo_upper_quantile: str
    perturbation_policy: PerturbationPolicy
    commission_multipliers: tuple[str, ...]
    perturbation_pass_return_floor: str
    perturbation_fail_return_threshold: str
    robustness_authority_ref: TraceabilityRef
    provenance_ref: TraceabilityRef
    contract_version: ObjectVersion

    def __post_init__(self) -> None:
        if (
            not isinstance(self.robustness_plan_id, ArtifactId)
            or self.version != _V1
            or self.walk_forward_policy is not WalkForwardPolicy.ROLLING_FIXED_STRATEGY
            or self.monte_carlo_policy is not MonteCarloPolicy.TRADE_BOOTSTRAP_WITH_REPLACEMENT
            or self.perturbation_policy is not PerturbationPolicy.COMMISSION_MULTIPLIER
            or self.contract_version != _V1
        ):
            raise RobustnessValidationContractError("unsupported robustness plan contract")
        _exact(
            self.source_scientific_validation_ref,
            ValidationId,
            "source_scientific_validation_ref",
        )
        _sorted_unique(self.target_methods, "target_methods")
        if set(self.target_methods) != set(RobustnessMethod):
            raise RobustnessValidationContractError("all bounded robustness methods are required")
        integer_values = (
            self.train_bars,
            self.test_bars,
            self.step_bars,
            self.minimum_window_count,
            self.minimum_completed_trades_per_test_slice,
            self.monte_carlo_iterations,
            self.monte_carlo_seed,
        )
        if any(isinstance(value, bool) or not isinstance(value, int) for value in integer_values):
            raise RobustnessValidationContractError("robustness integer bounds are invalid")
        if (
            min(self.train_bars, self.test_bars, self.minimum_window_count) < 1
            or self.minimum_completed_trades_per_test_slice < 1
            or self.step_bars < self.test_bars
            or not 100 <= self.monte_carlo_iterations <= 10_000
            or not 0 <= self.monte_carlo_seed <= 2**63 - 1
        ):
            raise RobustnessValidationContractError("robustness evidence bounds are invalid")
        pass_ratio = _decimal(
            self.walk_forward_pass_positive_ratio,
            "walk_forward_pass_positive_ratio",
        )
        fail_ratio = _decimal(
            self.walk_forward_fail_positive_ratio,
            "walk_forward_fail_positive_ratio",
        )
        if not Decimal(0) <= fail_ratio <= pass_ratio <= Decimal(1):
            raise RobustnessValidationContractError("walk-forward ratio thresholds are invalid")
        pass_floor = _decimal(
            self.walk_forward_pass_worst_return_floor,
            "walk_forward_pass_worst_return_floor",
        )
        severe_floor = _decimal(
            self.walk_forward_severe_loss_floor,
            "walk_forward_severe_loss_floor",
        )
        if severe_floor > pass_floor:
            raise RobustnessValidationContractError("walk-forward return floors are invalid")
        lower = _decimal(self.monte_carlo_lower_quantile, "monte_carlo_lower_quantile")
        upper = _decimal(self.monte_carlo_upper_quantile, "monte_carlo_upper_quantile")
        if not Decimal(0) <= lower < upper <= Decimal(1):
            raise RobustnessValidationContractError("Monte Carlo quantiles are invalid")
        if not self.commission_multipliers:
            raise RobustnessValidationContractError("commission scenarios are required")
        multipliers = tuple(
            _decimal(value, "commission_multiplier") for value in self.commission_multipliers
        )
        if (
            multipliers[0] != Decimal(1)
            or tuple(sorted(multipliers)) != multipliers
            or len(set(multipliers)) != len(multipliers)
            or any(value < 1 for value in multipliers)
        ):
            raise RobustnessValidationContractError(
                "commission multipliers must be sorted unique and start at one"
            )
        perturbation_pass = _decimal(
            self.perturbation_pass_return_floor,
            "perturbation_pass_return_floor",
        )
        perturbation_fail = _decimal(
            self.perturbation_fail_return_threshold,
            "perturbation_fail_return_threshold",
        )
        if perturbation_fail > perturbation_pass:
            raise RobustnessValidationContractError("perturbation thresholds are invalid")
        _exact(self.robustness_authority_ref, AuthorityBindingId, "robustness_authority_ref")
        _exact(self.provenance_ref, ProvenanceId, "provenance_ref")


@dataclass(frozen=True, slots=True)
class RobustnessValidationRequest:
    robustness_run_id: RunId
    robustness_result_id: ArtifactId
    robustness_plan_ref: TraceabilityRef
    scientific_validation_result_ref: TraceabilityRef
    validation_run_ref: TraceabilityRef
    backtest_result_ref: TraceabilityRef
    backtest_run_ref: TraceabilityRef
    robustness_authority_ref: TraceabilityRef
    provenance_ref: TraceabilityRef
    contract_version: ObjectVersion = _V1

    def __post_init__(self) -> None:
        if (
            not isinstance(self.robustness_run_id, RunId)
            or not isinstance(self.robustness_result_id, ArtifactId)
            or self.contract_version != _V1
        ):
            raise RobustnessValidationContractError("unsupported robustness request")
        for reference, identifier, field in (
            (self.robustness_plan_ref, ArtifactId, "robustness_plan_ref"),
            (
                self.scientific_validation_result_ref,
                ValidationId,
                "scientific_validation_result_ref",
            ),
            (self.validation_run_ref, RunId, "validation_run_ref"),
            (self.backtest_result_ref, ArtifactId, "backtest_result_ref"),
            (self.backtest_run_ref, RunId, "backtest_run_ref"),
            (self.robustness_authority_ref, AuthorityBindingId, "robustness_authority_ref"),
            (self.provenance_ref, ProvenanceId, "provenance_ref"),
        ):
            _exact(reference, identifier, field)


@dataclass(frozen=True, slots=True)
class TemporalPartitionEvidence:
    partition_id: ArtifactId
    role: TemporalPartitionRole
    start_index: int
    end_index: int
    bar_refs: tuple[TraceabilityRef, ...]

    def __post_init__(self) -> None:
        if (
            not isinstance(self.partition_id, ArtifactId)
            or not isinstance(self.role, TemporalPartitionRole)
            or isinstance(self.start_index, bool)
            or isinstance(self.end_index, bool)
            or not isinstance(self.start_index, int)
            or not isinstance(self.end_index, int)
            or not 0 <= self.start_index < self.end_index
            or len(self.bar_refs) != self.end_index - self.start_index
        ):
            raise RobustnessValidationContractError("temporal partition is invalid")
        if len(set(self.bar_refs)) != len(self.bar_refs):
            raise RobustnessValidationContractError("partition bar refs must be unique")
        for reference in self.bar_refs:
            _exact(reference, MarketBarId, "partition.bar_ref")


@dataclass(frozen=True, slots=True)
class WalkForwardSliceResult:
    slice_id: ArtifactId
    train_partition: TemporalPartitionEvidence
    test_partition: TemporalPartitionEvidence
    trade_count: int
    total_return: str
    net_pnl: str
    max_drawdown: str
    decision: RobustnessDecision

    def __post_init__(self) -> None:
        if (
            not isinstance(self.slice_id, ArtifactId)
            or self.train_partition.role is not TemporalPartitionRole.TRAIN
            or self.test_partition.role is not TemporalPartitionRole.TEST
            or self.train_partition.end_index != self.test_partition.start_index
            or isinstance(self.trade_count, bool)
            or not isinstance(self.trade_count, int)
            or self.trade_count < 0
            or not isinstance(self.decision, RobustnessDecision)
        ):
            raise RobustnessValidationContractError("walk-forward slice is invalid")
        _decimal(self.total_return, "slice.total_return")
        _decimal(self.net_pnl, "slice.net_pnl")
        if _decimal(self.max_drawdown, "slice.max_drawdown") < 0:
            raise RobustnessValidationContractError("slice drawdown cannot be negative")


@dataclass(frozen=True, slots=True)
class WalkForwardSummary:
    slices: tuple[WalkForwardSliceResult, ...]
    valid_window_count: int
    positive_window_ratio: str
    median_test_return: str
    worst_test_return: str
    aggregate_test_return: str
    maximum_test_drawdown: str
    minimum_trade_count: int
    decision: RobustnessDecision
    reason_codes: tuple[RobustnessReasonCode, ...]

    def __post_init__(self) -> None:
        if (
            self.valid_window_count != len(self.slices)
            or isinstance(self.minimum_trade_count, bool)
            or not isinstance(self.minimum_trade_count, int)
            or self.minimum_trade_count < 0
            or not isinstance(self.decision, RobustnessDecision)
        ):
            raise RobustnessValidationContractError("walk-forward summary is invalid")
        for field in (
            "positive_window_ratio",
            "median_test_return",
            "worst_test_return",
            "aggregate_test_return",
            "maximum_test_drawdown",
        ):
            _decimal(getattr(self, field), f"walk_forward.{field}")
        if not Decimal(0) <= Decimal(self.positive_window_ratio) <= Decimal(1):
            raise RobustnessValidationContractError("positive window ratio is invalid")
        if Decimal(self.maximum_test_drawdown) < 0:
            raise RobustnessValidationContractError("walk-forward drawdown is invalid")
        _reasons(self.reason_codes)


@dataclass(frozen=True, slots=True)
class MonteCarloSummary:
    policy: MonteCarloPolicy
    iterations: int
    seed: int
    median_terminal_return: str
    lower_terminal_return: str
    upper_terminal_return: str
    worst_observed_drawdown: str
    positive_terminal_fraction: str
    decision: RobustnessDecision
    reason_codes: tuple[RobustnessReasonCode, ...]

    def __post_init__(self) -> None:
        if (
            self.policy is not MonteCarloPolicy.TRADE_BOOTSTRAP_WITH_REPLACEMENT
            or isinstance(self.iterations, bool)
            or not isinstance(self.iterations, int)
            or self.iterations < 1
            or isinstance(self.seed, bool)
            or not isinstance(self.seed, int)
            or self.seed < 0
            or not isinstance(self.decision, RobustnessDecision)
        ):
            raise RobustnessValidationContractError("Monte Carlo summary is invalid")
        for field in (
            "median_terminal_return",
            "lower_terminal_return",
            "upper_terminal_return",
            "worst_observed_drawdown",
            "positive_terminal_fraction",
        ):
            _decimal(getattr(self, field), f"monte_carlo.{field}")
        if (
            Decimal(self.lower_terminal_return) > Decimal(self.upper_terminal_return)
            or Decimal(self.worst_observed_drawdown) < 0
            or not Decimal(0) <= Decimal(self.positive_terminal_fraction) <= Decimal(1)
        ):
            raise RobustnessValidationContractError("Monte Carlo statistics are inconsistent")
        _reasons(self.reason_codes)


@dataclass(frozen=True, slots=True)
class CostPerturbationScenario:
    scenario_id: ArtifactId
    commission_multiplier: str
    derived_commission_semantics: CostSemantics
    derived_commission_bps: int
    specification_ref: TraceabilityRef
    authorization_ref: TraceabilityRef
    backtest_result_ref: TraceabilityRef | None
    total_return: str | None
    net_pnl: str | None
    max_drawdown: str | None
    trade_count: int | None
    decision: RobustnessDecision
    reason_codes: tuple[RobustnessReasonCode, ...]

    def __post_init__(self) -> None:
        if (
            not isinstance(self.scenario_id, ArtifactId)
            or _decimal(self.commission_multiplier, "scenario.commission_multiplier") < 1
            or self.derived_commission_semantics
            not in (CostSemantics.DECLARED_ZERO, CostSemantics.DECLARED_BPS)
            or isinstance(self.derived_commission_bps, bool)
            or not isinstance(self.derived_commission_bps, int)
            or not 0 <= self.derived_commission_bps <= 100_000
            or not isinstance(self.decision, RobustnessDecision)
        ):
            raise RobustnessValidationContractError("cost scenario is invalid")
        _exact(self.specification_ref, ExperimentId, "scenario.specification_ref")
        _exact(self.authorization_ref, ArtifactId, "scenario.authorization_ref")
        _reasons(self.reason_codes)
        if self.derived_commission_semantics is CostSemantics.DECLARED_ZERO:
            if self.derived_commission_bps != 0:
                raise RobustnessValidationContractError("declared-zero scenario must have zero bps")
        elif self.derived_commission_bps <= 0:
            raise RobustnessValidationContractError("declared-bps scenario must have positive bps")
        numeric = (self.total_return, self.net_pnl, self.max_drawdown)
        if self.decision is RobustnessDecision.FAIL and self.backtest_result_ref is None:
            if any(value is not None for value in numeric) or self.trade_count is not None:
                raise RobustnessValidationContractError(
                    "failed cost execution cannot contain synthetic statistics"
                )
            if self.reason_codes != (RobustnessReasonCode.COST_PERTURBATION_EXECUTION_FAILED,):
                raise RobustnessValidationContractError(
                    "failed cost execution requires exact failure reason"
                )
            return
        if self.backtest_result_ref is None:
            raise RobustnessValidationContractError("successful cost scenario requires result ref")
        _exact(self.backtest_result_ref, ArtifactId, "scenario.backtest_result_ref")
        if any(value is None for value in numeric) or self.trade_count is None:
            raise RobustnessValidationContractError("cost scenario statistics are incomplete")
        assert self.total_return is not None
        assert self.net_pnl is not None
        assert self.max_drawdown is not None
        assert self.trade_count is not None
        _decimal(self.total_return, "scenario.total_return")
        _decimal(self.net_pnl, "scenario.net_pnl")
        if (
            _decimal(self.max_drawdown, "scenario.max_drawdown") < 0
            or isinstance(self.trade_count, bool)
            or not isinstance(self.trade_count, int)
            or self.trade_count < 0
        ):
            raise RobustnessValidationContractError("cost scenario statistics are invalid")


@dataclass(frozen=True, slots=True)
class CostPerturbationSummary:
    policy: PerturbationPolicy
    scenarios: tuple[CostPerturbationScenario, ...]
    decision: RobustnessDecision
    reason_codes: tuple[RobustnessReasonCode, ...]

    def __post_init__(self) -> None:
        if (
            self.policy is not PerturbationPolicy.COMMISSION_MULTIPLIER
            or not self.scenarios
            or not isinstance(self.decision, RobustnessDecision)
        ):
            raise RobustnessValidationContractError("cost perturbation summary is invalid")
        multipliers = tuple(Decimal(item.commission_multiplier) for item in self.scenarios)
        scenario_ids = tuple(item.scenario_id for item in self.scenarios)
        if (
            multipliers[0] != Decimal(1)
            or tuple(sorted(multipliers)) != multipliers
            or len(set(multipliers)) != len(multipliers)
            or len(set(scenario_ids)) != len(scenario_ids)
        ):
            raise RobustnessValidationContractError("cost scenarios must be sorted and unique")
        _reasons(self.reason_codes)


def _reasons(values: tuple[RobustnessReasonCode, ...]) -> None:
    if (
        not values
        or tuple(sorted(values, key=lambda item: item.value)) != values
        or len(set(values)) != len(values)
    ):
        raise RobustnessValidationContractError("reason codes must be sorted and unique")


@dataclass(frozen=True, slots=True)
class RobustnessValidationResult:
    robustness_result_id: ArtifactId
    version: ObjectVersion
    robustness_plan_ref: TraceabilityRef
    scientific_validation_result_ref: TraceabilityRef
    validation_run_ref: TraceabilityRef
    backtest_result_ref: TraceabilityRef
    backtest_run_ref: TraceabilityRef
    strategy_ref: TraceabilityRef
    experiment_ref: TraceabilityRef
    normalized_manifest_ref: TraceabilityRef
    normalized_lock_ref: TraceabilityRef
    walk_forward: WalkForwardSummary
    monte_carlo: MonteCarloSummary
    cost_perturbation: CostPerturbationSummary
    holdout_evidence: RobustnessHoldoutEvidence
    decision: RobustnessDecision
    reason_codes: tuple[RobustnessReasonCode, ...]
    robustness_authority_ref: TraceabilityRef
    provenance_ref: TraceabilityRef
    deployment_authorization: DeploymentAuthorizationStatus
    execution_state: ExecutionState
    contract_version: ObjectVersion

    def __post_init__(self) -> None:
        if (
            not isinstance(self.robustness_result_id, ArtifactId)
            or self.version != _V1
            or self.holdout_evidence is not RobustnessHoldoutEvidence.NOT_ESTABLISHED
            or not isinstance(self.decision, RobustnessDecision)
            or self.contract_version != _V1
        ):
            raise RobustnessValidationContractError("unsupported robustness result")
        for reference, identifier, field in (
            (self.robustness_plan_ref, ArtifactId, "robustness_plan_ref"),
            (
                self.scientific_validation_result_ref,
                ValidationId,
                "scientific_validation_result_ref",
            ),
            (self.validation_run_ref, RunId, "validation_run_ref"),
            (self.backtest_result_ref, ArtifactId, "backtest_result_ref"),
            (self.backtest_run_ref, RunId, "backtest_run_ref"),
            (self.strategy_ref, ArtifactId, "strategy_ref"),
            (self.experiment_ref, ExperimentId, "experiment_ref"),
            (self.normalized_manifest_ref, DatasetId, "normalized_manifest_ref"),
            (self.normalized_lock_ref, DatasetLockId, "normalized_lock_ref"),
            (self.robustness_authority_ref, AuthorityBindingId, "robustness_authority_ref"),
            (self.provenance_ref, ProvenanceId, "provenance_ref"),
        ):
            _exact(reference, identifier, field)
        _reasons(self.reason_codes)
        if self.deployment_authorization is not DeploymentAuthorizationStatus.NOT_AUTHORIZED:
            raise RobustnessValidationContractError("robustness cannot grant deployment")
        if self.execution_state is not ExecutionState.PLANNED_CLOSED:
            raise RobustnessValidationContractError("robustness cannot open execution")


@dataclass(frozen=True, slots=True)
class RobustnessValidationRunRecord:
    robustness_run_id: RunId
    version: ObjectVersion
    robustness_plan_ref: TraceabilityRef
    scientific_validation_result_ref: TraceabilityRef
    validation_run_ref: TraceabilityRef
    backtest_result_ref: TraceabilityRef
    backtest_run_ref: TraceabilityRef
    robustness_input_fingerprint: str
    monte_carlo_seed: int
    robustness_result_ref: TraceabilityRef
    robustness_authority_ref: TraceabilityRef
    provenance_ref: TraceabilityRef
    status: RobustnessRunStatus
    deployment_authorization: DeploymentAuthorizationStatus
    execution_state: ExecutionState
    contract_version: ObjectVersion

    def __post_init__(self) -> None:
        if (
            not isinstance(self.robustness_run_id, RunId)
            or self.version != _V1
            or not isinstance(self.robustness_input_fingerprint, str)
            or not _FP.fullmatch(self.robustness_input_fingerprint)
            or isinstance(self.monte_carlo_seed, bool)
            or not isinstance(self.monte_carlo_seed, int)
            or self.monte_carlo_seed < 0
            or self.status is not RobustnessRunStatus.COMPLETED
            or self.contract_version != _V1
        ):
            raise RobustnessValidationContractError("unsupported robustness run record")
        for reference, identifier, field in (
            (self.robustness_plan_ref, ArtifactId, "robustness_plan_ref"),
            (
                self.scientific_validation_result_ref,
                ValidationId,
                "scientific_validation_result_ref",
            ),
            (self.validation_run_ref, RunId, "validation_run_ref"),
            (self.backtest_result_ref, ArtifactId, "backtest_result_ref"),
            (self.backtest_run_ref, RunId, "backtest_run_ref"),
            (self.robustness_result_ref, ArtifactId, "robustness_result_ref"),
            (self.robustness_authority_ref, AuthorityBindingId, "robustness_authority_ref"),
            (self.provenance_ref, ProvenanceId, "provenance_ref"),
        ):
            _exact(reference, identifier, field)
        if self.deployment_authorization is not DeploymentAuthorizationStatus.NOT_AUTHORIZED:
            raise RobustnessValidationContractError("robustness run cannot grant deployment")
        if self.execution_state is not ExecutionState.PLANNED_CLOSED:
            raise RobustnessValidationContractError("robustness run cannot open execution")
