# Phase 3 Sprint 19 — AI Agent → Quant Lab → Pine → TradingView Research Workflow v1.0

## 1. Baseline

- Governed main: `4d9bb3e3d1537bfde906ba16b1c80d88c4b00c47`
- Constitutional baseline: v1.0 / `50b61266f880cb9657b7f1b477d3d90825fe013f`
- Predecessor: PR #79
- Reviewed predecessor head: `dd64bda63ae59492818207fb38c941a4a4dde2fe`

## 2. Mission

Sprint 19 integrates the existing governed Phase 3 research stack into one deterministic, local
research workflow. It does not add new scientific methods, a new backtest engine, Pine execution,
TradingView automation, deployment authority, broker connectivity or live execution.

## 3. Non-goals

No networked LLM client, Pine compiler, browser automation, TradingView login/API, chart scraping,
webhook execution, broker integration, deployment authorization or live trading is introduced.
EXE-01 remains `PLANNED_CLOSED`.

## 4. Workflow architecture

The integrated path is:

AI proposal → StrategyDefinition → experiment authorization → deterministic backtest →
scientific validation → robustness validation → optional governed optimization/selection →
Pine source intake → Pine/Python parity → human research handoff.

The orchestrator creates no scientific authority. It only verifies and binds the exact artifacts
produced by the existing authoritative modules.

## 5. AI proposal boundary

`AIStrategyProposal` records the exact proposing agent, declared hypothesis, primitive parameter
declarations and exact StrategyDefinition reference. `ACCEPTED_FOR_RESEARCH` permits only entry
to the research workflow. `ProposalAuthorityState.PROPOSAL_ONLY` explicitly prevents proposal
identity from being interpreted as authorization.

## 6. Authority separation

Workflow, Pine intake and parity authorities are exact fingerprint-bearing references and are
verified separately. The workflow authority may coordinate and create the final research handoff,
but cannot alter scientific decisions, optimization selection, parity decisions, deployment
authorization or execution state.

## 7. Direct strategy path

`DIRECT_STRATEGY` requires the proposal strategy, plan proposal strategy and final strategy to be
the same exact governed StrategyDefinition. No optimization selection reference may be present.

## 8. Optimized strategy path

`OPTIMIZED_STRATEGY` requires the independently verified Sprint 16 selection result to be
`SELECTED`. The proposal binds the parent strategy while the final workflow strategy must be the
strategy of the actually selected candidate. Parent/rejected/non-selected substitution fails
closed.

## 9. Experiment authorization stage

The workflow invokes `verify_experiment_authorization_lineage()`. Authorization state is consumed,
not re-decided by the orchestrator.

## 10. Backtest stage

Backtest integrity is re-established through the downstream authoritative scientific/robustness and
parity verifiers. The workflow does not implement a second backtest engine.

## 11. Scientific validation stage

Scientific decisions come only from the existing Sprint 14 validation artifacts. `FAIL` maps to
research rejection and `INCONCLUSIVE` remains distinct.

## 12. Robustness stage

The workflow invokes `verify_robustness_validation_lineage()`, which recursively re-verifies the
scientific validation and Python backtest lineage. Robustness `FAIL` and `INCONCLUSIVE` remain
separate final states.

## 13. Optimization stage

Optimized mode invokes `verify_optimization_selection_lineage()`. The orchestrator cannot choose a
winner and cannot substitute the parent strategy after selection.

## 14. Pine generation / intake boundary

Sprint 19 does not call an external AI service. A locally supplied Pine artifact remains governed
by Sprint 17 intake. The final handoff preserves both the proposing-agent ref and the Pine-generating
agent ref. AI-generated Pine receives no trust advantage.

## 15. Parity stage

The workflow invokes `verify_pine_python_parity_lineage()`. A parity `MISMATCH` mechanically
rejects research handoff readiness; `INCONCLUSIVE` remains inconclusive; only `MATCH` can enter
a ready research handoff.

## 16. Final research handoff

`ResearchHandoffPackage` binds proposal, final strategy, candidate/selection when applicable,
backtest, scientific validation, robustness, Pine artifact/intake, parity and agent provenance.
`READY_FOR_HUMAN_RESEARCH_USE` means only that the governed research evidence is internally
coherent for human research use.

It never means deployable, safe to trade or live-ready.

## 17. State machine

The successful optimized sequence is:

`PROPOSAL_ACCEPTED → EXPERIMENT_AUTHORIZED → BACKTEST_COMPLETED →
SCIENTIFIC_VALIDATION_COMPLETED → ROBUSTNESS_COMPLETED → OPTIMIZATION_COMPLETED →
PINE_INTAKE_COMPLETED → PARITY_COMPLETED → RESEARCH_HANDOFF_READY`.

Direct mode omits only `OPTIMIZATION_COMPLETED`.

## 18. Failure vs inconclusive

Mechanical mapping preserves:
- scientific FAIL → `RESEARCH_REJECTED`
- scientific INCONCLUSIVE → `RESEARCH_INCONCLUSIVE`
- robustness FAIL → `RESEARCH_REJECTED`
- robustness INCONCLUSIVE → `RESEARCH_INCONCLUSIVE`
- parity MISMATCH → `RESEARCH_REJECTED`
- parity INCONCLUSIVE → `RESEARCH_INCONCLUSIVE`

## 19. Exact lineage

`verify_integrated_research_workflow_lineage()` deterministically rebuilds the final result,
handoff, TradingView research manifest and run record after independently invoking the existing
authorization, robustness, optimization and parity lineage verifiers.

Stored final state and handoff readiness are not trusted.

## 20. Dataset identity

The exact normalized manifest, normalized lock, instrument and Python backtest references must
remain identical through the final parity result. No symbol, exchange or stablecoin equivalence is
inferred.

## 21. Strategy identity

Direct mode forbids any strategy substitution. Optimized mode requires the exact selected
candidate's StrategyDefinition and candidate-specific evidence.

## 22. Agent traceability

The final handoff keeps exact fingerprint-bearing references for:
- strategy proposing agent
- Pine generating agent
- exact proposal
- exact Pine artifact

Agent identity is evidence of provenance, not authority.

## 23. Determinism

No clock, random UUID, retry loop or adaptive regeneration participates. Exact inputs produce the
same stage sequence, final state, handoff, fingerprints and canonical bytes.

## 24. Persistence

Sprint 19 artifacts use the existing immutable LocalDatasetRepository with strict canonical codecs,
exact type/version identity, idempotent identical writes, no overwrite and corruption detection.

## 25. TradingView research manifest

`TradingViewResearchHandoffManifest` contains the exact Pine SHA-256, strategy/instrument/dataset
identity, parity result reference and research readiness. It is informational only and performs no
TradingView action.

## 26. Repaint boundary

Sprint 19 preserves `repaint_assessment = NOT_EVALUATED`. A historical parity match is not a
general no-repaint proof.

## 27. Deployment / execution closure

All workflow result, handoff, manifest and run records require:
- `deployment_authorization = NOT_AUTHORIZED`
- `execution_state = PLANNED_CLOSED`

No success path can open execution.

## 28. Tests

Focused tests cover optimized end-to-end success, direct-path decision semantics, fail versus
inconclusive mapping, authority mismatch, dataset/strategy substitution, handoff tampering, agent
traceability, codec/persistence idempotency and explicit deployment/execution closure.

## 29. Governance BEFORE → AFTER

Governance is reassessed conservatively. Sprint 19 improves end-to-end traceability,
reproducibility, workflow evidence custody and AI/Pine provenance. It does not resolve real-world
authentication, TradingView compilation, repaint guarantees, deployment authority, broker
authorization or live execution.

## 30. Readiness

- AI_STRATEGY_PROPOSAL_CONTRACT_READY
- INTEGRATED_WORKFLOW_CONTRACT_READY
- WORKFLOW_STATE_MACHINE_READY
- DIRECT_STRATEGY_PATH_READY
- OPTIMIZED_STRATEGY_PATH_READY
- AI_AGENT_TRACEABILITY_READY
- PINE_RESEARCH_HANDOFF_READY
- PARITY_GATED_HANDOFF_READY
- WORKFLOW_LINEAGE_READY
- WORKFLOW_PERSISTENCE_READY
- WORKFLOW_TAMPER_DETECTION_READY
- WORKFLOW_GOLDEN_EVIDENCE_READY
- HUMAN_RESEARCH_HANDOFF_READY
- PINE_REPAINT_ASSESSMENT_NOT_READY
- TRADINGVIEW_COMPILATION_NOT_READY
- TRADINGVIEW_AUTOMATION_NOT_READY
- BROKER_NOT_READY
- DEPLOYMENT_NOT_READY
- LIVE_EXECUTION_NOT_READY
- EXECUTION_CLOSED

## 31. Limitations

The workflow coordinates existing governed evidence only. It does not itself generate real alpha,
authenticate a human or provider, compile Pine on TradingView, prove general no-repaint behavior or
authorize deployment.

## 32. Next-phase recommendation only

After Sprint 19, perform a formal Phase 3 end-to-end readiness and governance review before any
new implementation phase. That review should decide readiness for controlled manual TradingView
research. Paper execution and broker/live execution remain later, separately governed phases.

## 33. Disposition

Target disposition after green CI and independent review:

`PHASE 3 SPRINT 19 COMPLETE WITH OPEN PRECONDITIONS`
