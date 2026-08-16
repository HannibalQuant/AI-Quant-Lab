# AI QUANT LAB — Data Quality Standard v1.0

**Document Class:** Constitutional Standard  
**Authority:** AI Quant Lab Data and Evidence Governance  
**Status:** v1.0  
**Applies To:** Every dataset and data-dependent institutional claim, artifact, workflow, decision, deployment, and monitoring state

## 1. Data Quality Philosophy

Data is admissible institutional input only when its identity, origin, transformations, temporal availability, defects, revisions, and limitations are known. Clean appearance is not quality. Quality is fitness for a declared purpose under reconstructable custody, and no favorable result may cure defective data.

## 2. Data Quality Principles

No research without data identity; no use without source lineage, version, symbol, timestamp, timezone, completeness, duplicate, gap, anomaly, session, and calendar review. No feature, experiment, robustness, Validation, deployment, or monitoring reliance precedes eligibility. Repairs, revisions, symbol changes, conversions, exclusions, and resampling are never silent. Data quality is neither Validation nor proof of edge.

## 3. Data Identity Model

Every dataset receives immutable Dataset ID, Data Quality ID, record version, canonical scope, source identity, observation interval, fields, granularity, and integrity reference. Derived datasets retain parent identities. Replacement, revision, remediation, or changed scope creates a new version; identity survives rejection and archive.

## 4. Data Quality Object Model

The record shall define owner and responsible agent; dataset/source/vendor/provider/license; universe, asset, venue, exchange or broker, instrument, canonical and vendor symbols; timeframe, granularity, period, timestamps, timezone, calendar, sessions and hours; fields and bases; raw/processed references and integrity reference; ingestion identity and time; preprocessing, transformations, resampling, adjustments and revisions; defect summaries, metrics, reconciliation, limitations, contradictions, eligibility, confidence, maturity, quarantine, remediation, excluded segments, follow-up, MACP source, SMI/EES/artifact/workflow/agent links, timestamps, and audit trail.

## 5. Data Quality Lifecycle

**Proposed → Source Registered → Dataset Ingested → Identity Reviewed → Lineage Reviewed → Temporal Integrity Reviewed → Structural Integrity Reviewed → Market Integrity Reviewed → Anomaly Review Completed → Preprocessing Review Completed → Cross-Source Review Completed → Eligibility Classified → Evidence Packaged → Quarantined → Remediated → Rejected → Challenged → Superseded → Archived**

Each transition records authority, owner, prior state, evidence, rationale, conditions, outputs, and time. Remediation never overwrites the original state.

## 6. Data Source Lineage Rules

Lineage identifies originator, vendor, acquisition route, license or access constraints, extraction time, source methodology, field definitions, revision practices, custody transfers, and every derived parent. Unknown or discontinuous lineage prohibits institutional reliance.

## 7. Dataset Versioning Rules

A version binds exact content, schema meaning, source release, scope, field basis, adjustments, preprocessing, exclusions, and integrity reference. Any material data, mapping, correction, transformation, or definition change creates a new version and downstream impact review.

## 8. Symbol and Instrument Integrity Rules

Canonical identity shall resolve vendor symbols, venue, contract type, currency and quote, multiplier, tick, lot, expiry, listing changes, redenominations, forks, mergers, and aliases where applicable. Unresolved collisions or silent symbol reuse require quarantine.

## 9. Timestamp Integrity Rules

Timestamps must be monotonic, unique where required, correctly typed, bounded, and tied to event meaning such as open, close, trade, quote, receipt, or publication. Clock drift, latency, revisions, and decision-time availability are disclosed.

## 10. Timezone and Calendar Rules

The record declares source timezone, canonical timezone, conversion, daylight-saving treatment, exchange calendar, weekends, holidays, shortened sessions, and exceptional closures. Conversion is deterministic, versioned, and never inferred silently.

## 11. Session Integrity Rules

Bars and events are reconciled to authorized trading sessions and session boundaries. Overnight behavior, auctions, maintenance, halts, pre/post-market, 24/7 markets, and synthetic sessions are separately identified when material.

## 12. OHLC Integrity Rules

Open, high, low, and close must be present when required; high must not be below open, low, or close; low must not exceed them; values must respect valid price domains. Impossible candles, extreme ranges, zero or negative events, basis (trade, bid, ask, midpoint), construction, and adjustments are recorded and reproducible.

## 13. Volume and Liquidity Integrity Rules

Volume identity distinguishes traded, quote, tick, venue, aggregate, estimated, and unavailable measures. Units, aggregation, wash or anomalous activity, missingness, depth or liquidity proxies, venue dependence, and capacity relevance are disclosed; volume fields are never assumed comparable by name alone.

## 14. Spread and Cost Data Rules

Bid/ask basis, spread sampling, commissions, fees, rebates, funding, borrow, rollover, taxes, impact proxies, and effective dates must match market and purpose. Estimated, historical, live, and stressed costs remain distinct with uncertainty and coverage stated.

## 15. Missing Data Rules

Missing fields, events, bars, segments, and expected intervals are quantified by location, duration, regime, session, and field. Absence is distinguished from zero and market closure. Filling requires rationale, method, version, uncertainty, and downstream sensitivity analysis.

## 16. Duplicate Data Rules

Duplicate timestamps, events, identifiers, bars, revisions, and overlapping vendor deliveries are detected. Resolution declares authoritative record, ordering, aggregation or exclusion rule, and effect. Deduplication cannot erase materially conflicting observations.

## 17. Gap Detection Rules

Expected continuity is derived from market calendar, session, instrument state, and granularity. Each gap is classified as closure, halt, source outage, illiquidity, missing delivery, listing boundary, rollover, or unresolved and assessed for research and execution impact.

## 18. Outlier and Spike Rules

Outliers are visible evidence until classified as genuine market events, source defects, unit or mapping errors, corporate actions, rollovers, or unresolved anomalies. Statistical rarity alone does not authorize removal; every correction or exclusion preserves the original.

## 19. Flatline and Stale Data Rules

Repeated values, frozen quotes, zero range, unchanged volume, delayed updates, and stale timestamps are measured against expected market behavior. Genuine inactivity is distinguished from feed failure; decision-affecting staleness blocks applicable use.

## 20. Data Revision Rules

Source and institutional revisions receive release time, reason, changed fields, affected periods, prior and new integrity references, and consumer impact. Revised data may not masquerade as information historically available at a decision point.

## 21. Preprocessing Integrity Rules

Every transformation declares identity, order, parameters, fit period, application period, rolling behavior, missing-data policy, normalization, scaling, smoothing, imputation, winsorization, filtering, adjustment, exclusions, leakage risk, and reproducibility material. Raw lineage remains immutable.

## 22. Resampling and Aggregation Rules

Resampling declares source granularity, target timeframe, timestamp label, interval closure, boundaries, session treatment, timezone, partial bars, OHLCV aggregation, missing intervals, and revision behavior. A change to any rule creates a new dataset version.

## 23. Feature Input Data Rules

FFS features may consume only scope-eligible inputs whose field meaning, temporal availability, missingness, revision status, and preprocessing lineage are explicit. Feature output inherits input limitations and the weakest material eligibility constraint.

## 24. Corporate Action Rules

Splits, reverse splits, dividends, distributions, rights, mergers, spinoffs, symbol changes, delistings, and adjustments are identified with effective and knowledge times. Raw and adjusted series remain distinguishable; adjustment methodology and backtest implications are stated.

## 25. Futures Rollover Rules

Contracts, expiries, first notice, settlement, roll dates, price basis, adjustment, splice, weighting, liquidity transfer, and gap treatment are governed. Continuous series cannot conceal non-tradable synthetic prices or future-informed roll choices.

## 26. Crypto Exchange Data Rules

Exchange, spot or derivative type, pair, contract unit, inverse/linear basis, funding, index/mark/trade price, maintenance, outages, forks, redenominations, 24/7 boundaries, wash risk, venue fragmentation, and delistings are explicit. One venue cannot silently represent the market.

## 27. Forex and CFD Data Rules

Provider, bid/ask/mid basis, decentralized venue scope, session convention, weekend boundary, daylight saving, rollover, synthetic volume, broker-specific pricing, contract specification, and financing are explicit. Provider feeds are not presumed interchangeable.

## 28. Equity and Index Data Rules

Listings, exchanges, corporate actions, survivorship, constituents, reconstitutions, dividends, auctions, halts, delistings, total-return versus price basis, and point-in-time universe are governed. An index series is not automatically an executable instrument series.

## 29. Commodity and Metals Data Rules

Spot, fixing, futures, forward, CFD, and synthetic identities remain distinct. Contract grade, location, currency, session, rollover, seasonality, delivery constraints, benchmark revisions, and source basis are disclosed.

## 30. Cross-Source Reconciliation Rules

Comparison declares source, period, mapping, timestamp/timezone, price/volume/spread/adjustment bases, sampling, tolerance, disagreements, materiality, and source-of-truth decision. Agreement supports confidence but does not erase shared-source or shared-method dependence.

## 31. Data Quality Metric Rules

Metrics cover source reliability, lineage completeness, version, symbol, temporal, timezone, calendar, session, OHLC, volume, liquidity, spread, cost, completeness, continuity, duplicates, anomalies, preprocessing, revisions, cross-source agreement, market-structure correctness, execution relevance, and auditability. Metrics retain denominators, scope, uncertainty, and threshold version.

## 32. Data Quality Threshold Rules

Warning, limitation, quarantine, rejection, and invalidity thresholds are declared before downstream results, by field, market, timeframe, purpose, and severity. Threshold changes are versioned and cannot retroactively rescue favorable evidence.

## 33. Data Quality Failure Rules

Unknown source, absent version, unresolved symbol/timezone, non-monotonic or duplicate time, excessive missingness, unexplained gaps, impossible OHLC, material anomalies or staleness, invalid volume/spread/cost, calendar/session conflict, leakage, look-ahead adjustment, untracked revision, undocumented resampling, material source contradiction, undisclosed survivorship, live/backtest mismatch, irreproducibility, or broken lineage causes downgrade, quarantine, rejection, or invalidity according to materiality.

## 34. Data Eligibility Classification Model

Permitted classifications are **ELIGIBLE**, **ELIGIBLE WITH LIMITATIONS**, **RESEARCH ONLY**, **QUARANTINED**, **REJECTED**, and **INVALID**. Classification states exact scope, purpose, fields, periods, exclusions, conditions, expiry, prohibited uses, and rationale. Eligibility for research does not imply eligibility for Validation, deployment, or live monitoring.

## 35. Data Quality Confidence Model

Confidence is **HIGH**, **MEDIUM**, **LOW**, **INSUFFICIENT**, or **CONFLICTED**, based on lineage completeness, source reliability, checks, reconciliation, custody, reproducibility, uncertainty, and contradiction—not downstream performance.

## 36. Data Quality Maturity Model

Maturity is **REGISTERED**, **REVIEWED**, **EVIDENCE_READY**, **VALIDATION_CANDIDATE**, **DEPLOYMENT_CANDIDATE**, **MONITORING_READY**, **RETURNED**, **REJECTED**, or **SUPERSEDED**. It expresses review readiness, never scientific or commercial merit.

## 37. Data Quarantine and Remediation Rules

Quarantine blocks declared consumers and preserves the exact affected version, scope, cause, severity, owner, evidence, and release criteria. Remediation creates a derived version with methods, approvals, validation checks, residual limitations, and impact analysis; the quarantined source remains reconstructable.

## 38. Deviation and Amendment Rules

Deviations identify rule, event, timing, authority, rationale, affected fields/periods/consumers, risk, temporary controls, expiry, and remediation. Amendments are prospective, versioned, and never overwrite frozen records or retroactively legitimize prior reliance.

## 39. Data Quality Evidence Packaging

The frozen package includes identities and versions; source/vendor lineage and access conditions; full market/instrument/symbol/timeframe/period/timezone/calendar scope; raw and processed integrity references; ingestion, preprocessing, transformation, resampling, adjustment and revision histories; metric and defect summaries; cross-source comparison; eligibility, confidence, maturity, quarantine/remediation, limitations, contradictions, exclusions, prohibited interpretations, and follow-up.

## 40. Data Quality Audit and Reconstruction

An independent reviewer must reproduce dataset identity, lineage, acquisition state, field meaning, temporal availability, checks, transformations, exclusions, repairs, revisions, classification, and every consumer decision without chat history or private memory. Audit preserves custody, authorship, versions, timestamps, integrity references, transitions, challenges, and supersession.

## 41. Integration with MACP

MACP transports identity-bound registration, defect, quarantine, remediation, challenge, eligibility, revision, handoff, and revocation messages. Each cites exact dataset and record versions, scope, severity, authority, conditions, and evidence; messages do not replace records.

## 42. Integration with SMI

SMI holds governed current eligibility, source and version references, limitations, open defects, quarantine, revisions, consumers, and expiry. Conflicting memory state blocks WOE progression until reconciled.

## 43. Integration with EES

EES governs provenance, admissibility, uncertainty, contradictions, chain of custody, freezing, transfer, challenge, consumer traceability, and expiry. Limitations and adverse quality evidence travel with every dependent package.

## 44. Integration with WOE

WOE enforces owners, dependencies, stage gates, eligibility, quarantine, remediation, return, rejection, escalation, and re-entry. Missing identity, lineage, temporal integrity, or applicable eligibility is a hard workflow block.

## 45. Integration with Agent Registry

Only registered agents with explicit data-review, evidence, message, memory, and workflow rights may classify, remediate, challenge, or release records. Producing or technically accessing data does not confer approval authority.

## 46. Integration with Artifact Registry

ART registers raw references, derived datasets, mappings, calendars, checks, defect reports, transformations, reconciliations, decisions, and packages with lineage, versions, owners, consumers, freeze, retention, and supersession. Data artifacts create no authority by themselves.

## 47. Integration with Strategy Lifecycle Standard

Every strategy version links exact eligible data versions. Material source, mapping, history, preprocessing, or eligibility change triggers impact review and may return the strategy to experiment, Validation, risk, deployment, or monitoring review.

## 48. Integration with Autonomous Research Pipeline

ARP cannot initiate data-dependent stage work without purpose-matched eligibility. It preserves rejected sources, defects, changes, returns, and learning, and may not silently substitute datasets between stages.

## 49. Integration with Market Discovery and Ranking Standard

MDRS receives source scope, coverage, continuity, liquidity/volume/cost fitness, eligibility, uncertainty, and exclusions. Market rank cannot compensate for poor or incomparable data.

## 50. Integration with Regime Classification Standard

RCS consumes temporally aligned, scope-eligible data with explicit resampling and revision status. Regime labels inherit gaps, session effects, anomalies, and uncertainty and must be revisited when source evidence changes.

## 51. Integration with Feature Factory Standard

FFS binds each feature version to exact input dataset versions and temporal availability. Imputation, scaling, normalization, smoothing, and transformations inherit DQS lineage and leakage restrictions.

## 52. Integration with Edge Discovery Standard

EDS records data fitness for the observed behavior, mechanism, effect size, controls, costs, regimes, and sample. Defects or source dependence limit or invalidate edge claims even when effects appear favorable.

## 53. Integration with Strategy Family Selection Standard

SFSS must preserve data scope and limitations when comparing families. Missing liquidity, execution, volume, regime, or cost data constrains eligible family claims and architecture handoff.

## 54. Integration with Experiment Design Standard

XDS preregisters exact dataset versions, partitions, fields, preprocessing, costs, assumptions, exclusions, and failure criteria. Substitution, revised history, or preprocessing change requires amendment before interpretation.

## 55. Integration with Walk-Forward and Robustness Standard

WFRS preserves chronological availability, version integrity, folds, embargoes, gaps, revisions, and regime coverage. Fold-quality differences and excluded periods remain visible in aggregation and classification.

## 56. Integration with Monte Carlo and Stress Testing Standard

MCSTS identifies source results and which observed data dependencies perturbations preserve or destroy. Simulation cannot repair deficient inputs, and synthetic stress outputs retain input-data limitations.

## 57. Integration with Parameter Stability Standard

PSS uses consistent, version-bound data across neighborhoods and contexts. Apparent islands caused by gaps, revisions, mapping, resampling, cost, or regime-data defects are challenged and cannot support stability.

## 58. Integration with Overfitting Defense Standard

ODS receives data-access, revision, preprocessing, universe, exclusion, and holdout histories. DQS blocks leakage and hindsight through data construction; repeated dataset inspection and repair after results count as research exposure.

## 59. Integration with Experiment Evidence Package

EEP cites the frozen DQS package and exact tested data version, coverage, partitions, defects, exclusions, transformations, revisions, and limitations. Missing or mismatched identity makes the package incomplete.

## 60. Integration with Validation Evidence Package

VEP independently assesses DQS provenance, admissibility, temporal integrity, reproducibility, defects, preprocessing, scope, and contradictions. Validation may narrow, qualify, return, or reject; it cannot rewrite data evidence.

## 61. Integration with Risk Review Package

RRP receives residual data, source, revision, liquidity, spread, cost, tail, operational, and live/backtest mismatch risks. Risk preserves Validation and DQS limits and specifies monitoring, redundancy, and suspension controls.

## 62. Integration with Deployment Governance Standard

DGS locks authorized production source, symbol mapping, field basis, version/configuration, timezone/calendar, freshness, reconciliation, fallback, and kill conditions. Unapproved substitution or mismatch blocks or suspends authority.

## 63. Integration with Monitoring and Edge Decay Standard

MEDS continuously observes freshness, missingness, duplicates, gaps, timestamps, mapping, sessions, OHLC, volume/liquidity, spreads/costs, revisions, reconciliation, and live/backtest drift. Material breach creates evidence and triggers warning, degradation, quarantine, or suspension.

## 64. Governance

The Data governance authority owns taxonomy, mandatory checks, eligibility and change control; independent Validation determines downstream admissibility. Changes require impact analysis, versioning, approval, migration, and prospective effect. Exceptions are scoped, owned, time-bounded, auditable, and cannot waive identity, lineage, temporal availability, custody, limitation, or reconstruction.

Mandatory risks include unknown source, unversioned data, mapping/timezone/timestamp errors, missing/duplicate/gap/outlier/spike/flatline/stale data, invalid OHLC/volume/spread/cost, calendar/session mismatch, preprocessing leakage, resampling bias, look-ahead adjustment, corporate actions, rollover, vendor revision, source disagreement, partial and survivorship histories, and live/backtest mismatch.

Every future AI Quant Lab dataset or dependent market, regime, feature, edge, family, experiment, robustness, Validation, risk, deployment, or monitoring claim must conform to DQS before institutional reliance. Rejection, quarantine, supersession, cancellation, or retirement never erases lineage or learning.
