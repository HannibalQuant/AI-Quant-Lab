# Research Run #3 — Candidate #2 Champion Freeze & Governed Research Handoff v1.0

## 1. Control

- Repository: `HannibalQuant/AI-Quant-Lab`
- Freeze baseline: `0b66ae82b776693cb20054801eccedc45191b7d6`
- Constitutional baseline: `v1.0 / 50b61266f880cb9657b7f1b477d3d90825fe013f`
- Research issue: `#96`
- Final Pine artifact: `docs/research/artifacts/AIQL_RR3_SOLUSDT_4H_CANDIDATE_2_FINAL.pine`
- Final Pine SHA-256: `4c3857331eba9c1c7cf141c91c63595ae9d7fa0ac3e719cc1abf9a5891e6aaf3`

This record freezes the selected Research Run #3 candidate for manual TradingView research
and forward observation. It does not authorize broker connectivity, order routing, paper
execution, live execution, or deployment.

## 2. Champion identity

Research status:

`FROZEN_RESEARCH_CHAMPION`

Strategy family:

`MULTI_SIGNAL_TREND_LONG_SHORT + REGIME_FILTERS`

Instrument / timeframe:

`BITGET:SOLUSDT.P / 4H`

Frozen Candidate #2 parameters:

- EMA: `12 / 72 / 160`
- RSI length: `10`
- RSI LONG threshold: `61`
- RSI SHORT threshold: `38`
- MACD: `7 / 49 / 17`
- ADX length / threshold: `14 / 20`
- ATR length: `14`
- ATR stop: `2.5x`
- take profit: `2R`
- break-even trigger: `1R`
- time stop: `18 bars`
- fixed notional: `100 USDT`
- initial capital: `1000 USDT`
- commission: `10 bps`
- governed Python slippage: `5 bps`
- pyramiding: `0`
- signal evaluation: confirmed bars only
- execution: first eligible next-bar open

Frozen RR3 regime filters:

- EMA fast/slow separation minimum: `0.20%`
- ADX slope: `ADX(now) > ADX(1 bar ago)`
- ATR% regime: `0.50% <= ATR/close*100 <= 4.00%`

The champion may not be changed in place. Any parameter, filter, execution-semantic or
strategy-logic change creates a new research identity and requires new governed evidence.

## 3. Development evidence

Development dataset:

- period: `2022-01-03T00:00:00Z -> 2026-01-01T00:00:00Z`
- bars: `8,754`
- canonical SHA-256:
  `1202586308d6aa85add15c51259ba59587badeeda0be64b1efceedb4865c4c6f`

RR3 search:

- deterministic filtered candidates: `240 / 240`
- runtime errors: `0`
- stage-1 eligible: `160`
- top-30 cost-stress pass: `30 / 30`
- corrected-bootstrap finalists: `5`
- corrected-bootstrap pass: `5 / 5`

Candidate #2 development result:

- total return: `+24.8645%`
- max drawdown: `2.5494%`
- completed trades: `167`
- rolling fixed-strategy WFO: `4 / 4 positive`
- worst rolling test window: `+0.4172%`
- aggregate rolling test return: `+9.7851%`
- LONG net PnL: `+168.3024 USDT`
- SHORT net PnL: `+80.3430 USDT`
- return at 40 bps commission: `+14.8178%`
- DD at 40 bps: `3.4605%`
- ordinary 95% bootstrap lower: `+9.0751%`
- Bonferroni-corrected lower: `+4.2375%`

Candidate #2 was frozen before the fresh 2026 OOS was opened.

## 4. Fresh OOS evidence

Protected OOS source:

- period: `2026-01-01T00:00:00Z -> 2026-09-28T08:00:00Z`
- closed bars: `1,622`
- source-subset SHA-256:
  `d3aec9f643ef6f3b6d202cedc3d8b6205bd7916f9dda751cbf298b5e0023f5d1`

Governed Python OOS:

- return: `+0.1741%`
- max drawdown: `4.1199%`
- completed trades: `36`
- wins / losses: `13 / 23`
- LONG: `14 trades / +16.5566 USDT`
- SHORT: `22 trades / -12.5341 USDT`
- terminal position: `LONG` open
- preregistered objective OOS gates: `PASS`

The negative fresh-OOS SHORT contribution remains an explicit limitation and monitoring
concern. It is not removed or hidden by the champion freeze.

## 5. Manual TradingView evidence and parity reconciliation

The exact final Pine artifact in this record was manually compiled/run in TradingView.

Observed TradingView development summary:

- PnL approximately `+25.98%`
- max drawdown approximately `2.10%`
- completed trades: `163`
- profit factor approximately `1.924`

Observed fresh-2026 TradingView summary:

- PnL approximately `+1.67%`
- max drawdown approximately `4.80%`
- completed trades: `33`
- profit factor approximately `1.21`
- LONG contribution positive
- SHORT contribution negative

Trade-level reconciliation of the supplied TradingView CSV found:

- `33 / 33` TradingView closed-trade entries align with Python by direction and entry bar;
- `32 / 33` matched closed trades align on the exit bar/reference open;
- the final open LONG aligns;
- three early Python-only trades are localized to January 2026 and are explained by the
  different recursive-indicator warm-up boundary used by the TradingView Deep Backtest range;
- one March SHORT exit differs because governed Python applies declared `5 bps` slippage to
  simulated execution price and therefore to the ATR risk boundary, while Pine Strategy Tester
  has no exact dynamic basis-point slippage primitive.

Disposition of runtime evidence:

`MANUAL_TRADINGVIEW_RESEARCH_VERIFIED_WITH_KNOWN_PARITY_LIMITATIONS`

This is intentionally not represented as a formal Sprint 18 `MATCH`. The known differences
remain visible and do not create deployment authority.

## 6. Champion / challenger policy

Champion:

- `RR3 Candidate #2`
- state: `FROZEN_RESEARCH_CHAMPION`

Preserved challengers:

- `RR3 Candidate #5`
- `RR3 Candidate #8`
- `RR3 Candidate #11`
- `RR3 Candidate #146`

All four challengers passed the preregistered corrected-bootstrap gate. They remain historical
research alternatives only.

The consumed 2026 OOS must not be reused to rank these challengers against Candidate #2.
No challenger is promoted by post-hoc comparison on already observed evidence.

The remaining RR3 candidates remain immutable historical search evidence and are not silently
re-optimized.

## 7. Forward monitoring boundary

The champion enters manual forward-research observation only after the frozen OOS data boundary:

`after 2026-09-28T08:00:00Z`

Forward monitoring records, without changing parameters:

- completed trade count;
- cumulative and rolling PnL;
- drawdown;
- LONG and SHORT contribution separately;
- profit factor;
- win/loss distribution;
- execution/timestamp deviations;
- regime-filter state;
- observed Pine/Python semantic deviations;
- data or platform changes.

Forward evidence is new research evidence. It does not automatically authorize a lifecycle
promotion.

Any strategy modification during the monitoring period terminates comparability with this
frozen champion and requires a successor research identity.

## 8. Next research lane

A separate future research lane may investigate LONG/SHORT asymmetry, especially the observed
weakness of the SHORT side in fresh 2026 evidence.

That work must be a new governed run (for example a separately preregistered RR4) and may not
mutate this champion in place.

## 9. Authority state

- research champion: `FROZEN`
- manual TradingView research: `READY WITH KNOWN LIMITATIONS`
- paper monitoring authorization: `NOT_AUTHORIZED`
- deployment authorization: `NOT_AUTHORIZED`
- broker connectivity: `NOT_AUTHORIZED`
- live execution: `NOT_AUTHORIZED`
- execution state: `PLANNED_CLOSED`

This freeze is a research handoff, not an Executive Decision Package granting operational
trading authority.

## 10. Final disposition

`RR3_CANDIDATE_2_FROZEN_AS_RESEARCH_CHAMPION`

`RR3_RESEARCH_HANDOFF_COMPLETE_WITH_KNOWN_PARITY_AND_SHORT_SIDE_LIMITATIONS`

`FORWARD_RESEARCH_OBSERVATION_READY`

`DEPLOYMENT_NOT_AUTHORIZED`

`EXECUTION_PLANNED_CLOSED`
