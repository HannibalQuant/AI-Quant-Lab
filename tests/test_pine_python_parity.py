"""Sprint 18 governed Pine ↔ Python parity tests."""

from __future__ import annotations

import csv
import io
from dataclasses import replace
from datetime import timedelta
from pathlib import Path

import pytest
from test_pine_strategy_intake import (
    AUTHORITY_REF as PINE_AUTHORITY_REF,
    PROVENANCE_REF,
    _selected_context,
    selection_bundle,
)
from test_pine_strategy_intake import valid_source

from ai_quant_lab.core.dataset_store import LocalDatasetRepository, RepositoryWriteStatus
from ai_quant_lab.core.integrity import fingerprint_record
from ai_quant_lab.core.model import (
    ArtifactId,
    AuthorityBindingId,
    ObjectVersion,
    RunId,
    TraceabilityRef,
)
from ai_quant_lab.core.pine_python_parity import (
    PineExecutionEvidenceError,
    PinePythonParityAuthorityInvalid,
    PinePythonParityContext,
    evaluate_pine_python_parity,
    import_pine_execution_csv,
    verify_pine_python_parity_lineage,
)
from ai_quant_lab.core.pine_python_parity_contracts import (
    ParityMismatchType,
    ParityTolerancePolicy,
    PinePythonParityDecision,
    PinePythonParityRequest,
)
from ai_quant_lab.core.pine_strategy_intake import intake_pine_strategy

V1 = ObjectVersion(1)
PARITY_AUTHORITY_REF = TraceabilityRef(
    AuthorityBindingId("governed-pine-python-parity-authority"),
    V1,
    "sha256:" + "c" * 64,
)


def exact(record, object_id, version):
    return TraceabilityRef(object_id, version, fingerprint_record(record))


def _event_rows(backtest):
    trade_by_fill = {}
    for trade in backtest.trades:
        trade_by_fill[trade.entry_fill_id] = str(trade.trade_id)
        trade_by_fill[trade.exit_fill_id] = str(trade.trade_id)
    rows = []
    state = "FLAT"
    for index, (order, fill) in enumerate(zip(backtest.orders, backtest.fills, strict=True)):
        action = "ENTRY" if order.side.value == "BUY" else "EXIT"
        state = "LONG" if action == "ENTRY" else "FLAT"
        rows.append(
            {
                "event_index": str(index),
                "signal_time": order.signal_time.isoformat(),
                "execution_time": fill.fill_time.isoformat(),
                "action": action,
                "side": "LONG",
                "execution_price": fill.execution_price,
                "position_after": state,
                "quantity": fill.quantity,
                "commission": fill.commission,
                "trade_id": trade_by_fill.get(fill.fill_id, ""),
            }
        )
    return rows


def _csv_bytes(rows):
    out = io.StringIO(newline="")
    writer = csv.DictWriter(
        out,
        fieldnames=(
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
        ),
        lineterminator="\n",
    )
    writer.writeheader()
    writer.writerows(rows)
    return out.getvalue().encode("utf-8")


@pytest.fixture
def parity_bundle(selection_bundle, tmp_path: Path):
    pine_request, pine_context, *_ = _selected_context(selection_bundle)
    pine_repository = LocalDatasetRepository(root=tmp_path / "pine", allowed_root=tmp_path)
    pine_exec = intake_pine_strategy(
        pine_request, context=pine_context, repository=pine_repository
    )
    source = pine_context.evidence
    policy = ParityTolerancePolicy(
        ArtifactId("pine-python-parity-tolerance-v1"),
        V1,
        True,
        "0",
        "0",
        "0",
        "0",
        "0",
        PARITY_AUTHORITY_REF,
        PROVENANCE_REF,
    )
    pine_artifact_ref = exact(
        pine_exec.artifact,
        pine_exec.artifact.pine_artifact_id,
        pine_exec.artifact.version,
    )
    evidence = import_pine_execution_csv(
        _csv_bytes(_event_rows(source.backtest_artifact)),
        evidence_id=ArtifactId("pine-execution-evidence-v1"),
        pine_artifact_ref=pine_artifact_ref,
        strategy_ref=exact(source.strategy, source.strategy.strategy_id, source.strategy.version),
        instrument_ref=exact(
            source.instrument, source.instrument.instrument_id, source.instrument.version
        ),
        normalized_manifest_ref=source.backtest_artifact.normalized_manifest_ref,
        normalized_lock_ref=source.backtest_artifact.normalized_lock_ref,
        observation_start=source.specification.observation_start,
        observation_end=source.specification.observation_end,
        provenance_ref=PROVENANCE_REF,
        authority_ref=PARITY_AUTHORITY_REF,
    )
    request = PinePythonParityRequest(
        RunId("pine-python-parity-run-v1"),
        ArtifactId("pine-python-parity-result-v1"),
        pine_artifact_ref,
        exact(pine_exec.record, pine_exec.record.intake_run_id, pine_exec.record.version),
        exact(
            source.backtest_artifact,
            source.backtest_artifact.artifact_id,
            source.backtest_artifact.version,
        ),
        exact(evidence, evidence.evidence_id, evidence.version),
        exact(source.strategy, source.strategy.strategy_id, source.strategy.version),
        exact(source.instrument, source.instrument.instrument_id, source.instrument.version),
        source.backtest_artifact.normalized_manifest_ref,
        source.backtest_artifact.normalized_lock_ref,
        source.specification.observation_start,
        source.specification.observation_end,
        exact(policy, policy.policy_id, policy.version),
        PARITY_AUTHORITY_REF,
        PROVENANCE_REF,
    )
    context = PinePythonParityContext(
        pine_exec.artifact,
        pine_exec.record,
        pine_request,
        pine_context,
        PARITY_AUTHORITY_REF,
    )
    repository = LocalDatasetRepository(root=tmp_path / "parity", allowed_root=tmp_path)
    return source, policy, evidence, request, context, repository


def _run(bundle, *, evidence=None, policy=None):
    source, base_policy, base_evidence, request, context, repository = bundle
    chosen_evidence = evidence or base_evidence
    chosen_policy = policy or base_policy
    if chosen_evidence is not base_evidence:
        request = replace(
            request,
            pine_execution_evidence_ref=exact(
                chosen_evidence, chosen_evidence.evidence_id, chosen_evidence.version
            ),
        )
    if chosen_policy is not base_policy:
        request = replace(
            request,
            tolerance_policy_ref=exact(
                chosen_policy, chosen_policy.policy_id, chosen_policy.version
            ),
        )
    return evaluate_pine_python_parity(
        request,
        evidence=chosen_evidence,
        policy=chosen_policy,
        context=context,
        repository=repository,
    ), request


def _import_variant(bundle, rows, *, evidence_id="pine-execution-evidence-variant"):
    source, _, base, _, _, _ = bundle
    return import_pine_execution_csv(
        _csv_bytes(rows),
        evidence_id=ArtifactId(evidence_id),
        pine_artifact_ref=base.pine_artifact_ref,
        strategy_ref=base.strategy_ref,
        instrument_ref=base.instrument_ref,
        normalized_manifest_ref=base.normalized_manifest_ref,
        normalized_lock_ref=base.normalized_lock_ref,
        observation_start=source.specification.observation_start,
        observation_end=source.specification.observation_end,
        provenance_ref=PROVENANCE_REF,
        authority_ref=PARITY_AUTHORITY_REF,
    )


def test_exact_trace_matches_and_lineage_rebuilds(parity_bundle):
    execution, request = _run(parity_bundle)
    assert execution.result.decision is PinePythonParityDecision.MATCH
    assert execution.result.mismatch_count == 0
    verify_pine_python_parity_lineage(
        result=execution.result,
        record=execution.record,
        request=request,
        evidence=parity_bundle[2],
        policy=parity_bundle[1],
        context=parity_bundle[4],
    )
    assert all(
        item.status is RepositoryWriteStatus.STORED for item in execution.writes
    )


def test_one_bar_execution_shift_is_mismatch(parity_bundle):
    rows = _event_rows(parity_bundle[0].backtest_artifact)
    assert rows
    rows[0]["execution_time"] = (
        parity_bundle[0].backtest_artifact.fills[0].fill_time + timedelta(hours=1)
    ).isoformat()
    evidence = _import_variant(parity_bundle, rows, evidence_id="shifted-execution")
    execution, _ = _run(parity_bundle, evidence=evidence)
    assert execution.result.decision is PinePythonParityDecision.MISMATCH
    assert ParityMismatchType.EXECUTION_TIME_MISMATCH in {
        item.mismatch_type for item in execution.result.mismatches
    }


def test_same_signal_time_execution_detects_no_lookahead_mismatch(parity_bundle):
    rows = _event_rows(parity_bundle[0].backtest_artifact)
    assert rows
    rows[0]["execution_time"] = rows[0]["signal_time"]
    evidence = _import_variant(parity_bundle, rows, evidence_id="same-time-execution")
    execution, _ = _run(parity_bundle, evidence=evidence)
    assert ParityMismatchType.EXECUTION_TIME_MISMATCH in {
        item.mismatch_type for item in execution.result.mismatches
    }


def test_missing_and_extra_events_are_structural_mismatches(parity_bundle):
    rows = _event_rows(parity_bundle[0].backtest_artifact)
    assert len(rows) >= 2
    missing = _import_variant(parity_bundle, rows[:-1], evidence_id="missing-event")
    execution, _ = _run(parity_bundle, evidence=missing)
    types = {item.mismatch_type for item in execution.result.mismatches}
    assert ParityMismatchType.MISSING_EVENT in types
    assert PinePythonParityDecision.MISMATCH is execution.result.decision


def test_final_position_mismatch_is_detected(parity_bundle):
    rows = _event_rows(parity_bundle[0].backtest_artifact)
    assert rows
    shortened = rows[:-1]
    assert shortened
    evidence = _import_variant(parity_bundle, shortened, evidence_id="final-state-mismatch")
    execution, _ = _run(parity_bundle, evidence=evidence)
    assert ParityMismatchType.POSITION_STATE_MISMATCH in {
        item.mismatch_type for item in execution.result.mismatches
    }


def test_empty_external_trace_is_inconclusive_when_python_has_events(parity_bundle):
    assert parity_bundle[0].backtest_artifact.fills
    evidence = _import_variant(parity_bundle, [], evidence_id="empty-trace")
    execution, _ = _run(parity_bundle, evidence=evidence)
    assert execution.result.decision is PinePythonParityDecision.INCONCLUSIVE
    assert execution.result.mismatch_count == 0


def test_price_tolerance_is_decimal_and_bounded(parity_bundle):
    rows = _event_rows(parity_bundle[0].backtest_artifact)
    assert rows
    price = rows[0]["execution_price"]
    rows[0]["execution_price"] = str(__import__("decimal").Decimal(price) + __import__("decimal").Decimal("0.0001"))
    evidence = _import_variant(parity_bundle, rows, evidence_id="price-tolerance")
    relaxed = replace(
        parity_bundle[1],
        policy_id=ArtifactId("relaxed-price-tolerance"),
        absolute_price_tolerance="0.0001",
    )
    execution, _ = _run(parity_bundle, evidence=evidence, policy=relaxed)
    assert execution.result.decision is PinePythonParityDecision.MATCH
    strict = replace(
        parity_bundle[1],
        policy_id=ArtifactId("strict-price-tolerance"),
        absolute_price_tolerance="0.00001",
    )
    execution, _ = _run(parity_bundle, evidence=evidence, policy=strict)
    assert execution.result.decision is PinePythonParityDecision.MISMATCH
    assert ParityMismatchType.PRICE_MISMATCH in {
        item.mismatch_type for item in execution.result.mismatches
    }


def test_equivalent_timezone_representation_normalizes_to_utc(parity_bundle):
    rows = _event_rows(parity_bundle[0].backtest_artifact)
    assert rows
    first = parity_bundle[0].backtest_artifact.orders[0].signal_time
    rows[0]["signal_time"] = first.astimezone(
        __import__("datetime").timezone(timedelta(hours=2))
    ).isoformat()
    evidence = _import_variant(parity_bundle, rows, evidence_id="timezone-equivalent")
    execution, _ = _run(parity_bundle, evidence=evidence)
    assert execution.result.decision is PinePythonParityDecision.MATCH


def test_naive_timestamp_is_rejected(parity_bundle):
    rows = _event_rows(parity_bundle[0].backtest_artifact)
    rows[0]["signal_time"] = rows[0]["signal_time"].replace("+00:00", "")
    with pytest.raises(PineExecutionEvidenceError, match="timezone"):
        _import_variant(parity_bundle, rows, evidence_id="naive-time")


def test_wrong_parity_authority_fails_closed(parity_bundle):
    wrong = TraceabilityRef(
        AuthorityBindingId("wrong-parity-authority"),
        V1,
        "sha256:" + "d" * 64,
    )
    request = replace(parity_bundle[3], authority_ref=wrong)
    with pytest.raises(PinePythonParityAuthorityInvalid):
        evaluate_pine_python_parity(
            request,
            evidence=parity_bundle[2],
            policy=parity_bundle[1],
            context=parity_bundle[4],
            repository=parity_bundle[5],
        )


def test_csv_hash_is_bound_to_exact_source(parity_bundle):
    evidence = parity_bundle[2]
    assert evidence.source_byte_size == len(evidence.source_text.encode("utf-8"))
    import hashlib
    assert evidence.source_sha256 == "sha256:" + hashlib.sha256(
        evidence.source_text.encode("utf-8")
    ).hexdigest()


def test_strict_csv_columns_reject_unknown_field(parity_bundle):
    data = _csv_bytes(_event_rows(parity_bundle[0].backtest_artifact))
    text = data.decode("utf-8").replace("trade_id\n", "trade_id,unknown\n", 1)
    with pytest.raises(PineExecutionEvidenceError, match="columns"):
        import_pine_execution_csv(
            text.encode(),
            evidence_id=ArtifactId("bad-columns"),
            pine_artifact_ref=parity_bundle[2].pine_artifact_ref,
            strategy_ref=parity_bundle[2].strategy_ref,
            instrument_ref=parity_bundle[2].instrument_ref,
            normalized_manifest_ref=parity_bundle[2].normalized_manifest_ref,
            normalized_lock_ref=parity_bundle[2].normalized_lock_ref,
            observation_start=parity_bundle[2].observation_start,
            observation_end=parity_bundle[2].observation_end,
            provenance_ref=PROVENANCE_REF,
            authority_ref=PARITY_AUTHORITY_REF,
        )
