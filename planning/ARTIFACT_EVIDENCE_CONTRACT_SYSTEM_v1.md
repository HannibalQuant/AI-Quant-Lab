# AI Quant Lab — Artifact & Evidence Contract System v1.0

## 1. Document Status

| Field | Value |
|---|---|
| Phase / Sprint | Phase 2 — Sprint 3 |
| Status | Proposed for governance review |
| Canonical path | `planning/ARTIFACT_EVIDENCE_CONTRACT_SYSTEM_v1.md` |
| Constitutional baseline | AI Quant Lab v1.0, tag `v1.0`, commit `50b61266f880cb9657b7f1b477d3d90825fe013f` |
| Planning baseline | Implementation Planning Charter v1.0, merge `82b683d252dba63cc7e8b0be44febef10eb5b7b3` |
| Architecture baseline | Module Boundary Architecture v1.0, merge `f7d2d46ab55ba9d6150443ae9c8623a0705f561d` |
| Contract version | 1.0 |
| Implementation / deployment authority | None |

This is a non-executable planning contract. It reconciles, but does not amend, the superior Artifact Registry (`ART`) and Evidence Exchange Standard (`EES`).

## 2. Purpose

Define how future institutional work becomes identifiable, attributable, inspectable, versioned, reproducible, admissible, challengeable, contradiction-aware, immutable when frozen, supersedable without historical deletion, and traceable into governed decisions.

**NO CLAIM WITHOUT EVIDENCE. NO EVIDENCE WITHOUT PROVENANCE. NO PROMOTION WITHOUT ADMISSIBLE EVIDENCE. NO DECISION WITHOUT TRACEABILITY.**

## 3. Authority and Inheritance

Authority descends: Constitution → Charter → Sprint 2 boundaries → this contract → future specifications → future implementation. Superior governance wins. ART owns artifact semantics; EES owns evidence semantics; domain authorities own scientific interpretation, validation, risk and decisions. AUD-01/02/03 provide registry, custody and reconstruction, never substantive authority.

Reviewed sources include ART, EES, Experiment/Validation Evidence Packages, Decision OS and Executive Decision Package, Scientific Research OS, Agent Contract Framework, SMI, MACP, relevant validation/risk/monitoring standards, and all Sprint 1–2 planning artifacts.

## 4. Scope

This contract defines documentary models, taxonomies, lifecycle meanings, admissibility and completeness semantics, provenance, lineage, contradiction and negative-evidence custody, reproducibility, immutability, responsibility, mappings, evidence gates, quarantine, audit, retention, future tests and handoff obligations.

## 5. Non-Goals

No code, executable schema, database, API, command, workflow automation, quantitative threshold, trading logic, validation method, infrastructure or execution capability is specified. Tables and pseudo-structures are documentary only.

## 6. Governing Principles

1. Result ≠ evidence; evidence ≠ validation; validation ≠ decision; decision ≠ deployment authority.
2. Identity, content, status, authority, custody and provenance are independent dimensions.
3. Registration records existence; admission permits consideration; neither proves truth.
4. Exact-version references are mandatory for consequential use.
5. Evidence scope cannot be expanded by summary, aggregation or decision.
6. Negative, failed and contradictory work is institutional memory.
7. Frozen material is immutable in place.
8. Amend, supersede and invalidate without erasing history.
9. Missing authority, provenance, lineage or integrity fails closed.
10. Technical capability and storage location confer no authority.

## 7. Terminology

| Term | Meaning | Must not be confused with |
|---|---|---|
| Artifact | Governed institutional product and record | Its storage representation |
| Evidence Object | Smallest independently governed evidentiary unit | Claim or decision |
| Evidence Package | Composite exact-version set for a declared use | New authority or rewritten sources |
| Claim | Scoped proposition capable of support or refutation | Result |
| Admission | Use-specific permission to consider evidence | Validation or approval |
| Validation | Independent evaluation within declared scope | Executive decision |
| Custody | Responsibility for integrity, transfer and access | Scientific ownership |
| Freeze | Immutable exact-version review baseline | Permanent truth |
| Amendment | Linked new version correcting/extending prior material | In-place edit |
| Supersession | New artifact replaces current use prospectively | Deletion or proof of defect |
| Invalidation | Evidenced restriction of specified uses due to defect | Mere obsolescence |
| Freshness | Continued temporal/use relevance | Integrity |
| Quarantine | Restricted custody pending resolution | Rejection or deletion |

## 8. Artifact Model

Every critical Artifact Record must declare:

| Dimension | Mandatory documentary content |
|---|---|
| Identity | Artifact ID, class, subtype, name, exact version, representation and integrity identity |
| Content | Purpose, scope, subject, claims, assumptions, limitations, exclusions and contradictions |
| Status | ART lifecycle, evidence/admission status if applicable, integrity, freeze, supersession, invalidation, freshness and retention |
| Authority | Governing source, producing authority, accountable owner, reviewers, approvals and prohibited uses |
| Custody | Current custodian, access, transfers, retention, archive and audit references |
| Provenance | Creation/amendment times, actor, module, workflow/task, sources, transformations, tools and handoffs |
| Relationships | Upstream/downstream artifacts; datasets; experiments; validations; evidence; decisions; transitions; reproduction and audit references |

Unknown or inapplicable fields are explicit; they are never silently omitted. Identity continuity does not imply content continuity. A material content/status/scope change creates a new exact version.

## 9. Artifact Taxonomy

The following 50 documentary contracts refine existing ART types rather than establish a rival registry.

| # | Canonical class | Reconciled existing term | Core contract / authority limit |
|---:|---|---|---|
| 1 | Research Question Record | Research intake/request | Question, scope, requester; no experiment authority |
| 2 | Research Hypothesis Record | Strategy Hypothesis Document | Falsifiable claim, mechanism, assumptions, rejection criteria |
| 3 | Research Evidence Record | EES research evidence | Exact claim relation, scope and provenance |
| 4 | Challenge Record | Challenge/conflict record | Challenger, target, grounds, response; no automatic invalidation |
| 5 | Data Source Record | DQS source record | Origin, license, availability and source identity |
| 6 | Dataset Manifest | Dataset record | Exact observations/version/transforms/lineage/eligibility |
| 7 | Data Quality Report | DQS report | Findings and exclusions; no hypothesis conclusion |
| 8 | Temporal Integrity Report | DQS temporal evidence | Timing, alignment, leakage findings |
| 9 | Experiment Specification | Experiment Plan / XDS | Hypothesis, methods, controls, metrics and failure criteria |
| 10 | Experiment Authorization Record | XDS authorization | Prerequisites and bounded execution permission only |
| 11 | Experiment Configuration Lock | Lock record | Exact data, implementation, config, objective and budget identities |
| 12 | Experiment Result Package | EEP / run output | All outcomes, deviations and raw references; not validation |
| 13 | Search / Optimization History Record | Search ledger | Search space, budget, objectives and full trial history |
| 14 | Failed Trial Record | Failure evidence | Failure class, inputs, outputs and disposition |
| 15 | Validation Specification | VEP plan | Independent methods, scope, controls and acceptance obligations |
| 16 | Chronological Validation Evidence | WF/OOS evidence | Temporal method, windows, contamination controls and outcomes |
| 17 | Stochastic / Stress Evidence | MC/stress evidence | Seeds, perturbations, scenarios and distributions |
| 18 | Stability & Generalization Evidence | Stability report | Parameter/market/time/cost boundary and failure zones |
| 19 | Negative-Control Evidence | Negative Control Report | Control design and null/negative outcomes |
| 20 | Adversarial / Overfitting Defense Evidence | ODS report | Multiple-testing, break tests and sensitivity evidence |
| 21 | Implementation Parity Record | IPS record | Representation identities, mismatches and tolerance status |
| 22 | Validation Evidence Package | VEP | Referenced validation evidence; no source rewriting or decision |
| 23 | Robustness Report | Validation Report | Scoped synthesis with contradictions and limitations |
| 24 | Evidence Admission Record | EES admissibility record | Use-specific admissibility outcome; not truth |
| 25 | Evidence Challenge Record | EES challenge | Evidenced challenge, affected use and response |
| 26 | Contradiction Record | Conflict record | Competing exact claims/evidence and unresolved status |
| 27 | Decision Support Package | Executive Decision Package | Organized evidence/limits; no non-delegable choice |
| 28 | Decision Record | Executive Decision Record | Actor, authority, evidence, rationale, outcome and bounds |
| 29 | Promotion Record | Lifecycle promotion record | Authorized bounded transition and prerequisites |
| 30 | Rejection Record | Decision rejection | Grounds, evidence and reconsideration conditions |
| 31 | Hold Record | Decision/workflow hold | Cause, restrictions, owner and release conditions |
| 32 | Failure Record | Failure Review Report | Failure, containment, dependencies and learning |
| 33 | Governance Exception Record | Exception record | Temporary bounded deviation; cannot rewrite facts |
| 34 | Risk Assessment Record | Risk Review Report | Risk findings/limits; no validation rewrite |
| 35 | Risk Escalation Record | Escalation record | Breach, severity, routing and authority requested |
| 36 | Kill / Suspension Record | Emergency Suspension Record | Authorized containment, scope and recovery requirements |
| 37 | Portfolio Admission Record | PCS candidate record | Eligibility for portfolio review only |
| 38 | Portfolio Evidence Record | PCS report | Dependencies, concentration/exposure and limits |
| 39 | Monitoring Report | MEDS report | Observations against exact baseline; no retuning authority |
| 40 | Edge Decay Report | Edge Decay Report | Deterioration evidence, scope and response request |
| 41 | Governance Alert Record | Governance violation alert | Finding, route, acknowledgement and closure |
| 42 | System State Snapshot | SMI snapshot | Exact observed state; not transition authority |
| 43 | State Transition Record | Transition ledger entry | Prior/new state, request, validation, authorization and recorder |
| 44 | Agent Handoff Record | MACP transfer | Task, sources, limitations, custody and acknowledgement |
| 45 | Reproducibility Manifest | EES/ART manifest | Reconstruction identities and results |
| 46 | Lineage Manifest | ART/EES lineage | Exact nodes, relationships, transforms and gaps |
| 47 | Amendment Record | ART/EES amendment | Reason, actor, authority, impacts and linked versions |
| 48 | Supersession Record | ART supersession | Predecessor/successor, reason and consumer review |
| 49 | Invalidation Record | EES/ART invalidation | Defect, authority, affected uses and impact assessment |
| 50 | Archive / Retention Record | ART archive | Retained versions, integrity, access and disposition authority |

## 10. Artifact Lifecycle

Superior ART states remain canonical. Sprint terms are a crosswalk, not replacements.

| Sprint concept | ART/EES alignment | Meaning | Mutation | Next / authority / audit |
|---|---|---|---|---|
| DRAFT | ART Proposed/Registered/Draft; EES Proposed | Incomplete candidate | Producer may edit with version history | Register/review/withdraw; owner + IAM/GOV; record material events |
| REGISTERED | ART Registered | Stable ID and custody exist | Controlled versioned edits | Draft/Active/retire; AUD-01 custody, domain owner authority |
| UNDER_REVIEW | ART/EES Under Review | Exact version evaluated | Content immutable for review | Return/freeze/approve/challenge; competent reviewer |
| ADMISSIBLE | EES Accepted plus use-specific admission | May be considered for stated use | Admission metadata only; content exact | Review/challenge/stale; AUD-02 records, competent reviewer decides |
| CHALLENGED | EES Challenged / ART conflict | Material issue registered | No suppression; linked response versions | Resolve/hold/invalidate/continue bounded |
| FROZEN | ART/EES Frozen | Exact review baseline | No in-place content mutation | Review/release/amend/supersede/invalidate |
| SUPERSEDED | ART Superseded | New current successor | Historical version immutable | Archive/retain; owner/authority with consumer impact |
| INVALIDATED | EES Invalidated / ART freeze invalidated | Specified uses prohibited | Status/impact append only | Archive or exceptionally reassess by competent authority |
| RETIRED | ART Retired | No new normal use | Metadata/retention only | Archive/exceptional reactivation review |
| ARCHIVED | ART/EES Archived | Preserved historical record | Custody-preserving operations only | Restore for inspection, never masquerade as current |

`ACTIVE`, `APPROVED`, `DEPRECATED`, EES `SUBMITTED`, `ACCEPTED`, `VALIDATED`, and `AMENDED` retain their superior-source meanings. Evidence admissibility is a separate axis and must not be encoded by overloading ART `Approved`.

## 11. Artifact Identity and Versioning

An Artifact ID is stable continuity; an Artifact Version is one exact state. Names, aliases, locations and formats are discovery metadata. Duplicate IDs, ambiguous current versions or mismatched integrity identities enter quarantine. Material changes to content, meaning, scope, data/configuration, assumptions, evidence, authority or relationships require a new version. Historical consumers cite exact versions; floating `current` references are prohibited for decisions.

## 12. Evidence Model

Evidence is a traceable object capable of supporting, weakening, refuting, qualifying or contextualizing a defined claim. Each Evidence Object retains EES mandatory fields, direction, independence, uncertainty, integrity, custody, scope, limitations, admissibility and exact version. Claim, interpretation, recommendation, approval, decision and authority remain separate objects.

## 13. Evidence Taxonomy

| Class | Examples | Required distinction |
|---|---|---|
| Raw | Source observations, original logs, unaltered outputs | Source fact, not interpretation |
| Derived | Normalized data, calculated measures, summaries | Every source and transformation disclosed |
| Experimental | Runs, trials, search histories, deviations | Produced result, not independent validation |
| Validation | OOS/WF/stress/stability/adversarial findings | Independent scope and specification |
| Negative | Failed trials, rejected hypotheses, adverse sensitivities | Preserved with equal identity and custody |
| Contradictory | Evidence opposing another scoped claim/evidence | Linked, never silently averaged |
| Reproducibility | Reproduction attempts, discrepancies, manifests | Repeatability status, not performance proof |
| Parity | Representation-equivalence checks | Logic equivalence, not edge validity |
| Risk | Risk assessments, breaches, limits | Risk authority only |
| Monitoring | Health, freshness, decay and regime observations | Observation, not modification permission |
| Governance | Authorizations, exceptions, reviews and audit events | Proves process/authority, not scientific success |

## 14. Evidence Package Contract

Every critical package answers, with exact IDs or an explicit `UNKNOWN/NOT_APPLICABLE` rationale:

| Area | Mandatory questions |
|---|---|
| Purpose | What and why was tested; hypothesis and claimed mechanism? |
| Scope | Market/instrument/timeframe/period/regime/strategy family/parameter region/portfolio/governance version? |
| Inputs | Data identity/version/source/transforms; implementation/configuration identities? |
| Assumptions | Costs, execution, environment, dependencies, controlled randomness/seeds? |
| Method | Specification, controls, search space/budget, trials and review boundaries? |
| Full outcomes | Successes, failures, failed/pruned/excluded trials and reasons; raw outputs? |
| Challenge | Contradictions, missing evidence, uncertainty and unresolved issues? |
| Attribution | Producer, owner, custodian, challenger, reviewer, modules and authority? |
| Traceability | Artifact, experiment, validation, claim, decision, transition and audit references? |
| Reproduction | Manifest, attempts, discrepancies and reconstruction limits? |
| Decision boundary | Permitted consumers, claims it can support, what it cannot prove or authorize? |

Packaging references exact source objects. A package cannot increase source confidence, erase limitations, combine dependent evidence as independent, or grant authority.

## 15. Evidence Admissibility

Admission is claim-, scope-, consumer-, purpose- and time-specific. AUD-02 records the outcome; the competent domain reviewer determines it under EES/GOV/IAM.

| Outcome | Meaning | Promotion effect |
|---|---|---|
| ADMISSIBLE | All mandatory dimensions sufficient for stated use | May be considered, not presumed true |
| CONDITIONALLY_ADMISSIBLE | Bounded gaps with explicit restrictions/expiry | Only named use; no scope expansion |
| INCOMPLETE | Required structure/provenance/method/review absent | Return or hold |
| STALE | Freshness condition no longer satisfied | Block new promotion pending review |
| CONTRADICTED | Material unresolved opposing evidence exists | Challenge/hold; decision must disclose |
| INADMISSIBLE | Integrity, eligibility, authority or use mismatch | Quarantine/reject/block use |

Dimensions: identity completeness, provenance, source integrity, data eligibility, temporal integrity, scope match, configuration and implementation identity, reproducibility, method traceability, producer attribution, independence, contradiction/failed-trial/exclusion disclosure, freshness, authority eligibility, integrity and freeze status. A dimension may be `PASS`, `CONDITIONAL`, `FAIL`, or `UNKNOWN`; no roll-up hides a blocking failure.

## 16. Evidence Completeness

| Dimension | Complete when | Important caveat |
|---|---|---|
| Structural | Required fields/components and references exist | Can still be scientifically weak |
| Provenance | Origin, actors, custody, sources and transforms reconstruct | Does not prove method quality |
| Scientific | Claim-relevant methods, controls, negatives, contradictions and uncertainty adequate | Domain authority judges |
| Reproducibility | Exact identities/manifests/outputs permit declared reconstruction | Reproduction may still fail |
| Governance | Authority, reviews, segregation, status and audit complete | Cannot turn weak science into truth |

Completeness is a vector, never one flattering score. Strong results may remain governance-incomplete; structurally complete packages may remain scientifically weak.

## 17. Provenance Model

Every material claim permits reconstruction:

`CLAIM → EVIDENCE → SOURCE ARTIFACT → RUN → CONFIGURATION → IMPLEMENTATION → DATASET → TRANSFORMATIONS → RAW SOURCE → ACTOR / MODULE / AUTHORITY`.

Each link cites exact identity/version, relation, time, actor and integrity state. Amendment, supersession, rejection, invalidation, archival, migration, handoff and restart append relationships and custody events; they never replace ancestry. A missing material link is a provenance gap and blocks unconditional admission.

## 18. Lineage Model

Documentary relationship semantics are: `DERIVED_FROM`, `PRODUCED_BY`, `CONSUMED_BY`, `VALIDATES`, `CHALLENGES`, `CONTRADICTS`, `SUPERSEDES`, `INVALIDATES`, `AMENDS`, `REFERENCES`, `AUTHORIZED_BY`, `DECIDED_BY`, `TRANSITIONED_BY`, and `REPRODUCES`.

Each relationship records subject/object exact versions, scope, direction, actor, authority, time and rationale. Relationships do not transfer authority. Cycles in derivation, validation, admission or authorization are prohibited; referential cycles must be declared and reviewed.

## 19. Claim–Evidence Model

| Field | Obligation |
|---|---|
| Claim ID/type/claimant | Stable attributable identity |
| Scope | Exact validity boundary |
| Supporting evidence | Exact IDs, versions, direction and independence |
| Contradicting evidence | Exact IDs, severity and status |
| Missing evidence | Explicit gaps and consequence |
| Confidence boundary | Dimensioned rationale; no certainty inflation |
| Admission/challenge status | Use-specific current state |
| Decision boundary | Permitted decisions and prohibited inference |

Unsupported claims, orphan evidence, unknown scope, evidence narrower than the claim, hidden contradiction, and validation use outside tested scope are prohibited. If `EVIDENCE SCOPE < CLAIM SCOPE`, the claim is narrowed, returned or explicitly held for competent review.

## 20. Contradiction Handling

A Contradiction Record identifies competing claims/evidence, affected artifacts/decisions, scope, severity, reviewer, required response, promotion impact and resolution status. Contradictions remain linked and visible in every relevant package.

Resolution state is `RESOLVED` or `UNRESOLVED`; impact classification is `MATERIAL`, `BLOCKING`, `NON_BLOCKING`, or `INVALIDATING`. Competent scientific/validation/risk/decision authority classifies within its domain; AUD-02 only preserves custody/status metadata. Unresolved blocking contradiction blocks promotion. Resolution produces evidence and rationale; it never deletes the losing evidence. Supersession preserves the contradiction history.

## 21. Negative Evidence

Failed experiments, rejected hypotheses, negative controls, unsuccessful searches, failed robustness/parity, invalidated implementations, adverse markets/periods/costs/regimes, monitoring deterioration and rejected decisions receive stable identity, normal provenance, retention and downstream links. Positive packages must reference applicable negative evidence. Outcome preference cannot lower retention or visibility.

## 22. Failed-Trial Visibility

Experiment/search packages disclose authorized search space, objectives and amendments; budget; attempted/successful/failed/pruned/excluded trials; reasons; objective history; dataset/configuration changes; and selection lineage. A “best trial” is never a complete package. Missing trial accounting triggers challenge and blocks admission for promotion.

## 23. Reproducibility Manifest

The manifest identifies dataset/version and source lineage; implementation/version; configuration; experiment/validation specifications; environment and dependency identities where relevant; randomness/seeds; cost/execution assumptions; timestamps; producer; transformations; exclusions; amendments; raw outputs; artifact/evidence package IDs; reproduction procedure assumptions; attempts; discrepancies; and declared reproducibility class. No environment technology is selected here.

## 24. Freeze and Immutability

Mutable Draft permits controlled editing. Registered material has stable identity and version history. Freeze binds exact content, representations, metadata, claims, scope, relationships, integrity and review purpose. No in-place silent mutation after freeze. Corrections use amendment, replacement uses supersession, defects use invalidation. A freeze violation triggers quarantine, audit and dependent-use assessment.

## 25. Amendment

An Amendment Record preserves prior/new versions, reason, actor, authority, timestamp, changed fields, affected claims, downstream consumers, evidence/decision impacts, re-review requirements and audit reference. It cannot retroactively alter what a historical decision consumed.

## 26. Supersession

Supersession is prospective replacement, not deletion or defect finding. Predecessor and successor remain addressable, attributable and connected to historical decisions. Consumers can resolve current/historical versions, reason, effective time and whether prior decisions require review. Partial supersession declares exact scope.

## 27. Invalidation

Invalidation is an evidenced restriction caused by corruption, leakage, wrong implementation, broken provenance, parity failure, unauthorized modification, method defect, invalid assumptions or critical contradiction. It preserves history and triggers planned impact assessment of dependent evidence, validations, decisions, portfolio records, monitoring baselines and transitions. Cascading is not implemented here; Sprint 4 must define governed routing and authorization.

## 28. Freshness

Freshness has last-reviewed time, review/expiry conditions, scope and owner. Triggers include new data, regime/market-structure/cost/policy/dependency/implementation change, unresolved contradiction and monitoring deterioration. Stale evidence remains historical but cannot silently support new promotion; it is held for refresh, revalidation or explicit bounded exception.

## 29. Scope Boundaries

Critical material declares instrument, market, timeframe, period, regime, source, implementation, cost/execution model, strategy family, parameter region, portfolio context and governance version. Aggregators compute intersections, not unions, unless extension evidence is separately admitted. Every consumer verifies claim scope against each evidence scope.

## 30. Custody and Responsibility

| Role | Responsibility | Prohibition |
|---|---|---|
| Producer | Creates attributable content and disclosures | Cannot self-admit/validate/approve where independence required |
| Owner | Accountable for lifecycle and consumer impact | Cannot rewrite domain verdicts |
| Custodian | Integrity, access, transfer, freeze and retention | Cannot infer scientific/decision authority |
| Reviewer | Evaluates assigned dimension and scope | Cannot exceed delegated competence |
| Challenger | Raises evidenced defect/alternative | Cannot silently alter target |
| Approver | Exercises named bounded authority | Cannot backfill missing evidence silently |
| Consumer | Verifies version, scope, status and limits | Cannot broaden or strip provenance |

AUD-01 owns artifact registry custody; AUD-02 evidence custody/admission metadata; AUD-03 append-only audit/decision/state/lineage reconstruction. Domain authority remains with the modules defined in Sprint 2.

## 31. Module-to-Artifact Matrix

All 46 Sprint 2 modules are explicit. “Amend” means only owned fields before freeze or through a governed amendment.

| Module | Consumes | Produces | Evidence in/out | Custody / amendment / freeze | Prohibited artifact action |
|---|---|---|---|---|---|
| GOV-01 | Governance sources, claim/status refs | Policy-resolution record | Governance in/out | GOV custody; amend resolution; respects freeze | Alter evidence or self-except |
| GOV-02 | Exception/escalation requests | Exception/escalation record | Governance/risk in/out | GOV custody; authority-bound amend | Approve own exception |
| IAM-01 | Identity assertions/contracts | Actor/object identity record | Identity provenance in/out | Identity custody; correct via version | Grant authority |
| IAM-02 | Identity, policy, action scope | Authorization record | Governance in/out | Authorization custody; exact decision frozen | Create identity/policy |
| DAT-01 | External source facts | Data Source Record | Raw provenance in/out | Source metadata custody; version changes | Qualify dataset alone |
| DAT-02 | Registered source/raw input | Raw custody/admission record | Raw in/out | Raw custody; freeze original | Silent repair/overwrite |
| DAT-03 | Raw/dataset candidates | DQ + Temporal Reports | Quality/temporal in/out | Review custody; findings frozen | Transform or approve hypothesis |
| DAT-04 | Eligible data, transform spec | Dataset + Lineage Manifests | Derived in/out | Builder custody; declared versions | Self-qualify output |
| DAT-05 | Manifests/quality reports | Dataset registry record | Eligibility evidence in/out | Dataset identity custody | Mutate dataset content |
| RES-01 | Authorized question | Research Question Record | Research context in/out | Intake custody; amend scope pre-freeze | Authorize experiment |
| RES-02 | Question/evidence | Hypothesis Record | Research evidence in/out | Hypothesis custody; version amendments | Declare truth/promotion |
| RES-03 | Hypotheses/evidence | Research Evidence/Challenge | Support/contradiction in/out | Challenge custody; preserve freeze | Suppress contradictions |
| KNW-01 | Admitted records | Knowledge registry record | Curated evidence in/out | Knowledge custody; versioned update | Treat output as automatic truth |
| KNW-02 | Handoffs/state refs | Agent Handoff/State refs | Provenance in/out | Gateway custody; no source edit | Promote transient context |
| KNW-03 | Failures/challenges/provenance | Failure/Learning/Lineage record | Negative evidence in/out | Failure memory custody | Delete failed work |
| EXP-01 | Hypothesis/dataset eligibility | Experiment Specification | Research/data in; spec out | Spec owner; freeze before run | Validate/approve result |
| EXP-02 | Spec/data/implementation/config | Configuration Lock | Identity evidence in/out | Lock custody; immutable per run | Silent objective/data change |
| EXP-03 | Spec/lock/authorization | Experiment Authorization | Governance evidence in/out | Gate record frozen | Judge performance |
| EXP-04 | Authorized spec/lock | Results/Failed Trial records | Experimental evidence out | Run custody; append outcomes | Hide trials/validate |
| EXP-05 | All run outputs | Experiment Result Package | Experimental/negative out | Package custody; source refs frozen | Rewrite or self-admit evidence |
| EXP-06 | Authorized search spec/lock | Search History/Failed Trials | Search evidence out | Full-history custody | Best-only disclosure/promotion |
| VAL-01 | Frozen candidate/package | Validation Specification | Admission context in/out | Validation intake custody | Change experiment |
| VAL-02 | Spec/frozen inputs | Chronological Evidence | Validation evidence out | Independent custody; freeze results | Executive decision |
| VAL-03 | Spec/frozen inputs | Stochastic/Stress Evidence | Validation evidence out | Independent custody | Alter seeds after fact |
| VAL-04 | Spec/frozen inputs | Stability/Generalization Evidence | Validation evidence out | Independent custody | Broaden tested scope |
| VAL-05 | All relevant evidence | Negative/Adversarial Evidence | Negative/contradictory out | Challenge custody | Suppress failures |
| VAL-06 | Validation objects | VEP/Robustness Report | Validation synthesis out | Aggregate custody; refs immutable | Rewrite source/admit own science |
| VAL-07 | Versioned representations | Parity Record | Parity evidence out | Parity custody; mismatch preserved | Treat parity as edge proof |
| DEC-01 | Admissible packages | Decision Support Package | Decision inputs organized | Support custody; freeze package | Decide or improve evidence |
| DEC-02 | Support/risk/authority | Decision/Promotion/Rejection/Hold | Decision evidence out | Decision authority; exact record frozen | Rewrite evidence/deploy |
| RSK-01 | Validation/portfolio/policy | Risk Assessment | Risk evidence out | Risk custody; findings frozen | Validate or relax policy |
| RSK-02 | Breaches/assessments | Escalation/Kill/Suspension | Risk/governance out | Containment record custody | Self-except/reactivate |
| PRT-01 | Eligible candidate packages | Portfolio Admission | Portfolio eligibility out | Admission custody | Validate strategy |
| PRT-02 | Candidate/exposure inputs | Portfolio Evidence/decision | Portfolio evidence out | Portfolio authority fields | Accept enterprise risk/deploy |
| MON-01 | Baselines/telemetry | Monitoring/Alert record | Health/freshness out | Monitor custody; observations immutable | Change baseline silently |
| MON-02 | Strategy/regime baselines | Edge Decay Report | Monitoring/risk out | Monitor custody | Retune/reactivate |
| MON-03 | Governance baseline/events | Governance Alert | Governance evidence out | Alert custody | Authorize remedy |
| ORC-01 | Authorized workflow inputs | Task/Handoff records | Process evidence out | Workflow custody | Create authority |
| ORC-02 | Dependency/status records | Eligibility/dependency record | Completeness evidence out | Coordination custody | Admit/validate evidence |
| ORC-03 | Authorized transition | State Transition/Recovery record | State evidence out | Records exact authority | Authorize recorded state |
| AUD-01 | Artifact submissions/events | Artifact/Amend/Supersede/Archive records | Integrity metadata out | Artifact custodian; field-owner amend | Scientific review/decision |
| AUD-02 | Evidence submissions/challenges | Admission/Custody/Quarantine refs | Evidence metadata out | Evidence custodian | Validate/approve because stored |
| AUD-03 | Actions/decisions/transitions | Audit/Lineage/Repro manifests | Audit evidence out | Append-only custody | Authorize event or rewrite sources |
| HUM-01 | Human command/status request | Attributable command record | Governance evidence out | Interface custody | Waive audit/evidence |
| HUM-02 | Review/escalation package | Human approval/rejection/halt record | Human authority evidence out | Interface records named authority | Impersonate authority/backfill proof |
| EXE-01 | Boundary/governance definitions only | Closed-boundary status/rejection | Governance evidence out | Frozen closed boundary | Any execution or capital action |

## 32. Artifact-to-Module Matrix

| Artifact family | Producer | Custodian | Required reviewer / authority | Downstream consumers | Prohibited use |
|---|---|---|---|---|---|
| Research/question/hypothesis/challenge | RES-01..03 | AUD-01/02 | Research/challenge authority | EXP, VAL, KNW | Direct promotion/execution |
| Source/dataset/quality/temporal | DAT-01..05 | AUD-01/02 | DAT-03 + domain eligibility authority | RES, EXP, VAL, MON | Mutable/unqualified final evidence |
| Experiment/spec/auth/lock/results/search/failure | EXP-01..06 | AUD-01/02 | EXP-03 for run; independent VAL for science | VAL, KNW, DEC after admission | Self-validation/approval |
| Validation/parity/robustness | VAL-01..07 | AUD-01/02 | Independent Validation authority | DEC, RSK, PRT, KNW | Deployment authority |
| Admission/challenge/contradiction | Competent reviewer/RES/VAL | AUD-02 | Domain-specific authority | All relevant gates | AUD-02 self-authority |
| Decision/promotion/reject/hold | DEC-01/02 | AUD-01/03 | DEC-02 within constitutional scope | RSK, PRT, ORC, MON | Evidence rewriting/execution |
| Risk/escalation/kill/suspension | RSK-01/02 | AUD-01/03 | Risk + named human authority where required | DEC, PRT, ORC, MON | Self-exception/validation |
| Portfolio admission/evidence | PRT-01/02 | AUD-01/02 | Portfolio authority + risk boundary | DEC, RSK, MON | Generalize individual validity |
| Monitoring/decay/alert | MON-01..03 | AUD-01/02 | Monitoring reviewer; response authority elsewhere | RSK, GOV, ORC, DEC | Auto-retune/reactivate |
| State/handoff/audit/lineage/repro | ORC/AUD/KNW | AUD-03 | Source authority + independent audit | All governed consumers | Ledger-as-authority |
| Amendment/supersession/invalidation/archive | Domain owner/authority | AUD-01/02/03 | Competent field owner + impact reviewers | Registered consumers | Delete history/retroactive rewrite |
| Governance exception/human action | GOV-02/HUM-02 | AUD-03 | Named constitutional human/governance authority | Affected gates | Cure missing facts silently |

Circular authority is exposed wherever producer, custodian, reviewer and approver collapse; such cases require segregation or explicit superior-authority exception.

## 33. Segregation of Duties

Prohibited loops include: same uncontrolled actor `PRODUCE → ADMIT → VALIDATE → APPROVE`; experimenter packaging and validating its own result; validator issuing executive promotion; decision authority rewriting audit; monitor retuning/reactivating; exception requester approving the exception; identity registry granting authorization; state recorder authorizing transition; evidence registry judging truth. Dual roles require declared identity, separated tasks, independent review and audit where superior governance permits them.

## 34. Evidence Gates

| Gate | Required classes | Minimum provenance/admission | Contradiction/stale behavior | Failure / authority boundary |
|---|---|---|---|---|
| Data | Source, Manifest, DQ, Temporal | Raw→transform lineage; eligible exact version | Hold/challenge | Return/quarantine; DAT authority |
| Experiment | Hypothesis, Spec, Auth, Lock | Identity/scope/config complete | Block unresolved prerequisite | Return/block run; EXP-03 only |
| Validation | Result Package, Validation Spec, negative/failed history | Frozen independent inputs | Blocking contradiction holds | Return/quarantine; VAL authority |
| Decision | VEP, admission, contradiction, reproducibility | Use-specific admissible exact versions | Must disclose; stale blocks | HOLD/RETURN; DEC-02 decides only |
| Risk | VEP, Risk Assessment, policy | Scope and current policy lineage | Escalate/hold | Reject/escalate; RSK authority |
| Portfolio | Admission, Portfolio Evidence, Risk refs | Candidate + portfolio-context provenance | Hold/reassess | Reject/hold; PRT authority |
| Monitoring | Baseline, Monitoring/Decay/Alert | Baseline and telemetry identities | Staleness is itself evidence | Alert/escalate; no auto-change |
| Governance | Identity, authorization, exception/audit | Actor/authority/action reconstruction | Unresolved authority blocks | Quarantine/escalate; GOV/HUM |

No quantitative thresholds are introduced. Gate passage means documentary eligibility only within the responsible domain.

## 35. Failure Modes

| Failure | Containment |
|---|---|
| Missing evidence / reviewer / authority | RETURN, HOLD, BLOCK PROMOTION |
| Incomplete provenance / broken lineage / audit gap | QUARANTINE, ESCALATE, BLOCK PROMOTION |
| Wrong dataset / unknown implementation or configuration | QUARANTINE, CHALLENGE, REJECT |
| Unregistered/orphan artifact / duplicate identity | RETURN or QUARANTINE |
| Stale artifact/evidence | HOLD, CHALLENGE, refresh review |
| Mutable artifact used as frozen / freeze violation | QUARANTINE, ESCALATE, INVALIDATE if material |
| Hidden trials/exclusions/negative controls | CHALLENGE, REJECT, BLOCK PROMOTION |
| Unsupported claim / scope mismatch | RETURN, narrow claim, BLOCK PROMOTION |
| Unauthorized amendment | QUARANTINE, ESCALATE, assess INVALIDATE |
| Contradiction suppression | CHALLENGE, ESCALATE, BLOCK PROMOTION |
| Circular self-review | REJECT review, assign independent reviewer |
| Reproducibility/parity failure | CHALLENGE, HOLD; INVALIDATE affected use if authorized |
| Invalidated upstream dependency | HOLD dependents, impact assessment, BLOCK PROMOTION |
| Ambiguous supersession | QUARANTINE current alias; resolve versions |

## 36. Evidence Quarantine

Entry causes: identity conflict, broken custody/provenance/lineage, integrity mismatch, unauthorized change, unknown scope, freeze violation, invalid upstream dependency or missing authority. Inspection by authorized custodian, reviewer, challenger and auditor is permitted; promotion, decision support, knowledge admission, reuse and scope extension are prohibited. Release requires evidenced correction/new version, competent review, restored integrity/authority, consumer-impact assessment and audit record. Irrecoverable or material defects route to scoped invalidation; unresolved authority routes to escalation.

## 37. Audit Reconstruction

For every material decision AUD-03 must enable reconstruction of: **WHO did WHAT, WHEN, under WHICH AUTHORITY, using WHICH ARTIFACTS, based on WHICH EVIDENCE, with WHICH CONTRADICTIONS, in WHICH STATE, producing WHICH DECISION, causing WHICH TRANSITION, with WHICH DOWNSTREAM EFFECTS.** Failure to reconstruct is an audit gap and prevents consequential new use.

## 38. Retention and Archival

| Class | Material | Retention intent |
|---|---|---|
| R0 Transient non-governed | Disposable working material never consumed | Bounded disposal with no institutional dependency |
| R1 Routine governed | Non-consequential registered records | Lifecycle + audit needs |
| R2 Scientific | Data, experiments, validation, reproduction | Reproduce claims and failures |
| R3 Decision/governance | Decisions, exceptions, authority, transitions | Long-term institutional accountability |
| R4 Permanent constitutional/safety | Frozen baselines, invalidations, kill events, critical contradictions | Permanent institutional meaning |

Exact durations and storage technology are deferred. Successes, failures, rejections, invalidations, superseded evidence, contradictions, exceptions and historical decisions are never silently deleted. Disposal requires authority, dependency check and Archive/Retention Record.

## 39. Agent-Generated Evidence

Agent output is candidate information. It records actor identity, agent/contract version, task/message identity, sources, process, provenance, uncertainty, limitations and contamination risks. Admission requires the applicable completeness, independence and review checks. The chain is: `AGENT OUTPUT → REGISTERED ARTIFACT → ADMISSIBLE EVIDENCE → VALIDATED EVIDENCE → AUTHORIZED DECISION`; no step is automatic.

## 40. Human-Generated Evidence

Human assertions and actions require identity, role/authority, rationale, scope, evidence references, time and audit. Human approval cannot erase missing evidence unless a superior-governed exception explicitly permits a bounded deviation; the exception and residual risk remain visible.

## 41. Governance Exceptions

An exception records requested deviation, reason, scope, requester, authority, risks, compensating controls, expiry/review condition, downstream impact and audit link. It never rewrites evidence, validation, data, provenance or historical state; cannot cure fabrication or unknown identity; and cannot be approved by its requester without superior explicit authority.

## 42. Traceability Matrix

| Constitutional requirement | Charter requirement | Sprint 2 module | Sprint 3 contract | Evidence obligation | Future test |
|---|---|---|---|---|---|
| Authority before action | Inheritance/change control | GOV/IAM/HUM | Authority/custody/gates | Authorization + audit evidence | Authorization/bypass |
| Evidence-driven research | Evidence Package Standard | RES/EXP/VAL | Evidence/package/claim models | Exact claim, scope, negatives | Completeness/scope |
| Reproducibility | Artifact/evidence planning | DAT/EXP/VAL/AUD | Provenance/lineage/repro manifest | Reconstruction chain | Reproduction/audit |
| Independent validation | Validation planning | EXP-01..06, VAL-01..07 | Segregation/gates | Independent frozen inputs | SoD/self-review |
| Decisions trace to evidence | Decision/state planning | DEC/ORC/AUD | Decision package/audit | Admissible evidence + contradictions | Trace reconstruction |
| Risk/portfolio separation | Dependency governance | RSK/PRT/DEC | Risk/portfolio gates | Scoped current risk evidence | Authority/scope |
| Monitoring is observation | Monitoring planning | MON/RSK/ORC | Freshness/alerts | Baseline-linked observations | Auto-retune bypass |
| History preserved | Traceability/change control | KNW/AUD | Freeze/amend/supersede/invalidate | Immutable prior versions | Mutation/history tests |
| Execution isolated | Non-goals/exit gate | EXE-01 | Prohibited uses/gates | Closed-boundary evidence | Execution bypass |

Every taxonomy class inherits through at least one row and its producing module contract; no registry entry creates authority.

## 43. Future Test Obligations

Future suites shall test identity uniqueness; exact versions; complete provenance/lineage; admissibility outcomes; freeze immutability; amendment linkage; supersession history/current resolution; invalidation impact; contradiction visibility/classification; failed-trial accounting; all completeness vectors; freshness; scope containment; authorization; segregation; quarantine; reproduction; audit reconstruction; negative paths and deliberate bypass attempts.

Expected failure behavior is fail closed: return incomplete work, hold stale/challenged work, quarantine integrity/provenance failures, reject unauthorized review, escalate authority/safety failures, invalidate only through competent evidenced authority, and always block unsafe promotion.

## 44. Planning ADRs

| ADR | Context / decision | Rationale | Alternatives | Consequences | Constitutional basis |
|---|---|---|---|---|---|
| ADR-S3-01 | Separate artifact identity from content | Continuity and exact historical state both required | Content-address only; mutable record | Stable ID + exact versions | ART, SMI, auditability |
| ADR-S3-02 | Separate evidence from claim | Evidence direction is relational | Result equals claim | Supports refutation and scope | EES, Research OS |
| ADR-S3-03 | Admission separate from interpretation | Storage/completeness cannot judge truth | Registry auto-acceptance | Domain reviewer retains authority | EES, Sprint 2 AUD boundary |
| ADR-S3-04 | Evidence separate from decision | Facts carry no executive authority | Automatic threshold approval | Explicit traceable decision | Decision OS |
| ADR-S3-05 | Freeze requires amendment for change | Review baseline must stay exact | In-place correction | More versions, honest history | ART/EES |
| ADR-S3-06 | Supersession differs from invalidation | Replacement ≠ defect | Single “obsolete” status | Accurate dependent impact | ART/EES |
| ADR-S3-07 | Producer differs from custodian | Integrity custody ≠ authorship/science | Registry owns content | Clear accountability | Agent Framework, ART |
| ADR-S3-08 | Registry/ledger never authority | Recording capability invites circular control | Registry approval | Prevents self-promotion | Sprint 2 AUD-01..03 |
| ADR-S3-09 | Preserve negative evidence | Best-only view causes survivorship bias | Retain winners only | Larger archive, honest inference | EES, Research OS |
| ADR-S3-10 | Preserve contradictions | Averaging/hiding destroys scope | Forced consensus | Challengeable institutional memory | EES |
| ADR-S3-11 | Reproducibility is first-class | Chat context is not durable evidence | Narrative summary | Explicit reconstruction burden | EES, ART |
| ADR-S3-12 | Agent output requires admission | Generation is not institutional proof | Trust agent role | Review and contamination controls | Agent Framework, Knowledge OS |

All ADRs are documentary, reversible through governed planning change, and cannot amend superior constitutional meaning.

## 45. Prohibited Shortcuts

Best-result-only evidence; silent trial deletion; silent evidence mutation; overwrite after freeze; unsupported claims; missing provenance; evidence self-approval; validation self-promotion; registry-as-authority; ledger-as-authority; hidden contradictions/exclusions; orphan artifacts; stale or invalidated evidence reuse; scope expansion; human override without record; agent assertion as proof; supersession as deletion; unaudited amendment; decision rewriting evidence; mutable OOS reuse; aggregator confidence inflation; package copying without lineage; exception as retroactive authorization; monitor-triggered retuning; and state recording as authorization are prohibited.

## 46. Open Questions Register

| ID | Question / source | Modules / classes | Severity | Status | Required authority | Target / resolution path |
|---|---|---|---|---|---|---|
| S3-OQ-01 | How should ART `Approved` coexist with EES `Validated` and use-specific `ADMISSIBLE` without status overloading? ART/EES | AUD-01/02, VAL-06; all evidence | High | Non-blocking | Artifact + Evidence Governance, Validation | Sprint 4: separate lifecycle axes and transition semantics |
| S3-OQ-02 | Which artifact classes require human review versus independent agent review? Charter/Sprint 2 | IAM, HUM, all C3/C4 records | High | Non-blocking | Constitutional human authority | Sprint 5 responsibility matrix |
| S3-OQ-03 | What exact freshness policies apply by evidence class/regime? EES | MON, VAL, DEC, RSK | Medium | Non-blocking | Domain + Evidence Governance | Sprints 9–10 policy plan; no default expiry invented |
| S3-OQ-04 | What retention durations/legal constraints apply? ART | AUD, DAT, KNW; R0–R4 | Medium | Non-blocking | Artifact Governance + legal/data authority | Later implementation specification |
| S3-OQ-05 | How is independence measured for shared data/code/agent ancestry? EES | RES/EXP/VAL/AUD | High | Non-blocking | Validation + Evidence Governance | Sprint 6 test architecture |
| S3-OQ-06 | Which invalidation impacts mandate automatic hold versus routed review? Sprint 2 | ORC, AUD, DEC, RSK, PRT, MON | High | Non-blocking | GOV/domain transition authorities | Sprint 4 workflow/state blueprint |
| S3-OQ-07 | Can a single actor fill producer and reviewer roles for low-criticality artifacts? Agent Framework | IAM, AUD; C0/C1 artifacts | Medium | Non-blocking | Agent/Human Governance | Sprint 5 with explicit controls |
| S3-OQ-08 | Canonical controlled vocabularies and ID syntax remain unspecified. ART/EES | IAM/AUD; all classes | Medium | Non-blocking | Artifact/Evidence Governance | Future implementation specification; Sprint 6 conformance tests |

No blocking constitutional contradiction was found. These questions are bounded and preserve fail-closed behavior until resolved.

## 47. Sprint 4 Handoff Contract

Sprint 4 shall consume this document and define workflows/state transitions for registration, submission, review, admission, challenge, freeze, amendment, supersession, invalidation, staleness, quarantine, archive and impact routing. It must preserve separate lifecycle axes, competent authority, exact-version evidence gates, negative/contradictory visibility and append-only audit meaning. It must resolve or govern S3-OQ-01 and S3-OQ-06 without implementing machinery.

## 48. Definition of Done

Canonical artifact/evidence classes, package contract, admissibility/completeness, lifecycle/version/freeze/change semantics, provenance/lineage, claim/contradiction/negative/failed-trial custody, reproducibility, both module mappings, segregation, gates, failure/quarantine, audit/retention, traceability, ADRs, future tests and classified open questions are present. All 46 Sprint 2 modules are represented. No critical authority ambiguity is hidden and no executable implementation exists.

## 49. Final Sprint Disposition

**SPRINT 3 COMPLETE WITH OPEN GOVERNANCE ITEMS**

Blocking issues: **0**. Eight bounded non-blocking questions remain assigned to later Phase 2 work. The artifact is ready for governance review and, only after acceptance/merge, handoff to **Phase 2 — Sprint 4: Workflow & State Transition Blueprint**.
