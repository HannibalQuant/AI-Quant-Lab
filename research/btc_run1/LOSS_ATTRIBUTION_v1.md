# BTC Run #1 — Loss attribution v1

Baseline `28f6d368ab386e25393f6ecec313cf694ce9d8d9`; PR #108 reviewed and merged after both CI jobs passed. Issue #101.

Read-only analysis of all six immutable production artifacts; no new backtest, optimization, parameter change, validation or OOS performance. Independent diagnostic reconstruction reconciles every completed trade exit and rejects any earlier eligible exit condition.

| Base scenario | Trades | Losing trades | Initial-stop condition net | Break-even condition net | Take-profit condition net | Commission |
|---|---:|---:|---:|---:|---:|---:|
| T0 | 214 | 142 | -170.3886 | -10.7355 | 121.2940 | 42.7922 |
| T1 | 195 | 125 | -157.2990 | -4.4477 | 114.7036 | 38.9850 |

Initial-stop-condition exits are the largest negative PnL group in both profiles. Break-even-condition exits are negative in aggregate after costs. At base costs T0 execution gross PnL is -19.4844 USDT and commissions 42.7922 USDT; T1 gross is -7.3487 and commissions 38.9850. Slippage already affects execution-price gross PnL and must not be deducted again. Positive-gross trades turned negative after commission: T0 14, T1 15.

Every base trade signal has ADX>=20 and ATR within the preregistered 0.15–3% band; these coarse regime splits cannot explain the losses. T0 signals failing the T1 filter bundle: 50 trades, -42.6800 USDT; passing: 164 trades, -19.5966 USDT. This is descriptive, not a replacement strategy: T1 has its own path-dependent trade set, 195 trades, -46.3337 USDT. Both directions remain negative after realistic costs. No winning subgroup selected.

**Execution interpretation:** SL, TP and break-even are confirmed-bar predicates causing a next-eligible-open exit. They are not intrabar fills at the threshold. A TAKE_PROFIT-condition trade may lose because the later opening price differs; a BREAK_EVEN-condition exit need not be zero PnL. This is the existing frozen engine semantics, not a newly found implementation error. No intrabar order or condition priority is invented when multiple predicates coincide.

All trade sums reconcile to frozen net results within 1e-25 USDT; each trade has an explained exit, no earlier exit predicate, entry information no later than signal availability, and no warmup entry. Source window has exactly 8760 development bars. Aggregate evidence: `loss_attribution_v1.json`. Private details preserve exact trade refs, signal timestamps and predicate sets.

No production code changed. Checks reuse the green 733-test/14-isolation baseline; this report has additional explicit diagnostic assertions. No independent AI-agent review asserted.

Next concrete step: preregister one new bounded BTC entry hypothesis (for example trend pullback rather than immediate trend confirmation), with its own fixed run budget and gates, before any new runs. Do not optimize the failed T0/T1 profiles or open validation/OOS based on these descriptive groups.
