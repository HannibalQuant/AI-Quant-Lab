"""Governed declarative contracts for controlled experiment authorization."""

from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum

from ai_quant_lab.core.data import DatasetLockId
from ai_quant_lab.core.model import (
    AgentId,
    ArtifactId,
    DatasetId,
    ExecutionState,
    ExperimentId,
    ObjectVersion,
    ProvenanceId,
    TraceabilityRef,
    require_utc,
)
from ai_quant_lab.core.research_eligibility_contracts import (
    DeploymentAuthorizationStatus,
    EligibilityCalendarSemantics,
    ValidationStatus,
)


class ExperimentContractError(ValueError):
    pass


class ExperimentFamily(StrEnum):
    FEATURE_RESEARCH = "FEATURE_RESEARCH"
    MARKET_STATISTICS = "MARKET_STATISTICS"
    REGIME_RESEARCH = "REGIME_RESEARCH"
    SIGNAL_RESEARCH = "SIGNAL_RESEARCH"
    STRATEGY_BACKTEST = "STRATEGY_BACKTEST"


class ExperimentAuthorizationDecision(StrEnum):
    AUTHORIZED = "AUTHORIZED"
    REJECTED = "REJECTED"
    QUARANTINED = "QUARANTINED"
    INCOMPLETE = "INCOMPLETE"
    UNSUPPORTED = "UNSUPPORTED"


class ExperimentLifecycleBoundary(StrEnum):
    AUTHORIZED_NOT_EXECUTED = "AUTHORIZED_NOT_EXECUTED"
    NOT_AUTHORIZED = "NOT_AUTHORIZED"


class NoLookaheadSemantics(StrEnum):
    EXPLICIT_EVENT_AVAILABILITY_NEXT_EVENT = "EXPLICIT_EVENT_AVAILABILITY_NEXT_EVENT"
    UNKNOWN = "UNKNOWN"


class CostSemantics(StrEnum):
    DECLARED_BPS = "DECLARED_BPS"
    DECLARED_ZERO = "DECLARED_ZERO"
    NOT_APPLICABLE = "NOT_APPLICABLE"
    UNKNOWN = "UNKNOWN"


class PositionSizingSemantics(StrEnum):
    FIXED_NOTIONAL = "FIXED_NOTIONAL"
    FIXED_QUANTITY = "FIXED_QUANTITY"
    PERCENT_EQUITY = "PERCENT_EQUITY"
    NOT_APPLICABLE = "NOT_APPLICABLE"
    UNKNOWN = "UNKNOWN"


def _exact(reference: TraceabilityRef, identifier: type, field: str) -> None:
    if (
        not isinstance(reference, TraceabilityRef)
        or not isinstance(reference.object_id, identifier)
        or reference.expected_fingerprint is None
    ):
        raise ExperimentContractError(f"{field} must be an exact fingerprint-bearing reference")


def _sorted_unique_strings(values: tuple[str, ...], field: str) -> None:
    if (
        any(not isinstance(value, str) or not value or len(value) > 96 for value in values)
        or tuple(sorted(values)) != values
        or len(set(values)) != len(values)
    ):
        raise ExperimentContractError(f"{field} must be sorted, unique bounded text")


def _configuration(values: tuple[tuple[str, str], ...]) -> None:
    keys = [key for key, _ in values]
    if (
        any(not isinstance(key, str) or not key or len(key) > 64 for key in keys)
        or keys != sorted(keys)
        or len(keys) != len(set(keys))
        or any(not isinstance(value, str) or len(value) > 256 for _, value in values)
    ):
        raise ExperimentContractError("configuration must use sorted unique bounded primitive text")


@dataclass(frozen=True, slots=True)
class ExperimentSpecification:
    """Immutable declaration of a future experiment; contains no executable logic."""

    experiment_id: ExperimentId
    version: ObjectVersion
    eligibility_ref: TraceabilityRef
    normalized_manifest_ref: TraceabilityRef
    normalized_lock_ref: TraceabilityRef
    family: ExperimentFamily
    research_objective: str
    hypothesis_id: ArtifactId
    configuration: tuple[tuple[str, str], ...]
    random_seed: int
    observation_start: datetime
    observation_end: datetime
    knowledge_cutoff: datetime
    no_lookahead: NoLookaheadSemantics
    warmup_bars: int
    commission_semantics: CostSemantics
    commission_bps: int
    slippage_semantics: CostSemantics
    slippage_bps: int
    funding_semantics: CostSemantics
    funding_bps: int
    calendar_semantics: EligibilityCalendarSemantics
    sizing_semantics: PositionSizingSemantics
    capital_notional_minor: int
    engine_contract_ref: TraceabilityRef
    requested_metrics: tuple[str, ...]
    requested_outputs: tuple[str, ...]
    proposer_id: AgentId
    provenance_ref: TraceabilityRef
    contract_version: ObjectVersion

    def __post_init__(self) -> None:
        if (
            not isinstance(self.experiment_id, ExperimentId)
            or self.version != ObjectVersion(1)
            or not isinstance(self.family, ExperimentFamily)
            or not isinstance(self.hypothesis_id, ArtifactId)
            or not isinstance(self.proposer_id, AgentId)
            or self.contract_version != ObjectVersion(1)
        ):
            raise ExperimentContractError("unsupported experiment specification contract")
        _exact(self.eligibility_ref, ArtifactId, "eligibility_ref")
        _exact(self.normalized_manifest_ref, DatasetId, "normalized_manifest_ref")
        _exact(self.normalized_lock_ref, DatasetLockId, "normalized_lock_ref")
        _exact(self.engine_contract_ref, ArtifactId, "engine_contract_ref")
        _exact(self.provenance_ref, ProvenanceId, "provenance_ref")
        if not isinstance(self.research_objective, str) or not self.research_objective.strip():
            raise ExperimentContractError("research_objective is required")
        if len(self.research_objective) > 512:
            raise ExperimentContractError("research_objective is too long")
        _configuration(self.configuration)
        if (
            isinstance(self.random_seed, bool)
            or not isinstance(self.random_seed, int)
            or not 0 <= self.random_seed <= 2**63 - 1
        ):
            raise ExperimentContractError("random_seed must be an explicit bounded integer")
        for name, value in (
            ("observation_start", self.observation_start),
            ("observation_end", self.observation_end),
            ("knowledge_cutoff", self.knowledge_cutoff),
        ):
            require_utc(value, name)
        if self.observation_start >= self.observation_end:
            raise ExperimentContractError("observation_start must be before observation_end")
        if self.knowledge_cutoff < self.observation_end:
            raise ExperimentContractError("knowledge_cutoff cannot precede observation_end")
        if not isinstance(self.no_lookahead, NoLookaheadSemantics):
            raise ExperimentContractError("no-lookahead semantics must be explicit")
        if isinstance(self.warmup_bars, bool) or not isinstance(self.warmup_bars, int) or self.warmup_bars < 0:
            raise ExperimentContractError("warmup_bars must be a non-negative integer")
        for semantic in (
            self.commission_semantics,
            self.slippage_semantics,
            self.funding_semantics,
        ):
            if not isinstance(semantic, CostSemantics):
                raise ExperimentContractError("cost semantics must be explicit")
        for value in (self.commission_bps, self.slippage_bps, self.funding_bps):
            if isinstance(value, bool) or not isinstance(value, int) or not 0 <= value <= 100_000:
                raise ExperimentContractError("cost basis points must be bounded non-negative integers")
        if self.commission_semantics is CostSemantics.DECLARED_ZERO and self.commission_bps != 0:
            raise ExperimentContractError("declared-zero commission must have zero bps")
        if self.slippage_semantics is CostSemantics.DECLARED_ZERO and self.slippage_bps != 0:
            raise ExperimentContractError("declared-zero slippage must have zero bps")
        if self.funding_semantics in {CostSemantics.DECLARED_ZERO, CostSemantics.NOT_APPLICABLE} and self.funding_bps != 0:
            raise ExperimentContractError("zero/not-applicable funding must have zero bps")
        if not isinstance(self.calendar_semantics, EligibilityCalendarSemantics):
            raise ExperimentContractError("calendar semantics must be explicit")
        if not isinstance(self.sizing_semantics, PositionSizingSemantics):
            raise ExperimentContractError("position sizing semantics must be explicit")
        if (
            isinstance(self.capital_notional_minor, bool)
            or not isinstance(self.capital_notional_minor, int)
            or self.capital_notional_minor < 0
        ):
            raise ExperimentContractError("capital_notional_minor must be non-negative")
        _sorted_unique_strings(self.requested_metrics, "requested_metrics")
        _sorted_unique_strings(self.requested_outputs, "requested_outputs")


@dataclass(frozen=True, slots=True)
class ExperimentAuthorizationPolicy:
    policy_id: ArtifactId
    version: ObjectVersion
    allowed_families: tuple[ExperimentFamily, ...]
    required_no_lookahead: NoLookaheadSemantics
    accepted_calendars: tuple[EligibilityCalendarSemantics, ...]
    require_explicit_commission: bool
    require_explicit_slippage: bool
    require_explicit_funding: bool
    require_position_sizing: bool
    maximum_window_days: int
    minimum_seed: int
    maximum_seed: int
    supported_engine_refs: tuple[TraceabilityRef, ...]
    require_verified_actor_authority: bool
    policy_owner_id: AgentId
    contract_version: ObjectVersion

    def __post_init__(self) -> None:
        if (
            not isinstance(self.policy_id, ArtifactId)
            or self.version != ObjectVersion(1)
            or not isinstance(self.policy_owner_id, AgentId)
            or self.contract_version != ObjectVersion(1)
        ):
            raise ExperimentContractError("unsupported authorization policy contract")
        if (
            not self.allowed_families
            or tuple(sorted(self.allowed_families, key=lambda x: x.value)) != self.allowed_families
            or len(set(self.allowed_families)) != len(self.allowed_families)
        ):
            raise ExperimentContractError("allowed_families must be non-empty sorted unique")
        if (
            not self.accepted_calendars
            or tuple(sorted(self.accepted_calendars, key=lambda x: x.value)) != self.accepted_calendars
            or len(set(self.accepted_calendars)) != len(self.accepted_calendars)
        ):
            raise ExperimentContractError("accepted_calendars must be non-empty sorted unique")
        if not isinstance(self.required_no_lookahead, NoLookaheadSemantics):
            raise ExperimentContractError("required no-lookahead semantics must be explicit")
        flags = (
            self.require_explicit_commission,
            self.require_explicit_slippage,
            self.require_explicit_funding,
            self.require_position_sizing,
            self.require_verified_actor_authority,
        )
        if any(not isinstance(flag, bool) for flag in flags):
            raise ExperimentContractError("authorization policy flags must be boolean")
        for value, field in (
            (self.maximum_window_days, "maximum_window_days"),
            (self.minimum_seed, "minimum_seed"),
            (self.maximum_seed, "maximum_seed"),
        ):
            if isinstance(value, bool) or not isinstance(value, int) or value < 0:
                raise ExperimentContractError(f"{field} must be a non-negative integer")
        if self.maximum_window_days < 1 or self.minimum_seed > self.maximum_seed:
            raise ExperimentContractError("authorization policy integer bounds are invalid")
        if not self.supported_engine_refs:
            raise ExperimentContractError("at least one supported engine contract is required")
        for ref in self.supported_engine_refs:
            _exact(ref, ArtifactId, "supported_engine_ref")
        if tuple(sorted(self.supported_engine_refs, key=lambda r: str(r.object_id))) != self.supported_engine_refs:
            raise ExperimentContractError("supported_engine_refs must be sorted")


@dataclass(frozen=True, slots=True)
class ExperimentAuthorizationRecord:
    authorization_id: ArtifactId
    version: ObjectVersion
    specification_ref: TraceabilityRef
    eligibility_ref: TraceabilityRef
    policy_ref: TraceabilityRef
    normalized_manifest_ref: TraceabilityRef
    normalized_lock_ref: TraceabilityRef
    configuration_fingerprint: str
    status: ExperimentAuthorizationDecision
    findings: tuple[str, ...]
    decision_time: datetime
    decision_actor_id: AgentId
    lifecycle: ExperimentLifecycleBoundary
    validation_status: ValidationStatus
    deployment_authorization: DeploymentAuthorizationStatus
    execution_state: ExecutionState
    contract_version: ObjectVersion

    def __post_init__(self) -> None:
        if (
            not isinstance(self.authorization_id, ArtifactId)
            or self.version != ObjectVersion(1)
            or not isinstance(self.decision_actor_id, AgentId)
            or self.contract_version != ObjectVersion(1)
        ):
            raise ExperimentContractError("unsupported authorization record contract")
        _exact(self.specification_ref, ExperimentId, "specification_ref")
        _exact(self.eligibility_ref, ArtifactId, "eligibility_ref")
        _exact(self.policy_ref, ArtifactId, "policy_ref")
        _exact(self.normalized_manifest_ref, DatasetId, "normalized_manifest_ref")
        _exact(self.normalized_lock_ref, DatasetLockId, "normalized_lock_ref")
        if not re.fullmatch(r"sha256:[0-9a-f]{64}", self.configuration_fingerprint):
            raise ExperimentContractError("configuration_fingerprint must be canonical SHA-256")
        if (
            not isinstance(self.status, ExperimentAuthorizationDecision)
            or not isinstance(self.lifecycle, ExperimentLifecycleBoundary)
        ):
            raise ExperimentContractError("authorization state must be explicit")
        if tuple(sorted(self.findings)) != self.findings or len(set(self.findings)) != len(self.findings):
            raise ExperimentContractError("findings must be sorted and unique")
        require_utc(self.decision_time, "decision_time")
        if self.validation_status is not ValidationStatus.NOT_VALIDATED:
            raise ExperimentContractError("authorization cannot grant validation")
        if self.deployment_authorization is not DeploymentAuthorizationStatus.NOT_AUTHORIZED:
            raise ExperimentContractError("authorization cannot grant deployment")
        if self.execution_state is not ExecutionState.PLANNED_CLOSED:
            raise ExperimentContractError("authorization cannot open execution")
        if self.status is ExperimentAuthorizationDecision.AUTHORIZED:
            if self.findings or self.lifecycle is not ExperimentLifecycleBoundary.AUTHORIZED_NOT_EXECUTED:
                raise ExperimentContractError("authorized record requires no findings and closed execution")
        elif not self.findings or self.lifecycle is not ExperimentLifecycleBoundary.NOT_AUTHORIZED:
            raise ExperimentContractError("non-authorized record requires findings and closed lifecycle")
