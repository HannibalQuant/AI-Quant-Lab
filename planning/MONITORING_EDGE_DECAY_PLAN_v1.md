# AI Quant Lab — Monitoring & Edge Decay Plan v1.0

## 1. Document Status

| Field | Value |
|---|---|
| Phase / Sprint | Phase 2 — Sprint 10 |
| Status | Proposed for governed review |
| Canonical path | `planning/MONITORING_EDGE_DECAY_PLAN_v1.md` |
| Constitutional baseline | AI Quant Lab v1.0, tag `v1.0`, commit `50b61266f880cb9657b7f1b477d3d90825fe013f` |
| Sprint 9 baseline | Merge `1f019a7840019676bdf0de1f548aeca01978816f` |
| Change class | Non-executable planning artifact |
| Implementation / execution authority | None; `EXE-01` remains `PLANNED_CLOSED` |

This Plan creates documentary contracts and future obligations. It does not monitor a strategy, issue an executable alert, alter a parameter, authorize capital, or open execution.

## 2. Purpose

Define how AI Quant Lab will compare governed validation expectations with attributable observations, preserve competing explanations, recognize possible edge decay, and route evidence without turning monitoring into validation, retuning, decision, risk acceptance, or execution authority.

## 3. Authority and Inheritance

Authority descends from the Constitutional Baseline through the Sprint 1 Charter, Sprint 2 Module Architecture, Sprint 3 Artifact/Evidence System, Sprint 4 Workflow/State Blueprint, Sprint 5 Responsibility Matrix, Sprint 6 Test Plan, Sprint 7 Data Plan, Sprint 8 Experiment Plan, Sprint 9 Validation Plan, then this Plan. Applicable constitutional sources include MEDS, the Edge Decay Response Playbook, Decision OS, Agent Contract Framework, MACP, SMI, EES, WOE, ART, RRP, EDP, VEP and agent contracts.

MEDS references future paper/live/deployment states. This Plan inherits its monitoring semantics but does not activate those states: Phase 2 execution remains closed. A conflict with superior governance is held and escalated; it is never repaired by silent reinterpretation.

## 4. Scope

This Plan covers monitoring eligibility, baselines, observations, windows, metrics, performance/statistical/risk/cost/liquidity/regime/structure/data/feature/dependency drift, freshness, anomalies, edge health and decay hypotheses, alerts, handoffs, quarantine, containment, recovery, authority, audit, tests, traceability and future command-interface/readiness handoffs.

## 5. Non-Goals

No code, runtime, dashboard, alert engine, database, API, schema, scheduler, CI, statistical algorithm, universal threshold, optimizer, retuner, strategy, signal, broker/exchange connection, paper/live trading, deployment or kill-switch implementation is created. No existing claim is declared healthy, decayed, revalidated, approved or deployable.

## 6. Governing Monitoring Principles

1. No signal without provenance; no alert without evidence.
2. Observation is not diagnosis, validation, decision, risk action or execution.
3. A single good or bad period proves neither health nor death.
4. Baselines, thresholds, windows, metrics and classifications are versioned; none changes silently.
5. Sample size, repeated looks, uncertainty and competing causes remain visible.
6. Negative and contradictory monitoring evidence is preserved.
7. Monitoring may request and escalate; it cannot retune, optimize, revalidate, reapprove, reactivate or allocate capital.
8. Every material event is attributable, scoped, challengeable and reconstructable.
9. Missing identity, authority, provenance, compatibility or audit fails closed.
10. `EXE-01` remains `PLANNED_CLOSED`.

## 7. Terminology and Separation Law

| Term | Meaning | Never implies |
|---|---|---|
| Observation | Attributable measured fact | Alert or cause |
| Anomaly | Deviation requiring interpretation | Edge decay |
| Drift | Evidence of distribution/condition change | Strategy failure |
| Alert | Routed evidence requiring a response | Decision or authority |
| Edge health | Scoped monitoring assessment | Capital eligibility |
| Edge-decay hypothesis | Falsifiable explanation of sustained deterioration | Proven death |
| Revalidation trigger | Request to reassess prior validation | Revalidation PASS |
| Containment | Risk-reducing restriction | KILL or later RELEASE |

`OBSERVATION ≠ ALERT ≠ DIAGNOSIS ≠ EDGE_DECAY_CLAIM ≠ REVALIDATION ≠ RETUNING ≠ DECISION ≠ RISK_ACTION ≠ EXECUTION`.

## 8. Monitoring Object Model

Nineteen canonical documentary objects are used: Monitoring Specification, Monitoring Baseline, Monitoring Observation, Monitoring Window, Monitoring Metric, Monitoring Event, Anomaly Record, Drift Record, Edge Health Record, Edge Decay Hypothesis, Alert Record, Escalation Record, Revalidation Trigger Record, Risk Notification, Decision Notification, Monitoring Evidence Package, Monitoring Disposition, Recovery Record and Monitoring Audit Record. Each inherits Sprint 3 identity/content/status/authority/custody/provenance separation and Sprint 4 orthogonal axes. An alert remains an artifact, not a decision.

## 9. Monitoring Pipeline Stages

| Stage | Purpose / required output | Fail-closed route |
|---|---|---|
| MP-00 | Eligibility intake; exact governed claim | HOLD if no eligible source |
| MP-01 | Validation baseline intake | RETURN incompatible package |
| MP-02 | Monitoring Specification | BLOCK incomplete scope/owner |
| MP-03 | Baseline registration/version freeze | QUARANTINE mutable baseline |
| MP-04 | Observation intake with identity/time | QUARANTINE unknown input |
| MP-05 | Observation integrity check | HOLD corrupt/duplicate conflict |
| MP-06 | Data quality/temporal check | DAT review; no interpretation |
| MP-07 | Window construction | BLOCK undeclared window |
| MP-08 | Metric evaluation | BLOCK mismatched metric version |
| MP-09 | Baseline comparison | Preserve uncertainty |
| MP-10 | Statistical/distribution drift | Record repeated-look context |
| MP-11 | Performance drift | No causal conclusion |
| MP-12 | Risk drift | Notify RSK; no limit change |
| MP-13 | Cost/slippage drift | Separate gross/net evidence |
| MP-14 | Liquidity drift | Record source/availability |
| MP-15 | Regime drift | Versioned temporal classifier |
| MP-16 | Market-structure drift | Route domain investigation |
| MP-17 | Data/feature drift | DAT review; preserve lineage |
| MP-18 | Dependency/model drift | Impact assessment |
| MP-19 | Validation freshness | Current/aging/stale routing |
| MP-20 | Anomaly consolidation | Retain distinct evidence |
| MP-21 | Edge-health assessment | Scoped disposition only |
| MP-22 | Edge-decay hypothesis formation | Research question, not verdict |
| MP-23 | Contradiction review | HOLD if material unresolved |
| MP-24 | Alert classification | Evidence-backed severity |
| MP-25 | Escalation routing | Competent destination only |
| MP-26 | Revalidation-trigger assessment | Request only |
| MP-27 | Risk/Decision handoff | No authority transfer |
| MP-28 | Containment/quarantine | Preserve last valid state |
| MP-29 | Recovery/re-entry review | Re-pass affected gates |
| MP-30 | Evidence consolidation | Frozen package |
| MP-31 | Audit/archive/reproduction | Reconstruct full chain |

Stages are independently gated. Completion of one does not authorize the next.

## 10. Monitoring Eligibility

Intake identifies hypothesis, experiment, validation ID/version/disposition, exact validated scope, dataset/configuration lineage, expected behavior, weaknesses, assumptions, regimes, costs, risk observations, limitations, freshness conditions, revalidation triggers and monitoring duties. Missing scientific scope is not inferred. `FAILED_VALIDATION`, incompatible, invalidated or quarantined inputs cannot become normal monitoring baselines.

## 11. Monitoring Specification

The versioned specification identifies monitored claim, validated scope, baseline, metrics, windows, data sources, time semantics, uncertainty model, threshold classes, persistence rules, multiplicity treatment, owners, reviewers, escalation routes, permitted responses, prohibited actions, freshness, reproduction and audit. It is frozen before consequential observation.

## 12. Monitoring Baseline

A baseline records ID/version, source validation ID/version, scope, expected metric/distribution/regime/cost/liquidity/risk behavior, uncertainty, failure regions, weaknesses, provenance, creation authority and effective period. Expected behavior is conditional on its tested boundary, never a promise of future profit.

## 13. Baseline and Threshold Change Governance

Material change is not ordinary monitoring. It requires reason, evidence, impact analysis, authority, new version, lineage and audit. Prior baselines and alerts remain addressable. Backdating or changing a baseline/threshold/window after adverse observation to remove an alert is prohibited. A changed scientific expectation may require new experiment and validation.

## 14. Monitoring Windows

SHORT, MEDIUM, LONG, ROLLING, EXPANDING, REGIME_CONDITIONAL and EVENT_CONDITIONAL are conceptual classes, not fixed durations. Selection considers sample size, frequency, regime duration, edge horizon, autocorrelation, seasonality and validation assumptions. Overlapping windows are correlated evidence and do not manufacture independent confirmations.

## 15. Monitoring Metrics

Every metric has stable ID/version, definition, unit, source, transformation, scope, expected behavior, uncertainty, cadence, window eligibility, alert relevance, owner and limitations. Metric replacement requires versioning and impact review. A composite score cannot average away provenance, quarantine, hard risk breach or authority failure.

## 16. Observation Integrity

Each observation records stable identity, source/venue/instrument, event/source/availability/record time, dataset/raw lineage, collection actor/module, quality/temporal disposition, revisions and fingerprint reference. Duplicate or conflicting observations remain linked. Future information, partial bars, unknown revision state and time ambiguity block consequential interpretation.

## 17. Performance Monitoring

Relevant measures may include return and risk-adjusted behavior, expectancy, payoff distribution, win/loss behavior, drawdown/recovery, frequency, exposure, turnover, tails, streaks and asymmetry. Results retain count, effective sample, window, regime and cost context. No universal target is selected here.

## 18. Edge Health Model

| Disposition | Meaning | Permitted consequence |
|---|---|---|
| NORMAL | Evidence remains compatible within declared uncertainty/scope | Continue observation |
| WATCH | Early or ambiguous deviation | Heighten observation/review |
| DEGRADED | Material deterioration or uncertainty | Restrict/request investigation |
| CRITICAL | Serious evidence or breached hard condition | Escalate/contain by authority |
| REVALIDATION_REQUIRED | Prior scientific basis must be reassessed | Request WF-04 |
| QUARANTINED | Integrity/authority uncertainty blocks interpretation | Inspect/remediate |
| HALTED | Governed containment is active | No consequential progression |

MEDS `HEALTHY/WEAKENING/BROKEN/INCONCLUSIVE/SUSPENDED` terms crosswalk respectively to scoped NORMAL, WATCH/DEGRADED, CRITICAL plus validation/decision review, UNCERTAIN handling within WATCH/QUARANTINE, and HALTED. No crosswalk creates an automatic lifecycle change.

## 19. Edge Decay Definition and Evidence Dimensions

Edge decay is sustained, evidence-supported deterioration between a validated hypothesis and observed behavior beyond reasonable variability inside its scope. Evidence remains separate across PERFORMANCE, STATISTICAL, TEMPORAL, REGIME, COST, LIQUIDITY, DATA, DEPENDENCY, STRUCTURAL and REPRODUCIBILITY dimensions. Multiple dimensions are required where scientifically relevant; a hard integrity/risk blocker cannot be diluted by favorable dimensions.

## 20. Edge Decay Hypothesis

This first-class artifact records monitored claim, deviation, baseline/window, affected metrics, possible causes, support and contradiction, regime/data/cost/sample context, uncertainty, severity, proposed discriminating investigation, revalidation relevance and provenance. It is falsifiable and starts research/revalidation; it does not amend the original hypothesis or prove death.

## 21. Performance and Distribution Drift

Plan comparisons of mean, variance, drawdown, hit rate, payoff ratio, expectancy, tails, frequency, exposure and turnover, plus returns, holding periods, excursions, volatility, spread, slippage, volume, liquidity, signal/regime frequency. Future methods may include distances, rank tests, change points, sequential evidence and bootstrap comparisons. Method/version/assumptions are attributable; formulas and thresholds are deferred.

## 22. Regime Drift

Monitor trend persistence, volatility, mean reversion, breakout behavior, liquidity, correlation, participation, session structure and transition frequency against versioned non-leaking regime definitions. Scope mismatch, classifier drift and actual mechanism decay are distinct explanations.

## 23. Market Structure Drift

Observe exchange rules, tick/contract/funding/market-hours changes, liquidity fragmentation, venue dominance, spread/volatility structure, participant behavior and relevant regulation. Structural evidence routes research, data, risk and validation review; it is not automatically strategy failure.

## 24. Cost, Slippage and Liquidity Drift

Observe commission, spread, slippage, funding, borrow, latency/impact proxies, volume, depth where available, turnover, gaps, tradeability and execution dispersion. Gross edge and net edge remain separate. Cost deterioration can make a claim economically unusable without scientifically disproving its gross mechanism; DEC/RSK govern consequences.

## 25. Data, Feature, Dependency and Model Drift

Data drift covers provider/schema/timestamp/missingness/revisions/venue/symbol/bar/normalization/transformation changes. Feature drift covers distributions, missingness, range, dependency, availability timing and version. Dependency drift covers data, model, feature, regime/cost model, implementation, venue, instrument, timeframe and references. Data drift, concept drift, model drift, performance drift and edge decay remain distinct. Material change can request revalidation; monitoring cannot mutate the dependency.

## 26. Validation Freshness

Freshness uses the Sprint 3 evidence axis and Sprint 9 validation disposition, not the artifact lifecycle field. Crosswalk: `CURRENT` means usable within scope; `AGING` means review is due but no silent invalidation; `STALE` blocks new consequential reliance; `REVALIDATION_REQUIRED` requests a new validation identity; `INVALIDATED` means the basis is unusable while history remains. Triggers include elapsed policy interval, volume of new data, regime/structure/cost/data/implementation changes, anomalies, contradictions and edge health. No universal expiry is set.

## 27. Revalidation Triggers

Sustained degradation, abnormal drawdown/tail evidence, structural/regime/cost/data/dependency/implementation change, validation expiry, contamination, contradiction, negative-control defect, upstream invalidation or market-structure change may create a Revalidation Trigger Record. The record identifies evidence, scope, urgency and authority. It requests `WF-04`; it cannot assert PASS.

## 28. Alert Taxonomy and Evidence

| Severity | Meaning | Required action boundary |
|---|---|---|
| INFO | Attributable informational evidence | Record/observe |
| WATCH | Potential deviation | Review/continue observation |
| WARNING | Material evidence | Investigation and owned response |
| CRITICAL | Serious integrity/risk/scientific evidence | Immediate governance/risk escalation |
| HALT | Governed fail-safe condition or containment request | A9 path; not permanent KILL |

Every alert records ID, specification, observation, baseline, metric/window, deviation/evidence/uncertainty, severity/scope/time, actor/module, provenance, routing, review and status/expiry. Alert prose without referenced evidence is inadmissible.

## 29. Alert Deduplication and Fatigue

Duplicates share identity/root-cause lineage and must not create repeated institutional effects. Correlated symptoms may be grouped, while distinct scientific evidence remains visible. Aggregation, acknowledgement, persistence, escalation windows and stale-alert closure are versioned policies. Noise reduction cannot suppress a critical fact, adverse period or dissent.

## 30. Repeated Testing, Change Points and Multiplicity

Repeated looks, overlapping windows, many metrics and sequential rules increase false alarms. Monitoring records look count, metric/window families, dependencies and stopping/escalation logic. Future change-point, Bayesian, sequential and rolling methods require governed specifications and oracles. A single algorithm cannot declare edge death.

## 31. False Positives and False Negatives

False-positive defenses include persistence, sample/regime context, multiple evidence dimensions, contradiction review and revalidation. False-negative defenses include distribution/tail/cost/dependency monitoring, long/short comparison and adversarial tests. Favorable performance cannot suppress a hard integrity signal; adverse performance cannot alone prove mechanism failure.

## 32. Competing-Cause Analysis

Every material decay assessment considers STRATEGY_FAILURE, MARKET_REGIME_CHANGE, MARKET_STRUCTURE_CHANGE, COST_CHANGE, DATA_ISSUE, IMPLEMENTATION_ISSUE, LIQUIDITY_CHANGE, SAMPLE_VARIANCE and UNKNOWN. Evidence may support several. Monitoring states causal confidence and discriminating tests rather than forcing one story.

## 33. Contradiction Management

`DETECTED → REGISTERED → SCOPE/MATERIALITY REVIEW → HOLD / BOUNDED_CONTINUE / QUARANTINE / ESCALATE → RESPONSE`. Short-window deterioration and intact long-window evidence coexist. Only competent scientific/risk/governance authority classifies impact; AUD-02 custody and MON storage do not.

## 34. Champion / Challenger Governance

Monitoring may identify champion degradation, a challenger research opportunity or need for a new experiment. Challenger outperformance cannot replace a champion. Replacement requires new question/specification/data lock/full experiment history/independent validation/decision/risk/portfolio and future separately authorized execution.

## 35. Controlled Research Loop and Retuning Boundary

Permitted loop: `MONITORING EVIDENCE → EDGE DECAY HYPOTHESIS → RESEARCH QUESTION → NEW HYPOTHESIS → EXPERIMENT → VALIDATION → DECISION`.

Prohibited loop: `MONITORING → RETUNE → DEPLOY`. Monitoring cannot change indicators, thresholds, stops, targets, risk, sizing, features, strategy parameters, search budgets, configuration/dataset locks, promote challengers, optimize or retrain. Any material change is a new governed scientific object.

## 36. Monitoring Failure Modes

| Failure class | Default containment |
|---|---|
| Missing/stale baseline; wrong validation/scope | RETURN/HOLD |
| Broken dataset lineage, timestamps, corrupt/missing observation | QUARANTINE; DAT review |
| Metric/window/regime/cost mismatch | BLOCK interpretation; review |
| Threshold/baseline drift or alert suppression | GOVERNANCE HOLD; audit |
| Alert flood/duplicate/replay | Deduplicate without deleting evidence |
| Repeated-testing bias, insufficient sample | WATCH/INCONCLUSIVE |
| False positive/negative concern | Challenge/revalidation |
| Data/dependency/implementation drift | Impact review/HOLD |
| Missing provenance/authority/audit | QUARANTINE/BLOCK |
| Unauthorized retuning/reactivation | REJECT, HALT/escalate, audit |

## 37. Monitoring Quarantine

Unknown/corrupt baseline, broken lineage, invalid metric, incompatible validation, timestamp ambiguity, material data defect, authority ambiguity or implementation inconsistency enters quarantine. Last valid state/history is preserved; consequential interpretation and promotion stop. Release requires resolved cause, new evidence/version as needed, competent independent review, explicit authority and audit. Retry cannot broaden authority.

## 38. Containment and S5-OQ-03 Resolution

`S5-OQ-03` is governed at planning level: a future autonomous system may apply only a pre-authorized, narrowly scoped, reversible, risk-reducing A9 fail-safe containment when an exact object, condition class, authority source, maximum scope, expiry, human notification/escalation and immutable audit are defined in advance. Ambiguity, missing telemetry or conflicting instructions defaults to the safer HOLD/HALT within that grant. It may not KILL institutionally, liquidate, retune, reactivate, widen scope or create authority. Exact numeric triggers and confirmation windows remain deferred and fail closed.

## 39. HOLD / SUSPEND / HALT / KILL / RELEASE / REACTIVATE

| Term | Meaning | Authority boundary |
|---|---|---|
| HOLD | Stops consequential progression | Competent reviewer; explicit release |
| SUSPEND | Removes an eligibility/authority temporarily | A9/human review by scope |
| HALT | Immediate bounded risk-reducing stop | Preauthorized A9 or human authority |
| KILL | Terminates relevant capital-affecting authority | Non-delegable A10 human path |
| RELEASE | Ends containment, not necessarily active status | Independent competent authority |
| REACTIVATE | New governed active eligibility | New evidence, validation/risk/decision gates |

Halter is not automatically releaser; killer is not automatically reactivator. KILL preserves cause, evidence, affected scope, authority, time and history.

## 40. Recovery

`CAUSE IDENTIFIED → CORRECTIVE ACTION → NEW EVIDENCE/VERSION → INTEGRITY RECHECK → REVALIDATION WHERE REQUIRED → RISK REVIEW → AUTHORIZED RELEASE OR CONTINUED HOLD`. Every failed gate is re-passed. Historical alerts, failures and baselines remain immutable.

## 41. Monitoring Authority Model

Monitoring normally uses A0 Observe, A1 Produce, A2 Request, A3 Challenge and A5 Recommend. A4 review is assigned independently where governed. MON receives no implicit A6 Validate, A7 consequential authorize, A8 approve/reject, A10 kill or A11 execution. A9 exists only under the narrow preauthorization in section 38. Severity, consensus, tool access and system capability never expand authority.

## 42. Human / Agent Responsibilities

| Actor | Permitted contribution | Required separation / accountable human |
|---|---|---|
| MON modules / future Monitoring Agent | Observe, produce evidence, request/challenge/escalate | No validate/retune/reactivate; Monitoring Owner |
| Validation Agent / H-06 | Consume trigger, independently revalidate | Cannot inherit MON conclusion |
| Risk Governance Agent / H-04 | Analyze/recommend risk, request containment | Human Risk Authority accepts material risk |
| Executive Decision Agent / H-03 | Synthesize options/recommend; governed DEC action | Agent name is not human authority |
| Experiment Orchestrator | Route new research/revalidation work | No monitoring/validation authority |
| Market Research Agent | Investigate regime/structure explanations | No lifecycle decision |
| Knowledge Curator / Research Librarian | Curate/retrieve governed history | Repetition is not evidence |
| QA Agent / H-10 | Challenge conformance and auditability | Cannot validate edge or authorize |
| CEO Agent / H-01 | Decision support; only explicit reserved authority | No undocumented override |
| H-09 Emergency Authority | A9/A10 within explicit scope | Independent release/review required |

## 43. Module Responsibility Map

Forty-one relevant Sprint 2 modules are mapped.

| Modules | Monitoring responsibility | Explicit prohibition |
|---|---|---|
| MON-01 | System/data/governance health, observation integrity | No repair/authority |
| MON-02 | Claim/evidence/regime/edge health and decay evidence | No revalidation/retune |
| MON-03 | Alert identity, deduplication and routing | Alert is not action |
| VAL-01..07 | Intake and perform independent revalidation/parity when routed | No MON self-validation |
| RSK-01..02 | Risk assessment, A9/A10 routes and release evidence | Analysis ≠ own exception/release |
| DEC-01..02 | Decision evidence intake and competent decision | Cannot rewrite monitoring evidence |
| DAT-01..05 | Source/raw/QC/build/lock lineage for observations | No uncontrolled monitoring data universe |
| EXP-01..06 | New experiment/spec/locks/runs/history/packages | MON cannot alter experiment objects |
| RES-01..03 | New question/hypothesis/evidence/challenge | Decay hypothesis ≠ approval |
| KNW-01..03 | Preserve curated knowledge, provenance/failure learning | Output ≠ institutional truth |
| ORC-01..03 | Route, sequence, dependency/recovery coordination | No classification/authorization |
| AUD-01..03 | Register/custody/reconstruct artifact/evidence/state | Storage/recording ≠ authority |
| GOV-01..02 | Resolve policy, exceptions and escalation authority | No evidence invention |
| IAM-01..02 | Resolve actor, authority and delegation | Identity/access ≠ authority |

## 44. MON-01 / MON-02 / MON-03 Boundary

MON-01 observes system, source, temporal, lineage and governance health; MON-02 evaluates scoped strategy/evidence/regime/edge health and drafts decay hypotheses; MON-03 packages/routs alerts and escalations. MON-01 findings constrain MON-02 interpretation; MON-02 cannot authorize state change; MON-03 cannot convert routing into action. Cross-module evidence uses exact versions.

## 45. Orchestration Boundary

ORC may schedule, route, request analysis, check prerequisites, coordinate handoffs and record workflow progression. It may not declare decay, validate, retune, approve, release/reactivate, waive a missing baseline, create authority or execute. Task completion is not monitoring disposition.

## 46. Audit Boundary

AUD registers, preserves, links and reconstructs evidence, alerts, authority and transitions. It cannot classify science because stored, approve because complete, release, create authority or execute. Audit gaps block consequential reliance; later ledger writes cannot retroactively create prior authority.

## 47. Data / Experiment / Validation Integration

Monitoring uses Sprint 7 source/venue/instrument/time/availability/version/revision/quality/lineage rules and cannot create parallel data. It may create requests but cannot mutate Sprint 8 specifications, locks, budgets or trial history. It consumes Sprint 9 identity/disposition/scope/robustness/weakness/freshness and cannot expand them.

## 48. Risk, Decision, Validation, Research and Knowledge Handoffs

Risk handoff carries drawdown/tail/liquidity/cost/volatility/concentration/correlation/structure evidence; RSK sets no consequence merely because MON sent it. Decision handoff carries claim, baseline, deviation, health, uncertainty, contradictions, freshness, revalidation/risk status and provenance. Validation handoff is a revalidation request, never PASS. Research handoff creates a new question/hypothesis. Knowledge admission requires curation and preserves negative lessons.

## 49. Monitoring Evidence Package

The package includes ID/version, specification, frozen baseline, validation lineage, observation IDs, windows/metrics, performance/statistical/regime/structure/cost/liquidity/data/feature/dependency evidence, health, decay hypotheses, anomalies/alerts, contradictions/uncertainty, freshness and triggers, risk/decision/research handoffs, containment/recovery events, actors/authority and audit. Source artifacts are referenced, not rewritten.

## 50. Edge Decay Report

The report identifies claim/baseline/period, expected and observed behavior, affected dimensions, statistical/sample/regime/structure/cost/liquidity/data context, competing explanations, supporting and contradicting evidence, confidence limits, severity, freshness, revalidation recommendation, risk/decision relevance, scope, provenance, authority and audit. It is neither a signal nor a parameter instruction.

## 51. Opportunity Map and Research Ledger Integration

Monitoring may label evidence for stable, weakening, uncertain, unsuitable-market or challenger-research opportunities. This prioritizes research only and allocates no capital. Ledger lineage preserves observations, hypotheses, alerts, investigations, requests, experiments, validations and decisions; recovery never rewrites decay history.

## 52. Edge Decay Knowledge and Retention

Preserve what stopped working, when, markets/regimes/costs/structure, antecedent warnings, contradictions, failed responses and recovery outcome. Curator authority governs publication. Raw observations, superseded baselines, alerts, quarantines, false alarms, invalidations and reports remain retained per governed class; unresolved legal durations are open, with no silent deletion.

## 53. Monitoring Freshness

Observations, alerts, health records, decay hypotheses and handoffs each declare observation/effective/record time, freshness policy/version and supersession status. Stale evidence remains historical but cannot masquerade as current or support new consequential action without review.

## 54. Escalation Matrix

| Severity / evidence / persistence / C | Review / destination | Permitted action | Prohibited action |
|---|---|---|---|
| INFO; weak/transient; C0–1 | MON/Data/Research | Record, observe | Promote/change |
| WATCH; ambiguous/repeated; C1–2 | MON + challenger | Increase evidence/review | Diagnose/retune |
| WARNING; material/persistent; C2–3 | VAL/RSK/Research/Data as cause indicates | Request revalidation/HOLD | Self-validate |
| CRITICAL; strong or hard conflict; C3–4 | H-04/H-06/H-03/H-09/GOV/AUD | Contain/escalate within authority | Release/execute |
| HALT condition; immediate safety; C4 | H-09/H-04/H-01 | Narrow A9 fail-safe/human halt | Automatic KILL/reactivation |

Destination receives a request and evidence, never sender authority.

## 55. Criticality and Independence

C0 attribution; C1 challenge availability; C2 scientific provenance/review; C3 independent review, named accountable authority, reproducibility and audit; C4 strongest human/emergency governance and fail-closed containment. Monitor, baseline author, strategy author, experiment producer, validator, risk assessor and decision maker relationships are disclosed. Shared model/context/data lineage can break independence; agent renaming cannot restore it.

## 56. Human Override and Multi-Agent Consensus

Override records authority, rationale, evidence, contradictions, scope, duration/review and downstream impact. It cannot erase evidence, waive Constitution, provenance, audit, identity, execution closure or fabricate validation. Any number of agents may improve challenge coverage but cannot create A6/A8/A10/A11 or human accountability.

## 57. Prohibited Monitoring Chains

| Prohibited chain | Required response |
|---|---|
| ALERT → RETUNE / OPTIMIZE / REACTIVATE / CAPITAL_INCREASE | BLOCK, record authority violation |
| EDGE_HEALTHY → EXECUTE | BLOCK at AX-10/EXE-01 |
| EDGE_DEGRADED → PARAMETER_CHANGE | Route new research |
| EDGE_DECAY → STRATEGY_REPLACEMENT | Experiment/validation/decision required |
| CHALLENGER_OUTPERFORMS → REPLACE_CHAMPION | BLOCK self-promotion |
| MONITORING_CONSENSUS → APPROVAL | Treat as evidence only |
| ALERT → VALIDATION_PASS / EXECUTION_AUTHORITY | BLOCK and audit |
| HALT → AUTOMATIC_RELEASE | Independent release required |
| KILL → AUTOMATIC_REACTIVATION | New gates and authority required |
| ORC_EVENT / AUD_RECORD → AUTHORIZATION | BLOCK |
| HUMAN_COMMAND → CONSTITUTIONAL_BYPASS | REJECT/escalate |

## 58. Concurrency, Idempotency and Replay

Baseline change vs observation, staleness vs monitoring, revalidation vs open alert, invalidation vs health assessment, HALT vs new evidence, release vs critical alert and contradictory agents route to one conflict record. Restrictive valid state dominates pending review. Same observation/specification/baseline/request has one institutional effect; changed versions create new identities. Replay preserves prior disposition and cannot overwrite newer evidence or reuse expired authority.

## 59. Test Architecture Integration

Thirty Sprint 6 families are inherited: T02, T03, T04, T05, T06, T07, T08, T09, T10, T11, T12, T13, T14, T15, T16, T17, T18, T19, T21, T22, T23, T24, T25, T27, T28, T29, T30, T32, T34, T35, T36, T37 and T38. (Thirty-three IDs are listed because boundary, version and end-to-end families are independently mandatory; PR reporting uses **33 test-family obligations**.) They cover baseline/lineage/observation/metric/window/drift/health/hypothesis/alert/deduplication/suppression/multiplicity/false outcomes/triggers/unauthorized retuning/reactivation/handoffs/quarantine/emergency/replay/concurrency/audit/isolation.

## 60. Monitoring Test Matrix

| Requirement | Failure | Positive / negative / adversarial test | Evidence / authority / C | Fail-closed response / future obligation |
|---|---|---|---|---|
| Eligibility/baseline | Missing/wrong/stale validation | Exact intake; swap ID/change baseline after loss | Package/version log; A4; C3 | HOLD; implement exact resolver |
| Observation/time | Corrupt/future/duplicate data | Clean lineage; future-data/deletion attack | Observation/TIR; DAT/MON; C2–3 | QUARANTINE |
| Metrics/windows | Drifted definition/cherry-picked window | Frozen specs; favorable-only attack | Metric/window record; A4; C2 | BLOCK/review |
| Drift/health | Single-period overclaim/missed decay | Multi-dimensional evidence; lucky/bad-period cases | Drift/health evidence; MON A1/A5; C3 | WATCH/revalidate |
| Alerts | Unsupported/suppressed/flooded | Valid route; hide/replay/flood attack | Alert/acknowledgement; A2; C3 | Escalate/quarantine router |
| Freshness/revalidation | Stale shown current/auto-PASS | Valid trigger; bypass validation attack | Trigger/freshness; H-06; C3 | HOLD/WF-04 |
| Retuning/reactivation | MON changes candidate/releases itself | Request-only; parameter/release attacks | Authority/audit; H-04/09; C4 | BLOCK/HALT/escalate |
| Handoffs | Sender authority transferred | Complete package; fake-authority attack | Handoff record; destination authority; C3–4 | RETURN/HOLD |
| Emergency | HALT/KILL/release conflated | Narrow fail-safe; auto-kill/release attack | Incident/authority; H-09; C4 | Contain, human review |
| Audit/execution | Missing chain/order attempt | Reconstruct; alert→order attack | AUD evidence; H-10; C4 | FAIL/BLOCK |

## 61. Adversarial Monitoring Obligations

Future tests hide adverse observations, delete losses, rebase after loss, alter thresholds, cherry-pick windows, suppress/flood alerts, spoof regimes/authority, present stale validation, corrupt costs/slippage, use future data, retune after alert, auto-reactivate, treat consensus as decision, ignore multiplicity, replace sources without lineage and change implementation without revalidation. Each must fail closed with preserved evidence.

## 62. Execution Isolation

No monitoring object, state, alert, disposition or human interface creates ORDER, TRADE, POSITION, CAPITAL_ALLOCATION, BROKER_COMMAND, EXCHANGE_COMMAND or WEBHOOK_EXECUTION. All paths `MON/ALERT/HEALTH/HALT → A11/EXE-01` block and audit. `EXE-01` remains `PLANNED_CLOSED`.

## 63. Traceability Matrix

| Constitutional requirement | Monitoring requirement/module | Baseline/object/evidence | Alert/disposition/authority | Test / failure / handoff |
|---|---|---|---|---|
| Monitoring≠authority | MON-01..03 boundaries | Specification/Observation | A0–A5 only | T08/27; BLOCK; RSK/VAL/DEC |
| Exact evidence/provenance | Sprint 3/7; AUD/DAT | Baseline + lineage/package | Scoped alert | T04/05/15/16/36; quarantine |
| Independent validation | Sprint 9; VAL | Trigger + full package | REVALIDATION_REQUIRED; H-06 | T11/12/20; HOLD; WF-04 |
| No silent mutation | Sprint 3/4; AUD | Frozen baseline/threshold | New version only | T04/19/36; reject amendment |
| Preserve contradictions | Sprint 3; MON-02 | Drift/decay records | WATCH/HOLD | T05/22; review |
| Emergency separation | Sprint 4/5; RSK/HUM | Incident evidence | A9≠A10≠release | T09/29/30; halt/escalate |
| Reproducibility/audit | Charter; AUD-03 | Exact observation chain | Attributable disposition | T17/25/38; FAIL |
| Execution isolation | Charter; EXE-01 | No execution artifact | No A11 | T37/38; BLOCK |

## 64. Planning ADRs

| ADR | Decision | Rejected alternative / consequence | Constitutional basis |
|---|---|---|---|
| S10-ADR-01 | Monitoring observes; never authorizes | Alert-as-action; route only | MEDS/Sprint 2 |
| S10-ADR-02 | Baselines frozen/versioned | Adaptive silent baseline; history preserved | ART/EES |
| S10-ADR-03 | Threshold changes are governed versions | Move-after-loss; impact review | MEDS |
| S10-ADR-04 | Multiple scoped windows coexist | Universal window; dependencies disclosed | Scientific OS |
| S10-ADR-05 | Edge health is orthogonal evidence state | Lifecycle overload; explicit crosswalk | Sprint 4 |
| S10-ADR-06 | Decay is a falsifiable hypothesis | One-loss death verdict; research route | Research OS |
| S10-ADR-07 | Performance drift retains sample context | Headline metric; uncertainty visible | VEP |
| S10-ADR-08 | Distribution drift has versioned methods | Magic score; component evidence | Sprint 6 |
| S10-ADR-09 | Regime classifier is versioned/non-leaking | Post-hoc regime; temporal integrity | Sprint 7/9 |
| S10-ADR-10 | Structure drift is competing cause | Blame strategy; domain review | MEDS |
| S10-ADR-11 | Cost drift separates gross/net edge | Aggregate return only; economic scope | RRP |
| S10-ADR-12 | Liquidity is multidimensional | Volume-only proxy; limitations | MEDS |
| S10-ADR-13 | Data drift precedes causal performance claim | Corrupt-data decay; quarantine | DQS/Sprint 7 |
| S10-ADR-14 | Feature drift ≠ edge decay | Status collapse; investigate lineage | Feature Standard |
| S10-ADR-15 | Dependency change routes impact review | Silent reuse; revalidate when material | Sprint 4 |
| S10-ADR-16 | Freshness is class/scope-dependent | Universal expiry; fail closed when unknown | Sprint 3/9 |
| S10-ADR-17 | Trigger requests revalidation only | Automatic validation; H-06 retained | Sprint 9 |
| S10-ADR-18 | INFO/WATCH/WARNING/CRITICAL/HALT taxonomy | Hidden severities; explicit routing | Charter/MEDS |
| S10-ADR-19 | Alert requires referenced evidence | Text-only alarm; inadmissible | Sprint 3 |
| S10-ADR-20 | Deduplication preserves distinct evidence | Blanket suppression; lineage grouping | Audit law |
| S10-ADR-21 | Repeated looks require multiplicity context | Independent-window fiction; humility | Sprint 9 |
| S10-ADR-22 | False positives and negatives both governed | One-sided tuning; multi-evidence challenge | Scientific OS |
| S10-ADR-23 | Champion/challenger cannot auto-replace | Performance promotion; full pipeline | Sprint 8 |
| S10-ADR-24 | Retuning always creates new scientific object | Online silent mutation; research loop | MEDS/WOE |
| S10-ADR-25 | Monitoring cannot reactivate | Self-release; independent authority | EDRP/Sprint 5 |
| S10-ADR-26 | Automated fail-safe is narrow A9 containment | Automated institutional KILL; human A10 | S5-OQ-03/RRP |
| S10-ADR-27 | HALT/KILL/release/reactivation are distinct | Emergency status collapse; separate gates | Sprint 4/5 |
| S10-ADR-28 | Override never deletes evidence | Owner-said-so; audit/constraints | Decision OS |
| S10-ADR-29 | Agent consensus adds no authority | Vote-created approval; evidence only | Sprint 5 |
| S10-ADR-30 | EXE-01 isolation is absolute in Phase 2 | Alert-to-order; block and audit | Charter/EXE-01 |
| S10-ADR-31 | Recovery re-passes failed gates | Retry bypass; new evidence/version | Sprint 4 |
| S10-ADR-32 | Restrictive valid state wins conflicts | Optimistic race winner; safety routing | Sprint 4 |

## 65. Open Governance Questions Register

| ID | Question / source | Stage / module / artifact / workflow / test | C / severity | Status / fail-closed default | Authority | Target / path |
|---|---|---|---|---|---|---|
| S10-OQ-01 | Exact thresholds and persistence by claim/market? S9-OQ-03 | MP-08..24; MON-02; Spec; WF-09; T20/27 | C3/High | Non-blocking plan; no consequential classification without preregistered rule | H-06 + Scientific/Monitoring Governance | Future monitoring specification |
| S10-OQ-02 | Statistical drift/change-point/sequential methods and oracles? S9-OQ-03 | MP-10/20; MON-02; Drift; T18/20/22 | C3/High | Non-blocking; method claim INCONCLUSIVE | Scientific Governance | Future implementation spec |
| S10-OQ-03 | Freshness policies by validation/evidence/monitoring class? S9-OQ-02 | MP-19/26; VAL/MON; Trigger; WF-04/09; T19/27 | C2–4/High | Non-blocking; unknown material freshness = STALE/HOLD | Evidence/VAL/MON authority | Sprint 12/future specs |
| S10-OQ-04 | Exact automated fail-safe triggers/confirmation windows? S5-OQ-03 | MP-28; MON/RSK/HUM; Incident; WF-09/16; T29/30 | C4/High | Non-blocking while EXE closed; only narrow preauthorized A9 or human halt | H-04/H-09/H-01 | Future risk/monitoring spec |
| S10-OQ-05 | Named A10 KILL and independent release/reactivation authority in future operation? | MP-28/29; RSK-02/HUM-02; Kill/Release; T29/30 | C4/Critical | Non-blocking Phase 2; blocks future opening; manual fail-closed | H-01/H-04/H-09/Governance | Sprint 12 + future deployment governance |
| S10-OQ-06 | Confidence component methodology without blocker averaging? | MP-21/22; MON-02; Health/Decay; T20/22 | C3/Medium | Non-blocking; no aggregate authority use | Scientific/Decision Governance | Future monitoring spec |
| S10-OQ-07 | Alert aggregation, acknowledgement and fatigue policy? | MP-24/25; MON-03; Alert; T27/35 | C2–3/Medium | Non-blocking; preserve/reroute critical evidence | Monitoring Governance | Future interface/monitoring spec |
| S10-OQ-08 | Legal/licensing/retention durations for monitoring evidence? inherited | MP-31; AUD/DAT; Archive; T25/36 | C2–4/Medium | Non-blocking; no disposal while dependency/legal status unknown | Legal/Data/Artifact authority | Sprint 12/future retention policy |
| S10-OQ-09 | Unknown off-platform search burden effect on baseline confidence? S9-OQ-04 | MP-01/21; MON/VAL; Baseline; T05/21 | C3/High | Non-blocking; prohibit strong health/decay certainty | Research/Evidence Governance | Sprint 12 |
| S10-OQ-10 | Exact Phase 2 exit-review composition? S9-OQ-09 | Governance; GOV/AUD; readiness evidence; T38 | C4/High | Non-blocking Sprint 10; blocks Sprint 12 exit | Existing Governance Authority | Sprint 12 |

Blocking issues for Sprint 10 planning: **0**. Ten bounded questions remain explicit; affected future implementation and consequential action paths fail closed.

## 66. Sprint 11 Handoff Contract

Sprint 11 receives exact Monitoring Specification/Baseline/Observation/Event/Health/Decay/Alert/Escalation/Trigger/Evidence/Disposition identities and states; INFO/WATCH/WARNING/CRITICAL/HALT; quarantine, HOLD/SUSPEND/HALT/KILL/RELEASE/REACTIVATE distinctions; request/review/authority evidence; deduplication/replay; audit; prohibited commands; and execution isolation. Command parsing must never convert user wording, urgency, tool access or agent consensus into unscoped authority.

## 67. Sprint 12 Readiness Preparation

Sprint 12 receives the ten open questions, 33 test-family obligations, 41-module map, unresolved thresholds/methods/freshness/retention/exit composition, authority gaps for future KILL/release, fail-safe constraints, exact artifact/state/transition requirements and P0 proof that MON/ORC/AUD/HUM cannot reach A11. Monitoring implementation readiness requires governed specifications/oracles, exact owners, test evidence and no blocking ambiguity.

## 68. Definition of Done

Current main and exact Sprint 9 merge were verified. One non-executable artifact defines 19 objects, 32 stages, versioned baselines/thresholds, windows/metrics/observations, ten drift dimensions, edge health/decay, freshness/triggers, alerts/multiplicity/false outcomes, champion/challenger and no-retuning loop, failure/quarantine/containment/recovery, S5-OQ-03 boundary, emergency separation, A0–A11 responsibilities, 41 modules, integrations/handoffs, evidence/report/retention, concurrency/replay, 33 tests, traceability, 32 ADRs, ten questions and Sprint 11/12 handoffs. Constitution and Sprints 1–9 remain unchanged; no runtime/code/trading/execution exists; EXE-01 is closed.

## 69. Final Sprint Disposition

**SPRINT 10 COMPLETE WITH OPEN GOVERNANCE ITEMS**

Blocking issues: **0 for Sprint 10 planning**. Ten bounded questions remain fail-closed. After governance review and merge, the next authorized planning step is **Phase 2 — Sprint 11: Command Interface Plan**.
