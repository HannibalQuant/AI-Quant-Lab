# Parameter Stability Standard (PSS) v1.0

## Specification Control

| Field | Value |
|---|---|
| Standard ID | `AIQL-PSS` |
| Version | `1.0.0` |
| Status | Proposed for Sprint 39 review |
| Scope | Every institutional parameter-stability, selection, and robust-island claim |
| Authority | XDS, WFRS, MCSTS, EEP, VEP, RRP, DGS, MEDS, EES, ART, and parameter governance |

PSS governs whether strategy behavior and risk persist across defensible parameter neighborhoods rather than isolated optimized points. It is not an optimizer, Validation, Risk approval, or proof of future performance.

## 1. Parameter Stability Philosophy

Parameters operationalize architecture; they do not manufacture edge. A defensible parameter choice should lie in a region where minor, plausible changes do not cause disproportionate performance or risk collapse.

Stability includes visibility of cliffs, interactions, boundaries, failure zones, and conditional dependence. Smooth mediocrity is not automatically desirable, and a spectacular isolated peak is not robustness.

## 2. Parameter Stability Principles

No claim proceeds without XDS, parameter scope, search-space integrity, preregistered neighborhoods, sensitivity, interactions, boundaries, temporal/regime/cost/execution/risk review, failure zones, and auditability. One optimized point, best trial, or final equity cannot establish stability. Silent exclusions/search changes, post-result neighborhoods, cherry-picked islands, and hidden fragility are prohibited.

## 3. Parameter Stability Identity Model

Every assessment has permanent Stability ID, Record ID, and exact version. Identity binds XDS, WFRS, MCSTS, experiment, strategy/implementation, market, data, parameters, search space, neighborhoods, and owner. Material scope, range, metric, threshold, or interaction-plan change creates a new version or identity.

## 4. Parameter Stability Object Model

The record defines upstream identities; market and data context; optimization/backtest/WFRS/MCSTS sources; parameter names, types, roles, fixed/variable/excluded/conditional/derived status; search-space rationale, neighborhoods, grids, sampling, constraints, dependencies, interactions, boundaries; candidate/selected/alternative/rejected sets; robust islands, peaks, cliffs, fragile/failure zones; stability/sensitivity/risk/cost/execution metrics; temporal/regime/market/timeframe/feature/WFRS/MCSTS results; drift; classifications; limitations, contradictions, deviations, follow-up; integrations, timestamps, custody, and audit trail.

## 5. Parameter Stability Lifecycle

**Proposed → Design Received → Parameter Scope Registered → Search Space Reviewed → Neighborhood Plan Registered → Sensitivity Plan Registered → Execution Authorized → Stability Assessment Executed → Island Review → Interaction Review → Boundary Review → Stability Classified → Evidence Packaged → Returned → Rejected → Challenged → Superseded → Archived**

Authorization freezes confirmatory scope. Completion does not grant downstream approval.

## 6. Parameter Scope Rules

Scope identifies every parameter, role, unit, domain, dependency, strategy module, applicable market/timeframe/regime, data version, and intended claim. Omitted parameters require rationale and impact analysis.

## 7. Parameter Classification Rules

Mandatory types include Entry, Exit, Filter, Regime, Feature, Risk, Stop, Take-Profit, Trailing, Time-Based, Volatility, Volume, Liquidity, Position-Sizing, Portfolio, Execution, Cost, Meta, Fixed, Conditional, and Derived Parameters.

Classification cannot hide a tuned value as fixed or derived.

## 8. Parameter Neighborhood Rules

Each neighborhood defines identity, center/reference, range, step or sampling, rationale, type/role, boundaries, exclusions, constraints, dependencies, expected metrics/degradation, failure thresholds, feature/regime/cost/risk context, and reproducibility.

Neighborhoods are preregistered before interpretation.

## 9. Robust Parameter Island Rules

An island is a connected or defensibly related region with acceptable distributions of performance, risk, trade count, drawdown, tails, costs, execution, regimes, temporal folds, and stochastic stress.

Each island records dimensions, ranges, center, boundaries, density, failure edges, coverage, contradictions, and confirmatory/exploratory status.

## 10. Isolated Peak and Cliff Rules

Assessment identifies single-point peaks, narrow ridges, unstable boundaries, discontinuities, interaction traps, suspicious precision, boundary optima, sharp local degradation, and adjacent failure zones.

Isolated peaks cannot support a stability claim without independent evidence and explicit limitation.

## 11. Parameter Sensitivity Rules

Sensitivity measures magnitude, direction, smoothness, asymmetry, nonlinearity, local/global effects, risk consequences, and uncertainty under preregistered perturbations.

## 12. Parameter Interaction Rules

Review covers pairs/groups, conditional, redundant, compensating, conflicting, regime/cost/execution/risk-dependent relationships, and whether one parameter merely absorbs another’s fragility.

## 13. Boundary Behavior Rules

Selected values near search boundaries require evidence that the boundary is scientifically justified rather than truncating an optimum. Boundary expansion, prohibited zones, discontinuities, and failure behavior remain visible.

## 14. Search Space Integrity Rules

Search spaces derive from architecture, mechanism, plausible measurement, constraints, and data resolution—not favorable outcomes. All revisions are versioned with timing, rationale, and result-visibility impact.

## 15. Optimization Result Intake Rules

Intake verifies objective, sampler, trials, seeds, constraints, pruning, partitions, all-trial reporting, failures, selection, and overfitting controls. Best-trial intake is insufficient without the candidate population.

## 16. Stability Metric Rules

Metrics cover neighborhood acceptance, connectedness, dispersion, gradients, cliffs, rank persistence, expectancy, PF, drawdown, tails, worst trade, counts, costs, execution, and parameter-selection frequency.

## 17. Stability Threshold Rules

Stable, limited, fragile, failed, invalid, island, cliff, boundary, degradation, and coverage thresholds are preregistered. Hard risk or integrity failures override favorable averages.

## 18. Temporal Stability Rules

Parameters are assessed across chronological periods, starts/ends, structural breaks, and decay. Later performance cannot determine earlier selected values.

## 19. Walk-Forward Stability Rules

WFRS evidence records selected values and islands across folds, frequency, migration, dispersion, regime relationship, and OOS consequences without test leakage.

## 20. Monte Carlo Stability Rules

MCSTS perturbs parameters jointly where dependencies matter and reports distributional degradation, survival, failure, tails, and interaction sensitivity.

## 21. Regime Stability Rules

Assessment cites exact RCS records and distinguishes universal, conditional, adaptive, transition-sensitive, and out-of-scope parameter behavior.

## 22. Market Stability Rules

Cross-market assessment defines transfer rationale, scale, liquidity, costs, structure, and expected degradation. Market-specific stability cannot be generalized silently.

## 23. Timeframe Stability Rules

Timeframe tests address construction, sampling, opportunity frequency, costs, lag scaling, and non-equivalent parameter meaning.

## 24. Feature Stability Rules

Assessment cites exact FFS versions and tests parameter dependence on feature drift, transformations, redundancy, missingness, and alternative measurements.

## 25. Cost and Execution Stability Rules

Neighborhoods are evaluated under baseline and adverse costs, spread, slippage, latency, fills, missed actions, liquidity, and capacity. Performance-only islands that collapse under friction are fragile.

## 26. Risk Stability Rules

Risk review covers drawdown, duration, tails, worst trade, loss clusters, exposure, leverage, concentration, liquidation, risk-of-ruin, and control behavior across neighborhoods.

## 27. Parameter Drift Rules

Drift records changes in optimal regions, stable islands, distributions, selection frequency, performance/risk gradients, and regime relationship. Drift does not authorize automatic retuning.

## 28. Parameter Fragility Rules

Fragility includes narrow acceptable regions, steep gradients, unstable interactions, boundary dependence, fold migration, cost sensitivity, regime concentration, and nearby failure zones.

## 29. Stability Failure Rules

Failure/downgrade includes one-point peaks, narrow ridges, adjacent cliffs, excessive minor-change sensitivity, single-parameter/interaction dependence, unjustified boundary optimum, unstable WFRS/MCSTS behavior, regime/cost/execution collapse, drawdown/tail instability, count collapse/explosion, hidden exclusions, post-result changes, upstream contradiction, inadequate coverage, or irreproducibility.

## 30. Stability Classification Model

Authorized classifications are `STABLE`, `STABLE WITH LIMITATIONS`, `FRAGILE`, `INCONCLUSIVE`, `FAILED`, and `INVALID`, each with exact scope and decisive evidence.

## 31. Stability Confidence Model

Authorized states are `HIGH`, `MEDIUM`, `LOW`, `INSUFFICIENT`, and `CONFLICTED`, based on coverage, evidence independence, consistency, uncertainty, and contradictions.

## 32. Stability Maturity Model

Authorized states are `DESIGNED`, `EXECUTED`, `EVIDENCE_READY`, `VALIDATION_CANDIDATE`, `RISK_REVIEW_CANDIDATE`, `RETURNED`, `REJECTED`, and `SUPERSEDED`.

## 33. Deviation and Amendment Rules

Every deviation states what, why, when, authority, result visibility, affected regions, and scientific impact. Post-result scope or neighborhood changes downgrade confirmatory status or require a new version.

## 34. Parameter Stability Evidence Packaging

The frozen package contains identity/version; XDS/WFRS/MCSTS; strategy and contexts; data and inputs; parameter scope/types; search space; selected/alternative/rejected/fixed/excluded sets; neighborhoods, islands, peaks, cliffs, fragile/failure zones; interactions, sensitivities, temporal/regime/cost/execution/risk results; classifications; limitations, contradictions, prohibited interpretations, deviations, custody, and follow-up.

## 35. Parameter Stability Audit and Reconstruction

Independent reviewers must reproduce search-space intake, neighborhoods, runs, metrics, islands, failures, interactions, classifications, and selected parameters from exact versions. Historical regions cannot be rewritten.

## 36. Integration with MACP

MACP governs intake, scope, plans, authorization, assessment, island/interaction/boundary review, classification, challenge, handoff, return, rejection, and archive.

## 37. Integration with SMI

SMI holds current state, locks, parameter sets, neighborhoods, blockers, deviations, and handoff; it cannot mutate frozen evidence.

## 38. Integration with EES

All stability claims use EES provenance, scope, uncertainty, contradictions, versions, custody, and admissibility.

## 39. Integration with WOE

WOE enforces design, scope, search, neighborhood, execution, review, classification, packaging, and return gates.

## 40. Integration with Agent Registry

Only registered agents may design, execute, review, classify, or consume stability evidence within rights. Optimization cannot approve itself.

## 41. Integration with Artifact Registry

Scopes, spaces, neighborhoods, runs, islands, peaks, cliffs, classifications, packages, challenges, and archives are governed ART artifacts.

## 42. Integration with Strategy Lifecycle Standard

PSS supports Experiment Executed and Validation Review; material parameter or logic changes trigger SLS version and revalidation consequences.

## 43. Integration with Autonomous Research Pipeline

ARP routes eligible experiments through PSS and cannot advance on a best trial or selected point alone.

## 44. Integration with Experiment Design Standard

PSS consumes and preserves XDS scope, metrics, costs, controls, criteria, and reproducibility.

## 45. Integration with Walk-Forward and Robustness Standard

WFRS supplies fold-level temporal selection and OOS evidence. PSS cannot replace or aggregate away fold instability.

## 46. Integration with Monte Carlo and Stress Testing Standard

MCSTS supplies stochastic parameter, cost, execution, tail, and failure distributions. PSS preserves its limitations and scenarios.

## 47. Integration with Experiment Evidence Package

EEP packages actual PSS conduct, candidate population, failures, deviations, classifications, and custody.

## 48. Integration with Validation Evidence Package

VEP independently assesses scope, stability, leakage, selection, peaks, cliffs, interactions, reproducibility, and contradictions. PSS is not Validation.

## 49. Integration with Risk Review Package

RRP consumes validated risk variation across neighborhoods and may impose stricter limits without treating stability as Risk approval.

## 50. Integration with Deployment Governance Standard

DGS locks exact approved parameter and configuration versions. Any mismatch or unauthorized retuning blocks or suspends operation.

## 51. Integration with Monitoring and Edge Decay Standard

MEDS observes parameter/configuration integrity, drift, feature/regime dependence, and deviation from approved islands. Drift triggers review, not automatic optimization.

## 52. Governance

Mandatory dimensions are local/global, islands, cliffs, interactions, temporal/WFRS/regime/market/timeframe/feature/cost/execution/risk/drawdown/tail/count/PF/expectancy/worst-trade/MCSTS/drift stability and failure-zone visibility.

All selected, alternative, rejected, fixed, excluded, and conditional parameters plus adverse regions remain visible. Frozen records cannot be edited in place; amendments create versions. Exceptions cannot legalize best-trial claims, hidden spaces, post-result neighborhoods, cherry-picked islands, or absent failure zones.

Every future AI Quant Lab parameter-stability, robust-island, optimization-reliance, parameter-selection, and parameter-dependent robustness claim must conform to PSS before EEP, VEP, RRP, DGS, or MEDS reliance.
