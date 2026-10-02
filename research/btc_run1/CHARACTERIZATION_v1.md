# BTC Run #1 — development market characterization v1

## Disposition

Descriptive stage complete. No strategy backtest, optimization, selection or
performance inference. PR #105's design was reviewed and merged after both
Python 3.12/3.13 CI checks succeeded. Analysis baseline:
`1aefdcb11bcb077a17d4fd7ca6e6afe288630f57`.

The exact development interval is 2025-04-01 00:00 UTC through
2026-04-01 00:00 UTC, end exclusive: 8,760 consecutive 1H bars. First 1,000
bars are indicator warmup; 7,760 bars enter regime/EMA-order statistics.
Monthly price-return and realized-volatility statistics describe the full
interval, including indicator warmup. These are underlying-market observations,
not portfolio returns. Definitions and exact lineage are in
`characterization_v1.json`; thresholds from design v1 remain unchanged.

## Principal observations

| Measure | Development observation |
|---|---:|
| First open to final close price change | -17.3054% |
| Annualized realized hourly volatility | 42.8916% |
| Downside / upside annualized semivolatility | 30.9949% / 29.6452% |
| Hourly up / down close-to-close observations | 4,371 / 4,388 |
| Lag-1 log-return autocorrelation | -0.002290 |
| EMA 20/50/200 ordered UP | 2,522 / 7,760 (32.50%) |
| EMA ordered DOWN | 2,984 / 7,760 (38.45%) |
| EMA mixed order | 2,254 / 7,760 (29.05%) |
| ADX >=20 | 5,425 / 7,760 (69.91%) |
| ATR/close in preregistered [0.15%, 3%] band | 7,760 / 7,760 |
| Joint T1 regime predicate eligible | 3,217 / 7,760 (41.46%) |

The trend labels use EMA ordering only, not the strategy's full LONG/SHORT
signal. T1 eligibility counts only its three regime filters, not entries,
exposure or trades. ADX >=20 does not establish predictive power. Sample
volatility annualization uses sqrt(8,760); it is descriptive, not a forecast.

| Month | Underlying price change | Realized vol, annualized |
|---|---:|---:|
| 2025-04 | +14.0681% | 52.0901% |
| 2025-05 | +11.0647% | 37.3378% |
| 2025-06 | +2.4537% | 32.3214% |
| 2025-07 | +8.0305% | 30.9015% |
| 2025-08 | -6.4808% | 32.1776% |
| 2025-09 | +5.3479% | 27.8613% |
| 2025-10 | -3.8950% | 42.9291% |
| 2025-11 | -17.5509% | 50.0044% |
| 2025-12 | -2.9922% | 44.7826% |
| 2026-01 | -10.1868% | 37.7317% |
| 2026-02 | -14.9511% | 65.1166% |
| 2026-03 | +1.9503% | 48.7462% |

Monthly change is final close / first open - 1. Return at a month boundary is
assigned to the later month for volatility, provided both closes are inside
development. No March 2025 close is used. April has no post-warmup regime
observations; May has 464, and later months use their full membership.

Median consecutive EMA UP/DOWN runs are 29/39.5 hours; maximum 186/280 hours.
The final observed run is right-censored, and these dependent runs are not
independent statistical replications. Neither market direction nor a longer
DOWN run proves profitable shorts. Retain H3 as a prospective costed diagnostic;
no reason exists here to discard SHORT before observing its authorized ledger.
No design threshold or profile was altered after inspecting these descriptions.

## Immutable partition and access audit

Development canonical SHA-256:
`1ea4bcacd92175c5451199de06241515a66aaff91172f047299453c37cd9f1e6`.

- Child raw manifest: `dataset:btc-run1-development-raw-v1`.
- Child raw lock: `dataset-lock:btc-run1-development-raw-lock-v1`.
- Child normalized manifest: `dataset:btc-run1-development-normalized-v1`.
- Child normalized lock: `dataset-lock:btc-run1-development-normalized-lock-v1`.

Production LocalDatasetRepository persisted/reloaded each manifest/lock and
all selected observations/bars in a separate development-only store. Existing
`verify_dataset_lineage` returned VERIFIED. Exact bar and raw-observation
memberships are subsets of parent R3 manifests; fingerprints, identity,
chronology, OHLC values and close/availability bounds were verified before use.
Parent manifests/locks remain immutable; child provenance retains the original
source declaration. The JSON sidecar records the exact parent-to-child subset
link. This is a derived partition inheriting parent admission/eligibility,
not a new standalone eligibility record or experiment authorization.

Partition construction read parent canonical bytes for hash integrity and
selected rows by timestamp before analysis. Parent manifests are metadata.
Only development bar objects were loaded for analysis and indicators;
validation/OOS analysis bar counts are both zero. No full-history indicator
calculation or pre-development indicator seed was used. The private package
contains the development CSV, selected immutable records, reproduction script
and results; raw bars are not committed to GitHub.

## Verification and limitations

Reproduction uses production Decimal EMA/RSI/MACD/ADX/ATR indicators with fixed
T0 parameters. It verifies 8,760 bars, unique contiguous 1H chronology, exact
parent membership and prices, all availability times <=2026-04-01 00:00 UTC,
manifest/lock integrity and repository reloads. Totals of regime/trend/monthly
counts reconcile. This is deterministic descriptive analysis, not an independent
scientific validation or a strategy performance test.

Volume and funding are absent. No inference about market liquidity, capacity
or net perpetual performance follows. The older missing 11 hours do not affect
this development partition. Prior source/admission attempts remain historical.

## Concrete next step and runtime blockers

Prepare a targeted governed warmup implementation before authorizing the six
preregistered experiments. Current `strategy_backtest.py` rejects
`specification.warmup_bars != 0`; `experiment_runner.py` also constrains warmup
in its supported runner contract. `multi_signal_runtime.py` evaluates entries
when indicators become ready and has no 1,000-bar entry suppression. Passing
warmup=0, dropping input bars, monkeypatching indicators or simulating trades
then deleting warmup trades would violate the frozen design.

The same review must preserve terminal-window fail-closed behavior: current
multi-signal runtime raises `MultiSignalMissingNextBar` for an unfillable
terminal transition. Report that as a failed run; never read the next partition
to obtain a fill or silently discard the transition. The design permits open
terminal positions, not cross-window execution or bypass of an engine error.

After faithful warmup support is reviewed and green, bind the locked development
partition to the exact ExperimentSpecification/authorization and run T0/T1 at
the three fixed cost scenarios. Optimization, validation/OOS performance,
Pine generation and execution remain outside this completed descriptive step.
