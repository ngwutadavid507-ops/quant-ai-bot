import requests
import csv
import os


class HistoricalFeed:

    def __init__(self):

        self.base_url = "https://api.binance.com/api/v3/klines"

    def fetch_candles(self, symbol, interval="1m", limit=100):

        params = {

            "symbol": symbol,

            "interval": interval,

            "limit": limit

        }

        response = requests.get(

            self.base_url,

            params=params,

            timeout=10

        )

        return response.json()

    def save_to_csv(self, symbol, candles):

        os.makedirs("historical_data", exist_ok=True)

        filename = f"historical_data/{symbol}.csv"

        file_exists = os.path.exists(filename)

        with open(filename, "a", newline="") as f:

            writer = csv.writer(f)

            if not file_exists:

                writer.writerow([

                    "open_time",

                    "open",

                    "high",

                    "low",

                    "close",

                    "volume"

                ])

            for c in candles:

                writer.writerow([

                    c[0],

                    c[1],

                    c[2],

                    c[3],

                    c[4],

                    c[5]

                ])
