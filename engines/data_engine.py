import requests
import time


class DataEngine:

    def __init__(self):

        self.cache = {}

    # =========================
    # BYBIT (FAST PRIMARY)
    # =========================

    def bybit(self, symbol):

        try:

            r = requests.get(

                "https://api.bybit.com/v5/market/tickers",

                params={
                    "category": "spot",
                    "symbol": symbol
                },

                timeout=5
            )

            return float(

                r.json()["result"]

                ["list"][0]

                ["lastPrice"]

            )

        except:

            return None

    # =========================
    # OKX (BACKUP)
    # =========================

    def okx(self, symbol):

        try:

            pair = symbol.replace(
                "USDT",
                "-USDT"
            )

            r = requests.get(

                "https://www.okx.com/api/v5/market/ticker",

                params={
                    "instId": pair
                },

                timeout=5
            )

            return float(

                r.json()["data"][0]["last"]

            )

        except:

            return None

    # =========================
    # KRAKEN (3RD BACKUP)
    # =========================

    def kraken(self, symbol):

        try:

            pair_map = {
                "BTCUSDT": "XBTUSD",
                "ETHUSDT": "ETHUSD"
            }

            r = requests.get(

                f"https://api.kraken.com/0/public/Ticker?pair={pair_map[symbol]}",

                timeout=5
            )

            data = r.json()["result"]

            key = list(data.keys())[0]

            return float(data[key]["c"][0])

        except:

            return None

    # =========================
    # SMART PRICE (MEDIAN)
    # =========================

    def get_price(self, symbol):

        prices = [

            self.bybit(symbol),

            self.okx(symbol),

            self.kraken(symbol)

        ]

        valid = [p for p in prices if p is not None]

        if len(valid) == 0:

            print(
                "ALL FEEDS FAILED"
            )

            return None

        valid.sort()

        return valid[len(valid)//2]
