from data_engine.live_feed import LiveFeed
from data_engine.historical_feed import HistoricalFeed


live = LiveFeed()

hist = HistoricalFeed()


# =========================
# LIVE PRICE TEST
# =========================

btc = live.get_price("BTCUSDT")

eth = live.get_price("ETHUSDT")

print("\nLIVE DATA:")

print(btc)

print(eth)


# =========================
# HISTORICAL TEST
# =========================

candles = hist.fetch_candles(

    "BTCUSDT",

    interval="1m",

    limit=10

)

hist.save_to_csv("BTCUSDT", candles)

print("\nHistorical data saved to CSV")
