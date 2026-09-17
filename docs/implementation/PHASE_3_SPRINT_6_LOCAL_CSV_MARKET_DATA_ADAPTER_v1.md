# AI Quant Lab — Phase 3 Sprint 6 Local CSV Market Data Adapter v1.0

## Governed baseline and scope

Current `main` before any change: `068c05f1220d055378239c6214a8d68331c87caa`, PR #66 merged. Constitution v1.0: `50b61266f880cb9657b7f1b477d3d90825fe013f`. Sprint 5 core market-data contracts and canonical-json v1 remain unchanged. This is a synchronous standard-library-only import of explicitly named repository-owned **synthetic** CSV fixtures. It provides no source authorization, user-data onboarding, market-data acquisition, external filesystem authority, storage, trading feature, strategy, deployment or execution. `EXE-01 = PLANNED_CLOSED`.

## Boundaries and exact path

`CsvImportRequest` pins the existing `IngestionRequest`/`IngestionSession`, explicit fixture path/root, exact fingerprint-bearing schema/timeframe refs, normalized dataset/lock IDs and versions, provenance refs, optional expected file-byte SHA-256, and contract v1. A different session may produce the same semantic snapshot, but report equality includes session context. `LocalCsvInputAdapter.prepare()` validates the file and produces immutable `ParsedCsvFile` candidates and safe `CsvRowRejection` metadata. The adapter is structural `InputAdapter` only; it has no acceptance authority. `CsvImportKernel.import_fixture()` passes the frozen prepared candidates **through existing `IngestionKernel.ingest()`**, then through existing `normalize_bar()`, `classify_bars()`, `classify_fixed_gaps()` and `assemble_normalized_dataset()`; no second ingestion or normalization engine is created.

Allowed root must be an explicitly supplied `tests/fixtures/market_data` tree. The named path must be a lowercase `.csv` regular file inside its resolved root; reject `..`, URLs, absent files, directories, non-CSV files, direct symlinks and resolved symlink escapes. There is no glob, directory discovery, network fallback or arbitrary file importer. Current path checks occur before opening; a malicious concurrent local filesystem actor could race a path replacement, so this bounded fixture mechanism is **not** a security-reviewed adapter for arbitrary user files. Future real-file onboarding needs atomic open/descriptor-based controls and a competent IP-13 trust review.

## Dialect, encoding, header, schema and resource contract

Exact UTF-8, no BOM or encoding guessing. Python standard-library `csv.reader`, comma delimiter, double quote, strict malformed quoting, header required, case-sensitive exact names; header order is irrelevant. Reject duplicate/empty/space-padded/missing/unknown header names. No `csv.Sniffer`, formula evaluation or positional inference. Field names come from exact `MarketDataSchema`, plus mandatory `availability_time`; source and instrument are pinned by the ingestion request, never by filename or CSV text. One source, one instrument, one exact timeframe/schema per import. Unexpected extra row columns produce safe row rejection. Technical **test-scale** limits: 1,000,000 file bytes, 2,000 rows and 256 characters per field; these are not institutional production thresholds. LF and CRLF can yield equal semantic datasets while file-byte hashes differ.

CSV timestamps must be exactly `YYYY-MM-DDTHH:MM:SS.ffffffZ`; strict UTC parse/format roundtrip rejects naive, offsets, ambiguous local dates and whitespace. Both open and close are explicit, no derived close. Open must be fixed-UTC-epoch aligned; interval length must equal pinned timeframe. Availability comes from its own mandatory column; the injected deterministic clock supplies ingestion time. No default `availability = close` and no uncontrolled wall-clock `now`. `IngestionKernel` separately enforces event ≤ availability ≤ ingestion and exact availability cutoff. A finalized bar with availability before its close is row-rejected, not repaired. Event timestamp follows the pinned schema OPEN/CLOSE meaning, while legitimate research knowledge follows availability.

Decimal fields stay text through `DecimalValue.from_text`; never binary float. Empty/NaN/Infinity/malformed/space-padded required OHLC or volume reject the row. A schema with a volume column requires a value (including exact zero); a schema with `volume_field=None` represents **ABSENT**, not zero. Provider volume conversion is absent. Finality accepts only exact `final` or `incomplete` in this CSV contract. Synthetic corrected-final rows are deferred because the existing correction path requires exact predecessor references; row order cannot infer authority or correction history. `normalize_bar` structurally rejects inconsistent geometry; accepted raw remains attributable, and the report holds a safe exact raw reference in `CsvNormalizationRejection`, not a repaired price or arbitrary exception/payload text.

## Failure, reconciliation and dataset semantics

Unsafe path, oversize file/row count, encoding/BOM, malformed quoting, bad header, context/schema/timeframe/expected hash mismatch are **critical file-level failures**: no dataset. A malformed individual data row (width, field length, strict timestamp, interval, decimal, finality, empty field) yields reason/column/physical line only; valid rows continue. The physical line is diagnostic, not market identity. Deterministic candidate IDs derive from exact row fields plus occurrence number for identical physical content; file row order never chooses the winning conflicting market observation. The existing ingestion kernel explicitly quarantines duplicate/conflicting raw observations and fails closed if none remains accepted. Report status is `SUCCESS_WITH_REJECTIONS` for row/ingestion/normalization rejections, raw quarantine or incomplete bars; not a clean success. An all-rejected or all-incomplete import cannot lock a disguised empty finalized dataset.

Raw accepted-only `DatasetManifest`/`DatasetLock` are produced first. Each finalized `MarketBar` binds its exact raw observation ID/version/fingerprint and schema/timeframe/source/instrument/provenance. Incomplete bars remain visible but excluded from finalized membership. Same-key duplicate or conflict findings block normalized finalized assembly, never first/last-write-wins; raw reconciliations remain explicit. Mechanical fixed-duration gap findings are reported without filling, resampling or asserting venue-calendar defects. `NormalizedBarManifest` binds raw dataset lock exact fingerprint and finalized bar refs; the existing `DatasetLock` binds the normalized snapshot and availability cutoff. Current kernel can retain accepted raw that later fails OHLC normalization; it must not be claimed as eligible normalized data. Research eligibility and source economic trust require later competent governance, not this import.

The immutable **operational** `CsvImportReport` retains file digest/size, row count, safe row and normalization rejects, exact existing ingestion result/audit events, normalized and incomplete bars, findings, two manifests and locks, pinned request/session, and status. The CSV layer adds typed, codec-reconstructable `AuditEvent`s for import start, file validation, row rejection/acceptance, bar normalization, normalized dataset creation and completion, each attributable to an actor and file SHA; these events record outcomes but authorize nothing. A critical exception aborts rather than fabricating a completed report; a future persistent failure ledger still requires storage/retention governance. The report itself is not registered as a persistent governed codec type and therefore does not silently expand canonical-json v1. `semantic_snapshot` explicitly compares four existing canonical manifest/lock fingerprints, excluding file bytes and session identity. Report/file SHA-256 proves reproducible content comparison, **not trusted authorship, source identity, signature, permission or authority**. Same exact file, pinned refs/clock/cutoff and semantics replay identically; reordering independent bar rows, column order or CRLF can change the file SHA but preserve the semantic snapshot. No golden fixture is rewritten by tests.

## Security and trust review

| Attack | Bounded control | Remaining boundary |
|---|---|---|
| traversal/symlink/malicious filename | explicit resolved fixture root, suffix, regular-file check | concurrent filesystem races and arbitrary user paths need IP-13 review |
| oversized file/field/rows | conservative test-scale caps | no production scale policy |
| encoding/header/parser differential | strict UTF-8 without BOM, exact header, fixed dialect, strict quoting | no provider-specific schema approval |
| source/schema/timeframe spoof | exact fingerprint-bearing refs and existing kernel source/instrument checks | SHA is not signer authentication (IP-02) |
| timestamp/knowledge spoof | canonical UTC, pinned interval, availability column and kernel cutoff | vendor clock/availability claims unverified (IP-05) |
| decimal/OHLC corruption | exact DecimalValue, explicit normalization rejection | real source thresholds/quality authority open (IP-11) |
| duplicate/conflict/gap/incomplete poisoning | existing quarantine and bar findings; finalized-only lock | no institutional conflict resolution/market calendar |
| file hash substitution/provenance removal | optional pinned byte hash, exact raw/bar/locks, existing integrity verifier | trust root/retention/licensing unresolved (IP-02/12) |
| formula/strategy/execution field injection | exact headers/field set; data text never run as code | no external adapter, command or execution runtime |

## Implementation traceability and tests

| Component | Governed source | Requirement / test | Fail-closed path |
|---|---|---|---|
| allowed-root `LocalCsvInputAdapter` | S2 DAT-02 boundary; S7 DP-03–07 | explicit local fixture; path/adversarial tests | `UnsafeCsvPath` before import |
| file/header/UTF-8 parser | S3 artifact provenance; S7 source/raw | no silent drift; BOM/header/width/resource tests | `CsvFileFailure` or safe row reject |
| timestamp/Decimal parser | S7 DP-09; S3/5 temporal/decimal | knowledge cutoff, exact decimals; look-ahead/numeric tests | row reject or kernel temporal reject |
| schema/source/instrument/timeframe binding | S2 DAT-01/04; S5 market schema | exact typed refs; wrong binding/header tests | `CsvFileFailure` / kernel integrity failure |
| `CandidateObservation` / `RawObservation` | S4 ingestion; S7 DP-05–07 | parsed ≠ accepted; mixed/duplicate tests | kernel rejection/quarantine |
| `MarketBar`, gap/conflict findings | S5 bar semantics; S7 DP-08/11 | raw ≠ normalized; geometry/gap/conflict tests | safe normalization reject / assembly failure |
| raw and normalized manifests/locks | S3–5 dataset contracts; S7 DP-15/16 | exact cutoff/membership; replay/lineage/tamper/golden tests | no empty or conflicting finalized lock |
| operational report/file SHA | S3 AUD/EVI; Sprint 12 IP-12 | byte ≠ semantic; CRLF/order/golden tests | fingerprint mismatch fails before processing |
| execution isolation | Constitution, S2 EXE-01, S6 T37/38 | no strategy/order/broker; negative suite and diff scan | `PLANNED_CLOSED` |

Pinned golden `tests/golden/csv_import_valid_1h_v1.json` contains exact file SHA, three raw/bar SHA fingerprints, four manifest/lock SHA fingerprints and counts; tests never update it. Repository fixtures include valid 1H/4H, reordered rows, mixed rejection and cutoff. Other adversarial fixture variants are created in temporary **test** fixture roots, not committed market data. All are synthetic.

## Fourteen implementation preconditions — BEFORE → AFTER

The actual registry in `core/governance.py` and Phase 2 Sprint 12 review supplies IDs, owners, domains, fail-closed defaults and test families. Neither file access nor a hash is institutional authorization. Statuses remain: **RESOLVED 0→0; PARTIALLY_RESOLVED 5→5; OPEN 9→9; DEFERRED 0→0**.

| ID | Before → after | Technical progress / remaining decision | Blocked future domain |
|---|---|---|---|
| IP-01 | OPEN → OPEN | none; competent IAM authentication model | command/agents |
| IP-02 | PARTIAL → PARTIAL | existing SHA verifies records; signer authority/trust roots unresolved | trusted provenance/authorship |
| IP-03 | OPEN → OPEN | no authority inferred from file/path/session; delegated/revoked bindings require GOV/IAM | consequential mutations |
| IP-04 | PARTIAL → PARTIAL | reuse canonical raw/bar/manifest/lock and pinned import vector; persistent report representation scope awaits ART/DAT | unsupported canonical persistence |
| IP-05 | PARTIAL → PARTIAL | strict UTC CSV timestamps, deterministic clock, availability cutoff; vendor clocks/late data/calendar policy awaits STA/DAT | real-source temporal acceptance |
| IP-06 | OPEN → OPEN | no HALT/RELEASE runtime; GOV/human emergency roles unresolved | risk/decision/emergency |
| IP-07 | OPEN → OPEN | no approval/confirmation/expiry; GOV/IAM decision unresolved | consequential commands |
| IP-08 | OPEN → OPEN | no freshness crosswalk; EVI/VAL/MON decision unresolved | evidence/validation/monitoring |
| IP-09 | OPEN → OPEN | no validation method; VAL/GOV decision unresolved | validation |
| IP-10 | OPEN → OPEN | no monitoring methods; MON/VAL/RSK decision unresolved | monitoring |
| IP-11 | PARTIAL → PARTIAL | strict synthetic CSV quality, existing duplicate/quarantine and bar findings; provider thresholds/acceptance authority awaits DAT/GOV | real-source quality and promotion |
| IP-12 | OPEN → OPEN | file SHA + exact raw/bar/lock chain; retention/privacy/licensing/legal awaits GOV/Legal/Data | real-data custody/retention |
| IP-13 | OPEN → OPEN | bounded fixture path/encoding/resource gates; arbitrary user/external adapters need Security/IAM trust approval | real CSV/live/network adapters |
| IP-14 | PARTIAL → PARTIAL | golden/replay/negative test evidence under existing CI; release criteria await GOV/QA/AUD | production release/wave promotion |

## Implementation ADRs and limited readiness

| ADR | Decision / explicit non-decision |
|---|---|
| P3S6-ADR-01 | explicit repository fixture root and named path; no discovery/URL; not a general user-file authority |
| 02 | fixed standard-library comma/double-quote strict dialect; no sniffing |
| 03 | UTF-8 strict; reject BOM/guessing |
| 04 | case-sensitive exact-name header mapping, order irrelevant, unknown names rejected |
| 05 | no whitespace trimming of headers, timestamps or decimals |
| 06 | canonical microsecond UTC Z only; no local offset guessing |
| 07 | schema without volume is ABSENT; present column requires exact value including zero |
| 08 | injected deterministic clock for ingestion; no uncontrolled wall clock |
| 09 | exact file-byte SHA separate from source authenticity and semantic dataset fingerprints |
| 10 | header/file trust failures abort; safe per-row contract failures continue |
| 11 | single exact source/instrument/timeframe/schema per request |
| 12 | raw kernel retains quarantine and rejection; no first/last conflict winner |
| 13 | candidate semantic identity and canonical manifest ignore arrival order where irrelevant; physical line remains diagnostic |
| 14 | normalized manifest binds exact raw lock; no resample/repair/incomplete membership |
| 15 | operational immutable report is not a new canonical persistent codec; future version decision required to persist it |
| 16 | conservative file/row/field limits only for synthetic fixture safety, not market policy |
| 17 | correction row semantics deferred until exact predecessor authority/reference, never inferred from ordering |

`LOCAL_CSV_ADAPTER_READY` and `SYNTHETIC_CSV_IMPORT_READY` mean **repository-owned fixtures only**. `NORMALIZED_DATASET_PIPELINE_READY` means only bounded synthetic finalized bars. `REAL_HISTORICAL_CSV_IMPORT_NOT_READY`, `REAL_MARKET_DATA_ADAPTERS_NOT_READY`, `EXPERIMENT_FOUNDATION_NOT_READY`, `EXECUTION_CLOSED`. No source economic reliability or research eligibility is claimed.

Recommended Sprint 7: assess IP-05/11/12/13 and choose controlled real historical CSV onboarding **only after** competent source/license/availability and trust decisions, or instead an immutable local dataset store for synthetic governed artifacts. Neither option grants strategy, backtest, live feed or execution authority.
