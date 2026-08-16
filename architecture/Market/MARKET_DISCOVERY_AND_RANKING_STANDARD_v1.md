# Market Discovery & Ranking Standard (MDRS) v1.0

## Specification Control

| Field | Value |
|---|---|
| Standard ID | `AIQL-MDRS` |
| Version | `1.0.0` |
| Status | Proposed for Sprint 31 review |
| Scope | Every institutional market, instrument, timeframe, regime, and research-opportunity selection |
| Authority | Market Research Agent contract, Research OS, EES, WOE, ART, SLS, ARP, and institutional market-discovery governance |
| Provider dependency | None |

The Market Discovery & Ranking Standard defines how AI Quant Lab identifies and prioritizes research-worthy market contexts before hypothesis creation. It governs universe boundaries, eligibility, evidence, transparent scoring, strategy-family fit, ranking, rejection, deferral, custody, and handoff.

It is not a strategy, indicator system, optimizer, signal generator, or prediction engine. A ranking describes research suitability under declared evidence and assumptions; it does not establish edge or deployability.

## 1. Market Discovery Philosophy

Market discovery begins with behavior, constraints, and evidence rather than preferred indicators or historical profit. Its purpose is to allocate research attention toward contexts where mechanisms can be studied with adequate data, liquidity, execution realism, and falsifiability.

Opportunity is multidimensional. Trend quality without execution feasibility, volatility without liquidity, or novelty without reliable data cannot independently justify research priority.

Rankings are conditional and time-bound. Markets change, data improves, costs shift, and rejected candidates may become research-worthy under new evidence.

## 2. Market Discovery Principles

The following principles are binding:

1. No Discovery Without Defined Universe.
2. No Instrument or Timeframe Without Data Assessment.
3. No Opportunity Without Market Rationale.
4. No Ranking Without Transparent Criteria.
5. No Strategy Hypothesis From an Unranked Market.
6. No Selection From Performance, Popularity, Narrative, or Hype Alone.
7. No Indicator-First Selection.
8. Liquidity, Costs, Execution, Noise, Whipsaw, and Regimes Are Mandatory.
9. No Silent Universe Expansion or Ranking Change.
10. Rejected and Deferred Markets Remain Learnable.
11. Every Discovery Decision Must Be Auditable.

## 3. Market Discovery Identity Model

Every discovery program has a permanent Market Discovery ID, Market Discovery Record ID, and exact version. Identity binds the registered universe, observation period, scoring model version, evidence versions, owner, purpose, and intended ARP handoff.

Each market candidate resolves to asset class, venue, instrument, symbol or governed identity, contract type, timeframe, and applicable regime context. Material universe or scoring changes create a new record version and reranking event.

## 4. Market Discovery Object Model

The Market Discovery Record must define:

| Record group | Mandatory content |
|---|---|
| Identity | Discovery ID, record ID, owner, responsible agent |
| Universe | Asset class, venue, instrument, symbol, contract type, timeframe |
| Observation | Period, data source/version, coverage, and data quality status |
| Feasibility | Liquidity, capacity, execution, spread, slippage, and cost status |
| Behavior | Volatility, trend quality, regime structure, efficiency, persistence, range behavior |
| Friction | Noise, whipsaw, false breakouts, tails, gaps, and operational constraints |
| Fit | Strategy-family fit with supporting and opposing evidence |
| Scoring | Component scores, penalties, overall score, rank, rationale, uncertainty |
| Disposition | Candidate, rejection, deferral, supersession, limitations, risks, contradictions, follow-up |
| Integrations | Source MACP and related SMI, EES, ART, WOE, and Agent records |
| History | Created At, Updated At, versions, and immutable Audit Trail |

Missing mandatory dimensions prevent final ranking unless explicitly inapplicable and justified.

## 5. Market Discovery Lifecycle

**Proposed → Universe Registered → Data Intake → Eligibility Review → Market Assessment → Opportunity Scoring → Ranked → Research Candidate → Rejected → Deferred → Superseded → Archived**

Eligibility failure may move directly to Rejected or Deferred with recorded reason. Ranked candidates require a separate disposition decision; ranking alone does not create ARP eligibility.

Supersession preserves the earlier universe, scores, evidence, rationale, and downstream use.

## 6. Universe Definition Rules

The universe record defines institutional purpose, included and excluded asset classes, venues, instruments, contract types, timeframes, currencies, observation periods, data requirements, liquidity floor, operational constraints, and review frequency.

Mandatory supported asset classes are Crypto, Forex, Metals, Commodities, Indices, Equities, Rates, Volatility Products, Portfolio Baskets, and Synthetic or Derived Markets. Inclusion does not imply eligibility.

Universe expansion requires rationale, evidence availability, governance approval, versioning, and full affected assessment. Survivorship and selection bias must be addressed.

## 7. Instrument Eligibility Rules

Eligibility requires stable identity, sufficient historical and current data, interpretable market mechanics, adequate liquidity for the research objective, observable costs, executable access assumptions, and no unresolved integrity defect.

Contract roll, corporate action, funding, session, venue, price construction, and symbol-history effects must be documented where material.

Instruments may be Eligible, Eligible With Limitations, Deferred, or Rejected. Eligibility means assessable, not attractive.

## 8. Timeframe Eligibility Rules

Mandatory classes are Intraday Low, Intraday Medium, Intraday High, Swing, Position, Daily, Multi-Day, and Weekly. Example intervals include 1m, 3m, 5m, 15m, 30m, 1H, 2H, 3H, 4H, 6H, 8H, 12H, 1D, and 1W.

Each timeframe is assessed independently for sample sufficiency, data construction, microstructure noise, costs, signal opportunity, execution timing, regime representation, and operational feasibility. Evidence cannot be assumed transferable between intervals.

## 9. Data Availability and Quality Rules

Assessment covers provenance, source authority, version, coverage, continuity, freshness, missingness, duplicates, ordering, timestamps, calendars, adjustments, revisions, outliers, survivorship, transformations, and access continuity.

Data Quality Score must separate completeness, correctness, temporal integrity, representativeness, and reproducibility. Insufficient data blocks opportunity scoring rather than receiving a neutral score.

## 10. Liquidity and Capacity Assessment

Assessment considers volume, depth where evidenced, spread, turnover, participation constraints, position liquidation, stressed liquidity, concentration, venue fragmentation, market impact, and scale sensitivity.

Capacity is conditional on timeframe, execution assumptions, capital, order behavior, and market state. Reported volume alone is insufficient. Unknown liquidity creates an explicit penalty or exclusion.

## 11. Volatility and Range Assessment

The record describes realized movement, range distribution, ATR structure, clustering, expansion, contraction, gaps, tails, asymmetry, stability, and relationship to costs.

Volatility is assessed for usability, not maximization. Excessively low movement may not cover costs; extreme movement may make execution or loss control unreliable.

## 12. Trend Quality Assessment

Trend Quality examines directional persistence, path efficiency, duration, smoothness, separation from noise, participation, retracement structure, breakout follow-through, regime stability, and false-transition frequency.

Measurements may estimate these properties but no indicator creates trend quality. The assessment reports uncertainty and opposing evidence.

## 13. Regime Structure Assessment

The record identifies observed trend, range, high/low volatility, breakout, mean-reversion, transition, liquidity-event, and uncertain states as applicable.

It assesses clarity, stability, duration, transition frequency, classification uncertainty, imbalance, and whether samples cover materially different conditions. Strategy-family fit is conditioned on regimes rather than averaged across them blindly.

## 14. Noise, Whipsaw, and False Breakout Assessment

Noise assessment covers short-horizon reversal, path inefficiency, signal instability, microstructure effects, and movement relative to costs. Whipsaw density measures repeated directional invalidation; false-breakout assessment examines rejection after apparent structural escape.

Definitions, windows, and market context must be declared. Penalties cannot be removed merely because they lower a preferred candidate’s rank.

## 15. Market Efficiency and Directional Persistence Assessment

The record evaluates serial dependence, autocorrelation, variance behavior, price efficiency, return persistence, reversion, asymmetry, session effects, and stability through time and regimes.

Statistical dependence does not by itself imply tradable edge. Effect size, uncertainty, costs, robustness, and plausible mechanism must remain separate.

## 16. Cost and Execution Feasibility Assessment

Assessment includes spread, slippage sensitivity, fees, funding, borrowing, gaps, latency sensitivity, fills, partial fills, minimum increments, session access, venue continuity, and exit feasibility.

Cost Feasibility compares plausible movement and opportunity frequency with conservative total friction. Execution Feasibility assesses whether research assumptions could eventually be represented operationally without claiming readiness.

## 17. Strategy-Family Fit Assessment

Fit is behavioral compatibility, not strategy selection or approval:

- Trend Following requires persistence, quality, usable volatility, acceptable whipsaw, and manageable cost.
- Breakout requires structure, compression, follow-through, controlled false breaks, and liquidity.
- Momentum requires return persistence, participation, usable volatility, and controlled tails.
- Pullback Continuation requires trend structure, recurrent retracement, continuation evidence, and defensible invalidation.
- Mean Reversion requires bounded behavior, overshoot and reversion evidence, liquidity, controlled tails, and clear failure conditions.
- Volatility Expansion requires compression-to-expansion behavior, executable transition, and manageable slippage.
- Volatility Compression requires persistent contraction and a defined expansion-risk context.
- Hybrid requires separately observable mechanisms and stronger evidence.

Fit records supporting, weakening, and missing evidence for each applicable family.

## 18. Opportunity Scoring Model

The model must assess Data Quality, Liquidity, Execution Feasibility, Cost Feasibility, Volatility Usability, Trend Quality, Directional Persistence, Regime Clarity, Regime Stability, Breakout Persistence, Research Novelty, Cross-Market Transferability, and Operational Feasibility.

Explicit penalties cover false breakouts, whipsaw, noise, tails, spread, slippage, capacity, uncertainty, missing evidence, and instability.

Outputs are Market Suitability, Trend, Breakout, Mean Reversion, Momentum, Pullback, Volatility Expansion, Volatility Compression, Execution Feasibility, Research Priority, and Overall Market Discovery scores.

Scores must expose definitions, component evidence, weights or decision importance, penalties, uncertainty, missingness treatment, and model version. A single total score cannot conceal a critical eligibility failure.

## 19. Ranking and Prioritization Rules

Candidates are ranked within comparable scope and declared objective. Ties, uncertainty, missing evidence, hard exclusions, portfolio duplication, novelty, research cost, and expected information gain are handled explicitly.

Priority must consider both suitability and learning value. Rankings include rationale, confidence, sensitivity to scoring assumptions, and the conditions under which order could change.

Ranking changes require new evidence or governed scoring revision, versioning, and impact analysis for active handoffs.

## 20. Rejection and Exclusion Rules

Rejection grounds include inadequate data, unreliable identity, insufficient liquidity, prohibitive cost, infeasible execution, excessive noise or tails, unavailable regime coverage, unresolved integrity issue, or lack of research rationale.

Deferral applies when a candidate may become eligible after more data, clarification, access, or changed conditions. Exclusion identifies scope decisions rather than candidate defects.

Every disposition preserves evidence, reason, owner, reconsideration condition, required follow-up, and expiry. Low score is not permanent rejection.

## 21. Market Opportunity Record

Every Research Candidate receives a frozen Market Opportunity Record containing market, instrument, venue, timeframe, data/version, observation period, behavior summary, component and overall scores, rank rationale, strategy-family fit, regimes, liquidity, execution, costs, noise, whipsaw, false-breakout, tail and gap risks, limitations, contradictions, suggested questions, hypothesis directions, prohibited interpretations, and follow-up.

The record explicitly states that opportunity is not edge, strategy approval, validation, or deployability.

## 22. Research Handoff Requirements

ARP handoff requires a current Market Opportunity Record, eligible status, exact evidence and artifact versions, research rationale, suggested questions, known gaps, assigned consumer, acknowledgement, expiry, and conditions for return.

The handoff may suggest hypothesis directions but cannot define entry, exit, position sizing, or implementation logic. The Quant Strategy Architect independently forms the hypothesis.

## 23. Integration with MACP

MACP governs universe registration, data intake, assessment requests, score publication, ranking changes, rejection, deferral, candidate nomination, handoff, return, supersession, and archival. Messages cite exact discovery, scoring, evidence, artifact, and agent versions.

## 24. Integration with SMI

SMI holds current universe, candidates, assessment state, dependencies, locks, rank version, blockers, and handoff acknowledgement. It cannot silently alter frozen scores, evidence, or disposition.

## 25. Integration with EES

Every component assessment, score, penalty, contradiction, limitation, and ranking rationale cites EES objects with provenance, scope, uncertainty, version, custody, and admissibility.

## 26. Integration with WOE

WOE enforces universe, data, eligibility, assessment, scoring, ranking, disposition, handoff, return, supersession, and archival gates. Ineligible agents or missing outputs block transition.

## 27. Integration with Agent Registry

The Market Research Agent owns objective assessment and ranking within registered rights. Research Librarian and Knowledge Curator support sources and institutional knowledge. No agent may convert ranking into strategy or approval authority.

## 28. Integration with Artifact Registry

Universe, data-quality, eligibility, assessment, score, ranking, rejection, deferral, opportunity, handoff, supersession, and archive records are governed ART artifacts with identity, owner, lineage, provenance, status, consumers, retention, and audit history.

## 29. Integration with Strategy Lifecycle Standard

MDRS operates before hypothesis creation. A Market Opportunity Record supports `Proposed` and `Researching` states but cannot advance a strategy beyond research or transfer approval between strategy versions.

## 30. Integration with Autonomous Research Pipeline

MDRS governs ARP Market Discovery and its handoff to Research Question Formation. ARP cannot accept an unranked market, absent opportunity record, stale scoring version, or unresolved hard eligibility failure.

Returns from later stages may trigger reassessment without silently rewriting earlier rankings.

## 31. Governance

### 31.1 Mandatory dimensions

Every assessment covers asset class, instrument, venue, timeframe, data, liquidity, spread, slippage, volatility, ATR structure, trend and directional persistence, range and regimes, breakout persistence, false breakouts, whipsaw, noise, autocorrelation, asymmetry, tails, sessions, execution, cost, capacity, and strategy-family fit.

### 31.2 Mandatory rules

1. Discovery precedes hypothesis creation and cannot define trading logic.
2. Data, liquidity, execution, costs, regimes, noise, whipsaw, and false breaks precede recommendation.
3. Market opportunity remains distinct from strategy edge and deployability.
4. Ranking criteria are transparent, versioned, and never silently changed.
5. Rejected and deferred candidates, limitations, and contradictions are preserved.
6. A high score is not validation; a low score is not permanent rejection.
7. Every ARP handoff requires a frozen Market Opportunity Record.

### 31.3 Exceptions and change control

Exceptions are scoped, time-bounded, justified, independently approved, and visible in scoring and handoff. They cannot legalize missing identity, missing data assessment, hidden costs, silent universe expansion, or unranked progression.

Changes to MDRS require impact analysis, Market Research and governance review, versioning, migration instructions, reranking policy, and preservation of prior versions.

### 31.4 Institutional rule

Every future AI Quant Lab market selection, timeframe selection, instrument ranking, and research-candidate handoff must conform to this standard before entering hypothesis creation in ARP.
