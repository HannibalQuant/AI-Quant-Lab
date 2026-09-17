# AI Quant Lab — Phase 3 Sprint 8 Controlled Real CSV Onboarding v1.0

## 1. Baseline

The exact starting `main` was
`dac93b61b1a5c53ae510188866304432d87d583f`, the merge commit of PR #68. PR #68
was verified merged before implementation. The constitutional baseline remains tag
`v1.0`, commit `50b61266f880cb9657b7f1b477d3d90825fe013f`. Phase 2 artifacts, Phase 3
Sprint 1–7 reports, prior golden files and all other historical governed artifacts were
inspected and remain unchanged.

The implementation started on branch `phase-3/controlled-real-csv-onboarding` from
that exact commit. At baseline the precondition register contained `RESOLVED 0`,
`PARTIALLY_RESOLVED 5`, `OPEN 9`, `DEFERRED 0`; `EXE-01 = PLANNED_CLOSED`.

## 2. Purpose and bounded capability

Sprint 8 adds one synchronous, local-only path for technical admission of one explicit
historical CSV file under one exact source declaration. It can record that the exact
file was evaluated and admitted under the declared contract. It cannot establish that
the provider, declaration, permission claim or market data is authentic, legally
usable, research eligible, validated or production approved.

The governing separations are explicit:

- `EXTERNAL FILE != TRUSTED SOURCE`;
- `PARSED CSV != ADMITTED DATASET`;
- `VALID FORMAT != VALID MARKET DATA`;
- `PERSISTED != ACCEPTED`;
- `DATA AVAILABLE != RESEARCH ELIGIBLE`;
- `ADMITTED != TRUSTED`;
- `RESEARCH ELIGIBLE != EXPERIMENT AUTHORIZED`;
- `EXPERIMENT AUTHORIZED != VALIDATED`;
- `VALIDATED != DEPLOYMENT AUTHORIZED`;
- `DEPLOYMENT AUTHORIZED != EXECUTION`.

## 3. Non-goals and execution closure

There is no URL, downloader, HTTP/WebSocket client, exchange/broker/vendor SDK,
stream, scheduler, cloud storage, database, recursive scan or wildcard bulk import.
There is no feature, indicator, signal, strategy, experiment, backtest, optimizer,
walk-forward, Monte Carlo, validation, monitoring, portfolio, paper/live trading or
execution capability. Runtime dependencies remain empty. No parsed or persisted data
is automatically promoted to research use. `EXE-01 = PLANNED_CLOSED`.

## 4. External-file threat model and input boundary

`CsvInputScope.CONTROLLED_HISTORICAL` extends the existing local CSV adapter without
creating a second parser. The caller must provide an existing, absolute, non-symlink
root and one absolute `.csv` path below it. The adapter does not scan directories.

The boundary rejects URL-like paths, `..`, outside-root resolution, a symlink root,
direct file symlinks, missing/non-regular inputs, extensions other than lowercase
`.csv`, files over 1,000,000 bytes, more than 2,000 rows, lines over 4,096 bytes,
more than 32 columns, fields over 256 characters, strict-UTF-8 failures, BOM, NUL and
unsupported control characters. CSV parsing remains strict for quoting and row width.
Content is never executed, evaluated, passed to a shell or used to load code. Formula
mitigation is not applicable because this sprint has no spreadsheet export; hostile
text remains bounded and is never executed.

The caller-supplied allowed root is a local trust anchor, not proof of operator
authority. A malicious concurrent filesystem administrator remains outside the
application threat boundary.

## 5. Source declaration

`RealCsvSourceDeclaration` is a frozen, versioned, canonically encoded governed
record. It binds exact fingerprint-bearing references to `SourceIdentity`,
`InstrumentIdentity`, `TimeframeIdentity` and `MarketDataSchema`, plus:

- declared provider and market;
- acquisition method (`operator_local_file` only in v1) and optional declared
  acquisition time when actually known;
- UTC timestamp and source-availability semantics;
- exact sorted column mapping;
- positive-or-signed price domain plus exact OHLC, volume and finality semantics;
- missing-data, duplicate and ordering policies;
- declared permission and license reference;
- retention, deletion and redistribution declarations;
- exact operator ID and provenance note.

The provider text must equal the governed `SourceIdentity`; the source must be
`FILE_SNAPSHOT`, not a synthetic fixture. Filename never supplies provider, source,
instrument, market, timeframe or permission authority.

## 6. Permission, licensing and retention boundary

`SourcePermissionState` records `DECLARED_PERMITTED`, `DECLARED_RESTRICTED`,
`UNKNOWN` or `PROHIBITED`. Only `DECLARED_PERMITTED` can reach `ADMITTED` in v1;
restricted/unknown is quarantined and prohibited is rejected. These are operator
declarations, not legal findings or independently verified licenses.

`RetentionClassification` records declared local-only, declared restricted or
unknown. Unknown produces `INCOMPLETE`. License notes and deletion/redistribution
restrictions are immutable text evidence. The system provides no legal inference,
external upload, redistribution, automated retention, deletion or recovery workflow.

## 7. File identity

Before row admission the existing adapter reads bounded bytes and records:

- lowercase SHA-256 of the exact bytes;
- exact byte size;
- original basename;
- exact path relative to the allowed root;
- caller-supplied immutable admission-attempt ID;
- canonical parser/codec versions and deterministic ingestion-configuration fingerprint;
- injected deterministic ingestion time.

The parser request is then pinned to the computed file digest before ingestion. The
same bytes have the same content digest across filenames, while basename and bounded
path remain explicit provenance. Reusing a filename with different bytes produces a
different file identity. Hash identifies evaluated bytes; it does not authenticate a
provider or signer.

## 8. CSV and parser contract

Sprint 8 reuses `LocalCsvInputAdapter`, `CsvImportKernel`, `IngestionKernel`, existing
typed data contracts and canonical integrity functions. It introduces no parallel CSV
parser. The exact schema must contain declared open/close timestamps, OHLC, optional
volume, finality and explicit `availability_time` columns.

The combined existing and Sprint 8 gates reject or quarantine duplicate/missing/
unknown headers, malformed quoting or width, malformed timestamps/decimals, NaN,
Infinity, invalid intervals/alignment, unsupported finality, invalid OHLC geometry,
incomplete bars, duplicate/conflicting timestamps, out-of-order events and configured
gap-policy violations. There are no implicit provider thresholds. Missing intervals
may only be admitted when the declaration explicitly selects `RECORD_GAPS`; the
finding is preserved.

## 9. Temporal semantics — IP-05

Admission requires `BAR_OPEN_AND_CLOSE_UTC`, the existing canonical microsecond `Z`
format, deterministic timeframe alignment and
`EXPLICIT_SOURCE_AVAILABILITY_UTC`. Ambiguous timezone semantics are `UNSUPPORTED`;
unknown availability is `QUARANTINED`. The pipeline never fabricates availability
time and never substitutes its injected ingestion time for source availability.

The record keeps ingestion time as a separate operational coordinate. This bounded
rule does not resolve vendor latency, late corrections, exchange calendars, clock
trust or institutional knowledge-time policy; IP-05 remains partial.

## 10. Data-quality technical admission — IP-11

Technical admission requires exact header/schema binding, complete deterministic
parse, strictly increasing unique event times, accepted ingestion records, valid OHLC
normalization, no duplicate/conflicting bars, no incomplete bars, and the declared gap
policy. Findings are sorted, unique and immutable in the admission record.

`ADMITTED` means only that these bounded checks passed under the declared contract.
It is stored alongside `NOT_TRUSTED` and `NOT_RESEARCH_ELIGIBLE`. No universal market
quality, provider acceptance, reconciliation threshold or research suitability is
declared; IP-11 remains partial.

## 11. Admission states and authority separation

`CsvAdmissionStatus` contains `ADMITTED`, `REJECTED`, `QUARANTINED`, `INCOMPLETE`
and `UNSUPPORTED`. These are technical outcomes, not aliases for trusted, validated,
research-approved or production-approved states. Non-admitted records cannot contain
dataset references. An admitted record must contain all four exact dataset references.

`CsvTrustState` has only `NOT_TRUSTED` and `ResearchEligibilityState` has only
`NOT_RESEARCH_ELIGIBLE`. Contract construction fails if stronger authority is
attempted. No success path changes execution state.

## 12. Provenance model and exact lineage

The implemented chain is:

`external CSV bytes -> file SHA/size/path -> RealCsvSourceDeclaration ->`
`RealCsvAdmissionRecord -> parse/ingestion result -> RawObservation membership ->`
`DatasetManifest -> raw DatasetLock -> MarketBar -> NormalizedBarManifest ->`
`normalized DatasetLock -> LocalDatasetRepository`.

The source declaration is a separate immutable provenance object so manifests can
bind its exact fingerprint without a circular hash. All observation, manifest, lock
and normalization provenance references must equal that exact declaration reference.
The post-import admission record binds the file identity and exact fingerprint-bearing
references to both manifests and both locks. It also binds canonical parser/codec
versions and a deterministic fingerprint of the IDs, references, cutoff, actor,
schema, timeframe, normalization and dataset/lock configuration used by ingestion;
the physical path remains separately recorded context rather than authority.

`verify_real_csv_lineage()` checks the declaration fingerprint, evaluated file hash,
all four admission-to-dataset references and manifest/lock provenance, then delegates
the raw-observation/source/instrument/bar/normalized chain to Sprint 7
`verify_dataset_lineage()`. Changed bytes, declaration or dataset linkage fail closed.
The function verifies integrity and lineage, not authenticity or permission truth.

## 13. Persistence integration

Sprint 8 reuses `LocalDatasetRepository`. Its supported set is minimally extended by
`RawObservation`, `MarketBar`, `RealCsvSourceDeclaration` and
`RealCsvAdmissionRecord`, all using canonical JSON v1, the existing fingerprint
algorithm, type/version-separated immutable keys and strict typed reload. Admitted
results store the declaration, every accepted raw observation, raw manifest and lock,
every finalized market bar, normalized manifest and lock, then the admission record.
Non-admitted policy outcomes store only the declaration and outcome record.

New deterministic paths are:

```text
<root>/objects/real-csv-source-declaration/v1/<sha256>.json
<root>/objects/raw-observation/v1/<sha256>.json
<root>/objects/market-bar/v1/<sha256>.json
<root>/objects/real-csv-admission-record/v1/<sha256>.json
```

There is no mutable latest/current alias, catalog, database or overwrite. Multi-object
admission is not a database transaction: an I/O failure can leave a prefix of valid
immutable objects, but without a final admitted record that prefix grants no admission
authority. Sprint 7 per-object exclusive creation, fsync and race limitations remain.

## 14. Traceability

| Constitutional chain | Implementation component | Evidence / failure path |
|---|---|---|
| principle -> explicit source contract | `RealCsvSourceDeclaration` | exact binding tests; mismatched source rejects |
| requirement -> local hostile-file boundary | `CsvInputScope.CONTROLLED_HISTORICAL` | traversal/symlink/type/size/encoding tests |
| file -> exact identity | bounded byte read + SHA-256 | same/different bytes and filename tests |
| declaration -> parser configuration | `_validate_bindings` | provider/schema/operator/provenance mismatch fails |
| parse -> raw observations | existing `LocalCsvInputAdapter` / `IngestionKernel` | corruption and rejection tests |
| raw -> normalized dataset | existing `CsvImportKernel` | OHLC/duplicate/order/gap tests |
| dataset -> immutable custody | `LocalDatasetRepository` | persisted typed reload tests |
| file -> declaration -> dataset | `RealCsvAdmissionRecord` / `verify_real_csv_lineage` | changed file/declaration/linkage tests |
| state -> authority | `NOT_TRUSTED`, `NOT_RESEARCH_ELIGIBLE` | governance tests and frozen enums |
| execution | no execution component | governance-negative suite and prohibited scan |

This supplies the requested
`CONSTITUTION -> PRINCIPLE -> REQUIREMENT -> MODULE -> ARTIFACT -> WORKFLOW -> STATE ->`
`AUTHORITY -> EVIDENCE -> TEST -> FAILURE PATH -> AUDIT RECORD -> IMPLEMENTATION`
trace without using storage or status as authority.

## 15. Tests and golden evidence

`tests/test_real_csv_onboarding.py` adds 29 focused tests (with parameterization) for:

- valid source declaration, file identity, deterministic parse, manifests/locks,
  immutable persistence/reload and exact lineage;
- same/different bytes and same/different filenames;
- relative/outside/traversal paths, direct and escaping symlinks, FIFO/non-regular
  inputs, extension and size rejection;
- malformed UTF-8, NUL/control characters, quoting, duplicate/missing/extra headers;
- pathological line/column/field bounds, malformed timestamp/numeric, NaN/Infinity,
  nonpositive declared-price-domain values, invalid OHLC, duplicate, conflicting and
  out-of-order timestamps, timeframe and volume-semantics mismatch;
- explicit UTC, unknown availability, ambiguous time, permission and retention gates;
- unchanged `NOT_TRUSTED`, `NOT_RESEARCH_ELIGIBLE` and execution closure;
- wrong source declaration, changed file linkage and typed canonical reload.

The repository-owned fixture
`tests/fixtures/real_csv/repository_owned_external_style_1h.csv` contains three tiny
synthetic external-style bars and no vendor data. The read-only golden
`tests/golden/real_csv_onboarding_v1.json` pins file SHA-256 and size, source,
instrument and timeframe IDs, row count, admission status, ingestion-configuration,
declaration, raw dataset/manifest/lock, normalized manifest/lock and admission
fingerprints.
No prior golden file was changed or regenerated.

Implementation-time Python 3.12 evidence before PR creation:

- focused Sprint 8: **29 passed**;
- full suite: **273 passed**;
- `ruff format --check .`: passed;
- `ruff check .`: passed;
- strict `mypy`: passed;
- governance-negative: **14 passed**;
- GitHub Actions: pending Draft PR push (Python 3.12 and 3.13 matrix preserved).

## 16. Preconditions — BEFORE -> AFTER

Counts remain **RESOLVED 0 -> 0; PARTIALLY_RESOLVED 5 -> 5; OPEN 9 -> 9;
DEFERRED 0 -> 0**. Descriptions were aligned to evidence; no status changed.

| ID | Before -> after | Sprint 8 evidence / remaining authority |
|---|---|---|
| IP-01 | OPEN -> OPEN | operator ID is attribution, not authenticated principal authority |
| IP-02 | PARTIAL -> PARTIAL | hashes detect changed canonical/file bytes; no signature, trust root or provider authenticity |
| IP-03 | OPEN -> OPEN | declaration, path and ID grant no delegation or revocation authority |
| IP-04 | PARTIAL -> PARTIAL | two versioned CSV records persist/reconstruct canonically; broader representation authority open |
| IP-05 | PARTIAL -> PARTIAL | explicit UTC/availability required and ingestion remains distinct; calendars, lateness and clock trust open |
| IP-06 | OPEN -> OPEN | no emergency, release or reactivation runtime |
| IP-07 | OPEN -> OPEN | no approval, confirmation or expiry authority |
| IP-08 | OPEN -> OPEN | technical admission is not evidence freshness or validation |
| IP-09 | OPEN -> OPEN | no validation methodology implemented |
| IP-10 | OPEN -> OPEN | no monitoring methodology implemented |
| IP-11 | PARTIAL -> PARTIAL | bounded declared-source checks added; universal/provider quality acceptance remains open |
| IP-12 | OPEN -> OPEN | permission/retention/restriction declarations recorded; legal verification and lifecycle policy open |
| IP-13 | OPEN -> OPEN | one local file adapter is bounded; authenticated operator and broader adapter threat model open |
| IP-14 | PARTIAL -> PARTIAL | golden, hostile-input, persistence and lineage evidence added; release authority remains open |

## 17. Readiness and blockers

| Capability | State |
|---|---|
| Controlled local real CSV pathway | `CONTROLLED_REAL_CSV_ONBOARDING_READY` |
| Exact external file identity | `EXTERNAL_FILE_IDENTITY_READY` |
| Versioned source declaration | `SOURCE_DECLARATION_READY` |
| Bounded technical admission | `REAL_CSV_TECHNICAL_ADMISSION_READY` |
| File-to-dataset provenance | `REAL_DATA_PROVENANCE_READY` |
| Immutable admitted-data custody | `IMMUTABLE_REAL_DATA_CUSTODY_READY` |
| Research dataset eligibility | `RESEARCH_DATASET_ELIGIBILITY_NOT_READY` |
| Experiment foundation | `EXPERIMENT_FOUNDATION_NOT_READY` |
| Backtesting | `BACKTESTING_NOT_READY` |
| Validation | `VALIDATION_NOT_READY` |
| Execution | `EXECUTION_CLOSED` |

There are no blockers for the bounded technical pathway. Open IP-01/IP-02/IP-05/
IP-11/IP-12/IP-13/IP-14 decisions block authenticated source trust, legal approval,
research eligibility, institutional quality acceptance and production use.

## 18. Durability and concurrency limits

Sprint 7 per-object semantics apply. Identical concurrent immutable creation converges
where local hard-link semantics are reliable and conflict fails closed. There is no
cross-object transaction, lock manager, WAL, distributed consistency, HA, backup,
restore or disaster recovery. Filesystem and allowed-root integrity are external
assumptions. No durability claim exceeds the bounded local fsync sequence.

## 19. Final verification boundaries

The executable diff adds no network import, external API, broker/exchange adapter,
credential, strategy, signal, backtest, optimizer, capital allocation, monitoring,
orchestration, paper/live trading or execution route. There is no fabricated
availability timestamp, filename-derived authority, silent permission promotion,
mutable pointer, hidden overwrite or automatic research promotion. Historical
governed artifacts and golden files remain byte-identical.

## 20. Sprint disposition

`PHASE 3 SPRINT 8 COMPLETE WITH OPEN PRECONDITIONS`

This disposition applies only after all final local quality gates and the Draft PR CI
matrix pass. It describes bounded technical onboarding, not source trust, legal
approval, research readiness or production authorization.

## 21. Recommended Sprint 9 — discussion only

Do not begin experiments or backtesting. Recommend a governed **Research Dataset
Eligibility & Data Quality Acceptance Policy** sprint that consumes exact Sprint 8
admission records and addresses the remaining competent-authority decisions in
IP-05, IP-11, IP-12 and IP-13: source-specific late-data/calendar semantics,
provider-quality acceptance, license/retention verification and authenticated operator
admission. A catalog/query layer may follow only if it preserves exact immutable keys
and does not become a mutable authority alias.
