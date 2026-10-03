# BTC Run #1 — SOL4H_TRANSFER screening v1

Baseline `404d73c6508e1a070f1cff1976a5efa357e94b27`; issue #101. Exact model MULTI_SIGNAL_TREND_LONG_SHORT with existing governed trend engine. Development-only governed admission/eligibility, exact authorizations and accounting verification.

| Cost scenario | State | Net USDT | Return % | DD / initial capital % | Completed trades | LONG trades/net | SHORT trades/net |
|---|---|---:|---:|---:|---:|---|---|
| base | COMPLETED | -38.5409 | -3.8541 | 4.2328 | 123 | 41 / -22.5186 | 82 / -16.0223 |
| stress | COMPLETED | -76.8959 | -7.6896 | 7.9789 | 122 | 40 / -34.8274 | 82 / -42.0685 |
| zero_cost_diagnostic | COMPLETED | -1.7862 | -0.1786 | 1.9546 | 124 | 41 / -10.4622 | 83 / 8.6761 |

Decision: **FAIL**. Gates remain fixed as in pullback_design_v1.json; all machine checks preserved. Any insufficient count is inconclusive, never promoted. No ranking against T0/T1 or additional variant inspected. Three attempts only; cumulative BTC screening count twelve.

Immediate trend entry with exact SOL Candidate2 parameters; no signals before index1000. First1000 equity points flat. Development8760 bars only; validation/OOS untouched. Full private source/store/orders/fills/trades/equity retained; repo contains aggregates only. Funding unmodeled, economic promotion blocked. No optimization, candidate freeze, Pine, execution or independent AI-agent approval.

Next step: Exact SOL transfer must pass fixed BTC gates before validation; if it fails preserve results and preregister any successor hypothesis. Protected windows remain sealed.

Mechanical retry: zero-cost original attempt failed before the first fill because generated order ID exceeded the identifier bound. Shortened only identifiers and reauthorized exact unchanged settings; base/stress not rerun. Original failure and authorization retained privately.
