# Phase 3 Sprint 13: Backtest Result Contract Hardening v1.0

## 1. Baseline

- governed `main`: `93eb782dfc130b425ff597224fda3c1b343725d5`
- constitutional v1.0: `50b61266f880cb9657b7f1b477d3d90825fe013f`
- predecessor PR: #73, merged with reviewed head
  `ab2e2f73a1b3ce8906f5a562476cefc88d4d5959`
- branch: `phase-3/backtest-result-contract-hardening`

## 2. Mission

Sprint 13 makes a completed Sprint 12 result independently verifiable. It reconstructs exact
order/fill/trade state, cash, quantity, realized and unrealized PnL, equity and summaries from the
immutable ledger and governed replay bars. Persisted totals are claims to verify, not trusted
inputs. Reproducibility remains distinct from scientific validation.

## 3. Non-goals

There is no new strategy, indicator, optimizer, search, walk-forward, Monte Carlo, validation,
portfolio, leverage, short, partial fill, FX conversion, broker/exchange adapter, network access,
deployment or live execution. `CLOSE_VS_OPEN_LONG_ONLY`, `LONG_ONLY`, `FIXED_NOTIONAL`, delayed
next-event fills, no pyramiding, no force-close, Decimal precision 34 / `ROUND_HALF_EVEN`, exact
cost rules and funding `NOT_APPLICABLE` remain unchanged.

## 4. Accounting invariants

`verify_backtest_accounting()` is separate from the simulation loop. Starting from the declared
initial capital, it independently applies each exact fill:

- BUY: `cash_after = cash_before - fill_notional - commission`
- SELL: `cash_after = cash_before + fill_notional - commission`
- `fill_notional = execution_price * quantity`
- `equity = cash + position_value`

BUY requires `FLAT` and positive quantity. SELL requires `LONG` and must close the exact open
quantity. Negative quantity, double entry, SELL while flat and hidden mutation fail closed.
For every BUY, the independent verifier reconstructs the exact governed `FIXED_NOTIONAL` entry
size from `StrategyDefinition.fixed_notional_minor / capital_minor_unit_scale`; an internally
self-consistent order/fill notional cannot replace that sizing declaration.

## 5. Order/fill invariants

Order IDs and fill IDs are unique. Every order has exactly one fill; every fill has exactly one
order. Side, order ID, source/fill bar refs, exact strategy/run refs, notional and time linkage are
checked. The exact source bar supplies signal availability; the exact fill bar supplies its open,
and the fill must remain inside the authorized observation window. Orphans, duplicates and
non-monotonic fills fail with typed accounting errors.

## 6. Trade invariants

Each completed trade binds one BUY entry fill to one later SELL exit fill. IDs are unique, fills
cannot participate in multiple trades, run/strategy refs match, quantities are identical and
entry time precedes exit time. Unknown fills or an unrepresented closed position fail closed.

## 7. Realized PnL

For every trade:

`gross_pnl = (exit_execution_price - entry_execution_price) * quantity`

`commission = entry_commission + exit_commission`

`net_pnl = gross_pnl - commission`

Equity-point `realized_pnl` equals cumulative completed-trade net PnL at that exact event.

## 8. Unrealized PnL

For LONG:

`unrealized_pnl = (mark_close - entry_execution_price) * current_quantity`

For FLAT it is exactly zero. The verifier checks every equity point, not only the final point.

## 9. Open-position valuation

An end-of-window LONG remains open. It requires exactly one unresolved BUY, positive quantity, no
synthetic exit/trade, and exact final mark valuation. Final position value is quantity times the
last governed close; final equity is final cash plus that value. A FLAT result requires zero final
quantity/value/unrealized PnL and no unresolved fill. No force-close is inferred.

## 10. Equity identity

`EquityPoint` now contains an exact `bar_ref`. For every selected replay bar the verifier checks
one point in canonical order, exact availability event time, cash, quantity,
`position_value = quantity * bar.close`, unrealized PnL, cumulative realized PnL and
`equity = cash + position_value`. Event time alone is never used as object identity.

## 11. Result summaries

The verifier reconstructs and compares `trade_count`, gross PnL, net PnL, final cash, final equity,
total return and max drawdown. Total return remains
`final_equity / initial_capital - 1`. Max drawdown remains the non-negative maximum
`1 - equity / running_peak`, with initial capital as the starting peak.

## 12. Temporal invariants

The exact model requires source availability = signal = submission, followed by a strictly later
eligible fill bar. `eligible_fill_time = fill_time = exact fill bar open`; fills are strictly
ordered and inside the authorized window. Trade entry precedes exit. No future or external bar may
enter the ledger.

## 13. Denomination

Sprint 12's exact instrument binding remains mandatory. Result currency and scale must equal the
strategy declarations, and the strategy currency must equal the governed instrument quote asset.
Initial capital, notional, cash, commission, position value, PnL and equity use that one conceptual
denomination. No FX or stablecoin equivalence exists.

## 14. Lineage

`verify_strategy_backtest_lineage()` now layers:

1. exact instrument/dataset/authorization lineage;
2. independent accounting and ledger verification;
3. exact deterministic replay reconstruction;
4. exact result and run-record references/fingerprints.

The independent verifier executes before equality with the replay-produced artifact, so accounting
tamper is not accepted merely because persisted summaries agree with each other.

## 15. Persistence

The hardened `BacktestResultArtifact` schema is explicit version 2 because `EquityPoint.bar_ref`
materially changes canonical bytes. There is no silent migration or auto-upgrade of legacy bytes.
`LocalDatasetRepository` retains canonical JSON, immutable type/version/fingerprint keys, verified
reload, idempotent identical writes, conflict rejection, no overwrite and no latest/current alias.

## 16. Golden evidence

New read-only `tests/golden/backtest_result_hardening_v1.json` pins a repository-owned synthetic
FLAT result: strategy/instrument/authorization/engine fingerprints, run-input fingerprint,
order/fill/trade IDs, final cash/equity, state, summaries and result fingerprint. No historical
golden was changed and no vendor data is included.

## 17. Tamper detection

Focused negative coverage mutates order side/fill ref, fill bar/time/execution/commission/quantity,
trade entry/exit/quantity/gross/commission/slippage/net, equity cash/quantity/value/unrealized/
realized/total, final cash/equity and every summary. Duplicate order/fill/trade IDs and orphaned
objects fail closed. Corrupted persisted bytes and wrong type/version remain rejected.

## 18. Determinism

The same immutable authorization, specification, dataset, instrument, strategy, engine, costs,
window and caller-supplied IDs produce identical canonical bytes, fingerprints, run-input
fingerprint and order/fill/trade IDs. No current time, random UUID or collection-order dependency
is introduced.

## 19. Tests

Focused Sprint 12+13 evidence covers valid FLAT/open-LONG verification, exact ledgers,
deterministic identity, immutable persistence and all required tamper families. The full historical
suite remains enabled. Local evidence: focused Sprint 12+13 `57 passed`; full suite `417 passed`;
governance-negative `14 passed`; combined execution-isolation/governance `16 passed`; `ruff format
--check .` reports 129 formatted files; `ruff check .` passes; and `mypy` succeeds for 38 source
files. GitHub Actions evidence is recorded in PR #74 for the exact published head.

## 20. Governance preconditions BEFORE -> AFTER

| Status | Before | After |
|---|---:|---:|
| RESOLVED | 0 | 0 |
| PARTIALLY_RESOLVED | 5 | 5 |
| OPEN | 9 | 9 |
| DEFERRED | 0 | 0 |

IP-02 gains independent tamper/accounting evidence; IP-04 gains explicit version-2 canonical
result representation; IP-11 gains deterministic result-quality invariants; IP-14 gains bounded
golden and negative CI evidence. All remain `PARTIALLY_RESOLVED`. Authentication/signatures,
provider/legal authority, scientific validation, release/deployment authority and execution remain
open. No status is promoted by implementation alone.

## 21. Readiness

- `BACKTEST_ACCOUNTING_VERIFIER_READY`
- `ORDER_FILL_LEDGER_VERIFICATION_READY`
- `TRADE_LEDGER_VERIFICATION_READY`
- `OPEN_POSITION_VALUATION_READY`
- `EQUITY_CURVE_VERIFICATION_READY`
- `RESULT_SUMMARY_RECONSTRUCTION_READY`
- `BACKTEST_RESULT_TAMPER_DETECTION_READY`
- `BACKTEST_RESULT_REPRODUCIBILITY_READY`
- `BACKTEST_RESULT_GOLDEN_EVIDENCE_READY`
- `OPTIMIZATION_NOT_READY`
- `WALK_FORWARD_NOT_READY`
- `MONTE_CARLO_NOT_READY`
- `SCIENTIFIC_VALIDATION_NOT_READY`
- `DEPLOYMENT_NOT_READY`
- `LIVE_EXECUTION_NOT_READY`
- `EXECUTION_CLOSED`

## 22. Blockers

No blocker remains for the bounded Sprint 13 verifier. Open institutional preconditions block
scientific validation, strategy selection, deployment and live execution.

## 23. Limitations

Verification covers the exact single-instrument, long-only, fixed-notional Sprint 12 model. It is
not multi-asset accounting, a generalized execution ledger, legal/provider authentication or a
scientific verdict. Slippage remains embedded in execution prices and is reported explanatorily;
it is not deducted twice.

## 24. Disposition

`PHASE 3 SPRINT 13 COMPLETE WITH OPEN PRECONDITIONS`

Validation remains `NOT_VALIDATED`, deployment remains `NOT_AUTHORIZED`, live execution and
EXE-01 remain `PLANNED_CLOSED`.

## 25. Sprint 14 recommendation — discussion only

The next candidate is **Scientific Validation Foundation v1.0**, after independent review of this
result substrate. It should govern hypotheses, holdouts, multiplicity, uncertainty and validation
authority before any optimizer/search work. Sprint 14 is not implemented here.
