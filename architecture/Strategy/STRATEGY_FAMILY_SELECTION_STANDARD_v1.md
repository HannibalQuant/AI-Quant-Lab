# Strategy Family Selection Standard (SFSS) v1.0

## Specification Control

| Field | Value |
|---|---|
| Standard ID | `AIQL-SFSS` |
| Version | `1.0.0` |
| Status | Proposed for Sprint 35 review |
| Scope | Every edge-to-strategy-family decision and architecture handoff |
| Authority | EDS, MDRS, RCS, FFS, ARP, SLS, EES, ART, and strategy governance |

SFSS governs selection, comparison, challenge, rejection, versioning, and handoff of the strategy family best aligned with a governed edge candidate. It is not a strategy, architecture, implementation, optimizer, or signal generator. Family selection constrains the design question; it does not answer it.

## 1. Strategy Family Selection Philosophy

Family follows mechanism. Selection begins with observed behavior, edge rationale, conditions, and failure modes, then asks which family offers the most faithful and parsimonious research representation.

The strongest selection explains both why one family fits and why credible alternatives fit less well. Historical profit cannot substitute for behavioral compatibility.

## 2. Strategy Family Selection Principles

No selection proceeds without frozen EDS, market, regime, feature, mechanism, execution, cost, risk, failure-mode, alternative-family, uncertainty, and audit review. Backtests, optimization, indicator preference, and popularity alone are inadmissible. Hybrid components require separate evidence; adaptive families require governed regimes. No silent family or scope change is permitted.

## 3. Strategy Family Identity Model

Every decision has permanent Selection ID, Record ID, and exact version. Identity binds edge, MDRS, RCS, FFS, Strategy ID, market, timeframe, data, selected family, candidates, and owner. Material edge, scope, mechanism, or family change requires a new decision or governed version.

## 4. Strategy Family Object Model

The record defines identity and owner; all source record versions; strategy and lifecycle state; market, venue, instrument, timeframe, period, data; selected, candidate, and rejected families; edge mapping; market, regime, feature, mechanism, execution, cost, risk, and failure fit; alternatives; limitations, contradictions, required/excluded conditions; confidence, maturity, handoff, deferral, rejection, follow-up; MACP, SMI, EES, ART, WOE, Agent references; timestamps and immutable audit trail.

## 5. Strategy Family Selection Lifecycle

**Proposed → Edge Context Received → Candidate Families Identified → Family Fit Assessed → Family Compared → Family Challenged → Family Selected → Selected With Limitations → Architecture Handoff Candidate → Deferred → Rejected → Superseded → Archived**

No state implies strategy approval. Challenge preserves the frozen decision; supersession preserves downstream history.

## 6. Strategy Family Taxonomy

Mandatory families are Trend Following, Breakout Continuation, Breakout Failure, Momentum, Pullback Continuation, Mean Reversion, Volatility Expansion, Volatility Compression, Range Rotation, Liquidity-Based, Session-Based, Relative Strength, Cross-Market, Portfolio Diversification, Regime-Adaptive, and Hybrid.

Taxonomy changes require definitions, migration, compatibility analysis, and preserved versions.

## 7. Edge-to-Family Mapping Rules

Mapping cites exact EDS behavior, mechanism, conditions, strength, confidence, maturity, contradictions, and prohibited interpretations. It states which property of the family represents the mechanism and which edge claims remain outside family scope.

## 8. Market Context Fit Rules

Fit evaluates MDRS data, liquidity, volatility, trend/range structure, noise, whipsaw, false breaks, tails, capacity, timeframe, costs, and operational feasibility. Research priority is not family proof.

## 9. Regime Fit Rules

Selection cites exact RCS labels, versions, confidence, uncertainty, transitions, applicable and excluded regimes. It cannot average incompatible regimes or relabel after performance observation.

## 10. Feature Fit Rules

Every required feature maps to an information need and cites exact FFS version, scope, lineage, timing, leakage, redundancy, stability, and limitations. Feature availability cannot create mechanism fit.

## 11. Mechanism Fit Rules

The family must preserve the expected behavioral, structural, liquidity, volatility, risk-transfer, participant, session, or cross-market mechanism. A family that needs a different mechanism is rejected or treated as a separate hypothesis.

## 12. Execution and Cost Fit Rules

Review covers spread, slippage, fees, latency, fills, turnover, gaps, liquidity, capacity, funding, borrowing, and exit feasibility. Unknown material friction limits confidence or defers selection.

## 13. Risk and Failure-Mode Fit Rules

Review identifies tails, drawdown shape, concentration, leverage, liquidity, capacity, regime failure, structural breaks, execution failure, data dependency, operational fragility, and monitorability. Selection does not accept risk.

## 14. Trend Following Family Requirements

Requires directional persistence, trend quality, suitable regime, path efficiency, tolerable whipsaw, usable volatility, and cost feasibility.

## 15. Breakout Family Requirements

Requires boundary or compression, pressure, acceptance, follow-through, liquidity, executable transition, and explicit false-break control.

## 16. Momentum Family Requirements

Requires return persistence, continuation behavior, participation, usable volatility, and bounded reversal and tail sensitivity.

## 17. Pullback Continuation Family Requirements

Requires established trend, recurrent retracement, continuation response, defensible invalidation context, and execution feasibility.

## 18. Mean Reversion Family Requirements

Requires bounded structure, displacement, restoration evidence, liquidity, controlled tails, and explicit structural-break failure.

## 19. Volatility Expansion Family Requirements

Requires compression or transition context, expansion tendency, executable movement, cost tolerance, and manageable slippage.

## 20. Volatility Compression Family Requirements

Requires persistent contraction, stable containment, meaningful low-movement state, and defined expansion-failure response.

## 21. Range Rotation Family Requirements

Requires stable boundaries, recurrent response and traversal, liquidity, and governed structural-break risk.

## 22. Liquidity-Based Family Requirements

Requires observable liquidity change or imbalance, executable effect, source reliability, capacity bounds, and stressed behavior.

## 23. Session-Based Family Requirements

Requires stable session-specific behavior, correct calendars and alignment, cost feasibility, and robustness to timing artifacts.

## 24. Relative Strength Family Requirements

Requires cross-sectional or pairwise persistence, ranking stability, common-factor controls, universe integrity, and rebalance feasibility.

## 25. Cross-Market Family Requirements

Requires source-target mechanism, lag or transmission rationale, stability, regime dependency, causality caution, and structural-change failure conditions.

## 26. Portfolio Diversification Family Requirements

Requires beneficial return and drawdown interaction, crisis evidence, tail dependence, capacity, and integration-risk assessment. Low average correlation alone is insufficient.

## 27. Hybrid Family Requirements

Each component requires separate edge, mechanism, features, regimes, contribution, failure modes, and controls. Interaction and redundancy require stronger experiments and Validation.

## 28. Regime-Adaptive Family Requirements

Requires independent RCS records, transition handling, uncertain-state behavior, switching rationale, classification error analysis, and stronger out-of-sample Validation.

## 29. Family Comparison and Ranking Rules

At least one credible alternative is compared unless none is defensible and the reason is recorded. Comparison covers mechanism fidelity, scope, information needs, complexity, execution, costs, risk, failure, experiments, Validation, and monitoring—not historical performance alone.

## 30. Family Rejection and Exclusion Rules

Poor-fit families are recorded with evidence and reasons: mechanism mismatch, regime incompatibility, missing information, prohibitive cost, execution infeasibility, excessive risk, redundancy, or unjustified complexity. Exclusion is scoped and reconsiderable.

## 31. Family Selection Confidence Model

Authorized confidence states are `HIGH`, `MEDIUM`, `LOW`, `INSUFFICIENT`, and `CONFLICTED`. Confidence reflects source integrity, edge maturity, fit consistency, alternatives, contradictions, and unknowns.

## 32. Family Selection Maturity Model

Authorized maturity states are `PROPOSED`, `COMPARISON_READY`, `SELECTED_FOR_ARCHITECTURE`, `SELECTED_WITH_LIMITATIONS`, `DEFERRED`, `REJECTED`, and `SUPERSEDED`.

## 33. Strategy Architecture Handoff Requirements

Handoff contains selection identity/version; frozen EDS; market, regime, and feature context; selected and rejected families; rationale and comparison; conditions and exclusions; information needs; expected modules and failures; risk, execution, cost, monitoring implications; limitations, prohibited interpretations, experiments, follow-up, and acknowledgement.

It cannot define entries, exits, sizing, parameters, or implementation.

## 34. Family Selection Evidence Packaging

Every selected, limited, challenged, deferred, rejected, or superseded decision has a frozen EES package with identities, evidence, comparison, classifications, contradictions, limitations, custody, and consumer history.

## 35. Family Selection Audit and Reconstruction

Independent reviewers must reconstruct what edge and alternatives were known, why the family fit, what was rejected, who decided, and whether Architecture preserved the handoff. Hindsight rewriting is prohibited.

## 36. Integration with MACP

MACP governs intake, candidates, assessments, comparison, challenge, selection, handoff, deferral, rejection, supersession, and archival with exact versions.

## 37. Integration with SMI

SMI holds current state, owner, locks, candidates, blockers, classification, and handoff. It cannot silently mutate frozen decisions.

## 38. Integration with EES

All fit claims and decisions use EES objects with provenance, scope, uncertainty, contradictions, versions, custody, and admissibility.

## 39. Integration with WOE

WOE enforces intake, assessment, comparison, challenge, selection, handoff, return, rejection, and archival gates.

## 40. Integration with Agent Registry

The registered Quant Strategy Architect owns selection proposals within contract and never self-approves downstream Validation, Risk, or Deployment.

## 41. Integration with Artifact Registry

Candidate, comparison, challenge, selection, handoff, rejection, deferral, supersession, and archive records are governed ART artifacts.

## 42. Integration with Strategy Lifecycle Standard

SFSS occurs after Edge Discovery and before full Architecture. Material family change returns SLS to the required state and invalidates incompatible downstream artifacts.

## 43. Integration with Autonomous Research Pipeline

ARP routes the frozen edge into SFSS and accepts only a governed Architecture Handoff Candidate. It cannot silently substitute a family.

## 44. Integration with Market Discovery & Ranking Standard

MDRS provides scoped market opportunity evidence; family fit cannot exceed its eligible market, timeframe, data, and execution context.

## 45. Integration with Regime Classification Standard

RCS provides labels, confidence, uncertainty, transitions, and conflicts. Adaptive selection requires stronger governed regime evidence.

## 46. Integration with Feature Factory Standard

FFS supplies governed measurements. SFSS maps information needs but cannot redefine feature semantics or ignore redundancy and leakage.

## 47. Integration with Edge Discovery Standard

Only a frozen, sufficiently mature EDS record enters selection. Family choice cannot broaden edge mechanism, regime, or evidence scope.

## 48. Integration with Experiment Evidence Package

SFSS specifies required family-comparison and mechanism experiments; EEP later packages results without retroactively changing selection rationale.

## 49. Integration with Validation Evidence Package

VEP independently assesses later evidence. Selection confidence does not bind Validation and is not scientific approval.

## 50. Integration with Risk Review Package

RRP consumes family failure, execution, cost, capacity, tail, and monitoring implications but cannot treat family selection as risk approval.

## 51. Integration with Monitoring and Edge Decay Standard

MEDS observes the selected family’s mechanism, regime dependencies, expected failure modes, and decay indicators. Monitoring may challenge selection through a governed return path.

## 52. Governance

Mandatory review dimensions are market behavior, edge mechanism, regimes, features, information needs, execution, costs, liquidity, volatility, noise, whipsaw, tails, capacity, timeframe, data, operations, risk controls, monitoring, Validation feasibility, alternatives, and contradictions.

Selection distinguishes edge, family, architecture, implementation, performance, Validation, Risk, and authority. A selected family is none of the latter. Frozen records cannot be edited in place; amendments create versions and preserve rejected alternatives.

Exceptions are scoped, time-bounded, independently approved, and cannot legalize absent EDS, no alternative comparison, indicator preference, performance-only choice, or silent scope change. Every future family choice and family-to-architecture handoff must conform to SFSS.
