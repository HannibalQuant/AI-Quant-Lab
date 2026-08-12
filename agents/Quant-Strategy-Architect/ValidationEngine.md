# Validation Engine

## Mandatory layers

1. Deterministic baseline with fees, spread, and slippage.
2. Chronological train/validation/test separation.
3. Walk-Forward analysis with train-only optimization.
4. Monte Carlo perturbation of trade order, fills, and/or returns as appropriate.
5. Parameter Stability Map around selected settings.
6. Regime, symbol, and timeframe stress tests when the hypothesis permits.
7. Pine/Python transaction parity for dual implementations.

## Minimum reporting

Report net profit, max drawdown, profit factor, expectancy, trade count, win rate, worst trade, exposure, and stability across folds. Include rejected candidates and failed folds.

## Leakage control

Record whether outer test data was touched. Final evaluation data must remain unseen until the candidate and parameters are frozen.

