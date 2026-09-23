# Phase 3 Sprint 16: Optimization & Selection Governance v1.0

## 1. Baseline

- governed `main`: `4328f3aa81654d3b6db2ae6d04aac7ed87585f73`
- constitutional baseline v1.0: `50b61266f880cb9657b7f1b477d3d90825fe013f`
- predecessor PR #76: merged
- reviewed predecessor head: `9f01ca7fe4a5fdb727fdc44abfce769e4bb757dc`
- branch: `phase-3/optimization-selection-governance`

## 2. Mission

Sprint 16 adds a bounded deterministic parameter-search and candidate-selection boundary. It asks
whether exact candidate strategies can be enumerated, independently evaluated and selected under a
pre-specified policy without inheriting parent validation or hiding selection multiplicity.

## 3. Non-goals

There is no Optuna, random/Bayesian/genetic optimization, dynamic plugin, Pine parser/export,
TradingView integration, portfolio construction, broker/exchange adapter, deployment or live
execution. Sprint 12 strategy, accounting and fill semantics remain unchanged.

## 4. Search-space contract

`OptimizationSearchSpace` contains sorted unique `OptimizationParameter` values. v1 supports only
integer `threshold_bps` for the existing `CLOSE_VS_OPEN_LONG_ONLY` model, bounded to 0..10,000 with
an exact positive step and explicit default. Missing, duplicate, unsupported or non-integral
parameters fail closed.

## 5. Grid enumeration

The only method is `GRID_SEARCH`. Parameter names are sorted and their discrete ranges use inclusive
bounds. Cartesian enumeration is deterministic and is truncated exactly at `maximum_trials`; the
same search space and budget produce the same ordered parameter tuples.

## 6. Candidate identity

Candidate identity hashes the exact optimization plan, search space, parent strategy, normalized
dataset refs, source experiment and canonical parameter tuple. IDs contain no wall clock, UUID or
uncontrolled randomness.

## 7. Candidate strategy derivation

`OptimizationCandidateDefinition` binds the exact parent strategy, plan, parameter tuple and exact
derived `StrategyDefinition`. Only `threshold_bps` and the deterministic candidate strategy ID may
change. Model, timing, side, sizing, capital denomination, pyramiding/force-close flags, engine and
provenance remain identical.

## 8. Candidate evaluation pipeline

Every candidate supplies and re-verifies its own chain:

`Candidate Strategy -> authorized deterministic Backtest -> Scientific Validation -> Robustness Validation -> Selection Eligibility`.

`verify_robustness_validation_lineage()` is reused and therefore re-runs the complete scientific,
backtest, dataset, authorization, replay and accounting lineage. Parent PASS evidence cannot be
substituted for candidate evidence.

## 9. Multiplicity handling

`SINGLE_CANDIDATE` is accepted only for one trial. More than one candidate requires `BONFERRONI`;
`UNSUPPORTED` and multi-candidate `SINGLE_CANDIDATE` produce `INCONCLUSIVE`, never a selection.

## 10. Bonferroni semantics

For `n` tested candidates, `corrected_alpha = declared_alpha / n` under Decimal precision 34 and
ROUND_HALF_EVEN. Candidate validation plans must use confidence `1 - corrected_alpha`. With two
candidates and alpha `0.05`, the exact corrected alpha is `0.025` and confidence is `0.975`.

A one-candidate evaluation is encoded as `SINGLE_PREDECLARED_TEST`. A multi-candidate Bonferroni
evaluation is encoded as `MULTIPLE_TESTS_CORRECTED`: it is a corrected member of a declared
multiple-test family, never a single predeclared test. Optimization governance computes and supplies
the corrected confidence; scientific validation consumes that declared confidence and does not
recompute the family-wise correction. Multi-candidate evidence without a supported correction is
encoded as `MULTIPLE_TESTS_UNCORRECTED` and cannot authorize selection.

This is a bounded family-wise correction, not a general solution for adaptive search, PBO or
selection bias across undocumented prior research.

## 11. Eligibility constraints

A candidate is eligible only when its own scientific decision is `PASS`, its own robustness decision
is `PASS`, completed trades meet the declared minimum, and maximum drawdown does not exceed the
declared ceiling. No eligible candidate yields `INCONCLUSIVE`; the least-bad candidate is never
selected.

## 12. Deterministic ranking

Eligible candidates are compared lexicographically, without a weighted score:

1. higher total return;
2. lower maximum drawdown;
3. higher trade count;
4. lexicographically lower candidate ID.

## 13. Tie-breaking

The complete order is persisted in the selection result and tested with a true equal-metric case.
Mapping insertion order, filesystem order and repository scan order are irrelevant.

## 14. Selection authority

The plan and request must carry the same exact fingerprint-bearing selection-authority ref. Strategy
generation, backtesting, scientific validation and robustness validation do not self-authorize
selection. This remains technical authority binding, not authenticated human principal authority.

## 15. Lineage

`verify_optimization_selection_lineage()` independently reconstructs the bounded grid, candidate
definitions, candidate evidence verification, Bonferroni threshold, constraints, ranking, trial
records, selection result and run fingerprint. Summaries and stored refs are not trusted by
themselves.

## 16. Persistence

The immutable repository supports search space, plan, candidate definition/result, trial record,
selection result and run record using canonical JSON v1. Reads verify exact type, version and
fingerprint; identical writes are idempotent; corruption and wrong types fail; no mutable
latest/current alias exists.

## 17. Determinism

The optimization input fingerprint binds plan, parent strategy, source experiment/robustness,
instrument, normalized dataset refs, engine, multiplicity, budget, ordered candidate parameters,
candidate definitions and independently verified candidate results. Exact reruns reproduce bytes,
fingerprints, trial order and selection.

## 18. Golden evidence

New `tests/golden/optimization_selection_v1.json` pins search-space/plan fingerprints, two exact
candidate IDs, trial count, Bonferroni method and threshold, selected candidate ref, decision,
reason codes and selection-result fingerprint. Previous goldens remain byte-identical.

## 19. Tamper detection

Tests reject changed parameter bounds, candidate metrics/strategy, robustness evidence, trial index,
decision, multiplicity method, corrected threshold, selected authority and persisted bytes. Strict
codec decoding rejects unknown fields, wrong types and versions through existing repository rules.

## 20. Tests

- focused Sprint 16: 25 passed;
- full repository: 500 passed;
- governance-negative: 14 passed;
- execution isolation: 3 passed;
- ruff format/check and mypy: passed locally.

The focused suite includes one selected candidate, no eligible candidate, multiplicity blocking, a
true deterministic tie, budget enforcement, independent candidate evidence, persistence and golden
pinning.

## 21. Governance BEFORE -> AFTER

| ID | Before | After | Sprint 16 evidence / remaining boundary |
|---|---|---|---|
| IP-01 | OPEN | OPEN | No principal authentication runtime. |
| IP-02 | PARTIALLY_RESOLVED | PARTIALLY_RESOLVED | Canonical candidate/selection tamper evidence; no signatures/trust roots. |
| IP-03 | OPEN | OPEN | Exact authority ref is not delegation/revocation. |
| IP-04 | PARTIALLY_RESOLVED | PARTIALLY_RESOLVED | Optimization records gain canonical identity; broader authority remains open. |
| IP-05 | PARTIALLY_RESOLVED | PARTIALLY_RESOLVED | Candidate windows are fixed; external clock/calendar trust remains open. |
| IP-06 | OPEN | OPEN | No emergency/release authority. |
| IP-07 | OPEN | OPEN | No approval expiry runtime. |
| IP-08 | OPEN | OPEN | No freshness/monitoring crosswalk. |
| IP-09 | PARTIALLY_RESOLVED | PARTIALLY_RESOLVED | Bounded Bonferroni grid selection; adaptive-search and broader methods remain open. |
| IP-10 | OPEN | OPEN | Monitoring multiplicity remains outside this sprint. |
| IP-11 | PARTIALLY_RESOLVED | PARTIALLY_RESOLVED | Exact same governed dataset required; universal data acceptance remains open. |
| IP-12 | OPEN | OPEN | No new legal/licensing authority. |
| IP-13 | OPEN | OPEN | No adapter/authentication expansion. |
| IP-14 | PARTIALLY_RESOLVED | PARTIALLY_RESOLVED | Reproducible search/selection evidence; production release authority remains open. |

Counts remain `RESOLVED 0`, `PARTIALLY_RESOLVED 6`, `OPEN 8`, `DEFERRED 0`.

## 22. Readiness

- SEARCH_SPACE_CONTRACT_READY
- DETERMINISTIC_GRID_SEARCH_READY
- CANDIDATE_LINEAGE_READY
- MULTIPLICITY_CONTROL_READY
- SELECTION_POLICY_READY
- SELECTION_LINEAGE_READY
- SELECTION_REPRODUCIBILITY_READY
- SELECTION_TAMPER_DETECTION_READY
- SELECTION_PERSISTENCE_READY
- SELECTION_GOLDEN_EVIDENCE_READY
- ADVANCED_OPTIMIZER_NOT_READY
- PBO_NOT_READY
- DEFLATED_SHARPE_NOT_READY
- PINE_INTEGRATION_NOT_READY
- TRADINGVIEW_PARITY_NOT_READY
- PORTFOLIO_NOT_READY
- DEPLOYMENT_NOT_READY
- LIVE_EXECUTION_NOT_READY
- EXECUTION_CLOSED

## 23. Blockers

No blocker remains for the bounded v1 grid-selection boundary. Stronger claims remain blocked by
absent protected final holdout evidence, adaptive-search bias controls, PBO/Deflated Sharpe,
authenticated selection authority, deployment/risk approval and live-execution governance.

## 24. Limitations

Only `threshold_bps` and grid search are supported. Bonferroni covers the declared candidate family
only. There is no optimizer, parameter importance, search acceleration, protected OOS promotion,
strategy ranking across datasets, portfolio selection, Pine parity or production authority.

## 25. Sprint 17 recommendation only

After independent review and merge, consider **Pine Strategy Contract & Governed Strategy Intake
v1.0**: exact versioned Pine artifacts bound to governed strategy definitions. Pine/Python parity
belongs to a later sprint. Sprint 17 is not implemented here.

## 26. Disposition

`PHASE 3 SPRINT 16 COMPLETE WITH OPEN PRECONDITIONS`
