"""Closed deterministic runner for authorized MARKET_STATISTICS experiments."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from decimal import ROUND_HALF_EVEN, Context, Decimal, localcontext
from itertools import pairwise

from ai_quant_lab.core.csv_import import CsvImportReport
from ai_quant_lab.core.dataset_store import LocalDatasetRepository, RepositoryWriteResult
from ai_quant_lab.core.experiment_authorization import (
    experiment_configuration_fingerprint,
    verify_experiment_authorization_lineage,
)
from ai_quant_lab.core.experiment_contracts import (
    CostSemantics,
    ExperimentAuthorizationDecision,
    ExperimentAuthorizationPolicy,
    ExperimentAuthorizationRecord,
    ExperimentFamily,
    ExperimentLifecycleBoundary,
    ExperimentSpecification,
    NoLookaheadSemantics,
    PositionSizingSemantics,
)
from ai_quant_lab.core.experiment_runner_contracts import (
    ExperimentReplayContract,
    ExperimentResultArtifact,
    ExperimentRunRecord,
    ExperimentRunStatus,
    NumericSemantics,
    ReplayOrdering,
    ResearchExperimentExecutionStatus,
)
from ai_quant_lab.core.integrity import fingerprint_record
from ai_quant_lab.core.market_data import BarFinality, MarketBar
from ai_quant_lab.core.model import (
    ArtifactId,
    ExecutionState,
    ExperimentId,
    ObjectVersion,
    ProvenanceId,
    RunId,
    TraceabilityRef,
    fingerprint,
    require_utc,
)
from ai_quant_lab.core.real_csv_contracts import RealCsvAdmissionRecord, RealCsvSourceDeclaration
from ai_quant_lab.core.research_eligibility_contracts import (
    DeploymentAuthorizationStatus,
    ResearchBoundaryStatus,
    ResearchDatasetEligibilityPolicy,
    ResearchDatasetEligibilityRecord,
    ResearchDatasetEligibilityStatus,
    ValidationStatus,
)


class ExperimentRunnerError(ValueError):
    pass


class InvalidExperimentAuthorization(ExperimentRunnerError):
    pass


class ExperimentRunnerLineageMismatch(ExperimentRunnerError):
    pass


class UnsupportedExperimentRunner(ExperimentRunnerError):
    pass


class ExperimentTimeWindowMismatch(ExperimentRunnerError):
    pass


class ReplayOrderingFailure(ExperimentRunnerError):
    pass


class MissingRequiredBars(ExperimentRunnerError):
    pass


class ExperimentResultLineageMismatch(ExperimentRunnerError):
    pass


_V1 = ObjectVersion(1)
_DECIMAL_CONTEXT = Context(prec=34, rounding=ROUND_HALF_EVEN)
_METRICS = (
    "close_max",
    "close_min",
    "observation_count",
    "simple_return_mean",
    "simple_return_population_variance",
)
_OUTPUTS = ("return_series",)


def market_statistics_replay_contract() -> ExperimentReplayContract:
    """Return the only executable engine contract in Sprint 11."""
    return ExperimentReplayContract(
        ArtifactId("market-statistics-replay-engine-v1"),
        _V1,
        ExperimentFamily.MARKET_STATISTICS,
        NoLookaheadSemantics.EXPLICIT_EVENT_AVAILABILITY_NEXT_EVENT,
        ReplayOrdering.BAR_OPEN_CLOSE_SOURCE_OBSERVATION_ID,
        NumericSemantics.DECIMAL128_HALF_EVEN,
        34,
        _METRICS,
        _OUTPUTS,
        _V1,
    )


def market_statistics_engine_ref() -> TraceabilityRef:
    contract = market_statistics_replay_contract()
    return TraceabilityRef(contract.engine_id, contract.version, fingerprint_record(contract))


@dataclass(frozen=True, slots=True)
class ExperimentRunRequest:
    run_id: RunId
    result_artifact_id: ArtifactId
    authorization_ref: TraceabilityRef
    specification_ref: TraceabilityRef
    policy_ref: TraceabilityRef
    eligibility_ref: TraceabilityRef
    engine_contract_ref: TraceabilityRef
    completed_at: datetime
    provenance_ref: TraceabilityRef
    contract_version: ObjectVersion = field(default_factory=lambda: ObjectVersion(1))

    def __post_init__(self) -> None:
        if (
            not isinstance(self.run_id, RunId)
            or not isinstance(self.result_artifact_id, ArtifactId)
            or self.contract_version != _V1
        ):
            raise ExperimentRunnerError("unsupported experiment run request")
        for reference, identifier, field_name in (
            (self.authorization_ref, ArtifactId, "authorization_ref"),
            (self.specification_ref, ExperimentId, "specification_ref"),
            (self.policy_ref, ArtifactId, "policy_ref"),
            (self.eligibility_ref, ArtifactId, "eligibility_ref"),
            (self.engine_contract_ref, ArtifactId, "engine_contract_ref"),
            (self.provenance_ref, ProvenanceId, "provenance_ref"),
        ):
            if (
                not isinstance(reference, TraceabilityRef)
                or not isinstance(reference.object_id, identifier)
                or reference.expected_fingerprint is None
            ):
                raise ExperimentRunnerError(f"{field_name} must be exact")
        require_utc(self.completed_at, "completed_at")


@dataclass(frozen=True, slots=True)
class ExperimentRunResult:
    record: ExperimentRunRecord
    artifact: ExperimentResultArtifact
    writes: tuple[RepositoryWriteResult, ...]


def _exact(record: object, object_id: object, version: ObjectVersion) -> TraceabilityRef:
    return TraceabilityRef(object_id, version, fingerprint_record(record))  # type: ignore[arg-type]


def _canonical_decimal(value: Decimal) -> str:
    if not value.is_finite():
        raise ExperimentRunnerError("non-finite experiment result")
    if value == 0:
        return "0"
    text = format(value, "f")
    if "." in text:
        text = text.rstrip("0").rstrip(".")
    return text


def _bar_order(bar: MarketBar) -> tuple[datetime, datetime, str, str, str, int]:
    return (
        bar.bar_open,
        bar.bar_close,
        str(bar.source_ref.object_id),
        str(bar.source_observation_ref.object_id),
        str(bar.bar_id),
        bar.version.number,
    )


def _run_input_fingerprint(
    request: ExperimentRunRequest,
    authorization: ExperimentAuthorizationRecord,
    specification: ExperimentSpecification,
    policy: ExperimentAuthorizationPolicy,
    eligibility: ResearchDatasetEligibilityRecord,
) -> str:
    return fingerprint(
        {
            "run_id": str(request.run_id),
            "run_version": 1,
            "result_artifact_id": str(request.result_artifact_id),
            "authorization_ref": request.authorization_ref,
            "specification_ref": request.specification_ref,
            "policy_ref": request.policy_ref,
            "eligibility_ref": request.eligibility_ref,
            "engine_contract_ref": request.engine_contract_ref,
            "authorization_fingerprint": fingerprint_record(authorization),
            "specification_fingerprint": fingerprint_record(specification),
            "policy_fingerprint": fingerprint_record(policy),
            "eligibility_fingerprint": fingerprint_record(eligibility),
            "configuration_fingerprint": experiment_configuration_fingerprint(specification),
            "seed": specification.random_seed,
            "observation_start": specification.observation_start,
            "observation_end": specification.observation_end,
            "knowledge_cutoff": specification.knowledge_cutoff,
            "completed_at": request.completed_at,
            "provenance_ref": request.provenance_ref,
        }
    )


def _verify_authorization(
    request: ExperimentRunRequest,
    *,
    authorization: ExperimentAuthorizationRecord,
    specification: ExperimentSpecification,
    policy: ExperimentAuthorizationPolicy,
    eligibility: ResearchDatasetEligibilityRecord,
    eligibility_policy: ResearchDatasetEligibilityPolicy,
    admission: RealCsvAdmissionRecord,
    declaration: RealCsvSourceDeclaration,
    report: CsvImportReport,
    engine_contract: ExperimentReplayContract,
) -> None:
    expected = (
        _exact(authorization, authorization.authorization_id, authorization.version),
        _exact(specification, specification.experiment_id, specification.version),
        _exact(policy, policy.policy_id, policy.version),
        _exact(eligibility, eligibility.eligibility_id, eligibility.version),
        _exact(engine_contract, engine_contract.engine_id, engine_contract.version),
    )
    actual = (
        request.authorization_ref,
        request.specification_ref,
        request.policy_ref,
        request.eligibility_ref,
        request.engine_contract_ref,
    )
    if actual != expected:
        raise ExperimentRunnerLineageMismatch("run request exact references do not match inputs")
    if (
        authorization.status is not ExperimentAuthorizationDecision.AUTHORIZED
        or authorization.lifecycle is not ExperimentLifecycleBoundary.AUTHORIZED_NOT_EXECUTED
        or authorization.validation_status is not ValidationStatus.NOT_VALIDATED
        or authorization.deployment_authorization
        is not DeploymentAuthorizationStatus.NOT_AUTHORIZED
        or authorization.execution_state is not ExecutionState.PLANNED_CLOSED
    ):
        raise InvalidExperimentAuthorization("experiment authorization is not runnable")
    if (
        eligibility.status is not ResearchDatasetEligibilityStatus.ELIGIBLE
        or eligibility.research_boundary is not ResearchBoundaryStatus.CONTROLLED_RESEARCH_DATASET
    ):
        raise InvalidExperimentAuthorization("research dataset is not eligible")
    try:
        verify_experiment_authorization_lineage(
            record=authorization,
            specification=specification,
            policy=policy,
            eligibility=eligibility,
            eligibility_policy=eligibility_policy,
            admission=admission,
            declaration=declaration,
            report=report,
        )
    except ValueError as exc:
        raise ExperimentRunnerLineageMismatch(
            "experiment authorization reconstruction failed"
        ) from exc
    if (
        authorization.specification_ref != expected[1]
        or authorization.policy_ref != expected[2]
        or authorization.eligibility_ref != expected[3]
        or authorization.normalized_manifest_ref != specification.normalized_manifest_ref
        or authorization.normalized_lock_ref != specification.normalized_lock_ref
        or specification.eligibility_ref != expected[3]
        or specification.normalized_manifest_ref != eligibility.normalized_manifest_ref
        or specification.normalized_lock_ref != eligibility.normalized_lock_ref
    ):
        raise ExperimentRunnerLineageMismatch("authorization lineage does not bind exact inputs")
    if authorization.configuration_fingerprint != experiment_configuration_fingerprint(
        specification
    ):
        raise ExperimentRunnerLineageMismatch("authorization configuration fingerprint changed")
    if specification.engine_contract_ref != expected[4] or expected[4] not in (
        policy.supported_engine_refs
    ):
        raise UnsupportedExperimentRunner("authorization does not bind supported exact engine")


def _select_replay_bars(
    specification: ExperimentSpecification, report: CsvImportReport
) -> tuple[MarketBar, ...]:
    bars = report.normalized_bars
    if not bars or tuple(sorted(bars, key=_bar_order)) != bars:
        raise ReplayOrderingFailure("normalized bars are not in canonical replay order")
    if len({bar.business_key for bar in bars}) != len(bars):
        raise ReplayOrderingFailure("duplicate replay business key")
    selected = tuple(
        bar
        for bar in bars
        if bar.bar_open >= specification.observation_start
        and bar.bar_close <= specification.observation_end
    )
    if not selected:
        raise MissingRequiredBars("authorized observation window contains no bars")
    if (
        selected[0].bar_open != specification.observation_start
        or selected[-1].bar_close != specification.observation_end
    ):
        raise ExperimentTimeWindowMismatch("replay window is not aligned to exact bars")
    for previous, following in pairwise(selected):
        if previous.bar_close != following.bar_open:
            raise MissingRequiredBars("authorized observation window contains a missing bar")
    if any(
        bar.finality is BarFinality.INCOMPLETE
        or bar.availability_time > specification.knowledge_cutoff
        for bar in selected
    ):
        raise ExperimentTimeWindowMismatch("bar is unavailable at the governed knowledge cutoff")
    availability = tuple(bar.availability_time for bar in selected)
    if availability != tuple(sorted(availability)) or len(set(availability)) != len(availability):
        raise ReplayOrderingFailure("bar availability order is non-deterministic")
    return selected


def available_bars_at(
    bars: tuple[MarketBar, ...], knowledge_boundary: datetime
) -> tuple[MarketBar, ...]:
    """Expose only bars legitimately available at an explicit UTC knowledge boundary."""
    require_utc(knowledge_boundary, "knowledge_boundary")
    return tuple(bar for bar in bars if bar.availability_time <= knowledge_boundary)


def _require_market_statistics_scope(
    specification: ExperimentSpecification, engine_contract: ExperimentReplayContract
) -> None:
    if specification.family is not ExperimentFamily.MARKET_STATISTICS:
        raise UnsupportedExperimentRunner("only MARKET_STATISTICS is supported")
    if engine_contract != market_statistics_replay_contract():
        raise UnsupportedExperimentRunner("unknown replay engine implementation")
    if specification.no_lookahead is not engine_contract.no_lookahead:
        raise UnsupportedExperimentRunner("unsupported no-lookahead semantics")
    if specification.requested_metrics != engine_contract.supported_metrics:
        raise UnsupportedExperimentRunner("requested metrics do not match the closed engine")
    if specification.requested_outputs != engine_contract.supported_outputs:
        raise UnsupportedExperimentRunner("requested outputs do not match the closed engine")
    if (
        specification.commission_semantics is not CostSemantics.NOT_APPLICABLE
        or specification.slippage_semantics is not CostSemantics.NOT_APPLICABLE
        or specification.funding_semantics is not CostSemantics.NOT_APPLICABLE
        or specification.sizing_semantics is not PositionSizingSemantics.NOT_APPLICABLE
        or specification.capital_notional_minor != 0
        or specification.warmup_bars != 0
    ):
        raise UnsupportedExperimentRunner(
            "MARKET_STATISTICS requires non-trading cost, sizing and warmup semantics"
        )


def _result_artifact(
    request: ExperimentRunRequest,
    authorization: ExperimentAuthorizationRecord,
    specification: ExperimentSpecification,
    engine_contract: ExperimentReplayContract,
    bars: tuple[MarketBar, ...],
    run_input_fingerprint: str,
) -> ExperimentResultArtifact:
    replayed_closes: list[Decimal] = []
    visible_count = 0
    for index, bar in enumerate(bars):
        while (
            visible_count < len(bars)
            and bars[visible_count].availability_time <= bar.availability_time
        ):
            visible_count += 1
        if visible_count != index + 1:
            raise ReplayOrderingFailure("future bar became visible before its availability event")
        replayed_closes.append(Decimal(bars[visible_count - 1].close.text))
    closes = tuple(replayed_closes)
    mean: Decimal | None
    variance: Decimal | None
    with localcontext(_DECIMAL_CONTEXT):
        returns = tuple(
            closes[index] / closes[index - 1] - Decimal(1) for index in range(1, len(closes))
        )
        if returns:
            mean = sum(returns, Decimal(0)) / Decimal(len(returns))
            variance = sum((value - mean) ** 2 for value in returns) / Decimal(len(returns))
        else:
            mean = None
            variance = None
    canonical_returns = tuple(_canonical_decimal(value) for value in returns)
    return ExperimentResultArtifact(
        request.result_artifact_id,
        _V1,
        request.run_id,
        _V1,
        run_input_fingerprint,
        request.authorization_ref,
        request.specification_ref,
        request.policy_ref,
        request.eligibility_ref,
        specification.normalized_manifest_ref,
        specification.normalized_lock_ref,
        _exact(engine_contract, engine_contract.engine_id, engine_contract.version),
        authorization.configuration_fingerprint,
        specification.random_seed,
        len(bars),
        bars[0].bar_open,
        bars[-1].bar_close,
        max(bar.availability_time for bar in bars),
        _canonical_decimal(min(closes)),
        _canonical_decimal(max(closes)),
        canonical_returns,
        None if mean is None else _canonical_decimal(mean),
        None if variance is None else _canonical_decimal(variance),
        fingerprint(canonical_returns),
        ValidationStatus.NOT_VALIDATED,
        DeploymentAuthorizationStatus.NOT_AUTHORIZED,
        ExecutionState.PLANNED_CLOSED,
        _V1,
    )


def run_authorized_experiment(
    request: ExperimentRunRequest,
    *,
    authorization: ExperimentAuthorizationRecord,
    specification: ExperimentSpecification,
    policy: ExperimentAuthorizationPolicy,
    eligibility: ResearchDatasetEligibilityRecord,
    eligibility_policy: ResearchDatasetEligibilityPolicy,
    admission: RealCsvAdmissionRecord,
    declaration: RealCsvSourceDeclaration,
    report: CsvImportReport,
    engine_contract: ExperimentReplayContract,
    repository: LocalDatasetRepository,
) -> ExperimentRunResult:
    """Execute one closed research engine; never validate, deploy, or trade."""
    _verify_authorization(
        request,
        authorization=authorization,
        specification=specification,
        policy=policy,
        eligibility=eligibility,
        eligibility_policy=eligibility_policy,
        admission=admission,
        declaration=declaration,
        report=report,
        engine_contract=engine_contract,
    )
    _require_market_statistics_scope(specification, engine_contract)
    bars = _select_replay_bars(specification, report)
    if request.completed_at < max(
        specification.knowledge_cutoff, max(bar.availability_time for bar in bars)
    ):
        raise ExperimentTimeWindowMismatch("run completion precedes governed knowledge")
    run_input = _run_input_fingerprint(request, authorization, specification, policy, eligibility)
    artifact = _result_artifact(
        request,
        authorization,
        specification,
        engine_contract,
        bars,
        run_input,
    )
    record = ExperimentRunRecord(
        request.run_id,
        _V1,
        request.authorization_ref,
        request.specification_ref,
        request.policy_ref,
        request.eligibility_ref,
        specification.normalized_manifest_ref,
        specification.normalized_lock_ref,
        request.engine_contract_ref,
        authorization.configuration_fingerprint,
        specification.random_seed,
        specification.observation_start,
        specification.observation_end,
        specification.knowledge_cutoff,
        run_input,
        _exact(artifact, artifact.artifact_id, artifact.version),
        ExperimentRunStatus.COMPLETED,
        request.completed_at,
        request.provenance_ref,
        ResearchExperimentExecutionStatus.RESEARCH_EXPERIMENT_EXECUTED,
        ValidationStatus.NOT_VALIDATED,
        DeploymentAuthorizationStatus.NOT_AUTHORIZED,
        ExecutionState.PLANNED_CLOSED,
        _V1,
    )
    verify_experiment_result_lineage(
        record=record,
        artifact=artifact,
        request=request,
        authorization=authorization,
        specification=specification,
        policy=policy,
        eligibility=eligibility,
        engine_contract=engine_contract,
        report=report,
    )
    writes = (
        repository.store(engine_contract),
        repository.store(artifact),
        repository.store(record),
    )
    return ExperimentRunResult(record, artifact, writes)


def verify_experiment_result_lineage(
    *,
    record: ExperimentRunRecord,
    artifact: ExperimentResultArtifact,
    request: ExperimentRunRequest,
    authorization: ExperimentAuthorizationRecord,
    specification: ExperimentSpecification,
    policy: ExperimentAuthorizationPolicy,
    eligibility: ResearchDatasetEligibilityRecord,
    engine_contract: ExperimentReplayContract,
    report: CsvImportReport,
) -> None:
    expected_input = _run_input_fingerprint(
        request, authorization, specification, policy, eligibility
    )
    if record.run_id != request.run_id or artifact.run_id != request.run_id:
        raise ExperimentResultLineageMismatch("result does not bind exact run identity")
    if (
        record.run_input_fingerprint != expected_input
        or artifact.run_input_fingerprint != expected_input
    ):
        raise ExperimentResultLineageMismatch("result run input fingerprint changed")
    if record.result_ref != _exact(artifact, artifact.artifact_id, artifact.version):
        raise ExperimentResultLineageMismatch("run does not bind exact result artifact")
    expected_artifact = _result_artifact(
        request,
        authorization,
        specification,
        engine_contract,
        _select_replay_bars(specification, report),
        expected_input,
    )
    if artifact != expected_artifact:
        raise ExperimentResultLineageMismatch("result values do not match exact replay inputs")
    refs = (
        request.authorization_ref,
        request.specification_ref,
        request.policy_ref,
        request.eligibility_ref,
        request.engine_contract_ref,
        specification.normalized_manifest_ref,
        specification.normalized_lock_ref,
    )
    if (
        record.authorization_ref,
        record.specification_ref,
        record.policy_ref,
        record.eligibility_ref,
        record.engine_contract_ref,
        record.normalized_manifest_ref,
        record.normalized_lock_ref,
    ) != refs or (
        artifact.authorization_ref,
        artifact.specification_ref,
        artifact.policy_ref,
        artifact.eligibility_ref,
        artifact.engine_contract_ref,
        artifact.normalized_manifest_ref,
        artifact.normalized_lock_ref,
    ) != refs:
        raise ExperimentResultLineageMismatch("run/result exact lineage references differ")
    if (
        record.configuration_fingerprint != authorization.configuration_fingerprint
        or record.random_seed != specification.random_seed
        or record.observation_start != specification.observation_start
        or record.observation_end != specification.observation_end
        or record.knowledge_cutoff != specification.knowledge_cutoff
        or record.completed_at != request.completed_at
        or record.provenance_ref != request.provenance_ref
    ):
        raise ExperimentResultLineageMismatch("run record does not preserve exact execution inputs")
