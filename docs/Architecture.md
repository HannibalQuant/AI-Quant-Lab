# Architecture

## Purpose

AI Quant Lab separates research responsibilities into independently reviewable components. The architecture preserves reproducibility, prevents self-approval, isolates vendors, and makes every strategy decision traceable to versioned evidence. This document defines logical architecture; deployment topology will be specified when runtime requirements are known.

## Principles

1. **Role separation:** hypothesis, implementation, validation, risk, QA, and promotion are distinct authorities.
2. **Artifact-based coordination:** agents exchange validated records, not unstructured conclusions.
3. **Immutable lineage:** material outputs reference exact inputs, code, configuration, data, environment, and parent artifacts.
4. **Deterministic core:** approved identical inputs produce identical outputs within declared numerical tolerances.
5. **Adapter isolation:** providers, brokers, TradingView, and MCP do not define core domain models.
6. **Least authority:** agents receive only capabilities required by their mandates.
7. **Research/production separation:** exploratory code and credentials cannot alter production state directly.
8. **Fail closed:** missing evidence, invalid schemas, stale data, or failed gates stop promotion.

## Agent hierarchy

### Governance layer

**CEO Agent** owns research priority, lifecycle transitions, resource allocation, and final promotion or retirement. It consumes evidence but cannot modify validation or risk reports.

### Control layer

- **Validation Agent** independently evaluates statistical and implementation robustness.
- **Risk Agent** defines and verifies position, portfolio, liquidity, and operational limits.
- **QA Agent** verifies repository integrity, contract compliance, test completeness, and release readiness.

These agents may block promotion within policy. Overrides require an explicit, expiring governance exception.

### Research and implementation layer

- **Quant Strategy Architect** produces falsifiable hypotheses and complete specifications.
- **Research Library** supplies curated evidence and provenance.
- **Python Agent** implements the reference research pipeline and experiments.
- **Pine Agent** implements approved TradingView behavior and parity artifacts.

No implementation agent validates or promotes its own output.

## Knowledge hierarchy

| Level | Content | Authority |
|---|---|---|
| Policy | Vision, architecture, standards, risk and validation policy | Project governance |
| Specification | Strategy rules, schemas, interfaces, acceptance criteria | Design owners with control review |
| Curated evidence | Papers, books, market mechanics, provider documentation | Research Library |
| Experimental evidence | Manifests, metrics, ledgers, plots, failed tests | Producers; independently validated |
| Decision records | Approval, rejection, exception, promotion, retirement | CEO Agent and named reviewers |
| Operational evidence | Telemetry, incidents, degradation reports | Operations, Risk, and QA |

Lower levels may motivate policy changes but cannot silently override them. Conflicts require a versioned decision record.

## Canonical artifacts

- `StrategySpecification`: hypothesis, universe, timeframe, regime, features, rules, sizing, costs, constraints, and invalidation criteria.
- `DatasetManifest`: source, venue, symbols, timestamps, timezone, adjustments, gaps, hashes, and licensing metadata.
- `ExperimentManifest`: code, configuration, dependencies, seeds, data fingerprints, splits, and parent specification.
- `TradeLedger`: signals, orders, fills, positions, fees, funding, and exits.
- `ValidationReport`: tests, distributions, thresholds, failures, and disposition.
- `RiskAssessment`: exposure, capacity, stress, concentration, limits, and kill switches.
- `ParityReport`: reconciled Python and Pine transactions with classified differences.
- `DecisionRecord`: actor, evidence, decision, rationale, exceptions, expiry, and lifecycle state.
- `DeploymentManifest`: immutable approved versions, environment, controls, and rollback target.
- `MonitoringReport`: expected versus observed behavior and degradation state.

Artifacts require schema versions and content identifiers. Markdown may accompany but cannot replace machine-readable records used by automation.

## Decision flow

1. CEO Agent authorizes a research objective and budget.
2. Research Library supplies evidence with provenance.
3. Quant Strategy Architect freezes a specification and validation plan.
4. Python Agent implements the reference and registers experiments.
5. Pine Agent implements TradingView behavior when required.
6. QA Agent verifies contracts and test completeness.
7. Validation Agent evaluates frozen artifacts independently.
8. Risk Agent evaluates standalone and portfolio constraints.
9. CEO Agent chooses `REJECT`, `REVISE`, `PAPER`, or `CANDIDATE`.
10. Approved candidates enter monitoring; degradation may force review or `DISABLED`.

A failed mandatory gate returns the candidate to its producing stage. It does not proceed with a warning.

## Communication flow

Agents communicate through an artifact registry and append-only event log.

### Command

A command includes an identifier, issuer, target, input artifact references, policy context, budget, deadline, and idempotency key.

### Event

An event records an occurrence such as artifact creation, validation failure, review completion, limit breach, or lifecycle transition. Events include causation and correlation identifiers.

### Response

An agent response includes status, output artifact references, tests, assumptions, warnings, and structured errors. Free text may explain but cannot carry an unversioned state change or exception.

## Logical components

### Control plane

- orchestration and task queue;
- policy and permission engine;
- lifecycle state machine;
- artifact and experiment registry;
- decision and audit log;
- human approval interface.

### Research plane

- data quality and normalization;
- feature computation;
- regime and market intelligence;
- edge discovery;
- backtesting and optimization;
- robustness and statistical analysis;
- portfolio and risk analysis.

### Integration plane

- market-data and storage adapters;
- TradingView adapter;
- broker and exchange adapters;
- MCP servers and clients;
- notification and observability exporters.

### Operational plane

- paper and live execution services;
- deployment registry;
- telemetry and reconciliation;
- kill-switch service;
- incident management and rollback.

## Repository philosophy

The repository stores code, schemas, configurations, tests, governance documents, and small durable reference artifacts. Large datasets, secrets, runtime state, and high-volume outputs belong in controlled stores referenced by immutable identifiers.

```text
agents/          mandates and policies
docs/            architecture, standards, operations, decisions
knowledge/       curated evidence metadata and permitted material
src/             production packages grouped by domain
schemas/         versioned artifact and event contracts
configs/         reviewed non-secret configuration
tests/           unit, contract, integration, parity, validation
experiments/     manifests and lightweight indexes
reports/         retained decision-grade reports
deployments/     approved manifests, never secrets
```

Top-level directories require architectural review. Modules own one coherent responsibility and expose stable interfaces. Shared utilities require explicit ownership and dependency direction.

## Lineage

Every decision-grade result is identified by:

```text
strategy specification version
+ code commit
+ environment lock hash
+ dataset manifest and content hashes
+ configuration hash
+ random seeds
+ execution model version
+ experiment identifier
```

Derived artifacts record parents. Mutable aliases such as `latest` may assist discovery but cannot be the sole input to a decision or deployment.

## Future API integrations

External APIs will use versioned adapters and canonical schemas. Categories include market data, exchanges and brokers, reference data, corporate actions, calendars, funding, object storage, experiment tracking, identity, secrets, source control, CI, incident response, and observability.

Adapters must implement authentication isolation, input validation, rate-limit handling, bounded retries, timeouts, idempotency where applicable, health checks, and provider-specific reconciliation.

## Future MCP integrations

MCP may expose narrowly scoped capabilities for research-library search, controlled repository work, dataset discovery, sandboxed experiments, TradingView operations, paper-order simulation, validation retrieval, and governed notifications.

Tools must declare side effects, permissions, schemas, timeouts, and audit fields. Reads and writes are separate. Production execution authority is never granted through transitive tool access.

## Security and failure boundaries

- secrets are injected at runtime and never committed;
- untrusted data and tool output are validated;
- prompts and retrieved documents cannot alter system policy;
- integrations are isolated behind circuit breakers;
- execution services enforce limits independently of strategy code;
- consequential writes are attributable and idempotent where possible;
- backup, restore, rollback, and audit replay are tested;
- emergency disablement does not depend on the failing component.

## Architecture evolution

Material changes require a decision record covering context, alternatives, consequences, migration, compatibility, and rollback. Contracts follow semantic versioning. Deprecated interfaces receive a declared support window or migration plan.

