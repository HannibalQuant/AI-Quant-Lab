# Phase 3 Sprint 11 — Controlled Deterministic Experiment Runner / Backtest Foundation v1.0

## 1. Governed baseline

- Starting `main`: `685294f1c96d47f34fb42b823f01d5e63f71dfb6`
- Predecessor PR: #71, merged from reviewed head `ce131f1e0a0f8611cafa6c670ef320dfad30c3e2`
- Constitutional baseline: v1.0 / `50b61266f880cb9657b7f1b477d3d90825fe013f`
- Branch: `phase-3/controlled-deterministic-experiment-runner`

The merge commit is exactly one commit ahead of the reviewed predecessor head, with that head as
the merge base. No Phase 1/2 artifact, Constitution, Sprint 1–10 report, or prior golden fixture is
changed.

## 2. Purpose

Sprint 11 introduces the first bounded research-experiment execution boundary. It consumes only an
exact, immutable `AUTHORIZED` Sprint 10 record and executes one closed deterministic
`MARKET_STATISTICS` engine against its exact normalized bars.

`RESEARCH_EXPERIMENT_EXECUTED` means only that the authorized descriptive calculation completed.
It creates no scientific-validation, deployment, market-execution, or source-trust authority.

## 3. Non-goals

This sprint adds no strategy, signal, indicator, position, order, fill, PnL, cost engine, optimizer,
parameter sweep, walk-forward, Monte Carlo, scientific validation, model ranking, deployment,
broker/exchange adapter, network client, subprocess, dynamic import, plugin, `eval`, or `exec`.

`STRATEGY_BACKTEST` and every experiment family except `MARKET_STATISTICS` remain unsupported.

## 4. Supported experiment family

The only supported family is `MARKET_STATISTICS`. Its fixed outputs are exact close extrema,
observation count, a simple-return series, simple-return mean, and simple-return population
variance. Requested metrics/outputs must exactly match this closed engine contract.

The family requires commission, slippage, funding, and position sizing to be explicitly
`NOT_APPLICABLE`, capital to be zero, and warmup to be zero. `UNKNOWN` and silent zero assumptions
are not executable.

## 5. Authorization precondition

The runner requires:

- `status == AUTHORIZED`
- `lifecycle == AUTHORIZED_NOT_EXECUTED`
- `validation == NOT_VALIDATED`
- `deployment == NOT_AUTHORIZED`
- `execution == PLANNED_CLOSED`
- an exact request reference to the authorization bytes

Every other authorization decision fails before replay. The authorization artifact remains
immutable; completion is represented by a new run artifact rather than a mutation.

## 6. Engine contract

`ExperimentReplayContract` is an immutable canonical object. It binds:

- exact engine ID/version/fingerprint
- `MARKET_STATISTICS`
- `EXPLICIT_EVENT_AVAILABILITY_NEXT_EVENT`
- canonical replay ordering
- Decimal precision/rounding semantics
- the closed metric/output allow-lists

The specification, policy, request, run, and result must all bind the same exact engine reference.
The same engine ID with a different fingerprint is rejected. Engine selection is a direct closed
comparison with `market_statistics_replay_contract()`; there is no module path or runtime dispatch.

## 7. Deterministic replay

Replay consumes only `CsvImportReport.normalized_bars` already verified by the complete Sprint 8/9
lineage. Input order must equal the canonical key:

`(bar_open, bar_close, source ID, source-observation ID, bar ID, bar version)`

Duplicate business keys, non-canonical order, repeated availability boundaries, incomplete bars,
gaps inside the authorized interval, or bars unavailable by the knowledge cutoff fail closed. The
runner performs no sort-and-continue fallback, resampling, interpolation, forward fill, synthetic
bar creation, filesystem scan, latest lookup, or network fetch.

## 8. Temporal semantics

All specification, bar, request, result, and completion times are UTC. `bar_open`, `bar_close`,
`availability_time`, `knowledge_cutoff`, and `completed_at` remain distinct.

`available_bars_at()` exposes only bars whose governed availability is at or before the explicit
knowledge boundary. The closed engine advances through strictly increasing availability events and
requires the visible set to be exactly the processed prefix. A future bar therefore cannot enter a
calculation early, and a final result cannot exist before both the cutoff and all consumed bar
availability times.

## 9. No-lookahead enforcement

For `EXPLICIT_EVENT_AVAILABILITY_NEXT_EVENT`, a close enters the engine only at that bar's exact
availability event. Simple return *t* is calculated only after both closes are present in the
available prefix. The engine offers no decision, order, or fill callback, so same-event or early
market execution is structurally absent.

Next-event fill behavior for trading experiments is deliberately not claimed: trading experiment
families are unsupported. If later work introduces decisions/fills, it must add an exact executable
next-eligible-event contract rather than reuse this descriptive engine as implied authority.

## 10. Observation window

The runner rechecks that start is before end, both boundaries exactly match governed bars, the
selected bars are contiguous, and only bars fully inside `[observation_start, observation_end]` are
consumed. It cannot widen the authorized interval or include newer data.

## 11. Numeric semantics

Prices use existing exact `DecimalValue` text. Calculations use a local decimal context with
precision 34 and `ROUND_HALF_EVEN`.

`simple_return_t = close_t / close_(t-1) - 1`

Mean is the arithmetic mean of those simple returns. Dispersion is population variance (division
by `N`), not annualized volatility. All persisted numeric outputs are canonical finite decimal
strings; exponent notation, NaN, infinity, negative zero, and fractional trailing zeros are
rejected. There is no performance interpretation or score.

## 12. Result contracts

New immutable contracts are:

- `ExperimentRunRequest` — exact input references and injected completion/provenance context
- `ExperimentReplayContract` — closed engine identity and semantics
- `ExperimentResultArtifact` — deterministic descriptive output
- `ExperimentRunRecord` — immutable completed research-run evidence
- `ExperimentRunResult` — in-memory record/artifact/write outcomes

Run status is `COMPLETED`; validation remains `NOT_VALIDATED`, deployment remains
`NOT_AUTHORIZED`, and live execution remains `PLANNED_CLOSED`.

## 13. Result lineage

The verified chain is:

`RealCsvSourceDeclaration -> RealCsvAdmissionRecord -> raw manifest/lock -> normalized bars + manifest/lock -> ResearchDatasetEligibilityRecord -> ExperimentSpecification -> ExperimentAuthorizationPolicy -> ExperimentAuthorizationRecord -> ExperimentReplayContract -> ExperimentRunRecord -> ExperimentResultArtifact`

The runner reuses `verify_research_eligibility_lineage()` through
`verify_experiment_authorization_lineage()`, which reconstructs the Sprint 10 policy outcome and
exact authorization record. It then verifies all exact references, configuration fingerprint,
normalized manifest/lock, policy and engine, and the request's authorization fingerprint.
`verify_experiment_result_lineage()` independently recomputes the descriptive result from the exact
bars, binds run and result to the same immutable input fingerprint, and requires the run to
reference the exact recomputed result bytes.

## 14. Persistence

`LocalDatasetRepository` is extended only for:

- `experiment-replay-contract`
- `experiment-result-artifact`
- `experiment-run-record`

All use canonical JSON v1, exact type/version/fingerprint addressing, verified reconstruction,
immutable writes, and corruption detection. No database, mutable catalog, cache authority,
`latest`, `current`, overwrite, or last-write-wins path is introduced.

## 15. Deterministic rerun semantics

Sprint 11 chooses model A: the same explicit run ID, result ID, exact governed inputs, injected
completion time, and provenance produce the same run-input fingerprint, result bytes, run bytes,
and repository keys. An identical rerun is an idempotent repository write. A changed seed,
configuration, exact reference, time, ID, or provenance is a different run identity/evidence set.
No UUID or current clock is generated internally.

## 16. Authority separation

The runner preserves:

`DATASET_ELIGIBLE != EXPERIMENT_AUTHORIZED != RESEARCH_EXPERIMENT_EXECUTED != NOT_VALIDATED != DEPLOYMENT_NOT_AUTHORIZED != LIVE_EXECUTION`

Positive statistics do not create evidence of edge, robustness, scientific validity, deployability,
or permission to trade.

## 17. Experiment execution versus live execution

The word *execution* in `RESEARCH_EXPERIMENT_EXECUTED` refers only to deterministic local research
calculation. `ExecutionState` still has only `PLANNED_CLOSED`; `EXE-01` is unchanged and rejects all
market-execution capabilities.

## 18. Test evidence

Focused tests cover authorized completion, deterministic bytes and idempotent writes, seed/config
identity changes, exact subwindows, four non-authorized states, tampered authorization/spec/policy/
eligibility refs, wrong engine fingerprint, unsupported family/metrics, order/duplicate/gap/cutoff
failures, future-bar invisibility, unaligned/outside windows, full lineage reverification,
completion-before-cutoff, result-lineage mutation, strict codecs, wrong stored type/version, and
corrupted run/result bytes.

No prior golden is changed and Sprint 11 adds no new golden file; deterministic canonical bytes and
fingerprints are pinned directly by repeatability and strict round-trip tests.

## 19. Governance preconditions before -> after

| Preconditions | Before | After | Sprint 11 evidence / remaining authority |
|---|---|---|---|
| IP-01 authentication | OPEN | OPEN | No authentication runtime. |
| IP-02 integrity/authenticity | PARTIALLY_RESOLVED | PARTIALLY_RESOLVED | Run/result tamper detection advances integrity; signatures and authenticity remain open. |
| IP-03 authority binding | OPEN | OPEN | Exact authorization is required; authenticated/revocable authority remains open. |
| IP-04 canonical equivalence | PARTIALLY_RESOLVED | PARTIALLY_RESOLVED | Three strict canonical runner types added; broader representation authority remains open. |
| IP-05 temporal rules | PARTIALLY_RESOLVED | PARTIALLY_RESOLVED | Executable availability-prefix replay advances ordering/no-lookahead; external clocks, corrections, sessions, and trading fills remain open. |
| IP-06 emergency authority | OPEN | OPEN | Outside scope. |
| IP-07 approval/expiry | OPEN | OPEN | No new approval authority. |
| IP-08 evidence freshness | OPEN | OPEN | Results remain not validated; freshness authority is absent. |
| IP-09 validation methods | OPEN | OPEN | No scientific validation method. |
| IP-10 monitoring/multiplicity | OPEN | OPEN | No monitoring or multiplicity policy. |
| IP-11 data quality | PARTIALLY_RESOLVED | PARTIALLY_RESOLVED | Existing exact eligible dataset is reverified; universal provider quality remains open. |
| IP-12 retention/legal | OPEN | OPEN | Existing local restrictions are preserved; no legal authority or lifecycle workflow. |
| IP-13 trust boundary | OPEN | OPEN | Closed local engine has no network/plugin boundary; provider/operator authenticity remains open. |
| IP-14 change/release | PARTIALLY_RESOLVED | PARTIALLY_RESOLVED | Determinism, regression, codec, isolation, and CI evidence advance implementation control; release authority remains open. |

Counts remain: `RESOLVED 0 -> 0`, `PARTIALLY_RESOLVED 5 -> 5`, `OPEN 9 -> 9`,
`DEFERRED 0 -> 0`.

## 20. Readiness matrix

- `CONTROLLED_EXPERIMENT_RUNNER_READY`
- `DETERMINISTIC_MARKET_REPLAY_READY`
- `NO_LOOKAHEAD_ENFORCEMENT_READY` — bounded to descriptive availability-event replay
- `EXPERIMENT_RESULT_ARTIFACT_READY`
- `EXPERIMENT_RESULT_LINEAGE_READY`
- `EXPERIMENT_REPRODUCIBILITY_READY`
- `STRATEGY_BACKTEST_ENGINE_NOT_READY`
- `OPTIMIZATION_NOT_READY`
- `WALK_FORWARD_NOT_READY`
- `MONTE_CARLO_NOT_READY`
- `SCIENTIFIC_VALIDATION_NOT_READY`
- `DEPLOYMENT_NOT_READY`
- `LIVE_EXECUTION_NOT_READY`
- `EXECUTION_CLOSED`

## 21. Blockers

No blocker remains for the bounded `MARKET_STATISTICS` runner. Open preconditions block stronger
claims involving authenticated authority, scientific validation, provider/legal truth, release,
deployment, and live execution.

## 22. Remaining limitations

- one descriptive family and one closed engine only
- repository-owned bounded data evidence only; no provider authenticity claim
- fixed continuous UTC calendar inherited from dataset eligibility
- no revisions/corrections after the exact locked dataset
- no environment/OS image fingerprint beyond the declarative engine contract
- canonical result objects remain subject to the repository's 1 MB object limit
- no strategy, trade, cost, fill, portfolio, validation, or deployment semantics
- local immutable repository durability/concurrency limits remain those documented in Sprint 7

## 23. Sprint disposition

`PHASE 3 SPRINT 11 COMPLETE WITH OPEN PRECONDITIONS`

## 24. Recommended Sprint 12 discussion only

The next direction may be **Controlled Strategy Backtest Engine v1.0** only after review confirms
the replay, no-lookahead, result-lineage, and reproducibility boundaries here. That future sprint
must first govern signal timing, next-event decisions/fills, orders, positions, explicit cost/
slippage/funding consumption, and trade-result lineage. It must not jump to optimization or
scientific validation. No Sprint 12 capability is implemented here.
