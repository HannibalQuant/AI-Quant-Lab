# Phase 3 Sprint 12: Controlled Strategy Backtest Engine v1.0

## 1. Baseline

- governed `main`: `5230d0dd2c36b5b5c95d6d5c8161de4f2aadfd3f`
- constitutional v1.0: `50b61266f880cb9657b7f1b477d3d90825fe013f`
- predecessor PR: #72, merged with reviewed head
  `56bb4734287d77738f84bae019d69abe909b6886`
- branch: `phase-3/controlled-strategy-backtest-engine`

## 2. Mission

Sprint 12 adds one local deterministic research simulation path for an exact previously
`AUTHORIZED` `STRATEGY_BACKTEST`. It proves signal timing, next-eligible-event fills, a bounded
position state, explicit costs, accounting, immutable results and exact lineage. A completed or
profitable simulation is not validation, scientific evidence, deployment authority or live
execution authority.

## 3. Non-goals

No optimizer, parameter sweep, strategy ranking, walk-forward, Monte Carlo, scientific validation,
portfolio allocation, broker/exchange adapter, network access, order submission, deployment,
paper broker or live trading is present. No dynamic plugin, external callable, module path,
`eval`, `exec` or subprocess is accepted.

## 4. Strategy contract

`StrategyDefinition` is frozen, versioned and canonically fingerprinted. It binds exact strategy
identity, model, threshold, signal/execution timing, long-only permission, fixed notional, capital
currency and scale, no-pyramiding/no-force-close declarations, engine reference and provenance.
The authorization specification includes the exact strategy ID and fingerprint in its sorted
configuration. Python code and callable behavior are not data fields.

## 5. Supported strategy family

The only executable strategy is `CLOSE_VS_OPEN_LONG_ONLY`. A fully available bar requests `LONG`
when `close / open - 1` is greater than the declared non-negative threshold; otherwise it requests
`FLAT`. This synthetic rule demonstrates architecture, not alpha. Sprint 11 `MARKET_STATISTICS`
remains unchanged and fully supported.

## 6. Signal timing

Signals use `BAR_CLOSE_AFTER_AVAILABILITY`. `signal_time` and `submitted_time` equal the source
bar's governed `availability_time`. A signal cannot observe a future bar, and an execution event
cannot precede this boundary.

## 7. Next-event fill semantics

`FIRST_ELIGIBLE_NEXT_BAR_OPEN` selects the first later locked bar whose `bar_open >= signal_time`.
This is deliberately stricter than blindly choosing bar N+1: if a vendor publishes bar N after
bar N+1 has opened, that already-past open is ineligible. No qualifying bar fails with typed
`MissingNextBar`; the engine never fills at an impossible time.

## 8. Order model

`SimulatedOrder` is immutable and explicitly simulation-only. It binds side, notional, signal,
submission and fill eligibility times, exact source/fill bars, exact strategy, run and `FILLED`
status. Only deterministic simulated market transitions are represented.

## 9. Fill model

`SimulatedFill` binds an order to one exact `MarketBar`, its open reference price, deterministic
execution price, quantity, notional, commission and slippage cost. There are no partial fills,
intrabar assumptions or hidden prices.

## 10. Position model

The model is single-instrument, `FLAT`/`LONG`, one position at a time, no pyramiding, leverage,
partial fills or partial closes. A contradictory signal while a future transition is pending
fails closed instead of being implicitly cancelled or reordered.

## 11. Sizing

Only `FIXED_NOTIONAL` is supported. `FIXED_QUANTITY`, `PERCENT_EQUITY`, `UNKNOWN` and
`NOT_APPLICABLE` fail closed at the runner boundary. Fixed notional must be positive and no larger
than initial capital.

## 12. Capital

Initial capital comes from `ExperimentSpecification.capital_notional_minor` and is interpreted
only with the strategy's explicit `capital_currency` and `capital_minor_unit_scale`. Sprint 12
uses no FX conversion. Initial capital must be positive.

## 13. Commission

Supported declarations are `DECLARED_ZERO` and `DECLARED_BPS`:

`commission = abs(fill_notional) * commission_bps / 10_000`

`UNKNOWN` and trading `NOT_APPLICABLE` fail closed.

## 14. Slippage

Slippage is deterministic and non-random:

- BUY: `reference_price * (1 + bps / 10_000)`
- SELL: `reference_price * (1 - bps / 10_000)`

`DECLARED_ZERO` preserves the reference price. `UNKNOWN` and `NOT_APPLICABLE` fail closed.

## 15. Funding limitation

Only `NOT_APPLICABLE` is executable. The engine does not claim to model perpetual funding.
Any other declaration raises typed `UnsupportedFunding`.

## 16. Execution-price validity

Signal open/close, fill reference, execution and mark prices must be strictly positive. This does
not alter Sprint 11 descriptive support for `PriceDomain.SIGNED`; it only prevents trading at a
zero/negative price. Violations raise `InvalidExecutionPrice`.

## 17. Accounting model

The long-only cash ledger is explicit:

- entry: `cash -= fill_notional + entry_commission`
- exit: `cash += fill_notional - exit_commission`
- equity: `cash + position_quantity * mark_close`
- gross closed PnL: `(exit_execution - entry_execution) * quantity`
- net closed PnL: `gross PnL - entry_commission - exit_commission`

Slippage is already embedded in execution prices and is also reported as an explanatory cost; it
is not deducted twice. Negative equity and inconsistent transitions fail closed.

## 18. Trade model

`SimulatedTrade` binds exact entry/exit fill IDs, quantity, execution prices, gross/net PnL,
commission, explanatory slippage cost, UTC times, strategy and run. It makes no performance or
quality judgment.

## 19. Equity curve

Every governed bar produces one immutable `EquityPoint` after any eligible open fill and at the
bar's availability event. Points record cash, position quantity/value, unrealized and realized
PnL and equity in deterministic temporal order.

## 20. End-of-window behavior

Sprint 12 never silently force-closes. An already-open position is preserved as `LONG` and marked
at the final governed close. A new required transition without a later eligible fill bar fails
closed. `force_close_at_window_end=True` is unsupported by contract.

## 21. Metrics

The closed result contract contains only `trade_count`, `gross_pnl`, `net_pnl`, `total_return` and
`max_drawdown`. `total_return = final_equity / initial_capital - 1`. Max drawdown is the
non-negative maximum loss magnitude `1 - equity / running_peak`, with initial capital included as
the initial peak. No Sharpe, Sortino, scoring or significance claim is calculated.

## 22. Result lineage

The exact chain is:

`RealCsvSourceDeclaration -> RealCsvAdmissionRecord -> ResearchDatasetEligibilityRecord ->`
`ExperimentSpecification -> ExperimentAuthorizationPolicy -> ExperimentAuthorizationRecord ->`
`ExperimentReplayContract -> StrategyDefinition -> BacktestRunRecord ->`
`SimulatedOrder/Fill/Trade -> BacktestResultArtifact`.

`verify_strategy_backtest_lineage()` recomputes the complete result from exact governed bars and
rejects changed inputs, references, accounting values or result content.

## 23. Reproducibility

The same authorization, specification, eligible dataset, engine, strategy, costs, capital,
configuration, seed, window, completion time and provenance create identical run/result bytes and
repository keys. IDs are caller supplied and deterministic; there is no current time or random
UUID dependency.

## 24. Persistence

`LocalDatasetRepository` now stores `StrategyDefinition`, `BacktestResultArtifact` and
`BacktestRunRecord` with canonical JSON v1, type/version/fingerprint addressing, verified reload,
tamper detection, idempotent identical writes, no overwrite and no mutable latest/current alias.
Orders, fills, trades and equity points are integrity-bound inside the bounded result artifact.

## 25. Tests

Focused tests cover successful authorization/run, strict delayed next-event timing, order/fill/
trade determinism, exact commission/slippage formulas, cash/equity identities, metrics, explicit
zero versus unknown costs, unsupported funding/sizing, bad strategy/authorization references,
positive execution-price requirements, terminal missing fills, exact lineage reconstruction,
canonical round-trip, immutable reload, tamper/type/version/extra-field rejection and prohibited
capability isolation. The full historical suite remains enabled and unchanged.

Local evidence for the implementation tree: focused Sprint 12 `17 passed`; full suite `377
passed`; governance-negative `14 passed`; combined Sprint 11/Sprint 12 execution-isolation plus
governance-negative `16 passed`; `ruff format --check .` reports 127 formatted files; `ruff check
.` passes; and `mypy` succeeds for 37 source files. GitHub Actions evidence is recorded on the
Draft PR for the exact published head.

## 26. Governance preconditions BEFORE -> AFTER

| Status | Before | After |
|---|---:|---:|
| RESOLVED | 0 | 0 |
| PARTIALLY_RESOLVED | 5 | 5 |
| OPEN | 9 | 9 |
| DEFERRED | 0 | 0 |

IP-02, IP-04, IP-05, IP-11 and IP-14 gain deterministic simulation/accounting/lineage evidence but
remain `PARTIALLY_RESOLVED`. Authentication, signatures/authenticity, institutional temporal and
data-quality authority, scientific validation, legal/provider authority and release authority
remain open. No precondition is promoted merely because the simulator exists.

## 27. Readiness

- `STRATEGY_BACKTEST_ENGINE_READY`
- `NEXT_EVENT_FILL_MODEL_READY`
- `SIMULATED_ORDER_MODEL_READY`
- `SIMULATED_FILL_MODEL_READY`
- `SIMULATED_POSITION_MODEL_READY`
- `SIMULATED_TRADE_ARTIFACT_READY`
- `BACKTEST_ACCOUNTING_READY`
- `BACKTEST_RESULT_LINEAGE_READY`
- `BACKTEST_REPRODUCIBILITY_READY`
- `OPTIMIZATION_NOT_READY`
- `WALK_FORWARD_NOT_READY`
- `MONTE_CARLO_NOT_READY`
- `SCIENTIFIC_VALIDATION_NOT_READY`
- `DEPLOYMENT_NOT_READY`
- `LIVE_EXECUTION_NOT_READY`
- `EXECUTION_CLOSED`

## 28. Blockers

No blocker remains for the bounded local synthetic strategy simulation. Open governance
preconditions block scientific validation, strategy selection, deployment and live execution.

## 29. Remaining limitations

Only one long-only rule and fixed-notional model exist. There is no shorting, leverage, portfolio,
intrabar execution, partial fill, funding, session calendar, forced close, benchmark, validation or
strategy quality claim. Actor/provider authenticity and legal authority remain outside this sprint.

## 30. Sprint disposition

`PHASE 3 SPRINT 12 COMPLETE WITH OPEN PRECONDITIONS`

Validation remains `NOT_VALIDATED`, deployment remains `NOT_AUTHORIZED`, and both live execution
and EXE-01 remain `PLANNED_CLOSED`.

## 31. Recommended Sprint 13 — discussion only

Prefer **Backtest Result Contract Hardening** before broader strategy families or scientific
validation. Review accounting invariants, open-position valuation, larger bounded ledgers and
independent golden evidence. Do not begin optimization automatically. No Sprint 13 capability is
implemented here.
