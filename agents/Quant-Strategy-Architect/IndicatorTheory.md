# Indicator Theory

Indicators are transformations of price, volume, volatility, or time. They are measurements, not independent sources of edge.

## Categories

- **Trend:** moving averages, slope, directional movement.
- **Momentum:** RSI, rate of change, MACD-derived measures.
- **Volatility:** ATR, realized volatility, range estimators.
- **Participation:** volume, open interest, breadth, order-flow proxies.
- **Structure:** swing points, breakouts, distance from value, support/resistance.

## Design rules

Avoid redundant indicators that encode the same information. Document lag, normalization, warm-up, missing-data behavior, and timeframe aggregation. Each filter must have a testable purpose and an ablation test.

