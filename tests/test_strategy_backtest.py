"""Sprint 12 controlled deterministic strategy backtest tests."""

from __future__ import annotations

import ast
import inspect
import json
from collections.abc import Callable
from dataclasses import replace
from datetime import UTC, datetime
from decimal import ROUND_HALF_EVEN, Context, Decimal, localcontext
from pathlib import Path

import pytest
from test_experiment_runner import exact, signed_authorized_context
from test_real_csv_onboarding import CLOCK, HEADER
from test_real_csv_onboarding import context as real_csv_context
from test_research_dataset_eligibility import (
    eligibility_request,
)
from test_research_dataset_eligibility import (
    policy as eligibility_policy_contract,
)

from ai_quant_lab import EXE_01
from ai_quant_lab.core import strategy_backtest as backtest_module
from ai_quant_lab.core.codec import decode, encode
from ai_quant_lab.core.csv_import import CsvImportReport
from ai_quant_lab.core.data import InstrumentClass, InstrumentId, InstrumentIdentity
from ai_quant_lab.core.dataset_store import (
    LocalDatasetRepository,
    RepositoryIntegrityFailure,
    RepositoryTypeMismatch,
    RepositoryWriteStatus,
    repository_key,
)
from ai_quant_lab.core.experiment_authorization import (
    ExperimentAuthorizationRequest,
    ExperimentAuthorizationResult,
    authorize_experiment,
)
from ai_quant_lab.core.experiment_contracts import (
    CostSemantics,
    ExperimentAuthorizationDecision,
    ExperimentAuthorizationPolicy,
    ExperimentFamily,
    ExperimentSpecification,
    NoLookaheadSemantics,
    PositionSizingSemantics,
)
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
from ai_quant_lab.core.real_csv_contracts import RealCsvAdmissionRecord, RealCsvSourceDeclaration
from ai_quant_lab.core.real_csv_onboarding import onboard_real_csv
from ai_quant_lab.core.research_eligibility import evaluate_research_dataset_eligibility
from ai_quant_lab.core.research_eligibility_contracts import (
    DeploymentAuthorizationStatus,
    EligibilityCalendarSemantics,
    ResearchDatasetEligibilityPolicy,
    ResearchDatasetEligibilityRecord,
    ValidationStatus,
)
from ai_quant_lab.core.strategy_backtest import (
    BacktestLineageMismatch,
    InvalidExecutionPrice,
    MissingNextBar,
    StrategyBacktestResult,
    StrategyBacktestRunRequest,
    UnsupportedCapitalDenomination,
    UnsupportedFunding,
    UnsupportedSizing,
    UnsupportedStrategy,
    run_authorized_strategy_backtest,
    strategy_backtest_engine_ref,
    strategy_backtest_replay_contract,
    verify_strategy_backtest_lineage,
)
from ai_quant_lab.core.strategy_backtest_contracts import (
    BacktestResultArtifact,
    BacktestRunRecord,
    BacktestRunStatus,
    SidePermission,
    SignalTiming,
    SimulatedExecutionTiming,
    SimulatedOrderSide,
    SimulatedPositionState,
    StrategyBacktestContractError,
    StrategyDefinition,
    StrategyModel,
)

V1 = ObjectVersion(1)
DECISION_TIME = datetime(2025, 2, 3, tzinfo=UTC)
COMPLETED_AT = datetime(2025, 2, 3, 1, tzinfo=UTC)
PROVENANCE_REF = TraceabilityRef(
    ProvenanceId("strategy-backtest-run-provenance"), V1, "sha256:" + "8" * 64
)

type BacktestContext = tuple[
    RealCsvSourceDeclaration,
    LocalDatasetRepository,
    RealCsvAdmissionRecord,
    CsvImportReport,
    ResearchDatasetEligibilityPolicy,
    ResearchDatasetEligibilityRecord,
    StrategyDefinition,
    ExperimentSpecification,
    ExperimentAuthorizationPolicy,
    ExperimentAuthorizationResult,
    InstrumentIdentity,
]


def strategy(
    *, fixed_notional_minor: int = 10_000, capital_currency: str = "USD"
) -> StrategyDefinition:
    return StrategyDefinition(
        ArtifactId("close-vs-open-long-only-v1"),
        V1,
        StrategyModel.CLOSE_VS_OPEN_LONG_ONLY,
        SignalTiming.BAR_CLOSE_AFTER_AVAILABILITY,
        SimulatedExecutionTiming.FIRST_ELIGIBLE_NEXT_BAR_OPEN,
        SidePermission.LONG_ONLY,
        0,
        fixed_notional_minor,
        capital_currency,
        100,
        False,
        False,
        strategy_backtest_engine_ref(),
        TraceabilityRef(ProvenanceId("strategy-definition-provenance"), V1, "sha256:" + "7" * 64),
        V1,
    )


def strategy_configuration(definition: StrategyDefinition) -> tuple[tuple[str, str], ...]:
    return tuple(
        sorted(
            (
                ("capital_currency", definition.capital_currency),
                ("capital_minor_unit_scale", str(definition.capital_minor_unit_scale)),
                ("fixed_notional_minor", str(definition.fixed_notional_minor)),
                ("strategy_fingerprint", fingerprint_record(definition)),
                ("strategy_id", str(definition.strategy_id)),
                ("strategy_model", definition.model.value),
            )
        )
    )


def specification(
    eligibility: ResearchDatasetEligibilityRecord,
    definition: StrategyDefinition,
    *,
    commission: CostSemantics = CostSemantics.DECLARED_BPS,
    slippage: CostSemantics = CostSemantics.DECLARED_BPS,
    funding: CostSemantics = CostSemantics.NOT_APPLICABLE,
    sizing: PositionSizingSemantics = PositionSizingSemantics.FIXED_NOTIONAL,
    capital_minor: int = 100_000,
) -> ExperimentSpecification:
    assert eligibility.normalized_manifest_ref is not None
    assert eligibility.normalized_lock_ref is not None
    return ExperimentSpecification(
        ExperimentId("controlled-long-only-backtest"),
        V1,
        exact(eligibility, eligibility.eligibility_id, eligibility.version),
        eligibility.normalized_manifest_ref,
        eligibility.normalized_lock_ref,
        ExperimentFamily.STRATEGY_BACKTEST,
        "Exercise deterministic timing, fills, accounting and lineage without validating edge.",
        ArtifactId("synthetic-backtest-architecture-hypothesis"),
        strategy_configuration(definition),
        42,
        datetime(2025, 2, 1, tzinfo=UTC),
        datetime(2025, 2, 1, 6, tzinfo=UTC),
        datetime(2025, 2, 2, tzinfo=UTC),
        NoLookaheadSemantics.EXPLICIT_EVENT_AVAILABILITY_NEXT_EVENT,
        0,
        commission,
        10 if commission is CostSemantics.DECLARED_BPS else 0,
        slippage,
        5 if slippage is CostSemantics.DECLARED_BPS else 0,
        funding,
        0,
        EligibilityCalendarSemantics.FIXED_UTC_CONTINUOUS,
        sizing,
        capital_minor,
        strategy_backtest_engine_ref(),
        ("gross_pnl", "max_drawdown", "net_pnl", "total_return", "trade_count"),
        ("equity_curve", "simulated_fills", "simulated_orders", "simulated_trades"),
        AgentId("strategy-backtest-proposer"),
        TraceabilityRef(ProvenanceId("strategy-backtest-specification"), V1, "sha256:" + "6" * 64),
        V1,
    )


def authorization_policy() -> ExperimentAuthorizationPolicy:
    return ExperimentAuthorizationPolicy(
        ArtifactId("strategy-backtest-authorization-policy"),
        V1,
        (ExperimentFamily.STRATEGY_BACKTEST,),
        NoLookaheadSemantics.EXPLICIT_EVENT_AVAILABILITY_NEXT_EVENT,
        (EligibilityCalendarSemantics.FIXED_UTC_CONTINUOUS,),
        True,
        True,
        False,
        True,
        365,
        0,
        2**31,
        (strategy_backtest_engine_ref(),),
        False,
        AgentId("experiment-governance-owner"),
        V1,
    )


def _six_bar_csv() -> str:
    values = ((100, 101), (101, 102), (102, 103), (103, 102), (102, 101), (101, 100))
    rows = []
    for index, (open_price, close_price) in enumerate(values):
        rows.append(
            f"2025-02-01T{index:02d}:00:00.000000Z,"
            f"2025-02-01T{index + 1:02d}:00:00.000000Z,"
            f"{open_price},{max(open_price, close_price) + 1},{min(open_price, close_price) - 1},"
            f"{close_price},{10 + index},final,"
            f"2025-02-01T{index + 1:02d}:00:05.000000Z\n"
        )
    return HEADER + "".join(rows)


def authorized_context(
    tmp_path: Path,
    *,
    suffix: str = "backtest",
    spec_mutator: Callable[[ExperimentSpecification], ExperimentSpecification] | None = None,
    capital_currency: str = "USD",
    quote_asset: str | None = "USD",
    csv_text: str | None = None,
) -> BacktestContext:
    csv_path = tmp_path / f"strategy-{suffix}.csv"
    csv_path.write_text(_six_bar_csv() if csv_text is None else csv_text, encoding="utf-8")
    onboarding, source, instrument, schema, timeframe, repository = real_csv_context(
        tmp_path, path=csv_path, allowed_root=tmp_path, suffix=suffix
    )
    instrument = replace(instrument, quote_asset=quote_asset)
    instrument_ref = exact(instrument, instrument.instrument_id, instrument.version)
    declaration = replace(onboarding.declaration, instrument_ref=instrument_ref)
    declaration_ref = exact(declaration, declaration.provenance_id, declaration.version)
    ingestion = replace(
        onboarding.csv_request.ingestion,
        instrument_ref=instrument_ref,
        observation_provenance_ref=declaration_ref,
        manifest_provenance_ref=declaration_ref,
        lock_provenance_ref=declaration_ref,
    )
    onboarding = replace(
        onboarding,
        declaration=declaration,
        csv_request=replace(
            onboarding.csv_request,
            ingestion=ingestion,
            normalization_provenance_ref=declaration_ref,
            normalized_provenance_ref=declaration_ref,
        ),
    )
    admitted = onboard_real_csv(
        onboarding,
        source=source,
        instrument=instrument,
        schema=schema,
        timeframe=timeframe,
        clock=CLOCK,
        repository=repository,
    )
    assert admitted.report is not None
    eligibility_policy = eligibility_policy_contract()
    eligibility = evaluate_research_dataset_eligibility(
        eligibility_request(
            onboarding.declaration,
            admitted.admission,
            eligibility_policy,
            admitted.report,
            eligibility_id=f"research-dataset-eligibility-{suffix}",
        ),
        admission=admitted.admission,
        declaration=onboarding.declaration,
        report=admitted.report,
        repository=repository,
    ).record
    definition = strategy(capital_currency=capital_currency)
    spec = specification(eligibility, definition)
    if spec_mutator is not None:
        spec = spec_mutator(spec)
    policy = authorization_policy()
    authorization = authorize_experiment(
        ExperimentAuthorizationRequest(
            ArtifactId("strategy-backtest-authorization"),
            spec,
            policy,
            DECISION_TIME,
            AgentId("experiment-authorizer"),
        ),
        eligibility=eligibility,
        eligibility_policy=eligibility_policy,
        admission=admitted.admission,
        declaration=onboarding.declaration,
        report=admitted.report,
        repository=repository,
    )
    return (
        onboarding.declaration,
        repository,
        admitted.admission,
        admitted.report,
        eligibility_policy,
        eligibility,
        definition,
        spec,
        policy,
        authorization,
        instrument,
    )


def request_for(context: BacktestContext) -> StrategyBacktestRunRequest:
    _, _, _, _, _, eligibility, definition, spec, policy, authorization, _ = context
    engine = strategy_backtest_replay_contract()
    return StrategyBacktestRunRequest(
        ExperimentRunRequest(
            RunId("deterministic-strategy-backtest-run"),
            ArtifactId("deterministic-strategy-backtest-result"),
            exact(authorization.record, authorization.record.authorization_id, V1),
            exact(spec, spec.experiment_id, spec.version),
            exact(policy, policy.policy_id, policy.version),
            exact(eligibility, eligibility.eligibility_id, eligibility.version),
            exact(engine, engine.engine_id, engine.version),
            COMPLETED_AT,
            PROVENANCE_REF,
        ),
        exact(definition, definition.strategy_id, definition.version),
    )


def execute_context(
    context: BacktestContext,
) -> tuple[StrategyBacktestRunRequest, StrategyBacktestResult]:
    (
        declaration,
        repository,
        admission,
        report,
        eligibility_policy,
        eligibility,
        definition,
        spec,
        policy,
        authorization,
        instrument,
    ) = context
    assert authorization.record.status is ExperimentAuthorizationDecision.AUTHORIZED
    request = request_for(context)
    result = run_authorized_strategy_backtest(
        request,
        authorization=authorization.record,
        specification=spec,
        policy=policy,
        eligibility=eligibility,
        eligibility_policy=eligibility_policy,
        admission=admission,
        declaration=declaration,
        report=report,
        engine_contract=strategy_backtest_replay_contract(),
        strategy=definition,
        instrument=instrument,
        repository=repository,
    )
    return request, result


def test_authorized_strategy_backtest_runs_with_exact_next_event_timing(tmp_path: Path) -> None:
    context = authorized_context(tmp_path)
    assert context[6].capital_currency == context[10].quote_asset == "USD"
    _, result = execute_context(context)
    artifact = result.artifact
    assert result.record.status is BacktestRunStatus.COMPLETED
    assert len(artifact.orders) == len(artifact.fills) == 2
    assert artifact.trade_count == len(artifact.trades) == 1
    assert [order.side for order in artifact.orders] == [
        SimulatedOrderSide.BUY,
        SimulatedOrderSide.SELL,
    ]
    assert all(
        order.signal_time <= fill.fill_time
        for order, fill in zip(artifact.orders, artifact.fills, strict=True)
    )
    assert artifact.orders[0].signal_time != artifact.fills[0].fill_time
    assert artifact.open_position is SimulatedPositionState.FLAT
    assert artifact.validation_status is ValidationStatus.NOT_VALIDATED
    assert artifact.deployment_authorization is DeploymentAuthorizationStatus.NOT_AUTHORIZED
    assert artifact.execution_state is ExecutionState.PLANNED_CLOSED
    assert EXE_01.state is ExecutionState.PLANNED_CLOSED


def test_capital_denomination_mismatch_fails_before_result_persistence(
    tmp_path: Path,
) -> None:
    context = authorized_context(
        tmp_path,
        suffix="capital-mismatch",
        capital_currency="USDT",
        quote_asset="USD",
    )
    with pytest.raises(
        UnsupportedCapitalDenomination,
        match="strategy capital currency must equal governed instrument quote asset",
    ):
        execute_context(context)
    objects = context[1].root / "objects"
    assert not (objects / "backtest-result-artifact").exists()
    assert not (objects / "backtest-run-record").exists()


def test_missing_instrument_quote_asset_fails_closed(tmp_path: Path) -> None:
    context = authorized_context(
        tmp_path,
        suffix="missing-quote",
        capital_currency="USD",
        quote_asset=None,
    )
    with pytest.raises(
        UnsupportedCapitalDenomination,
        match="instrument quote asset is required for strategy backtest capital denomination",
    ):
        execute_context(context)


def test_unrelated_instrument_cannot_satisfy_capital_denomination(tmp_path: Path) -> None:
    context = authorized_context(tmp_path, suffix="wrong-instrument")
    unrelated = replace(context[10], symbol="OTHERUSD", quote_asset="USD")
    with pytest.raises(
        BacktestLineageMismatch,
        match="instrument does not match exact source declaration",
    ):
        execute_context((*context[:10], unrelated))


def test_accounting_costs_metrics_and_equity_identity_are_exact(tmp_path: Path) -> None:
    _, result = execute_context(authorized_context(tmp_path, suffix="accounting"))
    artifact = result.artifact
    assert artifact.initial_capital == "1000"
    assert artifact.trade_count == 1
    assert artifact.trades[0].commission != "0"
    assert artifact.trades[0].slippage_cost != "0"
    assert artifact.final_equity == artifact.final_cash
    assert artifact.net_pnl == artifact.trades[0].net_pnl
    assert artifact.gross_pnl == artifact.trades[0].gross_pnl
    with localcontext(Context(prec=34, rounding=ROUND_HALF_EVEN)):
        assert Decimal(artifact.total_return) == (
            Decimal(artifact.final_equity) / Decimal(artifact.initial_capital) - Decimal(1)
        )
    for point in artifact.equity_curve:
        assert float(point.equity) == pytest.approx(float(point.cash) + float(point.position_value))
    assert float(artifact.max_drawdown) >= 0


def test_commission_and_buy_sell_slippage_formulas_are_exact(tmp_path: Path) -> None:
    _, result = execute_context(authorized_context(tmp_path, suffix="cost-formulas"))
    buy, sell = result.artifact.fills
    with localcontext(Context(prec=34, rounding=ROUND_HALF_EVEN)):
        assert Decimal(buy.execution_price) == Decimal(buy.reference_price) * (
            Decimal(1) + Decimal(5) / Decimal(10_000)
        )
        assert Decimal(sell.execution_price) == Decimal(sell.reference_price) * (
            Decimal(1) - Decimal(5) / Decimal(10_000)
        )
        assert Decimal(buy.commission) == Decimal(buy.fill_notional) * Decimal(10) / Decimal(10_000)
        assert Decimal(sell.commission) == Decimal(sell.fill_notional) * Decimal(10) / Decimal(
            10_000
        )


def test_no_fill_occurs_outside_authorized_window(tmp_path: Path) -> None:
    context = authorized_context(tmp_path, suffix="window")
    _, result = execute_context(context)
    spec = context[7]
    assert all(
        spec.observation_start <= fill.fill_time < spec.observation_end
        for fill in result.artifact.fills
    )
    assert all(
        spec.observation_start <= point.event_time <= spec.knowledge_cutoff
        for point in result.artifact.equity_curve
    )


def test_terminal_transition_without_eligible_next_bar_fails_closed(tmp_path: Path) -> None:
    context = authorized_context(
        tmp_path,
        suffix="missing-next",
        spec_mutator=lambda spec: replace(
            spec, observation_end=datetime(2025, 2, 1, 5, tzinfo=UTC)
        ),
    )
    with pytest.raises(MissingNextBar, match="eligible next bar"):
        execute_context(context)


def test_zero_cost_is_distinct_from_unknown_and_bps(tmp_path: Path) -> None:
    zero = authorized_context(
        tmp_path,
        suffix="zero-cost",
        spec_mutator=lambda spec: replace(
            spec,
            commission_semantics=CostSemantics.DECLARED_ZERO,
            commission_bps=0,
            slippage_semantics=CostSemantics.DECLARED_ZERO,
            slippage_bps=0,
        ),
    )
    _, result = execute_context(zero)
    assert all(
        fill.commission == "0" and fill.slippage_cost == "0" for fill in result.artifact.fills
    )
    unknown = authorized_context(
        tmp_path,
        suffix="unknown-cost",
        spec_mutator=lambda spec: replace(
            spec, commission_semantics=CostSemantics.UNKNOWN, commission_bps=0
        ),
    )
    assert unknown[9].record.status is not ExperimentAuthorizationDecision.AUTHORIZED


@pytest.mark.parametrize(
    ("mutator", "error"),
    [
        (
            lambda spec: replace(spec, funding_semantics=CostSemantics.DECLARED_ZERO),
            UnsupportedFunding,
        ),
        (
            lambda spec: replace(spec, sizing_semantics=PositionSizingSemantics.FIXED_QUANTITY),
            UnsupportedSizing,
        ),
    ],
)
def test_unsupported_funding_and_sizing_fail_closed(
    tmp_path: Path,
    mutator: Callable[[ExperimentSpecification], ExperimentSpecification],
    error: type[Exception],
) -> None:
    context = authorized_context(
        tmp_path,
        suffix=error.__name__.lower(),
        spec_mutator=mutator,
    )
    with pytest.raises(error):
        execute_context(context)


def test_wrong_strategy_fingerprint_and_configuration_fail_closed(tmp_path: Path) -> None:
    context = authorized_context(tmp_path, suffix="wrong-strategy")
    request = request_for(context)
    with pytest.raises(UnsupportedStrategy, match="exact strategy configuration"):
        execute_context((*context[:6], replace(context[6], threshold_bps=1), *context[7:]))
    with pytest.raises(StrategyBacktestContractError):
        replace(context[6], allow_pyramiding=True)
    assert request.strategy_ref.expected_fingerprint == fingerprint_record(context[6])


def test_wrong_authorization_and_engine_refs_fail_closed(tmp_path: Path) -> None:
    context = authorized_context(tmp_path, suffix="wrong-refs")
    request = request_for(context)
    bad = replace(
        request,
        experiment_run=replace(
            request.experiment_run,
            authorization_ref=TraceabilityRef(
                request.experiment_run.authorization_ref.object_id,
                V1,
                "sha256:" + "0" * 64,
            ),
        ),
    )
    (
        declaration,
        repository,
        admission,
        report,
        eligibility_policy,
        eligibility,
        definition,
        spec,
        policy,
        authorization,
        instrument,
    ) = context
    with pytest.raises(ValueError):
        run_authorized_strategy_backtest(
            bad,
            authorization=authorization.record,
            specification=spec,
            policy=policy,
            eligibility=eligibility,
            eligibility_policy=eligibility_policy,
            admission=admission,
            declaration=declaration,
            report=report,
            engine_contract=strategy_backtest_replay_contract(),
            strategy=definition,
            instrument=instrument,
            repository=repository,
        )


def test_signed_zero_or_negative_execution_prices_fail_closed(tmp_path: Path) -> None:
    market_context = signed_authorized_context(
        tmp_path, ("0", "100", "101"), suffix="invalid-price"
    )
    declaration, repository, admission, report, eligibility_policy, eligibility, _, _, _ = (
        market_context
    )
    definition = strategy()
    spec = replace(
        specification(eligibility, definition),
        observation_end=datetime(2025, 2, 1, 3, tzinfo=UTC),
    )
    policy = authorization_policy()
    authorization = authorize_experiment(
        ExperimentAuthorizationRequest(
            ArtifactId("signed-backtest-authorization"),
            spec,
            policy,
            DECISION_TIME,
            AgentId("experiment-authorizer"),
        ),
        eligibility=eligibility,
        eligibility_policy=eligibility_policy,
        admission=admission,
        declaration=declaration,
        report=report,
        repository=repository,
    )
    context: BacktestContext = (
        declaration,
        repository,
        admission,
        report,
        eligibility_policy,
        eligibility,
        definition,
        spec,
        policy,
        authorization,
        InstrumentIdentity(
            InstrumentId("external-spot-invalid-price"),
            V1,
            "EXTUSD",
            InstrumentClass.SPOT,
            "EXT",
            "USD",
            None,
            None,
            V1,
        ),
    )
    with pytest.raises(InvalidExecutionPrice):
        execute_context(context)


def test_result_is_deterministic_idempotent_and_roundtrips(tmp_path: Path) -> None:
    context = authorized_context(tmp_path, suffix="deterministic")
    request, first = execute_context(context)
    _, second = execute_context(context)
    assert first.record == second.record
    assert first.artifact == second.artifact
    assert encode(first.artifact) == encode(second.artifact)
    assert all(
        write.status is RepositoryWriteStatus.ALREADY_PRESENT_IDENTICAL for write in second.writes
    )
    assert decode(encode(context[6]), StrategyDefinition) == context[6]
    assert decode(encode(first.artifact), BacktestResultArtifact) == first.artifact
    assert decode(encode(first.record), BacktestRunRecord) == first.record
    verify_strategy_backtest_lineage(
        record=first.record,
        artifact=first.artifact,
        request=request,
        authorization=context[9].record,
        specification=context[7],
        policy=context[8],
        eligibility=context[5],
        engine_contract=strategy_backtest_replay_contract(),
        strategy=context[6],
        instrument=context[10],
        report=context[3],
    )


def test_tampered_result_values_fail_exact_lineage_reconstruction(tmp_path: Path) -> None:
    context = authorized_context(tmp_path, suffix="tampered-result")
    request, result = execute_context(context)
    with pytest.raises(BacktestLineageMismatch, match="exact deterministic replay"):
        verify_strategy_backtest_lineage(
            record=result.record,
            artifact=replace(result.artifact, run_input_fingerprint="sha256:" + "0" * 64),
            request=request,
            authorization=context[9].record,
            specification=context[7],
            policy=context[8],
            eligibility=context[5],
            engine_contract=strategy_backtest_replay_contract(),
            strategy=context[6],
            instrument=context[10],
            report=context[3],
        )


def test_invalid_capital_and_implicit_force_close_are_rejected(tmp_path: Path) -> None:
    context = authorized_context(tmp_path, suffix="invalid-contracts")
    with pytest.raises(StrategyBacktestContractError):
        replace(context[6], force_close_at_window_end=True)
    with pytest.raises(StrategyBacktestContractError):
        replace(context[6], fixed_notional_minor=0)
    invalid_capital = replace(context[7], capital_notional_minor=0)
    with pytest.raises(ValueError):
        execute_context((*context[:7], invalid_capital, *context[8:]))


def test_persistence_detects_corruption_and_wrong_type(tmp_path: Path) -> None:
    context = authorized_context(tmp_path, suffix="persistence")
    _, result = execute_context(context)
    repository = context[1]
    assert repository.load(repository_key(context[6]), StrategyDefinition).record == context[6]
    assert (
        repository.load(repository_key(result.artifact), BacktestResultArtifact).record
        == result.artifact
    )
    assert repository.load(repository_key(result.record), BacktestRunRecord).record == result.record
    with pytest.raises(RepositoryTypeMismatch):
        repository.load(repository_key(result.artifact), BacktestRunRecord)
    repository.path_for(repository_key(result.artifact)).write_bytes(b"{}")
    with pytest.raises(RepositoryIntegrityFailure):
        repository.load(repository_key(result.artifact), BacktestResultArtifact)


def test_contract_rejects_unknown_fields_and_wrong_version(tmp_path: Path) -> None:
    context = authorized_context(tmp_path, suffix="strict-codec")
    raw = json.loads(encode(context[6]))
    raw["payload"]["unknown"] = True
    from ai_quant_lab.core.model import InvalidSerialization, canonical_json

    with pytest.raises(InvalidSerialization):
        decode(canonical_json(raw).encode(), StrategyDefinition)
    with pytest.raises(StrategyBacktestContractError):
        replace(context[6], contract_version=ObjectVersion(2))


def test_strategy_engine_has_no_optimizer_network_plugin_or_live_execution() -> None:
    source = inspect.getsource(backtest_module)
    tree = ast.parse(source)
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
    assert not {"eval", "exec"}.intersection(
        {
            node.func.id
            for node in ast.walk(tree)
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
        }
    )
    assert not hasattr(backtest_module, "submit_order")
    assert not hasattr(backtest_module, "optimize")
    assert EXE_01.state is ExecutionState.PLANNED_CLOSED
