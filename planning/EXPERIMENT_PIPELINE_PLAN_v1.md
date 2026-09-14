# AI Quant Lab — Experiment Pipeline Plan v1.0

## 1. Document Status

| Field | Value |
|---|---|
| Phase / Sprint | Phase 2 — Sprint 8 |
| Status | Proposed for governance review |
| Canonical path | `planning/EXPERIMENT_PIPELINE_PLAN_v1.md` |
| Constitutional baseline | Tag `v1.0`, commit `50b61266f880cb9657b7f1b477d3d90825fe013f` |
| Phase 2 baseline | Sprints 1–7; current `main` merge `1df5a6c40e07bcab0601b87600e573df93dbc344` |
| Version | 1.0 |
| Implementation / execution authority | None; EXE-01 remains `PLANNED_CLOSED` |

This is a documentary planning contract. It creates no experiment, optimizer, backtest, strategy, test runner, production permission or capital authority.

## 2. Purpose

Define the governed scientific path from attributable question and falsifiable hypothesis through pre-registration, exact data/configuration locks, complete run/trial history, reproducibility and review to a bounded handoff for independent validation.

## 3. Authority and Inheritance

Authority descends: Constitutional Baseline → Planning Charter → Module Architecture → Artifact/Evidence Contracts → Workflow/State Blueprint → Responsibility Matrix → Test Architecture → Data Pipeline → this plan → future specifications. Scientific Research OS, Agent Framework, Decision OS, MACP/SMI and RES/EXP/VAL contracts remain superior within their scopes. Conflicts create HOLD, an open question and competent review—not a convenient experiment default.

## 4. Scope

This plan covers 13 experiment object classes, 21 stages, 38 relevant modules, 14 experiment families, 33 inherited canonical test families, full search burden, failures/negative evidence, contamination, reproduction, authority, audit and Validation Candidate handoff.

## 5. Non-Goals

No Python, Pine, JavaScript/TypeScript, Optuna, optimizer, backtester, Monte Carlo/walk-forward engine, database, executable schema, API/CLI, orchestration runtime, CI/scheduler/worker, feature/indicator/strategy/trade, broker/exchange integration, paper/live execution or deployment is implemented. No metric threshold, parameter, cost, search method or compute technology is selected.

## 6. Governing Experiment Principles

1. No experiment without a falsifiable attributable hypothesis and exact specification.
2. Pre-registration freezes primary choices before result observation.
3. Dataset and configuration locks are distinct and exact.
4. Every run, trial, campaign, result and reproduction has stable identity.
5. Search burden, failures, pruning, exclusions, post-hoc changes and contradictions remain visible.
6. Best trial is not the scientific object; complete attributable history is.
7. Experiment success means at most eligibility for independent validation review.
8. EXP cannot self-validate, self-promote or create A11/execution authority.
9. Recovery creates new versions/IDs and never rewrites failed history.
10. Missing authority, lineage, independence or audit fails closed.

## 7. Terminology

| Term | Meaning | Not equivalent to |
|---|---|---|
| Question | Attributable scientific uncertainty | “Find profit” mandate |
| Hypothesis | Falsifiable scoped claim with mechanism | Configuration |
| Specification | Frozen planned method and outputs | Run |
| Run | One execution attempt under exact locks | Experiment identity |
| Trial | One attributable configuration evaluation | Winning candidate |
| Campaign | Governed collection/search of trials | Best trial |
| Result | Derived finding from exact run outputs | Validation verdict |
| Validation Candidate | Complete package eligible for VAL intake | Validated/approved/deployable |

## 8. Experiment Object Model

| Object class | Canonical distinction |
|---|---|
| RESEARCH_QUESTION | Origin, scope and scientific objective |
| HYPOTHESIS | Falsifiable mechanism/effect claim |
| EXPERIMENT_SPECIFICATION | Versioned predeclared method |
| EXPERIMENT_AUTHORIZATION | Scoped permission to perform research run |
| EXPERIMENT_RUN | Single execution attempt identity |
| TRIAL | Single campaign/configuration evaluation |
| SEARCH_CAMPAIGN | Search space, budget, rules and all trials |
| RESULT | Scoped derived finding |
| RESULT_PACKAGE | Complete evidence/history bundle |
| NEGATIVE_RESULT | First-class weakening/rejection/inconclusive evidence |
| FAILED_RUN | Preserved failed attempt and reason |
| REPRODUCIBILITY_PACKAGE | Reconstruction contract and evidence |
| VALIDATION_CANDIDATE | Governed handoff object for independent review |

## 9. Experiment Pipeline Stages

| ID | Stage | Required output / failure boundary |
|---|---|---|
| EP-00 | Research Question Intake | Question Record or return |
| EP-01 | Hypothesis Registration | Versioned falsifiable Hypothesis Record |
| EP-02 | Experiment Candidate Formation | Candidate links and scope |
| EP-03 | Experiment Specification | Exact method/version |
| EP-04 | Pre-Registration / Freeze | Frozen hypothesis/metrics/data/search controls |
| EP-05 | Dataset Eligibility Verification | Current scoped eligibility evidence |
| EP-06 | Dataset Lock Verification | Exact valid lock or BLOCK RUN |
| EP-07 | Configuration Lock | Frozen parameters/metrics/costs/budget |
| EP-08 | Experiment Authorization | Competent scoped authorization record |
| EP-09 | Run Preparation | Identity, environment and prerequisites |
| EP-10 | Research Execution | Research-only run attempt |
| EP-11 | Run Recording | Run/trial/failure/raw-output records |
| EP-12 | Result Construction | Metrics/results linked to raw outputs |
| EP-13 | Trial / Search History Consolidation | Complete campaign and burden |
| EP-14 | Reproducibility Assessment | Reproducibility package/disposition |
| EP-15 | Experiment Review | Independent challenge/readiness review |
| EP-16 | Validation Candidate Assessment | Gate disposition only |
| EP-17 | Validation Handoff | Complete immutable handoff package |
| EP-18 | Failure / Quarantine / Invalidation Routing | Containment and impact record |
| EP-19 | Archive / Supersession | Preserved historical meaning |
| EP-20 | Audit / Reproduction | End-to-end reconstruction evidence |

No stage automatically causes the next; each consequential boundary checks state, evidence, authority and exact versions.

## 10. Research Question Contract

Records question ID/origin/proposer, objective, market/instrument/timeframe, expected mechanism, decision relevance, prior supporting/contradicting evidence, assumptions, uncertainty and related artifacts. “Find something profitable” is too vague and returns for bounded scientific formulation.

## 11. Hypothesis Contract

Records hypothesis ID/version and question, economic/market rationale, expected directional effect/regime, market/timeframe scope, measurable outcome, falsification condition, null interpretation, assumptions, competing explanations, contradictions and proposed experiment family. A parameter set is not a hypothesis.

## 12. Hypothesis Freeze

EP-04 freezes the authorized hypothesis version before observed results. Material mechanism, scope, expected effect or falsification changes create a new hypothesis and/or specification version. Retroactive rewriting is prohibited and tested as post-outcome contamination.

## 13. Experiment Specification

The specification includes experiment ID/version; hypothesis; family/purpose; exact dataset/lock; market/venue/instrument/timeframe/window and availability assumptions; research execution/cost assumptions; fixed/variable parameters and full parameter space; metric IDs with primary/secondary roles; acceptance/rejection/stopping rules; trial budget; randomness/seeds; negative controls/sensitivity; limitations; expected artifacts; producer/reviewer/authority and audit identity. No consequential value is silently selected during a run.

## 14. Pre-Registration

Before observing results, freeze hypothesis, primary metric, dataset/window, search space/budget, acceptance/rejection/stopping rules, cost/execution assumptions and negative controls. Amendments retain the prior version and timing. Later exploration is labeled `POST_HOC` and cannot masquerade as confirmation.

## 15. Dataset Integration

Sprint 7 controls exact dataset ID/version, Manifest, Data Quality Report, Temporal Integrity Report, fingerprint, DP-16 lock and use-specific eligibility. “Latest data,” “current CSV” and “whatever file exists” are prohibited. All anomalies, revisions, exclusions and availability semantics cross into the experiment record.

## 16. Dataset Lock Verification

Before EP-10 verify lock identity/fingerprint/scope, experiment binding, cutoff, current quality/temporal disposition and absence of blocking stale/quarantine/invalidation status. Mismatch, missing dependency or changed data returns `LOCK_MISMATCH`, blocks the run and audits the attempted basis.

## 17. Configuration Lock

Separate from the dataset lock, it binds specification version, parameter space/fixed values, cost/execution assumptions, metric definitions, randomness policy, future implementation/environment references and run budget. Change requires an attributable new lock and, when material, new specification/campaign/run identity.

## 18. Experiment Identity

Stable IDs separately identify experiment lineage, experiment version, run, trial, search campaign, result package and reproduction attempt. Display name, filename, agent name or matching parameters is not identity. Collisions/ambiguity follow Sprint 6/7 quarantine semantics.

## 19. Run Identity

Every run records run ID; experiment/version; dataset and configuration locks; actor/module; start/end; environment/implementation references; seed/process; state; failures/warnings; raw output/result package references and audit. Repeating identical inputs creates a new run linked to the prior run.

## 20. Trial Identity

Each trial records ID, campaign, exact parameters/seed, locks/configuration version, status, metrics, duration metadata, failure/pruning/rejection reason and output reference. Failed/pruned/rejected trials remain addressable and count toward scientific burden.

## 21. Search Campaign Model

Campaign ID/version binds experiment, search method, full space, budget/stopping/seed policy, objective/constraints/penalties, pruning/failure policy, selection rule, all trial IDs and best-candidate rule. The campaign is the scientific search object; a winner is one outcome within it.

## 22. Optimization Governance

Future grid, random, Bayesian/Optuna-like, evolutionary and manual searches may be supported only under the same provenance, budget, trial-history, objective and randomness contract. An optimizer cannot alter data, protected validation inputs, objective, search space, budget or promotion authority silently. Optimization ≠ robustness or validation.

## 23. Multiple Testing

The Research Ledger counts hypotheses, experiments, campaigns, trials/configurations, markets, venues, timeframes, windows, seeds, cost scenarios and metrics inspected, including duplicates and abandoned work. This disclosed search burden accompanies downstream validation for multiple-testing and selection-bias defense.

## 24. Research Ledger

An immutable documentary ledger preserves questions, hypotheses, pre-registrations, successful/failed/abandoned experiments, all campaigns/trials, negative results, post-hoc work, reproductions, supersessions and invalidations. It references evidence without rewriting source artifacts; registration does not imply validity.

## 25. Failed Trial Preservation

Failure classes include `INVALID_CONFIGURATION`, `DATA_FAILURE`, `TEMPORAL_FAILURE`, `RUNTIME_FAILURE`, `NUMERIC_FAILURE`, `INSUFFICIENT_DATA`, `CONSTRAINT_FAILURE`, `QUALITY_FAILURE`, `AUTHORITY_FAILURE` and `UNKNOWN_FAILURE`. Each retains attempted basis, reason/evidence and disposition. Deletion because failure hurts apparent performance is prohibited.

## 26. Negative Result Contract

Records hypothesis/experiment/locks, result and why negative, exact scope/confidence/limitations, whether the hypothesis is weakened/rejected/inconclusive and future relevance. Negative evidence remains discoverable and may seed challenges or prevent duplicated dead ends.

## 27. Result Contract

`RAW RUN OUTPUT ≠ METRIC SET ≠ RESULT ≠ RESULT PACKAGE ≠ SCIENTIFIC INTERPRETATION ≠ VALIDATION VERDICT`. Every derivation is attributable and versioned. Result creation cannot change its evidence, claim broader scope or issue a validation disposition.

## 28. Result Package

Includes experiment/hypothesis, locks, every run and trial/campaign history, primary/secondary metrics and distributions, cost assumptions, warnings/failures/negative evidence/contradictions/sensitivity, total search burden/selection procedure, reproducibility disposition, producer/time and audit/lineage. Cherry-picked metric-only packages are inadmissible.

## 29. Metric Governance

Each metric has ID/version, definition/formula reference, direction, units, scope, calculation implementation reference in future, primary/secondary role and known weaknesses. Returns, drawdown, Sharpe-like measures, profit factor, win rate, trade count, tail loss and stability metrics are examples only; no threshold is selected here.

## 30. Primary / Secondary Metrics

The primary metric is frozen before observation. Secondary metrics contextualize and challenge; they cannot silently replace a failed primary objective. Change creates an attributable post-hoc analysis or new specification.

## 31. Acceptance Criteria

Criteria are predeclared, measurable, scoped, versioned and linked to the hypothesis/null. Meeting them means only `ELIGIBLE_FOR_VALIDATION_REVIEW`; it does not mean validated, approved, robust, deployable or profitable in future.

## 32. Stopping Rules

Rules prevent stopping when good, extending until a winner, changing metric after failure or dropping unfavorable markets. Adaptive rules/extension authority must be predeclared. Post-result extension normally creates a new campaign/version and increases disclosed search burden.

## 33. Randomness Governance

Records seed identity/policy, random-source/process reference, stochastic method and required replication across seeds where applicable. Seed selection/mining is part of search burden. Randomness cannot excuse missing provenance or falsely claim deterministic reproduction.

## 34. Reproducibility Package

Identifies exact hypothesis/specification/pre-registration, dataset/lock, configuration, search space/budget/seeds, implementation/environment, run/trial/campaign IDs, metric versions, raw outputs/result package, failures/exclusions and audit. It states Sprint 6 reproducibility level and unresolved limits; this section implements no rerun.

## 35. Re-Run / Reproduction / Replication

`RE-RUN` repeats the same governed configuration; `REPRODUCTION` independently reconstructs the same experiment; `REPLICATION` tests generalization in a related experiment. Each has its own identity, context/actor independence evidence, deviations and result. One cannot be relabeled as another.

## 36. Determinism

For deterministic components, same dataset/configuration/implementation/environment/seed must meet a declared equivalence oracle. Stochastic/agent components use attributable process, distributions and invariant expectations. Non-determinism is bounded/disclosed; bit-identical LLM output is not promised.

## 37. Experiment Families

Fourteen supported planning families: single-configuration test, parameter sweep, optimization campaign, ablation, sensitivity, cost sensitivity, regime-conditioned, cross-market, cross-timeframe, temporal-window, negative control, placebo, randomized control and perturbation. Each inherits identity, locks, burden and evidence rules; none is implemented.

## 38. Ablation

Ablation removes one governed component at a time or under a declared design to test necessity, redundancy, accidental correlation and overfitting. Original and ablated experiment identities, equal-data assumptions and comparison oracle remain explicit.

## 39. Feature / Indicator Redundancy Boundary

Future feature ablation, correlation, incremental and conditional-contribution experiments may evaluate independent information. Feature/indicator definitions and availability lineage must be versioned, but Sprint 8 creates no feature, indicator or signal.

## 40. Sensitivity Analysis

Parameter-neighborhood and assumption perturbations record region, step/design, constraints, dataset and selection procedure. Results distinguish isolated peaks from stable regions without selecting numerical stability thresholds.

## 41. Parameter Stability

Evidence preserves parameter surfaces, neighbor comparisons, stability maps, plateau/fragility indicators and failures across the whole declared space. Best trial alone cannot satisfy stability evidence.

## 42. Temporal Experiments

Possible governed windows include 3m, 6m, 9m, 12m, 24m and 36m where scientifically appropriate. The specification selects justified windows before observation; each has exact dataset/cutoff/availability identity. This list is not mandatory for every hypothesis.

## 43. Cross-Market Experiments

Crypto, forex, metals/commodities, indices and equities remain separate markets with venue/instrument/data/cost identity. Portability is a tested hypothesis, never assumed. Failed markets and exclusions remain in the package and burden.

## 44. Cross-Timeframe Experiments

Every timeframe inherits Sprint 7 alignment, session anchor, timezone, bar-close/availability and resampling lineage. Comparing 1h/3h/4h etc. counts each inspected timeframe and prevents future sub-bar leakage.

## 45. Cost Sensitivity

Plausible future spread/commission/funding/borrow/fee/slippage scenario IDs reference exact sources or assumptions. Results remain scenario-specific. No cost is hardcoded and favorable-cost cherry-picking is disclosed.

## 46. Research Execution Assumptions

Separate signal time, information availability, order eligibility, next-bar open, fill, slippage and fee assumptions. These are hypothetical research model inputs, not orders or authority to trade. Their versions appear in the configuration lock.

## 47. Lookahead Defense

EP-05/06 inherit Sprint 7 rejection of future/partial bars, future high/low/funding/universe/corporate actions/labels, backdated features and lookahead resampling. Any temporal failure blocks experiment validity and downstream candidate status even if metrics look excellent.

## 48. Train / Validation / Test Boundary

Conceptually distinguish TRAIN, INTERNAL_RESEARCH_CHECK, INDEPENDENT_VALIDATION, PROTECTED_HOLDOUT and FINAL_TEST without forcing one method. Access and selection purpose are logged. EXP cannot consume protected VAL evidence silently; contamination changes eligibility and required review.

## 49. Holdout Governance

Holdout record states stable ID/version, scope, creation/time policy, custodian, authorized consumers, access history, observations/queries and contamination disposition. Repeated inspection weakens independence and is never reset by renaming an agent or dataset.

## 50. Contamination

Classes are `DATA_CONTAMINATION`, `HOLDOUT_CONTAMINATION`, `MODEL_CONTAMINATION`, `HYPOTHESIS_CONTAMINATION`, `HUMAN_CONTAMINATION`, `AGENT_CONTEXT_CONTAMINATION` and `SEARCH_CONTAMINATION`. Each record identifies source, affected claims/objects/scope, severity, evidence, containment and remediation/revalidation route.

## 51. Agent Context Contamination

Context provenance records model/instance/prompt/contract, memory/tool exposure and whether winning parameters, full search history, preferred result, executive preference or prior verdict were visible. Different agent names sharing contaminated context do not establish independence.

## 52. Experiment Independence

EXP producer may review mechanics and answer challenge but cannot be sole independent validator. Actor/role/module/workflow/evidence/data/implementation/context/memory and organizational dimensions follow Sprint 5/6. Unproven mandatory independence produces HOLD or reassignment.

## 53. Cherry-Picking Defense

The package exposes all inspected markets, timeframes, periods, seeds, metrics, parameters and cost scenarios, their selection rules and negative results. Reporting only the best member fails evidence completeness and Validation Candidate Gate.

## 54. Researcher Degrees of Freedom

Material data/date/market/timeframe/metric/parameter/filter/stopping/cost/budget choices and amendments are recorded with decision time and rationale. Hidden flexibility is an evidence failure and increases unknown search burden.

## 55. Post-Hoc Analysis

Post-hoc work is allowed as `EXPLORATORY_POST_HOC`, linked to observed evidence and clearly excluded from preregistered confirmation. It creates a new hypothesis, new specification/version or bounded exploratory evidence—never a rewritten original prediction.

## 56. Negative Controls

Future randomized signals, shuffled returns, shifted signals, irrelevant features, random parameters, destroyed temporal relationships and synthetic null strategies test false-edge rejection. Controls have exact versions/locks and remain evidence even when inconvenient.

## 57. Adversarial Experiments

Attack cases deliberately introduce future/selection leakage, seed mining, metric substitution, trial hiding, cost omission, outlier deletion, holdout reuse, boundary exploitation and market/window cherry-picking. Expected response is detect, preserve, contain and block—not optimize around the detector.

## 58. Experiment Failure Model

Canonical failures: `HYPOTHESIS_INVALID`, `SPEC_INCOMPLETE`, `DATASET_NOT_ELIGIBLE`, `LOCK_MISMATCH`, `CONFIGURATION_MISMATCH`, `AUTHORITY_MISSING`, `TEMPORAL_INTEGRITY_FAIL`, `RUN_FAILED`, `TRIAL_FAILED`, `SEARCH_BUDGET_VIOLATION`, `METRIC_UNDEFINED`, `RESULT_INCOMPLETE`, `REPRODUCIBILITY_FAIL`, `CONTAMINATION_DETECTED`, `INDEPENDENCE_FAIL`, `AUDIT_FAIL`. Each records scope/evidence/state/route.

## 59. Failure Containment

Authorized responses are HOLD, BLOCK RUN, quarantine result, request review, reject candidate, invalidate affected result or escalate. Ignoring/deleting failure, silently changing hypothesis/data/metric or running until profitable are prohibited.

## 60. Recovery

Identify cause; create new dataset/configuration/specification version and lock when affected; issue new run identity; re-execute; produce new evidence; re-pass the original gate; preserve the failed run and audit. Recovery cannot turn an old failure into PASS by mutation.

## 61. Experiment Authority Model

Thirty-eight relevant modules are explicitly covered: `RES-01`, `RES-02`, `RES-03`; `DAT-01`, `DAT-02`, `DAT-03`, `DAT-04`, `DAT-05`; `EXP-01`, `EXP-02`, `EXP-03`, `EXP-04`, `EXP-05`, `EXP-06`; `VAL-01`, `VAL-02`, `VAL-03`, `VAL-04`, `VAL-05`, `VAL-06`, `VAL-07`; `AUD-01`, `AUD-02`, `AUD-03`; `GOV-01`, `GOV-02`; `IAM-01`, `IAM-02`; `ORC-01`, `ORC-02`, `ORC-03`; `MON-01`, `MON-02`, `MON-03`; `DEC-01`, `DEC-02`; `RSK-01`, `RSK-02`.

| Power | Producer/requester | Reviewer/challenger | Competent authority / recorder | Prohibition |
|---|---|---|---|---|
| Propose experiment/spec | RES/EXP actor | RES-03, owner | Research Owner; AUD record | Proposal ≠ authorization |
| Request/verify dataset lock | EXP requests; DAT verifies/custodies | DAT-03/VAL challenge | Scoped H-08/DAT authority; AUD records | EXP cannot self-certify data |
| Authorize research run | EXP-03 request package | GOV/IAM and required reviewer | Competent A7/human under Sprint 5 | ORC/producer cannot self-authorize |
| Execute/record trial | EXP-04 executes; EXP-05 records outputs | Independent review later | Existing authorization; AUD links | Capability ≠ new authority |
| Package/challenge/reproduce | EXP-06 packages; RES/VAL challenge/request | VAL independence review | Domain authority routes; AUD records | Packaging ≠ validation |
| Declare candidate/accept handoff | EXP requests candidate; VAL intake accepts custody | VAL/GOV checks | Separate gate authority | EXP cannot issue VAL verdict |
| Quarantine/invalidate | Any may request | Domain/GOV review | Competent data/experiment authority | Registry/monitor cannot authorize |

## 62. Human / Agent Responsibility

Agents may generate hypothesis drafts, specifications, inspect eligibility, coordinate authorized runs, analyze/detect/challenge and package evidence under identity, delegation, scope, criticality and independence. Research Owner owns question/spec accountability; H-08 data; H-06 validation independence; H-02 governance; H-10 audit; C3/C4 paths have named accountable authority. No agent obtains live capital or A11.

## 63. Experiment Criticality

| C | Example / minimum governance |
|---|---|
| C0 | Documentary fixture; identity/audit |
| C1 | Exploratory experiment; review/challenge and full history |
| C2 | Formal science; preregistration, locks, reproducibility |
| C3 | Validation/decision candidate; independent review, named authority/human accountability |
| C4 | Future capital/safety evidence; strongest human gates, isolation and fail closed |

Criticality cannot be downgraded to escape controls.

## 64. Orchestration Boundary

ORC sequences/routes, checks prerequisites, schedules future work, collects artifacts and records failures. It cannot approve a hypothesis, authorize itself, alter locks/search space/criteria, validate or promote. Task completion is only an event.

## 65. Audit Boundary

AUD registers, preserves, links, reconstructs and reports missing provenance. It cannot declare success, validate, approve candidate/promotion or create missing authority. Ledger presence is evidence of a record, not legitimacy of the action.

## 66. Monitoring Boundary

MON may observe infrastructure/run health, emit evidence and request review/HOLD. It cannot retune, change parameters/budget/rules, restart under new rules, select winners or validate. Alert → governed review, never mutation.

## 67. Search Budget Governance

Every campaign freezes maximum trials, conceptual resource envelope, time/stopping policy and extension authority. Extension after poor results is attributable, increases burden and normally creates a new version/campaign. Unapproved excess trials fail the campaign contract.

## 68. Compute Budget Scheduler Boundary

A conceptual narrowing pattern such as `300 → 50 → 20 → 10 → 5 → 3` may allocate staged attention, but creates no scheduler or canonical numbers. Every stage preserves population, selection rule, all rejections/survivors, evidence and cumulative burden. Narrowing does not validate winners.

## 69. Champion / Challenger Boundary

Experimentation may label comparative `BASELINE`, `CHALLENGER`, `NEGATIVE_CONTROL` and research-ranked candidate. It cannot declare an institutional/deployed Champion. Independent VAL, DEC, RSK, portfolio and future execution gates remain separate.

## 70. Experiment Comparability

Dispositions are `IDENTICAL`, `REPRODUCIBLE`, `COMPARABLE`, `PARTIALLY_COMPARABLE`, `NON_COMPARABLE` or `UNKNOWN`, based on hypothesis, data/locks, configuration/implementation/environment, costs, market/timeframe/window and search burden. Similar profit is not equivalence.

## 71. Experiment Supersession

A new specification/version may supersede an old one through review/authority, preserving old hypothesis, locks, runs, results, decisions, reason and lineage. Supersession never retroactively changes prior meaning or erases burden.

## 72. Experiment Invalidation

Future leakage, wrong data/instrument, broken configuration, hidden trial history, corrupt metric, unrecoverable provenance/implementation or serious contamination may trigger authorized invalidation. The affected scope becomes unusable for new reliance; history remains addressable.

## 73. Downstream Impact Routing

Invalidated experiment evidence identifies affected Result Packages, Validation Candidates/Evidence, decisions, future portfolio records and knowledge entries. Sprint 4 contain-first routing applies HOLD/review/revalidation/redecision without destructive automatic cascade.

## 74. Knowledge / Memory Integration

`EXPERIMENT OUTPUT → REVIEWED EVIDENCE → VALIDATED EVIDENCE → DECISION → GOVERNED KNOWLEDGE`, where applicable. KNW cannot turn repetition or stored winners into truth. Failed, negative, abandoned, contradicted and invalidated work stays searchable with provenance.

## 75. Research Ledger Identity

Stable IDs support: Have we tested this mechanism? How many variants/markets/windows/seeds? What failed? Was holdout accessed? Was this space previously searched? Answers use versioned links, not filename similarity or agent memory.

## 76. Edge Family Classification

Future classifications include momentum, breakout, trend, pullback, mean reversion, volatility expansion/compression, relative strength, session, day-of-week, volume, range compression, price location and governed `OTHER`. Classification aids duplication/burden analysis and implements no edge logic.

## 77. Experiment Duplication

Semantic duplicate detection compares hypothesis/mechanism, data, space and transformations across renamed parameters, agents/files and shifted ranges. Duplicates remain separate runs where performed but link to predecessors and count toward burden.

## 78. Experiment Observability

Future observation covers run state/failure rate, trial/budget use, reproducibility failure, lock/config drift, contamination, search-space expansion and package completeness. MON/ORC may report/route only; observability cannot alter scientific rules.

## 79. Concurrency

Dataset invalidation during run, spec supersession, competing campaigns, active configuration change, validation handoff versus new result and packaging quarantine enter conflict routing. Restrictive valid state dominates unresolved consequential conflict; outputs retain the exact state/version observed.

## 80. Idempotency / Replay

Repeated orchestration request ID cannot create ambiguous duplicate institutional effect. Replays link to the original request/result. Every genuine execution attempt gets a new run ID even with identical locks; expired authority or superseded basis cannot be replayed.

## 81. Experiment Security / Integrity

Future protections cover artifact/configuration/dataset-lock integrity, actor identity, least privilege, tamper evidence and audit. This is a requirement boundary only; no credential, sandbox, compute or infrastructure mechanism is designed.

## 82. Test Obligations

Sprint 6 canonical meanings prevail. Thirty-three relevant families are inherited: `T02`, `T03`, `T04`, `T05`, `T06`, `T07`, `T08`, `T09`, `T10`, `T11`, `T12`, `T13`, `T15`, `T16`, `T17`, `T18`, `T19`, `T20`, `T21`, `T22`, `T23`, `T24`, `T25`, `T26`, `T27`, `T28`, `T29`, `T30`, `T32`, `T34`, `T35`, `T36`, `T38`. They retain Sprint 6 labels (for example T09 Human-Gate, T10 Agent-Ceiling, T26 Knowledge/Memory, T27 Monitoring, T28 Orchestration, T29 Emergency, T30 Kill/Release); experiment-specific authorization, completeness, failure and parity cases are obligations within the applicable canonical families, not silently renumbered test families.

## 83. Experiment-Specific Test Attacks

Future attacks hide/delete trials or negatives; change primary metric/search space/dataset/cost; mine seeds; extend budget; rewrite hypothesis post-hoc; reuse holdout; contaminate VAL; cherry-pick market/timeframe/window; exploit parameter boundaries; leak future data; omit burden. Each expects FAIL/HOLD/quarantine with preserved attack evidence and no candidate promotion.

## 84. Validation Candidate Gate

Requires attributable/frozen hypothesis/spec; eligible exact locked dataset and configuration; complete run/trial/campaign histories; declared primary metric; preserved negative/failed evidence; disclosed search burden; known reproducibility/contamination/independence; no blocking temporal/data/quarantine/invalidation; valid authority and complete audit. PASS means only `READY_FOR_INDEPENDENT_VALIDATION`.

## 85. Validation Handoff Package

The immutable package includes hypothesis/spec/pre-registration; Dataset Manifest/lock/quality/temporal reports; configuration lock; every run/trial/campaign record; full Result Package/negative evidence/burden; contamination/holdout access; Reproducibility Package; limitations/contradictions; authority/audit. VAL receives history, not a winning configuration.

## 86. Experiment Decision Separation

`EXPERIMENT SUCCESS ≠ VALIDATION SUCCESS ≠ DECISION APPROVAL ≠ PORTFOLIO ADMISSION ≠ EXECUTION AUTHORITY`. No cross-axis automatic transition exists. EXE-01 remains `PLANNED_CLOSED`.

## 87. Governance Exceptions

Exceptions cannot silently waive exact data/lock identity, temporal integrity, run/trial/campaign history, search burden, truthful provenance/audit or mandatory independence/SoD. These and Phase 2 execution isolation are candidate non-waivable controls. Bounded exceptions expose residual risk/scope/expiry and cannot rewrite evidence.

## 88. Planning ADRs

| ADR | Decision / context | Rationale / rejected alternative | Consequence | Constitutional basis |
|---|---|---|---|---|
| S8-ADR-01 | Hypothesis precedes experiment | Configuration-first search rejected | Scientific question/falsification required | Research OS |
| S8-ADR-02 | Hypothesis version freezes | Outcome rewrite rejected | New version/post-hoc label | Evidence integrity |
| S8-ADR-03 | Pre-register material choices | Hidden flexibility rejected | Amendments visible | Scientific governance |
| S8-ADR-04 | Exact DP-16 dataset lock | Latest-file input rejected | Reproducible input | Sprint 7 |
| S8-ADR-05 | Separate configuration lock | Mutable run setup rejected | Exact run basis | Sprint 3/4 |
| S8-ADR-06 | Every run has new stable ID | Filename/overwrite rejected | Attempts attributable | Audit law |
| S8-ADR-07 | All trials preserved | Winner-only history rejected | Full campaign evidence | Sprint 3 |
| S8-ADR-08 | Failed trials are evidence | Deletion rejected | Failure burden visible | Negative evidence |
| S8-ADR-09 | Negative results first-class | Success-only memory rejected | Survivorship defense | Research OS |
| S8-ADR-10 | Search campaign is an object | Best trial as campaign rejected | Rules/budget/history linked | Artifact model |
| S8-ADR-11 | Disclose complete search burden | Reported-winner denominator rejected | VAL sees selection pressure | Overfitting defense |
| S8-ADR-12 | Multiple testing traced institutionally | Per-run isolation rejected | Duplicate/abandoned work counts | Scientific integrity |
| S8-ADR-13 | Primary metric freezes | Metric substitution rejected | Post-hoc changes explicit | Pre-registration |
| S8-ADR-14 | Stopping/extension governed | Run-until-good rejected | New version/burden | Evidence law |
| S8-ADR-15 | Randomness provenance mandatory | Seed mining/unknown RNG rejected | Reproducibility bounded | Sprint 6 |
| S8-ADR-16 | Reproducibility Package required | “Works on my machine” rejected | Independent reconstruction basis | Sprint 3/6 |
| S8-ADR-17 | Re-run/reproduction/replication distinct | Label collapse rejected | Independence/generalization honest | Scientific method |
| S8-ADR-18 | Holdout identity/access protected | Unlimited peeking rejected | Contamination evidence | VAL boundary |
| S8-ADR-19 | Contamination first-class | Ignore/restart rejected | Eligibility impact routed | Sprint 5/6 |
| S8-ADR-20 | Agent context is provenance | Different-name independence rejected | Context ancestry tested | Agent Framework |
| S8-ADR-21 | Cherry-picking universe disclosed | Best-only package rejected | All inspected choices visible | Evidence completeness |
| S8-ADR-22 | Post-hoc work labeled | Retrospective confirmation rejected | New hypothesis/exploration | Research OS |
| S8-ADR-23 | Optimization ≠ validation | Objective success rejected as robustness | VAL remains independent | Module architecture |
| S8-ADR-24 | EXP ≠ VAL | Self-validation rejected | Separate handoff/gate | Constitutional validation |
| S8-ADR-25 | Search budget predeclared | Unlimited expansion rejected | Extension versioned | Governance control |
| S8-ADR-26 | Champion/challenger is research label only | Deployment status inference rejected | Later authorities preserved | Decision/Risk OS |
| S8-ADR-27 | Invalidation routes contain-first | Delete/destructive cascade rejected | History and impacts preserved | Sprint 4 |
| S8-ADR-28 | Validation handoff is complete history | Winner-only handoff rejected | VAL receives burden/negatives | Sprint 3 |

## 89. Open Questions Register

| ID | Question / source | Stage/module/artifact/workflow/test | C / severity | Status / fail-closed default | Authority | Target / resolution |
|---|---|---|---|---|---|---|
| S8-OQ-01 | Domain-specific A7 experiment authorization catalog? S7-OQ-04/S6-OQ-01 | EP-08; EXP/GOV/IAM; Authorization; WF-03; T08/33 | C3/High | Non-blocking plan; agent A7 denied unless named and eligibility contract passes | H-02/Research Owner | Sprint 12/domain spec |
| S8-OQ-02 | Quantitative independence/contamination thresholds? S7-OQ-03/S6-OQ-02 | EP-15/17; EXP/VAL; contamination/handoff; WF-04; T12 | C3/High | Non-blocking; unproven mandatory dimension blocks | H-06/Evidence Governance | Sprint 9/12 |
| S8-OQ-03 | Freshness policy for dataset/results/reproducibility evidence? S7-OQ-02 | EP-05/14/16; DAT/EXP/VAL; reports; WF-03/05; T05/19 | C2–4/High | Non-blocking; suspected stale basis HOLD | Data/Experiment/Evidence authority | Sprint 9–10 |
| S8-OQ-04 | Production ID syntax and semantic-duplicate matching? S7-OQ-01 | Sections 18–24; IAM/AUD; ledger; WF-03; T35/36 | C3/Medium | Non-blocking; collisions quarantined | Artifact/Workflow Governance | Future implementation spec |
| S8-OQ-05 | Statistical tolerances/oracles by stochastic experiment family? S6-OQ-08 | EP-14/15; EXP/VAL; Repro Package; WF-03/04; T17–T22 | C2–3/High | Non-blocking; no PASS without justified oracle | H-06/Scientific Governance | Sprint 9 |
| S8-OQ-06 | Minimum burden disclosure across manual/off-platform prior searches? New | EP-13/23/24; RES/EXP/KNW; Ledger; WF-01/03; T05/22 | C2–3/High | Non-blocking; unknown burden disclosed and weakens eligibility | Research/Evidence Governance | Sprint 9/12 |
| S8-OQ-07 | Exact holdout custodians and access partitions? New | Sections 48–49; VAL/DAT/IAM; Holdout Record; WF-04; T08/12 | C3/High | Non-blocking; protected holdout inaccessible absent grant | H-06/H-08 | Sprint 9 |
| S8-OQ-08 | Compute/search extension thresholds and authorities by domain? New | Sections 21, 31, 67–68; EXP/GOV; Campaign; WF-03; T08/22 | C2–3/Medium | Non-blocking; undeclared extension blocked/new campaign | Research/Governance authority | Future experiment spec |

Blocking issues for Sprint 8 planning: **0**. Eight bounded questions remain under explicit fail-closed defaults.

## 90. Sprint 9 Handoff Contract

Sprint 9 receives exact hypothesis/spec/pre-registration, dataset Manifest/quality/temporal/lock, configuration lock, complete run/trial/campaign history and burden, Result/Negative/Reproducibility Packages, contamination/holdout access and independence evidence, limitations/contradictions, candidate-gate and authority/audit records. VAL must reject a winner-only backtest, protect validation inputs and preserve EXP≠VAL.

## 91. Definition of Done

The plan defines 13 objects and 21 stages; question/hypothesis/falsification/freeze/spec/pre-registration; Sprint 7 dataset integration and separate locks; stable run/trial/campaign identities; optimization/multiple testing/ledger/failure/negative/result/metric/stopping/randomness/reproducibility; 14 experiment families, ablation/sensitivity/stability/cross-domain/cost/temporal defenses; holdout/contamination/independence/cherry-picking/post-hoc/controls/adversarial/failure/recovery; 38-module responsibility map, C0–C4 and ORC/AUD/MON limits; budgets/champion/comparability/supersession/invalidation/knowledge/duplication/observability/concurrency/replay; 33 canonical test obligations; candidate gate and complete Sprint 9 handoff; 28 ADRs and eight classified questions. No blocker is hidden, no executable infrastructure exists and EXE-01 stays closed.

## 92. Final Sprint Disposition

**SPRINT 8 COMPLETE WITH OPEN GOVERNANCE ITEMS**

Blocking issues: **0 for Sprint 8 planning**. Eight bounded governance/implementation questions remain fail-closed. After governance review and merge, the next authorized planning step is **Phase 2 — Sprint 9: Validation Pipeline Plan**.
