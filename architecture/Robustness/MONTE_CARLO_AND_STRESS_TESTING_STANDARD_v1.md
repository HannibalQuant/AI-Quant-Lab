# Monte Carlo & Stress Testing Standard (MCSTS) v1.0

## Specification Control

| Field | Value |
|---|---|
| Standard ID | `AIQL-MCSTS` |
| Version | `1.0.0` |
| Status | Proposed for Sprint 38 review |
| Scope | Every institutional Monte Carlo, perturbation, adversarial, and stress claim |
| Authority | XDS, WFRS, EEP, VEP, RRP, DGS, MEDS, EES, ART, and stress governance |

MCSTS governs stochastic and adversarial testing of path dependency, costs, execution, parameters, data, regimes, liquidity, tails, capacity, and portfolio interactions. It is not Validation, Risk approval, Deployment authority, an optimizer, or proof of future performance.

## 1. Monte Carlo and Stress Testing Philosophy

Stress testing asks how conclusions change when defensible adverse conditions replace convenient assumptions. Monte Carlo describes distributions conditional on a model of randomness; it does not reveal unknowable future probabilities without model risk.

Every perturbation must state what structure it preserves, what it destroys, and why that trade-off answers the declared question.

## 2. Monte Carlo and Stress Testing Principles

No test proceeds without XDS, stress scope, rationale, seed policy, reproducibility, scenario breadth, distribution evidence, and preregistered survival/failure thresholds. Cost, execution, liquidity, parameter, data, portfolio, tail, and drawdown claims require corresponding stress. Silent perturbation/seed/scenario changes, post-result redesign, favorable-only reporting, and excluded adverse scenarios are prohibited.

## 3. Monte Carlo and Stress Test Identity Model

Every program has permanent Stress Test ID, Record ID, and version. Identity binds XDS/WFRS, experiment, strategy/implementation, market, data, inputs, perturbations, scenarios, seed policy, and owner. Material scope, distribution, seed, threshold, or scenario change creates a new version or identity.

## 4. Monte Carlo and Stress Test Object Model

The record defines all upstream identities; market, venue, instrument, timeframe, data/period; input result/trade/equity sources; scope, perturbations and rationale; randomization, seeds, simulations/scenarios; baseline/adversarial cases; sequence, return, equity, parameter, feature, data, cost, slippage, spread, delay, missed/partial fill, liquidity, capacity, tail, gap, regime and portfolio assumptions; metrics/distributions; survival/failure thresholds; scenario verdicts; classifications; exclusions, deviations, limitations, contradictions, follow-up; integrations, timestamps, custody, and audit trail.

## 5. Monte Carlo and Stress Test Lifecycle

**Proposed → Design Received → Stress Scope Registered → Perturbation Plan Registered → Randomization Reviewed → Seed Policy Registered → Execution Authorized → Simulation Execution → Scenario Review → Distribution Review → Stress Classified → Evidence Packaged → Returned → Rejected → Challenged → Superseded → Archived**

Authorization freezes the confirmatory stress plan. Completion does not grant evidence eligibility.

## 6. Stress Scope Rules

Scope fixes exact strategy, implementation, input evidence, markets, periods, regimes, parameters, features, costs, execution, portfolio, assumptions, stress severities, and intended downstream claim.

## 7. Randomization and Seed Governance

Randomization states generator assumptions, sampling unit, replacement, dependence, stratification, preserved/destroyed structure, seeds, seed count, reproducibility, and prohibited reselection. Seeds are registered before outcomes and all registered seed summaries are reported.

## 8. Perturbation Design Rules

Each perturbation defines rationale, target assumption, distribution or scenario, severity, direction, dependencies, preserved/destroyed properties, expected failure, metrics, thresholds, and limitations.

## 9. Trade-Sequence Monte Carlo Rules

Shuffle and bootstrap designs address trade-order and sampling risk. Where clustering, serial dependence, regime sequence, or overlapping exposure matters, block or conditional methods are required or the destroyed structure is an explicit limitation.

## 10. Return Perturbation Rules

Return perturbations define additive/multiplicative behavior, dependence, volatility, tails, autocorrelation, gaps, regime conditioning, and whether strategy decisions are recalculated or only outcomes perturbed.

## 11. Equity Curve Perturbation Rules

Equity perturbations declare whether paths preserve trades, compounding, exposure, withdrawals, margin, and chronology. Perturbing an equity curve cannot stand in for execution-aware strategy simulation.

## 12. Parameter Perturbation Rules

Perturbations cover defensible neighborhoods, joint dependencies, boundaries, stable islands, interaction effects, and failure outside selected points. Random parameter noise cannot hide an unjustified original range.

## 13. Feature Perturbation Rules

Tests cite exact FFS versions and perturb values, missingness, timing, noise, drift, dependencies, and redundancy without introducing future information.

## 14. Data Perturbation Rules

Tests cover missing, stale, duplicated, reordered, revised, corrupted, delayed, biased, or source-shifted data and state which failure behavior and safe response are expected.

## 15. Cost Stress Rules

Cost inflation includes fees, funding, borrowing, impact, turnover, and compounded friction under baseline, adverse, and severe assumptions with defensible provenance.

## 16. Slippage Stress Rules

Slippage stress conditions on liquidity, volatility, size, direction, gaps, venue, and regime. Constant inflation alone is insufficient when asymmetry or tails are material.

## 17. Spread Stress Rules

Spread scenarios cover level, variability, widening, sessions, events, liquidity contraction, and interaction with order timing and trade frequency.

## 18. Execution Delay Stress Rules

Delay stress defines decision-to-order and order-to-fill delays, missed state transitions, price movement, stale signals, and exit impairment.

## 19. Missed-Trade and Partial-Fill Stress Rules

Tests define selection or random mechanism, dependence, fill fraction, position reconciliation, residual exposure, opportunity concentration, and whether missing favorable/adverse trades is asymmetric.

## 20. Liquidity and Capacity Stress Rules

Scenarios cover shrinking liquidity, widening costs, reduced depth, participation limits, impact, exit time, crowding, venue loss, and capital scaling. Volume alone cannot define capacity.

## 21. Tail Event and Gap Stress Rules

Tests include discontinuities beyond ordinary samples, clustered extremes, stop bypass, liquidation, correlation spikes, unavailable exits, asymmetric tails, and recovery assumptions.

## 22. Regime Stress Rules

Scenarios cite RCS and test regime shifts, transitions, persistence changes, unknown states, misclassification, delayed detection, and operation outside authorized scope.

## 23. Portfolio Interaction Stress Rules

Tests cover correlation convergence, drawdown and tail dependence, factor crowding, liquidity overlap, gross/net exposure, simultaneous failure, and constrained exit priority.

## 24. Adversarial Stress Rules

Adversarial scenarios deliberately combine plausible unfavorable assumptions without optimizing solely to guarantee failure. Severity, plausibility, interactions, and institutional question are explicit.

## 25. Survival and Failure Threshold Rules

Thresholds define survival, limitation, fragility, failure, ruin, drawdown, tails, loss clusters, costs, execution, liquidity, capacity, and coverage before results. Mild-stress survival cannot imply severe-stress survival.

## 26. Monte Carlo Metric Rules

Metrics include probability of loss, defined failure/ruin, drawdown breach, expectancy/PF distributions, max drawdown, duration, tails, worst trade, loss clusters, survival/failure rate, and sample uncertainty.

## 27. Stress Test Metric Rules

Scenario metrics measure absolute outcome, degradation from baseline, threshold distance, control response, recovery, operational containment, and contradiction with XDS/WFRS/EDS assumptions.

## 28. Distribution and Confidence Output Rules

Outputs include median, mean where meaningful, dispersion, percentiles, worst/best observed simulations, loss/drawdown/ruin probabilities, expectancy, PF, max-drawdown, tail/worst-trade distributions, survival/failure rates, and uncertainty statement.

Finite simulation estimates and model uncertainty remain explicit.

## 29. Scenario Comparison Rules

Comparisons use registered baseline, severity ladder, consistent metrics, preserved assumptions, and transparent differences. Cross-scenario aggregation cannot hide decisive failures.

## 30. Stress Failure Rules

Failure/downgrade includes unacceptable drawdown/tail/ruin probability, severe sequence/cost/slippage/spread/missed-trade/delay/liquidity/capacity/parameter/feature/data/regime/portfolio sensitivity, realistic adverse failure, invalid evidence, ungoverned seeds, post-result redesign, or unjustified scenario exclusion.

## 31. Stress Classification Model

Authorized classifications are `STRESS RESILIENT`, `STRESS RESILIENT WITH LIMITATIONS`, `STRESS FRAGILE`, `STRESS INCONCLUSIVE`, `STRESS FAILED`, and `STRESS INVALID`.

## 32. Stress Confidence Model

Authorized confidence states are `HIGH`, `MEDIUM`, `LOW`, `INSUFFICIENT`, and `CONFLICTED`, based on design, simulations, scenarios, dependencies, reproducibility, contradictions, and uncertainty.

## 33. Stress Maturity Model

Authorized maturity states are `DESIGNED`, `EXECUTED`, `EVIDENCE_READY`, `VALIDATION_CANDIDATE`, `RISK_REVIEW_CANDIDATE`, `RETURNED`, `REJECTED`, and `SUPERSEDED`.

## 34. Deviation and Amendment Rules

Every change records what, why, when, authority, result visibility, affected scenarios, and scientific impact. Material post-result changes downgrade confirmatory status or require a new version.

## 35. Stress Evidence Packaging

The frozen package contains identity/version; XDS/WFRS; strategy/implementation and all contexts; data and input sources; perturbations, preserved/destroyed structure, seeds, simulations, scenarios, assumptions; distributions; failures/exclusions; thresholds; classifications; limitations, contradictions, prohibited interpretations, deviations, custody, and follow-up.

## 36. Stress Audit and Reconstruction

Independent reviewers must reproduce registered simulations, scenarios, seeds, transformations, distributions, verdicts, exclusions, and classifications. Historical plans cannot be rewritten.

## 37. Integration with MACP

MACP governs design intake, registration, authorization, execution, scenario/distribution review, classification, challenge, handoff, return, rejection, and archival.

## 38. Integration with SMI

SMI holds current state, locks, seeds, scenarios, blockers, deviations, and handoff; it cannot mutate frozen evidence.

## 39. Integration with EES

Every perturbation, scenario, distribution, classification, contradiction, and limitation is an EES object with provenance, scope, versions, uncertainty, and custody.

## 40. Integration with WOE

WOE enforces plan, randomization, seed, execution, review, classification, packaging, and return gates.

## 41. Integration with Agent Registry

Only registered agents may design, execute, review, classify, or consume stress evidence within rights. Testing cannot validate or approve itself.

## 42. Integration with Artifact Registry

Plans, seeds, scenarios, runs, distributions, classifications, packages, challenges, exclusions, and archives are governed ART artifacts.

## 43. Integration with Strategy Lifecycle Standard

MCSTS supports Experiment Executed and Validation Review; material strategy change invalidates applicability.

## 44. Integration with Autonomous Research Pipeline

ARP routes eligible experiments through MCSTS and cannot advance based on selected favorable scenarios.

## 45. Integration with Experiment Design Standard

MCSTS consumes and preserves XDS scope, metrics, costs, controls, criteria, and reproducibility.

## 46. Integration with Walk-Forward and Robustness Standard

WFRS temporal evidence supplies input and context. MCSTS tests stochastic/adversarial sensitivity without replacing fold evidence.

## 47. Integration with Experiment Evidence Package

EEP packages actual stress conduct, all registered summaries, failures, deviations, and custody.

## 48. Integration with Validation Evidence Package

VEP independently assesses design, dependency preservation, reproducibility, thresholds, failures, and scope. MCSTS is not Validation.

## 49. Integration with Risk Review Package

RRP consumes validated tail, drawdown, liquidity, capacity, execution, portfolio, and survival evidence without converting simulation into certainty.

## 50. Integration with Deployment Governance Standard

DGS uses approved stress assumptions for limits, controls, kill paths, rollback, and readiness but cannot treat stress survival as Deployment authority.

## 51. Integration with Monitoring and Edge Decay Standard

MEDS uses stress distributions and failure scenarios as baselines and triggers, while observed live evidence may challenge stress assumptions.

## 52. Governance

Mandatory types include Trade Shuffle/Bootstrap/Block Bootstrap; Return, Equity, Parameter, Feature, and Data Perturbation; Cost, Slippage, Spread, Delay, Missed/Partial Fill, Liquidity, Capacity, Tail, Gap, Regime Shift/Misclassification, Portfolio Correlation, Drawdown Clustering, Adversarial, Failure Reproduction, and Forward Paper stress.

All registered simulations, scenarios, failures, exclusions, seeds, distributions, thresholds, limitations, and custody remain visible. Frozen records cannot be edited in place; amendments create versions. Exceptions cannot legalize favorable-only reporting, seed replacement, hidden scenarios, or post-result redesign.

Every future AI Quant Lab Monte Carlo and stress claim must conform to MCSTS before EEP, VEP, RRP, DGS, or MEDS reliance.
