from data_engine.live_feed import LiveFeed
from data_engine.historical_feed import HistoricalFeed
from storage.db import StorageEngine
import time


live = LiveFeed()
hist = HistoricalFeed()
db = StorageEngine()


# =========================
# LIVE DATA → DB
# =========================

btc = live.get_price("BTCUSDT")
eth = live.get_price("ETHUSDT")

if btc:

    db.insert_candles(

        btc["symbol"],

        [[

            int(time.time()),

            btc["price"],

            btc["price"],

            btc["price"],

            btc["price"],

            1.0

        ]]

    )

if eth:

    db.insert_candles(

        eth["symbol"],

        [[

            int(time.time()),

            eth["price"],

            eth["price"],

            eth["price"],

            eth["price"],

            1.0

        ]]

    )

print("LIVE DATA STORED")


# =========================
# HISTORICAL DATA → DB
# =========================

candles = hist.fetch_candles("BTCUSDT", limit=10)

db.insert_candles("BTCUSDT", candles)

print("HISTORICAL DATA STORED")


# =========================
# VERIFY DATA
# =========================

print("\nLATEST BTC CANDLES FROM DB:")
print(db.get_candles("BTCUSDT", limit=5))
