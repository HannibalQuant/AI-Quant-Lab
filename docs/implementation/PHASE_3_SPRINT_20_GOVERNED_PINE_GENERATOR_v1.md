# Phase 3 Sprint 20 — Governed Pine Generator v1.0

## 1. Baseline

- Governed main: `395012b43d27f01910677936e65cfcfc972eb161`
- Predecessor: PR #80 / Phase 3 Sprint 19
- Constitutional baseline: v1.0 / `50b61266f880cb9657b7f1b477d3d90825fe013f`
- Branch: `phase-3/governed-pine-generator`

## 2. Mission

Sprint 20 adds a deterministic local generator that converts the exact governed
`StrategyDefinition` into canonical Pine Script v6 source and immediately submits that source
through the existing Sprint 17 governed Pine intake.

The output is a research artifact intended for manual use in TradingView. The generator does not
open deployment or execution authority.

## 3. User goal

The current product boundary is:

`AI Quant Lab research → selected StrategyDefinition → governed Pine v6 source → manual TradingView research`.

Broker integration, automated order routing and live execution are explicitly outside the current
project target.

## 4. Non-goals

Sprint 20 does not add:

- broker or exchange connectivity;
- webhook execution;
- live or paper order routing;
- TradingView login, browser automation, scraping or API calls;
- a Pine compiler;
- a networked LLM client;
- new strategy families;
- new optimization methods;
- a no-repaint certification;
- deployment authorization.

`EXE-01` remains `PLANNED_CLOSED`.

## 5. Supported generation profile

v1 supports only the already-governed bounded model:

- `StrategyModel.CLOSE_VS_OPEN_LONG_ONLY`;
- close-evaluated signal semantics;
- first eligible next-bar-open execution;
- long-only;
- fixed cash notional;
- no pyramiding;
- no forced terminal close.

Unsupported strategy semantics fail closed.

## 6. Generated Pine semantics

The canonical source:

- declares `//@version=6`;
- uses `strategy()`, not `indicator()`;
- fixes `pyramiding=0`;
- fixes `process_orders_on_close=false`;
- fixes `calc_on_every_tick=false`;
- uses `default_qty_type=strategy.cash`;
- reconstructs exact fixed notional from the governed strategy;
- converts `threshold_bps` to a Pine threshold using 10,000 basis points per unit;
- evaluates only confirmed bars;
- enters long when `close / open - 1 > threshold`;
- exits the long position when the governed desired state returns to flat;
- contains no `request.*`, legacy `security()`, alerts or webhook behavior.

The generated source is deliberately narrow and template-controlled.

## 7. Determinism

`render_governed_pine_v6()` has no wall clock, UUID, random seed, network input or adaptive
generation. The same StrategyDefinition and script title produce byte-identical Pine source.

The source embeds the exact strategy identity and strategy fingerprint as comments. Strategy
parameter changes therefore change the generated source identity.

## 8. Generator authority

Generation has its own exact fingerprint-bearing authority reference.

The generation request must match the exact generator authority carried by
`GovernedPineGeneratorContext`. A well-formed but different authority reference fails closed.

Generation authority does not imply Pine intake authority.

## 9. Intake authority separation

The generator cannot mint or substitute Pine intake authority.

The request must bind the exact `pine_intake_authority_ref` already carried by
`PineStrategyIntakeContext`. Generated source then passes through the existing Sprint 17 intake,
which independently verifies static compatibility and the complete research evidence chain.

## 10. Strategy and evidence lineage

The generator request binds the exact StrategyDefinition fingerprint.

For direct strategies, generated intake contains no optimization references.

For optimized strategies, the generator deterministically derives:

- the exact selected candidate definition reference;
- the exact selected candidate result reference;
- the exact optimization selection reference.

The existing Sprint 17 verifier then independently proves that the selected candidate and its
backtest, scientific validation and robustness evidence are exact.

## 11. Existing governed intake reuse

Sprint 20 does not create a parallel Pine custody system.

Generated source is converted to the existing `PineStrategyIntakeRequest` and processed by
`intake_pine_strategy()`. The resulting `PineStrategySourceArtifact` and
`PineStrategyIntakeRecord` remain the canonical persisted source and intake evidence.

This reuses existing strict codec, immutable repository, source hashing, corruption detection and
candidate-lineage verification rather than duplicating them.

## 12. Generation verification

`verify_governed_pine_generation()` deterministically reconstructs:

- generator authority boundary;
- exact strategy binding;
- canonical source text;
- exact intake request;
- generation input fingerprint;
- exact generated artifact source;
- Sprint 17 Pine intake lineage.

Stored or returned generator summaries are not trusted by themselves.

## 13. TradingView boundary

The output is Pine source suitable for manual copy/paste or later controlled export to TradingView.

Sprint 20 performs no TradingView action. Compilation on the TradingView platform remains a separate
external validation step.

## 14. Parity boundary

A generated Pine artifact still records:

- `semantic_parity = NOT_EVALUATED`;
- `repaint_assessment = NOT_EVALUATED`.

Generation does not silently inherit a parity or no-repaint claim. Existing Sprint 18 parity must
still be run against actual Pine/TradingView execution evidence when such evidence is available.

## 15. Deployment and execution closure

Generated and intake artifacts remain:

- `deployment_authorization = NOT_AUTHORIZED`;
- `execution_state = PLANNED_CLOSED`.

The generator exposes no code path that opens deployment or execution.

## 16. Failure behavior

The generator fails closed for:

- wrong generator authority;
- substituted Pine intake authority;
- wrong strategy fingerprint;
- unsupported strategy profile;
- unsafe or non-canonical script title;
- missing selected candidate binding;
- any downstream Sprint 17 lineage or static-intake failure.

It does not downgrade governance failures into successful generation.

## 17. Source-title boundary

The script title is a bounded static literal of 1–96 characters. Quotes, backslashes and line breaks
are rejected so a title cannot escape the controlled `strategy()` declaration or inject Pine code.

## 18. Persistence

No new storage type is introduced. The canonical generated source is persisted through the existing
`PineStrategySourceArtifact` and `PineStrategyIntakeRecord` contracts and the immutable local
repository.

This intentionally minimizes governance surface and avoids a second source-of-truth for Pine code.

## 19. Golden evidence

`tests/golden/governed_pine_generator_v1.json` pins the optimized generation example including:

- generator profile;
- strategy identity;
- threshold;
- raw and normalized source hashes;
- byte size;
- generation input fingerprint;
- Pine artifact fingerprint;
- intake record fingerprint;
- optimization selection identity;
- parity/repaint states;
- deployment/execution closure.

## 20. Tests

Focused Sprint 20 coverage includes:

- optimized selected-candidate generation;
- direct-strategy generation;
- canonical Pine semantic template;
- byte determinism;
- strategy sensitivity;
- title injection rejection;
- generator-authority mismatch;
- intake-authority substitution;
- strategy fingerprint substitution;
- result tamper detection;
- exact Sprint 17 lineage verification;
- research-only authority closure;
- capability isolation;
- golden evidence.

The full repository suite must remain green on Python 3.12 and 3.13.

## 21. Governance BEFORE → AFTER

Sprint 20 improves controlled source generation and removes the manual authoring gap for the single
currently supported governed strategy model. It does not change scientific authority, selection
authority, platform authenticity, deployment authority or execution authority.

No existing constitutional precondition is silently upgraded to deployment-ready status.

## 22. Readiness

- `GOVERNED_PINE_GENERATOR_READY`
- `DETERMINISTIC_PINE_TEMPLATE_READY`
- `DIRECT_STRATEGY_PINE_GENERATION_READY`
- `SELECTED_CANDIDATE_PINE_GENERATION_READY`
- `GENERATOR_AUTHORITY_BOUNDARY_READY`
- `GENERATOR_TO_INTAKE_LINEAGE_READY`
- `GENERATED_SOURCE_GOLDEN_EVIDENCE_READY`
- `MANUAL_TRADINGVIEW_SOURCE_READY`
- `MULTI_STRATEGY_PINE_GENERATION_NOT_READY`
- `TRADINGVIEW_COMPILATION_NOT_READY`
- `PINE_REPAINT_ASSESSMENT_NOT_READY`
- `AUTOMATED_TRADINGVIEW_EXPORT_NOT_READY`
- `BROKER_NOT_READY`
- `DEPLOYMENT_NOT_READY`
- `LIVE_EXECUTION_NOT_READY`
- `EXECUTION_CLOSED`

## 23. Limitations

The generator covers one intentionally narrow strategy family. Pine floating-point behavior is not
declared equivalent to Python Decimal behavior merely because source generation is deterministic.

TradingView compilation, platform runtime semantics, actual Pine ↔ Python event parity and general
no-repaint proof remain external or later governed evidence.

## 24. Next-step recommendation only

After Sprint 20, the next useful sprint for the user's current goal is a bounded **Pine Safety /
No-Repaint Static Validation & TradingView Research Export** step. Broker and live-execution work
remain deferred.

## 25. Disposition

Target disposition after green CI and final review:

`PHASE 3 SPRINT 20 COMPLETE WITH OPEN PRECONDITIONS`
