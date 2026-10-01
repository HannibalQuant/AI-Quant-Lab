# RR4 SHORT trend-strength development replay

Research date: 2026-09-30. Issue: #100; diagnostic predecessor: #99.
Parent main: `1f73447b7a62a0a56ec39c2d3c183826bd0b7293`.

## Disposition

**No challenger promotion. Retain frozen RR3 Candidate #2.** The proposed
18-bar SHORT momentum filters reduce development-period SHORT profit, total
return, and full-period drawdown performance. C1 and C2 nevertheless pass the
draft's absolute development gates. C2 ranks first among those two challengers
by worst rolling-window return; this is not proof of improvement over C0.
C3 fails the minimum 120 completed-trade gate (114 trades).

This is an **exploratory prototype replay**, not a completed governed RR4
authorization/validation chain. The new SHORT predicate is not encoded by the
current StrategyDefinition contract. The runner therefore issues no governed
result artifact, authorization record, exact-parity verdict, or promotion.
The numeric comparison is reproducible using the pinned production Decimal
runtime and its accounting verifier. Formal integration would require a new
strategy/experiment identity before any promotion or Pine handoff.

## Data and reproduction

Source: operator-supplied `BITGET_SOLUSDT.P, 240 (10).csv`.
SHA-256: `56d7f99aa210a9ab52aa283561b7ca2d13c4b97a91b49e5d1b8e1d15d9c3dd5b`.
The existing TradingView adapter produced exactly 8,754 bars in
`[2022-01-03T00:00:00Z, 2026-01-01T00:00:00Z)` and canonical SHA-256
`1202586308d6aa85add15c51259ba59587badeeda0be64b1efceedb4865c4c6f`.
The runner checks both hashes, count, consecutive 4H timestamps, and OHLC geometry.
Raw market data remains local and is not committed here.

The C0 replay reproduces RR3: 167 trades; return 24.864541%; DD 2.549412%;
LONG +168.302367 USDT; SHORT +80.343044 USDT; four positive rolling windows;
compounded rolling return 9.785124%; return at 40 bps 14.817769%.
Its complete result/ledger is also compared with the unmodified simulation
function, not only with rounded historical summary numbers.

## Fixed experiment

C0 is the unchanged parent. C1/C2/C3 require the confirmed signal close to be
at least 4%/8%/12% below the close 18 bars earlier, respectively. The predicate
acts only while flat, before a SHORT entry is scheduled. It does not alter
opposite-signal exits, risk handling, or LONG signals. All 86 base-cost LONG
entry times, exit times and net PnLs matched C0 exactly in each candidate.

Initial capital 1000 USDT; fixed notional 100 USDT; commission 10 bps per fill;
adverse entry/exit slippage 5 bps; no pyramiding; no forced terminal close.
SL/TP/BE touches are evaluated by the parent confirmed-bar engine and filled at
the first eligible next-bar open, rather than at intrabar stop prices.
Indicators start from the first development bar, exactly as in C0.

| Variant | Return | Max DD | Trades | SHORT trades | SHORT net USDT | Positive windows | Worst window |
|---|---:|---:|---:|---:|---:|---:|---:|
| C0 unchanged | 24.8645% | 2.5494% | 167 | 81 | 80.3430 | 4/4 | 0.4172% |
| C1 4% | 22.9558% | 2.5823% | 160 | 74 | 61.2559 | 3/4 | -0.2966% |
| C2 8% | 18.5573% | 2.9723% | 140 | 54 | 17.2703 | 4/4 | 0.1726% |
| C3 12% | 18.1570% | 3.4233% | 114 | 28 | 13.2679 | 3/4 | -0.6083% |

At 40 bps commission, total returns are respectively 14.8178%, 13.3229%,
10.1100%, 11.2670%. C2 and C3 SHORT contributions become negative
(-15.0456 and -3.4756 USDT); C0 SHORT remains +32.0324 USDT.
The draft required total stress return > 0, not positive stress SHORT PnL:
this observation is a concern, not a retroactively added failure gate.

Four chronological test slices reproduce the existing robustness implementation:
train prefix 3285 bars, test 1095, step 1095, measured from the continuous
equity path, carrying any open position across boundaries. This is fixed-strategy
rolling evaluation, not nested refitting. The last 1089 bars remain in the full
development result but are outside the four complete test slices.
Returns compound across the four windows. C0/C1/C2/C3 compounded rolling
returns are 9.7851%/10.8396%/11.4957%/10.9557%, respectively. Thus the
challengers improve this particular aggregate, despite weaker full-period results;
that favorable evidence is retained. Per-window counts, side PnLs and DD are
in `results/results.json`, for every commission level 10/20/30/40 bps.

## Which trades were lost or added?

Matching uses side and entry time at base costs. A filtered entry can be delayed
and create a new position later, so deleting rows from C0 would be an invalid
backtest. All variants were simulated again through the full position state machine.

| Variant | Removed C0 SHORT entries | Removed winning entries | Their positive PnL | Removed negative PnL | New SHORT entries | New SHORT net |
|---|---:|---:|---:|---:|---:|---:|
| C1 | 27 | 13 | 63.3826 | -51.7027 | 20 | -7.4073 |
| C2 | 62 | 35 | 195.7949 | -108.1808 | 35 | 24.5414 |
| C3 | 76 | 41 | 233.2814 | -142.6747 | 23 | 23.5315 |

These are observed trade-set differences, not a causal claim about how an omitted
trade would have performed in another position path. The strongest gate loses
substantial profitable SHORT exposure; the proposed family has not established
a development advantage over the parent.

## Verification and limits

All 16 full-period replays passed the existing independent accounting verifier.
The five gate tests check exact threshold boundaries, insufficient lookback,
disabled control, and absence of reads beyond the completed signal bar.
The runtime file hash is pinned; source is copied into an isolated namespace
and a single, asserted entry-branch anchor receives the guard. Production source
and frozen champion Pine are unchanged. Returned results use diagnostic namespaces
and intentionally have no fabricated authorization/specification/eligibility refs.

No parameter search beyond the three draft thresholds was performed. The inspected
2026 OOS informed this hypothesis and was not used for this replay or labeled fresh
validation. Development 2022–2025 was used by previous research too. No statistical
significance or independence claim is made. No new OOS candidate is frozen by this
prototype. Any further hypothesis needs a separate record, not post-hoc tuning
of these thresholds until results look better.

## Commands

From the repository root (Python >=3.12):

```bash
PYTHONPATH=src python research/rr4/run.py /absolute/path/to/original.csv
PYTHONPATH=src pytest research/rr4/test_run.py
```

`results/trades.csv` contains every completed trade for all 16 runs. The runner
also generates a local `results/equity.csv`; it is reproducible and excluded
from version control to avoid a large redundant artifact.
