# Deployment Governance Standard (DGS) v1.0

## Specification Control

| Field | Value |
|---|---|
| Standard ID | `AIQL-DGS` |
| Version | `1.0.0` |
| Status | Proposed for Sprint 28 review |
| Scope | Every deployment candidate, paper, limited-live, live, scaling, reactivation, rollback, and retirement action |
| Authority | EDP, RRP, VEP, SLS, WOE, EES, ART, Agent Registry, and institutional deployment governance |
| Provider dependency | None |

The Deployment Governance Standard is the mandatory constitutional control layer between an issued Executive Decision Package and operation of a strategy. It verifies that exact authorized versions, scope, limits, controls, monitoring, ownership, custody, and operational conditions are satisfied before any governed deployment stage begins or changes.

It is not implementation, infrastructure automation, exchange integration, strategy approval, risk approval, or executive authority. Deployment governance confirms readiness and continued conformity; it cannot create missing authority.

## 1. Deployment Governance Philosophy

Deployment converts institutional decisions into controlled operational exposure. The central question is not whether a strategy appears profitable, but whether the exact authorized strategy can operate within enforceable scope, observable state, bounded failure, and recoverable control.

Readiness is stage-specific and temporary. A system ready for Paper Monitoring is not necessarily ready for Limited Live; a Limited Live deployment does not inherit Live Active authority.

Deployment state must remain reconstructable from authorization through retirement. Operational speed never justifies hidden versions, silent changes, absent monitoring, or missing kill capability.

## 2. Deployment Governance Principles

The following principles are binding:

1. No Deployment Without Issued Executive Decision.
2. No Deployment Outside Authorized Scope.
3. No Deployment Without Strategy, Implementation, and Configuration Version Locks.
4. No Deployment Without Implementation Fidelity.
5. No Deployment Without Data and Execution Readiness.
6. No Deployment Without Monitoring, Risk Controls, Kill Switch, and Operational Owner.
7. No Paper Monitoring Without Success and Failure Criteria.
8. No Limited Live Without Capital and Exposure Limits.
9. No Live Active Without Continuous Monitoring.
10. No Scaling Without New Authorization.
11. No Silent Deployment Change or Automatic Stage Promotion.
12. No Rollback Without Audit Trail.
13. Deployment Is Not Strategy or Risk Approval.
14. Every Deployment Must Be Auditable.

## 3. Deployment Identity Model

Every governed deployment has a permanent Deployment ID, Deployment Record ID, and exact version. The Deployment ID identifies the continuing operational lineage; the record version identifies a precise authorized state.

Identity binds Strategy ID and version, implementation artifact and version, configuration version, environment identity, data version, execution venue, source EDP version, and deployment stage.

A materially different strategy, authorization scope, execution context, or operational purpose requires a new Deployment ID. Amendments preserve predecessor and successor lineage; identifiers are never reused.

## 4. Deployment Object Model

The Deployment Record must define:

| Record group | Mandatory content |
|---|---|
| Identity | Deployment ID, record ID, owner, responsible agent |
| Strategy | Strategy ID/version and lifecycle state |
| Versions | Implementation artifact/version, configuration version, environment identity, data version |
| Execution | Venue and authorized execution assumptions |
| Authority | Source EDP/version, verdict, scope, conditions, expiry |
| Scope | Capital, exposure, markets, instruments, timeframes, regimes, and portfolio context |
| Limits | Risk, loss, leverage, sizing, liquidity, capacity, and concentration limits |
| Controls | Kill, suspension, reactivation, monitoring, incident, and rollback controls |
| Ownership | Deployment, monitoring, operations, incident, rollback, and escalation owners |
| State | Stage, status, readiness, version lock, open issues, and conditions |
| Readiness | Data, execution, monitoring, risk-control, kill-switch, and operational status |
| Validity | Expiry conditions and reassessment triggers |
| Integrations | Source MACP and related SMI, EES, ART, WOE, and SLS records |
| History | Created At, Updated At, lineage, and immutable Audit Trail |

All required fields must resolve to exact governed versions. Missing ownership or critical readiness blocks advancement.

## 5. Deployment Lifecycle

**Proposed → Executive Authorized → Readiness Review → Version Locked → Controls Verified → Deployment Candidate → Paper Monitoring → Limited Live → Live Active → Scaling Review → Degraded → Suspended → Rollback → Retired → Archived**

| State | Institutional meaning |
|---|---|
| Proposed | Deployment identity and requested stage registered |
| Executive Authorized | Current EDP permits readiness review |
| Readiness Review | Versions, environment, data, execution, controls, and ownership examined |
| Version Locked | Exact authorized versions sealed |
| Controls Verified | Monitoring, risk, kill, incident, and rollback paths tested |
| Deployment Candidate | Readiness work only; no live authority |
| Paper Monitoring | Forward observation without live capital |
| Limited Live | Constrained live authority within exact limits |
| Live Active | Active operation within bounded scope; never unlimited |
| Scaling Review | Proposed expansion independently assessed |
| Degraded | Heightened review after weakened evidence, control, or operation |
| Suspended | Trading authority removed or frozen |
| Rollback | Return to a prior authorized or disabled state |
| Retired | Deployment permanently closed for the identity or version |
| Archived | Complete history preserved for reconstruction |

No stage promotes itself. Every forward transition requires a current EDP and recorded gate decision.

## 6. Executive Decision Intake Record

Intake verifies exact EDP identity, version, issued status, custody, verdict, scope, conditions, capital, exposure, monitoring, kill, suspension, reactivation, expiry, reassessment triggers, and intended lifecycle transition.

It also verifies current VEP and RRP lineage. Expired, revoked, superseded, inconsistent, or incomplete authority blocks readiness review.

## 7. Authorized Scope Record

The record states exact permitted strategy and implementation versions, stage, capital, exposure, markets, instruments, timeframes, regimes, portfolio context, execution assumptions, effective time, and expiry.

Deployment scope may narrow but never broaden EDP, RRP, or VEP scope. Any ambiguity is resolved before activation.

## 8. Version Lock Record

The lock covers strategy, architecture, implementation, configuration, dependencies, environment, data source, risk controls, monitoring rules, and deployment artifacts.

Each lock identifies exact version, owner, integrity state, authorized consumers, effective time, and unlock authority. A mismatch blocks deployment or triggers immediate suspension if detected after activation.

## 9. Environment Readiness Record

Readiness assesses identity, isolation, dependency integrity, capacity, time synchronization, access control, secrets custody, resilience, recovery, observability, change control, and separation of research from governed operation.

The record states tested assumptions, unresolved weaknesses, failure containment, and stage eligibility without prescribing technology.

## 10. Data Readiness Record

Data readiness covers authorized source and version, provenance, availability, timeliness, completeness, quality, timestamp and calendar consistency, transformations, stale-data handling, anomaly detection, fallback, outage behavior, and escalation.

Critical data failure must fail closed or follow an explicitly authorized safe state. Silent substitution of a data source is prohibited.

## 11. Execution Readiness Record

Execution readiness covers authorized venue, instrument mapping, order behavior, timing, sizing, limits, spread, slippage, liquidity, partial fills, rejection, duplication, gaps, reconciliation, position truth, and safe exit.

Paper behavior must not be assumed equivalent to live execution. Limited and active stages require evidence that execution assumptions remain within authorized Risk and Executive scope.

## 12. Monitoring Readiness Record

Every required metric must identify source, cadence, normal range, warning threshold, breach threshold, owner, recipient, alert path, response time, evidence capture, and action.

Monitoring covers strategy state, signals, positions, exposure, loss, limits, data, execution, liquidity, operations, version integrity, conditions, regime alignment, and edge decay. Missing critical visibility blocks forward or live operation.

## 13. Risk Control Readiness Record

The record verifies every RRP and EDP limit is represented, enforceable, observable, tested, owned, and linked to warning, breach, escalation, and containment behavior.

Capital, position size, leverage, exposure, market, instrument, timeframe, regime, drawdown, daily, weekly, monthly, event, liquidity, and concentration limits must remain exact or stricter.

## 14. Kill Switch Readiness Record

Kill-switch categories include loss, drawdown, exposure, size, leverage, Validation/Risk/Executive scope breach, unauthorized strategy/implementation/configuration, data integrity, venue, routing, monitoring, alert delivery, liquidity collapse, extreme slippage, operational incident, governance violation, and manual executive intervention.

Each trigger defines detector, threshold or event, authority, automatic and manual action, position treatment, notifications, custody evidence, escalation, and restoration criteria. Failure of a required kill path blocks live authority.

## 15. Operational Ownership Record

Deployment, monitoring, operational response, incidents, rollback, risk escalation, executive escalation, and record custody each require named registered owners and alternates.

Ownership defines availability, decision rights, acknowledgement, response time, handoff, conflicts, and absence coverage. A technically functional deployment without accountable ownership is not ready.

## 16. Deployment Candidate Rules

Deployment Candidate permits readiness, verification, controlled packaging, and non-trading rehearsal only. It requires current EDP, resolved preconditions, exact versions, ownership, readiness plan, monitoring design, controls, rollback plan, and expiry.

Candidate status does not authorize paper or live operation unless the EDP explicitly grants the next stage and its DGS gate passes.

## 17. Paper Monitoring Deployment Rules

Paper Monitoring requires exact simulation assumptions, forward-only observation, authorized instruments and regimes, success and failure criteria, minimum duration and sample expectations, monitoring cadence, deviation treatment, expiry, and evidence packaging.

It creates new evidence and cannot promote itself. Material mismatch between paper and validated assumptions triggers return or reassessment.

## 18. Limited Live Deployment Rules

Limited Live requires a specific EDP grant, verified versions and controls, constrained capital and exposure, permitted instruments and regimes, loss limits, continuous monitoring, functioning kill and rollback paths, incident readiness, validity period, and promotion/failure criteria.

Any expansion beyond a limit is unauthorized scaling.

## 19. Live Active Deployment Rules

Live Active requires current VEP, RRP, and EDP; satisfied prior-stage requirements; demonstrated operational stability; portfolio compatibility; continuous monitoring; enforceable limits; verified kill, suspension, rollback, and incident paths; and periodic reassessment.

Live Active remains bounded. Continued operation depends on current authority and healthy control state.

## 20. Scaling and Scope Expansion Rules

Scaling includes increased capital, position size, leverage, markets, instruments, timeframes, regimes, venues, portfolio role, or operational autonomy.

Every material expansion requires impact evidence, updated capacity and liquidity analysis, portfolio assessment, current Validation and Risk applicability, an amended or new EDP, new versioned Deployment Record, and repeated affected readiness gates.

Past safe operation does not authorize future scale.

## 21. Suspension, Rollback, and Emergency Control

Degradation follows warning-level deterioration with heightened monitoring, constrained exposure, owner, deadline, and mandatory outcome. Suspension removes trading authority after material breach, control failure, version mismatch, expired decision, or executive order.

Rollback returns to a previously authorized state or disables operation. It defines target state, position treatment, configuration and version, owner, integrity verification, notifications, and evidence preservation.

Emergency control may stop activity immediately to protect capital or integrity. It cannot approve new scope. Reactivation requires root-cause evidence, remediation, renewed control verification, current authority, and explicit decision.

## 22. Deployment Change Control

Every proposed change is classified by materiality and impact on strategy logic, implementation, configuration, data, environment, execution, risk, monitoring, ownership, or scope.

Non-material corrections require versioning and audit review. Material changes require affected scientific, risk, executive, and deployment reassessment. Emergency changes remain temporary, documented, reviewed after action, and cannot silently become permanent.

## 23. Deployment Expiry and Reassessment

Deployment authority expires on the EDP or RRP expiry, an explicit DGS condition, or a material trigger. Triggers include version change, limit breach, control failure, monitoring loss, data or venue change, edge decay, regime shift, incident, new contradiction, scaling request, or governance amendment.

Expired authority blocks continued operation until renewed; grace periods require explicit prior authorization.

## 24. Deployment Freezing and Chain of Custody

Before activation, the Deployment Record, version manifest, scope, controls, readiness findings, ownership, conditions, and audit state are frozen. Frozen records cannot be edited in place.

Custody records intake, review, locks, tests, activation, acknowledgements, changes, alerts, incidents, degradation, suspension, rollback, reactivation, scaling, retirement, and archival. Amendments create new versions and preserve predecessors.

## 25. Integration with MACP

MACP governs authorization intake, readiness requests, locks, verification, activation, monitoring, breaches, incidents, changes, scaling, suspension, rollback, reactivation, retirement, and archival. Messages cite exact strategy, EDP, RRP, VEP, deployment, artifact, and agent versions.

Informal communication creates no deployment authority.

## 26. Integration with SMI

SMI holds current governed operational state: stage, owners, locks, limits, conditions, health, alerts, incidents, expiry, and acknowledgements. It cannot silently change frozen scope or evidence.

Stale or conflicting critical state causes degradation or suspension according to severity.

## 27. Integration with EES

Readiness tests, control verification, paper results, monitoring, breaches, incidents, rollback, and reactivation produce EES objects with provenance, scope, versions, limitations, custody, and uncertainty.

Deployment observations are evidence, not self-approval.

## 28. Integration with WOE

WOE enforces intake, readiness, locks, control verification, stage activation, monitoring, change, scaling, degradation, suspension, rollback, reactivation, retirement, and archival gates.

No workflow may skip a stage gate or assign deployment work outside agent rights.

## 29. Integration with Agent Registry

Only active registered agents may own, verify, activate, monitor, suspend, roll back, or retire deployment within their rights. Technical capability is not authority.

No agent may self-expand scope or alter its own authorization.

## 30. Integration with Artifact Registry

Deployment candidate, activation, readiness failure, degradation, suspension, rollback, reactivation readiness, scaling review, retirement, archive, monitoring, incident, and version-lock records are governed artifacts with lineage, provenance, consumers, status, retention, and audit history.

## 31. Integration with Strategy Lifecycle Standard

DGS enforces operational transitions to Deployment Candidate, Paper Monitoring, Live Limited, Live Active, Degraded, Suspended, Retired, and Archived. The deployment stage and strategy lifecycle state must remain consistent.

Operational change cannot bypass the lifecycle gate required by SLS.

## 32. Integration with Experiment Evidence Package

EEP supplies exact experimental implementation, data, parameters, execution assumptions, failures, robustness, and reproducibility lineage. DGS verifies deployment consistency but cannot reinterpret experimental admissibility.

## 33. Integration with Validation Evidence Package

VEP scope, limitations, conditions, accepted/qualified evidence, expiry, and revalidation triggers remain binding. Amendment, revocation, or expiry triggers deployment impact review and possible suspension.

## 34. Integration with Risk Review Package

RRP limits, monitoring, kill, suspension, reactivation, portfolio constraints, expiry, and reassessment triggers are mandatory deployment controls. DGS may enforce stricter controls but cannot broaden Risk scope.

## 35. Integration with Executive Decision Package

DGS may consume only an issued, current EDP. It verifies rather than grants EDP authority. Every activation or scaling action must fall within exact verdict, scope, conditions, effective time, and expiry.

EDP revocation, supersession, expiry, or material amendment immediately affects deployment authority.

## 36. Governance

### 36.1 Mandatory readiness areas

Every review covers Executive validity, strategy/implementation/configuration integrity, environment, data source and quality, execution venue and routing, sizing, risk and loss enforcement, monitoring and alerting, kill, suspension, rollback, incident response, ownership, and audit readiness.

### 36.2 Mandatory rules

1. Only issued EDPs may authorize review.
2. Deployment cannot broaden Executive, Risk, or Validation scope.
3. Exact versions and all upstream limitations and conditions remain binding.
4. Monitoring, operational ownership, and required controls precede forward operation.
5. Kill and rollback readiness precede live authority.
6. Paper and Limited Live cannot self-promote; scaling requires new authority.
7. Material change requires versioning and review.
8. Version mismatch, failed critical control, or expired authority blocks or suspends deployment.
9. Frozen records cannot be edited in place; amendments create new versions.
10. Revoked authority remains reconstructable.

### 36.3 Governed outputs

DGS supports Deployment Candidate Approval, Paper Monitoring Activation, Limited Live Activation, Live Active Activation, Readiness Failure, Degradation, Suspension, Rollback, Reactivation Readiness, Scaling Review, Retirement, and Deployment Archive records.

### 36.4 Exceptions and amendments

Exceptions are scoped, time-bounded, independently authorized, auditable, and supported by compensating controls. They cannot legalize missing authority, scope expansion, absent monitoring, failed kill controls, unknown versions, or silent change.

Changes to this standard require cross-system impact review, deployment-governance approval, executive authorization, versioning, migration rules, and preservation of prior versions.

### 36.5 Institutional rule

Every future AI Quant Lab deployment must satisfy this standard before a strategy may become Deployment Candidate, Paper Monitored, Limited Live, Live Active, scaled, reactivated, retired, or archived.
