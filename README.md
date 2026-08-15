# AI Quant Lab

AI Quant Lab is a versioned, multi-agent research platform for developing, implementing, validating, and governing systematic trading strategies. The repository is the source of truth for research policy, agent responsibilities, software contracts, validation evidence, and promotion decisions.

The project is designed for reproducible quantitative research. It does not treat a profitable backtest as sufficient evidence of an edge.

## Project vision

AI Quant Lab will provide a controlled operating environment in which specialized agents can move a research question from market observation to an auditable strategy candidate. Each agent operates within an explicit mandate, exchanges typed artifacts rather than informal conclusions, and is subject to independent validation.

The long-term target is an instrument-agnostic platform that can:

- rank markets and timeframes by research suitability;
- classify market regimes and detect transitions;
- discover and test conditional return hypotheses before optimization;
- implement equivalent Python and Pine Script strategies;
- run chronological, statistical, adversarial, and cross-market validation;
- construct portfolios subject to risk and concentration constraints;
- monitor live degradation and trigger governed responses;
- preserve the complete lineage of every result and decision.

See [Vision](docs/Vision.md) for the complete project thesis.

## Mission

The mission is to convert quantitative research into a disciplined, inspectable engineering process. AI Quant Lab exists to reduce four recurring risks: irreproducible experiments, hidden data leakage, implementation divergence, and promotion decisions based on incomplete evidence.

The platform must make it easier to reject a weak strategy than to rationalize it.

## Long-term goals

1. Establish reproducible research from immutable inputs, versioned configurations, deterministic code, and recorded random seeds.
2. Separate hypothesis formation, implementation, validation, risk review, and deployment approval.
3. Maintain Python-to-Pine semantic parity where TradingView delivery is required.
4. Support crypto, foreign exchange, commodities, indices, and equities without strategy-specific infrastructure rewrites.
5. Evaluate candidates across time, regimes, markets, parameter neighborhoods, and execution assumptions.
6. Build a governed champion/challenger lifecycle with explicit degradation and retirement rules.
7. Expose stable interfaces for data providers, brokers, TradingView, research services, and future MCP servers.

## Agent ecosystem

| Agent | Primary responsibility | Required output |
|---|---|---|
| CEO Agent | Research priorities, resource allocation, promotion and retirement decisions | Decision record and approved lifecycle state |
| Quant Strategy Architect | Hypothesis design, strategy specification, research constraints | Versioned strategy specification |
| Research Library | Evidence acquisition, provenance, synthesis, and citation | Curated evidence package |
| Python Agent | Data pipelines, backtests, optimization, analysis, and reference implementation | Reproducible research package |
| Pine Agent | TradingView implementation and platform-specific execution semantics | Versioned Pine implementation |
| Validation Agent | Independent robustness, leakage, parity, and adversarial testing | Validation report with pass/fail gates |
| Risk Agent | Position, portfolio, liquidity, exposure, and kill-switch policy | Risk assessment and enforceable limits |
| QA Agent | Repository quality, contracts, tests, traceability, and release checks | QA report and release disposition |

Agents do not approve their own work. The producer of an artifact is separate from the agent responsible for validating it. Full responsibilities and communication rules are defined in [Architecture](docs/Architecture.md).

## Repository structure

```text
AI-Quant-Lab/
├── agents/                     # Agent mandates, policies, and operating instructions
├── docs/                       # Project-level architecture and governance
│   ├── Vision.md
│   ├── Roadmap.md
│   ├── Architecture.md
│   └── Standards.md
├── knowledge/                  # Curated evidence with provenance and licensing metadata
│   ├── books/
│   ├── papers/
│   ├── pine/
│   ├── strategies/
│   └── market-mechanics/
├── tests/                      # Unit, integration, parity, regression, and validation tests
└── README.md
```

Future top-level directories may include `src/`, `configs/`, `schemas/`, `experiments/`, `reports/`, and `deployments/`. They will be introduced only with documented ownership and stable contracts.

## Development philosophy

- **Evidence before optimization.** A candidate begins with a falsifiable hypothesis and a predeclared evaluation plan.
- **Chronology is a constraint.** Training, validation, and final evaluation boundaries are explicit and machine-verifiable.
- **Contracts over conversations.** Agents exchange versioned specifications, manifests, reports, and decision records.
- **Independent review.** Implementation, validation, risk assessment, and promotion are separate responsibilities.
- **Reproducibility by default.** Every reported result must identify code, configuration, data lineage, environment, and seed.
- **Conservative execution.** Costs, slippage, latency, funding, liquidity, and fill rules are modeled explicitly.
- **Stable regions over isolated optima.** Parameter robustness and cross-window consistency take precedence over peak backtest performance.
- **Failure is an artifact.** Rejected hypotheses and failed tests are retained to prevent repeated work and selection bias.

## Roadmap overview

Development is divided into ten capability phases:

1. Project foundation and governance.
2. Quant Strategy Architect.
3. Research Library.
4. Python Agent and reproducible research runtime.
5. Pine Agent and semantic parity.
6. Independent Validation Agent.
7. Risk Agent and portfolio controls.
8. CEO Agent and lifecycle governance.
9. TradingView and MCP integrations.
10. Autonomous AI Quant Operating System under bounded authority.

Each phase has entry criteria, deliverables, validation gates, and exit criteria in the [Roadmap](docs/Roadmap.md).

## Future modules

Planned modules include a data quality engine, multi-asset loader, feature factory, market and timeframe scanner, Trend Quality Score, regime engine, edge discovery engine, hierarchical optimizer, parameter stability analysis, Walk-Forward and Monte Carlo engines, adversarial testing, portfolio construction, parity reporting, edge-decay monitoring, experiment registry, and deployment registry.

Module names describe responsibilities, not implementation commitments. Public interfaces will be specified before implementation.

## Contribution philosophy

Contributions are evaluated on correctness, traceability, test coverage, and compatibility with project contracts. A change must explain why it is needed, what assumptions it introduces, how it was validated, and which downstream artifacts it affects.

Research contributions must include negative results when they materially affect interpretation. Generated artifacts are not committed unless their retention policy requires it. Changes to governance, schemas, execution semantics, or validation thresholds require explicit owner review.

See [Standards](docs/Standards.md) for naming, documentation, review, testing, and versioning requirements.

## License

License: **TBD — legal and distribution review required before external reuse or redistribution.**

Until a license is selected and committed, no permission is granted beyond rights implied by the repository host and applicable law.
