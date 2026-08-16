# Workflow Orchestration Engine (WOE) v1.0

## Specification control

| Field | Value |
|---|---|
| Standard ID | `AIQL-WOE` |
| Standard name | Workflow Orchestration Engine |
| Version | `1.0.0` |
| Status | Proposed for Sprint 20 review |
| Scope | All institutional workflows executed by AI Quant Lab agents and authorized human authorities |
| Authority | Agent Contract Framework, Decision OS, Research OS, MACP, SMI, and EES |
| Provider dependency | None |
| Change control | Workflow Governance, QA, Executive Decision, and affected domain-owner review |

WOE is the constitutional workflow layer that governs how institutional work is identified, initiated, routed, accepted, executed, paused, resumed, blocked, reviewed, returned, approved, rejected, cancelled, archived, and converted into downstream action. It does not prescribe software, databases, APIs, schemas, schedulers, or implementation.

Every AI Quant Lab workflow must conform to WOE. No operational convenience, agent capability, or management preference may silently bypass its ownership, evidence, memory, validation, risk, decision, or audit requirements.

## 1. Workflow Philosophy

### 1.1 Workflow as institutional authority

A workflow is a governed chain of responsibilities and state transitions that transforms an authorized institutional question into traceable outputs and decisions. It is not a list of activities. Every stage defines who may act, which inputs are authoritative, which evidence is required, what state may change, and who may approve progression.

### 1.2 Work must survive agent boundaries

Institutional work cannot depend on hidden conversation, model memory, informal handoff, or undocumented intent. A qualified replacement agent must be able to continue from governed MACP messages, SMI state, EES packages, decisions, and audit history.

### 1.3 Progress is not permission

Completion of work does not automatically authorize the next stage. Each stage gate independently establishes readiness. A completed experiment is not validated; a validated strategy is not risk-approved; a risk-approved proposal is not deployed.

### 1.4 Failure is workflow output

Rejection, cancellation, contradiction, blocked dependency, invalid evidence, and failed experiment are legitimate institutional outcomes. WOE preserves them so the institution does not repeat work or learn only from successes.

### 1.5 Coordination without responsibility dilution

Several agents may contribute, but each stage has one accountable owner. Delegation transfers bounded tasks, not constitutional ownership. Consensus cannot replace the required specialist authority.

### 1.6 Workflow state is explicit

Only the registered Workflow Object and related governed states are authoritative. Queue position, conversation activity, generated artifact, or elapsed time cannot imply acceptance, approval, rejection, or completion.

### 1.7 Long-term purpose

A future reviewer must be able to reconstruct the complete workflow: initiating authority, exact inputs, assigned agents, evidence, memory versions, transitions, failures, decisions, conditions, and downstream consequences.

## 2. Workflow Principles

### 2.1 No Work Without Identity

Every institutional work item has a stable Workflow ID before it consumes governed resources or changes state.

### 2.2 No Work Without Owner

Each workflow and stage has one accountable owner. Committees and agent groups may review but cannot replace ownership.

### 2.3 No Hidden Workflow State

Current stage, state, dependencies, blockers, conditions, evidence, decisions, and next action are explicit in SMI and communicated through MACP.

### 2.4 No Stage Skipping

Stages advance only through declared gates. Emergency paths may contain work but cannot manufacture missing validation, risk, or executive authority.

### 2.5 No Evidence-Free Validation

Validation requires an admissible frozen EES package with intact provenance, scope, limitations, versions, and custody.

### 2.6 No Risk-Free Deployment

Deployment requires a current Risk Governance decision, explicit limits, monitoring, kill conditions, and production-readiness evidence.

### 2.7 No Decision Without Traceable Inputs

Every institutional decision cites exact evidence, memory, knowledge, validation, risk, alternatives, and authority versions.

### 2.8 Every Transition Must Be Auditable

Each transition records actor, authority, time, source message, prior state, resulting state, criteria, evidence, and consumers.

### 2.9 Every Agent Acts Within Its Contract

Routing cannot grant responsibilities or decision rights that an agent does not constitutionally possess.

### 2.10 Workflows Preserve Failure

Failed tasks, experiments, controls, reproductions, mitigations, and decisions remain linked to the workflow.

### 2.11 Rejected Work Remains Learnable

Rejection records failed criteria, evidence, alternatives, reconsideration conditions, and knowledge contributions.

### 2.12 Cancellation Does Not Erase History

Cancellation ends authorized future work but retains consumed resources, partial outputs, evidence, reasons, dependencies, and decisions.

### 2.13 Additional principles

- One authoritative current state exists per workflow scope.
- Workflow priority does not alter scientific or governance criteria.
- State changes are versioned, not rewritten.
- Return paths identify owner and required correction.
- Conditions must be objective and enforceable.
- Unknowns and conflicts remain visible.
- Downstream actions cannot exceed upstream scope.

## 3. Workflow Object Model

### 3.1 Definition

A Workflow Object is the stable institutional identity and governed state of one bounded body of work. It coordinates stages, tasks, agents, evidence, memory, decisions, dependencies, errors, and lifecycle without absorbing their distinct authorities.

### 3.2 Mandatory fields

| Field | Institutional requirement |
|---|---|
| Workflow ID | Stable unique identity across lifecycle and versions |
| Workflow Type | Approved workflow class and semantic contract |
| Workflow Owner | Single accountable owner for integration and state |
| Initiating Agent or Human Authority | Authorized originator and jurisdiction |
| Source MACP Message | Exact initiation or current transition message |
| Related Memory Objects | SMI identities and exact versions |
| Related Evidence Packages | EES package identities, states, scope, and versions |
| Related Knowledge Objects | Knowledge OS identities, status, and versions |
| Related Decision Objects | Decision IDs, states, scope, and versions |
| Assigned Agents | Agents, roles, contracts, delegations, and stage assignments |
| Current Stage | Active stage and responsible gate authority |
| Current State | Proposed, Registered, Routed, Accepted, In Progress, Blocked, Under Review, Returned, Approved, Rejected, Cancelled, or Archived |
| Dependencies | Direct and transitive identities, versions, owners, and readiness |
| Blocking Conditions | Condition, owner, severity, effect, and resolution criteria |
| Required Inputs | Exact governed objects required for acceptance or stage entry |
| Required Outputs | Output contracts, consumers, versions, and quality state |
| Acceptance Criteria | Conditions for owner and assignee acceptance |
| Completion Criteria | Observable requirements for workflow completion |
| Validation Requirements | Required validation scope, evidence, authority, and verdict |
| Risk Review Requirements | Required risk scope, limits, controls, and verdict |
| Executive Decision Requirement | Required decision category, inputs, and authority |
| Created At | Governed creation time and actor |
| Updated At | Most recent material transition time and actor |
| Audit Trail | Complete routing, state, task, evidence, error, decision, and access history |
| Archival Policy | Closure, retention, reproducibility, access, and retirement requirements |

### 3.3 Additional properties

Every object defines purpose, institutional question, scope, exclusions, priority, version, deadlines, resource assumptions, security, confidentiality, status cadence, error policy, cancellation authority, return paths, review dates, expiry, and downstream consumers where applicable.

### 3.4 Stable and run identities

Workflow ID preserves one institutional purpose. Material change to purpose, scientific intent, governance path, or output creates a new workflow version or related workflow. Individual tasks, attempts, experiments, reviews, and escalations retain separate identities.

### 3.5 Authoritative fields

Field ownership follows agent contracts. The Workflow Owner controls orchestration state but cannot alter evidence, validation verdicts, risk decisions, knowledge status, or executive decisions issued by competent authorities.

### 3.6 Relationships

Relationships include initiated by, assigned to, depends on, blocks, produces, consumes, validated by, risk-reviewed by, decided by, returned to, supersedes, conflicts with, suspended by, cancelled by, archived with, and feeds back to.

## 4. Workflow Lifecycle

### 4.1 Canonical states

Every workflow follows the governed lifecycle:

**Proposed → Registered → Routed → Accepted → In Progress → Under Review → Approved → Archived**

It may enter **Blocked**, **Returned**, **Rejected**, or **Cancelled** when applicable. The complete controlled state set is:

- Proposed
- Registered
- Routed
- Accepted
- In Progress
- Blocked
- Under Review
- Returned
- Approved
- Rejected
- Cancelled
- Archived

### 4.2 Proposed

An authorized initiator defines the institutional question, purpose, expected outcome, preliminary owner, workflow type, scope, required authorities, and initial dependencies. Proposed work has no execution authority.

### 4.3 Registered

The Workflow Object has stable identity, valid type, owner, source message, scope, lifecycle, inputs, outputs, gates, dependencies, security, and audit policy. Registration does not mean readiness.

### 4.4 Routed

Tasks and stage responsibilities have been assigned to agents whose contracts, capacity, access, versions, and independence satisfy the work. Recipients have not yet accepted.

### 4.5 Accepted

The Workflow Owner and assigned agents explicitly accept scope, authority, inputs, outputs, dependencies, conditions, deadlines, and escalation paths through MACP.

### 4.6 In Progress

At least one authorized stage task is executing. Current stage, health, evidence state, memory state, progress, blockers, and next checkpoint are observable.

### 4.7 Blocked

A required dependency, owner, evidence package, memory state, resource, permission, version, or decision prevents lawful progress. Blocked state defines the cause, owner, interim controls, response path, and deadline.

### 4.8 Under Review

Stage outputs and gate evidence are frozen or otherwise controlled and under authorized review. Producers cannot self-approve where independence is required.

### 4.9 Returned

The reviewer or downstream gate returns work to a named prior stage with failed criteria, required correction or evidence, preserved versions, and the path back to review.

### 4.10 Approved

All completion criteria and required gates for the workflow's declared outcome have passed. Approval is scoped and does not imply deployment unless the workflow is explicitly an executive deployment-authorization workflow.

### 4.11 Rejected

The competent authority determines that the workflow or output cannot proceed within current scope. Rejection records evidence, reasons, alternatives, reconsideration criteria, and learning outputs.

### 4.12 Cancelled

An authorized actor terminates future execution. Partial work, evidence, decisions, resources, dependencies, and downstream impact remain recorded.

### 4.13 Archived

The workflow is closed, reconciled, retained, and removed from active work. It remains reconstructable and discoverable according to access and retention policy.

### 4.14 Transition discipline

No transition occurs from silence, elapsed time, artifact existence, or model assertion. Every transition requires a MACP lifecycle message and corresponding SMI update. Material new evidence or version change may reopen an earlier gate through a new workflow version.

## 5. Workflow Types

### 5.1 Market Research Workflow

Produces objective market intelligence, classifications, uncertainty, and opportunity maps. It cannot produce tradable strategy rules.

### 5.2 Knowledge Acquisition Workflow

Discovers, acquires, evaluates, cites, and packages authoritative sources. It cannot accept institutional knowledge.

### 5.3 Knowledge Curation Workflow

Reviews candidate knowledge, governs lifecycle, lineage, conflicts, and acceptance. It does not conduct research or acquire sources.

### 5.4 Strategy Architecture Workflow

Transforms market understanding and research questions into falsifiable strategy specifications and experiments. It cannot implement or self-approve performance.

### 5.5 Strategy Engineering Workflow

Transforms approved architecture into faithful, reproducible research implementation. It cannot change hypotheses or optimize parameters.

### 5.6 Experiment Workflow

Registers, plans, executes, and packages an approved experiment with complete operational lineage. It cannot validate its own result.

### 5.7 Validation Workflow

Independently reviews frozen EES packages and issues an authorized validation verdict. It cannot modify evidence or approve deployment.

### 5.8 Risk Review Workflow

Assesses validated strategy and portfolio deployment risk, limits, controls, readiness, and kill policy. It cannot rewrite validation evidence.

### 5.9 Executive Decision Workflow

Integrates admissible inputs and independent verdicts into one authorized institutional decision. It cannot override unresolved validation or risk blocks.

### 5.10 Strategy Deployment Candidate Workflow

Coordinates a specific validated, risk-approved, executive-authorized candidate toward technical deployment readiness and handoff. It does not itself activate deployment.

### 5.11 Monitoring Workflow

Collects and routes operational, market, model, execution, evidence, limit, and control states. It cannot silently change governance or disable limits.

### 5.12 Failure Review Workflow

Preserves failure evidence, reconstructs decisions and state, determines causes, assigns corrective actions, and contributes lessons without rewriting history.

### 5.13 Conflict Resolution Workflow

Preserves competing positions and routes factual, scientific, engineering, validation, risk, knowledge, or executive conflicts to competent authorities.

### 5.14 Emergency Suspension Workflow

Coordinates immediate containment and safe-state decisions under delegated emergency authority while preserving evidence, notifications, and post-event review. It cannot create missing approvals.

## 6. Workflow Stage Model

### 6.1 Stage contract

Every stage defines Stage ID, purpose, owner, assigned agents, entry criteria, inputs, dependencies, evidence, SMI state, allowed actions, prohibited actions, outputs, review authority, exit criteria, return path, errors, and audit events.

### 6.2 Stage entry

Entry requires exact input versions, completed predecessor gates, valid agent contracts, accepted task assignments, compatible MACP/SMI/EES versions, and no unresolved blocking condition.

### 6.3 Stage execution

Work remains within approved scope. Material change to hypothesis, implementation, evidence, risk context, or decision use triggers amendment, return, or new workflow version.

### 6.4 Stage exit

Exit requires output reconciliation, completion evidence, limitations, failures, version identity, consumer acknowledgement, and authorized gate decision.

### 6.5 Canonical core strategy workflow

The standard strategy path is:

**Market Research → Strategy Architecture → Engineering Implementation → Experiment Design → Experiment Execution → Evidence Packaging → Validation Review → Risk Governance Review → Executive Decision → Deployment Candidate → Monitoring → Retirement or Feedback Loop**

### 6.6 Feedback loops

Feedback returns work to a named stage using new evidence and preserved history. It cannot turn production outcomes into unregistered optimization or contaminate prior out-of-sample evidence.

### 6.7 Stage gate rules

- Market Research cannot create a tradable strategy.
- Strategy Architecture cannot implement code.
- Engineering cannot change the approved strategy hypothesis.
- Experimentation cannot validate itself.
- Validation cannot approve deployment.
- Risk Governance cannot rewrite validation evidence.
- Executive Decision cannot ignore unresolved validation or risk blocks.
- Deployment cannot occur without executive approval.
- Monitoring cannot silently disable governance.
- Failure review must preserve evidence and decision history.

## 7. Agent Routing Rules

### 7.1 Contract-first routing

Routing begins with responsibility, decision rights, non-responsibilities, required independence, knowledge access, version compatibility, and current agent status. Capability alone is insufficient.

### 7.2 Assignment requirements

Every assignment identifies workflow and stage, task contract, owner, scope, outputs, evidence, memory access, deadline, status cadence, conflicts, escalation, and acceptance criteria.

### 7.3 Single accountable owner

Each workflow and stage has one accountable owner. Parallel agents may contribute under distinct tasks, but ownership does not become collective or ambiguous.

### 7.4 Independence routing

Validation, risk review, QA, and executive review must satisfy required separation from evidence production, implementation, optimization, and prior advocacy.

### 7.5 Parallel routing

Parallel work is permitted when dependencies, evidence freezes, object ownership, write fields, locks, merge rules, and integration authority are explicit.

### 7.6 Reassignment

Reassignment preserves work state, versions, evidence, assumptions, access, partial outputs, errors, and audit history. A new agent cannot infer missing context from private conversation.

### 7.7 Invalid assignment

Assignment is invalid when responsibility, authority, independence, access, compatibility, capacity, or conflict requirements fail. The task returns to routing or escalates.

## 8. Task Acceptance Rules

### 8.1 Acceptance review

The assignee validates identity, owner, purpose, scope, authority, inputs, versions, dependencies, outputs, completion criteria, evidence requirements, memory access, security, deadline, and escalation path.

### 8.2 Acceptance outcomes

- accepted;
- accepted with an explicitly permitted qualification;
- requires correction;
- blocked pending dependency;
- rejected as outside contract;
- escalated for authority, conflict, or feasibility decision.

### 8.3 No implied acceptance

Delivery, read access, heartbeat, preliminary work, or informal reply does not accept a task. Acceptance is a MACP state transition recorded in SMI.

### 8.4 Scope protection

Assignees reject or return requests that require prohibited work. They cannot fill missing scientific, engineering, validation, risk, or executive decisions to meet a deadline.

### 8.5 Amendment

Material scope, input, output, dependency, deadline, or authority change requires a new Task Contract version and renewed acceptance.

### 8.6 Completion

Completion states criteria passed and failed, outputs, versions, evidence, limitations, deviations, unresolved issues, downstream actions, and consumer acknowledgements.

## 9. Dependency and Blocking Rules

### 9.1 Dependency classes

Dependencies include agents, tasks, evidence, knowledge, memory, data, artifacts, experiments, versions, approvals, permissions, resources, external events, validation, risk, executive decisions, and monitoring state.

### 9.2 Dependency record

Every dependency defines identity, version, owner, state, required stage, compatibility, freshness, due time, failure effect, fallback authority, and consumers.

### 9.3 Readiness

A dependency is ready only when authoritative, accessible, compatible, within scope, unexpired, and in the required lifecycle state. Mere existence is insufficient.

### 9.4 Blocking condition

A block defines Block ID, cause, severity, owner, affected stages, evidence, interim controls, resolution criteria, deadline, and response path.

### 9.5 Cycles

Circular dependencies are prohibited unless an approved iterative workflow defines convergence, ownership, evidence boundaries, stopping criteria, and maximum iterations.

### 9.6 Dependency change

Material change triggers impact analysis across queued, active, review, approved, monitoring, and archived workflows. Responses include no action, acknowledge, return, revalidate, rerisk, suspend, cancel, or archive.

### 9.7 Block resolution

A workflow leaves Blocked only after evidence shows resolution and affected owners acknowledge current state. Silence or timeout cannot clear a block.

## 10. Evidence Requirements

### 10.1 EES conformance

All evidentiary inputs and outputs use exact EES identities, versions, provenance, scope, limitations, contradictions, confidence, reproducibility, admissibility, and custody status.

### 10.2 Stage evidence plan

Each stage specifies required evidence types, claims, producing agents, package composition, admissibility, freeze point, reviewers, failure evidence, and transfer consumers before execution.

### 10.3 Evidence gates

Stage progression verifies completeness, quality, scope match, custody, reproducibility, contradiction visibility, version consistency, and current admissibility.

### 10.4 Evidence freeze

Validation, risk, and executive decision stages consume exact frozen or otherwise governance-controlled packages. New evidence creates a new package or review version.

### 10.5 Negative evidence

Failed experiments, negative controls, rejected variants, reproduction discrepancies, and contradictory evidence remain part of workflow evidence. They cannot be removed to pass a gate.

### 10.6 Insufficient evidence

Missing, stale, inadmissible, out-of-scope, mutable, or broken-custody evidence blocks the relevant gate and routes to return, escalation, cancellation, or rejection.

## 11. Memory Requirements

### 11.1 SMI as authoritative state

Every workflow has SMI Workflow, Task, Context, Evidence Reference, Decision, Validation, Risk, Conflict, Lock, and Audit objects as applicable.

### 11.2 Required memory updates

Registration, routing, acceptance, progress, block, review, return, approval, rejection, cancellation, archival, assignment, dependency, evidence, decision, error, and escalation changes update SMI through MACP.

### 11.3 Field ownership

The Workflow Owner updates orchestration fields only. Domain owners retain authority over research, implementation, experiment, evidence, validation, risk, knowledge, and executive decision fields.

### 11.4 Locks

Critical reviews use SMI locks for evidence freezes, decision inputs, state transitions, and conflicting writes. Locks are bounded and auditable.

### 11.5 Memory consistency

Before gates, WOE verifies exact versions, ownership, lifecycle, expiry, conflicts, locks, dependencies, and acknowledgements. Conflicting state blocks progression.

### 11.6 Hidden-state prohibition

Private model memory, chat history, temporary files, or unregistered assumptions cannot establish workflow state or satisfy a gate.

## 12. Validation Gates

### 12.1 Entry requirements

Validation requires a current frozen EES package, exact hypothesis and versions, complete selection and experiment lineage, implementation conformance, reproducibility materials, negative evidence, criteria, and independent validator.

### 12.2 Gate authority

Only the Validation Agent issues the authoritative verdict. Workflow owners record and route it but cannot revise it.

### 12.3 Gate outcomes

- `APPROVED` advances within validated scope.
- `APPROVED WITH LIMITATIONS` advances only with enforceable limitations.
- `REQUIRES MORE EVIDENCE` returns to the named evidence-producing stage.
- `REJECTED` blocks progression of the reviewed version.

### 12.4 Version alignment

Any change to hypothesis, implementation, data, parameters, experiment, evidence, or scope determines whether validation must reopen.

### 12.5 No self-validation

Research, architecture, engineering, and experimentation agents cannot approve their own scientific evidence.

## 13. Risk Gates

### 13.1 Entry requirements

Risk review requires a current applicable validation verdict, exact proposed deployment use, portfolio context, capital and leverage, liquidity and capacity evidence, model and operational controls, limits, monitoring, kill policy, and production-readiness evidence.

### 13.2 Gate authority

Only Risk Governance issues risk acceptance and capital ceilings. Workflow or executive priority cannot raise limits.

### 13.3 Gate outcomes

- `APPROVED` advances within explicit risk scope.
- `APPROVED WITH LIMITS` advances only with enforceable limits.
- `REQUIRES RISK MITIGATION` returns to the responsible owner and does not permit deployment.
- `REJECTED` blocks deployment of the reviewed use.

### 13.4 Continuous validity

Expiry, breach, scope change, validation change, control failure, or new risk evidence suspends or reopens the gate.

### 13.5 No risk-free assumption

Absence of observed loss or historical risk does not satisfy risk review. Residual uncertainty and owner acceptance remain explicit.

## 14. Executive Decision Gates

### 14.1 Entry requirements

The Executive Decision gate requires aligned current versions, completed required stages, admissible evidence, validation verdict, risk verdict, production-readiness state, alternatives, conditions, owners, monitoring, rollback, and acknowledgements.

### 14.2 Gate authority

Only the Executive Decision Agent issues institutional deployment authorization. It cannot create missing validation, risk, engineering, or evidence authority.

### 14.3 Outcomes

- `APPROVED FOR DEPLOYMENT` advances to deployment candidate handoff.
- `APPROVED WITH CONDITIONS` advances only within conditions.
- `RETURN TO RESEARCH` routes to authorized research work.
- `RETURN TO ENGINEERING` routes to implementation or readiness work.
- `RETURN TO VALIDATION` reopens independent validation.
- `RETURN TO RISK REVIEW` reopens risk governance.
- `REJECTED` closes advancement for the reviewed version.

### 14.4 No silent override

Executive authority cannot ignore unresolved validation or risk blocks, widen scientific or risk scope, or convert mitigation requests into approval.

### 14.5 Deployment boundary

Executive approval authorizes but does not execute deployment. The deployment owner separately acknowledges conditions and readiness.

## 15. Error, Exception, and Escalation Handling

### 15.1 Error response paths

Every error chooses one governed response: **Retry**, **Return**, **Escalate**, **Cancel**, **Suspend**, or **Archive**. The response identifies authority, conditions, attempts, and effect on evidence and history.

### 15.2 Required error classes

| Error | Required institutional response |
|---|---|
| Invalid workflow | Reject registration or suspend; correct identity, type, scope, and contract before retry |
| Missing owner | Block and escalate ownership assignment; no execution permitted |
| Invalid agent assignment | Return to routing; preserve attempted assignment and reason |
| Missing evidence | Return to evidence-producing stage or cancel if unobtainable |
| Stale evidence | Suspend gate; acquire, amend, or revalidate before retry |
| Conflicting memory state | Lock affected state, create conflict, reconcile through SMI, then resume or cancel |
| Blocked dependency | Enter Blocked; resolve, substitute only with approval, escalate, or cancel |
| Failed task | Preserve outputs and failure evidence; retry by policy, return, escalate, or cancel |
| Rejected output | Return with failed criteria, reject workflow, or archive final rejection |
| Timeout | Report status; retry, reassign, escalate, suspend, or cancel under declared policy |
| Unauthorized stage transition | Revert or suspend, quarantine downstream effects, and audit authority breach |
| Scope violation | Stop affected work, return to authorized stage, assess evidence and decisions |
| Validation failure | Return for new evidence or reject; never proceed to risk as approved |
| Risk breach | Suspend or activate containment; escalate to Risk Governance and affected authorities |
| Executive rejection | Stop advancement, preserve rationale, archive or begin a separately authorized new workflow |
| Emergency suspension | Enter safe state, preserve evidence, notify authorities, and initiate review |

### 15.3 Retry

Retry uses a new attempt identity, preserves prior failure, and cannot continue until a preferred result appears. Changed inputs or semantics may require a new workflow version.

### 15.4 Return

Return identifies destination stage, owner, failed criteria, required evidence or correction, valid retained outputs, and resubmission gate.

### 15.5 Exception

Exceptions are narrow, authorized, time-bounded, monitored, auditable, and unable to waive immutable stage gates or evidence truthfulness.

### 15.6 Escalation

Escalation follows constitutional authority and includes issue, evidence, versions, prior attempts, urgency, alternatives, consequences, interim controls, and decision requested.

## 16. Cancellation, Suspension, and Resumption

### 16.1 Cancellation authority

Cancellation authority is declared at registration and may include owner, sponsor, domain reviewer, Risk Governance, Executive Decision, or emergency authority within scope.

### 16.2 Cancellation record

Records reason, authority, state, active tasks, resource use, partial outputs, evidence, dependencies, consumers, downstream actions, retention, and reconsideration conditions.

### 16.3 Suspension

Suspension pauses progression while preserving identity, locks, evidence, memory, assignments, and safe-state obligations. It states trigger, owner, permitted actions, review, and expiry.

### 16.4 Emergency suspension

Emergency suspension prioritizes containment and notification. It cannot erase history or create approval to resume.

### 16.5 Resumption

Resumption requires resolved cause, reconciled SMI state, valid dependencies, current evidence and approvals, agent reacceptance, lock review, and an authorized MACP lifecycle event.

### 16.6 Restart versus resume

If continuity, comparability, evidence freeze, or state integrity cannot be demonstrated, work restarts under a new attempt or workflow version rather than resuming.

### 16.7 Cancellation is not failure concealment

Cancelled unfavorable or failed work remains in evidence, audit, failure review, and knowledge-gap systems.

## 17. Auditability and Reconstruction

### 17.1 Audit objective

Authorized reviewers can reconstruct workflow intent, ownership, routing, tasks, state, dependencies, evidence, memory, gates, decisions, errors, exceptions, and outcomes at any material point.

### 17.2 Mandatory audit events

Creation, registration, routing, acceptance, execution, status, blocking, review, return, approval, rejection, cancellation, archival, reassignment, version change, evidence freeze, memory lock, gate decision, exception, escalation, suspension, resumption, and downstream handoff are recorded.

### 17.3 Reconstruction set

The archive preserves Workflow Object versions, MACP messages, SMI snapshots and lineage, EES packages and custody, knowledge references, task outputs, validation and risk verdicts, executive decisions, acknowledgements, conflicts, errors, resource state, and retrospective.

### 17.4 Immutable history

Audit events are append-only in institutional meaning. Correction creates a new event and does not erase the original.

### 17.5 Outcome reconstruction

Review must distinguish decision quality from outcome luck and identify what evidence, limits, uncertainty, and alternatives were available ex ante.

### 17.6 Audit failure

If a material workflow cannot be reconstructed, affected outputs and approvals are integrity risks and may be suspended, invalidated, or returned for independent review.

## 18. Integration with MACP

### 18.1 Relationship

MACP governs every workflow instruction, task exchange, acknowledgement, status, evidence transfer, decision, error, escalation, conflict, exception, and lifecycle event. WOE defines when and why those messages are required.

### 18.2 Source-message requirement

Every Workflow Object creation and transition cites the exact MACP message. No chat statement or artifact existence changes state without a valid message.

### 18.3 Message-state alignment

Task acceptance, execution, completion, rejection, cancellation, and archival states must align between MACP and WOE. Inconsistency creates a blocking error.

### 18.4 Required messages

Initiation uses Request; routing uses Task Contract or Delegation; acceptance uses Acknowledgement; progress uses Status; evidence uses Evidence Transfer; gates use Decision, Validation, or Risk messages; failures use Error; conflicts use Conflict Report; transitions use Lifecycle Event; unresolved authority uses Escalation.

### 18.5 Idempotency

Duplicate messages cannot duplicate workflows, tasks, approvals, transitions, cancellations, or downstream actions.

## 19. Integration with SMI

### 19.1 Relationship

SMI holds authoritative workflow state; WOE governs its lifecycle and gate semantics. MACP messages authorize state change, and SMI preserves the result.

### 19.2 Required objects

Each workflow uses Workflow, Task, Agent Context, Evidence Reference, Knowledge Reference, Decision, Validation, Risk, Lock, Conflict, Error, Exception, and Audit objects as applicable.

### 19.3 State consistency

WOE stage and lifecycle state must reconcile with SMI versions, owners, locks, dependencies, expiry, and acknowledgements before progression.

### 19.4 Controlled writes

Only field owners write their authoritative state. Workflow owners cannot rewrite domain evidence or decisions.

### 19.5 Impact propagation

Memory supersession, expiry, conflict, invalidation, access change, or retirement triggers workflow dependency analysis and governed response.

### 19.6 Hidden-state prohibition

No workflow gate may depend on private model context or state not represented in authorized SMI objects.

## 20. Integration with EES

### 20.1 Relationship

EES governs every evidence object and package; WOE governs when evidence must be produced, transferred, frozen, reviewed, challenged, and consumed by a gate.

### 20.2 Evidence plan

Every evidence-producing workflow identifies expected types, claims, scope, producer, process, quality, admissibility, custody, freeze, reviewer, and consumers.

### 20.3 Gate consumption

Validation, risk, and executive stages cite exact admissible package versions. Limitations and contradictions remain visible.

### 20.4 Evidence change

Amendment, invalidation, contradiction, custody break, expiry, or scope change triggers impact review and may return, suspend, or revoke the workflow state.

### 20.5 Failure evidence

WOE ensures rejected tasks, failed experiments, negative controls, reproduction failures, breaches, cancellations, and incidents create or link appropriate EES evidence.

### 20.6 No evidence laundering

Repackaging, summarizing, routing, or executive citation cannot improve evidence quality, confidence, admissibility, or scope beyond EES authority.

## 21. Governance

### 21.1 Constitutional scope

WOE is mandatory for every institutional workflow, agent, authorized human participant, external gateway, and future model. Specialized workflows may add controls but cannot weaken this standard.

### 21.2 Governance ownership

- Workflow Governance controls types, lifecycle, stage semantics, routing, and conformance.
- Agent Contract Governance controls responsibility and authority.
- MACP Governance controls communication.
- SMI Governance controls shared state, ownership, locking, and consistency.
- EES Governance controls evidence.
- Knowledge Governance controls knowledge state.
- Validation and Risk Governance control their respective gates.
- Executive Decision controls final institutional decisions within authority.
- QA independently audits workflows and remediation.
- Founder authority approves constitutional change and reserved exceptions.

### 21.3 Workflow conformance

Every workflow type defines stages, owners, agent contracts, input and output objects, dependencies, evidence, memory, gate rules, errors, escalation, cancellation, archival, and audit requirements before active use.

### 21.4 Violations

Violations include unregistered work, missing owner, hidden state, invalid assignment, stage skipping, self-validation, evidence-free review, risk-free deployment, unauthorized transition, scope breach, suppressed failure, unaudited exception, or erased cancellation history.

Material violation triggers containment, state lock, affected-output and decision tracing, notification, rollback or suspension, independent investigation, remediation, and institutional learning.

### 21.5 Exceptions

Every exception defines rule, evidence, purpose, scope, agents, stages, risk, information loss, controls, owner, authority, duration, expiry, monitoring, audit, and return to conformance. Immutable stage-gate responsibilities cannot be waived.

### 21.6 Standard evolution

Every amendment defines problem, evidence, semantic change, alternatives, affected workflows and agents, compatibility, migration, historical reconstruction, MACP/SMI/EES impact, security, audit, effective date, deprecation, rollback, and approving authorities.

### 21.7 Periodic review

Governance asks:

- Does every workflow have identity, owner, scope, and valid source message?
- Are agents assigned within contracts and independence requirements?
- Are dependencies and blocks explicit and current?
- Do evidence, memory, validation, risk, and executive gates use aligned versions?
- Are failures, rejections, returns, and cancellations preserved?
- Can each workflow be reconstructed without chat history?
- Are conditions, exceptions, and escalations enforceable and expiring?
- Are deployment and monitoring respecting governance?
- Are feedback loops contaminating prior evidence or becoming hidden optimization?

### 21.8 Archival and retirement

Archival requires completed state reconciliation, consumer acknowledgement, evidence and memory retention, decision preservation, unresolved-issue recording, and reproducibility. Workflow-type retirement requires migration and continued historical interpretation.

### 21.9 Permanent rules

- No work exists without Workflow ID and owner.
- No authoritative state exists outside MACP and SMI.
- No agent acts outside its contract.
- No stage is skipped.
- No validation occurs without frozen admissible evidence.
- No deployment proceeds without current risk and executive approval.
- No decision lacks traceable inputs and alternatives.
- No transition, error, exception, or escalation is unaudited.
- No failure, rejection, cancellation, or contradiction is erased.
- Every workflow remains explainable, versioned, reconstructable, and institutionally accountable.

WOE governs the movement of institutional work. It coordinates authorities without replacing them and converts explicit, evidence-bearing state into controlled downstream action.
