"""Strict typed canonical codecs for governed institutional records."""

from __future__ import annotations

import json
import re
from datetime import UTC, datetime
from typing import Any, Final, cast

from ai_quant_lab.core.data import (
    DataQualityState,
    DatasetLock,
    DatasetLockId,
    DatasetLockState,
    DatasetManifest,
    DecimalValue,
    InstrumentClass,
    InstrumentId,
    InstrumentIdentity,
    ObservationId,
    RawField,
    RawObservation,
    ReconciliationDisposition,
    SourceId,
    SourceIdentity,
    SourceType,
    TemporalCoordinates,
    TemporalPolicy,
    VenueId,
    VenueIdentity,
    VenueType,
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
from ai_quant_lab.core.integrated_research_workflow_contracts import (
    AIStrategyProposal,
    AIStrategyProposalStatus,
    IntegratedResearchWorkflowMode,
    IntegratedResearchWorkflowPlan,
    IntegratedResearchWorkflowResult,
    IntegratedResearchWorkflowRunRecord,
    IntegratedResearchWorkflowState,
    ProposalAuthorityState,
    ResearchHandoffPackage,
    ResearchHandoffReadiness,
    TradingViewResearchHandoffManifest,
    WorkflowReasonCode,
    WorkflowStage,
    WorkflowStageOutcome,
    WorkflowStageResult,
)
from ai_quant_lab.core.market_data import (
    AlignmentKind,
    BarFinality,
    BarTimestampMeaning,
    MarketBar,
    MarketBarId,
    MarketDataSchema,
    MarketDataSchemaId,
    NormalizedBarManifest,
    TimeframeId,
    TimeframeIdentity,
    TimeframeUnit,
    VolumeSemantic,
)
from ai_quant_lab.core.model import (
    AgentId,
    ArtifactEnvelope,
    ArtifactId,
    ArtifactLifecycle,
    AuditEvent,
    AuditEventId,
    AuditResult,
    AuthorityBindingId,
    CommandId,
    DatasetId,
    DecisionId,
    EvidenceEnvelope,
    EvidenceId,
    EvidenceState,
    ExecutionState,
    ExperimentId,
    FreshnessState,
    GovernedId,
    InvalidSerialization,
    MonitoringId,
    ObjectVersion,
    ProvenanceId,
    ProvenanceRecord,
    RunId,
    TraceabilityRef,
    TrialId,
    ValidationId,
    VersionedRef,
    canonical_json,
)
from ai_quant_lab.core.optimization_contracts import (
    CandidateEligibility,
    OptimizationCandidateDefinition,
    OptimizationCandidateResult,
    OptimizationMultiplicityPolicy,
    OptimizationObjective,
    OptimizationParameter,
    OptimizationParameterName,
    OptimizationParameterType,
    OptimizationPlan,
    OptimizationReasonCode,
    OptimizationRunRecord,
    OptimizationRunStatus,
    OptimizationSearchMethod,
    OptimizationSearchSpace,
    OptimizationSelectionResult,
    OptimizationTrialRecord,
    OptimizationTrialStatus,
    SelectionDecision,
)
from ai_quant_lab.core.pine_python_parity_contracts import (
    ParityMismatch,
    ParityMismatchType,
    ParityTolerancePolicy,
    PineEvidenceSourceFormat,
    PineExecutionAction,
    PineExecutionEvent,
    PineExecutionEvidence,
    PineExecutionSide,
    PineParityReasonCode,
    PineParitySemanticStatus,
    PinePythonParityDecision,
    PinePythonParityResult,
    PinePythonParityRunRecord,
)
from ai_quant_lab.core.pine_strategy_contracts import (
    PineDefaultQuantityType,
    PineIntakeReasonCode,
    PineIntakeStatus,
    PineLanguageVersion,
    PineScriptKind,
    PineSemanticParityStatus,
    PineStrategyIntakeRecord,
    PineStrategySourceArtifact,
    RepaintAssessmentStatus,
)
from ai_quant_lab.core.real_csv_contracts import (
    AcquisitionMethod,
    AvailabilitySemantics,
    CsvAdmissionStatus,
    CsvTrustState,
    DuplicatePolicy,
    MissingDataPolicy,
    OrderingPolicy,
    PriceDomain,
    RealCsvAdmissionRecord,
    RealCsvSourceDeclaration,
    ResearchEligibilityState,
    RetentionClassification,
    SourcePermissionState,
    TimestampSemantics,
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
from ai_quant_lab.core.robustness_validation_contracts import (
    CostPerturbationScenario,
    CostPerturbationSummary,
    MonteCarloPolicy,
    MonteCarloSummary,
    PerturbationPolicy,
    RobustnessDecision,
    RobustnessHoldoutEvidence,
    RobustnessMethod,
    RobustnessReasonCode,
    RobustnessRunStatus,
    RobustnessValidationPlan,
    RobustnessValidationResult,
    RobustnessValidationRunRecord,
    TemporalPartitionEvidence,
    TemporalPartitionRole,
    WalkForwardPolicy,
    WalkForwardSliceResult,
    WalkForwardSummary,
)
from ai_quant_lab.core.scientific_validation_contracts import (
    AlternativeHypothesis,
    HoldoutEvidenceStatus,
    HoldoutPolicy,
    MultiplicityPolicy,
    NullHypothesis,
    OutOfSampleEvidenceStatus,
    ScientificValidationBoundary,
    ScientificValidationDecision,
    ScientificValidationResult,
    UncertaintyMethod,
    ValidationMetric,
    ValidationPlan,
    ValidationReasonCode,
    ValidationRunRecord,
    ValidationRunStatus,
)
from ai_quant_lab.core.strategy_backtest_contracts import (
    BacktestResultArtifact,
    BacktestRunRecord,
    BacktestRunStatus,
    EquityPoint,
    SidePermission,
    SignalTiming,
    SimulatedExecutionTiming,
    SimulatedFill,
    SimulatedOrder,
    SimulatedOrderSide,
    SimulatedOrderStatus,
    SimulatedPositionState,
    SimulatedTrade,
    StrategyDefinition,
    StrategyModel,
)

REPRESENTATION_FORMAT: Final = "ai-quant-lab.canonical-json"
REPRESENTATION_VERSION: Final = 1
_TIMESTAMP = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{6}Z$")
_FINGERPRINT = re.compile(r"^sha256:[0-9a-f]{64}$")

type GovernedRecord = (
    ArtifactEnvelope
    | EvidenceEnvelope
    | ProvenanceRecord
    | AuditEvent
    | VenueIdentity
    | SourceIdentity
    | InstrumentIdentity
    | RawObservation
    | DatasetManifest
    | DatasetLock
    | TimeframeIdentity
    | MarketDataSchema
    | MarketBar
    | NormalizedBarManifest
    | RealCsvSourceDeclaration
    | RealCsvAdmissionRecord
    | ResearchDatasetEligibilityPolicy
    | ResearchDatasetEligibilityRecord
    | ExperimentSpecification
    | ExperimentAuthorizationPolicy
    | ExperimentAuthorizationRecord
    | ExperimentReplayContract
    | ExperimentResultArtifact
    | ExperimentRunRecord
    | StrategyDefinition
    | BacktestResultArtifact
    | BacktestRunRecord
    | ValidationPlan
    | ScientificValidationResult
    | ValidationRunRecord
    | RobustnessValidationPlan
    | RobustnessValidationResult
    | RobustnessValidationRunRecord
    | OptimizationSearchSpace
    | OptimizationPlan
    | OptimizationCandidateDefinition
    | OptimizationCandidateResult
    | OptimizationTrialRecord
    | OptimizationSelectionResult
    | OptimizationRunRecord
    | PineStrategySourceArtifact
    | PineStrategyIntakeRecord
    | ParityTolerancePolicy
    | PineExecutionEvidence
    | PinePythonParityResult
    | PinePythonParityRunRecord
    | AIStrategyProposal
    | IntegratedResearchWorkflowPlan
    | IntegratedResearchWorkflowResult
    | ResearchHandoffPackage
    | TradingViewResearchHandoffManifest
    | IntegratedResearchWorkflowRunRecord
)

_ID_TYPES: dict[str, type[GovernedId]] = {
    "agent": AgentId,
    "artifact": ArtifactId,
    "audit-event": AuditEventId,
    "authority-binding": AuthorityBindingId,
    "command": CommandId,
    "dataset": DatasetId,
    "decision": DecisionId,
    "evidence": EvidenceId,
    "experiment": ExperimentId,
    "monitoring": MonitoringId,
    "provenance": ProvenanceId,
    "run": RunId,
    "trial": TrialId,
    "validation": ValidationId,
    "source": SourceId,
    "venue": VenueId,
    "instrument": InstrumentId,
    "observation": ObservationId,
    "dataset-lock": DatasetLockId,
    "timeframe": TimeframeId,
    "market-data-schema": MarketDataSchemaId,
    "market-bar": MarketBarId,
}
_SUPPORTED_TYPES: dict[type[GovernedRecord], str] = {
    ArtifactEnvelope: "ArtifactEnvelope",
    EvidenceEnvelope: "EvidenceEnvelope",
    ProvenanceRecord: "ProvenanceRecord",
    AuditEvent: "AuditEvent",
    VenueIdentity: "VenueIdentity",
    SourceIdentity: "SourceIdentity",
    InstrumentIdentity: "InstrumentIdentity",
    RawObservation: "RawObservation",
    DatasetManifest: "DatasetManifest",
    DatasetLock: "DatasetLock",
    TimeframeIdentity: "TimeframeIdentity",
    MarketDataSchema: "MarketDataSchema",
    MarketBar: "MarketBar",
    NormalizedBarManifest: "NormalizedBarManifest",
    RealCsvSourceDeclaration: "RealCsvSourceDeclaration",
    RealCsvAdmissionRecord: "RealCsvAdmissionRecord",
    ResearchDatasetEligibilityPolicy: "ResearchDatasetEligibilityPolicy",
    ResearchDatasetEligibilityRecord: "ResearchDatasetEligibilityRecord",
    ExperimentSpecification: "ExperimentSpecification",
    ExperimentAuthorizationPolicy: "ExperimentAuthorizationPolicy",
    ExperimentAuthorizationRecord: "ExperimentAuthorizationRecord",
    ExperimentReplayContract: "ExperimentReplayContract",
    ExperimentResultArtifact: "ExperimentResultArtifact",
    ExperimentRunRecord: "ExperimentRunRecord",
    StrategyDefinition: "StrategyDefinition",
    BacktestResultArtifact: "BacktestResultArtifact",
    BacktestRunRecord: "BacktestRunRecord",
    ValidationPlan: "ValidationPlan",
    ScientificValidationResult: "ScientificValidationResult",
    ValidationRunRecord: "ValidationRunRecord",
    RobustnessValidationPlan: "RobustnessValidationPlan",
    RobustnessValidationResult: "RobustnessValidationResult",
    RobustnessValidationRunRecord: "RobustnessValidationRunRecord",
    OptimizationSearchSpace: "OptimizationSearchSpace",
    OptimizationPlan: "OptimizationPlan",
    OptimizationCandidateDefinition: "OptimizationCandidateDefinition",
    OptimizationCandidateResult: "OptimizationCandidateResult",
    OptimizationTrialRecord: "OptimizationTrialRecord",
    OptimizationSelectionResult: "OptimizationSelectionResult",
    OptimizationRunRecord: "OptimizationRunRecord",
    PineStrategySourceArtifact: "PineStrategySourceArtifact",
    PineStrategyIntakeRecord: "PineStrategyIntakeRecord",
    ParityTolerancePolicy: "ParityTolerancePolicy",
    PineExecutionEvidence: "PineExecutionEvidence",
    PinePythonParityResult: "PinePythonParityResult",
    PinePythonParityRunRecord: "PinePythonParityRunRecord",
    AIStrategyProposal: "AIStrategyProposal",
    IntegratedResearchWorkflowPlan: "IntegratedResearchWorkflowPlan",
    IntegratedResearchWorkflowResult: "IntegratedResearchWorkflowResult",
    ResearchHandoffPackage: "ResearchHandoffPackage",
    TradingViewResearchHandoffManifest: "TradingViewResearchHandoffManifest",
    IntegratedResearchWorkflowRunRecord: "IntegratedResearchWorkflowRunRecord",
}


def _reject_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise InvalidSerialization(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def _strict_object(value: Any, required: set[str], name: str) -> dict[str, Any]:
    if not isinstance(value, dict) or not all(isinstance(key, str) for key in value):
        raise InvalidSerialization(f"{name} must be an object")
    keys = set(value)
    if keys != required:
        missing = sorted(required - keys)
        unknown = sorted(keys - required)
        raise InvalidSerialization(f"{name} fields mismatch; missing={missing}, unknown={unknown}")
    return cast(dict[str, Any], value)


def _text(value: Any, field: str) -> str:
    if not isinstance(value, str):
        raise InvalidSerialization(f"{field} must be text")
    return value


def _optional_text(value: Any, field: str) -> str | None:
    return None if value is None else _text(value, field)


def _version(value: Any, field: str) -> ObjectVersion:
    if isinstance(value, bool) or not isinstance(value, int):
        raise InvalidSerialization(f"{field} must be a positive integer version")
    return ObjectVersion(value)


def _timestamp(value: Any, field: str) -> datetime:
    text = _text(value, field)
    if not _TIMESTAMP.fullmatch(text):
        raise InvalidSerialization(f"{field} must use UTC microsecond Z format")
    try:
        parsed = datetime.strptime(text, "%Y-%m-%dT%H:%M:%S.%fZ").replace(tzinfo=UTC)
    except ValueError as exc:
        raise InvalidSerialization(f"{field} is invalid") from exc
    return parsed


def _id(value: Any, field: str) -> GovernedId:
    text = _text(value, field)
    namespace = text.partition(":")[0]
    id_type = _ID_TYPES.get(namespace)
    if id_type is None:
        raise InvalidSerialization(f"{field} has unsupported identifier namespace")
    return id_type.parse(text)


def _typed_id(value: Any, expected: type[GovernedId], field: str) -> GovernedId:
    identifier = _id(value, field)
    if not isinstance(identifier, expected):
        raise InvalidSerialization(f"{field} requires {expected.namespace} namespace")
    return identifier


def _ref_payload(reference: VersionedRef) -> dict[str, Any]:
    return {"object_id": str(reference.object_id), "version": reference.version.number}


def _ref(value: Any, field: str) -> VersionedRef:
    item = _strict_object(value, {"object_id", "version"}, field)
    return VersionedRef(
        _id(item["object_id"], f"{field}.object_id"),
        _version(item["version"], f"{field}.version"),
    )


def _optional_ref(value: Any, field: str) -> VersionedRef | None:
    return None if value is None else _ref(value, field)


def _refs(value: Any, field: str) -> tuple[VersionedRef, ...]:
    if not isinstance(value, list):
        raise InvalidSerialization(f"{field} must be an array")
    return tuple(_ref(item, f"{field}[]") for item in value)


def _metadata(value: Any, field: str) -> tuple[tuple[str, str], ...]:
    if not isinstance(value, list):
        raise InvalidSerialization(f"{field} must be an array")
    result: list[tuple[str, str]] = []
    for item in value:
        if not isinstance(item, list) or len(item) != 2:
            raise InvalidSerialization(f"{field} entries must be two-element arrays")
        key, entry = item
        if not isinstance(key, str) or not isinstance(entry, str):
            raise InvalidSerialization(f"{field} entries must contain text")
        result.append((key, entry))
    return tuple(result)


def _strings(value: Any, field: str) -> tuple[str, ...]:
    if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
        raise InvalidSerialization(f"{field} must be an array of text")
    return tuple(value)


def _integer(value: Any, field: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise InvalidSerialization(f"{field} must be an integer")
    return value


def _boolean(value: Any, field: str) -> bool:
    if not isinstance(value, bool):
        raise InvalidSerialization(f"{field} must be boolean")
    return value


def _trace_ref_payload(reference: TraceabilityRef) -> dict[str, Any]:
    return {
        "object_id": str(reference.object_id),
        "version": reference.version.number,
        "expected_fingerprint": reference.expected_fingerprint,
    }


def _partition_payload(value: TemporalPartitionEvidence) -> dict[str, Any]:
    return {
        "partition_id": str(value.partition_id),
        "role": value.role.value,
        "start_index": value.start_index,
        "end_index": value.end_index,
        "bar_refs": [_trace_ref_payload(item) for item in value.bar_refs],
    }


def _walk_forward_slice_payload(value: WalkForwardSliceResult) -> dict[str, Any]:
    return {
        "slice_id": str(value.slice_id),
        "train_partition": _partition_payload(value.train_partition),
        "test_partition": _partition_payload(value.test_partition),
        "trade_count": value.trade_count,
        "total_return": value.total_return,
        "net_pnl": value.net_pnl,
        "max_drawdown": value.max_drawdown,
        "decision": value.decision.value,
    }


def _walk_forward_payload(value: WalkForwardSummary) -> dict[str, Any]:
    return {
        "slices": [_walk_forward_slice_payload(item) for item in value.slices],
        "valid_window_count": value.valid_window_count,
        "positive_window_ratio": value.positive_window_ratio,
        "median_test_return": value.median_test_return,
        "worst_test_return": value.worst_test_return,
        "aggregate_test_return": value.aggregate_test_return,
        "maximum_test_drawdown": value.maximum_test_drawdown,
        "minimum_trade_count": value.minimum_trade_count,
        "decision": value.decision.value,
        "reason_codes": [item.value for item in value.reason_codes],
    }


def _monte_carlo_payload(value: MonteCarloSummary) -> dict[str, Any]:
    return {
        "policy": value.policy.value,
        "iterations": value.iterations,
        "seed": value.seed,
        "median_terminal_return": value.median_terminal_return,
        "lower_terminal_return": value.lower_terminal_return,
        "upper_terminal_return": value.upper_terminal_return,
        "worst_observed_drawdown": value.worst_observed_drawdown,
        "positive_terminal_fraction": value.positive_terminal_fraction,
        "decision": value.decision.value,
        "reason_codes": [item.value for item in value.reason_codes],
    }


def _cost_perturbation_payload(value: CostPerturbationSummary) -> dict[str, Any]:
    return {
        "policy": value.policy.value,
        "scenarios": [
            {
                "scenario_id": str(item.scenario_id),
                "commission_multiplier": item.commission_multiplier,
                "derived_commission_semantics": item.derived_commission_semantics.value,
                "derived_commission_bps": item.derived_commission_bps,
                "specification_ref": _trace_ref_payload(item.specification_ref),
                "authorization_ref": _trace_ref_payload(item.authorization_ref),
                "backtest_result_ref": (
                    None
                    if item.backtest_result_ref is None
                    else _trace_ref_payload(item.backtest_result_ref)
                ),
                "total_return": item.total_return,
                "net_pnl": item.net_pnl,
                "max_drawdown": item.max_drawdown,
                "trade_count": item.trade_count,
                "decision": item.decision.value,
                "reason_codes": [reason.value for reason in item.reason_codes],
            }
            for item in value.scenarios
        ],
        "decision": value.decision.value,
        "reason_codes": [item.value for item in value.reason_codes],
    }


def _trace_ref(value: Any, field: str) -> TraceabilityRef:
    item = _strict_object(value, {"object_id", "version", "expected_fingerprint"}, field)
    fingerprint = item["expected_fingerprint"]
    if fingerprint is not None and (
        not isinstance(fingerprint, str) or not _FINGERPRINT.fullmatch(fingerprint)
    ):
        raise InvalidSerialization(f"{field}.expected_fingerprint is invalid")
    return TraceabilityRef(
        _id(item["object_id"], f"{field}.object_id"),
        _version(item["version"], f"{field}.version"),
        fingerprint,
    )


def _optional_trace_ref(value: Any, field: str) -> TraceabilityRef | None:
    return None if value is None else _trace_ref(value, field)


def _trace_refs(value: Any, field: str) -> tuple[TraceabilityRef, ...]:
    if not isinstance(value, list):
        raise InvalidSerialization(f"{field} must be an array")
    return tuple(_trace_ref(item, f"{field}[]") for item in value)


def _timestamp_payload(value: datetime) -> str:
    return value.isoformat(timespec="microseconds").replace("+00:00", "Z")


def _raw_value_payload(value: str | int | bool | DecimalValue | None) -> dict[str, Any]:
    if value is None:
        return {"kind": "null", "value": None}
    if isinstance(value, bool):
        return {"kind": "boolean", "value": value}
    if isinstance(value, int):
        return {"kind": "integer", "value": value}
    if isinstance(value, DecimalValue):
        return {"kind": "decimal", "value": value.text}
    if isinstance(value, str):
        return {"kind": "text", "value": value}
    raise InvalidSerialization("unsupported raw scalar")


def _raw_value(value: Any, field: str) -> str | int | bool | DecimalValue | None:
    item = _strict_object(value, {"kind", "value"}, field)
    kind = _text(item["kind"], f"{field}.kind")
    scalar = item["value"]
    if kind == "null" and scalar is None:
        return None
    if kind == "boolean" and isinstance(scalar, bool):
        return scalar
    if kind == "integer" and isinstance(scalar, int) and not isinstance(scalar, bool):
        return scalar
    if kind == "text" and isinstance(scalar, str):
        return scalar
    if kind == "decimal" and isinstance(scalar, str):
        return DecimalValue(scalar)
    raise InvalidSerialization(f"{field} has invalid typed raw value")


def _simulated_order_payload(record: SimulatedOrder) -> dict[str, Any]:
    return {
        "order_id": str(record.order_id),
        "side": record.side.value,
        "notional": record.notional,
        "signal_time": _timestamp_payload(record.signal_time),
        "submitted_time": _timestamp_payload(record.submitted_time),
        "eligible_fill_time": _timestamp_payload(record.eligible_fill_time),
        "source_bar_ref": _trace_ref_payload(record.source_bar_ref),
        "fill_bar_ref": _trace_ref_payload(record.fill_bar_ref),
        "strategy_ref": _trace_ref_payload(record.strategy_ref),
        "run_id": str(record.run_id),
        "run_version": record.run_version.number,
        "status": record.status.value,
    }


def _simulated_fill_payload(record: SimulatedFill) -> dict[str, Any]:
    return {
        "fill_id": str(record.fill_id),
        "order_id": str(record.order_id),
        "side": record.side.value,
        "bar_ref": _trace_ref_payload(record.bar_ref),
        "fill_time": _timestamp_payload(record.fill_time),
        "reference_price": record.reference_price,
        "execution_price": record.execution_price,
        "quantity": record.quantity,
        "fill_notional": record.fill_notional,
        "commission": record.commission,
        "slippage_cost": record.slippage_cost,
    }


def _simulated_trade_payload(record: SimulatedTrade) -> dict[str, Any]:
    return {
        "trade_id": str(record.trade_id),
        "entry_fill_id": str(record.entry_fill_id),
        "exit_fill_id": str(record.exit_fill_id),
        "quantity": record.quantity,
        "entry_price": record.entry_price,
        "exit_price": record.exit_price,
        "gross_pnl": record.gross_pnl,
        "commission": record.commission,
        "slippage_cost": record.slippage_cost,
        "net_pnl": record.net_pnl,
        "entry_time": _timestamp_payload(record.entry_time),
        "exit_time": _timestamp_payload(record.exit_time),
        "strategy_ref": _trace_ref_payload(record.strategy_ref),
        "run_id": str(record.run_id),
        "run_version": record.run_version.number,
    }


def _equity_point_payload(record: EquityPoint) -> dict[str, Any]:
    return {
        "event_time": _timestamp_payload(record.event_time),
        "bar_ref": _trace_ref_payload(record.bar_ref),
        "cash": record.cash,
        "position_quantity": record.position_quantity,
        "position_value": record.position_value,
        "unrealized_pnl": record.unrealized_pnl,
        "realized_pnl": record.realized_pnl,
        "equity": record.equity,
    }


def _payload(record: GovernedRecord) -> dict[str, Any]:
    if isinstance(record, ArtifactEnvelope):
        return {
            "artifact_id": str(record.artifact_id),
            "artifact_type": record.artifact_type,
            "version": record.version.number,
            "created_at": record.created_at.isoformat(timespec="microseconds").replace(
                "+00:00", "Z"
            ),
            "producer_id": str(record.producer_id),
            "provenance_id": str(record.provenance_id),
            "contract_version": record.contract_version.number,
            "lifecycle": record.lifecycle.value,
            "content_fingerprint": record.content_fingerprint,
            "parent_refs": [_ref_payload(item) for item in record.parent_refs],
            "metadata": [list(item) for item in record.metadata],
        }
    if isinstance(record, EvidenceEnvelope):
        return {
            "evidence_id": str(record.evidence_id),
            "evidence_type": record.evidence_type,
            "source_artifact": _ref_payload(record.source_artifact),
            "provenance_id": str(record.provenance_id),
            "created_at": record.created_at.isoformat(timespec="microseconds").replace(
                "+00:00", "Z"
            ),
            "scope": record.scope,
            "admissibility": record.admissibility.value,
            "freshness": record.freshness.value,
            "supersedes": None if record.supersedes is None else _ref_payload(record.supersedes),
            "invalidates": [_ref_payload(item) for item in record.invalidates],
            "metadata": [list(item) for item in record.metadata],
        }
    if isinstance(record, ProvenanceRecord):
        return {
            "provenance_id": str(record.provenance_id),
            "producer_id": str(record.producer_id),
            "produced_at": record.produced_at.isoformat(timespec="microseconds").replace(
                "+00:00", "Z"
            ),
            "process": record.process,
            "input_refs": [_ref_payload(item) for item in record.input_refs],
            "transformation_ref": (
                None
                if record.transformation_ref is None
                else _ref_payload(record.transformation_ref)
            ),
            "metadata": [list(item) for item in record.metadata],
        }
    if isinstance(record, AuditEvent):
        return {
            "event_id": str(record.event_id),
            "actor_id": str(record.actor_id),
            "action": record.action,
            "target": _ref_payload(record.target),
            "occurred_at": record.occurred_at.isoformat(timespec="microseconds").replace(
                "+00:00", "Z"
            ),
            "result": record.result.value,
            "context": [list(item) for item in record.context],
        }
    if isinstance(record, VenueIdentity):
        return {
            "venue_id": str(record.venue_id),
            "version": record.version.number,
            "name": record.name,
            "venue_type": record.venue_type.value,
            "jurisdiction": record.jurisdiction,
            "contract_version": record.contract_version.number,
        }
    if isinstance(record, SourceIdentity):
        return {
            "source_id": str(record.source_id),
            "version": record.version.number,
            "provider": record.provider,
            "source_type": record.source_type.value,
            "feed": record.feed,
            "source_version": record.source_version,
            "venue_ref": (
                None if record.venue_ref is None else _trace_ref_payload(record.venue_ref)
            ),
            "contract_version": record.contract_version.number,
        }
    if isinstance(record, InstrumentIdentity):
        return {
            "instrument_id": str(record.instrument_id),
            "version": record.version.number,
            "symbol": record.symbol,
            "instrument_class": record.instrument_class.value,
            "base_asset": record.base_asset,
            "quote_asset": record.quote_asset,
            "settlement_asset": record.settlement_asset,
            "venue_ref": (
                None if record.venue_ref is None else _trace_ref_payload(record.venue_ref)
            ),
            "contract_version": record.contract_version.number,
        }
    if isinstance(record, RawObservation):
        return {
            "observation_id": str(record.observation_id),
            "version": record.version.number,
            "source_ref": _trace_ref_payload(record.source_ref),
            "instrument_ref": _trace_ref_payload(record.instrument_ref),
            "temporal": {
                "event_time": _timestamp_payload(record.temporal.event_time),
                "availability_time": _timestamp_payload(record.temporal.availability_time),
                "ingestion_time": _timestamp_payload(record.temporal.ingestion_time),
                "policy": record.temporal.policy.value,
            },
            "payload": [
                {"name": field.name, "value": _raw_value_payload(field.value)}
                for field in record.payload
            ],
            "provenance_ref": _trace_ref_payload(record.provenance_ref),
            "source_sequence": record.source_sequence,
            "quality": record.quality.value,
            "reconciliation": record.reconciliation.value,
            "supersedes": (
                None if record.supersedes is None else _trace_ref_payload(record.supersedes)
            ),
            "contract_version": record.contract_version.number,
        }
    if isinstance(record, DatasetManifest):
        return {
            "dataset_id": str(record.dataset_id),
            "version": record.version.number,
            "created_at": _timestamp_payload(record.created_at),
            "observation_refs": [_trace_ref_payload(item) for item in record.observation_refs],
            "source_refs": [_trace_ref_payload(item) for item in record.source_refs],
            "instrument_refs": [_trace_ref_payload(item) for item in record.instrument_refs],
            "event_time_start": _timestamp_payload(record.event_time_start),
            "event_time_end": _timestamp_payload(record.event_time_end),
            "provenance_ref": _trace_ref_payload(record.provenance_ref),
            "contract_version": record.contract_version.number,
            "membership_policy": record.membership_policy,
        }
    if isinstance(record, DatasetLock):
        return {
            "lock_id": str(record.lock_id),
            "version": record.version.number,
            "dataset_ref": _trace_ref_payload(record.dataset_ref),
            "manifest_ref": _trace_ref_payload(record.manifest_ref),
            "locked_at": _timestamp_payload(record.locked_at),
            "temporal_cutoff": _timestamp_payload(record.temporal_cutoff),
            "provenance_ref": _trace_ref_payload(record.provenance_ref),
            "state": record.state.value,
            "contract_version": record.contract_version.number,
        }
    if isinstance(record, TimeframeIdentity):
        return {
            "timeframe_id": str(record.timeframe_id),
            "version": record.version.number,
            "unit": record.unit.value,
            "count": record.count,
            "alignment": record.alignment.value,
            "contract_version": record.contract_version.number,
        }
    if isinstance(record, MarketDataSchema):
        return {
            "schema_id": str(record.schema_id),
            "version": record.version.number,
            "timeframe_ref": _trace_ref_payload(record.timeframe_ref),
            "timestamp_meaning": record.timestamp_meaning.value,
            "open_time_field": record.open_time_field,
            "close_time_field": record.close_time_field,
            "open_field": record.open_field,
            "high_field": record.high_field,
            "low_field": record.low_field,
            "close_field": record.close_field,
            "volume_field": record.volume_field,
            "finality_field": record.finality_field,
            "volume_semantic": record.volume_semantic.value,
            "contract_version": record.contract_version.number,
        }
    if isinstance(record, MarketBar):
        return {
            "bar_id": str(record.bar_id),
            "version": record.version.number,
            "source_ref": _trace_ref_payload(record.source_ref),
            "instrument_ref": _trace_ref_payload(record.instrument_ref),
            "timeframe_ref": _trace_ref_payload(record.timeframe_ref),
            "schema_ref": _trace_ref_payload(record.schema_ref),
            "normalization_version": record.normalization_version.number,
            "bar_open": _timestamp_payload(record.bar_open),
            "bar_close": _timestamp_payload(record.bar_close),
            "availability_time": _timestamp_payload(record.availability_time),
            "ingestion_time": _timestamp_payload(record.ingestion_time),
            "open": record.open.text,
            "high": record.high.text,
            "low": record.low.text,
            "close": record.close.text,
            "volume": None if record.volume is None else record.volume.text,
            "volume_semantic": record.volume_semantic.value,
            "finality": record.finality.value,
            "source_observation_ref": _trace_ref_payload(record.source_observation_ref),
            "provenance_ref": _trace_ref_payload(record.provenance_ref),
            "supersedes": None
            if record.supersedes is None
            else _trace_ref_payload(record.supersedes),
            "contract_version": record.contract_version.number,
        }
    if isinstance(record, NormalizedBarManifest):
        return {
            "dataset_id": str(record.dataset_id),
            "version": record.version.number,
            "created_at": _timestamp_payload(record.created_at),
            "bar_refs": [_trace_ref_payload(item) for item in record.bar_refs],
            "source_refs": [_trace_ref_payload(item) for item in record.source_refs],
            "instrument_refs": [_trace_ref_payload(item) for item in record.instrument_refs],
            "timeframe_refs": [_trace_ref_payload(item) for item in record.timeframe_refs],
            "schema_ref": _trace_ref_payload(record.schema_ref),
            "normalization_version": record.normalization_version.number,
            "raw_dataset_lock_ref": _trace_ref_payload(record.raw_dataset_lock_ref),
            "provenance_ref": _trace_ref_payload(record.provenance_ref),
            "contract_version": record.contract_version.number,
            "membership_policy": record.membership_policy,
        }
    if isinstance(record, RealCsvSourceDeclaration):
        return {
            "provenance_id": str(record.provenance_id),
            "version": record.version.number,
            "source_ref": _trace_ref_payload(record.source_ref),
            "instrument_ref": _trace_ref_payload(record.instrument_ref),
            "timeframe_ref": _trace_ref_payload(record.timeframe_ref),
            "schema_ref": _trace_ref_payload(record.schema_ref),
            "provider_name": record.provider_name,
            "acquisition_method": record.acquisition_method.value,
            "declared_market": record.declared_market,
            "declared_acquisition_time": None
            if record.declared_acquisition_time is None
            else _timestamp_payload(record.declared_acquisition_time),
            "timestamp_semantics": record.timestamp_semantics.value,
            "availability_semantics": record.availability_semantics.value,
            "timezone_rule": record.timezone_rule,
            "column_mapping": [list(item) for item in record.column_mapping],
            "price_domain": record.price_domain.value,
            "ohlc_semantics": record.ohlc_semantics,
            "volume_semantics": record.volume_semantics.value,
            "finality_assumptions": record.finality_assumptions,
            "missing_data_policy": record.missing_data_policy.value,
            "duplicate_policy": record.duplicate_policy.value,
            "ordering_policy": record.ordering_policy.value,
            "permission_state": record.permission_state.value,
            "license_reference": record.license_reference,
            "retention_classification": record.retention_classification.value,
            "deletion_restriction": record.deletion_restriction,
            "redistribution_restriction": record.redistribution_restriction,
            "operator_id": str(record.operator_id),
            "provenance_note": record.provenance_note,
            "contract_version": record.contract_version.number,
        }
    if isinstance(record, RealCsvAdmissionRecord):
        return {
            "admission_id": str(record.admission_id),
            "version": record.version.number,
            "source_declaration_ref": _trace_ref_payload(record.source_declaration_ref),
            "original_filename": record.original_filename,
            "bounded_relative_path": record.bounded_relative_path,
            "file_sha256": record.file_sha256,
            "file_size": record.file_size,
            "ingestion_time": _timestamp_payload(record.ingestion_time),
            "parser_contract_version": record.parser_contract_version.number,
            "canonical_codec_version": record.canonical_codec_version.number,
            "ingestion_configuration_fingerprint": record.ingestion_configuration_fingerprint,
            "row_count": record.row_count,
            "status": record.status.value,
            "findings": list(record.findings),
            "raw_manifest_ref": None
            if record.raw_manifest_ref is None
            else _trace_ref_payload(record.raw_manifest_ref),
            "raw_lock_ref": None
            if record.raw_lock_ref is None
            else _trace_ref_payload(record.raw_lock_ref),
            "normalized_manifest_ref": None
            if record.normalized_manifest_ref is None
            else _trace_ref_payload(record.normalized_manifest_ref),
            "normalized_lock_ref": None
            if record.normalized_lock_ref is None
            else _trace_ref_payload(record.normalized_lock_ref),
            "trust_state": record.trust_state.value,
            "research_eligibility": record.research_eligibility.value,
            "contract_version": record.contract_version.number,
        }
    if isinstance(record, ResearchDatasetEligibilityPolicy):
        return {
            "policy_id": str(record.policy_id),
            "version": record.version.number,
            "accepted_permission_states": [
                item.value for item in record.accepted_permission_states
            ],
            "accepted_retention_classifications": [
                item.value for item in record.accepted_retention_classifications
            ],
            "required_timestamp_semantics": record.required_timestamp_semantics.value,
            "required_availability_semantics": record.required_availability_semantics.value,
            "accepted_missing_data_policies": [
                item.value for item in record.accepted_missing_data_policies
            ],
            "accepted_duplicate_policies": [
                item.value for item in record.accepted_duplicate_policies
            ],
            "accepted_ordering_policies": [
                item.value for item in record.accepted_ordering_policies
            ],
            "calendar_semantics": record.calendar_semantics.value,
            "knowledge_cutoff": _timestamp_payload(record.knowledge_cutoff),
            "minimum_row_count": record.minimum_row_count,
            "maximum_rejected_rows": record.maximum_rejected_rows,
            "maximum_quarantined_observations": record.maximum_quarantined_observations,
            "maximum_gap_findings": record.maximum_gap_findings,
            "maximum_missing_intervals": record.maximum_missing_intervals,
            "require_complete_bars": record.require_complete_bars,
            "allow_restricted_redistribution_for_local_research": (
                record.allow_restricted_redistribution_for_local_research
            ),
            "policy_owner_id": str(record.policy_owner_id),
            "contract_version": record.contract_version.number,
        }
    if isinstance(record, ResearchDatasetEligibilityRecord):
        return {
            "eligibility_id": str(record.eligibility_id),
            "version": record.version.number,
            "admission_ref": _trace_ref_payload(record.admission_ref),
            "source_declaration_ref": _trace_ref_payload(record.source_declaration_ref),
            "source_ref": _trace_ref_payload(record.source_ref),
            "instrument_ref": _trace_ref_payload(record.instrument_ref),
            "timeframe_ref": _trace_ref_payload(record.timeframe_ref),
            "schema_ref": _trace_ref_payload(record.schema_ref),
            "raw_manifest_ref": None
            if record.raw_manifest_ref is None
            else _trace_ref_payload(record.raw_manifest_ref),
            "raw_lock_ref": None
            if record.raw_lock_ref is None
            else _trace_ref_payload(record.raw_lock_ref),
            "normalized_manifest_ref": None
            if record.normalized_manifest_ref is None
            else _trace_ref_payload(record.normalized_manifest_ref),
            "normalized_lock_ref": None
            if record.normalized_lock_ref is None
            else _trace_ref_payload(record.normalized_lock_ref),
            "policy_ref": _trace_ref_payload(record.policy_ref),
            "quality_context_fingerprint": record.quality_context_fingerprint,
            "status": record.status.value,
            "findings": list(record.findings),
            "decision_time": _timestamp_payload(record.decision_time),
            "decision_actor_id": str(record.decision_actor_id),
            "trust_state": record.trust_state.value,
            "research_boundary": record.research_boundary.value,
            "experiment_authorization": record.experiment_authorization.value,
            "validation_status": record.validation_status.value,
            "deployment_authorization": record.deployment_authorization.value,
            "execution_state": record.execution_state.value,
            "contract_version": record.contract_version.number,
        }
    if isinstance(record, ExperimentSpecification):
        return {
            "experiment_id": str(record.experiment_id),
            "version": record.version.number,
            "eligibility_ref": _trace_ref_payload(record.eligibility_ref),
            "normalized_manifest_ref": _trace_ref_payload(record.normalized_manifest_ref),
            "normalized_lock_ref": _trace_ref_payload(record.normalized_lock_ref),
            "family": record.family.value,
            "research_objective": record.research_objective,
            "hypothesis_id": str(record.hypothesis_id),
            "configuration": [list(item) for item in record.configuration],
            "random_seed": record.random_seed,
            "observation_start": _timestamp_payload(record.observation_start),
            "observation_end": _timestamp_payload(record.observation_end),
            "knowledge_cutoff": _timestamp_payload(record.knowledge_cutoff),
            "no_lookahead": record.no_lookahead.value,
            "warmup_bars": record.warmup_bars,
            "commission_semantics": record.commission_semantics.value,
            "commission_bps": record.commission_bps,
            "slippage_semantics": record.slippage_semantics.value,
            "slippage_bps": record.slippage_bps,
            "funding_semantics": record.funding_semantics.value,
            "funding_bps": record.funding_bps,
            "calendar_semantics": record.calendar_semantics.value,
            "sizing_semantics": record.sizing_semantics.value,
            "capital_notional_minor": record.capital_notional_minor,
            "engine_contract_ref": _trace_ref_payload(record.engine_contract_ref),
            "requested_metrics": list(record.requested_metrics),
            "requested_outputs": list(record.requested_outputs),
            "proposer_id": str(record.proposer_id),
            "provenance_ref": _trace_ref_payload(record.provenance_ref),
            "contract_version": record.contract_version.number,
        }
    if isinstance(record, ExperimentAuthorizationPolicy):
        return {
            "policy_id": str(record.policy_id),
            "version": record.version.number,
            "allowed_families": [item.value for item in record.allowed_families],
            "required_no_lookahead": record.required_no_lookahead.value,
            "accepted_calendars": [item.value for item in record.accepted_calendars],
            "require_explicit_commission": record.require_explicit_commission,
            "require_explicit_slippage": record.require_explicit_slippage,
            "require_explicit_funding": record.require_explicit_funding,
            "require_position_sizing": record.require_position_sizing,
            "maximum_window_days": record.maximum_window_days,
            "minimum_seed": record.minimum_seed,
            "maximum_seed": record.maximum_seed,
            "supported_engine_refs": [
                _trace_ref_payload(item) for item in record.supported_engine_refs
            ],
            "require_verified_actor_authority": record.require_verified_actor_authority,
            "policy_owner_id": str(record.policy_owner_id),
            "contract_version": record.contract_version.number,
        }
    if isinstance(record, ExperimentAuthorizationRecord):
        return {
            "authorization_id": str(record.authorization_id),
            "version": record.version.number,
            "specification_ref": _trace_ref_payload(record.specification_ref),
            "eligibility_ref": _trace_ref_payload(record.eligibility_ref),
            "policy_ref": _trace_ref_payload(record.policy_ref),
            "normalized_manifest_ref": _trace_ref_payload(record.normalized_manifest_ref),
            "normalized_lock_ref": _trace_ref_payload(record.normalized_lock_ref),
            "configuration_fingerprint": record.configuration_fingerprint,
            "status": record.status.value,
            "findings": list(record.findings),
            "decision_time": _timestamp_payload(record.decision_time),
            "decision_actor_id": str(record.decision_actor_id),
            "lifecycle": record.lifecycle.value,
            "validation_status": record.validation_status.value,
            "deployment_authorization": record.deployment_authorization.value,
            "execution_state": record.execution_state.value,
            "contract_version": record.contract_version.number,
        }
    if isinstance(record, ExperimentReplayContract):
        return {
            "engine_id": str(record.engine_id),
            "version": record.version.number,
            "family": record.family.value,
            "no_lookahead": record.no_lookahead.value,
            "ordering": record.ordering.value,
            "numeric_semantics": record.numeric_semantics.value,
            "decimal_precision": record.decimal_precision,
            "supported_metrics": list(record.supported_metrics),
            "supported_outputs": list(record.supported_outputs),
            "contract_version": record.contract_version.number,
        }
    if isinstance(record, ExperimentResultArtifact):
        return {
            "artifact_id": str(record.artifact_id),
            "version": record.version.number,
            "run_id": str(record.run_id),
            "run_version": record.run_version.number,
            "run_input_fingerprint": record.run_input_fingerprint,
            "authorization_ref": _trace_ref_payload(record.authorization_ref),
            "specification_ref": _trace_ref_payload(record.specification_ref),
            "policy_ref": _trace_ref_payload(record.policy_ref),
            "eligibility_ref": _trace_ref_payload(record.eligibility_ref),
            "normalized_manifest_ref": _trace_ref_payload(record.normalized_manifest_ref),
            "normalized_lock_ref": _trace_ref_payload(record.normalized_lock_ref),
            "engine_contract_ref": _trace_ref_payload(record.engine_contract_ref),
            "configuration_fingerprint": record.configuration_fingerprint,
            "random_seed": record.random_seed,
            "observation_count": record.observation_count,
            "first_event_time": _timestamp_payload(record.first_event_time),
            "last_event_time": _timestamp_payload(record.last_event_time),
            "last_knowledge_time": _timestamp_payload(record.last_knowledge_time),
            "close_min": record.close_min,
            "close_max": record.close_max,
            "simple_returns": list(record.simple_returns),
            "simple_return_mean": record.simple_return_mean,
            "simple_return_population_variance": record.simple_return_population_variance,
            "return_series_fingerprint": record.return_series_fingerprint,
            "validation_status": record.validation_status.value,
            "deployment_authorization": record.deployment_authorization.value,
            "execution_state": record.execution_state.value,
            "contract_version": record.contract_version.number,
        }
    if isinstance(record, ExperimentRunRecord):
        return {
            "run_id": str(record.run_id),
            "version": record.version.number,
            "authorization_ref": _trace_ref_payload(record.authorization_ref),
            "specification_ref": _trace_ref_payload(record.specification_ref),
            "policy_ref": _trace_ref_payload(record.policy_ref),
            "eligibility_ref": _trace_ref_payload(record.eligibility_ref),
            "normalized_manifest_ref": _trace_ref_payload(record.normalized_manifest_ref),
            "normalized_lock_ref": _trace_ref_payload(record.normalized_lock_ref),
            "engine_contract_ref": _trace_ref_payload(record.engine_contract_ref),
            "configuration_fingerprint": record.configuration_fingerprint,
            "random_seed": record.random_seed,
            "observation_start": _timestamp_payload(record.observation_start),
            "observation_end": _timestamp_payload(record.observation_end),
            "knowledge_cutoff": _timestamp_payload(record.knowledge_cutoff),
            "run_input_fingerprint": record.run_input_fingerprint,
            "result_ref": _trace_ref_payload(record.result_ref),
            "status": record.status.value,
            "completed_at": _timestamp_payload(record.completed_at),
            "provenance_ref": _trace_ref_payload(record.provenance_ref),
            "research_execution": record.research_execution.value,
            "validation_status": record.validation_status.value,
            "deployment_authorization": record.deployment_authorization.value,
            "execution_state": record.execution_state.value,
            "contract_version": record.contract_version.number,
        }
    if isinstance(record, StrategyDefinition):
        return {
            "strategy_id": str(record.strategy_id),
            "version": record.version.number,
            "model": record.model.value,
            "signal_timing": record.signal_timing.value,
            "execution_timing": record.execution_timing.value,
            "side_permission": record.side_permission.value,
            "threshold_bps": record.threshold_bps,
            "fixed_notional_minor": record.fixed_notional_minor,
            "capital_currency": record.capital_currency,
            "capital_minor_unit_scale": record.capital_minor_unit_scale,
            "allow_pyramiding": record.allow_pyramiding,
            "force_close_at_window_end": record.force_close_at_window_end,
            "engine_contract_ref": _trace_ref_payload(record.engine_contract_ref),
            "provenance_ref": _trace_ref_payload(record.provenance_ref),
            "contract_version": record.contract_version.number,
        }
    if isinstance(record, BacktestResultArtifact):
        return {
            "artifact_id": str(record.artifact_id),
            "version": record.version.number,
            "run_id": str(record.run_id),
            "run_version": record.run_version.number,
            "run_input_fingerprint": record.run_input_fingerprint,
            "authorization_ref": _trace_ref_payload(record.authorization_ref),
            "specification_ref": _trace_ref_payload(record.specification_ref),
            "policy_ref": _trace_ref_payload(record.policy_ref),
            "eligibility_ref": _trace_ref_payload(record.eligibility_ref),
            "normalized_manifest_ref": _trace_ref_payload(record.normalized_manifest_ref),
            "normalized_lock_ref": _trace_ref_payload(record.normalized_lock_ref),
            "engine_contract_ref": _trace_ref_payload(record.engine_contract_ref),
            "strategy_ref": _trace_ref_payload(record.strategy_ref),
            "configuration_fingerprint": record.configuration_fingerprint,
            "capital_currency": record.capital_currency,
            "capital_minor_unit_scale": record.capital_minor_unit_scale,
            "initial_capital": record.initial_capital,
            "orders": [_simulated_order_payload(item) for item in record.orders],
            "fills": [_simulated_fill_payload(item) for item in record.fills],
            "trades": [_simulated_trade_payload(item) for item in record.trades],
            "equity_curve": [_equity_point_payload(item) for item in record.equity_curve],
            "final_cash": record.final_cash,
            "final_equity": record.final_equity,
            "open_position": record.open_position.value,
            "trade_count": record.trade_count,
            "gross_pnl": record.gross_pnl,
            "net_pnl": record.net_pnl,
            "total_return": record.total_return,
            "max_drawdown": record.max_drawdown,
            "validation_status": record.validation_status.value,
            "deployment_authorization": record.deployment_authorization.value,
            "execution_state": record.execution_state.value,
            "contract_version": record.contract_version.number,
        }
    if isinstance(record, BacktestRunRecord):
        return {
            "run_id": str(record.run_id),
            "version": record.version.number,
            "authorization_ref": _trace_ref_payload(record.authorization_ref),
            "specification_ref": _trace_ref_payload(record.specification_ref),
            "policy_ref": _trace_ref_payload(record.policy_ref),
            "eligibility_ref": _trace_ref_payload(record.eligibility_ref),
            "normalized_manifest_ref": _trace_ref_payload(record.normalized_manifest_ref),
            "normalized_lock_ref": _trace_ref_payload(record.normalized_lock_ref),
            "engine_contract_ref": _trace_ref_payload(record.engine_contract_ref),
            "strategy_ref": _trace_ref_payload(record.strategy_ref),
            "configuration_fingerprint": record.configuration_fingerprint,
            "run_input_fingerprint": record.run_input_fingerprint,
            "result_ref": _trace_ref_payload(record.result_ref),
            "status": record.status.value,
            "completed_at": _timestamp_payload(record.completed_at),
            "provenance_ref": _trace_ref_payload(record.provenance_ref),
            "validation_status": record.validation_status.value,
            "deployment_authorization": record.deployment_authorization.value,
            "execution_state": record.execution_state.value,
            "contract_version": record.contract_version.number,
        }
    if isinstance(record, ValidationPlan):
        return {
            "validation_plan_id": str(record.validation_plan_id),
            "version": record.version.number,
            "target_experiment_family": record.target_experiment_family.value,
            "target_metrics": [item.value for item in record.target_metrics],
            "primary_metric": record.primary_metric.value,
            "null_hypothesis": record.null_hypothesis.value,
            "alternative_hypothesis": record.alternative_hypothesis.value,
            "min_sample_size": record.min_sample_size,
            "min_trade_count": record.min_trade_count,
            "uncertainty_method": record.uncertainty_method.value,
            "confidence_level": record.confidence_level,
            "bootstrap_iterations": record.bootstrap_iterations,
            "random_seed": record.random_seed,
            "holdout_policy": record.holdout_policy.value,
            "multiplicity_policy": record.multiplicity_policy.value,
            "validator_authority_ref": _trace_ref_payload(record.validator_authority_ref),
            "provenance_ref": _trace_ref_payload(record.provenance_ref),
            "contract_version": record.contract_version.number,
        }
    if isinstance(record, ScientificValidationResult):
        return {
            "validation_result_id": str(record.validation_result_id),
            "version": record.version.number,
            "validation_plan_ref": _trace_ref_payload(record.validation_plan_ref),
            "backtest_result_ref": _trace_ref_payload(record.backtest_result_ref),
            "backtest_run_ref": _trace_ref_payload(record.backtest_run_ref),
            "experiment_ref": _trace_ref_payload(record.experiment_ref),
            "strategy_ref": _trace_ref_payload(record.strategy_ref),
            "normalized_manifest_ref": _trace_ref_payload(record.normalized_manifest_ref),
            "normalized_lock_ref": _trace_ref_payload(record.normalized_lock_ref),
            "primary_metric": record.primary_metric.value,
            "estimate": record.estimate,
            "lower_bound": record.lower_bound,
            "upper_bound": record.upper_bound,
            "confidence_level": record.confidence_level,
            "uncertainty_method": record.uncertainty_method.value,
            "sample_size": record.sample_size,
            "trade_count": record.trade_count,
            "holdout_status": record.holdout_status.value,
            "multiplicity_policy": record.multiplicity_policy.value,
            "decision": record.decision.value,
            "reason_codes": [item.value for item in record.reason_codes],
            "validator_authority_ref": _trace_ref_payload(record.validator_authority_ref),
            "provenance_ref": _trace_ref_payload(record.provenance_ref),
            "scientific_boundary": record.scientific_boundary.value,
            "out_of_sample_evidence": record.out_of_sample_evidence.value,
            "deployment_authorization": record.deployment_authorization.value,
            "execution_state": record.execution_state.value,
            "contract_version": record.contract_version.number,
        }
    if isinstance(record, ValidationRunRecord):
        return {
            "validation_run_id": str(record.validation_run_id),
            "version": record.version.number,
            "validation_plan_ref": _trace_ref_payload(record.validation_plan_ref),
            "backtest_result_ref": _trace_ref_payload(record.backtest_result_ref),
            "backtest_run_ref": _trace_ref_payload(record.backtest_run_ref),
            "validation_input_fingerprint": record.validation_input_fingerprint,
            "random_seed": record.random_seed,
            "validation_result_ref": _trace_ref_payload(record.validation_result_ref),
            "validator_authority_ref": _trace_ref_payload(record.validator_authority_ref),
            "completed_at": _timestamp_payload(record.completed_at),
            "provenance_ref": _trace_ref_payload(record.provenance_ref),
            "status": record.status.value,
            "deployment_authorization": record.deployment_authorization.value,
            "execution_state": record.execution_state.value,
            "contract_version": record.contract_version.number,
        }
    if isinstance(record, RobustnessValidationPlan):
        return {
            "robustness_plan_id": str(record.robustness_plan_id),
            "version": record.version.number,
            "source_scientific_validation_ref": _trace_ref_payload(
                record.source_scientific_validation_ref
            ),
            "target_methods": [item.value for item in record.target_methods],
            "walk_forward_policy": record.walk_forward_policy.value,
            "train_bars": record.train_bars,
            "test_bars": record.test_bars,
            "step_bars": record.step_bars,
            "minimum_window_count": record.minimum_window_count,
            "minimum_completed_trades_per_test_slice": (
                record.minimum_completed_trades_per_test_slice
            ),
            "walk_forward_pass_positive_ratio": record.walk_forward_pass_positive_ratio,
            "walk_forward_fail_positive_ratio": record.walk_forward_fail_positive_ratio,
            "walk_forward_pass_worst_return_floor": (record.walk_forward_pass_worst_return_floor),
            "walk_forward_severe_loss_floor": record.walk_forward_severe_loss_floor,
            "monte_carlo_policy": record.monte_carlo_policy.value,
            "monte_carlo_iterations": record.monte_carlo_iterations,
            "monte_carlo_seed": record.monte_carlo_seed,
            "monte_carlo_lower_quantile": record.monte_carlo_lower_quantile,
            "monte_carlo_upper_quantile": record.monte_carlo_upper_quantile,
            "perturbation_policy": record.perturbation_policy.value,
            "commission_multipliers": list(record.commission_multipliers),
            "perturbation_pass_return_floor": record.perturbation_pass_return_floor,
            "perturbation_fail_return_threshold": record.perturbation_fail_return_threshold,
            "robustness_authority_ref": _trace_ref_payload(record.robustness_authority_ref),
            "provenance_ref": _trace_ref_payload(record.provenance_ref),
            "contract_version": record.contract_version.number,
        }
    if isinstance(record, RobustnessValidationResult):
        return {
            "robustness_result_id": str(record.robustness_result_id),
            "version": record.version.number,
            "robustness_plan_ref": _trace_ref_payload(record.robustness_plan_ref),
            "scientific_validation_result_ref": _trace_ref_payload(
                record.scientific_validation_result_ref
            ),
            "validation_run_ref": _trace_ref_payload(record.validation_run_ref),
            "backtest_result_ref": _trace_ref_payload(record.backtest_result_ref),
            "backtest_run_ref": _trace_ref_payload(record.backtest_run_ref),
            "strategy_ref": _trace_ref_payload(record.strategy_ref),
            "experiment_ref": _trace_ref_payload(record.experiment_ref),
            "normalized_manifest_ref": _trace_ref_payload(record.normalized_manifest_ref),
            "normalized_lock_ref": _trace_ref_payload(record.normalized_lock_ref),
            "walk_forward": _walk_forward_payload(record.walk_forward),
            "monte_carlo": _monte_carlo_payload(record.monte_carlo),
            "cost_perturbation": _cost_perturbation_payload(record.cost_perturbation),
            "holdout_evidence": record.holdout_evidence.value,
            "decision": record.decision.value,
            "reason_codes": [item.value for item in record.reason_codes],
            "robustness_authority_ref": _trace_ref_payload(record.robustness_authority_ref),
            "provenance_ref": _trace_ref_payload(record.provenance_ref),
            "deployment_authorization": record.deployment_authorization.value,
            "execution_state": record.execution_state.value,
            "contract_version": record.contract_version.number,
        }
    if isinstance(record, RobustnessValidationRunRecord):
        return {
            "robustness_run_id": str(record.robustness_run_id),
            "version": record.version.number,
            "robustness_plan_ref": _trace_ref_payload(record.robustness_plan_ref),
            "scientific_validation_result_ref": _trace_ref_payload(
                record.scientific_validation_result_ref
            ),
            "validation_run_ref": _trace_ref_payload(record.validation_run_ref),
            "backtest_result_ref": _trace_ref_payload(record.backtest_result_ref),
            "backtest_run_ref": _trace_ref_payload(record.backtest_run_ref),
            "robustness_input_fingerprint": record.robustness_input_fingerprint,
            "monte_carlo_seed": record.monte_carlo_seed,
            "robustness_result_ref": _trace_ref_payload(record.robustness_result_ref),
            "robustness_authority_ref": _trace_ref_payload(record.robustness_authority_ref),
            "provenance_ref": _trace_ref_payload(record.provenance_ref),
            "status": record.status.value,
            "deployment_authorization": record.deployment_authorization.value,
            "execution_state": record.execution_state.value,
            "contract_version": record.contract_version.number,
        }
    if isinstance(record, OptimizationSearchSpace):
        return {
            "search_space_id": str(record.search_space_id),
            "version": record.version.number,
            "parameters": [
                {
                    "name": item.name.value,
                    "parameter_type": item.parameter_type.value,
                    "lower_bound": item.lower_bound,
                    "upper_bound": item.upper_bound,
                    "step": item.step,
                    "default_value": item.default_value,
                }
                for item in record.parameters
            ],
            "contract_version": record.contract_version.number,
        }
    if isinstance(record, OptimizationPlan):
        return {
            "optimization_plan_id": str(record.optimization_plan_id),
            "version": record.version.number,
            "search_space_ref": _trace_ref_payload(record.search_space_ref),
            "parent_strategy_ref": _trace_ref_payload(record.parent_strategy_ref),
            "source_experiment_ref": _trace_ref_payload(record.source_experiment_ref),
            "source_robustness_result_ref": _trace_ref_payload(record.source_robustness_result_ref),
            "normalized_manifest_ref": _trace_ref_payload(record.normalized_manifest_ref),
            "normalized_lock_ref": _trace_ref_payload(record.normalized_lock_ref),
            "engine_contract_ref": _trace_ref_payload(record.engine_contract_ref),
            "validation_plan_ref": _trace_ref_payload(record.validation_plan_ref),
            "robustness_plan_ref": _trace_ref_payload(record.robustness_plan_ref),
            "search_method": record.search_method.value,
            "maximum_trials": record.maximum_trials,
            "objective": record.objective.value,
            "minimum_trade_count": record.minimum_trade_count,
            "maximum_drawdown": record.maximum_drawdown,
            "multiplicity_policy": record.multiplicity_policy.value,
            "declared_alpha": record.declared_alpha,
            "selection_authority_ref": _trace_ref_payload(record.selection_authority_ref),
            "provenance_ref": _trace_ref_payload(record.provenance_ref),
            "contract_version": record.contract_version.number,
        }
    if isinstance(record, OptimizationCandidateDefinition):
        return {
            "candidate_id": str(record.candidate_id),
            "version": record.version.number,
            "optimization_plan_ref": _trace_ref_payload(record.optimization_plan_ref),
            "parent_strategy_ref": _trace_ref_payload(record.parent_strategy_ref),
            "parameter_values": [[name, value] for name, value in record.parameter_values],
            "candidate_strategy_ref": _trace_ref_payload(record.candidate_strategy_ref),
            "contract_version": record.contract_version.number,
        }
    if isinstance(record, OptimizationCandidateResult):
        return {
            "candidate_id": str(record.candidate_id),
            "version": record.version.number,
            "candidate_definition_ref": _trace_ref_payload(record.candidate_definition_ref),
            "candidate_strategy_ref": _trace_ref_payload(record.candidate_strategy_ref),
            "backtest_result_ref": _trace_ref_payload(record.backtest_result_ref),
            "scientific_validation_result_ref": _trace_ref_payload(
                record.scientific_validation_result_ref
            ),
            "robustness_result_ref": _trace_ref_payload(record.robustness_result_ref),
            "total_return": record.total_return,
            "max_drawdown": record.max_drawdown,
            "trade_count": record.trade_count,
            "eligibility": record.eligibility.value,
            "reason_codes": [item.value for item in record.reason_codes],
            "contract_version": record.contract_version.number,
        }
    if isinstance(record, OptimizationTrialRecord):
        return {
            "trial_id": str(record.trial_id),
            "version": record.version.number,
            "optimization_plan_ref": _trace_ref_payload(record.optimization_plan_ref),
            "trial_index": record.trial_index,
            "candidate_definition_ref": _trace_ref_payload(record.candidate_definition_ref),
            "candidate_result_ref": _trace_ref_payload(record.candidate_result_ref),
            "status": record.status.value,
            "reason_codes": [item.value for item in record.reason_codes],
            "contract_version": record.contract_version.number,
        }
    if isinstance(record, OptimizationSelectionResult):
        return {
            "selection_result_id": str(record.selection_result_id),
            "version": record.version.number,
            "optimization_plan_ref": _trace_ref_payload(record.optimization_plan_ref),
            "candidate_result_refs": [
                _trace_ref_payload(item) for item in record.candidate_result_refs
            ],
            "trial_refs": [_trace_ref_payload(item) for item in record.trial_refs],
            "attempted_trials": record.attempted_trials,
            "completed_trials": record.completed_trials,
            "eligible_candidates": record.eligible_candidates,
            "selected_candidate_ref": (
                None
                if record.selected_candidate_ref is None
                else _trace_ref_payload(record.selected_candidate_ref)
            ),
            "decision": record.decision.value,
            "multiplicity_policy": record.multiplicity_policy.value,
            "corrected_alpha": record.corrected_alpha,
            "tie_break_order": list(record.tie_break_order),
            "reason_codes": [item.value for item in record.reason_codes],
            "selection_authority_ref": _trace_ref_payload(record.selection_authority_ref),
            "provenance_ref": _trace_ref_payload(record.provenance_ref),
            "deployment_authorization": record.deployment_authorization.value,
            "execution_state": record.execution_state.value,
            "contract_version": record.contract_version.number,
        }
    if isinstance(record, OptimizationRunRecord):
        return {
            "optimization_run_id": str(record.optimization_run_id),
            "version": record.version.number,
            "optimization_plan_ref": _trace_ref_payload(record.optimization_plan_ref),
            "optimization_input_fingerprint": record.optimization_input_fingerprint,
            "declared_trials": record.declared_trials,
            "attempted_trials": record.attempted_trials,
            "completed_trials": record.completed_trials,
            "selection_result_ref": _trace_ref_payload(record.selection_result_ref),
            "selection_authority_ref": _trace_ref_payload(record.selection_authority_ref),
            "provenance_ref": _trace_ref_payload(record.provenance_ref),
            "status": record.status.value,
            "deployment_authorization": record.deployment_authorization.value,
            "execution_state": record.execution_state.value,
            "contract_version": record.contract_version.number,
        }
    if isinstance(record, PineStrategySourceArtifact):
        return {
            "pine_artifact_id": str(record.pine_artifact_id),
            "version": record.version.number,
            "pine_language_version": record.pine_language_version.value,
            "source_text": record.source_text,
            "normalized_source_text": record.normalized_source_text,
            "source_sha256": record.source_sha256,
            "normalized_source_sha256": record.normalized_source_sha256,
            "source_byte_size": record.source_byte_size,
            "script_kind": record.script_kind.value,
            "declared_script_title": record.declared_script_title,
            "pyramiding": record.pyramiding,
            "process_orders_on_close": record.process_orders_on_close,
            "calc_on_every_tick": record.calc_on_every_tick,
            "default_qty_type": record.default_qty_type.value,
            "default_qty_value": record.default_qty_value,
            "strategy_definition_ref": _trace_ref_payload(record.strategy_definition_ref),
            "optimization_candidate_definition_ref": (
                None
                if record.optimization_candidate_definition_ref is None
                else _trace_ref_payload(record.optimization_candidate_definition_ref)
            ),
            "optimization_candidate_result_ref": (
                None
                if record.optimization_candidate_result_ref is None
                else _trace_ref_payload(record.optimization_candidate_result_ref)
            ),
            "optimization_selection_ref": (
                None
                if record.optimization_selection_ref is None
                else _trace_ref_payload(record.optimization_selection_ref)
            ),
            "source_backtest_result_ref": _trace_ref_payload(record.source_backtest_result_ref),
            "source_scientific_validation_ref": _trace_ref_payload(
                record.source_scientific_validation_ref
            ),
            "source_robustness_result_ref": _trace_ref_payload(record.source_robustness_result_ref),
            "provenance_ref": _trace_ref_payload(record.provenance_ref),
            "authority_ref": _trace_ref_payload(record.authority_ref),
            "semantic_parity": record.semantic_parity.value,
            "repaint_assessment": record.repaint_assessment.value,
            "deployment_authorization": record.deployment_authorization.value,
            "execution_state": record.execution_state.value,
            "contract_version": record.contract_version.number,
        }
    if isinstance(record, PineStrategyIntakeRecord):
        return {
            "intake_run_id": str(record.intake_run_id),
            "version": record.version.number,
            "requested_artifact_id": str(record.requested_artifact_id),
            "source_artifact_ref": (
                None
                if record.source_artifact_ref is None
                else _trace_ref_payload(record.source_artifact_ref)
            ),
            "source_sha256": record.source_sha256,
            "normalized_source_sha256": record.normalized_source_sha256,
            "source_byte_size": record.source_byte_size,
            "input_fingerprint": record.input_fingerprint,
            "status": record.status.value,
            "reason_codes": [item.value for item in record.reason_codes],
            "authority_ref": _trace_ref_payload(record.authority_ref),
            "provenance_ref": _trace_ref_payload(record.provenance_ref),
            "deployment_authorization": record.deployment_authorization.value,
            "execution_state": record.execution_state.value,
            "contract_version": record.contract_version.number,
        }
    if isinstance(record, ParityTolerancePolicy):
        return {
            "policy_id": str(record.policy_id),
            "version": record.version.number,
            "timestamp_exact": record.timestamp_exact,
            "absolute_price_tolerance": record.absolute_price_tolerance,
            "relative_price_tolerance": record.relative_price_tolerance,
            "quantity_tolerance": record.quantity_tolerance,
            "commission_tolerance": record.commission_tolerance,
            "pnl_tolerance": record.pnl_tolerance,
            "authority_ref": _trace_ref_payload(record.authority_ref),
            "provenance_ref": _trace_ref_payload(record.provenance_ref),
            "contract_version": record.contract_version.number,
        }
    if isinstance(record, PineExecutionEvidence):
        return {
            "evidence_id": str(record.evidence_id),
            "version": record.version.number,
            "pine_artifact_ref": _trace_ref_payload(record.pine_artifact_ref),
            "strategy_ref": _trace_ref_payload(record.strategy_ref),
            "instrument_ref": _trace_ref_payload(record.instrument_ref),
            "normalized_manifest_ref": _trace_ref_payload(record.normalized_manifest_ref),
            "normalized_lock_ref": _trace_ref_payload(record.normalized_lock_ref),
            "observation_start": _timestamp_payload(record.observation_start),
            "observation_end": _timestamp_payload(record.observation_end),
            "source_format": record.source_format.value,
            "source_text": record.source_text,
            "source_sha256": record.source_sha256,
            "source_byte_size": record.source_byte_size,
            "events": [
                {
                    "event_index": item.event_index,
                    "signal_time": _timestamp_payload(item.signal_time),
                    "execution_time": _timestamp_payload(item.execution_time),
                    "action": item.action.value,
                    "side": item.side.value,
                    "execution_price": item.execution_price,
                    "position_after": item.position_after.value,
                    "quantity": item.quantity,
                    "commission": item.commission,
                    "trade_id": item.trade_id,
                    "source_row": item.source_row,
                }
                for item in record.events
            ],
            "provenance_ref": _trace_ref_payload(record.provenance_ref),
            "authority_ref": _trace_ref_payload(record.authority_ref),
            "contract_version": record.contract_version.number,
        }
    if isinstance(record, PinePythonParityResult):
        return {
            "parity_result_id": str(record.parity_result_id),
            "version": record.version.number,
            "pine_artifact_ref": _trace_ref_payload(record.pine_artifact_ref),
            "pine_execution_evidence_ref": _trace_ref_payload(record.pine_execution_evidence_ref),
            "python_backtest_ref": _trace_ref_payload(record.python_backtest_ref),
            "strategy_ref": _trace_ref_payload(record.strategy_ref),
            "instrument_ref": _trace_ref_payload(record.instrument_ref),
            "normalized_manifest_ref": _trace_ref_payload(record.normalized_manifest_ref),
            "normalized_lock_ref": _trace_ref_payload(record.normalized_lock_ref),
            "tolerance_policy_ref": _trace_ref_payload(record.tolerance_policy_ref),
            "expected_event_count": record.expected_event_count,
            "observed_event_count": record.observed_event_count,
            "mismatch_count": record.mismatch_count,
            "mismatches": [
                {
                    "mismatch_index": item.mismatch_index,
                    "mismatch_type": item.mismatch_type.value,
                    "expected_value": item.expected_value,
                    "observed_value": item.observed_value,
                    "expected_event_index": item.expected_event_index,
                    "observed_event_index": item.observed_event_index,
                    "explanation_code": item.explanation_code,
                }
                for item in record.mismatches
            ],
            "decision": record.decision.value,
            "reason_codes": [item.value for item in record.reason_codes],
            "input_fingerprint": record.input_fingerprint,
            "semantic_parity": record.semantic_parity.value,
            "repaint_assessment": record.repaint_assessment.value,
            "authority_ref": _trace_ref_payload(record.authority_ref),
            "provenance_ref": _trace_ref_payload(record.provenance_ref),
            "deployment_authorization": record.deployment_authorization.value,
            "execution_state": record.execution_state.value,
            "contract_version": record.contract_version.number,
        }
    if isinstance(record, PinePythonParityRunRecord):
        return {
            "parity_run_id": str(record.parity_run_id),
            "version": record.version.number,
            "request_fingerprint": record.request_fingerprint,
            "result_ref": _trace_ref_payload(record.result_ref),
            "input_fingerprint": record.input_fingerprint,
            "expected_event_count": record.expected_event_count,
            "observed_event_count": record.observed_event_count,
            "mismatch_count": record.mismatch_count,
            "decision": record.decision.value,
            "authority_ref": _trace_ref_payload(record.authority_ref),
            "provenance_ref": _trace_ref_payload(record.provenance_ref),
            "deployment_authorization": record.deployment_authorization.value,
            "execution_state": record.execution_state.value,
            "contract_version": record.contract_version.number,
        }
    if isinstance(record, AIStrategyProposal):
        return {
            "proposal_id": str(record.proposal_id),
            "version": record.version.number,
            "proposing_agent_ref": _trace_ref_payload(record.proposing_agent_ref),
            "strategy_family": record.strategy_family,
            "declared_hypothesis": record.declared_hypothesis,
            "parameter_declarations": [list(item) for item in record.parameter_declarations],
            "strategy_definition_ref": _trace_ref_payload(record.strategy_definition_ref),
            "status": record.status.value,
            "proposal_authority_state": record.proposal_authority_state.value,
            "provenance_ref": _trace_ref_payload(record.provenance_ref),
            "contract_version": record.contract_version.number,
        }
    if isinstance(record, IntegratedResearchWorkflowPlan):
        return {
            "workflow_plan_id": str(record.workflow_plan_id),
            "version": record.version.number,
            "mode": record.mode.value,
            "proposal_ref": _trace_ref_payload(record.proposal_ref),
            "proposal_strategy_ref": _trace_ref_payload(record.proposal_strategy_ref),
            "final_strategy_ref": _trace_ref_payload(record.final_strategy_ref),
            "normalized_manifest_ref": _trace_ref_payload(record.normalized_manifest_ref),
            "normalized_lock_ref": _trace_ref_payload(record.normalized_lock_ref),
            "instrument_ref": _trace_ref_payload(record.instrument_ref),
            "experiment_authorization_ref": _trace_ref_payload(record.experiment_authorization_ref),
            "validation_plan_ref": _trace_ref_payload(record.validation_plan_ref),
            "robustness_plan_ref": _trace_ref_payload(record.robustness_plan_ref),
            "optimization_selection_ref": (
                None
                if record.optimization_selection_ref is None
                else _trace_ref_payload(record.optimization_selection_ref)
            ),
            "pine_intake_authority_ref": _trace_ref_payload(record.pine_intake_authority_ref),
            "parity_authority_ref": _trace_ref_payload(record.parity_authority_ref),
            "workflow_authority_ref": _trace_ref_payload(record.workflow_authority_ref),
            "provenance_ref": _trace_ref_payload(record.provenance_ref),
            "contract_version": record.contract_version.number,
        }
    if isinstance(record, ResearchHandoffPackage):
        return {
            "handoff_id": str(record.handoff_id),
            "version": record.version.number,
            "workflow_run_id": str(record.workflow_run_id),
            "workflow_input_fingerprint": record.workflow_input_fingerprint,
            "proposal_ref": _trace_ref_payload(record.proposal_ref),
            "final_strategy_ref": _trace_ref_payload(record.final_strategy_ref),
            "selected_candidate_ref": (
                None
                if record.selected_candidate_ref is None
                else _trace_ref_payload(record.selected_candidate_ref)
            ),
            "backtest_ref": _trace_ref_payload(record.backtest_ref),
            "scientific_validation_ref": _trace_ref_payload(record.scientific_validation_ref),
            "robustness_ref": _trace_ref_payload(record.robustness_ref),
            "optimization_selection_ref": (
                None
                if record.optimization_selection_ref is None
                else _trace_ref_payload(record.optimization_selection_ref)
            ),
            "pine_artifact_ref": _trace_ref_payload(record.pine_artifact_ref),
            "pine_intake_ref": _trace_ref_payload(record.pine_intake_ref),
            "parity_result_ref": _trace_ref_payload(record.parity_result_ref),
            "parity_decision": record.parity_decision.value,
            "proposing_agent_ref": _trace_ref_payload(record.proposing_agent_ref),
            "pine_generating_agent_ref": _trace_ref_payload(record.pine_generating_agent_ref),
            "readiness": record.readiness.value,
            "provenance_ref": _trace_ref_payload(record.provenance_ref),
            "deployment_authorization": record.deployment_authorization.value,
            "execution_state": record.execution_state.value,
            "contract_version": record.contract_version.number,
        }
    if isinstance(record, TradingViewResearchHandoffManifest):
        return {
            "manifest_id": str(record.manifest_id),
            "version": record.version.number,
            "pine_artifact_ref": _trace_ref_payload(record.pine_artifact_ref),
            "pine_source_sha256": record.pine_source_sha256,
            "parity_result_ref": _trace_ref_payload(record.parity_result_ref),
            "strategy_ref": _trace_ref_payload(record.strategy_ref),
            "instrument_ref": _trace_ref_payload(record.instrument_ref),
            "normalized_manifest_ref": _trace_ref_payload(record.normalized_manifest_ref),
            "normalized_lock_ref": _trace_ref_payload(record.normalized_lock_ref),
            "repaint_assessment": record.repaint_assessment.value,
            "readiness": record.readiness.value,
            "deployment_authorization": record.deployment_authorization.value,
            "execution_state": record.execution_state.value,
            "contract_version": record.contract_version.number,
        }
    if isinstance(record, IntegratedResearchWorkflowResult):
        return {
            "workflow_result_id": str(record.workflow_result_id),
            "version": record.version.number,
            "workflow_plan_ref": _trace_ref_payload(record.workflow_plan_ref),
            "proposal_ref": _trace_ref_payload(record.proposal_ref),
            "final_strategy_ref": _trace_ref_payload(record.final_strategy_ref),
            "stages": [
                {
                    "stage": item.stage.value,
                    "state": item.state.value,
                    "evidence_ref": _trace_ref_payload(item.evidence_ref),
                    "outcome": item.outcome.value,
                    "reason_code": None if item.reason_code is None else item.reason_code.value,
                    "stage_fingerprint": item.stage_fingerprint,
                }
                for item in record.stages
            ],
            "final_state": record.final_state.value,
            "handoff_ref": (
                None if record.handoff_ref is None else _trace_ref_payload(record.handoff_ref)
            ),
            "tradingview_manifest_ref": (
                None
                if record.tradingview_manifest_ref is None
                else _trace_ref_payload(record.tradingview_manifest_ref)
            ),
            "reason_codes": [item.value for item in record.reason_codes],
            "input_fingerprint": record.input_fingerprint,
            "workflow_authority_ref": _trace_ref_payload(record.workflow_authority_ref),
            "provenance_ref": _trace_ref_payload(record.provenance_ref),
            "deployment_authorization": record.deployment_authorization.value,
            "execution_state": record.execution_state.value,
            "contract_version": record.contract_version.number,
        }
    if isinstance(record, IntegratedResearchWorkflowRunRecord):
        return {
            "workflow_run_id": str(record.workflow_run_id),
            "version": record.version.number,
            "workflow_plan_ref": _trace_ref_payload(record.workflow_plan_ref),
            "proposal_ref": _trace_ref_payload(record.proposal_ref),
            "result_ref": _trace_ref_payload(record.result_ref),
            "input_fingerprint": record.input_fingerprint,
            "final_state": record.final_state.value,
            "handoff_ref": (
                None if record.handoff_ref is None else _trace_ref_payload(record.handoff_ref)
            ),
            "stage_count": record.stage_count,
            "workflow_authority_ref": _trace_ref_payload(record.workflow_authority_ref),
            "provenance_ref": _trace_ref_payload(record.provenance_ref),
            "deployment_authorization": record.deployment_authorization.value,
            "execution_state": record.execution_state.value,
            "contract_version": record.contract_version.number,
        }
    raise InvalidSerialization(f"unsupported governed type: {type(record).__name__}")


def encode(record: GovernedRecord) -> bytes:
    """Encode only an explicitly supported governed record to canonical UTF-8 bytes."""
    record_type = _SUPPORTED_TYPES.get(type(record))
    if record_type is None:
        raise InvalidSerialization(f"unsupported governed type: {type(record).__name__}")
    envelope = {
        "$format": REPRESENTATION_FORMAT,
        "$representation_version": REPRESENTATION_VERSION,
        "$type": record_type,
        "payload": _payload(record),
    }
    return canonical_json(envelope).encode("utf-8")


def _decode_artifact(payload: Any) -> ArtifactEnvelope:
    item = _strict_object(
        payload,
        {
            "artifact_id",
            "artifact_type",
            "version",
            "created_at",
            "producer_id",
            "provenance_id",
            "contract_version",
            "lifecycle",
            "content_fingerprint",
            "parent_refs",
            "metadata",
        },
        "ArtifactEnvelope.payload",
    )
    return ArtifactEnvelope(
        cast(ArtifactId, _typed_id(item["artifact_id"], ArtifactId, "artifact_id")),
        _text(item["artifact_type"], "artifact_type"),
        _version(item["version"], "version"),
        _timestamp(item["created_at"], "created_at"),
        cast(AgentId, _typed_id(item["producer_id"], AgentId, "producer_id")),
        cast(ProvenanceId, _typed_id(item["provenance_id"], ProvenanceId, "provenance_id")),
        _version(item["contract_version"], "contract_version"),
        ArtifactLifecycle(_text(item["lifecycle"], "lifecycle")),
        _text(item["content_fingerprint"], "content_fingerprint"),
        _refs(item["parent_refs"], "parent_refs"),
        _metadata(item["metadata"], "metadata"),
    )


def _decode_evidence(payload: Any) -> EvidenceEnvelope:
    item = _strict_object(
        payload,
        {
            "evidence_id",
            "evidence_type",
            "source_artifact",
            "provenance_id",
            "created_at",
            "scope",
            "admissibility",
            "freshness",
            "supersedes",
            "invalidates",
            "metadata",
        },
        "EvidenceEnvelope.payload",
    )
    return EvidenceEnvelope(
        cast(EvidenceId, _typed_id(item["evidence_id"], EvidenceId, "evidence_id")),
        _text(item["evidence_type"], "evidence_type"),
        _ref(item["source_artifact"], "source_artifact"),
        cast(ProvenanceId, _typed_id(item["provenance_id"], ProvenanceId, "provenance_id")),
        _timestamp(item["created_at"], "created_at"),
        _text(item["scope"], "scope"),
        EvidenceState(_text(item["admissibility"], "admissibility")),
        FreshnessState(_text(item["freshness"], "freshness")),
        _optional_ref(item["supersedes"], "supersedes"),
        _refs(item["invalidates"], "invalidates"),
        _metadata(item["metadata"], "metadata"),
    )


def _decode_provenance(payload: Any) -> ProvenanceRecord:
    item = _strict_object(
        payload,
        {
            "provenance_id",
            "producer_id",
            "produced_at",
            "process",
            "input_refs",
            "transformation_ref",
            "metadata",
        },
        "ProvenanceRecord.payload",
    )
    return ProvenanceRecord(
        cast(ProvenanceId, _typed_id(item["provenance_id"], ProvenanceId, "provenance_id")),
        cast(AgentId, _typed_id(item["producer_id"], AgentId, "producer_id")),
        _timestamp(item["produced_at"], "produced_at"),
        _text(item["process"], "process"),
        _refs(item["input_refs"], "input_refs"),
        _optional_ref(item["transformation_ref"], "transformation_ref"),
        _metadata(item["metadata"], "metadata"),
    )


def _decode_audit(payload: Any) -> AuditEvent:
    item = _strict_object(
        payload,
        {"event_id", "actor_id", "action", "target", "occurred_at", "result", "context"},
        "AuditEvent.payload",
    )
    return AuditEvent(
        cast(AuditEventId, _typed_id(item["event_id"], AuditEventId, "event_id")),
        cast(AgentId, _typed_id(item["actor_id"], AgentId, "actor_id")),
        _text(item["action"], "action"),
        _ref(item["target"], "target"),
        _timestamp(item["occurred_at"], "occurred_at"),
        AuditResult(_text(item["result"], "result")),
        _metadata(item["context"], "context"),
    )


def _decode_venue(payload: Any) -> VenueIdentity:
    item = _strict_object(
        payload,
        {"venue_id", "version", "name", "venue_type", "jurisdiction", "contract_version"},
        "VenueIdentity.payload",
    )
    jurisdiction = item["jurisdiction"]
    if jurisdiction is not None:
        jurisdiction = _text(jurisdiction, "jurisdiction")
    return VenueIdentity(
        cast(VenueId, _typed_id(item["venue_id"], VenueId, "venue_id")),
        _version(item["version"], "version"),
        _text(item["name"], "name"),
        VenueType(_text(item["venue_type"], "venue_type")),
        jurisdiction,
        _version(item["contract_version"], "contract_version"),
    )


def _decode_source(payload: Any) -> SourceIdentity:
    item = _strict_object(
        payload,
        {
            "source_id",
            "version",
            "provider",
            "source_type",
            "feed",
            "source_version",
            "venue_ref",
            "contract_version",
        },
        "SourceIdentity.payload",
    )
    return SourceIdentity(
        cast(SourceId, _typed_id(item["source_id"], SourceId, "source_id")),
        _version(item["version"], "version"),
        _text(item["provider"], "provider"),
        SourceType(_text(item["source_type"], "source_type")),
        _text(item["feed"], "feed"),
        _text(item["source_version"], "source_version"),
        _optional_trace_ref(item["venue_ref"], "venue_ref"),
        _version(item["contract_version"], "contract_version"),
    )


def _decode_instrument(payload: Any) -> InstrumentIdentity:
    item = _strict_object(
        payload,
        {
            "instrument_id",
            "version",
            "symbol",
            "instrument_class",
            "base_asset",
            "quote_asset",
            "settlement_asset",
            "venue_ref",
            "contract_version",
        },
        "InstrumentIdentity.payload",
    )
    return InstrumentIdentity(
        cast(InstrumentId, _typed_id(item["instrument_id"], InstrumentId, "instrument_id")),
        _version(item["version"], "version"),
        _text(item["symbol"], "symbol"),
        InstrumentClass(_text(item["instrument_class"], "instrument_class")),
        _optional_text(item["base_asset"], "base_asset"),
        _optional_text(item["quote_asset"], "quote_asset"),
        _optional_text(item["settlement_asset"], "settlement_asset"),
        _optional_trace_ref(item["venue_ref"], "venue_ref"),
        _version(item["contract_version"], "contract_version"),
    )


def _decode_temporal(value: Any) -> TemporalCoordinates:
    item = _strict_object(
        value, {"event_time", "availability_time", "ingestion_time", "policy"}, "temporal"
    )
    return TemporalCoordinates(
        _timestamp(item["event_time"], "event_time"),
        _timestamp(item["availability_time"], "availability_time"),
        _timestamp(item["ingestion_time"], "ingestion_time"),
        TemporalPolicy(_text(item["policy"], "policy")),
    )


def _decode_raw_fields(value: Any) -> tuple[RawField, ...]:
    if not isinstance(value, list):
        raise InvalidSerialization("payload fields must be an array")
    fields: list[RawField] = []
    for raw in value:
        item = _strict_object(raw, {"name", "value"}, "payload[]")
        name = _text(item["name"], "payload[].name")
        fields.append(RawField(name, _raw_value(item["value"], f"payload[{name}].value")))
    return tuple(fields)


def _decode_observation(payload: Any) -> RawObservation:
    item = _strict_object(
        payload,
        {
            "observation_id",
            "version",
            "source_ref",
            "instrument_ref",
            "temporal",
            "payload",
            "provenance_ref",
            "source_sequence",
            "quality",
            "reconciliation",
            "supersedes",
            "contract_version",
        },
        "RawObservation.payload",
    )
    sequence = item["source_sequence"]
    if sequence is not None:
        sequence = _text(sequence, "source_sequence")
    return RawObservation(
        cast(ObservationId, _typed_id(item["observation_id"], ObservationId, "observation_id")),
        _version(item["version"], "version"),
        _trace_ref(item["source_ref"], "source_ref"),
        _trace_ref(item["instrument_ref"], "instrument_ref"),
        _decode_temporal(item["temporal"]),
        _decode_raw_fields(item["payload"]),
        _trace_ref(item["provenance_ref"], "provenance_ref"),
        sequence,
        DataQualityState(_text(item["quality"], "quality")),
        ReconciliationDisposition(_text(item["reconciliation"], "reconciliation")),
        _optional_trace_ref(item["supersedes"], "supersedes"),
        _version(item["contract_version"], "contract_version"),
    )


def _decode_manifest(payload: Any) -> DatasetManifest:
    item = _strict_object(
        payload,
        {
            "dataset_id",
            "version",
            "created_at",
            "observation_refs",
            "source_refs",
            "instrument_refs",
            "event_time_start",
            "event_time_end",
            "provenance_ref",
            "contract_version",
            "membership_policy",
        },
        "DatasetManifest.payload",
    )
    return DatasetManifest(
        cast(DatasetId, _typed_id(item["dataset_id"], DatasetId, "dataset_id")),
        _version(item["version"], "version"),
        _timestamp(item["created_at"], "created_at"),
        _trace_refs(item["observation_refs"], "observation_refs"),
        _trace_refs(item["source_refs"], "source_refs"),
        _trace_refs(item["instrument_refs"], "instrument_refs"),
        _timestamp(item["event_time_start"], "event_time_start"),
        _timestamp(item["event_time_end"], "event_time_end"),
        _trace_ref(item["provenance_ref"], "provenance_ref"),
        _version(item["contract_version"], "contract_version"),
        _text(item["membership_policy"], "membership_policy"),
    )


def _decode_lock(payload: Any) -> DatasetLock:
    item = _strict_object(
        payload,
        {
            "lock_id",
            "version",
            "dataset_ref",
            "manifest_ref",
            "locked_at",
            "temporal_cutoff",
            "provenance_ref",
            "state",
            "contract_version",
        },
        "DatasetLock.payload",
    )
    return DatasetLock(
        cast(DatasetLockId, _typed_id(item["lock_id"], DatasetLockId, "lock_id")),
        _version(item["version"], "version"),
        _trace_ref(item["dataset_ref"], "dataset_ref"),
        _trace_ref(item["manifest_ref"], "manifest_ref"),
        _timestamp(item["locked_at"], "locked_at"),
        _timestamp(item["temporal_cutoff"], "temporal_cutoff"),
        _trace_ref(item["provenance_ref"], "provenance_ref"),
        DatasetLockState(_text(item["state"], "state")),
        _version(item["contract_version"], "contract_version"),
    )


def _decode_timeframe(payload: Any) -> TimeframeIdentity:
    item = _strict_object(
        payload,
        {
            "timeframe_id",
            "version",
            "unit",
            "count",
            "alignment",
            "contract_version",
        },
        "TimeframeIdentity.payload",
    )
    count = item["count"]
    if isinstance(count, bool) or not isinstance(count, int):
        raise InvalidSerialization("timeframe count must be integer")
    return TimeframeIdentity(
        cast(TimeframeId, _typed_id(item["timeframe_id"], TimeframeId, "timeframe_id")),
        _version(item["version"], "version"),
        TimeframeUnit(_text(item["unit"], "unit")),
        count,
        AlignmentKind(_text(item["alignment"], "alignment")),
        _version(item["contract_version"], "contract_version"),
    )


def _decode_bar_schema(payload: Any) -> MarketDataSchema:
    fields = {
        "schema_id",
        "version",
        "timeframe_ref",
        "timestamp_meaning",
        "open_time_field",
        "close_time_field",
        "open_field",
        "high_field",
        "low_field",
        "close_field",
        "volume_field",
        "finality_field",
        "volume_semantic",
        "contract_version",
    }
    item = _strict_object(payload, fields, "MarketDataSchema.payload")
    return MarketDataSchema(
        cast(MarketDataSchemaId, _typed_id(item["schema_id"], MarketDataSchemaId, "schema_id")),
        _version(item["version"], "version"),
        _trace_ref(item["timeframe_ref"], "timeframe_ref"),
        BarTimestampMeaning(_text(item["timestamp_meaning"], "timestamp_meaning")),
        _text(item["open_time_field"], "open_time_field"),
        _text(item["close_time_field"], "close_time_field"),
        _text(item["open_field"], "open_field"),
        _text(item["high_field"], "high_field"),
        _text(item["low_field"], "low_field"),
        _text(item["close_field"], "close_field"),
        _optional_text(item["volume_field"], "volume_field"),
        _text(item["finality_field"], "finality_field"),
        VolumeSemantic(_text(item["volume_semantic"], "volume_semantic")),
        _version(item["contract_version"], "contract_version"),
    )


def _decode_market_bar(payload: Any) -> MarketBar:
    item = _strict_object(
        payload,
        {
            "bar_id",
            "version",
            "source_ref",
            "instrument_ref",
            "timeframe_ref",
            "schema_ref",
            "normalization_version",
            "bar_open",
            "bar_close",
            "availability_time",
            "ingestion_time",
            "open",
            "high",
            "low",
            "close",
            "volume",
            "volume_semantic",
            "finality",
            "source_observation_ref",
            "provenance_ref",
            "supersedes",
            "contract_version",
        },
        "MarketBar.payload",
    )
    volume = item["volume"]
    return MarketBar(
        cast(MarketBarId, _typed_id(item["bar_id"], MarketBarId, "bar_id")),
        _version(item["version"], "version"),
        _trace_ref(item["source_ref"], "source_ref"),
        _trace_ref(item["instrument_ref"], "instrument_ref"),
        _trace_ref(item["timeframe_ref"], "timeframe_ref"),
        _trace_ref(item["schema_ref"], "schema_ref"),
        _version(item["normalization_version"], "normalization_version"),
        _timestamp(item["bar_open"], "bar_open"),
        _timestamp(item["bar_close"], "bar_close"),
        _timestamp(item["availability_time"], "availability_time"),
        _timestamp(item["ingestion_time"], "ingestion_time"),
        DecimalValue(_text(item["open"], "open")),
        DecimalValue(_text(item["high"], "high")),
        DecimalValue(_text(item["low"], "low")),
        DecimalValue(_text(item["close"], "close")),
        None if volume is None else DecimalValue(_text(volume, "volume")),
        VolumeSemantic(_text(item["volume_semantic"], "volume_semantic")),
        BarFinality(_text(item["finality"], "finality")),
        _trace_ref(item["source_observation_ref"], "source_observation_ref"),
        _trace_ref(item["provenance_ref"], "provenance_ref"),
        _optional_trace_ref(item["supersedes"], "supersedes"),
        _version(item["contract_version"], "contract_version"),
    )


def _decode_normalized_manifest(payload: Any) -> NormalizedBarManifest:
    item = _strict_object(
        payload,
        {
            "dataset_id",
            "version",
            "created_at",
            "bar_refs",
            "source_refs",
            "instrument_refs",
            "timeframe_refs",
            "schema_ref",
            "normalization_version",
            "raw_dataset_lock_ref",
            "provenance_ref",
            "contract_version",
            "membership_policy",
        },
        "NormalizedBarManifest.payload",
    )
    return NormalizedBarManifest(
        cast(DatasetId, _typed_id(item["dataset_id"], DatasetId, "dataset_id")),
        _version(item["version"], "version"),
        _timestamp(item["created_at"], "created_at"),
        _trace_refs(item["bar_refs"], "bar_refs"),
        _trace_refs(item["source_refs"], "source_refs"),
        _trace_refs(item["instrument_refs"], "instrument_refs"),
        _trace_refs(item["timeframe_refs"], "timeframe_refs"),
        _trace_ref(item["schema_ref"], "schema_ref"),
        _version(item["normalization_version"], "normalization_version"),
        _trace_ref(item["raw_dataset_lock_ref"], "raw_dataset_lock_ref"),
        _trace_ref(item["provenance_ref"], "provenance_ref"),
        _version(item["contract_version"], "contract_version"),
        _text(item["membership_policy"], "membership_policy"),
    )


def _decode_real_csv_source_declaration(payload: Any) -> RealCsvSourceDeclaration:
    fields = {
        "provenance_id",
        "version",
        "source_ref",
        "instrument_ref",
        "timeframe_ref",
        "schema_ref",
        "provider_name",
        "acquisition_method",
        "declared_market",
        "declared_acquisition_time",
        "timestamp_semantics",
        "availability_semantics",
        "timezone_rule",
        "column_mapping",
        "price_domain",
        "ohlc_semantics",
        "volume_semantics",
        "finality_assumptions",
        "missing_data_policy",
        "duplicate_policy",
        "ordering_policy",
        "permission_state",
        "license_reference",
        "retention_classification",
        "deletion_restriction",
        "redistribution_restriction",
        "operator_id",
        "provenance_note",
        "contract_version",
    }
    item = _strict_object(payload, fields, "RealCsvSourceDeclaration.payload")
    return RealCsvSourceDeclaration(
        cast(ProvenanceId, _typed_id(item["provenance_id"], ProvenanceId, "provenance_id")),
        _version(item["version"], "version"),
        _trace_ref(item["source_ref"], "source_ref"),
        _trace_ref(item["instrument_ref"], "instrument_ref"),
        _trace_ref(item["timeframe_ref"], "timeframe_ref"),
        _trace_ref(item["schema_ref"], "schema_ref"),
        _text(item["provider_name"], "provider_name"),
        AcquisitionMethod(_text(item["acquisition_method"], "acquisition_method")),
        _text(item["declared_market"], "declared_market"),
        None
        if item["declared_acquisition_time"] is None
        else _timestamp(item["declared_acquisition_time"], "declared_acquisition_time"),
        TimestampSemantics(_text(item["timestamp_semantics"], "timestamp_semantics")),
        AvailabilitySemantics(_text(item["availability_semantics"], "availability_semantics")),
        _text(item["timezone_rule"], "timezone_rule"),
        _metadata(item["column_mapping"], "column_mapping"),
        PriceDomain(_text(item["price_domain"], "price_domain")),
        _text(item["ohlc_semantics"], "ohlc_semantics"),
        VolumeSemantic(_text(item["volume_semantics"], "volume_semantics")),
        _text(item["finality_assumptions"], "finality_assumptions"),
        MissingDataPolicy(_text(item["missing_data_policy"], "missing_data_policy")),
        DuplicatePolicy(_text(item["duplicate_policy"], "duplicate_policy")),
        OrderingPolicy(_text(item["ordering_policy"], "ordering_policy")),
        SourcePermissionState(_text(item["permission_state"], "permission_state")),
        _optional_text(item["license_reference"], "license_reference"),
        RetentionClassification(
            _text(item["retention_classification"], "retention_classification")
        ),
        _optional_text(item["deletion_restriction"], "deletion_restriction"),
        _optional_text(item["redistribution_restriction"], "redistribution_restriction"),
        cast(AgentId, _typed_id(item["operator_id"], AgentId, "operator_id")),
        _text(item["provenance_note"], "provenance_note"),
        _version(item["contract_version"], "contract_version"),
    )


def _decode_real_csv_admission(payload: Any) -> RealCsvAdmissionRecord:
    fields = {
        "admission_id",
        "version",
        "source_declaration_ref",
        "original_filename",
        "bounded_relative_path",
        "file_sha256",
        "file_size",
        "ingestion_time",
        "parser_contract_version",
        "canonical_codec_version",
        "ingestion_configuration_fingerprint",
        "row_count",
        "status",
        "findings",
        "raw_manifest_ref",
        "raw_lock_ref",
        "normalized_manifest_ref",
        "normalized_lock_ref",
        "trust_state",
        "research_eligibility",
        "contract_version",
    }
    item = _strict_object(payload, fields, "RealCsvAdmissionRecord.payload")
    file_size = item["file_size"]
    row_count = item["row_count"]
    if any(
        isinstance(value, bool) or not isinstance(value, int) for value in (file_size, row_count)
    ):
        raise InvalidSerialization("file_size and row_count must be integers")
    return RealCsvAdmissionRecord(
        cast(ArtifactId, _typed_id(item["admission_id"], ArtifactId, "admission_id")),
        _version(item["version"], "version"),
        _trace_ref(item["source_declaration_ref"], "source_declaration_ref"),
        _text(item["original_filename"], "original_filename"),
        _text(item["bounded_relative_path"], "bounded_relative_path"),
        _text(item["file_sha256"], "file_sha256"),
        file_size,
        _timestamp(item["ingestion_time"], "ingestion_time"),
        _version(item["parser_contract_version"], "parser_contract_version"),
        _version(item["canonical_codec_version"], "canonical_codec_version"),
        _text(
            item["ingestion_configuration_fingerprint"],
            "ingestion_configuration_fingerprint",
        ),
        row_count,
        CsvAdmissionStatus(_text(item["status"], "status")),
        _strings(item["findings"], "findings"),
        _optional_trace_ref(item["raw_manifest_ref"], "raw_manifest_ref"),
        _optional_trace_ref(item["raw_lock_ref"], "raw_lock_ref"),
        _optional_trace_ref(item["normalized_manifest_ref"], "normalized_manifest_ref"),
        _optional_trace_ref(item["normalized_lock_ref"], "normalized_lock_ref"),
        CsvTrustState(_text(item["trust_state"], "trust_state")),
        ResearchEligibilityState(_text(item["research_eligibility"], "research_eligibility")),
        _version(item["contract_version"], "contract_version"),
    )


def _decode_research_eligibility_policy(payload: Any) -> ResearchDatasetEligibilityPolicy:
    fields = {
        "policy_id",
        "version",
        "accepted_permission_states",
        "accepted_retention_classifications",
        "required_timestamp_semantics",
        "required_availability_semantics",
        "accepted_missing_data_policies",
        "accepted_duplicate_policies",
        "accepted_ordering_policies",
        "calendar_semantics",
        "knowledge_cutoff",
        "minimum_row_count",
        "maximum_rejected_rows",
        "maximum_quarantined_observations",
        "maximum_gap_findings",
        "maximum_missing_intervals",
        "require_complete_bars",
        "allow_restricted_redistribution_for_local_research",
        "policy_owner_id",
        "contract_version",
    }
    item = _strict_object(payload, fields, "ResearchDatasetEligibilityPolicy.payload")
    return ResearchDatasetEligibilityPolicy(
        cast(ArtifactId, _typed_id(item["policy_id"], ArtifactId, "policy_id")),
        _version(item["version"], "version"),
        tuple(
            SourcePermissionState(value)
            for value in _strings(item["accepted_permission_states"], "accepted_permission_states")
        ),
        tuple(
            RetentionClassification(value)
            for value in _strings(
                item["accepted_retention_classifications"],
                "accepted_retention_classifications",
            )
        ),
        TimestampSemantics(
            _text(item["required_timestamp_semantics"], "required_timestamp_semantics")
        ),
        AvailabilitySemantics(
            _text(item["required_availability_semantics"], "required_availability_semantics")
        ),
        tuple(
            MissingDataPolicy(value)
            for value in _strings(
                item["accepted_missing_data_policies"], "accepted_missing_data_policies"
            )
        ),
        tuple(
            DuplicatePolicy(value)
            for value in _strings(
                item["accepted_duplicate_policies"], "accepted_duplicate_policies"
            )
        ),
        tuple(
            OrderingPolicy(value)
            for value in _strings(item["accepted_ordering_policies"], "accepted_ordering_policies")
        ),
        EligibilityCalendarSemantics(_text(item["calendar_semantics"], "calendar_semantics")),
        _timestamp(item["knowledge_cutoff"], "knowledge_cutoff"),
        _integer(item["minimum_row_count"], "minimum_row_count"),
        _integer(item["maximum_rejected_rows"], "maximum_rejected_rows"),
        _integer(
            item["maximum_quarantined_observations"],
            "maximum_quarantined_observations",
        ),
        _integer(item["maximum_gap_findings"], "maximum_gap_findings"),
        _integer(item["maximum_missing_intervals"], "maximum_missing_intervals"),
        _boolean(item["require_complete_bars"], "require_complete_bars"),
        _boolean(
            item["allow_restricted_redistribution_for_local_research"],
            "allow_restricted_redistribution_for_local_research",
        ),
        cast(AgentId, _typed_id(item["policy_owner_id"], AgentId, "policy_owner_id")),
        _version(item["contract_version"], "contract_version"),
    )


def _decode_research_eligibility_record(payload: Any) -> ResearchDatasetEligibilityRecord:
    fields = {
        "eligibility_id",
        "version",
        "admission_ref",
        "source_declaration_ref",
        "source_ref",
        "instrument_ref",
        "timeframe_ref",
        "schema_ref",
        "raw_manifest_ref",
        "raw_lock_ref",
        "normalized_manifest_ref",
        "normalized_lock_ref",
        "policy_ref",
        "quality_context_fingerprint",
        "status",
        "findings",
        "decision_time",
        "decision_actor_id",
        "trust_state",
        "research_boundary",
        "experiment_authorization",
        "validation_status",
        "deployment_authorization",
        "execution_state",
        "contract_version",
    }
    item = _strict_object(payload, fields, "ResearchDatasetEligibilityRecord.payload")
    return ResearchDatasetEligibilityRecord(
        cast(ArtifactId, _typed_id(item["eligibility_id"], ArtifactId, "eligibility_id")),
        _version(item["version"], "version"),
        _trace_ref(item["admission_ref"], "admission_ref"),
        _trace_ref(item["source_declaration_ref"], "source_declaration_ref"),
        _trace_ref(item["source_ref"], "source_ref"),
        _trace_ref(item["instrument_ref"], "instrument_ref"),
        _trace_ref(item["timeframe_ref"], "timeframe_ref"),
        _trace_ref(item["schema_ref"], "schema_ref"),
        _optional_trace_ref(item["raw_manifest_ref"], "raw_manifest_ref"),
        _optional_trace_ref(item["raw_lock_ref"], "raw_lock_ref"),
        _optional_trace_ref(item["normalized_manifest_ref"], "normalized_manifest_ref"),
        _optional_trace_ref(item["normalized_lock_ref"], "normalized_lock_ref"),
        _trace_ref(item["policy_ref"], "policy_ref"),
        _text(item["quality_context_fingerprint"], "quality_context_fingerprint"),
        ResearchDatasetEligibilityStatus(_text(item["status"], "status")),
        _strings(item["findings"], "findings"),
        _timestamp(item["decision_time"], "decision_time"),
        cast(AgentId, _typed_id(item["decision_actor_id"], AgentId, "decision_actor_id")),
        CsvTrustState(_text(item["trust_state"], "trust_state")),
        ResearchBoundaryStatus(_text(item["research_boundary"], "research_boundary")),
        ExperimentAuthorizationStatus(
            _text(item["experiment_authorization"], "experiment_authorization")
        ),
        ValidationStatus(_text(item["validation_status"], "validation_status")),
        DeploymentAuthorizationStatus(
            _text(item["deployment_authorization"], "deployment_authorization")
        ),
        ExecutionState(_text(item["execution_state"], "execution_state")),
        _version(item["contract_version"], "contract_version"),
    )


def _decode_experiment_specification(payload: Any) -> ExperimentSpecification:
    fields = {
        "experiment_id",
        "version",
        "eligibility_ref",
        "normalized_manifest_ref",
        "normalized_lock_ref",
        "family",
        "research_objective",
        "hypothesis_id",
        "configuration",
        "random_seed",
        "observation_start",
        "observation_end",
        "knowledge_cutoff",
        "no_lookahead",
        "warmup_bars",
        "commission_semantics",
        "commission_bps",
        "slippage_semantics",
        "slippage_bps",
        "funding_semantics",
        "funding_bps",
        "calendar_semantics",
        "sizing_semantics",
        "capital_notional_minor",
        "engine_contract_ref",
        "requested_metrics",
        "requested_outputs",
        "proposer_id",
        "provenance_ref",
        "contract_version",
    }
    item = _strict_object(payload, fields, "ExperimentSpecification.payload")
    return ExperimentSpecification(
        cast(ExperimentId, _typed_id(item["experiment_id"], ExperimentId, "experiment_id")),
        _version(item["version"], "version"),
        _trace_ref(item["eligibility_ref"], "eligibility_ref"),
        _trace_ref(item["normalized_manifest_ref"], "normalized_manifest_ref"),
        _trace_ref(item["normalized_lock_ref"], "normalized_lock_ref"),
        ExperimentFamily(_text(item["family"], "family")),
        _text(item["research_objective"], "research_objective"),
        cast(ArtifactId, _typed_id(item["hypothesis_id"], ArtifactId, "hypothesis_id")),
        _metadata(item["configuration"], "configuration"),
        _integer(item["random_seed"], "random_seed"),
        _timestamp(item["observation_start"], "observation_start"),
        _timestamp(item["observation_end"], "observation_end"),
        _timestamp(item["knowledge_cutoff"], "knowledge_cutoff"),
        NoLookaheadSemantics(_text(item["no_lookahead"], "no_lookahead")),
        _integer(item["warmup_bars"], "warmup_bars"),
        CostSemantics(_text(item["commission_semantics"], "commission_semantics")),
        _integer(item["commission_bps"], "commission_bps"),
        CostSemantics(_text(item["slippage_semantics"], "slippage_semantics")),
        _integer(item["slippage_bps"], "slippage_bps"),
        CostSemantics(_text(item["funding_semantics"], "funding_semantics")),
        _integer(item["funding_bps"], "funding_bps"),
        EligibilityCalendarSemantics(_text(item["calendar_semantics"], "calendar_semantics")),
        PositionSizingSemantics(_text(item["sizing_semantics"], "sizing_semantics")),
        _integer(item["capital_notional_minor"], "capital_notional_minor"),
        _trace_ref(item["engine_contract_ref"], "engine_contract_ref"),
        _strings(item["requested_metrics"], "requested_metrics"),
        _strings(item["requested_outputs"], "requested_outputs"),
        cast(AgentId, _typed_id(item["proposer_id"], AgentId, "proposer_id")),
        _trace_ref(item["provenance_ref"], "provenance_ref"),
        _version(item["contract_version"], "contract_version"),
    )


def _decode_experiment_authorization_policy(payload: Any) -> ExperimentAuthorizationPolicy:
    fields = {
        "policy_id",
        "version",
        "allowed_families",
        "required_no_lookahead",
        "accepted_calendars",
        "require_explicit_commission",
        "require_explicit_slippage",
        "require_explicit_funding",
        "require_position_sizing",
        "maximum_window_days",
        "minimum_seed",
        "maximum_seed",
        "supported_engine_refs",
        "require_verified_actor_authority",
        "policy_owner_id",
        "contract_version",
    }
    item = _strict_object(payload, fields, "ExperimentAuthorizationPolicy.payload")
    return ExperimentAuthorizationPolicy(
        cast(ArtifactId, _typed_id(item["policy_id"], ArtifactId, "policy_id")),
        _version(item["version"], "version"),
        tuple(
            ExperimentFamily(value)
            for value in _strings(item["allowed_families"], "allowed_families")
        ),
        NoLookaheadSemantics(_text(item["required_no_lookahead"], "required_no_lookahead")),
        tuple(
            EligibilityCalendarSemantics(value)
            for value in _strings(item["accepted_calendars"], "accepted_calendars")
        ),
        _boolean(item["require_explicit_commission"], "require_explicit_commission"),
        _boolean(item["require_explicit_slippage"], "require_explicit_slippage"),
        _boolean(item["require_explicit_funding"], "require_explicit_funding"),
        _boolean(item["require_position_sizing"], "require_position_sizing"),
        _integer(item["maximum_window_days"], "maximum_window_days"),
        _integer(item["minimum_seed"], "minimum_seed"),
        _integer(item["maximum_seed"], "maximum_seed"),
        _trace_refs(item["supported_engine_refs"], "supported_engine_refs"),
        _boolean(item["require_verified_actor_authority"], "require_verified_actor_authority"),
        cast(AgentId, _typed_id(item["policy_owner_id"], AgentId, "policy_owner_id")),
        _version(item["contract_version"], "contract_version"),
    )


def _decode_experiment_authorization_record(payload: Any) -> ExperimentAuthorizationRecord:
    fields = {
        "authorization_id",
        "version",
        "specification_ref",
        "eligibility_ref",
        "policy_ref",
        "normalized_manifest_ref",
        "normalized_lock_ref",
        "configuration_fingerprint",
        "status",
        "findings",
        "decision_time",
        "decision_actor_id",
        "lifecycle",
        "validation_status",
        "deployment_authorization",
        "execution_state",
        "contract_version",
    }
    item = _strict_object(payload, fields, "ExperimentAuthorizationRecord.payload")
    return ExperimentAuthorizationRecord(
        cast(ArtifactId, _typed_id(item["authorization_id"], ArtifactId, "authorization_id")),
        _version(item["version"], "version"),
        _trace_ref(item["specification_ref"], "specification_ref"),
        _trace_ref(item["eligibility_ref"], "eligibility_ref"),
        _trace_ref(item["policy_ref"], "policy_ref"),
        _trace_ref(item["normalized_manifest_ref"], "normalized_manifest_ref"),
        _trace_ref(item["normalized_lock_ref"], "normalized_lock_ref"),
        _text(item["configuration_fingerprint"], "configuration_fingerprint"),
        ExperimentAuthorizationDecision(_text(item["status"], "status")),
        _strings(item["findings"], "findings"),
        _timestamp(item["decision_time"], "decision_time"),
        cast(AgentId, _typed_id(item["decision_actor_id"], AgentId, "decision_actor_id")),
        ExperimentLifecycleBoundary(_text(item["lifecycle"], "lifecycle")),
        ValidationStatus(_text(item["validation_status"], "validation_status")),
        DeploymentAuthorizationStatus(
            _text(item["deployment_authorization"], "deployment_authorization")
        ),
        ExecutionState(_text(item["execution_state"], "execution_state")),
        _version(item["contract_version"], "contract_version"),
    )


def _decode_experiment_replay_contract(payload: Any) -> ExperimentReplayContract:
    fields = {
        "engine_id",
        "version",
        "family",
        "no_lookahead",
        "ordering",
        "numeric_semantics",
        "decimal_precision",
        "supported_metrics",
        "supported_outputs",
        "contract_version",
    }
    item = _strict_object(payload, fields, "ExperimentReplayContract.payload")
    return ExperimentReplayContract(
        cast(ArtifactId, _typed_id(item["engine_id"], ArtifactId, "engine_id")),
        _version(item["version"], "version"),
        ExperimentFamily(_text(item["family"], "family")),
        NoLookaheadSemantics(_text(item["no_lookahead"], "no_lookahead")),
        ReplayOrdering(_text(item["ordering"], "ordering")),
        NumericSemantics(_text(item["numeric_semantics"], "numeric_semantics")),
        _integer(item["decimal_precision"], "decimal_precision"),
        _strings(item["supported_metrics"], "supported_metrics"),
        _strings(item["supported_outputs"], "supported_outputs"),
        _version(item["contract_version"], "contract_version"),
    )


def _decode_experiment_result_artifact(payload: Any) -> ExperimentResultArtifact:
    fields = {
        "artifact_id",
        "version",
        "run_id",
        "run_version",
        "run_input_fingerprint",
        "authorization_ref",
        "specification_ref",
        "policy_ref",
        "eligibility_ref",
        "normalized_manifest_ref",
        "normalized_lock_ref",
        "engine_contract_ref",
        "configuration_fingerprint",
        "random_seed",
        "observation_count",
        "first_event_time",
        "last_event_time",
        "last_knowledge_time",
        "close_min",
        "close_max",
        "simple_returns",
        "simple_return_mean",
        "simple_return_population_variance",
        "return_series_fingerprint",
        "validation_status",
        "deployment_authorization",
        "execution_state",
        "contract_version",
    }
    item = _strict_object(payload, fields, "ExperimentResultArtifact.payload")
    return ExperimentResultArtifact(
        cast(ArtifactId, _typed_id(item["artifact_id"], ArtifactId, "artifact_id")),
        _version(item["version"], "version"),
        cast(RunId, _typed_id(item["run_id"], RunId, "run_id")),
        _version(item["run_version"], "run_version"),
        _text(item["run_input_fingerprint"], "run_input_fingerprint"),
        _trace_ref(item["authorization_ref"], "authorization_ref"),
        _trace_ref(item["specification_ref"], "specification_ref"),
        _trace_ref(item["policy_ref"], "policy_ref"),
        _trace_ref(item["eligibility_ref"], "eligibility_ref"),
        _trace_ref(item["normalized_manifest_ref"], "normalized_manifest_ref"),
        _trace_ref(item["normalized_lock_ref"], "normalized_lock_ref"),
        _trace_ref(item["engine_contract_ref"], "engine_contract_ref"),
        _text(item["configuration_fingerprint"], "configuration_fingerprint"),
        _integer(item["random_seed"], "random_seed"),
        _integer(item["observation_count"], "observation_count"),
        _timestamp(item["first_event_time"], "first_event_time"),
        _timestamp(item["last_event_time"], "last_event_time"),
        _timestamp(item["last_knowledge_time"], "last_knowledge_time"),
        _text(item["close_min"], "close_min"),
        _text(item["close_max"], "close_max"),
        _strings(item["simple_returns"], "simple_returns"),
        _optional_text(item["simple_return_mean"], "simple_return_mean"),
        _optional_text(
            item["simple_return_population_variance"],
            "simple_return_population_variance",
        ),
        _text(item["return_series_fingerprint"], "return_series_fingerprint"),
        ValidationStatus(_text(item["validation_status"], "validation_status")),
        DeploymentAuthorizationStatus(
            _text(item["deployment_authorization"], "deployment_authorization")
        ),
        ExecutionState(_text(item["execution_state"], "execution_state")),
        _version(item["contract_version"], "contract_version"),
    )


def _decode_experiment_run_record(payload: Any) -> ExperimentRunRecord:
    fields = {
        "run_id",
        "version",
        "authorization_ref",
        "specification_ref",
        "policy_ref",
        "eligibility_ref",
        "normalized_manifest_ref",
        "normalized_lock_ref",
        "engine_contract_ref",
        "configuration_fingerprint",
        "random_seed",
        "observation_start",
        "observation_end",
        "knowledge_cutoff",
        "run_input_fingerprint",
        "result_ref",
        "status",
        "completed_at",
        "provenance_ref",
        "research_execution",
        "validation_status",
        "deployment_authorization",
        "execution_state",
        "contract_version",
    }
    item = _strict_object(payload, fields, "ExperimentRunRecord.payload")
    return ExperimentRunRecord(
        cast(RunId, _typed_id(item["run_id"], RunId, "run_id")),
        _version(item["version"], "version"),
        _trace_ref(item["authorization_ref"], "authorization_ref"),
        _trace_ref(item["specification_ref"], "specification_ref"),
        _trace_ref(item["policy_ref"], "policy_ref"),
        _trace_ref(item["eligibility_ref"], "eligibility_ref"),
        _trace_ref(item["normalized_manifest_ref"], "normalized_manifest_ref"),
        _trace_ref(item["normalized_lock_ref"], "normalized_lock_ref"),
        _trace_ref(item["engine_contract_ref"], "engine_contract_ref"),
        _text(item["configuration_fingerprint"], "configuration_fingerprint"),
        _integer(item["random_seed"], "random_seed"),
        _timestamp(item["observation_start"], "observation_start"),
        _timestamp(item["observation_end"], "observation_end"),
        _timestamp(item["knowledge_cutoff"], "knowledge_cutoff"),
        _text(item["run_input_fingerprint"], "run_input_fingerprint"),
        _trace_ref(item["result_ref"], "result_ref"),
        ExperimentRunStatus(_text(item["status"], "status")),
        _timestamp(item["completed_at"], "completed_at"),
        _trace_ref(item["provenance_ref"], "provenance_ref"),
        ResearchExperimentExecutionStatus(_text(item["research_execution"], "research_execution")),
        ValidationStatus(_text(item["validation_status"], "validation_status")),
        DeploymentAuthorizationStatus(
            _text(item["deployment_authorization"], "deployment_authorization")
        ),
        ExecutionState(_text(item["execution_state"], "execution_state")),
        _version(item["contract_version"], "contract_version"),
    )


def _decode_strategy_definition(payload: Any) -> StrategyDefinition:
    fields = {
        "strategy_id",
        "version",
        "model",
        "signal_timing",
        "execution_timing",
        "side_permission",
        "threshold_bps",
        "fixed_notional_minor",
        "capital_currency",
        "capital_minor_unit_scale",
        "allow_pyramiding",
        "force_close_at_window_end",
        "engine_contract_ref",
        "provenance_ref",
        "contract_version",
    }
    item = _strict_object(payload, fields, "StrategyDefinition.payload")
    return StrategyDefinition(
        cast(ArtifactId, _typed_id(item["strategy_id"], ArtifactId, "strategy_id")),
        _version(item["version"], "version"),
        StrategyModel(_text(item["model"], "model")),
        SignalTiming(_text(item["signal_timing"], "signal_timing")),
        SimulatedExecutionTiming(_text(item["execution_timing"], "execution_timing")),
        SidePermission(_text(item["side_permission"], "side_permission")),
        _integer(item["threshold_bps"], "threshold_bps"),
        _integer(item["fixed_notional_minor"], "fixed_notional_minor"),
        _text(item["capital_currency"], "capital_currency"),
        _integer(item["capital_minor_unit_scale"], "capital_minor_unit_scale"),
        _boolean(item["allow_pyramiding"], "allow_pyramiding"),
        _boolean(item["force_close_at_window_end"], "force_close_at_window_end"),
        _trace_ref(item["engine_contract_ref"], "engine_contract_ref"),
        _trace_ref(item["provenance_ref"], "provenance_ref"),
        _version(item["contract_version"], "contract_version"),
    )


def _decode_simulated_order(payload: Any, field: str) -> SimulatedOrder:
    item = _strict_object(
        payload,
        {
            "order_id",
            "side",
            "notional",
            "signal_time",
            "submitted_time",
            "eligible_fill_time",
            "source_bar_ref",
            "fill_bar_ref",
            "strategy_ref",
            "run_id",
            "run_version",
            "status",
        },
        field,
    )
    return SimulatedOrder(
        cast(ArtifactId, _typed_id(item["order_id"], ArtifactId, f"{field}.order_id")),
        SimulatedOrderSide(_text(item["side"], f"{field}.side")),
        _text(item["notional"], f"{field}.notional"),
        _timestamp(item["signal_time"], f"{field}.signal_time"),
        _timestamp(item["submitted_time"], f"{field}.submitted_time"),
        _timestamp(item["eligible_fill_time"], f"{field}.eligible_fill_time"),
        _trace_ref(item["source_bar_ref"], f"{field}.source_bar_ref"),
        _trace_ref(item["fill_bar_ref"], f"{field}.fill_bar_ref"),
        _trace_ref(item["strategy_ref"], f"{field}.strategy_ref"),
        cast(RunId, _typed_id(item["run_id"], RunId, f"{field}.run_id")),
        _version(item["run_version"], f"{field}.run_version"),
        SimulatedOrderStatus(_text(item["status"], f"{field}.status")),
    )


def _decode_simulated_fill(payload: Any, field: str) -> SimulatedFill:
    item = _strict_object(
        payload,
        {
            "fill_id",
            "order_id",
            "side",
            "bar_ref",
            "fill_time",
            "reference_price",
            "execution_price",
            "quantity",
            "fill_notional",
            "commission",
            "slippage_cost",
        },
        field,
    )
    return SimulatedFill(
        cast(ArtifactId, _typed_id(item["fill_id"], ArtifactId, f"{field}.fill_id")),
        cast(ArtifactId, _typed_id(item["order_id"], ArtifactId, f"{field}.order_id")),
        SimulatedOrderSide(_text(item["side"], f"{field}.side")),
        _trace_ref(item["bar_ref"], f"{field}.bar_ref"),
        _timestamp(item["fill_time"], f"{field}.fill_time"),
        _text(item["reference_price"], f"{field}.reference_price"),
        _text(item["execution_price"], f"{field}.execution_price"),
        _text(item["quantity"], f"{field}.quantity"),
        _text(item["fill_notional"], f"{field}.fill_notional"),
        _text(item["commission"], f"{field}.commission"),
        _text(item["slippage_cost"], f"{field}.slippage_cost"),
    )


def _decode_simulated_trade(payload: Any, field: str) -> SimulatedTrade:
    item = _strict_object(
        payload,
        {
            "trade_id",
            "entry_fill_id",
            "exit_fill_id",
            "quantity",
            "entry_price",
            "exit_price",
            "gross_pnl",
            "commission",
            "slippage_cost",
            "net_pnl",
            "entry_time",
            "exit_time",
            "strategy_ref",
            "run_id",
            "run_version",
        },
        field,
    )
    return SimulatedTrade(
        cast(ArtifactId, _typed_id(item["trade_id"], ArtifactId, f"{field}.trade_id")),
        cast(ArtifactId, _typed_id(item["entry_fill_id"], ArtifactId, f"{field}.entry_fill_id")),
        cast(ArtifactId, _typed_id(item["exit_fill_id"], ArtifactId, f"{field}.exit_fill_id")),
        _text(item["quantity"], f"{field}.quantity"),
        _text(item["entry_price"], f"{field}.entry_price"),
        _text(item["exit_price"], f"{field}.exit_price"),
        _text(item["gross_pnl"], f"{field}.gross_pnl"),
        _text(item["commission"], f"{field}.commission"),
        _text(item["slippage_cost"], f"{field}.slippage_cost"),
        _text(item["net_pnl"], f"{field}.net_pnl"),
        _timestamp(item["entry_time"], f"{field}.entry_time"),
        _timestamp(item["exit_time"], f"{field}.exit_time"),
        _trace_ref(item["strategy_ref"], f"{field}.strategy_ref"),
        cast(RunId, _typed_id(item["run_id"], RunId, f"{field}.run_id")),
        _version(item["run_version"], f"{field}.run_version"),
    )


def _decode_equity_point(payload: Any, field: str) -> EquityPoint:
    item = _strict_object(
        payload,
        {
            "event_time",
            "bar_ref",
            "cash",
            "position_quantity",
            "position_value",
            "unrealized_pnl",
            "realized_pnl",
            "equity",
        },
        field,
    )
    return EquityPoint(
        _timestamp(item["event_time"], f"{field}.event_time"),
        _trace_ref(item["bar_ref"], f"{field}.bar_ref"),
        _text(item["cash"], f"{field}.cash"),
        _text(item["position_quantity"], f"{field}.position_quantity"),
        _text(item["position_value"], f"{field}.position_value"),
        _text(item["unrealized_pnl"], f"{field}.unrealized_pnl"),
        _text(item["realized_pnl"], f"{field}.realized_pnl"),
        _text(item["equity"], f"{field}.equity"),
    )


def _decoded_tuple(value: Any, field: str, decoder: Any) -> tuple[Any, ...]:
    if not isinstance(value, list):
        raise InvalidSerialization(f"{field} must be an array")
    return tuple(decoder(item, f"{field}[]") for item in value)


def _decode_backtest_result(payload: Any) -> BacktestResultArtifact:
    fields = {
        "artifact_id",
        "version",
        "run_id",
        "run_version",
        "run_input_fingerprint",
        "authorization_ref",
        "specification_ref",
        "policy_ref",
        "eligibility_ref",
        "normalized_manifest_ref",
        "normalized_lock_ref",
        "engine_contract_ref",
        "strategy_ref",
        "configuration_fingerprint",
        "capital_currency",
        "capital_minor_unit_scale",
        "initial_capital",
        "orders",
        "fills",
        "trades",
        "equity_curve",
        "final_cash",
        "final_equity",
        "open_position",
        "trade_count",
        "gross_pnl",
        "net_pnl",
        "total_return",
        "max_drawdown",
        "validation_status",
        "deployment_authorization",
        "execution_state",
        "contract_version",
    }
    item = _strict_object(payload, fields, "BacktestResultArtifact.payload")
    return BacktestResultArtifact(
        cast(ArtifactId, _typed_id(item["artifact_id"], ArtifactId, "artifact_id")),
        _version(item["version"], "version"),
        cast(RunId, _typed_id(item["run_id"], RunId, "run_id")),
        _version(item["run_version"], "run_version"),
        _text(item["run_input_fingerprint"], "run_input_fingerprint"),
        _trace_ref(item["authorization_ref"], "authorization_ref"),
        _trace_ref(item["specification_ref"], "specification_ref"),
        _trace_ref(item["policy_ref"], "policy_ref"),
        _trace_ref(item["eligibility_ref"], "eligibility_ref"),
        _trace_ref(item["normalized_manifest_ref"], "normalized_manifest_ref"),
        _trace_ref(item["normalized_lock_ref"], "normalized_lock_ref"),
        _trace_ref(item["engine_contract_ref"], "engine_contract_ref"),
        _trace_ref(item["strategy_ref"], "strategy_ref"),
        _text(item["configuration_fingerprint"], "configuration_fingerprint"),
        _text(item["capital_currency"], "capital_currency"),
        _integer(item["capital_minor_unit_scale"], "capital_minor_unit_scale"),
        _text(item["initial_capital"], "initial_capital"),
        cast(
            tuple[SimulatedOrder, ...],
            _decoded_tuple(item["orders"], "orders", _decode_simulated_order),
        ),
        cast(
            tuple[SimulatedFill, ...],
            _decoded_tuple(item["fills"], "fills", _decode_simulated_fill),
        ),
        cast(
            tuple[SimulatedTrade, ...],
            _decoded_tuple(item["trades"], "trades", _decode_simulated_trade),
        ),
        cast(
            tuple[EquityPoint, ...],
            _decoded_tuple(item["equity_curve"], "equity_curve", _decode_equity_point),
        ),
        _text(item["final_cash"], "final_cash"),
        _text(item["final_equity"], "final_equity"),
        SimulatedPositionState(_text(item["open_position"], "open_position")),
        _integer(item["trade_count"], "trade_count"),
        _text(item["gross_pnl"], "gross_pnl"),
        _text(item["net_pnl"], "net_pnl"),
        _text(item["total_return"], "total_return"),
        _text(item["max_drawdown"], "max_drawdown"),
        ValidationStatus(_text(item["validation_status"], "validation_status")),
        DeploymentAuthorizationStatus(
            _text(item["deployment_authorization"], "deployment_authorization")
        ),
        ExecutionState(_text(item["execution_state"], "execution_state")),
        _version(item["contract_version"], "contract_version"),
    )


def _decode_backtest_run(payload: Any) -> BacktestRunRecord:
    fields = {
        "run_id",
        "version",
        "authorization_ref",
        "specification_ref",
        "policy_ref",
        "eligibility_ref",
        "normalized_manifest_ref",
        "normalized_lock_ref",
        "engine_contract_ref",
        "strategy_ref",
        "configuration_fingerprint",
        "run_input_fingerprint",
        "result_ref",
        "status",
        "completed_at",
        "provenance_ref",
        "validation_status",
        "deployment_authorization",
        "execution_state",
        "contract_version",
    }
    item = _strict_object(payload, fields, "BacktestRunRecord.payload")
    return BacktestRunRecord(
        cast(RunId, _typed_id(item["run_id"], RunId, "run_id")),
        _version(item["version"], "version"),
        _trace_ref(item["authorization_ref"], "authorization_ref"),
        _trace_ref(item["specification_ref"], "specification_ref"),
        _trace_ref(item["policy_ref"], "policy_ref"),
        _trace_ref(item["eligibility_ref"], "eligibility_ref"),
        _trace_ref(item["normalized_manifest_ref"], "normalized_manifest_ref"),
        _trace_ref(item["normalized_lock_ref"], "normalized_lock_ref"),
        _trace_ref(item["engine_contract_ref"], "engine_contract_ref"),
        _trace_ref(item["strategy_ref"], "strategy_ref"),
        _text(item["configuration_fingerprint"], "configuration_fingerprint"),
        _text(item["run_input_fingerprint"], "run_input_fingerprint"),
        _trace_ref(item["result_ref"], "result_ref"),
        BacktestRunStatus(_text(item["status"], "status")),
        _timestamp(item["completed_at"], "completed_at"),
        _trace_ref(item["provenance_ref"], "provenance_ref"),
        ValidationStatus(_text(item["validation_status"], "validation_status")),
        DeploymentAuthorizationStatus(
            _text(item["deployment_authorization"], "deployment_authorization")
        ),
        ExecutionState(_text(item["execution_state"], "execution_state")),
        _version(item["contract_version"], "contract_version"),
    )


def _decode_validation_plan(payload: Any) -> ValidationPlan:
    fields = {
        "validation_plan_id",
        "version",
        "target_experiment_family",
        "target_metrics",
        "primary_metric",
        "null_hypothesis",
        "alternative_hypothesis",
        "min_sample_size",
        "min_trade_count",
        "uncertainty_method",
        "confidence_level",
        "bootstrap_iterations",
        "random_seed",
        "holdout_policy",
        "multiplicity_policy",
        "validator_authority_ref",
        "provenance_ref",
        "contract_version",
    }
    item = _strict_object(payload, fields, "ValidationPlan.payload")
    return ValidationPlan(
        cast(
            ArtifactId,
            _typed_id(item["validation_plan_id"], ArtifactId, "validation_plan_id"),
        ),
        _version(item["version"], "version"),
        ExperimentFamily(_text(item["target_experiment_family"], "target_experiment_family")),
        tuple(
            ValidationMetric(value) for value in _strings(item["target_metrics"], "target_metrics")
        ),
        ValidationMetric(_text(item["primary_metric"], "primary_metric")),
        NullHypothesis(_text(item["null_hypothesis"], "null_hypothesis")),
        AlternativeHypothesis(_text(item["alternative_hypothesis"], "alternative_hypothesis")),
        _integer(item["min_sample_size"], "min_sample_size"),
        _integer(item["min_trade_count"], "min_trade_count"),
        UncertaintyMethod(_text(item["uncertainty_method"], "uncertainty_method")),
        _text(item["confidence_level"], "confidence_level"),
        _integer(item["bootstrap_iterations"], "bootstrap_iterations"),
        _integer(item["random_seed"], "random_seed"),
        HoldoutPolicy(_text(item["holdout_policy"], "holdout_policy")),
        MultiplicityPolicy(_text(item["multiplicity_policy"], "multiplicity_policy")),
        _trace_ref(item["validator_authority_ref"], "validator_authority_ref"),
        _trace_ref(item["provenance_ref"], "provenance_ref"),
        _version(item["contract_version"], "contract_version"),
    )


def _decode_scientific_validation_result(payload: Any) -> ScientificValidationResult:
    fields = {
        "validation_result_id",
        "version",
        "validation_plan_ref",
        "backtest_result_ref",
        "backtest_run_ref",
        "experiment_ref",
        "strategy_ref",
        "normalized_manifest_ref",
        "normalized_lock_ref",
        "primary_metric",
        "estimate",
        "lower_bound",
        "upper_bound",
        "confidence_level",
        "uncertainty_method",
        "sample_size",
        "trade_count",
        "holdout_status",
        "multiplicity_policy",
        "decision",
        "reason_codes",
        "validator_authority_ref",
        "provenance_ref",
        "scientific_boundary",
        "out_of_sample_evidence",
        "deployment_authorization",
        "execution_state",
        "contract_version",
    }
    item = _strict_object(payload, fields, "ScientificValidationResult.payload")
    return ScientificValidationResult(
        cast(
            ValidationId,
            _typed_id(item["validation_result_id"], ValidationId, "validation_result_id"),
        ),
        _version(item["version"], "version"),
        _trace_ref(item["validation_plan_ref"], "validation_plan_ref"),
        _trace_ref(item["backtest_result_ref"], "backtest_result_ref"),
        _trace_ref(item["backtest_run_ref"], "backtest_run_ref"),
        _trace_ref(item["experiment_ref"], "experiment_ref"),
        _trace_ref(item["strategy_ref"], "strategy_ref"),
        _trace_ref(item["normalized_manifest_ref"], "normalized_manifest_ref"),
        _trace_ref(item["normalized_lock_ref"], "normalized_lock_ref"),
        ValidationMetric(_text(item["primary_metric"], "primary_metric")),
        _text(item["estimate"], "estimate"),
        _text(item["lower_bound"], "lower_bound"),
        _text(item["upper_bound"], "upper_bound"),
        _text(item["confidence_level"], "confidence_level"),
        UncertaintyMethod(_text(item["uncertainty_method"], "uncertainty_method")),
        _integer(item["sample_size"], "sample_size"),
        _integer(item["trade_count"], "trade_count"),
        HoldoutEvidenceStatus(_text(item["holdout_status"], "holdout_status")),
        MultiplicityPolicy(_text(item["multiplicity_policy"], "multiplicity_policy")),
        ScientificValidationDecision(_text(item["decision"], "decision")),
        tuple(
            ValidationReasonCode(value) for value in _strings(item["reason_codes"], "reason_codes")
        ),
        _trace_ref(item["validator_authority_ref"], "validator_authority_ref"),
        _trace_ref(item["provenance_ref"], "provenance_ref"),
        ScientificValidationBoundary(_text(item["scientific_boundary"], "scientific_boundary")),
        OutOfSampleEvidenceStatus(_text(item["out_of_sample_evidence"], "out_of_sample_evidence")),
        DeploymentAuthorizationStatus(
            _text(item["deployment_authorization"], "deployment_authorization")
        ),
        ExecutionState(_text(item["execution_state"], "execution_state")),
        _version(item["contract_version"], "contract_version"),
    )


def _decode_validation_run(payload: Any) -> ValidationRunRecord:
    fields = {
        "validation_run_id",
        "version",
        "validation_plan_ref",
        "backtest_result_ref",
        "backtest_run_ref",
        "validation_input_fingerprint",
        "random_seed",
        "validation_result_ref",
        "validator_authority_ref",
        "completed_at",
        "provenance_ref",
        "status",
        "deployment_authorization",
        "execution_state",
        "contract_version",
    }
    item = _strict_object(payload, fields, "ValidationRunRecord.payload")
    return ValidationRunRecord(
        cast(RunId, _typed_id(item["validation_run_id"], RunId, "validation_run_id")),
        _version(item["version"], "version"),
        _trace_ref(item["validation_plan_ref"], "validation_plan_ref"),
        _trace_ref(item["backtest_result_ref"], "backtest_result_ref"),
        _trace_ref(item["backtest_run_ref"], "backtest_run_ref"),
        _text(item["validation_input_fingerprint"], "validation_input_fingerprint"),
        _integer(item["random_seed"], "random_seed"),
        _trace_ref(item["validation_result_ref"], "validation_result_ref"),
        _trace_ref(item["validator_authority_ref"], "validator_authority_ref"),
        _timestamp(item["completed_at"], "completed_at"),
        _trace_ref(item["provenance_ref"], "provenance_ref"),
        ValidationRunStatus(_text(item["status"], "status")),
        DeploymentAuthorizationStatus(
            _text(item["deployment_authorization"], "deployment_authorization")
        ),
        ExecutionState(_text(item["execution_state"], "execution_state")),
        _version(item["contract_version"], "contract_version"),
    )


def _decode_partition(payload: Any, field: str) -> TemporalPartitionEvidence:
    item = _strict_object(
        payload,
        {"partition_id", "role", "start_index", "end_index", "bar_refs"},
        field,
    )
    refs = item["bar_refs"]
    if not isinstance(refs, list):
        raise InvalidSerialization(f"{field}.bar_refs must be an array")
    return TemporalPartitionEvidence(
        cast(ArtifactId, _typed_id(item["partition_id"], ArtifactId, "partition_id")),
        TemporalPartitionRole(_text(item["role"], "role")),
        _integer(item["start_index"], "start_index"),
        _integer(item["end_index"], "end_index"),
        tuple(_trace_ref(value, f"{field}.bar_refs[]") for value in refs),
    )


def _decode_walk_forward_slice(payload: Any) -> WalkForwardSliceResult:
    item = _strict_object(
        payload,
        {
            "slice_id",
            "train_partition",
            "test_partition",
            "trade_count",
            "total_return",
            "net_pnl",
            "max_drawdown",
            "decision",
        },
        "WalkForwardSliceResult",
    )
    return WalkForwardSliceResult(
        cast(ArtifactId, _typed_id(item["slice_id"], ArtifactId, "slice_id")),
        _decode_partition(item["train_partition"], "train_partition"),
        _decode_partition(item["test_partition"], "test_partition"),
        _integer(item["trade_count"], "trade_count"),
        _text(item["total_return"], "total_return"),
        _text(item["net_pnl"], "net_pnl"),
        _text(item["max_drawdown"], "max_drawdown"),
        RobustnessDecision(_text(item["decision"], "decision")),
    )


def _decode_walk_forward(payload: Any) -> WalkForwardSummary:
    item = _strict_object(
        payload,
        {
            "slices",
            "valid_window_count",
            "positive_window_ratio",
            "median_test_return",
            "worst_test_return",
            "aggregate_test_return",
            "maximum_test_drawdown",
            "minimum_trade_count",
            "decision",
            "reason_codes",
        },
        "WalkForwardSummary",
    )
    slices = item["slices"]
    if not isinstance(slices, list):
        raise InvalidSerialization("walk_forward.slices must be an array")
    return WalkForwardSummary(
        tuple(_decode_walk_forward_slice(value) for value in slices),
        _integer(item["valid_window_count"], "valid_window_count"),
        _text(item["positive_window_ratio"], "positive_window_ratio"),
        _text(item["median_test_return"], "median_test_return"),
        _text(item["worst_test_return"], "worst_test_return"),
        _text(item["aggregate_test_return"], "aggregate_test_return"),
        _text(item["maximum_test_drawdown"], "maximum_test_drawdown"),
        _integer(item["minimum_trade_count"], "minimum_trade_count"),
        RobustnessDecision(_text(item["decision"], "decision")),
        tuple(
            RobustnessReasonCode(value) for value in _strings(item["reason_codes"], "reason_codes")
        ),
    )


def _decode_monte_carlo(payload: Any) -> MonteCarloSummary:
    item = _strict_object(
        payload,
        {
            "policy",
            "iterations",
            "seed",
            "median_terminal_return",
            "lower_terminal_return",
            "upper_terminal_return",
            "worst_observed_drawdown",
            "positive_terminal_fraction",
            "decision",
            "reason_codes",
        },
        "MonteCarloSummary",
    )
    return MonteCarloSummary(
        MonteCarloPolicy(_text(item["policy"], "policy")),
        _integer(item["iterations"], "iterations"),
        _integer(item["seed"], "seed"),
        _text(item["median_terminal_return"], "median_terminal_return"),
        _text(item["lower_terminal_return"], "lower_terminal_return"),
        _text(item["upper_terminal_return"], "upper_terminal_return"),
        _text(item["worst_observed_drawdown"], "worst_observed_drawdown"),
        _text(item["positive_terminal_fraction"], "positive_terminal_fraction"),
        RobustnessDecision(_text(item["decision"], "decision")),
        tuple(
            RobustnessReasonCode(value) for value in _strings(item["reason_codes"], "reason_codes")
        ),
    )


def _decode_cost_scenario(payload: Any) -> CostPerturbationScenario:
    item = _strict_object(
        payload,
        {
            "scenario_id",
            "commission_multiplier",
            "derived_commission_semantics",
            "derived_commission_bps",
            "specification_ref",
            "authorization_ref",
            "backtest_result_ref",
            "total_return",
            "net_pnl",
            "max_drawdown",
            "trade_count",
            "decision",
            "reason_codes",
        },
        "CostPerturbationScenario",
    )
    return CostPerturbationScenario(
        cast(ArtifactId, _typed_id(item["scenario_id"], ArtifactId, "scenario_id")),
        _text(item["commission_multiplier"], "commission_multiplier"),
        CostSemantics(_text(item["derived_commission_semantics"], "derived_commission_semantics")),
        _integer(item["derived_commission_bps"], "derived_commission_bps"),
        _trace_ref(item["specification_ref"], "specification_ref"),
        _trace_ref(item["authorization_ref"], "authorization_ref"),
        _optional_trace_ref(item["backtest_result_ref"], "backtest_result_ref"),
        _optional_text(item["total_return"], "total_return"),
        _optional_text(item["net_pnl"], "net_pnl"),
        _optional_text(item["max_drawdown"], "max_drawdown"),
        None if item["trade_count"] is None else _integer(item["trade_count"], "trade_count"),
        RobustnessDecision(_text(item["decision"], "decision")),
        tuple(
            RobustnessReasonCode(value) for value in _strings(item["reason_codes"], "reason_codes")
        ),
    )


def _decode_cost_perturbation(payload: Any) -> CostPerturbationSummary:
    item = _strict_object(
        payload,
        {"policy", "scenarios", "decision", "reason_codes"},
        "CostPerturbationSummary",
    )
    scenarios = item["scenarios"]
    if not isinstance(scenarios, list):
        raise InvalidSerialization("cost_perturbation.scenarios must be an array")
    return CostPerturbationSummary(
        PerturbationPolicy(_text(item["policy"], "policy")),
        tuple(_decode_cost_scenario(value) for value in scenarios),
        RobustnessDecision(_text(item["decision"], "decision")),
        tuple(
            RobustnessReasonCode(value) for value in _strings(item["reason_codes"], "reason_codes")
        ),
    )


def _decode_robustness_plan(payload: Any) -> RobustnessValidationPlan:
    fields = {
        "robustness_plan_id",
        "version",
        "source_scientific_validation_ref",
        "target_methods",
        "walk_forward_policy",
        "train_bars",
        "test_bars",
        "step_bars",
        "minimum_window_count",
        "minimum_completed_trades_per_test_slice",
        "walk_forward_pass_positive_ratio",
        "walk_forward_fail_positive_ratio",
        "walk_forward_pass_worst_return_floor",
        "walk_forward_severe_loss_floor",
        "monte_carlo_policy",
        "monte_carlo_iterations",
        "monte_carlo_seed",
        "monte_carlo_lower_quantile",
        "monte_carlo_upper_quantile",
        "perturbation_policy",
        "commission_multipliers",
        "perturbation_pass_return_floor",
        "perturbation_fail_return_threshold",
        "robustness_authority_ref",
        "provenance_ref",
        "contract_version",
    }
    item = _strict_object(payload, fields, "RobustnessValidationPlan.payload")
    return RobustnessValidationPlan(
        cast(
            ArtifactId,
            _typed_id(item["robustness_plan_id"], ArtifactId, "robustness_plan_id"),
        ),
        _version(item["version"], "version"),
        _trace_ref(item["source_scientific_validation_ref"], "source_scientific_validation_ref"),
        tuple(
            RobustnessMethod(value) for value in _strings(item["target_methods"], "target_methods")
        ),
        WalkForwardPolicy(_text(item["walk_forward_policy"], "walk_forward_policy")),
        _integer(item["train_bars"], "train_bars"),
        _integer(item["test_bars"], "test_bars"),
        _integer(item["step_bars"], "step_bars"),
        _integer(item["minimum_window_count"], "minimum_window_count"),
        _integer(
            item["minimum_completed_trades_per_test_slice"],
            "minimum_completed_trades_per_test_slice",
        ),
        _text(item["walk_forward_pass_positive_ratio"], "walk_forward_pass_positive_ratio"),
        _text(item["walk_forward_fail_positive_ratio"], "walk_forward_fail_positive_ratio"),
        _text(
            item["walk_forward_pass_worst_return_floor"],
            "walk_forward_pass_worst_return_floor",
        ),
        _text(item["walk_forward_severe_loss_floor"], "walk_forward_severe_loss_floor"),
        MonteCarloPolicy(_text(item["monte_carlo_policy"], "monte_carlo_policy")),
        _integer(item["monte_carlo_iterations"], "monte_carlo_iterations"),
        _integer(item["monte_carlo_seed"], "monte_carlo_seed"),
        _text(item["monte_carlo_lower_quantile"], "monte_carlo_lower_quantile"),
        _text(item["monte_carlo_upper_quantile"], "monte_carlo_upper_quantile"),
        PerturbationPolicy(_text(item["perturbation_policy"], "perturbation_policy")),
        _strings(item["commission_multipliers"], "commission_multipliers"),
        _text(item["perturbation_pass_return_floor"], "perturbation_pass_return_floor"),
        _text(
            item["perturbation_fail_return_threshold"],
            "perturbation_fail_return_threshold",
        ),
        _trace_ref(item["robustness_authority_ref"], "robustness_authority_ref"),
        _trace_ref(item["provenance_ref"], "provenance_ref"),
        _version(item["contract_version"], "contract_version"),
    )


def _decode_robustness_result(payload: Any) -> RobustnessValidationResult:
    fields = {
        "robustness_result_id",
        "version",
        "robustness_plan_ref",
        "scientific_validation_result_ref",
        "validation_run_ref",
        "backtest_result_ref",
        "backtest_run_ref",
        "strategy_ref",
        "experiment_ref",
        "normalized_manifest_ref",
        "normalized_lock_ref",
        "walk_forward",
        "monte_carlo",
        "cost_perturbation",
        "holdout_evidence",
        "decision",
        "reason_codes",
        "robustness_authority_ref",
        "provenance_ref",
        "deployment_authorization",
        "execution_state",
        "contract_version",
    }
    item = _strict_object(payload, fields, "RobustnessValidationResult.payload")
    return RobustnessValidationResult(
        cast(
            ArtifactId,
            _typed_id(item["robustness_result_id"], ArtifactId, "robustness_result_id"),
        ),
        _version(item["version"], "version"),
        _trace_ref(item["robustness_plan_ref"], "robustness_plan_ref"),
        _trace_ref(item["scientific_validation_result_ref"], "scientific_validation_result_ref"),
        _trace_ref(item["validation_run_ref"], "validation_run_ref"),
        _trace_ref(item["backtest_result_ref"], "backtest_result_ref"),
        _trace_ref(item["backtest_run_ref"], "backtest_run_ref"),
        _trace_ref(item["strategy_ref"], "strategy_ref"),
        _trace_ref(item["experiment_ref"], "experiment_ref"),
        _trace_ref(item["normalized_manifest_ref"], "normalized_manifest_ref"),
        _trace_ref(item["normalized_lock_ref"], "normalized_lock_ref"),
        _decode_walk_forward(item["walk_forward"]),
        _decode_monte_carlo(item["monte_carlo"]),
        _decode_cost_perturbation(item["cost_perturbation"]),
        RobustnessHoldoutEvidence(_text(item["holdout_evidence"], "holdout_evidence")),
        RobustnessDecision(_text(item["decision"], "decision")),
        tuple(
            RobustnessReasonCode(value) for value in _strings(item["reason_codes"], "reason_codes")
        ),
        _trace_ref(item["robustness_authority_ref"], "robustness_authority_ref"),
        _trace_ref(item["provenance_ref"], "provenance_ref"),
        DeploymentAuthorizationStatus(
            _text(item["deployment_authorization"], "deployment_authorization")
        ),
        ExecutionState(_text(item["execution_state"], "execution_state")),
        _version(item["contract_version"], "contract_version"),
    )


def _decode_robustness_run(payload: Any) -> RobustnessValidationRunRecord:
    fields = {
        "robustness_run_id",
        "version",
        "robustness_plan_ref",
        "scientific_validation_result_ref",
        "validation_run_ref",
        "backtest_result_ref",
        "backtest_run_ref",
        "robustness_input_fingerprint",
        "monte_carlo_seed",
        "robustness_result_ref",
        "robustness_authority_ref",
        "provenance_ref",
        "status",
        "deployment_authorization",
        "execution_state",
        "contract_version",
    }
    item = _strict_object(payload, fields, "RobustnessValidationRunRecord.payload")
    return RobustnessValidationRunRecord(
        cast(RunId, _typed_id(item["robustness_run_id"], RunId, "robustness_run_id")),
        _version(item["version"], "version"),
        _trace_ref(item["robustness_plan_ref"], "robustness_plan_ref"),
        _trace_ref(item["scientific_validation_result_ref"], "scientific_validation_result_ref"),
        _trace_ref(item["validation_run_ref"], "validation_run_ref"),
        _trace_ref(item["backtest_result_ref"], "backtest_result_ref"),
        _trace_ref(item["backtest_run_ref"], "backtest_run_ref"),
        _text(item["robustness_input_fingerprint"], "robustness_input_fingerprint"),
        _integer(item["monte_carlo_seed"], "monte_carlo_seed"),
        _trace_ref(item["robustness_result_ref"], "robustness_result_ref"),
        _trace_ref(item["robustness_authority_ref"], "robustness_authority_ref"),
        _trace_ref(item["provenance_ref"], "provenance_ref"),
        RobustnessRunStatus(_text(item["status"], "status")),
        DeploymentAuthorizationStatus(
            _text(item["deployment_authorization"], "deployment_authorization")
        ),
        ExecutionState(_text(item["execution_state"], "execution_state")),
        _version(item["contract_version"], "contract_version"),
    )


def _decode_optimization_parameter(payload: Any) -> OptimizationParameter:
    item = _strict_object(
        payload,
        {"name", "parameter_type", "lower_bound", "upper_bound", "step", "default_value"},
        "OptimizationParameter",
    )
    return OptimizationParameter(
        OptimizationParameterName(_text(item["name"], "name")),
        OptimizationParameterType(_text(item["parameter_type"], "parameter_type")),
        _integer(item["lower_bound"], "lower_bound"),
        _integer(item["upper_bound"], "upper_bound"),
        _integer(item["step"], "step"),
        _integer(item["default_value"], "default_value"),
    )


def _decode_search_space(payload: Any) -> OptimizationSearchSpace:
    item = _strict_object(
        payload,
        {"search_space_id", "version", "parameters", "contract_version"},
        "OptimizationSearchSpace.payload",
    )
    values = item["parameters"]
    if not isinstance(values, list):
        raise InvalidSerialization("parameters must be an array")
    return OptimizationSearchSpace(
        cast(ArtifactId, _typed_id(item["search_space_id"], ArtifactId, "search_space_id")),
        _version(item["version"], "version"),
        tuple(_decode_optimization_parameter(value) for value in values),
        _version(item["contract_version"], "contract_version"),
    )


def _decode_optimization_plan(payload: Any) -> OptimizationPlan:
    fields = {
        "optimization_plan_id",
        "version",
        "search_space_ref",
        "parent_strategy_ref",
        "source_experiment_ref",
        "source_robustness_result_ref",
        "normalized_manifest_ref",
        "normalized_lock_ref",
        "engine_contract_ref",
        "validation_plan_ref",
        "robustness_plan_ref",
        "search_method",
        "maximum_trials",
        "objective",
        "minimum_trade_count",
        "maximum_drawdown",
        "multiplicity_policy",
        "declared_alpha",
        "selection_authority_ref",
        "provenance_ref",
        "contract_version",
    }
    item = _strict_object(payload, fields, "OptimizationPlan.payload")
    return OptimizationPlan(
        cast(
            ArtifactId, _typed_id(item["optimization_plan_id"], ArtifactId, "optimization_plan_id")
        ),
        _version(item["version"], "version"),
        _trace_ref(item["search_space_ref"], "search_space_ref"),
        _trace_ref(item["parent_strategy_ref"], "parent_strategy_ref"),
        _trace_ref(item["source_experiment_ref"], "source_experiment_ref"),
        _trace_ref(item["source_robustness_result_ref"], "source_robustness_result_ref"),
        _trace_ref(item["normalized_manifest_ref"], "normalized_manifest_ref"),
        _trace_ref(item["normalized_lock_ref"], "normalized_lock_ref"),
        _trace_ref(item["engine_contract_ref"], "engine_contract_ref"),
        _trace_ref(item["validation_plan_ref"], "validation_plan_ref"),
        _trace_ref(item["robustness_plan_ref"], "robustness_plan_ref"),
        OptimizationSearchMethod(_text(item["search_method"], "search_method")),
        _integer(item["maximum_trials"], "maximum_trials"),
        OptimizationObjective(_text(item["objective"], "objective")),
        _integer(item["minimum_trade_count"], "minimum_trade_count"),
        _text(item["maximum_drawdown"], "maximum_drawdown"),
        OptimizationMultiplicityPolicy(_text(item["multiplicity_policy"], "multiplicity_policy")),
        _text(item["declared_alpha"], "declared_alpha"),
        _trace_ref(item["selection_authority_ref"], "selection_authority_ref"),
        _trace_ref(item["provenance_ref"], "provenance_ref"),
        _version(item["contract_version"], "contract_version"),
    )


def _decode_parameter_values(value: Any) -> tuple[tuple[str, int], ...]:
    if not isinstance(value, list):
        raise InvalidSerialization("parameter_values must be an array")
    result: list[tuple[str, int]] = []
    for entry in value:
        if not isinstance(entry, list) or len(entry) != 2:
            raise InvalidSerialization("parameter_values entries must be pairs")
        result.append((_text(entry[0], "parameter name"), _integer(entry[1], "parameter value")))
    return tuple(result)


def _decode_candidate_definition(payload: Any) -> OptimizationCandidateDefinition:
    item = _strict_object(
        payload,
        {
            "candidate_id",
            "version",
            "optimization_plan_ref",
            "parent_strategy_ref",
            "parameter_values",
            "candidate_strategy_ref",
            "contract_version",
        },
        "OptimizationCandidateDefinition.payload",
    )
    return OptimizationCandidateDefinition(
        cast(ArtifactId, _typed_id(item["candidate_id"], ArtifactId, "candidate_id")),
        _version(item["version"], "version"),
        _trace_ref(item["optimization_plan_ref"], "optimization_plan_ref"),
        _trace_ref(item["parent_strategy_ref"], "parent_strategy_ref"),
        _decode_parameter_values(item["parameter_values"]),
        _trace_ref(item["candidate_strategy_ref"], "candidate_strategy_ref"),
        _version(item["contract_version"], "contract_version"),
    )


def _decode_candidate_result(payload: Any) -> OptimizationCandidateResult:
    fields = {
        "candidate_id",
        "version",
        "candidate_definition_ref",
        "candidate_strategy_ref",
        "backtest_result_ref",
        "scientific_validation_result_ref",
        "robustness_result_ref",
        "total_return",
        "max_drawdown",
        "trade_count",
        "eligibility",
        "reason_codes",
        "contract_version",
    }
    item = _strict_object(payload, fields, "OptimizationCandidateResult.payload")
    return OptimizationCandidateResult(
        cast(ArtifactId, _typed_id(item["candidate_id"], ArtifactId, "candidate_id")),
        _version(item["version"], "version"),
        _trace_ref(item["candidate_definition_ref"], "candidate_definition_ref"),
        _trace_ref(item["candidate_strategy_ref"], "candidate_strategy_ref"),
        _trace_ref(item["backtest_result_ref"], "backtest_result_ref"),
        _trace_ref(item["scientific_validation_result_ref"], "scientific_validation_result_ref"),
        _trace_ref(item["robustness_result_ref"], "robustness_result_ref"),
        _text(item["total_return"], "total_return"),
        _text(item["max_drawdown"], "max_drawdown"),
        _integer(item["trade_count"], "trade_count"),
        CandidateEligibility(_text(item["eligibility"], "eligibility")),
        tuple(
            OptimizationReasonCode(value)
            for value in _strings(item["reason_codes"], "reason_codes")
        ),
        _version(item["contract_version"], "contract_version"),
    )


def _decode_optimization_trial(payload: Any) -> OptimizationTrialRecord:
    item = _strict_object(
        payload,
        {
            "trial_id",
            "version",
            "optimization_plan_ref",
            "trial_index",
            "candidate_definition_ref",
            "candidate_result_ref",
            "status",
            "reason_codes",
            "contract_version",
        },
        "OptimizationTrialRecord.payload",
    )
    return OptimizationTrialRecord(
        cast(TrialId, _typed_id(item["trial_id"], TrialId, "trial_id")),
        _version(item["version"], "version"),
        _trace_ref(item["optimization_plan_ref"], "optimization_plan_ref"),
        _integer(item["trial_index"], "trial_index"),
        _trace_ref(item["candidate_definition_ref"], "candidate_definition_ref"),
        _trace_ref(item["candidate_result_ref"], "candidate_result_ref"),
        OptimizationTrialStatus(_text(item["status"], "status")),
        tuple(
            OptimizationReasonCode(value)
            for value in _strings(item["reason_codes"], "reason_codes")
        ),
        _version(item["contract_version"], "contract_version"),
    )


def _decode_selection_result(payload: Any) -> OptimizationSelectionResult:
    fields = {
        "selection_result_id",
        "version",
        "optimization_plan_ref",
        "candidate_result_refs",
        "trial_refs",
        "attempted_trials",
        "completed_trials",
        "eligible_candidates",
        "selected_candidate_ref",
        "decision",
        "multiplicity_policy",
        "corrected_alpha",
        "tie_break_order",
        "reason_codes",
        "selection_authority_ref",
        "provenance_ref",
        "deployment_authorization",
        "execution_state",
        "contract_version",
    }
    item = _strict_object(payload, fields, "OptimizationSelectionResult.payload")
    return OptimizationSelectionResult(
        cast(ArtifactId, _typed_id(item["selection_result_id"], ArtifactId, "selection_result_id")),
        _version(item["version"], "version"),
        _trace_ref(item["optimization_plan_ref"], "optimization_plan_ref"),
        _trace_refs(item["candidate_result_refs"], "candidate_result_refs"),
        _trace_refs(item["trial_refs"], "trial_refs"),
        _integer(item["attempted_trials"], "attempted_trials"),
        _integer(item["completed_trials"], "completed_trials"),
        _integer(item["eligible_candidates"], "eligible_candidates"),
        _optional_trace_ref(item["selected_candidate_ref"], "selected_candidate_ref"),
        SelectionDecision(_text(item["decision"], "decision")),
        OptimizationMultiplicityPolicy(_text(item["multiplicity_policy"], "multiplicity_policy")),
        _optional_text(item["corrected_alpha"], "corrected_alpha"),
        _strings(item["tie_break_order"], "tie_break_order"),
        tuple(
            OptimizationReasonCode(value)
            for value in _strings(item["reason_codes"], "reason_codes")
        ),
        _trace_ref(item["selection_authority_ref"], "selection_authority_ref"),
        _trace_ref(item["provenance_ref"], "provenance_ref"),
        DeploymentAuthorizationStatus(
            _text(item["deployment_authorization"], "deployment_authorization")
        ),
        ExecutionState(_text(item["execution_state"], "execution_state")),
        _version(item["contract_version"], "contract_version"),
    )


def _decode_optimization_run(payload: Any) -> OptimizationRunRecord:
    fields = {
        "optimization_run_id",
        "version",
        "optimization_plan_ref",
        "optimization_input_fingerprint",
        "declared_trials",
        "attempted_trials",
        "completed_trials",
        "selection_result_ref",
        "selection_authority_ref",
        "provenance_ref",
        "status",
        "deployment_authorization",
        "execution_state",
        "contract_version",
    }
    item = _strict_object(payload, fields, "OptimizationRunRecord.payload")
    return OptimizationRunRecord(
        cast(RunId, _typed_id(item["optimization_run_id"], RunId, "optimization_run_id")),
        _version(item["version"], "version"),
        _trace_ref(item["optimization_plan_ref"], "optimization_plan_ref"),
        _text(item["optimization_input_fingerprint"], "optimization_input_fingerprint"),
        _integer(item["declared_trials"], "declared_trials"),
        _integer(item["attempted_trials"], "attempted_trials"),
        _integer(item["completed_trials"], "completed_trials"),
        _trace_ref(item["selection_result_ref"], "selection_result_ref"),
        _trace_ref(item["selection_authority_ref"], "selection_authority_ref"),
        _trace_ref(item["provenance_ref"], "provenance_ref"),
        OptimizationRunStatus(_text(item["status"], "status")),
        DeploymentAuthorizationStatus(
            _text(item["deployment_authorization"], "deployment_authorization")
        ),
        ExecutionState(_text(item["execution_state"], "execution_state")),
        _version(item["contract_version"], "contract_version"),
    )


def _decode_pine_source_artifact(payload: Any) -> PineStrategySourceArtifact:
    fields = {
        "pine_artifact_id",
        "version",
        "pine_language_version",
        "source_text",
        "normalized_source_text",
        "source_sha256",
        "normalized_source_sha256",
        "source_byte_size",
        "script_kind",
        "declared_script_title",
        "pyramiding",
        "process_orders_on_close",
        "calc_on_every_tick",
        "default_qty_type",
        "default_qty_value",
        "strategy_definition_ref",
        "optimization_candidate_definition_ref",
        "optimization_candidate_result_ref",
        "optimization_selection_ref",
        "source_backtest_result_ref",
        "source_scientific_validation_ref",
        "source_robustness_result_ref",
        "provenance_ref",
        "authority_ref",
        "semantic_parity",
        "repaint_assessment",
        "deployment_authorization",
        "execution_state",
        "contract_version",
    }
    item = _strict_object(payload, fields, "PineStrategySourceArtifact.payload")
    return PineStrategySourceArtifact(
        cast(ArtifactId, _typed_id(item["pine_artifact_id"], ArtifactId, "pine_artifact_id")),
        _version(item["version"], "version"),
        PineLanguageVersion(_text(item["pine_language_version"], "pine_language_version")),
        _text(item["source_text"], "source_text"),
        _text(item["normalized_source_text"], "normalized_source_text"),
        _text(item["source_sha256"], "source_sha256"),
        _text(item["normalized_source_sha256"], "normalized_source_sha256"),
        _integer(item["source_byte_size"], "source_byte_size"),
        PineScriptKind(_text(item["script_kind"], "script_kind")),
        _text(item["declared_script_title"], "declared_script_title"),
        _integer(item["pyramiding"], "pyramiding"),
        _boolean(item["process_orders_on_close"], "process_orders_on_close"),
        _boolean(item["calc_on_every_tick"], "calc_on_every_tick"),
        PineDefaultQuantityType(_text(item["default_qty_type"], "default_qty_type")),
        _text(item["default_qty_value"], "default_qty_value"),
        _trace_ref(item["strategy_definition_ref"], "strategy_definition_ref"),
        _optional_trace_ref(
            item["optimization_candidate_definition_ref"],
            "optimization_candidate_definition_ref",
        ),
        _optional_trace_ref(
            item["optimization_candidate_result_ref"],
            "optimization_candidate_result_ref",
        ),
        _optional_trace_ref(item["optimization_selection_ref"], "optimization_selection_ref"),
        _trace_ref(item["source_backtest_result_ref"], "source_backtest_result_ref"),
        _trace_ref(item["source_scientific_validation_ref"], "source_scientific_validation_ref"),
        _trace_ref(item["source_robustness_result_ref"], "source_robustness_result_ref"),
        _trace_ref(item["provenance_ref"], "provenance_ref"),
        _trace_ref(item["authority_ref"], "authority_ref"),
        PineSemanticParityStatus(_text(item["semantic_parity"], "semantic_parity")),
        RepaintAssessmentStatus(_text(item["repaint_assessment"], "repaint_assessment")),
        DeploymentAuthorizationStatus(
            _text(item["deployment_authorization"], "deployment_authorization")
        ),
        ExecutionState(_text(item["execution_state"], "execution_state")),
        _version(item["contract_version"], "contract_version"),
    )


def _decode_pine_intake_record(payload: Any) -> PineStrategyIntakeRecord:
    fields = {
        "intake_run_id",
        "version",
        "requested_artifact_id",
        "source_artifact_ref",
        "source_sha256",
        "normalized_source_sha256",
        "source_byte_size",
        "input_fingerprint",
        "status",
        "reason_codes",
        "authority_ref",
        "provenance_ref",
        "deployment_authorization",
        "execution_state",
        "contract_version",
    }
    item = _strict_object(payload, fields, "PineStrategyIntakeRecord.payload")
    return PineStrategyIntakeRecord(
        cast(RunId, _typed_id(item["intake_run_id"], RunId, "intake_run_id")),
        _version(item["version"], "version"),
        cast(
            ArtifactId,
            _typed_id(item["requested_artifact_id"], ArtifactId, "requested_artifact_id"),
        ),
        (
            None
            if item["source_artifact_ref"] is None
            else _trace_ref(item["source_artifact_ref"], "source_artifact_ref")
        ),
        _text(item["source_sha256"], "source_sha256"),
        (
            None
            if item["normalized_source_sha256"] is None
            else _text(item["normalized_source_sha256"], "normalized_source_sha256")
        ),
        _integer(item["source_byte_size"], "source_byte_size"),
        _text(item["input_fingerprint"], "input_fingerprint"),
        PineIntakeStatus(_text(item["status"], "status")),
        tuple(
            PineIntakeReasonCode(value) for value in _strings(item["reason_codes"], "reason_codes")
        ),
        _trace_ref(item["authority_ref"], "authority_ref"),
        _trace_ref(item["provenance_ref"], "provenance_ref"),
        DeploymentAuthorizationStatus(
            _text(item["deployment_authorization"], "deployment_authorization")
        ),
        ExecutionState(_text(item["execution_state"], "execution_state")),
        _version(item["contract_version"], "contract_version"),
    )


def _decode_parity_tolerance_policy(payload: Any) -> ParityTolerancePolicy:
    fields = {
        "policy_id",
        "version",
        "timestamp_exact",
        "absolute_price_tolerance",
        "relative_price_tolerance",
        "quantity_tolerance",
        "commission_tolerance",
        "pnl_tolerance",
        "authority_ref",
        "provenance_ref",
        "contract_version",
    }
    item = _strict_object(payload, fields, "ParityTolerancePolicy.payload")
    return ParityTolerancePolicy(
        cast(ArtifactId, _typed_id(item["policy_id"], ArtifactId, "policy_id")),
        _version(item["version"], "version"),
        _boolean(item["timestamp_exact"], "timestamp_exact"),
        _text(item["absolute_price_tolerance"], "absolute_price_tolerance"),
        _text(item["relative_price_tolerance"], "relative_price_tolerance"),
        _text(item["quantity_tolerance"], "quantity_tolerance"),
        _text(item["commission_tolerance"], "commission_tolerance"),
        _text(item["pnl_tolerance"], "pnl_tolerance"),
        _trace_ref(item["authority_ref"], "authority_ref"),
        _trace_ref(item["provenance_ref"], "provenance_ref"),
        _version(item["contract_version"], "contract_version"),
    )


def _decode_pine_event(payload: Any) -> PineExecutionEvent:
    fields = {
        "event_index",
        "signal_time",
        "execution_time",
        "action",
        "side",
        "execution_price",
        "position_after",
        "quantity",
        "commission",
        "trade_id",
        "source_row",
    }
    item = _strict_object(payload, fields, "PineExecutionEvent")
    return PineExecutionEvent(
        _integer(item["event_index"], "event_index"),
        _timestamp(item["signal_time"], "signal_time"),
        _timestamp(item["execution_time"], "execution_time"),
        PineExecutionAction(_text(item["action"], "action")),
        PineExecutionSide(_text(item["side"], "side")),
        _text(item["execution_price"], "execution_price"),
        SimulatedPositionState(_text(item["position_after"], "position_after")),
        _text(item["quantity"], "quantity"),
        _text(item["commission"], "commission"),
        _text(item["trade_id"], "trade_id"),
        _integer(item["source_row"], "source_row"),
    )


def _decode_pine_execution_evidence(payload: Any) -> PineExecutionEvidence:
    fields = {
        "evidence_id",
        "version",
        "pine_artifact_ref",
        "strategy_ref",
        "instrument_ref",
        "normalized_manifest_ref",
        "normalized_lock_ref",
        "observation_start",
        "observation_end",
        "source_format",
        "source_text",
        "source_sha256",
        "source_byte_size",
        "events",
        "provenance_ref",
        "authority_ref",
        "contract_version",
    }
    item = _strict_object(payload, fields, "PineExecutionEvidence.payload")
    if not isinstance(item["events"], list):
        raise InvalidSerialization("events must be an array")
    return PineExecutionEvidence(
        cast(ArtifactId, _typed_id(item["evidence_id"], ArtifactId, "evidence_id")),
        _version(item["version"], "version"),
        _trace_ref(item["pine_artifact_ref"], "pine_artifact_ref"),
        _trace_ref(item["strategy_ref"], "strategy_ref"),
        _trace_ref(item["instrument_ref"], "instrument_ref"),
        _trace_ref(item["normalized_manifest_ref"], "normalized_manifest_ref"),
        _trace_ref(item["normalized_lock_ref"], "normalized_lock_ref"),
        _timestamp(item["observation_start"], "observation_start"),
        _timestamp(item["observation_end"], "observation_end"),
        PineEvidenceSourceFormat(_text(item["source_format"], "source_format")),
        _text(item["source_text"], "source_text"),
        _text(item["source_sha256"], "source_sha256"),
        _integer(item["source_byte_size"], "source_byte_size"),
        tuple(_decode_pine_event(value) for value in item["events"]),
        _trace_ref(item["provenance_ref"], "provenance_ref"),
        _trace_ref(item["authority_ref"], "authority_ref"),
        _version(item["contract_version"], "contract_version"),
    )


def _decode_parity_mismatch(payload: Any) -> ParityMismatch:
    fields = {
        "mismatch_index",
        "mismatch_type",
        "expected_value",
        "observed_value",
        "expected_event_index",
        "observed_event_index",
        "explanation_code",
    }
    item = _strict_object(payload, fields, "ParityMismatch")
    return ParityMismatch(
        _integer(item["mismatch_index"], "mismatch_index"),
        ParityMismatchType(_text(item["mismatch_type"], "mismatch_type")),
        _text(item["expected_value"], "expected_value"),
        _text(item["observed_value"], "observed_value"),
        None
        if item["expected_event_index"] is None
        else _integer(item["expected_event_index"], "expected_event_index"),
        None
        if item["observed_event_index"] is None
        else _integer(item["observed_event_index"], "observed_event_index"),
        _text(item["explanation_code"], "explanation_code"),
    )


def _decode_pine_python_parity_result(payload: Any) -> PinePythonParityResult:
    fields = {
        "parity_result_id",
        "version",
        "pine_artifact_ref",
        "pine_execution_evidence_ref",
        "python_backtest_ref",
        "strategy_ref",
        "instrument_ref",
        "normalized_manifest_ref",
        "normalized_lock_ref",
        "tolerance_policy_ref",
        "expected_event_count",
        "observed_event_count",
        "mismatch_count",
        "mismatches",
        "decision",
        "reason_codes",
        "input_fingerprint",
        "semantic_parity",
        "repaint_assessment",
        "authority_ref",
        "provenance_ref",
        "deployment_authorization",
        "execution_state",
        "contract_version",
    }
    item = _strict_object(payload, fields, "PinePythonParityResult.payload")
    if not isinstance(item["mismatches"], list):
        raise InvalidSerialization("mismatches must be an array")
    return PinePythonParityResult(
        cast(ArtifactId, _typed_id(item["parity_result_id"], ArtifactId, "parity_result_id")),
        _version(item["version"], "version"),
        _trace_ref(item["pine_artifact_ref"], "pine_artifact_ref"),
        _trace_ref(item["pine_execution_evidence_ref"], "pine_execution_evidence_ref"),
        _trace_ref(item["python_backtest_ref"], "python_backtest_ref"),
        _trace_ref(item["strategy_ref"], "strategy_ref"),
        _trace_ref(item["instrument_ref"], "instrument_ref"),
        _trace_ref(item["normalized_manifest_ref"], "normalized_manifest_ref"),
        _trace_ref(item["normalized_lock_ref"], "normalized_lock_ref"),
        _trace_ref(item["tolerance_policy_ref"], "tolerance_policy_ref"),
        _integer(item["expected_event_count"], "expected_event_count"),
        _integer(item["observed_event_count"], "observed_event_count"),
        _integer(item["mismatch_count"], "mismatch_count"),
        tuple(_decode_parity_mismatch(value) for value in item["mismatches"]),
        PinePythonParityDecision(_text(item["decision"], "decision")),
        tuple(
            PineParityReasonCode(value) for value in _strings(item["reason_codes"], "reason_codes")
        ),
        _text(item["input_fingerprint"], "input_fingerprint"),
        PineParitySemanticStatus(_text(item["semantic_parity"], "semantic_parity")),
        RepaintAssessmentStatus(_text(item["repaint_assessment"], "repaint_assessment")),
        _trace_ref(item["authority_ref"], "authority_ref"),
        _trace_ref(item["provenance_ref"], "provenance_ref"),
        DeploymentAuthorizationStatus(
            _text(item["deployment_authorization"], "deployment_authorization")
        ),
        ExecutionState(_text(item["execution_state"], "execution_state")),
        _version(item["contract_version"], "contract_version"),
    )


def _decode_pine_python_parity_run(payload: Any) -> PinePythonParityRunRecord:
    fields = {
        "parity_run_id",
        "version",
        "request_fingerprint",
        "result_ref",
        "input_fingerprint",
        "expected_event_count",
        "observed_event_count",
        "mismatch_count",
        "decision",
        "authority_ref",
        "provenance_ref",
        "deployment_authorization",
        "execution_state",
        "contract_version",
    }
    item = _strict_object(payload, fields, "PinePythonParityRunRecord.payload")
    return PinePythonParityRunRecord(
        cast(RunId, _typed_id(item["parity_run_id"], RunId, "parity_run_id")),
        _version(item["version"], "version"),
        _text(item["request_fingerprint"], "request_fingerprint"),
        _trace_ref(item["result_ref"], "result_ref"),
        _text(item["input_fingerprint"], "input_fingerprint"),
        _integer(item["expected_event_count"], "expected_event_count"),
        _integer(item["observed_event_count"], "observed_event_count"),
        _integer(item["mismatch_count"], "mismatch_count"),
        PinePythonParityDecision(_text(item["decision"], "decision")),
        _trace_ref(item["authority_ref"], "authority_ref"),
        _trace_ref(item["provenance_ref"], "provenance_ref"),
        DeploymentAuthorizationStatus(
            _text(item["deployment_authorization"], "deployment_authorization")
        ),
        ExecutionState(_text(item["execution_state"], "execution_state")),
        _version(item["contract_version"], "contract_version"),
    )


def _decode_ai_strategy_proposal(payload: Any) -> AIStrategyProposal:
    fields = {
        "proposal_id",
        "version",
        "proposing_agent_ref",
        "strategy_family",
        "declared_hypothesis",
        "parameter_declarations",
        "strategy_definition_ref",
        "status",
        "proposal_authority_state",
        "provenance_ref",
        "contract_version",
    }
    item = _strict_object(payload, fields, "AIStrategyProposal.payload")
    params = item["parameter_declarations"]
    if not isinstance(params, list):
        raise InvalidSerialization("parameter_declarations must be an array")
    parsed: list[tuple[str, str]] = []
    for value in params:
        if not isinstance(value, list) or len(value) != 2:
            raise InvalidSerialization("parameter declaration must be a pair")
        parsed.append((_text(value[0], "parameter.name"), _text(value[1], "parameter.value")))
    return AIStrategyProposal(
        cast(ArtifactId, _typed_id(item["proposal_id"], ArtifactId, "proposal_id")),
        _version(item["version"], "version"),
        _trace_ref(item["proposing_agent_ref"], "proposing_agent_ref"),
        _text(item["strategy_family"], "strategy_family"),
        _text(item["declared_hypothesis"], "declared_hypothesis"),
        tuple(parsed),
        _trace_ref(item["strategy_definition_ref"], "strategy_definition_ref"),
        AIStrategyProposalStatus(_text(item["status"], "status")),
        ProposalAuthorityState(_text(item["proposal_authority_state"], "proposal_authority_state")),
        _trace_ref(item["provenance_ref"], "provenance_ref"),
        _version(item["contract_version"], "contract_version"),
    )


def _decode_integrated_workflow_plan(payload: Any) -> IntegratedResearchWorkflowPlan:
    fields = {
        "workflow_plan_id",
        "version",
        "mode",
        "proposal_ref",
        "proposal_strategy_ref",
        "final_strategy_ref",
        "normalized_manifest_ref",
        "normalized_lock_ref",
        "instrument_ref",
        "experiment_authorization_ref",
        "validation_plan_ref",
        "robustness_plan_ref",
        "optimization_selection_ref",
        "pine_intake_authority_ref",
        "parity_authority_ref",
        "workflow_authority_ref",
        "provenance_ref",
        "contract_version",
    }
    item = _strict_object(payload, fields, "IntegratedResearchWorkflowPlan.payload")
    return IntegratedResearchWorkflowPlan(
        cast(ArtifactId, _typed_id(item["workflow_plan_id"], ArtifactId, "workflow_plan_id")),
        _version(item["version"], "version"),
        IntegratedResearchWorkflowMode(_text(item["mode"], "mode")),
        _trace_ref(item["proposal_ref"], "proposal_ref"),
        _trace_ref(item["proposal_strategy_ref"], "proposal_strategy_ref"),
        _trace_ref(item["final_strategy_ref"], "final_strategy_ref"),
        _trace_ref(item["normalized_manifest_ref"], "normalized_manifest_ref"),
        _trace_ref(item["normalized_lock_ref"], "normalized_lock_ref"),
        _trace_ref(item["instrument_ref"], "instrument_ref"),
        _trace_ref(item["experiment_authorization_ref"], "experiment_authorization_ref"),
        _trace_ref(item["validation_plan_ref"], "validation_plan_ref"),
        _trace_ref(item["robustness_plan_ref"], "robustness_plan_ref"),
        _optional_trace_ref(item["optimization_selection_ref"], "optimization_selection_ref"),
        _trace_ref(item["pine_intake_authority_ref"], "pine_intake_authority_ref"),
        _trace_ref(item["parity_authority_ref"], "parity_authority_ref"),
        _trace_ref(item["workflow_authority_ref"], "workflow_authority_ref"),
        _trace_ref(item["provenance_ref"], "provenance_ref"),
        _version(item["contract_version"], "contract_version"),
    )


def _decode_workflow_stage(value: Any) -> WorkflowStageResult:
    fields = {
        "stage",
        "state",
        "evidence_ref",
        "outcome",
        "reason_code",
        "stage_fingerprint",
    }
    item = _strict_object(value, fields, "WorkflowStageResult")
    reason = item["reason_code"]
    return WorkflowStageResult(
        WorkflowStage(_text(item["stage"], "stage")),
        IntegratedResearchWorkflowState(_text(item["state"], "state")),
        _trace_ref(item["evidence_ref"], "evidence_ref"),
        WorkflowStageOutcome(_text(item["outcome"], "outcome")),
        None if reason is None else WorkflowReasonCode(_text(reason, "reason_code")),
        _text(item["stage_fingerprint"], "stage_fingerprint"),
    )


def _decode_research_handoff(payload: Any) -> ResearchHandoffPackage:
    fields = {
        "handoff_id",
        "version",
        "workflow_run_id",
        "workflow_input_fingerprint",
        "proposal_ref",
        "final_strategy_ref",
        "selected_candidate_ref",
        "backtest_ref",
        "scientific_validation_ref",
        "robustness_ref",
        "optimization_selection_ref",
        "pine_artifact_ref",
        "pine_intake_ref",
        "parity_result_ref",
        "parity_decision",
        "proposing_agent_ref",
        "pine_generating_agent_ref",
        "readiness",
        "provenance_ref",
        "deployment_authorization",
        "execution_state",
        "contract_version",
    }
    item = _strict_object(payload, fields, "ResearchHandoffPackage.payload")
    return ResearchHandoffPackage(
        cast(ArtifactId, _typed_id(item["handoff_id"], ArtifactId, "handoff_id")),
        _version(item["version"], "version"),
        cast(RunId, _typed_id(item["workflow_run_id"], RunId, "workflow_run_id")),
        _text(item["workflow_input_fingerprint"], "workflow_input_fingerprint"),
        _trace_ref(item["proposal_ref"], "proposal_ref"),
        _trace_ref(item["final_strategy_ref"], "final_strategy_ref"),
        _optional_trace_ref(item["selected_candidate_ref"], "selected_candidate_ref"),
        _trace_ref(item["backtest_ref"], "backtest_ref"),
        _trace_ref(item["scientific_validation_ref"], "scientific_validation_ref"),
        _trace_ref(item["robustness_ref"], "robustness_ref"),
        _optional_trace_ref(item["optimization_selection_ref"], "optimization_selection_ref"),
        _trace_ref(item["pine_artifact_ref"], "pine_artifact_ref"),
        _trace_ref(item["pine_intake_ref"], "pine_intake_ref"),
        _trace_ref(item["parity_result_ref"], "parity_result_ref"),
        PinePythonParityDecision(_text(item["parity_decision"], "parity_decision")),
        _trace_ref(item["proposing_agent_ref"], "proposing_agent_ref"),
        _trace_ref(item["pine_generating_agent_ref"], "pine_generating_agent_ref"),
        ResearchHandoffReadiness(_text(item["readiness"], "readiness")),
        _trace_ref(item["provenance_ref"], "provenance_ref"),
        DeploymentAuthorizationStatus(
            _text(item["deployment_authorization"], "deployment_authorization")
        ),
        ExecutionState(_text(item["execution_state"], "execution_state")),
        _version(item["contract_version"], "contract_version"),
    )


def _decode_tradingview_handoff(payload: Any) -> TradingViewResearchHandoffManifest:
    fields = {
        "manifest_id",
        "version",
        "pine_artifact_ref",
        "pine_source_sha256",
        "parity_result_ref",
        "strategy_ref",
        "instrument_ref",
        "normalized_manifest_ref",
        "normalized_lock_ref",
        "repaint_assessment",
        "readiness",
        "deployment_authorization",
        "execution_state",
        "contract_version",
    }
    item = _strict_object(payload, fields, "TradingViewResearchHandoffManifest.payload")
    return TradingViewResearchHandoffManifest(
        cast(ArtifactId, _typed_id(item["manifest_id"], ArtifactId, "manifest_id")),
        _version(item["version"], "version"),
        _trace_ref(item["pine_artifact_ref"], "pine_artifact_ref"),
        _text(item["pine_source_sha256"], "pine_source_sha256"),
        _trace_ref(item["parity_result_ref"], "parity_result_ref"),
        _trace_ref(item["strategy_ref"], "strategy_ref"),
        _trace_ref(item["instrument_ref"], "instrument_ref"),
        _trace_ref(item["normalized_manifest_ref"], "normalized_manifest_ref"),
        _trace_ref(item["normalized_lock_ref"], "normalized_lock_ref"),
        RepaintAssessmentStatus(_text(item["repaint_assessment"], "repaint_assessment")),
        ResearchHandoffReadiness(_text(item["readiness"], "readiness")),
        DeploymentAuthorizationStatus(
            _text(item["deployment_authorization"], "deployment_authorization")
        ),
        ExecutionState(_text(item["execution_state"], "execution_state")),
        _version(item["contract_version"], "contract_version"),
    )


def _decode_integrated_workflow_result(payload: Any) -> IntegratedResearchWorkflowResult:
    fields = {
        "workflow_result_id",
        "version",
        "workflow_plan_ref",
        "proposal_ref",
        "final_strategy_ref",
        "stages",
        "final_state",
        "handoff_ref",
        "tradingview_manifest_ref",
        "reason_codes",
        "input_fingerprint",
        "workflow_authority_ref",
        "provenance_ref",
        "deployment_authorization",
        "execution_state",
        "contract_version",
    }
    item = _strict_object(payload, fields, "IntegratedResearchWorkflowResult.payload")
    if not isinstance(item["stages"], list):
        raise InvalidSerialization("stages must be an array")
    return IntegratedResearchWorkflowResult(
        cast(ArtifactId, _typed_id(item["workflow_result_id"], ArtifactId, "workflow_result_id")),
        _version(item["version"], "version"),
        _trace_ref(item["workflow_plan_ref"], "workflow_plan_ref"),
        _trace_ref(item["proposal_ref"], "proposal_ref"),
        _trace_ref(item["final_strategy_ref"], "final_strategy_ref"),
        tuple(_decode_workflow_stage(value) for value in item["stages"]),
        IntegratedResearchWorkflowState(_text(item["final_state"], "final_state")),
        _optional_trace_ref(item["handoff_ref"], "handoff_ref"),
        _optional_trace_ref(item["tradingview_manifest_ref"], "tradingview_manifest_ref"),
        tuple(
            WorkflowReasonCode(value) for value in _strings(item["reason_codes"], "reason_codes")
        ),
        _text(item["input_fingerprint"], "input_fingerprint"),
        _trace_ref(item["workflow_authority_ref"], "workflow_authority_ref"),
        _trace_ref(item["provenance_ref"], "provenance_ref"),
        DeploymentAuthorizationStatus(
            _text(item["deployment_authorization"], "deployment_authorization")
        ),
        ExecutionState(_text(item["execution_state"], "execution_state")),
        _version(item["contract_version"], "contract_version"),
    )


def _decode_integrated_workflow_run(payload: Any) -> IntegratedResearchWorkflowRunRecord:
    fields = {
        "workflow_run_id",
        "version",
        "workflow_plan_ref",
        "proposal_ref",
        "result_ref",
        "input_fingerprint",
        "final_state",
        "handoff_ref",
        "stage_count",
        "workflow_authority_ref",
        "provenance_ref",
        "deployment_authorization",
        "execution_state",
        "contract_version",
    }
    item = _strict_object(payload, fields, "IntegratedResearchWorkflowRunRecord.payload")
    return IntegratedResearchWorkflowRunRecord(
        cast(RunId, _typed_id(item["workflow_run_id"], RunId, "workflow_run_id")),
        _version(item["version"], "version"),
        _trace_ref(item["workflow_plan_ref"], "workflow_plan_ref"),
        _trace_ref(item["proposal_ref"], "proposal_ref"),
        _trace_ref(item["result_ref"], "result_ref"),
        _text(item["input_fingerprint"], "input_fingerprint"),
        IntegratedResearchWorkflowState(_text(item["final_state"], "final_state")),
        _optional_trace_ref(item["handoff_ref"], "handoff_ref"),
        _integer(item["stage_count"], "stage_count"),
        _trace_ref(item["workflow_authority_ref"], "workflow_authority_ref"),
        _trace_ref(item["provenance_ref"], "provenance_ref"),
        DeploymentAuthorizationStatus(
            _text(item["deployment_authorization"], "deployment_authorization")
        ),
        ExecutionState(_text(item["execution_state"], "execution_state")),
        _version(item["contract_version"], "contract_version"),
    )


_DECODERS = {
    "ArtifactEnvelope": _decode_artifact,
    "EvidenceEnvelope": _decode_evidence,
    "ProvenanceRecord": _decode_provenance,
    "AuditEvent": _decode_audit,
    "VenueIdentity": _decode_venue,
    "SourceIdentity": _decode_source,
    "InstrumentIdentity": _decode_instrument,
    "RawObservation": _decode_observation,
    "DatasetManifest": _decode_manifest,
    "DatasetLock": _decode_lock,
    "TimeframeIdentity": _decode_timeframe,
    "MarketDataSchema": _decode_bar_schema,
    "MarketBar": _decode_market_bar,
    "NormalizedBarManifest": _decode_normalized_manifest,
    "RealCsvSourceDeclaration": _decode_real_csv_source_declaration,
    "RealCsvAdmissionRecord": _decode_real_csv_admission,
    "ResearchDatasetEligibilityPolicy": _decode_research_eligibility_policy,
    "ResearchDatasetEligibilityRecord": _decode_research_eligibility_record,
    "ExperimentSpecification": _decode_experiment_specification,
    "ExperimentAuthorizationPolicy": _decode_experiment_authorization_policy,
    "ExperimentAuthorizationRecord": _decode_experiment_authorization_record,
    "ExperimentReplayContract": _decode_experiment_replay_contract,
    "ExperimentResultArtifact": _decode_experiment_result_artifact,
    "ExperimentRunRecord": _decode_experiment_run_record,
    "StrategyDefinition": _decode_strategy_definition,
    "BacktestResultArtifact": _decode_backtest_result,
    "BacktestRunRecord": _decode_backtest_run,
    "ValidationPlan": _decode_validation_plan,
    "ScientificValidationResult": _decode_scientific_validation_result,
    "ValidationRunRecord": _decode_validation_run,
    "RobustnessValidationPlan": _decode_robustness_plan,
    "RobustnessValidationResult": _decode_robustness_result,
    "RobustnessValidationRunRecord": _decode_robustness_run,
    "OptimizationSearchSpace": _decode_search_space,
    "OptimizationPlan": _decode_optimization_plan,
    "OptimizationCandidateDefinition": _decode_candidate_definition,
    "OptimizationCandidateResult": _decode_candidate_result,
    "OptimizationTrialRecord": _decode_optimization_trial,
    "OptimizationSelectionResult": _decode_selection_result,
    "OptimizationRunRecord": _decode_optimization_run,
    "PineStrategySourceArtifact": _decode_pine_source_artifact,
    "PineStrategyIntakeRecord": _decode_pine_intake_record,
    "ParityTolerancePolicy": _decode_parity_tolerance_policy,
    "PineExecutionEvidence": _decode_pine_execution_evidence,
    "PinePythonParityResult": _decode_pine_python_parity_result,
    "PinePythonParityRunRecord": _decode_pine_python_parity_run,
    "AIStrategyProposal": _decode_ai_strategy_proposal,
    "IntegratedResearchWorkflowPlan": _decode_integrated_workflow_plan,
    "IntegratedResearchWorkflowResult": _decode_integrated_workflow_result,
    "ResearchHandoffPackage": _decode_research_handoff,
    "TradingViewResearchHandoffManifest": _decode_tradingview_handoff,
    "IntegratedResearchWorkflowRunRecord": _decode_integrated_workflow_run,
}


def decode[
    T: (
        ArtifactEnvelope,
        EvidenceEnvelope,
        ProvenanceRecord,
        AuditEvent,
        VenueIdentity,
        SourceIdentity,
        InstrumentIdentity,
        RawObservation,
        DatasetManifest,
        DatasetLock,
        TimeframeIdentity,
        MarketDataSchema,
        MarketBar,
        NormalizedBarManifest,
        RealCsvSourceDeclaration,
        RealCsvAdmissionRecord,
        ResearchDatasetEligibilityPolicy,
        ResearchDatasetEligibilityRecord,
        ExperimentSpecification,
        ExperimentAuthorizationPolicy,
        ExperimentAuthorizationRecord,
        ExperimentReplayContract,
        ExperimentResultArtifact,
        ExperimentRunRecord,
        StrategyDefinition,
        BacktestResultArtifact,
        BacktestRunRecord,
        ValidationPlan,
        ScientificValidationResult,
        ValidationRunRecord,
        RobustnessValidationPlan,
        RobustnessValidationResult,
        RobustnessValidationRunRecord,
        OptimizationSearchSpace,
        OptimizationPlan,
        OptimizationCandidateDefinition,
        OptimizationCandidateResult,
        OptimizationTrialRecord,
        OptimizationSelectionResult,
        OptimizationRunRecord,
        PineStrategySourceArtifact,
        PineStrategyIntakeRecord,
        ParityTolerancePolicy,
        PineExecutionEvidence,
        PinePythonParityResult,
        PinePythonParityRunRecord,
        AIStrategyProposal,
        IntegratedResearchWorkflowPlan,
        IntegratedResearchWorkflowResult,
        ResearchHandoffPackage,
        TradingViewResearchHandoffManifest,
        IntegratedResearchWorkflowRunRecord,
    )
](data: bytes, expected_type: type[T]) -> T:
    """Strictly reconstruct an exact governed type from canonical bytes."""
    if not isinstance(data, bytes):
        raise InvalidSerialization("canonical representation must be bytes")
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise InvalidSerialization("canonical bytes must be UTF-8") from exc
    try:
        raw = json.loads(
            text,
            object_pairs_hook=_reject_duplicate_keys,
            parse_constant=lambda value: (_ for _ in ()).throw(
                InvalidSerialization(f"non-finite number: {value}")
            ),
        )
    except (json.JSONDecodeError, TypeError, ValueError) as exc:
        if isinstance(exc, InvalidSerialization):
            raise
        raise InvalidSerialization("malformed canonical JSON") from exc
    if canonical_json(raw) != text:
        raise InvalidSerialization("input is not canonical JSON")
    envelope = _strict_object(
        raw, {"$format", "$representation_version", "$type", "payload"}, "representation"
    )
    if envelope["$format"] != REPRESENTATION_FORMAT:
        raise InvalidSerialization("unknown representation format")
    if envelope["$representation_version"] != REPRESENTATION_VERSION:
        raise InvalidSerialization("unknown representation version")
    type_name = _text(envelope["$type"], "$type")
    expected_name = _SUPPORTED_TYPES.get(expected_type)
    if expected_name is None or type_name != expected_name:
        raise InvalidSerialization("governed record type mismatch")
    decoder = _DECODERS.get(type_name)
    if decoder is None:
        raise InvalidSerialization("unknown governed record type")
    try:
        record = decoder(envelope["payload"])
    except (TypeError, ValueError) as exc:
        if isinstance(exc, InvalidSerialization):
            raise
        raise InvalidSerialization(f"invalid {type_name} payload") from exc
    if type(record) is not expected_type:
        raise InvalidSerialization("decoder returned an unexpected governed type")
    return record


def encode_traceability(reference: TraceabilityRef) -> bytes:
    """Canonical representation for an exact typed reference, not a following alias."""
    envelope = {
        "$format": REPRESENTATION_FORMAT,
        "$representation_version": REPRESENTATION_VERSION,
        "$type": "TraceabilityRef",
        "payload": {
            "object_id": str(reference.object_id),
            "version": reference.version.number,
            "expected_fingerprint": reference.expected_fingerprint,
        },
    }
    return canonical_json(envelope).encode("utf-8")


def decode_traceability(data: bytes) -> TraceabilityRef:
    if not isinstance(data, bytes):
        raise InvalidSerialization("canonical representation must be bytes")
    try:
        text = data.decode("utf-8")
        raw = json.loads(text, object_pairs_hook=_reject_duplicate_keys)
    except (UnicodeDecodeError, json.JSONDecodeError, TypeError, ValueError) as exc:
        if isinstance(exc, InvalidSerialization):
            raise
        raise InvalidSerialization("malformed traceability representation") from exc
    if canonical_json(raw) != text:
        raise InvalidSerialization("input is not canonical JSON")
    envelope = _strict_object(
        raw, {"$format", "$representation_version", "$type", "payload"}, "representation"
    )
    if (
        envelope["$format"] != REPRESENTATION_FORMAT
        or envelope["$representation_version"] != REPRESENTATION_VERSION
        or envelope["$type"] != "TraceabilityRef"
    ):
        raise InvalidSerialization("unsupported traceability representation")
    payload = _strict_object(
        envelope["payload"],
        {"object_id", "version", "expected_fingerprint"},
        "TraceabilityRef.payload",
    )
    expected = payload["expected_fingerprint"]
    if expected is not None and (
        not isinstance(expected, str) or not _FINGERPRINT.fullmatch(expected)
    ):
        raise InvalidSerialization("invalid expected fingerprint")
    return TraceabilityRef(
        _id(payload["object_id"], "object_id"),
        _version(payload["version"], "version"),
        expected,
    )
