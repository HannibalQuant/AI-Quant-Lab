# Walk-Forward & Robustness Standard (WFRS) v1.0

## Specification Control

| Field | Value |
|---|---|
| Standard ID | `AIQL-WFRS` |
| Version | `1.0.0` |
| Status | Proposed for Sprint 37 review |
| Scope | Every institutional Walk-Forward and temporal-robustness claim |
| Authority | XDS, EEP, VEP, SLS, ARP, RCS, FFS, EDS, SFSS, EES, and robustness governance |

WFRS governs temporal partitioning, rolling generalization, out-of-sample integrity, reoptimization, fold evidence, aggregation, degradation, classification, and handoff. It is not an optimizer, strategy, Validation, or Deployment approval. Robustness is a conditional evidence claim, never immunity from future failure.

## 1. Walk-Forward and Robustness Philosophy

Temporal robustness asks whether a mechanism and its implementation remain credible when decisions are made using only information available before each test period. It prioritizes chronology and repeated generalization over final equity.

Robustness includes failure visibility. A favorable average cannot erase catastrophic, clustered, regime-specific, or unexplained fold failure.

## 2. Walk-Forward and Robustness Principles

No assessment proceeds without governed XDS, temporal scope, partition integrity, train/validation/test discipline, true out-of-sample evidence, fold records, aggregation, regime and window sensitivity, costs, execution, reoptimization rules, and failure criteria. One favorable fold, final equity, or in-sample performance cannot establish robustness. Silent window/metric/fold changes, post-result repartitioning, backfilled OOS evidence, leakage, and selective exclusion are prohibited.

## 3. Walk-Forward Identity Model

Every assessment has permanent Walk-Forward ID, Record ID, and version. Identity binds XDS, Experiment ID, strategy and implementation versions, market, timeframe, data, partitions, window model, regimes, features, edge, family, and owner.

Material partition, window, selection, reoptimization, metric, or scope change creates a new version or assessment identity.

## 4. Walk-Forward Object Model

The record defines all identities and upstream versions; universe, venue, instrument, timeframe, data and full period; temporal plan, window type/count/lengths, embargo, overlap, rolling/anchoring/expansion; reoptimization and parameter-selection rules; fixed parameters/search space; every fold identity, periods, regimes, data quality, costs, execution, metrics, acceptance and failure; aggregation; robustness/risk/degradation metrics; window, regime, market and timeframe sensitivity; classifications; limitations, contradictions, exclusions, deviations, follow-up; integrations, timestamps, and immutable audit trail.

## 5. Walk-Forward Lifecycle

**Proposed → Design Received → Temporal Scope Registered → Window Plan Registered → Partition Integrity Reviewed → Execution Authorized → Fold Execution → Fold Review → Aggregation Review → Robustness Classified → Evidence Packaged → Returned → Rejected → Challenged → Superseded → Archived**

Execution authorization freezes partitions and rules. Completion does not guarantee evidence eligibility.

## 6. Robustness Scope Rules

Scope fixes strategy, implementation, markets, instruments, timeframes, regimes, data, period, costs, execution, features, parameters, metrics, and intended claim. Conclusions cannot exceed the weakest evidenced dimension.

## 7. Temporal Partitioning Rules

Partitions preserve chronology and define train, validation, test, holdout, overlap, purge, embargo, preprocessing fit, selection access, and repeated-use policy before execution.

No future, validation, or test information may influence earlier training decisions except where explicitly part of a later fold after chronology permits it.

## 8. Rolling Window Rules

Rolling designs use fixed or preregistered window lengths and step sizes. Dropped history, overlap, regime representation, parameter refresh, and sample sufficiency are explicit.

## 9. Anchored Window Rules

Anchored designs keep a fixed start and expand available training information. Increasing sample size, stale-history risk, regime imbalance, and unequal fold dependence are assessed.

## 10. Expanding Window Rules

Expanding designs define growth rule, retained history, weighting assumptions, validation placement, test cadence, and when older information may cease to be relevant.

## 11. Train / Validation / Test Rules

Training fits and selects; validation supports training-contained choices; test measures untouched generalization. Test results cannot select parameters for that test fold. Final holdouts remain protected from iterative design.

## 12. Out-of-Sample Integrity Rules

OOS evidence requires versioned data, unavailable outcomes at decision time, training-only transformation fitting, no label leakage, no repeated discretionary access, and complete custody. Contaminated OOS is reclassified, never repaired by renaming.

## 13. Reoptimization Rules

Reoptimization frequency, eligible data, search space, objective, constraints, pruning, budget, seeds, selection, fallback, and failure behavior are preregistered. Reoptimization occurs inside each fold without test leakage.

## 14. Parameter Selection Discipline

Selection records candidate population, stable regions, ties, failures, constraints, validation logic, and final choice. Cherry-picking from test results is prohibited. Parameter-frozen assessments state why no adaptation is allowed.

## 15. Window Sensitivity Rules

Assessment tests defensible alternative starts, ends, lengths, steps, ratios, embargoes, and overlap. Sensitivity analysis is preregistered or labeled exploratory; favorable boundaries cannot be selected after observation.

## 16. Regime Coverage Rules

Each fold cites exact RCS records, distribution, confidence, transitions, unknown states, and sample sufficiency. Regime imbalance, absence, and clustered failure qualify the robustness claim.

## 17. Market and Timeframe Coverage Rules

Cross-market/timeframe evidence defines transfer rationale, comparability, data construction, costs, liquidity, frequency, exclusions, and expected degradation. Results cannot be pooled across incomparable contexts without disclosure.

## 18. Fold-Level Evidence Requirements

Each fold records identity; train/validation/test dates; data version; regimes; feature status; selection path and parameters; costs/execution; primary, secondary and risk metrics; trades/signals; drawdown, tails and worst trade; verdict, limitations, contradictions, failure mode, and reproducibility material.

Every fold is reported, including failed, interrupted, low-sample, and excluded folds.

## 19. Fold Aggregation Rules

Aggregation preregisters weighting, metrics, failed/low-sample/regime-imbalanced/missing-data treatment, dispersion, uncertainty, boundary sensitivity, contradictions, and classification logic.

Means are accompanied by distributions, worst cases, failure counts, persistence, and concentration. Catastrophic or repeated failure cannot be averaged away.

## 20. Temporal Degradation Rules

Degradation assessment examines fold sequence, OOS decay, drawdown/tail worsening, cost growth, signal/trade collapse, regime concentration, parameter instability, recovery, and structural breaks.

## 21. Robustness Metric Rules

Metrics cover OOS expectancy, profit factor, risk-adjusted return, drawdown, duration, tails, worst loss, trade/signal counts, fold pass rate, dispersion, stability, cost/execution sensitivity, and degradation. Definitions and conflicts are fixed by XDS.

## 22. Robustness Threshold Rules

Acceptance, limitation, fragility, failure, invalidity, sample, fold, degradation, and contradiction thresholds are defined before results. No metric may override hard leakage, integrity, or catastrophic-failure criteria.

## 23. Robustness Failure Rules

Failure or downgrade includes repeated or catastrophic OOS failure, IS/OOS divergence, unstable folds, single-period/regime/parameter dependence, unacceptable drawdown/tails, count collapse/explosion, excessive cost/execution sensitivity, invalid exclusion, leakage, post-result changes, insufficient folds, coverage/data failure, or contradiction with edge/family rationale.

## 24. Robustness Classification Model

Authorized classifications are `ROBUST`, `ROBUST WITH LIMITATIONS`, `FRAGILE`, `INCONCLUSIVE`, `FAILED`, and `INVALID`. Classification states exact scope and decisive evidence.

## 25. Robustness Confidence Model

Authorized confidence states are `HIGH`, `MEDIUM`, `LOW`, `INSUFFICIENT`, and `CONFLICTED`, reflecting independence, folds, coverage, data, consistency, contradictions, and uncertainty.

## 26. Robustness Maturity Model

Authorized maturity states are `DESIGNED`, `EXECUTED`, `EVIDENCE_READY`, `VALIDATION_CANDIDATE`, `RETURNED`, `REJECTED`, and `SUPERSEDED`. Maturity is not Validation.

## 27. Walk-Forward Deviation Rules

Every deviation states what, why, when, authority, whether results were known, affected folds, scientific impact, and required downgrade/restart. Silent exclusions or window changes invalidate the affected claim.

## 28. Robustness Evidence Packaging

The frozen package contains identity/version; XDS; strategy/implementation and all contexts; data/period; partitions/windows/folds; reoptimization/selection; costs/execution; complete fold results; exclusions; aggregation; metrics; degradation and sensitivities; classifications; limitations, contradictions, prohibited interpretations, deviations, custody, and follow-up.

## 29. Robustness Audit and Reconstruction

Independent reviewers must reproduce fold construction, chronological decisions, selections, results, exclusions, aggregation, and classification from exact versions. Historical OOS status cannot be rewritten.

## 30. Integration with MACP

MACP governs design intake, partition approval, execution, fold reporting, aggregation, challenge, classification, handoff, return, rejection, supersession, and archival.

## 31. Integration with SMI

SMI holds current state, locks, folds, selections, blockers, deviations, and handoff. It cannot mutate frozen partitions or evidence.

## 32. Integration with EES

All fold and aggregate claims use EES provenance, scope, uncertainty, limitations, contradictions, versions, custody, and admissibility.

## 33. Integration with WOE

WOE enforces partition, authorization, fold, review, aggregation, classification, packaging, and return gates.

## 34. Integration with Agent Registry

Only registered agents may design, coordinate, execute, review, classify, or consume WFRS outputs within contract rights. Assessment cannot validate itself.

## 35. Integration with Artifact Registry

Plans, partitions, folds, selections, exclusions, aggregation, classifications, packages, challenges, and archives are governed ART artifacts.

## 36. Integration with Strategy Lifecycle Standard

WFRS provides robustness evidence for Experiment Executed and Validation Review. Material strategy changes invalidate applicability and trigger lifecycle return.

## 37. Integration with Autonomous Research Pipeline

ARP routes eligible XDS experiments through WFRS to EEP and cannot advance on summary results or missing folds.

## 38. Integration with Experiment Design Standard

WFRS consumes and preserves frozen XDS scope, hypotheses, metrics, partitions, costs, controls, criteria, reproducibility, and deviation rules.

## 39. Integration with Experiment Evidence Package

EEP packages actual WFRS conduct and complete results. It cannot omit failed folds or rewrite classifications.

## 40. Integration with Validation Evidence Package

VEP independently assesses partition integrity, reproducibility, robustness scope, fold failures, degradation, and contradictions. WFRS cannot grant Validation.

## 41. Integration with Risk Review Package

RRP consumes validated temporal, drawdown, tail, cost, execution, regime, and degradation evidence without broadening scope.

## 42. Integration with Monitoring and Edge Decay Standard

WFRS establishes historical temporal and degradation baselines; MEDS compares forward behavior without treating simulated limits as guaranteed live bounds.

## 43. Governance

Mandatory types include Rolling, Anchored, Expanding, Nested, Purged, Embargoed, Regime-Aware, Market-Aware, Timeframe-Aware, Parameter-Frozen, Reoptimized, Forward Paper, and Failure-Reproduction Walk-Forward.

Every assessment preserves chronology, partitions, all folds, selection, costs, execution, regimes, aggregation, failures, uncertainty, limitations, custody, and audit history. Frozen records cannot be edited in place; amendments create versions. Exceptions cannot legalize leakage, hidden folds, post-result repartitioning, metric replacement, or one-fold robustness.

Every future AI Quant Lab Walk-Forward, rolling/anchored/expanding/nested assessment, temporal validation, and robustness claim must conform to WFRS before EEP or VEP reliance.
