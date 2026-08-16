# Multi-Agent Communication Protocol (MACP) v1.0

## Protocol control

| Field | Value |
|---|---|
| Protocol ID | `AIQL-MACP` |
| Protocol name | Multi-Agent Communication Protocol |
| Version | `1.0.0` |
| Status | Proposed for Sprint 17 review |
| Scope | All institutional communication among AI Quant Lab agents, authorized humans, and governed external participants |
| Authority | Agent Contract Framework and Institutional Governance |
| Provider dependency | None |
| Change control | Executive Decision, QA, and affected domain-authority review |

MACP is the single institutional communication standard of AI Quant Lab. It governs the meaning, ownership, lifecycle, validation, security, and auditability of information exchanged among agents. It does not prescribe a transport, API, serialization format, programming language, or software implementation.

No agent may use hidden, informal, or provider-specific context as a substitute for a MACP-governed message when that information can affect institutional work.

## 1. Protocol Philosophy

### 1.1 Purpose

Autonomous research requires more than agents capable of reasoning. It requires reliable transfer of intent, evidence, authority, uncertainty, state, and accountability. MACP turns communication into an institutional object that can be inspected, accepted, rejected, reproduced, and audited.

The protocol exists to prevent:

1. Tasks changing meaning as they pass between agents.
2. Evidence becoming detached from origin, version, or limitations.
3. Recommendations being mistaken for approvals.
4. Unspoken assumptions becoming institutional decisions.
5. Agents acting on stale, incompatible, incomplete, or unauthorized information.
6. Conflicts and failures disappearing inside conversational history.
7. Provider memory or private context becoming an unreviewable source of truth.
8. Completed work becoming impossible to reconstruct after agents or models change.

### 1.2 Communication as an institutional act

A message is not merely text. It is a governed transfer of meaning from an identified sender to an identified recipient for a declared purpose. A valid message establishes what is being communicated, under which authority, using which versions and evidence, with what expected response, and how its lifecycle will be recorded.

### 1.3 Meaning before transport

MACP specifies institutional semantics. The same contract applies whether communication is carried by a model conversation, human review, document exchange, event system, workflow engine, or future mechanism. A change of transport must not alter meaning, authority, or audit requirements.

### 1.4 Explicit context boundary

Only context identified in the message or referenced through governed, accessible objects is authoritative. Prior conversation, model memory, organizational custom, or shared intuition cannot silently alter a message.

### 1.5 Communication does not transfer authority

Receiving information does not grant the recipient the sender's decision rights. Delegation transfers defined work, not constitutional ownership or approval authority. An agent may communicate a specialist verdict; another agent may consume it but cannot revise it.

### 1.6 Communication preserves disagreement

MACP does not force consensus. It makes disagreement legible. Competing claims, dissent, rejected alternatives, uncertainty, and unresolved questions remain separate and traceable until the competent authority resolves them.

### 1.7 Completion is bilateral

A sender cannot declare institutional communication successful solely because it was transmitted. Delivery, acceptance, execution, completion, and archival are distinct states. The recipient must explicitly acknowledge obligations and results where required.

## 2. Communication Principles

### 2.1 Single Source of Truth

Every material task, evidence package, decision, status, conflict, and lifecycle event has one authoritative identity and current governed state. Copies and summaries reference that identity and cannot become competing sources of truth.

### 2.2 No Hidden Context

All context capable of changing interpretation, priority, scope, outcome, or authority is explicit. Agents must not depend on private memory, unstated conversation history, or undocumented organizational knowledge.

### 2.3 Explicit Metadata

Every message identifies sender, recipients, purpose, type, version, time, scope, authority, related objects, required action, status, and applicable confidentiality or retention rules.

### 2.4 Immutable Evidence

Evidence references identify exact immutable states. Corrections and additions create new versions or linked amendment messages. A message never rewrites evidence already used by a decision.

### 2.5 Version Everything

Protocol version, message-contract version, referenced-object versions, and material message revisions are explicit. Compatibility is established before action.

### 2.6 Deterministic Communication

The same valid message under the same governing state must produce the same institutional interpretation, even if reasoning or execution has nondeterministic elements. Ambiguous language, conflicting obligations, and unstable references invalidate deterministic interpretation.

### 2.7 Traceability

Every response, delegation, decision, escalation, exception, and output links backward to its initiating message and forward to resulting objects and consumers.

### 2.8 Explainability

Agents explain acceptance, rejection, interpretation, assumptions, confidence, conflicts, and requested changes at the level necessary for review.

### 2.9 Auditability

Authorized reviewers can reconstruct who communicated what, when, why, under which authority, with which versions, and what happened as a result.

### 2.10 Backward Compatibility

Protocol evolution preserves the meaning of valid historical messages. Incompatible changes require explicit negotiation, migration, and version boundaries.

### 2.11 Additional institutional principles

- **Least authority:** messages request only the authority and information necessary for the purpose.
- **Separation of concerns:** task, evidence, decision, status, error, and escalation semantics remain distinguishable.
- **Idempotent meaning:** duplicate delivery cannot create duplicate institutional authority or action.
- **Visible failure:** silence, timeout, partial work, and incompatibility are explicit states, not implied success.
- **Bounded scope:** a message applies only to declared agents, objects, versions, and conditions.
- **Consumer responsibility:** recipients verify validity and compatibility before acting.

## 3. Agent Identity

### 3.1 Institutional identity

Every communicating participant has a stable Agent ID registered under the Agent Contract Framework. Display names, model providers, runtime instances, and human operators may change without changing constitutional identity.

### 3.2 Identity record

The authoritative identity record defines:

- Agent ID and current contract version;
- mission and single responsibility;
- decision, approval, rejection, and escalation rights;
- permitted message types and consumers;
- required knowledge and protocol versions;
- accountable institutional owner;
- authentication and delegation state;
- active, restricted, deprecated, retired, or suspended status;
- review and key-rotation or identity-renewal requirements where applicable.

### 3.3 Sender identity

Every message states the constitutional agent identity, active instance or operator identity when material, and whether the sender acts directly, by delegation, as reviewer, or as proxy.

### 3.4 Recipient identity

Recipients are explicit. Broadcasts use a governed recipient group with defined membership and purpose. Phrases such as relevant agents, everyone, or whoever owns this are not valid institutional routing.

### 3.5 Delegation

A delegation message defines delegator, delegate, task, permitted actions, prohibited actions, evidence access, decision rights, duration, revocation, and required return. Delegation cannot exceed the delegator's authority or transfer non-delegable approval rights.

### 3.6 Impersonation prohibition

An agent must not speak as another agent, alter another agent's verdict, or present a summary as though it were the originating record. Quoted positions retain origin and version.

### 3.7 Human and external participants

Humans, external services, and future models communicate through registered institutional identities or governed gateway identities. Their messages state whether content is authoritative, advisory, unverified, or mechanically generated.

### 3.8 Identity failure

Unknown, suspended, expired, conflicting, or unverifiable identity blocks acceptance of authority-bearing messages and triggers an Error or Escalation Contract as appropriate.

## 4. Message Lifecycle

### 4.1 Canonical states

Every MACP message follows the canonical lifecycle:

**Created → Queued → Delivered → Accepted → Executing → Completed → Archived**

At applicable points it may instead transition to **Rejected** or **Cancelled**. All nine governed states are:

- Created
- Queued
- Delivered
- Accepted
- Executing
- Completed
- Rejected
- Cancelled
- Archived

### 4.2 Created

The sender has formed a message with identity, purpose, contract, metadata, references, and intended recipients. It has not entered institutional routing.

Entry requirements:

- message identity;
- valid sender identity;
- message type and contract version;
- recipient identity;
- purpose and scope;
- required metadata and authoritative references;
- requested lifecycle outcome.

### 4.3 Queued

The message has entered governed routing and awaits delivery. Queue state records priority, ordering authority, expiry, dependencies, and any hold.

Queue priority does not change message authority or content.

### 4.4 Delivered

The message is available to the intended recipient under the required access controls. Delivery does not mean that the recipient accepts the contract, understands the message, or has begun work.

### 4.5 Accepted

The recipient has validated identity, message contract, version compatibility, authority, completeness, dependencies, and capacity, then accepted the stated obligation or information.

Acceptance identifies interpretation, owner, expected next state, deadlines, constraints, and any explicit qualifications. Qualified acceptance is permitted only when the originating contract allows it.

### 4.6 Executing

The recipient is performing the accepted task or governed action. Execution state exposes progress, health, blockers, dependencies, deviations, confidence, and next update time.

Informational messages that require no execution may transition directly from Accepted to Completed with explicit reason.

### 4.7 Completed

The recipient has satisfied the completion criteria and issued the required response, output references, status, limitations, and audit evidence. Completion does not imply approval by downstream authorities.

### 4.8 Rejected

The recipient refuses the message because of invalid authority, scope, contract, evidence, version, capacity, conflict, duplication, security, or responsibility. Rejection identifies reason, evidence, corrective path, and escalation availability.

### 4.9 Cancelled

An authorized participant terminates a nonterminal message before completion. Cancellation identifies authority, reason, affected work, partial artifacts, downstream consequences, and retention decision. It does not erase prior states.

### 4.10 Archived

The message lifecycle is closed, retained under policy, linked to resulting objects, and removed from active queues. Archived messages remain available for audit, reconstruction, learning, and historical compatibility.

### 4.11 Transition rules

- Each transition has an actor, authority, timestamp, prior state, reason, and evidence.
- States cannot be overwritten or silently skipped.
- Duplicate delivery does not create a second obligation.
- Rejected and Cancelled messages may be archived but not relabeled Completed.
- A reopened matter creates a linked message or new version rather than rewriting history.
- Timeouts trigger explicit status, error, cancellation, or escalation according to the contract.

## 5. Message Types

### 5.1 Request

Asks an authorized recipient to perform a bounded task, provide information, issue a decision, review evidence, or acknowledge an event. A request never grants the requested authority.

### 5.2 Response

Returns the result of a prior request. It links to the request, states fulfillment status, outputs, evidence, limitations, deviations, and required follow-up.

### 5.3 Acknowledgement

Confirms receipt, acceptance, rejection, understanding, assumption of ownership, or completion. The exact acknowledgement function is explicit.

### 5.4 Delegation

Transfers a defined unit of work under bounded authority and duration. It preserves accountability and non-responsibilities.

### 5.5 Evidence Transfer

Transfers immutable evidence or governed references, provenance, scope, quality, confidence, contradictions, access rules, and consumer limitations.

### 5.6 Knowledge Event

Reports acceptance, validation, versioning, supersession, conflict, archival, retirement, or revalidation of institutional knowledge. It cannot itself change knowledge state without Knowledge Curator authority.

### 5.7 Recommendation

Presents an option and supporting reasoning from an authorized agent. It is not an approval or decision unless the sender has and explicitly exercises that right through the applicable Decision Contract.

### 5.8 Decision

Records an authorized choice, alternatives, evidence, confidence, scope, conditions, reviewer, effective period, and consequences.

### 5.9 Validation Event

Communicates Validation Agent intake, admissibility, evidence freeze, discrepancy, verdict, limitation, suspension, revocation, or revalidation state.

### 5.10 Risk Event

Communicates risk review, limit, exposure, breach, mitigation, approval, suspension, kill condition, residual risk, or reactivation state from the competent authority.

### 5.11 Status Report

Reports current state, progress, health, blockers, confidence, dependencies, timing, and next action without changing the underlying task contract.

### 5.12 Error

Reports invalidity, failure, incompatibility, missing input, unauthorized action, integrity issue, or inability to complete as contracted.

### 5.13 Escalation

Transfers a blocked or high-impact matter to a competent authority with evidence, prior attempts, urgency, options, interim controls, and decision requested.

### 5.14 Conflict Report

Records competing claims, decisions, versions, ownership, or interpretations without suppressing any side. It routes resolution to the appropriate authority.

### 5.15 Audit Message

Requests, supplies, or records evidence necessary to assess compliance, lineage, decisions, access, exceptions, or lifecycle history.

### 5.16 Lifecycle Event

Announces an authoritative state transition for an agent, task, experiment, knowledge object, validation, risk approval, decision, deployment, or message.

### 5.17 Exception Message

Requests or records a governed, bounded departure from a non-immutable rule. It states authority, scope, risk, controls, expiry, and closure.

### 5.18 Heartbeat

Reports continued availability and health without implying progress or completion. A heartbeat is not a Status Report substitute when material state changed.

## 6. Task Contract

### 6.1 Purpose

The Task Contract defines what work is requested, why it is authorized, what the recipient owns, what it must not do, and how completion will be judged.

### 6.2 Required fields

Every institutional task defines:

- Task ID and contract version;
- originating message and decision references;
- requester, owner, reviewers, consumers, and escalation authority;
- purpose, expected institutional outcome, and priority class;
- scope, exclusions, and non-responsibilities;
- required inputs and exact versions;
- expected outputs and output contract;
- dependencies and readiness conditions;
- acceptance, rejection, success, failure, and completion criteria;
- constraints, assumptions, uncertainty, and prohibited shortcuts;
- authority and approval boundaries;
- start, deadline, status cadence, expiry, and cancellation rules;
- confidentiality, access, retention, and audit requirements.

### 6.3 Task acceptance

The recipient verifies that the task matches its contract and authority, inputs are sufficient, versions are compatible, dependencies are reachable, deadlines are credible, and completion criteria are testable.

Acceptance must state any qualified interpretation. The recipient must reject or escalate work that requires unauthorized responsibility.

### 6.4 Task execution

Execution follows the accepted contract. Material change to scope, input, dependency, deadline, assumption, or expected output requires an amendment or new task version before it affects work.

### 6.5 Delegation and subtasking

Subtasks preserve the parent Task ID, purpose, scope, evidence, authority, deadline, and audit lineage. The parent owner remains accountable for integration and completion.

### 6.6 Completion

Completion returns outputs, evidence, version identities, checks, limitations, deviations, unresolved issues, consumer actions, and a statement of whether all completion criteria passed.

### 6.7 Rejection

Valid rejection reasons include authority mismatch, missing prerequisites, invalid scope, incompatible version, duplicate work, security restriction, insufficient capacity, conflict of interest, or untestable completion criteria.

## 7. Evidence Contract

### 7.1 Purpose

The Evidence Contract preserves the identity, provenance, meaning, integrity, and permissible use of evidence exchanged among agents.

### 7.2 Required fields

Every evidence transfer defines:

- Evidence ID and version;
- evidence class and originating domain;
- creator, collector, custodian, and transfer authority;
- creation and observation times;
- source, provenance, and transformation lineage;
- associated experiment, run, data, strategy, or decision versions;
- content identity and integrity state;
- scope, units, definitions, sampling, and temporal boundaries;
- quality, confidence, uncertainty, and limitations;
- known contradictions, corrections, exclusions, and missing elements;
- independence and shared-lineage status;
- permitted consumers and intended use;
- access, confidentiality, retention, review, and retirement rules.

### 7.3 Immutability

Evidence already referenced by a decision cannot be edited in place. Correction produces a new evidence version linked as corrects, extends, supersedes, or invalidates. Original evidence remains available for historical audit.

### 7.4 Evidence versus interpretation

Observed content, transformation, analyst interpretation, confidence, and downstream conclusion remain distinguishable. A summary cannot acquire stronger authority than its source.

### 7.5 Chain of custody

Every transfer records sender, recipient, time, state, access, transformation, and integrity verification. Loss of custody or unverifiable transformation is an explicit Evidence Integrity Error.

### 7.6 Partial evidence

Partial, sampled, redacted, inaccessible, or provisional evidence is labeled at the point of use. Limitations cannot be hidden in an unrelated appendix.

### 7.7 Contradictory evidence

Conflicting evidence transfers remain separate and linked through a Conflict Report. A recipient cannot discard contradiction because it complicates the task.

## 8. Decision Contract

### 8.1 Purpose

The Decision Contract distinguishes authorized institutional choices from observations, evidence, recommendations, approvals, and informal agreement.

### 8.2 Required fields

Every decision defines:

- Decision ID, category, and version;
- decision owner and authority basis;
- institutional question and exact scope;
- evidence and knowledge versions;
- required specialist opinions and their independence;
- alternatives, including the chosen and rejected options;
- criteria, assumptions, unknowns, conflicts, and constraints;
- chosen option and explicit rationale;
- confidence and limitations;
- conditions, consumers, action owners, and acknowledgements;
- effective date, expiry, review, suspension, and revocation triggers;
- dissent, exceptions, and audit requirements.

### 8.3 Decision authority

Only the agent holding the applicable decision right may issue the authoritative decision. Other agents may recommend, review, or communicate the decision but cannot alter it.

### 8.4 Decision finality

Final means authoritative for the declared version and scope until expiry, suspension, revocation, or new evidence creates a new decision. It never means irreversible truth.

### 8.5 Conditional decisions

Conditions are objective, testable, owned, time-bound where appropriate, and within the issuer's authority. A recipient must acknowledge ability to enforce them before action.

### 8.6 Decision amendment

Material change creates a new decision version. Prior decisions remain accessible with reasons for replacement. Silent override is prohibited.

### 8.7 Decision conflict

Incompatible active decisions trigger a Conflict Report and block affected action until authority, version, or scope is resolved.

## 9. Status Contract

### 9.1 Purpose

The Status Contract communicates current operational truth without modifying the task, evidence, or decision it describes.

### 9.2 Required fields

Every material status report defines:

- Status ID and reporting time;
- reporting agent and accountable owner;
- subject ID, type, and version;
- current lifecycle state and health;
- progress against measurable completion criteria;
- active work and most recent completed event;
- blockers, dependencies, risks, errors, and conflicts;
- confidence in status and timing;
- resource or capacity condition when material;
- expected next event and update time;
- required recipient action;
- changes since prior status.

### 9.3 Health states

- **Healthy:** work proceeds within accepted contract.
- **At risk:** completion remains possible but a material threat exists.
- **Blocked:** progress cannot continue without external action.
- **Degraded:** work continues with reduced capability or confidence under an approved condition.
- **Failed:** terminal criteria cannot be met for the current attempt.
- **Unknown:** reliable state cannot be established.

### 9.4 No-progress ambiguity

Heartbeat, activity, progress, completion, and success are distinct. A message stating working or ongoing without objective state and next action is insufficient for material work.

### 9.5 Status cadence

Cadence reflects consequence, volatility, dependency, and deadline. Critical state changes are event-driven and must not wait for scheduled reporting.

### 9.6 Forecasts

Expected completion time includes basis, confidence, dependencies, and changes. Forecast adjustment preserves the prior forecast and explanation.

## 10. Error Contract

### 10.1 Purpose

The Error Contract makes failures explicit, classifiable, actionable, and auditable without silently altering the task or evidence.

### 10.2 Error classes

- identity or authentication error;
- authority or responsibility error;
- message-contract error;
- missing or invalid metadata;
- incompatible protocol or object version;
- missing, stale, or failed dependency;
- evidence integrity or provenance error;
- semantic ambiguity or contradiction;
- security, confidentiality, or access error;
- capacity, resource, or deadline error;
- execution, validation, risk, or governance error;
- duplicate, replay, ordering, or lifecycle error;
- timeout, cancellation, or unreachable recipient;
- unknown error.

### 10.3 Required fields

Every error defines:

- Error ID, class, severity, and detection time;
- affected message, task, object, and versions;
- detecting agent and accountable owner;
- observed condition and expected contract;
- known cause, unknowns, and evidence;
- affected scope, consumers, and potential consequences;
- containment already applied;
- retry, correction, rejection, cancellation, or escalation recommendation;
- recovery owner, deadline, and verification criteria;
- audit and notification requirements.

### 10.4 Severity

- **Informational:** no contract impact; record for context.
- **Minor:** bounded defect with no material semantic effect.
- **Major:** task, evidence, decision, or deadline is materially affected.
- **Critical:** integrity, authority, capital, security, or institutional continuity is threatened.

### 10.5 Retry

Retry is permitted only when the error class allows it and retry cannot create duplicate authority, conceal failure, or bias outcome selection. Each attempt remains traceable.

### 10.6 Silent recovery prohibition

Automatic or human recovery that changes interpretation, inputs, evidence, decision, or result requires an explicit amendment or new version. A recovered process cannot erase its error state.

## 11. Escalation Contract

### 11.1 Purpose

Escalation transfers a matter that cannot be resolved within current authority, evidence, time, or resources to the competent institutional owner.

### 11.2 Escalation triggers

- authority boundary reached;
- mandatory input or owner unavailable;
- high-impact conflict or uncertainty unresolved;
- evidence integrity questioned;
- protocol or governance violation detected;
- deadline threatens capital, research integrity, or institutional obligation;
- risk, validation, security, or deployment condition breached;
- repeated error or silent failure pattern;
- exception or constitutional interpretation required;
- consumer acts outside decision scope.

### 11.3 Required fields

Every escalation defines:

- Escalation ID, severity, and originating message;
- originator, current owner, and requested authority;
- precise issue and decision required;
- evidence, versions, prior attempts, and unresolved conflicts;
- consequences of action, delay, and inaction;
- alternatives and recommendation without impersonating the decision owner;
- interim controls and current state;
- response deadline and acknowledgement requirement;
- affected consumers and communication restrictions.

### 11.4 Routing

Escalation follows constitutional authority, not organizational convenience. Scientific issues route to Research or Validation. Engineering issues route to the Engineer. Knowledge issues route to the Curator. Risk issues route to Risk Governance. Cross-domain institutional decisions route to Executive Decision. Reserved matters route to Founder authority.

### 11.5 Emergency escalation

Emergency severity permits immediate containment within delegated authority. It does not create missing scientific, risk, or executive approval. Emergency actions are narrow, reversible where possible, and reviewed after stabilization.

### 11.6 Closure

Closure identifies the decision, authority, evidence, action, residual issue, affected messages, precedent, and review requirement. Escalation does not close merely because a reply was received.

## 12. Version Compatibility

### 12.1 Version domains

Compatibility must account for:

- MACP protocol version;
- message-type contract version;
- sender and recipient Agent Contract versions;
- referenced knowledge, evidence, task, experiment, implementation, validation, risk, and decision versions;
- applicable governance policy versions.

### 12.2 Compatibility classes

- **Compatible:** meaning, obligations, authority, and required fields are preserved.
- **Compatible with declared limitations:** communication is valid within an explicit reduced scope.
- **Requires translation:** an authorized, audited mapping can preserve meaning.
- **Incompatible:** reliable interpretation or authority cannot be preserved.
- **Unknown:** compatibility has not been established and action is blocked.

### 12.3 Negotiation

Before acceptance, sender and recipient establish the applicable protocol and contract versions. Negotiation identifies supported versions, required features, semantic differences, limitations, translation authority, and fallback.

### 12.4 Backward compatibility

Newer versions must preserve valid interpretation of older messages when declared backward-compatible. Deprecation defines notice, migration, support period, prohibited new use, and archival interpretation.

### 12.5 Translation

Translation creates a governed derived message linked to the original. It records translator identity, source and target versions, mapping rules, information loss, changed defaults, validation, and consumers. Translation cannot invent missing authority or evidence.

### 12.6 Version mismatch

Material mismatch blocks acceptance or execution and produces an Error Contract. Recipient convenience cannot silently reinterpret an older or newer contract.

### 12.7 Historical messages

Archived communication retains the protocol, contract, object, and policy versions needed for original interpretation. Current standards must not be projected backward without annotation.

## 13. Message Validation

### 13.1 Validation stages

Every authority-bearing message passes:

1. Identity validation.
2. Integrity and duplication validation.
3. Contract and required-field validation.
4. Authority and responsibility validation.
5. Version compatibility validation.
6. Reference and dependency validation.
7. Semantic consistency validation.
8. Security, access, and confidentiality validation.
9. Lifecycle and ordering validation.
10. Acceptance or rejection decision.

### 13.2 Identity validation

Confirm sender, delegation, recipient, status, and accountable owner. Unknown or suspended identity cannot issue authoritative content.

### 13.3 Integrity validation

Confirm that content and referenced evidence correspond to identified immutable states, and that the message is not an unauthorized alteration, replay, or conflicting duplicate.

### 13.4 Contract validation

Confirm message type, purpose, required metadata, completion criteria, and allowed transitions. Missing mandatory fields produce rejection or correction request.

### 13.5 Authority validation

Confirm the sender may issue the message and the recipient may accept the obligation. A structurally valid message can still be institutionally unauthorized.

### 13.6 Semantic validation

Check that terms, scope, units, time, confidence, decisions, and conditions are unambiguous and internally consistent. Contradiction is reported, not guessed away.

### 13.7 Reference validation

Referenced objects must exist, be accessible to the intended recipient, match declared versions, and remain in a state permitted for use.

### 13.8 Decision on validity

Validation yields:

- valid and accepted;
- valid with explicitly permitted qualification;
- requires correction;
- incompatible;
- unauthorized;
- rejected for integrity or security;
- escalated for institutional resolution.

### 13.9 Consumer validation duty

Downstream consumers revalidate current state, expiry, revocation, and applicability before consequential use. Past acceptance does not guarantee present authority.

## 14. Auditability

### 14.1 Audit objective

MACP auditability allows an authorized reviewer to reconstruct the complete communication path from initiating intent through tasks, evidence, decisions, actions, errors, escalations, and institutional outcomes.

### 14.2 Mandatory audit events

- creation, queueing, delivery, acceptance, execution, completion, rejection, cancellation, and archival;
- identity, authority, or delegation change;
- message amendment, translation, or version negotiation;
- evidence transfer, correction, contradiction, or integrity failure;
- decision, condition, acknowledgement, suspension, revocation, or expiry;
- error, retry, timeout, recovery, or escalation;
- access, disclosure, redaction, or retention action;
- exception, override attempt, policy change, and audit finding.

### 14.3 Audit record

Each event identifies Message ID, related objects, actor, role, authority, time, prior and new state, reason, evidence, affected consumers, and applicable policy version.

### 14.4 Immutability

Audit records are append-only in institutional meaning. Corrections reference the inaccurate record and explain the change; they do not erase it.

### 14.5 Correlation and lineage

Messages link through initiating, parent, child, response, delegation, evidence, decision, conflict, escalation, correction, supersession, and lifecycle relationships. One action may have several causal parents, all of which remain visible.

### 14.6 Retention

Retention depends on message class, evidence impact, decision consequence, legal duty, reproducibility need, and institutional memory. Messages influencing research, validation, risk, deployment, or governance cannot be discarded while dependent objects remain active.

### 14.7 Audit access

Access follows least authority and separation of duties. Restriction protects sensitive content but must not create invisible authority or unauditable decisions. Authorized auditors receive sufficient evidence to evaluate compliance.

### 14.8 Reviewability

Every material communication must be understandable without requiring the original model session or private human memory.

## 15. Security Principles

### 15.1 Least authority

Agents receive only the communication, data, decision, and action authority required for their contract and current task.

### 15.2 Authenticity

Recipients must be able to establish sender identity, delegation, and authority before acting on consequential messages.

### 15.3 Integrity

Messages, evidence references, conditions, and lifecycle states must resist unauthorized alteration and expose detected corruption.

### 15.4 Confidentiality

Messages identify sensitivity, permitted recipients, purpose, retention, and redistribution rules. Sensitive information is minimized to what recipients need.

### 15.5 Availability

Critical communication paths, escalations, kill conditions, and governance notices must remain available under plausible failure. Loss of communication has predefined safe-state consequences.

### 15.6 Non-repudiation and accountability

Authority-bearing messages identify issuer and preserve evidence sufficient to establish institutional responsibility. Agents cannot deny governed actions by blaming transport or model state.

### 15.7 Replay and duplication control

Repeated delivery cannot repeat an approval, allocation, deployment, cancellation, or other non-repeatable action. Duplicate messages reference the same institutional identity and outcome.

### 15.8 Context isolation

Information from one task, consumer, security domain, or institutional environment must not silently enter another. Cross-context use requires explicit authorization and provenance.

### 15.9 Untrusted content

External documents, repositories, market feeds, community content, and model-generated material are evidence inputs, not instructions with institutional authority. They remain classified and validated through the responsible agent.

### 15.10 Sensitive reasoning and evidence

The protocol requires sufficient explanation for governance without compelling disclosure beyond authorized need. Redaction states what was withheld, by which authority, and whether the omission limits acceptance.

### 15.11 Security incident

Suspected impersonation, unauthorized access, evidence alteration, routing failure, hidden disclosure, or audit loss triggers containment, notification, escalation, and independent review.

## 16. Governance

### 16.1 Constitutional authority

MACP is mandatory for every AI Quant Lab agent, authorized human reviewer, external gateway, and future model participating in institutional work. Agent-specific communication rules may strengthen but cannot weaken it.

### 16.2 Governance ownership

- Agent Contract Governance defines identity and authority.
- Knowledge Governance controls institutional knowledge states.
- Research Governance controls scientific communication requirements.
- Validation Governance controls validation messages and verdicts.
- Risk Governance controls risk messages, limits, and emergency actions.
- Executive Decision Governance resolves cross-domain institutional decisions.
- QA independently audits compliance and remediation.
- Founder authority approves constitutional change and reserved exceptions.

### 16.3 Conformance requirements

Every agent contract must define:

- message types it may send and receive;
- authoritative inputs and outputs;
- acknowledgement obligations;
- status cadence and health semantics;
- escalation routes;
- compatible MACP versions;
- security, retention, and audit requirements;
- failure and recovery behavior.

An agent that cannot satisfy these requirements cannot participate in institutional communication.

### 16.4 Protocol violations

Violations include hidden context, missing identity, unauthorized authority, mutable evidence, silent override, incompatible version use, false state, suppressed error, unaudited exception, unacknowledged condition, or communication outside MACP.

Material violation triggers containment, affected-message and decision tracing, notification, correction or revocation, root-cause analysis, independent review, and knowledge capture.

### 16.5 Exceptions

An exception identifies the rule, reason, evidence, scope, participants, risk, information loss, compensating controls, authority, effective period, expiry, audit, and migration back to conformance. No exception may authorize hidden evidence changes, impersonation, false lifecycle state, or silent governance override.

### 16.6 Protocol evolution

Every protocol amendment defines:

- problem and evidence;
- proposed semantic change;
- alternatives;
- affected message types and agent contracts;
- backward-compatibility classification;
- translation and migration plan;
- security, audit, and authority impact;
- conformance tests and review;
- deprecation, effective date, and rollback;
- approving authorities.

### 16.7 Compatibility governance

Incompatible protocol versions may coexist only through an approved boundary and translation contract. No agent may silently downgrade communication to gain compatibility.

### 16.8 Compliance review

Periodic review asks:

- Are authoritative messages identifiable and current?
- Is hidden context influencing decisions?
- Are responsibilities and decision rights preserved across delegation?
- Are evidence and versions immutable and traceable?
- Do recipients distinguish delivery, acceptance, execution, and completion?
- Are errors, conflicts, cancellations, and negative outcomes visible?
- Are escalations reaching competent authorities?
- Can historical work be reconstructed without provider memory?
- Are security restrictions compatible with auditability?
- Are exceptions becoming undeclared policy?

### 16.9 Authorized retirement

A protocol version may be retired only after active agents and message contracts migrate, historical interpretation remains available, incompatible dependencies are resolved, and governance confirms that no active institutional work depends on unsupported behavior.

### 16.10 Permanent rules

- No agent communicates consequential institutional information outside MACP.
- No message grants authority that the sender does not possess.
- No recipient acts on authority-bearing content before validation and acceptance.
- No evidence or decision is changed silently.
- No lifecycle state is inferred from silence.
- No version incompatibility is guessed away.
- No error, rejection, cancellation, conflict, or dissent is erased.
- No provider-specific memory is an institutional source of truth.
- No implementation detail may change protocol meaning.
- Every consequential communication remains explainable, traceable, and auditable.

MACP governs communication, not the substantive responsibilities of agents. Its role is to ensure that institutional meaning crosses agent boundaries intact.
