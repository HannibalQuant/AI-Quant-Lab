"""Local-only governed Pine ↔ Python event-level parity validation."""

from __future__ import annotations

import csv
import io
from dataclasses import dataclass
from datetime import UTC, datetime
from decimal import ROUND_HALF_EVEN, Context, Decimal, localcontext

from ai_quant_lab.core.dataset_store import LocalDatasetRepository, RepositoryWriteResult
from ai_quant_lab.core.integrity import fingerprint_record
from ai_quant_lab.core.model import (
    ArtifactId,
    ExecutionState,
    ObjectVersion,
    TraceabilityRef,
    fingerprint,
)
from ai_quant_lab.core.optimization_selection import OptimizationEvidence
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
    PinePythonParityRequest,
    PinePythonParityResult,
    PinePythonParityRunRecord,
)
from ai_quant_lab.core.pine_strategy_contracts import (
    PineIntakeStatus,
    PineSemanticParityStatus,
    PineStrategyIntakeRecord,
    PineStrategyIntakeRequest,
    PineStrategySourceArtifact,
    RepaintAssessmentStatus,
)
from ai_quant_lab.core.pine_strategy_intake import (
    PineStrategyIntakeContext,
    verify_pine_strategy_intake_lineage,
)
from ai_quant_lab.core.research_eligibility_contracts import DeploymentAuthorizationStatus
from ai_quant_lab.core.strategy_backtest import verify_strategy_backtest_lineage
from ai_quant_lab.core.strategy_backtest_contracts import (
    BacktestResultArtifact,
    SimulatedOrderSide,
    SimulatedPositionState,
)

_V1 = ObjectVersion(1)
_DECIMAL_CONTEXT = Context(prec=34, rounding=ROUND_HALF_EVEN)
_COLUMNS = (
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
)


class PinePythonParityError(ValueError):
    pass


class PineExecutionEvidenceError(PinePythonParityError):
    pass


class PinePythonParityLineageMismatch(PinePythonParityError):
    pass


class PinePythonParityAuthorityInvalid(PinePythonParityError):
    pass


@dataclass(frozen=True, slots=True)
class PinePythonParityContext:
    pine_artifact: PineStrategySourceArtifact
    pine_intake_record: PineStrategyIntakeRecord
    pine_intake_request: PineStrategyIntakeRequest
    pine_intake_context: PineStrategyIntakeContext
    parity_authority_ref: TraceabilityRef


@dataclass(frozen=True, slots=True)
class PinePythonParityExecutionResult:
    result: PinePythonParityResult
    record: PinePythonParityRunRecord
    writes: tuple[RepositoryWriteResult, ...]


def _exact(record: object, object_id: object, version: ObjectVersion) -> TraceabilityRef:
    return TraceabilityRef(object_id, version, fingerprint_record(record))  # type: ignore[arg-type]


def _parse_time(value: str, field: str) -> datetime:
    if not isinstance(value, str) or not value:
        raise PineExecutionEvidenceError(f"{field} is required")
    if value.endswith("Z"):
        value = value[:-1] + "+00:00"
    try:
        parsed = datetime.fromisoformat(value)
    except ValueError as exc:
        raise PineExecutionEvidenceError(f"{field} is malformed") from exc
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise PineExecutionEvidenceError(f"{field} must include an explicit timezone")
    return parsed.astimezone(UTC)


def _canonical_decimal(value: str, field: str, *, positive: bool = False) -> str:
    if not isinstance(value, str) or not value:
        raise PineExecutionEvidenceError(f"{field} is required")
    try:
        parsed = Decimal(value)
    except Exception as exc:
        raise PineExecutionEvidenceError(f"{field} is not decimal") from exc
    if not parsed.is_finite() or parsed < 0 or (positive and parsed <= 0):
        raise PineExecutionEvidenceError(f"{field} is outside the supported domain")
    text = format(parsed, "f")
    if "." in text:
        text = text.rstrip("0").rstrip(".")
    return text or "0"


def import_pine_execution_csv(
    source_bytes: bytes,
    *,
    evidence_id: ArtifactId,
    pine_artifact_ref: TraceabilityRef,
    strategy_ref: TraceabilityRef,
    instrument_ref: TraceabilityRef,
    normalized_manifest_ref: TraceabilityRef,
    normalized_lock_ref: TraceabilityRef,
    observation_start: datetime,
    observation_end: datetime,
    provenance_ref: TraceabilityRef,
    authority_ref: TraceabilityRef,