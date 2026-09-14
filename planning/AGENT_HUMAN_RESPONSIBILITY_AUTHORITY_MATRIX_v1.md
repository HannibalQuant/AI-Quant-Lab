# AI Quant Lab — Agent / Human Responsibility & Authority Matrix v1.0

## 1. Document Status

| Field | Value |
|---|---|
| Phase / Sprint | Phase 2 — Sprint 5 |
| Status | Proposed for governance review |
| Canonical path | `planning/AGENT_HUMAN_RESPONSIBILITY_AUTHORITY_MATRIX_v1.md` |
| Constitutional baseline | AI Quant Lab v1.0, tag `v1.0`, commit `50b61266f880cb9657b7f1b477d3d90825fe013f` |
| Sprint 1 | Charter v1.0, merge `82b683d252dba63cc7e8b0be44febef10eb5b7b3` |
| Sprint 2 | Module Boundary Architecture v1.0, merge `f7d2d46ab55ba9d6150443ae9c8623a0705f561d` |
| Sprint 3 | Artifact & Evidence Contract System v1.0, merge `3f887e993903840f35ce88c9a4124c2bd695331c` |
| Sprint 4 | Workflow & State Transition Blueprint v1.0, merge `f65acebf3dfd0644f677ad44ab3a28c20ab8eec3` |
| Version | 1.0 |
| Implementation / execution authority | None |

This is a documentary governance plan. It does not amend superior contracts or create executable permissions.

## 2. Purpose

Define who may observe, produce, request, challenge, review, recommend, validate, admit, authorize, approve, contain, amend, invalidate, record, coordinate or—only in a separately opened future phase—execute, and under what evidence, scope, independence, delegation and accountable-human conditions.

## 3. Authority and Inheritance

Authority descends: Constitution → Charter → Sprint 2 modules → Sprint 3 contracts → Sprint 4 workflows/axes → this matrix → future tests/specifications. Agent contracts remain authoritative for named roles. This matrix narrows ambiguity and maps responsibilities; it cannot silently remove a superior grant or manufacture a new one.

The Executive Decision Agent contract permits a qualified model or human to exercise bounded institutional decision authority, while founder-reserved, constitutional, capital-affecting and other non-delegable powers remain outside autonomous authority. Where role-provider status remains material, fail closed and route to the named accountable human/governance authority.

## 4. Scope

This plan covers human, agent and system actors; twelve authority classes; eight autonomy levels; enriched responsibility roles; SoD, independence and conflicts; all 46 modules, 16 workflows and 10 axes; delegation, expiry, emergency/kill, exceptions, accountability, failures/quarantine, C3/C4 rules, traceability, tests, ADRs and open questions.

## 5. Non-Goals

No agent, IAM/RBAC/ABAC engine, schema, code, API, database, state machine, workflow automation, LLM call, trading logic, monitoring/validation engine, broker connection, capital allocation, paper/live trading or deployment system is implemented. EXE-01 remains closed.

## 6. Governing Principles

1. Capability, identity, access, output, confidence, tool access, consensus and prior success do not create authority.
2. Responsibility is assigned; accountability is attributable; authority is explicit, scoped, evidenced, revocable and audited.
3. Recommendation ≠ decision; validation ≠ decision; decision ≠ execution authority.
4. Human presence is not an override; an undocumented “owner said so” has no institutional effect.
5. No implied or transitive delegation.
6. Independent review and challenge protect C2–C4 paths.
7. Requester, final approver and recorder remain distinct where required.
8. Emergency containment may reduce risk; reactivation needs separate authority.
9. Missing authority fails closed and enters authority quarantine.
10. No accountable action may terminate at “the system.”

## 7. Terminology

| Term | Meaning | Not synonymous with |
|---|---|---|
| Actor | Identified human, agent instance or system component | Role |
| Role | Governed bundle of duties/limits | Identity |
| Capability | What actor can technically do | Authority |
| Responsibility | Assigned duty to act or deliver | Final accountability |
| Accountability | Named answerability for outcome/control | Custody |
| Authority | Legitimate power to cause bounded institutional effect | Access |
| Permission | Current authorization for exact action/scope | Permanent authority |
| Delegation | Explicit temporary transfer of delegable power | Task routing |
| Scope | Objects, workflow, axis, action, time and criticality bounds | General mandate |
| Custody | Integrity/access/retention duty | Scientific or executive authority |

## 8. Actor Model

Every actor record identifies category, stable identity, role, instance/provider, contract/version, capabilities, responsibilities, accountable owner, authority source/classes, delegation, permissions, scope, custody, task/workflow, context exposure, conflicts, expiry/revocation and audit references. Unknown identity or authority blocks consequential action.

## 9. Human Actor Taxonomy

| ID | Human role | Core mandate | Explicit limit |
|---|---|---|---|
| H-01 | System Owner / Founder Authority | Constitutional stewardship and reserved decisions | Cannot rewrite evidence or waive immutable law |
| H-02 | Governance Authority | Policy interpretation, exceptions and violations | Cannot self-approve requested exception |
| H-03 | Executive Decision Authority | Accountable high-impact institutional decisions | Cannot establish science/risk by opinion |
| H-04 | Risk Authority | Risk acceptance, limits and emergency review | Cannot validate science or execute |
| H-05 | Portfolio Authority | Portfolio admission and capital-context decisions | Cannot create strategy validity |
| H-06 | Validation Authority / Reviewer | Independent validation ownership/verdict | Cannot approve own produced strategy |
| H-07 | Research Owner | Questions, hypotheses and research scope | Cannot self-validate/promote |
| H-08 | Data Steward | Source, custody, eligibility and data exceptions | Cannot infer edge |
| H-09 | Emergency Authority | Confirm/extend/release containment and kill decisions | No broader standing authority |
| H-10 | Auditor / Governance Reviewer | Independent reconstruction and findings | Cannot authorize because it records |
| H-11 | Operator / Interface User | Authorized commands and operational acknowledgement | Tool access grants nothing |

No omnipotent administrator role exists. One person holding multiple roles must disclose the combination and satisfy SoD or obtain an allowed independent control.

## 10. Agent Actor Taxonomy

Canonical repository roles are: Market Research Agent, Research Librarian Agent, Knowledge Curator Agent, Quant Strategy Architect, Quant Strategy Engineer, Experiment Orchestrator Agent, Validation Agent, Risk Governance Agent, Executive Decision Agent, Pine Agent, Python Agent, QA Agent and CEO Agent. No duplicate agents are created. Names describe contracts; they do not prove current identity, instance independence or authority.

## 11. System Actor Taxonomy

| System actor | Permitted institutional function | Prohibition |
|---|---|---|
| Module | Perform bounded domain capability | Self-authorize |
| Registry | Identify/version/custody metadata | Approve stored content |
| Orchestrator | Sequence, route, coordinate | Create authority |
| Monitor | Observe, classify, request | Retune/reactivate |
| Audit ledger | Preserve/reconstruct events | Authorize events |
| State recorder | Record authorized transition | Approve transition |
| Authorization resolver | Evaluate existing policy/delegation | Invent policy or authority |
| EXE-01 | Reject/route future readiness while closed | Execute or allocate capital |

## 12. Authority Classification

| Class | Meaning / actors | Evidence, scope, independence, human/delegation | Audit/expiry and prohibited consequence |
|---|---|---|---|
| A0 Observe | Read/observe by permitted humans, agents, systems | Identity/access/scope; delegable | Log material reads; no mutation |
| A1 Produce | Create candidate artifact/evidence | Task, sources, contract; producer attribution | Version/audit; no admission |
| A2 Request | Request governed action/transition | Current state, exact object and authority to request | Expires with task; no transition |
| A3 Challenge | Register evidenced challenge | Independence/conflict disclosure | Persistent record; no automatic invalidation |
| A4 Review | Assess assigned dimension | Competence, exact inputs, independence as required | Review record; no broader approval |
| A5 Recommend | Offer bounded disposition | Evidence and alternatives; agent/human permitted | Recommendation expires with basis; no decision |
| A6 Validate | Issue scientific disposition | Validation contract, frozen evidence, mandatory independence; qualified VAL authority | Exact verdict; no risk/execution |
| A7 Authorize | Permit bounded non-executive transition/action | Named authority, guards, scope; delegable only if superior source permits | Revocable/expiring; no cross-domain authority |
| A8 Executive Approve/Reject | Issue institutional decision | Complete packages, dissent, DEC contract; accountable H-03 for C4/capital/reserved matters | Immutable decision record; no execution |
| A9 Contain/Suspend/Halt | Reduce/stop current exposure or progression | Predeclared trigger or H-04/H-09; agent may request or bounded fail-safe | Immediate audit/review; no reactivation |
| A10 Emergency Kill | Terminate capital-affecting authority | Non-delegable H-09/H-01 as governed; strongest evidence available | Permanent event history; release is separate |
| A11 Future Execution | Activate/operate capital-affecting system | Prohibited in Phase 2; future non-delegable human authorization plus all gates | EXE-01 closed; documentation creates none |

## 13. Human Authority Model

| Requirement | Applies when | Rule |
|---|---|---|
| HUMAN REQUIRED | Identity/accountability, reserved exceptions, constitutional and capital decisions | Named human must participate |
| HUMAN FINAL AUTHORITY | A10/A11; constitutional amendment; material C4 capital/risk override | Human signs final bounded outcome |
| HUMAN REVIEW REQUIRED | C4 and conflicted C3; emergency containment; critical invalidation | Independent human review before progression or promptly after risk-reducing fail-safe |
| HUMAN ESCALATION REQUIRED | Authority conflict, missed kill, critical contradiction, audit/provenance failure | Work holds pending named recipient |
| HUMAN OPTIONAL | C0/C1 routine work and nonconsequential C2 under contract | Agent may complete with audit |
| AGENT PERMITTED UNDER DELEGATION | A0–A7 within contract; bounded A8 where superior Executive contract permits | Exact delegation and ceiling required |
| AUTONOMOUS SYSTEM PERMITTED | Deterministic observation, recording and predeclared risk-reducing containment | Cannot approve/release/expand authority |
| PROHIBITED IN PHASE 2 | A11 and any implementation/execution | Always fail closed |

Every human command records identity, role, source, action, scope, evidence, time and audit. Presence or ownership never implies unrestricted override.

## 14. Non-Delegable Human Powers

Fourteen powers remain human-reserved unless a superior constitutional amendment explicitly changes them: (1) constitutional amendment; (2) founder-reserved governance decision; (3) final approval of a material governance exception; (4) acceptance of unresolved critical contradiction; (5) waiver of independent validation where waiver is constitutionally permissible; (6) final C4 decision affecting capital/safety; (7) capital-affecting risk acceptance; (8) material risk-limit override; (9) portfolio capital authorization; (10) A10 emergency kill; (11) lifting kill/emergency suspension; (12) production deployment authorization; (13) live capital allocation; and (14) opening/activating EXE-01. No power exists to bypass non-waivable guards.

## 15. Agent Autonomy Model

| Level | Allowed / forbidden | Supervision, evidence, audit, criticality |
|---|---|---|
| L0 Read Only | Read permitted exact versions; no production | Access audit; C0–C4 observation only |
| L1 Analyze | Analyze and flag; no institutional write except draft notes | Task supervision; source traceability |
| L2 Produce Artifact | Create versioned candidate | Owner/reviewer; A1; usually C0–C2 |
| L3 Propose / Request | Submit challenge/request/recommendation | A2/A3/A5; gate review; C0–C3 |
| L4 Coordinate | Route authorized workflow and record status | ORC contract; no authorization; C0–C3 and C4 routing |
| L5 Bounded Domain Action | Review/admit/validate/authorize within explicit contract | Independent controls, exact delegation, human escalation; up to C3 |
| L6 Bounded Governed Autonomy | Narrow high-assurance action allowed by superior contract | Predeclared scope, revocation, accountable human; no non-delegable power |
| L7 Capital-Affecting Autonomy | Would affect capital/execution | Prohibited; no Phase 2 authority |

Revocation, expiry, guard failure or ambiguity reduces effective level to the last proven lower level or blocks action.

## 16. Responsibility Role Model

`P` Producer, `RQ` Requester, `RV` Reviewer, `CH` Challenger, `RC` Recommender, `VA` Validator, `AU` Authorizer, `AP` Approver, `CU` Custodian, `RE` Recorder, `CO` Coordinator, `MO` Monitor, `ES` Escalation Target, `EA` Emergency Authority and `AC` Accountable Human. Assignment is per object/workflow/axis/action; labels do not transfer power.

## 17. Segregation of Duties

| Combination | Rule |
|---|---|
| Produce→review/admit | Allowed only C0/C1 routine fields with declared conflict, policy and independent spot control; otherwise separate |
| Produce→validate/approve/invalidate | Prohibited for same material claim/path |
| Experiment→validate | Prohibited where independence required |
| Validate→executive decision | Validator may recommend; cannot be sole final authority |
| Decision→risk acceptance | Separate domain authority required |
| Risk assessment→risk exception | Assessor cannot finally approve own exception |
| Portfolio analysis→portfolio approval | Separate accountable authority for C4/capital context |
| Monitor→retune/reactivate | Prohibited |
| Exception request→approval | Prohibited |
| Emergency halt→release | Separate review/release authority required |
| State request→authorization | Separate at C3/C4 |
| Authorization→recording | Recorder may record but cannot validate its own authority record alone |
| Identity registration→authorization | Prohibited implication |
| Agent recommendation→final human decision | Recommendation only |

## 18. Independence Model

| Dimension | Independent when | Broken by / effect |
|---|---|---|
| Actor | Different accountable identity and no undisclosed interest | Same actor/self-review → reassign |
| Role | Separate mandate and verdict ownership | Dual-role conflict → disclose/control |
| Module/workflow | No control over producing path or mutable inputs | Shared control → hold |
| Evidence/dataset | Ancestry and selection exposure disclosed | Shared selected evidence ≠ independent confirmation |
| Implementation | Validator did not silently author target behavior | Author-as-validator → additional independent review |
| Validation | Specification, inputs, execution and verdict insulated from producer influence | Context leakage/self-validation → fail independence |
| Decision | Final authority did not manufacture prerequisite verdicts | Domain impersonation → block |
| Organizational/human | No material incentive, reporting or ownership conflict where required | Conflict → escalation/alternative reviewer |

Mandatory for final C2 scientific evidence, C3 gates and C4 decisions; recommended for C1 challenge. Conflicts are evidenced and registered. Bounded conflict may be accepted only by independent competent governance and never for non-waivable self-approval, fabricated provenance or capital-execution authority.

## 19. Conflict-of-Interest Model

Creation self-review, designer self-validation, optimizer selecting its own validation winner, self-challenge, risk assessor approving exception, recommender as sole approver, monitor authorizing remediation, undocumented owner override, same model instance reused as “independent,” and shared-context contamination are detectable conflicts. Each receives identity/context lineage, disclosure, severity, containment/HOLD, reassignment, escalation, waiver eligibility and audit. Undisclosed material conflict blocks eligibility; non-waivable conflicts cannot be excepted.

## 20. Agent Role vs Agent Instance

Independence records agent role, instance ID, model/provider identity and version, prompt/contract version, task/workflow IDs, memory/context exposure, input evidence, output artifact, authority scope and time. Two invocations of one role are not automatically independent; different names sharing contaminated context are not independent. The claim of independence requires its own evidence.

## 21. Human Accountability

| C3/C4 failure | Accountable authority |
|---|---|
| Incomplete evidence admitted | Evidence Governance owner / H-10 review |
| Wrong validation | H-06 Validation Authority |
| Agent exceeds scope | Delegator plus agent-contract Governance H-02 |
| Risk exception granted | H-04 and final exception authority H-02/H-01 |
| Kill signal ignored or emergency release | H-09 with H-04 oversight |
| HOLD released | Named release authority for original gate |
| Decision promoted | H-03 for human-required C4; otherwise registered DEC authority plus named consequence owner |
| Stale evidence reused | Consuming domain owner and Evidence Governance |
| Invalidated dependency remains | Owning domain authority plus ORC impact-routing owner |
| EXE-01 opened | H-01/H-03/H-04 and separately defined future deployment authority |

“The system” is never the terminal accountable party.

## 22. Criticality × Authority Matrix

| Class | Max agent autonomy | Minimum review/independence | Human requirement | Audit/recovery |
|---|---|---|---|---|
| C0 | L3 | Owner review as policy requires | Optional | Basic attribution; correct by version |
| C1 | L4 | Peer/challenge available; self-review declared | Optional/escalation available | Reconstruct inputs/output |
| C2 | L5 | Independent evidence/method reviewer | Human oversight defined; final human if material exception | Strong provenance; re-pass failed gate |
| C3 | L6 only under explicit superior contract/delegation | Independent reviewer and separate request/authorization | Human review for conflicts, exceptions, irreversible governance effect; named AC always | Full audit, challenge and containment |
| C4 | No autonomous final non-delegable action; L4 routing/L5 analysis | Strongest independent specialist reviews | Human final authority for capital, kill/release, constitutional/reserved and EXE actions | Fail closed, immediate escalation, full reconstruction |

Routine reversible C3 transitions may be agent-authorized only where the existing contract explicitly grants the power, no conflict exists, and a named accountable human/governance owner plus revocation path exists.

## 23. Module Responsibility Matrix

All 46 canonical modules are mapped. Codes use Section 16; “AU” never exceeds the superior module contract.

| Module | Responsible / allowed agent | Human / powers | Records & escalation | Prohibited / C / AC |
|---|---|---|---|---|
| GOV-01 | Governance role; RV/RC/AU policy eligibility | H-02 review | Resolution; H-01/H-02 | Exception/self-approval; C3; H-02 |
| GOV-02 | Governance support; RQ/RV/RC/ES | H-02/H-01 AP exceptions | Exception/escalation | Requester self-approval; C4; H-02 |
| IAM-01 | Registry; CU/RE | H-02 owner | Identity record; H-10 | Grant authority; C3; H-02 |
| IAM-02 | Resolver; RV/AU existing permission | H-02 for conflict/C4 | Authorization record | Invent authority; C4; H-02 |
| DAT-01 | Librarian/Data agent; P/CU | H-08 owner | Source record; H-08 | Dataset/science approval; C2; H-08 |
| DAT-02 | Data agent; P/CU/RQ | H-08 | Custody/admission; H-08 | Silent repair; C2; H-08 |
| DAT-03 | QA/Data; RV/CH/RC | H-08 review | DQ/temporal; H-08/H-06 | Edge inference; C2; H-08 |
| DAT-04 | Engineering/Data; P | H-08 oversight | Manifest/lineage | Self-qualify; C2; H-08 |
| DAT-05 | Registry; CU/RE | H-08 owner | Dataset record | Content mutation; C2; H-08 |
| RES-01 | Market Research; P/RQ | H-07 owner | Question; H-07 | Experiment authorize; C1; H-07 |
| RES-02 | QSA/Research; P/RQ | H-07 | Hypothesis; H-07 | Validate/promote; C1; H-07 |
| RES-03 | Research/QA; CH/RV/RC | H-07/H-06 | Challenge; H-07 | Suppress dissent; C2; H-07 |
| KNW-01 | Knowledge Curator; CU/RV/AU knowledge status | H-02 oversight | Knowledge record | Scientific truth; C2; H-02 |
| KNW-02 | Memory gateway; CU/RE | H-02 | Handoff/access | Authority creation; C2; H-02 |
| KNW-03 | Curator/QA; CH/RV/RC | H-02/H-10 | Failure/lineage | Delete negatives; C2; H-02 |
| EXP-01 | QSA/Experiment agent; P/RQ | H-07 | Spec; EXP-03 | Validation; C2; H-07 |
| EXP-02 | Engineer/Orchestrator; P/CO | H-07/H-08 | Lock; EXP-03 | Retroactive lock; C2; H-07 |
| EXP-03 | Experiment authority role; RV/AU run only | H-07 review for C3 exceptions | Authorization; GOV | Scientific verdict; C3; H-07 |
| EXP-04 | Experiment Orchestrator; CO/P/RE | H-07 operator owner | Run/failure; EXP-03 | Validate/promote; C2; H-07 |
| EXP-05 | Orchestrator; P/RQ | H-07 | Result package; AUD-02 | Self-admit; C2; H-07 |
| EXP-06 | Experiment/Search agent; P/CO | H-07 | Search/trials; VAL | Hide trials/promote; C2; H-07 |
| VAL-01 | Validation Agent; RV/AU intake | H-06 owner | Validation spec; H-06 | Edit experiment; C3; H-06 |
| VAL-02 | Validation Agent; VA/P | H-06 | Chronological evidence | Decision; C2; H-06 |
| VAL-03 | Validation Agent; VA/P | H-06 | Stress evidence | Risk acceptance; C2; H-06 |
| VAL-04 | Validation Agent; VA/P | H-06 | Stability evidence | Scope expansion; C2; H-06 |
| VAL-05 | Validation/QA; CH/RV/VA | H-06 | Negative/adversarial | Hide contradiction; C3; H-06 |
| VAL-06 | Validation Agent; RV/VA/RC | H-06 final validation owner | VEP/verdict; DEC | Executive/risk/deploy; C3; H-06 |
| VAL-07 | QA/Validation/Engineers separated; RV/CH | H-06 | Parity record; H-06 | Edge validation; C3; H-06 |
| DEC-01 | Executive Decision Agent; P/RV/RC | H-03 review C4 | Support package; DEC-02 | Final reserved decision; C3; H-03 |
| DEC-02 | Executive Decision role; A8 within contract | H-03 final for reserved/C4 capital | Decision record; H-01 | Evidence/risk rewrite or execution; C4; H-03 |
| RSK-01 | Risk Governance Agent; RV/RC/AU bounded risk | H-04 risk acceptance/override | Risk record; H-04 | Science/execution; C4; H-04 |
| RSK-02 | Risk Agent; MO/RQ/RC/A9 bounded containment | H-09/H-04 A9/A10 | Suspension/kill request | Self-release/exception; C4; H-09 |
| PRT-01 | Portfolio analyst; RV/RC | H-05 | Admission eligibility | Strategy validation; C3; H-05 |
| PRT-02 | Portfolio agent/analyst; RV/RC | H-05 AP; H-04 risk | Portfolio evidence/decision | Capital execution; C4; H-05 |
| MON-01 | Monitor/QA; MO/P/RQ | H-08/H-09 escalation | Health alert | Retune; C3; domain AC |
| MON-02 | Monitor/Risk; MO/P/RQ | H-04/H-06 | Decay report | Reactivate/replace; C4; H-04 |
| MON-03 | Governance Monitor; MO/P/ES | H-02/H-09 | Governance alert | Remedy approval; C4; H-02 |
| ORC-01 | Experiment Orchestrator; CO/RQ/RE | Workflow owner | Task/workflow; GOV | Create authority; C3; domain AC |
| ORC-02 | Orchestrator; RV eligibility/CO | Domain gate owner | Eligibility record | Admit/validate; C3; domain AC |
| ORC-03 | Orchestrator; CO/RQ/RE | Original transition authority | Transition record; H-02 | Authorize/release; C4; domain AC |
| AUD-01 | Registry/Curator; CU/RE | H-10 oversight | Artifact records | Science/decision; C3; H-10 |
| AUD-02 | Registry/Curator; CU/RE | H-10/evidence owner | Evidence custody | Admission solely by storage; C3; H-10 |
| AUD-03 | Audit system/QA; CU/RE/CH audit | H-10 | Audit/lineage | Authorize event; C4; H-10 |
| HUM-01 | Interface system/operator; RQ/RE | H-11 identified | Command record; authority owner | Waive guards; C3; H-11 |
| HUM-02 | Interface support; RE/CO | Named H-01..H-10 authority | Approval/halt record | Impersonate human; C4; named AC |
| EXE-01 | Boundary only; observe/reject/route | H-01/H-03/H-04 future | Closed-boundary record | Any execution; C4; H-01 |

## 24. Workflow Responsibility Matrix

| Workflow | Initiator / producer | Reviewer/challenger/validator | Recommender / authorizer | AC / recorder / escalation | Prohibited combination |
|---|---|---|---|---|---|
| WF-01 Research | H-07/Research/QSA | RES-03/QA | Research RC; EXP-03 later AU | H-07/AUD; GOV | Research self-promotes |
| WF-02 Data | H-08/Data/Librarian | DAT-03/QA | Data eligibility authority | H-08/AUD | Builder self-qualifies |
| WF-03 Experiment | EXP/QSA/Engineer | EXP-03 eligibility; VAL later | EXP-03 AU run only | H-07/AUD; GOV | Experiment validates |
| WF-04 Validation | VAL-01 | Independent VAL/VAL-05 | VAL-06 VA/RC | H-06/AUD; H-06/GOV | Producer sole validator |
| WF-05 Evidence | Producer | Domain reviewer/challenger | Evidence reviewer admits | Evidence AC/AUD-02 | Storage=admission |
| WF-06 Decision | DEC-01 | Specialist reviewers/challenger | DEC Agent RC/A8 bounded; H-03 reserved AP | H-03/AUD; H-01 | Recommender fabricates authority |
| WF-07 Risk | DEC/PRT/MON | RSK-01/challenger | Risk Agent RC; H-04 reserved AU | H-04/AUD; H-09 | Assessor approves own exception |
| WF-08 Portfolio | PRT-01 | PRT-02/RSK | Portfolio RC; H-05 AP | H-05/AUD; H-03 | Analyst allocates capital |
| WF-09 Monitoring | MON | Domain/Risk/GOV | MON requests only | Domain AC/AUD; H-09 | Monitor retunes/reactivates |
| WF-10 Governance | Any detector/GOV | H-10/challenger | H-02/H-01 AU | H-02/AUD | Requester self-approves |
| WF-11 Artifact | Producer/owner | Domain reviewer | Field/lifecycle authority | Domain AC/AUD-01 | Custodian changes verdict |
| WF-12 Exception | Requester | Risk + Governance + H-10 | Independent H-02/H-01 AP | H-02/AUD | Requester=final AP |
| WF-13 Invalidation | Detector/owner | Domain/challenger | Competent domain authority | Domain AC/AUD | Producer silently invalidates |
| WF-14 Quarantine | Custodian/detector | Domain/GOV | Named release authority | H-10/AUD | Custodian self-releases science |
| WF-15 Recovery | Remediator | Original gate reviewer | Original authority | Original AC/AUD | Retry bypasses gate |
| WF-16 Execution | Future governed readiness | VAL/RSK/PRT/GOV/H-10 | Human H-01/H-03/H-04 only | H-01/AUD; H-09 | Any Phase 2 activation |

## 25. State Axis Authority Matrix

| Axis | Observe | Request/challenge/review/recommend | Authorize / record | Contain/invalidate/escalate |
|---|---|---|---|---|
| AX-01 Workflow | Participants | Participants / owner / gate | Workflow authority / ORC-03-AUD | GOV/domain AC |
| AX-02 Artifact | Permitted consumers | Producer/challenger/domain reviewer | Field/lifecycle authority / AUD-01 | Domain authority / H-10 |
| AX-03 Evidence | Permitted consumers | Producer/consumer/challenger/evidence reviewer | Competent EES reviewer / AUD-02 | Evidence/domain authority / GOV |
| AX-04 Validation | Eligible consumers | Candidate owner/VAL-05/VAL reviewers | H-06/qualified VAL authority / AUD | VAL/GOV; not producer |
| AX-05 Decision | Authorized stakeholders | DEC-01/challenger/specialists | DEC role within contract; H-03 reserved / AUD | H-03/H-01 |
| AX-06 Risk | Authorized stakeholders | DEC/PRT/MON/RSK | H-04 or delegated bounded RSK / AUD | H-04/H-09 |
| AX-07 Portfolio | Authorized stakeholders | PRT/MON/RSK | H-05 / AUD | H-05/H-04 |
| AX-08 Monitoring | Permitted users | MON/domain reviewer | Observation classification only / AUD | H-09/domain authority |
| AX-09 Governance | Authorized users | Any detector/H-10/GOV | H-02/H-01 / AUD | H-02/H-09/H-01 |
| AX-10 Execution | Governance/readiness roles | Governed future request/challenge/review | No Phase 2 authority / AUD | H-09/H-01; remains closed |

Recorder never authorizes by implication. Reversal is a new governed transition, not deletion.

## 26. Agent Responsibility Matrix

| Agent | Purpose/domains; inputs→outputs | Max level/classes | Restrictions, evidence, challenge/escalation, supervision, ceiling |
|---|---|---|---|
| Market Research Agent | Market research; sources/data→research evidence | L3; A0–A5 | No experiment/validation/approval; provenance; H-07; C2 |
| Research Librarian Agent | Acquire/cite sources→source records | L3; A0–A4 | No interpretation/knowledge admission; H-08/H-02; C2 |
| Knowledge Curator Agent | Govern admitted knowledge lifecycle | L5; A0–A5, bounded A7 knowledge | Repetition≠evidence; no science/risk/decision; H-02; C3 |
| Quant Strategy Architect | Hypothesis/market evidence→strategy architecture/spec | L3; A0–A5 | No implementation validation/approval; H-07; C2 |
| Quant Strategy Engineer | Approved spec→versioned implementations/parity inputs | L3; A0–A5 | No research change/self-validation/deploy; H-07/H-06; C2 |
| Experiment Orchestrator Agent | Approved experiment→complete run package | L4; A0–A5, bounded A7 operational | No scientific intent/validation/risk/decision; H-07; C3 |
| Validation Agent | Frozen evidence→validation evidence/verdict | L5; A0–A6, bounded A7 validation | Independent instance/context; no own-production validation/risk/deploy; H-06; C3 |
| Risk Governance Agent | Validation/context→risk analysis/limits/escalation | L5; A0–A5, bounded A7/A9 | No own exception, executive decision, kill/release or execution; H-04/H-09; C4 analysis |
| Executive Decision Agent | Specialist packages→decision synthesis/bounded outcome | L6; A0–A5, A8 only per superior contract | Name grants nothing; reserved/C4 capital actions need H-03; no evidence/risk rewrite/execution; C4 support |
| Pine Agent | Approved engineering task→Pine artifact | L2; A0–A3 | No strategy authority/self-parity/deploy; H-07/H-06; C2 |
| Python Agent | Approved engineering task→Python artifact | L2; A0–A3 | No scientific/validation/deploy authority; H-07/H-06; C2 |
| QA Agent | Artifacts/evidence→quality/parity/audit findings | L4; A0–A5 | Cannot be sole validator of own work or authorize because tested; H-06/H-10; C3 |
| CEO Agent | Approved priorities/resources→institutional recommendation | L5; A0–A5, bounded A7 if contract grants | Not Founder/human executive by name; no science/risk/execution override; H-03/H-01; C4 support |

Every agent output identifies role/instance/model/contract/task/context, exact inputs, limitations and authority. Contract breach stops work, preserves evidence and escalates.

## 27. Human Role Matrix

| Role | Authority / non-delegable power | Delegable work / review-conflict duty | Emergency / audit / expiry / prohibitions |
|---|---|---|---|
| H-01 System Owner | Constitutional/reserved change; EXE opening | Analysis delegated, decision not | Final escalation; immutable record; no evidence rewrite |
| H-02 Governance | A4/A7; material exception with H-01 where reserved | Policy analysis delegated; independent review | Governance containment; term/scope bound |
| H-03 Executive | A8; C4 institutional/capital decision | DEC package/recommendation delegated | Escalates to H-01; cannot replace specialists |
| H-04 Risk | Risk acceptance/override; A9 as scoped | Analysis/monitoring delegated | Kill review with H-09; cannot validate science |
| H-05 Portfolio | Portfolio admission/capital-context approval | Exposure analysis delegated | Capital authorization remains reserved; no execution |
| H-06 Validation | A6 final validation ownership | Methods may be delegated to independent VAL instances | Must disclose conflicts; cannot validate own product |
| H-07 Research | Research scope and experiment sponsorship | Research/engineering delegated | No self-validation/promotion |
| H-08 Data Steward | Source/data eligibility and custody exceptions | QC/build work delegated | Provenance non-waivable; no edge claim |
| H-09 Emergency | A9/A10 and independent release | Detection/triage delegated | Every action immediate audit; authority expires by event/scope |
| H-10 Auditor | A3/A4 audit findings and closure review | Inspection delegated under independence | Cannot authorize recorded event |
| H-11 Operator | A0–A2 within permission | Routine commands only | No emergency release/override; session/task expiry |

## 28. Delegation Model

Every delegation records delegator/delegate identities and roles, authority source, exact power/scope/objects, workflow/axis, evidence, start/expiry, revocation, escalation, criticality ceiling, subdelegation flag and audit ID. Default: no implied, transitive or tool-based authority; no subdelegation unless expressly allowed. Delegator remains accountable for scope and supervision, not for fabricated delegate actions beyond authorization.

## 29. Agent-to-Agent Delegation

Agents may delegate bounded tasks only inside an authorized workflow when contracts permit. The receiving agent uses its own existing authority ceiling; task delegation does not transfer the sender’s authority. Agents cannot subdelegate non-delegable powers, create institutional roles or enlarge another contract. Handoffs preserve exact evidence, context exposure, limitations and accountability.

## 30. Human-to-Agent Delegation

Humans may delegate research, source acquisition, analysis, evidence preparation, experiment preparation/coordination, governed validation execution, recommendation preparation, monitoring and incident triage. They may delegate bounded domain actions only where superior contracts permit. Section 14 powers, final capital risk, kill release, constitutional bypass and A11 cannot be delegated.

## 31. Authority Expiry and Revocation

Authority may be time-, workflow-, object-, task-, state-, evidence-version- or emergency-bounded. It records effective interval and revoker. Changed state/version, completed task, expired review, superseded policy, conflict or incident may terminate it. Expired, revoked, stale or superseded authority fails closed; replay does not renew it. Revocation preserves historical actions and triggers dependent review.

## 32. Emergency Authority

HOLD pauses progression; SUSPEND withdraws eligibility; HALT immediately stops affected activity; KILL terminates capital-affecting authority; RELEASE ends containment; REACTIVATE grants a new bounded active status. Detector/MON/agent may request and a predeclared system may trigger risk-reducing fail-safe containment; H-09/H-04 confirms. Release/reactivation requires an independent named authority, resolved cause, new evidence, risk review and audit. Halter is never automatically releaser.

## 33. Kill-Switch Governance

MON/RSK/operator may request kill; only H-09/H-01 or future explicitly named non-delegable authority may authorize A10. Automated systems may trigger fail-safe HALT under predeclared conditions but not KILL institutional authority, unless superior future governance explicitly defines human-confirmed semantics. Escalation reaches H-09/H-04/H-01. Release is a separate C4 decision. False positives produce review without deleting the incident; missed conditions trigger audit/risk review. No execution mechanism is implemented.

## 34. Governance Exception Responsibility

Exception requester, analyst, H-04 risk reviewer, H-10 governance reviewer, H-02/H-01 authority, accountable human and AUD-03 recorder are separate assignments. Requester cannot finally approve. Exception is scoped, expiring, compensated, evidenced and cannot rewrite history, provenance or non-waivable controls.

## 35. Validation Responsibility

VAL actors inspect, challenge, perform governed validation, produce evidence and recommend/issue a validation disposition only within A6 and their contract. AUD-02 separately handles custody/admission metadata; DEC, RSK, PRT and future deployment remain separate. A strategy producer, implementation author, optimizer or contaminated agent instance cannot be its own sole final validator.

## 36. Executive Decision Responsibility

The Executive Decision Agent may synthesize evidence, expose contradictions, prepare alternatives and issue only those bounded decisions expressly granted by its superior contract and current delegation. Its name does not prove identity or human authority. DEC-02 actions involving constitutional/founder-reserved matters, unresolved critical contradiction, material C4 capital/risk, production deployment or EXE-01 require H-03 and, as applicable, H-01/H-04 final authority. The agent cannot fill missing specialist verdicts.

## 37. Risk Governance Responsibility

Risk analysis (agent permitted), recommendation (agent permitted), risk acceptance (H-04 or explicitly delegated bounded non-capital case), exception (independent H-02/H-01), escalation (agent permitted), containment request/limited fail-safe (agent/system permitted), kill (H-09/H-01) and release (independent H-09/H-04) are distinct. Risk Governance Agent does not automatically own the chain.

## 38. Portfolio Responsibility

PRT-01 governs candidate eligibility; analysts/agents may produce correlation, exposure and dependency evidence and recommendations; H-05 owns portfolio admission. H-04 owns risk constraints. Live capital allocation and execution are absent and non-delegable in Phase 2. Individual approval never implies portfolio or capital eligibility.

## 39. Monitoring Responsibility

Monitoring may observe, detect, classify, report, request review/HOLD/HALT and escalate. It cannot retune, reoptimize, revalidate, reapprove, reactivate, change limits/portfolio or execute. Remediation belongs to the original domain workflow and must re-pass gates.

## 40. Orchestration Responsibility

ORC sequences, routes, coordinates, checks eligibility, requests work, records workflow status and routes failure/escalation. It cannot invent authority, validate claims, admit evidence, approve risk/portfolio/deployment, override holds, bypass missing evidence or self-authorize transitions.

## 41. Audit Responsibility

AUD-01/02/03 identify, register, preserve, link, reconstruct and expose lineage/authority records. They cannot validate science, admit evidence merely because stored, approve decisions/risk, authorize transitions or execution. Recording is evidence of an authority action, not its source.

## 42. Knowledge & Memory Responsibility

Lifecycle: `TRANSIENT OUTPUT → PROPOSED KNOWLEDGE → REVIEWED KNOWLEDGE → ADMITTED KNOWLEDGE → SUPERSEDED or INVALIDATED KNOWLEDGE`. KNW preserves exact sources, context, challenge, authority and consumer impacts. Agent memory, chat history, repetition and previous output are not institutional truth. Curator admission does not validate market claims.

## 43. Authority Failure Modes

Unknown/ambiguous actor; expired/revoked/stale authority; wrong scope/workflow/object/state/criticality; missing human authority; prohibited/transitive delegation; self-approval/self-validation; conflict or missing independence; unauthorized emergency release; authority inferred from tool, name, access, consensus or success; missing audit; and inconsistent authority records all **FAIL CLOSED**. Responses are reject, hold, quarantine, reassign, escalate and preserve evidence.

## 44. Authority Quarantine

When authority cannot be proven, the consequential action is blocked, the last valid state remains, evidence/history is preserved, the request enters quarantine and H-02/H-10 or the named human owner reviews it. No retry expands authority. Release requires reconciled identity/source/scope/delegation/current versions, independent review, explicit authorization and AUD-03 record; otherwise reject or retain quarantine.

## 45. Responsibility Gap Detection

Future conformance checks must detect no AC, competing authorities, circular chains, orphan approval, unowned escalation/release/invalidation/transition/admission/C4 action. The owner of the affected workflow holds the action and routes H-02 when a gap appears. No default “system owner” catch-all silently fills it.

## 46. Responsibility Overlap Detection

| Overlap | Classification / treatment |
|---|---|
| Multiple monitors/detectors | VALID REDUNDANCY; one routed incident identity |
| RES-03 and VAL-05 challenge | INDEPENDENT CHALLENGE; retain scopes |
| AUD/KNW custody references | SEPARATION OF DUTIES; no verdict transfer |
| VAL method contributors | VALID specialist overlap; VAL-06 owns aggregate verdict |
| DEC Agent and H-03 decision | Delegated/support overlap; exact authority decides |
| RSK Agent, H-04 and H-09 emergency | Separation of analysis/contain/release |
| Multiple actors claiming final AP | AMBIGUOUS AUTHORITY; quarantine |
| Requester also exception/kill release AP | PROHIBITED OVERLAP |

## 47. C3/C4 Governance Resolution

**P2-OQ-002, A-OQ-002, S3-OQ-02, S3-OQ-07, S4-OQ-01 and S4-OQ-02 are governed at planning level.** C3 requires named AC, exact authority and independent review when irreversible, conflicted, exception-bearing or validation/decision-bearing. Routine reversible C3 may use qualified agent A7 only under explicit superior contract/delegation. C4 always requires human review; final human authority is mandatory for capital/safety, constitutional/reserved exceptions, A10/A11, material risk override and emergency release. Agents/systems may only perform predeclared risk-reducing containment pending review. Low-criticality producer-reviewer combination is allowed only for routine C0/C1, with disclosure, policy, versioned audit and no promotion/validation/exception effect.

## 48. Prohibited Authority Chains

Twenty prohibited classes: `AGENT_OUTPUT→FINAL_APPROVAL`; `TOOL_ACCESS→AUTHORITY`; `IDENTITY→AUTHORITY`; `REGISTRY_ENTRY→APPROVAL`; `EXPERIMENT_SUCCESS→VALIDATION_AUTHORITY`; `VALIDATION→EXECUTION_AUTHORITY`; `DECISION_RECOMMENDATION→CAPITAL_AUTHORITY`; `MONITOR_ALERT→RETUNE`; `MONITOR_ALERT→REACTIVATE`; `RISK_ANALYSIS→OWN_EXCEPTION_APPROVAL`; `EXCEPTION_REQUEST→SELF_APPROVAL`; `HALT_AUTHORITY→AUTOMATIC_RELEASE`; `ORCHESTRATION→AUTHORIZATION`; `AUDIT_RECORD→AUTHORIZATION`; `HUMAN_COMMAND→CONSTITUTIONAL_BYPASS`; `AGENT_NAME→EXECUTIVE_AUTHORITY`; `MULTI_AGENT_VOTES→HUMAN_AUTHORITY`; `PREVIOUS_SUCCESS→FUTURE_AUTHORITY`; `MODEL_CONFIDENCE→GOVERNANCE_AUTHORITY`; `STATE_RECORDING→STATE_AUTHORIZATION`.

## 49. Multi-Agent Consensus

Agent consensus can broaden evidence diversity, challenge coverage and recommendation confidence. It cannot manufacture executive, risk, constitutional, execution or human authority. Votes record eligible identities, instance/context independence, abstentions, dissent and authority. One hundred unauthorized agents still equal zero authorization—democracy is lovely, but governance arithmetic is ruthless.

## 50. Human Override

Every override records authority source, scope, affected guard, rationale/evidence, risk, contradictions, expiry/review, downstream effects and audit. Candidate non-waivable categories are constitutional constraints, explicit identity, provenance integrity, auditability of consequential action, execution isolation, truthful evidence, prohibition on fabricated/retroactive authority, and required SoD against self-approval. A human may contain risk but cannot declare missing facts to exist.

## 51. Future Execution Boundary

EXE-01 remains `PLANNED_CLOSED`. No agent, module, interface, orchestrator or presently documented human role receives A11 merely because future roles are described. Opening requires separate governance, implementation readiness, validation, risk, portfolio, monitoring, deployment and explicit non-delegable human authorization. Sprint 5 creates no order, capital or execution power.

## 52. Responsibility Traceability Matrix

| Constitutional requirement | Charter | Sprint 2 | Sprint 3 | Sprint 4 | Sprint 5 / class / human | Future test |
|---|---|---|---|---|---|---|
| Capability≠authority | Proposal/authority | IAM/GOV | Custody roles | Authority Guard | Actor record; A0–A11; H-02 | Tool/name/access bypass |
| Independent validation | Validation planning | EXP≠VAL | SoD | WF-04/AX-04 | H-06/VAL; A6 | Self-validation/context |
| Evidence before decision | Evidence Package | AUD/DEC | Admission/claim | WF-05/06 | DEC-01/02; A4/A8; H-03 | Missing/stale evidence |
| Risk/portfolio separation | Risk dependencies | RSK/PRT | Separate gates | WF-07/08 | H-04/H-05 | Cross-domain authority |
| Explicit state authority | State planning | ORC/AUD | Transition records | AX-01..10 | AU vs RE separation | State self-authorization |
| Human accountability | Responsibility planning | HUM | Human evidence | C3/C4 paths | H-01..11/AC | Human-required gates |
| Emergency containment | Fail closed | RSK/MON/HUM | Kill records | A9/A10 routes | H-09; separate release | Halt/kill/release |
| Execution isolation | Non-goals | EXE-01 | Prohibited use | WF-16/AX-10 | A11 prohibited; H-01 reserved future | Execution boundary |
| Auditability | Traceability | AUD-03 | Reconstruction | Audit Guard | H-10/RE not AU | Audit-authority bypass |

Every C3/C4 path resolves through this chain; missing linkage triggers authority quarantine.

## 53. Future Test Obligations

Sprint 6 shall plan positive/negative tests for actor/role identity; authority resolution and scope; delegation, expiry/revocation and non-delegable powers; self-approval/self-validation; conflicts and context independence; criticality; human-required/final gates; agent ceilings; emergency halt/release/kill; exceptions; state authorization; audit/ORC/MON separation; consensus/tool-access non-authority; quarantine/fail-closed; responsibility gaps/overlaps and end-to-end reconstruction. No tests are implemented here.

## 54. Planning ADRs

| ADR | Context / decision | Rationale / alternatives | Consequences | Constitutional basis |
|---|---|---|---|---|
| S5-ADR-01 | Capability ≠ authority | Performance-based power rejected | Explicit grant needed | Agent Framework |
| S5-ADR-02 | Identity ≠ authority | Authentication-only model rejected | IAM split | Sprint 2 IAM |
| S5-ADR-03 | Role ≠ instance | Named duplicate as independence rejected | Instance/context lineage | Agent Registry/EES |
| S5-ADR-04 | Recommendation ≠ decision | Agent confidence rejected as AP | Separate A5/A8 | Decision OS |
| S5-ADR-05 | Human presence ≠ authority | Owner-said-so rejected | Attributable scope | Charter |
| S5-ADR-06 | Delegable vs reserved powers | Unlimited delegation rejected | Fourteen human powers | Constitutional governance |
| S5-ADR-07 | C3 is conditional human/hybrid | All-human and all-agent extremes rejected | Named AC + risk-based independence | Sprint 4 |
| S5-ADR-08 | C4 human boundary | Autonomous final capital/safety rejected | Human review and reserved final power | Risk/Deployment |
| S5-ADR-09 | Validation independence | Same producer-validator rejected | Context/role/module separation | VEP |
| S5-ADR-10 | Halt ≠ release | Containment actor self-reactivation rejected | Independent release | EDRP/RRP |
| S5-ADR-11 | Recorder ≠ authorizer | Audit-as-power rejected | AUD preserves only | Sprint 2 AUD |
| S5-ADR-12 | ORC ≠ authority | Scheduler promotion rejected | Coordination only | WOE |
| S5-ADR-13 | Monitor ≠ remediation authority | Auto-retune rejected | Request and route | MEDS |
| S5-ADR-14 | Consensus ≠ authority | Vote-created legitimacy rejected | Evidence only | Decision OS |
| S5-ADR-15 | Tool access ≠ authority | Capability-based permission rejected | IAM/delegation required | Agent Framework |
| S5-ADR-16 | Human override is bounded | Omnipotent admin rejected | Non-waivable candidates | Constitution/Charter |
| S5-ADR-17 | EXE authority remains absent | Planning-created deployment rejected | A11 prohibited | EXE-01/DGS |
| S5-ADR-18 | Accountable human for reserved C3/C4 | “System accountable” rejected | Named consequence owner | IOP/Charter |

These are reversible planning decisions only through governed change and create no executable permission.

## 55. Open Questions Register

| ID | Question / source | Actor/module/workflow/axis | C / severity | Status / default | Competent authority | Target / resolution |
|---|---|---|---|---|---|---|
| S5-OQ-01 | Exact catalog of routine reversible C3 actions eligible for agent A7? S4-OQ-01 | Agents; GOV/IAM; all; AX-09 | C3/High | Non-blocking plan; BLOCK until cataloged | Agent/Governance H-02 | Sprint 6 tests then domain plans |
| S5-OQ-02 | Quantitative independence scoring for shared model/context ancestry? S4-OQ-04 | VAL/QA; WF-04; AX-04 | C3/High | Non-blocking; failed independence until evidenced | H-06 + Evidence Governance | Sprint 6 test architecture |
| S5-OQ-03 | Exact automatic fail-safe triggers and confirmation windows? S4-OQ-05 | MON/RSK/H-09; WF-09/16; AX-08/10 | C4/High | Non-blocking while EXE closed; manual/escalate | H-04/H-09/H-01 | Sprint 10 monitoring plan |
| S5-OQ-04 | Freshness policies by evidence class? S4-OQ-03 | MON/VAL/RSK; WF-05/09; AX-03 | C2-4/Medium | Non-blocking; treat trigger as HOLD | Evidence/domain authority | Sprints 9–10 |
| S5-OQ-05 | Controlled IDs/state reconciliation mechanics? S4-OQ-06 | IAM/ORC/AUD; all axes | C3/Medium | Non-blocking; ambiguity quarantined | Workflow/Artifact Governance | Sprint 6/future spec |
| S5-OQ-06 | Retention/legal constraints? S4-OQ-07/P2-OQ-004 | H-08/H-10; DAT/AUD; all | C2-4/Medium | Non-blocking; no disposal if dependency | Legal/data/artifact authority | Sprint 7/later plan |
| S5-OQ-07 | Exact independent composition of Phase 2 exit review? P2-OQ-006 | H-01/02/06/10; GOV/AUD; WF-10 | C4/High | Non-blocking Sprint 5; blocks Sprint 12 exit | Existing governance authority | Sprint 12 |

Earlier state/artifact questions resolved in Sprints 3–4 remain closed. Relevant responsibility questions are governed here; these seven refinements remain explicit and fail closed within their affected paths.

## 56. Sprint 6 Handoff Contract

Sprint 6 receives 13 agent roles, 11 human roles, 8 autonomy levels, 12 authority classes, 46 module assignments, 16 workflow assignments, 10 axis mappings, SoD/non-delegable rules, emergency/release separation, quarantine and seven open questions. It must design tests for permissions, ceilings, human gates, independence, delegation, failures, emergency authority and audit reconstruction without implementing them, and prioritize S5-OQ-01, S5-OQ-02 and S5-OQ-05.

## 57. Definition of Done

Actor/role taxonomies, authority/autonomy classes, enriched responsibility roles, SoD/independence/conflicts, human accountability, C0–C4 rules, all 46 modules, 16 workflows, 10 axes, 13 agents and 11 humans are mapped; delegation/expiry/emergency/kill/exception boundaries exist; non-delegable powers and prohibited chains are explicit; monitoring/ORC/AUD/consensus/tool access cannot create authority; human override is bounded; EXE-01 remains closed; tests and classified questions are handed to Sprint 6. No critical authority ambiguity is hidden and no implementation exists.

## 58. Final Sprint Disposition

**SPRINT 5 COMPLETE WITH OPEN GOVERNANCE ITEMS**

Blocking issues: **0 for Sprint 5 planning**. Seven bounded questions remain; each affected future implementation path fails closed until resolved. After governance review and merge, the next step is **Phase 2 — Sprint 6: Test Architecture Plan**.
