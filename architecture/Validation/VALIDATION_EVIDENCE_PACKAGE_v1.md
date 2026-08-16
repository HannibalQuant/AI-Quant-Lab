# Validation Evidence Package (VEP) v1.0

## Specification Control

| Field | Value |
|---|---|
| Standard ID | `AIQL-VEP` |
| Version | `1.0.0` |
| Status | Proposed for Sprint 25 review |
| Scope | Every institutional validation review and every handoff of validated evidence to Risk Governance |
| Authority | Research OS, EES, WOE, Agent Registry, Artifact Registry, SLS, EEP, and Validation Governance |
| Provider dependency | None |

The Validation Evidence Package is the mandatory constitutional output of independent scientific validation. It records what evidence was admitted, rejected, or qualified; how reproducibility, robustness, bias, leakage, overfitting, stability, controls, contradictions, and limitations were assessed; and why a verdict was issued.

It is not a performance report, risk approval, executive decision, or deployment authorization. A favorable result does not guarantee scientific admissibility, and scientific admissibility does not establish acceptable institutional risk.

## 1. Validation Evidence Package Philosophy

### 1.1 Validation as independent challenge

Validation tests whether the available evidence supports a stated hypothesis within an explicit scope. It does not improve the strategy, repair experiments, select preferred results, or advocate for deployment.

### 1.2 Evidence quality before performance

Performance magnitude cannot compensate for broken provenance, leakage, irreproducibility, selective reporting, unstable parameters, failed controls, or unsupported assumptions. Validation evaluates the quality and meaning of evidence, not merely its numerical attractiveness.

### 1.3 Conditional scientific conclusions

All verdicts are bounded by strategy version, evidence version, markets, instruments, timeframes, regimes, periods, implementation, data, costs, execution assumptions, and known uncertainty. Uncertainty is managed and disclosed; it is never declared eliminated.

### 1.4 Separation of authorities

Validation determines scientific fitness for Risk Governance. It cannot accept capital risk, authorize production, override governance, or rewrite source evidence.

## 2. Validation Evidence Package Principles

The following principles are binding:

1. No Validation Without Frozen Experiment Evidence.
2. No Verdict Without Defined Scope.
3. No Validation Without Reproducibility Review.
4. No Robustness Claim Without Robustness Evidence.
5. No Approval From Backtest Alone.
6. No Approval From Optimization Alone.
7. No Ignoring Negative Controls.
8. No Ignoring Contradictory Evidence.
9. No Silent Limitation Removal.
10. No Risk Handoff Without Explicit Conditions.
11. Validation Is Not Risk Approval.
12. Validation Is Not Deployment Approval.
13. Every Verdict Must Be Auditable.
14. Rejected Evidence Remains Learnable.

## 3. Package Identity Model

Every VEP has a permanent Validation Package ID, Validation ID, and exact version. Identifiers are never reused. The package is bound to one defined validation question, one strategy version, and exact source EEP versions.

A new package version is required for any amendment. A new Validation ID is required when the validation question, strategy version, material evidence base, or declared scope changes enough that the earlier verdict is no longer the same scientific decision.

Every downstream citation must resolve to the exact frozen package version. References without versions are inadmissible for Risk Governance, executive decisions, deployment review, or lifecycle transitions.

## 4. Package Object Model

The Validation Package Record must define:

| Field | Requirement |
|---|---|
| Validation Package ID | Permanent unique package identifier |
| Validation ID | Governed validation activity identifier |
| Validation Owner / Agent | Accountable registered authority and executing agent |
| Strategy ID / Version | Exact strategy under review |
| Strategy Lifecycle State | State at validation intake |
| Source EEP / Version | Exact frozen experimental package or packages |
| Validation Scope / Question | Boundaries and scientific question |
| Evidence Intake Status | Intake completion and defects |
| Evidence Admissibility Status | Admitted, excluded, or qualified evidence state |
| Completeness Status | Mandatory content and linkage assessment |
| Reproducibility Status | Independent reproduction assessment |
| Robustness Status | Robustness evidence assessment |
| Bias / Leakage / Overfitting Assessments | Separate findings, severity, and consequences |
| Parameter Stability Assessment | Stability regions, sensitivity, and selection risk |
| Negative Control Assessment | Control adequacy and outcomes |
| Adversarial Test Assessment | Stress design and outcomes |
| Contradictory Evidence Assessment | Conflicts and unresolved implications |
| Limitation Assessment | Known boundaries and uncertainty |
| Accepted Evidence | Exact evidence objects admitted without qualification |
| Rejected Evidence | Exact evidence objects excluded with reasons |
| Qualified Evidence | Evidence usable only under explicit constraints |
| Validation Verdict / Rationale | Authorized outcome and evidence-based reasoning |
| Verdict Scope / Limitations | Exact domain of validity and exclusions |
| Validation Conditions | Conditions attached to the verdict |
| Required Follow-Up | Required experiments, corrections, monitoring, or review |
| Risk Handoff Status / Conditions | Eligibility and constraints for Risk Governance |
| Source MACP Message | Initiating validation request |
| Related SMI Memory Objects | Governed shared-state references |
| Related EES Evidence Objects | Exact evidence inputs and validation outputs |
| Related Artifact Records | EEPs, reports, reproduction outputs, and package record |
| Related Workflow Objects | Governing WOE workflow and stages |
| Related Strategy Record | Exact SLS record and version |
| Created At / Updated At | Governed timestamps |
| Audit Trail | Immutable events, actors, versions, and custody changes |

Missing mandatory fields block issuance unless explicitly inapplicable, justified, and accepted by validation governance.

## 5. Package Lifecycle

**Proposed → Evidence Intake → Admissibility Review → Scientific Review → Verdict Drafted → Frozen → Issued → Returned → Amended → Revoked → Archived**

| State | Meaning |
|---|---|
| Proposed | Validation identity and question registered |
| Evidence Intake | Frozen EEPs and related evidence received |
| Admissibility Review | Completeness, provenance, custody, scope, and integrity assessed |
| Scientific Review | Reproducibility, robustness, bias, stability, controls, and contradictions examined |
| Verdict Drafted | Provisional conclusion and rationale prepared |
| Frozen | Package sealed against in-place editing |
| Issued | Authorized verdict released to named consumers |
| Returned | Evidence or package sent back with explicit deficiencies |
| Amended | New linked package version issued after governed change |
| Revoked | Earlier verdict no longer institutionally reliable |
| Archived | Immutable history retained for reconstruction and learning |

Only Frozen packages may be Issued. Return, amendment, and revocation preserve every earlier version and decision.

## 6. Validation Intake Record

Intake verifies the submitting workflow, sender authority, strategy identity and lifecycle state, exact EEP version, frozen status, chain of custody, experiment-plan linkage, implementation and data versions, completeness declaration, and unresolved package limitations.

The validation scope is fixed before scientific review and identifies claims, markets, instruments, timeframes, periods, regimes, implementation, execution model, costs, and intended downstream use.

Intake does not presume admissibility. Missing, stale, inconsistent, mutable, unauthorized, or out-of-scope evidence is returned or classified for exclusion.

## 7. Evidence Admissibility Record

Each evidence object is classified as `Accepted`, `Rejected`, or `Qualified`.

Accepted evidence has intact provenance, custody, version integrity, declared scope, relevant method, visible limitations, and sufficient reproducibility for its intended use. Rejected evidence remains recorded with a precise reason. Qualified evidence states the exact restrictions under which it may inform the verdict.

Admissibility review covers completeness, provenance, scope, recency, relevance, independence, consistency, plan conformance, implementation fidelity, data integrity, execution assumptions, known contradictions, and EES status.

Evidence is not admitted merely because it supports the hypothesis, and it is not rejected merely because it weakens it.

## 8. Reproducibility Review Record

The review determines whether an authorized independent party can reproduce inputs, environment, configuration, execution, calculations, and material outputs from the frozen EEP.

Status is `Not Assessed`, `Blocked`, `Partially Reproduced`, `Reproduced`, or `Failed`. The record identifies reviewer, source versions, reproduction method, comparison tolerances, matches, differences, unexplained divergence, and scientific consequence.

Approval requires reproduction sufficient for the declared scope. Partial reproduction may support only a limited verdict. Failed or blocked reproduction requires more evidence or rejection when it affects material claims.

## 9. Robustness Review Record

Robustness review evaluates whether conclusions persist under defensible changes in samples, time, regimes, markets, timeframes, parameters, costs, execution, and random perturbations.

Mandatory review areas include walk-forward design, untouched out-of-sample evidence, Monte Carlo methods, temporal stability, cross-market and cross-timeframe behavior, regime dependence, cost sensitivity, execution stress, adversarial tests, replication, and failure distribution.

The record distinguishes breadth of testing from independence of testing. Repeated variants of the same favorable sample do not establish robustness. Missing robustness dimensions become explicit limitations or follow-up requirements.

## 10. Bias, Leakage, and Overfitting Review Record

The Validation Agent assesses confirmation, selection, survivorship, look-ahead, data leakage, data snooping, publication, narrative, recency, authority, and post-selection bias.

Leakage analysis covers temporal ordering, labels, features, preprocessing, normalization, universe construction, parameter selection, repeated holdout access, walk-forward boundaries, and implementation timing.

Overfitting analysis covers search breadth, multiple testing, objective design, pruning, trial count, selection rules, parameter sensitivity, feature redundancy, model complexity, isolated optima, in/out-of-sample decay, and robustness across seeds.

Each assessment states evidence, severity, affected claims, mitigation, residual uncertainty, and verdict impact. Material uncorrected leakage invalidates affected evidence.

## 11. Parameter Stability Review Record

The review assesses whether acceptable behavior occupies defensible parameter regions rather than isolated peaks. It examines local sensitivity, interactions, boundary selections, economically plausible ranges, seed stability, selection frequency, and degradation away from the chosen point.

The record distinguishes parameters required by the mechanism from degrees of freedom added for fit. Stability cannot prove edge, but instability may refute robustness or restrict the verdict.

Parameter changes after validation require versioning and proportional revalidation under SLS.

## 12. Negative Control Review Record

Negative controls are reviewed for rationale, structural appropriateness, independence, implementation fidelity, expected behavior, complete results, and interpretation.

Controls that perform similarly to or better than the strategy weaken the proposed mechanism and require explanation, additional evidence, or rejection. Unfavorable controls cannot be omitted or reclassified after observation.

The absence of a feasible control must be justified and carried as a limitation. Validation must also assess adversarial tests intended to expose dependence on favorable execution, data, timing, or regimes.

## 13. Contradiction and Limitation Record

Every material contradiction identifies the conflicting evidence, claims affected, source quality, scope, possible reconciliation, unresolved uncertainty, and verdict consequence. Contradictions remain visible even if the final verdict is favorable.

Limitations cover data, sample sufficiency, power, regime representation, markets, timeframes, implementation, assumptions, costs, liquidity, capacity, statistics, reproducibility, robustness, external validity, and monitoring needs.

The record must state what evidence supports, weakens, refutes, and fails to prove. Silence is not resolution.

## 14. Validation Verdict Model

Authorized verdicts are:

### APPROVED

Evidence is admissible, sufficiently reproducible and robust for the declared scope, and scientifically fit to proceed to Risk Governance. Approval does not imply acceptable risk or deployment authority.

### APPROVED WITH LIMITATIONS

Evidence is scientifically usable only within explicit limits, restrictions, regimes, markets, timeframes, assumptions, or monitoring conditions. Every limitation travels to Risk Governance.

### REQUIRES MORE EVIDENCE

Evidence is incomplete, underpowered, insufficiently robust, non-reproducible, materially contradicted, or too uncertain for risk review. Required follow-up must be specific and testable.

### REJECTED

Material defects—such as broken provenance, leakage, invalid assumptions, irreproducibility, severe overfitting, failed controls, unsupported claims, or decisive contradictions—prevent scientific reliance.

Every verdict includes rationale, accepted/rejected/qualified evidence, scope, confidence, assumptions, limitations, conditions, alternatives considered, follow-up, revalidation triggers, and authorized signer.

## 15. Conditional Approval Rules

A limited verdict must define exact permissible markets, instruments, timeframes, regimes, periods, implementation, data, parameters, execution assumptions, costs, exposure context, monitoring requirements, expiry, and invalidation triggers.

Conditions must be observable and enforceable. Ambiguous phrases such as “use cautiously” are prohibited. Failure to satisfy a condition prevents Risk Handoff or revokes eligibility.

Risk Governance may impose stricter limits but cannot broaden the scientific scope approved by Validation.

## 16. Rejection and Return Rules

Return is appropriate when remediable packaging, completeness, consistency, or reproducibility defects prevent review. Rejection is appropriate when evidence materially fails the scientific claim or contains defects that cannot be cured without a new experiment or hypothesis.

Every return or rejection identifies reasons, affected claims, evidence status, required owner, permitted remedy, lifecycle destination, and whether a new EEP, experiment, strategy version, or validation is required.

Rejected evidence and negative findings remain available to the Failure Database and Knowledge OS. Resubmission cannot overwrite prior history.

## 17. Risk Governance Handoff Requirements

The issued VEP must provide Risk Governance with:

- validation verdict, rationale, scope, and expiry;
- exact Strategy ID and version;
- accepted, rejected, and qualified evidence;
- robustness and reproducibility limitations;
- market, timeframe, regime, data, and execution limitations;
- leakage, bias, overfitting, stability, and statistical concerns;
- known contradictions and failure cases;
- required monitoring conditions and proposed risk controls;
- open questions, conditions, and revalidation triggers;
- exact frozen VEP, EEP, EES, ART, and decision references.

Risk Handoff status is `Not Eligible`, `Eligible With Conditions`, `Eligible`, `Returned`, or `Revoked`. Only `APPROVED` or `APPROVED WITH LIMITATIONS` may be Eligible, subject to all conditions.

## 18. Validation Freezing and Chain of Custody

Freezing seals the package manifest, evidence classifications, analyses, verdict, rationale, conditions, artifacts, versions, and audit trail. A frozen package cannot be edited in place.

Custody records intake, access, reviewer assignments, reproduction, challenges, freeze, issuance, handoff, amendment, revocation, and archival. Loss of integrity suspends admissibility and Risk Handoff.

Amendments create new versions, enumerate changes and reasons, preserve predecessors, reassess affected areas, and repeat freeze and issuance controls. Revocation never deletes the original verdict.

## 19. Integration with MACP

MACP governs validation requests, intake acknowledgements, evidence questions, returns, challenges, verdict issuance, Risk Handoff, amendments, revocations, and archival events. Messages cite exact strategy, EEP, VEP, EES, artifact, workflow, and agent-contract versions.

Informal communication cannot create or modify a verdict.

## 20. Integration with SMI

SMI holds governed review state, ownership, assignments, locks, outstanding questions, conflicts, dependencies, current package version, and handoff status. It cannot hide evidence or mutate frozen records.

Stale or conflicting memory state blocks issuance until reconciled through auditable events.

## 21. Integration with EES

All validation inputs and outputs are governed EES objects with provenance, scope, versions, limitations, contradictions, confidence, reproducibility, admissibility, custody, and audit history.

The VEP classifies evidence but does not alter source evidence. Challenges and amendments create linked evidence objects.

## 22. Integration with WOE

WOE enforces intake, admissibility, scientific review, verdict, freeze, issue, return, amendment, revocation, and handoff gates. Validation Review cannot advance to Risk Review without an issued eligible VEP.

Workflow acceleration cannot skip scientific or custody gates.

## 23. Integration with Agent Registry

Only active registered agents with validation rights may review evidence or issue verdicts. The Validation Agent cannot validate its own research, accept risk, authorize deployment, or expand its authority through technical capability.

Delegation is bounded, explicit, and auditable; final verdict authority remains with the registered Validation owner.

## 24. Integration with Artifact Registry

The VEP, review workpapers, reproduction records, challenges, returns, verdicts, amendments, revocations, and handoff records are registered artifacts with identity, ownership, versions, lineage, provenance, consumers, status, retention, and audit history.

An artifact is not authoritative outside the scope and authority of its registered record.

## 25. Integration with Strategy Lifecycle Standard

The VEP is the mandatory output for transition from `Validation Review` to `Validation Passed` and eligibility for `Risk Review`. It binds its verdict to the exact Strategy ID, version, implementation, evidence, and lifecycle state.

Material strategy changes invalidate or limit prior applicability and trigger lifecycle return and proportional revalidation.

## 26. Integration with Experiment Evidence Package

Validation may review only frozen EEP versions. It verifies package completeness, plan conformance, exact version linkage, evidence integrity, failures, deviations, controls, reproducibility, limitations, and Validation Readiness.

The Validation Agent may return the EEP for amendment but cannot edit, curate, or selectively replace its contents. An amended EEP requires renewed intake and impact assessment.

## 27. Governance

### 27.1 Mandatory review areas

Every validation covers evidence completeness, provenance, scope, version integrity, plan conformance, implementation fidelity, data integrity, execution and cost assumptions, reproducibility, walk-forward, Monte Carlo, parameter stability, cross-market, cross-timeframe, temporal robustness, negative controls, adversarial tests, bias, leakage, overfitting, statistical reliability, practical significance, contradictions, limitations, and failure cases.

### 27.2 Mandatory rules

1. Only frozen EEPs may be reviewed.
2. Scope is defined before verdict.
3. Scientific validity is separate from risk acceptability and performance.
4. Backtest or optimization output alone cannot prove edge.
5. Reproducibility, leakage, bias, overfitting, controls, and stability are assessed before approval.
6. Negative controls and contradictions remain visible.
7. Accepted, rejected, and qualified evidence are explicit.
8. Limitations travel to Risk Governance.
9. Conditional verdicts state exact conditions.
10. Rejected packages preserve learning value.
11. Validation may return evidence but cannot rewrite it.
12. Validation cannot approve deployment or accept risk.
13. Frozen VEPs cannot be edited in place.
14. Amendments create new versions.
15. Revoked validations remain reconstructable.

### 27.3 Exceptions and change control

Exceptions are explicit, scoped, time-bounded, independently approved, and attached to all downstream use. They cannot authorize self-validation, mutable source evidence, hidden limitations, ignored contradictions, or deployment approval.

Amendments to this standard require cross-system impact analysis, independent validation-governance review, executive approval, versioning, migration rules, and preservation of prior versions.

### 27.4 Institutional rule

Every future AI Quant Lab validation review must produce a conforming Validation Evidence Package before a strategy may proceed to Risk Governance, Executive Decision, deployment review, or lifecycle advancement.
