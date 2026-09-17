# AI Quant Lab — Phase 3 Sprint 7 Immutable Local Dataset Store v1.0

## 1. Governed baseline and scope

The exact starting `main` was
`9870842d1dd1efaabe8a7af718e87f4483e41554`, the merge commit of PR #67.
The constitutional baseline remains tag `v1.0`, commit
`50b61266f880cb9657b7f1b477d3d90825fe013f`. PR #67 was verified merged and no
open Phase 3 Sprint 7 PR existed before implementation. Phase 3 Sprints 1–6 and
all historical governed artifacts remain unchanged.

Sprint 7 adds a synchronous, standard-library-only, bounded local repository for
already-governed synthetic dataset records. It adds no data acquisition, arbitrary
user-file onboarding, source authorization, database, network, catalog query engine,
experiment, strategy, backtest, optimizer, deployment or execution capability.
`EXE-01 = PLANNED_CLOSED`.

The governing separations are preserved:

- `OBJECT IDENTITY != STORAGE LOCATION`;
- `DATASET != DATASET LOCK`;
- `HASH != AUTHENTICITY`;
- `PERSISTED != TRUSTED`;
- `LOAD != ACCEPT`;
- `STORAGE != AUTHORITY`;
- no mutable latest;
- no silent overwrite;
- no last-write-wins.

## 2. Architecture and supported object scope

`LocalDatasetRepository` reuses the existing canonical JSON v1 `encode`/`decode`
contracts and `fingerprint_record`/`verify_integrity`. It supports exactly:

- `DatasetManifest`;
- `DatasetLock`;
- `NormalizedBarManifest`.

`RawObservation`, `MarketBar`, `CsvImportReport`, provenance envelopes, audit
envelopes and other types are not silently added to the persistent object scope.
`MarketBar` remains an explicit input to lineage verification; it is not persisted by
this bounded repository. The operational `CsvImportReport` remains outside the
canonical persistent registry, as established in Sprint 6.

The exact flow is:

`governed object -> canonical typed bytes -> SHA-256 fingerprint -> immutable key ->`
`exclusive local creation -> verified read -> typed reconstruction -> integrity check`.

No parallel dataset model, serializer or integrity algorithm is introduced.

## 3. Explicit root and repository layout

The caller must provide two absolute `Path` values:

- `allowed_root`: an existing non-symlink trust boundary;
- `root`: the exact repository directory below that boundary.

There is no global default, home discovery, environment-variable lookup, URL, remote
filesystem or network fallback. Relative paths, `..`, outside-root resolution,
non-directory roots and symlink roots fail closed.

The deterministic layout is:

```text
<root>/
  objects/
    dataset-manifest/
      v<object-version>/
        <sha256-hex>.json
    dataset-lock/
      v<object-version>/
        <sha256-hex>.json
    normalized-bar-manifest/
      v<object-version>/
        <sha256-hex>.json
```

There is no `latest`, `current`, mutable alias, index or catalog state file. Raw and
normalized locks share the existing `DatasetLock` type but remain different exact
objects with different IDs, fingerprints and immutable keys.

## 4. Addressing and identity

`RepositoryObjectKey` is exactly:

`StoredObjectType + ObjectVersion + canonical typed fingerprint`.

The canonical type envelope provides domain separation. The fingerprint is encoded
as a lowercase SHA-256 token and the resulting filename is strictly
`<64-lowercase-hex>.json`. Object ID is retained in the canonical object and write
result but does not replace the content address. Directory names never infer lineage,
authority, acceptance or dataset parentage.

The same exact object produces the same key after a new process-like repository
construction and regardless of the order in which independent objects are stored.
Different content produces a different key. A cryptographic collision is not treated
as a permitted overwrite.

## 5. Write semantics

`store()` returns immutable `RepositoryWriteResult` with exact key, object ID,
fingerprint, canonical byte size and one of:

- `STORED_NEW`;
- `ALREADY_PRESENT_IDENTICAL`;
- `REJECTED_CONFLICT` in the typed `RepositoryConflict` failure.

An existing destination is read and compared byte-for-byte. Identical bytes are an
explicit idempotent outcome. Different bytes fail closed and remain untouched. The
repository never repairs, replaces or selects a last writer.

The bounded atomic creation sequence is:

1. encode and verify the governed object in memory;
2. create a private random temporary file in the exact destination directory;
3. write canonical bytes, flush and `fsync` the temporary file;
4. atomically hard-link it into a previously absent immutable destination;
5. `fsync` the destination directory on platforms exposing `O_DIRECTORY`;
6. remove the temporary name.

`os.replace` is deliberately not used. Destination creation by hard link is exclusive:
it cannot overwrite an existing name. If another writer wins the creation race, the
loser verifies the winner's exact bytes and returns identical or conflict.

## 6. Read semantics

`load(key, expected_type)` performs:

1. exact typed-key validation;
2. deterministic path resolution below the configured root;
3. no-follow regular-file open where the platform provides `O_NOFOLLOW`;
4. bounded byte read;
5. strict UTF-8 and canonical JSON v1 decode;
6. exact typed reconstruction with duplicate/unknown-field rejection;
7. exact object-version comparison;
8. canonical fingerprint recomputation and comparison with the key;
9. exact re-encoding comparison;
10. `FOUND_VERIFIED` result.

Typed failures distinguish not-found, unsafe path, type mismatch, version mismatch,
integrity/representation failure, unsupported type and immutable conflict. Missing is
never substituted for corrupt. No closest match, migration, auto-upgrade, permissive
parse or partially trusted return exists.

## 7. Exact lineage verification

`verify_dataset_lineage()` verifies the existing chain without creating policy:

`DatasetManifest -> raw DatasetLock -> MarketBar references ->`
`NormalizedBarManifest -> normalized DatasetLock`.

It requires:

- raw lock dataset and manifest references equal the exact raw manifest fingerprint;
- normalized manifest raw-lock reference equals the exact raw lock fingerprint;
- normalized lock dataset and manifest references equal the exact normalized manifest;
- normalized bar membership equals the exact provided bar references;
- every bar source observation occurs in the raw manifest;
- every bar source and instrument occurs in the raw manifest's exact scope;
- normalized source, instrument and timeframe scope matches the bars;
- normalized schema and normalization-version scope matches the bars.

The function returns fingerprints as technical verification evidence. It does not
declare source authenticity, data quality acceptance, research eligibility or
authorization. Lineage is never inferred from filenames or directories.

## 8. Security and fail-closed boundaries

| Threat | Bounded control | Remaining boundary |
|---|---|---|
| traversal/outside root | absolute paths, reject `..`, resolved containment | allowed root is caller-supplied trust anchor |
| root/path symlink | direct symlink rejection and component checks | malicious concurrent directory replacement is not fully eliminated |
| object symlink | precheck plus `O_NOFOLLOW` where available | weaker platforms retain a documented pre-open race |
| unsafe filename/type/version | closed enum, typed version, strict fingerprint-derived filename | no arbitrary file lookup API |
| malformed/duplicate/extra JSON | existing strict codec and canonical byte equality | no repair or migration |
| tamper/truncation/wrong fingerprint | decode, exact reconstruction, fingerprint and re-encode checks | hash is not signer authenticity |
| overwrite/collision | exclusive hard-link creation and byte comparison | filesystem integrity remains an external assumption |
| oversized object | 1,000,000-byte bounded object limit | not an institutional scale policy |
| mutable latest alias | no alias/index API or mutable pointer | filesystem administrators remain outside application authority |

Unexpected `.txt` files or other directory entries are not discovered or treated as
objects. Exact lookup always addresses the derived `.json` path.

## 9. Concurrency boundary

This is not a multi-process transactional storage engine. For a basic local creation
race on a filesystem supporting atomic hard links:

- exactly one absent destination is created;
- an identical competing writer converges to `ALREADY_PRESENT_IDENTICAL`;
- a conflicting competing writer fails closed.

The code does not claim protection against a malicious actor concurrently replacing
ancestor directories, filesystem rollback, hostile mount behavior or operations on a
filesystem without reliable local hard-link semantics. There are no locks, leases,
distributed coordination or last-write-wins behavior.

## 10. Durability boundary

File and directory `fsync` are used where the local platform exposes the required
semantics. This improves the bounded write sequence but is not a claim of database
transactions, WAL, distributed consistency, HA, backup/restore or disaster recovery.
There is no garbage collection or deletion API. Operational retention and recovery
policy remain governed work under IP-12.

## 11. No-real-data and no-experiment boundary

Sprint 7 persists only already-governed, repository-owned synthetic dataset artifacts.
It does not authorize or import SOL, ETH, XRP, ATOM, XAG, NAS100, broker, exchange,
user or other external historical data. Persistence cannot turn an unauthorized input
into an accepted dataset.

No feature, indicator, signal, strategy, experiment, backtest, optimizer,
walk-forward, Monte Carlo, PBO, Deflated Sharpe, portfolio, monitoring, orchestration,
paper/live trading or execution capability is present. Runtime dependencies remain
empty. No database, cloud SDK or network client is added.

## 12. Traceability

| Governed chain | Sprint 7 implementation | Evidence and failure path |
|---|---|---|
| Constitution -> identity/integrity separation | exact typed codecs and content key | golden/key tests; unsupported type rejects |
| Requirement -> module | `core/dataset_store.py` | focused Sprint 7 suite |
| DatasetManifest -> canonical bytes | existing `encode` | byte equality and golden SHA |
| canonical bytes -> fingerprint | existing `fingerprint_record` | tamper/wrong-fingerprint tests |
| fingerprint -> immutable key | `repository_key` | deterministic/restart/order tests |
| key -> stored object | exclusive hard-link creation | idempotence/concurrency/conflict tests |
| stored object -> verified read | `LocalDatasetRepository.load` | corrupt/type/version/UTF-8/JSON tests |
| raw -> normalized lineage | `verify_dataset_lineage` | exact and corrupt-parent/bar tests |
| state -> authority | verified state only; no approval state | `PERSISTED != TRUSTED`, `LOAD != ACCEPT` |
| audit record | write/read result contracts | operational result only, no authority claim |
| execution boundary | no executable trading capability | governance-negative suite and diff scan |

## 13. Tests and golden evidence

`tests/test_dataset_store.py` contains 28 focused tests covering the required positive
and negative families, including parameterized supported-object and corruption cases:

- manifest, lock and normalized-manifest store/load;
- exact typed round trip, bytes, fingerprint and version;
- deterministic key, idempotence and restart-like reload;
- storage-order independence;
- identical concurrent creation convergence;
- exact raw-to-normalized lineage and corrupt parent/bar rejection;
- malformed/truncated/extra/duplicate/non-UTF-8 representation rejection;
- wrong requested/stored type, version and fingerprint;
- attempted overwrite conflict without mutation;
- exact not-found and unexpected extension behavior;
- traversal, outside root, relative root, direct symlink and symlink escape;
- no mutable-latest API;
- new persistence golden and pinned historical golden byte hashes.

`tests/golden/dataset_store_v1.json` pins four synthetic vectors: object version,
canonical fingerprint, repository key and canonical byte SHA-256. Tests read it but
never rewrite it. All five prior golden files remain byte-identical.

Quality evidence on Python 3.12 at implementation time:

- focused Sprint 7: **28 passed**;
- full suite: **244 passed**;
- governance-negative: **14 passed**;
- `ruff format --check .`: required final gate;
- `ruff check .`: required final gate;
- strict `mypy`: required final gate;
- GitHub CI remains Python 3.12 and 3.13.

## 14. Fourteen implementation preconditions — BEFORE -> AFTER

Counts remain **RESOLVED 0->0; PARTIALLY_RESOLVED 5->5; OPEN 9->9; DEFERRED
0->0**. Technical progress does not substitute for competent governance authority.

| ID | Before -> after | Sprint 7 evidence / remaining decision |
|---|---|---|
| IP-01 | OPEN -> OPEN | no authentication or agent-command admission added |
| IP-02 | PARTIAL -> PARTIAL | canonical persistence and verified reload detect tamper; signatures, signer authority and trust roots remain open |
| IP-03 | OPEN -> OPEN | a path, ID or successful write grants no delegated authority |
| IP-04 | PARTIAL -> PARTIAL | three existing dataset object families persist/reconstruct exactly; broader representation approval and report persistence remain open |
| IP-05 | PARTIAL -> PARTIAL | no storage timestamp is introduced or confused with event/availability/ingestion time; vendor/calendar/clock policy remains open |
| IP-06 | OPEN -> OPEN | no emergency, release or reactivation runtime |
| IP-07 | OPEN -> OPEN | no approval, confirmation or expiry policy/runtime |
| IP-08 | OPEN -> OPEN | storage verification is not evidence/validation/monitoring freshness |
| IP-09 | OPEN -> OPEN | no validation methodology implemented |
| IP-10 | OPEN -> OPEN | no monitoring methodology implemented |
| IP-11 | PARTIAL -> PARTIAL | storage preserves existing dispositions but grants no source/data-quality acceptance authority |
| IP-12 | OPEN -> OPEN | immutable exact-key storage materially advances bounded technical custody; retention, privacy, licensing, legal, backup and recovery policy remain open |
| IP-13 | OPEN -> OPEN | allowed-root, traversal, symlink and resource gates bound the synthetic store; arbitrary user/external inputs remain unauthorized |
| IP-14 | PARTIAL -> PARTIAL | deterministic reload, golden, lineage, race and negative tests extend release evidence; production wave/release authority remains open |

## 15. Readiness, blockers and disposition

| Capability | Disposition |
|---|---|
| Local dataset store | `LOCAL_DATASET_STORE_READY` — bounded local synthetic scope |
| Immutable persistence | `IMMUTABLE_DATASET_PERSISTENCE_READY` — three supported governed object families |
| Verified reload | `VERIFIED_DATASET_RELOAD_READY` — exact typed key/version/fingerprint |
| Synthetic repository | `SYNTHETIC_DATASET_REPOSITORY_READY` |
| Real historical CSV import | `REAL_HISTORICAL_CSV_IMPORT_NOT_READY` |
| Real market-data adapters | `REAL_MARKET_DATA_ADAPTERS_NOT_READY` |
| Experiment foundation | `EXPERIMENT_FOUNDATION_NOT_READY` |
| Execution | `EXECUTION_CLOSED` |

Sprint blockers are **0** for the bounded repository-owned synthetic persistence
scope. The open preconditions block affected real-data, external-input, production,
retention and authority domains.

Sprint disposition:

`PHASE 3 SPRINT 7 COMPLETE WITH OPEN PRECONDITIONS`.

## 16. Recommended Sprint 8 — recommendation only

Recommend **Controlled Real Historical CSV Onboarding & Source Governance** only
after competent decisions close or narrowly authorize the applicable portions of
IP-05, IP-11, IP-12 and IP-13: source identity and permission, temporal/availability
semantics, provider-specific quality/reconciliation thresholds, licensing/retention
and external-file threat boundary.

If those authorities are not ready, Sprint 8 should remain a bounded governance
sprint rather than implement a dataset catalog, query layer or experiment engine.
Backtesting must not start merely because local persistence now exists.
