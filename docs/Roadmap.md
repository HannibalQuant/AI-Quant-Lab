# Roadmap

## Roadmap policy

This roadmap defines capability milestones rather than fixed dates. A phase is complete only when its exit criteria are satisfied and its artifacts are versioned. Prototypes may begin early, but downstream phases must not depend on an unvalidated interface.

Every phase must produce an approved scope, versioned contracts, test evidence, operational documentation, known failure modes, and a decision record accepting completion or residual risk.

## Phase 1 — Project foundation

### Objective

Establish the repository as the authoritative location for project purpose, architecture, standards, and governance.

### Deliverables

- vision, mission, and design philosophy;
- repository architecture and agent hierarchy;
- documentation, naming, versioning, testing, and review standards;
- initial agent mandates and roadmap;
- auditable branch, pull-request, and decision workflow.

### Exit criteria

- foundational documents are internally consistent and linked from `README.md`;
- ownership and review requirements are explicit;
- future modules have defined boundaries without premature coupling;
- changes can be independently reviewed and traced.

## Phase 2 — Quant Strategy Architect

### Objective

Standardize the conversion of market observations into falsifiable strategy specifications.

### Deliverables

- strategy specification schema;
- strategy-family taxonomy;
- market-mechanics checklist;
- feature and indicator selection policy;
- hypothesis, regime, execution, risk, and invalidation templates;
- candidate statuses and handoff contracts.

### Exit criteria

- specifications support independent implementation;
- entries, exits, sizing, timing, costs, and state transitions are unambiguous;
- the Architect cannot approve its own candidate.

## Phase 3 — Research Library

### Objective

Create a curated, provenance-aware evidence layer for research agents.

### Deliverables

- metadata schemas for sources and datasets;
- citation, licensing, retention, and freshness policy;
- ingestion and deduplication workflow;
- evidence-quality classification;
- links between claims, sources, experiments, and specifications.

### Exit criteria

- every source has provenance and licensing metadata;
- summaries distinguish source claims from project inference;
- superseded and conflicting evidence remains discoverable.

## Phase 4 — Python Agent

### Objective

Build the reference research runtime and reproducible implementation path.

### Deliverables

- data quality engine and multi-asset loader;
- canonical market-data and event schemas;
- feature factory;
- vectorized and event-driven backtest contracts;
- experiment manifest and artifact registry;
- market/timeframe scanner, Trend Quality Score, regime engine, and edge discovery;
- staged optimization with deterministic seeds and pruning;
- locked, reproducible runtime environment.

### Exit criteria

- deterministic reruns reproduce outputs within declared tolerances;
- leakage tests cover features, labels, splits, and optimization;
- fees, funding, spread, slippage, fills, and sizing are explicit;
- adapters pass canonical contract tests.

## Phase 5 — Pine Agent

### Objective

Provide auditable TradingView implementations that preserve approved semantics.

### Deliverables

- Pine coding and release standards;
- strategy-specification translation contract;
- close-only and next-bar-open execution modes;
- real-price policy for transformed charts;
- alert schemas and versioned inputs;
- exported trade ledger and parity harness.

### Exit criteria

- no repainting or undeclared look-ahead behavior;
- signal timing and orders are documented;
- Python/Pine parity is verified trade by trade within tolerances;
- platform limitations are explicit exceptions.

## Phase 6 — Validation Agent

### Objective

Create an independent system whose primary role is to invalidate weak candidates.

### Deliverables

- chronological train/validation/test enforcement;
- rolling and anchored Walk-Forward tests;
- Monte Carlo trade, return, parameter, and execution perturbations;
- parameter stability maps;
- negative controls and destroyed-structure tests;
- multiple-testing and selection-bias analysis;
- adversarial market and execution scenarios;
- cross-seed, cross-window, cross-market, and parity reports;
- machine-readable pass/fail policy.

### Exit criteria

- validation consumes frozen candidate artifacts;
- access to final holdouts is recorded and controlled;
- failures cannot be overridden without a governance exception;
- reports include adverse distributions and rejected folds.

## Phase 7 — Risk Agent

### Objective

Translate strategy behavior into enforceable position, portfolio, liquidity, and operational limits.

### Deliverables

- sizing and exposure policy;
- leverage, margin, concentration, and liquidity constraints;
- correlation and drawdown-correlation analysis;
- portfolio allocation and stress framework;
- loss, volatility, data-quality, and execution kill switches;
- capacity, venue-risk, incident, and recovery procedures.

### Exit criteria

- controls operate outside strategy code;
- kill switches remain available when strategy or data paths fail;
- portfolio tests include common-factor and tail dependence;
- risk exceptions expire and require named approval.

## Phase 8 — CEO Agent

### Objective

Govern priorities, compute allocation, promotion, capital eligibility, degradation, and retirement.

### Deliverables

- lifecycle state machine;
- champion/challenger policy;
- evidence-based confidence score;
- decision-record schema;
- research and compute budget policy;
- escalation, exception, and conflict-resolution procedure;
- immutable approval and rejection log.

### Exit criteria

- transitions require role-separated evidence;
- the CEO Agent cannot rewrite validation results;
- every decision is attributable and reversible when operationally possible;
- research and production credentials remain separate.

## Phase 9 — TradingView and MCP integrations

### Objective

Expose controlled external interfaces without coupling core logic to vendors.

### Deliverables

- TradingView adapter for scripts, alerts, and trade exports;
- MCP servers for approved repository, research, data, and execution capabilities;
- capability-based permissions and scoped credentials;
- idempotency, retry, timeout, rate-limit, and audit policies;
- connector contract tests and sandboxes;
- human approval points for consequential actions.

### Exit criteria

- external payloads are validated before core use;
- credentials never enter prompts, logs, artifacts, or history;
- connectors can be disabled without corrupting research state;
- writes are bounded, attributable, and replay-safe.

## Phase 10 — Autonomous AI Quant Operating System

### Objective

Coordinate the complete lifecycle under bounded authority and continuous oversight.

### Deliverables

- event-driven multi-agent orchestration;
- policy engine for permissions and transitions;
- continuous scanning and hypothesis queueing;
- automated experiment planning within compute budgets;
- portfolio-aware champion/challenger evaluation;
- edge-decay monitoring and governed adaptation;
- observability, audit replay, rollback, and incident response;
- human control plane and emergency stop.

### Exit criteria

- autonomous actions remain within machine-enforced policy;
- every decision can be reconstructed from immutable records;
- failure injection demonstrates safe degradation and recovery;
- research agents cannot acquire production authority implicitly;
- live operation requires separate operational approval.

## Cross-phase workstreams

Security, data licensing, observability, cost accounting, reproducible environments, schema migration, backward compatibility, agent threat modeling, performance benchmarking, and documentation maintenance continue through all phases.

## Release targets

- **V0.x:** contracts, prototypes, and non-production workflows.
- **V1.0:** reproducible single-strategy lifecycle with independent validation and Python/Pine parity.
- **V2.0:** multi-strategy portfolio and risk governance.
- **V3.0:** controlled integrations and paper-trading operations.
- **V4.0:** champion/challenger live monitoring under bounded automation.
- **V5.0:** policy-governed autonomous research operating system.

Release numbers indicate contract maturity, not expected profitability.

