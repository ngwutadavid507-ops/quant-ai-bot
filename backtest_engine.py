from storage.db import StorageEngine
from strategies.trend_pullback import TrendPullbackStrategy


class BacktestEngine:

    def __init__(self, symbol):

        self.symbol = symbol
        self.db = StorageEngine()
        self.strategy = TrendPullbackStrategy()

        self.position = None
        self.entry_price = None

        self.pnl = 0.0
        self.wins = 0
        self.losses = 0
        self.trades = []

    # =========================
    # PnL
    # =========================

    def calc_pnl(self, exit_price):

        if self.position == "BUY":
            return exit_price - self.entry_price

        if self.position == "SELL":
            return self.entry_price - exit_price

        return 0.0

    # =========================
    # EXECUTION
    # =========================

    def execute(self, signal, price):

        price = float(price)

        if self.position is None and signal in ["BUY", "SELL"]:

            self.position = signal
            self.entry_price = price

            print(f"OPEN {signal} @ {price}")
            return

        if self.position is not None and signal != self.position and signal in ["BUY", "SELL"]:

            pnl = self.calc_pnl(price)

            self.pnl += pnl

            if pnl > 0:
                self.wins += 1
            else:
                self.losses += 1

            self.trades.append(pnl)

            print(f"CLOSE {self.position} PnL: {pnl}")

            self.position = signal
            self.entry_price = price

            print(f"OPEN {signal} @ {price}")

    # =========================
    # RUN BACKTEST (CLEAN FIX)
    # =========================

    def run(self):

        candles = self.db.get_candles(self.symbol, limit=300)

        candles = candles[::-1]

        print("\nSTARTING BACKTEST...\n")

        print(f"CANDLES LOADED: {len(candles)}")

        if len(candles) < 10:

            print("NOT ENOUGH DATA")

            return

        for i in range(10, len(candles)):

            window = candles[i-10:i]

            price = float(candles[i][6])

            signal = self.strategy.generate(window)

            print(f"i={i} PRICE={price} SIGNAL={signal}")

            self.execute(signal, price)

        self.summary()

    # =========================
    # SUMMARY
    # =========================

    def summary(self):

        total = self.wins + self.losses

        win_rate = (self.wins / total * 100) if total > 0 else 0

        print("\n===================")
        print(f"SYMBOL: {self.symbol}")
        print(f"TOTAL PnL: {self.pnl:.2f}")
        print(f"WIN RATE: {win_rate:.2f}%")
        print(f"TRADES: {total}")
        print("===================")
