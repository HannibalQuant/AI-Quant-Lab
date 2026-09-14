# Phase 3 Sprint 3 — Governed Data Foundation & Temporal Integrity Contracts v1.0

## Status

- Governed implementation baseline: `1a27d54481e5a5eb2598d8522464812a1c8bdb99`
- Constitutional baseline: `50b61266f880cb9657b7f1b477d3d90825fe013f` (`v1.0`)
- Canonical representation: `ai-quant-lab.canonical-json` representation version 1
- Scope: immutable data contracts only; no acquisition, persistence, orchestration, research, or execution engine
- EXE-01: `PLANNED_CLOSED`

## Implemented scope

Sprint 3 adds immutable, explicitly versioned contracts for venue, source, instrument,
raw observation, temporal coordinates, exact decimal scalars, dataset manifests, and
dataset locks. It extends the Sprint 2 typed codec, fingerprints, integrity verifier,
traceability references, and audit targeting instead of creating a parallel contract
system.

Deliberately absent are network adapters, CSV loaders, databases, filesystem
repositories, streaming, scheduling, ETL orchestration, quality thresholds, market-data
normalization, features, signals, experiments, validation, and execution.

## Contract architecture

### Identity and attribution

`VenueIdentity` distinguishes the market or publication venue. `SourceIdentity`
distinguishes provider, feed, source type, source-definition version, and optional exact
venue reference. Provider is not assumed to be venue; a file is not reduced to source
identity; source identity contains no credentials.

`InstrumentIdentity` binds a canonical instrument ID and object version to symbol,
instrument class, optional base/quote/settlement assets, and optional exact venue
reference. A symbol is descriptive, not globally identifying. This is intentionally not
a security master.

`DatasetId` remains separate from `DatasetLockId`, source identity, instrument
identity, object version, and fingerprint. No contract accepts a mutable `latest`
reference.

### Temporal model

`TemporalCoordinates` has three orthogonal UTC timestamps:

| Field | Meaning |
|---|---|
| `event_time` | Time the event occurred under source semantics |
| `availability_time` | Earliest time the information was legitimately knowable to research |
| `ingestion_time` | Time AI Quant Lab accepted/recorded the observation |

For accepted foundational observations, the bounded policy is
`event_time <= availability_time <= ingestion_time`. All values are timezone-aware,
UTC, immutable, and encoded with six-digit microsecond precision and `Z`. The
`legitimate_knowledge_time` accessor returns availability time and never event time.

This policy does not settle causal ordering, source clock accuracy, clock skew,
late-arriving-data windows, amended vendor publication times, or future event-specific
policies. Those remain under IP-05 and must fail closed at affected consumers.

### Exact numeric and payload policy

Binary floats are rejected. Exact price/quantity-like values use `DecimalValue`, a
finite canonical base-10 text value. Scale variants `1`, `1.0`, `1.00`, and
`1e0` are intentionally equivalent and encode as `1`; zero encodes as `0`.
NaN and infinities are rejected.

A raw payload is a sorted, unique tuple of named `RawField` values. Values are bounded
to text, integer, Boolean, `DecimalValue`, or null and receive explicit scalar type
tags in canonical JSON. Arbitrary Python objects and binary floats are rejected.
Reserved derived/execution semantic names and prefixes (feature, indicator, signal,
strategy, decision, order, position) are rejected. This mechanically preserves
RAW != DERIVED, RAW != SIGNAL, and DATA != EXECUTION at this layer.

The bounded scalar policy is not a universal financial unit, precision, currency,
corporate-action, or market-data schema policy.

### Raw observation

`RawObservation` binds:

- a typed observation ID and exact object version;
- exact, fingerprint-bearing source, instrument, and provenance references;
- explicit temporal coordinates;
- immutable sorted raw fields;
- optional source sequence without fabrication;
- a quality state and reconciliation disposition;
- an optional exact supersession reference;
- an explicit contract version.

An observation cannot supersede itself. `CORRECTION` requires an exact prior
observation reference. `ACCEPTED` cannot coexist with `CONFLICT` or `UNRESOLVED`.
Correction creates a new immutable record; it does not rewrite its predecessor.

### Duplicate and reconciliation semantics

The bounded dispositions distinguish `UNIQUE`, `BYTE_IDENTICAL_DUPLICATE`,
`SAME_EVENT_DUPLICATE`, `RETRANSMISSION`, `CORRECTION`, `CONFLICT`, and
`UNRESOLVED`. They provide representation, not automated classification. A future
acceptance pipeline must record a disposition and must not silently discard or choose
between conflicting records.

Quality states are `ACCEPTED`, `SUSPECT`, `QUARANTINED`, and `INVALIDATED`.
They do not validate a strategy or evidence claim. Rejection before canonical
acceptance is distinct from later quarantine/invalidation; unsafe rejected payloads
need not be retained in full, but rejection audit metadata remains a future obligation.

### Quarantine and correction

Quarantine preserves identity, payload, provenance, temporal coordinates, version, and
fingerprint and does not imply deletion or later acceptance. Release criteria,
thresholds, and competent authority are not implemented.

Correction and supersession use an exact observation reference with fingerprint.
Historical reconstruction remains possible. Full lineage graph cycle detection is
deferred; direct self-supersession is rejected now.

### Dataset manifest

`DatasetManifest` is an immutable snapshot declaration with:

- exact dataset identity and version;
- creation time and explicit event-time range;
- non-empty, sorted, unique, fingerprint-bearing observation membership;
- exact source and instrument scope references;
- exact provenance reference;
- contract version;
- the only supported policy, `accepted_only`.

Query-like or mutable membership descriptions are rejected. Same exact membership,
versions, references, and governed metadata produce the same fingerprint; changing
membership or version changes it.

### Dataset lock

`DatasetLock` binds a typed lock ID and version to an exact dataset/manifest snapshot,
its fingerprint, lock time, temporal cutoff, provenance, state, and contract version.
The dataset and manifest references must identify the same exact object/version.
The cutoff cannot be later than the lock time. A lock never means “current contents.”

No materialization, repository, storage, or experiment binding is implemented.

## Canonical representation and integrity

All six new top-level types have explicit `$type` identities under the existing
representation version. Adding explicitly supported types does not change the canonical
rules, so representation v1 remains valid and prior Sprint 2 vectors remain unchanged.

Canonical data references carry object type through typed ID namespace, object version,
and expected SHA-256 fingerprint. Typed raw scalar tags prevent Boolean/integer/text/
decimal confusion. Strict decoding rejects malformed JSON, duplicate keys, unknown
fields, wrong type, wrong namespace, unsupported representation versions, invalid
timestamps, invalid enums, noncanonical input, and invalid fingerprints.

Fingerprints derive from canonical UTF-8 bytes and are domain-separated by the top-level
`$type`. SHA-256 detects content changes but does not prove authenticity, identity,
authorization, trusted authorship, or non-repudiation. IP-02 therefore remains partial.

Six read-only golden vectors anchor venue, source, instrument, delayed raw observation,
manifest, and lock representations and fingerprints. Normal tests never rewrite them.

## Data custody boundary

Technical custody capability now includes immutable identity/version, exact references,
canonical bytes, fingerprints, provenance links, lifecycle dispositions, correction
history, and auditable targets. This does not decide retention periods, deletion law,
licensing, privacy, source entitlements, or jurisdictional obligations. IP-12 remains
open and affected persistence/retention work remains fail-closed.

Credentials and personal data are excluded from source contracts.

## Threat review

| Threat | Sprint 3 control | Remaining boundary |
|---|---|---|
| Source spoofing | Typed/versioned source and exact provenance reference | Authentication/signatures/trust roots remain IP-02/IP-13 |
| Timestamp manipulation | UTC validation, strict ordering, canonical timestamp bytes | Clock trust and late-data policy remain IP-05 |
| Look-ahead contamination | Availability time is separate and is the knowledge-time primitive | Experiment access policy is not implemented |
| Replay/duplicates | Observation identity, source sequence, explicit dispositions | Automated classification is deferred |
| Payload/numeric ambiguity | Tagged bounded scalars; canonical finite decimal; float rejection | Domain units/precision schemas are deferred |
| Canonicalization attack | Strict typed decoder, canonical-input check, duplicate-key rejection | Resource/size limits belong to adapter/runtime specs |
| Manifest/lock tampering | Exact fingerprint-bearing membership and integrity verification | Persistent custody and signatures are deferred |
| Provenance removal | Required fingerprint-bearing provenance references | Provenance graph storage is deferred |
| Quarantine bypass | Non-accepted explicit state and incompatible accepted/conflict pair | Transition authority/runtime is deferred |
| History destruction | Frozen records and exact supersession | Durable append-only persistence is deferred |

## Governance-as-code invariants

The suite enforces: ID != VERSION; SOURCE != CREDENTIAL; EVENT_TIME !=
AVAILABILITY_TIME; AVAILABILITY_TIME != INGESTION_TIME; RAW != DERIVED; RAW != SIGNAL;
DATASET != DATASET_LOCK; QUALITY != STRATEGY_VALIDATION; QUARANTINE != DELETION;
CORRECTION != MUTATION; HASH != AUTHENTICITY; AUDIT != AUTHORIZATION; DATA != EXECUTION;
and EXE-01 CLOSED.

## Implementation traceability

| Component | Phase 2 source | Governed requirement | Test | Failure behavior |
|---|---|---|---|---|
| Source/venue identity | Sprint 7 DP-01/02, Sprint 2 DAT boundaries | Exact attributable source; provider != venue | source/venue distinction and codec tests | Reject invalid namespace/field |
| Instrument identity | Sprint 7 DP-03 | Venue-aware instrument identity | instrument golden/round-trip tests | Reject malformed identity |
| Temporal coordinates | Sprint 7 DP-04/05/10 | Event, availability, ingestion separation | delay, naive/reverse, leakage tests | Reject/hold invalid ordering |
| Raw observation | Sprint 7 DP-06/07 | Immutable raw, lineage, no derived semantics | immutability, scalar, reserved-field tests | Reject invalid observation |
| Decimal value | Sprint 7 data-contract boundary; Sprint 12 IP-04 | Deterministic numeric representation | equivalence and non-finite tests | Reject float/invalid decimal |
| Quality/reconciliation | Sprint 7 DP-09/16/17; Sprint 12 IP-11 | Explicit conflict, duplicate, quarantine | acceptance-conflict and quarantine tests | Quarantine/deny acceptance |
| Dataset manifest | Sprint 7 DP-21/25/27 | Exact deterministic membership | reproducibility and duplicate tests | Reject mutable/duplicate membership |
| Dataset lock | Sprint 7 DP-27; Sprint 8 input lock | Exact immutable snapshot binding | lock version/cutoff tests | Reject mismatch |
| Typed codec/fingerprint | Sprint 3 contracts; Sprint 12 IP-04 | Exact reconstructable records | six round-trips, golden vectors | Reject unknown/noncanonical input |
| Preconditions | Sprint 12 Sections 46/48 | Open decisions cannot be treated satisfied | IP-05/IP-11/IP-12 status test | Domain remains blocked |
| Execution isolation | Constitution; Sprints 2/6/12 | EXE-01 remains closed | inherited negative governance suite | ExecutionBoundaryViolation |

## Implementation ADRs

### ADR-S3-01 — Separate venue, source, instrument, dataset, and lock identities

Decision: use typed IDs and immutable versioned records; references are exact.  
Rationale: shared symbols or providers cannot establish institutional identity.  
Consequence: future adapters must register definitions before observations.

### ADR-S3-02 — Availability time is legitimate knowledge time

Decision: preserve three timestamps and expose only availability time as the knowledge
primitive.  
Rationale: event time alone permits look-ahead.  
Consequence: future experiment access must bind availability cutoffs.

### ADR-S3-03 — Strict accepted-observation temporal policy

Decision: the only implemented policy is event <= availability <= ingestion.  
Rationale: conservative, testable intake semantics for this bounded layer.  
Consequence: alternative/late-data cases require a new governed policy, not coercion.

### ADR-S3-04 — Canonical finite decimal text

Decision: reject float and encode normalized finite base-10 values; scale is not
semantic.  
Rationale: avoid binary floating representation drift.  
Consequence: domain scale/units remain a later schema concern.

### ADR-S3-05 — Bounded tagged raw scalars

Decision: permit only tagged text, integer, Boolean, decimal, and null.  
Rationale: strict portable decoding without arbitrary-object construction.  
Consequence: structured source schemas require later explicitly governed contracts.

### ADR-S3-06 — Explicit duplicate/reconciliation disposition

Decision: distinguish duplicate, retransmission, correction, conflict, and unresolved
states without automating classification.  
Rationale: no observation may silently disappear or become truth.  
Consequence: IP-11 progresses only to partial.

### ADR-S3-07 — Quarantine preserves the record

Decision: quarantine is a state, not deletion or acceptance.  
Rationale: preserve negative evidence and history.  
Consequence: release policy remains outside Sprint 3.

### ADR-S3-08 — Correction creates a new observation

Decision: exact supersession reference; direct self-reference rejected.  
Rationale: immutable historical reconstruction.  
Consequence: full graph-cycle checks await the lineage layer.

### ADR-S3-09 — Manifest membership is enumerated and fingerprint-bearing

Decision: reject query-like membership and duplicate references.  
Rationale: dataset composition must be reconstructable.  
Consequence: very large manifest strategies are deferred to implementation specs.

### ADR-S3-10 — Dataset lock binds an exact manifest snapshot

Decision: dataset and manifest ID/version must match and carry fingerprints.  
Rationale: an experiment cannot consume mutable “latest” data.  
Consequence: experiment binding remains unimplemented.

### ADR-S3-11 — Extend canonical-json v1 by explicit type registration

Decision: preserve representation rules and old golden vectors while adding new typed
records.  
Rationale: no existing byte rule changed.  
Consequence: a future incompatible representation change must create a new version.

### ADR-S3-12 — Technical custody does not decide legal custody

Decision: implement identity, integrity, provenance, and history only.  
Rationale: retention/privacy/licensing require competent governance/legal authority.  
Consequence: IP-12 remains OPEN.

## Tests and golden fixtures

Tests cover typed round trips, exact ID/version/reference preservation, delayed temporal
coordinates, knowledge-time separation, naive/reversed time rejection, decimal
equivalence, non-finite rejection, bounded payloads, derived-field rejection,
acceptance/conflict incompatibility, immutable correction history, direct
self-supersession, quarantine preservation, deterministic membership, lock binding,
tamper detection, decoder type/field/version attacks, audit non-authority, precondition
truth, and six golden vectors. The existing complete suite remains the quality gate
under Python 3.12 and 3.13.

## Preconditions before and after

| ID | Before | After | Technical progress | Remaining governance decision | Blocked future domains |
|---|---|---|---|---|---|
| IP-01 | OPEN | OPEN | No change | Identity/authentication source and assurance | IAM, command |
| IP-02 | PARTIALLY_RESOLVED | PARTIALLY_RESOLVED | Data records inherit canonical fingerprints/tamper checks | Signatures, trust roots, signer authority | high-assurance audit/data/command |
| IP-03 | OPEN | OPEN | Exact refs do not grant authority | Delegation/revocation binding | IAM, mutations |
| IP-04 | PARTIALLY_RESOLVED | PARTIALLY_RESOLVED | Six typed data codecs, tagged decimal/scalars, golden vectors | Competent approval of representation scope | persisted governed data |
| IP-05 | PARTIALLY_RESOLVED | PARTIALLY_RESOLVED | Three UTC times, ordering, knowledge-time primitive | Clock trust, late-data, causal/source policies | full ingestion, experiment access |
| IP-06 | OPEN | OPEN | No change | Emergency/release/reactivation authority | risk/command |
| IP-07 | OPEN | OPEN | No change | State transition maps | mutation runtimes |
| IP-08 | OPEN | OPEN | No change | Statistical method specifications | validation/monitoring |
| IP-09 | OPEN | OPEN | No change | Validation method specifications | validation |
| IP-10 | OPEN | OPEN | No change | Monitoring thresholds/windows | monitoring |
| IP-11 | OPEN | PARTIALLY_RESOLVED | Bounded quality, duplicates, conflicts, corrections, quarantine, reconciliation | Source-specific thresholds and acceptance authority | automated data acceptance/reconciliation |
| IP-12 | OPEN | OPEN | Technical custody primitives added | Retention/privacy/licensing/legal policy | durable storage/retention |
| IP-13 | OPEN | OPEN | Data threat review added | Full trust-boundary model | external adapters/high assurance |
| IP-14 | PARTIALLY_RESOLVED | PARTIALLY_RESOLVED | Typed tests and traceability extended | Repository protection/release governance | protected implementation delivery |

Counts before: RESOLVED 0, PARTIALLY_RESOLVED 4, OPEN 10, DEFERRED 0.  
Counts after: RESOLVED 0, PARTIALLY_RESOLVED 5, OPEN 9, DEFERRED 0.

## Known limitations and readiness

The contract layer does not determine provider-specific schemas, units, corporate
actions, bar construction, calendars, clock trust, quality thresholds, reconciliation
authority, rejection-payload retention, legal retention, entitlement, adapter
authentication, storage, or orchestration.

The technical data contract foundation is ready for a bounded next sprint, while
affected production-grade domains remain conditional on IP-05, IP-11, IP-12, and
IP-13. `DATA_FOUNDATION_READY` means only that a local deterministic input adapter,
raw acceptance pipeline, explicit quality/reconciliation gates, immutable dataset
assembly, and dataset locking can next be specified and implemented. It does not
authorize external feeds, experiments, validation, strategies, or execution.

## Recommended Sprint 4

**Data Ingestion Kernel & Immutable Dataset Assembly**, limited initially to synthetic
and local deterministic fixtures. It may implement adapter contracts, bounded input
acceptance, temporal and quality gates, reconciliation orchestration, manifest assembly,
and lock creation. It must not add live APIs, automated source trust, mutable datasets,
experiments, strategy logic, or execution.

EXE-01 remains `PLANNED_CLOSED`.
