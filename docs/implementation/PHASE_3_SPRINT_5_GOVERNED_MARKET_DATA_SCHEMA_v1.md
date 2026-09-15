# Phase 3 Sprint 5 — Governed Market-Data Schema v1.0

## Baseline, authority and scope

Exact merged Sprint 4 `main`: `733bf69a86b3847029faf0c69e0b07531001c3a4`; PR #65 MERGED before this branch was created. Superior Constitution tag `v1.0`: `50b61266f880cb9657b7f1b477d3d90825fe013f`. This document is a technical implementation report, not a competent governance approval. Phase 1/2 plans, Sprint 1–4 reports and historical goldens are unchanged. EXE-01 remains `PLANNED_CLOSED`.

Only existing accepted synthetic `RawObservation` records become already-bar-shaped `MarketBar` records. No fetch, filesystem adapter, CSV importer, streaming, resampling, backtest, optimizer, features, strategy or execution is introduced. This is a market-data semantic/normalization contract, not a Data Engine.

## Contracts and exact representation

`TimeframeIdentity` has typed `TimeframeId`, exact version, count, unit and `UTC_EPOCH_FIXED` alignment. Supported synthetic identities include 15m, 30m, 1h/2h/3h/4h and fixed 1d. `60m` and `1h` are distinct typed identities despite equal duration; no alias/equivalence rule is invented. Zero, boolean/negative counts, mismatched ID/unit and calendar-unresolved construction reject. Fixed 1d means exactly 24 hours from the UTC epoch, **not** a market-session daily bar; holidays/weekends, DST, trading calendars and venue-session anchoring require IP-05 governance and later calendar support. Interval convention is exactly `[bar_open, bar_close)`: open included, close excluded; `bar_close-bar_open` must equal pinned timeframe duration, and open aligns to the UTC epoch. Calculations use exact `timedelta` modulo, not float seconds.

`MarketDataSchema` binds exact fingerprinted timeframe reference, schema identity/version, source event-time meaning OPEN or CLOSE, named open/close timestamp and OHLCV/finality source fields, and explicit volume semantic. Mappings must be unique; unknown extra source fields or missing required fields fail instead of disappearing. Mapping is versioned; `normalization_version` pins the implementation behavior. The current bounded contract version is v1, not a universal schema negotiation policy. A provider-specific format and authority remain IP-11/IP-13 decisions.

`MarketBar` carries typed ID/version, exact source/instrument/timeframe/schema references, normalization version, UTC open/close/availability/ingestion, `DecimalValue` OHLC and optional `DecimalValue` volume, its volume meaning, finality, source observation fingerprint reference, normalization provenance and optional exact superseded bar. Price geometry uses exact base-10 `Decimal` comparisons: high ≥ open/close/low, low ≤ open/close; negative prices are not globally prohibited. Volume must be ≥0 when present, but provider meaning is `BASE`, `QUOTE`, `CONTRACTS`, `SHARES`, `TICKS` or `PROVIDER_DEFINED`. Missing volume uses `ABSENT` and `None`; it is not zero and no conversion is implied. Binary float, nonfinite and malformed Decimal are refused upstream by Sprint 3 contracts. A still-forming `INCOMPLETE` bar can have availability before the scheduled close but cannot enter `finalized_only` membership; `FINAL` and `CORRECTED_FINAL` require availability ≥ close. No final bar can leak into a research cutoff at its close if source availability is later.

Bar business key is source identity + instrument identity + timeframe identity + bar open time; symbol alone is never identity. Exact source/instrument reference versions and fingerprints remain on the bar. A normalized bar is not raw data, a feature, signal or strategy result.

## Normalization, lineage, corrections and dataset

`normalize_bar` accepts only an `ACCEPTED` raw observation and a schema whose timeframe fingerprint matches the exact supplied `TimeframeIdentity`. It checks exact schema-field set, explicit raw event timestamp meaning, canonical UTC open/close strings, duration/alignment, strict decimal field types, finality and source availability. It neither alters raw history nor repairs bad geometry/timestamps/values. A `NormalizationResult` carries exact raw observation/schema/timeframe references, normalization version and bar. Correction lineage requires **both** raw exact `supersedes` reference and normalized exact bar `supersedes` reference with `CORRECTED_FINAL`; changing a historical bar makes a new ID/version/fingerprint. Transformation produces no resampled/aggregated bar and creates no derived indicator.

`classify_bars` groups exact series business keys independent of arrival order. Same key with equal declared bar content is DUPLICATE, different declared OHLCV/availability/finality is CONFLICT; singleton corrected bar is CORRECTION. Neither first nor last arrival is a truth rule. `classify_fixed_gaps` reports only **mechanical** discontinuity for bars of the same exact fixed-duration timeframe and scope: 10:00, 11:00, 13:00 1h bars report one mechanically absent interval. No bar is filled, and no holiday/session quality judgement is inferred. A zero-volume bar is not a missing bar.

Sprint 3 `DatasetManifest` is expressly observation-reference based and unchanged. `NormalizedBarManifest` is a separate domain-separated canonical type with exact sorted finalized bar refs, source/instrument/timeframe scope, schema, normalization version, pinned raw dataset-lock ref and provenance. Its dataset ID must be distinct from the raw snapshot ID by caller governance; no implicit conversion of raw manifests. Duplicate/conflicting business keys, reused ID/version, incomplete bars, mixed schema/normalization versions, empty membership and any bar available after cutoff block assembly. The existing `DatasetLock` binds exact normalized manifest fingerprint and cutoff, never `latest`. A raw lock supplied through `raw_dataset_lock_ref` is an exact fingerprint-bearing dependency; the bounded in-memory assembler does not fetch or cryptographically authenticate that upstream lock. Persistence, ownership and eligibility decisions remain governed downstream.

## Canonical bytes, compatibility and test anchors

Four explicit new typed-codec registrations—TimeframeIdentity, MarketDataSchema, MarketBar, NormalizedBarManifest—extend the existing `ai-quant-lab.canonical-json` representation v1 without changing its rules, old payloads or old golden vectors. Strict decoder rejects unexpected/missing governed fields, wrong type/namespace, duplicate keys and noncanonical timestamp/decimal values. Existing `fingerprint_record` uses encoded type domain separation and SHA-256 canonical bytes. Golden fixture has ten synthetic cases, including six pinned SHA-256 bar vectors; normal tests read them and never regenerate them. Matching hash compares content, **not** trusted source/authenticity/signature/authority (IP-02).

## Security and failure review

| Attack / failure | Bounded control | Remaining boundary |
| --- | --- | --- |
| Source spoofing / symbol ambiguity | Exact typed source/instrument/version/fingerprint on bar | Principal/signature trust IP-01/02 |
| Schema or timeframe confusion | Strict mapped field set, exact timeframe ref, event meaning and alignment | Venue-session calendar and real-source onboarding IP-05/11/13 |
| Timestamp look-ahead | Close ≠ availability; finalized cutoff uses availability | Provider clock trust, revisions/late data IP-05 |
| Float/decimal/OHLC corruption | Exact DecimalValue input and Decimal geometry; no positive-price heuristic | Instrument-specific price policy IP-11 |
| Gap concealment or fake zero volume | Mechanical gap findings; missing volume ≠ zero; no synthetic fill | Session calendar and completeness thresholds IP-05/11 |
| Duplicate poison / overwrite | Explicit DUPLICATE/CONFLICT; both fail finalized assembly | Provider conflict authority IP-11 |
| Incomplete leakage / correction erasure | FINAL requirement; exact raw+bar supersession refs | Competent release/revision policy IP-11 |
| Manifest/hash/provenance substitution | Exact sorted refs, domain-separated fingerprints, raw-lock/provenance bindings | Hash ≠ authenticity; custody/legal and signer IP-02/12 |
| Strategy/execution injection | Sprint 3 RawField semantic exclusions; no downstream consumer | EXE-01 stays closed |

No local CSV adapter is created. Even test-only CSV requires source/timezone/header/schema/path/custody and trust-boundary choices; the repository-owned typed synthetic fixtures cover the currently permitted scope. No untrusted arbitrary filesystem discovery, network, secrets or real user CSV is used.

## Implementation traceability and tests

| Component | Governed source | Requirement / tests | Failure |
| --- | --- | --- | --- |
| Timeframe / alignment | S7 Data Plan; S9 Validation; IP-05 | fixed/calendar and canonical labels; timeframe/alignment negatives | InvalidTimeframe |
| MarketDataSchema | S3 Artifact Contracts; S7 DAT-04 | exact version/field meaning; mapping/decoder negatives | SchemaMappingError |
| MarketBar / decimal / volume | S3 contracts; S7 quality | OHLC geometry, negative-price, missing-vs-zero and finality tests | InvalidOHLCGeometry/MarketDataError |
| Normalizer / temporal | S7 availability; Sprint 3 RawObservation | raw lineage, delayed availability, early final rejection | SchemaMappingError |
| Gap / duplicate / correction | S7 DP-10–12, DAT-03; Sprint 4 reconciliation | gap count, source/timeframe separation, conflict/correction history | Findings or BarConflict |
| Manifest / lock | Sprint 3 DAT-05; Sprint 8 exact lock | accepted finalized scope, order independence, cutoff, fingerprint tamper | NormalizedDatasetAssemblyError |
| Codec / golden / integrity | Sprint 2 canonical v1; Sprint 6 T04/T16/T25/T36 | round trips, six pinned SHA-256 vectors, tamper/duplicate-key attacks | InvalidSerialization/IntegrityMismatch |
| EXE-01 | Constitution, Sprint 11 execution isolation | `tests/test_governance_negative.py`; capability scan | PLANNED_CLOSED |

Focus uses synthetic fixture objects, no nondeterministic clock/network. Existing Foundation CI remains Python 3.12/3.13, format, lint, strict mypy, full pytest and execution isolation.

## All fourteen Phase 2 implementation preconditions

Source of exact IP IDs, owners, required decisions, default and tests: Sprint 12 review and `core/governance.py`. Technical code does not approve policy. Before and after counts remain RESOLVED 0, PARTIALLY_RESOLVED 5, OPEN 9, DEFERRED 0. Registry fail-closed defaults continue to apply unchanged.

| IP | Before → after | Technical progress; remaining competent decision | Domains still blocked |
| --- | --- | --- | --- |
| 01 | OPEN → OPEN | No principal auth; IAM + Security authentication/threat model | IAM, agents, commands |
| 02 | PARTIAL → PARTIAL | SHA-256 codec-integrity extended; GOV + Security signatures/trust roots | authoritative ART/EVI/AUD custody |
| 03 | OPEN → OPEN | No delegation/authority runtime; GOV + IAM binding policy | consequential IAM/mutations |
| 04 | PARTIAL → PARTIAL | Four typed market-data codecs and golden anchors; ART + DAT representation scope approval | unsupported data locks |
| 05 | PARTIAL → PARTIAL | Fixed timeframes, UTC alignment, availability/gap tests; STA + DAT clocks, vendor availability, calendars, late data | general DAT/STA/commands |
| 06 | OPEN → OPEN | No emergency runtime; GOV + humans roles/dual control | RSK/DEC/HUM/command |
| 07 | OPEN → OPEN | No approval runtime; GOV + IAM confirmation/expiry | decisions/commands |
| 08 | OPEN → OPEN | No freshness methodology; EVI + VAL + MON crosswalk | EVI/VAL/MON |
| 09 | OPEN → OPEN | No validation engine; VAL + GOV methods | VAL |
| 10 | OPEN → OPEN | No monitoring engine; MON + VAL + RSK thresholds | MON |
| 11 | PARTIAL → PARTIAL | Bar geometry, missing volume, duplicates, conflicts, incomplete and gaps; DAT + GOV provider semantics, thresholds and eligibility/acceptance authority | real-market DAT |
| 12 | OPEN → OPEN | Exact raw→bar→manifest/lock lineage; GOV + Legal + Data retention/licensing/privacy/deletion policy | real-data DAT/AUD ledgers |
| 13 | OPEN → OPEN | Only typed synthetic mapping; Security + IAM external/local CSV adapter trust model | external adapters |
| 14 | PARTIAL → PARTIAL | Versioned typed codecs, deterministic goldens and tests/CI; GOV + QA + AUD release gates | wave/production promotion |

## Implementation ADR register

| ID | Decision; no governance override |
| --- | --- |
| S5-ADR-01 | Unit/count/ID fixed timeframe is typed; 60m ≠ 1h by default. |
| S5-ADR-02 | Fixed UTC epoch alignment; calendar/session 1d remains unsupported. |
| S5-ADR-03 | Interval is [open,close), exact duration and epoch anchoring. |
| S5-ADR-04 | Bar business key is source+instrument+timeframe+open. |
| S5-ADR-05 | OHLC/volume use DecimalValue; geometry compares Decimal, never float. |
| S5-ADR-06 | No universal positive-price rule; negative historical prices can be structural. |
| S5-ADR-07 | Missing volume is absent, not zero; semantic units never guessed. |
| S5-ADR-08 | INCOMPLETE is representable but excluded from finalized-only membership. |
| S5-ADR-09 | Schema fields, timestamp meaning and normalization behavior are exact/versioned. |
| S5-ADR-10 | Normalization maps already-bar-shaped raw, does not repair/resample. |
| S5-ADR-11 | Mechanical fixed gap reports missing interval count, does not manufacture bars. |
| S5-ADR-12 | Same-key duplicate/conflict explicit, no order-selected winner. |
| S5-ADR-13 | Raw and bar correction lineage both required; old versions retained. |
| S5-ADR-14 | NormalizedBarManifest is separate from raw observation DatasetManifest. |
| S5-ADR-15 | Existing lock pins normalized manifest fingerprint and availability cutoff. |
| S5-ADR-16 | Strict typed codec registrations add types without changing canonical-json v1. |
| S5-ADR-17 | CSV/live adapters, calendar engine, dataframes, persistence and execution deferred. |

## Readiness and next bounded scope

With the full required gate passing: MARKET_DATA_SCHEMA_READY, TIMEFRAME_MODEL_READY (fixed UTC only), BAR_NORMALIZATION_READY, SYNTHETIC_BAR_DATASET_READY. LOCAL_CSV_ADAPTER_NOT_READY, REAL_MARKET_DATA_ADAPTERS_NOT_READY, EXPERIMENT_FOUNDATION_NOT_READY and EXECUTION_CLOSED remain. Suggested Sprint 6: strict *repository-owned synthetic* local CSV fixture adapter and import-validation contracts after governing local schema/clock/quality/custody boundaries; no real-user import or live APIs until independently permitted. This Sprint 5 draft does not approve that work.
