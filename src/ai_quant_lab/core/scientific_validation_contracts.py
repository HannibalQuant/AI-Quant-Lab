"""Immutable contracts for the bounded Sprint 14 scientific validation boundary."""

from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal, InvalidOperation
from enum import StrEnum

from ai_quant_lab.core.data import DatasetLockId
from ai_quant_lab.core.experiment_contracts import ExperimentFamily
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
    require_utc,
)
from ai_quant_lab.core.research_eligibility_contracts import DeploymentAuthorizationStatus


class ScientificValidationContractError(ValueError):
    pass


class ValidationMetric(StrEnum):
    GROSS_PNL = "GROSS_PNL"
    MAX_DRAWDOWN = "MAX_DRAWDOWN"
    NET_PNL = "NET_PNL"
    TOTAL_RETURN = "TOTAL_RETURN"
    TRADE_COUNT = "TRADE_COUNT"


class NullHypothesis(StrEnum):
    EXPECTED_TOTAL_RETURN_NONPOSITIVE = "EXPECTED_TOTAL_RETURN_NONPOSITIVE"


class AlternativeHypothesis(StrEnum):
    EXPECTED_TOTAL_RETURN_POSITIVE = "EXPECTED_TOTAL_RETURN_POSITIVE"


class UncertaintyMethod(StrEnum):
    TRADE_RETURN_BOOTSTRAP = "TRADE_RETURN_BOOTSTRAP"


class HoldoutPolicy(StrEnum):
    NONE_DECLARED = "NONE_DECLARED"
    RESERVED_HOLDOUT = "RESERVED_HOLDOUT"


class HoldoutEvidenceStatus(StrEnum):
    NONE_DECLARED = "NONE_DECLARED"
    REQUIRED_NOT_PROVEN = "REQUIRED_NOT_PROVEN"


class MultiplicityPolicy(StrEnum):
    SINGLE_PREDECLARED_TEST = "SINGLE_PREDECLARED_TEST"
    MULTIPLE_TESTS_UNCORRECTED = "MULTIPLE_TESTS_UNCORRECTED"
    MULTIPLE_TESTS_CORRECTED = "MULTIPLE_TESTS_CORRECTED"
    UNKNOWN = "UNKNOWN"


class ScientificValidationDecision(StrEnum):
    PASS = "PASS"
    FAIL = "FAIL"
    INCONCLUSIVE = "INCONCLUSIVE"


class ValidationReasonCode(StrEnum):
    FAILED_NONPOSITIVE_BOUND = "FAILED_NONPOSITIVE_BOUND"
    HOLDOUT_REQUIRED = "HOLDOUT_REQUIRED"
    INSUFFICIENT_TRADES = "INSUFFICIENT_TRADES"
    INTERVAL_OVERLAPS_ZERO = "INTERVAL_OVERLAPS_ZERO"
    MULTIPLICITY_UNSUPPORTED = "MULTIPLICITY_UNSUPPORTED"
    MULTIPLICITY_UNKNOWN = "MULTIPLICITY_UNKNOWN"
    OPEN_POSITION_UNRESOLVED = "OPEN_POSITION_UNRESOLVED"
    PASSED_CONFIDENCE_BOUND = "PASSED_CONFIDENCE_BOUND"


class ValidationRunStatus(StrEnum):
    COMPLETED = "COMPLETED"


class ScientificValidationBoundary(StrEnum):
    SCIENTIFIC_METHOD_APPLIED = "SCIENTIFIC_METHOD_APPLIED"


class OutOfSampleEvidenceStatus(StrEnum):
    NOT_ESTABLISHED = "NOT_ESTABLISHED"


_V1 = ObjectVersion(1)
_FINGERPRINT = re.compile(r"sha256:[0-9a-f]{64}")


def _exact(reference: TraceabilityRef, identifier: type, field: str) -> None:
    if (
        not isinstance(reference, TraceabilityRef)
        or not isinstance(reference.object_id, identifier)
        or reference.expected_fingerprint is None
    ):
        raise ScientificValidationContractError(
            f"{field} must be an exact fingerprint-bearing reference"
        )


def _decimal_text(value: str, field: str) -> Decimal:
    if not isinstance(value, str) or not re.fullmatch(r"-?(?:0|[1-9][0-9]*)(?:\.[0-9]+)?", value):
        raise ScientificValidationContractError(f"{field} must be canonical decimal text")
    try:
        parsed = Decimal(value)
    except InvalidOperation as exc:  # pragma: no cover
        raise ScientificValidationContractError(f"{field} is invalid") from exc
    if not parsed.is_finite() or (parsed == 0 and value != "0") or value.endswith(".0"):
        raise ScientificValidationContractError(f"{field} has invalid decimal semantics")
    return parsed


@dataclass(frozen=True, slots=True)
class ValidationPlan:
    validation_plan_id: ArtifactId
    version: ObjectVersion
    target_experiment_family: ExperimentFamily
    target_metrics: tuple[ValidationMetric, ...]
    primary_metric: ValidationMetric
    null_hypothesis: NullHypothesis
    alternative_hypothesis: AlternativeHypothesis
    min_sample_size: int
    min_trade_count: int
    uncertainty_method: UncertaintyMethod
    confidence_level: str
    bootstrap_iterations: int
    random_seed: int
    holdout_policy: HoldoutPolicy
    multiplicity_policy: MultiplicityPolicy
    validator_authority_ref: TraceabilityRef
    provenance_ref: TraceabilityRef
    contract_version: ObjectVersion

    def __post_init__(self) -> None:
        if (
            not isinstance(self.validation_plan_id, ArtifactId)
            or self.version != _V1
            or self.target_experiment_family is not ExperimentFamily.STRATEGY_BACKTEST
            or self.primary_metric is not ValidationMetric.TOTAL_RETURN
            or self.null_hypothesis is not NullHypothesis.EXPECTED_TOTAL_RETURN_NONPOSITIVE
            or self.alternative_hypothesis
            is not AlternativeHypothesis.EXPECTED_TOTAL_RETURN_POSITIVE
            or self.uncertainty_method is not UncertaintyMethod.TRADE_RETURN_BOOTSTRAP
            or self.contract_version != _V1
        ):
            raise ScientificValidationContractError("unsupported validation plan contract")
        if (
            not self.target_metrics
            or tuple(sorted(self.target_metrics, key=lambda item: item.value))
            != self.target_metrics
            or len(set(self.target_metrics)) != len(self.target_metrics)
            or self.primary_metric not in self.target_metrics
        ):
            raise ScientificValidationContractError("target metrics must be sorted and unique")
        if (
            isinstance(self.min_sample_size, bool)
            or not isinstance(self.min_sample_size, int)
            or self.min_sample_size < 1
            or isinstance(self.min_trade_count, bool)
            or not isinstance(self.min_trade_count, int)
            or self.min_trade_count < 1
            or isinstance(self.bootstrap_iterations, bool)
            or not isinstance(self.bootstrap_iterations, int)
            or not 100 <= self.bootstrap_iterations <= 10_000
            or isinstance(self.random_seed, bool)
            or not isinstance(self.random_seed, int)
            or not 0 <= self.random_seed <= 2**63 - 1
        ):
            raise ScientificValidationContractError("validation evidence bounds are invalid")
        confidence = _decimal_text(self.confidence_level, "confidence_level")
        if not Decimal("0.5") < confidence < Decimal(1):
            raise ScientificValidationContractError("confidence_level must be between 0.5 and 1")
        if not isinstance(self.holdout_policy, HoldoutPolicy) or not isinstance(
            self.multiplicity_policy, MultiplicityPolicy
        ):
            raise ScientificValidationContractError("holdout and multiplicity must be explicit")
        _exact(self.validator_authority_ref, AuthorityBindingId, "validator_authority_ref")
        _exact(self.provenance_ref, ProvenanceId, "provenance_ref")


@dataclass(frozen=True, slots=True)
class ValidationRequest:
    validation_run_id: RunId
    validation_result_id: ValidationId
    validation_plan_ref: TraceabilityRef
    backtest_result_ref: TraceabilityRef
    backtest_run_ref: TraceabilityRef
    validator_authority_ref: TraceabilityRef
    completed_at: datetime
    provenance_ref: TraceabilityRef
    contract_version: ObjectVersion = _V1

    def __post_init__(self) -> None:
        if (
            not isinstance(self.validation_run_id, RunId)
            or not isinstance(self.validation_result_id, ValidationId)
            or self.contract_version != _V1
        ):
            raise ScientificValidationContractError("unsupported validation request")
        _exact(self.validation_plan_ref, ArtifactId, "validation_plan_ref")
        _exact(self.backtest_result_ref, ArtifactId, "backtest_result_ref")
        _exact(self.backtest_run_ref, RunId, "backtest_run_ref")
        _exact(self.validator_authority_ref, AuthorityBindingId, "validator_authority_ref")
        _exact(self.provenance_ref, ProvenanceId, "provenance_ref")
        require_utc(self.completed_at, "completed_at")


@dataclass(frozen=True, slots=True)
class ScientificValidationResult:
    validation_result_id: ValidationId
    version: ObjectVersion
    validation_plan_ref: TraceabilityRef
    backtest_result_ref: TraceabilityRef
    backtest_run_ref: TraceabilityRef
    experiment_ref: TraceabilityRef
    strategy_ref: TraceabilityRef
    normalized_manifest_ref: TraceabilityRef
    normalized_lock_ref: TraceabilityRef
    primary_metric: ValidationMetric
    estimate: str
    lower_bound: str
    upper_bound: str
    confidence_level: str
    uncertainty_method: UncertaintyMethod
    sample_size: int
    trade_count: int
    holdout_status: HoldoutEvidenceStatus
    multiplicity_policy: MultiplicityPolicy
    decision: ScientificValidationDecision
    reason_codes: tuple[ValidationReasonCode, ...]
    validator_authority_ref: TraceabilityRef
    provenance_ref: TraceabilityRef
    scientific_boundary: ScientificValidationBoundary
    out_of_sample_evidence: OutOfSampleEvidenceStatus
    deployment_authorization: DeploymentAuthorizationStatus
    execution_state: ExecutionState
    contract_version: ObjectVersion

    def __post_init__(self) -> None:
        if (
            not isinstance(self.validation_result_id, ValidationId)
            or self.version != _V1
            or self.primary_metric is not ValidationMetric.TOTAL_RETURN
            or self.uncertainty_method is not UncertaintyMethod.TRADE_RETURN_BOOTSTRAP
            or self.scientific_boundary
            is not ScientificValidationBoundary.SCIENTIFIC_METHOD_APPLIED
            or self.out_of_sample_evidence is not OutOfSampleEvidenceStatus.NOT_ESTABLISHED
            or self.contract_version != _V1
        ):
            raise ScientificValidationContractError("unsupported scientific validation result")
        for reference, identifier, field in (
            (self.validation_plan_ref, ArtifactId, "validation_plan_ref"),
            (self.backtest_result_ref, ArtifactId, "backtest_result_ref"),
            (self.backtest_run_ref, RunId, "backtest_run_ref"),
            (self.experiment_ref, ExperimentId, "experiment_ref"),
            (self.strategy_ref, ArtifactId, "strategy_ref"),
            (self.normalized_manifest_ref, DatasetId, "normalized_manifest_ref"),
            (self.normalized_lock_ref, DatasetLockId, "normalized_lock_ref"),
            (self.validator_authority_ref, AuthorityBindingId, "validator_authority_ref"),
            (self.provenance_ref, ProvenanceId, "provenance_ref"),
        ):
            _exact(reference, identifier, field)
        _decimal_text(self.estimate, "estimate")
        lower = _decimal_text(self.lower_bound, "lower_bound")
        upper = _decimal_text(self.upper_bound, "upper_bound")
        confidence = _decimal_text(self.confidence_level, "confidence_level")
        if lower > upper or not Decimal("0.5") < confidence < Decimal(1):
            raise ScientificValidationContractError("validation interval is inconsistent")
        if (
            isinstance(self.sample_size, bool)
            or not isinstance(self.sample_size, int)
            or self.sample_size < 0
            or isinstance(self.trade_count, bool)
            or not isinstance(self.trade_count, int)
            or self.trade_count < 0
            or self.sample_size != self.trade_count
        ):
            raise ScientificValidationContractError("validation sample is inconsistent")
        if (
            not self.reason_codes
            or tuple(sorted(self.reason_codes, key=lambda item: item.value)) != self.reason_codes
            or len(set(self.reason_codes)) != len(self.reason_codes)
        ):
            raise ScientificValidationContractError("reason codes must be sorted and unique")
        if not isinstance(self.decision, ScientificValidationDecision):
            raise ScientificValidationContractError("validation decision is invalid")
        if self.deployment_authorization is not DeploymentAuthorizationStatus.NOT_AUTHORIZED:
            raise ScientificValidationContractError("validation cannot grant deployment")
        if self.execution_state is not ExecutionState.PLANNED_CLOSED:
            raise ScientificValidationContractError("validation cannot open live execution")


@dataclass(frozen=True, slots=True)
class ValidationRunRecord:
    validation_run_id: RunId
    version: ObjectVersion
    validation_plan_ref: TraceabilityRef
    backtest_result_ref: TraceabilityRef
    backtest_run_ref: TraceabilityRef
    validation_input_fingerprint: str
    random_seed: int
    validation_result_ref: TraceabilityRef
    validator_authority_ref: TraceabilityRef
    completed_at: datetime
    provenance_ref: TraceabilityRef
    status: ValidationRunStatus
    deployment_authorization: DeploymentAuthorizationStatus
    execution_state: ExecutionState
    contract_version: ObjectVersion

    def __post_init__(self) -> None:
        if (
            not isinstance(self.validation_run_id, RunId)
            or self.version != _V1
            or not isinstance(self.validation_input_fingerprint, str)
            or not _FINGERPRINT.fullmatch(self.validation_input_fingerprint)
            or isinstance(self.random_seed, bool)
            or not isinstance(self.random_seed, int)
            or not 0 <= self.random_seed <= 2**63 - 1
            or self.status is not ValidationRunStatus.COMPLETED
            or self.contract_version != _V1
        ):
            raise ScientificValidationContractError("unsupported validation run record")
        for reference, identifier, field in (
            (self.validation_plan_ref, ArtifactId, "validation_plan_ref"),
            (self.backtest_result_ref, ArtifactId, "backtest_result_ref"),
            (self.backtest_run_ref, RunId, "backtest_run_ref"),
            (self.validation_result_ref, ValidationId, "validation_result_ref"),
            (self.validator_authority_ref, AuthorityBindingId, "validator_authority_ref"),
            (self.provenance_ref, ProvenanceId, "provenance_ref"),
        ):
            _exact(reference, identifier, field)
        require_utc(self.completed_at, "completed_at")
        if self.deployment_authorization is not DeploymentAuthorizationStatus.NOT_AUTHORIZED:
            raise ScientificValidationContractError("validation run cannot grant deployment")
        if self.execution_state is not ExecutionState.PLANNED_CLOSED:
            raise ScientificValidationContractError("validation run cannot open live execution")
