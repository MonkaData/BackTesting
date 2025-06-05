# Basic strategies for backtesting
from dataclasses import dataclass
import pandas as pd
import numpy as np

@dataclass
class StrategyResult:
    equity_curve: pd.Series


def buy_and_hold(prices: pd.Series, initial_cash: float = 1000.0) -> StrategyResult:
    """Simple buy and hold strategy."""
    shares = initial_cash / prices.iloc[0]
    equity = shares * prices
    return StrategyResult(equity_curve=equity)


def moving_average_crossover(prices: pd.Series, short_window: int = 20, long_window: int = 50, initial_cash: float = 1000.0) -> StrategyResult:
    """Moving average crossover strategy."""
    short_ma = prices.rolling(window=short_window).mean()
    long_ma = prices.rolling(window=long_window).mean()
    signal = (short_ma > long_ma).astype(int)
    positions = signal.diff().fillna(0)

    cash = initial_cash
    shares = 0
    equity_curve = []

    for price, pos_change in zip(prices, positions):
        if pos_change == 1:  # buy
            shares = cash / price
            cash = 0
        elif pos_change == -1:  # sell
            cash = shares * price
            shares = 0
        equity_curve.append(cash + shares * price)

    return StrategyResult(equity_curve=pd.Series(equity_curve, index=prices.index))

# Map strategy names to functions
STRATEGIES = {
    "Buy and Hold": buy_and_hold,
    "MA Crossover": moving_average_crossover,
}
