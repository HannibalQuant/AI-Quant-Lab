# AI Quant Lab — Test Architecture Plan v1.0

## 1. Document Status

| Field | Value |
|---|---|
| Phase / Sprint | Phase 2 — Sprint 6 |
| Status | Proposed for governance review |
| Canonical path | `planning/TEST_ARCHITECTURE_PLAN_v1.md` |
| Constitutional baseline | AI Quant Lab v1.0, tag `v1.0`, commit `50b61266f880cb9657b7f1b477d3d90825fe013f` |
| Sprint 1–5 baseline | Merges `82b683d`, `f7d2d46`, `3f887e9`, `f65aceb`, `3ddc2c0` |
| Version | 1.0 |
| Implementation / execution authority | None; EXE-01 remains `PLANNED_CLOSED` |

This is a non-executable planning contract. It creates test obligations, not tests, permissions, implementation readiness, scientific truth or deployment authority.

## 2. Purpose

Define how future implementation will prove conformance to constitutional, module, artifact, evidence, workflow, state, authority, scientific, temporal, reproducibility, containment and audit requirements. A technically correct result produced unlawfully is a failed institutional test.

## 3. Authority and Inheritance

Authority descends: Constitutional Baseline → Implementation Planning Charter → Module Boundary Architecture → Artifact & Evidence Contract System → Workflow & State Transition Blueprint → Agent/Human Responsibility Matrix → this plan → future test specifications and evidence. A lower test or oracle cannot weaken a superior rule. Conflicts fail closed and are escalated rather than encoded as convenient expected behavior.

## 4. Scope

The plan covers 38 test families, eight levels, all 46 modules, 16 workflows, 10 state axes, 12 authority classes, 13 agents, 11 human roles, C0–C4, artifacts/evidence, independence, delegation, data/time, reproducibility, validation-of-validation, failures/recovery, concurrency/replay, emergency controls, isolation, coverage, gates, oracles and audit reconstruction.

## 5. Non-Goals

No executable test, code, schema, fixture, runner, CI job, API, database, state machine, agent, strategy, parameter, backtest, validator, monitor, broker/exchange connection, paper/live trading, deployment or execution capability is created. No numerical scientific, independence, freshness or trading threshold is selected.

## 6. Governing Testing Principles

1. Every governed requirement has a positive, negative or documentary conformance obligation.
2. Every C3/C4 authority path has negative and bypass tests.
3. Test evidence is versioned, attributable, reproducible and challengeable.
4. PASS means only the named test passed its exact scope and versions.
5. Missing oracle, evidence, authority, independence or lineage fails closed.
6. Negative results and failed trials remain visible.
7. Recovery re-passes the failed gate; retry never expands authority.
8. CI, code coverage, consensus and tool access do not create authority.
9. Determinism is claimed only where justified; stochastic and agent behavior use attributable invariants.
10. EXE-01 isolation is tested negatively throughout Phase 2.

## 7. Terminology

| Term | Meaning | Does not mean |
|---|---|---|
| Test obligation | Governed future verification duty | Executable test |
| Test case | Versioned documentary stimulus/oracle/expected outcome | Authority |
| Oracle | Independent source of expected result or invariant | Component under test |
| Test evidence | Raw and derived proof of a run | Governance approval |
| Coverage | Mapped obligations exercised | Correctness by percentage |
| Gate | Distinct readiness disposition backed by evidence | Deployment permission |
| Negative test | Proves forbidden behavior fails safely | Absence of happy-path failure |
| Meta-test | Verifies test system detects seeded defects | Self-certification |

## 8. Test Taxonomy

| ID | Family | Primary obligation |
|---|---|---|
| T01 | Unit | Isolated deterministic behavior |
| T02 | Module Contract | Inputs, outputs, limits and failures |
| T03 | Integration | Allowed multi-module interaction |
| T04 | Artifact Contract | Identity, lifecycle, version and freeze |
| T05 | Evidence Contract | Provenance, scope, admission and contradictions |
| T06 | Workflow | Gate order and cross-workflow boundaries |
| T07 | State Transition | Legal state movement and guards |
| T08 | Authority | Identity, scope and competent authority |
| T09 | Human-Gate | Required and final human actions |
| T10 | Agent-Ceiling | Autonomy/class ceilings and name/tool non-authority |
| T11 | Segregation-of-Duties | Prohibited role combinations |
| T12 | Independence | Actor, context, data and implementation separation |
| T13 | Delegation | Explicit bounded non-transitive grants |
| T14 | Expiry / Revocation | Stale/revoked authority rejection |
| T15 | Data Integrity | Source, quality, transformations and locks |
| T16 | Temporal Integrity | Availability and causal ordering |
| T17 | Reproducibility | Inputs through decision reconstruction |
| T18 | Determinism | Repeatability or attributable stochasticity |
| T19 | Regression | Preserved governed behavior across versions |
| T20 | Validation Architecture | Method and boundary correctness |
| T21 | Negative-Control | Known-no-edge rejection |
| T22 | Adversarial | Deliberate bypass and contamination |
| T23 | Failure-Path | Detect, contain, route and record |
| T24 | Recovery | Re-pass original gates and preserve history |
| T25 | Audit Reconstruction | Full causal/authority reconstruction |
| T26 | Knowledge / Memory | Admission, provenance and contamination |
| T27 | Monitoring Boundary | Observe/request, never retune/reactivate |
| T28 | Orchestration Boundary | Coordinate, never authorize |
| T29 | Emergency Authority | HOLD/SUSPEND/HALT/KILL/RELEASE roles |
| T30 | Kill / Release Governance | Separate kill and reactivation authority |
| T31 | Governance Exception | Scope, expiry, SoD and non-waivable guards |
| T32 | Quarantine | Isolation, inspection and governed release |
| T33 | Criticality Enforcement | C0–C4 controls and anti-downgrade |
| T34 | Concurrency | Competing transition safety |
| T35 | Idempotency / Replay | Single effect and stale grant rejection |
| T36 | Version / Lineage | Exact-version links and impact propagation |
| T37 | Execution Isolation | AX-10/WF-16/EXE-01 closed behavior |
| T38 | End-to-End Governance | Requirement-to-audit lawful system path |

## 9. Test Level Model

| Level | Proves | Does not prove |
|---|---|---|
| L-T0 Documentary conformance | Contract completeness and trace links | Runtime behavior |
| L-T1 Isolated component | Local logic for controlled inputs | Module boundary or authority |
| L-T2 Module contract | Module accepts/rejects and emits correctly | Whole workflow safety |
| L-T3 Multi-module integration | Interface and custody boundaries | Consequential authorization |
| L-T4 Governed workflow | Gates, actors, axes and audit path | Adversarial resilience |
| L-T5 Adversarial / failure | Fail-closed containment and recovery | System-wide readiness alone |
| L-T6 System governance | Cross-domain authority/evidence invariants | Execution qualification |
| L-T7 Execution-boundary qualification | Future proof that closed/open boundary behaves as separately governed | A11 or deployment approval |

## 10. Requirement-to-Test Traceability

Every obligation record links immutable requirement ID/version → planning clause → module → artifact/evidence → workflow → axis → actor/authority → test ID/version → oracle → expected failure → run evidence. Missing links mark the requirement `TEST_ORPHANED`, block readiness and route governance review.

| Constitutional obligation | Planning path | System locus | Mandatory test/evidence |
|---|---|---|---|
| Evidence before promotion | Charter evidence; Sprint 3 | AUD-02, WF-05, AX-03 | T05/T06; missing/stale/contradictory evidence evidence |
| Independent validation | Charter; Sprints 2/5 | VAL, WF-04, AX-04, A6 | T11/T12/T20; contamination evidence |
| Explicit authority/state | Sprints 4/5 | IAM/GOV/ORC/AUD, AX-01..10 | T07–T10; unauthorized-transition evidence |
| Reproducibility | Constitution; Sprint 3 | DAT/EXP/VAL/AUD | T17/T18/T25 manifest |
| No hidden failure | Sprint 3 | EXP/VAL/KNW | T05/T21/T23 negative evidence |
| Execution isolation | Charter; Sprints 2–5 | EXE-01, WF-16, AX-10, A11 | P0 T37/T38 rejection evidence |

## 11. Module Test Matrix

All 46 Sprint 2 modules appear. `+/-` means positive plus negative; `ARF` means authority/recovery/failure; every row also requires T02 contract, T19 regression and attributable test evidence.

| Module | C | Required families / positive path | Negative, failure, recovery and prohibited-behavior oracle | Min level / readiness gate |
|---|---:|---|---|---|
| GOV-01 Constitutional & Policy Authority Resolver | C3 | T02,08,33 + valid resolution | Spoofed/invented authority blocked; conflict HOLD/escalate | L-T6 / AUTHORITY_TEST_PASS |
| GOV-02 Governance Gate, Exception & Escalation | C3 | T06,08,11,31 | Self-exception/bypass blocked; scoped recovery | L-T6 / SYSTEM_GOVERNANCE_PASS |
| IAM-01 Actor Identity Registry | C3 | T02,08,36 + unique identity | Collision/name-is-authority blocked; reconcile/quarantine | L-T5 / MODULE_CONTRACT_PASS |
| IAM-02 Authorization & Delegation Resolver | C3 | T08,13,14,33 | Implied/transitive/expired grant blocked | L-T6 / AUTHORITY_TEST_PASS |
| DAT-01 Data Source Registry & Ingestion Boundary | C2 | T02,15,16,36 | Unknown source/provenance blocked; re-register | L-T4 / MODULE_CONTRACT_PASS |
| DAT-02 Raw Data Custody | C2 | T04,15,16,36 | Mutation/loss blocked; preserve/restore by authority | L-T4 / EVIDENCE_CONTRACT_PASS |
| DAT-03 Data Quality & Temporal Integrity | C2 | T15,16,21,23 | Corruption/leakage detected; quarantine/reassess | L-T5 / VALIDATION_TEST_PASS |
| DAT-04 Dataset Builder | C2 | T02,15,17,18 | Unauthorized transform/version drift blocked | L-T4 / MODULE_CONTRACT_PASS |
| DAT-05 Dataset Registry & Lock | C2 | T04,15,35,36 | Mutable/retroactive lock blocked; new version | L-T5 / EVIDENCE_CONTRACT_PASS |
| RES-01 Research Intake & Hypothesis Registry | C1 | T02,04,06 | Orphan hypothesis/implicit experiment authority blocked | L-T4 / WORKFLOW_TEST_PASS |
| RES-02 Research Evidence & Knowledge Gateway | C2 | T05,17,26,36 | Repetition/orphan evidence rejected; provenance repair | L-T5 / EVIDENCE_CONTRACT_PASS |
| RES-03 Research Challenge Function | C2 | T05,11,12,22 | Self-challenge/hidden dissent blocked; independent reroute | L-T5 / SYSTEM_GOVERNANCE_PASS |
| KNW-01 Knowledge Registry | C2 | T04,05,26,36 | Stored/repeated content treated as truth blocked | L-T5 / EVIDENCE_CONTRACT_PASS |
| KNW-02 Shared Memory Gateway | C2 | T03,08,12,26 | Ungoverned write/context contamination blocked | L-T5 / MODULE_CONTRACT_PASS |
| KNW-03 Provenance, Failure & Learning Gate | C2 | T04–T06,11,17,26,36 | Negative history deletion or agent-output auto-admission blocked | L-T6 / EVIDENCE_CONTRACT_PASS |
| EXP-01 Experiment Intake & Specification Registry | C2 | T02,04,06 | Incomplete spec/revision ambiguity blocked | L-T4 / MODULE_CONTRACT_PASS |
| EXP-02 Dataset & Configuration Lock | C2 | T04,15,35,36 | Retroactive/mismatched lock blocked | L-T5 / EVIDENCE_CONTRACT_PASS |
| EXP-03 Experiment Authorization Gate | C3 | T06–T14,33 | Producer self-authorizes/missing evidence blocked | L-T6 / AUTHORITY_TEST_PASS |
| EXP-04 Experiment Orchestration Boundary | C2 | T03,18,23,28 | Task completion becomes authority blocked; retry gated | L-T5 / WORKFLOW_TEST_PASS |
| EXP-05 Result Collector & Trial History | C2 | T04,05,17,21 | Failed/pruned/excluded trial suppression blocked | L-T5 / EVIDENCE_CONTRACT_PASS |
| EXP-06 Experiment Evidence Packager | C2 | T04,05,17,25 | Best-only/scope expansion blocked; repackage versioned | L-T5 / EVIDENCE_CONTRACT_PASS |
| VAL-01 Validation Intake & Specification | C3 | T02,06,11,12 | Producer-controlled spec/invalid candidate blocked | L-T6 / VALIDATION_TEST_PASS |
| VAL-02 Chronological Validation Boundary | C3 | T16,20,21,22 | Leakage/cutoff violation detected | L-T6 / VALIDATION_TEST_PASS |
| VAL-03 Stochastic & Stress Validation Boundary | C3 | T17,18,20,21 | Missing seed/process or weak control invalidates run | L-T6 / VALIDATION_TEST_PASS |
| VAL-04 Stability & Generalization Boundary | C3 | T20–T22 | Optimizer-chosen winner/self-validation blocked | L-T6 / VALIDATION_TEST_PASS |
| VAL-05 Negative Control, Adversarial & Overfitting Defense | C3 | T20–T22,30 | Known-bad control approval fails system | L-T6 / VALIDATION_TEST_PASS |
| VAL-06 Validation Evidence Aggregator & Disposition | C3 | T05,08,11,12,20 | Aggregator rewrites/source producer validates blocked | L-T6 / SYSTEM_GOVERNANCE_PASS |
| VAL-07 Implementation Parity Boundary | C3 | T02,17,19,23 | Parity mismatch promotion blocked; fix/revalidate | L-T6 / VALIDATION_TEST_PASS |
| DEC-01 Decision Evidence Intake & Support | C3 | T05,06,08,25 | Missing/stale evidence or recommendation-as-decision blocked | L-T6 / AUTHORITY_TEST_PASS |
| DEC-02 Executive Decision Gate | C4 | T07–T12,25,33,38 | Wrong actor/self-approval/no human gate blocked | L-T6 / SYSTEM_GOVERNANCE_PASS |
| RSK-01 Risk Policy & Assessment Boundary | C4 | T02,05,08,20,33 | Science overrides risk/own exception blocked | L-T6 / SYSTEM_GOVERNANCE_PASS |
| RSK-02 Risk Escalation, Kill & Suspension Boundary | C4 | T08,09,23,29,30 | Unauthorized release/ignored kill blocked; independent recovery | L-T6 / SYSTEM_GOVERNANCE_PASS |
| PRT-01 Portfolio Admission Gate | C4 | T06,08,11,33 | Strategy approval implies admission blocked | L-T6 / SYSTEM_GOVERNANCE_PASS |
| PRT-02 Exposure & Portfolio Evidence Boundary | C3 | T05,17,20,33 | Missing dependencies/capital action blocked | L-T6 / EVIDENCE_CONTRACT_PASS |
| MON-01 System, Data & Governance Health | C3 | T23,27,34 | Retune/reactivate/authorize prohibited | L-T6 / SYSTEM_GOVERNANCE_PASS |
| MON-02 Strategy, Evidence, Regime & Edge Health | C3 | T05,20,23,27 | Stale evidence remains eligible blocked | L-T6 / SYSTEM_GOVERNANCE_PASS |
| MON-03 Alert & Escalation Router | C3 | T03,08,27,35 | Alert becomes action/duplicate escalation effect blocked | L-T5 / WORKFLOW_TEST_PASS |
| ORC-01 Workflow Orchestrator & Task Router | C3 | T03,06,08,28,35 | Sequence/completion creates authority blocked | L-T6 / SYSTEM_GOVERNANCE_PASS |
| ORC-02 Dependency & State Transition Coordinator | C3 | T07,23,28,34 | Recorder/ORC authorizes/conflicting state blocked | L-T6 / SYSTEM_GOVERNANCE_PASS |
| ORC-03 Recovery, Retry & Escalation Coordinator | C3 | T23,24,28,35 | Retry bypasses failed gate blocked | L-T6 / FAILURE_PATH_PASS |
| AUD-01 Artifact Registry Boundary | C2 | T04,25,36 | Registration becomes approval/mutation blocked | L-T5 / EVIDENCE_CONTRACT_PASS |
| AUD-02 Evidence Registry & Custody Boundary | C3 | T05,08,25,32 | Storage becomes admission/truth blocked | L-T6 / AUTHORITY_TEST_PASS |
| AUD-03 Audit, Decision, State & Lineage Ledger | C3 | T07,08,25,36 | Recording authorizes/history rewrite blocked | L-T6 / AUDIT_RECONSTRUCTION_PASS |
| HUM-01 Governed Command & Inspection Gateway | C3 | T08,09,14,25 | Tool/human presence/owner-said-so bypass blocked | L-T6 / AUTHORITY_TEST_PASS |
| HUM-02 Approval, Escalation & Emergency Interface | C4 | T09,14,29–31 | Self-approval/undocumented release blocked | L-T6 / SYSTEM_GOVERNANCE_PASS |
| EXE-01 Future Execution Boundary | C4 | T08–T10,29,33,37,38 | Every Phase 2 execution/A11 attempt blocked | L-T7 / EXECUTION_ISOLATION_PASS |

Readiness additionally requires governed requirements, I/O, authority, artifacts/evidence, positive/negative/failure/recovery/audit obligations and no blocking test ambiguity.

## 12. Workflow Test Matrix

Every workflow runs the common suite `H` happy path; `E` missing/stale/invalid/contradictory evidence; `A` wrong/expired/revoked actor-authority; `I` conflict/missing independence; `S` wrong state; `D` duplicate/replay; `C` concurrency; `F` containment; `R` recovery; `U` audit reconstruction.

| Workflow | Specific oracle in addition to H/E/A/I/S/D/C/F/R/U |
|---|---|
| WF-01 Research / Hypothesis | Idea cannot authorize experiment; challenge persists |
| WF-02 Data | Provenance, availability time, quality and lock exactness |
| WF-03 Experiment | Authorization and locks precede run; all trials visible |
| WF-04 Validation | Producer/context independence and frozen inputs |
| WF-05 Evidence | Admission ≠ truth; quarantine/stale/invalid blocks use |
| WF-06 Decision | Validation/recommendation ≠ approval; decision artifact required |
| WF-07 Risk | Scientific success cannot waive risk; exception SoD |
| WF-08 Portfolio | Individual approval ≠ portfolio/capital admission |
| WF-09 Monitoring | Alert may request, never retune/reactivate |
| WF-10 Governance | Policy source exists; recorder/registry not authority |
| WF-11 Artifact Lifecycle | Frozen mutation fails; amendment/supersession preserve history |
| WF-12 Exception | Requester cannot approve; expiry/scope/non-waivable controls |
| WF-13 Invalidation | Contain first; dependency review without destructive cascade |
| WF-14 Quarantine | Normal promotion blocked; release independently authorized |
| WF-15 Recovery | Failed original gate re-passed with new evidence |
| WF-16 Future Execution Eligibility | A11 absent and EXE-01 closed for all actors |

## 13. State Axis Test Matrix

Every axis must pass valid, invalid, unauthorized, stale/missing-evidence, duplicate, concurrent, post-invalidation, quarantined, HOLD, recorder-as-authorizer, ORC-as-authorizer, agent-ceiling, recovery and reconstruction cases.

| Axis | Additional invariant |
|---|---|
| AX-01 Workflow | Request/event is not transition |
| AX-02 Artifact Lifecycle | Frozen history never mutates in place |
| AX-03 Evidence Admissibility | Admissible is neither true nor validated |
| AX-04 Scientific Validation | Experiment success never changes validation automatically |
| AX-05 Decision | Recommendation/validation never creates decision |
| AX-06 Risk | Scientific axis cannot override risk state |
| AX-07 Portfolio | Strategy decision cannot auto-admit portfolio |
| AX-08 Monitoring | Observation cannot mutate governed object |
| AX-09 Governance | Registry/audit/orchestration cannot authorize |
| AX-10 Execution Eligibility | Remains closed; no cross-axis automatic opening |

## 14. Authority Test Matrix

Each class receives positive, negative, boundary, scope, expiry, revocation, delegation, audit and criticality cases.

| Class | Positive proof | Required negative proof |
|---|---|---|
| A0 Observe | Authorized exact-scope read | Read outside identity/scope rejected |
| A1 Produce | Attributed versioned candidate | Production treated as admission rejected |
| A2 Request | Valid object/workflow request | Request treated as transition rejected |
| A3 Challenge | Independent evidenced challenge | Challenge deletes/auto-invalidates rejected |
| A4 Review | Competent scoped review | Reviewer gains approval rejected |
| A5 Recommend | Evidence-bounded recommendation | Confidence/consensus becomes decision rejected |
| A6 Validate | Independent exact-input disposition | Producer/self-validator or execution inference rejected |
| A7 Authorize | Eligible bounded reversible C3 under contract | Any missing S5-OQ-01 dimension blocks |
| A8 Executive approve/reject | Competent decision with required human gate | Agent name/recommendation creates final power rejected |
| A9 Contain/suspend/halt | Predeclared risk-reducing containment | Containment grants release/retune rejected |
| A10 Emergency kill | Named non-delegable human path | Agent/unauthorized kill or self-release rejected |
| A11 Future execution | No positive Phase 2 case | Every invocation fails closed and audits |

## 15. Agent Authority Testing

All 13 roles—Market Research, Research Librarian, Knowledge Curator, Quant Strategy Architect, Quant Strategy Engineer, Experiment Orchestrator, Validation, Risk Governance, Executive Decision, Pine, Python, QA and CEO Agent—receive role/scope/ceiling/self-review/self-validation/self-approval/decision/execution/delegation/context/tool/name/consensus/escalation tests. Empty or placeholder contracts do not grant authority. Executive/CEO names do not create A8–A11; Validation name does not prove independence.

## 16. Human Authority Testing

All 11 roles H-01 System Owner, H-02 Governance, H-03 Executive Decision, H-04 Risk, H-05 Portfolio, H-06 Validation, H-07 Research, H-08 Data Steward, H-09 Emergency, H-10 Auditor and H-11 Operator receive valid-role, wrong-role/scope, expired/revoked, conflict, self-approval, invalid/undocumented override, non-delegable delegation, emergency action/release and constitutional-bypass tests. Human presence is never the oracle for authority.

## 17. Segregation-of-Duties Testing

Negative cases must block and audit: producer→own validator/final approver; experimenter→validator; validator→executive approver; risk assessor→own exception; exception requester→approver; monitor→retune/reactivate; HALT authority→automatic RELEASE; state recorder→authorizer; ORC→authorizer; registry→approval; AUD→authorization; agent recommendation→human decision; identity registration→authorization. Reassignment must preserve the original conflict record.

## 18. Independence Testing

Independence evidence dimensions are actor identity, role, instance, model/provider/version, prompt/contract, context, memory, implementation authorship, data selection, workflow, authority and organizational interest. Signals include stable IDs, hashes/version references, context and memory ancestry, author/selector logs, task separation, conflict declarations and authority records. Mandatory dimension is binary: proven for exact scope or failed. No aggregate score can compensate for a failed non-waivable dimension; numerical thresholds remain deferred.

Cases include the same instance pretending independence, different names sharing context, selected-dataset contamination, producer-authored validation specification, optimizer-selected validation winner and shared-memory contamination. Missing mandatory evidence produces `FAILED_INDEPENDENCE`, HOLD and reassignment. This governs S5-OQ-02 without inventing a production score.

## 19. Delegation Testing

Cases cover valid/no/expired/revoked delegation, wrong delegate/object/workflow/state/criticality, subdelegation, transitive delegation, authority expansion, task-vs-authority confusion, human→agent, agent→agent task handoff and attempted delegation of fourteen reserved human powers. Exact source, scope, object, versions, start/expiry and revoker are oracles. Ambiguity quarantines the request.

## 20. Criticality Testing

| C | Mandatory test emphasis |
|---|---|
| C0 | Identity and attribution |
| C1 | Review/challenge availability and declared self-review |
| C2 | Independent evidence review, provenance and recovery |
| C3 | Named accountable authority, scope, explicit delegation, independence, reversibility, audit and revocation |
| C4 | Human review/final authority where reserved, strongest audit, fail closed and emergency escalation |

Unauthorized C4→C3 or C3→C2 reclassification fails, preserves original classification and escalates governance review.

### S5-OQ-01 Testable A7 Eligibility Contract

A C3 action is A7-eligible only if all mandatory dimensions pass: reversible; bounded object/workflow/state/time; no capital or constitutional effect; no unresolved blocking contradiction, exception or critical invalidation; explicit superior contract and delegation; named accountable human; independent review where required; available revocation/containment; exact evidence/versions; full auditability. Failure of any dimension returns `A7_INELIGIBLE`, blocks autonomous authorization and routes the competent authority. The exact domain action catalog remains open for domain plans; testing semantics are resolved.

## 21. Artifact Contract Testing

T04/T36 cover identity, version, orthogonal status, authority, custody, provenance, lineage, freeze, amendment, supersession, invalidation, freshness, contradiction and retention. Silent frozen mutation, ambiguous supersession, deletion on invalidation, orphaning and consumption of wrong versions must fail. Lawful amendment creates a new version and impact record.

## 22. Evidence Contract Testing

T05 covers missing provenance/lineage, unsupported claims, evidence-scope < claim-scope, stale/contradictory/negative evidence, failed-trial/exclusion suppression, inadmissible/quarantined evidence, out-of-scope use and version mismatch. Promotion fails where the contract requires; admission never establishes truth, validation, decision or execution eligibility.

## 23. Negative Evidence Testing

Packages must preserve failed experiments, rejected hypotheses, failed/pruned/excluded trials with reasons, negative controls, failed robustness/parity, invalidated implementations, adverse regimes, deterioration and rejected decisions. Best-result-only packaging, silent filtering and deletion seed deliberate failures detectable by T05/T21/T62 meta-tests.

## 24. Reproducibility Testing

| Level | Required reconstruction |
|---|---|
| R0 Not reproducible | Missing critical identity or lineage; blocks use |
| R1 Artifact reconstructable | Exact artifact/version/content/status |
| R2 Inputs reconstructable | Dataset/config/source/transforms/environment identities |
| R3 Experiment reproducible | Specification, implementation, seeds/process and raw outputs |
| R4 Evidence reproducible | Derivations, exclusions, validation and package |
| R5 Decision path reconstructable | Actors, authority, contradictions, gates, decision and transitions |

Critical claims specify minimum R-level. Model/prompt/contract/tool/context lineage is required for agent work. A rerun discrepancy is evidence to investigate, not silently averaged away.

## 25. Determinism Testing

Deterministic components require same exact input/version/configuration → same defined output. Stochastic components require seed, generator/process, distribution, configuration and tolerance oracle. Market-data-dependent components pin data identity and availability snapshot. Agent/LLM components record model/provider/version, prompt/contract, context/memory, tools and evidence; tests use invariants, provenance and bounded outcome classes rather than falsely promising bit-identical prose.

## 26. Temporal Integrity Testing

T16 verifies event, effective, observation, availability, decision and record times; cutoff ordering; source availability; transformations; validation/decision chronology; and monitoring chronology. Tests seed lookahead, future leakage, retroactive locks/authorization, delayed/out-of-order events and post-decision evidence misrepresented as prior. Historical correction uses amendment, never timeline rewrite.

## 27. Quant Research Temporal Testing

Future cases explicitly relate signal time, information/feature availability, order-decision time, order-eligibility time, next-bar execution assumption, funding information time and session information time. Known future-leak traps must be rejected. This section defines no signal, strategy, order logic or numerical threshold.

## 28. Validation Test Architecture

T20 verifies the machinery and custody for holdout/OOS, walk-forward, Monte Carlo, bootstrap, parameter stability, temporal/cross-market robustness, cost/slippage sensitivity, perturbation, negative controls, adversarial validation, multiple-testing defense and overfitting diagnostics. It checks exact inputs, method identity, independence, repeatability, exclusions and disposition boundaries—not trading acceptance thresholds.

## 29. Validation-of-Validation

Meta-validation uses governed synthetic cases: known-valid behavior, deliberately overfit/leaking/unstable strategies, random strategies, impossible-alpha controls, shuffled returns, randomized labels, future-leak and parameter-selection traps. A validation component that approves a known-bad control, rejects a required known-good invariant without explanation or cannot reproduce its disposition fails and is quarantined.

## 30. Negative Controls

The future suite includes random entries/exits, shuffled returns, shifted signals, future-leaking control, noise-only features, destroyed temporal order, randomized market labels and parameter permutations. Controls are versioned and hidden from candidate selection where appropriate. The purpose is to prove false edge can be rejected; passing a negative control never proves a real edge.

## 31. Adversarial Testing

T22 attacks governance/evidence bypass, authority spoofing, identity confusion, scope expansion, state corruption, stale reuse, duplicates/replay, agent collusion/consensus abuse, hidden failures, validation contamination, optimizer overfitting, human override and emergency-release abuse. Expected behavior is reject/HOLD/quarantine/escalate with preserved audit, never optimistic continuation.

## 32. Failure Injection

Controlled future injections include missing/corrupt/wrong-version artifacts, missing evidence/authority, revoked/stale delegation, invalid state, module outage, partial workflow, contradiction, monitor/audit outage, ORC retry, validator unavailable and human authority unavailable. Each case specifies detector, containment boundary, expected state, evidence, routing and forbidden side effect.

## 33. Recovery Testing

For each failure, tests prove history persists, invalid action did not apply, HOLD/quarantine and escalation are correct, new evidence is required, the original gate is re-run, authority is lawfully restored/replaced and audit continuity remains. A retry using the same failed basis or broader authority fails.

## 34. Concurrency Testing

Simultaneous approve/invalidate, promote/HOLD, release/HALT, competing decisions, duplicate experiment authorizations, evidence versions, transitions and monitor alerts test ordering and conflict routing. While unresolved, the valid restrictive state dominates progression; there is no destructive auto-merge of authority or evidence.

## 35. Idempotency and Replay

Same request ID + object/version + authority + evidence yields at most one institutional effect and one canonical result with linked repeats. Changed inputs or versions require a new attributable request. Replayed expired/revoked authority, old evidence, old transition or exception fails and audits the attempt.

## 36. Invalidation Testing

Upstream invalidation stops new reliance, preserves history and discovers direct/transitive/decision/portfolio/monitoring/transition dependencies. Tests verify appropriate HOLD, revalidation, decision/risk/portfolio review and baseline suspension without automatic destructive cascading. Invalidated evidence cannot promote.

## 37. Quarantine Testing

Artifact, evidence, authority and workflow quarantine tests ensure normal promotion is blocked, history stays visible, scope does not expand, retries do not bypass, inspection is read-only as governed, and release requires resolved cause, current versions, independent competent authority and audit.

## 38. Monitoring Boundary Testing

Positive tests permit observe, detect, classify, report, request and escalate. Negative tests prohibit retune, reoptimize, revalidate, reapprove, reactivate, change risk/portfolio or execute. A monitoring alert may lead only to a governed request or predeclared risk-reducing containment, never model mutation.

## 39. Orchestration Boundary Testing

ORC may sequence, route, check prerequisites and record progress. Tests reject invented authority, evidence waiver, validation/risk/portfolio approval, HOLD release, “task completed” authorization and recommendation-to-decision conversion. Retry routes back through the original gate.

## 40. Audit Boundary Testing

AUD may register, preserve, link and reconstruct. Tests reject authorization because recorded, validation because stored, approval because reconstructed and historical rewrite. Append-only preservation semantics are tested at the documentary contract boundary; any amendment remains linked and attributable.

## 41. Knowledge and Memory Testing

Tests enforce agent output ≠ knowledge, repetition ≠ evidence and memory ≠ authority; superseded/invalidated knowledge is not silently reused; contradictions persist; provenance survives handoff/restart. Shared-context ancestry and contamination are explicit test inputs.

## 42. Emergency Testing

HOLD, SUSPEND, HALT, KILL, RELEASE and REACTIVATE receive requester/authorizer, fail-safe containment, human confirmation, independent release, audit, false-positive, missed-trigger and conflicting-command cases. Risk-reducing automated HALT may be tested only against a predeclared superior contract; it never creates KILL or release authority.

## 43. Kill Governance Testing

Cases: agent/MON/RSK requests KILL; unauthorized actor attempts KILL; authorized H-09/H-01 decision; agent attempts release; halter self-releases; release lacks evidence/review. Only the governed non-delegable human path can pass A10. No capital or execution mechanism is exercised.

## 44. Governance Exception Testing

Valid bounded exception is contrasted with self-approval, expiry, wrong object/scope, history rewrite, non-waivable bypass, missing risk/governance review and reuse after supersession. Invalid paths fail closed; exception PASS does not change underlying evidence.

## 45. Human Override Testing

Tests distinguish a valid bounded, evidenced, expiring override from undocumented “owner said so,” wrong authority/scope, non-waivable bypass, expired override, contradiction hiding and evidence deletion. Human identity alone is never a pass oracle.

## 46. Multi-Agent Consensus Testing

One, three, ten or all agents recommending leaves institutional authority unchanged absent a separate valid grant. Metamorphic cases increase votes/confidence while requiring identical authority outcome. Dissent and shared-context non-independence remain visible.

## 47. Execution Isolation Testing

P0 T37/T38 cases attempt A11/execution from RES, EXP, VAL, DEC, RSK, PRT, MON, ORC, HUM interfaces, every agent and humans lacking future A11. All must return blocked, preserve state, emit violation/audit evidence and escalate as required. Future L-T7 qualification obligations may be documented later but cannot activate EXE-01.

## 48. Test Evidence Model

Sprint 3 mappings are extended, not replaced: Test Specification maps to Experiment/Validation Specification; Test Case Record is a governed specification subtype; Test Run Manifest maps to Reproducibility Manifest; Test Result and Failure/Regression/Coverage/Authority/Reproducibility/Audit/Adversarial evidence are evidence subtypes; Test Exception Record maps to Governance Exception Record. Each carries artifact identity/version, requirement links, producer, reviewer, environment/input/config/oracle, raw output, exclusions, result, contradictions, lineage, freeze and audit.

## 49. Test Result States

`NOT_RUN`, `PASS`, `FAIL`, `BLOCKED`, `INCONCLUSIVE`, `QUARANTINED`, `STALE`, `SUPERSEDED` are test-result axis states, not artifact lifecycle or governance approval. PASS requires exact test/requirement/system/environment/input/oracle versions and result evidence. Changed basis makes the result stale or creates a new result; it is never edited silently.

## 50. Coverage Model

Coverage dimensions: requirement, module, workflow, state, authority, negative path, failure, recovery, artifact, evidence, agent, human role, criticality, audit and execution isolation. Coverage reports expose missing and excluded obligations. Percentages are descriptive; 100% mapped coverage cannot prove oracle correctness, scientific validity or governance readiness.

## 51. Test Priority Model

| Priority | Scope |
|---|---|
| P0 | Constitutional invariants, non-waivable controls, A10/A11 and execution isolation |
| P1 | Authority, state, evidence, validation, C3/C4 and audit |
| P2 | Workflow, module, data, temporal integrity and reproducibility |
| P3 | Monitoring, knowledge and operational resilience |
| P4 | Convenience and noncritical behavior |

C4 obligations map to P0 or P1. Priority never permits skipping a superior requirement.

## 52. Test Gates

Distinct gates are `TEST_SPEC_READY`, `MODULE_TEST_READY`, `MODULE_CONTRACT_PASS`, `ARTIFACT_EVIDENCE_PASS`, `WORKFLOW_TEST_PASS`, `AUTHORITY_TEST_PASS`, `VALIDATION_TEST_PASS`, `FAILURE_PATH_PASS`, `AUDIT_RECONSTRUCTION_PASS`, `EXECUTION_ISOLATION_PASS`, `SYSTEM_GOVERNANCE_PASS`, `IMPLEMENTATION_TEST_READY`. Each records exact scope/evidence/authority. Passing one never implies another or deployment approval.

## 53. Implementation Readiness

A future module may be designated `IMPLEMENTATION_READY` only after governed requirements, I/O, authority boundaries, artifacts/evidence, positive/negative/failure/recovery/audit plans, traceability and absence of blocking ambiguity are reviewed by competent planning authority. Sprint 6 gives no module that designation and creates no executable capability.

## 54. ID / State Reconciliation Testing

This governs S5-OQ-05 at the test-contract level without selecting syntax. Stable actor, artifact, evidence, workflow, transition, request, authority, delegation, test and run IDs must support uniqueness, immutable identity, explicit version linkage, collision detection/quarantine, replay detection, referential integrity, axis reconciliation and full audit reconstruction. Renaming/display labels cannot change identity or authority. Conflicting mappings block action until governed reconciliation; production ID format remains a future specification decision.

## 55. Test Data Architecture

Future governed categories are synthetic, fixture, historical, adversarial, corrupted, boundary, negative-control, golden/reference, randomized and replay data. Each declares source or generator, version, scope, temporal semantics, sensitivity, expected defects, transformations, custody, retention and allowed tests. Test data cannot silently enter research evidence or validation datasets.

## 56. Golden Cases

The versioned golden library will contain known-valid/invalid workflows and authority, clean/leaking datasets, reproducible/nonreproducible experiments, valid validation/known-overfit candidates and valid/broken audit trails. Golden-case creation, review, freeze, amendments and contradictions follow Sprint 3; the component under test cannot approve its own golden answer.

## 57. Test Oracle Architecture

Oracle types: constitutional, contract, state-transition, authority, artifact, evidence, synthetic-data, independent reference implementation, invariant and human-governance. Every test identifies oracle source/version/authority and ambiguity behavior. The component under test cannot be its sole oracle; disputed or stale oracles produce BLOCKED/INCONCLUSIVE, not manual PASS.

## 58. Metamorphic Testing

For agent, stochastic validation, Monte Carlo and synthesis, test invariants across controlled transformations: irrelevant evidence adds no authority; renaming an agent changes no authority; evidence reorder retains contradictions; more agent votes create no human authority; replay creates no duplicate effect; narrowing claim scope cannot broaden evidence. Variability must remain inside declared invariant boundaries.

## 59. Property-Based Testing

Future generators seek counterexamples to: no unauthorized transition; no promotion from quarantine/stale/invalidated evidence; no self-approved exception; no A11 in Phase 2; no deleted negative evidence; no validation without lineage/independence; no decision without evidence; no recovery without re-passing the gate; no recorder/ORC/MON authority escalation.

## 60. Chaos / Resilience Testing

Governance-safe scenarios cover module/registry/audit/monitor outage, agent timeout, unavailable human, partial workflow, duplicate/delayed/out-of-order messages. Expected outcomes prefer HOLD, quarantine, escalation and fail closed. Chaos cannot be run against capital or production merely because it is planned here.

## 61. Audit Reconstruction Testing

Every material run reconstructs WHO did WHAT, WHEN, under WHICH AUTHORITY, with WHICH artifact/evidence versions, in WHICH state, with WHICH contradictions, through WHICH gates, producing WHICH result/transition/downstream effects. Failure for any consequential C3/C4 action is `FAIL`, not incomplete PASS.

## 62. Testing the Tests

Mutation/meta-validation deliberately removes authority/provenance checks, admits stale evidence, enables self-approval, leakage, failed-trial hiding or execution calls. The suite must detect each seeded defect and attribute which gate caught it. Surviving P0/P1 mutations block test-system readiness.

## 63. Prohibited Test Shortcuts

Prohibited: happy-path-only; code-coverage-only assurance; self-generated sole oracle; mocking away authority/provenance; ignoring negative evidence/failures; successful-trial-only testing; current output as truth; evidence-free manual PASS; ungoverned test exception; skipped C4 negative paths; green CI as approval; lower-environment PASS as production qualification; hidden flaky/adversarial failures.

## 64. Future CI Relationship

Future CI may execute exact versioned tests and emit test evidence: `TESTS → TEST EVIDENCE → DISTINCT TEST GATES → GOVERNED READINESS`. CI is a coordinator/producer, not authority, validator of institutional meaning or deployment approver. Green CI ≠ scientific success ≠ executive decision ≠ A11.

## 65. Planning ADRs

| ADR | Context / decision | Rationale / rejected alternative | Consequence | Constitutional basis |
|---|---|---|---|---|
| S6-ADR-01 | Requirement→test traceability mandatory | Orphan tests/requirements rejected | Missing link blocks readiness | Charter traceability |
| S6-ADR-02 | Positive + negative obligations | Happy path alone rejected | C3/C4 need bypass cases | Fail closed |
| S6-ADR-03 | Authority is independently tested | Functional correctness alone rejected | Wrong actor makes FAIL | Agent Framework |
| S6-ADR-04 | Human gates are scoped tests | Human presence oracle rejected | Reserved powers evidenced | Sprint 5 |
| S6-ADR-05 | Independence uses evidence dimensions | Vague label/single score rejected | Mandatory dimension binary | Validation governance |
| S6-ADR-06 | Agent ceilings tested per instance/scope | Name/capability authority rejected | Ceiling bypass fails | Agent Framework |
| S6-ADR-07 | Controlled failure injection required | Log-only failure review rejected | Containment is provable | Charter |
| S6-ADR-08 | Recovery re-passes original gate | Retry-as-waiver rejected | New evidence/authority required | Sprint 4 |
| S6-ADR-09 | Temporal availability is explicit | Timestamp-only testing rejected | Causal leakage traps | Research OS |
| S6-ADR-10 | Reproducibility is layered R0–R5 | Binary reproducible label rejected | Claims state required level | Sprint 3 |
| S6-ADR-11 | Determinism separated from stochasticity | Bit-identical LLM promise rejected | Invariants/process attribution | Scientific integrity |
| S6-ADR-12 | Validation machinery is meta-validated | Validator self-trust rejected | Known-bad controls mandatory | Validation standards |
| S6-ADR-13 | Negative controls are governed assets | Results-only confidence rejected | False-edge rejection tested | Research OS |
| S6-ADR-14 | Adversarial testing is first-class | Accidental coverage rejected | Bypass attempts explicit | Governance principles |
| S6-ADR-15 | Oracle independence required | Component as sole oracle rejected | Dispute blocks/inconclusive | SoD |
| S6-ADR-16 | Governance coverage ≠ code coverage | Percentage assurance rejected | Multi-dimensional gaps visible | Charter |
| S6-ADR-17 | Execution isolation is P0 | Deferred boundary test rejected | All Phase 2 A11 attempts fail | EXE-01 |
| S6-ADR-18 | CI ≠ authority | Green-build approval rejected | Separate readiness authority | Sprint 5 |
| S6-ADR-19 | Test system requires mutation/meta-tests | Untested tests rejected | Seeded defects must be caught | Reproducibility/audit |
| S6-ADR-20 | Unsafe ambiguity fails closed | Optimistic defaults rejected | HOLD/quarantine/escalation | Constitution/Charter |

## 66. Open Questions Register

| ID | Question / source | Family / module / workflow / axis | C / severity | Status / default | Competent authority | Target / resolution |
|---|---|---|---|---|---|---|
| S6-OQ-01 | Which domain-specific reversible C3 actions enter the A7 catalog? S5-OQ-01 | T08/33; GOV/IAM; all; AX-09 | C3/High | Non-blocking plan; A7 denied unless every eligibility dimension and named action pass | H-02/domain authority | Sprints 7–11 domain plans, Sprint 12 integration |
| S6-OQ-02 | Numerical independence thresholds by use case? S5-OQ-02 | T12; VAL; WF-04; AX-04 | C3/High | Non-blocking; mandatory dimension failure blocks | H-06 + Evidence Governance | Sprint 9, then Sprint 12 |
| S6-OQ-03 | Exact automatic fail-safe triggers/windows? S5-OQ-03 | T29/30; RSK/MON; WF-09/16; AX-08/10 | C4/High | Non-blocking while EXE closed; manual escalation | H-04/H-09/H-01 | Sprint 10 |
| S6-OQ-04 | Freshness periods/triggers by evidence class? S5-OQ-04 | T05/19; MON/VAL; WF-05/09; AX-03 | C2–4/Medium | Non-blocking; suspected stale basis HOLD | Evidence/domain authority | Sprints 9–10 |
| S6-OQ-05 | Production ID syntax, namespace and reconciliation protocol? S5-OQ-05 | T35/36; IAM/ORC/AUD; all | C3/Medium | Non-blocking; collision/ambiguity quarantined | Workflow/Artifact Governance | Future implementation specification |
| S6-OQ-06 | Retention/legal constraints for test data/evidence? S5-OQ-06 | T04/05/25; DAT/AUD | C2–4/Medium | Non-blocking; no disposal with dependency | Legal/Data/Artifact authority | Sprint 7/later |
| S6-OQ-07 | Exact independent Phase 2 exit-test review composition? S5-OQ-07 | T25/38; GOV/AUD; WF-10; AX-09 | C4/High | Non-blocking Sprint 6; blocks Sprint 12 exit | Existing governance authority | Sprint 12 |
| S6-OQ-08 | Statistical tolerance/oracle policy for stochastic regression? New | T17–T22; VAL | C2–3/Medium | Non-blocking; no PASS without declared justified oracle | H-06/Scientific Governance | Sprint 9 |

S5-OQ-01 is governed by a testable eligibility contract; S5-OQ-02 by evidence dimensions; S5-OQ-05 by invariant test obligations. Their production catalogs, thresholds and syntax remain explicit questions. Blocking issues for Sprint 6 planning: zero.

## 67. Sprint 7 Handoff Contract

Sprint 7 shall inherit DAT-01..05 tests for source identity, admission, raw preservation, quality, transformations, version/lineage, temporal and information availability, reproducibility, dataset locks, corruption/missing data, source changes, leakage, quarantine, recovery and audit. It must specify data-stage gates and failure semantics that satisfy T04/T05/T15–T19/T23–T25/T32/T36 without implementing pipeline or tests. It must address S6-OQ-06 and contribute domain actions, if any, to S6-OQ-01.

## 68. Definition of Done

The plan defines 38 families and eight levels; maps 46/46 modules, 16/16 workflows, 10/10 axes, 12/12 authority classes, 13/13 agents and 11/11 humans; covers C0–C4, positive/negative paths, SoD, independence, delegation/expiry, artifacts/evidence, temporal integrity, reproducibility, validation-of-validation, negative controls, adversarial/failure/recovery/concurrency/replay/invalidation/quarantine/emergency/override/consensus/isolation/audit, coverage/gates/oracles/meta-testing; classifies all questions; hands off Sprint 7; leaves EXE-01 closed; and introduces no executable test, code, CI, trading logic or authority.

## 69. Final Sprint Disposition

**SPRINT 6 COMPLETE WITH OPEN GOVERNANCE ITEMS**

Blocking issues: **0 for Sprint 6 planning**. Eight bounded questions remain under explicit fail-closed defaults. After governance review and merge, the next authorized planning step is **Phase 2 — Sprint 7: Data Pipeline Plan**.
