# AI Quant Lab — Phase 3 Sprint 27
## Governed TradingView CSV Adapter v1.0

### Baseline
- Repository: `HannibalQuant/AI-Quant-Lab`
- Governed predecessor: Phase 3 Sprint 26
- Sprint 27 base main: `490a8513fa9145a0d9e2e695dbfe1f660f7bdb8b`
- Constitutional baseline remains `v1.0 / 50b61266f880cb9657b7f1b477d3d90825fe013f`

### Purpose
Accept a bounded operator-supplied TradingView historical bar export as a source snapshot and
produce the canonical CSV shape already required by the existing controlled historical
onboarding pipeline. This sprint is an adapter only. It does not weaken admission,
eligibility, experiment authorization, validation, optimization, Pine, or deployment gates.

### Supported v1 profile
The source must explicitly map:
- bar-open epoch timestamp;
- open, high, low, close;
- optional volume. When the source export has no volume, the canonical profile omits the
  volume column and downstream schema must declare `VolumeSemantic.ABSENT`.

Extra TradingView columns, including exported indicators, are ignored by the adapter and
are never promoted into governed OHLCV evidence. Missing volume is represented as absent,
never as an empty or zero value.

The operator must explicitly declare:
- UTC source timestamps;
- epoch unit (seconds or milliseconds);
- exact governed timeframe;
- authority to derive `bar_close_time = bar_open_time + timeframe duration`;
- that the supplied rows are a historical/confirmed-bar export and may therefore be
  represented as `final`;
- that confirmed-bar research uses bar close as the earliest modeled availability time.

The downstream declaration records these facts truthfully as derived semantics:
- `TimestampSemantics.BAR_OPEN_UTC_CLOSE_DERIVED_FROM_TIMEFRAME`;
- `AvailabilitySemantics.DERIVED_BAR_CLOSE_UTC`.

They are distinct from source-explicit close/availability semantics and cannot be silently
substituted for them.

If those declarations are absent, the adapter fails closed. The code does not claim that
derived close/finality/availability fields physically existed in the source export.

### Lineage
The adapter records and returns the SHA-256 of the exact original source bytes. It also
computes a separate SHA-256 for deterministic canonical output. It emits a bounded
machine-readable provenance note containing both hashes. Derived-semantics onboarding
requires that note and verifies that its canonical hash matches the exact evaluated
canonical file. The persisted source declaration therefore preserves the original-source
to canonical-file lineage without claiming that derived fields existed in the source.
The source file is never rewritten. Canonical output cannot silently overwrite an existing
file.

### Security and boundedness
- local files only;
- explicit absolute allowed root;
- lowercase `.csv` only;
- no symlink input;
- existing controlled-historical 8 MB / 20,000-row budget;
- bounded header width and line length;
- strict UTF-8;
- duplicate/missing mappings rejected;
- strictly ascending unique bar opens;
- governed timeframe alignment enforced.

### Research Run #1
The user has accepted SOLUSDT 4H research beginning on 2022-01-03 rather than
2022-01-01. Sprint 27 makes the TradingView export format admissible for the *next*
existing governance stages after the adapter output is passed through normal controlled
historical onboarding and eligibility. It does not itself claim admission or research
eligibility.

### Explicit non-goals
No:
- broker or exchange connectivity;
- live or paper execution;
- TradingView login/browser automation;
- network acquisition;
- Pine compiler;
- webhook execution;
- autonomous agent/orchestrator identity;
- silent inference of source permission;
- deployment authorization.

Execution remains `PLANNED_CLOSED`; deployment remains `NOT_AUTHORIZED`.

### Verification gate
Sprint 27 is complete only after:
1. focused adapter tests pass;
2. full pytest passes;
3. `ruff format --check .` passes;
4. `ruff check .` passes;
5. strict mypy passes;
6. GitHub Actions matrix is green;
7. adapter -> controlled real CSV onboarding integration coverage passes with exact
   source/canonical lineage and derived semantics;
8. final PR re-review confirms no scope/governance regression.
