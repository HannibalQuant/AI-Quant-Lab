"""Governed contracts for research-dataset eligibility decisions."""

from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum

from ai_quant_lab.core.data import DatasetLockId, InstrumentId, SourceId
from ai_quant_lab.core.market_data import MarketDataSchemaId, TimeframeId
from ai_quant_lab.core.model import (
    AgentId,
    ArtifactId,
    DatasetId,
    ExecutionState,
    ObjectVersion,
    ProvenanceId,
    TraceabilityRef,
    require_utc,
)
from ai_quant_lab.core.real_csv_contracts import (
    AvailabilitySemantics,
    CsvTrustState,
    DuplicatePolicy,
    MissingDataPolicy,
    OrderingPolicy,
    RetentionClassification,
    SourcePermissionState,
    TimestampSemantics,
)


class ResearchEligibilityContractError(ValueError):
    pass


class ResearchDatasetEligibilityStatus(StrEnum):
    ELIGIBLE = "ELIGIBLE"
    INELIGIBLE = "INELIGIBLE"
    QUARANTINED = "QUARANTINED"
    INCOMPLETE = "INCOMPLETE"
    UNSUPPORTED = "UNSUPPORTED"


class EligibilityCalendarSemantics(StrEnum):
    FIXED_UTC_CONTINUOUS = "fixed_utc_continuous"
    SOURCE_SPECIFIC_REQUIRED = "source_specific_required"


class ResearchBoundaryStatus(StrEnum):
    CONTROLLED_RESEARCH_DATASET = "CONTROLLED_RESEARCH_DATASET"
    NOT_ADMITTED_TO_RESEARCH = "NOT_ADMITTED_TO_RESEARCH"


class ExperimentAuthorizationStatus(StrEnum):
    NOT_AUTHORIZED = "NOT_AUTHORIZED"


class ValidationStatus(StrEnum):
    NOT_VALIDATED = "NOT_VALIDATED"


class DeploymentAuthorizationStatus(StrEnum):
    NOT_AUTHORIZED = "NOT_AUTHORIZED"


def _exact(
    reference: TraceabilityRef,
    identifier: type[ArtifactId]
    | type[ProvenanceId]
    | type[SourceId]
    | type[InstrumentId]
    | type[TimeframeId]
    | type[MarketDataSchemaId]
    | type[DatasetId]
    | type[DatasetLockId],
    field: str,
) -> None:
    if (
        not isinstance(reference, TraceabilityRef)
        or not isinstance(reference.object_id, identifier)
        or reference.expected_fingerprint is None
    ):
        raise ResearchEligibilityContractError(
            f"{field} must be an exact fingerprint-bearing reference"
        )


def _enum_tuple[T: StrEnum](values: tuple[T, ...], enum_type: type[T], field: str) -> None:
    if (
        not values
        or any(not isinstance(value, enum_type) for value in values)
        or tuple(sorted(values, key=lambda value: value.value)) != values
        or len(set(values)) != len(values)
    ):
        raise ResearchEligibilityContractError(f"{field} must be non-empty, sorted and unique")


@dataclass(frozen=True, slots=True)
class ResearchDatasetEligibilityPolicy:
    """Explicit technical policy; it is neither legal judgment nor trusted authority."""

    policy_id: ArtifactId
    version: ObjectVersion
    accepted_permission_states: tuple[SourcePermissionState, ...]
    accepted_retention_classifications: tuple[RetentionClassification, ...]
    required_timestamp_semantics: TimestampSemantics
    required_availability_semantics: AvailabilitySemantics
    accepted_missing_data_policies: tuple[MissingDataPolicy, ...]
    accepted_duplicate_policies: tuple[DuplicatePolicy, ...]
    accepted_ordering_policies: tuple[OrderingPolicy, ...]
    calendar_semantics: EligibilityCalendarSemantics
    knowledge_cutoff: datetime
    minimum_row_count: int
    maximum_rejected_rows: int
    maximum_quarantined_observations: int
    maximum_gap_findings: int
    maximum_missing_intervals: int
    require_complete_bars: bool
    allow_restricted_redistribution_for_local_research: bool
    policy_owner_id: AgentId
    contract_version: ObjectVersion

    def __post_init__(self) -> None:
        if (
            not isinstance(self.policy_id, ArtifactId)
            or not isinstance(self.version, ObjectVersion)
            or not isinstance(self.policy_owner_id, AgentId)
            or self.contract_version != ObjectVersion(1)
        ):
            raise ResearchEligibilityContractError("unsupported eligibility policy contract")
        if (
            not isinstance(self.required_timestamp_semantics, TimestampSemantics)
            or not isinstance(self.required_availability_semantics, AvailabilitySemantics)
            or not isinstance(self.calendar_semantics, EligibilityCalendarSemantics)
        ):
            raise ResearchEligibilityContractError("eligibility semantics must be explicit enums")
        _enum_tuple(
            self.accepted_permission_states,
            SourcePermissionState,
            "accepted_permission_states",
        )
        _enum_tuple(
            self.accepted_retention_classifications,
            RetentionClassification,
            "accepted_retention_classifications",
        )
        _enum_tuple(
            self.accepted_missing_data_policies,
            MissingDataPolicy,
            "accepted_missing_data_policies",
        )
        _enum_tuple(
            self.accepted_duplicate_policies,
            DuplicatePolicy,
            "accepted_duplicate_policies",
        )
        _enum_tuple(
            self.accepted_ordering_policies,
            OrderingPolicy,
            "accepted_ordering_policies",
        )
        require_utc(self.knowledge_cutoff, "knowledge_cutoff")
        bounds = (
            self.minimum_row_count,
            self.maximum_rejected_rows,
            self.maximum_quarantined_observations,
            self.maximum_gap_findings,
            self.maximum_missing_intervals,
        )
        if any(
            isinstance(value, bool) or not isinstance(value, int) or value < 0 for value in bounds
        ):
            raise ResearchEligibilityContractError("eligibility quality bounds must be integers")
        if self.minimum_row_count < 1:
            raise ResearchEligibilityContractError("minimum_row_count must be positive")
        if not isinstance(self.require_complete_bars, bool) or not isinstance(
            self.allow_restricted_redistribution_for_local_research, bool
        ):
            raise ResearchEligibilityContractError("eligibility policy flags must be boolean")


@dataclass(frozen=True, slots=True)
class ResearchDatasetEligibilityRecord:
    """Immutable policy decision; ELIGIBLE grants no experiment or execution authority."""

    eligibility_id: ArtifactId
    version: ObjectVersion
    admission_ref: TraceabilityRef
    source_declaration_ref: TraceabilityRef
    source_ref: TraceabilityRef
    instrument_ref: TraceabilityRef
    timeframe_ref: TraceabilityRef
    schema_ref: TraceabilityRef
    raw_manifest_ref: TraceabilityRef | None
    raw_lock_ref: TraceabilityRef | None
    normalized_manifest_ref: TraceabilityRef | None
    normalized_lock_ref: TraceabilityRef | None
    policy_ref: TraceabilityRef
    quality_context_fingerprint: str
    status: ResearchDatasetEligibilityStatus
    findings: tuple[str, ...]
    decision_time: datetime
    decision_actor_id: AgentId
    trust_state: CsvTrustState
    research_boundary: ResearchBoundaryStatus
    experiment_authorization: ExperimentAuthorizationStatus
    validation_status: ValidationStatus
    deployment_authorization: DeploymentAuthorizationStatus
    execution_state: ExecutionState
    contract_version: ObjectVersion

    def __post_init__(self) -> None:
        if (
            not isinstance(self.eligibility_id, ArtifactId)
            or self.version != ObjectVersion(1)
            or not isinstance(self.decision_actor_id, AgentId)
            or self.contract_version != ObjectVersion(1)
        ):
            raise ResearchEligibilityContractError("unsupported eligibility record version")
        if not isinstance(self.status, ResearchDatasetEligibilityStatus) or not isinstance(
            self.research_boundary, ResearchBoundaryStatus
        ):
            raise ResearchEligibilityContractError("eligibility state must be explicit")
        for reference, identifier, field in (
            (self.admission_ref, ArtifactId, "admission_ref"),
            (self.source_declaration_ref, ProvenanceId, "source_declaration_ref"),
            (self.source_ref, SourceId, "source_ref"),
            (self.instrument_ref, InstrumentId, "instrument_ref"),
            (self.timeframe_ref, TimeframeId, "timeframe_ref"),
            (self.schema_ref, MarketDataSchemaId, "schema_ref"),
            (self.policy_ref, ArtifactId, "policy_ref"),
        ):
            _exact(reference, identifier, field)
        if not re.fullmatch(r"sha256:[0-9a-f]{64}", self.quality_context_fingerprint):
            raise ResearchEligibilityContractError(
                "quality_context_fingerprint must be canonical SHA-256"
            )
        if self.raw_manifest_ref is not None:
            _exact(self.raw_manifest_ref, DatasetId, "raw_manifest_ref")
        if self.raw_lock_ref is not None:
            _exact(self.raw_lock_ref, DatasetLockId, "raw_lock_ref")
        if self.normalized_manifest_ref is not None:
            _exact(self.normalized_manifest_ref, DatasetId, "normalized_manifest_ref")
        if self.normalized_lock_ref is not None:
            _exact(self.normalized_lock_ref, DatasetLockId, "normalized_lock_ref")
        if len(self.findings) != len(set(self.findings)) or tuple(sorted(self.findings)) != (
            self.findings
        ):
            raise ResearchEligibilityContractError("findings must be unique and sorted")
        require_utc(self.decision_time, "decision_time")
        if self.trust_state is not CsvTrustState.NOT_TRUSTED:
            raise ResearchEligibilityContractError("eligibility cannot grant source trust")
        if self.experiment_authorization is not ExperimentAuthorizationStatus.NOT_AUTHORIZED:
            raise ResearchEligibilityContractError("eligibility cannot authorize experiments")
        if self.validation_status is not ValidationStatus.NOT_VALIDATED:
            raise ResearchEligibilityContractError("eligibility cannot grant validation")
        if self.deployment_authorization is not DeploymentAuthorizationStatus.NOT_AUTHORIZED:
            raise ResearchEligibilityContractError("eligibility cannot authorize deployment")
        if self.execution_state is not ExecutionState.PLANNED_CLOSED:
            raise ResearchEligibilityContractError("eligibility cannot open execution")
        if self.status is ResearchDatasetEligibilityStatus.ELIGIBLE:
            if self.findings or any(
                reference is None
                for reference in (
                    self.raw_manifest_ref,
                    self.raw_lock_ref,
                    self.normalized_manifest_ref,
                    self.normalized_lock_ref,
                )
            ):
                raise ResearchEligibilityContractError(
                    "eligible record requires exact dataset refs and no findings"
                )
            if self.research_boundary is not ResearchBoundaryStatus.CONTROLLED_RESEARCH_DATASET:
                raise ResearchEligibilityContractError(
                    "eligible record has wrong research boundary"
                )
        elif (
            not self.findings
            or self.research_boundary is not ResearchBoundaryStatus.NOT_ADMITTED_TO_RESEARCH
        ):
            raise ResearchEligibilityContractError(
                "non-eligible record requires findings and a closed research boundary"
            )
