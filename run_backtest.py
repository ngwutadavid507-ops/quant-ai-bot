from backtest_engine import BacktestEngine


def main():

    symbol = "BTCUSDT"

    engine = BacktestEngine(symbol)

    engine.run()


if __name__ == "__main__":

    main()
