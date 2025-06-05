"""Command line interface for running backtests."""
import pandas as pd
import requests
from strategies import STRATEGIES


def fetch_prices(symbol: str = "BTCUSDT", interval: str = "1d", limit: int = 200) -> pd.Series:
    """Fetch historical close prices from the Binance API."""
    url = "https://api.binance.com/api/v3/klines"
    params = {"symbol": symbol, "interval": interval, "limit": limit}
    resp = requests.get(url, params=params, timeout=10)
    resp.raise_for_status()
    data = resp.json()
    closes = [float(item[4]) for item in data]
    index = pd.to_datetime([int(item[0]) for item in data], unit="ms")
    return pd.Series(closes, index=index)


def run_backtest(strategy_name: str, *, symbol: str = "BTCUSDT", initial_cash: float = 1000.0):
    prices = fetch_prices(symbol)
    strategy_fn = STRATEGIES[strategy_name]
    result = strategy_fn(prices, initial_cash=initial_cash)
    return result


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Run backtests")
    parser.add_argument("strategy", choices=list(STRATEGIES.keys()))
    parser.add_argument("--symbol", default="BTCUSDT", help="Trading pair symbol")
    parser.add_argument("--initial-cash", type=float, default=1000.0, help="Starting capital")
    args = parser.parse_args()
    result = run_backtest(args.strategy, symbol=args.symbol, initial_cash=args.initial_cash)
    print(result.equity_curve)


if __name__ == "__main__":
    main()
