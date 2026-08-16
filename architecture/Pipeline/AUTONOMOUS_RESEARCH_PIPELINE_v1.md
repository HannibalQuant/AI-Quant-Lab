# Autonomous Research Pipeline (ARP) v1.0

## Specification Control

| Field | Value |
|---|---|
| Standard ID | `AIQL-ARP` |
| Version | `1.0.0` |
| Status | Proposed for Sprint 30 review |
| Scope | Every institutional autonomous research program and strategy pipeline |
| Authority | Research OS, WOE, SLS, MACP, SMI, EES, Agent Registry, ART, EEP, VEP, RRP, EDP, DGS, and MEDS |
| Provider dependency | None |

The Autonomous Research Pipeline is the constitutional end-to-end process by which AI Quant Lab converts market observation into governed research, strategy architecture, implementation, experiments, evidence, independent review, bounded deployment, monitoring, and institutional learning.

It is not code, automation, a workflow file, optimizer, strategy, or universal agent. It coordinates specialized authorities while preserving their independence, contracts, evidence boundaries, and approval rights.

## 1. Autonomous Research Pipeline Philosophy

Autonomy means the capacity to continue governed institutional work without losing accountability, scientific discipline, or human review rights. It does not mean unconstrained action.

The pipeline transforms uncertainty through staged inquiry. Each stage has one primary purpose, explicit inputs and outputs, named ownership, completion criteria, failure criteria, and a governed handoff.

Progress is defined by evidence and satisfied gates, not activity volume, elapsed compute, or favorable results. Returns, rejection, suspension, and failure are legitimate pipeline outcomes.

## 2. Autonomous Research Pipeline Principles

The following principles are binding:

1. No Pipeline Without Identity, Owner, and Registered Scope.
2. No Market Selection Without Research Rationale.
3. No Strategy Without Hypothesis and Knowledge Context.
4. No Architecture Without Mechanism.
5. No Engineering Without Approved Architecture.
6. No Experiment Without Registered Plan.
7. No Evidence Without Frozen Package.
8. No Validation Without Complete Evidence.
9. No Risk Review Without Issued Validation.
10. No Executive Decision Without Risk Review.
11. No Deployment Without Executive Decision and DGS.
12. No Active Strategy Without MEDS Monitoring.
13. No Feedback Loop Without Learning Record.
14. No Silent Stage Skipping, Agent Substitution, Scope Expansion, or Evidence Replacement.
15. No Backtest-Only or Optimization-Only Progression.
16. Every State Must Be Auditable; Failure Is Knowledge.

## 3. Pipeline Identity Model

Every pipeline has a permanent Pipeline ID, Pipeline Record ID, and exact version. Identity binds the institutional purpose, scope, initiating authority, owner, responsible WOE workflow, target research domain, and linked Strategy IDs.

Material changes to purpose, target market domain, decision question, ownership model, or institutional output require a new Pipeline ID. Scoped amendments create new record versions and preserve lineage. Identifiers are never reused.

## 4. Pipeline Object Model

The Pipeline Record must define:

| Record group | Mandatory content |
|---|---|
| Identity | Pipeline ID, record ID, owner, initiating agent, responsible workflow |
| State | Current state, scope, target market/instrument/timeframe/regime |
| Research | Objective, question, knowledge-intake scope, hypothesis, expected mechanism |
| Strategy | Strategy ID/version, lifecycle state, architecture artifact |
| Engineering | Implementation artifact, version, deviations, and handoff status |
| Experiment | Plan, Experiment ID, execution status, and EEP reference |
| Reviews | VEP, RRP, EDP, current verdict, conditions, and limitations |
| Operations | DGS record, Monitoring record, stage, health, and authority |
| Governance | Current blockers, open questions, return/rejection stage, failure mode, learning record |
| Integrations | Source MACP and related SMI, EES, ART, WOE, and Agent records |
| History | Created At, Updated At, lineage, and immutable Audit Trail |

Every field resolves to exact versions where institutional reliance exists. Missing critical identity, owner, input, or authority blocks progression.

## 5. Pipeline Lifecycle

**Proposed → Registered → Market Discovery → Research Question Defined → Knowledge Intake → Hypothesis Formation → Strategy Architecture → Engineering Handoff → Implementation Development → Experiment Planning → Experiment Execution → Evidence Packaging → Validation Review → Risk Review → Executive Decision → Deployment Governance → Monitoring → Feedback Loop → Returned → Rejected → Suspended → Retired → Archived**

The canonical forward sequence is mandatory. Return transitions identify a precise destination and invalidate affected downstream states. Rejection and retirement preserve reconstructability. Suspension pauses authority without deleting work.

## 6. Pipeline Initiation Rules

Initiation defines purpose, scope, owner, target domain, expected institutional output, success and failure criteria, resource class, required agents, decision boundaries, dependencies, expiry, and termination conditions.

Registration verifies Agent Registry eligibility, WOE workflow identity, communication rights, memory access, evidence rights, artifact obligations, conflicts of interest, and audit readiness.

## 7. Market Discovery Stage

The Market Research Agent produces objective market observation before strategy design. The stage examines structure, regimes, trend quality, volatility, liquidity, participation, statistical behavior, cross-market relationships, uncertainty, and opportunity candidates.

Output is a registered Market Opportunity Record containing observation, scope, evidence, limitations, threats, alternative explanations, and research-worthiness. It cannot contain a tradable strategy or indicator selection.

## 8. Research Question Stage

The question must define scope, motivation, economic or behavioral rationale, expected mechanism, alternative explanations, required evidence, failure criteria, success criteria, unknowns, and intended consumer.

A question too broad to falsify, too narrow to matter, or framed around a desired answer is returned for reformulation.

## 9. Knowledge Intake Stage

The Research Librarian acquires authoritative external sources with provenance. The Knowledge Curator governs acceptance, conflicts, lineage, freshness, confidence, dependencies, and retirement under Knowledge OS.

The Knowledge Intake Record identifies prior evidence, contradictions, source quality, gaps, applicable failure knowledge, and what remains unknown. Memory or model recall cannot substitute for available authoritative knowledge.

## 10. Strategy Hypothesis Stage

The Quant Strategy Architect defines a falsifiable claim linking observed market behavior to an expected persistent mechanism under declared conditions.

The record includes observation, behavior, mechanism, target regimes, expected persistence, null and alternatives, assumptions, invalidation, failure modes, required information, validation method, and pre-test confidence. Indicators cannot serve as the hypothesis.

## 11. Strategy Architecture Stage

Architecture converts the approved hypothesis into modular regime, information, entry, confirmation, exit, stop, sizing, risk, trade-management, validation, and monitoring requirements.

It defines measurement rationale, redundancy, module contribution, interfaces, failure propagation, alternatives, open questions, and experiment proposals. Approval freezes scientific intent for Engineering.

## 12. Engineering Handoff Stage

The handoff cites exact architecture and strategy versions, required behavior, timing, assumptions, data, execution semantics, tests, reproducibility, parity, prohibited interpretations, and acceptance criteria.

Engineering may return ambiguity but cannot invent strategy logic. Every interpretation and deviation remains visible.

## 13. Experiment Planning Stage

Before results are known, the Experiment Orchestrator registers plan identity, purpose, hypotheses, variables, controls, baselines, datasets, partitions, metrics, costs, execution assumptions, statistical methods, robustness, negative controls, stopping, replication, and acceptance criteria.

The plan identifies confirmatory versus exploratory work and prevents post-result criteria from masquerading as preregistration.

## 14. Experiment Execution Stage

Execution uses exact registered plan, strategy, implementation, data, configuration, and environment versions. All runs, failures, exclusions, seeds, controls, deviations, interruptions, and outputs are retained or explicitly accounted for.

The Experiment Orchestrator coordinates execution but cannot change scientific intent, select favorable evidence, or validate its own results.

## 15. Evidence Packaging Stage

Every completed experiment produces a frozen EEP before Validation. Packaging preserves purpose, versions, data coverage, configuration, costs, execution, main results, robustness, negative controls, adversarial tests, failures, deviations, contradictions, limitations, reproducibility, and custody.

Incomplete, mutable, inconsistent, or selectively reported packages are returned.

## 16. Validation Stage

The independent Validation Agent reviews only frozen EEP evidence and issues a VEP. It assesses admissibility, reproducibility, robustness, bias, leakage, overfitting, parameter stability, controls, contradictions, limitations, practical significance, and statistical reliability.

Authorized outcomes are approval, limited approval, more evidence, or rejection. Validation cannot accept risk or authorize deployment.

## 17. Risk Review Stage

Risk Governance consumes an issued VEP within its exact scope and produces an RRP covering market, regime, execution, liquidity, model, data, assumption, drawdown, tail, portfolio, operational, capital, monitoring, kill, suspension, and reactivation risk.

Risk may narrow but never broaden Validation. It cannot rewrite evidence or authorize deployment.

## 18. Executive Decision Stage

The Executive Decision Agent consumes current VEP and RRP packages and issues an EDP. It decides the precise institutional disposition: stage authorization, conditional approval, return, rejection, suspension, reactivation, or retirement.

The decision preserves all upstream limitations and cannot override unresolved Validation or Risk blocks.

## 19. Deployment Governance Stage

DGS verifies the exact authorized strategy, implementation, configuration, environment, data, execution, monitoring, limits, kill paths, ownership, rollback, custody, and expiry before any Candidate, Paper, Limited Live, Live Active, scaling, or reactivation action.

Deployment readiness is not executive authority. No stage promotes itself.

## 20. Monitoring and Edge Decay Stage

MEDS establishes baselines, metrics, thresholds, owners, evidence, and escalation for performance, risk, drawdown, execution, data, regimes, portfolio, operations, scope, and edge health.

Monitoring distinguishes normal variance, mechanism decay, regime mismatch, data failure, execution deterioration, and operational failure. Material state changes create governed evidence and actions.

## 21. Feedback Loop and Learning Stage

Feedback from experiments, Validation, Risk, decisions, deployment, monitoring, incidents, failures, returns, rejection, and retirement is classified by affected hypothesis, module, assumption, version, scope, materiality, and urgency.

Every loop produces a Learning Record, updates Knowledge OS when accepted, identifies the exact return stage, preserves negative findings, and states which downstream artifacts or authorities become stale.

Feedback cannot silently change active strategy logic, thresholds, or scope.

## 22. Failure, Return, and Rejection Rules

Return paths may target Market Discovery, Research Question, Knowledge Intake, Strategy Hypothesis, Architecture, Engineering, Experiment Planning, Execution, Evidence Packaging, Validation, Risk Review, Executive Decision, Deployment Governance, or Monitoring.

Every return names reason, owner, required artifact, invalidated downstream state, completion criteria, re-entry condition, and deadline.

Rejection records purpose, evidence, rationale, alternatives, reconsideration criteria, closure, and learning. Failures include insufficient rationale or knowledge, contradiction, unsupported mechanism, fidelity failure, biased plan, irreproducible execution, incomplete evidence, review rejection, readiness failure, edge decay, risk breach, control failure, data/execution failure, portfolio conflict, and governance violation.

## 23. Pipeline State and Progress Rules

The pipeline has one authoritative current state and may have explicitly tracked parallel sub-work only where WOE permits independent ownership. Progress requires satisfied entry and exit criteria, complete artifacts, accepted handoff, and recorded transition authority.

Blocked, waiting, returned, rejected, suspended, retired, and archived are first-class states. “Work completed” is not a valid transition without accepted outputs.

## 24. Pipeline Evidence and Artifact Rules

All observations, hypotheses, experiments, controls, reviews, decisions, monitoring, failures, and learning follow EES. Every institutional product is registered in ART with identity, owner, version, lineage, provenance, status, consumers, dependencies, retention, and audit history.

Evidence cannot be silently replaced. A new version preserves predecessor, reason, impact, and custody. Artifact existence does not create approval authority.

## 25. Pipeline Memory Rules

SMI holds current shared working state, assignments, dependencies, blockers, versions, locks, questions, and handoff status. It does not replace EES, ART, Knowledge OS, or immutable decision records.

No pipeline state may depend on chat history, private model memory, or unstored assumptions. Stale or conflicting shared state blocks transition until reconciled.

## 26. Pipeline Communication Rules

All requests, responses, acknowledgements, delegations, evidence transfers, returns, verdicts, escalations, exceptions, cancellations, and lifecycle events use MACP with explicit identity, version, scope, owner, consumer, required action, and deadline.

Informal communication cannot create authority or complete a gate.

## 27. Pipeline Audit and Reconstruction Rules

An independent reviewer must reconstruct why the pipeline began, what was known, which agents acted, which versions were used, what failed, what evidence existed, how each decision was reached, what authority applied, and why the pipeline progressed, returned, rejected, suspended, retired, or archived.

Reconstruction includes MACP, SMI, EES, WOE, Agent Registry, ART, SLS, EEP, VEP, RRP, EDP, DGS, MEDS, Knowledge OS, timestamps, rejected alternatives, exceptions, and acknowledgements.

## 28. Integration with MACP

MACP is the exclusive institutional communication layer for pipeline actions. Pipeline identity and current versions accompany every authority-bearing message.

## 29. Integration with SMI

SMI stores governed current state, not hidden evidence or private reasoning. Writes follow ownership, locks, lineage, expiry, and audit requirements.

## 30. Integration with EES

EES governs evidence identity, provenance, scope, confidence, limitations, contradictions, custody, freezing, amendments, and admissibility throughout the pipeline.

## 31. Integration with WOE

WOE routes tasks, assigns eligible agents, enforces dependencies and stage gates, handles blocks and returns, and preserves the workflow audit trail. ARP defines the institutional sequence; WOE governs its execution state.

## 32. Integration with Agent Registry

Only active registered agents may enter stages and act within contract, message, memory, evidence, artifact, decision, and workflow rights. Technical capability does not expand authority.

## 33. Integration with Artifact Registry

Every pipeline output—registration, opportunity, question, knowledge intake, hypothesis, handoff, plan, package, verdict, deployment, monitoring, return, rejection, failure, learning, and archive—is an ART-governed artifact.

## 34. Integration with Strategy Lifecycle Standard

Pipeline state and SLS state must remain consistent. ARP coordinates research and institutional handoffs; SLS governs the strategy’s constitutional lifecycle and version consequences.

## 35. Integration with Experiment Evidence Package

EEP is the mandatory frozen evidence handoff from Experiment Execution to Validation. ARP cannot replace EEP with a summary or selected results.

## 36. Integration with Validation Evidence Package

VEP is the mandatory scientific verdict handoff to Risk Review. Its scope, evidence classifications, limitations, conditions, and triggers remain binding downstream.

## 37. Integration with Risk Review Package

RRP is the mandatory risk handoff to Executive Decision. Its limits, controls, monitoring, kill, suspension, reactivation, expiry, and scope remain binding.

## 38. Integration with Executive Decision Package

EDP is the only final institutional strategy decision output. ARP routes and records its authorized transition but cannot alter its verdict or conditions.

## 39. Integration with Deployment Governance Standard

DGS verifies readiness, exact versions, controls, ownership, activation, scaling, suspension, rollback, and retirement execution after EDP authority.

## 40. Integration with Monitoring and Edge Decay Standard

MEDS governs ongoing baselines, health states, thresholds, evidence, escalation, degradation, suspension, reactivation review, and retirement signals. Monitoring feedback re-enters ARP only through a Learning Record and governed return path.

## 41. Governance

### 41.1 Stage responsibility model

- Market Research Agent owns objective discovery.
- Research Librarian owns external acquisition and provenance.
- Knowledge Curator owns institutional knowledge governance.
- Quant Strategy Architect owns hypothesis and architecture.
- Quant Strategy Engineer owns faithful implementation.
- Experiment Orchestrator owns experiment coordination.
- Validation Agent owns independent scientific verdicts.
- Risk Governance Agent owns institutional risk assessment.
- Executive Decision Agent owns final decisions.
- Deployment Governance owns readiness and activation controls.
- Monitoring Governance owns health, decay, escalation, and review.

No agent self-approves prior work where independence is required.

### 41.2 Mandatory stages and outputs

The pipeline must support Pipeline Registration, Market Opportunity, Research Question, Knowledge Intake, Strategy Hypothesis, Architecture Handoff, Engineering Handoff, Experiment Plan Handoff, EEP, VEP, RRP, EDP, DGS, MEDS, Return-to-Stage, Rejection, Failure, Learning, and Archive records.

### 41.3 Mandatory rules

1. Initiation defines purpose, scope, owner, outputs, and success/failure criteria.
2. Each stage has exact ownership, input, output, evidence, and gate.
3. Required packages and authorities cannot be skipped or substituted.
4. Returns name destination, reason, owner, artifact, and re-entry condition.
5. Rejection and failure preserve evidence and learning.
6. Scope, agents, evidence, and state cannot change silently.
7. Backtests and optimization alone cannot advance a strategy.
8. State remains reconstructable without chat history or private memory.

### 41.4 Exceptions and change control

Exceptions are explicit, scoped, time-bounded, independently authorized, and auditable. They cannot legalize self-approval, hidden evidence, stage skipping, unauthorized deployment, missing monitoring, or deleted failure history.

Changes to ARP require cross-system impact analysis, affected-agent and governance review, Executive approval, versioning, migration instructions, and preservation of prior versions.

### 41.5 Institutional rule

Every future AI Quant Lab autonomous research process must conform to this standard before it may claim pipeline status, strategy advancement, deployment readiness, monitoring continuity, or institutional learning completion.
