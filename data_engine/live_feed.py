import requests
import time


class LiveFeed:

    def __init__(self):

        self.endpoints = {

            "BINANCE":
            "https://api.binance.com/api/v3/ticker/price?symbol={}",

            "BYBIT":
            "https://api.bybit.com/v5/market/tickers?category=spot&symbol={}"

        }

    def fetch_binance(self, symbol):

        url = self.endpoints["BINANCE"].format(symbol)

        response = requests.get(url, timeout=10)

        data = response.json()

        return {

            "exchange": "BINANCE",

            "symbol": symbol,

            "price": float(data["price"]),

            "timestamp": time.time()

        }

    def fetch_bybit(self, symbol):

        url = self.endpoints["BYBIT"].format(symbol)

        response = requests.get(url, timeout=10)

        data = response.json()

        price = float(
            data["result"]["list"][0]["lastPrice"]
        )

        return {

            "exchange": "BYBIT",

            "symbol": symbol,

            "price": price,

            "timestamp": time.time()

        }

    def get_price(self, symbol):

        for feed in [
            self.fetch_binance,
            self.fetch_bybit
        ]:

            try:

                return feed(symbol)

            except Exception as e:

                print(f"Feed failed: {e}")

        return None
