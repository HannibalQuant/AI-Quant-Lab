# Phase 3 Sprint 15: Controlled Robustness Validation v1.0

## 1. Baseline

- governed `main`: `eff334fe7c1cfba1ea6d1b8a5d1d7df4bef2d9f1`
- constitutional v1.0: `50b61266f880cb9657b7f1b477d3d90825fe013f`
- predecessor PR #75: merged
- reviewed predecessor head: `890fcb3019733da0fa14a8ef7dff8cc5fc2077cd`
- branch: `phase-3/controlled-robustness-validation`

## 2. Mission

Sprint 15 adds a deterministic robustness boundary for an exact, independently verified Sprint 14
scientific-validation result and its verified source backtest. It asks whether that fixed result
remains materially supported under three narrow, declared forms of evidence: rolling temporal test
partitions, completed-trade bootstrap, and worse-commission perturbation. It does not search for a
better strategy or authorize deployment.

## 3. Non-goals

There is no optimizer, grid/random/Bayesian search, parameter sweep, strategy/model selection,
synthetic OHLC generation, market-path simulation, PBO, Deflated Sharpe, portfolio construction,
broker/exchange adapter, network access, deployment or live execution. The Sprint 12 strategy and
accounting semantics remain unchanged.

## 4. Robustness boundary

`RobustnessValidationResult.PASS` means only that every enabled bounded method passed its exact
plan thresholds. It is neither proof of edge nor authorization for optimization, risk acceptance,
deployment or execution. A scientific PASS is mandatory for an overall robustness PASS; a source
FAIL or INCONCLUSIVE cannot be promoted.

## 5. Partition model

`TemporalPartitionEvidence` binds each TRAIN or TEST range by half-open bar indices and by every
exact fingerprint-bearing `MarketBar` reference. Each split is contiguous (`train_end ==
test_start`), its train and test bars cannot overlap, and plan construction requires `step_bars >=
test_bars`, so TEST slices cannot overlap. Ordering comes only from the already verified canonical
replay; filesystem or mapping order is irrelevant.

Sprint 15 records no HOLDOUT partition and every result states `NOT_ESTABLISHED`. TEST evidence is
not relabeled as protected holdout evidence.

## 6. Walk-forward semantics

The only policy is `ROLLING_FIXED_STRATEGY`. Exact `train_bars`, `test_bars` and `step_bars` are
fingerprinted plan inputs. The immutable strategy, experiment, dataset, engine and accounting
ledger remain fixed across slices; there is no fitting, tuning or per-slice parameter selection.

Each TEST slice records exact partitions, completed trade count, return, net PnL, maximum drawdown
and method decision. `trade_count` and `net_pnl` are exit-attributed completed-trade statistics: a
trade belongs to the TEST slice containing its exit. `total_return` is instead equity-based over
the exact TEST window, so these measures are related but not interchangeable.

Aggregation records valid windows, positive-window ratio, median and worst test return, maximum
test drawdown and minimum per-slice trade count. `aggregate_test_return` compounds chronological,
non-overlapping TEST returns exactly as `product(1 + r_i) - 1`; it is not their arithmetic sum.
Any factor below zero fails closed. All thresholds are explicit plan fields.

This is a rolling evaluation foundation over the exact verified ledger/equity evidence. TRAIN
ranges establish preceding temporal context; they do not train a model.

## 7. Monte Carlo semantics

The only policy is `TRADE_BOOTSTRAP_WITH_REPLACEMENT`. Each draw samples from completed trade net
PnL contributions normalized by initial capital. SHA-256 counter-derived indices bind the explicit
seed, iteration and draw number; no platform RNG, wall clock or hidden state is used. Outputs are
median, declared lower/upper empirical terminal-return quantiles, worst observed drawdown and the
empirical fraction of terminal returns greater than zero.

This measures completed-trade sampling/sequence sensitivity only. It is not a price-path model, a
future calibrated probability, temporal-independence proof or market-regime robustness claim. No
synthetic market bar is created.

## 8. Perturbation semantics

The only family is `COMMISSION_MULTIPLIER`. The plan carries a sorted, unique tuple beginning at
one. Each multiplier derives exact integer commission basis points from the source specification;
fractional-bps derivations fail closed, while `DECLARED_ZERO` remains exactly zero and never
invents a cost.

Every scenario receives deterministic specification, authorization, run and result identities
bound to the plan, source specification, source strategy, source backtest and multiplier. It then
passes through the same authorization reconstruction and public deterministic strategy-backtest
engine as the source run. Dataset, bars, strategy, signal logic, sizing, slippage, funding and
observation window remain unchanged; only commission changes. The multiplier-one scenario must
reproduce the source statistics exactly.

If the engine rejects an entry because perturbed commission makes fixed notional plus commission
exceed available cash, the scenario records `FAIL / COST_PERTURBATION_EXECUTION_FAILED` with no
synthetic statistics or result ref. Original fills are never reused. This is a true governed replay,
not post-hoc ledger subtraction or an exchange-cost forecast.

## 9. Decision rules

- overall `PASS`: source scientific decision is PASS and all three methods PASS;
- overall `FAIL`: source is PASS and any enabled method crosses its declared fail rule;
- overall `INCONCLUSIVE`: source is not PASS, evidence is insufficient, a method falls between its
  pass/fail thresholds, or another mandatory condition cannot be established.

Walk-forward PASS requires declared minimum windows/trades, positive-window ratio and worst-return
floor. Monte Carlo PASS requires a strictly positive lower empirical quantile; FAIL requires a
nonpositive upper quantile. Cost PASS requires every scenario above its declared floor; FAIL uses
the declared worst-scenario threshold. Closed, sorted, duplicate-free reason codes identify the
path. Conflicting evidence cannot be averaged into PASS.

## 10. Source validation requirement

The request and plan bind the exact fingerprint-bearing `ScientificValidationResult` and
`ValidationRunRecord`. Both execution and later lineage verification call
`verify_scientific_validation_lineage()`; matching IDs or caller assertions are insufficient.

## 11. Source backtest requirement

The reused Sprint 14 verifier itself calls `verify_strategy_backtest_lineage()`. Consequently the
robustness boundary re-verifies the exact hardened v2 result, run record, authorization,
specification, policy, eligibility, engine, strategy, instrument, dataset lineage, deterministic
replay and independent accounting verification. Intermediate objects are never trusted merely
because their references agree.

## 12. Lineage

The governed chain is:

`RobustnessValidationPlan -> ScientificValidationResult -> ValidationRunRecord -> BacktestResultArtifact -> BacktestRunRecord -> exact strategy/experiment/dataset/instrument -> RobustnessValidationRunRecord -> RobustnessValidationResult`.

`verify_robustness_validation_lineage()` verifies exact request refs, re-runs source scientific and
backtest verification, reconstructs partitions and every method output, recomputes the aggregate
decision and input fingerprint, and then verifies the run/result references and deterministic
object equality.

## 13. Determinism

The robustness input fingerprint includes fingerprints for plan, scientific result/run, backtest
result/run, experiment, strategy and instrument, plus normalized dataset refs, seed, partition
parameters and commission scenarios. Thresholds and all remaining method parameters are already
bound through the plan fingerprint. Identical inputs produce identical partitions, draws,
scenarios, bytes, IDs, decisions and fingerprints. IDs are caller supplied; no `now()` or random
UUID exists.

## 14. Persistence

`RobustnessValidationPlan`, `RobustnessValidationResult` and
`RobustnessValidationRunRecord` use strict canonical JSON v1 and the existing immutable
`LocalDatasetRepository`. Exact type/version/fingerprint verification, idempotent identical
writes, corruption and wrong-type rejection, no overwrite, and no latest/current alias remain in
force. No database or mutable catalog is added.

## 15. Golden evidence

New read-only `tests/golden/robustness_validation_v1.json` pins a repository-owned synthetic PASS
case: plan and source-result fingerprints, robustness-input fingerprint, partition count,
compounded aggregate TEST return, Monte Carlo seed/iterations and lower return, deterministic cost
scenario IDs, derived commission bps, bounded summaries, decision, reason codes and result
fingerprint. The Sprint 15 golden changed because corrected compounding and true engine replay are
part of its governed identity; all earlier goldens remain byte-identical.

## 16. Tamper detection

Focused tests alter plan/result refs, strategy/instrument/source objects, source backtest values,
partitions, Monte Carlo seed and summary, perturbation summary, decision, reason codes, stored
bytes, type and version. The verifier rejects the changed evidence rather than accepting an
internally self-consistent substitute.

## 17. Authority boundary

Plan and request must carry the same exact fingerprint-bearing `AuthorityBindingId` reference.
Backtest runner, scientific validator, strategy proposer, actor string or boolean cannot substitute
for it. This is technical authority separation only; principal authentication, delegation and
revocation remain open under IP-01/IP-03.

Every result and run record preserves `deployment_authorization = NOT_AUTHORIZED` and
`execution_state = PLANNED_CLOSED`. EXE-01 remains `PLANNED_CLOSED`.

## 18. Multiplicity handling

Sprint 15 does not implement Bonferroni or another corrected multiplicity method. The plan fixes
exactly three required methods and uses a conservative all-methods-must-pass aggregate, but that is
not represented as general multiple-testing correction. PBO and Deflated Sharpe remain absent.

## 19. Holdout evidence

Exact rolling TRAIN/TEST partition lineage is available. Protected external or reserved HOLDOUT
lineage is not. `RobustnessHoldoutEvidence.NOT_ESTABLISHED` is mandatory, preventing TEST slices
from being promoted to an out-of-sample holdout claim.

## 20. Tests

Focused tests cover explicit plan bounds and authority, robust PASS, fragile FAIL, insufficient
evidence, exact non-overlapping partitions, all three Monte Carlo decision paths, deterministic
seed behavior, exact compounded-return examples, true cost replay, deterministic scenario identity,
capital-infeasible cost failure without reused fills, source-validation/backtest re-verification,
strategy/instrument mismatch, output tampering, strict codec, immutable persistence, corruption,
wrong type/version, golden evidence, reproducible bytes and prohibited-capability isolation.

Final local and CI counts are recorded in the Draft PR after all gates complete. The unchanged CI
matrix runs Python 3.12 and 3.13.

## 21. Governance preconditions BEFORE -> AFTER

| ID | Before | After | Sprint 15 evidence and remaining authority |
|---|---|---|---|
| IP-01 | OPEN | OPEN | Exact authority ref is not authenticated identity. |
| IP-02 | PARTIALLY_RESOLVED | PARTIALLY_RESOLVED | Canonical tamper evidence extends to robustness; signatures/authenticity remain open. |
| IP-03 | OPEN | OPEN | Authority is separated but authentication/delegation/revocation remain open. |
| IP-04 | PARTIALLY_RESOLVED | PARTIALLY_RESOLVED | Three strict versioned robustness codecs; broader representation approval remains open. |
| IP-05 | PARTIALLY_RESOLVED | PARTIALLY_RESOLVED | Exact bar partitions and ordering; external clock/calendar authority remains open. |
| IP-06 | OPEN | OPEN | No emergency/reactivation runtime. |
| IP-07 | OPEN | OPEN | No deployment approval or expiry workflow. |
| IP-08 | OPEN | OPEN | No validation freshness/monitoring crosswalk. |
| IP-09 | PARTIALLY_RESOLVED | PARTIALLY_RESOLVED | Bounded rolling, trade-bootstrap and commission-perturbation evidence; protected holdout, dependence-aware methods, corrected multiplicity and broader method approval remain open. |
| IP-10 | OPEN | OPEN | No monitoring threshold/window methodology. |
| IP-11 | PARTIALLY_RESOLVED | PARTIALLY_RESOLVED | Exact result quality and fail-closed evidence; universal/provider acceptance remains open. |
| IP-12 | OPEN | OPEN | No legal, retention or licensing authority added. |
| IP-13 | OPEN | OPEN | Closed local implementation; authenticated actors/providers remain open. |
| IP-14 | PARTIALLY_RESOLVED | PARTIALLY_RESOLVED | Determinism, golden, tamper, codec, lineage and CI evidence; release authority remains open. |

Counts remain: `RESOLVED 0 -> 0`, `PARTIALLY_RESOLVED 6 -> 6`, `OPEN 8 -> 8`,
`DEFERRED 0 -> 0`.

## 22. Readiness

- `ROBUSTNESS_PLAN_CONTRACT_READY`
- `TEMPORAL_PARTITION_LINEAGE_READY`
- `WALK_FORWARD_FOUNDATION_READY`
- `MONTE_CARLO_TRADE_ROBUSTNESS_READY`
- `COST_PERTURBATION_READY`
- `ROBUSTNESS_DECISION_READY`
- `ROBUSTNESS_LINEAGE_READY`
- `ROBUSTNESS_REPRODUCIBILITY_READY`
- `ROBUSTNESS_TAMPER_DETECTION_READY`
- `ROBUSTNESS_PERSISTENCE_READY`
- `ROBUSTNESS_GOLDEN_EVIDENCE_READY`
- `OPTIMIZATION_NOT_READY`
- `PBO_NOT_READY`
- `DEFLATED_SHARPE_NOT_READY`
- `PORTFOLIO_NOT_READY`
- `DEPLOYMENT_NOT_READY`
- `LIVE_EXECUTION_NOT_READY`
- `EXECUTION_CLOSED`

## 23. Blockers

No blocker remains for this bounded robustness foundation. Protected holdout lineage, corrected
multiplicity, dependence-aware uncertainty, broader market/regime evidence, authenticated
authority and release/risk decisions block stronger robustness or operational claims.

## 24. Limitations

Rolling slices evaluate the fixed verified ledger; they do not refit a model. Trade bootstrap does
not preserve serial dependence or simulate markets. Cost perturbation reruns the exact engine but
covers commission only; it does not perturb slippage, funding or strategy parameters. Compounded
TEST returns summarize chronological non-overlapping windows and are not a deployable portfolio
claim. Evidence is limited to the existing one-instrument, long-only, fixed-notional synthetic
architecture fixture.

## 25. Sprint 16 recommendation — discussion only

After independent review and merge, the next candidate may be **Optimization & Selection
Governance v1.0**. It should first govern search spaces, trial identity, multiple-testing and
selection-bias controls before any optimizer is enabled. Sprint 16 is not implemented here.

## 26. Disposition

`PHASE 3 SPRINT 15 COMPLETE WITH OPEN PRECONDITIONS`

Deployment remains `NOT_AUTHORIZED`; live execution and EXE-01 remain `PLANNED_CLOSED`.
