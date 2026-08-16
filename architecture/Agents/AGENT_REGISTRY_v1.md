# Agent Registry (AR) v1.0

## Specification control

| Field | Value |
|---|---|
| Registry ID | `AIQL-AR` |
| Registry name | Agent Registry |
| Version | `1.0.0` |
| Status | Proposed for Sprint 21 review |
| Scope | All institutional agents, authorized proxies, and future agent classes in AI Quant Lab |
| Authority | Agent Contract Framework, MACP, SMI, EES, WOE, and Institutional Governance |
| Provider dependency | None |
| Change control | Agent Governance, QA, Executive Decision, and Founder-reserved approval where applicable |

The Agent Registry is the constitutional governance layer that determines which agents institutionally exist, what identities and contracts bind them, what authority and permissions they possess, and which messages, memory objects, evidence, workflows, delegations, and lifecycle states are permitted. It is not a software registry, runtime service, database, API, schema, or implementation file.

No agent may perform institutional work unless it has a current valid Registry Record under this standard.

## 1. Agent Registry Philosophy

### 1.1 Institutional existence

An agent exists institutionally only when the Registry recognizes a stable identity, approved contract, accountable owner, explicit authority, permissions, restrictions, status, and audit history. Model availability or technical capability does not establish institutional existence.

### 1.2 Authority before capability

The Registry separates what an agent can technically do from what it may institutionally do. Capability supports assignment only after contract, status, independence, access, workflow, evidence, and decision-right checks pass.

### 1.3 Identity must survive providers

Agent identity is independent of GPT, Claude, Gemini, local models, human operators, versions, instances, and transports. A provider may implement an identity but cannot redefine its mission or authority.

### 1.4 Registration is bounded

Registration admits an agent to the institutional system under specified rights. It does not approve every task, workflow, message, memory access, evidence action, or decision.

### 1.5 Registry as source of authority

Agent Contracts define constitutional responsibilities. The Registry binds an approved contract version to an active identity and exposes its operationally valid rights and restrictions. A contract without registration cannot act; a registration without a valid contract cannot exist.

### 1.6 Status controls authority

Authority is conditional on current status. Restrictions, suspension, deprecation, retirement, expiry, conflict, or security state can narrow or remove otherwise valid rights.

### 1.7 History is institutional memory

Agent actions, permissions, contract changes, delegations, restrictions, incidents, deprecations, and retirement remain reconstructable. Replacing an agent does not erase its decisions or accountability.

### 1.8 Registry does not manage work

The Registry establishes eligibility and authority. WOE routes work, MACP communicates it, SMI preserves state, EES governs evidence, and domain agents perform their responsibilities.

## 2. Agent Registry Principles

### 2.1 No Agent Without Identity

Every institutional action resolves to a stable Agent ID and current Registry Record.

### 2.2 No Agent Without Contract

Every registered identity is bound to an approved, versioned Agent Contract defining mission, responsibility, non-responsibility, inputs, outputs, authority, and failure governance.

### 2.3 No Authority Without Registration

Unregistered models, tools, humans, or external services may provide untrusted input but cannot issue authority-bearing institutional outputs.

### 2.4 No Hidden Agent Role

Every role performed in a workflow is declared in the Registry and task assignment. An agent cannot silently act as researcher, engineer, validator, risk officer, or executive.

### 2.5 No Silent Permission Expansion

Permissions change only through governed Registry versions with evidence, impact analysis, approval, and notification.

### 2.6 Capability Is Not Authority

Technical ability, model confidence, access, or organizational rank cannot expand contract-defined rights.

### 2.7 Registration Is Not Approval for All Work

Every assignment separately verifies workflow eligibility, task scope, status, independence, dependencies, and capacity.

### 2.8 Agent Status Must Be Explicit

Current status, restrictions, effective time, expiry, and allowed actions are authoritative and visible to permitted consumers.

### 2.9 Delegation Must Be Bounded

Delegation identifies work, authority, fields, messages, evidence, workflow, duration, revocation, and accountability. It cannot exceed the delegator's rights.

### 2.10 Suspension Must Be Auditable

Suspension records cause, evidence, authority, affected actions, interim controls, review, and reinstatement or retirement criteria.

### 2.11 Retirement Does Not Erase History

Retired agents cannot perform new work, but their historical outputs, decisions, evidence, delegations, and audit records remain attributable.

### 2.12 Every Agent Action Must Be Traceable

Every consequential action links Agent ID, contract and registry versions, MACP message, SMI state, EES evidence, WOE workflow, authority, and time.

### 2.13 Additional principles

- Least authority and separation of duties apply by default.
- One identity cannot hide several incompatible responsibilities.
- Restrictions override broad permissions.
- Invalid or expired registration blocks authority.
- Agent replacement requires explicit continuity and handoff.
- Registry state is immutable in history and versioned in change.

## 3. Agent Identity Model

### 3.1 Stable Agent ID

Agent ID is the permanent institutional identity. Names, implementations, models, instances, and operators may change, but history remains linked to the stable ID.

### 3.2 Identity layers

- **Constitutional identity:** mission, responsibility, authority, and contract.
- **Registry identity:** current status, permissions, restrictions, eligibility, and versions.
- **Implementation identity:** model, human, composite system, or future executor currently realizing the agent.
- **Instance identity:** bounded execution instance acting under the registered identity.
- **Operator identity:** responsible human or governance owner where applicable.

These layers remain distinguishable in audit records.

### 3.3 Identity uniqueness

No two Active agents may share an Agent ID. Similar names or duplicate capabilities require separate IDs and explicit relationships.

### 3.4 Agent types

An agent may be model-based, human-operated, hybrid, committee, or governed external authority. Type describes implementation form, not constitutional power.

### 3.5 Agent categories

The controlled categories are:

- Research Agent
- Knowledge Agent
- Architecture Agent
- Engineering Agent
- Experiment Agent
- Validation Agent
- Risk Agent
- Decision Agent
- Governance Agent
- Orchestration Agent
- Monitoring Agent
- Emergency Agent

An agent may have a primary category and limited secondary classifications, but one Single Responsibility governs.

### 3.6 Identity continuity

Replacement preserves Agent ID only when mission, responsibility, authority, and contract remain equivalent and governance approves the implementation transition. Material mandate change creates a new identity.

### 3.7 Identity conflict

Conflicting claims, impersonation, duplicate Active identities, or uncertain implementation binding trigger immediate restriction and audit.

## 4. Agent Registration Model

### 4.1 Registration prerequisites

Registration requires:

- proposed Agent ID, name, type, and category;
- approved Agent Contract and version;
- mission and Single Responsibility;
- owned and prohibited decisions;
- MACP, SMI, EES, and WOE rights;
- inputs, outputs, dependencies, consumers, and review gates;
- security and confidentiality classification;
- activation, restriction, suspension, deprecation, and retirement criteria;
- accountable governance owner and reviewers;
- capability and conformance evidence appropriate to intended authority.

### 4.2 Registration review

Review examines uniqueness, necessity, overlap, responsibility isolation, authority boundaries, independence, protocol compatibility, security, auditability, provider independence, and future retirement.

### 4.3 Registration outcomes

- Registered and eligible for activation.
- Registered with restrictions.
- Returned for contract or evidence correction.
- Rejected as duplicative, unsafe, ambiguous, or outside institutional mandate.
- Quarantined pending identity, security, or governance investigation.

### 4.4 Record activation

Registration creates the identity and record. Activation separately requires current contract, required dependencies, permissions, conformance, security, communication, memory, evidence, workflow, and oversight readiness.

### 4.5 Duplicate responsibility

New agents cannot absorb or duplicate existing Single Responsibility without an explicit architecture decision defining distinction, collaboration, conflict, and retirement implications.

### 4.6 Registration amendment

Material changes to mission, authority, permissions, evidence rights, workflow eligibility, security, or lifecycle create a new Registry Record version and may require contract amendment or a new Agent ID.

## 5. Agent Lifecycle

### 5.1 Canonical states

Every agent follows:

**Proposed → Registered → Active → Restricted → Suspended → Deprecated → Retired → Archived**

The path may vary under governance, but every transition remains explicit and audited.

### 5.2 Proposed

Identity and contract are candidates under review. The agent cannot perform institutional work.

### 5.3 Registered

The Agent Record is valid, but activation conditions have not all passed or activation has not been authorized. It may participate only in explicitly permitted conformance evaluation.

### 5.4 Active

The agent may act within current contract, registry permissions, workflow assignments, task scope, security, and independent review requirements.

### 5.5 Restricted

The agent remains active only within a narrowed set of messages, memory fields, evidence types, workflows, decisions, time, consumers, or supervision conditions.

### 5.6 Suspended

Authority-bearing output and new institutional work are prohibited. Only containment, handoff, audit, evidence preservation, and specifically authorized remediation actions are allowed.

### 5.7 Deprecated

The identity remains temporarily supported for existing obligations or migration but cannot receive new work unless an explicit exception permits it.

### 5.8 Retired

The agent cannot act, receive delegation, or re-enter workflows. History and ownership lineage remain preserved. Reactivation requires new governance and ordinarily a new identity.

### 5.9 Archived

The complete Agent Record, contracts, permissions, actions, outputs, incidents, and retirement evidence are retained for institutional memory and audit.

### 5.10 Transition rules

Every transition cites a MACP lifecycle message, SMI version, authority, evidence, time, affected workflows, outstanding tasks, access changes, consumers, handoff, and review conditions.

## 6. Agent Status Classes

### 6.1 Operational status

Operational status describes whether the agent is available, healthy, degraded, blocked, unavailable, or under review without replacing lifecycle state.

### 6.2 Authority status

Authority may be current, restricted, suspended, expired, revoked, or pending activation. Authority status controls whether outputs may carry institutional force.

### 6.3 Conformance status

Conformance may be passed, conditional, under review, failed, or unknown across Agent Contract, MACP, SMI, EES, WOE, security, and audit domains.

### 6.4 Independence status

For review roles, the record states independent, qualified independence, conflicted, recused, or not applicable.

### 6.5 Composite status

Consumers must evaluate lifecycle, operational, authority, conformance, and independence states together. A technically healthy Suspended agent has no authority.

### 6.6 Status expiry

Time, contract change, dependency failure, incident, conflict, audit finding, or missed review can automatically restrict authority pending governance.

## 7. Agent Contract Binding

### 7.1 Binding rule

Every Registry Record identifies one authoritative Agent Contract location and exact version. The Registry cannot broaden rights beyond the contract.

### 7.2 Contract precedence

Constitutional standards and Agent Contract control mission and responsibilities. Registry restrictions may narrow current rights for safety, security, compatibility, or governance but cannot silently alter mission.

### 7.3 Compatibility

Contract, registry, MACP, SMI, EES, and WOE versions must be compatible before activation and assignment.

### 7.4 Contract change

Material contract change triggers registry impact review, permission recalculation, workflow eligibility review, delegations, active tasks, consumers, security, and possible restriction or reactivation.

### 7.5 Contract conflict

If Registry and Agent Contract conflict, the narrower safe authority applies while Agent Governance resolves the inconsistency. No action proceeds on the more permissive interpretation.

### 7.6 Binding audit

Every agent action records the contract and registry versions active at the time.

## 8. Agent Authority and Permissions

### 8.1 Authority domains

Authority includes create, observe, research, design, implement, orchestrate, validate, accept knowledge, assess risk, approve, reject, escalate, authorize deployment, monitor, suspend, and retire. Each is granted separately.

### 8.2 Permission layers

Effective permission is the intersection of:

- Agent Contract rights;
- current Registry Record;
- lifecycle and authority status;
- WOE workflow and stage eligibility;
- MACP task assignment;
- SMI object and field access;
- EES evidence rights;
- security and confidentiality policy;
- delegation and expiry;
- active restrictions, locks, conflicts, and exceptions.

### 8.3 Decision rights

Owned Decisions, Decision Authority, Approval Authority, Rejection Authority, and Escalation Authority are explicit and scoped by object, workflow, stage, version, consumer, and condition.

### 8.4 Prohibition precedence

Explicit prohibitions override general capabilities and permissions. An agent cannot interpret silence as authority.

### 8.5 Permission change

Expansion requires evidence, contract compatibility, segregation analysis, security review, downstream impact, approval, versioning, and notification. Reduction may occur immediately for containment but requires audit and review.

### 8.6 No self-modification

An agent cannot change its own status, authority, permissions, contract binding, restrictions, or lifecycle state.

## 9. MACP Message Rights

### 9.1 Message-right model

For each MACP type, the Registry defines whether the agent may create, send, receive, acknowledge, delegate, approve, reject, escalate, or audit it, and in which workflows and roles.

### 9.2 Authority-bearing messages

Decision, Validation Event, Risk Event, lifecycle transition, exception, suspension, and deployment authorization require specific registered authority. Ability to format or transmit them is irrelevant.

### 9.3 Required rights

Every agent may receive governance notices necessary for its active obligations. Send rights remain bounded by contract and assignment.

### 9.4 Prohibited messages

Prohibited MACP Message Types are explicit. Attempts are rejected, audited, and escalated when consequential.

### 9.5 Delegated messaging

A proxy may transmit content on behalf of an authority only through an explicit delegation that preserves origin, decision owner, exact message, and non-editability of authority-bearing meaning.

### 9.6 Message validation

Recipients verify Registry status, sender rights, contract version, delegation, scope, and message type before accepting authority.

## 10. SMI Memory Access Rights

### 10.1 Object and field rights

The Registry identifies which SMI object types and fields an agent may discover, read, reference, propose, write, lock, transition, approve, or audit.

### 10.2 Owner-specific writes

Workflow owners update orchestration fields; evidence producers update permitted evidence metadata; Validation owns verdict fields; Risk Governance owns risk fields; Executive Decision owns executive decision fields; Knowledge Curator owns knowledge state.

### 10.3 Least privilege

Access is limited by task, workflow, purpose, exact versions, security class, duration, and consumer need.

### 10.4 Hidden-state prohibition

Registry permissions cannot authorize use of private model memory, personal memory, or chat history as shared institutional state.

### 10.5 Lock and conflict behavior

Lock rights and conflict-resolution rights are distinct. An agent may hold a lock without owning resolution authority.

### 10.6 Access incident

Unauthorized read, write, lock, or transition triggers containment, status review, affected-object tracing, and possible restriction or suspension.

## 11. EES Evidence Rights

### 11.1 Evidence actions

For each evidence type, the Registry specifies rights to create, submit, transfer, consume, reproduce, freeze, challenge, assess, validate, amend, invalidate, archive, or audit.

### 11.2 Production versus validation

Producing evidence does not grant validation authority. Validating evidence does not grant authority to rewrite it. Risk and executive consumers may assess use but not alter evidence content.

### 11.3 Evidence scope

Rights are limited to evidence classes and processes within Single Responsibility. Technical capability to analyze other evidence does not expand rights.

### 11.4 Chain of custody

Custody rights identify permissible handling, transfer, freeze, and access without implying content ownership.

### 11.5 Challenge right

Authorized consumers may challenge evidence within competence. Challenge does not grant amendment or invalidation authority.

### 11.6 Evidence violation

Unregistered evidence production, hidden mutation, out-of-scope validation, or broken custody may suspend evidence rights and dependent outputs.

## 12. WOE Workflow Eligibility

### 12.1 Eligibility dimensions

Workflow eligibility depends on agent category, contract, status, role, authority, independence, required inputs, memory and evidence rights, security, compatibility, capacity, and active restrictions.

### 12.2 Role-specific eligibility

The Registry distinguishes Workflow Owner, stage owner, task assignee, producer, reviewer, approver, auditor, escalation authority, and observer roles.

### 12.3 Stage eligibility

Eligibility is stage-specific. A Strategy Architect may own architecture but cannot enter engineering as implementer or validation as approver.

### 12.4 Assignment validation

WOE verifies current Registry Record before routing and again before consequential stage gates. Stale eligibility blocks acceptance.

### 12.5 Parallel roles

Parallel roles are allowed only when duties do not conflict and field ownership, evidence independence, and review segregation remain intact.

### 12.6 Emergency workflows

Emergency eligibility is narrow and predeclared. It permits containment but cannot create scientific, risk, or executive approval.

## 13. Delegation and Proxy Rules

### 13.1 Delegation record

Every delegation defines delegator, delegate, task, workflow, role, permitted actions, message types, memory fields, evidence types, decision rights, duration, security, review, revocation, and return obligations.

### 13.2 Delegation limits

An agent cannot delegate authority it does not possess, non-delegable constitutional rights, broader scope than assigned, or rights beyond its active status.

### 13.3 Accountability

The delegator remains accountable for delegated work unless a governing contract explicitly transfers ownership. The delegate remains accountable for acting within bounds.

### 13.4 Proxy communication

A proxy may relay but cannot edit authority-bearing meaning. Messages identify both proxy and originating authority.

### 13.5 Subdelegation

Subdelegation is prohibited unless explicitly authorized, bounded, and traceable through the full chain.

### 13.6 Expiry and revocation

Delegation expires automatically by time, task, status, workflow state, contract change, or revocation. Outstanding work and access are reconciled.

### 13.7 Delegation incident

Scope breach, impersonation, orphaned authority, or hidden subdelegation triggers containment, suspension, and audit.

## 14. Agent Restriction and Suspension

### 14.1 Restriction triggers

Restrictions may follow audit findings, partial conformance, dependency failure, security change, conflict, model migration, insufficient independence, repeated errors, or bounded remediation.

### 14.2 Restriction record

Defines restricted rights, allowed actions, reason, evidence, authority, affected workflows, consumers, controls, review, expiry, and restoration criteria.

### 14.3 Suspension triggers

Suspension is required for identity uncertainty, critical authority violation, evidence manipulation, hidden scope expansion, security incident, audit loss, repeated noncompliance, or inability to act safely.

### 14.4 Suspension effects

Suspended agents cannot issue authority-bearing outputs, accept new work, delegate, write institutional state, validate evidence, approve, reject, or alter workflows. Permitted containment and handoff are explicit.

### 14.5 Active-work handling

Suspension triggers task pause or reassignment, evidence and memory freeze, credential and access review, consumer notification, decision impact analysis, and continuity handoff.

### 14.6 Reinstatement

Requires root-cause resolution, remediation evidence, conformance review, security and independence checks, updated record, governance approval, and controlled reactivation.

### 14.7 No self-status change

An agent cannot restrict, suspend, reinstate, deprecate, or retire itself.

## 15. Deprecation and Retirement

### 15.1 Deprecation purpose

Deprecation announces that an agent is leaving active service while preserving controlled completion, migration, and historical interpretation.

### 15.2 Deprecation conditions

May include superseding architecture, contract incompatibility, obsolete capability, sustained quality failure, consolidation, security risk, or planned replacement.

### 15.3 Deprecated behavior

Deprecated agents cannot receive new institutional work unless an explicit exception defines necessity, scope, supervision, and expiry. Existing obligations follow a migration plan.

### 15.4 Retirement prerequisites

- active tasks and delegations resolved;
- decisions, evidence, memory, and workflows attributed;
- consumers and dependencies migrated;
- access and authority revoked;
- replacement and compatibility documented;
- incidents and audit findings closed or transferred;
- archival and reproducibility obligations satisfied.

### 15.5 Retirement record

States authority, reason, effective date, successor, migrated obligations, unresolved issues, prohibited use, access after retirement, and audit retention.

### 15.6 Reactivation prohibition

Retired agents cannot be reactivated by changing a status flag. New governance evaluates whether a new Agent ID and contract are required.

### 15.7 Archival

Archived records preserve all contract versions, statuses, permissions, actions, decisions, evidence, workflows, delegations, incidents, reviews, and retirement rationale.

## 16. Registry Auditability

### 16.1 Audit objective

Authorized reviewers can reconstruct which agents existed, what they were permitted to do, which status and contract applied, and how every consequential action was authorized.

### 16.2 Mandatory events

Proposal, registration, activation, restriction, suspension, reinstatement, deprecation, retirement, archive, contract binding, permission change, delegation, access, message right, workflow eligibility, evidence right, assignment, authority action, exception, violation, and audit finding are recorded.

### 16.3 Audit event fields

Each event identifies Agent ID, record and contract versions, actor, authority, time, prior and resulting state, reason, evidence, rights affected, workflows, consumers, source MACP message, SMI state, and review.

### 16.4 Action reconstruction

Every authority-bearing output resolves the Agent Record, status, contract, delegation, workflow role, message rights, memory and evidence rights, and decision authority active at issuance.

### 16.5 Immutable history

Audit history is append-only in institutional meaning. Corrections preserve inaccurate records and explain the change.

### 16.6 Independent audit

Agents cannot close material findings about their own identity, authority, permission, evidence, or audit violations. QA or competent governance verifies closure.

## 17. Registry Change Governance

### 17.1 Change classes

- metadata correction;
- implementation or operator update;
- contract-version binding;
- permission narrowing or expansion;
- message, memory, evidence, or workflow right change;
- lifecycle transition;
- delegation-policy change;
- security or classification change;
- breaking mission or authority change.

### 17.2 Change proposal

Every proposal defines problem, evidence, current and proposed state, alternatives, authority and segregation impact, affected workflows and consumers, security, compatibility, migration, audit, and rollback.

### 17.3 Approval

Permission expansion and authority change require independent governance and contract compatibility. Emergency narrowing may be immediate but is reviewed.

### 17.4 Impact propagation

Changes notify active workflows, MACP correspondents, SMI consumers, EES custodians, decision owners, delegations, security, and auditors.

### 17.5 No silent expansion

New model capability, successful performance, added access, or emergency history cannot silently expand the record.

### 17.6 Registry versioning

Every material change creates a new record version with effective time and historical compatibility.

## 18. Integration with MACP

### 18.1 Relationship

The Registry defines who may communicate and which MACP rights apply. MACP carries registration, lifecycle, assignment, delegation, status, error, escalation, decision, and audit messages.

### 18.2 Sender validation

Every authority-bearing message validates Agent ID, current status, contract, right to send the type, workflow role, delegation, and scope.

### 18.3 Recipient validation

Routing verifies the recipient may receive and act on the message. Delivery cannot grant missing authority.

### 18.4 Lifecycle events

Registration and status transitions generate MACP events to affected workflows, consumers, owners, and auditors.

### 18.5 Invalid message

Messages outside rights are rejected, preserved, and escalated based on consequence.

### 18.6 Communication history

Archived Agent Records retain message rights and the exact version used for historical interpretation.

## 19. Integration with SMI

### 19.1 Relationship

SMI holds authoritative Agent Registry state and access references. The Registry governs semantics, owners, permissions, lifecycle, and constitutional validity.

### 19.2 Registry Memory Object

Every Agent Record exists as a versioned SMI Registry State with owner, readers, writers, source message, status, conditions, expiry, and audit trail.

### 19.3 Access enforcement

SMI resolves Registry rights before read, write, lock, transition, or audit. Historical access does not imply current permission.

### 19.4 Controlled mutation

Agents cannot write their own Registry fields. Changes require governed owners, locks where applicable, exact versions, and MACP lineage.

### 19.5 Status propagation

Restriction, suspension, deprecation, and retirement update access, locks, active contexts, tasks, and consumer notifications.

### 19.6 Reconstruction

SMI preserves exact Registry versions associated with every consequential memory action.

## 20. Integration with EES

### 20.1 Relationship

The Registry defines which evidence types and actions an agent may perform. EES governs the resulting evidence objects, packages, custody, and admissibility.

### 20.2 Producer rights

Evidence creation requires registered type and process rights. Unregistered output remains untrusted input until governed.

### 20.3 Consumer rights

Access and consumption are distinct from validation, amendment, or invalidation authority.

### 20.4 Custody

The Registry defines custody eligibility and security classification. EES records each actual transfer and freeze.

### 20.5 Rights change

Restriction or suspension triggers impact analysis for evidence under creation, custody, review, and downstream use.

### 20.6 Historical attribution

Archived evidence retains the Agent Record and rights active when produced or reviewed.

## 21. Integration with WOE

### 21.1 Relationship

The Registry determines workflow and stage eligibility. WOE assigns and governs actual work.

### 21.2 Routing gate

Before routing, WOE validates current status, contract, category, role eligibility, rights, independence, dependencies, security, and capacity.

### 21.3 Acceptance gate

The assignee confirms the task remains within registered authority. Registry eligibility does not force acceptance.

### 21.4 Continuous eligibility

WOE rechecks status before critical stages and authority-bearing outputs. Status change may block, return, reassign, suspend, or cancel work.

### 21.5 Separation of duties

Registry roles enforce that research, implementation, validation, risk, executive approval, and deployment remain appropriately independent.

### 21.6 Emergency handling

Emergency workflows use predeclared Emergency Agent rights. Containment authority cannot create missing stage approvals.

## 22. Governance

### 22.1 Constitutional scope

Every current and future AI Quant Lab agent, authorized human authority, model, committee, proxy, and external gateway must be registered before institutional action.

### 22.2 Mandatory initial registered agents

The initial registry must contain the following records, each bound to its approved Agent Contract:

| Agent | Primary category | Single institutional responsibility | Core prohibited substitution |
|---|---|---|---|
| Quant Strategy Architect | Architecture Agent | Design falsifiable strategy architecture | Cannot implement, optimize, validate, approve risk, or deploy |
| Market Research Agent | Research Agent | Produce objective market intelligence | Cannot design or validate strategies |
| Research Librarian Agent | Knowledge Agent | Acquire and classify authoritative sources | Cannot conduct market research or create strategy logic |
| Knowledge Curator Agent | Knowledge Agent / Governance Agent | Govern institutional knowledge lifecycle | Cannot acquire sources or conduct research |
| Quant Strategy Engineer | Engineering Agent | Faithfully implement approved research | Cannot invent or change hypotheses, optimize, or validate |
| Experiment Orchestrator Agent | Experiment Agent / Orchestration Agent | Coordinate approved experiment operations | Cannot create hypotheses, implement, or validate results |
| Validation Agent | Validation Agent | Independently evaluate scientific evidence | Cannot create, implement, optimize, approve risk, or deploy |
| Risk Governance Agent | Risk Agent / Governance Agent | Accept or reject institutional deployment risk | Cannot validate science, implement, or execute deployment |
| Executive Decision Agent | Decision Agent / Governance Agent | Issue final institutional decisions within governance | Cannot create evidence, validate, assess risk, or override gates |

### 22.3 Initial rights baseline

Detailed rights remain in individual Registry Records. At minimum:

- the Quant Strategy Architect may produce architecture evidence and enter Strategy Architecture workflows;
- the Market Research Agent may produce Market Observation Evidence and enter Market Research workflows;
- the Research Librarian may produce Research Literature Evidence and enter Knowledge Acquisition workflows;
- the Knowledge Curator may govern Knowledge References and enter Knowledge Curation workflows;
- the Quant Strategy Engineer may produce Engineering Implementation Evidence and enter Strategy Engineering workflows;
- the Experiment Orchestrator may own experiment state and enter Experiment workflows;
- the Validation Agent may freeze and validate evidence and enter Validation workflows;
- Risk Governance may produce risk decisions and enter Risk Review workflows;
- Executive Decision may issue authorized executive decisions and enter Executive Decision workflows.

No baseline grants rights outside the bound Agent Contract.

### 22.4 Mandatory Agent Record schema

Every Registry Record defines all of the following:

| Field | Requirement |
|---|---|
| Agent ID | Stable institutional identity |
| Agent Name | Controlled human-readable name |
| Agent Type | Model, human, hybrid, committee, or governed external authority |
| Agent Category | Primary and permitted secondary categories |
| Current Status | Lifecycle, authority, operational, conformance, and independence state |
| Contract Location | Authoritative contract reference |
| Contract Version | Exact active contract version |
| Mission | Constitutional mission |
| Single Responsibility | One owned institutional purpose |
| Owned Decisions | Decisions the agent may issue |
| Prohibited Decisions | Decisions the agent must never issue |
| Allowed MACP Message Types | Types, actions, workflows, and scope |
| Prohibited MACP Message Types | Explicit prohibited authority-bearing communication |
| Allowed SMI Memory Objects | Object and field read/write/lock/transition rights |
| Allowed EES Evidence Types | Create, consume, freeze, challenge, validate, or custody rights |
| Allowed Workflow Types | WOE types, stages, and roles |
| Decision Authority | Scope and conditions of decision creation |
| Approval Authority | Scope and conditions of approval |
| Rejection Authority | Scope and conditions of rejection |
| Escalation Authority | Destinations, triggers, and interim powers |
| Delegation Rights | Delegable and non-delegable rights |
| Required Inputs | Governed objects and versions required to act |
| Required Outputs | Output contracts and consumers |
| Required Review Gates | Independent reviews before outputs gain authority |
| Dependencies | Agents, knowledge, evidence, memory, workflow, and policy dependencies |
| Consumers | Authorized downstream users |
| Security Classification | Access, confidentiality, and handling requirements |
| Activation Conditions | Requirements for Active state |
| Restriction Conditions | Triggers and permitted restricted actions |
| Suspension Conditions | Triggers and immediate effects |
| Deprecation Conditions | Migration and new-work policy |
| Retirement Conditions | Closure, revocation, handoff, and archive requirements |
| Created At | Governed creation time and authority |
| Updated At | Latest material version time and authority |
| Audit Trail | Complete lifecycle, rights, actions, delegation, incident, and review history |

### 22.5 Mandatory rules

- An agent may not perform institutional work unless registered.
- An agent may not exceed its contract-defined authority.
- An agent may not send MACP message types outside its registry rights.
- An agent may not write SMI objects outside its registry rights.
- An agent may not produce or validate EES evidence outside its registry rights.
- An agent may not enter a WOE workflow unless eligible.
- An agent may not delegate authority it does not possess.
- An agent may not change its own registry status.
- An agent may not silently expand scope because it is technically capable.
- Suspended agents cannot issue authority-bearing outputs.
- Deprecated agents cannot be assigned new institutional work unless explicitly allowed.
- Retired agents cannot be reactivated without new governance.

### 22.6 Governance owners

Agent Governance owns registration and lifecycle. Domain governance owns domain authority. Security owns access classification. QA independently audits. Executive Decision resolves cross-domain institutional conflicts. Founder authority approves constitutional changes, risk-appetite authority restructuring, and reserved exceptions.

### 22.7 Violations

Violations include unregistered action, impersonation, hidden role, authority excess, unauthorized message, memory or evidence action, ineligible workflow entry, delegation breach, self-status change, silent permission expansion, or output during suspension.

Material violation triggers containment, restriction or suspension, affected-action and decision tracing, access review, consumer notification, independent investigation, remediation, and institutional learning.

### 22.8 Exceptions

An exception defines rule, identity, contract, rights, scope, purpose, evidence, risk, security, workflow, duration, controls, authority, monitoring, expiry, audit, and return to conformance. It cannot authorize unregistered institutional action or false identity.

### 22.9 Registry evolution

Every standard amendment defines problem, evidence, semantic change, alternatives, affected agents and rights, compatibility, migration, historical interpretation, MACP/SMI/EES/WOE impact, security, audit, effective date, deprecation, rollback, and approval.

### 22.10 Periodic review

Governance asks:

- Does every acting identity have a current contract and record?
- Are permissions narrower than capability and aligned with responsibility?
- Are message, memory, evidence, and workflow rights consistent?
- Are status and restrictions enforced continuously?
- Are validation, risk, executive, and QA roles independent?
- Are delegations bounded, expiring, and attributable?
- Can every authority-bearing action be reconstructed?
- Are deprecated and retired agents prevented from new work?
- Are replacements preserving history without inheriting excess authority?
- Are exceptions becoming hidden roles or permissions?

### 22.11 Permanent rules

- No institutional agent exists outside the Registry.
- No Registry Record exists without an approved Agent Contract.
- No capability, access, confidence, or provider status creates authority.
- No agent changes its own rights or status.
- No restriction, suspension, deprecation, retirement, or historical action is erased.
- Every message, memory action, evidence action, workflow role, decision, delegation, and lifecycle event resolves to exact Registry and Contract versions.

The Agent Registry governs institutional identity and eligibility. It enables specialized agents to cooperate without allowing capability, convenience, or hierarchy to dissolve constitutional boundaries.

## Phase 1.5 Integration Reconciliation

This reconciliation note binds later operational responsibilities without creating new agents or enlarging authority.

### Operational role bindings

| Responsibility | Binding for v1.0 | Authority boundary |
|---|---|---|
| Deployment governance | Explicit human governance role operating DGS, supported by registered agents within their existing contracts | May activate only within current EDP, PRC, RRP and DGS scope; cannot create evidence, Validation or risk authority |
| Monitoring governance | Hybrid human operator and registered monitoring-workflow participants | Observes, records and escalates under MEDS; cannot silently retune, change limits or reactivate |
| Portfolio construction ownership | Hybrid governed workflow using Quant Strategy Architect, Validation Agent, Risk Governance Agent and Executive Decision Agent only for their existing bounded functions | No participant inherits another participant's authority; PCS classification is not risk or deployment approval |
| Production-readiness ownership | Explicit human readiness coordinator supported by registered reviewers | Classifies readiness under PRC only; cannot issue EDP, risk approval or DGS activation |
| Command operations | Human command issuer/owner and WOE coordinator | CM routes and constrains commands; it cannot expand AR rights or override standards |
| Institutional operations | Explicit human operating-cycle owner supported by registered agents | IOP coordinates queues, reviews and records; it cannot bypass constitutional gates |
| Future specialized operational agents | Deferred governance decision | Any future agent requires an approved contract and AR registration before institutional action |

### Original placeholder folders

| Folder | v1.0 classification | Institutional effect |
|---|---|---|
| `agents/CEO-Agent/` | Deprecated alias pending governance mapping to Executive Decision Agent | No authority arises from the folder; Executive Decision authority exists only under the approved contract and Registry record |
| `agents/Python-Agent/` | Retained bounded non-authority implementation helper under Quant Strategy Engineer governance | Cannot change hypotheses, validate, approve risk or deploy |
| `agents/Pine-Agent/` | Retained bounded non-authority implementation helper under Quant Strategy Engineer governance | Cannot change reference behavior or issue parity/Validation verdicts |
| `agents/QA-Agent/` | Retained bounded non-authority review helper; not equivalent to Validation Agent | Cannot issue VEP, accept risk or authorize deployment |

The folders are preserved for lineage. They remain inactive for institutional authority until a governed contract and Registry decision states otherwise.
