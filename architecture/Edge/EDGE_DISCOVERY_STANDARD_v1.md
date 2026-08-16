# Edge Discovery Standard (EDS) v1.0

## Specification Control

| Field | Value |
|---|---|
| Standard ID | `AIQL-EDS` |
| Version | `1.0.0` |
| Status | Proposed for Sprint 34 review |
| Scope | Every institutional edge candidate and edge-to-architecture handoff |
| Authority | Research OS, MDRS, RCS, FFS, ARP, SLS, EES, EEP, VEP, RRP, MEDS, and edge governance |

The Edge Discovery Standard governs pre-strategy investigation of whether observed market behavior may contain a research-worthy, conditional effect. It is not a strategy, optimizer, signal generator, backtest approval, or implementation. An edge candidate is a falsifiable research claim—not permission to trade.

## 1. Edge Discovery Philosophy

Edge discovery begins with behavior and mechanism, then identifies measurements. It asks whether an effect exists, why it may persist, where it applies, what would refute it, and whether it survives realistic frictions and controls.

Statistical association is evidence, not causality. Profit is an outcome, not proof. Strong candidates remain provisional until later experimentation and independent Validation.

## 2. Edge Discovery Principles

No discovery proceeds without market context, defined behavior, mechanism rationale, null hypothesis, alternatives, regime context, governed features, costs, execution, sample review, stability, negative controls, contradictions, and auditability.

Backtest profit, optimization output, indicator signals, and correlation alone cannot establish edge. Hindsight definitions, silent reclassification, and performance-only progression are prohibited. Weak, deferred, contradicted, and rejected candidates remain institutional knowledge.

## 3. Edge Discovery Identity Model

Every candidate has a permanent Edge Discovery ID, Edge Record ID, and exact version. Identity binds market, instrument, timeframe, period, data, MDRS record, RCS record, FFS records, behavior, mechanism, and owner.

Material changes to behavior, mechanism, scope, regime dependency, or intended interpretation require a new Edge ID. Evidence amendments create linked versions and preserve history.

## 4. Edge Discovery Object Model

The Edge Record must define identity and ownership; market, venue, instrument, timeframe, period, and data versions; candidate name/type; behavior and mechanism; rationale; null and alternative hypotheses; alternative explanations; required and excluded conditions; regime and feature records; measurement rationale; effect size, direction, persistence, sample sufficiency, and stability; cost and execution awareness; controls; contradictions, limitations, risks, biases, and leakage; strength, confidence, maturity, handoff, rejection, deferral, follow-up; MACP, SMI, EES, ART, WOE, Agent references; timestamps and immutable audit trail.

## 5. Edge Discovery Lifecycle

**Proposed → Behavior Observed → Candidate Defined → Evidence Intake → Preliminary Tested → Mechanism Reviewed → Control Tested → Edge Classified → Research Handoff Candidate → Deferred → Rejected → Challenged → Superseded → Archived**

No state implies Validation. Challenge preserves the frozen classification while new evidence is assessed. Rejection and supersession never erase prior use.

## 6. Edge Candidate Definition

A candidate defines the observed behavior, market scope, expected mechanism, conditions, failure conditions, regime dependency, required information, measurable effect, null, alternatives, costs, execution constraints, and minimum evidence for progression.

The definition precedes confirmatory testing. Post-result refinements are exploratory and separately versioned.

## 7. Edge Taxonomy

Mandatory types are Trend Continuation, Momentum Persistence, Breakout Continuation, Breakout Failure, Mean Reversion, Pullback Continuation, Volatility Expansion, Volatility Compression, Range Rotation, Liquidity Expansion, Liquidity Contraction, Volume Participation, Session Behavior, Relative Strength, Cross-Market Relationship, Regime Transition, Risk Premium, Execution Inefficiency, Portfolio Diversification, and Hybrid Edge.

Hybrid candidates preserve separate mechanisms, evidence, dependencies, and failure modes.

## 8. Market Behavior Evidence Requirements

Evidence identifies exact MDRS market context, data lineage, observation window, behavior definition, magnitude, frequency, persistence, uncertainty, regimes, noise, whipsaw, tails, gaps, liquidity, costs, and contradictions.

Behavior must be observable independently of the proposed strategy implementation.

## 9. Mechanism Plausibility Requirements

The mechanism may invoke microstructure, participant behavior, liquidity imbalance, volatility clustering, risk transfer, positioning, persistence, delayed reaction, forced flows, sessions, structural ranges, breakout acceptance/rejection, reversion, cross-market transmission, execution inefficiency, or portfolio interaction.

It must explain expected conditions, persistence, failure, alternatives, and evidence that could challenge it. Narrative plausibility without discriminating predictions is insufficient.

## 10. Feature Relationship Requirements

Every measurement cites exact FFS identity, version, lineage, timing, scope, transformation, redundancy, leakage, bias, and limitations. Feature relationship is distinguished from mechanism and tradable strategy.

Multiple redundant features cannot masquerade as independent confirmation.

## 11. Regime Dependency Requirements

Candidates cite exact RCS labels, versions, confidence, uncertainty, transitions, applicable and excluded regimes, and conflicting evidence. Effects are disaggregated rather than averaged across materially different regimes.

Unknown and transition regimes receive explicit handling.

## 12. Effect Size Requirements

Effect reporting includes definition, direction, magnitude, uncertainty interval, practical relevance, baseline comparison, distribution, tails, regime breakdown, and sensitivity to defensible measurement choices.

Statistical significance without meaningful magnitude, costs, or mechanism is insufficient.

## 13. Sample Sufficiency Requirements

Review considers independent observations, event count, trade-independent behavior count, regime representation, temporal span, dependence, power, tails, missingness, and data quality.

Large row counts do not substitute for independent market episodes. Weak samples remain visible and restrict maturity.

## 14. Stability Requirements

Stability is assessed across time, windows, markets, timeframes, regimes, data sources, feature alternatives, perturbations, seeds where applicable, and realistic costs.

The record distinguishes stable effect, conditional effect, isolated episode, decay, contradiction, and insufficient evidence.

## 15. Cost and Execution Awareness

Discovery estimates whether plausible spread, fees, slippage, funding, borrowing, latency, fills, gaps, liquidity, capacity, and impact could consume or reverse the effect.

This is feasibility screening, not deployment readiness. Unknown critical friction blocks research-ready classification or becomes a hard limitation.

## 16. Null Hypothesis Requirements

The null states what outcome is expected without the proposed mechanism and how it will be evaluated. It must be capable of surviving testing; a null designed only to lose is invalid.

Failure to reject the null is preserved and cannot be relabeled as support.

## 17. Alternative Explanation Requirements

Alternatives include regime coincidence, data artifact, selection, leakage, survivorship, common factor, volatility exposure, liquidity premium, cost omission, session effect, execution artifact, and chance.

Each credible alternative identifies distinguishing evidence and unresolved implications.

## 18. Negative Control Requirements

Controls are preregistered where possible and may include randomized timing, shuffled returns, shifted or inverted features, unrelated features/markets/timeframes, destroyed temporal structure, placebo or random regimes, random thresholds, leakage checks, cost inflation, slippage/spread stress, and missed actions.

Controls do not validate edge by themselves; material failure against them blocks progression.

## 19. Edge Strength Classification

Authorized strength states are `STRONG`, `MODERATE`, `WEAK`, `INCONCLUSIVE`, `CONTRADICTED`, and `INVALID`. Strength reflects evidence magnitude, consistency, controls, stability, and practical relevance—not optimism.

## 20. Edge Confidence Classification

Authorized confidence states are `HIGH`, `MEDIUM`, `LOW`, `INSUFFICIENT`, and `CONFLICTED`. Confidence accounts for data quality, sample sufficiency, independence, contradictions, regime scope, costs, and reproducibility.

## 21. Edge Maturity Classification

Authorized maturity states are `OBSERVED`, `PLAUSIBLE`, `PRELIMINARY`, `RESEARCH_READY`, `EXPERIMENT_READY`, `VALIDATION_CANDIDATE`, `REJECTED`, and `DEFERRED`.

Maturity governs the next research action, not institutional approval. `VALIDATION_CANDIDATE` requires later EEP and VEP processes.

## 22. Edge Rejection and Deferral Rules

Rejection applies to invalid behavior, decisive contradiction, broken mechanism, material leakage, control failure, non-executable effect, or absent research value. Deferral applies to remediable data, sample, regime, cost, execution, or knowledge gaps.

Every disposition records reason, evidence, owner, reconsideration criteria, follow-up, expiry, and learning value.

## 23. Edge Research Handoff Requirements

Architecture handoff requires a frozen record classified at least `RESEARCH_READY`, exact market/regime/feature context, behavior, mechanism, null, alternatives, effect, sample, stability, costs, execution, controls, contradictions, limitations, prohibited interpretations, suggested family, experiments, and follow-up.

The handoff may recommend direction but cannot define entry, exit, parameters, Validation, Risk, or Deployment approval.

## 24. Edge Evidence Packaging

Every classified, challenged, deferred, rejected, superseded, or invalidated candidate has a frozen EES package containing identities, versions, scope, evidence, methods, controls, failures, classifications, uncertainty, limitations, custody, and consumer history.

## 25. Edge Audit and Reconstruction

An independent reviewer must reconstruct what behavior and mechanism were defined before testing, which evidence and controls were available, how classifications changed, who consumed them, and whether downstream work remained within scope.

Historical records are never rewritten with hindsight.

## 26. Integration with MACP

MACP governs observation, proposal, evidence intake, tests, mechanism review, controls, classification, challenge, handoff, rejection, deferral, supersession, and archival with exact versions.

## 27. Integration with SMI

SMI holds current state, owner, blockers, locks, open alternatives, classification, consumers, and follow-up. It cannot silently mutate frozen evidence or definitions.

## 28. Integration with EES

All edge claims and challenges use EES objects with provenance, scope, uncertainty, contradictions, confidence, versions, custody, and admissibility.

## 29. Integration with WOE

WOE enforces definition, evidence, testing, mechanism, control, classification, handoff, return, rejection, challenge, supersession, and archival gates.

## 30. Integration with Agent Registry

Only registered agents may create, review, challenge, classify, or consume edge records within their rights. No originating agent self-validates institutional truth.

## 31. Integration with Artifact Registry

Candidate, evidence, control, classification, handoff, rejection, deferral, challenge, supersession, learning, and archive records are ART-governed artifacts with lineage and provenance.

## 32. Integration with Strategy Lifecycle Standard

EDS operates between Market Research and full Architecture. No strategy advances beyond hypothesis formation without a scoped Edge Discovery Record. Material edge changes trigger SLS return and version review.

## 33. Integration with Autonomous Research Pipeline

ARP routes Market Discovery through Edge Discovery to hypothesis and Architecture. It cannot substitute ungoverned analysis, backtest output, or optimizer results for EDS.

## 34. Integration with Market Discovery & Ranking Standard

MDRS provides the frozen Market Opportunity Record and research context. A high MDRS score is not edge evidence and cannot preselect the conclusion.

## 35. Integration with Regime Classification Standard

RCS supplies exact regime context, confidence, uncertainty, transitions, and conflicts. EDS cannot silently relabel regimes after observing effects.

## 36. Integration with Feature Factory Standard

FFS supplies governed measurements and review status. EDS cannot redefine feature semantics, ignore redundancy, or use out-of-scope versions.

## 37. Integration with Experiment Evidence Package

Research-ready candidates generate preregistered experiments whose evidence is packaged through EEP. EDS classifications travel as prior claims and cannot be rewritten by results.

## 38. Integration with Validation Evidence Package

VEP independently assesses whether later experiment evidence supports the strategy hypothesis. Edge confidence does not constrain Validation from rejecting it.

## 39. Integration with Risk Review Package

RRP may inspect edge conditions, decay, costs, capacity, tails, and failure modes but cannot treat EDS as validated evidence or broaden scope.

## 40. Integration with Monitoring and Edge Decay Standard

MEDS monitors the expected mechanism, conditions, feature relations, regime dependencies, and decay triggers derived from the frozen edge record. Monitoring evidence may challenge EDS through governed review.

## 41. Governance

Every review covers behavior, mechanism, feature and regime dependencies, effect, sample, temporal/cross-market/cross-regime stability, costs, execution, noise, whipsaw, tails, capacity, data, leakage, bias, alternatives, contradictions, controls, novelty, family relevance, and operational feasibility.

Mandatory rules preserve the separation of behavior, mechanism, measurement, statistical effect, executable edge, strategy, Validation, and Deployment. Frozen records cannot be edited in place; amendments create versions; invalidated records remain reconstructable.

Exceptions are scoped, time-bounded, independently approved, and cannot legalize hindsight definition, absent nulls, hidden controls, leakage, or performance-only progression. Changes require cross-system impact review, versioning, migration, and preserved history.

Every future AI Quant Lab edge claim, candidate, pre-strategy research direction, strategy-family recommendation, and edge-to-architecture handoff must conform to this standard.
