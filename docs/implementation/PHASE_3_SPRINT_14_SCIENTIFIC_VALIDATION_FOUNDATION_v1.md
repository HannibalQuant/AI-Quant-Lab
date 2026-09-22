# Phase 3 Sprint 14: Scientific Validation Foundation v1.0

## 1. Baseline

- governed `main`: `ff487a3b3821225eec67dd5e809b7ef2f00d2618`
- constitutional v1.0: `50b61266f880cb9657b7f1b477d3d90825fe013f`
- predecessor PR #74: merged, reviewed head
  `ade8f0804cc6ba823eaccbc11df7eca697cb1551`
- branch: `phase-3/scientific-validation-foundation`

## 2. Mission

Sprint 14 introduces a separate, deterministic scientific-validation boundary for an exact
verified Sprint 13 backtest result. It answers whether one result was evaluated under one declared,
reproducible method contract. It does not establish general robustness, transferable edge,
out-of-sample validity, risk acceptance, deployment authority or live-execution readiness.

## 3. Non-goals

There is no optimizer, parameter/grid/random/Bayesian search, strategy selection, walk-forward,
Monte Carlo, PBO, Deflated Sharpe, CSCV, regime or cross-market robustness, portfolio, deployment,
broker/exchange adapter, network path or live trading. No strategy, backtest accounting, cost,
fill, sizing or result semantics from Sprints 12–13 are changed.

## 4. Scientific boundary

`BacktestResultArtifact.validation_status` remains `NOT_VALIDATED` and cannot self-promote.
`ScientificValidationResult` is a new immutable output from the validation boundary. PASS means
only that the exact bounded positive-edge hypothesis passed the declared interval rule. PASS does
not authorize risk, deployment or execution.

## 5. Hypothesis semantics

The closed Sprint 14 hypothesis pair is pre-specified in `ValidationPlan`:

- null: `EXPECTED_TOTAL_RETURN_NONPOSITIVE`
- alternative: `EXPECTED_TOTAL_RETURN_POSITIVE`

There are no callables, plugins, runtime imports, `eval` or `exec` paths.

## 6. Primary metric

The only primary metric is dimensionless `TOTAL_RETURN`. The bounded supporting set is gross PnL,
net PnL, max drawdown and trade count. Supporting metrics do not silently alter the decision.

## 7. Sample definition

One sample observation is one completed `SimulatedTrade`. Bars, orders, fills and an unresolved
open position are not counted as statistical samples. Each trade contribution is
`trade.net_pnl / initial_capital`; one bootstrap replicate is the sum of exactly `n` resampled
trade contributions, where `n` is the number of completed trades.

## 8. Uncertainty method

`TRADE_RETURN_BOOTSTRAP` is the only method. It uses completed trades only, an explicit seed and
iteration count, Decimal precision 34 / `ROUND_HALF_EVEN`, and a SHA-256 counter-derived index
stream. It has no platform RNG, wall clock, network, NumPy or hidden state. This bounded method
does not claim that trade observations are temporally independent.

## 9. Confidence interval

Bootstrap statistics are sorted canonically. The two-sided percentile bounds use declared
confidence, floor for the lower index and ceiling for the upper index. Canonical finite decimal
text is persisted. The point estimate is the independently verified backtest total return.

## 10. Decision semantics

- `PASS`: lower bound is strictly greater than zero;
- `FAIL`: upper bound is less than or equal to zero;
- `INCONCLUSIVE`: the interval overlaps zero or a mandatory evidence/governance condition blocks
  interpretation.

Closed reason codes identify the exact path. No grade, score, champion, profitability label or
deployment recommendation is produced.

## 11. Minimum evidence

`ValidationPlan.min_sample_size` and `min_trade_count` are positive, explicit and fingerprinted.
Failure to meet either yields `INCONCLUSIVE / INSUFFICIENT_TRADES`; a small sample can never PASS.

## 12. Holdout semantics

The plan declares `NONE_DECLARED` or `RESERVED_HOLDOUT`. Sprint 14 has no exact partition-lineage
contract capable of proving a holdout. Therefore `RESERVED_HOLDOUT` yields
`INCONCLUSIVE / HOLDOUT_REQUIRED`, and every result states
`out_of_sample_evidence = NOT_ESTABLISHED`. No out-of-sample claim is inferred.

## 13. Multiplicity semantics

PASS is available only for `SINGLE_PREDECLARED_TEST`. `UNKNOWN` yields
`MULTIPLICITY_UNKNOWN`; `MULTIPLE_TESTS_UNCORRECTED` yields `MULTIPLICITY_UNSUPPORTED`; both are
INCONCLUSIVE. Corrected multiplicity methods are deliberately absent.

## 14. Open-position handling

An end-of-window LONG is never synthetically exited. It yields
`INCONCLUSIVE / OPEN_POSITION_UNRESOLVED`. Completed trades remain visible as bounded uncertainty
evidence, but the unresolved result cannot PASS or FAIL under the current closed method.

## 15. Validation authority

Plan and request must carry the same exact fingerprint-bearing `AuthorityBindingId` reference.
An `AgentId`, proposer identity, strategy, runner, backtest result or boolean cannot substitute for
that binding. This is technical authority separation, not authenticated principal assurance;
IP-01 and IP-03 remain OPEN.

## 16. Exact lineage

Before evaluation, `run_scientific_validation()` reuses
`verify_strategy_backtest_lineage()`, which includes deterministic replay and independent Sprint
13 accounting verification. The validator accepts only current BacktestResultArtifact v2.

`verify_scientific_validation_lineage()` independently repeats the authoritative source-backtest
verification before it verifies and recomputes:

`ValidationPlan -> BacktestResultArtifact -> BacktestRunRecord -> ValidationRunRecord -> ScientificValidationResult`

The input fingerprint binds plan, backtest result/run, experiment, strategy, instrument, method,
iterations, confidence and seed. Changed refs, seed, authority, bounds, estimate, decision or reason
codes fail closed.

## 17. Persistence

`ValidationPlan`, `ScientificValidationResult` and `ValidationRunRecord` use strict canonical JSON
v1 codecs and the existing immutable `LocalDatasetRepository`. Exact type/version/fingerprint,
verified reload, identical-write idempotency, corruption/wrong-type rejection, no overwrite and no
latest/current alias remain mandatory.

## 18. Determinism

Identical exact inputs produce identical interval, decision, reason codes, canonical bytes,
fingerprints and run record. IDs and timestamps are caller supplied. A changed governed seed
changes the plan and validation-input identity.

## 19. Golden evidence

New read-only `tests/golden/scientific_validation_v1.json` pins a repository-owned synthetic PASS
case: plan and backtest fingerprints, input fingerprint, seed, sample size, estimate, interval,
confidence, decision, reasons and result fingerprint. Sprint 13 and all earlier goldens remain
byte-identical.

## 20. Tamper detection

Tests mutate plan/result/run refs, authority, seed, estimate, bounds, sample/trade counts,
confidence, decision and reason codes. They also exercise invalid/legacy backtest input, strict
codec fields, repository corruption and wrong stored type. Each path rejects without producing a
replacement authority claim.

## 21. Tests

Focused tests cover valid contracts, invalid metric/confidence/minimum/method/authority, exact v2
input, PASS/FAIL/interval-overlap, insufficient samples, open LONG, missing holdout, unknown and
uncorrected multiplicity, deterministic seeds and bytes, exact lineage, persistence, corruption,
strict decode, golden evidence and downstream closure. Full historical tests and execution
isolation remain enabled.

Local quality evidence on Python 3.12:

- focused Sprint 14: `28 passed`;
- full suite: `446 passed`;
- governance-negative / execution isolation: `14 passed`;
- `ruff format --check .`, `ruff check .` and `mypy`: passed.

The unchanged CI matrix independently runs the same gates on Python 3.12 and 3.13.

## 22. Governance preconditions BEFORE -> AFTER

| Precondition | Before | After | Evidence and remaining authority |
|---|---|---|---|
| IP-01 | OPEN | OPEN | Exact authority ref is not principal authentication. |
| IP-02 | PARTIALLY_RESOLVED | PARTIALLY_RESOLVED | Canonical validation tamper evidence; signatures/authenticity remain open. |
| IP-03 | OPEN | OPEN | Authority boundary is exact but authentication/delegation/revocation remain open. |
| IP-04 | PARTIALLY_RESOLVED | PARTIALLY_RESOLVED | Three strict versioned validation codecs; broader representation approval remains open. |
| IP-05 | PARTIALLY_RESOLVED | PARTIALLY_RESOLVED | Existing exact result chronology reused; external clock/calendar authority remains open. |
| IP-06 | OPEN | OPEN | No emergency/reactivation runtime. |
| IP-07 | OPEN | OPEN | No deployment approval or expiry workflow. |
| IP-08 | OPEN | OPEN | No freshness/monitoring crosswalk. |
| IP-09 | OPEN | PARTIALLY_RESOLVED | One bounded pre-specified trade-bootstrap method; temporal preregistration, OOS, dependence-aware robustness, corrected multiplicity and broader approval remain open. |
| IP-10 | OPEN | OPEN | Multiplicity ambiguity blocks; no monitoring methodology. |
| IP-11 | PARTIALLY_RESOLVED | PARTIALLY_RESOLVED | Verified result input and minimum evidence; provider/universal quality authority remains open. |
| IP-12 | OPEN | OPEN | No new legal, retention or licensing authority. |
| IP-13 | OPEN | OPEN | Closed local validator; authenticated actors/providers remain open. |
| IP-14 | PARTIALLY_RESOLVED | PARTIALLY_RESOLVED | Determinism, golden, tamper, codec and CI evidence; release authority remains open. |

Counts: `RESOLVED 0 -> 0`, `PARTIALLY_RESOLVED 5 -> 6`, `OPEN 9 -> 8`,
`DEFERRED 0 -> 0`.

## 23. Readiness

- `VALIDATION_PLAN_CONTRACT_READY`
- `HYPOTHESIS_CONTRACT_READY`
- `VALIDATION_AUTHORITY_BOUNDARY_READY`
- `UNCERTAINTY_ESTIMATION_FOUNDATION_READY`
- `VALIDATION_DECISION_READY`
- `VALIDATION_LINEAGE_READY`
- `VALIDATION_REPRODUCIBILITY_READY`
- `VALIDATION_TAMPER_DETECTION_READY`
- `VALIDATION_PERSISTENCE_READY`
- `VALIDATION_GOLDEN_EVIDENCE_READY`
- `OUT_OF_SAMPLE_VALIDATION_NOT_READY`
- `MULTIPLICITY_CORRECTION_NOT_READY`
- `WALK_FORWARD_NOT_READY`
- `MONTE_CARLO_NOT_READY`
- `OPTIMIZATION_NOT_READY`
- `PORTFOLIO_NOT_READY`
- `DEPLOYMENT_NOT_READY`
- `LIVE_EXECUTION_NOT_READY`
- `EXECUTION_CLOSED`

## 24. Blockers

No blocker remains for the bounded single-result method foundation. Actual holdout lineage,
dependence-aware robustness, corrected multiplicity, broader validation governance, authenticated
authority and release/risk/deployment decisions block stronger scientific or operational claims.

## 25. Limitations

The method evaluates one exact single-instrument, long-only, fixed-notional result using completed
trade contributions. It does not establish temporal independence, external replication,
cross-market transfer, parameter stability or strategy robustness. PASS is scoped scientific
evidence, not proof of edge.

## 26. Sprint 15 recommendation — discussion only

After independent review and merge, the preferred candidate is **Controlled Robustness Validation
v1.0**, introducing actual partition lineage and carefully governed robustness/multiplicity
methods. Sprint 15 is not implemented here.

## 27. Disposition

`PHASE 3 SPRINT 14 COMPLETE WITH OPEN PRECONDITIONS`

Deployment remains `NOT_AUTHORIZED`; live execution and EXE-01 remain `PLANNED_CLOSED`.
