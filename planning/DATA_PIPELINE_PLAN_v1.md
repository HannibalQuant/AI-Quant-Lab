# AI Quant Lab — Data Pipeline Plan v1.0

## 1. Document Status

| Field | Value |
|---|---|
| Phase / Sprint | Phase 2 — Sprint 7 |
| Status | Proposed for governance review |
| Canonical path | `planning/DATA_PIPELINE_PLAN_v1.md` |
| Constitutional baseline | AI Quant Lab v1.0, tag `v1.0`, commit `50b61266f880cb9657b7f1b477d3d90825fe013f` |
| Phase 2 baseline | Sprints 1–6; current `main` merge `6c9b1fb983bcbd1f78edff03363fab2250ecad36` |
| Version | 1.0 |
| Implementation / execution authority | None; EXE-01 remains `PLANNED_CLOSED` |

This is a documentary planning contract. It creates no pipeline, connector, schema, storage, feature, test, strategy or execution authority.

## 2. Purpose

Define the future governed route from source discovery to exact, versioned, locked and reproducible research input while preserving identity, raw history, temporal availability, negative findings, lineage, authority and audit.

## 3. Authority and Inheritance

Authority descends: Constitutional Baseline → Implementation Planning Charter → Module Boundary Architecture → Artifact & Evidence Contract System → Workflow & State Transition Blueprint → Responsibility & Authority Matrix → Test Architecture Plan → this plan → future specifications. The Data Quality Standard and relevant research, evidence, validation, memory, communication and agent contracts supply domain obligations but cannot be weakened here. Conflict means HOLD, record and competent governance review.

## 4. Scope

This plan covers 13 data classes, 21 stages, five market asset families, source/instrument/time identity, raw preservation, quality and temporal evidence, transformations, manifests, versioning/locking, eligibility, quarantine/invalidation, lineage, reproducibility, authority, failure/recovery, observability, 34 relevant modules and 22 inherited test families.

## 5. Non-Goals

No Python, SQL, executable schema, database, API, ETL, data loader, exchange/broker/TradingView client, stream, storage technology, cloud/CI, feature, indicator, strategy, backtest, validator, monitor, trading or execution is implemented. No provider, hashing algorithm, physical partition format, quality threshold, imputation method or cost constant is selected.

## 6. Governing Data Principles

1. No data without source and instrument identity.
2. No dataset without exact provenance and lineage.
3. Raw evidence is immutable; correction creates a new attributable version.
4. Event time is not availability time; historical decisions may use only then-available information.
5. Quality PASS is scoped evidence, not scientific success.
6. Outlier is not synonymous with error; failed and adverse observations remain visible.
7. Transformation never silently mutates its input or creates authority.
8. Experiment inputs are exact immutable snapshots under a governed lock.
9. Quarantine, invalidation and stale states block new consequential reliance.
10. Access, custody, orchestration, monitoring and registration do not create eligibility authority.

## 7. Terminology

| Term | Meaning | Not equivalent to |
|---|---|---|
| Source | Identified origin/provider/mechanism | Filename |
| Raw version | Preserved acquired representation | Clean dataset |
| Canonical data | Identity/time/field semantics expressed consistently | Scientific feature |
| Dataset | Purpose- and scope-bounded versioned collection | Latest query |
| Lock | Authorized binding to exact manifest/version/fingerprint | Ownership |
| Availability time | Earliest governed time information was usable | Event time |
| Finding | Attributable quality/temporal observation | Automatic correction |
| Quarantine | Reversible isolation pending review | Invalidation |
| Invalidation | Determination that basis is unusable in affected scope | Deletion |

## 8. Data Class Model

| Class | Contract boundary |
|---|---|
| SOURCE_DATA | Provider-origin observations before Lab custody |
| RAW_DATA | Acquired original representation, immutable by version |
| CANONICAL_DATA | Standard identities and semantic fields without scientific inference |
| NORMALIZED_DATA | Consistent representations preserving meaning |
| DERIVED_DATA | Explicit governed transformation output |
| FEATURE_DATA | Research feature output, outside implementation scope here |
| DATASET | Purpose/scope manifest over exact inputs |
| LOCKED_DATASET | Exact dataset version bound to governed use |
| TEST_DATA | Isolated synthetic/fixture/adversarial/golden input |
| REFERENCE_DATA | Calendars, mappings, corporate actions or authoritative reference facts |
| QUARANTINED_DATA | Isolated from normal eligibility paths |
| SUPERSEDED_DATA | Historical version replaced but still addressable |
| INVALIDATED_DATA | Preserved history prohibited from affected reliance |

Classes are explicit metadata and custody contracts; conversion requires an attributable stage and never happens by filename or storage location.

## 9. Data Pipeline Stages

| ID | Stage | Required output / failure boundary |
|---|---|---|
| DP-00 | Source Discovery | Candidate source note; no eligibility |
| DP-01 | Source Registration | Source Record with stable identity |
| DP-02 | Source Authorization | Scoped acquisition eligibility or rejection |
| DP-03 | Ingestion Request | Exact source/window/instrument request |
| DP-04 | Acquisition | Attributed original representation and timestamps |
| DP-05 | Raw Preservation | Immutable raw version/fingerprint |
| DP-06 | Integrity Verification | Identity/transfer integrity evidence or quarantine |
| DP-07 | Structural Validation | Field/type/shape findings without silent repair |
| DP-08 | Data Quality Assessment | Scoped Data Quality Report |
| DP-09 | Temporal Integrity Assessment | Scoped Temporal Integrity Report |
| DP-10 | Canonicalization | Canonical identities/semantics and lineage |
| DP-11 | Normalization | Meaning-preserving normalized version |
| DP-12 | Transformation | Versioned transformation output and lineage |
| DP-13 | Dataset Construction | Dataset Manifest over exact versions |
| DP-14 | Dataset Quality Gate | Eligibility evidence/disposition |
| DP-15 | Dataset Version Registration | Stable dataset ID and immutable version |
| DP-16 | Dataset Lock | Exact manifest/version/fingerprint/use binding |
| DP-17 | Research Eligibility | Governed research-use disposition |
| DP-18 | Experiment Eligibility | Stronger exact-use authorization basis |
| DP-19 | Archive / Supersede / Invalidate | Preserved history and impact routing |
| DP-20 | Audit / Reproduction | End-to-end reconstruction evidence |

No stage auto-promotes to the next. Each boundary requires its own evidence, current state and competent authority.

## 10. Source Governance

Every Source Record declares source ID/version, provider, market, venue, instrument/type/symbol/base/quote, timeframe where applicable, mechanism, timezone, timestamp/session semantics, expected frequency, fields/definitions, adjustment/revision/availability policies, historical availability, licensing/access restrictions, provenance, responsible steward and review status. Unknown semantics produce `SOURCE_UNKNOWN`, quarantine and no research eligibility.

## 11. Market Data Source Model

| Family | Distinct future sources / non-equivalence |
|---|---|
| Crypto | Spot, perpetual, dated futures, funding, OI, liquidations and order-book-derived data; venue/price type remain explicit |
| Forex | Broker and reference feeds, bid/ask, spreads, calendars and session semantics; feeds are not fungible |
| Metals / Commodities | Spot proxies, futures and CFD/broker data with contract/session distinctions |
| Indices | Cash index, futures and CFD/broker proxy are distinct economic objects |
| Equities | OHLCV plus corporate actions; adjusted and unadjusted histories remain distinct |

## 12. Venue Identity

`BTCUSDT@Binance`, `BTCUSDT@Bitget` and `BTCUSDT@Bybit` are distinct. Venue, market type, contract, price type and settlement are part of identity: spot ≠ perpetual ≠ dated future; cash index ≠ CFD; adjusted ≠ raw equity. Mapping creates a reference relationship, never silent equivalence. T08/T15/T36 verify it.

## 13. Raw Data Immutability

Each raw version records source/acquisition timestamps, original representation reference, source/instrument identity, retrieval window, actor/process, acquisition request, integrity fingerprint and revision status. Raw bytes/meaning are never overwritten. Provider correction creates a new raw version linked to its predecessor; previous experiments continue to reference their historical input.

## 14. Multi-Time Model

| Time | Meaning / applicability |
|---|---|
| EVENT_TIME | Economic event occurred; ticks, trades, actions |
| SOURCE_TIME | Provider assigned time |
| EXCHANGE_TIME | Venue clock time where supplied |
| RECEIVE_TIME | Lab boundary first received payload |
| INGESTION_TIME | Acquisition admitted into custody |
| PROCESSING_TIME | Transformation executed |
| AVAILABILITY_TIME | Information first eligible for a governed consumer |
| EFFECTIVE_TIME | Fact/policy economically applies |
| RECORD_TIME | Institutional record written |

Not every type has every time, but omissions and derivations are explicit. One generic timestamp cannot substitute for the model.

## 15. Temporal Integrity

DP-09 and T16 detect lookahead, future/revised-data/survivorship/session/corporate-action/funding/bar-close leakage, timezone/DST errors and out-of-order events. Historical consumption uses `availability_time ≤ decision_time` under the exact source policy. Unknown availability fails closed; later corrections cannot be represented as originally known.

## 16. OHLCV Bar Contract

Each bar declares open/close/availability times, OHLCV, venue, instrument, timeframe identity, source, completeness and revision state. States distinguish `FORMING`, `CLOSED`, `LATE_CORRECTED`, `MISSING` and `SYNTHETIC`. A forming/partial or late-corrected bar cannot masquerade as an historically closed original bar.

## 17. Next-Bar Research Integrity

Future records relate signal-bar close, completion and information availability, order eligibility, next-bar open and modeled execution-assumption time. A next-bar model may consume only information available before eligibility. Same-bar high/low/close and unavailable funding/session facts are seeded leakage traps. No strategy or execution rule is implemented here.

## 18. Data Quality Dimensions

Quality remains multidimensional: completeness, uniqueness, validity, consistency, continuity, timeliness, accuracy proxy, temporal integrity, cross-field integrity, cross-source consistency, schema conformance, range/volume/price plausibility, session integrity, corporate-action integrity and instrument identity integrity. Each dimension has checks, scope, evidence, severity, unknowns and disposition; no opaque composite score replaces findings.

## 19. Quality Findings

Canonical finding classes: `MISSING`, `DUPLICATE`, `OUT_OF_ORDER`, `INVALID_TIMESTAMP`, `INVALID_OHLC`, `ZERO_VOLUME`, `NEGATIVE_VOLUME`, `EXTREME_JUMP`, `SESSION_VIOLATION`, `TIMEFRAME_GAP`, `SOURCE_GAP`, `SYMBOL_MISMATCH`, `VENUE_MISMATCH`, `REVISION_DETECTED`, `CORPORATE_ACTION_MISMATCH`, `FUTURE_TIMESTAMP`, `STALE_DATA`. Every finding includes record scope, detection rule/version, evidence, severity, reviewer, disposition and linkage; severity thresholds remain future governed specifications.

## 20. OHLC Invariants

Future checks require `high ≥ open`, `high ≥ close`, `high ≥ low`, `low ≤ open`, `low ≤ close`, `low ≤ high` and `volume ≥ 0` where volume is semantically applicable. Violation is rejected, quarantined or corrected only through a separately versioned, justified transformation. Silent repair is forbidden.

## 21. Missing Data

Missingness distinguishes expected market closure, session gap, source/venue outage, not-yet-listed, delisted, corrupt and unknown. Automated price forward-fill is not a default. Imputation, if later authorized, records method/version, scope, source records, assumptions, availability impact and visible flags; raw evidence remains unchanged.

## 22. Duplicate Semantics

Exact duplicate, same timestamp/different values, same event ID, same bar key, retransmission and source correction are separate cases. Exact retransmission may link to one canonical observation under evidence; conflicting duplicates remain visible and require source/revision review. A conceptual `drop_duplicates` shortcut is prohibited.

## 23. Outlier Semantics

Findings classify plausible market event, bad tick, flash crash, liquidity event, source error, corporate action, contract rollover or unknown. Extreme observations are preserved and challenged; deletion because a strategy performs poorly is evidence manipulation. Any exclusion is versioned and research-visible.

## 24. Source Corrections

Revision detection preserves prior representation, registers new source/raw versions, compares differences and discovers affected datasets, locks, experiments, validations and decisions. Sprint 4 contain-first routing determines HOLD/review/revalidation; correction never rewrites old scientific history.

## 25. Normalization

DP-10/11 may normalize timestamps/timezones, symbol/venue/instrument mappings, field names, numeric and missing-value representation. Input/output versions and semantic equivalence evidence are retained. Normalization standardizes representation; it does not infer edge, fill unknown facts or authorize research use.

## 26. Transformation Governance

Every transformation record has ID/version, purpose, exact inputs/outputs, parameters, actor/module/time, future code/version reference, assumptions, availability semantics, lineage and failure status. Material change creates a new output and dataset version. Failed transformations are retained as negative evidence.

## 27. Feature Boundary

`DATA TRANSFORMATION ≠ FEATURE ENGINEERING ≠ INDICATOR ≠ STRATEGY SIGNAL`. DAT-04 may produce canonical/derived data under explicit semantics; future feature modules must inherit source, transformation and availability lineage. No feature or signal is implemented, and a feature cannot backdate its availability.

## 28. Dataset Manifest

Sprint 3 Dataset Manifest is specialized, not replaced. It records dataset ID/version/purpose/scope, markets/venues/instruments/timeframes/window, source/raw/transformation versions, quality/temporal reports, gaps/anomalies/revisions/exclusions/assumptions, fingerprint, producer/custodian/creation time, availability model, lineage root, lifecycle/admissibility references and allowed consumers.

## 29. Dataset Versioning

A new version is mandatory for source/raw revision, transformation/normalization change, quality correction, mapping change, time-boundary/exclusion change, corporate-action policy or timestamp semantic change. Stable dataset ID denotes lineage continuity, not identical content. Materially different input can never hide behind the same version.

## 30. Dataset Lock

The lock identifies dataset ID/version/fingerprint, manifest version, quality and temporal report versions/dispositions, allowed scope, requesting experiment/workflow, authority identity and lock time. Locked content is immutable. Change requires new dataset version, new lock and new attributable experiment input; a retroactive lock fails T07/T16/T36.

## 31. Dataset Lifecycle / State Crosswalk

Dataset stage labels do not overload Sprint 3/4 axes.

| Pipeline label | Artifact lifecycle axis | Evidence / eligibility meaning |
|---|---|---|
| DISCOVERED | DRAFT | Candidate only |
| REGISTERED / INGESTED / RAW_PRESERVED | REGISTERED | Custody exists; no eligibility |
| QUALITY_PENDING / TEMPORAL_PENDING | UNDER_REVIEW | Evidence incomplete |
| QUALITY_REVIEWED / TEMPORAL_REVIEWED / DATASET_BUILT | REGISTERED or FROZEN version | Exact reports exist; no automatic eligibility |
| ELIGIBILITY_REVIEW | UNDER_REVIEW | Use-specific assessment |
| ELIGIBLE / CONDITIONALLY_ELIGIBLE | Artifact remains registered/frozen | Separate use-specific eligibility disposition |
| QUARANTINED | Historical lifecycle unchanged | Quarantine axis blocks use |
| SUPERSEDED / INVALIDATED / ARCHIVED | Matching artifact lifecycle state | History preserved; impacts routed |

## 32. Research Eligibility

Requires known source/lineage/scope, exact version/fingerprint, quality and temporal evidence, disclosed limitations/anomalies, integrity evidence, authorized use and no blocking quarantine/invalidation/staleness. Readability, registration, custody or a quality score alone are insufficient.

## 33. Experiment Eligibility

Requires research eligibility plus exact immutable dataset version/manifest, DP-16 lock, experiment-compatible scope and temporal cutoff, known anomalies/exclusions, current quality disposition and Reproducibility Manifest linkage. EXP cannot choose “latest” mutable data or silently replace a locked version.

## 34. Data Quarantine

Triggers include unknown source, broken provenance, corruption, ambiguous timestamps, suspected leakage, identity/duplicate conflict, unexpected revision, fingerprint failure, unknown transformation, scope ambiguity and material quality failure. Quarantined data remains inspectable and preserved but cannot support new promotion or authorization. Release needs resolved cause, current evidence, independent competent review/authority and AUD record.

## 35. Data Invalidation

Confirmed corruption/leakage, wrong instrument/venue/contract, broken transformation, unrecoverable provenance or invalid corporate-action handling may invalidate exact scope/version. Invalidation is an authorized decision distinct from quarantine/supersession. It blocks new reliance and triggers contain-first dependency review without deleting artifacts, evidence or prior decisions.

## 36. Lineage

Documentary lineage is `SOURCE → ACQUISITION REQUEST/RUN → RAW VERSION → CANONICALIZATION/NORMALIZATION → TRANSFORMATION → DATASET VERSION/MANIFEST → LOCK → EXPERIMENT → RESULT → VALIDATION → DECISION`. Relationships use Sprint 3 semantics and exact versions; any broken edge blocks consequential claims.

## 37. Provenance

Source provenance answers who/what originated data; acquisition provenance how/when/by whom it entered custody; transformation provenance how exact versions changed; dataset provenance how scope and selection formed; experiment provenance which lock was consumed. Filename, folder, row count or provider logo proves none of these.

## 38. Fingerprinting

Future fingerprints bind raw acquisition/partition, canonical output, dataset version, lock and manifest to exact content and declared semantics. They must support change detection, version verification, duplicate/replay relationships and audit reconstruction. Algorithm/encoding remain implementation choices; fingerprint match does not by itself prove source truth or eligibility.

## 39. Logical Partitioning

Logical keys may include source, venue, canonical instrument, instrument type, timeframe, date/window, data class and version. Partition identity supports scoped checks, lineage and reproduction. Physical storage/path formats are deferred and cannot serve as canonical identity.

## 40. Instrument Master

Instrument Identity Record includes canonical ID, venue symbol/venue, asset class/type, base/quote/settlement, contract/expiry, tick/lot semantics, listing/delisting, timezone/session and corporate-action relevance. Mappings carry validity intervals and authority. Symbol string alone is insufficient.

## 41. Timeframe Model

Timeframe identity records duration label (for example 1m, 5m, 15m, 1h, 2h, 3h, 4h, 1D), vendor alignment, session anchor, timezone, close convention, DST behavior, aggregation source and availability rule. Equal labels across vendors are not assumed equivalent.

## 42. Resampling Governance

Each resample records source/target timeframe, alignment, timezone/session boundary, OHLCV aggregation semantics, missing/partial-bar treatment and resulting availability time. A target bar becomes available only after all permitted source intervals are available. Future sub-bars or incomplete windows cannot leak backward.

## 43. Multi-Source Reconciliation

Comparisons produce `CONSISTENT`, `MINOR_VARIANCE`, `MATERIAL_VARIANCE`, `SOURCE_CONFLICT` or `UNKNOWN` with exact source/version/window/fields and tolerance policy. No silent averaging or majority-vote truth. Material/unknown conflicts block affected eligibility pending competent review.

## 44. Corporate Actions

Equity reference data distinguishes splits, reverse splits, dividends, symbol changes, mergers, spin-offs and delistings. Adjusted/unadjusted series and adjustment method/version remain separate. Tests use what actions were historically available, preventing later-known corrections from leaking into earlier decisions.

## 45. Futures / Perpetuals

Records distinguish contract/expiry/roll, raw contracts versus continuous series, back-adjustment version, funding, mark/index/last price, OI and liquidation semantics. Continuous futures are derived datasets, never raw exchange history. Funding/roll availability is explicit.

## 46. Crypto 24/7

Venue maintenance/outages, listing/delisting, funding intervals, candle boundary and UTC assumptions are source-specific. Twenty-four-hour trading does not imply uninterrupted observations or cross-venue equality. Missing periods retain cause classifications.

## 47. Forex Sessions

Records capture weekend closure, rollover, DST, broker timezone, Sunday candles, bid/ask/spread and session boundary. Broker feeds retain provider identity and are not silently blended. Session calendar versions determine expected gaps.

## 48. Cost Data Boundary

Spread, commission, funding, borrow, fees and slippage proxies use separate sources, identities, timestamps, scope and lineage. Cost assumptions reference exact versions in future experiments. Sprint 7 selects no value and never treats a constant as observed evidence.

## 49. Survivorship Bias

Historical universe membership, listing/delisting and eligibility at each decision time are preserved. Today’s top assets cannot define yesterday’s universe unless the research question explicitly and honestly studies that retrospective selection. T16/T21/T22 use future-membership attacks.

## 50. Selection Bias

Dataset construction records selection rule/version, decision time, eligible universe, all excluded instruments/reasons and any data-dependent filtering. Winner-centered datasets or silent exclusion of missing/failed instruments are prohibited. Selection evidence is part of the manifest.

## 51. Leakage Attack Library

Future governed bad cases insert future close early; expose future high/low at bar open; treat revisions as originals; leak funding, future universe/corporate actions/volatility labels; shift timestamps backward; use lookahead resampling; and construct post-selection universes. Sprint 6 T16/T21/T22/T62-equivalent meta-tests must detect them.

## 52. Golden Data Cases

Versioned cases include clean OHLCV, missing/conflicting duplicate/bad OHLC, future timestamp, late revision, venue/symbol mismatch, DST/session boundaries, flash crash, corporate action, contract rollover and funding event. Their expected findings/oracles are independently governed; no datasets are created now.

## 53. Data Failure Model

Canonical failures: `SOURCE_UNAVAILABLE`, `SOURCE_UNKNOWN`, `INGESTION_INCOMPLETE`, `RAW_INTEGRITY_FAIL`, `STRUCTURE_FAIL`, `QUALITY_FAIL`, `TEMPORAL_FAIL`, `IDENTITY_FAIL`, `LINEAGE_FAIL`, `TRANSFORMATION_FAIL`, `VERSION_CONFLICT`, `LOCK_FAIL`, `QUARANTINE_REQUIRED`, `INVALIDATED`. Each has detector, affected scope, evidence, severity, current state, containment, authority, route and recovery condition.

## 54. Failure Containment

Responses are HOLD, quarantine, block eligibility, request review, escalate or invalidate according to evidence and authority. The last valid version remains addressable and no new consequential reliance proceeds. Guessing, silent fixing, ignoring or continuing because a backtest looks attractive are prohibited.

## 55. Recovery

Recovery identifies cause, uses corrected/new source or transformation, creates an attributable new raw/dataset version, repeats structural/quality/temporal checks, issues new manifest/fingerprint/eligibility and obtains a new lock where required. Failed history and impact records remain immutable; retry never bypasses the failed gate.

## 56. Data Authority Model

Thirty-four relevant modules are mapped; technical capability never expands the listed power: `DAT-01`, `DAT-02`, `DAT-03`, `DAT-04`, `DAT-05`; `RES-01`, `RES-02`, `RES-03`; `EXP-01`, `EXP-02`, `EXP-03`, `EXP-04`, `EXP-05`, `EXP-06`; `VAL-01`, `VAL-02`, `VAL-03`, `VAL-04`, `VAL-05`, `VAL-06`, `VAL-07`; `AUD-01`, `AUD-02`, `AUD-03`; `GOV-01`, `GOV-02`; `IAM-01`, `IAM-02`; `ORC-01`, `ORC-02`, `ORC-03`; and `MON-01`, `MON-02`, `MON-03`.

| Module(s) | Permitted data role | Explicit prohibition / competent route |
|---|---|---|
| DAT-01 | Register source identity; request/perform governed acquisition | Cannot grant dataset eligibility; H-08/GOV authorizes source use |
| DAT-02 | Preserve raw versions and fingerprints | Cannot correct/transform raw in place |
| DAT-03 | Assess structural, quality and temporal evidence; request quarantine | Cannot authorize its own material exception/release |
| DAT-04 | Construct canonical/normalized/derived datasets under specification | Cannot create feature truth or self-approve inputs |
| DAT-05 | Register versions/manifests; custody locks and eligibility metadata | Registry/custody cannot authorize by storage |
| RES-01..03 | Consume eligible data; challenge scope/selection/findings | Cannot change data or bypass lock |
| EXP-01..06 | Request exact datasets/locks; consume and package references | Cannot select mutable latest input or repair data |
| VAL-01..07 | Independently review data basis, temporal integrity and parity | Cannot rewrite evidence or accept producer-controlled lineage |
| AUD-01..03 | Register/link/preserve/reconstruct artifacts, evidence and transitions | Cannot quality-pass, release or authorize |
| GOV-01..02 | Resolve authority/policy, exceptions and escalation | Cannot manufacture data facts or hide failure |
| IAM-01..02 | Resolve actor and scoped delegation | Identity/access does not create data authority |
| ORC-01..03 | Route stages, prerequisites, failure and recovery | Cannot promote, release quarantine or waive evidence |
| MON-01..03 | Observe source/quality/lineage/lock health; request containment | Cannot silently repair or re-eligible data |

Roles separate register source, acquire, preserve raw, assess quality/time, construct, register version, request/authorize lock, challenge, quarantine/release, invalidate and record. Requester/producer/custodian/recorder is not authorizer by implication.

## 57. Human / Agent Responsibilities

H-08 Data Steward owns scoped source, quality/temporal and dataset governance; H-02 resolves exceptions/ambiguity; H-06 owns independent validation use; H-10 audits; affected research/experiment owners request use. Agents may discover, inspect, profile, detect anomalies, propose mappings, produce reports, request quarantine and challenge within contract/delegation. Material C3/C4 eligibility, exception, invalidation and release require Sprint 5 competent/accountable authority and independence; no agent gains capital/A11 authority.

## 58. Data Criticality

| C | Example and minimum controls |
|---|---|
| C0 | Documentation/reference; identity and attribution |
| C1 | Exploratory research; source/lineage and review/challenge |
| C2 | Formal experiment input; exact versions, quality/time evidence and lock |
| C3 | Validation/decision-support input; independent review, full reconstruction and named authority |
| C4 | Future capital/safety data; strongest independent/human gates, fail closed and emergency routing |

Unauthorized criticality downgrade fails. Higher criticality never retroactively upgrades weak evidence.

## 59. Test Obligations

Sprint 6 obligations inherited: T02 Module Contract, T04 Artifact Contract, T05 Evidence Contract, T07 State, T08 Authority, T11 SoD, T12 Independence, T15 Data Integrity, T16 Temporal Integrity, T17 Reproducibility, T18 Determinism, T19 Regression, T21 Negative Control, T22 Adversarial, T23 Failure, T24 Recovery, T25 Audit, T32 Quarantine, T34 Concurrency, T35 Replay, T36 Version/Lineage and T38 End-to-End Governance. Every DP stage maps positive, negative, failure/recovery and audit evidence before implementation readiness.

## 60. Temporal Test Obligations

Future T16 cases cover lookahead, future/partial-bar and resampling leakage, timezone/DST shift, revised-data leakage, future funding/corporate action/universe membership, decision-time and availability-time mismatch, out-of-order receipt and retroactive lock. Unsafe cases fail closed and identify the violated time relation.

## 61. Reproducibility Contract

A future researcher can reconstruct WHAT data, FROM WHERE, WHICH source/raw/dataset/manifest versions, WHEN acquired/available, HOW normalized/transformed, WHICH findings/exclusions/revisions, WHICH fingerprint and WHICH lock produced the exact experiment input. Missing any critical link blocks R3+ reproducibility and experiment eligibility.

## 62. Dataset Snapshot vs Query

A mutable query definition expresses intent and may be versioned; it does not freeze results. A reproducible experiment uses an immutable materialized logical snapshot or equivalently exact content-addressable input under DP-16. “Query latest BTC data” is never sufficient evidence.

## 63. Concurrency

Source revision during build, review during ingestion, lock during change, invalidation while experiment starts, competing dataset versions and quarantine dispositions enter conflict routing. Optimistic progression pauses; the valid restrictive state dominates until exact version/order and competent authority resolve the conflict.

## 64. Idempotency / Replay

Same acquisition request ID/source/window/version does not create conflicting institutional identities. Identical bytes retain attributable duplicate/retransmission relationships; identity is not inferred from content alone. Replay cannot overwrite newer versions, refresh expired authority or produce a second lock effect.

## 65. Access ≠ Authority

Reading an API does not authorize source registration; writing storage does not authorize eligibility; owning/custody of a dataset does not authorize experiment use; registry presence does not create truth. T08/T11/T22 test these exact bypasses.

## 66. Data Security Boundary

Future designs must provide source authenticity evidence, integrity/tamper evidence, least privilege, separated credentials/roles, scoped access and attributable audit. Credentials and storage security are implementation concerns; this plan defines no secret, network or infrastructure design.

## 67. Retention / Archival

Retention classes cover raw versions, canonical/normalized/derived data, dataset/manifests/locks, quality/temporal reports, superseded/invalidated/quarantined data and failure evidence. Dependencies, legal holds and scientific reconstruction prevent silent deletion. Exact legal durations remain open under S7-OQ-06.

## 68. Data Observability

Future MON observes source availability, gaps/latency, quality/schema drift, revision rate, timestamp anomalies, missing bars, duplicate conflicts, lineage breaks and lock violations. It emits versioned monitoring evidence and may request HOLD/quarantine/review. It cannot repair, transform, release or authorize.

## 69. Schema Evolution

Field addition/removal, type/semantic/timestamp change, symbol mapping and provider schema change create versioned compatibility and downstream impact assessments. Semantic change cannot hide as a compatible field rename. This is documentary governance; no executable schema is selected.

## 70. Source Deprecation

Deprecation records reason/effective time, replacement candidate, overlap comparison and affected consumers. Historical source/raw data and experiment provenance remain addressable. Replacement requires new source identity/authorization and new dataset versions; provider swap is not an amendment to history.

## 71. Dataset Comparability

Two exact versions may be `IDENTICAL`, `SCIENTIFICALLY_EQUIVALENT`, `COMPATIBLE`, `PARTIALLY_COMPATIBLE`, `NON_COMPARABLE` or `UNKNOWN` under a versioned comparison scope/oracle. Similar filenames, symbols, row counts or metrics never prove equivalence. Unknown/material differences block pooled conclusions.

## 72. Data Quality Report

The Sprint 3 Data Quality Report specialization states source/dataset/version/window, checks and rule versions, findings/severity, known gaps/unknowns, exceptions, producer/reviewer/challenge, disposition/scope/time and lineage. It references raw evidence and exclusions. Quality PASS does not validate a claim or strategy.

## 73. Temporal Integrity Report

The report states the multi-time and availability model, bar/session assumptions, lookahead/revision/resampling/universe checks, known limitations, exact source/dataset scope, producer, independent reviewer/challenge and disposition. PASS is use- and cutoff-specific; changed timestamp semantics make it stale.

## 74. Data Decision Separation

`DATA QUALITY PASS ≠ RESEARCH SUCCESS`; `RESEARCH SUCCESS ≠ VALIDATION PASS`; `VALIDATION PASS ≠ DECISION APPROVAL`; `DECISION APPROVAL ≠ EXECUTION AUTHORITY`. No cross-axis automatic transition follows from data eligibility.

## 75. Governance Exceptions

Exception records use Sprint 3/5 semantics and cannot hide corruption, confirmed future leakage, unknown identity/source, fabricated/broken provenance, raw-history mutation, unauditable transformation, prohibited self-approval or EXE isolation. These are candidate non-waivable categories for consequential research. A bounded exception exposes residual risk, scope, expiry and compensating controls; it never rewrites evidence.

## 76. Planning ADRs

| ADR | Context / decision | Rationale / rejected alternative | Consequence | Constitutional basis |
|---|---|---|---|---|
| S7-ADR-01 | Raw versions immutable | Silent correction rejected | New revision/version | Evidence preservation |
| S7-ADR-02 | Multi-time model | Generic timestamp rejected | Availability reconstructable | Temporal integrity |
| S7-ADR-03 | Venue-aware identity | Symbol-only identity rejected | Cross-venue separation | Data quality |
| S7-ADR-04 | Instrument Master | Free-text symbol rejected | Stable economic identity | Provenance |
| S7-ADR-05 | Material change creates dataset version | Mutable ID rejected | Exact input history | Sprint 3 versioning |
| S7-ADR-06 | Lock binds exact manifest/content | Query lock rejected | No mutation after authorization | Sprint 4 freeze |
| S7-ADR-07 | Availability time governs use | Event time alone rejected | Lookahead detectable | Research OS |
| S7-ADR-08 | No silent repair | Convenient cleanup rejected | Findings and transform versions | Evidence law |
| S7-ADR-09 | Quarantine is first-class | Optimistic continuation rejected | Promotion/use blocked | Sprint 3/4 |
| S7-ADR-10 | Invalidation is preserved decision | Delete/cascade rejected | Contain-first review | Sprint 4 |
| S7-ADR-11 | Every transform has lineage | Filename inference rejected | Reproducible derivation | Sprint 3 |
| S7-ADR-12 | Feature boundary remains separate | Feature smuggling rejected | Sprint 8+ owns computation | Module architecture |
| S7-ADR-13 | Resampling has availability semantics | Naive aggregation rejected | No future sub-bar leakage | Temporal law |
| S7-ADR-14 | Source revisions create new versions | Provider overwrite rejected | Impact routing | Immutable history |
| S7-ADR-15 | Missingness has causes | Automatic fill rejected | Research-visible uncertainty | Scientific integrity |
| S7-ADR-16 | Outliers preserved until classified | Performance-driven deletion rejected | Market events retained | Negative evidence |
| S7-ADR-17 | Multi-source conflict remains visible | Silent averaging rejected | Review/UNKNOWN possible | Contradiction law |
| S7-ADR-18 | Experiments consume snapshots | Latest-query dependency rejected | Exact reproducibility | Sprint 3 manifest |
| S7-ADR-19 | Access ≠ authority | Technical capability rejected | Competent gate required | Sprint 5 |
| S7-ADR-20 | Monitoring ≠ repair | Auto-fix rejected | Request/contain only | Sprint 2/5 |
| S7-ADR-21 | Historical universe membership required | Today’s winners projected backward rejected | Survivorship defense | Research OS |
| S7-ADR-22 | Selection rule/exclusions traced | Winner-centered dataset rejected | Bias challengeable | Evidence completeness |
| S7-ADR-23 | Corporate actions versioned by availability | Backfilled adjustment treated as original rejected | Adjusted/raw distinction | Temporal integrity |
| S7-ADR-24 | Futures/perpetual identities distinct | Continuous/raw conflation rejected | Contract/roll/funding lineage | Instrument integrity |

## 77. Open Questions Register

| ID | Question / source | Stage/module/artifact/workflow/test | C / severity | Status / fail-closed default | Authority | Target / resolution |
|---|---|---|---|---|---|---|
| S7-OQ-01 | Production ID syntax/namespaces and state reconciliation? S6-OQ-05 | DP-01/15/16; IAM/DAT/AUD; manifests/locks; WF-02; T35/36 | C3/Medium | Non-blocking; ambiguity/collision quarantined | Artifact/Workflow Governance | Future implementation spec |
| S7-OQ-02 | Freshness triggers/periods by data/evidence class? S6-OQ-04 | DP-14/17/18; DAT/MON/VAL; reports; WF-02/05; T05/19 | C2–4/High | Non-blocking; suspected stale basis HOLD | H-08 + domain authority | Sprints 9–10 |
| S7-OQ-03 | Numerical independence criteria for external source/reviewer overlap? S6-OQ-02 | DP-08/09/14; DAT/VAL; reports; WF-02/04; T12 | C3/High | Non-blocking; mandatory dimension unproven = fail | H-06/H-08/Evidence Governance | Sprint 9/12 |
| S7-OQ-04 | Which bounded data actions qualify for agent A7? S6-OQ-01 | All; DAT/GOV/IAM; records; WF-02; T08/33 | C3/High | Non-blocking; no A7 unless named and all eligibility dimensions pass | H-02/H-08 | Sprint 12/domain specs |
| S7-OQ-05 | Provider-specific availability/revision semantics catalog? New | DP-01/09; DAT-01/03; Source Record/TIR; WF-02; T16 | C2–3/High | Non-blocking plan; unknown source ineligible | H-08 | Future source onboarding |
| S7-OQ-06 | Legal/licensing retention durations and permitted reproduction? S6-OQ-06 | DP-05/19/20; DAT/AUD; archive; WF-02/11; T04/25 | C2–4/High | Non-blocking; preserve unless law/authority directs otherwise | Legal/Data/Artifact authority | Later governance plan |
| S7-OQ-07 | Quantitative source reconciliation tolerances? New | DP-08/14; DAT-03; DQR; WF-02; T15/18 | C2–3/Medium | Non-blocking; unexplained material variance blocks | H-08/Scientific Governance | Sprint 9/source specs |
| S7-OQ-08 | Exact physical fingerprint, snapshot and partition technologies? New | DP-05/15/16; DAT-02/05; manifests; WF-02; T17/36 | C2–3/Low | Non-blocking; implementation cannot proceed without chosen verified design | Implementation Governance | Future implementation spec |

Blocking issues for Sprint 7 planning: **0**. All eight questions have explicit containment and no affected implementation path may guess.

## 78. Sprint 8 Handoff Contract

Sprint 8 inherits exact dataset/source/raw/manifest/quality/temporal report versions, selection rule, anomalies/exclusions, availability model, lineage root, fingerprint, research/experiment eligibility, quarantine/invalidation and DP-16 lock. Experiment authorization must verify these before configuration lock/run; it cannot select latest mutable data, weaken findings, alter the dataset or bypass DAT/AUD/GOV authority. It also inherits T05/T07/T08/T11/T12/T15–T25/T32/T34–T36/T38 obligations.

## 79. Definition of Done

The plan defines the full lifecycle, 13 classes and 21 stages; source/venue/instrument/raw/multi-time/OHLCV/next-bar/quality/missing/duplicate/outlier/revision/normalization/transformation/feature boundaries; Sprint 3 manifest/version/lock and Sprint 4 lifecycle crosswalk; eligibility/quarantine/invalidation/lineage/provenance/fingerprints/partitioning/resampling/reconciliation; five asset families and cost/bias/leakage cases; failure/recovery, 34-module authority mapping, human/agent/C0–C4 responsibilities, 22 inherited tests, reproducibility/concurrency/replay/security/retention/observability/evolution/deprecation/comparability/reports/exceptions; 24 ADRs and eight classified questions. EXE-01 is closed; no executable infrastructure exists.

## 80. Final Sprint Disposition

**SPRINT 7 COMPLETE WITH OPEN GOVERNANCE ITEMS**

Blocking issues: **0 for Sprint 7 planning**. Eight bounded governance/implementation questions remain fail-closed. After governance review and merge, the next authorized planning step is **Phase 2 — Sprint 8: Experiment Pipeline Plan**.
