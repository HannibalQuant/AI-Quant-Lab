# Decision Engine

## Intake

For every request, identify the instrument, timeframe, market regime, data source, execution model, objective, and constraints.

## Decision sequence

1. State the market hypothesis and why the edge may exist.
2. Select a strategy family compatible with the hypothesized regime.
3. Define measurable entry and exit rules before optimization.
4. Set risk, fees, slippage, liquidity, and position-sizing assumptions.
5. Define acceptance thresholds and validation splits in advance.
6. Request implementation from Pine-Agent and/or Python-Agent.
7. Submit results to QA-Agent.
8. Recommend `REJECT`, `REVISE`, `PAPER`, or `CANDIDATE` to CEO-Agent.

## Tie-breakers

When candidates are similar, prefer lower complexity, lower drawdown, fewer sensitive parameters, higher trade count, and better out-of-sample stability.

