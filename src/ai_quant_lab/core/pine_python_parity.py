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
from ai_quant_lab.core.optimization_selection import OptimizationEvidence
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
) -> PineExecutionEvidence:
    """Parse one strict local CSV representation; no network or Pine execution occurs."""
    if not isinstance(source_bytes, bytes) or not source_bytes:
        raise PineExecutionEvidenceError("Pine execution CSV cannot be empty")
    try:
        text = source_bytes.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise PineExecutionEvidenceError("Pine execution CSV must be UTF-8") from exc
    reader = csv.DictReader(io.StringIO(text, newline=""))
    if reader.fieldnames is None or tuple(reader.fieldnames) != _COLUMNS:
        raise PineExecutionEvidenceError("Pine execution CSV columns must match the v1 contract")
    events: list[PineExecutionEvent] = []
    for row_number, row in enumerate(reader, start=2):
        if None in row or set(row) != set(_COLUMNS):
            raise PineExecutionEvidenceError("Pine execution CSV row shape is invalid")
        try:
            index = int(row["event_index"])
        except (TypeError, ValueError) as exc:
            raise PineExecutionEvidenceError("event_index must be an integer") from exc
        try:
            action = PineExecutionAction(row["action"])
            side = PineExecutionSide(row["side"])
            position = SimulatedPositionState(row["position_after"])
        except ValueError as exc:
            raise PineExecutionEvidenceError("event enum value is unsupported") from exc
        events.append(
            PineExecutionEvent(
                index,
                _parse_time(row["signal_time"], "signal_time"),
                _parse_time(row["execution_time"], "execution_time"),
                action,
                side,
                _canonical_decimal(row["execution_price"], "execution_price", positive=True),
                position,
                _canonical_decimal(row["quantity"], "quantity", positive=True),
                _canonical_decimal(row["commission"], "commission"),
                row["trade_id"],
                row_number,
            )
        )
    import hashlib

    digest = "sha256:" + hashlib.sha256(source_bytes).hexdigest()
    return PineExecutionEvidence(
        evidence_id,
        _V1,
        pine_artifact_ref,
        strategy_ref,
        instrument_ref,
        normalized_manifest_ref,
        normalized_lock_ref,
        observation_start.astimezone(UTC),
        observation_end.astimezone(UTC),
        PineEvidenceSourceFormat.CSV_V1,
        text,
        digest,
        len(source_bytes),
        tuple(events),
        provenance_ref,
        authority_ref,
        _V1,
    )


def _verify_context(
    request: PinePythonParityRequest,
    evidence: PineExecutionEvidence,
    policy: ParityTolerancePolicy,
    context: PinePythonParityContext,
) -> OptimizationEvidence:
    if request.authority_ref != context.parity_authority_ref:
        raise PinePythonParityAuthorityInvalid("parity request lacks exact governed authority")
    if evidence.authority_ref != context.parity_authority_ref:
        raise PinePythonParityAuthorityInvalid(
            "Pine execution evidence lacks exact governed authority"
        )
    if policy.authority_ref != context.parity_authority_ref:
        raise PinePythonParityAuthorityInvalid("tolerance policy lacks exact governed authority")

    pine_artifact = context.pine_artifact
    pine_record = context.pine_intake_record
    if (
        getattr(pine_artifact, "semantic_parity", None)
        is not PineSemanticParityStatus.NOT_EVALUATED
        or getattr(pine_artifact, "repaint_assessment", None)
        is not RepaintAssessmentStatus.NOT_EVALUATED
        or getattr(pine_record, "status", None) is not PineIntakeStatus.ACCEPTED
    ):
        raise PinePythonParityLineageMismatch("Sprint 17 Pine intake state is not admissible")
    try:
        verify_pine_strategy_intake_lineage(
            artifact=pine_artifact,
            record=pine_record,
            request=context.pine_intake_request,
            context=context.pine_intake_context,
        )
    except ValueError as exc:
        raise PinePythonParityLineageMismatch("Pine intake lineage failed verification") from exc

    source = context.pine_intake_context.evidence
    try:
        verify_strategy_backtest_lineage(
            record=source.backtest_record,
            artifact=source.backtest_artifact,
            request=source.backtest_request,
            authorization=source.authorization,
            specification=source.specification,
            policy=source.authorization_policy,
            eligibility=source.eligibility,
            engine_contract=source.engine_contract,
            strategy=source.strategy,
            instrument=source.instrument,
            report=source.report,
        )
    except ValueError as exc:
        raise PinePythonParityLineageMismatch(
            "Python backtest lineage failed verification"
        ) from exc

    expected_refs = {
        "pine_artifact_ref": _exact(
            pine_artifact,
            pine_artifact.pine_artifact_id,
            pine_artifact.version,
        ),
        "pine_intake_record_ref": _exact(
            pine_record,
            pine_record.intake_run_id,
            pine_record.version,
        ),
        "python_backtest_ref": _exact(
            source.backtest_artifact,
            source.backtest_artifact.artifact_id,
            source.backtest_artifact.version,
        ),
        "pine_execution_evidence_ref": _exact(evidence, evidence.evidence_id, evidence.version),
        "strategy_ref": _exact(
            source.strategy, source.strategy.strategy_id, source.strategy.version
        ),
        "instrument_ref": _exact(
            source.instrument, source.instrument.instrument_id, source.instrument.version
        ),
        "normalized_manifest_ref": source.backtest_artifact.normalized_manifest_ref,
        "normalized_lock_ref": source.backtest_artifact.normalized_lock_ref,
        "tolerance_policy_ref": _exact(policy, policy.policy_id, policy.version),
    }
    for field, expected in expected_refs.items():
        if getattr(request, field) != expected:
            raise PinePythonParityLineageMismatch(f"{field} does not bind exact governed evidence")
    if (
        evidence.pine_artifact_ref != expected_refs["pine_artifact_ref"]
        or evidence.strategy_ref != expected_refs["strategy_ref"]
        or evidence.instrument_ref != expected_refs["instrument_ref"]
        or evidence.normalized_manifest_ref != expected_refs["normalized_manifest_ref"]
        or evidence.normalized_lock_ref != expected_refs["normalized_lock_ref"]
        or request.observation_start != source.specification.observation_start
        or request.observation_end != source.specification.observation_end
        or evidence.observation_start != request.observation_start
        or evidence.observation_end != request.observation_end
    ):
        raise PinePythonParityLineageMismatch("parity identity/window binding is inconsistent")
    if pine_artifact.source_backtest_result_ref != expected_refs["python_backtest_ref"]:
        raise PinePythonParityLineageMismatch("Pine source is not bound to this Python backtest")
    return source


def _expected_events(
    backtest_artifact: BacktestResultArtifact,
) -> tuple[PineExecutionEvent, ...]:
    trade_by_fill: dict[object, str] = {}
    for trade in backtest_artifact.trades:
        trade_by_fill[trade.entry_fill_id] = str(trade.trade_id)
        trade_by_fill[trade.exit_fill_id] = str(trade.trade_id)
    events: list[PineExecutionEvent] = []
    for index, (order, fill) in enumerate(
        zip(backtest_artifact.orders, backtest_artifact.fills, strict=True)
    ):
        action = (
            PineExecutionAction.ENTRY
            if order.side is SimulatedOrderSide.BUY
            else PineExecutionAction.EXIT
        )
        state = (
            SimulatedPositionState.LONG
            if action is PineExecutionAction.ENTRY
            else SimulatedPositionState.FLAT
        )
        events.append(
            PineExecutionEvent(
                index,
                order.signal_time,
                fill.fill_time,
                action,
                PineExecutionSide.LONG,
                fill.execution_price,
                state,
                fill.quantity,
                fill.commission,
                trade_by_fill.get(fill.fill_id, ""),
                index + 2,
            )
        )
    return tuple(events)


def _within(actual: str, expected: str, absolute: str, relative: str = "0") -> bool:
    with localcontext(_DECIMAL_CONTEXT):
        observed = Decimal(actual)
        target = Decimal(expected)
        allowed = max(Decimal(absolute), abs(target) * Decimal(relative))
        return abs(observed - target) <= allowed


def _mismatch(
    items: list[ParityMismatch],
    kind: ParityMismatchType,
    expected: object,
    observed: object,
    expected_index: int | None,
    observed_index: int | None,
) -> None:
    items.append(
        ParityMismatch(
            len(items),
            kind,
            str(expected),
            str(observed),
            expected_index,
            observed_index,
            kind.value,
        )
    )


def _compare(
    expected: tuple[PineExecutionEvent, ...],
    observed: tuple[PineExecutionEvent, ...],
    *,
    backtest_artifact: BacktestResultArtifact,
    policy: ParityTolerancePolicy,
) -> tuple[PinePythonParityDecision, tuple[ParityMismatch, ...]]:
    if expected and not observed:
        return PinePythonParityDecision.INCONCLUSIVE, ()
    mismatches: list[ParityMismatch] = []
    overlap = min(len(expected), len(observed))
    for index in range(overlap):
        exp, obs = expected[index], observed[index]
        if exp.action is not obs.action:
            _mismatch(
                mismatches,
                ParityMismatchType.ACTION_MISMATCH,
                exp.action,
                obs.action,
                index,
                index,
            )
        if exp.side is not obs.side:
            _mismatch(
                mismatches,
                ParityMismatchType.SIDE_MISMATCH,
                exp.side,
                obs.side,
                index,
                index,
            )
        if exp.signal_time != obs.signal_time:
            _mismatch(
                mismatches,
                ParityMismatchType.SIGNAL_TIME_MISMATCH,
                exp.signal_time.isoformat(),
                obs.signal_time.isoformat(),
                index,
                index,
            )
        if exp.execution_time != obs.execution_time:
            _mismatch(
                mismatches,
                ParityMismatchType.EXECUTION_TIME_MISMATCH,
                exp.execution_time.isoformat(),
                obs.execution_time.isoformat(),
                index,
                index,
            )
        if not _within(
            obs.execution_price,
            exp.execution_price,
            policy.absolute_price_tolerance,
            policy.relative_price_tolerance,
        ):
            _mismatch(
                mismatches,
                ParityMismatchType.PRICE_MISMATCH,
                exp.execution_price,
                obs.execution_price,
                index,
                index,
            )
        if not _within(obs.quantity, exp.quantity, policy.quantity_tolerance):
            _mismatch(
                mismatches,
                ParityMismatchType.QUANTITY_MISMATCH,
                exp.quantity,
                obs.quantity,
                index,
                index,
            )
        if not _within(obs.commission, exp.commission, policy.commission_tolerance):
            _mismatch(
                mismatches,
                ParityMismatchType.COMMISSION_MISMATCH,
                exp.commission,
                obs.commission,
                index,
                index,
            )
        if exp.position_after is not obs.position_after:
            _mismatch(
                mismatches,
                ParityMismatchType.POSITION_STATE_MISMATCH,
                exp.position_after,
                obs.position_after,
                index,
                index,
            )

    for index in range(overlap, len(expected)):
        _mismatch(
            mismatches,
            ParityMismatchType.MISSING_EVENT,
            expected[index].action,
            "<missing>",
            index,
            None,
        )
    for index in range(overlap, len(observed)):
        _mismatch(
            mismatches,
            ParityMismatchType.EXTRA_EVENT,
            "<none>",
            observed[index].action,
            None,
            index,
        )

    expected_completed = sum(event.action is PineExecutionAction.EXIT for event in expected)
    observed_completed = sum(event.action is PineExecutionAction.EXIT for event in observed)
    if (
        expected_completed != backtest_artifact.trade_count
        or observed_completed != backtest_artifact.trade_count
    ):
        _mismatch(
            mismatches,
            ParityMismatchType.TRADE_COUNT_MISMATCH,
            backtest_artifact.trade_count,
            observed_completed,
            None,
            None,
        )

    expected_final = expected[-1].position_after if expected else SimulatedPositionState.FLAT
    observed_final = observed[-1].position_after if observed else SimulatedPositionState.FLAT
    if (
        expected_final is not backtest_artifact.open_position
        or observed_final is not backtest_artifact.open_position
    ):
        _mismatch(
            mismatches,
            ParityMismatchType.POSITION_STATE_MISMATCH,
            backtest_artifact.open_position,
            observed_final,
            len(expected) - 1 if expected else None,
            len(observed) - 1 if observed else None,
        )
    return (
        PinePythonParityDecision.MISMATCH if mismatches else PinePythonParityDecision.MATCH,
        tuple(mismatches),
    )


def _input_fingerprint(
    request: PinePythonParityRequest,
    evidence: PineExecutionEvidence,
    policy: ParityTolerancePolicy,
    expected: tuple[PineExecutionEvent, ...],
) -> str:
    return fingerprint(
        {
            "request": request,
            "evidence_fingerprint": fingerprint_record(evidence),
            "policy_fingerprint": fingerprint_record(policy),
            "expected_events": expected,
        }
    )


def _build(
    request: PinePythonParityRequest,
    *,
    evidence: PineExecutionEvidence,
    policy: ParityTolerancePolicy,
    context: PinePythonParityContext,
) -> tuple[PinePythonParityResult, PinePythonParityRunRecord]:
    source = _verify_context(request, evidence, policy, context)
    expected = _expected_events(source.backtest_artifact)
    decision, mismatches = _compare(
        expected,
        evidence.events,
        backtest_artifact=source.backtest_artifact,
        policy=policy,
    )
    input_fp = _input_fingerprint(request, evidence, policy, expected)
    semantic = {
        PinePythonParityDecision.MATCH: PineParitySemanticStatus.MATCHED,
        PinePythonParityDecision.MISMATCH: PineParitySemanticStatus.MISMATCHED,
        PinePythonParityDecision.INCONCLUSIVE: PineParitySemanticStatus.INCONCLUSIVE,
    }[decision]
    reason = {
        PinePythonParityDecision.MATCH: (PineParityReasonCode.EXACT_EVENT_PARITY,),
        PinePythonParityDecision.MISMATCH: (PineParityReasonCode.EVENT_MISMATCH,),
        PinePythonParityDecision.INCONCLUSIVE: (PineParityReasonCode.INCOMPLETE_EXTERNAL_EVIDENCE,),
    }[decision]
    result = PinePythonParityResult(
        request.result_id,
        _V1,
        request.pine_artifact_ref,
        request.pine_execution_evidence_ref,
        request.python_backtest_ref,
        request.strategy_ref,
        request.instrument_ref,
        request.normalized_manifest_ref,
        request.normalized_lock_ref,
        request.tolerance_policy_ref,
        len(expected),
        len(evidence.events),
        len(mismatches),
        mismatches,
        decision,
        reason,
        input_fp,
        semantic,
        RepaintAssessmentStatus.NOT_EVALUATED,
        request.authority_ref,
        request.provenance_ref,
        DeploymentAuthorizationStatus.NOT_AUTHORIZED,
        ExecutionState.PLANNED_CLOSED,
        _V1,
    )
    record = PinePythonParityRunRecord(
        request.parity_run_id,
        _V1,
        fingerprint(request),
        _exact(result, result.parity_result_id, result.version),
        input_fp,
        result.expected_event_count,
        result.observed_event_count,
        result.mismatch_count,
        result.decision,
        request.authority_ref,
        request.provenance_ref,
        DeploymentAuthorizationStatus.NOT_AUTHORIZED,
        ExecutionState.PLANNED_CLOSED,
        _V1,
    )
    return result, record


def evaluate_pine_python_parity(
    request: PinePythonParityRequest,
    *,
    evidence: PineExecutionEvidence,
    policy: ParityTolerancePolicy,
    context: PinePythonParityContext,
    repository: LocalDatasetRepository,
) -> PinePythonParityExecutionResult:
    result, record = _build(request, evidence=evidence, policy=policy, context=context)
    writes = (
        repository.store(policy),
        repository.store(evidence),
        repository.store(result),
        repository.store(record),
    )
    return PinePythonParityExecutionResult(result, record, writes)


def verify_pine_python_parity_lineage(
    *,
    result: PinePythonParityResult,
    record: PinePythonParityRunRecord,
    request: PinePythonParityRequest,
    evidence: PineExecutionEvidence,
    policy: ParityTolerancePolicy,
    context: PinePythonParityContext,
) -> None:
    expected_result, expected_record = _build(
        request, evidence=evidence, policy=policy, context=context
    )
    if result != expected_result or record != expected_record:
        raise PinePythonParityLineageMismatch(
            "Pine ↔ Python parity lineage is not exact and deterministic"
        )
