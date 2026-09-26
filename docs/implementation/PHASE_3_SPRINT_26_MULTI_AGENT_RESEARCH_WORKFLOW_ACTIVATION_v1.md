# AI Quant Lab — Phase 3 Sprint 26
# Existing Multi-Agent Research Workflow Activation & Historical Data Scaling v1.0

## 1. Baseline

Sprint 26 starts from governed `main`:

`d8dcc8e7b8831756698b512694ac0aec8f313836`

This is the merge commit of Phase 3 Sprint 25 / PR #87.

Constitutional baseline remains:

- tag: `v1.0`
- commit: `50b61266f880cb9657b7f1b477d3d90825fe013f`

No prior governed sprint artifact is rewritten.

## 2. Purpose

Sprint 26 does **not** add a new institutional agent.

It activates the already-built current-order research path for the Sprint 24/25
`MULTI_SIGNAL_TREND_LONG_SHORT` strategy profile and removes the bounded historical
CSV resource limit that prevented a multi-year SOLUSDT 4H research dataset from being
admitted as one file.

The intended operating model remains the original project model:

`Founder / conversational coordinator -> existing specialist roles -> governed research runtime -> Pine -> manual TradingView research`

The conversational coordinator is outside the repository runtime. The repository
contains the governed evidence pipeline and specialist contracts; it does not create a
new autonomous LLM, broker, browser robot, or hidden deployment authority.

## 3. Existing specialist-role boundary

Sprint 26 preserves the existing roles and their responsibilities:

- `AIQL-AGENT-MARKET-RESEARCH` — market observation/research context;
- `AIQL-AGENT-RESEARCH-LIBRARIAN` — knowledge/source stewardship;
- `AIQL-AGENT-QUANT-STRATEGY-ARCHITECT` — strategy architecture and experiment proposal;
- `AIQL-AGENT-QUANT-STRATEGY-ENGINEER` — faithful research implementation;
- `AIQL-AGENT-EXPERIMENT-ORCHESTRATOR` — experiment operations and run lifecycle;
- `AIQL-AGENT-VALIDATION` — independent scientific/robustness validation;
- `AIQL-AGENT-RISK-GOVERNANCE` — independent deployment-risk authority when that
  future stage is requested;
- `AIQL-AGENT-EXECUTIVE-DECISION` — institutional integration/decision authority,
  not strategy creation or validation.

No role is broadened by this sprint.

## 4. Existing executable path reused

Sprint 26 reuses, without redesign:

- controlled real CSV onboarding;
- research dataset eligibility;
- experiment authorization;
- deterministic strategy backtest runtime;
- Sprint 25 multi-signal LONG/SHORT runtime;
- scientific validation;
- robustness validation;
- bounded deterministic optimization;
- governed Pine v6 generation;
- governed Pine intake;
- static Pine safety validation;
- TradingView research export;
- Phase 3 current-order end-to-end closure.

The activation coverage proves two complementary properties:

- existing multi-signal governed evidence can bind to deterministic Pine v6 generation
  and governed Pine intake with exact lineage;
- the final Phase 3 closure remains fail-closed when scientific validation is not
  `PASS`, so inconclusive research cannot be promoted to a manual TradingView export.

Sprint 25 separately verifies the bounded multi-signal optimization path through
candidate derivation, backtest, scientific validation, robustness, and deterministic
selection. Sprint 26 does not force an optimization candidate to be selected and does
not manufacture a scientific `PASS` when the controlled sample is inconclusive.

The authoritative intended path remains:

`real CSV -> eligibility -> authorization -> multi-signal backtest -> validation -> robustness -> optional governed selection -> Pine generation/intake -> final closure -> manual TradingView export`

The final closure advances past validation only when its existing PASS gates are
satisfied. No Pine↔Python parity claim is created by this test. TradingView runtime
remains `NOT_VERIFIED_ON_TRADINGVIEW`.

## 5. Historical data scaling

Before Sprint 26, both repository fixtures and controlled historical CSV input used:

- `MAX_FILE_BYTES = 1_000_000`
- `MAX_ROWS = 2_000`

That historical-data resource envelope cannot carry the requested continuous
2022-01-01 through 2026-01-01 SOLUSDT 4H window (approximately 8,766 bars).

Sprint 26 preserves the smaller repository-fixture limits and adds a separate bounded
resource envelope only for `CONTROLLED_HISTORICAL`:

- `MAX_CONTROLLED_HISTORICAL_FILE_BYTES = 8_000_000`
- `MAX_CONTROLLED_HISTORICAL_ROWS = 20_000`

The existing fixture limits remain 1 MB / 2,000 rows.

The security boundary remains explicit and finite. The sprint does not introduce:

- URL download;
- network market-data adapters;
- recursive discovery;
- wildcard import;
- symlink/traversal relaxation;
- arbitrary file types;
- mutable dataset aliases;
- silent source trust;
- silent research eligibility.

Existing UTF-8, path, schema, timestamp, OHLC, ordering, gap, finality, availability,
source declaration, immutable lineage, and permission gates remain unchanged.

## 6. Sprint 26 verification

New focused coverage proves:

1. A controlled historical CSV with 8,766 valid rows can be parsed inside the bounded
   resource envelope.
2. A file exceeding the new row limit still fails closed.
3. Existing `MULTI_SIGNAL_TREND_LONG_SHORT` governed evidence generates deterministic
   Pine v6 containing both LONG and SHORT entries and is accepted by governed Pine
   intake with exact evidence lineage.
4. The final Phase 3 closure rejects that same controlled sample when scientific
   validation is not `PASS`; no test or runtime path promotes inconclusive evidence.
5. Sprint 25's separate optimization E2E coverage remains the authority for the
   bounded multi-signal optimization path.
6. All generated research artifacts remain:
   - deployment `NOT_AUTHORIZED`;
   - execution `PLANNED_CLOSED`;
   - TradingView runtime unverified until a package legitimately reaches that stage.

## 7. Research Run #1

Registered issue:

`#88 — Research Run #1 — SOLUSDT 4H Multi-Signal Trend Research (2022–2026)`

After Sprint 26, the importer-size blocker and the multi-signal Pine
generation/intake integration blocker are removed. The existing final closure remains
intentionally conditional on scientific and robustness PASS evidence.

The remaining external input is the exact governed historical source bytes for
SOLUSDT 4H covering the requested period, together with the source declaration needed
by the existing admission and eligibility gates.

No synthetic data may be substituted and represented as the requested real research
dataset.

## 8. Non-goals

Sprint 26 does not add:

- a new Agent Orchestrator identity;
- a new CEO agent identity;
- an in-repository autonomous LLM runtime;
- broker or exchange connectivity;
- live or paper execution;
- TradingView login/browser automation;
- webhook execution;
- automatic deployment;
- a Pine compiler;
- a claim of TradingView runtime verification.

## 9. Final target after merge

The bounded manual-research target remains:

`user research mandate -> conversational coordinator -> existing governed specialist workflow -> research evidence -> selected strategy -> governed Pine v6 -> manual TradingView research`

The repository remains fail-closed at deployment/execution boundaries.

## 10. Sprint disposition

Sprint 26 may be marked complete only after:

- focused Sprint 26 tests pass;
- full pytest passes;
- Ruff format/check pass;
- strict mypy passes;
- governance-negative tests pass;
- GitHub Actions matrix is green;
- final PR re-review confirms no authority expansion and no execution capability.
