import numpy as np


class SignalEngine:

    def __init__(self):

        self.price_history = {}

    def update_price(self, symbol, price):

        if symbol not in self.price_history:

            self.price_history[symbol] = []

        self.price_history[symbol].append(price)

        if len(self.price_history[symbol]) > 100:

            self.price_history[symbol].pop(0)

    def moving_average(self, prices, period):

        if len(prices) < period:

            return None

        return np.mean(prices[-period:])

    def volatility(self, prices):

        if len(prices) < 10:

            return 0

        return np.std(prices[-10:])

    def trend_strength(self, short_ma, long_ma):

        return abs(short_ma - long_ma)

    def generate_signal(self, symbol):

        prices = self.price_history.get(symbol, [])

        if len(prices) < 15:

            return "WAIT"

        short_ma = self.moving_average(prices, 5)

        long_ma = self.moving_average(prices, 12)

        current = prices[-1]

        previous = prices[-2]

        momentum = current - previous

        vol = self.volatility(prices)

        trend = self.trend_strength(short_ma, long_ma)

        # sideways market filter
        if trend < current * 0.0005:

            print(f"{symbol} market sideways")

            return "WAIT"

        # excessive volatility filter
        if vol > current * 0.01:

            print(f"{symbol} volatility too high")

            return "WAIT"

        # strong bullish trend
        if (
            short_ma > long_ma
            and momentum > current * 0.0002
        ):

            return "BUY"

        # strong bearish trend
        elif (
            short_ma < long_ma
            and momentum < -(current * 0.0002)
        ):

            return "SELL"

        return "WAIT"
