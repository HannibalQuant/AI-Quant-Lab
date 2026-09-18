"""Fail-closed authorization gate for declarative experiment specifications."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime

from ai_quant_lab.core.csv_import import CsvImportReport
from ai_quant_lab.core.dataset_store import LocalDatasetRepository, RepositoryWriteResult
from ai_quant_lab.core.experiment_contracts import (
    CostSemantics,
    ExperimentAuthorizationDecision,
    ExperimentAuthorizationPolicy,
    ExperimentAuthorizationRecord,
    ExperimentLifecycleBoundary,
    ExperimentSpecification,
    NoLookaheadSemantics,
    PositionSizingSemantics,
)
from ai_quant_lab.core.integrity import fingerprint_record
from ai_quant_lab.core.model import (
    AgentId,
    ArtifactId,
    ExecutionState,
    GovernedId,
    ObjectVersion,
    TraceabilityRef,
    fingerprint,
    require_utc,
)
from ai_quant_lab.core.real_csv_contracts import RealCsvAdmissionRecord, RealCsvSourceDeclaration
from ai_quant_lab.core.research_eligibility import verify_research_eligibility_lineage
from ai_quant_lab.core.research_eligibility_contracts import (
    DeploymentAuthorizationStatus,
    ResearchBoundaryStatus,
    ResearchDatasetEligibilityPolicy,
    ResearchDatasetEligibilityRecord,
    ResearchDatasetEligibilityStatus,
    ValidationStatus,
)


class ExperimentAuthorizationError(ValueError):
    pass


@dataclass(frozen=True, slots=True)
class ExperimentAuthorizationRequest:
    authorization_id: ArtifactId
    specification: ExperimentSpecification
    policy: ExperimentAuthorizationPolicy
    decision_time: datetime
    decision_actor_id: AgentId
    actor_authority_verified: bool = False
    contract_version: ObjectVersion = field(default_factory=lambda: ObjectVersion(1))

    def __post_init__(self) -> None:
        if (
            not isinstance(self.authorization_id, ArtifactId)
            or not isinstance(self.specification, ExperimentSpecification)
            or not isinstance(self.policy, ExperimentAuthorizationPolicy)
            or not isinstance(self.decision_actor_id, AgentId)
            or not isinstance(self.actor_authority_verified, bool)
            or self.contract_version != ObjectVersion(1)
        ):
            raise ExperimentAuthorizationError("unsupported authorization request")
        require_utc(self.decision_time, "decision_time")


@dataclass(frozen=True, slots=True)
class ExperimentAuthorizationResult:
    record: ExperimentAuthorizationRecord
    writes: tuple[RepositoryWriteResult, ...]


def _exact(record: object, object_id: GovernedId, version: ObjectVersion) -> TraceabilityRef:
    return TraceabilityRef(object_id, version, fingerprint_record(record))  # type: ignore[arg-type]


def experiment_configuration_fingerprint(specification: ExperimentSpecification) -> str:
    return fingerprint(
        {
            "configuration": specification.configuration,
            "random_seed": specification.random_seed,
            "warmup_bars": specification.warmup_bars,
            "commission_semantics": specification.commission_semantics,
            "commission_bps": specification.commission_bps,
            "slippage_semantics": specification.slippage_semantics,
            "slippage_bps": specification.slippage_bps,
            "funding_semantics": specification.funding_semantics,
            "funding_bps": specification.funding_bps,
            "calendar_semantics": specification.calendar_semantics,
            "sizing_semantics": specification.sizing_semantics,
            "capital_notional_minor": specification.capital_notional_minor,
        }
    )


def _policy_outcome(
    request: ExperimentAuthorizationRequest,
    eligibility: ResearchDatasetEligibilityRecord,
) -> tuple[ExperimentAuthorizationDecision, tuple[str, ...]]:
    spec = request.specification
    policy = request.policy
    findings: set[str] = set()
    priorities: set[ExperimentAuthorizationDecision] = set()

    if eligibility.status is not ResearchDatasetEligibilityStatus.ELIGIBLE:
        findings.add("dataset_not_eligible")
        priorities.add(ExperimentAuthorizationDecision.REJECTED)
    if eligibility.research_boundary is not ResearchBoundaryStatus.CONTROLLED_RESEARCH_DATASET:
        findings.add("research_boundary_closed")
        priorities.add(ExperimentAuthorizationDecision.REJECTED)
    if spec.family not in policy.allowed_families:
        findings.add("experiment_family_not_allowed")
        priorities.add(ExperimentAuthorizationDecision.UNSUPPORTED)
    if spec.no_lookahead is not policy.required_no_lookahead:
        findings.add("lookahead_contract_missing")
        priorities.add(ExperimentAuthorizationDecision.UNSUPPORTED)
    if spec.no_lookahead is NoLookaheadSemantics.UNKNOWN:
        findings.add("lookahead_contract_unknown")
        priorities.add(ExperimentAuthorizationDecision.INCOMPLETE)
    if spec.calendar_semantics not in policy.accepted_calendars:
        findings.add("calendar_semantics_unknown")
        priorities.add(ExperimentAuthorizationDecision.INCOMPLETE)
    if not policy.minimum_seed <= spec.random_seed <= policy.maximum_seed:
        findings.add("seed_outside_policy")
        priorities.add(ExperimentAuthorizationDecision.REJECTED)
    window_days = (spec.observation_end - spec.observation_start).total_seconds() / 86400
    if window_days > policy.maximum_window_days:
        findings.add("observation_window_exceeds_policy")
        priorities.add(ExperimentAuthorizationDecision.REJECTED)
    if request.decision_time < spec.knowledge_cutoff:
        findings.add("decision_precedes_knowledge_cutoff")
        priorities.add(ExperimentAuthorizationDecision.INCOMPLETE)
    if spec.engine_contract_ref not in policy.supported_engine_refs:
        findings.add("unsupported_engine_contract")
        priorities.add(ExperimentAuthorizationDecision.UNSUPPORTED)
    if policy.require_verified_actor_authority and not request.actor_authority_verified:
        findings.add("authorization_actor_unverified")
        priorities.add(ExperimentAuthorizationDecision.INCOMPLETE)
    if policy.require_explicit_commission and spec.commission_semantics is CostSemantics.UNKNOWN:
        findings.add("cost_semantics_unknown")
        priorities.add(ExperimentAuthorizationDecision.INCOMPLETE)
    if policy.require_explicit_slippage and spec.slippage_semantics is CostSemantics.UNKNOWN:
        findings.add("slippage_semantics_unknown")
        priorities.add(ExperimentAuthorizationDecision.INCOMPLETE)
    if policy.require_explicit_funding and spec.funding_semantics is CostSemantics.UNKNOWN:
        findings.add("funding_semantics_unknown")
        priorities.add(ExperimentAuthorizationDecision.INCOMPLETE)
    if policy.require_position_sizing and spec.sizing_semantics is PositionSizingSemantics.UNKNOWN:
        findings.add("position_sizing_ambiguous")
        priorities.add(ExperimentAuthorizationDecision.INCOMPLETE)

    for status in (
        ExperimentAuthorizationDecision.REJECTED,
        ExperimentAuthorizationDecision.UNSUPPORTED,
        ExperimentAuthorizationDecision.INCOMPLETE,
        ExperimentAuthorizationDecision.QUARANTINED,
    ):
        if status in priorities:
            return status, tuple(sorted(findings))
    return ExperimentAuthorizationDecision.AUTHORIZED, ()


def authorize_experiment(
    request: ExperimentAuthorizationRequest,
    *,
    eligibility: ResearchDatasetEligibilityRecord,
    eligibility_policy: ResearchDatasetEligibilityPolicy,
    admission: RealCsvAdmissionRecord,
    declaration: RealCsvSourceDeclaration,
    report: CsvImportReport,
    repository: LocalDatasetRepository,
) -> ExperimentAuthorizationResult:
    """Authorize an immutable declaration only; never execute an experiment."""
    spec = request.specification
    expected_eligibility = _exact(eligibility, eligibility.eligibility_id, eligibility.version)
    if spec.eligibility_ref != expected_eligibility:
        raise ExperimentAuthorizationError("experiment does not bind exact eligibility record")
    if eligibility.normalized_manifest_ref is None or eligibility.normalized_lock_ref is None:
        raise ExperimentAuthorizationError("eligible record lacks exact normalized dataset refs")
    if (
        spec.normalized_manifest_ref != eligibility.normalized_manifest_ref
        or spec.normalized_lock_ref != eligibility.normalized_lock_ref
    ):
        raise ExperimentAuthorizationError("experiment does not bind exact eligible dataset")
    verify_research_eligibility_lineage(
        record=eligibility,
        policy=eligibility_policy,
        admission=admission,
        declaration=declaration,
        report=report,
    )

    status, findings = _policy_outcome(request, eligibility)
    record = ExperimentAuthorizationRecord(
        request.authorization_id,
        ObjectVersion(1),
        _exact(spec, spec.experiment_id, spec.version),
        expected_eligibility,
        _exact(request.policy, request.policy.policy_id, request.policy.version),
        spec.normalized_manifest_ref,
        spec.normalized_lock_ref,
        experiment_configuration_fingerprint(spec),
        status,
        findings,
        request.decision_time,
        request.decision_actor_id,
        ExperimentLifecycleBoundary.AUTHORIZED_NOT_EXECUTED
        if status is ExperimentAuthorizationDecision.AUTHORIZED
        else ExperimentLifecycleBoundary.NOT_AUTHORIZED,
        ValidationStatus.NOT_VALIDATED,
        DeploymentAuthorizationStatus.NOT_AUTHORIZED,
        ExecutionState.PLANNED_CLOSED,
        ObjectVersion(1),
    )
    writes = (
        repository.store(spec),
        repository.store(request.policy),
        repository.store(record),
    )
    return ExperimentAuthorizationResult(record, writes)
