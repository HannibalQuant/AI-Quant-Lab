# Executive Decision Package (EDP) v1.0

## Specification Control

| Field | Value |
|---|---|
| Standard ID | `AIQL-EDP` |
| Version | `1.0.0` |
| Status | Proposed for Sprint 27 review |
| Scope | Every final institutional strategy decision and lifecycle authorization |
| Authority | Decision OS, Executive Decision Agent contract, VEP, RRP, SLS, WOE, EES, ART, and Agent Registry |
| Provider dependency | None |

The Executive Decision Package is the mandatory constitutional record of final institutional strategy decisions. It integrates issued Validation and Risk outputs, exact lifecycle state, unresolved issues, conditions, deployment assumptions, monitoring obligations, limits, and governance constraints into one bounded, auditable authorization or disposition.

It is not evidence, validation, risk review, performance analysis, implementation, or unlimited authority. The Executive Decision Agent decides only within the scientific and risk boundaries established by independent authorities.

## 1. Executive Decision Package Philosophy

### 1.1 Decision as accountable commitment

An executive decision is an explicit institutional commitment to permit, restrict, return, reject, suspend, reactivate, or retire work. It names what may happen, under which scope and conditions, for how long, and who remains accountable.

### 1.2 Integration without substitution

Executive review integrates independent conclusions. It may resolve prioritization and authorized trade-offs, but it cannot manufacture missing evidence, alter validation findings, accept risks rejected by Risk Governance, or silently broaden scope.

### 1.3 Stage-specific authority

Deployment Candidate, Paper Monitoring, Limited Live, and Live Active are distinct grants. Authority at one stage does not imply authority at the next.

### 1.4 Revocable and time-bounded authority

Approval persists only while exact versions, conditions, controls, monitoring, limits, evidence, and validity periods remain current. Institutional authority is always subject to suspension, expiry, reassessment, and supersession.

## 2. Executive Decision Package Principles

The following principles are binding:

1. No Decision Without Strategy Identity.
2. No Decision Without Issued Validation Evidence and Risk Review.
3. No Decision Without Defined Scope.
4. No Approval Without Explicit Conditions.
5. No Deployment Candidate Without Monitoring Requirements.
6. No Paper Monitoring Without Success and Failure Criteria.
7. No Limited Live Without Capital and Exposure Limits.
8. No Live Active Without Kill Conditions.
9. No Ignoring Validation or Risk Limitations.
10. No Broadening Validation or Risk Scope.
11. No Silent Assumption Acceptance.
12. No Decision From Performance, Backtest, or Optimization Alone.
13. Decision Is Not Evidence or Risk Review.
14. Every Decision Must Be Auditable.
15. Rejected Strategies Remain Learnable.

## 3. Package Identity Model

Every EDP has a permanent Executive Decision Package ID, Executive Decision ID, and exact version. Identifiers are never reused. The package binds one decision question to an exact Strategy ID and version, lifecycle state, VEP version, RRP version, and proposed institutional action.

Amendment creates a new immutable package version. A materially different decision question, strategy version, lifecycle transition, validation scope, risk scope, capital authorization, or deployment stage requires a new Executive Decision ID.

Every authority-bearing reference resolves to the exact frozen EDP version. Unversioned or superseded decisions cannot authorize institutional action.

## 4. Package Object Model

The Executive Decision Package Record must define:

| Record group | Mandatory content |
|---|---|
| Identity | Package ID, Decision ID, owner, Executive Decision Agent |
| Strategy | Strategy ID, version, lifecycle state, and exact Strategy Record |
| Validation | Source VEP/version, verdict, scope, limitations, conditions, and expiry |
| Risk | Source RRP/version, verdict, scope, limitations, limits, conditions, and expiry |
| Decision | Scope, question, intake, evidence sufficiency, risk sufficiency, and open-issue status |
| Inputs | Accepted, rejected, and qualified inputs with reasons |
| Verdict | Authorized verdict, rationale, scope, conditions, and required follow-up |
| Stage status | Deployment Candidate, Paper Monitoring, Limited Live, and Live Active status |
| Closure status | Return, rejection, suspension, reactivation, and retirement status |
| Authorization | Capital, exposure, market, instrument, timeframe, and regime authorization |
| Controls | Monitoring, kill, suspension, reactivation, expiry, and reassessment triggers |
| Integrations | Source MACP; related SMI, EES, ART, WOE, and SLS records |
| History | Created At, Updated At, lineage, and immutable Audit Trail |

The record must state unresolved issues and identify every condition owner, evidence requirement, deadline, verification authority, and consequence of non-compliance.

## 5. Package Lifecycle

**Proposed → Intake Review → Decision Review → Decision Drafted → Frozen → Issued → Returned → Amended → Revoked → Superseded → Archived**

| State | Meaning |
|---|---|
| Proposed | Decision identity, question, and owner registered |
| Intake Review | Strategy, VEP, RRP, lifecycle, and authority checked |
| Decision Review | Sufficiency, conflicts, scope, conditions, and alternatives assessed |
| Decision Drafted | Proposed verdict and rationale prepared |
| Frozen | Package sealed against in-place mutation |
| Issued | Authorized verdict released to named consumers |
| Returned | Inputs or controls sent back with specific deficiencies |
| Amended | New linked version issued after governed change |
| Revoked | Authority withdrawn because its basis is no longer reliable |
| Superseded | A later decision replaces future authority while preserving history |
| Archived | Immutable record retained for reconstruction and learning |

Only Frozen packages may be Issued. Return, amendment, revocation, and supersession never erase earlier decisions or actions.

## 6. Executive Intake Record

Intake verifies sender authority, exact Strategy ID and version, lifecycle eligibility, issued and current VEP and RRP, custody, compatible scope, unresolved blocks, requested transition, deployment context, monitoring readiness, and required artifacts.

Expired, revoked, superseded, inconsistent, incomplete, or out-of-scope inputs block review. Intake records accepted, rejected, and qualified inputs without rewriting them.

## 7. Evidence and Validation Review Record

Executive review confirms the Validation verdict, rationale, scope, accepted/rejected/qualified evidence, reproducibility status, robustness limitations, contradictions, open questions, monitoring conditions, and revalidation triggers.

Evidence sufficiency status is `Insufficient`, `Sufficient With Conditions`, or `Sufficient for Decision`. This status evaluates decision readiness, not scientific truth, and cannot broaden Validation findings.

## 8. Risk Review Record

Review confirms the Risk verdict, scope, accepted/rejected/qualified assumptions, capital and exposure limits, drawdown and loss limits, execution, liquidity, portfolio and operational concerns, monitoring, kill, suspension, reactivation, expiry, and reassessment triggers.

Risk sufficiency status is `Insufficient`, `Sufficient With Conditions`, or `Sufficient for Decision`. An unresolved Risk block cannot be overridden by executive preference.

## 9. Open Issues and Contradictions Record

Every open issue identifies origin, affected claim or control, severity, owner, required evidence or remediation, deadline, and decision consequence. Contradictions identify conflicting inputs, authority, scope, resolution status, and whether they block or condition action.

Unresolved material Validation or Risk blocks prohibit approval. Non-blocking uncertainty must remain visible in conditions, monitoring, expiry, and reassessment requirements.

## 10. Decision Scope Model

Scope defines exact strategy and implementation version, market, instrument, timeframe, regime, portfolio context, capital, exposure, deployment stage, execution assumptions, monitoring state, effective time, and expiry.

The authorized scope is the intersection of requested scope, Validation scope, Risk scope, operational readiness, and executive restrictions. It can only be equal to or narrower than every prerequisite authority.

## 11. Executive Decision Verdict Model

Authorized verdicts are:

- `APPROVED FOR DEPLOYMENT CANDIDATE`
- `APPROVED FOR PAPER MONITORING`
- `APPROVED FOR LIMITED LIVE`
- `APPROVED FOR LIVE ACTIVE`
- `APPROVED WITH CONDITIONS`
- `RETURN TO RESEARCH`
- `RETURN TO ARCHITECTURE`
- `RETURN TO ENGINEERING`
- `RETURN TO EXPERIMENTATION`
- `RETURN TO VALIDATION`
- `RETURN TO RISK REVIEW`
- `REJECTED`
- `SUSPENDED`
- `REACTIVATION APPROVED`
- `RETIREMENT APPROVED`

Every verdict states rationale, exact scope, accepted/rejected/qualified inputs, conditions, unresolved issues, effective time, expiry, monitoring, follow-up, decision alternatives, and authorizing identity.

## 12. Conditional Approval Rules

Conditions must be observable, enforceable, owned, time-bounded, and auditable. Each condition defines the requirement, evidence of satisfaction, verifier, deadline, dependency, and consequence of failure.

Conditions cannot defer fundamental Validation, Risk, custody, monitoring, or kill requirements until after exposure begins. Authority remains inactive until all stated preconditions are verified.

## 13. Return Decision Rules

Return decisions identify the precise destination, defect, affected input, required output, owner, completion criteria, evidence, and lifecycle state.

`RETURN TO RESEARCH` addresses inadequate market rationale, literature, knowledge, or question. `RETURN TO ARCHITECTURE` addresses hypothesis, mechanism, modules, or failure design. `RETURN TO ENGINEERING` addresses fidelity, determinism, parity, or reproducibility. `RETURN TO EXPERIMENTATION` addresses plan, execution, controls, robustness, failures, or EEP. `RETURN TO VALIDATION` addresses scientific assessment. `RETURN TO RISK REVIEW` addresses limits, controls, capital, liquidity, execution, portfolio, or operations.

Return does not imply eventual approval and never overwrites prior history.

## 14. Rejection Decision Rules

Rejection applies when the current institutional purpose is unsupported, defects are decisive, risk is unacceptable, remediation is disproportionate, or continued work lacks justified value.

The record states reasons, scope, rejected alternatives, evidence and risk basis, reconsideration criteria if any, lifecycle destination, closure tasks, and learning requirements. Rejection cannot delete evidence or prevent historical study.

## 15. Deployment Candidate Authorization Rules

This verdict authorizes readiness work only. It requires exact approved versions, complete artifacts, resolved prerequisite conditions, operational ownership, monitoring plan, controls, rollback, security, data and execution readiness, and expiry.

It does not authorize live trading. Any version mismatch or expired prerequisite suspends candidate authority.

## 16. Paper Monitoring Authorization Rules

Paper Monitoring permits forward observation without live capital. Authorization defines duration, markets, instruments, regimes, signal and execution simulation, success and failure criteria, minimum evidence, monitoring cadence, deviation handling, and review trigger.

Paper results are new evidence, not automatic permission for live exposure.

## 17. Limited Live Authorization Rules

Limited Live requires current VEP and RRP, verified paper readiness, constrained capital and exposure, exact instruments and regimes, enforceable loss limits, monitoring, kill conditions, incident response, rollback, duration, and promotion or failure criteria.

Scaling beyond any limit requires a new decision. Limited Live is a controlled institutional experiment, not a ceremonial step toward automatic promotion.

## 18. Live Active Authorization Rules

Live Active requires demonstrated operational stability, current evidence and risk authority, satisfied Limited Live criteria where required, portfolio compatibility, enforceable controls, continuous monitoring, kill and suspension paths, accountable operations, and explicit reassessment cadence.

Full live authority remains bounded; “unlimited live” is prohibited. Capital or scope expansion requires renewed review and authorization.

## 19. Suspension and Reactivation Decision Rules

`SUSPENDED` removes or freezes authority after loss, exposure, monitoring, validation, risk, data, execution, operational, version, or governance breach. It states effective time, position treatment, control actions, notifications, evidence preservation, and required investigation.

`REACTIVATION APPROVED` requires verified root cause, remediation evidence, updated VEP or RRP where affected, control tests, current versions, restored monitoring, revised conditions, and explicit authorization. Time elapsed is not remediation.

## 20. Retirement Decision Rules

Retirement requires reason, effective date, position and authority closure, dependency shutdown, final monitoring and failure analysis, preserved evidence and decisions, successor relationships, learning artifacts, Knowledge OS contribution, retention, and archival instructions.

Retirement is irreversible for the retired identity. Renewed work requires a governed successor version or new Strategy ID.

## 21. Monitoring and Reporting Obligations

Every forward or live authorization defines metrics, sources, cadence, normal range, warning and breach thresholds, owners, recipients, response times, evidence capture, escalation, and mandatory reports.

Monitoring covers performance only as one dimension alongside exposure, loss, risk, data, execution, operations, portfolio interaction, validation assumptions, regime alignment, edge decay, and compliance with scope and conditions.

Monitoring cannot silently alter thresholds, strategy logic, or authority.

## 22. Decision Expiry and Reassessment Triggers

Every authorization has an expiry date or objective expiry condition. Reassessment triggers include strategy or implementation change, VEP or RRP amendment/revocation/expiry, capital or scope change, limit breach, monitoring failure, edge decay, regime shift, data or execution change, operational incident, contradiction, and governance amendment.

Expired authority cannot be extended informally. Continued action requires a new or amended EDP.

## 23. Decision Freezing and Chain of Custody

Freezing seals inputs, classifications, review, verdict, rationale, scope, conditions, authorizations, obligations, expiry, artifacts, and audit trail. Frozen packages cannot be edited in place.

Custody records intake, access, challenges, drafting, freeze, issuance, acknowledgement, downstream use, amendments, revocation, supersession, and archival. Loss of integrity suspends authority.

## 24. Integration with MACP

MACP governs requests, intake, questions, returns, verdict issuance, authorizations, acknowledgements, breaches, suspensions, reactivation, retirement, amendments, revocation, supersession, and archival. Each message cites exact strategy, VEP, RRP, EDP, artifact, workflow, and agent versions.

Informal communication creates no authority.

## 25. Integration with SMI

SMI maintains governed decision and authorized operating state: current version, owners, conditions, limits, monitoring, breaches, locks, effective time, expiry, and downstream acknowledgements. It cannot silently mutate a frozen decision.

Conflicting or stale critical state blocks issuance or triggers suspension.

## 26. Integration with EES

The decision cites exact admissible evidence and preserves provenance, scope, uncertainty, limitations, contradictions, and custody. Decision rationale and observed outcomes become governed evidence, but the decision itself does not prove the hypothesis.

## 27. Integration with WOE

WOE enforces intake, review, drafting, freeze, issuance, return, authorization, monitoring, suspension, reactivation, retirement, amendment, revocation, supersession, and archival gates.

No lifecycle transition occurs until the EDP is issued, acknowledged, and its preconditions are satisfied.

## 28. Integration with Agent Registry

Only an active registered Executive Decision Agent with appropriate rights may issue authority-bearing EDP verdicts. It cannot perform Validation, Risk Review, engineering, or evidence mutation.

Delegation is bounded and auditable; final decision authority remains with the registered owner.

## 29. Integration with Artifact Registry

The EDP, intake record, review workpapers, verdict, authorization, returns, rejections, suspensions, reactivations, retirements, amendments, revocations, supersessions, acknowledgements, and reports are registered artifacts with identity, version, lineage, provenance, status, consumers, retention, and audit history.

## 30. Integration with Strategy Lifecycle Standard

The EDP is mandatory for transitions to Deployment Candidate, Paper Monitoring, Live Limited, Live Active, suspension release, Retired, and other final lifecycle actions. It binds authority to the exact SLS record and versions.

Material changes return the strategy to the required lifecycle gate and suspend incompatible downstream authority.

## 31. Integration with Experiment Evidence Package

EEP evidence is consumed through Validation lineage. Executive review may inspect experiments, negative controls, failures, deviations, and limitations but cannot independently reclassify inadmissible evidence or bypass VEP.

## 32. Integration with Validation Evidence Package

Only an issued, current VEP may support a decision. Its verdict, scope, limitations, conditions, accepted/rejected/qualified evidence, open questions, expiry, and revalidation triggers remain binding.

VEP revocation, expiry, or material amendment triggers immediate EDP impact review.

## 33. Integration with Risk Review Package

Only an issued, current RRP may support deployment-related authority. Its verdict, scope, limits, conditions, monitoring, kill, suspension, reactivation, expiry, and reassessment triggers remain binding.

RRP revocation, expiry, breach, or material amendment triggers restriction or suspension pending review.

## 34. Governance

### 34.1 Mandatory review areas

Every decision reviews strategy identity and lifecycle, VEP and RRP verdicts and limitations, evidence and risk sufficiency, open issues, contradictions, deployment and monitoring readiness, capital and exposure, execution and operations, portfolio compatibility, kill, suspension, reactivation, expiry, reassessment, and learning.

### 34.2 Mandatory rules

1. Only issued VEPs and RRPs may be consumed.
2. Validation and Risk scope cannot be broadened.
3. All prerequisite limitations remain visible.
4. Candidate, Paper, Limited Live, and Live Active are separate grants.
5. Exact scope, conditions, monitoring, kill requirements, expiry, and reassessment are mandatory.
6. Accepted, rejected, and qualified inputs plus unresolved issues are explicit.
7. Backtests and optimization cannot independently justify deployment.
8. Validation evidence and Risk Review cannot be rewritten or ignored.
9. Frozen packages cannot be edited in place.
10. Amendments create new versions; revoked and rejected decisions remain reconstructable and learnable.

### 34.3 Decision handoff outputs

Each EDP produces one or more governed outputs: lifecycle transition, Deployment Candidate authorization, Paper Monitoring authorization, Limited Live authorization, Live Active authorization, return-to-stage order, rejection record, suspension order, reactivation order, retirement order, follow-up workflow, monitoring mandate, risk-control mandate, or learning-artifact requirement.

### 34.4 Exceptions and change control

Exceptions are explicit, scoped, time-bounded, independently approved, and accompanied by compensating controls. They cannot override Validation or Risk blocks, authorize absent monitoring or kill controls, broaden scope, or conceal unresolved issues.

Changes to this standard require cross-system impact analysis, independent governance review, executive approval, versioning, migration instructions, and preservation of prior versions.

### 34.5 Institutional rule

Every future AI Quant Lab executive decision must produce a conforming Executive Decision Package before a strategy may advance to Deployment Candidate, Paper Monitoring, Limited Live, Live Active, suspension release, retirement, or any final lifecycle transition.
