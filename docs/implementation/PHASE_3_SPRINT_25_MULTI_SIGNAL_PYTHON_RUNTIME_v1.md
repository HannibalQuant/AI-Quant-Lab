# Phase 3 Sprint 25 — Multi-Signal Python Backtest & Optimization Runtime v1.0

## 1. Baseline

- Governed main baseline: `649c96125c1add10e03ae2ea6b4c71fdbabf202e`
- Predecessor: Phase 3 Sprint 24 — Multi-Signal Long/Short Strategy Model & Pine Generator Expansion v1.0
- Constitutional baseline: `v1.0 / 50b61266f880cb9657b7f1b477d3d90825fe013f`
- Branch: `phase-3/multi-signal-python-runtime`

## 2. Mission

Sprint 25 turns the Sprint 24 strategy declaration into a deterministic governed Python
research runtime.  The runtime supports the closed `MULTI_SIGNAL_TREND_LONG_SHORT` profile with:

- EMA trend structure;
- RSI;
- MACD;
- ADX / DMI;
- ATR;
- LONG and SHORT positions;
- ATR stop;
- take profit expressed in R;
- break-even arming and stop;
- time stop;
- opposite-signal exit;
- explicit commission and slippage;
- fixed-notional sizing;
- first-eligible-next-bar-open fills;
- exact lineage and deterministic replay verification.

The initial research target remains SOLUSDT 4H, but the runtime itself is instrument-neutral within
the governed dataset and capital-denomination contracts.

## 3. Indicator semantics

All indicator state is calculated locally with Decimal128-style arithmetic under the repository's
34-digit half-even numeric context.

The engine computes every indicator incrementally from the authorized replay bars only.  No future
bar is visible to an earlier signal.

EMA uses the standard recursive alpha `2 / (length + 1)`.

RSI uses Wilder-style RMA smoothing of positive and negative close changes.

ATR uses Wilder-style RMA smoothing of true range.

DMI uses Wilder-smoothed true range and directional movement.  ADX is the Wilder-smoothed DX
series.

MACD is the difference between fast and slow EMA with a recursive EMA signal line.

Indicators that require seed history remain unavailable until their deterministic seed is complete.
No trade signal can fire before the entire multi-signal point is ready.

## 4. Signal semantics

LONG requires:

- fast EMA > medium EMA > slow EMA;
- close > slow EMA;
- RSI >= declared long threshold;
- MACD > MACD signal;
- ADX >= declared threshold;
- +DI > -DI.

SHORT requires the symmetric inverse.

Signals are evaluated only after the bar is final and available.  An order is filled only at the
first later bar open whose timestamp is not earlier than the signal bar's explicit availability
time.

This preserves the repository's no-lookahead event semantics even when source availability occurs
after the nominal bar close.

## 5. Position and accounting model

LONG entry is a BUY of the declared fixed notional.

LONG exit is a SELL of the exact open quantity.

SHORT entry is a SELL of the declared fixed notional.  Cash receives the sale proceeds and the
position quantity is stored as negative.

SHORT exit is a BUY of the exact absolute open quantity.

For SHORT positions:

`equity = cash + signed_quantity * mark_price`

therefore the negative marked position value offsets the short-sale cash proceeds.

Gross PnL is direction-aware:

- LONG: `(exit - entry) * quantity`
- SHORT: `(entry - exit) * quantity`

Execution prices already include declared slippage.  Commission is subtracted separately.

An independent accounting verifier reconstructs all fills, trades, cash, signed positions,
realized/unrealized PnL, equity, total return and maximum drawdown before lineage acceptance.

## 6. Risk-state semantics

At entry, the engine pins the ATR known at the source signal event.

For LONG:

- initial stop = entry - ATR * stop multiplier;
- target = entry + risk distance * take-profit R;
- break-even trigger = entry + risk distance * break-even R.

For SHORT the formulas are symmetric.

Break-even is armed only after a completed bar reaches the trigger and only if no exit was already
required on that bar.  Once armed, a later completed bar crossing the entry price requests a
break-even exit.

Time stop uses completed bars since the actual fill bar.

All risk exits request a close for the first eligible later bar open.  Sprint 25 does not silently
fill stop/target orders intrabar at the threshold price; this is intentionally aligned with the
Sprint 24 generated Pine close semantics and the existing governed next-bar-open boundary.

Opposite signals close the existing position first.  The runtime does not perform a same-event
LONG↔SHORT reversal.

## 7. Dedicated replay engine identity

Sprint 25 introduces:

`multi-signal-trend-long-short-backtest-engine-v1`

The legacy:

`close-vs-open-long-only-backtest-engine-v1`

remains unchanged.

The runner dispatches by exact StrategyModel and requires the StrategyDefinition,
ExperimentSpecification and authorization policy to bind the exact matching engine reference.

## 8. Optimization runtime expansion

The bounded grid-search contract now supports the multi-signal parameter family while preserving
legacy `threshold_bps` behavior.

Supported integer grid names include:

- fast / medium / slow EMA;
- RSI length;
- MACD fast / slow / signal;
- ADX length;
- ATR length;
- time-stop bars.

Decimal strategy parameters are represented canonically as integer x100 search values:

- `rsi_long_min_x100`;
- `rsi_short_max_x100`;
- `adx_threshold_x100`;
- `atr_stop_mult_x100`;
- `take_profit_r_x100`;
- `break_even_trigger_r_x100`.

Candidate derivation converts x100 integers back to canonical decimal text and rebuilds the exact
immutable `MultiSignalTrendParameters`.

Cross-parameter invariants remain fail-closed.  For example, a candidate with
`fast_ema >= medium_ema` is rejected during deterministic derivation rather than silently repaired.

The existing Bonferroni, scientific-validation and robustness-selection governance remains
unchanged.

## 9. Backward compatibility

Sprint 25 does not change the serialized shape of legacy StrategyDefinition records.

The legacy backtest engine and legacy accounting verifier remain available and continue to use the
same exact engine identity.

Existing optimization search spaces using only `threshold_bps` retain their prior canonical
representation and derivation behavior.

## 10. Safety boundary

Sprint 25 remains research-only.

It adds no:

- broker connection;
- exchange API;
- order submission;
- TradingView browser automation;
- webhook execution;
- credential handling;
- live/paper account execution;
- dynamic plugin loading;
- network dependency in the runtime.

Deployment remains `NOT_AUTHORIZED`.

Execution remains `PLANNED_CLOSED`.

## 11. What Sprint 25 does not claim

Sprint 25 does not claim TradingView runtime equivalence.

The existing Sprint 22 parity subsystem is still LONG-only and must be explicitly expanded before
multi-signal Pine↔Python parity can be governed.

Therefore after Sprint 25:

- multi-signal Python backtest: READY;
- multi-signal bounded parameter derivation/grid runtime: READY;
- multi-signal scientific/robustness pipeline compatibility: READY through the generic governed
  backtest evidence path;
- multi-signal Pine renderer: READY from Sprint 24;
- multi-signal Pine↔Python parity: NOT READY;
- TradingView runtime verification: NOT VERIFIED;
- deployment: NOT AUTHORIZED;
- execution: CLOSED.

## 12. Recommended successor

`Phase 3 Sprint 26 — Multi-Signal Pine ↔ Python Parity Expansion & SOLUSDT 4H Research Run v1.0`

The successor should extend external Pine execution evidence to SHORT events, verify exact
multi-signal event/state parity, and then run the governed SOLUSDT 4H 2022–2026 research dataset
through backtest, validation, robustness and bounded optimization.
