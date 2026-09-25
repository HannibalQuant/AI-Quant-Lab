# Phase 3 Sprint 21 — Pine Safety / No-Repaint Static Validation v1.0

## 1. Baseline

- Governed `main`: `61dd2f5c82cd1986f7bc3fcb8ac7cfca4ba61d3e`
- Predecessor: PR #81 / Phase 3 Sprint 20
- Constitutional baseline: v1.0 / `50b61266f880cb9657b7f1b477d3d90825fe013f`
- Branch: `phase-3/pine-safety-static-validation`

## 2. Mission

Sprint 21 adds a deterministic local safety gate for the exact Pine source produced by Sprint 20.

The validator checks the generated source for a bounded set of explicit repaint/runtime hazards and
verifies that the safety decision is attached to the exact generator result, Pine artifact,
StrategyDefinition, authority and provenance.

The result is a static research-safety assessment only. It is not a TradingView runtime proof.

## 3. Current product target

The active product path remains:

`AI Quant Lab research → selected StrategyDefinition → governed Pine v6 generation → static safety gate → manual TradingView research`.

Broker integration, deployment automation and live trading remain deferred.

## 4. Non-goals

Sprint 21 does not add:

- TradingView login, browser automation, scraping or API calls;
- Pine compilation;
- broker or exchange connectivity;
- webhook execution;
- paper or live order routing;
- deployment authority;
- runtime no-repaint certification;
- new strategy families;
- new optimization methods.

`EXE-01` remains `PLANNED_CLOSED`.

## 5. Exact generator lineage requirement

A governed safety assessment can only run after
`verify_governed_pine_generation()` succeeds on the exact Sprint 20 request/result/context.

A changed source string, substituted strategy fingerprint, changed generated artifact, mismatched
generation fingerprint or substituted provenance fails closed before a safety claim is issued.

## 6. Safety authority

Sprint 21 uses a separate exact fingerprint-bearing safety authority.

The safety authority does not replace or inherit:

- generator authority;
- Pine intake authority;
- optimization-selection authority;
- deployment authority.

A well-formed but different safety authority fails closed.

## 7. Static hazard profile

The bounded scanner detects explicit source constructs that can invalidate the current governed
historical semantics or make historical/realtime behavior diverge:

- `request.*`;
- legacy `security()`;
- `barmerge.lookahead_on`;
- dynamic/mixed timeframe access;
- `barstate.isrealtime`;
- `timenow`;
- `varip`;
- `calc_on_every_tick=true`;
- `calc_on_order_fills=true`;
- `process_orders_on_close=true`;
- alert side effects;
- `use_bar_magnifier=true`;
- absence of the bounded `barstate.isconfirmed` guard.

Strings and comments are masked before hazard scanning so text that merely mentions a forbidden token
does not manufacture a finding.

## 8. Canonical generated profile

The current Sprint 20 generator emits the narrow governed close-vs-open, long-only,
next-bar-open strategy template.

That canonical source contains the confirmed-bar guard and none of the Sprint 21 hazard constructs.

For an exact verified generator result with no findings, the safety decision is `PASS`.

## 9. Static repaint status

Sprint 21 introduces a separate scoped assessment status:

- `NO_STATIC_REPAINT_HAZARD_DETECTED`;
- `STATIC_REPAINT_HAZARD_DETECTED`.

This is deliberately different from a claim of runtime `NO_REPAINT`.

The existing `PineStrategySourceArtifact.repaint_assessment` remains `NOT_EVALUATED` after a
Sprint 21 pass. Static analysis does not upgrade platform-runtime evidence.

## 10. Failure behavior

Governance/lineage failures remain hard failures, including:

- wrong safety authority;
- substituted Pine artifact reference;
- substituted strategy reference;
- substituted generation fingerprint;
- tampered generator result.

Static source hazards are deterministic findings from the bounded scanner.

No failure path opens execution or deployment authority.

## 11. Determinism

The safety scanner and assessment use:

- no wall clock;
- no UUID;
- no random seed;
- no filesystem discovery;
- no network input;
- no provider or model call.

The same exact governed generation evidence and authority produce the same assessment bytes and
input fingerprint.

## 12. Assessment result

`PineSafetyAssessmentResult` records:

- assessment identity and run identity;
- exact Pine artifact reference;
- exact StrategyDefinition reference;
- exact generation input fingerprint;
- raw and normalized source hashes;
- decision;
- scoped static repaint status;
- ordered reason codes;
- deterministic findings with source line/evidence;
- exact safety authority and provenance;
- closed deployment/execution states.

## 13. Exact verification

`verify_pine_static_safety_assessment()` reconstructs the complete expected assessment and requires
exact equality.

Stored summaries or external labels are not trusted by themselves.

## 14. Persistence boundary

Sprint 21 does not introduce a second mutable Pine source or a new repository alias. The canonical
Pine source remains the immutable Sprint 17 `PineStrategySourceArtifact`.

The static safety result is deterministically reconstructable and golden-pinned, but it is not added
as a new `LocalDatasetRepository` stored type in this sprint. Durable packaging/custody of the
safety result belongs to the next governed TradingView research-export package. This limitation is
explicit and does not weaken the immutable custody of the Pine source itself.

## 24. Deployment / execution closure

Every Sprint 21 result remains:

- `deployment_authorization = NOT_AUTHORIZED`;
- `execution_state = PLANNED_CLOSED`.

The validator has no order-submission, webhook, broker or browser capability.

## 15. Relationship to Sprint 17 and Sprint 20

Sprint 17 remains the authoritative Pine source intake and custody boundary.

Sprint 20 remains the authoritative deterministic Pine generator.

Sprint 21 does not replace either layer. It consumes the exact verified Sprint 20 output that already
passed Sprint 17 intake lineage and adds a separate bounded static safety decision.

## 16. Relationship to Pine ↔ Python parity

A Sprint 21 pass does not imply Pine ↔ Python runtime parity.

Sprint 18 parity still requires actual governed Pine/TradingView execution evidence when runtime
parity is being claimed.

## 17. Relationship to TradingView

Sprint 21 never contacts TradingView.

Compilation, chart behavior and runtime execution on TradingView remain external/manual evidence until
a separately governed export/validation step is implemented.

## 18. Golden evidence

`tests/golden/pine_safety_validation_v1.json` pins the canonical optimized example including:

- assessment identity;
- Pine artifact identity;
- strategy identity;
- generation input fingerprint;
- source hashes;
- safety decision;
- scoped static repaint status;
- reason codes;
- finding count;
- unchanged artifact repaint state;
- deployment/execution closure.

## 19. Tests

Focused Sprint 21 tests cover:

- optimized generated-source PASS;
- direct generated-source PASS;
- each explicit static hazard family;
- missing confirmed-bar guard;
- comment/string masking;
- wrong safety authority;
- Pine artifact substitution;
- strategy substitution;
- generation fingerprint substitution;
- tampered generator result;
- deterministic rerun;
- assessment tamper rejection;
- no runtime repaint-state upgrade;
- deployment/execution closure;
- capability isolation;
- golden evidence.

The full repository suite must remain green on Python 3.12 and Python 3.13.

## 20. Governance BEFORE → AFTER

Sprint 21 reduces the risk that generated Pine contains explicit lookahead, mixed-timeframe,
realtime-only or intrabar constructs that contradict the current governed research semantics.

It does not resolve platform authenticity, runtime Pine semantics, TradingView compilation,
general no-repaint proof, deployment authority or execution governance.

## 21. Readiness

- `PINE_STATIC_SAFETY_GATE_READY`
- `PINE_STATIC_REPAINT_HAZARD_SCAN_READY`
- `PINE_CONFIRMED_BAR_GUARD_READY`
- `PINE_GENERATOR_LINEAGE_TO_SAFETY_READY`
- `PINE_SAFETY_AUTHORITY_BOUNDARY_READY`
- `PINE_SAFETY_GOLDEN_EVIDENCE_READY`\n- `PINE_SAFETY_DURABLE_PACKAGE_NOT_READY`
- `PINE_RUNTIME_NO_REPAINT_NOT_READY`
- `TRADINGVIEW_COMPILATION_NOT_READY`
- `TRADINGVIEW_RUNTIME_VALIDATION_NOT_READY`
- `AUTOMATED_TRADINGVIEW_EXPORT_NOT_READY`
- `BROKER_NOT_READY`
- `DEPLOYMENT_NOT_READY`
- `LIVE_EXECUTION_NOT_READY`
- `EXECUTION_CLOSED`

## 22. Limitations

This validator is intentionally conservative and bounded to the generated strategy profile.

Static absence of known hazards cannot prove all future Pine features are safe, cannot prove
TradingView runtime equivalence and cannot prove semantic parity under all market/platform behavior.

A broader Pine grammar or new generator profile requires a new governed safety profile or contract
version.

## 23. Next-step recommendation only

After Sprint 21, the next useful sprint for the current product goal is **TradingView Research Export
v1.0**: package the exact generated Pine source together with strategy identity, parameters,
validation evidence, static-safety result and manual TradingView instructions.

Broker and live-execution work remain outside scope.

## 24. Disposition

Target disposition after green CI and final governed review:

`PHASE 3 SPRINT 21 COMPLETE WITH OPEN PRECONDITIONS`
