"""Command line interface for running backtests."""
import pandas as pd
import numpy as np
from strategies import STRATEGIES


def generate_prices(n=200, seed=42):
    rng = np.random.default_rng(seed)
    returns = rng.normal(0, 0.01, size=n)
    price = 100 * (1 + returns).cumprod()
    return pd.Series(price)


def run_backtest(strategy_name: str):
    prices = generate_prices()
    strategy_fn = STRATEGIES[strategy_name]
    result = strategy_fn(prices)
    return result


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Run backtests")
    parser.add_argument("strategy", choices=list(STRATEGIES.keys()))
    args = parser.parse_args()
    result = run_backtest(args.strategy)
    print(result.equity_curve)


if __name__ == "__main__":
    main()
