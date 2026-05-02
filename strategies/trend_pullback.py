class TrendPullbackStrategy:

    def sma(self, candles, period=20):

        if len(candles) < period:

            return None

        closes = [float(c[6]) for c in candles[-period:]]

        return sum(closes) / period

    def generate(self, candles):

        if len(candles) < 25:

            return "WAIT"

        price = float(candles[-1][6])

        prev = float(candles[-2][6])

        ma = self.sma(candles)

        if ma is None:

            return "WAIT"

        # =========================
        # REALISTIC TREND SYSTEM
        # =========================

        trend_up = price > ma

        trend_down = price < ma

        pullback_up = price < prev * 0.999

        pullback_down = price > prev * 1.001

        # =========================
        # SIGNAL RULES (FIXED)
        # =========================

        if trend_up and pullback_up:

            return "BUY"

        if trend_down and pullback_down:

            return "SELL"

        return "WAIT"
