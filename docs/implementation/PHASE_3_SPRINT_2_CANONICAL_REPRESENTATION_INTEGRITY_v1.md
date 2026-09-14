# Phase 3 Sprint 2 — Canonical Representation & Integrity Contracts v1.0

## Status

Governed baseline: `main@47a81efe369cd11501f8ea88f9082fb1522efa11`.
Constitutional baseline: `50b61266f880cb9657b7f1b477d3d90825fe013f`.
Disposition: **PHASE 3 SPRINT 2 COMPLETE WITH OPEN PRECONDITIONS**.
EXE-01: **PLANNED_CLOSED**.

## Scope and architecture

Sprint 2 hardens the Sprint 1 non-execution records. It adds strict typed codecs for
`ArtifactEnvelope`, `EvidenceEnvelope`, `ProvenanceRecord`, and `AuditEvent`;
exact `TraceabilityRef` values; canonical byte fingerprints; fail-closed integrity
verification; direct lineage self-reference guards; and four immutable golden vectors.

The supported flow is:

`typed record → canonical envelope → UTF-8 bytes → SHA-256 → strict typed decode`.

There is no universal object serializer, persistence layer, network service, signature
service, domain engine, or execution adapter.

## Canonical representation specification

Representation identity is `ai-quant-lab.canonical-json`, representation version `1`.
It is separate from object version, contract version, package version, and fingerprint
algorithm.

The byte contract is:

- UTF-8 without BOM;
- one compact JSON value with keys sorted lexicographically;
- separators `,` and `:` without insignificant whitespace;
- Unicode emitted directly rather than normalized or ASCII-escaped;
- JSON `true`, `false`, and `null` semantics;
- ordered arrays; mappings with text keys; duplicate keys rejected;
- identifiers encoded as `namespace:token`;
- versions encoded as positive JSON integers, never booleans or “latest”;
- UTC timestamps encoded exactly as `YYYY-MM-DDTHH:MM:SS.ffffffZ`;
- enums encoded by their exact governed values;
- optional fields remain present as `null`; empty collections remain present;
- NaN and positive/negative Infinity are rejected;
- unknown formats, versions, record types, fields, missing fields, and wrong field types
  are rejected.

Floats remain available only in the generic Sprint 1 canonical primitive. The Sprint 2
typed record contracts contain no float fields and introduce no universal financial numeric
policy. A future governed numeric specification is required before quantitative domain data
uses these codecs.

## Typed decoding and equivalence

The decoder requires an expected Python governed type and reconstructs typed identifiers,
`ObjectVersion`, enums, tuples, references, and UTC datetimes. Artifact bytes cannot decode
as Evidence or Provenance. Unknown content is never ignored.

Equality distinctions:

| Relation | Meaning |
|---|---|
| object equality | every immutable dataclass field is equal |
| identity equality | typed identifier equality only |
| version equality | exact `ObjectVersion` equality only |
| canonical equality | canonical byte sequences are identical |
| fingerprint equality | SHA-256 outputs match for canonical bytes |
| semantic equivalence | not inferred; requires a future governed domain rule |

None of these creates authority, admissibility, validation, approval, or execution rights.

## Fingerprint and integrity contract

`fingerprint_record` applies SHA-256 to the typed canonical envelope bytes. The envelope
contains `$type`, so different governed record domains are separated. It never uses
`hash()`, `repr()`, pickle, process identity, locale, or unordered representation.

`verify_integrity` validates the expected fingerprint, recomputes it, compares with
`hmac.compare_digest`, returns an explicit `VERIFIED` record on equality, and raises on
mismatch. A mismatch is never silently accepted.

**HASH ≠ AUTHENTICITY.** SHA-256 comparison detects content change relative to a trusted
expected value. It does not prove actor identity, authorship, authorization, non-repudiation,
trust-root validity, or signing authority. Digital signatures and trust roots remain under
IP-02 and competent governance.

## Traceability, lineage, supersession, and invalidation

`TraceabilityRef` binds a typed object ID, exact positive version, and optional canonical
fingerprint. It never follows “latest”. Existing exact `VersionedRef` fields remain the
lineage links for inputs, transformations, parents, evidence sources, supersession,
invalidation, and audit targets.

Artifacts reject their own exact ID/version as a parent. Provenance rejects any direct
reference to its own ID. Full graph-cycle detection remains a later repository/graph-layer
obligation because no graph store is authorized here.

Evidence source references remain exact. Existing explicit `supersedes` and `invalidates`
fields preserve historical and negative evidence. Audit targets remain exact; audit events
contain no authority or approval binding.

## Golden vector policy

Four version-controlled vectors cover Artifact, Evidence, Provenance, and Audit. Each stores
a logical fixture name, record type, exact canonical text, representation version, and
expected SHA-256 fingerprint. Tests only verify them. Normal test execution cannot rewrite
them. Changing a vector requires an explicit representation-contract/version decision.

## Threat review

| Threat | Control / boundary |
|---|---|
| duplicate keys / parser differential | object-pairs hook rejects duplicates |
| unknown/missing fields | exact field-set checks |
| type/ID/version confusion | expected type plus namespace and positive-int checks |
| whitespace/order/escape ambiguity | re-encoding must equal input bytes |
| NaN/Infinity | parse-time and canonical rejection |
| timestamp ambiguity | exact UTC microsecond grammar |
| fingerprint confusion | typed envelope domain separation |
| arbitrary construction | fixed decoder dispatch; no imports or reflection |
| hidden mutable defaults | frozen/slotted records and tuple defaults |
| process/hash randomness | subprocess tests with different `PYTHONHASHSEED` |
| oversized structures | not bounded here; future adapter/input-limit specification |
| authenticity spoofing | deliberately unresolved IP-02 signatures/trust roots |

No pickle, database, filesystem repository abstraction, external API, network call, remote
trust service, or signing dependency is present.

## Preconditions before and after

| ID | Before | After | Technical progress / remaining decision | Blocked domains |
|---|---|---|---|---|
| IP-01 | OPEN | OPEN | none; authentication policy/runtime absent | IAM, commands, agents |
| IP-02 | PARTIALLY_RESOLVED | PARTIALLY_RESOLVED | canonical bytes, domain fingerprints, verification and tamper tests; signatures/trust roots/authority remain | signed ART/EVI/AUD |
| IP-03 | OPEN | OPEN | none; authority binding remains | consequential mutations |
| IP-04 | PARTIALLY_RESOLVED | PARTIALLY_RESOLVED | bounded technical contract complete for four records with golden vectors; competent approval and future domain numeric scope remain | broader artifact/data contracts |
| IP-05 | PARTIALLY_RESOLVED | PARTIALLY_RESOLVED | exact UTC microseconds; event/market/ingestion ordering, skew and lateness remain | DAT/STA/commands |
| IP-06 | OPEN | OPEN | no emergency runtime | emergency commands |
| IP-07 | OPEN | OPEN | no approval/expiry runtime | decisions/commands |
| IP-08 | OPEN | OPEN | no freshness policy | EVI/VAL/MON |
| IP-09 | OPEN | OPEN | outside scope | validation |
| IP-10 | OPEN | OPEN | outside scope | monitoring |
| IP-11 | OPEN | OPEN | outside scope | data |
| IP-12 | OPEN | OPEN | no persistence or retention policy | durable ledgers/data |
| IP-13 | OPEN | OPEN | no adapters/network | external interfaces |
| IP-14 | PARTIALLY_RESOLVED | PARTIALLY_RESOLVED | reviewable commits, ADRs, traceability and cross-version CI; release governance remains | wave promotion/release |

Counts remain **0 RESOLVED / 4 PARTIALLY_RESOLVED / 10 OPEN / 0 DEFERRED**.
Technical completion never self-authorizes institutional closure.

## Traceability

| Component | Governed source | Requirement | Test | Failure mode |
|---|---|---|---|---|
| typed codec | Sprint 3; Sprint 12 IP-04 | exact reconstruction | codec contract | `InvalidSerialization` |
| representation/version | Sprint 3/12 | explicit portable version | adversarial codec | reject mismatch |
| fingerprint/integrity | Sprint 3; IP-02/04 | deterministic tamper evidence | golden/integrity | `IntegrityMismatch` |
| traceability | Sprints 3/4/12 | exact ID/version/fingerprint | codec contract | invalid reference |
| lineage guards | Sprints 3/7 | attributable acyclic foundations | adversarial codec | `InvalidRecord` |
| audit linkage | Sprints 3/5 | exact target; no authority | codec/governance | reject/type invariant |
| golden vectors | Sprint 6; IP-04 | compatibility anchors | golden test | regression failure |
| preconditions | Sprint 12 §48 | OPEN never satisfied | governance tests | fail-closed exception |
| execution isolation | Sprints 2–12 | no A11/market path | governance-negative | boundary violation |

## Implementation ADRs

| ADR | Decision | Rationale and consequence |
|---|---|---|
| P3S2-01 | retain canonical JSON and version it as v1 | portable Sprint 1 continuity; change requires new version |
| P3S2-02 | typed envelope includes format/version/type/payload | prevents representation and domain confusion |
| P3S2-03 | exact field sets | unknown and missing governed semantics fail closed |
| P3S2-04 | reject duplicate keys | avoids parser-differential ambiguity |
| P3S2-05 | typed records add no floats | avoids inventing universal financial numeric policy |
| P3S2-06 | UTC with fixed six-digit microseconds | deterministic time representation; domain ordering remains open |
| P3S2-07 | type metadata domain-separates SHA-256 | identical-looking payloads across types are not equivalent |
| P3S2-08 | golden vectors are read-only fixtures | compatibility changes become visible and reviewable |
| P3S2-09 | exact TraceabilityRef with optional fingerprint | no mutable latest; fingerprint strengthens but does not authenticate |
| P3S2-10 | integrity mismatch raises | no ambiguous false status or silent continuation |
| P3S2-11 | direct self-reference only at this layer | full cycle checks wait for governed graph/repository layer |
| P3S2-12 | no signature library | infrastructure cannot pretend to resolve trust governance |

## Tests and CI

The existing Python 3.12/3.13 workflow continues to run:

`ruff format --check .`
`ruff check .`
`mypy`
`pytest`
`pytest tests/test_governance_negative.py`

Normal discovery includes unit, contract, golden-vector, integrity, negative, adversarial,
cross-process determinism, and execution-isolation tests. Tests require no network or live data.

## Known limitations and readiness

IP-02 authenticity, IP-04 governance approval/broader numeric scope, IP-05 temporal ordering,
IP-11 data-quality/reconciliation, and IP-12 retention/legal policy remain unresolved.
Therefore:

- **CORE_CONTRACTS_READY** for governed review;
- **DATA_FOUNDATION_NOT_READY**;
- **EXPERIMENT_NOT_READY**;
- **VALIDATION_NOT_READY**;
- **COMMAND_NOT_READY**;
- **EXECUTION_CLOSED**.

Recommended Sprint 3: close the bounded data-foundation preconditions—especially IP-05,
IP-11, and the technical/data-custody portion of IP-12—by specifying and implementing
source identity, event/availability/ingestion time primitives, immutable raw-record
contracts, quality/reconciliation dispositions, and fixtures. Do not implement a Data Engine.

## Baseline integrity

No constitutional, Phase 1, Phase 2, or Sprint 1 governed artifact is modified. Runtime
dependencies remain empty. No strategy, indicator, optimizer, domain engine, broker,
exchange, order, position, capital, webhook, paper/live trading, or deployment capability
exists. EXE-01 remains **PLANNED_CLOSED**.
