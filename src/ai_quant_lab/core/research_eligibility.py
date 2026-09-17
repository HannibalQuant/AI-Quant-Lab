"""Fail-closed gate from technical CSV admission to controlled research eligibility."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from datetime import datetime
from enum import StrEnum

from ai_quant_lab.core.codec import GovernedRecord
from ai_quant_lab.core.csv_import import CsvImportReport
from ai_quant_lab.core.dataset_store import LocalDatasetRepository, RepositoryWriteResult
from ai_quant_lab.core.integrity import fingerprint_record
from ai_quant_lab.core.model import (
    AgentId,
    ArtifactId,
    ExecutionState,
    GovernedId,
    ObjectVersion,
    ProvenanceId,
    TraceabilityRef,
    fingerprint,
    require_utc,
)
from ai_quant_lab.core.real_csv_contracts import (
    AvailabilitySemantics,
    CsvAdmissionStatus,
    CsvTrustState,
    RealCsvAdmissionRecord,
    RealCsvSourceDeclaration,
    ResearchEligibilityState,
    RetentionClassification,
    SourcePermissionState,
    TimestampSemantics,
)
from ai_quant_lab.core.real_csv_onboarding import (
    RealCsvLineageVerification,
    verify_real_csv_lineage,
)
from ai_quant_lab.core.research_eligibility_contracts import (
    DeploymentAuthorizationStatus,
    EligibilityCalendarSemantics,
    ExperimentAuthorizationStatus,
    ResearchBoundaryStatus,
    ResearchDatasetEligibilityPolicy,
    ResearchDatasetEligibilityRecord,
    ResearchDatasetEligibilityStatus,
    ValidationStatus,
)


class ResearchEligibilityError(ValueError):
    """Missing or mismatched governed context cannot produce eligibility."""


class EligibilityLineageStatus(StrEnum):
    VERIFIED = "VERIFIED"


@dataclass(frozen=True, slots=True)
class ResearchDatasetEligibilityRequest:
    eligibility_id: ArtifactId
    admission_ref: TraceabilityRef
    source_declaration_ref: TraceabilityRef
    policy: ResearchDatasetEligibilityPolicy
    quality_context_fingerprint: str
    decision_time: datetime
    decision_actor_id: AgentId
    contract_version: ObjectVersion = field(default_factory=lambda: ObjectVersion(1))

    def __post_init__(self) -> None:
        if (
            not isinstance(self.eligibility_id, ArtifactId)
            or not isinstance(self.policy, ResearchDatasetEligibilityPolicy)
            or not isinstance(self.decision_actor_id, AgentId)
            or self.contract_version != ObjectVersion(1)
        ):
            raise ResearchEligibilityError("unsupported eligibility request version")
        if (
            not isinstance(self.admission_ref.object_id, ArtifactId)
            or self.admission_ref.expected_fingerprint is None
            or not isinstance(self.source_declaration_ref.object_id, ProvenanceId)
            or self.source_declaration_ref.expected_fingerprint is None
        ):
            raise ResearchEligibilityError("eligibility request requires exact input references")
        if not re.fullmatch(r"sha256:[0-9a-f]{64}", self.quality_context_fingerprint):
            raise ResearchEligibilityError("eligibility request requires quality fingerprint")
        require_utc(self.decision_time, "decision_time")


@dataclass(frozen=True, slots=True)
class ResearchEligibilityLineageVerification:
    status: EligibilityLineageStatus
    admission_fingerprint: str
    declaration_fingerprint: str
    policy_fingerprint: str
    eligibility_fingerprint: str
    real_csv_lineage: RealCsvLineageVerification


@dataclass(frozen=True, slots=True)
class ResearchDatasetEligibilityResult:
    record: ResearchDatasetEligibilityRecord
    writes: tuple[RepositoryWriteResult, ...]
    lineage: ResearchEligibilityLineageVerification | None


def _exact(
    record: GovernedRecord, object_id: GovernedId, version: ObjectVersion
) -> TraceabilityRef:
    return TraceabilityRef(object_id, version, fingerprint_record(record))


def _require_request_bindings(
    request: ResearchDatasetEligibilityRequest,
    admission: RealCsvAdmissionRecord,
    declaration: RealCsvSourceDeclaration,
) -> None:
    if request.admission_ref != _exact(admission, admission.admission_id, admission.version):
        raise ResearchEligibilityError("eligibility request does not bind exact admission")
    if request.source_declaration_ref != _exact(
        declaration, declaration.provenance_id, declaration.version
    ):
        raise ResearchEligibilityError("eligibility request does not bind exact source declaration")
    if admission.source_declaration_ref != request.source_declaration_ref:
        raise ResearchEligibilityError("admission does not bind requested source declaration")


def _require_dataset_scope(declaration: RealCsvSourceDeclaration, report: CsvImportReport) -> None:
    raw = report.ingestion.manifest
    normalized = report.normalized_manifest
    if raw.source_refs != (declaration.source_ref,) or normalized.source_refs != (
        declaration.source_ref,
    ):
        raise ResearchEligibilityError("dataset source scope differs from declaration")
    if raw.instrument_refs != (declaration.instrument_ref,) or normalized.instrument_refs != (
        declaration.instrument_ref,
    ):
        raise ResearchEligibilityError("dataset instrument scope differs from declaration")
    if normalized.timeframe_refs != (declaration.timeframe_ref,):
        raise ResearchEligibilityError("dataset timeframe scope differs from declaration")
    if normalized.schema_ref != declaration.schema_ref:
        raise ResearchEligibilityError("dataset schema scope differs from declaration")


def eligibility_quality_context_fingerprint(report: CsvImportReport) -> str:
    """Fingerprint deterministic quality inputs consumed by eligibility policy."""
    return fingerprint(
        {
            "file_sha256": report.file_sha256,
            "file_size": report.file_size,
            "row_count": report.row_count,
            "csv_rejections": report.csv_rejections,
            "ingestion_rejections": report.ingestion.rejected,
            "quarantined_observation_refs": report.ingestion.quarantined_refs,
            "normalization_rejections": report.normalization_rejections,
            "incomplete_bar_fingerprints": tuple(
                fingerprint_record(bar) for bar in report.incomplete_bars
            ),
            "gap_findings": report.gap_findings,
            "bar_findings": report.bar_findings,
            "normalized_bar_availability": tuple(
                bar.availability_time for bar in report.normalized_bars
            ),
            "status": report.status,
        }
    )


def non_admitted_eligibility_context_fingerprint(
    admission: RealCsvAdmissionRecord,
) -> str:
    """Bind a denial to the exact non-admitted technical outcome."""
    return fingerprint(
        {
            "admission_fingerprint": fingerprint_record(admission),
            "status": admission.status,
            "findings": admission.findings,
        }
    )


def _non_admitted_outcome(
    admission: RealCsvAdmissionRecord, declaration: RealCsvSourceDeclaration
) -> tuple[ResearchDatasetEligibilityStatus, tuple[str, ...]]:
    findings = {
        "technical_admission_required",
        f"admission_status_{admission.status.value.lower()}",
    }
    if declaration.permission_state is SourcePermissionState.PROHIBITED:
        findings.add("source_permission_prohibited")
        status = ResearchDatasetEligibilityStatus.INELIGIBLE
    elif declaration.permission_state is SourcePermissionState.UNKNOWN:
        findings.add("source_permission_unknown")
        status = ResearchDatasetEligibilityStatus.QUARANTINED
    elif declaration.permission_state is SourcePermissionState.DECLARED_RESTRICTED:
        findings.add("source_permission_restricted")
        status = ResearchDatasetEligibilityStatus.QUARANTINED
    elif declaration.retention_classification is RetentionClassification.UNKNOWN:
        findings.add("retention_unknown")
        status = ResearchDatasetEligibilityStatus.INCOMPLETE
    elif declaration.timestamp_semantics is TimestampSemantics.AMBIGUOUS:
        findings.add("timestamp_semantics_ambiguous")
        status = ResearchDatasetEligibilityStatus.UNSUPPORTED
    elif declaration.availability_semantics is AvailabilitySemantics.UNKNOWN:
        findings.add("availability_semantics_unknown")
        status = ResearchDatasetEligibilityStatus.INCOMPLETE
    else:
        status = ResearchDatasetEligibilityStatus.INELIGIBLE
    return status, tuple(sorted(findings))


def _policy_outcome(
    policy: ResearchDatasetEligibilityPolicy,
    admission: RealCsvAdmissionRecord,
    declaration: RealCsvSourceDeclaration,
    report: CsvImportReport,
    decision_time: datetime,
) -> tuple[ResearchDatasetEligibilityStatus, tuple[str, ...]]:
    findings: set[str] = set()
    priority: set[ResearchDatasetEligibilityStatus] = set()

    if declaration.permission_state is SourcePermissionState.PROHIBITED:
        findings.add("source_permission_prohibited")
        priority.add(ResearchDatasetEligibilityStatus.INELIGIBLE)
    elif declaration.permission_state not in policy.accepted_permission_states:
        finding = (
            "source_permission_unknown"
            if declaration.permission_state is SourcePermissionState.UNKNOWN
            else "source_permission_restricted"
        )
        findings.add(finding)
        priority.add(ResearchDatasetEligibilityStatus.QUARANTINED)
    if declaration.retention_classification not in policy.accepted_retention_classifications:
        findings.add(
            "retention_unknown"
            if declaration.retention_classification is RetentionClassification.UNKNOWN
            else "retention_not_allowed_by_policy"
        )
        priority.add(
            ResearchDatasetEligibilityStatus.INCOMPLETE
            if declaration.retention_classification is RetentionClassification.UNKNOWN
            else ResearchDatasetEligibilityStatus.QUARANTINED
        )
    if (
        declaration.redistribution_restriction is not None
        and not policy.allow_restricted_redistribution_for_local_research
    ):
        findings.add("redistribution_restricted_by_policy")
        priority.add(ResearchDatasetEligibilityStatus.QUARANTINED)
    if declaration.timestamp_semantics is not policy.required_timestamp_semantics:
        findings.add("timestamp_semantics_unsupported")
        priority.add(ResearchDatasetEligibilityStatus.UNSUPPORTED)
    if declaration.availability_semantics is not policy.required_availability_semantics:
        findings.add("availability_semantics_unknown")
        priority.add(ResearchDatasetEligibilityStatus.INCOMPLETE)
    if declaration.missing_data_policy not in policy.accepted_missing_data_policies:
        findings.add("missing_data_policy_unsupported")
        priority.add(ResearchDatasetEligibilityStatus.UNSUPPORTED)
    if declaration.duplicate_policy not in policy.accepted_duplicate_policies:
        findings.add("duplicate_policy_unsupported")
        priority.add(ResearchDatasetEligibilityStatus.UNSUPPORTED)
    if declaration.ordering_policy not in policy.accepted_ordering_policies:
        findings.add("ordering_policy_unsupported")
        priority.add(ResearchDatasetEligibilityStatus.UNSUPPORTED)
    if policy.calendar_semantics is EligibilityCalendarSemantics.SOURCE_SPECIFIC_REQUIRED:
        findings.add("calendar_semantics_unknown")
        priority.add(ResearchDatasetEligibilityStatus.INCOMPLETE)
    if decision_time < admission.ingestion_time:
        findings.add("decision_precedes_ingestion")
        priority.add(ResearchDatasetEligibilityStatus.INCOMPLETE)
    if admission.row_count < policy.minimum_row_count:
        findings.add("insufficient_row_count")
        priority.add(ResearchDatasetEligibilityStatus.INCOMPLETE)

    rejected_rows = (
        len(report.csv_rejections)
        + report.ingestion.rejected_count
        + len(report.normalization_rejections)
    )
    if rejected_rows > policy.maximum_rejected_rows:
        findings.add("rejected_rows_exceed_policy")
        priority.add(ResearchDatasetEligibilityStatus.QUARANTINED)
    if report.ingestion.quarantined_count > policy.maximum_quarantined_observations:
        findings.add("quarantined_observations_exceed_policy")
        priority.add(ResearchDatasetEligibilityStatus.QUARANTINED)
    actual_gap_count = sum(finding.missing_intervals > 0 for finding in report.gap_findings)
    if actual_gap_count > policy.maximum_gap_findings:
        findings.add("gaps_exceed_declared_policy")
        priority.add(ResearchDatasetEligibilityStatus.QUARANTINED)
    if sum(finding.missing_intervals for finding in report.gap_findings) > (
        policy.maximum_missing_intervals
    ):
        findings.add("missing_intervals_exceed_policy")
        priority.add(ResearchDatasetEligibilityStatus.QUARANTINED)
    if policy.require_complete_bars and report.incomplete_bars:
        findings.add("incomplete_bars_present")
        priority.add(ResearchDatasetEligibilityStatus.QUARANTINED)
    if any(bar.availability_time > policy.knowledge_cutoff for bar in report.normalized_bars):
        findings.add("availability_after_policy_cutoff")
        priority.add(ResearchDatasetEligibilityStatus.QUARANTINED)

    for status in (
        ResearchDatasetEligibilityStatus.INELIGIBLE,
        ResearchDatasetEligibilityStatus.UNSUPPORTED,
        ResearchDatasetEligibilityStatus.INCOMPLETE,
        ResearchDatasetEligibilityStatus.QUARANTINED,
    ):
        if status in priority:
            return status, tuple(sorted(findings))
    return ResearchDatasetEligibilityStatus.ELIGIBLE, ()


def _record(
    request: ResearchDatasetEligibilityRequest,
    admission: RealCsvAdmissionRecord,
    declaration: RealCsvSourceDeclaration,
    status: ResearchDatasetEligibilityStatus,
    findings: tuple[str, ...],
) -> ResearchDatasetEligibilityRecord:
    policy_ref = _exact(request.policy, request.policy.policy_id, request.policy.version)
    return ResearchDatasetEligibilityRecord(
        request.eligibility_id,
        ObjectVersion(1),
        request.admission_ref,
        request.source_declaration_ref,
        declaration.source_ref,
        declaration.instrument_ref,
        declaration.timeframe_ref,
        declaration.schema_ref,
        admission.raw_manifest_ref,
        admission.raw_lock_ref,
        admission.normalized_manifest_ref,
        admission.normalized_lock_ref,
        policy_ref,
        request.quality_context_fingerprint,
        status,
        findings,
        request.decision_time,
        request.decision_actor_id,
        CsvTrustState.NOT_TRUSTED,
        ResearchBoundaryStatus.CONTROLLED_RESEARCH_DATASET
        if status is ResearchDatasetEligibilityStatus.ELIGIBLE
        else ResearchBoundaryStatus.NOT_ADMITTED_TO_RESEARCH,
        ExperimentAuthorizationStatus.NOT_AUTHORIZED,
        ValidationStatus.NOT_VALIDATED,
        DeploymentAuthorizationStatus.NOT_AUTHORIZED,
        ExecutionState.PLANNED_CLOSED,
        ObjectVersion(1),
    )


def verify_research_eligibility_lineage(
    *,
    record: ResearchDatasetEligibilityRecord,
    policy: ResearchDatasetEligibilityPolicy,
    admission: RealCsvAdmissionRecord,
    declaration: RealCsvSourceDeclaration,
    report: CsvImportReport,
) -> ResearchEligibilityLineageVerification:
    """Verify exact eligibility inputs while granting no downstream authority."""
    if record.admission_ref != _exact(admission, admission.admission_id, admission.version):
        raise ResearchEligibilityError("eligibility record does not bind exact admission")
    if record.source_declaration_ref != _exact(
        declaration, declaration.provenance_id, declaration.version
    ):
        raise ResearchEligibilityError("eligibility record does not bind exact declaration")
    if record.policy_ref != _exact(policy, policy.policy_id, policy.version):
        raise ResearchEligibilityError("eligibility record does not bind exact policy version")
    if record.quality_context_fingerprint != eligibility_quality_context_fingerprint(report):
        raise ResearchEligibilityError("eligibility record does not bind exact quality context")
    if (
        record.source_ref,
        record.instrument_ref,
        record.timeframe_ref,
        record.schema_ref,
    ) != (
        declaration.source_ref,
        declaration.instrument_ref,
        declaration.timeframe_ref,
        declaration.schema_ref,
    ):
        raise ResearchEligibilityError("eligibility identity scope differs from declaration")
    expected_dataset_refs = (
        admission.raw_manifest_ref,
        admission.raw_lock_ref,
        admission.normalized_manifest_ref,
        admission.normalized_lock_ref,
    )
    if (
        record.raw_manifest_ref,
        record.raw_lock_ref,
        record.normalized_manifest_ref,
        record.normalized_lock_ref,
    ) != expected_dataset_refs:
        raise ResearchEligibilityError("eligibility record does not bind exact dataset refs")
    real_csv_lineage = verify_real_csv_lineage(
        admission=admission, declaration=declaration, report=report
    )
    _require_dataset_scope(declaration, report)
    return ResearchEligibilityLineageVerification(
        EligibilityLineageStatus.VERIFIED,
        fingerprint_record(admission),
        fingerprint_record(declaration),
        fingerprint_record(policy),
        fingerprint_record(record),
        real_csv_lineage,
    )


def evaluate_research_dataset_eligibility(
    request: ResearchDatasetEligibilityRequest,
    *,
    admission: RealCsvAdmissionRecord,
    declaration: RealCsvSourceDeclaration,
    report: CsvImportReport | None,
    repository: LocalDatasetRepository,
) -> ResearchDatasetEligibilityResult:
    """Evaluate dataset eligibility; never authorize an experiment, validation or execution."""
    _require_request_bindings(request, admission, declaration)
    if (
        admission.trust_state is not CsvTrustState.NOT_TRUSTED
        or admission.research_eligibility is not ResearchEligibilityState.NOT_RESEARCH_ELIGIBLE
    ):
        raise ResearchEligibilityError("technical admission authority boundary was altered")

    lineage: ResearchEligibilityLineageVerification | None = None
    if admission.status is not CsvAdmissionStatus.ADMITTED:
        if request.quality_context_fingerprint != non_admitted_eligibility_context_fingerprint(
            admission
        ):
            raise ResearchEligibilityError("eligibility request denial context changed")
        status, findings = _non_admitted_outcome(admission, declaration)
    else:
        if report is None:
            raise ResearchEligibilityError("admitted eligibility requires complete finding context")
        if request.quality_context_fingerprint != eligibility_quality_context_fingerprint(report):
            raise ResearchEligibilityError("eligibility request quality context changed")
        verify_real_csv_lineage(admission=admission, declaration=declaration, report=report)
        _require_dataset_scope(declaration, report)
        status, findings = _policy_outcome(
            request.policy, admission, declaration, report, request.decision_time
        )

    record = _record(request, admission, declaration, status, findings)
    if admission.status is CsvAdmissionStatus.ADMITTED:
        if report is None:  # pragma: no cover - guarded above for static narrowing
            raise ResearchEligibilityError("admitted eligibility requires finding context")
        lineage = verify_research_eligibility_lineage(
            record=record,
            policy=request.policy,
            admission=admission,
            declaration=declaration,
            report=report,
        )
    writes = (repository.store(request.policy), repository.store(record))
    return ResearchDatasetEligibilityResult(record, writes, lineage)
