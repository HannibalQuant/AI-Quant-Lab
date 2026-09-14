# Phase 3 Sprint 1 — Implementation Foundation & Preconditions Closure v1.0

## Status

Baseline: `main@544bac4d769b189cbcbb88080bf477a2588b9056`.
Constitution: `50b61266f880cb9657b7f1b477d3d90825fe013f`.
Disposition: **PHASE 3 SPRINT 1 COMPLETE WITH OPEN PRECONDITIONS**.
EXE-01: **PLANNED_CLOSED**.

## Implemented

A Python 3.12+ standard-library runtime foundation provides typed namespaced IDs, exact
positive versions, immutable version references, UTC-only timestamps, orthogonal state axes,
immutable Artifact/Evidence/Provenance/Audit envelopes, canonical JSON v1, SHA-256
fingerprinting, the exact 14-item Sprint 12 precondition register, and an explicit rejecting
execution boundary. No database, API, network adapter, domain engine, agent runtime, strategy,
signal, optimizer, portfolio, order, broker, exchange, webhook, paper/live trading, or capital
function exists.

Package layout is deliberately compact: `core.model` owns coupled foundational value objects;
`core.governance` owns precondition representation; `core.execution_boundary` owns only the
closed boundary. Splitting into empty micro-packages was rejected.

## Implementation decisions

| ADR | Decision | Reason |
|---|---|---|
| P3S1-01 | Python 3.12+, src layout | modern typing; clean import boundary |
| P3S1-02 | Standard-library runtime | smallest dependency/trust surface |
| P3S1-03 | `namespace:token` IDs | type and domain remain explicit |
| P3S1-04 | positive integer object versions | identity/version separation; no latest |
| P3S1-05 | frozen slotted dataclasses | immutable records without framework |
| P3S1-06 | canonical UTF-8 JSON v1 | deterministic portable representation |
| P3S1-07 | SHA-256 fingerprints | persistent deterministic hash, never `hash()` |
| P3S1-08 | UTC-only foundational timestamps | naive/local timestamps fail closed |
| P3S1-09 | explicit state-axis assignments | prevents universal-status conflation |
| P3S1-10 | pytest + ruff + mypy | lightweight tests, format/lint, strict typing |
| P3S1-11 | no Hypothesis yet | finite contracts have direct tests; avoid decorative dependency |
| P3S1-12 | EXE-01 exposes rejection only | execution capability remains impossible |

Technical decisions do not close governance decisions belonging to competent authorities.

## Preconditions

This table reproduces Sprint 12 Section 48, with honest Sprint 1 status.

| ID | Status | Sprint 1 effect | Blocks |
|---|---|---|---|
| IP-01 authentication | OPEN | no authentication runtime | IAM/commands/agents |
| IP-02 integrity/signatures | PARTIALLY_RESOLVED | SHA-256 only | signed evidence/audit |
| IP-03 authority/delegation | OPEN | IDs grant no authority | consequential mutation |
| IP-04 serialization/ID/hash | PARTIALLY_RESOLVED | Sprint 1 canonical JSON/IDs/hash | later data/contract formats |
| IP-05 time/ordering | PARTIALLY_RESOLVED | UTC foundation only | domain temporal ordering |
| IP-06 emergency/release roles | OPEN | no runtime | emergency commands |
| IP-07 approval/expiry | OPEN | no runtime | decision/command admission |
| IP-08 freshness | OPEN | UNASSESSED is explicit | validation/monitoring use |
| IP-09 validation methods | OPEN | deferred by scope | validation engine |
| IP-10 monitoring methods | OPEN | deferred by scope | monitoring engine |
| IP-11 data quality/reconciliation | OPEN | deferred by scope | Data Engine |
| IP-12 retention/privacy/legal | OPEN | no persistence/deletion | durable ledgers/data |
| IP-13 external trust/adapters | OPEN | no adapters/network | external interfaces |
| IP-14 implementation governance | PARTIALLY_RESOLVED | package/CI/traceability | wave promotion/release |

Counts: **0 RESOLVED / 4 PARTIALLY_RESOLVED / 10 OPEN / 0 DEFERRED**.
Every non-resolved item evaluates false and raises if required as resolved.

## Invariants and traceability

| Component | Phase 2 source / requirement | Tests | Failure |
|---|---|---|---|
| typed IDs/versions | S2 IAM; S3 exact version; S12 IP-04 | `test_model` | reject invalid/latest/raw confusion |
| envelopes/provenance | S3 Artifact/Evidence contracts | `test_model` | reject missing type/scope/provenance/time |
| serialization/fingerprint | S3/S12 IP-02/04 | `test_model` | reject malformed/noncanonical/nonfinite |
| state vector | S4 orthogonal axes | governance-negative tests | reject duplicate/conflated axes |
| preconditions | S12 §48 | `test_governance` | OPEN/PARTIAL blocks domain |
| EXE-01 | S2/S4/S5/S12 Gate J | governance-negative tests | ExecutionBoundaryViolation |

Executable assertions begin enforcing: ID ≠ version; result ≠ evidence type; audit records do not
authorize; state axes stay distinct; OPEN ≠ satisfied; validation/approval do not imply execution;
EXE-01 is closed. Command, authority, monitoring, halt/release, and kill/reactivation production
objects remain absent until their preconditions are closed.

## Verification

CI executes on Python 3.12 and 3.13:

`ruff format --check .`
`ruff check .`
`mypy`
`pytest`
`pytest tests/test_governance_negative.py`

Tests require no network or current market data. The diff must contain no executable trading
concepts except negative tests and explicit prohibitions.

## Readiness after Sprint 1

- **CORE_READY** after CI passes: IDs, versions, immutable envelopes, serialization, audit metadata.
- **DATA_FOUNDATION_NOT_READY**: IP-05/IP-11/IP-12 remain.
- **EXPERIMENT_NOT_READY**: data and authority dependencies remain.
- **VALIDATION_NOT_READY**: IP-08/IP-09 remain.
- **MONITORING_NOT_READY**: IP-08/IP-10 remain.
- **COMMAND_NOT_READY**: IP-01/IP-03/IP-06/IP-07/IP-13 remain.
- **EXECUTION_CLOSED**: EXE-01 remains PLANNED_CLOSED.

Recommended Sprint 2: close the bounded canonical representation specification and implement
artifact/evidence/audit envelope round-trip codecs plus traceability and integrity golden vectors.
Do not start a domain engine.
