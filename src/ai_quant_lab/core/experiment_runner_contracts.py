"""Immutable contracts for bounded deterministic research experiment execution."""

from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal, InvalidOperation
from enum import StrEnum

from ai_quant_lab.core.data import DatasetLockId
from ai_quant_lab.core.experiment_contracts import (
    ExperimentFamily,
    NoLookaheadSemantics,
)
from ai_quant_lab.core.model import (
    ArtifactId,
    DatasetId,
    ExecutionState,
    ExperimentId,
    ObjectVersion,
    ProvenanceId,
    RunId,
    TraceabilityRef,
    fingerprint,
    require_utc,
)
from ai_quant_lab.core.research_eligibility_contracts import (
    DeploymentAuthorizationStatus,
    ValidationStatus,
)


class ExperimentRunnerContractError(ValueError):
    pass


class ExperimentRunStatus(StrEnum):
    COMPLETED = "COMPLETED"
    REJECTED = "REJECTED"
    INCOMPLETE = "INCOMPLETE"
    UNSUPPORTED = "UNSUPPORTED"
    FAILED = "FAILED"


class ResearchExperimentExecutionStatus(StrEnum):
    RESEARCH_EXPERIMENT_EXECUTED = "RESEARCH_EXPERIMENT_EXECUTED"


class ReplayOrdering(StrEnum):
    BAR_OPEN_CLOSE_SOURCE_OBSERVATION_ID = "BAR_OPEN_CLOSE_SOURCE_OBSERVATION_ID"


class NumericSemantics(StrEnum):
    DECIMAL128_HALF_EVEN = "DECIMAL128_HALF_EVEN"


def _exact(reference: TraceabilityRef, identifier: type, field: str) -> None:
    if (
        not isinstance(reference, TraceabilityRef)
        or not isinstance(reference.object_id, identifier)
        or reference.expected_fingerprint is None
    ):
        raise ExperimentRunnerContractError(
            f"{field} must be an exact fingerprint-bearing reference"
        )


def _fingerprint(value: str, field: str) -> None:
    if not isinstance(value, str) or not re.fullmatch(r"sha256:[0-9a-f]{64}", value):
        raise ExperimentRunnerContractError(f"{field} must be canonical SHA-256")


def _sorted_unique(values: tuple[str, ...], field: str) -> None:
    if (
        not values
        or tuple(sorted(values)) != values
        or len(set(values)) != len(values)
        or any(not isinstance(value, str) or not value or len(value) > 96 for value in values)
    ):
        raise ExperimentRunnerContractError(f"{field} must be nonempty sorted unique text")


def _decimal_text(value: str, field: str) -> None:
    if not isinstance(value, str) or not re.fullmatch(r"-?(?:0|[1-9][0-9]*)(?:\.[0-9]+)?", value):
        raise ExperimentRunnerContractError(f"{field} must be canonical finite decimal text")
    try:
        parsed = Decimal(value)
    except InvalidOperation as exc:  # pragma: no cover - regex excludes malformed decimals
        raise ExperimentRunnerContractError(
            f"{field} must be canonical finite decimal text"
        ) from exc
    if (
        not parsed.is_finite()
        or (parsed == 0 and value != "0")
        or ("." in value and value.endswith("0"))
    ):
        raise ExperimentRunnerContractError(f"{field} must be canonical finite decimal text")


@dataclass(frozen=True, slots=True)
class ExperimentReplayContract:
    """Closed engine contract; it contains no dynamic import or plugin path."""

    engine_id: ArtifactId
    version: ObjectVersion
    family: ExperimentFamily
    no_lookahead: NoLookaheadSemantics
    ordering: ReplayOrdering
    numeric_semantics: NumericSemantics
    decimal_precision: int
    supported_metrics: tuple[str, ...]
    supported_outputs: tuple[str, ...]
    contract_version: ObjectVersion

    def __post_init__(self) -> None:
        if (
            not isinstance(self.engine_id, ArtifactId)
            or self.version != ObjectVersion(1)
            or self.family
            not in (ExperimentFamily.MARKET_STATISTICS, ExperimentFamily.STRATEGY_BACKTEST)
            or self.no_lookahead is not NoLookaheadSemantics.EXPLICIT_EVENT_AVAILABILITY_NEXT_EVENT
            or self.ordering is not ReplayOrdering.BAR_OPEN_CLOSE_SOURCE_OBSERVATION_ID
            or self.numeric_semantics is not NumericSemantics.DECIMAL128_HALF_EVEN
            or self.decimal_precision != 34
            or self.contract_version != ObjectVersion(1)
        ):
            raise ExperimentRunnerContractError("unsupported deterministic replay contract")
        _sorted_unique(self.supported_metrics, "supported_metrics")
        _sorted_unique(self.supported_outputs, "supported_outputs")


@dataclass(frozen=True, slots=True)
class ExperimentResultArtifact:
    artifact_id: ArtifactId
    version: ObjectVersion
    run_id: RunId
    run_version: ObjectVersion
    run_input_fingerprint: str
    authorization_ref: TraceabilityRef
    specification_ref: TraceabilityRef
    policy_ref: TraceabilityRef
    eligibility_ref: TraceabilityRef
    normalized_manifest_ref: TraceabilityRef
    normalized_lock_ref: TraceabilityRef
    engine_contract_ref: TraceabilityRef
    configuration_fingerprint: str
    random_seed: int
    observation_count: int
    first_event_time: datetime
    last_event_time: datetime
    last_knowledge_time: datetime
    close_min: str
    close_max: str
    simple_returns: tuple[str, ...]
    simple_return_mean: str | None
    simple_return_population_variance: str | None
    return_series_fingerprint: str
    validation_status: ValidationStatus
    deployment_authorization: DeploymentAuthorizationStatus
    execution_state: ExecutionState
    contract_version: ObjectVersion

    def __post_init__(self) -> None:
        if (
            not isinstance(self.artifact_id, ArtifactId)
            or self.version != ObjectVersion(1)
            or not isinstance(self.run_id, RunId)
            or self.run_version != ObjectVersion(1)
            or self.contract_version != ObjectVersion(1)
        ):
            raise ExperimentRunnerContractError("unsupported result artifact contract")
        _fingerprint(self.run_input_fingerprint, "run_input_fingerprint")
        _fingerprint(self.configuration_fingerprint, "configuration_fingerprint")
        _fingerprint(self.return_series_fingerprint, "return_series_fingerprint")
        for reference, identifier, field in (
            (self.authorization_ref, ArtifactId, "authorization_ref"),
            (self.specification_ref, ExperimentId, "specification_ref"),
            (self.policy_ref, ArtifactId, "policy_ref"),
            (self.eligibility_ref, ArtifactId, "eligibility_ref"),
            (self.normalized_manifest_ref, DatasetId, "normalized_manifest_ref"),
            (self.normalized_lock_ref, DatasetLockId, "normalized_lock_ref"),
            (self.engine_contract_ref, ArtifactId, "engine_contract_ref"),
        ):
            _exact(reference, identifier, field)
        if (
            isinstance(self.random_seed, bool)
            or not isinstance(self.random_seed, int)
            or self.random_seed < 0
            or isinstance(self.observation_count, bool)
            or not isinstance(self.observation_count, int)
            or self.observation_count < 1
            or len(self.simple_returns) != self.observation_count - 1
        ):
            raise ExperimentRunnerContractError("result cardinality or seed is invalid")
        for field in ("first_event_time", "last_event_time", "last_knowledge_time"):
            require_utc(getattr(self, field), field)
        if self.first_event_time >= self.last_event_time:
            raise ExperimentRunnerContractError("result event interval is invalid")
        if self.last_knowledge_time < self.last_event_time:
            raise ExperimentRunnerContractError("result knowledge precedes final event")
        decimals = (self.close_min, self.close_max, *self.simple_returns)
        optional = (self.simple_return_mean, self.simple_return_population_variance)
        for index, value in enumerate(decimals):
            _decimal_text(value, f"result_decimal_{index}")
        for index, optional_value in enumerate(optional):
            if optional_value is not None:
                _decimal_text(optional_value, f"optional_result_decimal_{index}")
        if Decimal(self.close_min) > Decimal(self.close_max):
            raise ExperimentRunnerContractError("result close range is inverted")
        if self.return_series_fingerprint != fingerprint(self.simple_returns):
            raise ExperimentRunnerContractError("return series fingerprint does not match values")
        if self.observation_count == 1:
            if any(value is not None for value in optional):
                raise ExperimentRunnerContractError("single observation has no return summary")
        elif any(value is None for value in optional):
            raise ExperimentRunnerContractError("return summary is required")
        if self.validation_status is not ValidationStatus.NOT_VALIDATED:
            raise ExperimentRunnerContractError("result cannot grant validation")
        if self.deployment_authorization is not DeploymentAuthorizationStatus.NOT_AUTHORIZED:
            raise ExperimentRunnerContractError("result cannot grant deployment")
        if self.execution_state is not ExecutionState.PLANNED_CLOSED:
            raise ExperimentRunnerContractError("result cannot open live execution")


@dataclass(frozen=True, slots=True)
class ExperimentRunRecord:
    run_id: RunId
    version: ObjectVersion
    authorization_ref: TraceabilityRef
    specification_ref: TraceabilityRef
    policy_ref: TraceabilityRef
    eligibility_ref: TraceabilityRef
    normalized_manifest_ref: TraceabilityRef
    normalized_lock_ref: TraceabilityRef
    engine_contract_ref: TraceabilityRef
    configuration_fingerprint: str
    random_seed: int
    observation_start: datetime
    observation_end: datetime
    knowledge_cutoff: datetime
    run_input_fingerprint: str
    result_ref: TraceabilityRef
    status: ExperimentRunStatus
    completed_at: datetime
    provenance_ref: TraceabilityRef
    research_execution: ResearchExperimentExecutionStatus
    validation_status: ValidationStatus
    deployment_authorization: DeploymentAuthorizationStatus
    execution_state: ExecutionState
    contract_version: ObjectVersion

    def __post_init__(self) -> None:
        if (
            not isinstance(self.run_id, RunId)
            or self.version != ObjectVersion(1)
            or self.status is not ExperimentRunStatus.COMPLETED
            or self.research_execution
            is not ResearchExperimentExecutionStatus.RESEARCH_EXPERIMENT_EXECUTED
            or self.contract_version != ObjectVersion(1)
        ):
            raise ExperimentRunnerContractError("unsupported completed run contract")
        for reference, identifier, field in (
            (self.authorization_ref, ArtifactId, "authorization_ref"),
            (self.specification_ref, ExperimentId, "specification_ref"),
            (self.policy_ref, ArtifactId, "policy_ref"),
            (self.eligibility_ref, ArtifactId, "eligibility_ref"),
            (self.normalized_manifest_ref, DatasetId, "normalized_manifest_ref"),
            (self.normalized_lock_ref, DatasetLockId, "normalized_lock_ref"),
            (self.engine_contract_ref, ArtifactId, "engine_contract_ref"),
            (self.result_ref, ArtifactId, "result_ref"),
            (self.provenance_ref, ProvenanceId, "provenance_ref"),
        ):
            _exact(reference, identifier, field)
        _fingerprint(self.configuration_fingerprint, "configuration_fingerprint")
        _fingerprint(self.run_input_fingerprint, "run_input_fingerprint")
        if isinstance(self.random_seed, bool) or not isinstance(self.random_seed, int):
            raise ExperimentRunnerContractError("run seed is invalid")
        for field in ("observation_start", "observation_end", "knowledge_cutoff", "completed_at"):
            require_utc(getattr(self, field), field)
        if not self.observation_start < self.observation_end <= self.knowledge_cutoff:
            raise ExperimentRunnerContractError("run temporal boundaries are invalid")
        if self.completed_at < self.knowledge_cutoff:
            raise ExperimentRunnerContractError("run completion precedes knowledge cutoff")
        if self.validation_status is not ValidationStatus.NOT_VALIDATED:
            raise ExperimentRunnerContractError("run cannot grant validation")
        if self.deployment_authorization is not DeploymentAuthorizationStatus.NOT_AUTHORIZED:
            raise ExperimentRunnerContractError("run cannot grant deployment")
        if self.execution_state is not ExecutionState.PLANNED_CLOSED:
            raise ExperimentRunnerContractError("run cannot open live execution")
