# BTC Run #1 — explicit multi-signal warmup support

## Behavior

The existing ExperimentSpecification.warmup_bars field now controls a counted
entry-suppression prefix for MULTI_SIGNAL_TREND_LONG_SHORT. The specification,
authorization and run fingerprints already bind this field; changing it requires
new exact authorization. No new strategy profile, schema or execution authority
is introduced. Repository source baseline remains part of reproduction evidence.

For warmup N, replay indexes 0..N-1 update indicators and retain flat capital in
the equity curve, without signals, pending orders, fills, fees or positions.
Index N is the first eligible signal index, subject to indicator readiness and
all existing filters. Its order executes at the first later bar open at or after
the signal's availability time. If availability is later than the immediately
following open, that open is skipped as before. BTC's admitted availability at
bar close normally permits the following open.

Indicators are calculated from the entire authorized partition, including its
warmup prefix. Bars and timestamps are not sliced/reindexed, and no prior-window
or future-partition data are introduced. Equity output covers every replay bar;
flat warmup contributes zero return. No warmup trade is simulated then removed.

A nonzero warmup must leave at least one signal bar and one later fill bar;
otherwise the run fails closed. Existing terminal MissingNextBar behavior is
preserved: an unfillable terminal transition fails the run, never borrows an
execution bar from validation/OOS. Open terminal positions without a pending
transition retain the existing marked-equity semantics.

The independent accounting verifier rejects any ledger order whose source bar
lies within warmup, in addition to reconstructing exact cash/position/equity.
Zero-warmup results retain the previous behavior and pinned fingerprints. The
legacy CLOSE_VS_OPEN_LONG_ONLY profile and MARKET_STATISTICS retain their
existing zero-warmup restrictions. The MARKET_STATISTICS guard in
experiment_runner.py does not govern this strategy runner; it is not relaxed.

## Downstream boundary

Current Pine generation/intake does not represent explicit counted warmup.
Both fail closed for nonzero warmup, preventing an otherwise identical script
from being treated as faithful evidence. This change generates no Pine source
and does not grant Pine, TradingView, broker, paper/live or deployment authority.
A future handoff needs separately reviewed warmup representation/parity.

## Verification and next stage

Synthetic governed admission/eligibility/authorization/replay/accounting tests
cover exact 1,000-bar warmup, preserved indicator history, first signal/fill timing,
flat warmup equity, insufficient replay capacity, stale authorization rejection,
independent early-order rejection, unchanged terminal fail-closed behavior and
legacy/Pine boundaries. Existing zero-warmup golden evidence remains unchanged.
These are runtime mechanics tests, not BTC strategy profitability evidence.

After green CI and review/merge: prepare exact development-only experiment
specifications/authorization and execute the six preregistered fixed T0/T1 cost
scenarios. No optimization or validation/OOS performance evaluation is included
in this implementation step. Funding remains unavailable and economic promotion
remains blocked as recorded in design v1.
