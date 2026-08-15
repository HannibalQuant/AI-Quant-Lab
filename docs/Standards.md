# Standards

## Scope

These standards apply to documentation, source code, schemas, configuration, tests, research artifacts, and agent-generated changes. Specific standards may strengthen but not weaken them without approval. `MUST`, `MUST NOT`, `SHOULD`, and `MAY` indicate requirement strength.

## Documentation standards

Documentation MUST be precise, testable where possible, and understandable without the original discussion. It MUST distinguish requirements, assumptions, examples, observations, and unresolved decisions.

Decision-relevant documents MUST include purpose, audience, status, owner, scope, non-goals, dependencies, affected contracts, and review trigger. Each concept MUST have one authoritative location; other documents SHOULD link rather than duplicate mutable rules.

Research results MUST identify the hypothesis, universe, timeframe, sample boundaries, data source, features, execution, costs, sizing, parameter space, objective, seeds, validation, limitations, and artifact identifiers. Negative results and failed gates MUST be retained when material to selection or interpretation.

## Naming conventions

- Names MUST describe domain responsibility, not temporary ownership or convenience.
- Avoid abbreviations unless established and defined.
- Do not use subjective or transient names such as `final`, `best`, `new`, or `fixed`.
- Include units where ambiguous: `latency_ms`, `fee_bps`.
- Booleans SHOULD use `is_`, `has_`, `can_`, or `should_`.
- Python modules, functions, variables, and keys use `snake_case`.
- Classes and typed domain objects use `PascalCase`.
- Constants use `UPPER_SNAKE_CASE`.
- Tests use `test_<subject>.py` or the language-native equivalent.
- Schemas use `<artifact_name>.v<major>.schema.json` until a registry replaces file discovery.

Existing hyphenated agent directories remain valid repository identifiers.

## Markdown conventions

- Use one level-one heading and sequential heading levels.
- Use sentence case except for proper names.
- Fence code with a language identifier where applicable.
- Use tables for exact mappings, not decorative layout.
- Use relative links for repository files and descriptive link text.
- Label non-normative examples.
- Approved documents MUST NOT contain placeholders except explicitly authorized fields such as the pending license.

## Folder philosophy

Every top-level directory MUST have an owner and retention policy. A directory represents a stable domain boundary, not file count.

- `agents/`: mandates and operating policies, not outputs.
- `docs/`: architecture, standards, governance, operations, and decisions.
- `knowledge/`: curated material or metadata permitted by licensing policy.
- `src/`: production packages when introduced.
- `schemas/`: machine-readable contracts.
- `configs/`: non-secret reviewed configuration.
- `tests/`: executable verification by test class or domain.
- `experiments/` and `reports/`: retained manifests and decision-grade evidence, not bulk output.

The repository MUST NOT contain credentials, private keys, tokens, unrestricted proprietary datasets, caches, local environments, or large reproducible outputs.

## Coding standards

### Design

- Modules MUST have one coherent responsibility and explicit public interfaces.
- Domain logic MUST be separate from adapters, persistence, orchestration, and presentation.
- Dependencies MUST point toward stable domain contracts.
- Hidden global state and implicit time dependence are prohibited in research-critical logic.
- Randomness MUST be injected or seeded and recorded.
- Timezones, units, currencies, adjustment, and missing-data behavior MUST be explicit.
- Floating-point comparisons MUST use documented tolerances when exact equality is inappropriate.

### Interfaces

Public interfaces MUST define types, invariants, errors, side effects, and compatibility. Inputs from files, APIs, agents, and tools MUST be validated at boundaries. Breaking changes require a major version and migration instructions.

### Errors and logging

Errors MUST be classified and actionable. Research code MUST NOT silently substitute data, skip failed tests, or convert invalid values into acceptable results. Logs MUST contain correlation identifiers and MUST NOT contain secrets.

### Dependencies

Dependencies MUST be locked, reviewed for licensing and security, and justified by maintenance value. Core research calculations SHOULD favor transparent and testable implementations.

## Versioning

Software and contracts follow semantic versioning:

- `MAJOR`: incompatible contract, schema, execution-semantic, or policy change;
- `MINOR`: backward-compatible capability;
- `PATCH`: backward-compatible correction.

Pre-1.0 breaking changes still require release notes and migration guidance.

Strategy specifications, dataset and experiment manifests, validation reports, and deployments MUST be immutable once used in a decision. Corrections create a linked new version. Mutable names such as `latest` MUST NOT appear as sole references in decision or deployment records.

### Git workflow

- Protected default branches SHOULD require pull requests.
- Branches use `<type>/<short-description>`; agent branches use `agent/<short-description>`.
- Commits SHOULD be focused, imperative, and coherent.
- Force-push to protected or shared branches is prohibited.
- Releases MUST be tagged and documented.

## Quality requirements

A change is acceptable only when it is correct against specification, reproducible, proportionally tested, traceable, independently reviewed, documented, policy-compatible, observable where operational, and reversible or covered by recovery. Quantitative results MUST include uncertainty and adverse behavior. Metrics MUST define calculation conventions.

## Review process

Material pull requests MUST state the problem, scope, rationale, changed contracts, downstream effects, validation, risks, limitations, migration, rollback, and unresolved decisions.

Required reviews follow ownership:

- governance documents: document owner;
- research logic: Quant Strategy Architect;
- statistical validation: Validation Agent;
- risk logic: Risk Agent;
- external interfaces and secrets: security-aware reviewer;
- releases: QA disposition.

The authoring agent MUST NOT be the sole approver. Correctness comments are resolved by a change or documented decision, not acknowledgment alone.

Exceptions MUST identify the rule, reason, owner, scope, risk, compensating control, expiry, and removal plan. Permanent undocumented exceptions are prohibited.

## Testing philosophy

Testing demonstrates properties and contracts; it does not merely execute lines.

1. **Unit:** deterministic calculations, states, and edge cases.
2. **Property:** invariants across generated inputs.
3. **Contract:** schemas and provider adapters.
4. **Integration:** data, strategy, validation, and storage interaction.
5. **Regression:** approved behavior and known bug cases.
6. **Parity:** Python, Pine, and execution-path agreement.
7. **Research validation:** chronology, Walk-Forward, Monte Carlo, stability, negative controls, and multiple-testing defenses.
8. **Operational:** failures, retries, idempotency, reconciliation, kill switches, rollback, and recovery.

Quantitative tests MUST prevent future data from influencing earlier decisions. Signal, order, and fill timestamps must be testable separately. Fees, spread, slippage, funding, gaps, and partial fills require boundary cases. Metrics require manually verifiable fixtures. Optimization MUST be separated from final evaluation. Stochastic tests record seeds; parity tests classify rather than hide mismatches.

Continuous integration SHOULD include formatting, linting, type checks, unit and contract tests, documentation links, schema validation, secret scanning, and dependency checks. Expensive research validation MAY run on scheduled workflows, but its absence MUST be visible. Flaky tests are defects and require repair or time-bounded quarantine.

## Definition of done

Work is done when acceptance criteria are met, tests pass, documentation and schemas are current, lineage is recorded, reviews are satisfied, and no unresolved high-severity risk remains. Generated output or a successful workflow alone does not establish completion.

