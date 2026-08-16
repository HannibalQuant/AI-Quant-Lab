# Strategy Lifecycle Standard (SLS) v1.0

## Specification Control

| Field | Value |
|---|---|
| Standard ID | `AIQL-SLS` |
| Version | `1.0.0` |
| Status | Proposed for Sprint 23 review |
| Scope | Every institutional trading strategy and every governed strategy version |
| Authority | Institutional governance, Decision OS, Research OS, Agent Contract Framework, MACP, SMI, EES, WOE, Agent Registry, and Artifact Registry |
| Provider dependency | None |
| Change control | Strategy lifecycle governance with independent validation, risk, executive, and affected-agent review |

This standard defines the constitutional lifecycle of a strategy from first observation through archival. It governs identity, hypothesis integrity, architecture, implementation fidelity, experiments, evidence, validation, risk review, executive decisions, deployment readiness, monitoring, degradation, suspension, retirement, learning, and reconstruction.

It is not a strategy, implementation, backtesting framework, deployment mechanism, database, API, or schema. A strategy is institutionally valid only to the extent that its identity, current version, lifecycle state, evidence, approvals, restrictions, and history conform to this standard.

## 1. Strategy Lifecycle Philosophy

### 1.1 Strategy as a governed hypothesis

A strategy is a falsifiable claim that defined market behavior can be converted into repeatable decisions under declared conditions, constraints, costs, and risks. Rules and measurements operationalize that claim; they do not replace its economic or behavioral rationale.

### 1.2 Lifecycle before performance

Performance does not grant authority. A favorable simulation, optimized parameter set, or recent live result cannot move a strategy through the lifecycle without the required ownership, artifacts, evidence, reviews, and decisions.

### 1.3 Separation of institutional functions

Market observation, hypothesis creation, architecture, engineering, experimentation, validation, risk governance, executive decision, and monitoring remain independently owned. Separation prevents an originating agent from manufacturing its own approval.

### 1.4 Conditional validity

Every edge is conditional. Strategy validity depends on the stated market mechanism, regime, instruments, time horizon, execution assumptions, risk limits, evidence version, and operational environment. Approval outside that scope is prohibited.

### 1.5 Lifecycle as accumulated accountability

Each transition adds obligations without erasing earlier reasoning. Rejection, degradation, suspension, and retirement preserve institutional value because they reveal invalid assumptions, boundary conditions, and failure mechanisms.

## 2. Strategy Lifecycle Principles

The following principles are binding:

1. **No Strategy Without Identity.** Every institutional strategy has a persistent Strategy ID.
2. **No Strategy Without Hypothesis.** Rules without a falsifiable claim are not a strategy.
3. **No Hypothesis Without Market Rationale.** The claim must explain the behavior and mechanism expected to create edge.
4. **No Architecture Without Mechanism.** Measurements follow information needs; indicators do not define the edge.
5. **No Implementation Without Approved Architecture.** Engineering preserves scientific intent.
6. **No Experiment Without Registered Plan.** Methods and acceptance criteria precede results.
7. **No Validation Without Frozen Evidence.** Review uses immutable, version-exact evidence packages.
8. **No Risk Approval Without Validated Evidence.** Scientific adequacy precedes institutional risk acceptance.
9. **No Deployment Without Executive Decision.** Technical readiness cannot substitute for authorization.
10. **No Live Strategy Without Monitoring.** Live authority requires observability, thresholds, and kill conditions.
11. **No Silent Strategy Mutation.** Every material or parameter change is classified, versioned, and reviewed.
12. **No Backtest-Only Approval.** A backtest is one evidence type, not proof of edge.
13. **No Optimization-Only Justification.** Optimization may test stability; it cannot create a mechanism.
14. **No Retirement Without Learning Record.** Closure produces durable institutional knowledge.
15. **Every State Must Be Auditable.** Current status and complete history must be reconstructable.

Where speed conflicts with these principles, governance takes precedence unless an authorized emergency control explicitly limits activity to capital protection.

## 3. Strategy Identity Model

### 3.1 Strategy ID

The Strategy ID is permanent, unique, non-semantic, and never reused. Names, owners, implementations, instruments, and states may change without changing the identifier when the underlying hypothesis and decision logic remain materially continuous.

### 3.2 Identity boundary

A new Strategy ID is required when a change creates a different edge hypothesis, market mechanism, decision structure, exposure profile, or intended institutional purpose. A new version is sufficient only when lineage remains scientifically and operationally meaningful.

### 3.3 Strategy name

The Strategy Name is human-readable and descriptive. It must not imply approval, robustness, profitability, or production status.

### 3.4 Version identity

Every institutional reference resolves to both Strategy ID and exact strategy version. References to a strategy without a version are informational and inadmissible for validation, risk review, deployment, or decision authority.

### 3.5 Identity continuity

Mergers, splits, adaptations, and portfolio compositions must record predecessor and successor relationships. Derived strategies do not inherit approval automatically.

## 4. Strategy Object Model

The Strategy Record is the authoritative lifecycle record. It references governed objects rather than embedding mutable copies of evidence or artifacts.

| Required field | Governance requirement |
|---|---|
| Strategy ID | Permanent institutional identifier |
| Strategy Name | Stable descriptive name |
| Strategy Type | Registered lifecycle type |
| Strategy Family | Behavioral strategy family |
| Target Market | Declared venue or market domain |
| Target Instrument | Exact instrument or governed universe |
| Target Timeframe | Decision and observation horizon |
| Target Regime | Conditions in which the mechanism is expected to operate |
| Current Lifecycle State | Current authorized state |
| Owner Agent | Accountable lifecycle owner within registry rights |
| Originating Workflow | Governing WOE workflow |
| Source MACP Message | Initiating communication reference |
| Related SMI Memory Objects | Governed shared-state references |
| Related EES Evidence Packages | Exact evidence package references |
| Related Artifact Records | Specifications, implementations, reports, and outputs |
| Related Knowledge Objects | Cited institutional knowledge |
| Related Decision Objects | Approval, rejection, exception, and return decisions |
| Related Agent Records | Participating registered agents and contract versions |
| Hypothesis | Falsifiable strategy claim |
| Market Rationale | Observed behavior and economic or behavioral explanation |
| Expected Edge Mechanism | Causal or structural mechanism expected to persist |
| Information Inputs | Required information categories and source constraints |
| Indicator Modules | Justified measurements mapped to information needs |
| Entry Logic | Conditions initiating exposure |
| Exit Logic | Conditions terminating exposure |
| Stop Logic | Loss-limiting and invalidation behavior |
| Risk Logic | Strategy-level exposure constraints |
| Position Sizing Logic | Governed sizing rationale and boundaries |
| Regime Filters | Inclusion, exclusion, and uncertainty handling |
| Invalidation Conditions | Conditions that falsify or suspend confidence in the hypothesis |
| Failure Modes | Scientific, market, execution, operational, and governance failures |
| Experiment Plan | Registered plan and version |
| Validation Verdict | Verdict, limitations, scope, and evidence version |
| Risk Verdict | Verdict, limits, conditions, and expiry |
| Executive Decision | Authorized decision and cited inputs |
| Deployment Status | Candidate, paper, limited live, active, suspended, or none |
| Monitoring Requirements | Metrics, frequency, owners, thresholds, and response paths |
| Edge Decay Status | Current decay classification and supporting evidence |
| Suspension Conditions | Mandatory and discretionary triggers |
| Retirement Conditions | Scientific, risk, operational, and economic exit criteria |
| Current Version | Exact governed version |
| Previous Versions | Ordered immutable version references |
| Created At | Institutional creation time |
| Updated At | Last governed update time |
| Audit Trail | Immutable lifecycle events and authorities |

Missing required fields block advancement unless the field is explicitly inapplicable, the rationale is recorded, and the relevant gate authority accepts the exception.

## 5. Strategy Lifecycle States

The canonical lifecycle is:

**Proposed → Researching → Hypothesis Defined → Architecture Drafted → Architecture Approved → Implementation Drafted → Implementation Verified → Experiment Planned → Experiment Executed → Evidence Packaged → Validation Review → Validation Passed → Risk Review → Risk Approved → Executive Decision Pending → Approved for Deployment Candidate → Paper Monitoring → Live Limited → Live Active → Degraded → Suspended → Retired → Archived**

### 5.1 State meanings

| State | Institutional meaning | Required exit authority |
|---|---|---|
| Proposed | Observation or question registered under a Strategy ID | Research workflow owner |
| Researching | Market behavior and prior knowledge under investigation | Research authority |
| Hypothesis Defined | Falsifiable mechanism and failure conditions recorded | Strategy architecture authority |
| Architecture Drafted | Modular strategy design produced | Independent architecture review |
| Architecture Approved | Scientific intent approved for faithful implementation | Authorized architecture approver |
| Implementation Drafted | Research implementation exists but is not verified | Engineering verification authority |
| Implementation Verified | Fidelity, determinism, tests, and deviations reviewed | Experiment planning authority |
| Experiment Planned | Registered, versioned plan is approved | Experiment Orchestrator |
| Experiment Executed | Planned runs completed with preserved outputs | Evidence-producing owner |
| Evidence Packaged | EES package frozen with custody and limitations | Validation intake authority |
| Validation Review | Independent scientific review in progress | Validation Agent |
| Validation Passed | Evidence accepted within explicit scope and limits | Risk intake authority |
| Risk Review | Institutional deployment risk under review | Risk Governance Agent |
| Risk Approved | Risk accepted within explicit limits and validity period | Executive intake authority |
| Executive Decision Pending | Complete decision record awaiting authority | Executive Decision Agent |
| Approved for Deployment Candidate | Eligible for readiness work; not live-approved by status alone | Deployment governance |
| Paper Monitoring | Forward observation without live capital authority | Risk and executive gates |
| Live Limited | Constrained capital, exposure, universe, and duration | Risk and executive gates |
| Live Active | Authorized production operation within approved scope | Continuous monitoring governance |
| Degraded | Edge, risk, data, execution, or operations breached a review threshold | Review or suspension authority |
| Suspended | Trading authority removed or disabled | Reactivation governance |
| Retired | No new trading authority; learning and closure complete | Retirement authority |
| Archived | Immutable historical record retained for reconstruction | Archival governance |

### 5.2 Transition discipline

No stage may be skipped. A fast-tracked process may compress elapsed time but must satisfy every gate. Return transitions are permitted when recorded with cause, owner, required remediation, and invalidated downstream states.

### 5.3 Terminal and reversible states

Rejection may occur at any review gate and returns the strategy to a named earlier state or initiates retirement. Suspension is reversible only through explicit reactivation. Retirement is not reversible; renewed work requires a successor version or new Strategy ID under governance.

## 6. Strategy Classification

Every strategy is classified by family, market, instrument, timeframe, regime, holding horizon, directionality, data dependency, execution sensitivity, capacity profile, and institutional purpose.

Mandatory Strategy Types are:

1. **Trend Following Strategy** — captures persistent directional movement.
2. **Breakout Strategy** — acts on price acceptance beyond a defined structure.
3. **Momentum Strategy** — acts on persistence in returns or participation.
4. **Pullback Continuation Strategy** — enters temporary retracement within a continuing directional structure.
5. **Mean Reversion Strategy** — acts on conditional return toward a defensible reference state.
6. **Volatility Expansion Strategy** — acts on transition into higher realized movement.
7. **Volatility Compression Strategy** — governs exposure around persistent contraction or its resolution.
8. **Regime-Adaptive Strategy** — changes governed modules based on independently defined regime state.
9. **Hybrid Strategy** — combines distinct mechanisms whose contribution and interaction are separately testable.
10. **Portfolio Strategy** — governs allocation or interaction among multiple strategy exposures.
11. **Monitoring-Only Strategy** — retained for forward observation without trading authority.
12. **Retired Research Strategy** — closed strategy retained for historical study and learning.

Classification never substitutes for mechanism. Hybrid and adaptive classifications require stronger modular attribution because complexity can conceal unsupported logic.

## 7. Strategy Hypothesis Requirements

Before architecture, the record must define:

- the market observation and bounded research question;
- the behavior expected to recur;
- the economic, behavioral, structural, liquidity, or risk-transfer mechanism;
- the target market, regime, horizon, and participant context;
- expected persistence and plausible decay mechanism;
- null and alternative hypotheses;
- competing explanations;
- assumptions and unknowns;
- falsification and failure conditions;
- required evidence and pre-test confidence.

The hypothesis must be specific enough to fail. It may not be retrofitted to explain observed results without a new version and an independent research cycle.

## 8. Strategy Architecture Requirements

Architecture translates the hypothesis into modular decision logic while preserving the mechanism.

Every architecture must define:

- regime identification and uncertainty behavior;
- required information: direction, momentum, volatility, participation, liquidity, efficiency, risk, and timing as applicable;
- measurements justified for each information need;
- redundancy and dependency analysis;
- entry, confirmation, exit, stop, sizing, trade-management, and monitoring modules;
- module ownership and boundaries;
- expected contribution of each module;
- interaction assumptions and failure propagation;
- prohibited interpretations and non-goals;
- experimentable alternatives;
- known risks, open questions, and invalidation conditions.

Mechanism precedes measurement. Indicators are sensors. Replacing a measurement does not necessarily change identity; replacing the mechanism does.

Architecture approval freezes the scientific intent for the implementation cycle. Later changes follow the change classification rules in Section 19.

## 9. Strategy Implementation Requirements

Implementation must be faithful to the approved architecture and must preserve its information boundaries, timing model, execution assumptions, and failure behavior.

The implementation record must provide:

- exact architecture version implemented;
- deterministic decision semantics;
- declared data, dependency, timing, cost, and execution assumptions;
- traceability from each strategy module to implementation artifacts;
- tests for module behavior, boundaries, and failure paths;
- reproducibility requirements and environment constraints;
- explicit deviations, ambiguities, and engineering interpretations;
- parity requirements across research and target representations;
- limitations that may affect experimental interpretation.

Engineering may reject ambiguity or return the architecture for clarification. It may not resolve ambiguity by silently changing the hypothesis or inventing strategy logic.

## 10. Strategy Experiment Requirements

Experiments are registered before execution and governed independently of desired outcomes. Each plan must define:

- Experiment ID, purpose, strategy and implementation versions;
- independent and dependent variables;
- datasets, periods, markets, regimes, and inclusion rules;
- baselines, benchmarks, positive controls, and negative controls;
- primary and secondary metrics;
- transaction-cost and execution assumptions;
- sample-sufficiency rationale;
- out-of-sample, walk-forward, robustness, sensitivity, and stress-testing design;
- parameter ranges justified by the architecture;
- stopping, failure, replication, and acceptance criteria;
- planned comparisons and multiple-testing controls;
- resource dependencies and execution owner.

Post-result changes create a new experiment version and cannot overwrite the original plan. Optimization output is exploratory or stability evidence; it is not independent confirmation.

## 11. Strategy Evidence Requirements

Strategy evidence must comply with EES and remain attached to provenance, scope, uncertainty, limitations, custody, and exact versions.

The evidence body should include, when applicable:

- market observation and literature evidence;
- architecture and implementation fidelity evidence;
- experiment results and negative findings;
- out-of-sample and walk-forward evidence;
- parameter stability and sensitivity evidence;
- Monte Carlo and stress evidence;
- negative control and adversarial evidence;
- cross-market, cross-timeframe, cross-regime, and cross-period evidence;
- execution realism and operational evidence;
- contradictions, failed replications, and unresolved unknowns.

A frozen validation package cannot be edited in place. New findings become amendments or new evidence versions. Backtest evidence alone is insufficient, and the absence of contradictory evidence is not proof of robustness.

## 12. Strategy Validation Requirements

Validation is independent from research, architecture, engineering, and experiment execution. The Validation Agent evaluates whether frozen evidence supports the hypothesis within the declared scope.

Validation must assess:

- hypothesis-to-test consistency;
- implementation fidelity and reproducibility;
- sample quality and sufficiency;
- statistical uncertainty and practical significance;
- out-of-sample priority and leakage controls;
- robustness across parameters, periods, regimes, markets, and perturbations;
- costs, execution realism, and sensitivity;
- alternative explanations and contradictory findings;
- limitations and unresolved assumptions;
- replication status and failure classification.

Authorized verdicts are `APPROVED`, `APPROVED WITH LIMITATIONS`, `REQUIRES MORE EVIDENCE`, and `REJECTED`. Lifecycle state `Validation Passed` requires an approval verdict whose conditions are satisfied and recorded. Validation cannot authorize deployment or modify evidence.

## 13. Strategy Risk Review Requirements

Risk review begins only after validation or an explicitly governed qualified-evidence exception. It evaluates deployment acceptability rather than scientific truth.

The review must address:

- loss distribution, drawdown, tail exposure, leverage, and gap behavior;
- liquidity, capacity, market impact, and execution risk;
- correlation, concentration, common-factor, and portfolio interaction risk;
- model, data, technology, operational, vendor, and governance risk;
- stress scenarios and failure containment;
- capital allocation boundaries and exposure limits;
- monitoring thresholds, kill conditions, and escalation paths;
- validity period, assumptions, and conditions for re-review.

Authorized verdicts are `APPROVED`, `APPROVED WITH LIMITS`, `REQUIRES RISK MITIGATION`, and `REJECTED`. Risk Governance cannot rewrite validation evidence or change strategy logic.

## 14. Strategy Executive Decision Requirements

Executive decision integrates independent outputs without replacing them. The decision record must cite exact strategy, architecture, implementation, evidence, validation, risk, monitoring, and artifact versions.

It must state:

- the authorized outcome and scope;
- alternatives considered and reasons rejected;
- unresolved conflicts and their treatment;
- assumptions, conditions, limits, and expiry;
- capital and deployment boundaries where applicable;
- required monitoring and review cadence;
- return, rejection, suspension, or escalation instructions;
- accountable authority and timestamp.

The Executive Decision Agent may authorize a Deployment Candidate, return work to a named lifecycle state, impose conditions, or reject. It may not ignore unresolved validation or risk blocks, alter evidence, or manufacture missing approval.

## 15. Deployment Candidate Rules

Deployment Candidate status means that scientific, risk, and executive gates permit controlled readiness work. It does not itself authorize live capital.

Candidate readiness requires:

- exact approved implementation and artifact versions;
- resolved mandatory validation and risk conditions;
- operational ownership and dependency readiness;
- paper-monitoring plan and acceptance thresholds;
- execution and data-quality controls;
- exposure limits, kill conditions, and rollback path;
- observability and incident-response readiness;
- authorization scope and expiry.

Any mismatch between candidate and approved versions invalidates candidate status until reconciled. Paper Monitoring must precede live activation unless an explicit, auditable exception is approved by validation, risk, and executive authorities.

## 16. Monitoring and Edge Decay Rules

### 16.1 Monitoring contract

Before live authority, the strategy must define metrics, expected ranges, sampling cadence, owners, alert thresholds, evidence capture, response paths, and comparison baselines.

Monitoring must cover:

- signal frequency, participation, and regime alignment;
- expectancy, return distribution, drawdown, and tail events;
- execution costs, slippage, fills, latency, and rejected actions;
- data integrity and dependency health;
- exposure, correlation, concentration, liquidity, and capacity;
- divergence between expected, simulated, paper, and live behavior;
- parameter, feature, and decision-distribution drift;
- changes in market mechanics and edge assumptions.

### 16.2 Edge decay classification

Edge decay is classified as `None Detected`, `Watch`, `Probable`, `Confirmed`, or `Uncertain`. Classification must distinguish statistical noise, adverse regime, execution degradation, data failure, implementation drift, capacity effects, and structural mechanism failure.

### 16.3 Required response

Threshold breaches produce a MACP event, SMI state update, EES monitoring evidence, Artifact Registry record, and WOE response path. Degradation may restrict exposure, return the strategy to research, initiate validation or risk review, or trigger suspension. Monitoring may not silently rewrite logic or loosen thresholds.

## 17. Suspension and Emergency Control

Suspension removes trading authority while preserving identity, evidence, state, and audit history.

Mandatory suspension triggers include:

- breach of an executive or risk limit;
- invalid, stale, or unavailable critical evidence;
- material implementation divergence;
- failed data or execution integrity;
- uncontrolled exposure or kill-switch activation;
- unauthorized mutation or version mismatch;
- confirmed governance violation;
- operational condition that prevents safe monitoring or containment.

Emergency authority may stop or reduce activity immediately to protect capital or integrity. It may not approve new logic, erase evidence, or bypass post-event review.

Reactivation requires root-cause evidence, remediation artifacts, renewed verification, affected gate reviews, an explicit decision, and restoration of monitoring readiness. The original suspension remains immutable.

## 18. Retirement and Learning

A strategy enters retirement when its mechanism is invalidated, edge decays beyond acceptable recovery, risk becomes unacceptable, capacity or economics fail, dependencies become unsustainable, governance requires closure, or continued research has insufficient value.

Retirement requires:

- final lifecycle and deployment state;
- reason and responsible authority;
- closure of positions, permissions, dependencies, and outstanding workflows;
- preserved versions, artifacts, evidence, decisions, incidents, and monitoring history;
- final failure and performance analysis;
- unresolved questions and successor relationships;
- Knowledge OS contributions and a registered learning artifact;
- retention and archival instructions.

Retirement is not deletion. A retired strategy cannot trade or receive new institutional work. Archived records remain discoverable for comparison, negative knowledge, audit, and prevention of repeated failure.

## 19. Feedback Loop Rules

Feedback may originate from research, experiments, validation, risk, paper monitoring, live monitoring, incidents, failures, or external knowledge changes.

Every feedback item must identify:

- originating event and evidence;
- affected hypothesis, module, assumption, version, and scope;
- materiality and urgency;
- proposed lifecycle destination;
- required owners and review gates;
- knowledge and artifact outputs.

Change classification is mandatory:

| Change class | Examples | Minimum response |
|---|---|---|
| Non-material correction | Wording or metadata with no semantic change | Patch version and audit review |
| Parameter change | Threshold, period, sizing, or limit | New version, experiment, and proportional revalidation/risk review |
| Measurement change | Indicator or data source serving the same information need | Architecture review, experiment, evidence, validation |
| Logic change | Entry, exit, regime, stop, or sizing behavior | New version and lifecycle return to architecture |
| Mechanism change | Different explanation of edge | New Strategy ID unless governance proves identity continuity |
| Scope change | New market, instrument, timeframe, regime, or deployment class | New version with scoped evidence, validation, and risk decision |

Positive feedback cannot silently expand authority. Negative feedback cannot be hidden by selecting a new comparison window or redefining success after observation.

## 20. Auditability and Reconstruction

An independent reviewer must be able to reconstruct what the strategy was, why it existed, what was known, what was tested, what changed, who decided, which limits applied, what traded, what failed, and why the strategy advanced, returned, degraded, suspended, or retired.

Reconstruction requires:

- immutable state-transition history;
- exact contract and Agent Registry versions;
- MACP messages and acknowledgements;
- SMI state versions and locks;
- frozen EES evidence and chain of custody;
- WOE stages, gates, blocks, returns, and exceptions;
- Artifact Registry versions and lineage;
- hypothesis, architecture, implementation, experiment, validation, risk, and decision records;
- deployment, monitoring, incident, suspension, and retirement records;
- timestamps, authorities, rationales, and rejected alternatives.

Missing reconstruction material is a governance defect and may invalidate approval, require suspension, or prevent archival closure.

## 21. Integration with MACP

All lifecycle actions are communicated through authorized MACP messages. Each request, acceptance, handoff, evidence transfer, verdict, escalation, state transition, exception, and cancellation must identify Strategy ID, exact version, lifecycle state, workflow, artifacts, evidence, sender authority, intended consumer, and required action.

MACP transports lifecycle claims; it does not create authority. Informal conversation cannot approve architecture, validation, risk, deployment, reactivation, or retirement.

## 22. Integration with SMI

SMI holds governed shared working state for the active lifecycle. Strategy state objects must identify owner, readers, writers, source MACP message, related evidence and artifacts, current and previous versions, lock status, expiry, and audit trail.

Evidence remains immutable through EES; institutional artifacts remain governed through ART. SMI cannot become a hidden substitute for either. Conflicting or stale shared state blocks transitions until reconciled.

## 23. Integration with EES

All evidence supporting strategy claims, validation, risk, decisions, monitoring, degradation, suspension, or retirement follows EES. Consumers cite exact frozen versions and carry provenance, scope, uncertainty, limitations, contradictions, admissibility, and custody status.

Evidence is not a lifecycle decision. A valid package may support a verdict, but only the contract-authorized agent can issue that verdict.

## 24. Integration with WOE

WOE coordinates the canonical path:

**Market Observation → Research Question → Strategy Hypothesis → Strategy Architecture → Implementation Specification → Research Implementation → Experiment Plan → Experiment Execution → Evidence Package → Validation Verdict → Risk Governance Verdict → Executive Decision → Deployment Candidate → Paper Monitoring → Limited Live → Full Live or Rejected → Continuous Monitoring → Edge Decay Review → Retirement or Feedback Loop**

WOE enforces owners, assignments, dependencies, stage gates, required inputs and outputs, blocks, returns, timeouts, exceptions, cancellations, and audit events. WOE cannot override the state authority defined here or assign work outside an agent contract.

## 25. Integration with Agent Registry

Only active, registered agents may perform lifecycle work. The Agent Registry determines identity, contract binding, message rights, memory rights, evidence rights, workflow eligibility, decision authority, approval authority, rejection authority, escalation authority, and delegation limits.

Technical capability is not permission. Restricted, suspended, deprecated, or retired agents act only within their registry status. No agent may change its own authority or self-approve an output that requires independence.

## 26. Integration with Artifact Registry

Every institutional product of the lifecycle is registered in ART, including market reports, hypothesis documents, architecture specifications, implementations, experiment plans and outputs, evidence packages, validation reports, risk reviews, executive decisions, deployment candidate records, monitoring reports, edge-decay reports, failure reviews, suspensions, and retirement learning records.

Artifacts retain identity, owner, version, lineage, provenance, scope, limitations, consumers, dependencies, quality state, freeze status, and audit history. A code artifact is not the strategy. A backtest artifact is not validation. A report is not a decision unless issued by the authorized agent and registered as the corresponding decision artifact.

## 27. Governance

### 27.1 Authority model

- The Quant Strategy Architect owns hypothesis and architecture proposals, never self-approval.
- The Quant Strategy Engineer owns faithful implementation, never scientific reinterpretation.
- The Experiment Orchestrator owns lifecycle coordination of registered experiments, never results or validation.
- The Validation Agent owns independent scientific verdicts, never deployment approval.
- The Risk Governance Agent owns institutional risk verdicts and limits, never scientific evidence.
- The Executive Decision Agent owns institutional decisions within unresolved validation and risk constraints.
- Monitoring owners observe and escalate; they do not silently mutate strategy logic.
- Human authorities act through the same identity, evidence, decision, artifact, and audit requirements.

### 27.2 Mandatory rules

1. A strategy may not exist institutionally without a Strategy ID.
2. A strategy may not proceed beyond research without a falsifiable hypothesis.
3. A hypothesis must explain why market behavior may create edge.
4. Architecture must define mechanism before indicators.
5. Indicators are measurement tools, not edge by themselves.
6. Engineering may not change the approved hypothesis.
7. Implementation deviations must be explicit and reviewed.
8. Experiments must be planned before execution.
9. Backtest results alone cannot validate a strategy.
10. Optimization output cannot prove edge.
11. Validation must use frozen EES evidence packages.
12. Risk review must use validated or explicitly qualified evidence.
13. Executive decisions must cite validation and risk outputs.
14. Deployment Candidate status does not equal live approval.
15. Live activation requires monitoring and kill conditions.
16. Parameter changes require versioning and may trigger revalidation.
17. Material logic changes require a new version or identity.
18. Degraded strategies must enter review, suspension, or retirement.
19. Suspended strategies cannot trade without governed reactivation.
20. Retired strategies remain historically reconstructable.
21. Every failure must generate a learning artifact.

### 27.3 Exceptions

Exceptions must be rare, time-bounded, scoped, justified, approved by every authority whose gate is affected, and recorded with compensating controls and expiry. Exceptions cannot legalize self-approval, mutable validation evidence, hidden live operation, or deletion of history.

### 27.4 Amendments

Changes to this standard require an amendment proposal, affected-system analysis, contradiction review, backward-compatibility assessment, independent governance review, executive approval, version release, migration instructions, and preserved prior versions.

### 27.5 Institutional rule

Every future AI Quant Lab strategy must obey this standard before it can be researched, implemented, experimented upon, evidenced, validated, risk-reviewed, decided, deployed, monitored, modified, degraded, suspended, retired, or archived.
