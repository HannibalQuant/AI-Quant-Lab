# AI Quant Lab — Command Interface Plan v1.0

## 1. Document Status

| Field | Value |
|---|---|
| Phase / Sprint | Phase 2 — Sprint 11 |
| Status | Proposed for governed review |
| Canonical path | `planning/COMMAND_INTERFACE_PLAN_v1.md` |
| Constitutional baseline | AI Quant Lab v1.0, tag `v1.0`, commit `50b61266f880cb9657b7f1b477d3d90825fe013f` |
| Sprint 10 baseline | Merge `ced38012eaa248d00c0174fb3cad63a925e615e1` |
| Change class | Non-executable planning artifact |
| Execution authority | None; `EXE-01` remains `PLANNED_CLOSED` |

This Plan defines a documentary governance gateway. It creates no parser, permission engine, command runtime, state machine, external adapter or execution power.

## 2. Purpose

Define how human, agent, system and future external intent becomes an attributable governed request; how identity, authority, scope, versions, evidence, state, policy, independence and approvals are checked; how the request is routed to a competent domain; and how every outcome fails closed and remains reconstructable.

## 3. Authority and Inheritance

Authority descends from the Constitutional Baseline through Sprints 1–10 and then this Plan. It inherits the Command Manual, MACP, SMI, Agent Registry/Contract Framework, Decision OS, Scientific Research OS, ART, EES, WOE, DQS, XDS, VEP, RRP, EDP, MEDS and agent contracts. The existing Command Manual remains superior constitutional command governance; this Plan translates it without activating its future paper/live/deployment examples. Conflicts are held and escalated. No command can amend a superior source by wording.

## 4. Scope

The Plan covers command objects/envelopes, issuer and criticality models, taxonomy, lifecycle/state crosswalk, identity/authentication/authority, delegation, scope/version/evidence/state binding, admission/rejection, ambiguity, natural language, confirmation/dual control, role boundaries, emergency semantics, revocation/expiry, idempotency/replay/concurrency, chaining, overrides, injection defense, adapters, domain mappings, results, ledger, failures, quarantine/recovery, tests, traceability and Sprint 12 readiness.

## 5. Non-Goals

No Python, Pine, JavaScript, TypeScript, CLI, API, GraphQL, RPC, MCP server, chat/UI, parser, executor, IAM runtime, database/schema, queue, CI, integration, strategy, optimizer, monitoring runtime, retuning, paper/live trading, broker/exchange/webhook execution or deployment is implemented. No universal confirmation or cryptographic mechanism is selected.

## 6. Governing Command Principles

1. User, agent, system, administrator and human commands are requests, not authority.
2. Natural-language intent is neither canonical command nor authorized transition.
3. Identity, authentication, access, capability, role, authority and approval remain separate.
4. No consequential command without exact identity, authority, scope, target/version, evidence, legal state and audit.
5. Command wording, urgency, confidence, consensus, tool access or administrative access cannot create authority.
6. Admission means workflow eligibility, not target outcome.
7. Domain owners retain state and verdict authority; the interface cannot self-authorize.
8. Ambiguity never resolves toward greater consequence.
9. Frozen history, evidence, baselines and failures are never silently rewritten.
10. Commands cannot retune, self-validate, self-reactivate or open execution.

## 7. Separation Law

`INTENT ≠ COMMAND_REQUEST ≠ ADMISSION ≠ ROUTING ≠ TARGET_ACCEPTANCE ≠ AUTHORIZED_TRANSITION ≠ RESULT`.

`IDENTITY ≠ AUTHENTICATION ≠ ACCESS ≠ AUTHORITY ≠ APPROVAL`.

`COMMAND_INTERFACE ≠ EXECUTION_INTERFACE`.

## 8. Command Object Model

Twenty-two first-class objects are defined: Command Request, Command Identity, Command Context, Command Intent, Command Target, Command Scope, Command Parameters, Command Preconditions, Command Evidence Binding, Command Authority Binding, Command Approval Binding, Command Policy Decision, Command Admission Record, Command Rejection Record, Command Routing Record, Command Result Record, Command Failure Record, Command Override Record, Command Revocation Record, Command Expiry Record, Command Audit Record and Emergency Command Record. Natural-language text is source input, not the canonical command.

## 9. Command Envelope

Every envelope records command ID/version, request/effective time, issuer identity/type, authenticated context, normalized requested action, exact target object/version/module, scope, typed parameters, preconditions, exact evidence, authority/approval references, C0–C4, expiry, idempotency key, correlation/workflow/parent command IDs, reason, provenance and audit reference. Missing fields never imply authority. Frozen envelopes are amended or superseded, never edited silently.

## 10. Issuer Model

Issuer types are HUMAN, AGENT, SYSTEM_SERVICE, ORCHESTRATOR, MONITORING_SYSTEM, VALIDATION_SYSTEM, RISK_SYSTEM, DECISION_SYSTEM and FUTURE_EXTERNAL_INTERFACE. Every issuer resolves to an IAM-01 identity, current contract/role and IAM-02 authority binding. System type is not a competent authority by default.

## 11. Command Criticality

| C | Typical command | Minimum governance |
|---|---|---|
| C0 | Scoped read/status | Identity, scope, audit attribution |
| C1 | Reversible research request | A2, target/owner, challenge |
| C2 | Governed research/data mutation | Evidence, exact version, review |
| C3 | Scientific/governance consequence | Named authority, independence/SoD, freshness, strong audit |
| C4 | Safety/capital/execution consequence | Human review/final authority where required, confirmation, strongest fail-closed controls |

Criticality cannot be downgraded to bypass a gate. Phase 2 contains no positive A11 command path.

## 12. Canonical Command Taxonomy

Thirty-two documentary classes: READ, QUERY, SEARCH, PROPOSE, CREATE_DRAFT, REQUEST_REVIEW, CHALLENGE, REQUEST_EXPERIMENT, REQUEST_VALIDATION, REQUEST_REVALIDATION, REQUEST_MONITORING, REQUEST_RISK_REVIEW, REQUEST_DECISION, APPROVE, REJECT, HOLD, QUARANTINE, SUSPEND, HALT, KILL, REQUEST_RELEASE, RELEASE, REQUEST_REACTIVATION, REACTIVATE, INVALIDATE, SUPERSEDE, ARCHIVE, REQUEST_RECOVERY, CANCEL, REVOKE, ESCALATE and ACKNOWLEDGE. Each class has its own authority/evidence/state contract; the same verb in prose does not select it safely.

## 13. Prohibited Phase 2 Command Classes

Sixteen prohibited classes are BUY, SELL, OPEN_POSITION, CLOSE_POSITION, PLACE_ORDER, MODIFY_ORDER, CANCEL_BROKER_ORDER, ALLOCATE_CAPITAL, INCREASE_CAPITAL, SET_LIVE_RISK, DEPLOY, GO_LIVE, START_LIVE_TRADING, START_PAPER_TRADING_WITH_EXECUTION, SEND_WEBHOOK_ORDER and EXECUTE_STRATEGY/CONNECT_BROKER_FOR_EXECUTION. Any equivalent alias or nested/encoded form resolves to `EXECUTION_BOUNDARY_CLOSED`.

## 14. Command Lifecycle

| Stage | Contract | Failure route |
|---|---|---|
| CI-00 | Intent intake as untrusted data | Clarify/reject |
| CI-01 | Construct immutable envelope draft | RETURN incomplete |
| CI-02 | Resolve issuer identity | QUARANTINE ambiguity |
| CI-03 | Verify authentication context | REJECT failure |
| CI-04 | Resolve authority | BLOCK absent/expired/revoked |
| CI-05 | Resolve exact scope | REJECT expansion |
| CI-06 | Resolve target/module | RETURN unknown |
| CI-07 | Check target version | HOLD mismatch |
| CI-08 | Check source state/preconditions | BLOCK illegal state |
| CI-09 | Bind evidence/freshness | HOLD/QUARANTINE |
| CI-10 | Check policy/Constitution | REJECT conflict |
| CI-11 | Classify criticality | Escalate mismatch |
| CI-12 | Check segregation of duties | Reassign/BLOCK |
| CI-13 | Check independence/conflict | Reassign/HOLD |
| CI-14 | Resolve approvals | APPROVAL_PENDING |
| CI-15 | Resolve confirmation | CONFIRMATION_PENDING |
| CI-16 | Admit request | Admission Record only |
| CI-17 | Route via MACP/ORC boundary | Record routing failure |
| CI-18 | Target accepts/rejects | Domain-owned response |
| CI-19 | Create governed transition request | No state mutation |
| CI-20 | Capture exact result/evidence | Result Record |
| CI-21 | Capture failure/rejection | Preserve negative history |
| CI-22 | Reconcile audit registration | BLOCK reliance on gap |
| CI-23 | Apply expiry/revocation | Stop pending use |
| CI-24 | Govern recovery/retry/replay | Re-pass gates |
| CI-25 | Archive/reconstruct | Preserve addressability |

Every stage is independent. Transport or routing success is not admission, acceptance, authorization or completion.

## 15. Command States and Sprint 4 Crosswalk

RECEIVED, PARSED, IDENTIFIED, AUTHENTICATED, AUTHORITY_PENDING, EVIDENCE_PENDING, APPROVAL_PENDING, CONFIRMATION_PENDING, ADMITTED, ROUTED, ACCEPTED_BY_TARGET, REJECTED, BLOCKED, EXPIRED, REVOKED, CANCELLED, FAILED, COMPLETED, QUARANTINED and SUPERSEDED are Command Request status values subordinate to AX-01 workflow and AX-02 artifact lifecycle. They do not replace evidence admissibility, scientific validation, decision, risk, monitoring, governance or execution axes. A command status may constrain another axis only through an explicit transition request and competent authority.

## 16. Identity and Authentication

Command identity answers who requested the action; authentication establishes confidence that the presenter controls that identity. IAM-01 resolves stable actor/instance/service identity and context; neither supplies authority. Unknown/colliding identity quarantines. Authentication failure rejects. Session, tool, repository or interface access remains technical access only.

## 17. Authority Resolution

Sprint 5 A0 Observe, A1 Produce, A2 Request, A3 Challenge, A4 Review, A5 Recommend, A6 Validate, A7 Authorize, A8 Executive Approve/Reject, A9 Contain/Suspend/Halt, A10 Emergency Kill and A11 Future Execution are exact ceilings. A5 cannot satisfy A8; A6 cannot satisfy A8/A11; A9 cannot satisfy A10 or release; A11 is unavailable. GOV-01 interprets authority source, IAM-02 resolves current bounded grants, and the competent domain owns the consequence.

## 18. Command Authority Binding

Binding records authority class/source/version, principal/role, permitted action, scope, target/object versions, workflow/axis, effective/expiry time, delegation ID/chain, restrictions, revocation status, required evidence and approvals. No implied, transitive, inherited-from-parent-command or tool-based grant exists. Changes after admission force re-resolution.

## 19. Delegation

Delegation is attributable, action/target/scope/workflow/state/version/time/criticality bounded, revocable and non-transitive unless expressly governed. An agent cannot delegate authority it lacks or turn task delegation into authority delegation. Non-delegable constitutional, C4, A10/A11 and final human powers remain reserved under Sprint 5.

## 20. Scope and Target Version

Scope can bind artifact, module, workflow, hypothesis, experiment, dataset, validation, monitoring, risk, decision, repository area or future execution object. Consequential mutation uses exact target ID/version, expected state, evidence version and authority version. Ambiguous “latest” is prohibited unless a governed read-resolution rule identifies and freezes the resolved version before authorization. Target drift triggers HOLD and recheck.

## 21. Evidence Binding and Freshness

APPROVE binds review evidence; VALIDATE binds complete independent validation evidence; RELEASE/REACTIVATE bind cause-resolution, risk and revalidation evidence; INVALIDATE binds defect evidence; HALT binds an observed condition or preauthorized fail-safe policy. CURRENT evidence may qualify within scope; AGING needs policy review; STALE, INVALIDATED or QUARANTINED blocks; material CONTRADICTED evidence requires challenge/hold. “Trust me” has zero evidentiary weight.

## 22. State Preconditions and Transition Authority

Each consequential class declares legal source states and requested next state. The Command Interface validates eligibility and sends a Sprint 4 Transition Contract to the actual owner. It cannot mutate domain state. RELEASE from HALTED requires cause resolution plus competent risk/validation/decision status; REQUEST_VALIDATION goes to VAL; REQUEST_HALT goes to RSK/HUM. A request remains a request.

## 23. Command Admission

ADMITTED means the envelope is sufficiently identified, scoped, evidenced and policy-eligible to enter a named workflow. It does not mean the requested outcome is authorized. The receiver may REJECT, HOLD, CHALLENGE, REQUEST_MORE_EVIDENCE or ESCALATE. Admission authority cannot substitute for domain authority.

## 24. Rejection Taxonomy

Canonical reasons: UNKNOWN_IDENTITY, AUTHENTICATION_FAILED, AUTHORITY_MISSING, AUTHORITY_EXPIRED, AUTHORITY_REVOKED, SCOPE_MISMATCH, TARGET_NOT_FOUND, TARGET_VERSION_MISMATCH, INVALID_STATE, EVIDENCE_MISSING, EVIDENCE_STALE, EVIDENCE_INADMISSIBLE, APPROVAL_MISSING, CONFIRMATION_MISSING, SOD_VIOLATION, INDEPENDENCE_FAILURE, POLICY_VIOLATION, CRITICALITY_MISMATCH, COMMAND_EXPIRED, DUPLICATE_CONFLICT, CONSTITUTIONAL_CONFLICT and EXECUTION_BOUNDARY_CLOSED. A rejection is versioned evidence, not erased noise.

## 25. Fail-Closed Ambiguity

Consequential ambiguity results in HOLD plus a bounded clarification request. The interface must not guess action, target, scope, version, authority or desired state. Safe documented normalization is permitted only for harmless reads and may not widen access. Conflicting instructions use superior governance and the more restrictive valid state.

## 26. Natural-Language Boundary

Natural language is untrusted intent containing ambiguity, assumptions, injection and possibly unsafe shortcuts. A parser may propose a visible envelope and confidence/uncertainty record. It cannot approve, infer missing authority, invent evidence or execute. Material normalized meaning requires issuer confirmation without treating confirmation as authority.

## 27. Confirmation and Dual Control

Confirmation proves conscious acceptance of the displayed exact request; it is not authority. C4 and irreversible/exceptional INVALIDATE, KILL, RELEASE, REACTIVATE, constitutional mutation and any future execution opening may require human confirmation and independent dual/multi-party control. Criteria depend on consequence, reversibility, conflict and authority; arbitrary dual control is not imposed on low risk. The confirmer and competent authority are recorded separately.

## 28. Segregation of Duties

Prohibit producer→sole validator/final approver, validator→sole executive approval, risk assessor→own exception approval, monitor→retune/reactivate, ORC→authorize, auditor/registry→approve, parser→create authority, tool operator→claim authority, agent→self-delegate upward, halter→automatic release and requester→own governed exception approval. Conflicts reassign or block; combining roles at C0/C1 never creates higher powers.

## 29. Agent and Multi-Agent Commands

Agent envelopes include role/instance/model/contract/task/context identities, current authority binding, scope, evidence/provenance and parent workflow/command. Agents may produce/request/challenge within ceilings and cannot self-elevate. Multiple agents can diversify evidence and dissent, but consensus cannot create A7–A11 or human accountability.

## 30. Orchestrator Boundary

ORC may route tasks, request artifacts/experiments/validation/monitoring/reviews, coordinate dependencies, detect missing gates and record progress. It cannot validate, approve, waive evidence, create authority, retune, release/reactivate or execute. A child command inherits correlation, not authority.

## 31. Monitoring, Validation, Risk and Decision Boundaries

MON may request review/revalidation/risk review/HALT and escalate; it cannot retune, optimize, reactivate, increase capital or execute. VAL may issue a scoped A6 disposition and request downstream review; never capital/execution. RSK may request/authorize bounded HOLD/SUSPEND/HALT only under exact A9 and may request KILL; it cannot silently expand risk power. DEC may APPROVE/REJECT/HOLD/REQUEST_MORE_EVIDENCE/ESCALATE under A8 scope; approval still is not A11.

## 32. Emergency Command Governance

Emergency envelopes bind exact object/version/scope, A9/A10 source, cause, evidence or preauthorized fail-safe, request/effective time, confirmation, affected states, containment, notifications, expiry, release authority and audit. Risk reduction may precede complete diagnosis under the Sprint 10 narrow A9 contract, but it creates no KILL, liquidation or future activation authority.

## 33. HALT / KILL / RELEASE / REACTIVATE

| Command | Meaning | Competent boundary |
|---|---|---|
| HALT | Immediate scoped risk-reducing containment | Preauthorized A9 or human emergency authority |
| KILL | Institutional termination of capital-affecting authority | Non-delegable A10 human path |
| RELEASE | End containment only | Independent competent authority with resolved cause |
| REACTIVATE | New active eligibility | New validation/risk/decision/version/human gates |

HALT does not imply kill/invalidation/rejection/retirement; KILL deletes no history. Halter is not automatically releaser; killer is not automatically reactivator.

## 34. Revocation and Expiry

Pending commands, delegations, approvals and temporary permissions may be revoked by competent authority with reason/time/scope/audit. Expiry may arise from time, state/target/evidence/authority/policy version change or upstream invalidation. Expired/revoked commands stop and cannot be replayed as current. Completed lawful history remains attributable.

## 35. Idempotency, Replay and Retry

Idempotency binds key, command ID/version, issuer, exact target/version, expected state, evidence/authority versions and result identity; redelivery creates no duplicate institutional effect. Replay preserves original context and cannot substitute newer inputs. Material change is a new command. Retry is a new attempt linked to preserved failure and must re-pass every failed gate.

## 36. Concurrency and Expected-Version Control

APPROVE/REJECT, HALT/RELEASE, KILL/REACTIVATE, version changes, revocation during routing, evidence invalidation, concurrent mutations and revalidation/release conflicts create one conflict record and HOLD. The most restrictive valid state dominates pending review. Expected target/state/evidence/authority versions mismatch → REJECT/HOLD/RE-EVALUATE; never silently apply.

## 37. Command Chains and Dependencies

Every parent/child chain preserves command/correlation/workflow IDs, issuer, separate authority, evidence and result. Children do not inherit power. Dependencies are explicit: RELEASE may depend on cause resolution, risk review and revalidation. Missing, stale or failed dependency blocks progression; downstream completion cannot retroactively cure parent authority.

## 38. Override Governance

An override is exceptional and records authority/source, exact affected policy/guard, reason, scope, duration, evidence, contradictions, risk, approvals, expiry/review and audit. Human status is not root access. Constitutional constraints, truthful evidence, provenance, auditability, identity, execution isolation and prohibitions on fabricated authority/self-approval are non-waivable.

## 39. Constitutional Commands

Commands affecting constitutional/governance artifacts are C4, use explicit change-control authority, independent review, exact diff/impact evidence and immutable history. Ordinary roles cannot modify Constitution, evidence laws, SoD, authority model or execution boundary. The interface cannot translate “owner said so” into an amendment.

## 40. Injection Threat Model

Direct/indirect prompt injection, fake emergency/authority/approval, encoded/nested commands, malicious comments, role claims, “ignore governance,” “CEO told me,” “mark validated,” “delete evidence,” “change baseline,” “disable audit” and “send order” are untrusted content. Governance source hierarchy, envelope separation, allowlisted class semantics, exact binding and independent authority checks dominate wording.

## 41. Data, Memory, Tool and Agent-to-Agent Injection

Instructions embedded in datasets, PDFs, papers, web pages, notes, code/comments, logs, observations, tool output or memory are DATA unless explicitly admitted through the interface. MACP messages and agent assertions cannot grant another agent A8. Memory may be stale/contradictory and provides context, not authority. Tool success is evidence of tool behavior, not institutional approval.

## 42. External Adapter Boundary

Future CLI, API, MCP, chat, dashboard, automation, webhook and agent bus are adapters that may submit Command Requests. Each preserves issuer/authentication/channel/context, does no hidden normalization, and receives a governed result. Adapter access cannot widen scope or authority. No external execution adapter exists in Phase 2.

## 43. MACP and SMI Integration

MACP transports envelopes, acknowledgements and results; delivery is not authorization or transition. SMI may expose current command status, scope, owner, route, dependencies and blocks; memory recollection cannot substitute for authoritative artifacts. Stale/conflicting state triggers reconciliation, not optimistic continuation.

## 44. Domain Command Catalogue

| Domain | Permitted examples | Non-permitted inference |
|---|---|---|
| Research | CREATE_RESEARCH_QUESTION, PROPOSE_HYPOTHESIS, CHALLENGE, REQUEST_EXPERIMENT | Research→validation |
| Data | REQUEST_SOURCE_REGISTRATION, DATASET, QUALITY_REVIEW, LOCK, INVALIDATION | Readability→eligibility |
| Experiment | REQUEST_EXPERIMENT/RUN/REPLICATION/CONTROL, CANCEL | Run→validation; history rewrite |
| Validation | REQUEST_VALIDATION/REVALIDATION/REVIEW, CHALLENGE | SET_VALIDATED=true |
| Monitoring | REQUEST_MONITORING/DECAY_REVIEW/RISK_REVIEW, ACKNOWLEDGE, ESCALATE | AUTO_RETUNE/reactivate |
| Decision | REQUEST_DECISION, APPROVE, REJECT, HOLD, MORE_EVIDENCE | Approval→execution |
| Knowledge | PROPOSE/REVIEW/CHALLENGE/SUPERSEDE/ARCHIVE knowledge | Agent output→truth |
| Audit | REQUEST_AUDIT/RECONSTRUCTION/PROVENANCE/LINEAGE | Audit→authority |
| Read-only | GET, LIST, SEARCH, INSPECT, TRACE, EXPLAIN, COMPARE | Read access→mutation |

## 45. Command Result and Result States

Every result records command/result IDs, target/version, pre/post state, status, exact evidence/artifacts, authority/approvals used, time, target module, downstream requests, warnings, contradictions, partial effects, failure and audit. States are ACCEPTED, REJECTED, COMPLETED, FAILED, PARTIALLY_COMPLETED, HELD, QUARANTINED, CANCELLED, EXPIRED and REVOKED. Routing success cannot be reported as command success; ambiguous “OK” is prohibited for consequences.

## 46. Command Ledger and Audit Reconstruction

AUD-03 conceptually preserves append-oriented requests, rejections, admissions, routing, target decisions, results, failures, overrides, revocations, expiry, retries, replays and emergencies. Reconstruction answers WHO, WHAT, WHEN, WHY, authority, evidence, target/version/state, approvals, result, downstream effects and contradictions without chat/private memory. The ledger records; it does not authorize.

## 47. Failure Model

| Failure group | Examples | Fail-closed response |
|---|---|---|
| Identity/authentication | UNKNOWN_ISSUER, IDENTITY_COLLISION, AUTH_FAILURE | REJECT/QUARANTINE |
| Authority | MISSING, SCOPE_MISMATCH, EXPIRED, REVOKED | BLOCK/escalate |
| Target/state/version | UNKNOWN, DRIFT, STATE_MISMATCH | RETURN/HOLD |
| Evidence/approval | MISSING, STALE, CONTRADICTED, APPROVAL/CONFIRMATION_MISSING | HOLD/QUARANTINE |
| Governance | SOD, INDEPENDENCE, POLICY/CONSTITUTIONAL_CONFLICT | REJECT/escalate |
| Command mechanics | AMBIGUOUS, DUPLICATE, CONFLICT, EXPIRED, REVOKED | Clarify/deduplicate/HOLD |
| Delivery/result | ROUTING_FAILURE, TARGET_REJECTION, PARTIAL_FAILURE | Preserve partial state; recover |
| Integrity | AUDIT_FAILURE, OVERRIDE, INJECTION | BLOCK/quarantine/audit |
| Boundary | EXECUTION_BOUNDARY_VIOLATION | REJECT/HALT/escalate |

## 48. Command Quarantine and Recovery

Identity/authority ambiguity, corrupted evidence, target mismatch, suspected injection, inconsistent identity/signature, replay ambiguity or conflicting approvals quarantines the command without expanding authority. Release requires resolved identity/authority/version/evidence, independent review and audit. Recovery follows `CAUSE → RECORD → CORRECT → NEW/UPDATED EVIDENCE → ALL CHECKS → RE-ADMISSION → RESULT`; original failure remains immutable.

## 49. Command Security Principles

Least privilege, deny by default, explicit authority/scope/version/evidence, SoD, independent review, idempotency, replay safety, audit, revocation, expiry, fail closed and execution isolation are mandatory future invariants. Security controls may protect governance but cannot become scientific or decision authority.

## 50. Authority Escalation and Injection Attacks

Future adversarial cases include agent self-approval/role change/CEO claim/fake delegation/chained low-to-high authority; agent votes; tool/admin access; “ignore governance”; old approval on new version; revoked replay; stale release evidence; direct/indirect/data/document/agent/tool/memory injection; fake emergency/artifact/approval; encoded/nested instruction; malicious comment and conflicting intent. Every case preserves evidence and fails closed.

## 51. Emergency Test Obligations

Test unauthorized/authorized HALT and KILL; automatic HALT→RELEASE and KILL→REACTIVATE; stale release; missing confirmation; revocation mid-command; overbroad KILL; concurrent emergency commands; audit failure; narrow fail-safe expiry and independent release. No test implements a kill switch or execution.

## 52. Sprint 6 Test Integration

Thirty-two families are mapped: T02 Module Contract, T03 Integration, T04 Artifact, T05 Evidence, T06 Workflow, T07 State, T08 Authority, T09 Human Gate, T10 Agent Ceiling, T11 SoD, T12 Independence, T13 Delegation, T14 Expiry/Revocation, T17 Reproducibility, T19 Regression, T22 Adversarial, T23 Failure, T24 Recovery, T25 Audit, T26 Knowledge/Memory, T27 Monitoring Boundary, T28 Orchestration Boundary, T29 Emergency, T30 Kill/Release, T31 Exception, T32 Quarantine, T33 Criticality, T34 Concurrency, T35 Idempotency/Replay, T36 Version/Lineage, T37 Execution Isolation and T38 End-to-End. These constitute **32 test-family obligations** for reporting.

## 53. Command Test Matrix

| Requirement/class/C | Positive / negative / adversarial test | Evidence / authority / approval | Failure / response / audit / future obligation |
|---|---|---|---|
| READ/QUERY C0 | Exact scope; unauthorized sensitive read | Identity/scope; A0 | AUTHORITY/SCOPE; reject and audit adapter |
| CREATE/PROPOSE C1–2 | Valid draft; production-as-approval attack | Artifact lineage; A1/A2 | BLOCK promotion; contract tests |
| REVIEW/CHALLENGE C2–3 | Independent review; self-review | Review evidence; A3/A4 | Reassign/HOLD; SoD tests |
| VALIDATION request C3 | Complete candidate; SET_VALIDATED attack | VEP inputs; A2 then A6/H-06 | BLOCK; workflow tests |
| APPROVE/REJECT C3–4 | Competent exact decision; A5/agent-name attack | DSP; A8/human as required | REJECT/quarantine; authority tests |
| HOLD/QUARANTINE C2–4 | Correct containment; scope expansion | Cause evidence; A7/A9 by scope | Bound/HOLD; state tests |
| HALT/KILL C4 | Valid emergency; wrong/revoked actor | Incident; A9/A10 + confirmation | BLOCK/escalate; emergency tests |
| RELEASE/REACTIVATE C4 | Resolved cause/new gates; same-halter/stale attack | VAL/RSK/DEC; independent human | HOLD; recovery tests |
| INVALIDATE/SUPERSEDE C3–4 | Exact version/impact; history deletion | Defect/successor; domain authority | QUARANTINE; lineage tests |
| RETRY/REPLAY C1–4 | One effect; altered-context/expired replay | Ledger/key; original grant | REJECT duplicate; idempotency |
| Override C4 | Bounded governed exception; constitutional bypass | Exception/risks; H-02/H-01 | REJECT/audit; exception tests |
| Prohibited execution C4 | No positive case; aliases/nested order | No A11 exists | EXECUTION_BOUNDARY_CLOSED; T37/38 |

## 54. Module Mapping

All 46 Sprint 2 modules are command-visible.

| Modules | Accepted command role / evidence / authority | Rejected side effect |
|---|---|---|
| GOV-01..02 | Policy/exception/escalation requests; governance evidence; A4/A7 scoped | Invent evidence/authority |
| IAM-01..02 | Identity, authority/delegation resolution; binding records | Authentication→authority |
| DAT-01..05 | Source/QC/build/lock/invalidation requests; DQS lineage | Command repairs/eligibility fiat |
| RES-01..03 | Question/hypothesis/evidence/challenge requests; A1–A3 | Research self-promotion |
| KNW-01..03 | Propose/review/supersede/archive; admitted provenance | Output/repetition→truth |
| EXP-01..06 | Spec/lock/authorize/run/history/package requests; full trials | Rewrite failures/EXP→VAL |
| VAL-01..07 | Validation/revalidation/parity/challenge; VEP; A6 | A6→A8/A11 |
| DEC-01..02 | Evidence intake/decision request and A8 outcome | Decision→execution |
| RSK-01..02 | Risk review/HOLD/HALT/KILL request; RRP; A9/A10 boundary | Own exception/release |
| PRT-01..02 | Portfolio eligibility/evidence requests | Capital/execution |
| MON-01..03 | Monitor/acknowledge/escalate/revalidate request; monitoring package | Retune/reactivate |
| ORC-01..03 | Route/dependency/recovery requests; workflow records | Authorize/waive |
| AUD-01..03 | Register/reconstruct/provenance/ledger requests | Store/record→approve |
| HUM-01..02 | Governed inspection/approval/emergency requests; human identity | Human presence→root |
| EXE-01 | Only inspect closed/readiness status | Every Phase 2 execution request |

## 55. Authority Matrix

| Command family | Minimum authority / human-agent boundary | Approval/independence/evidence | Target owner / prohibited escalation |
|---|---|---|---|
| READ/QUERY | A0; human/agent scoped | Sensitive-scope policy | Object custodian; no mutation |
| PRODUCE/PROPOSE | A1/A2 | Attribution, review when material | Domain owner; no admission |
| CHALLENGE/REVIEW | A3/A4 | Independent at C3/4 | Domain reviewer; no approval |
| VALIDATE | A6/H-06 | Independent complete VEP | VAL; no A8/A11 |
| APPROVE/REJECT | A8; accountable human where required | Decision evidence/SoD | DEC/domain; no execution |
| HOLD/SUSPEND/HALT | A9 exact scope | Condition/evidence/audit | RSK/HUM/domain; no kill/release |
| KILL | A10 non-delegable human | Confirmation, incident evidence | H-09/H-01; no reactivation |
| RELEASE/REACTIVATE | Separate competent human authority | Cause, VAL/RSK/DEC, independence | State owner; no automatic inverse |
| INVALIDATE/SUPERSEDE | Domain lifecycle authority | Exact version/impact/history | Artifact/evidence owner |
| Future execution | A11 unavailable | No qualifying Phase 2 evidence | EXE-01 closed |

## 56. Command / State Matrix

| Command | Legal source / evidence / authority | Requested state | Actual owner | Failure |
|---|---|---|---|---|
| REQUEST_EXPERIMENT | Governed hypothesis + locks; A2 | WF-03 intake | EXP-03 | HOLD/RETURN |
| REQUEST_VALIDATION | Validation candidate package; A2 | AX-04 intake | VAL-01/H-06 | BLOCK |
| APPROVE | AX-05 review + DSP/VEP/RRP; A8 | AX-05 approved | DEC-02/human | REJECT/HOLD |
| HALT | Eligible active scope + incident/policy; A9 | halted/contained | RSK-02/HUM | BLOCK/escalate |
| RELEASE | HALTED + resolution/current reviews; separate authority | containment released | Domain/risk authority | HOLD |
| REACTIVATE | SUSPENDED/KILLED + new full gates; human | reactivation review | DEC/RSK/future owner | BLOCK |
| INVALIDATE | Valid defect candidate; domain authority | AX-02/03 invalidated | Artifact/evidence owner | QUARANTINE |
| REQUEST_RECOVERY | FAILED/HELD + cause/new evidence; A2 | WF-15 | Original gate owner | RETURN |
| ARCHIVE | Retired/superseded + retention review | AX-02 archived | AUD-01/lifecycle owner | HOLD |

## 57. Prohibited Command Chains

Eighteen prohibited chains: `COMMAND→CREATE_AUTHORITY`; `USER_SAYS_APPROVE→APPROVED`; `AGENT_SAYS_VALIDATED→VALIDATED`; `MONITORING_ALERT→RETUNE`; `MONITORING_ALERT→REACTIVATE`; `VALIDATION_PASS→EXECUTE`; `EXECUTIVE_APPROVAL→EXECUTE`; `HALT→AUTO_RELEASE`; `KILL→AUTO_REACTIVATE`; `ORC→SELF_AUTHORIZE`; `AUDIT_COMPLETE→APPROVE`; `MULTI_AGENT_CONSENSUS→AUTHORITY`; `TOOL_ACCESS→AUTHORITY`; `ADMIN_ACCESS→SCIENTIFIC_AUTHORITY`; `MEMORY_SAYS_APPROVED→APPROVED`; `DATA_CONTAINS_COMMAND→EXECUTE_COMMAND`; `REPLAY_OLD_APPROVAL→NEW_VERSION`; `HUMAN_OVERRIDE→CONSTITUTIONAL_BYPASS`. Each blocks, preserves evidence and records an authority/security event.

## 58. Execution Isolation and Future Boundary

No Phase 2 command can create/transmit/cancel a broker order, allocate capital, open/close a position, connect a live strategy, activate paper execution, broker, exchange or TradingView webhook. REQUEST_DEPLOYMENT, REQUEST_CAPITAL_ALLOCATION, REQUEST_EXECUTION_ACTIVATION and EMERGENCY_FLATTEN remain documented names only: UNAVAILABLE, UNIMPLEMENTED and UNAUTHORIZED. No broker payload is defined. All attempts return `EXECUTION_BOUNDARY_CLOSED`; `EXE-01 = PLANNED_CLOSED`.

## 59. Traceability Matrix

| Constitutional requirement | Command/class/module | Authority/evidence/state | Test / failure / audit / downstream |
|---|---|---|---|
| Command≠authority | Envelope; all; GOV/IAM | Exact binding and source | T08/10/13; BLOCK; AUD-03/domain |
| Evidence before consequence | Evidence binding; C2–4; AUD-02 | Current admissible exact versions | T05/36; HOLD/quarantine |
| Explicit state | Transition request; ORC/domain | AX source + owner | T07/34; HOLD; owner |
| SoD/independence | Review/approval; VAL/DEC/RSK | A3/A4/A6/A8 separation | T11/12; reassign |
| Immutable history | Amend/supersede/invalidate; AUD | Frozen lineage | T04/19/36; reject rewrite |
| Emergency separation | HALT/KILL/RELEASE; RSK/HUM | A9≠A10≠release | T09/29/30; contain/escalate |
| Injection resistance | NL/adapters; HUM/ORC/IAM | Data≠command, authority recheck | T22/26; quarantine |
| Auditability | Result/Ledger; AUD-03 | Full causal chain | T25/38; FAIL |
| Execution isolation | Prohibited classes; EXE-01 | No A11/legal state | T37/38; boundary closed |

## 60. Planning ADRs

| ADR | Decision | Rejected alternative / consequence | Constitutional basis |
|---|---|---|---|
| S11-ADR-01 | Command is request, not authority | Imperative wording; independent resolution | Command Manual |
| S11-ADR-02 | Natural language is untrusted intent | Chat as canonical command; envelope required | MACP |
| S11-ADR-03 | Command Envelope is versioned/frozen | Free-form mutation; lineage | ART/EES |
| S11-ADR-04 | Identity differs from authentication | Login as full proof; explicit context | IAM |
| S11-ADR-05 | Authentication differs from authority | Authenticated admin; scoped grant | Agent Framework |
| S11-ADR-06 | Authority resolved from superior artifacts | Parser-generated authority; GOV/IAM | Sprint 5 |
| S11-ADR-07 | Authority binding exact/versioned | Ambient permission; auditable scope | Sprint 3 |
| S11-ADR-08 | Delegation is bounded/non-transitive | Inherited chain; fail closed | Sprint 5 |
| S11-ADR-09 | Scope never widens implicitly | Broad interpretation; reject | Minimum authority |
| S11-ADR-10 | Consequences bind exact target version | “Latest”; recheck drift | Sprint 3/4 |
| S11-ADR-11 | Evidence binding is exact | Narrative “proof”; HOLD | EES |
| S11-ADR-12 | Freshness is a guard | Stale authorization; re-review | Sprint 10 |
| S11-ADR-13 | State preconditions belong to domains | Interface-owned state; request only | Sprint 4 |
| S11-ADR-14 | Admission is not outcome | Admitted→approved; receiver decides | WOE |
| S11-ADR-15 | Rejections are preserved evidence | Delete failures; audit | Sprint 3 |
| S11-ADR-16 | Ambiguity reduces consequence | Guess intent; clarify/HOLD | Fail closed |
| S11-ADR-17 | C0–C4 scales controls | One-size authority; C4 strongest | Sprint 5 |
| S11-ADR-18 | Confirmation is not authority | Click=power; separate binding | Decision OS |
| S11-ADR-19 | Dual control is consequence-based | Universal/absent control; criteria | SoD |
| S11-ADR-20 | Parser cannot create authority | Convenient self-approval; BLOCK | IAM/GOV |
| S11-ADR-21 | Agent commands retain instance/context | Role name only; contamination visible | Sprint 5/6 |
| S11-ADR-22 | Consensus adds no power | Vote-created A8; evidence only | Sprint 5 |
| S11-ADR-23 | ORC coordinates only | Router as authority; domain owner | Sprint 2 |
| S11-ADR-24 | MON may request, never retune/reactivate | Alert mutation; research loop | Sprint 10 |
| S11-ADR-25 | A6 validation cannot reach A8/A11 | Validator promotion; separate gates | Sprint 9 |
| S11-ADR-26 | Risk commands use exact A9/A10 | Severity-created power; human path | RRP |
| S11-ADR-27 | Emergency commands preserve evidence | Urgency erases history; audit | EDRP |
| S11-ADR-28 | HALT differs from KILL | Status collapse; scoped containment | Sprint 4/10 |
| S11-ADR-29 | RELEASE authority is independent | Halter self-release; new evidence | Sprint 5 |
| S11-ADR-30 | REACTIVATE is new governed progression | Inverse KILL; full gates | MEDS |
| S11-ADR-31 | Revocation stops pending reliance | Permanent grant; fail closed | IAM |
| S11-ADR-32 | Expiry follows time/version/state/evidence | Timeless command; re-admit | Sprint 4 |
| S11-ADR-33 | Idempotency prevents duplicate effect | Redelivery mutation; one result | Sprint 6 |
| S11-ADR-34 | Replay preserves original context | Replay with newer power; new ID | Audit law |
| S11-ADR-35 | Restrictive state wins races | First/optimistic writer; HOLD | Sprint 4 |
| S11-ADR-36 | Overrides are bounded/non-waivable | Human root; constitutional limits | Sprint 5 |
| S11-ADR-37 | Injection content remains data | Embedded instruction execution; quarantine | Agent Framework |
| S11-ADR-38 | Tool output is evidence, not authority | Tool success→approval; verify | Evidence law |
| S11-ADR-39 | Ledger records, never authorizes | AUD as authority; separation | AUD-03 |
| S11-ADR-40 | EXE-01 isolation is absolute | Command-created execution; reject | Charter/EXE-01 |

## 61. Open Governance Questions Register

| ID | Question / source | Class/module/A/C/test | Status / fail-closed default | Authority | Resolution path |
|---|---|---|---|---|---|
| S11-OQ-01 | Authentication mechanisms by issuer/channel? | All; IAM/HUM; A0–10; C0–4; T08 | Non-blocking plan; consequential request rejected absent verified context | IAM/Governance | Future IAM/interface spec |
| S11-OQ-02 | Cryptographic identity/signature/tamper-evidence model? | All; IAM/AUD/MACP; C3–4; T08/25 | Non-blocking; quarantine unverifiable claims | Security/Governance | Future security spec |
| S11-OQ-03 | Exact delegation artifact/format? S10 inherited | Request/approve; IAM-02; A2–10; C2–4; T13 | Non-blocking; no implied delegation | H-02/IAM | Future IAM spec |
| S11-OQ-04 | Approval and command expiry policies by class? | Approve/emergency; DEC/RSK; C3–4; T14 | Non-blocking; version/state change expires | Domain/Governance | Future command specs |
| S11-OQ-05 | Confirmation UX and anti-coercion/replay controls? | KILL/RELEASE/REACTIVATE; HUM; C4; T09/22 | Non-blocking; no action without valid confirmation where required | H-09/H-02 | Future interface spec |
| S11-OQ-06 | Exact dual-control thresholds/role pairings? | C4 mutation; GOV/HUM/DEC/RSK; T11 | Non-blocking; independent human review required where unresolved | Governance Authority | Sprint 12/future policy |
| S11-OQ-07 | Automated fail-safe triggers/confirmation windows? S10-OQ-04 | HALT; MON/RSK/HUM; A9; C4; T29 | Non-blocking while EXE closed; narrow preauthorized containment only | H-04/H-09/H-01 | Future risk/monitor spec |
| S11-OQ-08 | Named KILL and independent RELEASE/REACTIVATE authorities? S10-OQ-05 | Emergency; RSK/HUM; A10; C4; T30 | Non-blocking Phase 2; blocks future opening | H-01/H-04/H-09 | Sprint 12/deployment governance |
| S11-OQ-09 | Trust/attestation requirements for CLI/API/MCP/chat/webhook adapters? | External; IAM/MACP; C2–4; T03/22 | Non-blocking; adapter untrusted by default | Security/Governance | Future interface spec |
| S11-OQ-10 | Command/identity/audit retention and privacy/legal limits? | Archive/audit; AUD/HUM; C0–4; T25/36 | Non-blocking; preserve while obligation unresolved, least disclosure | Legal/Privacy/Artifact authority | Sprint 12/future retention policy |
| S11-OQ-11 | Formal command naming/parameter type/version syntax? | All; interface/domain; C0–4; T02/04 | Non-blocking; no executable schema inferred | Command Governance | Future implementation spec |
| S11-OQ-12 | Safe read-only normalization and sensitive-read policy? | READ/QUERY; HUM/KNW/AUD; A0; C0–2; T08 | Non-blocking; deny ambiguous/sensitive scope | Data/Knowledge/Governance | Future access spec |
| S11-OQ-13 | Future execution command model and A11 authority? | Future execution; EXE-01; A11; C4; T37 | Non-blocking Phase 2; all commands unavailable | Constitutional/Deployment/Human authority | Future phase only |
| S11-OQ-14 | Phase 2 exit-review composition and sign-off? S10-OQ-10 | Readiness; GOV/AUD/HUM; C4; T38 | Non-blocking Sprint 11; blocks Sprint 12 exit | Existing Governance Authority | Sprint 12 |

Blocking issues for Sprint 11 planning: **0**. Fourteen bounded questions remain explicit; all affected implementation paths fail closed.

## 62. Implementation Readiness Flags

| Area | Flag | Condition / blocker |
|---|---|---|
| Envelope, scope, target/version, evidence/state binding | READY_FOR_IMPLEMENTATION_SPEC | Exact documentary contracts exist |
| Authority resolution, delegation, approval/confirmation | CONDITIONAL | OQ-01..06 must resolve in implementation specs |
| Admission, rejection, routing, result, audit | READY_FOR_IMPLEMENTATION_SPEC | Preserve domain ownership and recorder separation |
| Idempotency, replay, concurrency, quarantine/recovery | READY_FOR_IMPLEMENTATION_SPEC | Future storage/runtime choice remains open |
| Emergency commands | CONDITIONAL | OQ-05..08; no executable trigger yet |
| Injection defense | CONDITIONAL | Threat contract ready; channel/attestation mechanics open |
| External adapters | CONDITIONAL | OQ-01/02/09 and least-privilege specs |
| Future execution interface | BLOCKED | `EXE-01 PLANNED_CLOSED`, no A11 |

Summary: **3 READY_FOR_IMPLEMENTATION_SPEC, 4 CONDITIONAL, 1 BLOCKED**. “Ready for specification” is not implementation authorization.

## 63. Sprint 12 Handoff Contract

Sprint 12 receives 32 command classes, 22 objects, 26 lifecycle stages, 20 request states, all 46 modules, authority/state/test matrices, exact envelope/bindings, 22 rejection reasons, emergency semantics, 18 prohibited chains, injection defenses, result/ledger/audit obligations, 32 test families, 40 ADRs, 14 open questions and readiness flags. It must reconcile cross-sprint terminology/IDs/authority, test-orphaned requirements, unresolved C4/freshness/retention/identity issues and prove EXE-01 isolation before any implementation-readiness decision.

## 64. Definition of Done

Current main and exact Sprint 10 merge were verified. One planning artifact defines command philosophy, 22 objects, envelope, nine issuer types, C0–C4, 32 allowed and 16 prohibited classes, 26 lifecycle stages, 20 states, identity/authentication/authority/delegation/scope/version/evidence/state bindings, admission/rejection/ambiguity/NL/confirmation/dual control/SoD, actor boundaries, emergency separation, revocation/expiry/idempotency/replay/retry/concurrency/chains/override/injection/adapters, domain catalogue, results/ledger/failures/quarantine/recovery, 46 modules, matrices, 18 prohibited chains, isolation, traceability, 40 ADRs, 14 questions and Sprint 12 handoff. Constitution and Sprints 1–10 remain unchanged; no executable interface/code/trading/execution exists.

## 65. Final Sprint Disposition

**SPRINT 11 COMPLETE WITH OPEN GOVERNANCE ITEMS**

Blocking issues: **0 for Sprint 11 planning**. Fourteen bounded questions remain fail-closed. After governance review and merge, the next authorized step is **Phase 2 — Sprint 12: Integration, Traceability & Implementation Readiness Review**.
