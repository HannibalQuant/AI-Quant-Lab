# BTCUSDT 1H Research Run #1 — preregistered design v1

## Control and authority

Issue #101. Design baseline: `384c3a828a0adba758c8091d472a5bc74a0ac5c4`.
Constitutional baseline: `v1.0 / 50b61266f880cb9657b7f1b477d3d90825fe013f`.
This independent BTC lane follows admitted R3 lineage; R3 denotes the third
onboarding attempt, not the SOL Research Run #3.

State: **DESIGN_PREREGISTERED_PENDING_REVIEW**. No strategy result has been
inspected, no candidate selected, no optimization run. This document records
prospective screening rules, not evidence that BTC has an edge. Merge/review
freezes v1; deviations require an appended version and disclosure before runs.
The specification in `design_v1.json` is a research plan, not an executable
ExperimentSpecification or an ExperimentAuthorizationRecord.

## Question, prior knowledge and hypotheses

Can confirmed BTC 1H trend signals produce economically useful price-based
returns after declared commission/slippage, and does SHORT contribute enough
to justify retaining both directions?

Internal context: Sprint 25/26 provides an exact multi-signal runtime. SOL RR4
(`research/rr4/README.md`) found no basis for promoting its short filters or
removing SHORT; it supplies methodological caution, not BTC evidence. The
SOL champion is neither modified nor used as BTC parameter authority. External
literature review remains pending before any confirmatory claim; this screening
is exploratory and cannot establish accepted knowledge.

| ID | Prospective claim | Null / disconfirmation |
|---|---|---|
| H1 | Fixed trend profile T0 has positive development net PnL with sufficient activity and temporal consistency | Nonpositive PnL, inadequate trades or failure of any absolute screening gate |
| H2 | T1's preregistered regime filters reduce choppy-market damage relative to T0 without destroying useful returns | T1 fails absolute gates, has greater drawdown, loses more than 20% of positive T0 net PnL, or improves drawdown by less than 10% |
| H3 | SHORT contributes positive price-based net PnL under both base and stress costs, with adequate activity | SHORT has fewer than 30 completed development trades or nonpositive net PnL at either cost level |

H3 is a ledger contribution diagnostic within each combined strategy. It is
not a standalone LONG-only comparison: removing SHORT changes exposure and
entry opportunities. A LONG-only or SHORT-only replacement requires a new
identity, explicit runtime support and prospective comparison; do not patch
or monkeypatch the runtime to manufacture an ablation.

## Locked source and partition boundaries

Private source SHA-256:
`43c2b1cbb3734320801c26cada7dc2c97cf1715978156aafffeabfd22419e4dd`.
Canonical SHA-256:
`096269f2afa4f66ce9657590399e20921202ef921b977d670f2d94e94248071b`.
Source: 24,105 rows / 2,764,554 bytes. Canonical: 24,085 rows.
Admission ADMITTED; eligibility ELIGIBLE; operational RESEARCH_READY;
lineage VERIFIED. Exact refs/fingerprints are in the JSON plan.

All boundaries are UTC, start inclusive / end exclusive, selected by bar open.

| Partition | Interval | Permitted use |
|---|---|---|
| Historical robustness | 2024-01-01 11:00 → 2025-04-01 00:00 | Later frozen-profile stress evidence; no tuning from it |
| Development | 2025-04-01 00:00 → 2026-04-01 00:00 | Descriptive characterization and bounded exploratory screening |
| Validation | 2026-04-01 00:00 → 2026-07-01 00:00 | Sealed until profile/design freeze and separate authorization |
| Protected OOS | 2026-07-01 00:00 → 2026-10-01 00:00 | Sealed until final preregistered evaluation; no discovery or tuning |

The first 11 requested hours of 2024 are unavailable. Do not fill them or merge
another source silently. Twenty October rows were explicitly excluded.
Dataset admission inspected OOS quality only, not strategy performance.

Create immutable child manifests/locks for each research interval and verify
parent linkage and row counts before any experiment. Each runner receives only
its authorized partition; full canonical input must not be passed to a discovery
runner and sliced after indicator calculation. Log partition access and hashes.
No cross-boundary trade or future exit price may affect development metrics.

## Bounded profiles and information timing

Use existing `MULTI_SIGNAL_TREND_LONG_SHORT` and production Decimal indicators.
Two fixed profiles only; parameters are conventional a priori design choices,
not an inferred optimum and not a copy of SOL settings. Exact values are in JSON.

T0: EMA 20/50/200; RSI(14) LONG >=55 / SHORT <=45; MACD 12/26/9;
ADX/DMI(14) threshold 20; ATR(14), SL 2 ATR, TP 2R, BE trigger 1R;
time stop 48 bars. T1 differs only by minimum fast/slow EMA separation 0.25%,
ADX increasing over 3 bars, and ATR/close in [0.15%, 3%]. The filter bundle is
one hypothesis; no individual causal attribution follows from its comparison.

Signal evaluation uses only confirmed available OHLC at close; orders fill at
the first eligible next-bar open. Indicators reset at each experiment interval;
exclude its first 1,000 bars from entries and scored returns, with no pre-window
input. Indicator-only warmup must preserve original timestamps and contain no
positions. If the current runner cannot enforce this faithfully, fail closed
and prepare a targeted contract-compatible implementation before backtesting.
The warmup is a conservative convergence policy, not a precise EMA guarantee.

No pyramiding. Start flat; capital 1,000 USDT; fixed entry notional 100 USDT;
no compounding. Preserve production semantics for ATR reference, opposite-signal
exit, BE activation and terminal positions. SL/TP/BE touches are evaluated on
confirmed bars and exit at next open, not simulated intrabar touch prices.
Do not invent within-bar ordering. Terminal positions remain open and marked;
report realized and unrealized PnL separately, do not force a close beyond the
window, and disclose pending transitions without executing them outside it.

Commission/slippage assumptions per fill:
- base: commission 10 bps, adverse slippage 5 bps;
- stress: commission 20 bps, adverse slippage 10 bps;
- zero-cost diagnostic: 0/0 bps, never eligible for promotion.
These are fixed research assumptions, not asserted current exchange tariffs.
Three scenarios x two profiles = six full-development runs, no parameter search.
Record round-trip costs and turnover, including each entry/exit fill.

Volume is absent. No volume, order-flow, liquidity or funding field may be
invented. Historical funding is unavailable and excluded explicitly: findings
are price-based net of commission/slippage, **not all-cost perpetual returns**.
Funding evidence/model and capacity analysis remain blockers to economic
promotion or deployment. No zero-funding observation is asserted.

## Measurements, stopping and scientific limits

Before strategy screening, characterize development only: monthly log returns,
realized volatility, ATR%, ADX/DMI, trend persistence, downside/upside asymmetry
and fixed regime bins. Use these descriptive bins: ADX <20 versus >=20;
ATR% <0.15, [0.15,3], >3. Preserve counts and definitions. Do not move thresholds
based on observed results or use validation/OOS for characterization.

For every profile/scenario preserve the full trade ledger, equity, drawdown,
net/realized/unrealized PnL, turnover/exposure, trade counts, profit factor,
LONG/SHORT contribution, monthly and quarterly returns. Empty and losing runs
remain in the denominator. Define profit factor as gross positive completed
trade net PnL divided by absolute gross negative completed trade net PnL;
zero loss denominator is reported undefined, not used as proof of quality.

Prospective development screening gates (all required at base):
- at least 80 completed trades total and 30 per direction;
- positive total net PnL and profit factor >=1.10 with defined denominator;
- max marked-equity drawdown <=5% of initial capital;
- at least 3 of 4 UTC development quarters positive, worst quarter >=-2%;
- stress total net PnL >0, stress drawdown <=7.5%, and H3's direction gates.
Calendar quarters include warmup hours as flat, zero-return hours. Quarterly
returns use marked equity at boundaries; side diagnostics use completed trades
assigned by exit time, with unrealized positions disclosed separately.
These are screening choices, not statistically proven feasibility thresholds.
Insufficient trades means INCONCLUSIVE, not permission to lower the gate.

H2 additionally requires T0 positive base PnL, T1 base PnL >=80% of T0,
and T1 drawdown <=90% of T0. No division by zero: zero T0 drawdown makes H2
INCONCLUSIVE. H1/H2/H3 are exploratory comparisons; no claim of independent
statistical significance, causality or market-wide generalization is allowed.

Run the six fixed experiments once after exact authorization. Stop on integrity,
accounting or chronology failure; reruns only repair documented mechanical
errors with the same settings. A negative outcome is a completed research result.
No extra profile, threshold, cost scenario or favorable subperiod may be added
without a new prospective design version disclosing all earlier attempts.
A development survivor is merely eligible for later scrutiny, not a champion.

## Later gates, still closed

If exploratory screening is useful, preregister any bounded optimization space
and walk-forward design separately before running it. Walk-forward must fit on
past training data only, freeze each fold before its forward period, keep the
protected OOS inaccessible, disclose overlapping/dependent windows and preserve
all trials. No optimization budget is granted by this document.

Validation and historical robustness require frozen settings and exact governed
experiment authorization. Protected OOS is evaluated only after the final
selection protocol is frozen; failed OOS cannot be reused to tune a replacement.
Independent scientific review, replication, funding/cost realism and governed
PASS decisions are required for any later promotion. Existing institutional
specialist roles apply; this file does not assert that an independent reviewer
has already approved it.

## Exact next action

After review/merge of this design: construct locked development-only child
lineage and run the descriptive market/regime characterization listed above.
Produce a report with no strategy performance and no validation/OOS access.
Then prepare exact ExperimentSpecification/authorization for the six fixed
screening runs, checking warmup and terminal-boundary support first.

No Pine, broker, live/paper execution or deployment is authorized here.
