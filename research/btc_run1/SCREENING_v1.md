# BTC Run #1 — Development screening v1

Issue #101. Baseline `720fc1db39905d22609c77ac46f25716b78f29db`.

Six exact production authorizations AUTHORIZED; local operator scope, actor authority not independently verified.

Development: 2025-04-01 inclusive → 2026-04-01 exclusive; 8760 hourly bars, 1000 indicator-only warmup bars. Initial capital 1000 USDT; fixed position notional 100 USDT. Parameters and costs match design_v1 exactly.

| Profile | Costs | Net USDT | Return % | Max DD % | Trades | LONG net | SHORT net | PF |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| T0 | base | -62.2767 | -6.2277 | 6.6934 | 214 | -32.2039 | -30.0728 | 0.6743 |
| T0 | stress | -131.4323 | -13.1432 | 13.5130 | 216 | -64.5897 | -66.8426 | 0.4502 |
| T0 | zero_cost_diagnostic | -7.2828 | -0.7283 | 2.4301 | 211 | -11.7094 | 4.4266 | 0.9538 |
| T1 | base | -46.3337 | -4.6334 | 5.7655 | 195 | -27.7519 | -18.5819 | 0.7243 |
| T1 | stress | -102.1392 | -10.2139 | 10.3751 | 193 | -53.0055 | -49.1338 | 0.4972 |
| T1 | zero_cost_diagnostic | 4.2317 | 0.4232 | 2.2330 | 195 | -8.3345 | 12.5662 | 1.0303 |

Both T0 and T1 FAIL the preregistered development gate. Trade counts are sufficient; this is a negative result, not a low-sample inconclusive result. H2 is not established because positive T0 is required. H3 fails under both realistic cost scenarios. T1 zero-cost profit does not qualify it for promotion. LONG is also negative for both profiles at base/stress costs, so these results do not justify switching to LONG-only.

All six runs completed, terminal positions flat, 8760 equity points each. Production lineage/accounting verification passed; all first 1000 equity points are flat with no position. No parameter selection, validation performance, OOS access, Pine or execution. Funding is unavailable and unmodeled, not observed zero; economic promotion remains blocked.

Monthly/quarterly equity, exact source/dataset hashes, admission/eligibility refs, authorization/run/result fingerprints and machine-verifiable gate checks are in `screening_v1.json`. Raw data and full ledgers remain private. Full source hash `43c2b1cbb3734320801c26cada7dc2c97cf1715978156aafffeabfd22419e4dd`; development canonical hash `1ea4bcacd92175c5451199de06241515a66aaff91172f047299453c37cd9f1e6`. Independent development admission is linked to parent source/manifest/lock; no claim of standalone provider authentication.

Baseline CI passed for Python 3.12 and 3.13. This evidence-only change modifies no production code. No independent AI-agent review was performed.

Next step: Review development-only loss attribution by side, exit reason and preregistered regime labels; no new runs or parameter changes before a new research mandate.
