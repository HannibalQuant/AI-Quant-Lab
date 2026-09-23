# Phase 3 Sprint 18 — Pine ↔ Python Parity Validation v1.0

## 1. Baseline

- Governed main: `75feedad18f6c041100d85f8ff203468cdd43867`
- Constitutional baseline: v1.0 / `50b61266f880cb9657b7f1b477d3d90825fe013f`
- Predecessor: PR #78 / reviewed head `5c39fb8465461efd01762f037c0dfcffe4a35d58`

## 2. Mission

Sprint 18 introduces local, deterministic, event-level comparison between the exact independently
reverified Python backtest and externally supplied Pine/TradingView execution evidence. It does not
execute Pine or contact TradingView.

## 3. Non-goals

No Pine compiler, browser automation, TradingView API, webhook, broker connectivity, deployment
authorization or live execution is added. EXE-01 remains `PLANNED_CLOSED`.

## 4. Pine execution evidence

`PineExecutionEvidence` preserves the exact UTF-8 CSV text, SHA-256, byte size, exact Pine
artifact/strategy/instrument/dataset refs, observation window, ordered parsed events, provenance
and exact parity authority.

## 5. Local evidence import

Only `CSV_V1` is supported. Columns are closed and ordered:
`event_index,signal_time,execution_time,action,side,execution_price,position_after,quantity,commission,trade_id`.
Unknown/missing columns fail closed.

## 6. Source hashing

The stored source text is re-encoded as UTF-8 and must reproduce both byte size and SHA-256.
Tampering changes canonical identity.

## 7. Event contract

Events are contiguous from index zero, strictly execution-time ordered, long-only, and follow a
FLAT -> ENTRY/LONG -> EXIT/FLAT state machine. Same-time signal/execution is representable so the
parity layer can report it as an explicit no-lookahead mismatch rather than hiding it as a parser
error.

## 8. Timestamp semantics

All source timestamps require an explicit offset and normalize to UTC. Naive timestamps fail
closed. Timestamp comparison is exact in v1.

## 9. Expected Python trace

Expected events are derived directly from the authoritative `BacktestResultArtifact` orders and
fills only after `verify_strategy_backtest_lineage()` independently reconstructs the Python
backtest.

## 10. No-lookahead / next-bar-open semantics

Python signal time and exact fill time are compared event by event. Same-time execution or any
one-bar/other execution shift is `EXECUTION_TIME_MISMATCH`.

## 11. Tolerance policy

`ParityTolerancePolicy` uses Decimal text only. Structural dimensions and timestamps are exact.
Price supports explicit absolute and relative tolerance; quantity, commission and PnL have
explicit absolute tolerances. Relative price tolerance is bounded at 1%.

## 12. Structural parity

Event existence, action, side, signal time, execution time, position state and trade count cannot
be hidden by numeric tolerance.

## 13. Numeric parity

Execution price, quantity and commission are compared with Decimal arithmetic. PnL tolerance is
contracted for later evidence that exposes comparable PnL; aggregate PnL does not override any
event-level mismatch.

## 14. Open-position handling

The Python backtest's `open_position` is compared with the observed final Pine state. No forced
close is invented.

## 15. Costs and slippage

Execution price is compared as the executed price. Commission is compared separately. Slippage is
not double-counted.

## 16. Mismatch taxonomy

Structured mismatches include missing/extra event, action/side, signal/execution time, price,
quantity, commission, position state, trade count and PnL categories.

## 17. Decision semantics

- `MATCH`: no structural or numeric mismatch.
- `MISMATCH`: at least one deterministic mismatch.
- `INCONCLUSIVE`: external trace is absent while Python expects events.

A matching aggregate result never overrides an event mismatch.

## 18. Lineage

`verify_pine_python_parity_lineage()` rebuilds the complete result from independently reverified
Sprint 17 Pine intake, Python backtest, exact evidence, tolerance and authority bindings.

## 19. Authority

Parity request, Pine execution evidence and tolerance policy must all bind the exact governed
parity authority. A merely fingerprint-bearing alternate authority is insufficient. Parity
authority grants no scientific-validation, deployment or execution authority.

## 20. Determinism

No clock, random UUID or RNG participates. Same inputs produce the same evidence, mismatches,
decision, fingerprints and canonical bytes.

## 21. Persistence

Tolerance policy, Pine execution evidence, parity result and parity run record are immutable
LocalDatasetRepository objects with strict canonical codecs, idempotent identical writes and
corruption detection.

## 22. Golden evidence

A repository-owned deterministic parity golden pins the positive exact-match result after the
focused fixture is validated. Prior sprint goldens remain unchanged.

## 23. Tamper detection

Exact CSV bytes, evidence refs, source hashes, result summaries and lineage are all fingerprint
bound. Rebuilding the lineage rejects persisted substitutions.

## 24. Tests

Focused coverage includes exact match, no-lookahead/same-time execution, execution shift,
missing events, final-state mismatch, incomplete trace, Decimal price tolerance, timezone
normalization, naive timestamp rejection, authority mismatch and strict CSV columns.

## 25. Governance BEFORE -> AFTER

Conservative governance counts remain unchanged. Sprint 18 adds implementation-parity evidence
without resolving provider authentication, repaint guarantees, deployment or execution.

## 26. Readiness

- PINE_EXECUTION_EVIDENCE_CONTRACT_READY
- PINE_TRACE_IMPORT_READY
- PYTHON_EXPECTED_TRACE_READY
- EVENT_LEVEL_PARITY_READY
- TIMESTAMP_PARITY_READY
- EXECUTION_PARITY_READY
- PRICE_PARITY_READY
- POSITION_STATE_PARITY_READY
- COST_PARITY_READY
- PARITY_LINEAGE_READY
- PARITY_PERSISTENCE_READY
- PARITY_TAMPER_DETECTION_READY
- PINE_REPAINT_ASSESSMENT_NOT_READY
- TRADINGVIEW_COMPILATION_NOT_READY
- TRADINGVIEW_AUTOMATION_NOT_READY
- BROKER_NOT_READY
- DEPLOYMENT_NOT_READY
- LIVE_EXECUTION_NOT_READY
- EXECUTION_CLOSED

## 27. Limitations

This sprint validates supplied historical execution evidence only. It does not establish a general
no-repaint guarantee or prove TradingView compilation. The v1 CSV does not carry an independent
aggregate PnL field, so PnL cannot be used to establish MATCH.

## 28. Sprint 19 recommendation only

Preferred next direction: governed AI Agent -> Quant Lab -> Pine -> TradingView research workflow.
No Sprint 19 implementation is included here.

## 29. Disposition

`PHASE 3 SPRINT 18 COMPLETE WITH OPEN PRECONDITIONS`
