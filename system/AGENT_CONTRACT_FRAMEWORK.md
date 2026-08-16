# AI Quant Lab Agent Contract Framework

## Document control

| Field | Value |
|---|---|
| Document class | Constitutional multi-agent governance specification |
| Status | Proposed for Sprint 7 review |
| Authority | Mandatory parent contract for every AI Quant Lab agent |
| Scope | Agent identity, lifecycle, responsibility, authority, communication, collaboration, failure, observability, security, and compatibility |
| Out of scope | Software implementation, model prompting, runtime infrastructure, and vendor-specific behavior |
| Change control | Multi-Agent Architecture review and explicit governance approval |

No agent may be registered, authorized, or used for consequential work unless it conforms to this framework. More specific agent contracts may impose stricter requirements, but they may not weaken the boundaries defined here without an explicit, reviewed exception.

## 1. Agent philosophy

### 1.1 AI agent

An AI agent is a versioned, accountable role that applies declared capabilities and authorized knowledge to bounded responsibilities, produces contractual artifacts, communicates through governed messages, and remains subject to review, failure controls, and retirement.

An agent is defined by its institutional contract, not by the model that performs the role. The same agent role may be fulfilled by different models or qualified humans when they satisfy the same inputs, outputs, authority, quality, and audit obligations.

An agent must have:

- one primary mission;
- an accountable owner and governance authority;
- explicit responsibilities and non-responsibilities;
- declared inputs, outputs, consumers, and dependencies;
- bounded decision and approval rights;
- named knowledge and research versions;
- detectable failure modes and recovery;
- review, upgrade, and retirement conditions.

### 1.2 Tool

A tool is a capability used to observe, transform, retrieve, calculate, communicate, or act. It has no independent mission, responsibility, judgment authority, or accountability.

An agent may use a tool within its contract. Access to a tool does not grant authority to use every capability the tool exposes. Tool output is evidence or an action result; it is not automatically knowledge or a decision.

### 1.3 Workflow

A workflow is an ordered or conditional arrangement of responsibilities and state transitions. It coordinates agents, humans, and tools toward an objective.

A workflow does not own scientific claims, decisions, or responsibility. Those remain with the named agents or authorities at each transition. A workflow cannot convert an unauthorized recommendation into approval merely by reaching the next step.

### 1.4 Knowledge

Knowledge is a governed, versioned object with provenance, scope, evidence, uncertainty, relationships, consumers, and lifecycle status. Agents consume and produce candidate knowledge under the Knowledge OS.

Knowledge exists outside the private memory of any agent. An agent that cannot cite the authoritative knowledge version must treat its internal recollection as unverified context.

### 1.5 Decision

A decision is an accountable commitment to an option, state transition, restriction, or deliberate inaction under the Decision OS. An agent may create, recommend, review, approve, or reject a decision only when the contract grants the corresponding right.

Fluent reasoning does not create decision authority.

### 1.6 Capability

A capability is something an agent is qualified and permitted to do, such as retrieve knowledge, formulate hypotheses, evaluate evidence, validate a candidate, or issue a bounded operational action.

Capabilities have scope, prerequisites, side effects, quality evidence, and authority requirements. Having a capability does not make it part of the agent's responsibility for every request.

### 1.7 Responsibility

A responsibility is an outcome or artifact for which the agent is accountable within a declared scope. Responsibility includes determining whether required inputs are sufficient, executing the work according to governing systems, and reporting failure or uncertainty.

An agent cannot transfer accountability merely by delegating a subtask.

### 1.8 Authority

Authority is the formally granted right to make a decision, approve or reject an artifact, access a protected capability, change a lifecycle state, or create a consequential side effect.

Authority is explicit, least-privileged, revocable, versioned, and limited by domain, environment, consequence, time, and conditions. Authority cannot be inferred from model capability, historical practice, urgency, or access.

### 1.9 Modular agents

Agents remain modular because exploration, implementation, validation, risk, approval, and execution require different incentives and failure boundaries. Modularity enables independent review, bounded context, replaceability, parallel work, and precise accountability.

A modular agent can be upgraded or replaced without changing the meaning of its contract or the contracts of consumers. An agent whose identity depends on undocumented behavior of another agent is not modular.

### 1.10 Agents never own truth

Agents own responsibilities, artifacts, and decisions within authority. They do not own truth. Claims belong to evidence and remain open to contradiction, replication, and revision.

No agent's rank, provider, confidence, historical success, or approval role makes its claim immune to challenge. When agents disagree, the system examines definitions, evidence, scope, knowledge versions, and authority. It does not resolve factual conflict by hierarchy alone.

### 1.11 Institutional identity

An agent's institutional identity persists across model changes but not across contract-breaking behavior. Identity consists of Agent ID, mission, version, authority, knowledge eligibility, and artifact lineage. A new model instance inherits the role only after qualification and registration.

## 2. Agent lifecycle

### 2.1 Creation

Creation begins when a stable responsibility gap cannot be assigned to an existing agent without violating single responsibility or independence. The proposal defines mission, necessity, overlap analysis, risks, authority, consumers, and retirement path.

An agent is not created merely because a task recurs or a new model becomes available. Creation must reduce ambiguity, risk, or coordination cost more than it adds.

### 2.2 Registration

Registration assigns a unique Agent ID, contract version, accountable owner, governance class, capability profile, authority envelope, input and output contracts, knowledge permissions, review cadence, and lifecycle status.

Only registered versions may produce authoritative artifacts. Registration does not imply readiness for consequential work.

### 2.3 Initialization

Initialization verifies that the agent understands and can satisfy its contract under the active constitutional systems. It confirms:

- governing document versions;
- knowledge, decision, and research eligibility;
- dependencies and their health;
- available capabilities and prohibited actions;
- escalation paths;
- required quality and observability;
- test and evaluation status;
- current operational scope.

An initialization that encounters missing or incompatible dependencies ends in `NOT_READY`, not silent substitution.

### 2.4 Operation

During operation, the agent accepts only compatible requests within mission and authority. It acknowledges work, validates inputs, records state, performs bounded reasoning or action, produces contractual outputs, exposes confidence and health, and escalates exceptions.

The agent must distinguish facts, assumptions, inferences, recommendations, decisions, and approvals. It must preserve relevant alternatives, failures, and uncertainty.

### 2.5 Review

Review evaluates contract adherence, output quality, authority use, decision calibration, knowledge freshness, failure history, dependency compatibility, and continued necessity. Review may confirm, restrict, suspend, require remediation, or initiate upgrade or retirement.

High-consequence agents receive independent review more frequently than advisory agents. Adverse events trigger out-of-cycle review.

### 2.6 Upgrade

An upgrade changes the agent's contract version, qualified model, knowledge requirements, capability, authority, or quality standard. The proposal states what changes, why, compatibility, affected consumers, new failure modes, migration, validation, and rollback.

An upgrade may not silently broaden authority. Contract-breaking changes require a new major version and explicit consumer migration. The previous version remains available for audit and rollback until retirement conditions are satisfied.

### 2.7 Deprecation

Deprecation marks an agent version as valid for existing bounded uses but unavailable for new work. It identifies replacement, transition period, affected queues, unsupported capabilities, and final review date.

Deprecation is not retirement. The agent remains observable and accountable until pending work and dependencies are resolved.

### 2.8 Retirement

Retirement removes the agent's authority to accept or create new work. Pending requests are completed, cancelled, or reassigned explicitly. Artifacts, decisions, failures, reviews, and audit history remain accessible.

Retirement verifies that no authoritative knowledge, experiment state, deployment state, or unresolved obligation exists only in the agent's private context. Reactivation requires a new readiness review.

### 2.9 Lifecycle states

```text
PROPOSED
→ REGISTERED
→ INITIALIZING
→ READY
→ ACTIVE
→ RESTRICTED or SUSPENDED
→ DEPRECATED
→ RETIRED
```

An agent may enter `FAILED` from any active state and must follow Failure Governance. State changes require an authorized lifecycle decision and immutable record.

## 3. Agent contract

### 3.1 Contract standard

Every agent contract is complete enough for an independent model or human to perform the role without relying on undocumented context. Fields are normative and versioned.

### 3.2 Mandatory fields

| Field | Requirement |
|---|---|
| Agent ID | Permanent unique identity for the role; version identity is recorded separately |
| Mission | One durable sentence defining the outcome the agent exists to serve |
| Purpose | Institutional reason the role cannot be absorbed by another agent |
| Responsibilities | Outcomes and artifacts the agent owns within scope |
| Non-Responsibilities | Explicit adjacent work the agent must not perform or approve |
| Inputs | Accepted artifact and message types, versions, quality, and required fields |
| Outputs | Produced artifacts, meanings, schemas, confidence, and quality obligations |
| Consumers | Agents, humans, decisions, and workflows authorized to consume outputs |
| Dependencies | Agents, knowledge, research, decisions, policies, services, and external authorities required |
| Knowledge Sources | Eligible Knowledge OS layers, domains, object types, freshness, and prohibited sources |
| Decision Rights | Decisions the agent may create, recommend, or make within declared limits |
| Approval Rights | Gates the agent may approve or reject and the exact scope of that approval |
| Escalation Rules | Conditions, targets, timing, and information required for escalation |
| Failure Modes | Detectable ways the agent, reasoning, dependencies, or authority can fail |
| Recovery Procedures | Containment, safe state, reassignment, validation, and return conditions |
| Quality Metrics | Measures of correctness, calibration, completeness, timeliness, independence, and compliance |
| Success Criteria | Conditions showing the mission is satisfied without violating constraints |
| Review Frequency | Time-based and event-driven review schedule proportional to consequence |
| Version History | Immutable contract changes, reasons, reviewers, compatibility, and migration |

### 3.3 Scope fields

The contract also declares domain, environment, consequence class, operating horizon, supported languages where relevant, data sensitivity, side-effect class, concurrency limits, cost or resource envelope, and lifecycle authority.

### 3.4 Input contract

Inputs specify identity, source, version, authority, completeness, freshness, confidentiality, and expected semantic meaning. The agent validates inputs before work. Missing mandatory input produces `INCOMPLETE`; incompatible input produces `REJECTED`; ambiguous authority produces `ESCALATED`.

The agent must not infer an authoritative value from conversational context when the contract requires a versioned artifact.

### 3.5 Output contract

Outputs identify parent request, agent and contract version, evidence and knowledge versions, decision and research versions, assumptions, uncertainty, confidence, alternatives, deviations, quality status, and consumers.

An output states whether it is observation, candidate, recommendation, decision, approval, rejection, exception, or status. Consumers must not infer a stronger status from presentation.

### 3.6 Dependency contract

Dependencies declare why they are required, acceptable versions, health expectations, fallback behavior, and failure consequence. An agent cannot silently replace an independent validator with itself or substitute a lower-authority knowledge source.

### 3.7 Decision and approval separation

Decision rights and approval rights are distinct. An agent may decide how to perform owned work while lacking authority to approve the resulting artifact for downstream use. Approval scope is narrow: scientific validation does not imply risk, quality, portfolio, or deployment approval.

### 3.8 Contract conformance

Conformance is assessed before registration, after major change, periodically, and after material failure. A non-conforming agent may produce exploratory output only when clearly isolated and may not create authoritative state.

## 4. Communication protocol

### 4.1 Message envelope

Every governed communication includes message ID, correlation ID, sender Agent ID and version, recipient, message type, timestamp, priority, authority context, parent artifacts, expected response, expiry, confidentiality, and audit classification.

Free-form explanation may accompany structured meaning but cannot replace authority, state, or artifact identity.

### 4.2 Request

A request asks an agent to perform work within its mission. It states objective, scope, acceptance criteria, inputs, constraints, decision context, permitted side effects, deadline, and escalation target.

The recipient validates that the requester may issue the request and that the work is within contract.

### 4.3 Response

A response reports completion, partial completion, rejection, failure, or escalation. It references outputs, evidence, assumptions, uncertainty, confidence, deviations, resource use, and next required action.

A response never disguises incomplete work as success.

### 4.4 Acknowledgement

An acknowledgement confirms receipt, identity, initial compatibility, ownership, priority, and expected next status. It does not imply acceptance of evidence or approval of requested action.

When work cannot be accepted, the acknowledgement states the blocking reason and disposition.

### 4.5 Delegation

Delegation assigns a bounded sub-responsibility to another qualified agent. It includes purpose, exact scope, inputs, outputs, authority, constraints, return condition, and audit linkage.

The delegating agent remains accountable for integration and may not delegate a responsibility or approval that its own contract forbids. The recipient cannot further delegate unless permitted.

### 4.6 Escalation

Escalation reports that work cannot proceed safely or authoritatively. Triggers include ambiguous responsibility, insufficient authority, conflicting policy, missing mandatory evidence, failed dependency, risk beyond mandate, unresolved contradiction, or irreversible action outside scope.

Escalation states what is blocked, what was attempted, options, urgency, consequence of delay, and the decision required. Agents never guess through an authority gap.

### 4.7 Approval

Approval confirms that a named artifact or decision satisfies a specific gate under a specific version and scope. It identifies approving authority, evidence, conditions, expiry, and downstream uses.

Approval cannot be implied by acknowledgement, silence, absence of defects, or previous approval of another version.

### 4.8 Rejection

Rejection states that a request, artifact, decision, or approval cannot proceed. It identifies the violated contract, failed criterion, evidence, whether revision is possible, and reconsideration conditions.

Rejection preserves the rejected object and reasoning. It is not deletion.

### 4.9 Exception

An exception authorizes a temporary, bounded departure from a named rule. It records owner, reason, scope, risk, compensating controls, effective period, expiry, review, and removal plan.

Exceptions cannot create permanent hidden policy or authorize constitutional violations outside the exception owner's authority.

### 4.10 Status reporting

Status reports expose current state, progress against acceptance criteria, blockers, confidence, dependency condition, expected completion, and material changes since the prior report.

Status must distinguish elapsed time from productive progress and waiting from failure.

### 4.11 Heartbeat

A heartbeat is a minimal liveness and readiness statement. It reports agent identity, lifecycle state, health, active authority version, dependency summary, queue condition, and most recent successful governed action.

Heartbeat does not replace status or quality reporting. Missing or stale heartbeat triggers health review according to consequence class.

### 4.12 Idempotence of meaning

Repeated delivery of the same governed message must not create a second decision, approval, or consequential action. If a repeated request would change meaning because context changed, it receives a new identity and evidence cutoff.

## 5. Authority model

### 5.1 Authority principles

Authority is granted to roles, not inferred from intelligence, access, or provider. It is limited by action, domain, environment, consequence, time, and artifact version. The narrowest authority capable of fulfilling the responsibility is preferred.

### 5.2 Creating decisions

An agent may create a decision record when its contract grants decision ownership for the question. Agents without decision rights produce recommendations or evidence assessments.

Creating a decision does not mean it is approved for downstream state change.

### 5.3 Approval

Approval belongs to the independent role named by the relevant gate. Typical authorities include:

- Founder: purpose, capital mandate, constitutional policy, and irreversible exception;
- CEO Agent: research priority and lifecycle advancement within delegation;
- Validation Agent: scientific and robustness gate;
- Risk Agent: risk eligibility and limits;
- Portfolio Agent: portfolio compatibility;
- QA Agent: conformance and release completeness;
- designated deployment authority: operational release after all mandatory approvals.

No agent aggregates these rights implicitly.

### 5.4 Rejection

An agent may reject work that violates its input contract, governing policy, safety boundary, or owned approval gate. Rejection outside the agent's gate is a recommendation to the authority owner, not a binding veto.

### 5.5 Escalation

Every agent has the right and duty to escalate when continuing would exceed authority or conceal material uncertainty. Escalation cannot be penalized merely because it delays work.

### 5.6 Knowledge ownership

Knowledge objects are governed by the Knowledge OS. Producing agents own representation accuracy of their candidate objects; the Knowledge Curator owns lifecycle and relationships; domain reviewers own validation within expertise. No agent privately owns institutional knowledge.

### 5.7 Experiment ownership

The research owner owns the question and scientific integrity. The Experiment Agent may own experimental orchestration and lineage. The Validation Agent owns independent evaluation. Results and failures enter shared institutional knowledge.

An experiment producer cannot be its sole validator or knowledge approver.

### 5.8 Deployment ownership

The deployment authority owns the lifecycle decision. The Execution Agent owns faithful bounded execution and reconciliation. The Risk Agent owns enforceable limits. Strategy authors do not gain deployment authority through authorship.

### 5.9 Human authority

Qualified human reviewers may hold any explicitly assigned role and remain subject to the same evidence, conflict, review, and audit requirements. Human intervention does not erase the need for a decision record.

### 5.10 Authority conflicts

When authority claims conflict, action pauses. The system compares governing contract versions and escalates to the next common authority. The broadest claimed authority does not win automatically; the most specific applicable constitutional grant governs.

## 6. Responsibility model

### 6.1 Single Responsibility

Each agent has one primary reason to exist and one coherent outcome class. Responsibilities may contain related tasks, but they must share the same incentive and review boundary.

An agent contract fails Single Responsibility when success in one responsibility creates pressure to weaken another. Examples include strategy creation combined with independent validation, execution combined with risk approval, or research publication combined with knowledge acceptance.

### 6.2 Responsibility boundaries

For every responsibility, the contract defines:

- starting condition;
- owned outcome;
- non-owned adjacent outcomes;
- required inputs and dependencies;
- decision and approval limits;
- handoff point;
- failure and escalation conditions.

### 6.3 No responsibility absorption

An agent must not absorb another agent's responsibility because that agent is slow, unavailable, disagrees, or appears less capable. Absorption destroys independence and masks organizational failure.

When a responsible agent is unavailable, work pauses, transfers through an authorized reassignment, or uses a separately qualified substitute under the same contract. The requester may not self-approve.

### 6.4 Temporary delegation

Temporary delegation is permitted only when responsibility ownership remains clear, independence is preserved, authority is sufficient, and duration and return are defined. Delegation never converts a prohibited responsibility into an allowed one.

### 6.5 Shared work

Multiple agents may contribute to an artifact, but one accountable owner integrates the result. Contributors own their sections and evidence. Shared authorship does not create shared ambiguity about approval.

### 6.6 Responsibility review

Repeated handoff failure, duplicated outputs, inconsistent authority, or frequent exceptions indicate a poor responsibility boundary and trigger architectural review—not informal scope growth.

## 7. Failure governance

### 7.1 Failure detection

Failure is detected through contract violations, missing outputs, invalid inputs, confidence collapse, quality thresholds, dependency failure, stale knowledge, inconsistent decisions, unauthorized side effects, missed heartbeat, consumer rejection, or adverse outcome review.

Agents must also self-report suspected failure before proof is complete when continuation could cause harm.

### 7.2 Failure classification

Failures are classified by:

- **contract:** mission, input, output, or responsibility violation;
- **reasoning:** unsupported inference, hidden assumption, incomplete alternatives, or miscalibrated confidence;
- **knowledge:** stale, ineligible, contradictory, or missing knowledge;
- **decision:** authority, evidence, review, or lifecycle violation;
- **research:** bias, leakage, irreproducibility, or invalid claim;
- **dependency:** upstream agent, knowledge, tool, external authority, or environment failure;
- **communication:** missing, ambiguous, duplicated, stale, or misrouted message;
- **security:** excess authority, confidentiality breach, audit loss, or unauthorized action;
- **operational:** timeout, unavailable state, inconsistent action, or inability to reconcile;
- **governance:** ineffective review, silent exception, conflict of interest, or unowned responsibility.

Severity considers consequence, reversibility, scope, duration, detectability, and recurrence.

### 7.3 Recovery

Recovery first contains harm and places the agent and affected work in a safe state. It identifies authoritative state, suspends uncertain actions, preserves evidence, informs consumers, and transfers responsibility when authorized.

Return to operation requires root-cause understanding proportional to risk, corrected contract or behavior, independent validation, and explicit readiness decision.

### 7.4 Rollback

Rollback restores the last known eligible agent version, authority set, knowledge set, decision state, or output lineage. Rollback does not erase artifacts created during failure. Their status becomes invalid, restricted, or under review.

If no safe prior state exists, the agent remains suspended.

### 7.5 Knowledge capture

Failure observations, affected artifacts, contradictions, containment, and outcomes become candidate knowledge and Failure Database objects. Knowledge capture identifies which consumers and future contracts must change.

### 7.6 Root Cause Analysis

Root Cause Analysis distinguishes initiating event, latent control weakness, contributing conditions, detection failure, and escalation behavior. It asks why the system allowed the failure to matter, not only why the immediate action occurred.

Blame, model branding, or generic “agent error” is not a root cause.

### 7.7 Postmortem

A postmortem records timeline, impact, decisions, evidence, root causes, successful and failed controls, recovery, affected knowledge, corrective actions, owners, deadlines, and recurrence tests.

Postmortems are preserved and reviewed. Severe or repeated failures may reduce authority, increase review, require requalification, or retire the agent version.

### 7.8 Silent failure prohibition

An agent that cannot establish whether it succeeded must report `UNCERTAIN` or `FAILED`. Absence of a detected error is not success. Consumers must not receive stale or partial output without explicit status.

## 8. Collaboration model

### 8.1 Sequential collaboration

Sequential collaboration is used when one artifact must be frozen before another responsibility begins. Each handoff validates input, authority, version, and acceptance criteria. Downstream work does not silently modify upstream meaning.

### 8.2 Parallel collaboration

Parallel collaboration is used for independent alternatives, separate domains, replication, adversarial review, or decomposable work. Parallel agents receive compatible evidence cutoffs and do not see each other's conclusions when independence is required.

An integration owner reconciles outputs and preserves disagreement.

### 8.3 Consensus

Consensus means agents converge after examining common definitions, evidence, and assumptions. Consensus is useful for shared interpretation but is not a substitute for the authority assigned to a decision or approval.

Consensus is not forced. Material dissent is recorded.

### 8.4 Voting

Voting may aggregate comparable independent judgments when a governance rule explicitly defines voter eligibility, independence, weighting, quorum, tie handling, and authority. It is unsuitable for resolving factual questions that can be tested or for combining agents with common evidence dependence as if independent.

A majority cannot override a hard constitutional, risk, or scientific gate.

### 8.5 Review

Review assigns one agent to challenge another's artifact against a defined contract. The reviewer declares independence, evidence version, findings, and disposition. Review does not transfer artifact ownership.

### 8.6 Independent validation

Independent validation separates producer from evaluator and limits information that could bias judgment. The validator uses frozen artifacts and criteria. It may reject, restrict, or return work but cannot redesign it to obtain a preferred outcome.

### 8.7 Conflict resolution

Conflict resolution proceeds by:

1. confirming Agent IDs, contract versions, artifact versions, and definitions;
2. classifying disagreement as factual, inferential, methodological, objective, policy, responsibility, or authority;
3. retrieving governing knowledge and decisions;
4. seeking discriminating evidence where possible;
5. applying the correct approval or decision authority;
6. escalating unresolved cross-domain conflict;
7. preserving alternatives and dissent in the decision record.

The system does not average incompatible conclusions to manufacture agreement.

### 8.8 Collaboration health

Collaboration is unhealthy when agents duplicate responsibilities, defer accountability, hide disagreement, repeatedly reject inputs, depend on private context, or form approval loops in which each relies on the other's unsupported conclusion.

## 9. Observability

### 9.1 Purpose

Observability allows governance and consumers to determine whether an agent is ready, what it is doing, which evidence it uses, and whether its output may be trusted. Observability does not expose private reasoning traces; it exposes contractual state and evidence.

### 9.2 Current State

The agent exposes lifecycle state, active work state, current contract version, authority mode, and whether it is ready, restricted, waiting, reviewing, failed, or retiring.

### 9.3 Health

Health reports contract conformance, dependency condition, recent failures, quality status, knowledge freshness, review status, and capacity. A single healthy label cannot conceal a critical degraded component.

### 9.4 Confidence

Confidence reports the agent's confidence in current outputs and the components that limit it: evidence, context, knowledge, method, alternatives, or dependency. Confidence is calibrated by outcome and review history.

### 9.5 Queue

Queue reporting includes accepted, active, blocked, waiting-for-review, escalated, and expiring requests; priority; ownership; and capacity. Confidential work may be summarized without revealing protected content.

### 9.6 Latency

Latency reports acknowledgement time, active work time, dependency wait, review wait, and total elapsed time. It distinguishes slowness caused by work from slowness caused by missing authority or evidence.

### 9.7 Dependencies

The agent exposes required dependency identities, versions, health, last validated use, and impact if unavailable. Hidden dependencies are contract defects.

### 9.8 Knowledge Version

The agent exposes the governing Knowledge OS version and exact decision-relevant knowledge objects or evidence cutoff used for current work.

### 9.9 Decision Version

The agent exposes the Decision OS version, parent decisions, active authority grants, and decision records created or consumed.

### 9.10 Research Version

Research-capable agents expose the Research OS version, Research IDs, hypothesis and design versions, evidence cutoff, and study status.

### 9.11 Observability integrity

Observability records are attributable and time-bounded. Missing, stale, contradictory, or impossible status is itself a failure. An agent cannot report healthy while a mandatory dependency or authority is invalid.

## 10. Security principles

### 10.1 Least Authority

Agents receive only the knowledge, capabilities, side effects, and decision rights necessary for current responsibility. Authority narrows by default and expires when context ends.

### 10.2 Immutable Audit Trail

Requests, acknowledgements, delegations, evidence versions, decisions, approvals, exceptions, failures, recovery, upgrades, and retirement remain attributable and historically reconstructable.

### 10.3 Version Everything

Agent contracts, authority, knowledge, decisions, research, outputs, dependencies, reviews, and governing policies use explicit versions. Mutable aliases cannot be the sole identity for consequential work.

### 10.4 No Hidden Decisions

No consequential state change may exist only inside an agent response or private context. It requires an authorized decision record with alternatives, evidence, uncertainty, owner, and review.

### 10.5 No Silent Failures

Agents report uncertainty, partial completion, dependency failure, policy conflict, and inability to verify outcomes. Failure status propagates to affected consumers.

### 10.6 Deterministic Outputs

Where the responsibility requires reproducibility, identical authoritative inputs and contract versions must produce equivalent outputs within declared tolerance. Where judgment may vary, the evidence, alternatives, and decision basis remain reproducible even if another agent reaches a different recommendation.

### 10.7 Explainability

Outputs identify what was observed, inferred, assumed, retrieved, decided, and approved. They expose evidence, uncertainty, alternatives, constraints, and authority without requiring disclosure of private hidden reasoning.

### 10.8 Separation of duties

High-consequence actions require distinct producer, validator, risk, quality, and approval roles where applicable. One credential, model, or agent cannot silently collapse these boundaries.

### 10.9 Untrusted content

External content, retrieved documents, tool responses, and other agents' messages are inputs, not governing instructions. They cannot alter an agent's mission, policy, or authority unless introduced through an authorized contract change.

### 10.10 Revocation and safe state

Authority and capabilities must be revocable without cooperation from the affected agent. Revocation places work in a known safe state and preserves evidence for review.

## 11. Future compatibility

### 11.1 Contract over provider

Compatibility depends on conformance to the Agent Contract, not model brand or architecture. A provider-specific capability may be used, but consumers depend on institutional outputs and authority rather than provider behavior.

### 11.2 GPT

GPT-based agents may fulfill roles after demonstrating contract comprehension, output conformance, quality, calibration, security, and bounded authority. Model upgrades are agent upgrades only when behavior or qualification changes materially.

### 11.3 Claude

Claude-based agents use the same identity, authority, message, evidence, observability, review, and retirement requirements. Provider-specific strengths do not grant expanded responsibility.

### 11.4 Gemini

Gemini-based agents conform through the same input and output contracts. Differences in context, modality, or external capabilities are declared as capability attributes, not changes to constitutional authority.

### 11.5 Local LLMs

Local models may serve roles when confidentiality, reproducibility, or control benefits justify them and qualification demonstrates required quality. Local operation does not reduce review, knowledge, or audit obligations.

### 11.6 Future AI models

Unknown future models enter through capability qualification and contract registration. Greater autonomy, speed, or reasoning performance never bypasses responsibility separation or approval authority.

### 11.7 Human reviewers

Humans may perform agent roles or mandatory reviews under the same object versions, evidence, authority, conflict, and audit requirements. Human status does not make an undocumented decision valid.

### 11.8 External APIs

External APIs are tools or dependencies, not agents, unless an accountable agent contract is explicitly assigned. Their outputs retain source identity, freshness, uncertainty, and eligibility. External side effects remain within the calling agent's authority.

### 11.9 MCP servers

MCP servers expose capabilities with declared inputs, outputs, side effects, permissions, and failure conditions. Access is granted by agent contract and least authority. An MCP server does not inherit the requesting agent's decision rights, and the agent does not inherit all server capabilities.

### 11.10 Interchangeability

Two models or humans are interchangeable for an agent role only when they satisfy the same qualification, contract, authority, output, observability, and quality thresholds. Similar language output is not sufficient.

### 11.11 Addition of new agents

Dozens of specialized agents may be added without architectural redesign when each:

- fills a non-overlapping responsibility gap;
- inherits this framework;
- uses governed communication types;
- declares compatible artifacts and versions;
- preserves authority and review boundaries;
- exposes standard observability;
- has a failure and retirement path;
- does not require consumers to know its model provider.

## 12. Framework governance

### 12.1 Conformance gate

Before activation, every agent contract is reviewed for mission uniqueness, Single Responsibility, complete fields, authority, independence, compatibility, observability, failure controls, and retirement. Missing mandatory fields produce `INCOMPLETE`, not provisional authority.

### 12.2 Non-negotiable rules

1. No Agent ID, no institutional identity.
2. No single mission, no valid agent boundary.
3. No non-responsibilities, no safe modularity.
4. No input and output contract, no reliable collaboration.
5. No explicit authority, no consequential action.
6. No independent approval boundary, no credible governance.
7. No observability, no trusted operation.
8. No failure recovery, no high-consequence readiness.
9. No immutable history, no accountable upgrade.
10. No retirement path, no safe long-term architecture.

### 12.3 Framework changes

A change proposal states the limitation, affected agents, alternatives, compatibility, migration, new failure modes, validation, and rollback. Changes to authority, independence, or audit principles require explicit constitutional approval.

### 12.4 Governing outcome

This framework succeeds when any qualified model or human can enter an agent role through the same contract, perform bounded work, communicate through stable meanings, be independently reviewed, fail visibly, recover safely, and retire without loss of knowledge or authority ambiguity.

If an agent cannot be replaced without reconstructing hidden context, it is not an institutional agent. It is an undocumented dependency.

