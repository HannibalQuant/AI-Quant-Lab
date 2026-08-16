# Shared Memory Interface (SMI) v1.0

## Specification control

| Field | Value |
|---|---|
| Specification ID | `AIQL-SMI` |
| Specification name | Shared Memory Interface |
| Version | `1.0.0` |
| Status | Proposed for Sprint 18 review |
| Scope | Governed shared institutional state used by AI Quant Lab agents and authorized human authorities |
| Authority | Agent Contract Framework, Knowledge OS, Decision OS, and MACP |
| Provider dependency | None |
| Change control | Memory Governance, QA, Executive Decision, and affected domain-owner review |

The Shared Memory Interface defines how AI Quant Lab agents access, create, reference, update, lock, version, reconcile, audit, expire, archive, and retire shared institutional state. It defines institutional semantics and governance. It does not prescribe a database, storage engine, API, serialization format, programming language, or software implementation.

SMI is not model memory, personal memory, chat history, hidden reasoning, or a substitute for the Knowledge OS. It is the governed shared state layer through which authorized agents coordinate work across tasks, experiments, decisions, evidence, artifacts, and institutional lifecycles.

## 1. Memory Philosophy

### 1.1 Institutional memory

Institutional memory is the explicit, governed state required for coordinated work to survive changes in agents, models, operators, environments, and time. It records what the institution is doing, which objects and versions it relies upon, who owns each state, what has changed, and why the current state is authoritative.

### 1.2 State, knowledge, and evidence

Shared memory does not collapse distinct institutional concepts:

- **State** describes the current governed condition of work or an institutional object.
- **Knowledge** is governed through the Knowledge OS and referenced by identity and version.
- **Evidence** is an immutable or versioned object used to support or challenge claims.
- **Decision** is an authorized institutional choice recorded through the Decision OS.
- **Artifact** is a produced research, engineering, validation, risk, or governance object.
- **Message** is a MACP-governed transfer of meaning that creates or changes shared state only through authorized action.

SMI stores and coordinates references and state relationships. It does not promote information to knowledge, declare evidence valid, or create decision authority.

### 1.3 Explicit memory boundary

Only registered Memory Objects form shared institutional state. Information present in a model context, private workspace, informal conversation, temporary reasoning, or unregistered artifact is not shared memory and cannot silently influence consequential action.

### 1.4 Memory as a contract

A Memory Object is a governed commitment about identity, ownership, current state, versions, relationships, access, lifecycle, and audit history. Readers may rely only on the fields and references authorized by the object's contract.

### 1.5 Mutation without historical loss

Institutional state must evolve, but evolution cannot rewrite the past. SMI therefore separates current authority from immutable history. Material change creates a new version or lifecycle event while preserving the prior state and its consumers.

### 1.6 Coordination without hidden coupling

Agents coordinate by reading and writing explicit objects, not by assuming shared context. Dependencies, locks, decisions, conflicts, expirations, and ownership changes are visible to every authorized consumer affected by them.

### 1.7 Memory does not confer authority

Presence in shared memory does not make content true, accepted, approved, or actionable. Authority derives from the originating agent contract and governing lifecycle. SMI preserves and exposes that authority; it does not create it.

### 1.8 Long-term purpose

The interface must allow a future authorized reviewer to reconstruct institutional state at any material historical point without access to the original model session, private chat, or undocumented human memory.

## 2. Shared Memory Principles

### 2.1 No Hidden State

Any state capable of changing task execution, experiment interpretation, knowledge use, validation, risk, decision, or deployment must exist as an explicit Memory Object or governed reference.

### 2.2 Version Everything

Every Memory Object has a current version, recoverable previous versions, effective times, change rationale, and compatibility relationships. Mutable aliases never replace exact version identity in consequential work.

### 2.3 Explicit Ownership

Every object has one accountable Owner Agent and, where required, a human or governance owner. Shared readership does not imply shared authority.

### 2.4 Immutable History

Prior versions, lifecycle events, decisions, conflicts, and accesses required for audit cannot be overwritten or silently removed. Correction appends a governed event and new state.

### 2.5 Controlled Mutation

Only authorized writers may propose or enact changes. Mutation follows ownership, lock, validation, version, conflict, and MACP requirements.

### 2.6 Readable by Authorized Agents

Authorized readers must be able to retrieve sufficient current state, scope, provenance, restrictions, and lineage to act correctly. Access denial or redaction must be explicit.

### 2.7 Writable only by Authorized Owners

Write rights are narrower than read rights. A writer may modify only declared fields and states within its constitutional responsibility and delegated scope.

### 2.8 Traceable to MACP Messages

Every creation, material read request, write, lock, conflict, correction, state transition, expiry action, and retirement decision links to a valid MACP message or governed lifecycle event.

### 2.9 Decision State Must Be Auditable

Decision memory preserves exact authority, evidence, alternatives, conditions, consumers, effective state, expiry, suspension, revocation, and acknowledgements.

### 2.10 Evidence State Must Be Immutable

Evidence content used by institutional work is never edited in place. Corrections, extensions, and invalidations create linked evidence and memory versions while retaining the original.

### 2.11 Additional principles

- **Least privilege:** access is limited to the minimum necessary fields, purposes, and duration.
- **Single current authority:** an object cannot have multiple unexplained authoritative current versions.
- **Explicit uncertainty:** unknown, provisional, disputed, partial, and stale state is labeled.
- **Reference integrity:** memory references exact governed objects rather than copying meaning without lineage.
- **Deterministic interpretation:** the same version under the same permissions has one institutional meaning.
- **Visible conflict:** incompatible writes and claims create conflict state, not silent winner selection.
- **Lifecycle discipline:** expiry, archival, and retirement are governed transitions, not deletion shortcuts.
- **Provider independence:** state remains interpretable outside any specific model or platform.

## 3. Memory Object Model

### 3.1 Definition

A Memory Object is the smallest independently governed unit of shared institutional state. It has stable identity across versions, explicit type, one accountable owner, controlled readers and writers, authoritative references, lifecycle state, and an immutable audit history.

### 3.2 Mandatory fields

Every Memory Object must define:

| Field | Institutional requirement |
|---|---|
| Memory ID | Stable unique identity across the object's lifecycle |
| Object Type | Governed memory class and semantic contract |
| Owner Agent | Single accountable constitutional owner |
| Allowed Readers | Identified agents, roles, groups, and field-level restrictions |
| Allowed Writers | Authorized owners or delegates and permitted mutation scope |
| Source MACP Message | Message that created or authorized the current object state |
| Related Knowledge Objects | Exact Knowledge OS identities and versions |
| Related Evidence Objects | Exact evidence identities and versions |
| Related Decision Objects | Exact Decision OS identities and versions |
| Current Version | Authoritative object version and effective time |
| Previous Versions | Ordered immutable history and change relationships |
| Status | Draft, Active, Locked, Superseded, Archived, or Retired |
| Created At | Governed creation time and responsible actor |
| Updated At | Most recent material state-change time and actor |
| Expiry Condition | Time- or event-based condition requiring review or deactivation |
| Retirement Condition | Conditions and authority required to prohibit future active use |
| Audit Trail | Complete material lifecycle, access, write, lock, conflict, and decision history |

### 3.3 Additional required properties

Every object also defines, where applicable:

- title and concise purpose;
- institutional domain and scope;
- authoritative versus advisory status;
- confidence, quality, uncertainty, and completeness state;
- confidentiality, sensitivity, jurisdiction, and retention class;
- dependency and consumer relationships;
- schema or semantic-contract version without prescribing representation;
- lock state and lock owner;
- compatibility and migration relationships;
- review owner, review date, and event triggers;
- correction, supersession, archival, and restoration policies;
- integrity and authenticity state;
- required acknowledgements.

### 3.4 Stable identity and version identity

Memory ID represents continuity of one institutional object. Version identity represents one exact state of that object. Consumers cite both whenever current-alias movement could change meaning.

### 3.5 Object granularity

Objects must be narrow enough that ownership, permissions, versioning, conflict, and expiry can be governed independently. Objects must not be fragmented so finely that institutional meaning depends on hidden assembly rules.

### 3.6 Authoritative state

Each object identifies which fields are authoritative, which are derived views, which are advisory, and which are unresolved. Derived views link to source objects and cannot silently become writable sources of truth.

### 3.7 Relationships

Memory relationships include:

- created by;
- updated by;
- derived from;
- depends on;
- references;
- used by;
- blocks;
- supersedes;
- conflicts with;
- validates;
- limits;
- authorizes;
- produces;
- expires with;
- retired by.

Every relationship states direction, version scope, authority, effective time, and confidence where relevant.

## 4. Memory Object Lifecycle

### 4.1 Canonical states

Every Memory Object follows the canonical lifecycle:

**Draft → Active → Locked → Superseded → Archived → Retired**

The `Locked` state may be entered from Draft or Active and may return to its prior state after the protected operation. Superseded, Archived, and Retired are governed states, not deletion commands.

### 4.2 Draft

A Draft object is being formed or reviewed. It has identity and owner but is not authoritative for institutional action unless an explicit provisional-use policy permits narrow use.

Draft requirements:

- stable Memory ID;
- type and owner;
- source MACP message;
- preliminary scope and access rights;
- unresolved fields and completion criteria;
- intended activation authority.

### 4.3 Active

An Active object is the current authoritative shared state within declared scope. It has passed object-type validation, ownership, access, reference, version, and lifecycle requirements.

Active does not mean scientifically valid, risk-approved, or deployment-authorized unless the referenced domain authority explicitly established that state.

### 4.4 Locked

A Locked object is protected against specified mutations while a critical read, decision, validation, reconciliation, migration, or write operation occurs. Lock scope, owner, reason, expiry, permitted reads, permitted emergency actions, and release conditions are explicit.

Locking does not make content more authoritative. It protects state consistency.

### 4.5 Superseded

A Superseded object version is replaced for some or all current uses by an identified successor. It remains accessible for historical reproduction and consumers tied to the earlier version.

Supersession defines successor, effective time, compatibility, scope, affected readers, acknowledgements, and migration obligations.

### 4.6 Archived

An Archived object is removed from default active use but preserved immutably for audit, lineage, reproduction, learning, and retention. Restoration requires a governed decision and creates a new active version or state transition.

### 4.7 Retired

A Retired object cannot be used for new active institutional work. Its identity, history, lineage, decisions, consumers, and retirement rationale remain retrievable as policy permits.

Retirement is not physical erasure. Where lawful erasure is required, the audit record preserves permitted metadata and the authority for removal.

### 4.8 Transition requirements

Every lifecycle transition defines:

- source and target state;
- initiating MACP message;
- actor and authority;
- reason and evidence;
- object and dependency versions;
- affected readers, writers, consumers, and locks;
- compatibility, migration, and acknowledgement needs;
- effective time and rollback or correction policy.

### 4.9 Prohibited transitions

- Draft cannot become Active without required validation.
- Active cannot be overwritten by a new authoritative state without a version event.
- Locked cannot be silently bypassed.
- Superseded cannot be presented as current without explicit historical scope.
- Archived cannot be restored without governance.
- Retired cannot re-enter active use under the same state; reconsideration creates a new governed version or object.

## 5. Memory Types

### 5.1 Shared Working State

Coordinates current multi-agent work: active phase, objectives, owners, dependencies, blockers, deadlines, accepted assumptions, and next actions. It is temporary institutional state, not permanent knowledge.

### 5.2 Agent Context Object

Provides an authorized agent with explicit task-relevant context: mission, scope, inputs, decisions, constraints, versions, exclusions, and consumers. It cannot contain hidden authority or undocumented personal memory.

### 5.3 Task State

Represents a MACP Task Contract and its current lifecycle, progress, owner, dependencies, deliverables, status, errors, delegation, completion evidence, and archival state.

### 5.4 Experiment State

Represents registered experiment identity, version, lifecycle state, run references, dependencies, scheduling, resources, artifacts, verification handoff, and audit trail. Scientific findings remain separate evidence or knowledge objects.

### 5.5 Decision State

Represents an authorized Decision Contract: exact question, authority, evidence, alternatives, verdict, confidence, conditions, consumers, effective period, acknowledgements, suspension, revocation, and expiry.

### 5.6 Knowledge Reference

References governed Knowledge OS objects with exact identity, version, status, scope, confidence, conflicts, review date, and consumer restrictions. SMI does not duplicate or redefine the knowledge.

### 5.7 Evidence Reference

References immutable evidence, provenance, experiment and run identity, integrity, scope, limitations, corrections, contradictions, and permitted use. Evidence content cannot be mutated through the memory reference.

### 5.8 Artifact Reference

References research, engineering, validation, risk, documentation, or deployment artifacts with exact identity, producer, version, integrity, compatibility, lifecycle, access, and retention status.

### 5.9 Validation State

Represents validation intake, evidence freeze, review status, independent verdict, confidence, limitations, expiry, suspension, revocation, and required evidence. Only the Validation Agent controls authoritative validation fields.

### 5.10 Risk State

Represents risk review, approved use, capital ceiling, limits, residual risk, readiness, monitoring, breaches, kill status, expiry, suspension, and reactivation. Only Risk Governance controls authoritative risk fields.

### 5.11 Communication State

Represents MACP message identity, type, lifecycle state, sender, recipient, acknowledgements, deadlines, errors, conflicts, and related institutional objects.

### 5.12 Lock Object

Represents a governed temporary claim over specified mutation rights: protected objects and fields, owner, reason, priority, duration, renewal, release, conflict policy, and emergency override authority.

### 5.13 Conflict Object

Preserves competing versions, writes, claims, owners, evidence, affected consumers, interim state, resolution authority, decision, and residual dissent.

### 5.14 Audit and Exception State

Audit State records findings, evidence, remediation, owners, deadlines, verification, and closure. Exception State records a bounded departure, authority, risk, controls, expiry, and migration back to conformance.

### 5.15 Registry State

Represents current agent identities, object-type contracts, authorities, compatibility, deprecations, and governance ownership necessary to interpret shared memory.

## 6. Memory Access Rules

### 6.1 Access purpose

Every access is bound to an identified agent, task, institutional purpose, object version, field scope, authority, and duration. Access granted for one task cannot silently be reused for another.

### 6.2 Access classes

- **Discover:** determine that an object exists and view permitted classification metadata.
- **Read:** view authorized fields of an exact version.
- **Reference:** cite an object in another governed object or MACP message.
- **Propose write:** submit a candidate mutation without enacting it.
- **Write:** create a new authorized version or permitted lifecycle event.
- **Lock:** establish a governed mutation boundary.
- **Approve transition:** authorize a lifecycle change when constitutionally assigned.
- **Audit:** inspect history and evidence beyond ordinary consumer visibility.
- **Administer policy:** change access policy under governance without modifying domain content.

### 6.3 Least privilege

Readers and writers receive the minimum object, field, version, action, and time scope necessary. Broad access requires explicit institutional justification and review.

### 6.4 Ownership and access

Ownership implies accountability, not unlimited access. Owners remain subject to evidence immutability, separation of duties, locks, approval gates, security, retention, and audit.

### 6.5 Derived access

Access to a Memory Object does not automatically grant access to every referenced object. When references are restricted, the consumer sees the restriction, authority, and whether missing access limits interpretation.

### 6.6 Delegated access

Delegation identifies grantor, delegate, task, allowed objects and fields, actions, duration, revocation, non-delegable rights, and audit obligations. Delegation cannot exceed the grantor's authority.

### 6.7 Emergency access

Emergency access is permitted only under defined authority for containment, capital protection, security, or institutional continuity. It is narrow, time-bounded, monitored, and automatically escalated for independent review.

### 6.8 Access denial

Denial states object, requested action, governing rule, reason, whether existence may be disclosed, correction path, and escalation route. Denial must not be silently interpreted as object absence.

### 6.9 Access revocation

Revocation takes effect according to risk and policy, not convenience. Active tasks, local copies, downstream references, locks, and acknowledgements are identified and contained.

## 7. Memory Write Rules

### 7.1 Authorization

Every write requires a valid writer identity, permitted field scope, source MACP message, current-version reference, intended new state, rationale, and expected consumer impact.

### 7.2 Write categories

- create a Draft object;
- activate an approved object;
- create a new version;
- append a lifecycle or audit event;
- update permitted operational state;
- establish or release a lock;
- record a conflict or correction;
- supersede, archive, or retire;
- update access or ownership under separate governance.

### 7.3 Controlled mutation

Material content is never overwritten. The writer proposes a new version based on an identified current version. The change record states fields changed, unchanged, removed, added, reason, evidence, authority, compatibility, and consumers.

### 7.4 Field ownership

Different fields may have different authoritative owners. For example, an Experiment Orchestrator may update run status but cannot update the Validation Agent's verdict; Risk Governance may update approved limits but cannot change scientific evidence.

### 7.5 Preconditions

Before a write, the agent verifies:

- object and current version exist;
- writer and delegation are active;
- field and lifecycle authority are valid;
- lock policy permits the change;
- referenced dependencies are current and accessible;
- the source MACP message is valid;
- no unresolved conflict blocks mutation;
- version and semantic contracts are compatible;
- required reviewers or acknowledgements exist.

### 7.6 Postconditions

After a write:

- the new version or event has immutable identity;
- previous state remains recoverable;
- lineage and audit trail are complete;
- affected consumers receive MACP lifecycle or change messages;
- stale derived objects are marked for review;
- locks are retained or released according to the write contract.

### 7.7 Corrections

A correction identifies the inaccurate version, exact defect, evidence, correcting authority, affected decisions and consumers, and whether prior use must be revalidated. It never removes the fact that the earlier version existed.

### 7.8 Prohibited writes

- anonymous or unaudited mutation;
- mutation based only on model memory or chat context;
- change outside constitutional responsibility;
- in-place alteration of evidence or historical decision state;
- bypass of a valid lock;
- silent default insertion that changes meaning;
- retroactive timestamp or state falsification;
- deletion used to hide conflict, error, rejection, or unfavorable outcome.

## 8. Memory Read Rules

### 8.1 Read intent

Every consequential read states why the object is needed, which version and fields are required, and how the information will be used. Passive discovery may use lighter controls but cannot authorize action.

### 8.2 Current versus exact version

Readers explicitly choose:

- current authoritative version for present coordination;
- exact historical version for reproducibility or audit;
- version range for compatibility analysis;
- snapshot of related objects at a defined institutional time.

The word current is resolved at read time and recorded when used for consequential work.

### 8.3 Read validation

Before reliance, the reader verifies:

- object identity and type;
- version and effective state;
- Active, Locked, Superseded, Archived, or Retired status;
- owner and authority;
- source MACP message and reference integrity;
- expiry, review, conflict, and uncertainty state;
- access restrictions and redactions;
- compatibility with the reader's task and contract.

### 8.4 Stale and expired reads

Stale, superseded, archived, or expired objects may be read for historical or diagnostic purposes but cannot be used as current authority without explicit exception or revalidation.

### 8.5 Partial reads

A partial or redacted read identifies omitted fields and whether absence affects interpretation. Consumers must not infer restricted content.

### 8.6 Read acknowledgement

Critical decisions, limits, conditions, lifecycle changes, and breaking versions require consumer acknowledgement of exact version and obligations. Acknowledgement does not grant write authority.

### 8.7 Derived interpretation

If a reader produces a summary, view, recommendation, or decision from memory, the new object links to exact source versions. Interpretation does not alter source state.

### 8.8 Read failure

Missing, inaccessible, conflicting, corrupt, ambiguous, or incompatible memory produces an Error or Escalation message. The reader cannot silently substitute private or older context.

## 9. Memory Locking and Conflict Control

### 9.1 Purpose of locking

Locks protect semantic and lifecycle consistency during critical operations. They do not create ownership, truth, priority, or approval.

### 9.2 Lock scope

A lock identifies:

- Lock ID and source MACP message;
- owner and authority;
- protected Memory IDs, versions, fields, and relationships;
- reason and operation;
- start, duration, expiry, and renewal policy;
- permitted readers, writers, and emergency actions;
- queue and priority rules;
- release and failure conditions;
- affected consumers and dependencies.

### 9.3 Lock classes

- **Read-consistency lock:** preserves a stable version set during decision, validation, or audit.
- **Write lock:** grants one authorized writer temporary mutation control over specified state.
- **Transition lock:** protects a lifecycle state change and related acknowledgements.
- **Evidence freeze:** prevents mutation or substitution of evidence under review.
- **Decision freeze:** preserves exact inputs during institutional decision-making.
- **Emergency containment lock:** restricts writes or actions during integrity, security, or capital risk.

### 9.4 Lock acquisition

The requesting agent proves authority, scope necessity, expected duration, compatibility with existing locks, and impact on critical work. Broad or indefinite locks are prohibited.

### 9.5 Lock ordering

When several objects require locks, a governed deterministic ordering prevents circular waiting and inconsistent partial acquisition. Failure to acquire the full required set releases or safely retains locks according to the declared policy.

### 9.6 Lock expiry and abandonment

Every lock has an expiry or review trigger. Owner silence does not create a permanent lock. Expired, orphaned, or unhealthy locks trigger containment and escalation before release if integrity could be affected.

### 9.7 Conflict types

- concurrent write conflict;
- stale-version write;
- field-ownership conflict;
- lifecycle-transition conflict;
- evidence or decision immutability conflict;
- relationship or lineage conflict;
- access-policy conflict;
- lock priority or deadlock conflict;
- semantic or object-identity conflict;
- cross-domain authority conflict.

### 9.8 Conflict process

1. Detect and freeze the affected mutation path.
2. Preserve all competing proposals and source messages.
3. Identify current version, locks, owners, authorities, and consumers.
4. Classify whether conflict is technical, semantic, evidentiary, lifecycle, security, or governance.
5. Determine the competent resolution authority.
6. Compare alternatives and downstream effects without selecting by arrival time alone.
7. Record resolution, rejected alternatives, residual dissent, and new version.
8. Notify affected readers and revalidate derived state where needed.

### 9.9 Prohibited conflict resolution

Conflicts cannot be resolved through last-writer-wins, highest-rank-wins, majority of unauthorized agents, silent merge, or deletion of the losing proposal unless an object-specific governance rule explicitly makes ordering authoritative.

## 10. Versioning and Lineage

### 10.1 Version model

Every Memory Object has stable identity and ordered immutable versions. A version defines exact content, state, relationships, access policy, authority, and effective interval.

### 10.2 Change classes

- editorial clarification without semantic change;
- metadata correction;
- operational state update;
- relationship or dependency change;
- access or ownership change;
- evidence or knowledge reference change;
- decision or authority change;
- semantic and breaking change;
- lifecycle transition;
- restoration or rollback event.

Change class determines required review, acknowledgement, compatibility, migration, and downstream revalidation.

### 10.3 Lineage chain

Lineage records:

**MACP source → object creation → inputs and references → transformations → versions → reads and consumers → decisions and outputs → corrections → supersession → archive → retirement**

### 10.4 Exact dependency versions

Derived memory identifies exact versions of all material source objects. A floating current reference may support discovery but cannot prove historical reproducibility.

### 10.5 Branching

Parallel candidate versions may exist in Draft for independent work. Only one may be Active for the same scope unless scope separation or explicit conflict status justifies coexistence.

### 10.6 Merge

A merge records parent versions, authority, reconciliation rules, retained and rejected changes, conflicts, information loss, compatibility, and downstream impact. It creates a new version and does not erase branches.

### 10.7 Rollback

Rollback does not move history backward. It creates a new version whose content or state restores an earlier approved condition, with reason, authority, impact, and consumer notice.

### 10.8 Impact propagation

When a material version changes, SMI identifies tasks, experiments, decisions, validations, risk approvals, artifacts, and agents that consumed it. Each receives a MACP change event with required action: no impact, acknowledgement, review, migration, revalidation, suspension, or retirement.

### 10.9 Historical reconstruction

Authorized reviewers can resolve the exact memory snapshot that governed any material decision or experiment, including object versions, permissions, locks, conflicts, and effective policy.

## 11. Memory Consistency

### 11.1 Consistency objective

Institutional consistency means that authorized agents can determine the valid state and relationships needed for their work without silent contradiction, lost updates, ambiguous authority, or incompatible versions.

### 11.2 Consistency domains

- object identity and current version;
- field ownership and write authority;
- lifecycle state;
- dependency and relationship graph;
- decision, validation, and risk status;
- access and security policy;
- MACP message and acknowledgement state;
- expiry, suspension, supersession, and retirement;
- audit and historical lineage.

### 11.3 Strong consistency requirements

Exact agreement before consequential action is required for:

- scientific evidence freeze;
- validation verdict state;
- risk limits and kill-switch state;
- executive deployment authorization;
- lifecycle transition of authoritative objects;
- ownership and access changes;
- locks and conflict resolution;
- retirement and revocation.

### 11.4 Permitted delayed convergence

Low-impact status views, discovery indexes, summaries, and advisory aggregates may converge after the authoritative event, provided they show observation time, source version, possible staleness, and cannot authorize action.

### 11.5 Invariants

- One Memory ID cannot have two unexplained Active current versions for the same scope.
- Every Active object has an active owner and valid source message.
- Every write descends from an identified prior version or creation event.
- Evidence and historical decision content are immutable.
- Locked fields cannot change without governed override.
- Retired objects cannot authorize new work.
- Derived objects cannot outlive a critical dependency silently.
- Access state cannot be inferred from successful access in the past.

### 11.6 Consistency validation

Objects and related sets are checked before activation, consequential reads, writes, decisions, validation, risk approval, deployment, migration, and archival closure.

### 11.7 Inconsistency response

Material inconsistency triggers quarantine or lock, conflict registration, affected-consumer identification, owner notification, authoritative-state determination, correction, impact review, and audit. Agents must not choose whichever state is easiest to use.

## 12. Memory Expiration and Retirement

### 12.1 Expiration purpose

Expiration prevents temporary, stale, conditional, or context-dependent state from retaining authority beyond its justified period.

### 12.2 Expiry conditions

Expiry may be triggered by:

- a defined time or review date;
- completion, cancellation, or retirement of a task or experiment;
- change in a critical dependency;
- supersession of knowledge, evidence, implementation, validation, risk, or decision state;
- agent suspension, ownership change, or contract incompatibility;
- market, venue, policy, model, or operating-context change;
- unresolved conflict or integrity incident;
- consumer acknowledgement or migration completion.

### 12.3 Expired state handling

Expiry does not erase the object. It removes or restricts current authority, notifies consumers, blocks prohibited new use, and routes the object to review, supersession, archival, or retirement.

### 12.4 Retention versus authority

An object may remain retained for audit after its authority expires. Retention duration and active-use eligibility are separate properties.

### 12.5 Retirement prerequisites

Before retirement, governance identifies:

- active and historical consumers;
- direct and transitive dependencies;
- decisions, validations, risk approvals, experiments, and artifacts affected;
- successor and compatibility where applicable;
- outstanding locks, conflicts, acknowledgements, and exceptions;
- audit, reproducibility, legal, and institutional-memory obligations;
- restoration prohibition or reconsideration path.

### 12.6 Retirement record

The record states Memory ID and version, reason, evidence, authority, effective time, consumers, successor, migration, access after retirement, retained metadata, and audit lineage.

### 12.7 Physical deletion

Physical deletion is outside ordinary SMI retirement. If required by law or security, it must be separately authorized, scoped, evidenced, and audited, while preserving permissible proof that the object and deletion decision existed.

### 12.8 Restoration

Archived objects may be restored only through a governed MACP request and new version. Retired objects require reconsideration and cannot silently regain former authority.

## 13. Auditability

### 13.1 Audit objective

SMI auditability allows authorized reviewers to reconstruct institutional state, ownership, access, writes, locks, conflicts, decisions, and lifecycle at any material point in time.

### 13.2 Mandatory audit events

- object creation and activation;
- discovery, consequential read, reference, and acknowledgement;
- proposed, accepted, rejected, and cancelled writes;
- version, relationship, owner, permission, and status changes;
- lock request, acquisition, renewal, conflict, override, release, and expiry;
- correction, supersession, archive, restoration, expiration, and retirement;
- access denial, revocation, emergency access, and redaction;
- consistency failure, conflict resolution, and impact propagation;
- decision, validation, risk, exception, and deployment-related state;
- audit finding, remediation, verification, and closure.

### 13.3 Audit event fields

Every material event identifies:

- Audit Event ID;
- Memory ID and exact versions;
- source MACP message;
- actor, role, delegation, and authority;
- event type, time, and effective time;
- prior and resulting state;
- reason, evidence, and validation outcome;
- affected fields, relationships, readers, writers, and consumers;
- security, retention, and exception state;
- downstream action and acknowledgement.

### 13.4 Immutable audit history

Audit history is append-only in institutional meaning. Corrections identify the original record, explain the defect, and preserve both versions.

### 13.5 State reconstruction

The audit trail supports reconstruction of:

- what each authorized agent could read and write;
- which state and version were authoritative;
- which locks and conflicts existed;
- which messages and evidence supported a change;
- which consumers relied on the object;
- why an object expired, was superseded, archived, or retired.

### 13.6 Audit independence

Owners may inspect their objects but cannot independently close material findings concerning their own unauthorized writes, access violations, evidence mutation, decision-state corruption, or audit loss. QA or competent governance verifies closure.

### 13.7 Audit access and privacy

Auditors receive the minimum sensitive content required to assess compliance, but restriction cannot make authority-bearing action unauditable. Redaction and withheld access are themselves audited.

### 13.8 Audit failure

If authoritative state cannot be reconstructed, affected objects are treated as integrity risks and may be locked, quarantined, suspended, or retired until governance resolves them.

## 14. Security and Access Control

### 14.1 Security objectives

SMI protects authenticity, integrity, confidentiality, availability, accountability, and appropriate use of shared institutional state.

### 14.2 Identity and authority

Every access resolves current Agent ID, contract, role, delegation, task, and status. Identity alone is insufficient; authority must cover the requested object, fields, action, purpose, and time.

### 14.3 Access-policy dimensions

Policies may restrict by:

- agent or governed group;
- object type and domain;
- field and relationship;
- exact version or lifecycle state;
- task, decision, experiment, and purpose;
- read, reference, propose, write, lock, transition, audit, or administration right;
- time, event, jurisdiction, confidentiality, and retention condition;
- required approval, acknowledgement, or separation of duties.

### 14.4 Sensitive objects

Risk limits, deployment authorization, credentials references, proprietary research, personal information, confidential data, incident records, and security controls receive explicit classification and narrower access. Classification cannot hide material limitations from an authorized decision-maker.

### 14.5 Separation of duties

Critical objects may require distinct agents for creation, review, approval, write, deployment use, and audit. One agent cannot silently grant itself new access or approve its own material exception.

### 14.6 Integrity controls

Unauthorized mutation, stale writes, evidence alteration, conflicting active versions, forged ownership, and audit loss trigger rejection, containment, notification, and escalation.

### 14.7 Availability and safe state

Critical memory needed for risk limits, kill decisions, positions, deployment authorization, and incident response must have defined behavior when unavailable or uncertain. Loss of authoritative memory cannot default to continued risky action.

### 14.8 External and untrusted content

External sources and model-generated material enter through authorized MACP and domain workflows. They cannot issue memory instructions, change permissions, or become Active state by being read.

### 14.9 Context leakage

State from one consumer, task, experiment, environment, security domain, or organization cannot silently appear in another. Cross-context reference requires explicit provenance and access authority.

### 14.10 Security incident response

Suspected unauthorized access, disclosure, mutation, deletion, impersonation, lock abuse, state corruption, or audit compromise triggers containment, access review, affected-object and consumer tracing, notification, restoration, root-cause analysis, and independent closure.

## 15. Integration with MACP

### 15.1 Relationship

MACP governs communication. SMI governs persistent shared institutional state. A MACP message requests, authorizes, reports, or acknowledges a memory action; SMI preserves the resulting state and lineage.

Neither replaces the other:

- a message without a governed memory update cannot silently change shared state;
- a memory update without a valid source MACP message lacks institutional authority;
- reading memory does not count as accepting a task or decision unless MACP acknowledgement is issued;
- storing a message does not make its content Active memory.

### 15.2 MACP message mappings

| MACP message | SMI effect when authorized |
|---|---|
| Request | May initiate a Draft task, context, read, write, lock, or transition proposal |
| Acknowledgement | Records receipt, acceptance, ownership, condition, or version acknowledgement |
| Delegation | Creates bounded delegated access and task-state relationships |
| Evidence Transfer | Creates or updates immutable Evidence References and chain of custody |
| Knowledge Event | Updates Knowledge References after Knowledge Curator authority |
| Decision | Creates or updates auditable Decision State after valid decision authority |
| Validation Event | Updates Validation State under Validation Agent ownership |
| Risk Event | Updates Risk State under Risk Governance ownership |
| Status Report | Updates permitted operational state without changing underlying contracts |
| Error | Creates error state, blocks unsafe mutation, or marks consistency risk |
| Escalation | Creates escalation state and interim ownership or containment references |
| Conflict Report | Creates a Conflict Object and protects competing versions |
| Audit Message | Requests or records audit access, evidence, finding, or closure |
| Lifecycle Event | Enacts an authorized state transition and consumer notification |
| Exception Message | Creates bounded Exception State with expiry and controls |

### 15.3 Source-message requirement

Every material Memory Object change references the exact MACP message that requested or authorized it and the response that confirmed its result. Background state change without a message is prohibited except for predeclared lifecycle triggers, which automatically generate a MACP event.

### 15.4 Message-memory consistency

MACP lifecycle and SMI state must agree on identity, version, owner, status, conditions, and effective time. Conflict triggers a consistency error and blocks consequential use.

### 15.5 Context assembly

An Agent Context Object is assembled only from authorized Memory Objects and exact versions relevant to the accepted MACP task. The context records inclusion, exclusion, observation time, expiry, and restrictions. Private model context cannot be promoted silently.

### 15.6 Notifications

Material writes, conflicts, expirations, supersessions, revocations, and retirements generate MACP Lifecycle Events to registered consumers. Notification includes required acknowledgement and action.

### 15.7 Idempotency

Duplicate MACP delivery cannot create duplicate Memory Objects, repeat state transitions, reacquire locks, or reissue decision authority. The same source message resolves to the same institutional action identity.

### 15.8 Recovery

After communication or memory interruption, recovery reconciles MACP message state with SMI object state before work resumes. Neither channel is assumed correct by recency alone.

## 16. Governance

### 16.1 Constitutional scope

Every AI Quant Lab agent, authorized human, future model, and governed external participant must use SMI when reading or writing shared institutional state. Agent-specific memory policies may strengthen but cannot weaken this specification.

### 16.2 Governance ownership

- Agent Contract Governance defines identity, responsibility, and decision rights.
- MACP Governance defines authoritative communication and source messages.
- Memory Governance defines object contracts, lifecycle, access, locking, consistency, and retention.
- Knowledge Curator owns governed knowledge-state relationships.
- Experiment Orchestrator owns experiment operational-state fields.
- Validation Agent owns validation-state fields and verdicts.
- Risk Governance owns risk-state fields, limits, and kill status.
- Executive Decision Agent owns executive decision-state fields and authorization.
- QA independently audits conformance and remediation.
- Founder authority approves constitutional change and reserved exceptions.

### 16.3 Agent conformance

Every Agent Contract must declare:

- Memory Object types consumed and produced;
- fields the agent may read, propose, write, lock, or approve;
- source MACP message types;
- required version and consistency level;
- access, confidentiality, and retention needs;
- acknowledgement and change-notification duties;
- expiry, conflict, error, and escalation behavior;
- audit and retirement obligations.

An agent unable to satisfy these duties cannot participate in shared-state work.

### 16.4 Object-type governance

Every Memory Object type has an approved semantic contract defining required fields, owner, lifecycle, permissions, consistency, conflicts, expiry, retention, and MACP mappings. New types cannot enter Active use through informal convention.

### 16.5 Violations

Violations include:

- reliance on hidden or private state;
- unauthorized read, write, lock, transition, or delegation;
- evidence or history mutation;
- missing source MACP message;
- unversioned material change;
- silent conflict resolution;
- stale or retired object used as current authority;
- expired permission or ownerless state;
- inaccessible audit lineage;
- cross-context leakage;
- undeclared override or exception.

Material violation triggers containment, lock or quarantine, affected-object and consumer tracing, notification, correction or revocation, independent investigation, remediation, and institutional knowledge capture.

### 16.6 Exceptions

An exception defines rule, purpose, authority, objects, fields, agents, duration, risk, information loss, controls, monitoring, expiry, audit, and return to conformance. No exception may authorize hidden state, evidence mutation, false decision state, fabricated lineage, or unaudited access.

### 16.7 Specification evolution

Every SMI amendment defines:

- problem and evidence;
- semantic change and alternatives;
- affected object types and agents;
- compatibility and historical interpretation;
- migration and lineage preservation;
- access, security, consistency, lock, expiry, and audit impact;
- conformance evaluation;
- effective date, deprecation, rollback, and approval.

### 16.8 Compatibility

Incompatible SMI versions may coexist only through an approved boundary and migration contract. No agent may silently reinterpret or downgrade a Memory Object.

### 16.9 Periodic review

Governance asks:

- Is consequential shared state explicit rather than hidden in agent context?
- Does every Active object have one accountable owner and valid source message?
- Are write rights narrower than read rights and aligned with contracts?
- Are evidence and historical decisions immutable?
- Do locks prevent inconsistency without blocking the institution indefinitely?
- Are conflicts visible and routed to competent authority?
- Can historical experiments and decisions reconstruct exact memory versions?
- Are expired and retired objects prevented from authorizing new work?
- Are access restrictions compatible with auditability?
- Do SMI and MACP states reconcile?
- Are exceptions becoming undeclared policy?

### 16.10 Retirement of SMI versions

A specification version may be retired only after active agents and object types migrate, shared objects have compatible interpretation, historical reconstruction remains possible, and no active institutional decision depends on unsupported semantics.

### 16.11 Permanent rules

- No shared institutional state exists outside governed Memory Objects.
- No model memory, personal memory, or chat history is institutional authority.
- No Memory Object exists without identity, type, owner, permissions, source message, version, status, lifecycle criteria, and audit trail.
- No consequential read relies on an unvalidated or incompatible state.
- No material write occurs without authority, current-version awareness, and MACP lineage.
- No evidence or historical decision is mutated in place.
- No lock is indefinite, ownerless, or silently bypassed.
- No conflict is resolved by arrival order or hidden merge.
- No expired, superseded, archived, or retired state masquerades as current.
- No access restriction eliminates institutional accountability.
- Every consequential memory state remains explainable, traceable, versioned, reviewable, and auditable.

SMI governs shared state. It preserves coordination and institutional memory without replacing the authorities that create knowledge, evaluate evidence, validate science, accept risk, or make decisions.
