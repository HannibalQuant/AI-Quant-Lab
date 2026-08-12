# Market Mechanics

Every design must consider:

- tick size, lot size, leverage, margin, and funding;
- maker/taker fees, spread, slippage, and latency;
- session structure, gaps, maintenance windows, and exchange outages;
- liquidity, market impact, volume quality, and data-source differences;
- spot, perpetual, futures, CFD, and equity-specific mechanics;
- signal evaluation time versus actual fill time.

Backtests must use conservative executable assumptions. Close-only and next-bar-open modes must be named explicitly, never mixed silently.

