# Risk Review Package (RRP) v1.0

## Specification Control

| Field | Value |
|---|---|
| Standard ID | `AIQL-RRP` |
| Version | `1.0.0` |
| Status | Proposed for Sprint 26 review |
| Scope | Every institutional risk review and handoff of a validated strategy to Executive Decision |
| Authority | Risk Governance, VEP, EES, WOE, Agent Registry, ART, SLS, and institutional decision governance |
| Provider dependency | None |

The Risk Review Package is the mandatory constitutional output of independent Risk Governance. It determines whether a scientifically validated strategy is acceptable, conditionally acceptable, remediable, or unacceptable from an institutional risk perspective within exact scope, capital context, operating assumptions, limits, controls, and monitoring obligations.

It is not a performance report, validation verdict, executive decision, or deployment authorization. Scientific validity is an input to risk review, not a guarantee of risk acceptability.

## 1. Risk Review Package Philosophy

### 1.1 Risk as bounded exposure to uncertainty

Risk is the possibility that uncertain market, execution, liquidity, model, data, operational, portfolio, or governance conditions produce loss or institutional impairment. It includes what is measurable, what is only estimable, and what remains unknown.

### 1.2 Risk approval is conditional

No strategy is safe in absolute terms. An approval applies only to an exact strategy version, validated scope, deployment context, capital allocation, exposure limits, controls, monitoring state, and validity period.

### 1.3 Capital preservation before performance

Expected return cannot compensate for risks that cannot be identified, bounded, monitored, contained, or exited. Risk Governance evaluates survivability and institutional fit, not attractiveness alone.

### 1.4 Independent authority

Risk Governance may restrict or reject a scientifically valid strategy. It cannot broaden Validation scope, rewrite evidence, change strategy logic, authorize deployment, or issue the executive decision.

## 2. Risk Review Package Principles

The following principles are binding:

1. No Risk Review Without Issued Validation Evidence.
2. No Risk Verdict Without Defined Scope.
3. No Risk Approval Without Explicit Limits.
4. No Deployment Risk Approval Without Kill Conditions.
5. No Capital Exposure Without Monitoring.
6. No Ignoring Validation Limitations.
7. No Broadening Validation Scope.
8. No Risk Approval From Performance Alone.
9. No Silent Assumption Acceptance.
10. No Risk-Free Deployment.
11. No Unlimited Live Strategy.
12. No Portfolio Blindness.
13. Tail, Execution, Liquidity, Data, and Operational Risk Are Mandatory.
14. Risk Approval Is Not Executive Approval.
15. Every Verdict Must Be Auditable.
16. Rejected Risk Remains Learnable.

## 3. Package Identity Model

Every RRP has a permanent Risk Package ID, Risk Review ID, and exact version. Identifiers are never reused. The package is bound to one Strategy ID and version, one defined risk question, one deployment context, and exact VEP versions.

Any amendment creates a new immutable package version. A new Risk Review ID is required when the strategy version, validation scope, capital context, deployment mode, material evidence, or risk question changes enough to constitute a new risk decision.

Downstream consumers must cite the exact frozen RRP version. Unversioned references are inadmissible for Executive Decision or lifecycle advancement.

## 4. Package Object Model

The Risk Package Record must define:

| Record group | Mandatory content |
|---|---|
| Identity | Risk Package ID, Risk Review ID, Risk Owner, Risk Governance Agent |
| Strategy | Strategy ID, version, lifecycle state, and exact Strategy Record |
| Validation | Source VEP, package version, verdict, scope, limitations, conditions, and expiry |
| Review | Risk scope, risk question, intake status, assessment status, and deployment context |
| Market | Market and regime risk assessments |
| Execution | Execution, slippage, spread, liquidity, capacity, and market-impact assessments |
| Model | Model, data, assumption, implementation, and dependency risk assessments |
| Loss | Drawdown, tail, worst-case, risk-of-ruin, leverage, and margin assessments |
| Portfolio | Interaction, correlation, drawdown correlation, concentration, and common-factor assessments |
| Operations | Operational, monitoring, vendor, access, incident, and recovery assessments |
| Capital limits | Allocation, position size, leverage, instrument, market, timeframe, regime, and aggregate exposure limits |
| Loss limits | Drawdown plus daily, weekly, monthly, and event loss limits |
| Controls | Kill, suspension, reactivation, monitoring, escalation, and required risk controls |
| Verdict | Verdict, rationale, scope, limitations, conditions, follow-up, and expiry |
| Handoff | Executive Handoff status, conditions, open questions, and reassessment triggers |
| Integrations | Source MACP message; related SMI, EES, ART, WOE, and SLS records |
| History | Created At, Updated At, version lineage, and immutable Audit Trail |

The record must separately identify accepted, rejected, and qualified risk assumptions. Missing mandatory information blocks issuance unless explicitly inapplicable, justified, and accepted by Risk Governance.

## 5. Package Lifecycle

**Proposed → Validation Intake → Risk Assessment → Limit Design → Verdict Drafted → Frozen → Issued → Returned → Amended → Revoked → Archived**

| State | Meaning |
|---|---|
| Proposed | Review identity, owner, and question registered |
| Validation Intake | Issued VEP and exact strategy context received |
| Risk Assessment | Required risk domains independently examined |
| Limit Design | Enforceable limits, controls, monitoring, and kill conditions specified |
| Verdict Drafted | Outcome and rationale prepared for governance review |
| Frozen | Package contents sealed against in-place change |
| Issued | Authorized risk verdict released to named consumers |
| Returned | Evidence, controls, or assumptions sent back with defects |
| Amended | New linked version issued after governed change |
| Revoked | Prior verdict is no longer institutionally reliable |
| Archived | Immutable record retained for reconstruction and learning |

Only Frozen packages may be Issued. Amendment and revocation never erase prior authority or history.

## 6. Risk Intake Record

Intake verifies sender authority, exact strategy and lifecycle state, issued VEP identity and version, validation verdict, scope, conditions, limitations, expiry, evidence custody, implementation version, proposed deployment context, portfolio context, and requested capital use.

The risk scope is declared before assessment. It may equal or narrow Validation scope but may never broaden it. Inconsistent, expired, revoked, incomplete, or out-of-scope inputs are returned.

Validation limitations are preserved verbatim as governed references and translated into risk implications without altering their scientific meaning.

## 7. Strategy Risk Profile Record

The profile describes the strategy’s return mechanism only to locate risk. It records exposure direction, holding horizon, turnover, signal density, concentration, sizing, leverage, stop behavior, dependency on regime, liquidity needs, capital path dependence, and expected failure modes.

It distinguishes normal operating loss, expected drawdown, adverse regime, model failure, execution failure, data failure, and structural edge failure. Historical observations are not treated as hard bounds on future loss.

## 8. Market and Regime Risk Record

The review assesses volatility shifts, gaps, discontinuities, trends, ranges, transitions, structural breaks, event risk, venue behavior, trading halts, funding, basis, market hours, and regime misclassification.

It identifies where exposure accumulates, where the strategy is unvalidated, and how quickly conditions can move beyond approved scope. Regime limits specify permitted, restricted, and prohibited states plus uncertainty behavior.

Cross-market assumptions must address transferability, common shocks, market-specific mechanics, and correlated stress.

## 9. Execution and Liquidity Risk Record

Execution review covers signal-to-order timing, latency, fills, partial fills, rejections, gaps, order types, queue effects, spread, slippage, fees, funding, borrowing, market impact, venue outage, and exit feasibility.

Liquidity and capacity review covers volume, depth, concentration, participation rate, time-to-liquidate, stressed liquidity, position crowding, capacity decay, instrument limits, and the effect of capital scale on the edge.

Backtest execution assumptions are compared with paper and observable conditions. Sensitivity to worse fills, wider spreads, missed trades, delays, and constrained exits must inform limits and kill conditions.

## 10. Model, Data, and Assumption Risk Record

Model risk includes incorrect mechanism, unstable parameters, regime error, hidden nonlinearity, complexity, approximation, implementation divergence, extrapolation, and model decay.

Data risk includes stale, missing, delayed, revised, corrupted, biased, incomplete, misaligned, or unauthorized data; timestamp and calendar errors; survivorship; corporate or contract adjustments; and vendor dependence.

Every material assumption is classified as accepted, rejected, or qualified with evidence, uncertainty, monitoring, and invalidation trigger. Silent acceptance is prohibited.

## 11. Drawdown, Tail, and Loss Risk Record

The record assesses maximum and typical drawdown, duration, recovery, clustering, worst trade, worst period, consecutive losses, gap loss, liquidation, leverage amplification, margin stress, risk of ruin, and capital impairment.

Tail analysis examines empirical and modeled extremes, asymmetry, dependence, regime shifts, correlation spikes, discontinuities, and scenarios beyond historical observations. Point estimates must be accompanied by uncertainty and sensitivity.

Worst-case assessment includes plausible severe conditions, compound failures, control failure, exit failure, and unknown-risk allowance. Simulated drawdown is evidence, not a guaranteed live ceiling.

## 12. Portfolio and Correlation Risk Record

Where applicable, review covers return correlation, downside and drawdown correlation, common factors, shared instruments, direction, regime concentration, liquidity overlap, execution overlap, tail dependence, net and gross exposure, and simultaneous failure.

Diversification claims require stress evidence and cannot rely solely on average correlation. Portfolio limits state aggregation rules, concentration caps, conflict handling, and priority under constrained liquidity.

A strategy acceptable in isolation may be rejected or restricted in the intended portfolio.

## 13. Operational and Monitoring Risk Record

Operational review covers ownership, access, separation of duties, data and execution dependencies, monitoring coverage, alert delivery, incident response, rollback, reconciliation, recovery, manual intervention, vendor failure, and governance continuity.

Monitoring requirements define metric, source, cadence, expected range, warning threshold, breach threshold, owner, recipient, response time, evidence capture, escalation, and action. A strategy cannot receive capital if critical monitoring is unavailable or unauditable.

The review also assesses whether controls can function during stress rather than only in normal conditions.

## 14. Exposure and Capital Limit Record

Limits must be explicit, measurable, enforceable, versioned, and scoped. The record defines capital allocation, position size, leverage, gross and net exposure, instrument, market, timeframe, regime, liquidity, capacity, turnover, drawdown, and daily, weekly, monthly, and event loss limits.

Each limit includes rationale, measurement method, warning level, hard level, owner, action, escalation, expiry, and review trigger. Dependencies among limits and portfolio aggregation rules are explicit.

Absence of a defensible limit requires rejection or mitigation; “reasonable exposure” is not a limit.

## 15. Kill Switch and Suspension Rules

Kill conditions define immediate removal or reduction of trading authority. Mandatory categories include loss and drawdown breach, exposure breach, validation-scope breach, data or execution integrity failure, uncontrolled order behavior, liquidity collapse, model divergence, monitoring failure, unauthorized version, operational incident, and governance violation.

Each condition specifies detector, threshold or qualitative trigger, authority, automatic and manual action, position treatment, notification, evidence preservation, and escalation.

Suspension conditions cover persistent warning breaches, degraded edge, unresolved contradictions, stale approval, failed controls, and inability to verify state. Reactivation requires root-cause evidence, remediation, control verification, updated review where needed, and explicit governance approval. Resuming automatically after time passes is prohibited.

## 16. Risk Verdict Model

Authorized verdicts are:

### APPROVED

The strategy is acceptable within the declared validation scope, deployment assumptions, capital context, monitoring requirements, and explicit limits. This does not authorize deployment.

### APPROVED WITH LIMITS

The strategy is acceptable only under exact exposure caps, markets, instruments, timeframes, regimes, monitoring requirements, kill conditions, deployment restrictions, and validity period.

### REQUIRES RISK MITIGATION

Scientific evidence may be adequate, but specified controls, limits, monitoring, operational protections, or additional risk evidence are required before Executive Handoff.

### REJECTED

Risk is unacceptable because of excessive or unbounded drawdown, tail, liquidity, execution, operational, portfolio, exposure, control, validation-scope, or enforceability concerns.

Every verdict states rationale, scope, accepted/rejected/qualified assumptions, limits, limitations, conditions, follow-up, expiry, reassessment triggers, alternatives considered, and authorizing agent.

## 17. Conditional Risk Approval Rules

Conditions must be observable and enforceable. They define exact strategy and implementation version, capital, position size, leverage, instruments, markets, timeframes, regimes, portfolio context, execution assumptions, monitoring, kill conditions, suspension and reactivation rules, validity period, and required evidence.

Conditions cannot broaden Validation scope or be delegated to informal judgment. Failure to satisfy any precondition blocks Executive Handoff; breach after issuance triggers restriction, suspension, or revocation.

## 18. Rejection and Return Rules

Return is used for remediable missing evidence, unclear assumptions, unenforceable draft controls, incomplete monitoring, or correctable inconsistencies. Rejection is used when risk remains unacceptable or cannot be bounded within institutional constraints.

Every return or rejection identifies causes, affected domains, required owner, permitted remedy, evidence needed, lifecycle destination, and whether renewed Validation is required.

Rejected strategies, assumptions, scenarios, and controls remain registered learning artifacts. Resubmission cannot overwrite history.

## 19. Executive Decision Handoff Requirements

The issued RRP must provide:

- risk verdict, rationale, scope, limitations, conditions, and expiry;
- exact strategy version plus Validation verdict, scope, and limitations;
- accepted, rejected, and qualified risk assumptions;
- capital, sizing, leverage, instrument, market, timeframe, regime, and exposure limits;
- drawdown plus daily, weekly, monthly, and event loss limits;
- tail, liquidity, execution, operational, data, model, and portfolio concerns;
- required monitoring, controls, kill, suspension, and reactivation conditions;
- required mitigations, open questions, and reassessment triggers;
- exact VEP, EES, ART, WOE, SLS, and MACP references.

Executive Handoff status is `Not Eligible`, `Eligible With Conditions`, `Eligible`, `Returned`, or `Revoked`. Only `APPROVED` or `APPROVED WITH LIMITS` may be eligible.

## 20. Risk Freezing and Chain of Custody

Freezing seals inputs, assumptions, assessments, scenarios, limits, controls, verdict, rationale, conditions, handoff, artifacts, and audit trail. Frozen packages cannot be edited in place.

Custody records intake, access, reviewers, challenges, freeze, issuance, handoff, monitoring references, amendments, revocation, and archival. Integrity loss suspends institutional reliance.

Amendments create new versions, preserve predecessors, enumerate changes, reassess affected risks, and repeat freeze and issuance. Revocation preserves the original verdict and all actions taken under it.

## 21. Integration with MACP

MACP governs intake, requests, assumptions, challenges, returns, verdict issuance, Executive Handoff, breaches, amendments, revocations, and archival. Messages cite exact strategy, VEP, RRP, evidence, artifact, workflow, and agent versions.

Informal communication cannot create, broaden, or modify risk authority.

## 22. Integration with SMI

SMI maintains governed review and live risk state: owners, assignments, limits, breaches, locks, outstanding questions, dependencies, package version, and handoff status. It cannot silently change frozen limits or hide breaches.

Conflicting, stale, or unavailable critical state blocks issuance or triggers suspension.

## 23. Integration with EES

Risk assessments, scenarios, assumptions, limit rationales, control tests, breaches, and verdicts are EES objects with provenance, scope, uncertainty, limitations, contradictions, custody, and versions.

Risk Governance consumes evidence but does not rewrite Validation or experiment evidence.

## 24. Integration with WOE

WOE enforces Validation Intake, assessment, limit design, verdict, freeze, issuance, return, amendment, revocation, and Executive Handoff gates. Risk Review cannot advance without an issued eligible RRP.

Workflow acceleration cannot skip risk domains, limit design, kill conditions, or custody controls.

## 25. Integration with Agent Registry

Only active registered agents with risk rights may assess, limit, issue, revoke, or hand off an RRP. Risk Governance cannot validate science, implement strategy logic, authorize deployment, or issue Executive Decision.

Delegation is bounded and auditable; final verdict authority remains with the registered Risk owner.

## 26. Integration with Artifact Registry

The RRP, workpapers, scenarios, limit schedules, control specifications, returns, verdicts, amendments, revocations, breaches, and handoff records are registered artifacts with identity, owner, version, lineage, provenance, consumers, retention, and audit history.

An artifact does not create authority outside its registered scope.

## 27. Integration with Strategy Lifecycle Standard

The RRP is mandatory for transition from `Risk Review` to `Risk Approved` and eligibility for `Executive Decision Pending`. It binds the verdict to exact strategy, implementation, Validation, evidence, and deployment-context versions.

Material strategy, scope, capital, execution, portfolio, or control changes trigger lifecycle return and proportional reassessment.

## 28. Integration with Experiment Evidence Package

EEP evidence informs risk only through governed lineage and Validation qualification. Risk Governance may inspect underlying experimental assumptions, failure cases, execution sensitivity, and robustness but cannot substitute its judgment for the Validation verdict or silently admit rejected evidence.

## 29. Integration with Validation Evidence Package

Risk review may consume only an issued, current VEP. It preserves verdict, scope, limitations, conditions, accepted/rejected/qualified evidence, open questions, expiry, and revalidation triggers.

An amended, revoked, or expired VEP triggers RRP impact review and may suspend Executive Handoff or existing risk authority.

## 30. Governance

### 30.1 Mandatory review areas

Every review covers Validation intake, version integrity, market and regime risk, execution assumptions, slippage and spread sensitivity, liquidity and capacity, drawdown, tail loss, worst trade and period, risk of ruin, capital, leverage, sizing, stops, portfolio and drawdown correlation, concentration, operational and data failures, monitoring, kill, suspension, reactivation, expiry, and reassessment.

### 30.2 Mandatory rules

1. Only issued VEPs may enter risk review.
2. Risk scope cannot exceed Validation scope.
3. All Validation limitations remain visible.
4. Approval defines enforceable limits, monitoring, kill, suspension, and reactivation conditions.
5. Scientific validity remains separate from risk acceptability.
6. Backtest drawdown is not a live-risk ceiling.
7. Execution, liquidity, tail, operational, data, model, and portfolio risks are mandatory.
8. Risk Governance cannot rewrite evidence, authorize deployment, or issue Executive Decisions.
9. Rejected risk remains learnable.
10. Frozen packages cannot be edited in place.
11. Amendments create new versions.
12. Revoked approvals remain reconstructable.

### 30.3 Exceptions and change control

Exceptions are explicit, scoped, time-bounded, independently approved, and accompanied by compensating controls. They cannot authorize unlimited exposure, missing monitoring, absent kill conditions, broader scientific scope, hidden assumptions, or deployment.

Changes to this standard require cross-system impact analysis, independent Risk Governance review, executive approval, versioning, migration rules, and preservation of prior versions.

### 30.4 Institutional rule

Every future AI Quant Lab risk review must produce a conforming Risk Review Package before a strategy may proceed to Executive Decision, deployment review, live authorization, monitoring, or lifecycle advancement.
