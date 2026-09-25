# Phase 3 Sprint 23 — End-to-End Pipeline Closure & Real-Data Golden Path v1.0

## 1. Baseline

- Governed `main`: `f2d1d5ef391358ccd19adfef46b5aa347ca6c492`
- Predecessor review: Phase 3 End-to-End Readiness & Governance Review v1.0 / PR #84
- Constitutional baseline: `v1.0 / 50b61266f880cb9657b7f1b477d3d90825fe013f`
- Branch: `phase-3/end-to-end-pipeline-closure`

## 2. Mission

Sprint 23 closes the two material findings from the Phase 3 end-to-end review:

- `E2E-B-001`: the Sprint 19 research workflow and the Sprint 20→21→22
  generator/safety/export path were not one authoritative current-order closure;
- `E2E-B-002`: no single CI golden path began with governed real CSV evidence and finished at the
  final TradingView export.

The sprint adds one current-order closure function, one durable closure record and one real-data
golden test spanning the full bounded path.

## 3. Current product target

The governed Phase 3 product target is:

`real CSV → admission → eligibility → authorization → backtest → scientific validation → robustness
→ optional optimization/selection → Pine generation/intake → static safety → manual TradingView
export`.

Broker connectivity, automated order placement and live execution remain outside scope.

## 4. Authoritative current-order sequence

For the current manual TradingView research target the authoritative closure order is:

1. `REAL_CSV_ADMITTED`
2. `DATASET_ELIGIBLE`
3. `EXPERIMENT_AUTHORIZED`
4. `BACKTEST_COMPLETED`
5. `SCIENTIFIC_VALIDATION_PASSED`
6. `ROBUSTNESS_PASSED`
7. optional `OPTIMIZATION_SELECTED`
8. `PINE_GENERATED`
9. `PINE_INTAKE_ACCEPTED`
10. `STATIC_SAFETY_PASSED`
11. `TRADINGVIEW_EXPORT_READY`

TradingView runtime evidence and runtime Pine↔Python parity are deliberately downstream of the
manual export because the export is needed to obtain platform runtime evidence.

## 5. Relationship to Sprint 19

Sprint 19 remains a valid historical governed workflow for its declared research-handoff ordering.

Sprint 23 does not delete or silently rewrite Sprint 19.

For the **current manual TradingView export target**, Sprint 23 is the authoritative closure layer
because it incorporates the capabilities introduced later in Sprints 20, 21 and 22 and places
runtime verification after export.

This resolves the split identified as `E2E-B-001`.

## 6. Upstream readiness gate

The closure fails before Pine generation unless exact upstream evidence is ready:

- real CSV admission = `ADMITTED`;
- dataset eligibility = `ELIGIBLE`;
- experiment authorization = `AUTHORIZED`;
- scientific validation = `PASS`;
- robustness = `PASS`;
- if optimization evidence exists, selection = `SELECTED` with an exact selected candidate.

The later Sprint 20 generator still re-verifies the exact governed Pine-intake/research lineage, so
the closure does not trust these state labels by themselves.

## 7. Pine generation and intake

Sprint 23 invokes the existing Sprint 20 generator with:

- the exact governed StrategyDefinition;
- exact generator authority;
- the existing exact Pine-intake authority;
- exact provenance.

The Sprint 20 path deterministically renders Pine v6 and immediately routes it through the Sprint 17
governed Pine intake.

The closure requires the resulting intake record to be `ACCEPTED`.

## 8. Static safety

The exact generated Pine artifact is passed through Sprint 21.

The closure requires:

- safety decision = `PASS`;
- static repaint status = `NO_STATIC_REPAINT_HAZARD_DETECTED`.

This remains a static claim only.

The Pine artifact runtime repaint state is not upgraded to a TradingView runtime claim.

## 9. TradingView export

The exact generator and safety results are routed through Sprint 22.

The closure requires:

`READY_FOR_MANUAL_TRADINGVIEW_RESEARCH`

and preserves:

`runtime_status = NOT_VERIFIED_ON_TRADINGVIEW`.

The export contains the exact Pine source, source hash, strategy/evidence references, parameters,
symbol/timeframe, normalized dataset references and manual TradingView instructions.

## 10. Durable closure record

`Phase3EndToEndClosureRecord` provides one immutable record of the current-order path.

It binds exact references for:

- source declaration;
- CSV admission;
- research eligibility;
- experiment authorization;
- StrategyDefinition;
- backtest artifact;
- scientific validation;
- robustness result;
- optional optimization selection;
- generated Pine artifact;
- static-safety assessment identity/fingerprint;
- final TradingView export package.

It also records the canonical ordered stages, final manual-research state and explicit
TradingView-runtime status.

The record is stored in `LocalDatasetRepository` under its own stored-object type and has strict
canonical codec support.

## 11. Authority separation

Sprint 23 keeps separate exact authority references for:

- Pine generation;
- Pine intake (already carried by the Pine context);
- static safety;
- TradingView research export;
- final Phase 3 closure.

Closure authority does not mint or substitute any upstream authority.

## 12. Real-data golden path

`tests/test_phase3_end_to_end_closure.py` contains one optimized golden-path test that executes the
existing real-CSV research fixtures and then continues through the final current-order closure.

The test proves in one case:

`real operator-local CSV → admission → eligibility → candidate research evidence → governed
selection → generated Pine → governed intake → static safety → TradingView export → immutable
closure reload`.

It explicitly checks real CSV admission metadata, normalized manifest/lock continuity, exact
research-evidence references, exact final source and immutable reload of both export and closure
records.

This closes `E2E-B-002`.

## 13. Direct strategy path

The same closure also supports the direct governed strategy path.

When no optimization evidence is present:

- the `OPTIMIZATION_SELECTED` stage is omitted;
- the closure record carries no optimization-selection reference;
- the Sprint 22 package also carries no optimization-selection reference.

## 14. Failure behavior

The closure fails closed for:

- wrong closure authority;
- non-admitted CSV evidence;
- non-eligible research data;
- non-authorized experiment evidence;
- scientific validation other than PASS;
- robustness other than PASS;
- optimized path without a selected candidate;
- failed Pine intake;
- failed static safety;
- non-ready TradingView export;
- any exact lineage failure detected by the existing Sprint 17/20/21/22 verifiers.

A failed upstream scientific decision is explicitly tested to prove that it cannot reach export.

## 15. Persistence and canonical codec

The closure record is a first-class governed stored type:

`phase3-end-to-end-closure-record`.

It supports:

- canonical deterministic encoding;
- strict decoding;
- exact fingerprint addressing;
- immutable store;
- verified reload;
- corruption/type/version behavior inherited from `LocalDatasetRepository`.

## 16. Deployment and execution closure

Sprint 23 adds no operational trading capability.

The final closure record remains:

- `deployment_authorization = NOT_AUTHORIZED`;
- `execution_state = PLANNED_CLOSED`.

The implementation contains no broker API, TradingView browser automation, webhook order execution
or live-order submission path.

## 17. Runtime boundary

Sprint 23 intentionally does not claim TradingView runtime verification.

The final state is:

`READY_FOR_MANUAL_TRADINGVIEW_RESEARCH`

with:

`runtime_status = NOT_VERIFIED_ON_TRADINGVIEW`.

Compilation, observed TradingView orders/trades, runtime no-repaint behavior and runtime Pine↔Python
parity remain a separate evidence activity.

This open runtime item does not block the bounded project target of producing a governed Pine package
ready for manual TradingView research.

## 18. Strategy breadth limitation

Sprint 23 does not broaden the strategy model.

The current governed generator remains limited to the bounded
`CLOSE_VS_OPEN_LONG_ONLY` profile and the current optimization profile remains narrow.

General EMA/RSI/MACD/multi-parameter/multi-family strategy generation remains later product work and
is not required for closure of the current bounded Phase 3 target.

## 19. Golden evidence

`tests/golden/phase3_end_to_end_closure_v1.json` pins the optimized real-data closure example,
including:

- closure fingerprint;
- source declaration/admission/eligibility identities;
- strategy/backtest/scientific/robustness/selection identities;
- Pine and export identities;
- source CSV SHA-256;
- normalized dataset manifest/lock;
- Pine source SHA-256;
- safety fingerprint;
- exact ordered stages;
- final readiness;
- runtime state;
- deployment/execution closure.

## 20. Tests

Sprint 23 focused tests cover:

- one real-CSV→TradingView-export optimized golden path;
- direct strategy path;
- exact canonical current-order stages;
- immutable export reload;
- immutable closure reload;
- strict codec roundtrip;
- scientific-failure fail-closed behavior;
- closure-authority mismatch;
- explicit TradingView-runtime non-verification;
- deployment/execution closure;
- capability isolation;
- pinned golden evidence.

The full repository suite must remain green on Python 3.12 and 3.13.

## 21. Closure of review findings

### E2E-B-001

Target state after green CI:

`CLOSED`

Reason: Sprint 23 supplies the authoritative current-order manual-export closure and explicitly
defines the relationship to the older Sprint 19 ordering.

### E2E-B-002

Target state after green CI:

`CLOSED`

Reason: one current CI test begins with governed real CSV evidence and reaches the persisted Sprint 22
TradingView export and persisted Sprint 23 closure record.

## 22. Readiness

After green CI and final re-review:

- `PHASE3_CURRENT_ORDER_PIPELINE_READY`
- `REAL_CSV_TO_PINE_GOLDEN_PATH_READY`
- `REAL_CSV_TO_TRADINGVIEW_EXPORT_GOLDEN_PATH_READY`
- `PHASE3_DURABLE_CLOSURE_RECORD_READY`
- `MANUAL_TRADINGVIEW_RESEARCH_READY`
- `TRADINGVIEW_RUNTIME_VERIFICATION_NOT_READY`
- `TRADINGVIEW_RUNTIME_NO_REPAINT_NOT_READY`
- `GENERAL_MULTI_STRATEGY_GENERATION_NOT_READY`
- `BROKER_DEFERRED`
- `DEPLOYMENT_NOT_AUTHORIZED`
- `EXECUTION_CLOSED`

## 23. Final disposition target

After green CI and the requested short final re-review:

`PHASE 3 SPRINT 23 COMPLETE — BOUNDED MANUAL-TRADINGVIEW PROJECT TARGET CLOSED`

Open items such as TradingView runtime verification and broader strategy-family support remain
explicit future scope, not blockers to this bounded closure.
