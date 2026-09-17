"""Sprint 9 governed research-dataset eligibility gate tests."""

from __future__ import annotations

import json
from dataclasses import replace
from datetime import UTC, datetime, timedelta
from pathlib import Path

import pytest
from test_real_csv_onboarding import CLOCK, context

from ai_quant_lab import EXE_01
from ai_quant_lab.core.codec import GovernedRecord, decode, encode
from ai_quant_lab.core.csv_import import CsvImportReport
from ai_quant_lab.core.data import SourceId
from ai_quant_lab.core.dataset_store import (
    LocalDatasetRepository,
    RepositoryIntegrityFailure,
    repository_key,
)
from ai_quant_lab.core.integrity import fingerprint_record
from ai_quant_lab.core.model import (
    AgentId,
    ArtifactId,
    ExecutionState,
    GovernedId,
    ObjectVersion,
    TraceabilityRef,
)
from ai_quant_lab.core.real_csv_contracts import (
    AvailabilitySemantics,
    CsvAdmissionStatus,
    CsvTrustState,
    DuplicatePolicy,
    MissingDataPolicy,
    OrderingPolicy,
    RealCsvAdmissionRecord,
    RealCsvSourceDeclaration,
    ResearchEligibilityState,
    RetentionClassification,
    SourcePermissionState,
    TimestampSemantics,
)
from ai_quant_lab.core.real_csv_onboarding import (
    RealCsvOnboardingRequest,
    RealCsvOnboardingResult,
    onboard_real_csv,
)
from ai_quant_lab.core.research_eligibility import (
    EligibilityLineageStatus,
    ResearchDatasetEligibilityRequest,
    ResearchDatasetEligibilityResult,
    ResearchEligibilityError,
    eligibility_quality_context_fingerprint,
    evaluate_research_dataset_eligibility,
    non_admitted_eligibility_context_fingerprint,
    verify_research_eligibility_lineage,
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

V1 = ObjectVersion(1)
DECISION_TIME = datetime(2025, 2, 3, tzinfo=UTC)
GOLDEN = Path(__file__).parent / "golden" / "research_dataset_eligibility_v1.json"


def exact(record: GovernedRecord, object_id: GovernedId) -> TraceabilityRef:
    return TraceabilityRef(object_id, record.version, fingerprint_record(record))  # type: ignore[union-attr]


def policy(
    *,
    version: ObjectVersion = V1,
    minimum_row_count: int = 3,
    calendar: EligibilityCalendarSemantics = EligibilityCalendarSemantics.FIXED_UTC_CONTINUOUS,
) -> ResearchDatasetEligibilityPolicy:
    return ResearchDatasetEligibilityPolicy(
        ArtifactId("research-eligibility-policy"),
        version,
        (SourcePermissionState.DECLARED_PERMITTED,),
        (RetentionClassification.DECLARED_LOCAL_ONLY,),
        TimestampSemantics.BAR_OPEN_AND_CLOSE_UTC,
        AvailabilitySemantics.EXPLICIT_SOURCE_AVAILABILITY_UTC,
        (MissingDataPolicy.RECORD_GAPS,),
        (DuplicatePolicy.REJECT_ALL,),
        (OrderingPolicy.STRICT_ASCENDING_EVENT_TIME,),
        calendar,
        datetime(2025, 2, 2, tzinfo=UTC),
        minimum_row_count,
        0,
        0,
        0,
        0,
        True,
        True,
        AgentId("dataset-governance-owner"),
        V1,
    )


def onboard(
    tmp_path: Path,
    *,
    suffix: str = "eligibility",
    permission: SourcePermissionState = SourcePermissionState.DECLARED_PERMITTED,
    retention: RetentionClassification = RetentionClassification.DECLARED_LOCAL_ONLY,
    timestamps: TimestampSemantics = TimestampSemantics.BAR_OPEN_AND_CLOSE_UTC,
    availability: AvailabilitySemantics = AvailabilitySemantics.EXPLICIT_SOURCE_AVAILABILITY_UTC,
) -> tuple[RealCsvOnboardingRequest, LocalDatasetRepository, RealCsvOnboardingResult]:
    request, source, instrument, schema, timeframe, repository = context(
        tmp_path,
        suffix=suffix,
        permission=permission,
        retention=retention,
        timestamps=timestamps,
        availability=availability,
    )
    result = onboard_real_csv(
        request,
        source=source,
        instrument=instrument,
        schema=schema,
        timeframe=timeframe,
        clock=CLOCK,
        repository=repository,
    )
    return request, repository, result


def eligibility_request(
    declaration: RealCsvSourceDeclaration,
    admission: RealCsvAdmissionRecord,
    eligibility_policy: ResearchDatasetEligibilityPolicy,
    report: CsvImportReport | None = None,
    *,
    eligibility_id: str = "research-dataset-eligibility",
) -> ResearchDatasetEligibilityRequest:
    return ResearchDatasetEligibilityRequest(
        ArtifactId(eligibility_id),
        exact(admission, admission.admission_id),
        exact(declaration, declaration.provenance_id),
        eligibility_policy,
        eligibility_quality_context_fingerprint(report)
        if report is not None
        else non_admitted_eligibility_context_fingerprint(admission),
        DECISION_TIME,
        AgentId("dataset-eligibility-reviewer"),
    )


def evaluate(
    tmp_path: Path, *, suffix: str = "eligibility"
) -> tuple[
    RealCsvOnboardingRequest,
    LocalDatasetRepository,
    RealCsvOnboardingResult,
    ResearchDatasetEligibilityPolicy,
    ResearchDatasetEligibilityResult,
]:
    onboarding, repository, admitted = onboard(tmp_path, suffix=suffix)
    assert admitted.report is not None
    eligibility_policy = policy()
    decision = evaluate_research_dataset_eligibility(
        eligibility_request(
            onboarding.declaration, admitted.admission, eligibility_policy, admitted.report
        ),
        admission=admitted.admission,
        declaration=onboarding.declaration,
        report=admitted.report,
        repository=repository,
    )
    return onboarding, repository, admitted, eligibility_policy, decision


def test_admitted_dataset_becomes_only_controlled_research_eligible_and_reloads(
    tmp_path: Path,
) -> None:
    onboarding, repository, admitted, eligibility_policy, decision = evaluate(tmp_path)
    record = decision.record
    assert record.status is ResearchDatasetEligibilityStatus.ELIGIBLE
    assert record.research_boundary is ResearchBoundaryStatus.CONTROLLED_RESEARCH_DATASET
    assert record.trust_state is CsvTrustState.NOT_TRUSTED
    assert admitted.admission.research_eligibility is ResearchEligibilityState.NOT_RESEARCH_ELIGIBLE
    assert record.experiment_authorization is ExperimentAuthorizationStatus.NOT_AUTHORIZED
    assert record.validation_status is ValidationStatus.NOT_VALIDATED
    assert record.deployment_authorization is DeploymentAuthorizationStatus.NOT_AUTHORIZED
    assert record.execution_state is ExecutionState.PLANNED_CLOSED
    assert EXE_01.state is ExecutionState.PLANNED_CLOSED
    assert decision.lineage is not None
    assert decision.lineage.status is EligibilityLineageStatus.VERIFIED
    assert len(decision.writes) == 2
    assert (
        repository.load(repository_key(eligibility_policy), ResearchDatasetEligibilityPolicy).record
        == eligibility_policy
    )
    assert (
        repository.load(repository_key(record), ResearchDatasetEligibilityRecord).record == record
    )
    assert decode(encode(record), ResearchDatasetEligibilityRecord) == record
    assert record.source_declaration_ref == exact(
        onboarding.declaration, onboarding.declaration.provenance_id
    )


def test_same_dataset_and_policy_is_deterministic_and_idempotent(tmp_path: Path) -> None:
    onboarding, repository, admitted, eligibility_policy, first = evaluate(tmp_path)
    request = eligibility_request(
        onboarding.declaration, admitted.admission, eligibility_policy, admitted.report
    )
    second = evaluate_research_dataset_eligibility(
        request,
        admission=admitted.admission,
        declaration=onboarding.declaration,
        report=admitted.report,
        repository=repository,
    )
    assert first.record == second.record
    assert fingerprint_record(first.record) == fingerprint_record(second.record)
    assert all(write.status.value == "ALREADY_PRESENT_IDENTICAL" for write in second.writes)


def test_different_exact_policy_changes_decision_fingerprint(tmp_path: Path) -> None:
    onboarding, repository, admitted, first_policy, first = evaluate(tmp_path)
    second_policy = replace(first_policy, version=ObjectVersion(2), minimum_row_count=2)
    second = evaluate_research_dataset_eligibility(
        eligibility_request(
            onboarding.declaration, admitted.admission, second_policy, admitted.report
        ),
        admission=admitted.admission,
        declaration=onboarding.declaration,
        report=admitted.report,
        repository=repository,
    )
    assert first.record.policy_ref != second.record.policy_ref
    assert fingerprint_record(first.record) != fingerprint_record(second.record)


@pytest.mark.parametrize(
    ("permission", "retention", "timestamps", "availability", "expected"),
    [
        (
            SourcePermissionState.UNKNOWN,
            RetentionClassification.DECLARED_LOCAL_ONLY,
            TimestampSemantics.BAR_OPEN_AND_CLOSE_UTC,
            AvailabilitySemantics.EXPLICIT_SOURCE_AVAILABILITY_UTC,
            ResearchDatasetEligibilityStatus.QUARANTINED,
        ),
        (
            SourcePermissionState.PROHIBITED,
            RetentionClassification.DECLARED_LOCAL_ONLY,
            TimestampSemantics.BAR_OPEN_AND_CLOSE_UTC,
            AvailabilitySemantics.EXPLICIT_SOURCE_AVAILABILITY_UTC,
            ResearchDatasetEligibilityStatus.INELIGIBLE,
        ),
        (
            SourcePermissionState.DECLARED_PERMITTED,
            RetentionClassification.UNKNOWN,
            TimestampSemantics.BAR_OPEN_AND_CLOSE_UTC,
            AvailabilitySemantics.EXPLICIT_SOURCE_AVAILABILITY_UTC,
            ResearchDatasetEligibilityStatus.INCOMPLETE,
        ),
        (
            SourcePermissionState.DECLARED_PERMITTED,
            RetentionClassification.DECLARED_LOCAL_ONLY,
            TimestampSemantics.AMBIGUOUS,
            AvailabilitySemantics.EXPLICIT_SOURCE_AVAILABILITY_UTC,
            ResearchDatasetEligibilityStatus.UNSUPPORTED,
        ),
        (
            SourcePermissionState.DECLARED_PERMITTED,
            RetentionClassification.DECLARED_LOCAL_ONLY,
            TimestampSemantics.BAR_OPEN_AND_CLOSE_UTC,
            AvailabilitySemantics.UNKNOWN,
            ResearchDatasetEligibilityStatus.INCOMPLETE,
        ),
    ],
)
def test_non_admitted_or_ambiguous_source_never_becomes_eligible(
    tmp_path: Path,
    permission: SourcePermissionState,
    retention: RetentionClassification,
    timestamps: TimestampSemantics,
    availability: AvailabilitySemantics,
    expected: ResearchDatasetEligibilityStatus,
) -> None:
    onboarding, repository, result = onboard(
        tmp_path,
        suffix=expected.value.lower(),
        permission=permission,
        retention=retention,
        timestamps=timestamps,
        availability=availability,
    )
    assert result.admission.status is not CsvAdmissionStatus.ADMITTED
    decision = evaluate_research_dataset_eligibility(
        eligibility_request(onboarding.declaration, result.admission, policy()),
        admission=result.admission,
        declaration=onboarding.declaration,
        report=None,
        repository=repository,
    )
    assert decision.record.status is expected
    assert decision.record.research_boundary is ResearchBoundaryStatus.NOT_ADMITTED_TO_RESEARCH
    assert decision.record.experiment_authorization is ExperimentAuthorizationStatus.NOT_AUTHORIZED


def test_policy_quality_and_calendar_requirements_fail_closed(tmp_path: Path) -> None:
    onboarding, repository, admitted = onboard(tmp_path)
    assert admitted.report is not None
    for suffix, changed_policy, expected_finding in (
        ("coverage", policy(minimum_row_count=4), "insufficient_row_count"),
        (
            "calendar",
            policy(calendar=EligibilityCalendarSemantics.SOURCE_SPECIFIC_REQUIRED),
            "calendar_semantics_unknown",
        ),
    ):
        decision = evaluate_research_dataset_eligibility(
            eligibility_request(
                onboarding.declaration,
                admitted.admission,
                changed_policy,
                admitted.report,
                eligibility_id=f"research-dataset-{suffix}",
            ),
            admission=admitted.admission,
            declaration=onboarding.declaration,
            report=admitted.report,
            repository=repository,
        )
        assert decision.record.status is ResearchDatasetEligibilityStatus.INCOMPLETE
        assert expected_finding in decision.record.findings


def test_tampered_admission_wrong_declaration_and_missing_context_fail_closed(
    tmp_path: Path,
) -> None:
    onboarding, repository, admitted = onboard(tmp_path)
    request = eligibility_request(
        onboarding.declaration, admitted.admission, policy(), admitted.report
    )
    tampered_admission = replace(admitted.admission, original_filename="tampered.csv")
    with pytest.raises(ResearchEligibilityError, match="exact admission"):
        evaluate_research_dataset_eligibility(
            request,
            admission=tampered_admission,
            declaration=onboarding.declaration,
            report=admitted.report,
            repository=repository,
        )
    wrong_declaration = replace(onboarding.declaration, provider_name="Wrong Provider")
    with pytest.raises(ResearchEligibilityError, match="exact source declaration"):
        evaluate_research_dataset_eligibility(
            request,
            admission=admitted.admission,
            declaration=wrong_declaration,
            report=admitted.report,
            repository=repository,
        )
    with pytest.raises(ResearchEligibilityError, match="complete finding context"):
        evaluate_research_dataset_eligibility(
            request,
            admission=admitted.admission,
            declaration=onboarding.declaration,
            report=None,
            repository=repository,
        )


@pytest.mark.parametrize(
    "component",
    ["raw_manifest", "raw_lock", "normalized_manifest", "normalized_lock", "bar"],
)
def test_wrong_dataset_artifact_or_broken_bar_lineage_fails_closed(
    tmp_path: Path, component: str
) -> None:
    onboarding, repository, admitted = onboard(tmp_path, suffix=component)
    assert admitted.report is not None
    report = admitted.report
    if component == "raw_manifest":
        ingestion = replace(
            report.ingestion,
            manifest=replace(report.ingestion.manifest, created_at=DECISION_TIME),
        )
        report = replace(report, ingestion=ingestion)
    elif component == "raw_lock":
        ingestion = replace(
            report.ingestion,
            dataset_lock=replace(report.ingestion.dataset_lock, locked_at=DECISION_TIME),
        )
        report = replace(report, ingestion=ingestion)
    elif component == "normalized_manifest":
        report = replace(
            report,
            normalized_manifest=replace(report.normalized_manifest, created_at=DECISION_TIME),
        )
    elif component == "normalized_lock":
        report = replace(
            report,
            normalized_lock=replace(report.normalized_lock, locked_at=DECISION_TIME),
        )
    else:
        wrong_source = TraceabilityRef(SourceId("wrong-source"), V1, "sha256:" + "f" * 64)
        bars = (
            replace(report.normalized_bars[0], source_ref=wrong_source),
            *report.normalized_bars[1:],
        )
        report = replace(report, normalized_bars=bars)
    with pytest.raises(ValueError):
        evaluate_research_dataset_eligibility(
            eligibility_request(
                onboarding.declaration, admitted.admission, policy(), admitted.report
            ),
            admission=admitted.admission,
            declaration=onboarding.declaration,
            report=report,
            repository=repository,
        )


def test_policy_version_mismatch_and_corrupted_persisted_record_fail_closed(
    tmp_path: Path,
) -> None:
    onboarding, repository, admitted, eligibility_policy, decision = evaluate(tmp_path)
    assert admitted.report is not None
    wrong_policy_ref = replace(
        decision.record.policy_ref,
        version=ObjectVersion(2),
    )
    wrong_record = replace(decision.record, policy_ref=wrong_policy_ref)
    with pytest.raises(ResearchEligibilityError, match="exact policy version"):
        verify_research_eligibility_lineage(
            record=wrong_record,
            policy=eligibility_policy,
            admission=admitted.admission,
            declaration=onboarding.declaration,
            report=admitted.report,
        )
    path = repository.path_for(repository_key(decision.record))
    path.write_bytes(path.read_bytes().replace(b'"ELIGIBLE"', b'"INELIGIBLE"'))
    with pytest.raises(RepositoryIntegrityFailure):
        repository.load(repository_key(decision.record), ResearchDatasetEligibilityRecord)


def test_decision_timestamp_and_knowledge_cutoff_are_not_silently_substituted(
    tmp_path: Path,
) -> None:
    onboarding, repository, admitted = onboard(tmp_path)
    assert admitted.report is not None
    early_decision = eligibility_request(
        onboarding.declaration, admitted.admission, policy(), admitted.report
    )
    early_decision = replace(
        early_decision, decision_time=admitted.admission.ingestion_time - timedelta(seconds=1)
    )
    result = evaluate_research_dataset_eligibility(
        early_decision,
        admission=admitted.admission,
        declaration=onboarding.declaration,
        report=admitted.report,
        repository=repository,
    )
    assert result.record.status is ResearchDatasetEligibilityStatus.INCOMPLETE
    assert "decision_precedes_ingestion" in result.record.findings


def test_quality_context_change_requires_exact_rebinding_and_applies_policy(
    tmp_path: Path,
) -> None:
    onboarding, repository, admitted = onboard(tmp_path)
    assert admitted.report is not None
    request = eligibility_request(
        onboarding.declaration, admitted.admission, policy(), admitted.report
    )
    changed_gap = replace(admitted.report.gap_findings[0], missing_intervals=1)
    changed_report = replace(
        admitted.report,
        gap_findings=(changed_gap, *admitted.report.gap_findings[1:]),
    )
    with pytest.raises(ResearchEligibilityError, match="quality context changed"):
        evaluate_research_dataset_eligibility(
            request,
            admission=admitted.admission,
            declaration=onboarding.declaration,
            report=changed_report,
            repository=repository,
        )
    rebound = eligibility_request(
        onboarding.declaration, admitted.admission, policy(), changed_report
    )
    result = evaluate_research_dataset_eligibility(
        rebound,
        admission=admitted.admission,
        declaration=onboarding.declaration,
        report=changed_report,
        repository=repository,
    )
    assert result.record.status is ResearchDatasetEligibilityStatus.QUARANTINED
    assert "gaps_exceed_declared_policy" in result.record.findings


def test_research_eligibility_golden_is_pinned_and_read_only(tmp_path: Path) -> None:
    onboarding, _, admitted, eligibility_policy, decision = evaluate(tmp_path, suffix="golden")
    assert admitted.report is not None
    actual = {
        "admission_fingerprint": fingerprint_record(admitted.admission),
        "source_declaration_fingerprint": fingerprint_record(onboarding.declaration),
        "raw_manifest_fingerprint": fingerprint_record(admitted.report.ingestion.manifest),
        "raw_lock_fingerprint": fingerprint_record(admitted.report.ingestion.dataset_lock),
        "normalized_manifest_fingerprint": fingerprint_record(admitted.report.normalized_manifest),
        "normalized_lock_fingerprint": fingerprint_record(admitted.report.normalized_lock),
        "policy_fingerprint": fingerprint_record(eligibility_policy),
        "quality_context_fingerprint": decision.record.quality_context_fingerprint,
        "eligibility_record_fingerprint": fingerprint_record(decision.record),
        "eligibility_status": decision.record.status.value,
        "findings": list(decision.record.findings),
    }
    assert actual == json.loads(GOLDEN.read_text(encoding="utf-8"))
