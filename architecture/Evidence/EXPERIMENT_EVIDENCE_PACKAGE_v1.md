# Experiment Evidence Package (EEP) v1.0

## Specification Control

| Field | Value |
|---|---|
| Standard ID | `AIQL-EEP` |
| Version | `1.0.0` |
| Status | Proposed for Sprint 24 review |
| Scope | Every completed institutional experiment and every submission of experimental results |
| Authority | Research OS, EES, MACP, SMI, WOE, Agent Registry, Artifact Registry, and Strategy Lifecycle Standard |
| Provider dependency | None |

The Experiment Evidence Package is the mandatory, governed body of evidence produced by a completed experiment before its results may enter Validation. It preserves scientific intent, exact tested versions, methods, complete results, uncertainty, negative findings, deviations, reproducibility, custody, and limitations.

It is not a backtest report, optimization report, performance summary, implementation, or approval. Packaging makes evidence reviewable; it does not make the hypothesis true.

## 1. Experiment Evidence Package Philosophy

### 1.1 Evidence as a reconstructable claim

Experimental evidence is useful only when an independent reviewer can determine what was asked, what was planned, what was tested, what actually ran, what changed, what failed, and what the results do and do not support.

### 1.2 Completeness before persuasion

The package is designed to prevent favorable summaries from becoming detached from unsuccessful runs, contradictory outcomes, assumptions, and boundary conditions. Completeness takes priority over narrative convenience.

### 1.3 Package versus verdict

An EEP transports frozen experimental evidence. It cannot validate itself, accept risk, authorize deployment, or advance a strategy lifecycle state. Those acts belong to contract-authorized agents.

### 1.4 Exact-version reasoning

Every conclusion is conditional on the exact experiment plan, strategy, implementation, data, parameters, environment, and execution assumptions tested. An unversioned reference is inadmissible.

## 2. Experiment Evidence Package Principles

The following principles are binding:

1. No Experiment Evidence Without Experiment ID.
2. No Result Without Registered Plan.
3. No Result Without Strategy Version.
4. No Result Without Implementation Version.
5. No Result Without Data Version.
6. No Result Without Configuration.
7. No Result Without Assumption Disclosure.
8. No Optimization Result Without Search Space.
9. No Backtest Result Without Costs and Execution Model.
10. No Robustness Claim Without Robustness Evidence.
11. No Validation Submission Without Frozen Package.
12. No Silent Deviation.
13. No Selective Result Reporting.
14. Negative Results Must Be Preserved.
15. Failed Runs Must Be Explainable.
16. Reproducibility Is Mandatory.
17. Limitations Must Travel With the Package.

## 3. Package Identity Model

Each package has a permanent, unique Package ID and exact version. The ID is never reused, including after invalidation or archival. Package identity is distinct from Experiment ID because one experiment may require amendments or separately frozen evidence packages.

Every citation must resolve to Package ID, package version, Experiment ID, experiment-plan version, Strategy ID and version, implementation version, and data version. A package version is immutable after freezing.

A material amendment creates a new package version linked to its predecessor. Evidence from materially different plans, strategies, implementations, or datasets must not be blended under one identity unless the registered experiment explicitly defines the comparison.

## 4. Package Object Model

The Package Record must define:

| Field | Requirement |
|---|---|
| Package ID | Permanent unique identifier |
| Experiment ID | Registered experiment identifier |
| Experiment Type | Governed experiment classification |
| Experiment Owner | Accountable lifecycle owner |
| Producing Agent | Registered evidence producer |
| Strategy ID / Version | Exact tested strategy identity and version |
| Strategy Lifecycle State | State at experiment authorization |
| Hypothesis Tested | Falsifiable claim and null hypothesis |
| Research Question | Bounded question addressed |
| Experiment Plan Artifact | Exact preregistered plan |
| Implementation Artifact / Version | Exact implementation tested |
| Data Source / Version | Exact source, snapshot, transformations, and lineage |
| Market Coverage | Venues and market domains |
| Instrument Coverage | Instruments and inclusion rules |
| Timeframe Coverage | Observation and decision horizons |
| Period Coverage | Exact temporal boundaries and exclusions |
| Regime Coverage | Regime definitions, occurrences, and gaps |
| Parameter Set | Exact parameters used |
| Parameter Search Space | Bounds, distributions, conditional structure, and exclusions |
| Optimization Method | Objective, constraints, pruning, trials, seeds, and selection rules |
| Run Configuration | Run identifiers, ordering, seeds, dependencies, and resources |
| Execution Model | Signal timing, order timing, fills, partial fills, gaps, and liquidity |
| Cost / Slippage / Spread Models | Values, sources, variability, and sensitivity assumptions |
| Position Sizing / Risk Assumptions | Exposure, compounding, limits, and loss controls |
| Result Summary | Non-promotional synthesis of all planned outcomes |
| Detailed Results | Complete planned metrics and disaggregated outcomes |
| Robustness Results | Stability, sensitivity, replication, and stress evidence |
| Negative Control Results | All registered control outcomes |
| Adversarial Test Results | Deliberate challenge outcomes |
| Failure Cases | Failed runs, mechanisms, and consequences |
| Deviations From Plan | Every authorized and unauthorized deviation |
| Known Limitations / Contradictions | Boundaries, uncertainty, and conflicting evidence |
| Reproducibility Instructions / Status | Independent reconstruction requirements and verdict |
| Validation Readiness Status | Readiness decision, blocks, and reviewer |
| Source MACP Message | Initiating or submission message |
| Related SMI Memory Objects | Exact shared-state references |
| Related EES Evidence Objects | Constituent evidence and versions |
| Related Artifact Records | Plans, outputs, reports, logs, and manifests |
| Related Workflow Objects | Governing WOE workflow and stage |
| Created At / Updated At | Governed timestamps |
| Audit Trail | Immutable actions, actors, changes, and custody events |

Missing fields block submission unless explicitly inapplicable, justified, and accepted during Completeness Review.

## 5. Package Lifecycle

**Proposed → Assembling → Submitted → Completeness Review → Frozen → Validation Ready → Returned → Amended → Invalidated → Archived**

| State | Meaning |
|---|---|
| Proposed | Package identity reserved for a registered experiment |
| Assembling | Evidence, records, failures, and artifacts being collected |
| Submitted | Producer declares assembly complete |
| Completeness Review | Independent structural and consistency review |
| Frozen | Exact contents sealed; chain of custody begins |
| Validation Ready | Completeness, integrity, and reproducibility prerequisites satisfied |
| Returned | Named deficiencies require correction or explanation |
| Amended | New version created with explicit change lineage |
| Invalidated | Package cannot support institutional reliance |
| Archived | Immutable record retained for reconstruction and learning |

Freezing must precede Validation Ready. Return does not erase submission history. Invalidation does not delete evidence. Archived status preserves all versions and verdicts.

## 6. Mandatory Package Sections

Every EEP contains these result sections in order:

1. Executive Experimental Summary
2. Experiment Purpose
3. Hypothesis Tested
4. Strategy Version Tested
5. Implementation Version Tested
6. Data and Period Coverage
7. Market and Regime Coverage
8. Configuration and Parameters
9. Execution Assumptions
10. Cost and Slippage Assumptions
11. Main Results
12. Robustness Results
13. Negative Control Results
14. Adversarial Test Results
15. Failure Cases
16. Deviations From Plan
17. Known Limitations
18. Contradictory Evidence
19. Reproducibility Instructions
20. Validation Readiness Statement

“Not performed,” “not observed,” and “not applicable” are distinct statements and require reasons. Empty sections are prohibited.

## 7. Experiment Design Record

The design record captures the preregistered purpose, research question, hypothesis, null and alternatives, mechanism, variables, controls, baselines, datasets, sampling rules, metrics, success and failure criteria, stopping rules, replication criteria, statistical methods, and planned analyses.

It must distinguish confirmatory tests from exploratory analysis. Analyses conceived after observing results are labeled post hoc and cannot masquerade as preregistered confirmation.

Mandatory Experiment Types are:

- Backtest Experiment
- Walk-Forward Experiment
- Monte Carlo Experiment
- Parameter Stability Experiment
- Cross-Market Experiment
- Cross-Timeframe Experiment
- Temporal Robustness Experiment
- Negative Control Experiment
- Adversarial Stress Experiment
- Execution Assumption Experiment
- Data Quality Experiment
- Implementation Parity Experiment
- Forward Paper Monitoring Experiment
- Failure Reproduction Experiment

## 8. Data and Market Coverage Record

The package must identify provenance, ownership, retrieval date, snapshot or release, transformations, cleaning rules, corporate or contract adjustments, missingness, outliers, exclusions, survivorship treatment, timezone, calendars, bar construction, sampling, and integrity checks.

Coverage is reported by market, venue, instrument, timeframe, period, regime, liquidity condition, and data-quality status. Gaps and underrepresented regimes remain visible.

Train, validation, test, and untouched holdout partitions must be explicit. Leakage controls must cover time, labels, features, normalization, universe selection, parameter selection, and repeated access to holdout data.

## 9. Implementation and Environment Record

The package links the exact implementation artifact, architecture version, dependencies, execution environment, deterministic settings, numerical assumptions, and verification results. It records module-to-architecture traceability and all known implementation deviations.

Environment identity must be sufficient for independent reproduction. If hardware, concurrency, numerical precision, or dependency behavior may alter results, the sensitivity is disclosed.

Implementation parity experiments must identify both representations, event timing, comparison keys, tolerated differences, mismatches, and resolution status.

## 10. Parameter and Configuration Record

Every fixed parameter, derived value, default, conditional rule, seed, initialization, and configuration override must be recorded.

Optimization disclosure includes search space, distributions, objective function, penalties, constraints, pruning, sampler, trial budget, seed policy, failed trials, selection criteria, tie-breaking, and all post-selection filters. The package reports the candidate population, not only the winner.

Parameter stability evidence must distinguish isolated optima from broad stable regions and disclose whether ranges were selected before or after observing results.

## 11. Execution Assumption Record

The record defines signal formation, decision timestamp, order submission, next eligible execution, order types, fill logic, partial fills, gaps, price limits, latency, liquidity, market hours, funding, borrowing, tick and lot constraints, and position concurrency.

Costs, spread, slippage, commissions, fees, financing, and market impact must have provenance and sensitivity analysis appropriate to the strategy. Zero-cost assumptions require explicit justification and cannot support deployment readiness where costs are material.

Sizing and risk assumptions include initial capital, compounding, leverage, exposure caps, margin, liquidation, stops, portfolio interaction, and treatment of unavailable executions.

## 12. Result Record

Results must map directly to preregistered questions, metrics, controls, and thresholds. The record includes aggregate and disaggregated results, uncertainty intervals, sample counts, trade counts, missing outcomes, distributional characteristics, tail behavior, and practical significance.

Results are separated by in-sample, validation, out-of-sample, holdout, market, timeframe, regime, and relevant operating condition. Aggregation must not conceal material weakness.

The Executive Experimental Summary states what evidence supports, weakens, or refutes; it must not use validation or deployment language.

## 13. Robustness Evidence Record

Robustness claims require named tests, rationale, methods, perturbations, seeds, thresholds, complete results, failures, and scope. Relevant tests include walk-forward, Monte Carlo, resampling, sensitivity, parameter stability, cross-market, cross-timeframe, cross-regime, temporal, cost, execution, and stress analysis.

Walk-forward evidence discloses train/test windows, anchoring or rolling logic, selection inside each training window, leakage controls, aggregation, and dispersion.

Monte Carlo evidence discloses randomization method, seed policy, number of runs, dependence assumptions, perturbations, survival thresholds, and failure distribution.

Robustness is not established by repeating equivalent tests or by excluding unfavorable conditions after observation.

## 14. Negative Control Evidence Record

Negative controls test whether apparent performance could arise without the proposed mechanism. Controls may randomize signals, labels, timing, direction, features, or market association while preserving appropriate structure.

The package records control rationale, expected behavior, implementation, complete outcomes, comparison method, and implications. Failed negative controls weaken admissibility and must never be omitted.

Absence of a suitable negative control must be explained and becomes a Validation Readiness limitation.

## 15. Failure and Exception Record

All failed, interrupted, timed-out, non-convergent, corrupted, rejected, or anomalous runs are preserved or referenced. Each record states run identity, failure class, cause if known, affected outputs, remediation, rerun linkage, and whether exclusion changes conclusions.

Exceptions identify the rule affected, authorizing role, justification, compensating controls, scope, duration, and downstream consequence. Technical inconvenience is not sufficient grounds to hide a failed run.

## 16. Deviation Record

A deviation is any difference between the registered plan and actual conduct. The record identifies what changed, when, why, who authorized it, whether results had been observed, scientific impact, affected artifacts, and required follow-up.

Unauthorized deviations block Validation Ready until adjudicated. Material deviations require a revised plan, new experiment or package version, and clear separation of pre- and post-deviation evidence.

## 17. Reproducibility Record

The package must enable an authorized independent party to reconstruct inputs, environment, configuration, execution order, randomness, transformations, runs, calculations, and outputs.

Reproducibility status is one of `Not Assessed`, `Blocked`, `Partially Reproduced`, `Reproduced`, or `Failed`. A claim of Reproduced requires an identified reviewer, exact package version, independent run, comparison criteria, differences, and conclusion.

Unavailable proprietary inputs must be governed through accessible references and a documented verification path; confidentiality cannot become hidden evidence.

## 18. Limitation and Uncertainty Record

Limitations cover data, samples, regimes, methods, assumptions, models, execution, costs, capacity, transferability, reproducibility, and external validity. Uncertainty is reported quantitatively where defensible and qualitatively where not.

Known contradictions must identify the conflicting evidence, affected claim, reconciliation status, and consequence. Limitations and contradictions travel with every downstream citation and cannot be removed by summarization.

## 19. Validation Readiness Record

Readiness is a packaging and admissibility assessment, not scientific approval. It confirms:

- exact identities and versions resolve;
- registered plan and complete results are present;
- mandatory sections and experiment-specific disclosures are complete;
- evidence lineage and custody are intact;
- deviations, failures, contradictions, and limitations are visible;
- reproduction requirements are usable;
- package is frozen and internally consistent;
- no unresolved block prevents independent review.

Status is `Not Ready`, `Ready With Declared Limitations`, `Validation Ready`, or `Returned`. The Validation Agent may reject any incomplete, unfrozen, inconsistent, stale, selectively reported, or non-reproducible package.

## 20. Package Freezing and Chain of Custody

Freezing seals package contents, manifest, constituent evidence, artifacts, versions, and checks. A frozen package cannot be edited in place. Access, transfer, review, challenge, copy, and amendment events are recorded.

Custody identifies the producing agent, completeness reviewer, freezing authority, Validation recipient, timestamps, authorized locations or references, and integrity status. Loss of custody integrity suspends admissibility.

Amendments create a new version, preserve the original, enumerate changes, state reasons and impact, and repeat affected completeness and freeze controls.

## 21. Integration with MACP

MACP carries package proposal, evidence requests, submissions, acknowledgements, returns, freeze notices, transfers, challenges, amendments, invalidations, and archival events. Every message cites exact package, experiment, strategy, implementation, data, workflow, and artifact versions plus sender authority and requested action.

Informal communication cannot substitute for a governed submission or custody transfer.

## 22. Integration with SMI

SMI maintains governed assembly and workflow state: owner, status, locks, outstanding sections, review blocks, constituent references, and current version. It may not contain hidden evidence or silently mutate frozen content.

Evidence remains governed by EES and artifacts by ART. Conflicting or stale memory state blocks freezing until reconciled.

## 23. Integration with EES

The EEP is a governed evidence package composed of exact EES Evidence Objects. Each retains identity, provenance, scope, assumptions, limitations, contradictions, confidence, reproducibility, admissibility, custody, version, and audit trail.

Package assembly does not elevate weak evidence or convert evidence into knowledge, validation, risk approval, or decision.

## 24. Integration with WOE

WOE controls package initiation, assignment, assembly, dependencies, completeness review, freezing, transfer, return, amendment, invalidation, and archival. Required gates cannot be skipped, including under accelerated execution.

The Experiment Workflow cannot advance to Validation Review until the package is Frozen and Validation Ready.

## 25. Integration with Agent Registry

Only registered, active agents with appropriate evidence and workflow rights may produce, review, freeze, transfer, challenge, or consume an EEP. Capability is not authority.

The Experiment Orchestrator coordinates package completion but cannot alter scientific results or grant validation. The producer cannot independently certify scientific validity.

## 26. Integration with Artifact Registry

The package, plan, implementation, data reference, run outputs, robustness reports, controls, failure records, reproduction records, amendments, and validation-readiness statement are registered artifacts with identity, owner, version, lineage, provenance, status, consumers, dependencies, retention, and audit history.

An artifact’s existence does not make its evidence admissible. Frozen EEP artifacts cannot be edited in place.

## 27. Integration with Strategy Lifecycle Standard

The EEP binds experimental evidence to the exact Strategy ID, version, lifecycle state, hypothesis, architecture, and implementation tested. It is the mandatory handoff from Experiment Executed through Evidence Packaged to Validation Review.

Evidence from one strategy version cannot advance another without explicit scope analysis and authorization. Parameter, measurement, logic, mechanism, or scope changes follow SLS versioning and revalidation rules.

## 28. Governance

### 28.1 Mandatory rules

1. No valid experiment evidence exists without a registered plan.
2. Submission requires exact strategy, implementation, and data versions.
3. Optimization discloses search space, objective, constraints, pruning, and selection.
4. Backtests disclose costs, slippage, spread, timing, sizing, and assumptions.
5. Walk-forward evidence discloses windows and leakage controls.
6. Monte Carlo evidence discloses randomization, seeds, perturbations, and survival thresholds.
7. Parameter stability distinguishes peaks from robust regions.
8. Negative controls are reported even when unfavorable.
9. Failed runs are preserved or explicitly explained.
10. Deviations are visible and justified.
11. Selective reporting is prohibited.
12. Validation may reject incomplete, unfrozen, inconsistent, or non-reproducible packages.
13. Frozen packages cannot be edited in place.
14. Amendments create new versions.
15. Invalidated packages remain reconstructable.

### 28.2 Authority

Producing agents own accurate assembly. Experiment Orchestration owns coordination and status integrity. Independent completeness review owns readiness checks. EES governance owns evidence integrity and custody. Validation owns scientific admissibility and verdict. Risk and Executive agents may consume only validated or explicitly qualified packages within their authority.

### 28.3 Exceptions and amendments

Exceptions are explicit, scoped, time-bounded, independently approved, and attached to downstream use. They cannot legalize selective reporting, missing provenance, mutable frozen evidence, or self-validation.

Changes to this standard require impact analysis across EES, WOE, SLS, ART, SMI, MACP, Agent Registry, Validation, Risk, and Decision governance; approved versioning; migration rules; and preservation of earlier versions.

### 28.4 Institutional rule

Every future AI Quant Lab experiment must produce a conforming Experiment Evidence Package before its results may be submitted to Validation, Risk Governance, Executive Decision, deployment review, or strategy lifecycle advancement.
