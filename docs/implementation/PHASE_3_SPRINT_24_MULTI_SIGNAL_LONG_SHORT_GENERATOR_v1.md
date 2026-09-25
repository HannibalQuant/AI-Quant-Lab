# Phase 3 Sprint 24 — Multi-Signal Long/Short Strategy Model & Pine Generator Expansion v1.0

## 1. Baseline

- Governed main baseline: `1a90971a980d63735e34ca04834d3a13ef93f452`
- Predecessor: Phase 3 Sprint 23 — End-to-End Pipeline Closure & Real-Data Golden Path v1.0
- Constitutional baseline: `v1.0 / 50b61266f880cb9657b7f1b477d3d90825fe013f`
- Branch: `phase-3/multi-signal-long-short-generator`

## 2. Mission

Sprint 24 expands the previously bounded Pine-generation model from the legacy
`CLOSE_VS_OPEN_LONG_ONLY` profile to a governed multi-signal trend strategy definition capable of
representing and deterministically rendering:

- LONG and SHORT;
- fast / medium / slow EMA trend structure;
- RSI momentum thresholds;
- MACD direction;
- ADX + DMI trend-strength confirmation;
- ATR-derived stop distance;
- take profit expressed in R;
- break-even trigger expressed in R;
- time stop expressed in bars;
- bar-close signal evaluation with first-eligible-next-bar-open order semantics.

The initial intended research target is SOLUSDT 4H.

## 3. Backward compatibility

The existing Sprint 12 / Sprint 20 legacy strategy remains byte-compatible in canonical
serialization. Legacy `StrategyDefinition` records do not gain an extra serialized field and their
generator profile remains:

`AIQL_GOVERNED_PINE_V6_CLOSE_VS_OPEN_LONG_ONLY_V1`.

This prevents Sprint 24 from silently changing historical fingerprints or governed evidence.

## 4. Multi-signal strategy contract

The new profile uses:

- `StrategyModel.MULTI_SIGNAL_TREND_LONG_SHORT`;
- `SidePermission.LONG_SHORT`;
- StrategyDefinition version / contract version 2;
- `MultiSignalTrendParameters` as one closed immutable parameter bundle.

The parameter contract requires:

- `fast_ema < medium_ema < slow_ema`;
- `macd_fast < macd_slow`;
- `0 <= rsi_short_max < rsi_long_min <= 100`;
- `0 < adx_threshold <= 100`;
- positive ATR-stop, take-profit-R and break-even-R declarations;
- positive bounded integer lengths and time-stop bars;
- no pyramiding;
- no implicit force-close at research-window end.

The legacy threshold field is fixed to zero for this profile and carries no hidden signal meaning.

## 5. Pine v6 semantics

The new deterministic generator profile is:

`AIQL_GOVERNED_PINE_V6_MULTI_SIGNAL_TREND_LONG_SHORT_V1`.

LONG entry requires all of the following on a confirmed bar:

- fast EMA > medium EMA > slow EMA;
- close > slow EMA;
- RSI >= long threshold;
- MACD line > signal line;
- ADX >= threshold;
- +DI > -DI.

SHORT entry is the symmetric inverse.

The generated source uses TradingView-native `ta.ema`, `ta.rsi`, `ta.macd`, `ta.dmi` and
`ta.atr` without external or mixed-timeframe data requests.

## 6. Exit semantics

Sprint 24 deliberately keeps execution semantics deterministic and compatible with the existing
next-bar-open governance boundary.

ATR stop, take profit, break-even and time-stop thresholds are evaluated only on confirmed bars.
When an exit condition is observed, `strategy.close` is issued and, with
`process_orders_on_close=false`, the close is intended for the next eligible bar open.

Break-even becomes armed only after a completed bar reaches the declared R trigger. It does not
retroactively alter the same bar's stop semantics.

Opposite-direction signals close the current position first. They do not silently reverse the
position inside the same governed decision.

## 7. No repaint / no external-data expansion

The generator:

- uses confirmed-bar decisions;
- does not use `request.*`;
- does not use `security()`;
- does not enable `calc_on_every_tick`;
- does not enable `process_orders_on_close`;
- does not add browser automation, webhooks, broker connectivity or live execution.

Static source generation therefore remains research-only.

## 8. Versioning and lineage

The existing `StrategyDefinition` record type remains canonical.

Legacy records continue using version 1.

The multi-signal profile uses version 2 and serializes its parameter bundle only for that profile.
The decoder remains strict for both shapes.

The generated Pine source continues to embed the exact StrategyDefinition identity and fingerprint.

## 9. Scope boundary

Sprint 24 expands the **strategy model and deterministic Pine renderer**.

It does **not** claim that the existing Python backtest, scientific validation, robustness or
optimization runtime already executes the new EMA/RSI/MACD/ADX long/short profile.

The current upstream research runtime remains the legacy close-vs-open model until a later sprint
adds exact Python execution semantics and parity tests for the new profile.

Therefore Sprint 24 must not claim:

- multi-signal Python backtest readiness;
- multi-signal optimizer readiness;
- Pine ↔ Python runtime parity;
- TradingView runtime verification;
- deployment authorization;
- live execution.

## 10. Tests

Focused Sprint 24 tests cover:

- strict v2 multi-signal contract construction;
- strict codec round-trip;
- long and short Pine entries;
- EMA, RSI, MACD, ADX/DMI and ATR rendering;
- ATR stop, R take-profit, break-even and time-stop rendering;
- deterministic byte-stable rendering;
- parameter sensitivity;
- invalid-parameter fail-closed behavior;
- side-permission downgrade rejection;
- preservation of the legacy serialized shape.

The full repository suite must remain green.

## 11. Readiness after green CI

- `MULTI_SIGNAL_STRATEGY_MODEL_READY`
- `MULTI_SIGNAL_LONG_SHORT_PINE_RENDERER_READY`
- `EMA_RSI_MACD_ADX_PINE_READY`
- `ATR_SL_TP_BE_TIME_STOP_PINE_READY`
- `LEGACY_STRATEGY_FINGERPRINT_COMPATIBILITY_PRESERVED`
- `MULTI_SIGNAL_PYTHON_BACKTEST_NOT_READY`
- `MULTI_SIGNAL_OPTIMIZATION_NOT_READY`
- `MULTI_SIGNAL_PINE_PYTHON_PARITY_NOT_READY`
- `TRADINGVIEW_RUNTIME_VERIFICATION_NOT_READY`
- `DEPLOYMENT_NOT_AUTHORIZED`
- `EXECUTION_CLOSED`

## 12. Recommended successor

`Phase 3 Sprint 25 — Multi-Signal Python Backtest & Optimization Runtime v1.0`

The successor should implement exact deterministic Python execution for the Sprint 24 profile,
including long/short accounting, indicator warm-up semantics, ATR/TP/BE/time-stop state transitions,
cost/slippage treatment, robust optimization search space and Pine↔Python parity evidence.
