from engines.data_engine import DataEngine

engine = DataEngine()

while True:

    btc = engine.get_price(
        "BTCUSDT"
    )

    eth = engine.get_price(
        "ETHUSDT"
    )

    print(
        "BTC:",
        btc
    )

    print(
        "ETH:",
        eth
    )

    print(
        "----------------"
    )
