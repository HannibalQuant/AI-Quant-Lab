# AI-Quant-Lab

AI-Quant-Lab is a multi-agent research workspace for designing, implementing, and validating systematic trading strategies under the ARTUR QUANT standard.

## Agent roles

- **Quant-Strategy-Architect** — research hypotheses, strategy design, market logic, and validation requirements.
- **Pine-Agent** — TradingView Pine Script implementations aligned with approved specifications.
- **Python-Agent** — backtesting, optimization, data pipelines, and research tooling.
- **QA-Agent** — parity checks, leakage detection, reproducibility, and robustness audits.
- **CEO-Agent** — priorities, approvals, release decisions, and coordination between agents.

## Research workflow

1. Define a falsifiable market hypothesis.
2. Specify entries, exits, filters, sizing, costs, and execution assumptions.
3. Implement equivalent Pine and Python versions where required.
4. Validate chronologically with out-of-sample tests, Walk-Forward analysis, Monte Carlo, and parameter-stability checks.
5. QA verifies reproducibility and Pine/Python parity.
6. CEO-Agent approves, rejects, or returns the candidate for revision.

## Repository map

- `agents/` — agent mandates and operating rules.
- `knowledge/` — curated books, papers, Pine references, strategies, and market mechanics.
- `tests/` — parity, regression, robustness, and integration tests.

## Core rule

No strategy is promoted because of one attractive backtest. Evidence must survive realistic costs, unseen data, perturbation, and independent QA.
