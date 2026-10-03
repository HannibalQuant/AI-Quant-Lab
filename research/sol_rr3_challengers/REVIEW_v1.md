# SOL 4H RR3 — Historical challenger review v1

Baseline `404d73c6508e1a070f1cff1976a5efa357e94b27`; source issue #96. Read-only historical aggregate audit; no new backtests, optimization, OOS access, candidate promotion or Champion change.

| Candidate | EMA separation % | ATR minimum % | Development return % | DD % | Trades | LONG USDT | SHORT USDT | Return at40bps % | Corrected bootstrap lower % |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 2 | 0.2 | 0.5 | 24.8645 | 2.5494 | 167 | 168.3024 | 80.3430 | 14.8178 | 4.2375 |
| 5 | 0.2 | 0.75 | 24.8645 | 2.5494 | 167 | 168.3024 | 80.3430 | 14.8178 | 4.2375 |
| 8 | 0.2 | 1.0 | 24.8645 | 2.5494 | 167 | 168.3024 | 80.3430 | 14.8178 | 4.2375 |
| 11 | 0.2 | 1.25 | 24.8645 | 2.5494 | 167 | 168.3024 | 80.3430 | 14.8178 | 4.2375 |
| 146 | 0.8 | 0.5 | 24.6927 | 2.5494 | 167 | 163.9470 | 82.9797 | 14.6480 | 3.8087 |

All five have4/4 positive development rolling windows, minimum20 trades/window, ADX slope1 and ATR maximum4%. Development2022-01-03 through2026-01-01; costs10bps commission/5bps slippage base,40bps commission/5bps slippage stress. Counts86LONG/81SHORT each. No independent new validation inferred from old results.

#5/#8/#11 share all recorded performance fields with #2 across the240-results, top30-cost-stress and finalist-bootstrap tables. They are aggregate-equivalent, not proven identical ledgers. Only ATR minimum differs. Do not count them as three independent successful alternatives or rerank on consumed2026 OOS.

#146 raises separation0.2→0.8%; historical SHORT contribution improves by2.6367USDT while LONG falls4.3553USDT; total return decreases0.1719percentage points. This is a descriptive contrast, not evidence of superiority. All historical bootstrap gates passed; deterministic Champion selection remains #2. No alternative promoted.

Source tables were read in current version1 and common fields reconciled by candidate ID across three sources. Exact Library IDs/versions and selected rows are retained in challenger_review_v1.json. Values come from parsed CSV text; original-byte hashes and full governed ledger identities are unavailable here and are not invented. No full trade/equity fingerprints, stress side ledgers or per-trade attribution can be verified from aggregates. Frozen Champion Pine remains untouched.

Next concrete step: recover the frozen development ledgers and exact run/strategy/dataset references. Verify #5/#8/#11 equivalence, then explain only #146/#2 differing development trades. Keep all four challenger identities; no new OOS use or independent validation claim.
