# Monitoring & Edge Decay Standard (MEDS) v1.0

## Specification Control

| Field | Value |
|---|---|
| Standard ID | `AIQL-MEDS` |
| Version | `1.0.0` |
| Status | Proposed for Sprint 29 review |
| Scope | Every paper-monitored, deployed, degraded, suspended, reactivated, retired, or archived strategy |
| Authority | DGS, EDP, RRP, VEP, SLS, EES, WOE, ART, Agent Registry, and monitoring governance |
| Provider dependency | None |

The Monitoring and Edge Decay Standard is the constitutional governance layer for continuous observation of strategy health, edge health, assumptions, limits, execution, data, regimes, portfolio effects, operations, and institutional compliance.

It is not a dashboard, alerting implementation, strategy, validation, or risk approval. Monitoring produces governed evidence and required actions; it cannot silently change strategy logic, thresholds, or authority.

## 1. Monitoring and Edge Decay Philosophy

Monitoring tests whether the conditions that justified authority remain true. It compares observed behavior with declared baselines, expected ranges, Validation and Risk assumptions, Executive conditions, and Deployment configuration.

Edge decay is not synonymous with loss. Loss can occur under a healthy probabilistic edge, while a positive return can conceal mechanism failure, deteriorating execution, unstable data, or growing tail exposure.

Monitoring therefore separates market variance, regime mismatch, mechanism weakening, implementation divergence, execution deterioration, data failure, portfolio stress, and operational failure before assigning institutional meaning.

## 2. Monitoring and Edge Decay Principles

The following principles are binding:

1. No Monitoring Without Strategy Identity, Authorized Scope, Baseline, Thresholds, Owner, and Escalation Path.
2. No Live Strategy Without Continuous Monitoring.
3. No Edge Claim Without Ongoing Evidence.
4. No Silent Edge Decay or Threshold Change.
5. Execution, Data, Regime, Portfolio, and Operational Deterioration Cannot Be Ignored.
6. Warning, Breach, and Kill States Are Distinct.
7. No Automatic Reactivation After Suspension.
8. No Retirement Without Learning Record.
9. Monitoring Is Not Validation or Risk Approval.
10. Every Monitoring State Must Be Auditable.

## 3. Monitoring Identity Model

Every monitoring mandate has a permanent Monitoring ID, Monitoring Record ID, and exact version. Identity binds the exact strategy version, Deployment ID and stage, DGS record, EDP, RRP, VEP, authorized scope, baseline, thresholds, owners, and monitoring period.

Material changes to strategy, deployment, metrics, baselines, thresholds, scope, or authority require a new record version and impact review. Identifiers are never reused, including after retirement.

## 4. Monitoring Object Model

The Monitoring Record must define:

| Record group | Mandatory content |
|---|---|
| Identity | Monitoring ID, record ID, owner, responsible agent |
| Strategy | Strategy ID/version, lifecycle state, expected mechanism and regimes |
| Deployment | Deployment ID/stage, DGS record, authorized scope |
| Authorities | Exact EDP, RRP, and VEP versions and binding conditions |
| Baseline | Expected performance, drawdown, execution, slippage, data quality, regime, and portfolio impact |
| Measurement | Metrics, cadence, windows, data lineage, and uncertainty treatment |
| Thresholds | Warning, breach, kill, degradation, suspension, reactivation, and retirement conditions |
| Response | Escalation path, owners, deadlines, restrictions, and required workflows |
| Health | Edge state, strategy state, monitoring status, open incidents, breaches, and contradictions |
| Evidence | Monitoring evidence objects, artifacts, and package references |
| Integrations | Source MACP and related SMI, EES, ART, WOE, and SLS records |
| History | Created At, Updated At, versions, and immutable Audit Trail |

Each metric must have a purpose, source, unit, transformation, expected range, uncertainty, cadence, warning, breach, kill relevance, owner, and response.

## 5. Monitoring Lifecycle

**Proposed → Monitoring Authorized → Baseline Established → Active Monitoring → Warning → Degraded → Breach → Escalated → Suspended → Reactivation Review → Retirement Review → Retired Monitoring → Archived**

No state transition erases prior observations. Warning and Degraded may return to Active Monitoring only through recorded review. Breach requires escalation; kill-level breach requires suspension or emergency control.

Retired Monitoring remains active only for closure evidence and retention obligations before archival.

## 6. Monitoring Intake Record

Intake verifies exact strategy and deployment versions, current DGS, EDP, RRP, and VEP authority, scope, conditions, limits, expected assumptions, required metrics, ownership, data availability, alert paths, kill readiness, expiry, and reassessment triggers.

Monitoring cannot begin with unresolved version mismatch, absent critical metric, missing owner, invalid authority, or undefined response path.

## 7. Strategy Health State Model

Authorized states are:

- `HEALTHY` — behavior remains within scope, expected ranges, and controls.
- `WATCH` — early warning exists; review and deadline are active.
- `DEGRADED` — material deterioration or uncertainty requires restriction and reassessment.
- `BREACHED` — a hard threshold, limit, condition, or governance rule failed.
- `SUSPENDED` — operating authority is removed or frozen.
- `REACTIVATION_PENDING` — remediation is under review; authority remains inactive.
- `RETIREMENT_PENDING` — evidence questions continued institutional value.
- `RETIRED` — strategy or deployment is closed and preserved.

The most severe unresolved material state governs institutional action.

## 8. Edge Health State Model

Authorized states are `UNKNOWN`, `BASELINING`, `HEALTHY`, `WEAKENING`, `DEGRADED`, `BROKEN`, `INCONCLUSIVE`, `SUSPENDED`, and `RETIRED`.

Edge health concerns the mechanism and evidence, not only realized performance. `BROKEN` requires evidence that the expected relationship materially fails or its sustaining conditions no longer exist. `INCONCLUSIVE` is used when data or sample quality prevents distinction between noise and decay.

## 9. Performance Monitoring Record

Monitoring covers rolling expectancy, profit factor, win rate, average trade, return distribution, trade and signal frequency, holding period, drawdown, recovery, tail loss, worst trade, and deviation from paper, validation, and live expectations.

Metrics are evaluated across multiple defensible windows and disaggregated by market, instrument, timeframe, direction, regime, and deployment stage. No single metric or window determines edge health in isolation.

## 10. Risk and Drawdown Monitoring Record

The record tracks all RRP and EDP limits, exposure, leverage, position size, concentration, liquidity, drawdown magnitude and duration, loss clusters, daily/weekly/monthly loss, tail events, margin pressure, and risk-of-ruin indicators.

Observed drawdown is compared with distributional expectations and operating conditions. A statistical drawdown and a hard risk-limit breach receive different classifications but both remain visible.

## 11. Execution and Slippage Monitoring Record

Monitoring covers spread, slippage, fees, fill rate and quality, partial fills, missed and duplicate trades, rejection, latency, execution delay, price impact, reconciliation, position divergence, exit ability, and venue availability.

Execution decay is separated from strategy decay by comparing decision intent, eligible price, actual action, and realized cost. Extreme or structurally rising execution friction triggers risk and deployment review.

## 12. Data Quality Monitoring Record

The record observes freshness, availability, completeness, missingness, duplication, ordering, timestamps, calendars, revisions, anomalies, transformations, source identity, schema consistency, and fallback usage.

Data-quality breaches are classified before performance interpretation. A strategy cannot be declared broken from corrupted evidence, and corrupted data cannot be ignored because results appear favorable.

## 13. Regime Alignment Monitoring Record

Monitoring compares observed regime distribution, confidence, transition frequency, volatility, liquidity, correlation, and market mechanics with the strategy’s validated and authorized regimes.

It distinguishes genuine mechanism decay from operation outside scope, regime misclassification, and an unprecedented transition. Persistent scope mismatch triggers restriction, reassessment, or suspension.

## 14. Portfolio Impact Monitoring Record

The record tracks return, downside, drawdown, tail, factor, instrument, liquidity, and execution correlation; gross and net exposure; concentration; portfolio heat; common shocks; and simultaneous failure.

A strategy may remain individually healthy while becoming institutionally unacceptable because portfolio interaction changed. Portfolio breaches follow RRP aggregation and escalation rules.

## 15. Operational Monitoring Record

Operational monitoring covers owner availability, access, dependencies, environment, control status, alerts, incidents, reconciliation, manual intervention, recovery, custody, version integrity, vendor health, and audit continuity.

Monitoring coverage and alert delivery are themselves monitored. Loss of critical observability is a risk event, not merely a technical inconvenience.

## 16. Edge Decay Detection Model

Edge-decay assessment must include rolling expectancy, profit factor, win rate, average trade, drawdown and duration, tail loss, trade and signal frequency, slippage, spread, fill quality, regime and volatility distributions, portfolio correlation, and deviations from Validation, Risk, Executive, and Deployment assumptions.

Assessment uses persistence, magnitude, statistical uncertainty, sample sufficiency, cross-window consistency, regime attribution, execution attribution, and plausible alternative explanations.

No decay verdict may be based solely on arbitrary recent-period selection. Evidence must state what supports weakening, what contradicts it, and what remains unknown.

## 17. Threshold and Breach Model

Thresholds are classified as informational, warning, degradation, breach, or kill. Each has exact metric or event, baseline, direction, window, persistence, owner, action, escalation, and expiry.

Thresholds are versioned and approved before use. They cannot be moved after observation to avoid an action. Multiple weak signals may create a composite escalation only when the combination rule was governed in advance.

## 18. Escalation Rules

Every warning has an owner, acknowledgement deadline, investigation deadline, evidence requirement, permitted interim action, and resolution path. Breaches notify Monitoring, Deployment, Risk, Executive, and affected owners according to authority.

Escalation may produce continued observation, heightened cadence, exposure restriction, controlled degradation, return to Validation or Risk, emergency suspension, retirement review, or incident workflow.

No agent may suppress escalation because it expects the condition to self-correct.

## 19. Degradation Rules

Degradation triggers include persistent edge weakening, underperformance beyond range, abnormal drawdown or tail loss, signal collapse or explosion, regime mismatch, assumption or condition breach, execution or data deterioration, monitoring gaps, correlation spike, concentration, operational instability, and unresolved contradiction.

The Degradation Record defines cause, evidence, restrictions, reduced authority, monitoring cadence, owners, deadline, reassessment gates, and mandatory outcome. Degraded status cannot persist indefinitely without decision.

## 20. Suspension Rules

Suspension triggers include kill breach, hard risk or loss breach, unauthorized strategy/implementation/configuration, Deployment/Executive/Risk/Validation scope breach, monitoring or alert failure, data or execution integrity failure, liquidity collapse, critical incident, governance violation, manual executive intervention, or unresolved critical contradiction.

Suspension removes or freezes authority, records effective time, position treatment, notifications, evidence preservation, investigation owner, and required workflow. Time passing cannot self-resolve suspension.

## 21. Reactivation Review Rules

Reactivation requires root-cause analysis, remediation evidence, control verification, current versions and authorities, updated Validation or Risk review where affected, restored monitoring, revised baseline or thresholds only when scientifically justified, and an issued EDP plus DGS readiness confirmation.

Status remains `REACTIVATION_PENDING` until every precondition is verified. Partial remediation cannot restore broader authority.

## 22. Retirement Signal Rules

Retirement signals include confirmed broken edge, persistent degradation without credible remedy, unacceptable risk, capacity loss, structural market change, operational unsustainability, obsolete dependencies, repeated suspension, or insufficient institutional value.

The signal initiates review; it does not retire automatically. Retirement requires final evidence, position and authority closure, failure analysis, successor relationships, learning artifact, Knowledge OS update, retention, and Executive decision.

## 23. Monitoring Evidence Packaging

Material baselines, warnings, degradation, breaches, edge-state changes, incidents, suspensions, reactivation reviews, and retirement signals produce frozen Monitoring Evidence Packages under EES.

Packages include identity, scope, versions, observation period, baseline, metrics, thresholds, raw and derived evidence references, uncertainty, contradictions, root-cause hypotheses, actions, owners, limitations, and custody.

## 24. Monitoring Freezing and Chain of Custody

Baselines, thresholds, state decisions, material evidence, actions, and reports are frozen before institutional reliance. Frozen records cannot be edited in place; corrections and amendments create linked versions.

Custody records collection, transformation, review, state transition, escalation, acknowledgement, action, amendment, retirement, and archival. Gaps in custody reduce admissibility and may trigger suspension.

## 25. Integration with MACP

MACP governs intake, status, warnings, breaches, evidence transfer, escalation, degradation, suspension, reactivation, retirement, amendments, and archival. Messages cite exact strategy, deployment, EDP, RRP, VEP, monitoring, artifact, and agent versions.

## 26. Integration with SMI

SMI maintains current health, thresholds, owners, open incidents, locks, breach state, required actions, expiry, and acknowledgements. It cannot silently mutate frozen baselines, evidence, or authority.

## 27. Integration with EES

All material observations, classifications, contradictions, incidents, and actions are EES objects with provenance, scope, versions, limitations, confidence, custody, and audit history. Monitoring evidence is not self-validation.

## 28. Integration with WOE

WOE coordinates authorization, baseline, active monitoring, warning, degradation, breach, escalation, suspension, reactivation review, retirement review, and archival gates. Required response workflows cannot be skipped.

## 29. Integration with Agent Registry

Only active registered agents may observe, classify, escalate, restrict, or recommend action within their rights. Monitoring agents cannot validate science, accept risk, expand scope, or issue Executive authority.

## 30. Integration with Artifact Registry

Baseline, health, warning, degradation, breach, escalation, suspension, reactivation, retirement signal, evidence package, incident, and archive records are governed artifacts with identity, lineage, provenance, consumers, status, retention, and audit history.

## 31. Integration with Strategy Lifecycle Standard

MEDS supplies governed evidence for Paper Monitoring, Live Limited, Live Active, Degraded, Suspended, Reactivation, Retired, and Archived transitions. Health state and lifecycle state must remain consistent.

## 32. Integration with Experiment Evidence Package

EEP defines tested expectations, execution assumptions, robustness, failures, and boundaries used to establish baselines. Monitoring cannot retroactively alter experimental evidence.

## 33. Integration with Validation Evidence Package

VEP scope, limitations, conditions, contradictions, and revalidation triggers become mandatory monitoring inputs. Material deviation triggers Validation impact review.

## 34. Integration with Risk Review Package

RRP limits, assumptions, monitoring mandates, kill, suspension, reactivation, expiry, and portfolio constraints remain binding. Risk breach triggers the prescribed action without reinterpretation.

## 35. Integration with Executive Decision Package

EDP defines authorized stage, scope, conditions, reporting, expiry, and reassessment. Monitoring cannot broaden or extend authority. Decision expiry or revocation triggers suspension or closure.

## 36. Integration with Deployment Governance Standard

DGS supplies exact versions, configuration, stage, controls, ownership, and readiness state. Monitoring verifies continued conformity. Version mismatch, control failure, or scope deviation triggers DGS escalation.

## 37. Governance

### 37.1 Mandatory monitoring areas

Every mandate covers version and scope integrity, Executive conditions, Risk limits, Validation limitations, performance and expectancy drift, drawdown and tails, execution and slippage, data quality, regime alignment, portfolio correlation and concentration, operations, alert delivery, kill availability, and edge decay.

### 37.2 Mandatory rules

1. Monitoring requires exact identity, authority, baseline, thresholds, owners, and escalation.
2. Upstream scope, limitations, conditions, and limits remain binding.
3. Thresholds are versioned and never silently changed.
4. Normal variance, mechanism decay, regime shift, data failure, and execution failure are distinguished.
5. Every warning, breach, escalation, and action is recorded and produces evidence when material.
6. Degradation defines restrictions and reassessment; breach triggers escalation; kill breach triggers suspension or emergency control.
7. Reactivation requires root cause, remediation, renewed authority, and readiness.
8. Retirement produces learning.
9. Frozen records cannot be edited in place; amendments preserve history.

### 37.3 Governed outputs

MEDS supports Monitoring Baseline, Strategy Health, Edge Health, Warning, Degradation, Breach, Escalation, Suspension Recommendation, Emergency Suspension, Reactivation Review, Retirement Signal, Monitoring Evidence Package, and Monitoring Archive records.

### 37.4 Exceptions and change control

Exceptions are explicit, scoped, time-bounded, independently authorized, and supported by compensating controls. They cannot legalize absent monitoring, silent threshold changes, ignored breaches, automatic reactivation, or missing custody.

Changes to MEDS require cross-system impact analysis, monitoring and risk governance review, executive approval, versioning, migration instructions, and preservation of prior versions.

### 37.5 Institutional rule

Every future AI Quant Lab paper-monitored, deployed, degraded, suspended, reactivated, retired, or archived strategy must conform to this standard while institutional state or authority exists.
