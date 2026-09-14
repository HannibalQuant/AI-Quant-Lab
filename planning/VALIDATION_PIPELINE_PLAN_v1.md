# AI Quant Lab — Validation Pipeline Plan v1.0

## 1. Document Status

| Field | Value |
|---|---|
| Phase / Sprint | Phase 2 — Sprint 9 |
| Status | Proposed for governance review |
| Canonical path | `planning/VALIDATION_PIPELINE_PLAN_v1.md` |
| Constitutional baseline | Tag `v1.0`, commit `50b61266f880cb9657b7f1b477d3d90825fe013f` |
| Phase 2 baseline | Sprints 1–8; current `main` merge `ffd2ab50a6ed061be0581f678f2f37bf97cc6da1` |
| Version | 1.0 |
| Implementation / execution authority | None; EXE-01 remains `PLANNED_CLOSED` |

This is a non-executable planning contract. It creates validation obligations, not engines, strategy approval, deployment permission or capital authority.

## 2. Purpose

Define how an independently governed validation function attempts to disprove experiment claims through provenance, holdout integrity, reproduction, null comparisons, temporal/statistical robustness, adversarial controls and complete evidence before any decision-system handoff.

## 3. Authority and Inheritance

Authority descends: Constitutional Baseline → Planning Charter → Module Architecture → Artifact/Evidence Contracts → Workflow/State Blueprint → Responsibility Matrix → Test Architecture → Data Pipeline → Experiment Pipeline → this plan → future specifications. Validation Agent, Scientific Research OS, Decision OS, risk, evidence, communication and memory contracts remain superior in scope. Conflict or missing authority produces HOLD/quarantine and explicit escalation.

## 4. Scope

This plan covers 12 validation object classes, 30 stages, 16 validation method families, 41 relevant modules, all 12 Sprint 5 authority classes, 13 agent roles, relevant human roles, 28 mapped Sprint 6 test families, 27 ADRs and independent handoffs to decision, risk and Sprint 10 monitoring planning.

## 5. Non-Goals

No Python, Pine, JS/TS, notebook, test, backtest, walk-forward/Monte Carlo/bootstrap/PBO/DSR/optimizer engine, database, executable schema, API/CLI, CI, scheduler/worker, monitor, integration, trading, order, portfolio execution or deployment is implemented. No strategy, parameter, formula implementation, split percentage, threshold or deployability verdict is selected.

## 6. Governing Validation Principles

1. Experiment produces a claim; validation independently tries to break it.
2. No validation from a single backtest, parameter point or winner-only package.
3. Complete search burden, failures, negatives and contradictions are mandatory inputs.
4. Holdout, actor, context, data, implementation and decision independence are evidenced, not assumed.
5. Temporal integrity and exact versions precede every robustness claim.
6. Negative controls and deliberately bad cases test the validator itself.
7. Robustness/generalization claims never exceed tested markets, windows, regimes or costs.
8. Missing provenance, independence, authority or audit fails closed.
9. VALIDATED ≠ APPROVED ≠ DEPLOYABLE ≠ EXECUTED.
10. A6 validation never creates A8 executive or A11 execution authority.

## 7. Terminology

| Term | Meaning | Not equivalent to |
|---|---|---|
| Candidate | Complete Sprint 8 handoff eligible for intake | Valid strategy |
| Validation specification | Independently defined scoped challenge plan | Experiment specification |
| Holdout | Protected data role with access history | Any OOS slice |
| Validation run | Attributable execution attempt of a method | Disposition |
| Robustness evidence | Method-specific stress/falsification evidence | Guaranteed future performance |
| Disposition | Scoped scientific validation state | Executive/risk/deployment decision |
| Contradiction | Evidence inconsistent with claim or other evidence | Averaging target |
| Revalidation | New versioned validation after trigger | Editing prior verdict |

## 8. Validation Object Model

| Object class | Contract boundary |
|---|---|
| VALIDATION_CANDIDATE | Full experiment handoff and declared scope |
| VALIDATION_SPECIFICATION | Frozen independent method/obligations |
| INDEPENDENCE_RECORD | Actor/model/context/data/authority evidence |
| HOLDOUT_RECORD | Identity, role, access and contamination history |
| VALIDATION_RUN | One method execution attempt |
| METHOD_EVIDENCE | OOS/WF/MC/bootstrap/stability/etc. evidence |
| NEGATIVE_CONTROL_EVIDENCE | Known-bad/null rejection evidence |
| OVERFITTING_ASSESSMENT | Multi-signal diagnostic matrix |
| CONTRADICTION_RECORD | Scope/materiality/impact and response |
| VALIDATION_EVIDENCE_PACKAGE | Consolidated references without source rewrite |
| VALIDATION_DISPOSITION | Scoped independent conclusion |
| DECISION_HANDOFF | Immutable downstream evidence/limits package |

## 9. Validation Pipeline Stages

| ID | Stage | Output / fail-closed boundary |
|---|---|---|
| VP-00 | Validation Candidate Intake | Candidate identity/custody or return |
| VP-01 | Candidate Completeness Check | Completeness evidence or HOLD |
| VP-02 | Provenance Verification | Exact lineage or quarantine |
| VP-03 | Search Burden Verification | Complete/unknown burden disposition |
| VP-04 | Independence Verification | Independence Record or BLOCK |
| VP-05 | Holdout Integrity Verification | Protected/uncontaminated scope |
| VP-06 | Reproducibility Verification | Reproduction disposition |
| VP-07 | Baseline / Null Comparison | Reference/null evidence |
| VP-08 | Out-of-Sample Validation | OOS evidence |
| VP-09 | Walk-Forward Validation | Fold/path evidence |
| VP-10 | Monte Carlo Robustness | Outcome/tail distributions |
| VP-11 | Bootstrap / Resampling Analysis | Dependence-aware evidence |
| VP-12 | Parameter Stability Validation | Surface/neighborhood evidence |
| VP-13 | Temporal Robustness Validation | Window/structural-break evidence |
| VP-14 | Cross-Market Robustness | Market-scope evidence |
| VP-15 | Cross-Timeframe Robustness | Bar/timeframe evidence |
| VP-16 | Regime Robustness | Regime concentration/failure evidence |
| VP-17 | Cost / Slippage / Friction Stress | Deterioration evidence |
| VP-18 | Perturbation Testing | Input/execution/parameter sensitivity |
| VP-19 | Negative-Control Testing | Known-bad rejection evidence |
| VP-20 | Adversarial Validation | Attack outcomes |
| VP-21 | Multiple-Testing / Selection-Bias Assessment | Burden/PBO/DSR-family evidence |
| VP-22 | Overfitting Diagnostics | Diagnostic matrix |
| VP-23 | Evidence Contradiction Review | Materiality/impact route |
| VP-24 | Validation Evidence Consolidation | Referenced immutable package |
| VP-25 | Independent Validation Review | Review/challenge record |
| VP-26 | Validation Disposition | Scoped authorized A6 disposition |
| VP-27 | Decision-System Handoff | Evidence/limits, no decision |
| VP-28 | Failure / Quarantine / Invalidation | Containment/impact record |
| VP-29 | Audit / Reproduction / Archive | Full reconstruction/history |

No stage auto-authorizes another. Every consequential transition resolves current state, evidence, provenance, authority, independence, scope, contradictions and audit.

## 10. Candidate Intake

Sprint 8 supplies question/hypothesis/version, specification/pre-registration, dataset identity/Manifest/quality/temporal report/lock, configuration lock, experiment authorization, complete runs/trials/campaigns including failed/pruned/rejected work, negative evidence/contradictions, metric definitions/roles, stopping/search budget/randomness/cost assumptions, Reproducibility Package, lineage and audit. Intake records exact versions and never silently repairs history.

## 11. Completeness Gate

Structural, provenance, scientific, reproducibility and governance completeness remain separate Sprint 3 axes. Missing critical locks, search history, failed trials, primary metric, negative evidence, independence or audit produces HOLD/BLOCK/quarantine according to integrity. A structurally full winner-only package fails scientific completeness.

## 12. Provenance Gate

Reconstruct source/raw/dataset/transformation, experiment/configuration locks, implementation/environment, actors/authority, every run/trial/campaign and derived result. Filename, registry storage or matching metric is insufficient. Broken or unverifiable consequential lineage quarantines evidence and blocks VP-08 onward.

## 13. Search Burden Gate

Verify disclosed hypotheses, experiments, campaigns, configurations, markets, timeframes, windows, metrics, seeds, costs, regimes, holdout exposures and abandoned/duplicate work. Unknown off-platform burden is explicitly marked and constrains interpretation; best-trial evidence alone cannot pass.

## 14. Independence

Independence dimensions cover actor, role, agent instance, model/provider/version, prompt/contract, context/memory, dataset/holdout, implementation, experiment, validation specification, metric/parameter selection, evidence ancestry and decision ancestry. Signals include stable IDs, authorship/access/context lineage, conflicts and authority records.

Dangerous cases—renamed same agent, shared model/context, reading winners before designing validation, producer-designed post-result validation, optimizer-selected window/holdout, shared-memory or prior-data contamination, agent consensus and different instances with common contaminated ancestry—fail mandatory independence. No numeric score compensates for a non-waivable failed dimension.

## 15. Holdout Governance

TRAIN, INTERNAL VALIDATION, TEST, HOLDOUT and FINAL HOLDOUT are declared data roles, not universal split percentages. Holdout Record freezes identity/scope/creation/custodian/access policy and every observation/query. Reuse, peeking, tuning, post-observation metric/parameter changes, undisclosed search extension, post-result selection or overlap creates contamination evidence and may require a new protected holdout or inconclusive/failure disposition.

## 16. OOS Validation

OOS evidence binds chronological separation, information availability, previously unseen status/access history, exact dataset/window/version, costs, regime/sample context and IS comparison/degradation. OOS success is one challenge result, not a robustness/generalization claim; failure interpretation distinguishes expected degradation, instability, data defect and insufficient power.

## 17. Walk-Forward

Rolling and anchored TRAIN→TEST cycles record fold count/identity, temporal ordering, re-estimation/selection boundaries, zero future leakage, parameters per fold, fold evidence, aggregate/worst-fold behavior, dispersion, failures, regimes and path dependence. Universal thresholds are deferred. Hidden failed folds or aggregate-only reporting fails completeness.

## 18. Monte Carlo

Future trade-order shuffle, bootstrap/block bootstrap, return/execution/cost/parameter/missing-trade/timing perturbations and randomized sequences generate outcome, drawdown/tail, failure-probability, dispersion, path-sensitivity and fragility evidence. Each method states preservation assumptions, seed/process and limits; no production threshold is set.

## 19. Bootstrap

Validation distinguishes IID, block/stationary or other dependence-aware resampling, trade versus return bootstrap and regime-aware designs. Financial observations are not assumed IID. Block choice, dependence assumptions, seed and sample construction are versioned; incompatible methods cannot support strong claims.

## 20. Parameter Stability

Stability Maps inspect neighborhoods, perturbations, plateaus/cliffs, isolated peaks, smooth degradation, unstable regions, interactions and boundary effects across the declared search space. An exact-point optimum is fragile evidence. The full surface and failures are retained; no magic stability score is adopted.

## 21. Temporal Robustness

Scientifically justified windows may include 3/6/9/12/24/36 months without requiring all. Evidence assesses concentration, decay, structural breaks, recent/historical divergence, crisis and low/high volatility behavior with exact cutoffs. Window mining and omitted periods remain visible.

## 22. Cross-Market Robustness

Where a portability claim exists, test separately attributable crypto, forex, metals, commodities, indices and equities with exact venue/instrument/data/cost semantics. Market-specific hypotheses need not pass unrelated markets, but cannot claim portability without evidence. Failed markets stay in scope and burden.

## 23. Cross-Timeframe Robustness

Scientifically relevant neighbors such as 15m, 30m, 1H, 2H, 3H, 4H, 6H, 12H and 1D preserve bar alignment/session/timezone/availability/resampling lineage. Evidence tests immediate disappearance, single-bar dependence and session/resampling artifacts; not all timeframes are universally required.

## 24. Regime Robustness

Versioned, non-leaking regime definitions may include TREND_UP/DOWN, RANGE, HIGH/LOW_VOL, BREAKOUT, MEAN_REVERSION, TRANSITION and UNCERTAIN. Assess concentration, failure, transitions and classification uncertainty. Regime filtering selected after outcomes is post-hoc/search burden.

## 25. Cost / Slippage Stress

Challenge commission, spread, slippage, funding, borrow, latency, market impact, session availability and liquidity assumptions using explicit scenario/source versions. Edge survival is scoped to tested deterioration; favorable-cost omission or scenario cherry-picking fails evidence completeness.

## 26. Execution-Assumption Validation

Test signal/decision timestamps, information/bar-close availability, order eligibility, next-bar open, intrabar/fill/partial-fill assumptions and unavailable periods. Lookahead or impossible fills invalidate affected evidence. Future Pine↔Python parity has T02/T03/T17/T19/T29 obligations but creates no execution capability.

## 27. Perturbation Testing

Declared parameter, data, timing, missing-trade, cost, execution and sampling perturbations test local robustness while preserving exact seed/design and baseline relationship. Perturbation cannot alter protected holdout or become undeclared optimization.

## 28. Negative Controls

Random entries/exits, shuffled returns, shifted signals, random labels, noise/placebo features, destroyed temporal order, meaningless parameters, synthetic nulls, impossible alpha and future-leak positive controls verify rejection capability. A validator that accepts known-bad controls fails validation-of-validation and is quarantined.

## 29. Adversarial Validation

Attack data/lookahead/selection leakage, cherry-picking, metric switching, holdout reuse, hidden trials/markets/timeframes, optimizer/seed/regime/timeframe/market mining, costs, parameter cliffs, post-hoc rewriting, contamination/fake independence, agent collusion/consensus, human override and provenance gaps. Expected response is detection, preservation and containment—not helpful confirmation.

## 30. Multiple Testing

Use Sprint 8 total burden across hypotheses/configurations/markets/timeframes/windows/metrics/seeds/costs/regimes/holdout exposures/abandoned work. Future family-wise error, false-discovery, DSR, PBO, bootstrap confidence and reality-check concepts may be specified. Formulas and thresholds remain future governed choices; undisclosed burden blocks strong validation.

## 31. PBO

Conceptual Probability of Backtest Overfitting consumes the complete candidate set, selection rule, partitions and IS/OOS ranking behavior to evaluate selection-process overfit. It cannot be reconstructed meaningfully from a lone winner. Incomplete history yields `PBO_NOT_INTERPRETABLE`, not a favorable estimate.

## 32. Deflated Sharpe

Conceptual DSR contextualizes observed Sharpe using trial burden/selection and distributional properties such as variance, skew and kurtosis where applicable. Metric/calculation assumptions are versioned. It supplements, never replaces, falsification and receives no universal pass threshold here.

## 33. Overfitting Diagnostics

| Evidence signal | Fragility concern | Required response |
|---|---|---|
| IS/OOS degradation or unstable folds | Sample fitting/path dependence | Scope, challenge, fail/condition |
| Parameter cliffs/isolated peak/boundary optimum | Parameter fragility | Stability evidence/HOLD |
| Market/timeframe/regime/window concentration | Mining or narrow scope | Bound claim; retain failures |
| Extreme winner under large burden | Selection bias | PBO/DSR-family review |
| Poor reproduction/seed fragility | Process dependence | Reproduction/revalidation |
| Null-like or negative-control similarity | False edge | Fail/challenge |
| Cost/tail fragility or low effective sample | Economic/statistical weakness | Risk note, condition/fail |
| Suspicious smoothness/impossible alpha | Leakage/data defect | Quarantine/invalidate |
| Holdout/context contamination | Invalid independence | New clean validation or fail |

No single magic score can erase a blocking diagnostic.

## 34. Validation-of-Validation

Governed golden/adversarial cases include known overfit, random, leaking, unstable, one-period, impossible-alpha, massive-search-selected, hidden-failure, contaminated-holdout, seed-dependent and unrealistic-cost strategies. Validator versions must reject/detect these and reproduce expected invariants; surviving critical mutations block readiness.

## 35. Reproducibility

Deterministic, stochastic, agent/LLM and market-data-dependent components follow Sprint 6 R0–R5. Record model/provider/version, prompt/spec/contract, context/memory/tools, exact data/holdout, seeds/process, environment/implementation, outputs/package and deviations. Agent prose need not be bit-identical, but lineage and governed invariant outcomes must be reproducible.

## 36. Validation Evidence Package

Includes validation ID/version, candidate/hypothesis/experiment lineage, validator identity and Independence Record, datasets/holdouts/specification/methods and every run; OOS/WF/MC/bootstrap/stability/temporal/market/timeframe/regime/cost/perturbation/negative-control/adversarial/multiple-testing/overfitting evidence; reproduction, contradictions, failures, limits/questions, disposition and audit. Aggregation references rather than rewrites source evidence.

## 37. Validation Dispositions

| Disposition | Meaning / permitted consequence |
|---|---|
| VALIDATED | Required program survived within exact scope; may enter decision review only |
| CONDITIONALLY_VALIDATED | Bounded survival with explicit conditions/expiry/follow-up |
| FAILED_VALIDATION | Material falsification/guard failure; preserve and stop promotion |
| INCONCLUSIVE | Evidence cannot support pass or failure; no promotion |
| REVALIDATION_REQUIRED | Prior basis changed/staled; new attempt needed |
| QUARANTINED | Integrity/authority uncertainty blocks use pending resolution |

No disposition means deployment, trading or A11.

## 38. VALIDATED Semantics

VALIDATED means the candidate survived required methods within declared data, market, timeframe, regime, cost, implementation and time boundaries. It does not guarantee profit or future stability and is not capital approval, portfolio admission, deployment/readiness, live state or execution authority.

## 39. CONDITIONAL Validation

The record names every condition, weakness, scope, freshness/expiry trigger, required evidence/review and prohibited interpretation. Conditions propagate into decision/risk/monitoring handoffs. No registry, ORC or consumer may silently upgrade it.

## 40. Failed Validation

Preserve candidate, methods, failed controls/folds/markets, contradictions and authority/audit. Failure may generate revised hypothesis/new experiment, negative institutional knowledge, risk warning or anti-pattern—but never edits the original experiment or disappears from burden.

## 41. Inconclusive

Applies to insufficient sample, conflicting robustness evidence, unresolved integrity/independence, missing search history or excessive uncertainty. It blocks consequential progression. More computation alone does not convert uncertainty into PASS without a new governed specification/evidence.

## 42. Revalidation

Triggers include new data/regime, material source revision, implementation/metric/selection/cost change, contamination, invalidated dependency, material monitoring/edge decay and staleness. Revalidation has new identity/version/specification/locks where affected and preserves the prior disposition.

## 43. Contradictions

`FOUND → REGISTERED → SCOPE/MATERIALITY ASSESSED → HOLD / CONTINUE BOUNDED / FAIL / QUARANTINE → RESPONSE/AUDIT`. Supporting and contradicting evidence coexist. Only competent scientific/governance authority classifies impact; AUD-02 custody does not decide truth.

## 44. Failure Modes

Missing provenance; invalid/stale lock; temporal leakage; holdout/context contamination; incomplete burden/search/failure/negative history; independence/reproduction failure; unstable parameters/folds/cost/market/timeframe/regime; negative-control/adversarial failure; multiple-testing/overfit concern; conflicting evidence; authority/audit failure all record exact scope. Responses include RETURN, HOLD, BLOCK, quarantine, fail, revalidate, invalidate or escalate.

## 45. Quarantine

Critical uncertainty preserves evidence and last valid state, blocks progression, routes competent review and prevents retries from expanding authority. Release needs resolved cause, current exact evidence, independent reviewer, competent authorization and audit. Unresolved items remain quarantined or invalidated.

## 46. Recovery

Recovery identifies cause and creates new evidence, versions, validation attempt and audit chain; changed data/spec/implementation gets new locks/identities. Every failed gate is repeated. Old failed evidence/disposition is immutable and linked.

## 47. Authority

All Sprint 5 classes apply: A0 observe, A1 produce, A2 request, A3 challenge, A4 review, A5 recommend, A6 validate, A7 authorize bounded process, A8 executive approve/reject, A9 contain/halt, A10 kill, A11 future execution. VAL may exercise only explicit A6/A0–A5/A7 process grants. A6≠A8≠A11; A11 is unavailable. Recorder/registry/orchestrator/consensus cannot manufacture a disposition.

## 48. Agent/Human Responsibilities

All 13 agents—Validation, Experiment Orchestrator, Quant Strategy Architect/Engineer, Market Research, Risk Governance, Executive Decision, QA, Python, Pine, Research Librarian, Knowledge Curator and CEO Agent—are bounded by identity, contract, instance/context lineage and Sprint 5 ceilings. Producer/optimizer/author may answer challenges but not serve as sole VA; Validation Agent produces evidence/recommends/issues only scoped A6; Risk/Executive agents consume but cannot backfill validation. H-06 is accountable validation authority; H-02 governance, H-08 data, H-10 audit, H-03 decision and H-04 risk remain distinct. Name never creates authority.

## 49. Segregation of Duties

Prohibit experiment producer, optimizer or strategy author as sole validator; validator as sole executive approver; risk assessor approving own exception; monitor retuning; ORC or AUD gaining validation authority. Same person/model across roles requires conflict evidence and independent control; non-waivable independence failure blocks validation.

## 50. Orchestration Boundary

ORC may sequence, route, check prerequisites, request work and record workflow state. It cannot validate, waive a method, create authority, override failure, declare independence, promote or execute. “All tasks complete” is not A6.

## 51. Audit Boundary

AUD preserves, registers, links and reconstructs exact evidence and authority. It cannot validate because evidence is stored, approve because fields are complete, authorize, promote or execute. Audit gaps cause failure; ledger writes do not cure them.

## 52. Monitoring Boundary

Sprint 10 may observe decay, regime/performance/cost/data divergence and validation freshness, then generate evidence/request review/HOLD/revalidation. MON cannot retune, revalidate, reapprove or reactivate. Sprint 9 implements no monitor.

## 53. Decision Handoff

Immutable handoff states disposition/scope, confidence limits (not false certainty), contradictions, risk observations, unresolved items, freshness/revalidation triggers, full Validation Evidence Package and audit/authority. DEC independently checks evidence/authority; validation cannot approve its own downstream decision.

## 54. Risk Handoff

Surface tail/drawdown/parameter/fold/cost fragility, low sample, market/timeframe/regime concentration and temporal decay with exact evidence. RSK may constrain or reject scientifically validated candidates. VAL sets no live limits and performs no capital acceptance.

## 55. Freshness

Triggers include new market data/regime, dataset/source revision, implementation/configuration/metric/cost change, elapsed policy interval and monitoring evidence. Each evidence class later receives governed policy; no universal duration is invented. Triggered/unknown material freshness marks evidence stale or review-required and blocks silent reuse.

## 56. Lineage

`QUESTION → HYPOTHESIS → EXPERIMENT/PRE-REGISTRATION → DATASET/CONFIG LOCKS → RUNS/TRIALS/CAMPAIGN → RESULT PACKAGE → CANDIDATE → VALIDATION SPEC → VALIDATION RUNS/METHOD EVIDENCE → PACKAGE → DISPOSITION → DECISION/RISK/MONITORING HANDOFF`. Every edge uses exact identity/version and survives supersession/invalidation.

## 57. Test Integration

Sprint 6 families mapped: T02 module, T03 integration, T04 artifact, T05 evidence, T06 workflow, T07 state, T08 authority, T09 human gate, T10 agent ceiling, T11 SoD, T12 independence, T13 delegation, T15 data, T16 temporal, T17 reproducibility, T18 determinism, T19 regression, T20 validation architecture, T21 negative controls, T22 adversarial, T23 failure, T24 recovery, T25 audit, T32 quarantine, T33 criticality, T36 version/lineage, T37 execution isolation and T38 end-to-end. Each method has positive, negative, contamination, failure/recovery and reconstruction cases.

## 58. Validation Test Matrix

| Requirement | Failure | Positive / negative / adversarial test | Evidence / authority / C | Fail-closed response / future obligation |
|---|---|---|---|---|
| Intake/completeness | Missing history/negatives | Complete package; remove trial/burden | Checklist/package; A4; C3 | HOLD; implement gate |
| Provenance | Broken/wrong version | Reconstruct; swap lock/lineage | Manifest/ledger; A4; C3 | Quarantine; exact-version resolver |
| Independence/holdout | Shared context/peek | Clean separation; renamed-agent/shared-memory attack | Independence/access records; A6/H-06; C3 | BLOCK/reassign/new holdout |
| OOS/WF | Leakage/unstable folds | Ordered unseen windows; future-fold/hidden-failure attack | Fold evidence; A6; C3 | Fail/inconclusive |
| MC/bootstrap | Invalid dependence/seed | Reproducible distributions; IID misuse/seed mining | Run/process manifests; A6; C2–3 | Condition/fail |
| Stability/temporal | Isolated peak/window mining | Plateau/windows; boundary/cherry-pick attack | Surfaces/window evidence; A6; C3 | Bound claim/fail |
| Market/timeframe/regime | Concentration/mining | Scoped portability; omit failed domain attack | Domain evidence; A6; C3 | Narrow scope/fail |
| Costs/execution | Optimistic/leaking fills | Stress and timing; zero-cost/future-fill attack | Scenario/parity evidence; A6; C3 | Fail/condition |
| Controls/adversarial | Known bad accepted | Reject nulls; impossible-alpha case | Control evidence; H-06 review; C3 | Quarantine validator |
| Multiple testing | Winner-only burden | Complete burden; hidden search attack | Ledger/PBO/DSR inputs; A6; C3 | Inconclusive/fail |
| Disposition/authority | A6→A8/A11 | Valid scoped disposition; self-promotion attack | Authority/audit; H-06; C3–4 | BLOCK/escalate |
| Revalidation/recovery | Old verdict overwritten | New identity/gates; retry-bypass attack | Versioned package; A6; C3 | Preserve old/HOLD |
| Audit/isolation | Missing reconstruction/execution attempt | Full chain; VALIDATED→ORDER attack | AUD evidence; H-10/GOV; C4 | FAIL/BLOCK |

## 59. Execution Isolation

Prohibited transitions include `VALIDATED→EXECUTE`, `VALIDATED→LIVE`, `VALIDATED→ORDER`, `VALIDATED→CAPITAL`, `A6→A11` and `VAL→EXE-01`. T37/T38 require every attempt to block, preserve state/evidence and emit governance/audit alert. EXE-01 remains `PLANNED_CLOSED`.

## 60. Traceability Matrix

Forty-one relevant modules are mapped: `VAL-01`, `VAL-02`, `VAL-03`, `VAL-04`, `VAL-05`, `VAL-06`, `VAL-07`; `EXP-01`, `EXP-02`, `EXP-03`, `EXP-04`, `EXP-05`, `EXP-06`; `DAT-01`, `DAT-02`, `DAT-03`, `DAT-04`, `DAT-05`; `RES-01`, `RES-02`, `RES-03`; `AUD-01`, `AUD-02`, `AUD-03`; `GOV-01`, `GOV-02`; `IAM-01`, `IAM-02`; `ORC-01`, `ORC-02`, `ORC-03`; `MON-01`, `MON-02`, `MON-03`; `DEC-01`, `DEC-02`; `RSK-01`, `RSK-02`; `KNW-01`, `KNW-02`, `KNW-03`.

| Constitutional requirement | Planning/module | Experiment artifact | Validation method/evidence | Authority/test | Failure/downstream |
|---|---|---|---|---|---|
| Independent validation | Charter; VAL/EXP split | Candidate/full history | Independence, OOS/WF; package | A6/H-06; T11/12/20 | BLOCK; DEC handoff denied |
| Exact evidence/provenance | S3/S7; DAT/AUD | Locks/Manifest/Result | VP-01/02/06 | A4/A6; T04/05/17/36 | Quarantine/reproduce |
| Negative/search visibility | S3/S8; RES/EXP/KNW | Ledger/campaign/failures | VP-03/19/21/22 | A4/A6; T05/21/22 | Inconclusive/fail |
| Temporal integrity | S7; DAT/VAL | TIR/holdout/runs | OOS/WF/timeframe | A6; T16/20 | Invalidate/revalidate |
| Scientific robustness | Research OS; VAL-02..06 | Specification | MC/bootstrap/stability/domain/cost | A6; T18–22 | Bound/fail/condition |
| Authority separation | S4/S5; GOV/IAM/DEC/RSK | Disposition/handoff | Independent review | H-06 then DEC/RSK; T08–12/33 | HOLD/escalate |
| Auditability | Charter; AUD-03 | All exact versions | VP-24/29 package | H-10 recorder≠A6; T25 | FAIL |
| Execution isolation | Charter; EXE-01 boundary | No execution artifact | Prohibited transitions | No A11; T37/38 | BLOCK/governance alert |

## 61. Planning ADRs

| ADR | Decision | Rejected alternative / consequence | Constitutional basis |
|---|---|---|---|
| S9-ADR-01 | Independence evidenced across actor/context/data/authority | Different-name validator; failure blocks | Agent/validation law |
| S9-ADR-02 | Holdout identity/access immutable | Reusable secret test; contamination recorded | Scientific integrity |
| S9-ADR-03 | OOS is necessary where scoped, never sufficient alone | Single OOS proof; bounded evidence | Research OS |
| S9-ADR-04 | Rolling/anchored WF retain every fold | Aggregate-only reporting; worst/dispersion visible | Negative evidence |
| S9-ADR-05 | MC process/assumptions/seeds attributable | Unspecified simulation; reproducibility | Sprint 6 |
| S9-ADR-06 | Bootstrap declares dependence model | Automatic IID; limitation visible | Statistical humility |
| S9-ADR-07 | Stability uses neighborhoods/surfaces | Best point; fragility exposed | Overfitting defense |
| S9-ADR-08 | Temporal claims match tested windows | Best-period claim; failures retained | Scope law |
| S9-ADR-09 | Portability needs cross-market evidence | One-market generalization; scope bounded | Evidence scope |
| S9-ADR-10 | Timeframe robustness preserves bar semantics | Similar labels; resampling artifacts tested | Sprint 7 |
| S9-ADR-11 | Regime definitions versioned/non-leaking | Post-hoc regimes; uncertainty retained | Temporal integrity |
| S9-ADR-12 | Cost/friction deterioration challenged | Optimistic single cost; conditional/fail | Risk evidence |
| S9-ADR-13 | Known-bad controls mandatory | Validator self-trust; validator may fail | Sprint 6 |
| S9-ADR-14 | Adversarial validation first-class | Confirmation checklist; attacks evidenced | Falsification |
| S9-ADR-15 | Total search burden enters validation | Winner-only denominator; strong claims blocked | Sprint 8 |
| S9-ADR-16 | PBO requires complete selection history | Winner-only PBO; not interpretable | Scientific method |
| S9-ADR-17 | DSR is contextual evidence, not magic gate | Universal threshold; multi-evidence assessment | Statistical humility |
| S9-ADR-18 | Overfitting uses diagnostic matrix | Single score; blockers cannot average away | Evidence completeness |
| S9-ADR-19 | Failed validation remains immutable | Delete/retry overwrite; institutional memory | Sprint 3 |
| S9-ADR-20 | Six dispositions are separate scoped states | Pass/fail collapse; uncertainty explicit | Sprint 4 axes |
| S9-ADR-21 | Revalidation creates new identity | Edit old verdict; historical meaning preserved | Version law |
| S9-ADR-22 | Critical uncertainty quarantines | Optimistic continuation; block and review | Fail closed |
| S9-ADR-23 | A6 does not imply A8/A11 | Validator promotion; decision/execution separate | Sprint 5 |
| S9-ADR-24 | AUD records, never validates | Stored-is-approved; authority separate | AUD boundary |
| S9-ADR-25 | EXE-01 isolation is P0 | Validation-created deployment; attempts block | Constitutional boundary |
| S9-ADR-26 | Reproduction precedes strong validation where required | Producer rerun only; independence evidenced | Reproducibility law |
| S9-ADR-27 | Contradictions coexist and route impact | Averaging/deletion; challenge remains visible | Sprint 3/4 |

## 62. Open Governance Questions

| ID | Question / source | Domain / C | Status / fail-closed default | Authority | Resolution path |
|---|---|---|---|---|---|
| S9-OQ-01 | Quantitative independence/contamination criteria? S8-OQ-02 | VAL/holdout; C3 | Non-blocking plan; failed mandatory dimension blocks | H-06/Evidence Governance | Sprint 12/future spec |
| S9-OQ-02 | Freshness policies by validation/evidence class? S8-OQ-03 | VAL/MON; C2–4 | Non-blocking; trigger/uncertainty means stale/HOLD | Evidence/VAL/MON authority | Sprint 10 |
| S9-OQ-03 | Statistical tolerances/oracles by method/family? S8-OQ-05 | VAL/statistics; C3 | Non-blocking; no PASS without justified preregistered oracle | H-06/Scientific Governance | Future validation spec |
| S9-OQ-04 | Minimum treatment of unknown prior/off-platform search burden? S8-OQ-06 | Multiple testing; C3 | Non-blocking; disclose unknown and prohibit strong validation | Research/Evidence Governance | Sprint 12 |
| S9-OQ-05 | Exact holdout custodians/access partitions? S8-OQ-07 | IAM/DAT/VAL; C3 | Non-blocking; access denied absent exact grant | H-06/H-08 | Sprint 12/future IAM spec |
| S9-OQ-06 | Method obligations by hypothesis/market and waiver policy? New | VAL program; C3 | Non-blocking; omitted relevant method requires independent rationale/authority | H-06/Scientific Governance | Future validation spec |
| S9-OQ-07 | PBO/DSR and multiple-testing implementation standards/thresholds? New | Overfitting; C3 | Non-blocking; no quantitative claim before governed method | H-06/Scientific Governance | Future implementation spec |
| S9-OQ-08 | Cross-market/timeframe comparability rules and minimum neighboring scope? New | Generalization; C2–3 | Non-blocking; claims limited to exact tested scope | H-06/domain authority | Future validation spec |
| S9-OQ-09 | Phase 2 exit-review composition and validation sign-off? S6-OQ-07 | Governance; C4 | Non-blocking Sprint 9; blocks Sprint 12 exit | Existing governance authority | Sprint 12 |

Blocking issues for Sprint 9 planning: **0**. Nine bounded questions remain explicit and all affected implementation/claims fail closed.

## 63. Sprint 10 Handoff

Sprint 10 receives validation/disposition identity, exact validated scope and expected behavior, baseline metrics/distributions, robustness/parameter/temporal/market/timeframe/regime/cost boundaries, known weaknesses/contradictions, freshness/revalidation triggers, failures and risk observations, monitoring-relevant evidence, edge-decay hypotheses, lineage and authority/audit. Monitoring may detect/request/contain only; it cannot retune, revalidate, reapprove or reactivate.

## 64. Definition of Done

Current main and Sprint 8 baseline were verified; one artifact defines 12 objects, 30 stages, completeness/provenance/burden/independence/holdout, OOS/WF/MC/bootstrap/stability/temporal/market/timeframe/regime/cost/execution/perturbation/control/adversarial/multiple-testing/PBO/DSR/overfit/meta-validation/reproduction, package/dispositions/freshness/revalidation/contradictions/failure/quarantine/recovery, all A0–A11 and 13 agents/humans/SoD, ORC/AUD/MON/DEC/RSK boundaries, 41 modules, 28 tests, execution isolation, traceability, 27 ADRs, nine questions and Sprint 10 handoff. Constitution/Sprints 1–8 remain unchanged; no runtime/trading/code exists; EXE-01 is closed.

## 65. Final Sprint Disposition

**SPRINT 9 COMPLETE WITH OPEN GOVERNANCE ITEMS**

Blocking issues: **0 for Sprint 9 planning**. Nine bounded governance/method questions remain fail-closed. After governance review and merge, the next authorized planning step is **Phase 2 — Sprint 10: Monitoring & Edge Decay Plan**.
