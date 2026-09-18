# Phase 3 Sprint 10 — Controlled Experiment Authorization & Experiment Foundation v1.0

## Governed baseline

- Starting `main`: `46a96ebdb60bd927d254be3d842dcf2bedd35fac`
- Predecessor PR: #70, merged from reviewed head `00746d9ad77adb83e5230afd0229db7a3c0ac0e5`
- Constitutional baseline: v1.0 / `50b61266f880cb9657b7f1b477d3d90825fe013f`
- Branch: `phase-3/controlled-experiment-foundation`

## Purpose

Sprint 10 introduces a governed, immutable experiment specification and a fail-closed experiment authorization boundary. It does not execute experiments, simulate trades, calculate PnL, perform backtests, optimize parameters, validate results, authorize deployment, or open execution.

Core separation:

`RESEARCH_DATASET_ELIGIBLE != EXPERIMENT_AUTHORIZED != EXPERIMENT_EXECUTED != VALIDATED != DEPLOYMENT_AUTHORIZED != EXECUTION`

## New governed contracts

- `ExperimentSpecification`
- `ExperimentAuthorizationPolicy`
- `ExperimentAuthorizationRecord`
- `ExperimentAuthorizationRequest`
- `ExperimentAuthorizationResult`

Declarative enums cover experiment family, no-lookahead semantics, cost semantics, sizing semantics, authorization status, and lifecycle boundary.

## Dataset eligibility binding

An experiment specification must bind an exact fingerprint-bearing `ResearchDatasetEligibilityRecord`, normalized manifest, and normalized lock. Authorization reuses `verify_research_eligibility_lineage()`; it does not substitute a weaker verifier.

Only an exact `ELIGIBLE` / `CONTROLLED_RESEARCH_DATASET` input can reach authorization.

## Temporal and no-lookahead contract

The specification requires:

- UTC observation start/end
- strict start < end
- knowledge cutoff not earlier than the observation end
- explicit no-lookahead semantics
- explicit warmup bars
- explicit calendar semantics
- exact dataset refs

No order timing or market replay engine exists in this sprint.

## Deterministic experiment identity

The specification binds:

- explicit deterministic seed
- sorted immutable configuration
- observation boundaries
- cost/slippage/funding declarations
- sizing/capital declaration
- expected engine contract ref
- requested output/metric declarations

There is no implicit random seed, mutable current configuration, plugin path, callable, eval/exec, or environment-dependent identity.

## Cost, slippage, funding, and sizing

These are declarations only. `UNKNOWN` remains distinguishable from `DECLARED_ZERO` and fails closed when policy requires explicit semantics.

No fee lookup, broker integration, cost engine, sizing calculation, or order fill implementation is added.

## Authorization policy

The authorization policy can require:

- allowed experiment families
- exact no-lookahead semantics
- accepted calendar semantics
- explicit commission/slippage/funding semantics
- explicit sizing
- bounded observation window
- bounded deterministic seed
- supported exact engine contract ref
- verified actor authority

Actor identity is not equivalent to authenticated authority. If verified authority is required and unavailable, authorization remains incomplete.

## Authorization states

- `AUTHORIZED`
- `REJECTED`
- `QUARANTINED`
- `INCOMPLETE`
- `UNSUPPORTED`

`AUTHORIZED` means only that the immutable declaration may be handed to a future controlled experiment runner.

Authorized records remain:

- lifecycle: `AUTHORIZED_NOT_EXECUTED`
- validation: `NOT_VALIDATED`
- deployment: `NOT_AUTHORIZED`
- execution: `PLANNED_CLOSED`

## Lineage

Governed lineage is:

`RealCsvSourceDeclaration -> RealCsvAdmissionRecord -> ResearchDatasetEligibilityRecord -> exact normalized dataset manifest/lock -> ExperimentSpecification -> ExperimentAuthorizationPolicy -> ExperimentAuthorizationRecord`

The authorization boundary verifies the existing eligibility lineage and exact dataset binding before making a decision.

## Persistence

`LocalDatasetRepository` is extended only for:

- `experiment-specification`
- `experiment-authorization-policy`
- `experiment-authorization-record`

All use canonical JSON v1, immutable fingerprint addressing, verified reload, no overwrite, and no mutable latest/current alias.

## Capability isolation

Sprint 10 introduces no:

- backtest loop
- trade simulator
- order fills
- PnL calculation
- position engine
- signal generation
- indicator calculation
- optimization
- walk-forward
- Monte Carlo
- portfolio construction
- validation engine
- broker/exchange/network client
- paper/live trading
- order routing
- subprocess
- eval/exec
- plugin loader

## Governance preconditions

No implementation-precondition status is promoted merely because the contracts exist.

Expected state counts remain:

- RESOLVED: 0
- PARTIALLY_RESOLVED: 5
- OPEN: 9
- DEFERRED: 0

Open authority remains for authenticated decision authority, validation governance, production release governance, legal/provider truth, and execution.

## Readiness

If focused tests, full regression, static analysis, and CI pass:

- `EXPERIMENT_SPECIFICATION_READY`
- `EXPERIMENT_AUTHORIZATION_GATE_READY`
- `EXPERIMENT_LINEAGE_READY`
- `EXPERIMENT_CONFIGURATION_IDENTITY_READY`
- `NO_LOOKAHEAD_CONTRACT_READY`
- `EXPERIMENT_REPRODUCIBILITY_FOUNDATION_READY`
- `EXPERIMENT_EXECUTION_NOT_READY`
- `BACKTEST_ENGINE_NOT_READY`
- `VALIDATION_NOT_READY`
- `DEPLOYMENT_NOT_READY`
- `LIVE_EXECUTION_NOT_READY`
- `EXECUTION_CLOSED`
- `EXE-01 = PLANNED_CLOSED`

## Sprint disposition

Target disposition:

`PHASE 3 SPRINT 10 COMPLETE WITH OPEN PRECONDITIONS`

## Recommended Sprint 11 discussion

If Sprint 10 passes governance review, the next bounded direction is a controlled deterministic experiment runner/backtest foundation that consumes only an exact authorized experiment, enforces deterministic market-data replay and no-lookahead semantics, emits immutable result artifacts, and grants no validation/deployment/execution authority.
