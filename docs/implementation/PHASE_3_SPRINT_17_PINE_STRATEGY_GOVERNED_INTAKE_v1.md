# Phase 3 Sprint 17: Pine Strategy Contract & Governed Strategy Intake v1.0

## 1. Baseline

Implementation starts from governed `main` commit
`bcdda7e48553f0ebc26384dc2e0f75ed25731aee`, merged predecessor PR #77, reviewed predecessor
head `26f7fc49df2eac524046cca6f0034997dbe97261`, and constitutional baseline v1.0 at
`50b61266f880cb9657b7f1b477d3d90825fe013f`.

## 2. Mission

Sprint 17 admits an exact local Pine strategy source into immutable research custody and binds it to
the exact governed strategy and evidence chain. Intake establishes source identity and lineage only.

## 3. Non-goals

There is no Pine execution, compiler, generator, TradingView call, browser automation, webhook,
network client, broker, deployment, live execution, Pine/Python parity, repaint determination or new
optimizer. Existing strategy logic and evidence are not redesigned.

## 4. Pine artifact contract

`PineStrategySourceArtifact` is frozen and versioned. It contains exact submitted and normalized
source, raw and normalized SHA-256, byte size, Pine version, script kind, static title, bounded
`strategy()` settings, exact strategy/candidate/selection/evidence references, authority and
provenance, and closed downstream authority states.

## 5. Source normalization

Normalization changes CRLF and bare CR line endings to LF. It does not add a newline, strip comments,
collapse whitespace, format code, rename identifiers, alter literals or reorder text. The exact
submitted UTF-8 text and normalized text are both persisted.

## 6. Hashing

`source_sha256` hashes exact submitted bytes. `normalized_source_sha256` hashes normalized UTF-8.
CRLF and LF inputs therefore have different raw hashes but may have the same normalized hash. A
one-character semantic or textual change changes raw hash, normalized hash and artifact fingerprint.

## 7. Static declaration extraction

A bounded lexical mask excludes quoted strings, line comments and block comments before declaration
classification. Exactly one column-zero `strategy(` or `indicator(` declaration is recognized. The
scanner extracts only a trivial static quoted title and literal required settings; it is not a Pine
parser or syntax validator.

## 8. Version support

Exactly one standalone `//@version=6` declaration is required. Missing, duplicate, conflicting or
non-v6 declarations fail closed. Version text inside unrelated comments does not grant support.

## 9. Script-kind classification

`STRATEGY` is the only accepted kind. `INDICATOR` is rejected and no declaration is incomplete.
Multiple top-level declarations are rejected. Strings and ordinary comments cannot manufacture a
strategy declaration.

## 10. Compatibility profile

The accepted static profile is deliberately narrow: long-only governed strategy binding,
`pyramiding=0`, `process_orders_on_close=false`, `calc_on_every_tick=false`,
`default_qty_type=strategy.cash`, and exact fixed-notional `default_qty_value` reconstructed from
`StrategyDefinition`. Signals remain close-evaluated and execution remains the governed next-bar-open
model. External/dynamic `request.*`, legacy `security()`, timeframe-mixing and alert/webhook-style
constructs are unsupported. These checks establish declaration compatibility, never runtime parity.

## 11. Strategy binding

The request and artifact carry a fingerprint-bearing reference to the exact `StrategyDefinition`.
The verifier compares the full object and reference; strategy ID alone is insufficient. Direct
non-optimization binding is supported only with the exact strategy-specific backtest, scientific and
robustness evidence.

## 12. Optimization candidate binding

Candidate binding is all-or-none: candidate definition, candidate result and selection references
must all be supplied. The authoritative Sprint 16 verifier is rerun. Selection must be `SELECTED`,
its selected reference must be the supplied result, and both candidate contracts must bind the exact
Pine strategy. Parent or rejected candidate evidence cannot substitute.

## 13. Evidence binding

Every accepted artifact binds exact `BacktestResultArtifact`, `ScientificValidationResult` and
`RobustnessValidationResult` references. Candidate intake requires candidate-specific evidence; it
cannot reuse the parent's favorable evidence.

## 14. Lineage verification

`verify_pine_strategy_intake_lineage()` rebuilds source analysis, re-runs robustness lineage (which
recursively re-verifies scientific validation, backtest, dataset, replay and accounting), optionally
re-runs the full optimization-selection lineage, and reconstructs the expected artifact, input
fingerprint and intake record. Equality is exact and deterministic.

## 15. Semantic parity

Every accepted artifact records `PineSemanticParityStatus.NOT_EVALUATED`. Reference binding does not
prove Pine implements Python behavior. No stronger state exists in Sprint 17.

## 16. Repaint assessment

Every accepted artifact records `RepaintAssessmentStatus.NOT_EVALUATED`. Static intake makes no
`NO_REPAINT` claim.

## 17. Authority

The intake request must bind the exact governed Pine-intake authority carried by
`PineStrategyIntakeContext.pine_intake_authority_ref`. A merely well-formed
`AuthorityBindingId` with a fingerprint is insufficient. Any mismatch fails closed before
static source admission. This preserves the project invariant that identity is not authority.

Bounded static source failures are audited separately from lineage corruption. Expected source
outcomes such as `REJECTED`, `INCOMPLETE`, and `UNSUPPORTED` produce immutable
`PineStrategyIntakeRecord` evidence with the requested artifact id, raw source hash, normalized
hash when UTF-8 normalization is available, byte size, exact status/reason, authority and
provenance. They do not create a `PineStrategySourceArtifact`. Governance/lineage failures such
as wrong strategy/candidate/evidence or wrong governed authority remain hard failures rather than
ordinary source rejections.



The Pine-intake authority reference is exact and fingerprint-bearing. It authorizes only bounded
local custody acceptance. It does not validate performance, authenticate a real actor or author,
establish parity, approve deployment or open execution.

## 18. Determinism

No wall clock, UUID or uncontrolled randomness is used. Same source, governed references, authority
and provenance produce identical classification, hashes, artifact bytes, input fingerprint, record
bytes and repository keys.

## 19. Persistence

`LocalDatasetRepository` stores `PineStrategySourceArtifact` and `PineStrategyIntakeRecord` under
canonical immutable type/version/fingerprint keys. Strict read verifies canonical reconstruction and
integrity. Identical writes are idempotent; conflicts, corruption, wrong type/version and unknown
fields fail closed. There is no latest/current alias.

## 20. Golden evidence

`tests/golden/pine_strategy_intake_v1.json` pins source hashes and size, Pine version, kind, title,
strategy/candidate/selection and evidence identities, parity/repaint states, intake outcome, input
fingerprint and artifact/record fingerprints. All earlier goldens remain byte-identical.

## 21. Tamper detection

Tests mutate raw source, raw/normalized hashes, strategy and evidence fingerprints, candidate and
selection references, stored bytes, input fingerprint and intake status. Exact lineage or repository
integrity rejects every mutation.

## 22. Tests

Focused coverage includes valid selected-candidate and direct intake, Pine v6/version failures,
strategy/indicator/comment/string classification, duplicate declarations, UTF-8/NUL/control and
256 KiB boundaries, line-ending normalization, one-character identity changes, required settings,
unsupported external data, selected-candidate enforcement, full evidence lineage, strict codec,
immutable persistence, determinism, golden evidence and capability isolation.

## 23. Governance BEFORE -> AFTER

| Preconditions | Before | After | Sprint 17 evidence / remaining authority |
|---|---|---|---|
| IP-01 | OPEN | OPEN | Pine authority IDs are not real-world authentication. |
| IP-02 | PARTIALLY_RESOLVED | PARTIALLY_RESOLVED | Source and persisted-byte tamper evidence improves; signatures remain open. |
| IP-03 | OPEN | OPEN | No delegation or revocation authority added. |
| IP-04 | PARTIALLY_RESOLVED | PARTIALLY_RESOLVED | Canonical Pine source/record identity added; broader equivalence authority remains open. |
| IP-05 | PARTIALLY_RESOLVED | PARTIALLY_RESOLVED | No new temporal authority; runtime Pine timing parity is untested. |
| IP-06 | OPEN | OPEN | Emergency/release authority remains absent. |
| IP-07 | OPEN | OPEN | Human approval/expiry remains absent. |
| IP-08 | OPEN | OPEN | Evidence freshness remains ungoverned. |
| IP-09 | PARTIALLY_RESOLVED | PARTIALLY_RESOLVED | Source binds evidence but parity/repaint/TradingView validation remain open. |
| IP-10 | OPEN | OPEN | Monitoring remains outside scope. |
| IP-11 | PARTIALLY_RESOLVED | PARTIALLY_RESOLVED | Dataset quality authority is unchanged. |
| IP-12 | OPEN | OPEN | Pine authorship/licensing/legal authority is not inferred. |
| IP-13 | OPEN | OPEN | Bounded local static checks improve evidence; author/platform authenticity remains open. |
| IP-14 | PARTIALLY_RESOLVED | PARTIALLY_RESOLVED | Golden, tamper and CI evidence advance; release authority remains open. |

Counts remain `RESOLVED 0`, `PARTIALLY_RESOLVED 6`, `OPEN 8`, `DEFERRED 0`.

## 24. Readiness

- `PINE_SOURCE_CONTRACT_READY`
- `PINE_STATIC_INTAKE_READY`
- `PINE_SOURCE_HASHING_READY`
- `PINE_STRATEGY_BINDING_READY`
- `PINE_CANDIDATE_BINDING_READY`
- `PINE_EVIDENCE_LINEAGE_READY`
- `PINE_PERSISTENCE_READY`
- `PINE_TAMPER_DETECTION_READY`
- `PINE_GOLDEN_EVIDENCE_READY`
- `PINE_SEMANTIC_PARITY_NOT_READY`
- `PINE_REPAINT_ASSESSMENT_NOT_READY`
- `TRADINGVIEW_COMPILATION_NOT_READY`
- `TRADINGVIEW_PARITY_NOT_READY`
- `BROKER_NOT_READY`
- `DEPLOYMENT_NOT_READY`
- `LIVE_EXECUTION_NOT_READY`
- `EXECUTION_CLOSED`

## 25. Blockers

Pine/Python event parity, TradingView compilation and platform evidence, repaint analysis, source
authorship/authentication, licensing, protected platform export custody, deployment authority and
live execution remain blocked.

## 26. Limitations

The scanner recognizes only a deliberately narrow static declaration grammar. It does not prove
general Pine syntax, compilation, runtime behavior, signal equivalence, order equivalence, numeric
parity, no-repaint behavior or TradingView support. Failed intake is exposed as a deterministic typed
status/reason exception and is not persisted as an accepted governed source artifact.

## 27. Sprint 18 recommendation only

After independent review and merge, the recommended next sprint is **Pine ↔ Python Parity Validation
v1.0**, using exact exported Pine/TradingView evidence and governed Python events. Sprint 18 is not
implemented here.

## 28. Disposition

`PHASE 3 SPRINT 17 COMPLETE WITH OPEN PRECONDITIONS`