"""Local-only bounded static Pine v6 strategy intake and exact lineage verification."""

from __future__ import annotations

import re
from dataclasses import dataclass
from decimal import Decimal

from ai_quant_lab.core.dataset_store import LocalDatasetRepository, RepositoryWriteResult
from ai_quant_lab.core.integrity import fingerprint_record
from ai_quant_lab.core.model import ExecutionState, ObjectVersion, TraceabilityRef, fingerprint
from ai_quant_lab.core.optimization_contracts import (
    OptimizationCandidateDefinition,
    OptimizationCandidateResult,
    OptimizationPlan,
    OptimizationRequest,
    OptimizationRunRecord,
    OptimizationSearchSpace,
    OptimizationSelectionResult,
    OptimizationTrialRecord,
    SelectionDecision,
)
from ai_quant_lab.core.optimization_selection import (
    OptimizationEvidence,
    verify_optimization_selection_lineage,
)
from ai_quant_lab.core.pine_strategy_contracts import (
    PineDefaultQuantityType,
    PineIntakeReasonCode,
    PineIntakeStatus,
    PineLanguageVersion,
    PineScriptKind,
    PineSemanticParityStatus,
    PineStrategyIntakeRecord,
    PineStrategyIntakeRequest,
    PineStrategySourceArtifact,
    RepaintAssessmentStatus,
    normalize_pine_source,
    pine_sha256,
)
from ai_quant_lab.core.research_eligibility_contracts import DeploymentAuthorizationStatus
from ai_quant_lab.core.robustness_validation import verify_robustness_validation_lineage
from ai_quant_lab.core.strategy_backtest_contracts import StrategyDefinition


class PineStrategyIntakeError(ValueError):
    pass


class PineIntakeFailure(PineStrategyIntakeError):
    def __init__(
        self,
        status: PineIntakeStatus,
        reason: PineIntakeReasonCode,
        message: str,
    ) -> None:
        super().__init__(message)
        self.status = status
        self.reason_codes = (reason,)


class PineLineageMismatch(PineStrategyIntakeError):
    pass


_V1 = ObjectVersion(1)
_MAX_SOURCE_BYTES = 256 * 1024
_VERSION_LINE = re.compile(r"^[ \t]*//@version[ \t]*=[ \t]*([0-9]+)[ \t]*$")
_DECLARATION = re.compile(r"(?m)^(strategy|indicator)[ \t]*\(")
_UNSUPPORTED = re.compile(
    r"\b(?:request\.[A-Za-z_][A-Za-z0-9_]*|security[ \t]*\(|"
    r"input\.timeframe|timeframe\.|alert(?:condition)?[ \t]*\()"
)


@dataclass(frozen=True, slots=True)
class PineOptimizationSelectionEvidence:
    request: OptimizationRequest
    plan: OptimizationPlan
    search_space: OptimizationSearchSpace
    source: OptimizationEvidence
    candidates: tuple[OptimizationEvidence, ...]
    record: OptimizationRunRecord
    result: OptimizationSelectionResult
    candidate_definitions: tuple[OptimizationCandidateDefinition, ...]
    candidate_results: tuple[OptimizationCandidateResult, ...]
    trials: tuple[OptimizationTrialRecord, ...]


@dataclass(frozen=True, slots=True)
class PineStrategyIntakeContext:
    strategy: StrategyDefinition
    evidence: OptimizationEvidence
    optimization: PineOptimizationSelectionEvidence | None = None


@dataclass(frozen=True, slots=True)
class PineStrategyIntakeExecutionResult:
    artifact: PineStrategySourceArtifact
    record: PineStrategyIntakeRecord
    writes: tuple[RepositoryWriteResult, ...]


@dataclass(frozen=True, slots=True)
class _StaticDeclaration:
    version: PineLanguageVersion
    kind: PineScriptKind
    title: str
    pyramiding: int
    process_orders_on_close: bool
    calc_on_every_tick: bool
    default_qty_type: PineDefaultQuantityType
    default_qty_value: str


def _failure(
    status: PineIntakeStatus, reason: PineIntakeReasonCode, message: str
) -> PineIntakeFailure:
    return PineIntakeFailure(status, reason, message)


def _exact(record: object, object_id: object, version: ObjectVersion) -> TraceabilityRef:
    return TraceabilityRef(object_id, version, fingerprint_record(record))  # type: ignore[arg-type]


def _mask_non_code(source: str) -> str:
    chars = list(source)
    index = 0
    quote: str | None = None
    block_comment = False
    while index < len(chars):
        current = chars[index]
        following = chars[index + 1] if index + 1 < len(chars) else ""
        if block_comment:
            if current == "*" and following == "/":
                chars[index] = chars[index + 1] = " "
                index += 2
                block_comment = False
            else:
                if current != "\n":
                    chars[index] = " "
                index += 1
            continue
        if quote is not None:
            if current == "\\" and following:
                chars[index] = chars[index + 1] = " "
                index += 2
            else:
                if current == quote:
                    quote = None
                if current != "\n":
                    chars[index] = " "
                index += 1
            continue
        if current == "/" and following == "*":
            chars[index] = chars[index + 1] = " "
            block_comment = True
            index += 2
        elif current == "/" and following == "/":
            while index < len(chars) and chars[index] != "\n":
                chars[index] = " "
                index += 1
        elif current in ('"', "'"):
            quote = current
            chars[index] = " "
            index += 1
        else:
            index += 1
    return "".join(chars)


def _version_declarations(source: str) -> tuple[int, ...]:
    versions: list[int] = []
    block_comment = False
    for line in source.splitlines():
        stripped = line.strip()
        if block_comment:
            if "*/" in stripped:
                block_comment = False
            continue
        if stripped.startswith("/*"):
            if "*/" not in stripped[2:]:
                block_comment = True
            continue
        match = _VERSION_LINE.fullmatch(line)
        if match:
            versions.append(int(match.group(1)))
    return tuple(versions)


def _call_body(source: str, open_parenthesis: int) -> str:
    depth = 0
    quote: str | None = None
    escaped = False
    for index in range(open_parenthesis, len(source)):
        current = source[index]
        if quote is not None:
            if escaped:
                escaped = False
            elif current == "\\":
                escaped = True
            elif current == quote:
                quote = None
            continue
        if current in ('"', "'"):
            quote = current
        elif current == "(":
            depth += 1
        elif current == ")":
            depth -= 1
            if depth == 0:
                return source[open_parenthesis + 1 : index]
    raise _failure(
        PineIntakeStatus.INCOMPLETE,
        PineIntakeReasonCode.SCRIPT_KIND_UNKNOWN,
        "Pine declaration is not statically complete",
    )


def _setting(body: str, name: str) -> str | None:
    match = re.search(rf"\b{re.escape(name)}[ \t]*=[ \t]*([^,\n)]+)", body)
    return None if match is None else match.group(1).strip()


def _canonical_decimal(value: Decimal) -> str:
    text = format(value, "f")
    if "." in text:
        text = text.rstrip("0").rstrip(".")
    return text or "0"


def _parse_static_source(source: str, strategy: StrategyDefinition) -> _StaticDeclaration:
    versions = _version_declarations(source)
    if not versions:
        raise _failure(
            PineIntakeStatus.INCOMPLETE,
            PineIntakeReasonCode.MISSING_VERSION,
            "Pine source is missing an exact version declaration",
        )
    if len(versions) != 1:
        raise _failure(
            PineIntakeStatus.REJECTED,
            PineIntakeReasonCode.MULTIPLE_VERSION_DECLARATIONS,
            "Pine source contains multiple version declarations",
        )
    if versions[0] != 6:
        raise _failure(
            PineIntakeStatus.UNSUPPORTED,
            PineIntakeReasonCode.UNSUPPORTED_VERSION,
            "only Pine version 6 is supported",
        )
    masked = _mask_non_code(source)
    declarations = tuple(_DECLARATION.finditer(masked))
    if not declarations:
        raise _failure(
            PineIntakeStatus.INCOMPLETE,
            PineIntakeReasonCode.SCRIPT_KIND_UNKNOWN,
            "Pine source has no supported top-level declaration",
        )
    if len(declarations) != 1:
        raise _failure(
            PineIntakeStatus.REJECTED,
            PineIntakeReasonCode.MULTIPLE_TOP_LEVEL_DECLARATIONS,
            "Pine source has multiple top-level declarations",
        )
    declaration = declarations[0]
    kind = (
        PineScriptKind.STRATEGY if declaration.group(1) == "strategy" else PineScriptKind.INDICATOR
    )
    if kind is PineScriptKind.INDICATOR:
        raise _failure(
            PineIntakeStatus.REJECTED,
            PineIntakeReasonCode.INDICATOR_NOT_STRATEGY,
            "indicator source cannot enter governed strategy intake",
        )
    if _UNSUPPORTED.search(masked):
        raise _failure(
            PineIntakeStatus.UNSUPPORTED,
            PineIntakeReasonCode.UNSUPPORTED_FEATURE,
            "Pine source uses unsupported external or mixed-timeframe data",
        )
    open_parenthesis = masked.find("(", declaration.start())
    body = _call_body(source, open_parenthesis)
    title_match = re.match(r'\s*"([^"\\]+)"\s*(?:,|$)', body)
    if title_match is None:
        raise _failure(
            PineIntakeStatus.INCOMPLETE,
            PineIntakeReasonCode.STATIC_TITLE_REQUIRED,
            "Pine strategy title must be a static literal",
        )
    settings = {
        name: _setting(body, name)
        for name in (
            "pyramiding",
            "process_orders_on_close",
            "calc_on_every_tick",
            "default_qty_type",
            "default_qty_value",
        )
    }
    if any(value is None for value in settings.values()):
        raise _failure(
            PineIntakeStatus.INCOMPLETE,
            PineIntakeReasonCode.MISSING_STATIC_SETTING,
            "Pine strategy declaration is missing a required static setting",
        )
    expected_notional = _canonical_decimal(
        Decimal(strategy.fixed_notional_minor) / Decimal(strategy.capital_minor_unit_scale)
    )
    literal_value = settings["default_qty_value"]
    try:
        quantity_matches = (
            literal_value is not None
            and re.fullmatch(r"(?:0|[1-9][0-9]*)(?:\.[0-9]+)?", literal_value) is not None
            and Decimal(literal_value) == Decimal(expected_notional)
        )
    except Exception:  # pragma: no cover - guarded by the literal expression
        quantity_matches = False
    if (
        settings["pyramiding"] != "0"
        or settings["process_orders_on_close"] != "false"
        or settings["calc_on_every_tick"] != "false"
        or settings["default_qty_type"] != PineDefaultQuantityType.STRATEGY_CASH.value
        or not quantity_matches
    ):
        raise _failure(
            PineIntakeStatus.UNSUPPORTED,
            PineIntakeReasonCode.STATIC_SETTING_MISMATCH,
            "Pine strategy settings do not match the governed engine profile",
        )
    return _StaticDeclaration(
        PineLanguageVersion.PINE_V6,
        kind,
        title_match.group(1),
        0,
        False,
        False,
        PineDefaultQuantityType.STRATEGY_CASH,
        expected_notional,
    )


def _decode_source(source_bytes: bytes) -> tuple[str, str, str, str]:
    if not source_bytes:
        raise _failure(
            PineIntakeStatus.REJECTED,
            PineIntakeReasonCode.EMPTY_SOURCE,
            "Pine source cannot be empty",
        )
    if len(source_bytes) > _MAX_SOURCE_BYTES:
        raise _failure(
            PineIntakeStatus.REJECTED,
            PineIntakeReasonCode.SOURCE_TOO_LARGE,
            "Pine source exceeds the 256 KiB limit",
        )
    if b"\x00" in source_bytes:
        raise _failure(
            PineIntakeStatus.REJECTED,
            PineIntakeReasonCode.NUL_BYTE_PRESENT,
            "Pine source contains a NUL byte",
        )
    try:
        source = source_bytes.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise _failure(
            PineIntakeStatus.REJECTED,
            PineIntakeReasonCode.INVALID_ENCODING,
            "Pine source must be valid UTF-8",
        ) from exc
    if any(ord(char) < 32 and char not in "\t\n\r" for char in source):
        raise _failure(
            PineIntakeStatus.REJECTED,
            PineIntakeReasonCode.BINARY_CONTENT,
            "Pine source contains unsupported control bytes",
        )
    normalized = normalize_pine_source(source)
    return (
        source,
        normalized,
        pine_sha256(source_bytes),
        pine_sha256(normalized.encode("utf-8")),
    )


def _verify_robustness(evidence: OptimizationEvidence) -> None:
    try:
        verify_robustness_validation_lineage(
            record=evidence.robustness_record,
            result=evidence.robustness_result,
            request=evidence.robustness_request,
            plan=evidence.robustness_plan,
            scientific_result=evidence.scientific_result,
            validation_record=evidence.validation_record,
            scientific_request=evidence.scientific_request,
            validation_plan=evidence.validation_plan,
            backtest_artifact=evidence.backtest_artifact,
            backtest_record=evidence.backtest_record,
            backtest_request=evidence.backtest_request,
            authorization=evidence.authorization,
            specification=evidence.specification,
            policy=evidence.authorization_policy,
            eligibility=evidence.eligibility,
            eligibility_policy=evidence.eligibility_policy,
            admission=evidence.admission,
            declaration=evidence.declaration,
            engine_contract=evidence.engine_contract,
            strategy=evidence.strategy,
            instrument=evidence.instrument,
            report=evidence.report,
        )
    except ValueError as exc:
        raise PineLineageMismatch("Pine source evidence failed exact verification") from exc


def _verify_context(request: PineStrategyIntakeRequest, context: PineStrategyIntakeContext) -> None:
    strategy_ref = _exact(context.strategy, context.strategy.strategy_id, context.strategy.version)
    if (
        request.strategy_definition_ref != strategy_ref
        or context.evidence.strategy != context.strategy
    ):
        raise PineLineageMismatch("Pine strategy does not bind the exact StrategyDefinition")
    _verify_robustness(context.evidence)
    expected_evidence = (
        _exact(
            context.evidence.backtest_artifact,
            context.evidence.backtest_artifact.artifact_id,
            context.evidence.backtest_artifact.version,
        ),
        _exact(
            context.evidence.scientific_result,
            context.evidence.scientific_result.validation_result_id,
            context.evidence.scientific_result.version,
        ),
        _exact(
            context.evidence.robustness_result,
            context.evidence.robustness_result.robustness_result_id,
            context.evidence.robustness_result.version,
        ),
    )
    if (
        request.source_backtest_result_ref,
        request.source_scientific_validation_ref,
        request.source_robustness_result_ref,
    ) != expected_evidence:
        raise PineLineageMismatch("Pine source evidence references do not match exact evidence")
    optional = (
        request.optimization_candidate_definition_ref,
        request.optimization_candidate_result_ref,
        request.optimization_selection_ref,
    )
    if context.optimization is None:
        if any(item is not None for item in optional):
            raise PineLineageMismatch("direct Pine binding cannot claim optimization selection")
        return
    selection = context.optimization
    try:
        verify_optimization_selection_lineage(
            record=selection.record,
            result=selection.result,
            candidate_definitions=selection.candidate_definitions,
            candidate_results=selection.candidate_results,
            trials=selection.trials,
            request=selection.request,
            plan=selection.plan,
            search_space=selection.search_space,
            source=selection.source,
            candidates=selection.candidates,
        )
    except ValueError as exc:
        raise PineLineageMismatch("Pine optimization selection failed exact verification") from exc
    if selection.result.decision is not SelectionDecision.SELECTED:
        raise PineLineageMismatch("Pine optimization binding requires a selected candidate")
    definition = next(
        (
            item
            for item in selection.candidate_definitions
            if request.optimization_candidate_definition_ref
            == _exact(item, item.candidate_id, item.version)
        ),
        None,
    )
    candidate_result = next(
        (
            item
            for item in selection.candidate_results
            if request.optimization_candidate_result_ref
            == _exact(item, item.candidate_id, item.version)
        ),
        None,
    )
    if definition is None or candidate_result is None:
        raise PineLineageMismatch("Pine candidate references are absent from exact selection")
    if request.optimization_selection_ref != _exact(
        selection.result, selection.result.selection_result_id, selection.result.version
    ):
        raise PineLineageMismatch("Pine selection reference is not exact")
    if selection.result.selected_candidate_ref != request.optimization_candidate_result_ref:
        raise PineLineageMismatch("Pine source does not bind the actually selected candidate")
    if (
        definition.candidate_strategy_ref != strategy_ref
        or candidate_result.candidate_definition_ref
        != request.optimization_candidate_definition_ref
        or candidate_result.candidate_strategy_ref != strategy_ref
        or candidate_result.backtest_result_ref != expected_evidence[0]
        or candidate_result.scientific_validation_result_ref != expected_evidence[1]
        or candidate_result.robustness_result_ref != expected_evidence[2]
        or context.evidence not in selection.candidates
    ):
        raise PineLineageMismatch("Pine selected-candidate evidence binding is not exact")


def _input_fingerprint(
    request: PineStrategyIntakeRequest,
    *,
    raw_hash: str,
    normalized_hash: str,
    declaration: _StaticDeclaration,
) -> str:
    return fingerprint(
        {
            "raw_source_sha256": raw_hash,
            "normalized_source_sha256": normalized_hash,
            "pine_language_version": declaration.version,
            "script_kind": declaration.kind,
            "strategy_definition_ref": request.strategy_definition_ref,
            "optimization_candidate_definition_ref": (
                request.optimization_candidate_definition_ref
            ),
            "optimization_candidate_result_ref": request.optimization_candidate_result_ref,
            "optimization_selection_ref": request.optimization_selection_ref,
            "source_backtest_result_ref": request.source_backtest_result_ref,
            "source_scientific_validation_ref": request.source_scientific_validation_ref,
            "source_robustness_result_ref": request.source_robustness_result_ref,
            "authority_ref": request.authority_ref,
            "provenance_ref": request.provenance_ref,
        }
    )


def _build(
    request: PineStrategyIntakeRequest,
    *,
    context: PineStrategyIntakeContext,
) -> tuple[PineStrategySourceArtifact, PineStrategyIntakeRecord]:
    source, normalized, raw_hash, normalized_hash = _decode_source(request.source_bytes)
    _verify_context(request, context)
    declaration = _parse_static_source(source, context.strategy)
    artifact = PineStrategySourceArtifact(
        request.requested_artifact_id,
        _V1,
        declaration.version,
        source,
        normalized,
        raw_hash,
        normalized_hash,
        len(request.source_bytes),
        declaration.kind,
        declaration.title,
        declaration.pyramiding,
        declaration.process_orders_on_close,
        declaration.calc_on_every_tick,
        declaration.default_qty_type,
        declaration.default_qty_value,
        request.strategy_definition_ref,
        request.optimization_candidate_definition_ref,
        request.optimization_candidate_result_ref,
        request.optimization_selection_ref,
        request.source_backtest_result_ref,
        request.source_scientific_validation_ref,
        request.source_robustness_result_ref,
        request.provenance_ref,
        request.authority_ref,
        PineSemanticParityStatus.NOT_EVALUATED,
        RepaintAssessmentStatus.NOT_EVALUATED,
        DeploymentAuthorizationStatus.NOT_AUTHORIZED,
        ExecutionState.PLANNED_CLOSED,
        _V1,
    )
    record = PineStrategyIntakeRecord(
        request.intake_run_id,
        _V1,
        _exact(artifact, artifact.pine_artifact_id, artifact.version),
        normalized_hash,
        _input_fingerprint(
            request,
            raw_hash=raw_hash,
            normalized_hash=normalized_hash,
            declaration=declaration,
        ),
        PineIntakeStatus.ACCEPTED,
        (PineIntakeReasonCode.ACCEPTED_BOUNDED_STATIC_INTAKE,),
        request.authority_ref,
        request.provenance_ref,
        DeploymentAuthorizationStatus.NOT_AUTHORIZED,
        ExecutionState.PLANNED_CLOSED,
        _V1,
    )
    return artifact, record


def intake_pine_strategy(
    request: PineStrategyIntakeRequest,
    *,
    context: PineStrategyIntakeContext,
    repository: LocalDatasetRepository,
) -> PineStrategyIntakeExecutionResult:
    artifact, record = _build(request, context=context)
    writes = (repository.store(artifact), repository.store(record))
    return PineStrategyIntakeExecutionResult(artifact, record, writes)


def verify_pine_strategy_intake_lineage(
    *,
    artifact: PineStrategySourceArtifact,
    record: PineStrategyIntakeRecord,
    request: PineStrategyIntakeRequest,
    context: PineStrategyIntakeContext,
) -> None:
    try:
        expected_artifact, expected_record = _build(request, context=context)
    except PineIntakeFailure as exc:
        raise PineLineageMismatch("persisted Pine source no longer passes bounded intake") from exc
    if artifact != expected_artifact or record != expected_record:
        raise PineLineageMismatch("Pine intake lineage is not exact and deterministic")
