import requests


class DataEngine:

    def __init__(self):

        self.symbols = [
            "BTCUSDT",
            "ETHUSDT"
        ]

    def fetch_binance(self, symbol):

        try:

            url = (
                f"https://api.binance.com/api/v3/ticker/price"
                f"?symbol={symbol}"
            )

            response = requests.get(
                url,
                timeout=15
            )

            data = response.json()

            return float(data["price"])

        except Exception as e:

            print(f"{symbol} Binance feed failed -> {e}")

            return None

    def fetch_bybit(self, symbol):

        try:

            url = (
                f"https://api.bybit.com/v5/market/tickers"
                f"?category=linear&symbol={symbol}"
            )

            response = requests.get(
                url,
                timeout=15
            )

            data = response.json()

            return float(
                data["result"]["list"][0]["lastPrice"]
            )

        except Exception as e:

            print(f"{symbol} Bybit feed failed -> {e}")

            return None

    def get_price(self, symbol):

        # try Binance first

        price = self.fetch_binance(symbol)

        if price is not None:

            return price

        # fallback to Bybit

        price = self.fetch_bybit(symbol)

        if price is not None:

            return price

        print(f"ALL FEEDS FAILED FOR {symbol}")

        return None

    def get_market_snapshot(self):

        snapshot = {}

        for symbol in self.symbols:

            snapshot[symbol] = self.get_price(symbol)

        return snapshot
