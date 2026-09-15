# Phase 3 Sprint 4 — Data Ingestion Kernel & Immutable Dataset Assembly v1.0

## Document status and governed baseline

Implementation report, Draft PR; not approval for real-data use, execution, or deployment. Current `main` was verified against Sprint 3 merge `b9ed5049833809099cac3013859402e95d9ca7c9`; PR #64 was verified MERGED before mutation. Constitutional tag `v1.0` targets `50b61266f880cb9657b7f1b477d3d90825fe013f`. Existing Phase 1/2 and Sprint 1–3 historical artifacts are unchanged. This document and `ingestion.py` are subordinate to those sources. EXE-01 remains `PLANNED_CLOSED`.

## Boundary and architecture

The kernel receives synthetic, deterministic, in-memory candidate records; it never acquires external data. `InputAdapter.read()` supplies bounded candidates only. `SyntheticInputAdapter` has an exact versioned, fingerprint-bearing adapter reference; `IngestionRequest` pins source/instrument definitions and all output identities/versions, three provenance references, a UTC knowledge-time cutoff, actor and contract version. `IngestionSession` identifies one run independently of dataset content. Retried runs use new session identities and retain distinguishable audit events. `CandidateObservation` is pre-acceptance; its bounded `CandidateField` distinguishes text, integer, boolean, decimal-text and null. A parsed candidate is never automatically accepted.

The synchronous path is candidate parse → exact source/instrument binding → strict UTC temporal gate → structural raw-field quality gate → group reconciliation → accepted-only assembly → existing `DatasetManifest` and `DatasetLock` → existing domain-separated fingerprints and `AuditEvent` records. No serializer rule in `ai-quant-lab.canonical-json` v1 changes. Output `RawObservation`, `DatasetManifest`, `DatasetLock` remain the existing typed codec-governed types; ephemeral input/session/result objects do not claim persistent canonical codec coverage. The new two-case synthetic fixture is read-only test input, not a replacement for Sprint 2/3 golden serialization vectors.

## Temporal, quality, identity and cutoff gates

The currently bounded acceptance policy is `event_time <= availability_time <= ingestion_time`, all UTC. Canonical candidate timestamps require `YYYY-MM-DDTHH:MM:SS.ffffffZ`; no repair, local-time inference or uncontrolled wall-clock call. A missing ingestion timestamp uses injected `DeterministicClock`. `TemporalCoordinates.legitimate_knowledge_time` is availability time, not event time; candidates whose availability exceeds the explicit dataset cutoff are rejected before accepted-only assembly. A lock cutoff denotes the latest *legitimate availability time* represented by this bounded snapshot; the kernel does not promise vendor time trust, causal ordering or late-data governance.

The kernel verifies exact source and instrument identity/version/fingerprint and only admits `SYNTHETIC_FIXTURE` source definitions. This is content integrity comparison, **not source authentication**. The exact provenance references are pinned but no producer signature, trust root, persistence or external registry validation exists. Candidate source/instrument mismatch, source-definition fingerprint mismatch, adapter mismatch, reused observation ID/version, wrong session or unsupported contract version invalidate the session. No credentials are accepted.

The structural quality gate delegates to the existing sorted, unique, bounded `RawField` contract. Binary float, nonfinite decimal, malformed decimal and derived/execution field names are prohibited. There are no economic price/volume/spread thresholds. `ACCEPTED` means only bounded structural/temporal acceptance; it is not source endorsement, strategy validation, deployment, or trading permission.

## Duplicates, reconciliation and correction

For this bounded synthetic policy, event identity is source ID + instrument ID + event timestamp + optional source sequence. Missing sequence is explicit; provider-specific event-key equivalence remains an IP-11 governance decision. Canonical payload equality compares typed field names and canonical values, including `DecimalValue`; scale-equivalent decimal text is equivalent under the existing Sprint 3 policy. The group is sorted by exact observation identity before disposition; arrival order never selects truth.

If content conflicts within an event group, **all** conflicting records are quarantined `CONFLICT`; none wins. Identical content/timestamps produces one `UNIQUE` accepted record and explicit `BYTE_IDENTICAL_DUPLICATE` quarantined records. Identical content with different availability/ingestion coordinates produces explicit `RETRANSMISSION`. This is bounded technical classification, not universal market-feed reconciliation. Multiple groups with the same observation ID/version are a session integrity failure.

An explicit correction must bind a known same-source/instrument **ACCEPTED** prior exact observation/version/fingerprint. A correction becomes a new immutable `CORRECTION` accepted record; a same-session predecessor is retained in `IngestionResult.superseded_observations` and excluded from accepted-only membership. A prior external predecessor is supplied through the explicit `prior_observations` boundary and remains unchanged. Unknown target → `ReconciliationError`; known identity with wrong fingerprint → `CriticalIntegrityFailure`. No self-correction, mutation, last-write-wins or silent history erasure.

An explicit quarantine reason creates a canonical `QUARANTINED` raw observation, preserving its ID, payload, provenance and fingerprint, but never accepted-only manifest membership. A rejection occurs before accepted raw status and records only safe candidate/session ID/version, stage, reason and deterministic timestamp—never arbitrary rejected payload. In a mixed batch, structurally/temporally invalid candidates are recorded as per-record rejections and eligible accepted records may assemble. If none remain, `DatasetAssemblyError` prevents a seemingly valid research lock. Integrity/binding/session failures invalidate the whole session with an explicit exception rather than producing a partial success. There is no persistent failure ledger or automatic retry: future orchestration must independently preserve exception/failure audit evidence before claiming an institutional session history.

## Assembly, replay, provenance and audit

`DatasetManifest` uses the Sprint 3 `accepted_only` contract, sorted exact fingerprint-bearing observation references, source/instrument scope, event-time range, pinned provenance, and explicit dataset ID/version. `DatasetLock` pins that exact manifest fingerprint and the explicit UTC knowledge cutoff; changed membership changes manifest and lock fingerprints. The lock never follows `latest`. Deterministic inputs, fixed request/output identities and clock reproduce observation/manifest/lock content fingerprints across reordered semantically unordered input; a different session ID changes session/audit identity but not dataset content fingerprints.

Exact output references retain source → request/session → raw observations → manifest → lock relationships. Session identity is carried in the result and audit targets; raw observation provenance itself is a pinned, separately supplied provenance reference and is intentionally **not** mutated per session. To reconstruct actual producer/session provenance across persistence boundaries, future governed provenance registration and custody are needed. Audit actions include ingestion.started, observation.accepted/quarantined, candidate.rejected, dataset.manifest_created, dataset.locked and ingestion.completed. The immutable result holds exact accepted, quarantined and superseded objects, rejection and reconciliation records, manifest/lock and audit events; counts derive from exact membership. Audit is recordkeeping, not authorization. Duplicate/conflict/correction-specific audit action registration and auditable failure paths are future orchestration obligations; the reconciliation records are retained in the result now.

## Threat review

| Attack or ambiguity | Present control | Remaining boundary |
| --- | --- | --- |
| Source spoofing / adapter impersonation | Exact typed source/instrument definition fingerprints and adapter reference; synthetic-only source | HASH ≠ AUTHENTICITY; no signing trust root (IP-02), principal authentication (IP-01) |
| Credential leak / live acquisition | No credential, transport, network or local-file adapter interface | Future adapters remain disabled pending IP-13 |
| Look-ahead / timestamp manipulation | Three UTC coordinates, strict ordering, availability cutoff, deterministic clock | Vendor clock trust and late data (IP-05) |
| Duplicate replay / conflict overwrite | Event-key and typed-content classification, no last-write-wins, all-conflict quarantine | Provider-specific identity and thresholds (IP-11) |
| Payload/decimal ambiguity | Explicit value kinds, canonical finite decimal, raw-field restrictions | Market schema and source-value authority deferred |
| Correction history / quarantine bypass | Exact correction fingerprint, retained predecessor, accepted-only membership | Release authority not implemented |
| Manifest poisoning / lock substitution | Sorted exact membership and existing SHA-256 integrity verification | Custody/signing/retention (IP-02/IP-12) |
| Provenance removal / audit spoofing | Required exact provenance references and typed AuditEvent | Provenance signer/ledger is not implemented |
| Signal / execution-field injection | Raw-field semantic prohibition; EXE-01 has only PLANNED_CLOSED | No execution module exists |

The in-memory batch is bounded for Sprint 4 test-scale use; future adapters must govern input size and parser resource limits. Golden synthetic fixtures are not real market evidence.

## Implementation traceability

| Component | Governed source | Invariant | Test | Fail-closed response |
| --- | --- | --- | --- | --- |
| Adapter/request/session/candidate | Sprint 2 module boundaries; Sprint 4 workflow blueprint; Sprint 3 data contracts | Adapter ≠ authority; parse ≠ accept; exact identities | `test_clean_end_to_end_integrity_and_knowledge_time`, binding negatives | Critical failure or explicit rejection |
| Clock/temporal gate/cutoff | Sprint 7 data plan; Sprint 3 TemporalCoordinates; IP-05 | Availability ≠ event ≠ ingestion; no look-ahead | delayed, mixed and cutoff tests | Temporal rejection |
| Structural quality | Sprint 3 RawField; Sprint 7; IP-11 | RAW ≠ SIGNAL; no float/nonfinite | numeric and prohibited-field tests | Candidate rejection |
| Duplicate/reconciliation | Sprint 7; Sprint 3 ReconciliationDisposition | Conflict ≠ winner; no last-write-wins | conflict order and duplicate tests | Conflict quarantine |
| Correction/quarantine | Sprint 3 RawObservation; Sprint 4 state model | Correction ≠ mutation; quarantine ≠ acceptance | correction and quarantine tests | Target failure or exclusion |
| Manifest/lock/provenance | Sprint 3 DatasetManifest/DatasetLock; Sprint 8 dataset-lock obligation | Exact accepted-only snapshot; dataset ≠ lock | end-to-end, replay, membership tests | No empty lock / integrity failure |
| Fingerprint/audit/fixture | Sprint 2 codec/integrity; Sprint 3 audit references; Sprint 6 T15/T16/T25/T32/T35/T36/T37 | Hash ≠ authenticity; audit ≠ authority | integrity, golden, replay, governance-negative | Fingerprint mismatch fails |
| Execution isolation | Constitution; Sprint 2 EXE-01; Sprint 11 execution boundary | Data ≠ execution | governance-negative and kernel execution test | PLANNED_CLOSED |

## Preconditions: authoritative 14-item reassessment

Source of the IDs, owners, dependencies, statuses and required decisions: Phase 2 Sprint 12 review and existing `governance.PRECONDITIONS`. All before/after statuses are unchanged: 0 RESOLVED, 5 PARTIALLY_RESOLVED, 9 OPEN, 0 DEFERRED. Technical progress is not competent institutional approval.

| ID | Before → after | Technical progress / remaining competent decision | Future domains blocked |
| --- | --- | --- | --- |
| IP-01 | OPEN → OPEN | None; IAM + Security must approve authentication/threat model | IAM, command, agents |
| IP-02 | PARTIAL → PARTIAL | Existing hashes verify source/instrument and assembled outputs; GOV + Security must approve signatures/trust roots | authoritative ART/EVI/AUD custody |
| IP-03 | OPEN → OPEN | No authority binding; GOV + IAM must approve delegation/revocation | IAM and consequential mutations |
| IP-04 | PARTIAL → PARTIAL | Existing canonical codecs/fingerprints cover raw/manifest/lock outputs, no v1 rule change; ART + DAT representation-scope approval pending | unsupported artifact/data locks |
| IP-05 | PARTIAL → PARTIAL | Deterministic clock, explicit knowledge cutoff, temporal gate/failure path; STA + DAT clock trust/late-data policy pending | general DAT, STA, commands |
| IP-06 | OPEN → OPEN | No emergency runtime; GOV + humans must decide authority/dual control | RSK, DEC, HUM, command |
| IP-07 | OPEN → OPEN | No approval runtime; GOV + IAM must define confirmation/expiry | command, decision |
| IP-08 | OPEN → OPEN | No validation/monitoring freshness gate; EVI + VAL + MON decision | EVI, VAL, MON |
| IP-09 | OPEN → OPEN | No method engine; VAL + GOV method specifications | VAL |
| IP-10 | OPEN → OPEN | No monitoring engine; MON + VAL + RSK thresholds/windows | MON |
| IP-11 | PARTIAL → PARTIAL | Structural quality, duplicate/conflict quarantine/correction orchestration; DAT + GOV source contracts, event-key semantics, thresholds and acceptance policy pending | real-data DAT ingestion |
| IP-12 | OPEN → OPEN | Immutable exact synthetic history, results/locks and audit capability; GOV + Legal + Data retention/privacy/licensing/legal policy pending | DAT/AUD ledgers, real-data custody |
| IP-13 | OPEN → OPEN | Synthetic-only adapter; Security + IAM external threat/adapters decision pending | external adapters, MACP, SMI |
| IP-14 | PARTIAL → PARTIAL | Reviewable tests, replay and CI/golden evidence; GOV + QA + AUD release gates pending | wave promotion / production release |

Fail-closed defaults remain those recorded verbatim in `governance.py`; `OPEN` and `PARTIALLY_RESOLVED` cannot be treated as satisfied. This sprint does not change their governed statuses.

## Implementation ADRs

| ID | Technical decision and boundary |
| --- | --- |
| S4-ADR-01 | InputAdapter has only an exact adapter reference and candidate read operation; no acquisition/authority. |
| S4-ADR-02 | Synthetic in-memory adapter only; CSV/live/local-file adapter deferred. |
| S4-ADR-03 | Candidate and accepted RawObservation are distinct; parsing never grants acceptance. |
| S4-ADR-04 | Explicit deterministic clock is injected; no wall-clock dependence. |
| S4-ADR-05 | Mixed record failures are explicit rejections; critical identity/integrity errors fail session; no empty accepted-only lock. |
| S4-ADR-06 | Bounded event key is source/instrument/event-time/optional sequence; source-specific mapping needs governance. |
| S4-ADR-07 | Conflicting same-event payloads all quarantine; no last-write-wins. |
| S4-ADR-08 | Duplicate classification uses typed canonical payload and temporal coordinates, independent of arrival order. |
| S4-ADR-09 | Corrections require known exact same-scope predecessor/fingerprint; original remains reconstructable. |
| S4-ADR-10 | Quarantine and superseded records are returned but never accepted-only membership. |
| S4-ADR-11 | Deterministic assembly sorts exact refs and binds manifest fingerprint to lock. |
| S4-ADR-12 | Session IDs distinguish institutional runs but do not contaminate dataset content fingerprints. |
| S4-ADR-13 | Existing canonical-json v1, typed output codecs and SHA-256 integrity are reused, not changed. |
| S4-ADR-14 | Existing AuditEvent records describe transitions, not authorize them; failure ledger is later governed orchestration. |
| S4-ADR-15 | Storage/network/async/quant engines are deferred; EXE-01 stays closed. |

None of these technical ADRs approves unresolved IP governance.

## Test and next-domain disposition

Focused synthetic kernel tests cover clean integration, delayed temporal coordinates, mixed rejection, duplicate/retransmission/conflict, correction history, quarantine exclusion, deterministic replay, exact membership/lock fingerprints, source/instrument binding, tamper and prohibited-field injection. Two read-only synthetic scenario vectors supplement historical golden codec vectors. The existing Python 3.12/3.13 Foundation CI runs format, lint, strict typing, full pytest and execution isolation; no new workflow or dependency is introduced.

If all gates pass, `DATA_INGESTION_KERNEL_READY` and `LOCAL_DATASET_ASSEMBLY_READY` apply only to deterministic synthetic in-memory inputs. `REAL_MARKET_DATA_ADAPTERS_NOT_READY`, `EXPERIMENT_FOUNDATION_NOT_READY` and `EXECUTION_CLOSED` remain. Recommended Sprint 5: governed bar/OHLCV schema, timeframe identity and normalization rules, followed by a bounded deterministic local fixture/CSV mapping adapter only after IP-05/IP-11/IP-12/IP-13 scope decisions. No live APIs, strategy code or execution.
