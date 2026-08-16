# Experiment Design Standard (XDS) v1.0

## Specification Control

| Field | Value |
|---|---|
| Standard ID | `AIQL-XDS` |
| Version | `1.0.0` |
| Status | Proposed for Sprint 36 review |
| Scope | Every institutional experiment before result interpretation |
| Authority | Research OS, ARP, SLS, MDRS, RCS, FFS, EDS, SFSS, EES, EEP, VEP, and experiment governance |

XDS governs how experiments are designed, preregistered, scoped, controlled, authorized, amended, interpreted, frozen, and handed to EEP. It is not code, an optimizer, Validation, Risk approval, or a trading system. A result is institutional evidence only when its design existed before the result was interpreted.

## 1. Experiment Design Philosophy

Experiment design separates what was expected from what was discovered. It makes hypotheses, data choices, metrics, criteria, controls, assumptions, and failure paths visible before outcomes can influence them.

Good design permits an experiment to fail clearly. Ambiguous success criteria and post-result scope changes manufacture narratives rather than knowledge.

## 2. Experiment Design Principles

No experiment proceeds without identity, purpose, preregistered scope, hypothesis, null, data plan, costs, execution assumptions, metrics, acceptance/failure/stopping criteria, controls, negative-control review, reproducibility, and auditability. Confirmatory status cannot be assigned after seeing results. Optimization requires fixed search space and overfitting controls; Walk-Forward requires temporal discipline; Monte Carlo requires perturbation rationale. Silent amendments, metric replacement, selective reporting, and out-of-scope interpretation are prohibited.

## 3. Experiment Identity Model

Every experiment has permanent Experiment ID, Record ID, and exact version. Identity binds purpose, question, strategy, market, regime, features, edge, family, architecture, implementation, data, and owner. Material hypothesis, scope, partition, primary metric, or design change requires a new experiment or governed version.

## 4. Experiment Object Model

The record defines identity/owner/type; purpose/scope/question; Strategy and upstream MDRS/RCS/FFS/EDS/SFSS records; architecture and implementation; data/version/coverage/partitions; variables, fixed/excluded parameters and search space; costs and execution; primary/secondary/risk/robustness metrics; acceptance, failure and stopping criteria; positive/negative controls and baselines; randomization/seeds; robustness plans; reproducibility; deviations/amendments; output eligibility; limitations, risks, contradictions, follow-up; MACP, SMI, EES, ART, WOE, Agent references; timestamps and audit trail.

## 5. Experiment Design Lifecycle

**Proposed → Design Drafted → Scope Registered → Hypotheses Registered → Data Plan Registered → Controls Registered → Metrics Registered → Acceptance Criteria Registered → Execution Authorized → Running → Completed → Deviation Review → Evidence Eligible → Returned → Rejected → Superseded → Archived**

Execution authorization freezes the design baseline. Completion alone does not grant evidence eligibility.

## 6. Experiment Purpose and Scope Rules

Purpose states the decision-relevant question and intended consumer. Scope fixes markets, instruments, timeframes, regimes, periods, data, strategy/implementation versions, features, edge, family, assumptions, and prohibited generalization.

## 7. Preregistration Rules

Preregistration timestamps and freezes the design before results are available. It identifies confirmatory and exploratory components, owners, amendments, blind or protected data, and publication obligations.

## 8. Hypothesis and Null Model Rules

The record defines primary hypothesis, null, alternatives, mechanism, expected direction/magnitude, failure conditions, and discriminating evidence. The null must be capable of surviving testing.

## 9. Variable and Parameter Scope Rules

Independent, dependent, controlled, nuisance, derived, and observed variables are defined with versions and timing. Fixed parameters, search space, exclusions, constraints, conditional relationships, and degrees of freedom are preregistered.

## 10. Data Partition and Temporal Scope Rules

Train, validation, test, untouched holdout, and external replication partitions are fixed before access to outcomes. Temporal order, embargo, overlap, preprocessing fit, repeated access, and leakage prevention are explicit.

## 11. Cost and Execution Assumption Rules

Design specifies spread, slippage, fees, funding, borrowing, latency, fills, partial fills, gaps, liquidity, capacity, order timing, sizing, and unavailable-execution behavior. Zero or unknown costs require justification and sensitivity limits.

## 12. Metric Selection Rules

Primary metric follows the research question; secondary, risk, robustness, and diagnostic metrics have declared roles. Definitions, aggregation, uncertainty, multiplicity, missing outcomes, and conflicts are specified before results.

## 13. Acceptance and Failure Criteria Rules

Acceptance, rejection, failure, stopping, continuation, replication, and inconclusive criteria are measurable, scoped, and preregistered. No single favorable metric may override a hard failure criterion.

## 14. Control Experiment Rules

Positive controls test whether the design detects a known effect; baselines define meaningful comparison; process controls verify data, implementation, and measurement integrity. Control failure qualifies or invalidates outputs.

## 15. Negative Control Rules

Controls may randomize timing, labels, regimes, thresholds, features, markets, or temporal structure and stress costs, execution, and missed actions. Expected failure behavior and progression-blocking outcomes are preregistered.

## 16. Robustness Experiment Design Rules

Robustness covers temporal, regime, market, timeframe, parameter, feature, data, cost, execution, perturbation, and replication dimensions. Tests must be independent enough to add information rather than repeat equivalent samples.

## 17. Exploratory Experiment Rules

Exploratory work discovers candidate relationships and may adapt transparently. It cannot generate confirmatory claims without later independent preregistration. All explored alternatives and multiplicity remain visible.

## 18. Confirmatory Experiment Rules

Confirmatory work uses frozen hypotheses, scope, data, metrics, controls, and criteria. Post-result deviations downgrade confirmatory status and require explicit impact assessment.

## 19. Optimization Experiment Rules

Optimization defines objective, search space, constraints, sampler, pruning, trials, seeds, train-only decisions, selection rules, tie-breaking, all-trial reporting, multiple-testing and overfitting controls. Best output is a candidate, not proof.

## 20. Walk-Forward Experiment Design Rules

Design specifies rolling or anchored windows, train/validation/test boundaries, training-only selection, reoptimization, embargo, leakage controls, aggregation, minimum folds, regime representation, and failure thresholds.

## 21. Monte Carlo Experiment Design Rules

Design specifies perturbation type and rationale, dependence preservation, sample count, randomization, seed policy, outputs, intervals, survival thresholds, and failure distribution.

## 22. Parameter Stability Experiment Design Rules

Design defines neighborhoods, grids or perturbations, interaction effects, stable regions, isolated peaks, boundary behavior, acceptable degradation, and instability criteria.

## 23. Cross-Market and Cross-Timeframe Experiment Rules

Comparisons define transfer mechanism, comparable and excluded markets/timeframes, data construction, liquidity, costs, frequency, sample alignment, expected degradation, and non-transferability.

## 24. Regime-Specific Experiment Rules

Experiments cite exact RCS records, taxonomy, labels, confidence, uncertainty, samples, transitions, conflicts, and treatment of unknown states. Post-result relabeling is prohibited.

## 25. Feature-Specific Experiment Rules

Experiments cite exact FFS versions, lineage, transformations, temporal alignment, leakage/bias/redundancy reviews, ablation, replacement, dependency, missingness, and drift assumptions.

## 26. Edge-Specific Experiment Rules

Experiments preserve frozen EDS behavior, mechanism, null, alternatives, conditions, classifications, controls, limitations, and prohibited interpretations.

## 27. Strategy-Family Experiment Rules

Experiments preserve SFSS selected and rejected families, comparison rationale, conditions, failure modes, information needs, and required family-discriminating tests.

## 28. Deviation and Amendment Rules

Every deviation records what changed, why, when, who authorized it, whether results were visible, and scientific impact. Material amendments create new versions, preserve the baseline, and may require restart or downgrade.

## 29. Result Interpretation Boundaries

Interpretation is limited to registered questions, scope, metrics, assumptions, and evidence maturity. Success is not Validation, edge proof, Risk acceptance, or Deployment authority.

## 30. Experiment Output Eligibility Rules

Eligibility requires authorized design, exact versions, completed controls, preserved runs/failures, reviewed deviations, reproducibility material, complete outputs, visible limitations, and no unresolved integrity block. Status is Eligible, Eligible With Limitations, Returned, or Ineligible.

## 31. Experiment Evidence Handoff Requirements

EEP receives identity/version; purpose/scope/question; hypotheses/null/alternatives; all upstream context; data/version/partitions; variables/parameters/search; costs/execution; metrics/criteria; controls; reproducibility; deviations/amendments; limitations, prohibited interpretations, eligibility, and follow-up.

## 32. Experiment Audit and Reconstruction

Independent reviewers must reconstruct what was planned before results, what ran, what changed, what failed, which outputs were excluded, and why evidence was eligible. Hindsight rewriting is prohibited.

## 33. Integration with MACP

MACP governs design, registration, authorization, status, deviations, completion, eligibility, return, rejection, handoff, supersession, and archival with exact versions.

## 34. Integration with SMI

SMI holds current state, owner, locks, partitions, execution status, deviations, blockers, and handoff. It cannot mutate the frozen design.

## 35. Integration with EES

All design claims, controls, deviations, results, and eligibility decisions use EES provenance, scope, uncertainty, limitations, versions, and custody.

## 36. Integration with WOE

WOE enforces all preregistration, authorization, execution, review, eligibility, and handoff gates and preserves failed and returned work.

## 37. Integration with Agent Registry

Only registered agents may design, authorize, coordinate, execute, review, or consume experiments within contract rights. Execution cannot validate itself.

## 38. Integration with Artifact Registry

Designs, registrations, controls, runs, deviations, eligibility, handoffs, rejections, and archives are versioned ART artifacts.

## 39. Integration with Strategy Lifecycle Standard

XDS governs Experiment Planned and Executed transitions. Material design or strategy changes return the lifecycle to the necessary gate.

## 40. Integration with Autonomous Research Pipeline

ARP routes approved Architecture and Engineering outputs into XDS and cannot advance to EEP without eligibility.

## 41. Integration with Market Discovery & Ranking Standard

MDRS market scope, data, costs, liquidity, and limitations remain binding experimental context.

## 42. Integration with Regime Classification Standard

RCS taxonomy and records govern regime-specific design, partitioning, uncertainty, and transition handling.

## 43. Integration with Feature Factory Standard

FFS governs exact feature definitions, lineage, timing, leakage, redundancy, and scope used by the design.

## 44. Integration with Edge Discovery Standard

EDS supplies the candidate behavior, mechanism, null, alternatives, controls, conditions, and evidence maturity under test.

## 45. Integration with Strategy Family Selection Standard

SFSS supplies family rationale, alternatives, failure modes, and required discriminating experiments without defining trading logic.

## 46. Integration with Experiment Evidence Package

EEP packages actual conduct and results against frozen XDS. It cannot silently rewrite the plan or omit failures.

## 47. Integration with Validation Evidence Package

VEP evaluates design integrity, conformance, leakage, controls, robustness, reproducibility, and deviations. XDS cannot grant Validation.

## 48. Integration with Risk Review Package

RRP may consume cost, execution, tail, capacity, and failure assumptions only through validated evidence and cannot reinterpret design success as Risk approval.

## 49. Integration with Monitoring and Edge Decay Standard

Forward and monitoring experiments preregister baselines, windows, thresholds, evidence, and failure paths under XDS while MEDS owns operational health decisions.

## 50. Governance

Mandatory experiment types include Exploratory, Confirmatory, Backtest, Optimization, Walk-Forward, Monte Carlo, Parameter Stability, Cross-Market, Cross-Timeframe, Temporal Robustness, Regime-Specific, Feature Ablation/Redundancy, Negative Control, Adversarial Stress, Execution, Cost, Data Quality, Parity, Forward Paper, and Failure Reproduction.

Every design preserves purpose, scope, hypotheses, contexts, data, partitions, costs, execution, metrics, controls, criteria, robustness, reproducibility, deviations, eligibility, limitations, and audit history. Frozen designs cannot be edited in place; amendments create versions. Exceptions cannot legalize post-result confirmation, silent metric or partition replacement, selective reporting, or missing controls.

Every future AI Quant Lab experiment must conform to XDS before institutional interpretation or EEP handoff.
