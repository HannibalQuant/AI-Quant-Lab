# Regime Classification Standard (RCS) v1.0

## Specification Control

| Field | Value |
|---|---|
| Standard ID | `AIQL-RCS` |
| Version | `1.0.0` |
| Status | Proposed for Sprint 32 review |
| Scope | Every institutional regime label, assumption, experiment, review, deployment boundary, and drift assessment |
| Authority | Market Research, MDRS, ARP, SLS, EES, VEP, RRP, DGS, MEDS, and regime governance |
| Provider dependency | None |

The Regime Classification Standard governs how market context is identified, evidenced, labeled, qualified, challenged, versioned, transferred, monitored, and retired throughout AI Quant Lab.

It is not a strategy, indicator system, signal generator, prediction engine, or implementation. Regime is contextual evidence, not edge. Classification describes an observed or historically bounded state; it does not guarantee persistence or forecast transition.

## 1. Regime Classification Philosophy

Markets exhibit overlapping properties rather than perfectly separated categories. A useful regime record therefore states scope, evidence, confidence, uncertainty, alternatives, and contradictions instead of presenting a label as objective truth.

Classification exists to prevent materially different conditions from being averaged into misleading conclusions. It preserves the environmental context in which hypotheses, experiments, Validation, Risk, Deployment, and Monitoring are interpreted.

Unknown, uncertain, mixed, and transitional states are valid institutional outputs. Forced certainty is a classification failure.

## 2. Regime Classification Principles

The following principles are binding:

1. No Regime Without Scope, Evidence, Confidence, and Uncertainty Disclosure.
2. No Strategy Assumption From an Unclassified Regime.
3. No Regime Label From One Indicator Alone.
4. No Silent Regime Change or Conflict Resolution.
5. Transition, Uncertain, Mixed, and Unknown States Cannot Be Ignored.
6. Materially Different Regimes Cannot Be Averaged Away.
7. Validation Requires Regime Scope; Risk Requires Regime Limits.
8. Deployment Cannot Operate Outside Authorized Regime Scope.
9. Monitoring Must Detect Drift, Mismatch, and Transition.
10. Regime Is Context, Not Edge or Prediction.
11. Every Classification Must Be Auditable.

## 3. Regime Identity Model

Every classification has a permanent Regime Classification ID, Regime Record ID, and exact version. Identity binds market universe, asset class, venue, instrument, timeframe, observation period, data version, taxonomy version, label, and owner.

A materially different scope or taxonomy requires a new classification identity. Amendments to evidence, confidence, limitations, or label create linked versions. Identifiers are never reused.

## 4. Regime Object Model

The Regime Record must define:

| Record group | Mandatory content |
|---|---|
| Identity | Classification ID, record ID, owner, responsible agent, Market Discovery ID |
| Scope | Universe, asset class, venue, instrument, symbol, timeframe, period |
| Data | Source, version, coverage, quality, and limitations |
| Classification | Taxonomy version, label, subtype, scope, rationale, method rationale |
| Evidence | Supporting, weakening, conflicting, alternative-label, and contradictory evidence |
| Confidence | Level, uncertainty, persistence, duration, stability, and transition status |
| Dimensions | Trend, range, volatility, liquidity, breakout, reversion, noise, whipsaw, tails, gaps, correlation, sessions |
| Implications | Strategy-family, Validation, Risk, Deployment, and Monitoring implications |
| Governance | Known limitations, prohibited interpretations, follow-up, status, and expiry |
| Integrations | Source MACP and related SMI, EES, ART, WOE, and Agent records |
| History | Created At, Updated At, versions, and immutable Audit Trail |

Every institutional use cites the exact Regime Record version.

## 5. Regime Lifecycle

**Proposed → Evidence Intake → Preliminary Classification → Confidence Review → Accepted → Accepted With Limitations → Challenged → Superseded → Invalidated → Archived**

Acceptance does not freeze the market; it freezes the institutional interpretation of evidence for the stated scope and period. Challenge preserves the current record while new evidence is evaluated.

Invalidation removes future reliance but preserves every historical use and downstream consequence.

## 6. Regime Taxonomy

Mandatory regime types are:

- `TREND_UP`, `TREND_DOWN`, `RANGE`
- `HIGH_VOLATILITY`, `LOW_VOLATILITY`
- `VOLATILITY_EXPANSION`, `VOLATILITY_COMPRESSION`
- `BREAKOUT_FORMATION`, `BREAKOUT_CONTINUATION`, `BREAKOUT_FAILURE`
- `MEAN_REVERSION`
- `LIQUIDITY_EXPANSION`, `LIQUIDITY_CONTRACTION`
- `EVENT_DRIVEN`, `TRANSITION`, `MIXED`, `UNCERTAIN`, `UNKNOWN`

Labels may coexist across orthogonal dimensions, such as directional and volatility state. A primary label cannot conceal a material secondary dimension.

Taxonomy changes require definitions, relationships, migration rules, backward-compatibility analysis, and preserved earlier versions.

## 7. Regime Evidence Requirements

Evidence must define provenance, data version, scope, period, sampling, quality, measurement rationale, relevant dimensions, uncertainty, contradictions, and reproducibility.

Required dimensions include directionality, trend strength and persistence, path efficiency, range boundaries and stability, volatility level/change/clustering, breakout pressure and follow-through, false breaks, reversion pressure, liquidity, spread, slippage, noise, whipsaw, tails, gaps, correlation, sessions, duration, and transition frequency.

No single measurement may establish a regime. Evidence must be sufficiently independent and relevant to the classification claim.

## 8. Trend Regime Classification

Trend classification separates direction from quality. It evaluates directional persistence, path efficiency, duration, retracement behavior, participation, usable volatility, whipsaw, transition risk, and stability across observation windows.

`TREND_UP` and `TREND_DOWN` require evidence of persistent direction, not merely positive or negative recent return. Weak quality or conflicting volatility/liquidity state remains visible.

## 9. Range Regime Classification

Range classification evaluates bounded structure, boundary stability, traversal, reversion pressure, overshoots, false escapes, duration, volatility, liquidity, and structural-break risk.

A range is not inferred solely from low trend measurement. Uncertain containment or frequent boundary change may require `MIXED` or `TRANSITION`.

## 10. Volatility Regime Classification

Volatility classification separates level from change, clustering, usability, and execution consequence. High or low volatility is relative to a declared reference distribution and scope.

Expansion and compression identify directional change in volatility state, not strategy signals. Extreme movement, gaps, spread, liquidity, and tails qualify the label.

## 11. Breakout Regime Classification

`BREAKOUT_FORMATION` requires an evidenced structural boundary or compression context and growing release pressure. `BREAKOUT_CONTINUATION` requires acceptance and follow-through. `BREAKOUT_FAILURE` records rejection, reversal, or inability to sustain escape.

Formation is never treated as successful breakout after observing only boundary contact. False-breakout evidence remains explicit.

## 12. Mean Reversion Regime Classification

Mean-reversion classification evaluates bounded reference behavior, displacement, conditional return, restoration speed, overshoot, persistence, liquidity, tail risk, and failure under structural transition.

Reversion pressure is not proof of tradable mean reversion. The record distinguishes statistical tendency from executable opportunity.

## 13. Liquidity Regime Classification

Liquidity classification evaluates availability, depth or defensible proxies, turnover, spread, slippage, fragmentation, participation constraints, resilience, and stressed exit capacity.

Liquidity availability is distinct from executable capacity. Expansion or contraction is relative to a declared baseline and conditioned on venue, instrument, size, and timeframe.

## 14. Transition and Uncertain Regime Classification

`TRANSITION` applies when evidence supports an ongoing move between states. It records origin candidates, destination candidates, transition evidence, confidence, instability, and invalidation.

`MIXED` applies to simultaneously material incompatible or orthogonal states. `UNCERTAIN` applies when evidence is usable but insufficiently decisive. `UNKNOWN` applies when classification is not defensible because evidence or data is inadequate.

Transition must be distinguished from noise using persistence, breadth, structure, and alternative explanations.

## 15. Regime Confidence Model

Authorized confidence levels are `HIGH`, `MEDIUM`, `LOW`, `INSUFFICIENT`, and `CONFLICTED`.

HIGH requires consistent multi-dimensional evidence, adequate data, sufficient representation, low contradiction, stable classification, and clear scope. MEDIUM permits bounded limitations. LOW indicates visible but unstable support. INSUFFICIENT means reliable classification is unavailable. CONFLICTED means materially different labels have credible support.

Confidence is conditional, time-stamped, and independent of label desirability.

## 16. Regime Persistence and Duration Rules

Persistence records how consistently the state remains observable across defensible windows. Duration records observed time in state without implying future survival.

The record includes interruptions, uncertainty intervals, right-censoring, historical distribution, and differences by market session or condition. Minimum persistence requirements depend on intended use and timeframe.

## 17. Regime Transition Rules

Every transition records source label, candidate destination, initiating evidence, start estimate, confidence, persistence, alternative explanations, and completion or failure criteria.

Classification changes are versioned events. They cannot be backdated to improve strategy results. Historical labels remain as known at the relevant decision time.

## 18. Regime Conflict and Ambiguity Rules

Conflicts preserve all credible labels, evidence quality, dimensional source, scope, and downstream impact. Resolution may produce primary/secondary labels, narrower scope, lower confidence, `MIXED`, `UNCERTAIN`, or `CONFLICTED`.

No conflict may be resolved by deleting inconvenient evidence or selecting the label most favorable to a strategy.

## 19. Regime Fit for Strategy Families

- Trend Following requires direction, persistence, efficiency, usable volatility, and tolerable whipsaw.
- Breakout requires formation, structural boundary, pressure, follow-through potential, and controlled false breaks.
- Momentum requires persistence, participation, usable volatility, and controlled tails.
- Pullback Continuation requires established trend, recurrent retracement, continuation evidence, and invalidation context.
- Mean Reversion requires range structure, reversion pressure, bounded failure, liquidity, and controlled tails.
- Volatility Expansion requires compression, expansion potential, executable transition, and manageable slippage.
- Volatility Compression requires persistent contraction, containment, and expansion-failure response.
- Regime-Adaptive and Hybrid strategies require independent classifications, transition and uncertainty rules, and stronger evidence.

Fit is an implication for research, not a strategy verdict.

## 20. Regime Use in Market Discovery

MDRS uses regime clarity, stability, diversity, transition frequency, uncertainty, and family-fit implications when scoring research suitability. A high opportunity score cannot conceal insufficient regime evidence.

## 21. Regime Use in Strategy Architecture

Architecture declares applicable, excluded, uncertain, and transition regimes; information needs; classification dependencies; failure behavior; and scope consequences. The Architect cannot redefine labels to fit preferred logic.

## 22. Regime Use in Experiment Design

Experiments preregister taxonomy and record versions, classification timing, sampling, regime coverage, minimum representation, transition handling, uncertainty treatment, and comparisons. Post-result relabeling is exploratory and separately versioned.

## 23. Regime Use in Validation

Validation preserves the exact regime scope tested, assesses classification integrity and sample sufficiency, and prohibits generalization beyond evidenced labels. Conflicted or underrepresented regimes become limitations or rejection grounds.

## 24. Regime Use in Risk Review

Risk Governance defines permitted, restricted, prohibited, and uncertain regime conditions; exposure implications; transition risk; monitoring; kill conditions; and reassessment triggers. It cannot broaden validated regime scope.

## 25. Regime Use in Deployment Governance

DGS verifies that the deployed classifier, taxonomy, data, strategy, and authorized regime versions match the EDP and RRP. Operation outside scope triggers degradation, restriction, or suspension.

## 26. Regime Use in Monitoring and Edge Decay

MEDS monitors current distribution, confidence, persistence, transitions, mismatch, classification drift, volatility/liquidity changes, and deviations from Validation, Risk, Executive, and Deployment assumptions.

Regime mismatch is distinguished from mechanism failure, data failure, and classifier failure before edge conclusions are drawn.

## 27. Regime Evidence Packaging

Every material accepted, limited, challenged, transition, superseded, or invalidated classification produces a frozen evidence package containing identity, scope, taxonomy, data, methods rationale, supporting and conflicting evidence, alternatives, confidence, uncertainty, implications, limitations, prohibited interpretations, and custody.

## 28. Regime Audit and Reconstruction

An independent reviewer must reconstruct what label was known at each decision time, which data and taxonomy were used, why confidence was assigned, what alternatives existed, who consumed it, and how revisions affected downstream work.

Historical classifications are never rewritten with hindsight.

## 29. Integration with MACP

MACP governs classification requests, evidence transfer, preliminary labels, confidence review, acceptance, challenge, transition, supersession, invalidation, handoff, and archival. Messages cite exact record versions.

## 30. Integration with SMI

SMI holds current classification state, confidence, locks, open conflicts, transition status, consumers, and required actions. It cannot silently alter frozen evidence or historical labels.

## 31. Integration with EES

All classification inputs and outputs are EES objects with provenance, scope, confidence, uncertainty, contradictions, versions, admissibility, custody, and audit history.

## 32. Integration with WOE

WOE enforces evidence intake, classification, confidence review, acceptance, challenge, supersession, invalidation, handoff, and archival gates with eligible owners.

## 33. Integration with Agent Registry

Only registered agents may create, review, challenge, approve, or consume regime records within their rights. The Market Research Agent owns classification; downstream agents cannot silently relabel for convenience.

## 34. Integration with Artifact Registry

Taxonomy, classification, confidence, conflict, transition, challenge, handoff, supersession, invalidation, and archive records are governed artifacts with identity, version, lineage, provenance, consumers, retention, and audit history.

## 35. Integration with Strategy Lifecycle Standard

Every regime-dependent hypothesis, architecture, experiment, Validation, Risk, decision, deployment, and monitoring state cites exact regime records. Material regime-scope changes trigger lifecycle impact review.

## 36. Integration with Autonomous Research Pipeline

ARP uses RCS from Market Discovery through Monitoring and learning. No pipeline gate may rely on an unclassified or unversioned regime assumption.

## 37. Integration with Market Discovery & Ranking Standard

RCS supplies regime evidence, confidence, stability, uncertainty, transitions, and family-fit context to MDRS. MDRS ranks opportunities but cannot redefine RCS taxonomy or labels.

## 38. Integration with Monitoring and Edge Decay Standard

MEDS consumes accepted regime records as baselines and creates drift, mismatch, transition, and classifier-failure evidence. New monitoring evidence may challenge RCS through a governed workflow, never by silent mutation.

## 39. Governance

### 39.1 Mandatory rules

1. Exact market, instrument, timeframe, period, data, and taxonomy versions are mandatory.
2. Confidence, uncertainty, alternatives, and conflicts remain explicit.
3. Current regime is distinct from historical distribution; direction from quality; volatility level from usability; formation from breakout success; reversion pressure from tradability; liquidity from capacity; transition from noise.
4. No one-indicator or post-performance silent reclassification is permitted.
5. Unknown and uncertain states are valid.
6. Strategy fit remains conditional on evidence.
7. Validation scope, Risk limits, Deployment scope, and Monitoring drift requirements remain binding.
8. Frozen records cannot be edited in place; amendments preserve history.

### 39.2 Handoff requirements

Every handoff includes market/instrument/timeframe identity, data/version, observation period, label and alternatives, confidence, uncertainty, evidence and conflicts, transition, persistence, family fit, Validation/Risk/Deployment/Monitoring implications, limitations, prohibited interpretations, and follow-up.

### 39.3 Exceptions and change control

Exceptions are explicit, scoped, time-bounded, independently approved, and visible downstream. They cannot legalize missing evidence, hidden conflict, false certainty, silent relabeling, or operation outside authorized regime.

Changes to RCS require taxonomy and cross-system impact analysis, Market Research and governance review, versioning, migration rules, and preservation of prior classifications.

### 39.4 Institutional rule

Every future AI Quant Lab regime assumption, label, filter, experiment, Validation, Risk review, deployment, and drift-monitoring process must conform to this standard.
