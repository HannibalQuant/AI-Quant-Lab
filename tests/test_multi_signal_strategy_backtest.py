"""Sprint 25 governed multi-signal Python backtest runtime tests."""

from __future__ import annotations

import ast
import inspect
from dataclasses import replace
from datetime import UTC, datetime, timedelta
from decimal import Decimal
from pathlib import Path

import pytest
from test_strategy_backtest import (
    authorized_context,
    strategy_configuration,
)

from ai_quant_lab import EXE_01
from ai_quant_lab.core import multi_signal_runtime as runtime_module
from ai_quant_lab.core.experiment_authorization import (
    ExperimentAuthorizationRequest,
    authorize_experiment,
)
from ai_quant_lab.core.experiment_contracts import ExperimentAuthorizationDecision
from ai_quant_lab.core.experiment_runner import ExperimentRunRequest
from ai_quant_lab.core.integrity import fingerprint_record
from ai_quant_lab.core.model import (
    AgentId,
    ArtifactId,
    ExecutionState,
    ExperimentId,
    ObjectVersion,
    ProvenanceId,
    RunId,
    TraceabilityRef,
)
from ai_quant_lab.core.multi_signal_runtime import (
    build_multi_signal_indicators,
    multi_signal_direction,
)
from ai_quant_lab.core.research_eligibility_contracts import DeploymentAuthorizationStatus
from ai_quant_lab.core.strategy_backtest import (
    AccountingMismatch,
    BacktestLineageMismatch,
    StrategyBacktestRunRequest,
    multi_signal_strategy_backtest_engine_ref,
    multi_signal_strategy_backtest_replay_contract,
    run_authorized_strategy_backtest,
    verify_strategy_backtest_lineage,
)
from ai_quant_lab.core.strategy_backtest_contracts import (
    MultiSignalTrendParameters,
    SidePermission,
    SignalTiming,
    SimulatedExecutionTiming,
    SimulatedOrderSide,
    SimulatedPositionState,
    StrategyDefinition,
    StrategyModel,
)
from test_real_csv_onboarding import HEADER

V1 = ObjectVersion(1)
V2 = ObjectVersion(2)
COMPLETED_AT = datetime(2025, 2, 3, 1, tzinfo=UTC)
PROVENANCE_REF = TraceabilityRef(
    ProvenanceId("sprint-25-multi-signal-backtest"),
    V1,
    "sha256:" + "c" * 64,
)


def parameters(
    *,
    atr_stop_mult: str = "100",
    take_profit_r: str = "100",
    break_even_trigger_r: str = "100",
    time_stop_bars: int = 100,
) -> MultiSignalTrendParameters:
    return MultiSignalTrendParameters(
        2,
        3,
        4,
        2,
        "55",
        "45",
        2,
        4,
        2,
        2,
        "5",
        2,
        atr_stop_mult,
        take_profit_r,
        break_even_trigger_r,
        time_stop_bars,
    )


def strategy(
    *,
    params: MultiSignalTrendParameters | None = None,
) -> StrategyDefinition:
    return StrategyDefinition(
        ArtifactId("solusdt-4h-multi-signal-runtime-v1"),
        V2,
        StrategyModel.MULTI_SIGNAL_TREND_LONG_SHORT,
        SignalTiming.BAR_CLOSE_AFTER_AVAILABILITY,
        SimulatedExecutionTiming.FIRST_ELIGIBLE_NEXT_BAR_OPEN,
        SidePermission.LONG_SHORT,
        0,
        10_000,
        "USD",
        100,
        False,
        False,
        multi_signal_strategy_backtest_engine_ref(),
        TraceabilityRef(
            ProvenanceId("sprint-25-strategy-definition"),
            V1,
            "sha256:" + "d" * 64,
        ),
        V2,
        parameters() if params is None else params,
    )


def _trend_csv() -> str:
    closes = (
        101,
        103,
        105,
        107,
        109,
        111,
        113,
        111,
        109,
        107,
        105,
        103,
        101,
        99,
        101,
        103,
        105,
        107,
        109,
        111,
        113,
        113,
        113,
    )
    rows: list[str] = []
    prior = 100
    start = datetime(2025, 2, 1, tzinfo=UTC)
    for index, close in enumerate(closes):
        opened = start + timedelta(hours=index)
        closed = opened + timedelta(hours=1)
        availability = closed + timedelta(seconds=5)
        high = max(prior, close) + 1
        low = min(prior, close) - 1
        rows.append(
            f"{opened.strftime('%Y-%m-%dT%H:%M:%S.000000Z')},"
            f"{closed.strftime('%Y-%m-%dT%H:%M:%S.000000Z')},"
            f"{prior},{high},{low},{close},{100 + index},final,"
            f"{availability.strftime('%Y-%m-%dT%H:%M:%S.000000Z')}\n"
        )
        prior = close
    return HEADER + "".join(rows)


def _multi_context(
    tmp_path: Path,
    *,
    params: MultiSignalTrendParameters | None = None,
) -> tuple[object, ...]:
    base = authorized_context(
        tmp_path,
        suffix="sprint-25-multi",
        csv_text=_trend_csv(),
    )
    (
        declaration,
        repository,
        admission,
        report,
        eligibility_policy,
        eligibility,
        _legacy_strategy,
        legacy_specification,
        legacy_policy,
        _legacy_authorization,
        instrument,
    ) = base
    definition = strategy(params=params)
    engine = multi_signal_strategy_backtest_replay_contract()
    engine_ref = multi_signal_strategy_backtest_engine_ref()
    specification = replace(
        legacy_specification,
        experiment_id=ExperimentId("sprint-25-multi-signal-experiment"),
        research_objective=(
            "Exercise deterministic EMA/RSI/MACD/ADX long-short timing and risk controls."
        ),
        configuration=strategy_configuration(definition),
        observation_start=report.normalized_bars[0].bar_open,
        observation_end=report.normalized_bars[-1].bar_close,
        knowledge_cutoff=datetime(2025, 2, 2, tzinfo=UTC),
        engine_contract_ref=engine_ref,
    )
    policy = replace(
        legacy_policy,
        policy_id=ArtifactId("sprint-25-multi-signal-authorization-policy"),
        supported_engine_refs=(engine_ref,),
    )
    authorization = authorize_experiment(
        ExperimentAuthorizationRequest(
            ArtifactId("sprint-25-multi-signal-authorization"),
            specification,
            policy,
            datetime(2025, 2, 3, tzinfo=UTC),
            AgentId("experiment-authorizer"),
        ),
        eligibility=eligibility,
        eligibility_policy=eligibility_policy,
        admission=admission,
        declaration=declaration,
        report=report,
        repository=repository,
    )
    request = StrategyBacktestRunRequest(
        ExperimentRunRequest(
            RunId("sprint-25-multi-signal-backtest-run"),
            ArtifactId("sprint-25-multi-signal-backtest-result"),
            TraceabilityRef(
                authorization.record.authorization_id,
                authorization.record.version,
                fingerprint_record(authorization.record),
            ),
            TraceabilityRef(
                specification.experiment_id,
                specification.version,
                fingerprint_record(specification),
            ),
            TraceabilityRef(
                policy.policy_id,
                policy.version,
                fingerprint_record(policy),
            ),
            TraceabilityRef(
                eligibility.eligibility_id,
                eligibility.version,
                fingerprint_record(eligibility),
            ),
            engine_ref,
            COMPLETED_AT,
            PROVENANCE_REF,
        ),
        TraceabilityRef(
            definition.strategy_id,
            definition.version,
            fingerprint_record(definition),
        ),
    )
    return (
        declaration,
        repository,
        admission,
        report,
        eligibility_policy,
        eligibility,
        definition,
        specification,
        policy,
        authorization,
        instrument,
        engine,
        request,
    )


def _execute(context: tuple[object, ...]):
    (
        declaration,
        repository,
        admission,
        report,
        eligibility_policy,
        eligibility,
        definition,
        specification,
        policy,
        authorization,
        instrument,
        engine,
        request,
    ) = context
    assert authorization.record.status is ExperimentAuthorizationDecision.AUTHORIZED
    return run_authorized_strategy_backtest(
        request,
        authorization=authorization.record,
        specification=specification,
        policy=policy,
        eligibility=eligibility,
        eligibility_policy=eligibility_policy,
        admission=admission,
        declaration=declaration,
        report=report,
        engine_contract=engine,
        strategy=definition,
        instrument=instrument,
        repository=repository,
    )


def test_indicator_state_is_deterministic_and_emits_both_directions(tmp_path: Path) -> None:
    context = _multi_context(tmp_path)
    report = context[3]
    definition = context[6]
    points_a = build_multi_signal_indicators(
        report.normalized_bars,
        definition.multi_signal,
    )
    points_b = build_multi_signal_indicators(
        report.normalized_bars,
        definition.multi_signal,
    )

    assert points_a == points_b
    directions = tuple(
        multi_signal_direction(bar, point, definition.multi_signal)
        for bar, point in zip(report.normalized_bars, points_a, strict=True)
    )
    assert SimulatedPositionState.LONG in directions
    assert SimulatedPositionState.SHORT in directions
    assert all(point.atr is None or point.atr >= 0 for point in points_a)


def test_governed_backtest_executes_completed_long_and_short_cycles(tmp_path: Path) -> None:
    context = _multi_context(tmp_path)
    result = _execute(context)
    artifact = result.artifact
    fills = {fill.fill_id: fill for fill in artifact.fills}

    completed_sides = tuple(
        (fills[trade.entry_fill_id].side, fills[trade.exit_fill_id].side)
        for trade in artifact.trades
    )
    assert (SimulatedOrderSide.BUY, SimulatedOrderSide.SELL) in completed_sides
    assert (SimulatedOrderSide.SELL, SimulatedOrderSide.BUY) in completed_sides
    assert any(point.position_quantity.startswith("-") for point in artifact.equity_curve)
    assert all(
        order.signal_time < fill.fill_time
        for order, fill in zip(artifact.orders, artifact.fills, strict=True)
    )
    assert artifact.deployment_authorization is DeploymentAuthorizationStatus.NOT_AUTHORIZED
    assert artifact.execution_state is ExecutionState.PLANNED_CLOSED
    assert EXE_01.state is ExecutionState.PLANNED_CLOSED


def test_short_accounting_uses_signed_position_value_and_exact_cash_identity(
    tmp_path: Path,
) -> None:
    result = _execute(_multi_context(tmp_path))
    short_points = [
        point
        for point in result.artifact.equity_curve
        if Decimal(point.position_quantity) < 0
    ]
    assert short_points
    for point in short_points:
        assert Decimal(point.position_value) < 0
        assert Decimal(point.equity) == Decimal(point.cash) + Decimal(point.position_value)


def test_multi_signal_result_is_deterministic_and_exactly_verifiable(tmp_path: Path) -> None:
    context = _multi_context(tmp_path)
    first = _execute(context)
    second = _execute(context)
    assert first.artifact == second.artifact
    assert first.record == second.record

    (
        _declaration,
        _repository,
        _admission,
        report,
        _eligibility_policy,
        eligibility,
        definition,
        specification,
        policy,
        authorization,
        instrument,
        engine,
        request,
    ) = context
    verify_strategy_backtest_lineage(
        record=first.record,
        artifact=first.artifact,
        request=request,
        authorization=authorization.record,
        specification=specification,
        policy=policy,
        eligibility=eligibility,
        engine_contract=engine,
        strategy=definition,
        instrument=instrument,
        report=report,
    )


def test_tampered_short_equity_fails_independent_accounting(tmp_path: Path) -> None:
    context = _multi_context(tmp_path)
    result = _execute(context)
    artifact = result.artifact
    short_index = next(
        index
        for index, point in enumerate(artifact.equity_curve)
        if Decimal(point.position_quantity) < 0
    )
    changed_points = list(artifact.equity_curve)
    changed_points[short_index] = replace(
        changed_points[short_index],
        position_value="0",
        equity=changed_points[short_index].cash,
    )
    changed = replace(artifact, equity_curve=tuple(changed_points))

    (
        _declaration,
        _repository,
        _admission,
        report,
        _eligibility_policy,
        eligibility,
        definition,
        specification,
        policy,
        authorization,
        instrument,
        engine,
        request,
    ) = context
    with pytest.raises((AccountingMismatch, BacktestLineageMismatch)):
        verify_strategy_backtest_lineage(
            record=result.record,
            artifact=changed,
            request=request,
            authorization=authorization.record,
            specification=specification,
            policy=policy,
            eligibility=eligibility,
            engine_contract=engine,
            strategy=definition,
            instrument=instrument,
            report=report,
        )


def test_wrong_engine_profile_fails_closed(tmp_path: Path) -> None:
    context = _multi_context(tmp_path)
    changed = list(context)
    from ai_quant_lab.core.strategy_backtest import strategy_backtest_replay_contract

    changed[11] = strategy_backtest_replay_contract()
    with pytest.raises(ValueError, match="engine"):
        _execute(tuple(changed))


def test_multi_signal_runtime_has_no_optimizer_network_or_live_execution_capability() -> None:
    tree = ast.parse(inspect.getsource(runtime_module))
    imported = {
        alias.name.split(".")[0]
        for node in ast.walk(tree)
        if isinstance(node, (ast.Import, ast.ImportFrom))
        for alias in node.names
    }
    assert not imported.intersection(
        {
            "aiohttp",
            "ccxt",
            "httpx",
            "importlib",
            "optuna",
            "requests",
            "socket",
            "subprocess",
            "urllib",
        }
    )
    calls = {
        node.func.id
        for node in ast.walk(tree)
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
    }
    assert not calls.intersection({"eval", "exec"})
