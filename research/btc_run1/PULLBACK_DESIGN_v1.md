# BTC Run #1 — Pullback research design v1

Baseline `ac3daf5359e82e5fadf35d9b9e3cbc002f0ca98d`; issue #101. Status: PREREGISTERED_PENDING_REVIEW_NOT_AUTHORIZED. PR #109 merged after successful Python 3.12/3.13 CI. This design is informed by development results already observed and does not create an independent statistical test.

PB0 is one fixed LONG+SHORT hypothesis. Keep T0 EMA20/50/200, RSI/MACD/ADX/DMI direction conditions and all risk settings. Change only entry: require exactly the preceding completed bar to pull back to EMA20, then current close to reclaim EMA20 and break the preceding bar extreme.

| Side | Previous bar | Current confirmed bar |
|---|---|---|
| LONG | low <= EMA20 and close <= EMA20 | T0 LONG direction; close > EMA20 and close > previous high |
| SHORT | high >= EMA20 and close >= EMA20 | T0 SHORT direction; close < EMA20 and close < previous low |

EMA values belong to their own bar. Both bars must be after indicator-only warmup: current index >=1001 (zero based). Flat position required; no pending order or pyramiding. No setup search, optimization or extra variants. Use production Decimal arithmetic. Signal after availability; fill first eligible later open inside development only.

Keep entry-signal ATR, 2ATR initial stop, 2R target, 1R break-even trigger, 48-bar time stop and opposite **T0 direction** exit. Stops/TP/BE remain confirmed-bar conditions with subsequent-open fills; they are not intrabar price-level fills. No forced closing or validation bar to complete a terminal order.

Use the exact locked 8760-bar development dataset from 2025-04-01 inclusive to 2026-04-01 exclusive; 1000-bar warmup; capital1000 USDT, fixed notional100 USDT. PB0 has exactly three future attempts: base commission/slippage10/5bps per fill, stress20/10bps, and zero-cost diagnostic0/0bps. Existing six attempts remain immutable; cumulative screening budget nine. No T0/T1 reruns or ranking. Funding unavailable/unmodeled blocks economic promotion.

The original absolute gates remain: >=80 completed base trades and >=30 per direction, positive net, PF>=1.10, drawdown <=5% initial capital, >=3 positive quarters with worst >=-2%; stress positive net, drawdown <=7.5%, positive SHORT base/stress with >=30 SHORT trades in both. Missing activity is INCONCLUSIVE, thresholds stay fixed. Undefined PF fails. Zero cost never supports promotion. Passing remains exploratory and requires separately authorized untouched validation and later walk-forward before any candidate decision.

**Implementation boundary:** existing production model has immediate trend entries and cannot represent PB0. Do not pretend this document authorizes executable experiments. A separate reviewed/versioned strategy and engine change must bind exact PB0 semantics, retain old golden fingerprints and SOL behavior, and prove timing, warmup, opposite-direction exit and accounting with synthetic tests. No BTC PB0 performance inspected while drafting.

Machine specification, exact dataset/manifest/lock refs, inherited parameters, costs and gates: `pullback_design_v1.json`. Validation/OOS, optimization, Pine and deployment remain unauthorized.

Next concrete step: implement isolated versioned PB0 entry support and complete targeted review/CI; only then authorize the three exact experiments.
