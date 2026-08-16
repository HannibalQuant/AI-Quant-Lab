# Feature Factory Standard (FFS) v1.0

## Specification Control

| Field | Value |
|---|---|
| Standard ID | `AIQL-FFS` |
| Version | `1.0.0` |
| Status | Proposed for Sprint 33 review |
| Scope | Every institutional feature, indicator-derived measure, statistic, composite, risk, execution, regime, and monitoring variable |
| Authority | Research OS, SLS, ARP, MDRS, RCS, EES, VEP, RRP, DGS, MEDS, ART, and feature governance |
| Provider dependency | None |

The Feature Factory Standard governs how institutional features are defined, evidenced, versioned, reviewed, approved, restricted, superseded, retired, transferred, and audited across AI Quant Lab.

It is not an indicator library, strategy, signal generator, optimizer, or implementation. A feature measures information. It does not create a market mechanism or constitute edge by itself.

## 1. Feature Factory Philosophy

A feature is a governed representation of an information need derived from identified data under explicit transformations and scope. Its value depends on lineage, temporal integrity, stability, interpretability, independence, and fitness for a declared purpose.

Mechanism precedes measurement. Strategy reasoning states what must be known before selecting how to estimate it. Feature performance cannot retroactively become a rationale.

Feature governance preserves failed, redundant, unstable, biased, and retired measures because they prevent repeated research debt.

## 2. Feature Factory Principles

The following principles are binding:

1. No Feature Without Identity, Purpose, Scope, Version, Data Lineage, and Construction Rationale.
2. No Feature Without Leakage, Bias, Redundancy, Stability, Regime, and Limitation Review.
3. No Indicator-First Strategy Design.
4. No Feature Is Edge By Itself.
5. No Selection From Performance Alone.
6. No Silent Mutation, Replacement, or Scope Expansion.
7. No Use Outside Approved Scope.
8. No Approval Without Evidence.
9. Research Approval Does Not Imply Validation, Risk, Deployment, or Monitoring Approval.
10. Retired and Rejected Features Remain Learnable.
11. Feature Governance Must Be Auditable.

## 3. Feature Identity Model

Every feature has a permanent Feature ID, Feature Record ID, and exact semantic version. Identity binds purpose, information need, family, definition, inputs, transformation, temporal alignment, scope, and owner.

Changes to formula, inputs, timing, normalization, smoothing, lag, window, update behavior, or scope require a new version. A materially different information need or interpretation requires a new Feature ID.

## 4. Feature Object Model

The Feature Record must define:

| Record group | Mandatory content |
|---|---|
| Identity | Feature ID, record ID, owner, responsible agent, name, family, type |
| Purpose | Information need, construction rationale, intended interpretation |
| Scope | Universe, asset class, venue, instruments, timeframes, regimes |
| Data | Source/version, input fields, lineage, quality, missingness |
| Construction | Transformation description, window, normalization, scaling, smoothing, lag, update frequency |
| Dependencies | Known dependencies, redundancies, correlations, composites, upstream versions |
| Review | Leakage, bias, stability, regime dependency, interpretability, sensitivity, reproducibility |
| Use | Strategy-family fit, approved and prohibited cases, limitations, contradictions |
| Status | Validation, Risk, Deployment, Monitoring, supersession, and retirement status |
| Integrations | Source MACP and related SMI, EES, ART, WOE, and Agent records |
| History | Created At, Updated At, versions, and immutable Audit Trail |

Institutional references resolve to exact Feature ID and version.

## 5. Feature Lifecycle

**Proposed → Defined → Data Lineage Verified → Construction Reviewed → Candidate → Experiment Eligible → Validated for Scope → Approved for Governed Use → Challenged → Restricted → Superseded → Deprecated → Retired → Archived**

Approval is purpose- and scope-specific. Challenge preserves current evidence while review proceeds. Supersession and retirement prohibit silent future use but preserve complete lineage.

## 6. Feature Taxonomy

Mandatory families are Trend, Momentum, Volatility, Liquidity, Market Structure, Regime, Participation, Volume, Risk, Execution, Noise, Friction, Time and Session, Portfolio, Meta, and Derived Composite Features.

Each feature has one primary family and may reference secondary dimensions. Classification cannot obscure cross-family dependencies or double-count equivalent information.

## 7. Feature Data and Lineage Requirements

Lineage identifies source authority, version, fields, timestamps, calendars, transformations, adjustments, filtering, missingness, revisions, survivorship, joins, dependencies, access date, and custody.

Temporal availability must state when each input became knowable relative to the decision. Reconstructed or revised data cannot masquerade as contemporaneously available information.

## 8. Feature Construction Rationale

The rationale defines the information need, why the data may estimate it, assumptions, expected behavior, alternative measurements, failure modes, prohibited interpretation, and evidence required.

Construction describes behavior without prescribing code. A formula copied from convention without institutional rationale remains exploratory.

## 9. Trend Feature Requirements

Trend features may measure direction, persistence, efficiency, duration, alignment, structure, or separation from noise. Direction alone cannot be interpreted as trend quality.

They disclose lag, reversal sensitivity, regime dependency, whipsaw behavior, and redundancy with other directional measures.

## 10. Momentum Feature Requirements

Momentum features measure return persistence, acceleration, participation, or continuation pressure. They distinguish momentum from trend direction and disclose reversal, tail, volatility, and window sensitivity.

## 11. Volatility Feature Requirements

Volatility features distinguish level, change, compression, expansion, clustering, range, tails, and usability. They define reference distribution, horizon, scaling, gap treatment, and sensitivity to market hours and data construction.

## 12. Liquidity Feature Requirements

Liquidity features distinguish observed activity, available liquidity, executable capacity, spread, slippage, depth proxies, resilience, and stressed exit feasibility.

Venue, size, timeframe, fragmentation, source reliability, and operational availability remain explicit.

## 13. Market Structure Feature Requirements

Structure features define ranges, boundaries, swings, breaks, compression, expansion, acceptance, rejection, stability, and invalidation context.

Levels are contextual measurements, not universal support or resistance truth. Hindsight-defined structures are prohibited from confirmatory use.

## 14. Regime Feature Requirements

Regime features cite exact RCS taxonomy and record versions, confidence, uncertainty, transition state, scope, and conflicting evidence.

No single feature may independently create an institutional regime label.

## 15. Participation and Volume Feature Requirements

These features define source, venue coverage, reliability, normalization, session effects, missingness, relation to price behavior, and whether observed volume represents the relevant market.

Participation and volume are not interchangeable, and neither independently proves direction.

## 16. Risk Feature Requirements

Risk features may measure drawdown pressure, tails, loss clustering, exposure, leverage, margin, concentration, correlation, liquidity stress, or risk-of-ruin context.

They disclose estimation uncertainty, path dependence, aggregation, horizon, and failure under structural change.

## 17. Execution Feature Requirements

Execution features measure latency, fill quality, slippage, spread, missed or rejected actions, impact, liquidity consumption, reconciliation, and operational feasibility.

They distinguish simulated, paper, and live observations and retain venue and size scope.

## 18. Noise and Friction Feature Requirements

Noise and friction features measure whipsaw, false breakouts, microstructure noise, path inefficiency, transaction-cost pressure, instability, gaps, and signal degradation.

They state reference horizon and cannot label all adverse movement as noise.

## 19. Feature Transformation Rules

Every transformation records purpose, order, inputs, window, normalization, scaling, smoothing, clipping, lag, missing-value treatment, outlier treatment, update timing, and invertibility where relevant.

Transformations learned from data must specify fitting scope and prevent future or holdout information from entering earlier observations.

## 20. Feature Redundancy and Dependency Rules

Review identifies shared inputs, mathematical dependence, correlation, conditional association, information overlap, causal dependency, and duplicate timing.

EMA versus SMA, MACD versus moving-average slope, ATR versus range-width measures, and oscillators derived from similar price changes require explicit overlap review. Multiple correlated measures do not create independent confirmation.

Composite features preserve component identities, versions, weights, dependencies, failure modes, and missing-component behavior.

## 21. Feature Stability Rules

Stability is assessed across time, markets, instruments, timeframes, regimes, data sources, transformations, windows, perturbations, and relevant operational conditions.

The record distinguishes distribution drift, relationship drift, missingness drift, sensitivity, and complete failure. Stability in one sample cannot authorize broader scope.

## 22. Feature Leakage and Bias Rules

Review covers temporal alignment, look-ahead, label leakage, feature leakage, repeated holdout access, survivorship, selection, normalization, universe construction, revision, publication, and post-selection bias.

Material leakage invalidates affected evidence. Mitigation, residual risk, and downstream impact remain explicit; leakage cannot be cured by narrative explanation alone.

## 23. Feature Interpretability Rules

Interpretability requires a bounded description of what the feature measures, expected direction or state, units, range, invariances, failure conditions, dependencies, and prohibited claims.

Complexity must be justified by incremental information. A feature that cannot be interpreted may remain exploratory but requires stronger evidence and restrictions.

## 24. Feature Strategy-Family Fit Rules

Fit maps features to information needs, not directly to trades. Trend families need direction and persistence; Breakout needs structure, pressure, false-break risk, and liquidity; Momentum needs persistence and participation; Pullback needs trend and retracement context; Mean Reversion needs bounded structure and reversion pressure; Volatility families need level/change and execution context; Adaptive and Hybrid families require explicit regime and dependency handling.

Fit never substitutes for mechanism or hypothesis.

## 25. Feature Use in Market Discovery

Features may support MDRS dimensions and scoring only within approved data and scope. They cannot define strategy edge, and correlated features cannot inflate opportunity scores through double counting.

## 26. Feature Use in Regime Classification

RCS may consume multiple governed features with confidence, uncertainty, conflict, and taxonomy controls. One measurement cannot determine the institutional label.

## 27. Feature Use in Strategy Architecture

Every architecture feature maps to an information need and expected mechanism. Redundancy, dependency, failure behavior, alternatives, and module contribution are reviewed before approval.

## 28. Feature Use in Experiment Design

Experiments preregister exact Feature IDs, versions, scope, transformations, fitting, missingness, leakage review, alternatives, controls, and evaluation criteria before results are known.

Post-result feature creation or mutation is exploratory and separately versioned.

## 29. Feature Use in Validation

Validation assesses admissibility, lineage, timing, reproducibility, leakage, bias, redundancy, stability, sensitivity, regime dependency, interpretability, and tested scope.

Feature usefulness in a backtest is insufficient for approval.

## 30. Feature Use in Risk Review

Risk Governance assesses feature failure, drift, concentration, hidden dependency, data/vendor reliance, operational availability, monitoring, and consequence of incorrect or missing values.

## 31. Feature Use in Deployment Governance

DGS locks exact feature, data, transformation, configuration, dependency, and environment versions before activation. Version mismatch or unavailable critical feature blocks or suspends operation.

## 32. Feature Use in Monitoring and Edge Decay

MEDS observes feature distribution, missingness, quality, stability, correlation, regime mismatch, calculation availability, and deviations from Validation, Risk, Executive, and Deployment assumptions.

Feature drift is evidence requiring attribution; it is not automatically edge decay.

## 33. Feature Evidence Packaging

Every Candidate, validated, approved, challenged, restricted, superseded, deprecated, or retired feature has a frozen evidence package containing identity, scope, lineage, rationale, transformations, reviews, experiments, contradictions, limitations, approved/prohibited use, status, and custody.

## 34. Feature Audit and Reconstruction

An independent reviewer must reconstruct the exact feature value from authorized inputs and determine what definition, data, timing, transformation, evidence, scope, and status were known at each institutional use.

Historical feature values and records are not rewritten with revised data or definitions without linked versions.

## 35. Integration with MACP

MACP governs proposal, definition, lineage verification, review, experiment eligibility, validation, approval, challenge, restriction, supersession, retirement, handoff, and archival. Messages cite exact versions.

## 36. Integration with SMI

SMI holds current status, ownership, locks, dependencies, review blocks, consumers, and operational health. It cannot silently mutate frozen definitions or evidence.

## 37. Integration with EES

Every rationale, review, experiment, contradiction, status, and handoff uses EES objects with provenance, scope, uncertainty, limitations, confidence, versions, custody, and admissibility.

## 38. Integration with WOE

WOE enforces definition, lineage, review, experimentation, approval, challenge, restriction, supersession, retirement, and archival gates with eligible owners.

## 39. Integration with Agent Registry

Only registered agents may define, review, approve, consume, challenge, or retire features within their rights. Technical capability does not confer feature-governance authority.

## 40. Integration with Artifact Registry

Definitions, lineage manifests, reviews, evidence packages, approvals, restrictions, handoffs, supersessions, retirements, and archives are ART-governed artifacts with preserved lineage.

## 41. Integration with Strategy Lifecycle Standard

Every strategy version cites exact governed features. Material feature change triggers SLS impact classification, new versions, experiments, and proportional revalidation.

## 42. Integration with Autonomous Research Pipeline

ARP coordinates feature handoffs without bypassing lifecycle gates. No pipeline stage may consume an unversioned, out-of-scope, or ineligible feature.

## 43. Integration with Market Discovery & Ranking Standard

FFS supplies governed measurements to MDRS. MDRS owns opportunity assessment; FFS owns feature identity and integrity. Scoring cannot redefine feature semantics.

## 44. Integration with Regime Classification Standard

FFS supplies governed regime measurements; RCS owns labels, confidence, uncertainty, and conflicts. RCS changes do not silently mutate feature history.

## 45. Integration with Monitoring and Edge Decay Standard

MEDS consumes frozen feature baselines and creates drift evidence. Material drift may challenge a feature through WOE but cannot silently change its definition, threshold, or scope.

## 46. Governance

### 46.1 Mandatory review areas

Every feature review covers provenance, version integrity, temporal alignment, look-ahead, label and feature leakage, survivorship, selection, normalization and universe bias, market/timeframe/regime dependency, stability, drift, redundancy, correlation, interpretability, sensitivity, missingness, outliers, reproducibility, and operational feasibility.

### 46.2 Mandatory rules

1. Information need and mechanism remain distinct from measurement.
2. Every feature preserves data lineage, exact timing, construction, version, and scope.
3. Leakage, bias, redundancy, stability, regime dependency, and operational feasibility precede relevant use.
4. No post-result mutation, performance-only selection, unversioned definition, or silent replacement is permitted.
5. Approval cannot exceed tested market, timeframe, data, regime, and purpose.
6. Research eligibility does not grant downstream approval.
7. Rejected, deprecated, superseded, invalidated, and retired records remain reconstructable.
8. Frozen records cannot be edited in place; amendments create new versions.

### 46.3 Handoff requirements

Every handoff includes identity/version, family, purpose, information need, data/version, inputs, rationale, transformation, temporal alignment, scope, leakage, bias, redundancy, stability, interpretability, limitations, prohibited and approved uses, and follow-up.

### 46.4 Exceptions and change control

Exceptions are explicit, scoped, time-bounded, independently approved, and visible downstream. They cannot legalize unknown lineage, material leakage, silent mutation, hidden redundancy, or out-of-scope use.

Changes to FFS require cross-system impact analysis, feature-governance review, versioning, migration rules, consumer impact handling, and preserved prior versions.

### 46.5 Institutional rule

Every future AI Quant Lab feature, indicator-derived measure, statistic, regime variable, risk variable, execution variable, monitoring variable, or composite must conform to this standard before institutional use.
