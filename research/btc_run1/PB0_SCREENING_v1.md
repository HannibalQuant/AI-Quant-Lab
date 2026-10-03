# BTC Run #1 — PB0 screening v1

Baseline `404d73c6508e1a070f1cff1976a5efa357e94b27`; issue #101. Exact model MULTI_SIGNAL_PULLBACK_LONG_SHORT with separate PB0 engine. Development-only governed admission/eligibility, exact authorizations and accounting verification.

| Cost scenario | State | Net USDT | Return % | DD / initial capital % | Completed trades | LONG trades/net | SHORT trades/net |
|---|---|---:|---:|---:|---:|---|---|
| base | COMPLETED | 0.0860 | 0.0086 | 0.2699 | 8 | 2 / -0.8006 | 6 / 0.8867 |
| stress | COMPLETED | -2.0615 | -0.2061 | 0.3001 | 8 | 2 / -1.1508 | 6 / -0.9106 |
| zero_cost_diagnostic | COMPLETED | 0.7320 | 0.0732 | 0.2839 | 8 | 2 / -1.1869 | 6 / 1.9189 |

Decision: **INCONCLUSIVE_INSUFFICIENT_ACTIVITY**. Gates remain fixed as in pullback_design_v1.json; all machine checks preserved. Any insufficient count is inconclusive, never promoted. No ranking against T0/T1 or additional variant inspected. Three attempts only; cumulative BTC screening count nine.

Both bars used by an entry setup are post-warmup; no signals before index1001. First1000 equity points flat. Development8760 bars only; validation/OOS untouched. Full private source/store/orders/fills/trades/equity retained; repo contains aggregates only. Funding unmodeled, economic promotion blocked. No optimization, candidate freeze, Pine, execution or independent AI-agent approval.

Next step: Review PB0 outcome against fixed gates; insufficient activity requires a newly preregistered research decision, not retrospective threshold relaxation. Protected windows remain sealed.
