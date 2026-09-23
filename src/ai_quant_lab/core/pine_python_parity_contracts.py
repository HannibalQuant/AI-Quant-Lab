"""Immutable contracts for governed Pine ↔ Python parity validation."""

from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal, InvalidOperation
from enum import StrEnum

from ai_quant_lab.core.model import (
    ArtifactId,
    AuthorityBindingId,
    ExecutionState,
    ObjectVersion,
    ProvenanceId,
    RunId,
    TraceabilityRef,
    require_utc,
)
from ai_quant_lab.core.pine_strategy_contracts import RepaintAssessmentStatus
from ai_quant_lab.core.research_eligibility_contracts import DeploymentAuthorizationStatus
from ai_quant_lab.core.strategy_backtest_contracts import SimulatedPositionState


class PinePythonParityContractError(ValueError):
    pass


class PineEvidenceSourceFormat(StrEnum):
    CSV_V1 = "CSV_V1"


class PineExecutionAction(StrEnum):
    ENTRY = "ENTRY"
    EXIT = "EXIT"


class PineExecutionSide(StrEnum):
    LONG = "LONG"


class PinePythonParityDecision(StrEnum):
    MATCH = "MATCH"
    MISMATCH = "MISMATCH"
    INCONCLUSIVE = "INCONCLUSIVE"


class PineParitySemanticStatus(StrEnum):
    MATCHED = "MATCHED"
    MISMATCHED = "MISMATCHED"
    INCONCLUSIVE = "INCONCLUSIVE"


class ParityMismatchType(StrEnum):
    MISSING_EVENT = "MISSING_EVENT"
    EXTRA_EVENT = "EXTRA_EVENT"
    ACTION_MISMATCH = "ACTION_MISMATCH"
    SIDE_MISMATCH = "SIDE_MISMATCH"
    SIGNAL_TIME_MISMATCH = "SIGNAL_TIME_MISMATCH"
    EXECUTION_TIME_MISMATCH = "EXECUTION_TIME_MISMATCH"
    PRICE_MISMATCH = "PRICE_MISMATCH"
    QUANTITY_MISMATCH = "QUANTITY_MISMATCH"
    COMMISSION_MISMATCH = "COMMISSION_MISMATCH"
    POSITION_STATE_MISMATCH = "POSITION_STATE_MISMATCH"
    TRADE_COUNT_MISMATCH = "TRADE_COUNT_MISMATCH"
    PNL_MISMATCH = "PNL_MISMATCH"


class PineParityReasonCode(StrEnum):
    EXACT_EVENT_PARITY = "EXACT_EVENT_PARITY"
    EVENT_MISMATCH = "EVENT_MISMATCH"
    INCOMPLETE_EXTERNAL_EVIDENCE = "INCOMPLETE_EXTERNAL_EVIDENCE"


_SHA256 = re.compile(r"sha256:[0-9a-f]{64}")
_DECIMAL = re.compile(r"(?:0|[1-9][0-9]*)(?:\.[0-9]+)?")
_V1 = ObjectVersion(1)


def _exact(reference: TraceabilityRef, field: str) -> None:
    if not isinstance(reference, TraceabilityRef) or reference.expected_fingerprint is None:
        raise PinePythonParityContractError(f"{field} must be an exact fingerprint reference")


def _decimal(value: str, field: str) -> None:
    if not isinstance(value, str) or _DECIMAL.fullmatch(value) is None:
        raise PinePythonParityContractError(f"{field} must be canonical non-negative decimal text")
    try:
        parsed = Decimal(value)
    except InvalidOperation as exc:
        raise PinePythonParityContractError(f"{field} is invalid") from exc
    if not parsed.is_finite() or parsed < 0 or (parsed == 0 and value != "0"):
        raise PinePythonParityContractError(f"{field} has invalid decimal semantics")
    if "." in value and value.endswith("0"):
        raise PinePythonParityContractError(f"{field} must not contain trailing zeroes")


@dataclass(frozen=True, slots=True)
class ParityTolerancePolicy:
    policy_id: ArtifactId
    version: ObjectVersion
    timestamp_exact: bool
    absolute_price_tolerance: str
    relative_price_tolerance: str
    quantity_tolerance: str
    commission_tolerance: str
    pnl_tolerance: str
    authority_ref: TraceabilityRef
    provenance_ref: TraceabilityRef
    contract_version: ObjectVersion = _V1

    def __post_init__(self) -> None:
        if (
            not isinstance(self.policy_id, ArtifactId)
            or self.version != _V1
            or self.contract_version != _V1
            or self.timestamp_exact is not True
        ):
            raise PinePythonParityContractError("unsupported parity tolerance policy")
        for field in (
            "absolute_price_tolerance",
            "relative_price_tolerance",
            "quantity_tolerance",
            "commission_tolerance",
            "pnl_tolerance",
        ):
            _decimal(getattr(self, field), field)
        if Decimal(self.relative_price_tolerance) > Decimal("0.01"):
            raise PinePythonParityContractError("relative price tolerance exceeds bounded 1% ceiling")
        _exact(self.authority_ref, "authority_ref")
        _exact(self.provenance_ref, "provenance_ref")


@dataclass(frozen=True, slots=True)
class PineExecutionEvent:
    event_index: int
    signal_time: datetime
    execution_time: datetime
    action: PineExecutionAction
    side: PineExecutionSide
    execution_price: str
    position_after: SimulatedPositionState
    quantity: str
    commission: str
    trade_id: str
    source_row: int

    def __post_init__(self) -> None:
        if (
            isinstance(self.event_index, bool)
            or not isinstance(self.event_index, int)
            or self.event_index < 0
            or isinstance(self.source_row, bool)
            or not isinstance(self.source_row, int)
            or self.source_row < 2
            or not isinstance(self.action, PineExecutionAction)
            or self.side is not PineExecutionSide.LONG
            or not isinstance(self.trade_id, str)
        ):
            raise PinePythonParityContractError("invalid Pine execution event")
        require_utc(self.signal_time, "signal_time")
        require_utc(self.execution_time, "execution_time")
        if self.execution_time < self.signal_time:
            raise PinePythonParityContractError("execution cannot precede signal time")
        for field in ("execution_price", "quantity", "commission"):
            _decimal(getattr(self, field), field)
        if Decimal(self.execution_price) <= 0 or Decimal(self.quantity) <= 0:
            raise PinePythonParityContractError("execution price and quantity must be positive")
        expected_state = (
            SimulatedPositionState.LONG
            if self.action is PineExecutionAction.ENTRY
            else SimulatedPositionState.FLAT
        )
        if self.position_after is not expected_state:
            raise PinePythonParityContractError("event action and position state are inconsistent")


@dataclass(frozen=True, slots=True)
class PineExecutionEvidence:
    evidence_id: ArtifactId
    version: ObjectVersion
    pine_artifact_ref: TraceabilityRef
    strategy_ref: TraceabilityRef
    instrument_ref: TraceabilityRef
    normalized_manifest_ref: TraceabilityRef
    normalized_lock_ref: TraceabilityRef
    observation_start: datetime
    observation_end: datetime
    source_format: PineEvidenceSourceFormat
    source_sha256: str
    source_byte_size: int
    events: tuple[PineExecutionEvent, ...]
    provenance_ref: TraceabilityRef
    authority_ref: TraceabilityRef
    contract_version: ObjectVersion = _V1

    def __post_init__(self) -> None:
        if (
            not isinstance(self.evidence_id, ArtifactId)
            or self.version != _V1
            or self.contract_version != _V1
            or self.source_format is not PineEvidenceSourceFormat.CSV_V1
            or not isinstance(self.source_sha256, str)
            or _SHA256.fullmatch(self.source_sha256) is None
            or isinstance(self.source_byte_size, bool)
            or not isinstance(self.source_byte_size, int)
            or self.source_byte_size <= 0
        ):
            raise PinePythonParityContractError("invalid Pine execution evidence")
        for field in (
            "pine_artifact_ref",
            "strategy_ref",
            "instrument_ref",
            "normalized_manifest_ref",
            "normalized_lock_ref",
            "provenance_ref",
            "authority_ref",
        ):
            _exact(getattr(self, field), field)
        require_utc(self.observation_start, "observation_start")
        require_utc(self.observation_end, "observation_end")
        if self.observation_start >= self.observation_end:
            raise PinePythonParityContractError("invalid parity observation window")
        indexes = tuple(event.event_index for event in self.events)
        if indexes != tuple(range(len(self.events))):
            raise PinePythonParityContractError("event indexes must be contiguous from zero")
        executions = tuple(event.execution_time for event in self.events)
        if executions != tuple(sorted(executions)) or len(set(executions)) != len(executions):
            raise PinePythonParityContractError("execution events must be strictly time ordered")
        state = SimulatedPositionState.FLAT
        for event in self.events:
            if state is SimulatedPositionState.FLAT and event.action is not PineExecutionAction.ENTRY:
                raise PinePythonParityContractError("EXIT while FLAT is invalid")
            if state is SimulatedPositionState.LONG and event.action is not PineExecutionAction.EXIT:
                raise PinePythonParityContractError("ENTRY while LONG is invalid")
            state = event.position_after


@dataclass(frozen=True, slots=True)
class ParityMismatch:
    mismatch_index: int
    mismatch_type: ParityMismatchType
    expected_value: str
    observed_value: str
    expected_event_index: int | None
    observed_event_index: int | None
    explanation_code: str

    def __post_init__(self) -> None:
        if (
            isinstance(self.mismatch_index, bool)
            or not isinstance(self.mismatch_index, int)
            or self.mismatch_index < 0
            or not isinstance(self.mismatch_type, ParityMismatchType)
            or not isinstance(self.expected_value, str)
            or not isinstance(self.observed_value, str)
            or not isinstance(self.explanation_code, str)
            or not self.explanation_code
        ):
            raise PinePythonParityContractError("invalid parity mismatch")
        for value in (self.expected_event_index, self.observed_event_index):
            if value is not None and (
                isinstance(value, bool) or not isinstance(value, int) or value < 0
            ):
                raise PinePythonParityContractError("invalid mismatch event index")


@dataclass(frozen=True, slots=True)
class PinePythonParityRequest:
    parity_run_id: RunId
    result_id: ArtifactId
    pine_artifact_ref: TraceabilityRef
    pine_intake_record_ref: TraceabilityRef
    python_backtest_ref: TraceabilityRef
    pine_execution_evidence_ref: TraceabilityRef
    strategy_ref: TraceabilityRef
    instrument_ref: TraceabilityRef
    normalized_manifest_ref: TraceabilityRef
    normalized_lock_ref: TraceabilityRef
    observation_start: datetime
    observation_end: datetime
    tolerance_policy_ref: TraceabilityRef
    authority_ref: TraceabilityRef
    provenance_ref: TraceabilityRef
    contract_version: ObjectVersion = _V1

    def __post_init__(self) -> None:
        if (
            not isinstance(self.parity_run_id, RunId)
            or not isinstance(self.result_id, ArtifactId)
            or self.contract_version != _V1
        ):
            raise PinePythonParityContractError("invalid parity request identity")
        for field in (
            "pine_artifact_ref",
            "pine_intake_record_ref",
            "python_backtest_ref",
            "pine_execution_evidence_ref",
            "strategy_ref",
            "instrument_ref",
            "normalized_manifest_ref",
            "normalized_lock_ref",
            "tolerance_policy_ref",
            "authority_ref",
            "provenance_ref",
        ):
            _exact(getattr(self, field), field)
        require_utc(self.observation_start, "observation_start")
        require_utc(self.observation_end, "observation_end")
        if self.observation_start >= self.observation_end:
            raise PinePythonParityContractError("invalid parity request window")


@dataclass(frozen=True, slots=True)
class PinePythonParityResult:
    parity_result_id: ArtifactId
    version: ObjectVersion
    pine_artifact_ref: TraceabilityRef
    pine_execution_evidence_ref: TraceabilityRef
    python_backtest_ref: TraceabilityRef
    strategy_ref: TraceabilityRef
    instrument_ref: TraceabilityRef
    normalized_manifest_ref: TraceabilityRef
    normalized_lock_ref: TraceabilityRef
    tolerance_policy_ref: TraceabilityRef
    expected_event_count: int
    observed_event_count: int
    mismatch_count: int
    mismatches: tuple[ParityMismatch, ...]
    decision: PinePythonParityDecision
    reason_codes: tuple[PineParityReasonCode, ...]
    input_fingerprint: str
    semantic_parity: PineParitySemanticStatus
    repaint_assessment: RepaintAssessmentStatus
    authority_ref: TraceabilityRef
    provenance_ref: TraceabilityRef
    deployment_authorization: DeploymentAuthorizationStatus
    execution_state: ExecutionState
    contract_version: ObjectVersion = _V1

    def __post_init__(self) -> None:
        if (
            not isinstance(self.parity_result_id, ArtifactId)
            or self.version != _V1
            or self.contract_version != _V1
            or any(
                isinstance(value, bool) or not isinstance(value, int) or value < 0
                for value in (
                    self.expected_event_count,
                    self.observed_event_count,
                    self.mismatch_count,
                )
            )
            or self.mismatch_count != len(self.mismatches)
            or tuple(item.mismatch_index for item in self.mismatches)
            != tuple(range(len(self.mismatches)))
            or _SHA256.fullmatch(self.input_fingerprint) is None
        ):
            raise PinePythonParityContractError("invalid parity result")
        for field in (
            "pine_artifact_ref",
            "pine_execution_evidence_ref",
            "python_backtest_ref",
            "strategy_ref",
            "instrument_ref",
            "normalized_manifest_ref",
            "normalized_lock_ref",
            "tolerance_policy_ref",
            "authority_ref",
            "provenance_ref",
        ):
            _exact(getattr(self, field), field)
        expected_semantic = {
            PinePythonParityDecision.MATCH: PineParitySemanticStatus.MATCHED,
            PinePythonParityDecision.MISMATCH: PineParitySemanticStatus.MISMATCHED,
            PinePythonParityDecision.INCONCLUSIVE: PineParitySemanticStatus.INCONCLUSIVE,
        }[self.decision]
        expected_reason = {
            PinePythonParityDecision.MATCH: (PineParityReasonCode.EXACT_EVENT_PARITY,),
            PinePythonParityDecision.MISMATCH: (PineParityReasonCode.EVENT_MISMATCH,),
            PinePythonParityDecision.INCONCLUSIVE: (
                PineParityReasonCode.INCOMPLETE_EXTERNAL_EVIDENCE,
            ),
        }[self.decision]
        if self.semantic_parity is not expected_semantic or self.reason_codes != expected_reason:
            raise PinePythonParityContractError("parity decision semantics are inconsistent")
        if self.decision is PinePythonParityDecision.MATCH and self.mismatches:
            raise PinePythonParityContractError("MATCH cannot contain mismatches")
        if self.decision is PinePythonParityDecision.MISMATCH and not self.mismatches:
            raise PinePythonParityContractError("MISMATCH requires mismatch evidence")
        if (
            self.repaint_assessment is not RepaintAssessmentStatus.NOT_EVALUATED
            or self.deployment_authorization is not DeploymentAuthorizationStatus.NOT_AUTHORIZED
            or self.execution_state is not ExecutionState.PLANNED_CLOSED
        ):
            raise PinePythonParityContractError("parity cannot grant repaint/deployment/execution")


@dataclass(frozen=True, slots=True)
class PinePythonParityRunRecord:
    parity_run_id: RunId
    version: ObjectVersion
    request_fingerprint: str
    result_ref: TraceabilityRef
    input_fingerprint: str
    expected_event_count: int
    observed_event_count: int
    mismatch_count: int
    decision: PinePythonParityDecision
    authority_ref: TraceabilityRef
    provenance_ref: TraceabilityRef
    deployment_authorization: DeploymentAuthorizationStatus
    execution_state: ExecutionState
    contract_version: ObjectVersion = _V1

    def __post_init__(self) -> None:
        if (
            not isinstance(self.parity_run_id, RunId)
            or self.version != _V1
            or self.contract_version != _V1
            or _SHA256.fullmatch(self.request_fingerprint) is None
            or _SHA256.fullmatch(self.input_fingerprint) is None
            or any(
                isinstance(value, bool) or not isinstance(value, int) or value < 0
                for value in (
                    self.expected_event_count,
                    self.observed_event_count,
                    self.mismatch_count,
                )
            )
        ):
            raise PinePythonParityContractError("invalid parity run record")
        _exact(self.result_ref, "result_ref")
        _exact(self.authority_ref, "authority_ref")
        _exact(self.provenance_ref, "provenance_ref")
        if (
            self.deployment_authorization is not DeploymentAuthorizationStatus.NOT_AUTHORIZED
            or self.execution_state is not ExecutionState.PLANNED_CLOSED
        ):
            raise PinePythonParityContractError("parity run cannot grant downstream authority")