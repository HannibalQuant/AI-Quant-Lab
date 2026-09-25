# Phase 3 Sprint 22 — TradingView Research Export v1.0

## 1. Baseline

- Governed `main`: `d0dfc93f2782d6c739ecc90af03177d3aad267aa`
- Predecessor: PR #82 / Phase 3 Sprint 21
- Constitutional baseline: v1.0 / `50b61266f880cb9657b7f1b477d3d90825fe013f`
- Branch: `phase-3/tradingview-research-export`

## 2. Mission

Sprint 22 packages the exact governed Pine source and its research evidence into a durable,
deterministic manual TradingView research export.

The export contains the Pine source, strategy parameters, exact research-evidence references,
Sprint 21 static-safety status and deterministic manual instructions.

## 3. Current product target

The active user-facing path is now:

`AI Quant Lab research → selected StrategyDefinition → governed Pine v6 generation →
static Pine safety → immutable TradingView research export → manual TradingView use`.

Broker connectivity and automated execution remain outside scope.

## 4. Non-goals

Sprint 22 does not add:

- TradingView login, browser automation, scraping or API calls;
- automatic Pine compilation;
- automatic chart insertion;
- broker or exchange connectivity;
- webhook execution;
- paper/live order routing;
- deployment authorization;
- runtime no-repaint certification;
- automatic TradingView parity proof.

`EXE-01` remains `PLANNED_CLOSED`.

## 5. Export preconditions

Export requires exact verification of:

- Sprint 20 governed Pine generation;
- Sprint 21 Pine static-safety assessment;
- exact Pine artifact identity and source hashes;
- exact StrategyDefinition identity;
- exact safety assessment identity and input fingerprint;
- exact provenance;
- exact export authority.

Static safety must be `PASS` with
`NO_STATIC_REPAINT_HAZARD_DETECTED`.

## 6. Export authority

Sprint 22 introduces a separate exact fingerprint-bearing export authority.

Export authority does not inherit or replace generator, Pine-intake, safety, optimization,
deployment or execution authority.

## 7. Durable export package

`TradingViewResearchExportPackage` is a new immutable repository-backed governed record.

It binds:

- Pine artifact;
- StrategyDefinition;
- backtest result;
- scientific validation result;
- robustness result;
- optional optimization selection;
- instrument;
- timeframe;
- normalized dataset manifest and lock;
- generator fingerprint;
- static-safety assessment identity and fingerprint;
- Pine source hash, byte size and exact source text;
- manual TradingView filenames;
- exact strategy parameters;
- manual research instructions;
- runtime/repaint limitations;
- export authority and provenance.

## 8. Pine source custody

The package contains the exact Sprint 17/Sprint 20 Pine source text and hash.

No new Pine content is generated during export. Any changed generator artifact or source fails
lineage verification before export.

## 9. Strategy parameters

The manual package exposes the bounded governed strategy parameters in deterministic sorted form:

- model;
- signal timing;
- execution timing;
- side permission;
- threshold basis points;
- fixed notional;
- capital currency and minor-unit scale;
- pyramiding setting;
- force-close setting.

These values are informational export metadata derived from the exact StrategyDefinition.

## 10. Research evidence

The package carries exact fingerprint-bearing references to:

- backtest;
- scientific validation;
- robustness validation;
- optimization selection when present;
- instrument;
- timeframe;
- normalized dataset manifest;
- normalized dataset lock.

Direct strategies explicitly omit optimization selection.

## 11. Manual files

Sprint 22 produces two deterministic byte outputs:

- `<file_stem>.pine` — exact governed Pine source;
- `<file_stem>.manifest.json` — human-facing deterministic research manifest.

The file stem is bounded and cannot contain traversal, separators, spaces or unsafe characters.

## 12. Manual TradingView instructions

The manifest instructs the human researcher to:

1. open the governed symbol;
2. use the governed timeframe;
3. create a new Pine strategy in Pine Editor;
4. paste the exact exported source;
5. avoid changing governed parameters;
6. confirm TradingView compilation;
7. inspect Strategy Tester;
8. record orders/trades for later runtime parity review.

This sprint performs none of those actions automatically.

## 13. Runtime status

Every Sprint 22 package explicitly records:

`runtime_status = NOT_VERIFIED_ON_TRADINGVIEW`.

This means the package is ready for manual TradingView research, but TradingView platform runtime
behavior has not yet been proven by this export step.

## 14. Repaint semantics

Sprint 21 static safety is preserved as:

`STATIC_SAFETY_PASS`

and:

`NO_STATIC_REPAINT_HAZARD_DETECTED`.

The original Pine artifact still remains:

`repaint_assessment = NOT_EVALUATED`.

Sprint 22 therefore does not convert static analysis into a false runtime no-repaint claim.

## 15. Persistence

`TradingViewResearchExportPackage` is added to the strict canonical codec and
`LocalDatasetRepository`.

The package is stored immutably by exact type/version/fingerprint address and can be loaded only when
the canonical bytes verify against that fingerprint.

This closes the Sprint 21 durable packaging precondition.

## 16. Determinism

The export uses no:

- wall clock;
- UUID;
- randomness;
- network input;
- browser state;
- external model call.

The same exact governed inputs and export request produce the same package, Pine bytes and manifest
bytes.

## 17. Exact verification

`verify_tradingview_research_export()` reconstructs the complete expected package from the
verified Sprint 20/Sprint 21 context and requires exact equality.

A manually edited package is not accepted as governed export evidence.

## 18. Deployment / execution closure

Every Sprint 22 package remains:

- `deployment_authorization = NOT_AUTHORIZED`;
- `execution_state = PLANNED_CLOSED`.

No code path grants live execution.

## 19. Runtime parity boundary

Sprint 22 prepares the material needed for manual runtime verification but does not itself prove:

- TradingView compilation success;
- TradingView order timing;
- TradingView fill parity;
- TradingView Strategy Tester parity;
- runtime no-repaint behavior.

Those require actual TradingView platform observations.

## 20. Tests

Focused Sprint 22 coverage includes:

- optimized export;
- direct export;
- immutable repository roundtrip;
- exact Pine source/evidence binding;
- deterministic manifest;
- exact symbol/timeframe instructions;
- strategy parameter export;
- filename traversal/injection rejection;
- export-authority mismatch;
- Pine artifact substitution;
- safety fingerprint substitution;
- provenance substitution;
- package tamper rejection;
- runtime/repaint claim closure;
- capability isolation;
- golden evidence.

The full repository suite must remain green on Python 3.12 and Python 3.13.

## 21. Golden evidence

`tests/golden/tradingview_research_export_v1.json` pins the canonical optimized example including
package fingerprint, research evidence identities, symbol/timeframe, generation and safety
fingerprints, Pine hash/size, filenames, readiness and authority closure.

## 22. Governance BEFORE → AFTER

Before Sprint 22, Pine generation and static safety existed but there was no single durable manual
TradingView delivery artifact.

After Sprint 22, the user-facing research handoff is immutable, deterministic and evidence-bound.

No platform-runtime claim, deployment authority or broker capability is introduced.

## 23. Readiness

- `TRADINGVIEW_RESEARCH_EXPORT_READY`
- `DURABLE_PINE_RESEARCH_PACKAGE_READY`
- `MANUAL_PINE_FILE_READY`
- `MANUAL_RESEARCH_MANIFEST_READY`
- `STRATEGY_PARAMETER_EXPORT_READY`
- `GENERATOR_TO_SAFETY_TO_EXPORT_LINEAGE_READY`
- `DIRECT_EXPORT_READY`
- `OPTIMIZED_EXPORT_READY`
- `TRADINGVIEW_MANUAL_RESEARCH_READY`
- `TRADINGVIEW_RUNTIME_VERIFICATION_NOT_READY`
- `TRADINGVIEW_RUNTIME_NO_REPAINT_NOT_READY`
- `TRADINGVIEW_AUTOMATION_NOT_READY`
- `BROKER_NOT_READY`
- `DEPLOYMENT_NOT_READY`
- `LIVE_EXECUTION_NOT_READY`
- `EXECUTION_CLOSED`

## 24. Limitations

The generated strategy family remains intentionally bounded to the current governed
`CLOSE_VS_OPEN_LONG_ONLY` model.

The export package cannot prove what TradingView will do until the exported Pine is actually compiled
and observed on TradingView.

## 25. Next-step recommendation only

For the user's current project target, Sprint 22 completes the automated local path to a governed Pine
package ready for manual TradingView research.

The next activity should be an end-to-end final readiness review and, if desired, a separately
governed manual TradingView runtime-verification step.

Broker/live work remains deferred.

## 26. Disposition

Target disposition after green CI and final governed review:

`PHASE 3 SPRINT 22 COMPLETE WITH OPEN PRECONDITIONS`
