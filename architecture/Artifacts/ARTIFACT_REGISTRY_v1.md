# Artifact Registry (ART) v1.0

## Specification control

| Field | Value |
|---|---|
| Registry ID | `AIQL-ART` |
| Registry name | Artifact Registry |
| Version | `1.0.0` |
| Status | Proposed for Sprint 22 review |
| Scope | All institutional artifacts created, transferred, consumed, reviewed, or retained by AI Quant Lab |
| Authority | Agent Contract Framework, MACP, SMI, EES, WOE, Agent Registry, and Institutional Governance |
| Provider dependency | None |
| Change control | Artifact Governance, QA, Knowledge Curator, Executive Decision, and affected domain-owner review |

The Artifact Registry is the constitutional governance layer for products of institutional work. It governs artifact identity, classification, ownership, versions, lineage, provenance, relationships, consumers, quality state, freeze, supersession, deprecation, retirement, archival, and auditability. It is not a file system, database, software registry, API, schema, or implementation layer.

No artifact may be used institutionally unless it is registered or explicitly referenced through a governed Artifact Record. Physical existence, a repository path, a filename, or model output does not establish institutional authority.

## 1. Artifact Registry Philosophy

### 1.1 Institutional artifact

An artifact is a bounded, identifiable product of governed work created by an agent, human authority, workflow, or approved tool. It may represent a document, specification, implementation, dataset reference, experimental result, evidence package, report, decision, monitoring record, or failure record.

### 1.2 Artifact versus content

Content becomes an institutional artifact only after identity, owner, purpose, scope, provenance, version, status, consumers, dependencies, access, retention, and audit requirements are established.

### 1.3 Artifact versus authority

Artifacts carry the authority granted by their producing process and responsible agent. They do not create authority themselves. A report authored outside the appropriate decision right remains a report, not an approval.

### 1.4 Artifact versus domain object

An artifact may represent or reference evidence, knowledge, a decision, an implementation, or workflow output, but it does not collapse their separate governance. EES governs evidence, Knowledge OS governs knowledge, Decision OS governs decisions, and Agent Registry governs producer authority.

### 1.5 Registration before reliance

Institutional use begins only after registration validates artifact identity, type, ownership, status, version, provenance, scope, access, and permitted consumers. Draft circulation does not create authority.

### 1.6 Evolution without historical loss

Artifacts evolve through new versions and lifecycle events. Material mutation after use never overwrites history. Every decision remains tied to the exact artifact versions it consumed.

### 1.7 Reconstruction as a requirement

The institution must be able to reconstruct the artifact, its meaning, producing process, dependencies, reviewers, consumers, and historical state without relying on chat history, private model memory, or an original operator.

### 1.8 Artifact registry versus storage

ART governs institutional identity and meaning independently of where or how content is stored. Movement, replication, or format conversion cannot silently alter the Artifact Record.

## 2. Artifact Registry Principles

### 2.1 No Artifact Without Identity

Every institutional artifact has a stable Artifact ID and exact version.

### 2.2 No Artifact Without Owner

Every artifact has one accountable Owner Agent. Producing and owning agents may differ, but their roles remain explicit.

### 2.3 No Institutional Use Without Registration

Unregistered outputs may be inspected as untrusted candidates but cannot satisfy workflow gates, evidence requirements, validation, risk, or decisions.

### 2.4 No Silent Artifact Mutation

Material changes create new versions. Historical content and status remain recoverable.

### 2.5 Version Everything

Content, metadata, relationships, provenance, scope, validation, access, and lifecycle changes are versioned according to consequence.

### 2.6 Lineage Must Be Preserved

Every artifact links to exact inputs, transformations, producing workflow, predecessors, successors, and downstream products.

### 2.7 Provenance Must Be Explicit

Producer, process, source messages, evidence, memory, tools, human contributions, transformations, and creation context remain attached.

### 2.8 Consumers Must Be Traceable

Every consequential read, reference, validation, risk review, decision, deployment, and monitoring use identifies the consumer and exact version.

### 2.9 Artifacts Do Not Create Authority

Authority comes from registered agents, contracts, workflows, evidence admissibility, and decisions.

### 2.10 Code Is Not Strategy

Code is an implementation artifact. The approved Strategy Architecture Specification remains the authoritative strategy design.

### 2.11 Backtest Output Is Not Validation

Backtest artifacts are evidence inputs and cannot issue an independent validation verdict.

### 2.12 Report Is Not Decision Unless Authorized

A report becomes an authoritative decision record only when issued by the registered decision owner under the applicable contract.

### 2.13 Frozen Artifacts Cannot Be Edited In Place

Review freezes protect exact content and relationships. Additions and corrections create new versions.

### 2.14 Superseded Artifacts Remain Reconstructable

Supersession removes default current authority but preserves prior use, meaning, consumers, and lineage.

### 2.15 Retirement Does Not Erase History

Retired artifacts cannot support new work but remain attributable and auditable as policy permits.

### 2.16 Additional principles

- Scope, limitations, confidence, and status travel with the artifact.
- One current artifact version exists per declared scope unless a conflict is explicit.
- Copies and format conversions do not create independent evidence.
- Validation, risk, and decision states remain independently owned.
- Access restrictions cannot eliminate accountability.

## 3. Artifact Identity Model

### 3.1 Stable identity

Artifact ID represents continuity of one institutional product. Version identity represents one exact state of content, metadata, relationships, and governance.

### 3.2 Identity components

Identity distinguishes:

- institutional Artifact ID;
- Artifact Version;
- physical or logical representation identities;
- content integrity identity;
- producing workflow and agent identities;
- source and derived artifact relationships.

### 3.3 Artifact name

Artifact Name supports human recognition but is not identity. Renaming does not create a new Artifact ID unless institutional meaning changes.

### 3.4 Identity uniqueness

No two artifacts may claim the same Artifact ID. Duplicates, mirrors, exports, translations, and conversions are linked rather than silently re-registered as original work.

### 3.5 Composite artifacts

A package or report set may have a composite Artifact ID while preserving exact identities and versions of every component. Composite approval does not automatically approve each component for unrelated use.

### 3.6 Artifact branching

Parallel Draft candidates may branch from one version. Only one becomes current for the same scope unless explicit alternatives or conflict state justify coexistence.

### 3.7 Identity conflict

Ambiguous origin, duplicate identity, mismatched content, impersonated producer, or conflicting current version triggers quarantine and review.

## 4. Artifact Object Model

### 4.1 Definition

An Artifact Record is the governed institutional description of an artifact and its lifecycle. It references content without depending on storage location and controls how consumers interpret and use it.

### 4.2 Mandatory fields

| Field | Institutional requirement |
|---|---|
| Artifact ID | Stable identity across lifecycle and versions |
| Artifact Name | Controlled human-readable name |
| Artifact Type | Approved semantic type |
| Artifact Category | Research, knowledge, architecture, engineering, experiment, validation, risk, decision, deployment, monitoring, failure, governance, or other governed class |
| Current Status | Lifecycle and quality state |
| Owner Agent | Single accountable owner |
| Producing Agent | Registered agent or governed human/tool authority that produced it |
| Producing Workflow | Exact WOE workflow, stage, task, and versions |
| Source MACP Message | Message authorizing creation or current material state |
| Related SMI Memory Objects | Exact shared-state identities and versions |
| Related EES Evidence Packages | Exact evidence package identities, status, scope, and versions |
| Related Knowledge Objects | Knowledge OS identities and versions |
| Related Decision Objects | Decision identities, status, and versions |
| Related Agent Records | Agent Registry identities and versions |
| Related Workflow Objects | Related upstream and downstream workflows |
| Current Version | Authoritative artifact version and effective time |
| Previous Versions | Ordered immutable history |
| Lineage | Inputs, transformations, branches, merges, successors, and consumers |
| Provenance | Origin, producer, process, tools, human contributions, and custody |
| Purpose | Institutional reason for existence |
| Scope | Claims, markets, periods, versions, workflows, and permitted uses |
| Limitations | Known defects, uncertainty, restrictions, and unsupported uses |
| Consumers | Agents, workflows, decisions, and external governed users |
| Dependencies | Exact objects, versions, owners, and readiness requirements |
| Validation Status | Not reviewed, under review, qualified, approved, rejected, suspended, or expired with authority |
| Risk Status | Not applicable, pending, approved, limited, mitigation required, rejected, suspended, or expired |
| Decision Status | Advisory, pending, authorized, conditional, returned, rejected, suspended, or revoked |
| Freeze Status | Unfrozen, requested, frozen, challenged, released, or invalidated |
| Supersession Status | Current, partially superseded, fully superseded, or successor pending |
| Deprecation Status | Not deprecated, announced, restricted, migration active, or expired |
| Retirement Status | Not eligible, eligible, pending, retired, or exceptional retention |
| Access Classification | Readers, writers, sensitivity, purpose, and redistribution rules |
| Retention Policy | Duration, trigger, archive, legal, reproduction, and disposal obligations |
| Created At | Governed creation time and actor |
| Updated At | Latest material change time and actor |
| Audit Trail | Complete lifecycle, access, version, review, decision, and consumer history |

### 4.3 Additional properties

Records define integrity state, format representations, exact locations where relevant, review dates, expiry, correction policy, restoration conditions, conflict state, acknowledgements, security classification, and archival verification.

### 4.4 Field ownership

The Owner Agent governs artifact lifecycle and integration. Domain fields remain owned by competent agents: Engineering controls implementation conformance, Validation controls validation verdicts, Risk controls risk status, and Executive Decision controls executive decision state.

### 4.5 Reference versus copy

Artifact Records reference EES, SMI, knowledge, decisions, workflows, and agents by exact identity and version. Copying content does not transfer ownership or authority.

## 5. Artifact Lifecycle

### 5.1 Canonical states

Every artifact follows:

**Proposed → Registered → Draft → Active → Frozen → Under Review → Approved → Superseded → Deprecated → Retired → Archived**

Not every artifact must enter every state, but transitions remain explicit and governed.

### 5.2 Proposed

The artifact concept, owner, purpose, type, workflow, and preliminary scope exist. It cannot support institutional action.

### 5.3 Registered

Stable identity, record, owner, type, source message, producing workflow, access, lifecycle, and audit policy exist. Content may not yet be complete.

### 5.4 Draft

The artifact is being produced or revised. Consumers may review only under Draft restrictions and cannot treat it as current authority.

### 5.5 Active

The artifact is complete enough for declared non-gated institutional use within its status, scope, and limitations. Active does not imply validated, risk-approved, or decided.

### 5.6 Frozen

Exact content, metadata, relationships, and version are protected for experiment, evidence packaging, validation, risk review, decision, release, or audit.

### 5.7 Under Review

An authorized agent evaluates the frozen or controlled version. Producers may clarify but cannot silently alter the object under review.

### 5.8 Approved

The competent authority approves the artifact for a declared purpose and scope. Approval type, reviewer, conditions, expiry, and prohibited interpretations are explicit.

### 5.9 Superseded

An identified successor replaces the artifact for some or all current use. Historical consumers remain bound to the version they used.

### 5.10 Deprecated

New use is discouraged or prohibited according to policy while migration and existing obligations are completed.

### 5.11 Retired

New institutional use is prohibited. History, lineage, consumers, decisions, and retirement rationale remain preserved.

### 5.12 Archived

The artifact and complete governance history are retained for reproduction, audit, knowledge, legal, and institutional-memory purposes.

### 5.13 Transition controls

Every transition records source MACP message, actor, authority, prior and new state, version, evidence, conditions, consumers, dependencies, acknowledgements, and effective time.

## 6. Artifact Types

### 6.1 Market Research Report

Objective market intelligence, classifications, scope, uncertainty, and observations produced by Market Research. It is not strategy design.

### 6.2 Knowledge Acquisition Report

Sources, provenance, citations, reliability, coverage, contradictions, and gaps produced by Research Librarian.

### 6.3 Knowledge Curation Record

Knowledge acceptance, lifecycle, lineage, conflict, version, and retirement decision produced by Knowledge Curator.

### 6.4 Strategy Architecture Specification

Approved strategy hypothesis, mechanism, information needs, modules, failure conditions, and experiment proposals. It is the design authority, not executable code.

### 6.5 Strategy Hypothesis Document

Falsifiable observation, behavior, mechanism, expected persistence, alternatives, null, validation, and failure criteria.

### 6.6 Strategy Engineering Specification

Requirements, interfaces, timing, data, state, deterministic, testing, and reproducibility contracts for faithful implementation.

### 6.7 Python Implementation Artifact

Versioned implementation and related manifests. It cannot redefine approved strategy architecture.

### 6.8 Pine Script Artifact

Versioned Pine implementation, compatibility, limitations, and parity context. It is not scientific validation.

### 6.9 Experiment Plan

Approved variables, controls, baselines, metrics, stopping, resources, dependencies, and replication plan.

### 6.10 Experiment Run Output

Run-specific outputs linked to exact experiment, implementation, data, configuration, environment, and terminal state.

### 6.11 Backtest Result Artifact

Historical simulation results with assumptions, costs, timing, data, selection, and limitations. It is not proof of edge.

### 6.12 Walk-Forward Result Artifact

Fold boundaries, selection, parameter freezing, outer-test status, distributions, degradation, and failures.

### 6.13 Monte Carlo Result Artifact

Uncertainty model, resampling, perturbations, dependence, distributions, tails, and limitations.

### 6.14 Parameter Stability Report

Neighborhoods, robust regions, interactions, boundaries, sensitivity, and cross-window stability.

### 6.15 Negative Control Report

Control design, destroyed mechanism, expected behavior, results, anomalies, and interpretation.

### 6.16 Adversarial Test Report

Stress assumptions, scenarios, execution degradation, dependency failures, results, and scope.

### 6.17 Evidence Package

EES-governed collection of exact evidence objects with provenance, scope, limitations, contradictions, custody, and admissibility.

### 6.18 Validation Report

Independent Validation Agent assessment and authorized verdict. Engineering cannot alter it.

### 6.19 Risk Review Report

Risk Governance assessment, capital limits, controls, residual risk, kill policy, and authorized risk decision. It cannot rewrite validation evidence.

### 6.20 Executive Decision Record

Authorized institutional decision with inputs, alternatives, conditions, accountability, expiry, and audit trail.

### 6.21 Deployment Candidate Record

Exact candidate versions, approvals, limits, readiness, monitoring, rollback, and handoff. It is not deployment execution.

### 6.22 Monitoring Report

Time-indexed production state, exposures, execution, model, data, controls, limits, anomalies, and escalations.

### 6.23 Edge Decay Report

Evidence about changing expectancy, stability, regime distribution, signal behavior, execution, and confidence. It cannot silently disable governance.

### 6.24 Failure Review Report

Failure evidence, timeline, state, decisions, causes, consequences, lessons, actions, and closure.

### 6.25 Conflict Resolution Record

Competing objects, claims, versions, authorities, evidence, resolution, rejected alternatives, and residual dissent.

### 6.26 Emergency Suspension Record

Trigger, authority, containment, affected artifacts and workflows, evidence, safe state, review, and reactivation conditions.

## 7. Artifact Ownership

### 7.1 Accountable owner

Every artifact has one Owner Agent responsible for record completeness, lifecycle, consumers, dependency impact, access, retention, and archival.

### 7.2 Producing agent

The Producing Agent creates content within its registered contract and WOE assignment. It may differ from the lifecycle owner or reviewing authority.

### 7.3 Domain authority

Ownership does not permit changing fields controlled by another authority. A workflow owner cannot edit evidence; Engineering cannot edit Validation; Risk cannot rewrite evidence; Executive cannot edit specialist verdicts.

### 7.4 Shared contribution

Contributors are attributed by exact role and version. Collective authorship cannot hide responsibility for material sections or decisions.

### 7.5 Ownership transfer

Transfer identifies old and new owner, reason, effective time, open tasks, versions, consumers, permissions, locks, incidents, and acknowledgements.

### 7.6 Owner absence

Ownerless artifacts cannot remain Active or Approved. Governance restricts use and assigns stewardship or retires the artifact.

## 8. Artifact Versioning and Lineage

### 8.1 Version rule

Material changes to content, meaning, scope, assumptions, relationships, dependencies, status, validation, risk, decision, or access create a new Artifact Version.

### 8.2 Change classes

- editorial;
- metadata correction;
- clarifying;
- content extension;
- dependency or relationship;
- scope or limitation;
- evidence or result;
- validation, risk, or decision status;
- breaking semantic;
- lifecycle transition.

### 8.3 Lineage chain

Lineage records:

**Source MACP message → producing workflow and task → agents and tools → inputs and evidence → transformations → artifact versions → reviews and decisions → consumers → successors → archive and retirement**

### 8.4 Branch and merge

Branches preserve parent versions and purpose. Merge creates a new version and records retained, rejected, conflicting, and transformed content.

### 8.5 Rollback

Rollback creates a new version restoring an earlier approved condition. It never deletes intervening history.

### 8.6 Format conversion

Conversion records source, target representation, transformation, fidelity, losses, verifier, and whether institutional meaning remains equivalent.

### 8.7 Consumer impact

Material version changes identify every dependent workflow, evidence package, validation, risk review, decision, deployment, monitoring process, and knowledge object.

## 9. Artifact Provenance Requirements

### 9.1 Provenance chain

Every artifact identifies initiator, source message, producing agent and Agent Record, WOE workflow and task, inputs, SMI state, EES packages, knowledge, decisions, tools, human contributions, transformations, and custody.

### 9.2 Content provenance

Sections, results, datasets, code, tables, summaries, and decisions retain source attribution at the granularity needed to prevent false authorship or authority.

### 9.3 Tool provenance

Governed tools are identified by role and output. Tool generation does not establish agent authority or evidence validity.

### 9.4 External provenance

External artifacts state source, creator, version, license, access, authenticity, retrieval time, and institutional intake authority.

### 9.5 Provenance gaps

Missing or disputed provenance is explicit, lowers quality and admissibility, and may block registration, activation, freeze, approval, or use.

### 9.6 Correction

Corrected provenance creates a new version and traces affected evidence, decisions, consumers, and review requirements.

## 10. Artifact Relationship Model

### 10.1 Relationship types

- produced by;
- derived from;
- depends on;
- references;
- implements;
- tests;
- validates;
- risk-assesses;
- decides on;
- monitors;
- contradicts;
- corrects;
- extends;
- supersedes;
- replaces;
- invalidates;
- used by;
- archived with;
- retired by.

### 10.2 Relationship fields

Every relationship defines source and target IDs and versions, direction, purpose, authority, scope, confidence, effective time, expiry, and audit event.

### 10.3 Semantic integrity

Relationships cannot imply authority they do not possess. `implements` does not mean `is`; `tests` does not mean `validates`; `references` does not mean `approves`.

### 10.4 Circular relationships

Cycles are reviewed for hidden self-validation, circular evidence, recursive authority, or unresolved dependency.

### 10.5 Broken relationship

Unavailable, retired, invalidated, or incompatible dependencies trigger consumer impact and may restrict current status.

## 11. Artifact Consumer and Dependency Rules

### 11.1 Consumer registration

Consequential consumers identify agent, workflow, purpose, exact version, access, acknowledgement, decision use, and retention obligation.

### 11.2 Consumer duty

Before use, consumers verify status, scope, limitations, version, provenance, validation, risk, decision, freeze, supersession, deprecation, access, and expiry.

### 11.3 Dependency record

Dependencies identify exact object, version, owner, status, compatibility, freshness, availability, failure effect, and replacement policy.

### 11.4 No floating critical dependencies

Critical evidence, implementation, validation, risk, and decision dependencies use exact versions. Current aliases do not establish historical reconstruction.

### 11.5 Dependency change

Material change triggers impact classification: no impact, acknowledgement, update, revalidation, risk review, decision review, suspension, supersession, or retirement.

### 11.6 Consumer traceability

Every artifact used in a decision, deployment, validation, risk review, or monitoring gate remains traceable to consumer and exact version.

## 12. Artifact Freeze and Release Rules

### 12.1 Freeze purpose

Freeze establishes an immutable artifact version for evidence packaging, experiment execution, validation, risk review, executive decision, deployment candidate, audit, or release.

### 12.2 Freeze record

Defines Freeze ID, artifact and version, purpose, authority, custodian, readers, start, expiry, prohibited changes, permitted annotations, integrity, consumers, related SMI lock, and release criteria.

### 12.3 Frozen state

Frozen content, metadata, lineage, relationships, and referenced versions cannot be edited or substituted. New information creates linked artifacts or a new version.

### 12.4 Challenge during freeze

Challenges remain separate and visible. Competent governance may continue, suspend, or restart review with a new frozen version.

### 12.5 Release

Release records outcome, integrity, review, decisions, consumers, new versions, retained locks, and archival requirements.

### 12.6 Freeze violation

Unauthorized mutation invalidates the freeze, quarantines downstream use, and triggers impact review and audit.

## 13. Artifact Validation and Quality Status

### 13.1 Quality dimensions

Quality includes identity, completeness, provenance, correctness, conformance, scope, clarity, reproducibility, internal consistency, dependency validity, access, and auditability.

### 13.2 Quality states

- unassessed;
- candidate;
- structurally complete;
- technically verified;
- scientifically validated where applicable;
- qualified with limitations;
- failed review;
- challenged;
- invalidated;
- expired.

### 13.3 Validation ownership

Artifact quality review does not replace scientific validation. Only Validation Agent controls the Validation Report verdict and related fields.

### 13.4 Code quality versus research validity

A code artifact may be correct and reproducible while the strategy fails scientifically. These states remain separate.

### 13.5 Report quality versus authority

A clear, complete report remains advisory unless issued by an agent with decision rights under the proper workflow.

### 13.6 Re-review triggers

Material change to content, dependencies, evidence, scope, implementation, market context, standards, or producing-agent status may reopen review.

## 14. Artifact Supersession, Deprecation, and Retirement

### 14.1 Supersession

Supersession identifies successor, replaced scope, compatibility, effective date, migration, consumers, and whether the predecessor remains valid for historical or bounded use.

### 14.2 Partial supersession

If only some scope or fields are replaced, the record states which authority remains current. Ambiguous partial supersession blocks new use.

### 14.3 Deprecation

Deprecation announces end of preferred use and defines prohibited new work, permitted existing use, migration owner, deadline, warnings, and successor.

### 14.4 Retirement

Retirement prohibits new institutional use. Preconditions include consumer migration, dependency resolution, active workflow closure, decision impact, access revocation, retention, and archival.

### 14.5 Reactivation

Retired artifacts cannot return to Active by status change alone. Governance requires a new version or artifact identity, current provenance, dependencies, review, and authorization.

### 14.6 No masquerading

Superseded, deprecated, retired, invalidated, or expired artifacts must display status at every consequential read and cannot be presented as current.

## 15. Artifact Archival and Reconstruction

### 15.1 Archival package

Archive includes Artifact Record versions, content identities, representations, provenance, lineage, relationships, inputs, evidence, memory, workflows, agents, reviews, decisions, consumers, access, retention, and audit trail.

### 15.2 Reconstruction standard

Authorized reviewers can determine what the artifact contained, how it was produced, which versions it used, who approved it, where it was consumed, and why it changed or retired.

### 15.3 Historical environment

Where reproduction depends on data, implementation, environment, configuration, or external material, the archive retains governed references and known reconstruction limitations.

### 15.4 Archive integrity

Archival verification confirms completeness, identity, relationships, accessibility, retention, and migration readiness.

### 15.5 Restoration

Restoration creates a new governed lifecycle event and, when active use is intended, a new reviewed version. Historical archives remain unchanged.

### 15.6 Disposal

Physical disposal, if required, is separately authorized and audited. It cannot erase permitted proof of artifact identity, decisions, or governance history.

## 16. Registry Auditability

### 16.1 Audit objective

Authorized reviewers can reconstruct artifact existence, versions, ownership, provenance, lineage, use, freeze, reviews, decisions, access, supersession, retirement, and archive state.

### 16.2 Mandatory events

Proposal, registration, draft, activation, freeze, review, approval, rejection, version, branch, merge, conversion, relationship, access, consumer use, challenge, correction, supersession, deprecation, retirement, archival, restoration, exception, and audit finding are recorded.

### 16.3 Audit fields

Each event records Artifact ID and version, actor and Agent Record, authority, MACP message, workflow and task, SMI state, EES references, prior and resulting state, reason, evidence, consumers, time, and review.

### 16.4 Immutable history

Audit history is append-only in institutional meaning. Correction does not remove the inaccurate record.

### 16.5 Independent review

Owners cannot independently close material findings about unauthorized mutation, false provenance, hidden consumer use, freeze violation, or decision-record corruption.

### 16.6 Audit failure

Artifacts that cannot be reconstructed are restricted or quarantined and cannot support consequential new work.

## 17. Integration with MACP

### 17.1 Relationship

MACP governs artifact creation requests, transfers, acknowledgements, reviews, decisions, errors, conflicts, freezes, lifecycle events, and archival notices.

### 17.2 Source message

Every Artifact Record creation and material transition cites an exact MACP message. Informal transmission does not establish institutional use.

### 17.3 Transfer

Artifact transfer identifies ID, version, status, scope, limitations, provenance, access, intended use, consumer, integrity, and acknowledgement.

### 17.4 Message rights

Agent Registry rights determine who may issue artifact-related messages and authority-bearing approvals.

### 17.5 State alignment

MACP message lifecycle and Artifact Record status must agree. Conflict blocks consequential use.

### 17.6 Idempotency

Duplicate delivery cannot duplicate registration, freeze, approval, supersession, retirement, or consumer action.

## 18. Integration with SMI

### 18.1 Relationship

SMI preserves Artifact References and current shared state; ART governs artifact semantics and lifecycle.

### 18.2 Artifact Reference

SMI records Artifact ID, exact version, status, owner, readers, writers, source message, consumers, dependencies, freeze, expiry, retirement, and audit references.

### 18.3 Controlled writes

Only registered field owners may update Artifact Records through governed MACP and SMI version events.

### 18.4 Locks

Frozen artifact reviews use SMI locks. Lock ownership does not permit content mutation or review approval.

### 18.5 Consistency

ART and SMI states must reconcile before use. Conflicting status, version, owner, access, or freeze creates a blocking error.

### 18.6 Impact propagation

Artifact change triggers SMI dependency analysis and MACP notification to registered consumers.

## 19. Integration with EES

### 19.1 Relationship

Evidence Packages and evidence-bearing artifacts are registered in ART while their evidentiary meaning, provenance, scope, custody, admissibility, contradiction, and freeze are governed by EES.

### 19.2 Evidence distinction

Not every artifact is evidence. An artifact becomes evidentiary only through an EES relationship to a defined claim and declared use.

### 19.3 Frozen alignment

Artifact Freeze and EES Evidence Freeze must identify the same exact versions when the artifact forms part of a validation package.

### 19.4 Amendment and invalidation

EES challenge, amendment, or invalidation triggers Artifact Record version and consumer impact review without overwriting historical content.

### 19.5 Backtest rule

Backtest and optimization artifacts are evidence inputs, never standalone proof of edge or validation.

### 19.6 Evidence lineage

Artifact lineage preserves all Evidence IDs, packages, claims, limitations, and custody relevant to its content.

## 20. Integration with WOE

### 20.1 Relationship

WOE defines when artifacts are required, produced, reviewed, frozen, accepted, returned, approved, rejected, consumed, and archived.

### 20.2 Producing workflow

Every institutional artifact cites the exact Workflow ID, stage, task, owner, inputs, outputs, and lifecycle state that produced it.

### 20.3 Stage gates

WOE gates verify registration, exact version, status, owner, provenance, scope, dependencies, validation, risk, decision, freeze, access, and consumer acknowledgement.

### 20.4 Returned work

Returned artifacts preserve failed criteria and versions. Correction produces a new Draft version and review path.

### 20.5 Failure and cancellation

Partial and failed artifacts remain registered and classified; cancellation does not erase them.

### 20.6 Archival

Workflow archival requires output reconciliation and Artifact Registry closure for all mandatory deliverables.

## 21. Integration with Agent Registry

### 21.1 Relationship

Agent Registry determines which agents may produce, own, review, approve, transfer, consume, freeze, supersede, retire, or audit each artifact type.

### 21.2 Producer validation

Before registration, ART validates the Producing Agent's status, contract, evidence rights, workflow role, message rights, security, and artifact-type permission.

### 21.3 Owner validation

Owners must be Active or explicitly Restricted with artifact-lifecycle rights. Suspended agents cannot issue authority-bearing artifact changes.

### 21.4 Status change

Agent restriction, suspension, deprecation, or retirement triggers artifact ownership, custody, consumer, access, and pending-review impact analysis.

### 21.5 Delegation

Delegated artifact actions remain within Agent Registry rights and identify delegator, delegate, scope, fields, duration, and accountability.

### 21.6 Historical attribution

Archives preserve the exact Agent Record and Contract versions active when each artifact action occurred.

## 22. Governance

### 22.1 Constitutional scope

Every future AI Quant Lab artifact must be registered under ART before institutional workflow, evidence packaging, validation, risk review, executive decision, deployment, or monitoring use.

### 22.2 Governance ownership

- Artifact Governance owns identity, type contracts, lifecycle, version, ownership, relationship, and archival rules.
- Agent Registry controls producer and owner eligibility.
- WOE controls producing and consuming workflows.
- MACP controls artifact communication.
- SMI controls shared artifact-reference state and locks.
- EES controls evidence meaning and custody.
- Knowledge Curator controls knowledge relationships.
- Validation, Risk, and Executive agents own their respective status fields and records.
- QA independently audits conformance.
- Founder authority approves constitutional change and reserved exceptions.

### 22.3 Type conformance

Every artifact type defines required content, producer, owner, workflow, provenance, evidence, consumers, reviews, states, access, retention, and retirement before Active use.

### 22.4 Mandatory rules

- An artifact may not be used institutionally without registration.
- An artifact may not be treated as authoritative outside its declared scope.
- An artifact may not be silently edited after institutional use.
- A new material version must preserve lineage to prior versions.
- A code artifact is not the strategy itself.
- A backtest artifact is not proof of edge.
- A Validation Report cannot be altered by Engineering.
- A Risk Review Report cannot rewrite validation evidence.
- An Executive Decision Record must cite admissible inputs.
- Frozen artifacts cannot be edited in place.
- Superseded artifacts cannot masquerade as current.
- Deprecated artifacts cannot be used for new work unless explicitly allowed.
- Retired artifacts cannot be reactivated without governance.
- Every artifact consumer must be traceable.
- Every artifact used in a decision must be reconstructable.

### 22.5 Violations

Violations include unregistered use, missing owner, false type, unauthorized producer, hidden mutation, lost lineage, false provenance, untracked consumer, scope breach, freeze violation, status impersonation, stale use, or historical deletion.

Material violation triggers quarantine, access restriction, affected-workflow and decision tracing, notification, review suspension, correction or invalidation, independent audit, and institutional learning.

### 22.6 Exceptions

An exception defines rule, artifact and version, purpose, scope, owner, producer, consumers, risk, evidence, limitations, controls, authority, duration, expiry, monitoring, audit, and return to conformance. It cannot authorize silent mutation, fabricated provenance, false authority, or erased history.

### 22.7 Standard evolution

Every ART amendment defines problem, evidence, semantic change, alternatives, affected types and agents, compatibility, migration, historical reconstruction, MACP/SMI/EES/WOE/AR impact, security, audit, effective date, deprecation, rollback, and approval.

### 22.8 Periodic review

Governance asks:

- Is every institutionally used artifact registered and owned?
- Are producer and owner rights valid under Agent Registry?
- Are versions, provenance, lineage, scope, and consumers complete?
- Are code, backtests, reports, evidence, and decisions kept distinct?
- Are frozen artifacts immutable?
- Are superseded and deprecated artifacts prevented from masquerading as current?
- Can every decision reconstruct its input artifacts?
- Are failures, contradictions, and cancelled outputs retained?
- Do MACP, SMI, EES, WOE, and AR states reconcile?
- Are exceptions becoming hidden artifact policy?

### 22.9 Registry retirement

An Artifact Registry version may be retired only after artifact types and consumers migrate, active records remain interpretable, historical decisions remain reconstructable, and no institutional process relies on unsupported semantics.

### 22.10 Permanent rules

- No institutional artifact exists without identity, owner, type, version, provenance, lineage, scope, consumers, status, retention, and audit trail.
- No storage location or file name creates authority.
- No artifact changes the authority of its producer.
- No frozen, historical, superseded, deprecated, or retired state is silently rewritten.
- Every consequential artifact relationship and use remains explainable, traceable, versioned, reviewable, and reconstructable.

ART governs institutional artifacts without replacing the agents and standards that create research, evidence, implementations, validation, risk decisions, executive decisions, deployments, and knowledge.
