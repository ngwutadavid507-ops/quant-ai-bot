from engines.data_engine import DataEngine
from engines.signal_engine import SignalEngine
from engines.risk_engine import RiskEngine
from engines.pnl_engine import PnLEngine

import time


data_engine = DataEngine()

signal_engine = SignalEngine()

risk_engine = RiskEngine()

pnl_engine = PnLEngine()


while True:

    snapshot = data_engine.get_market_snapshot()

    print("\n===================")

    for symbol, price in snapshot.items():

        print(f"{symbol}: {price}")

        if price is None:

            continue

        # update market history

        signal_engine.update_price(symbol, price)

        # generate signal

        signal = signal_engine.generate_signal(symbol)

        print(f"{symbol} | Signal: {signal}")

        # manage open trades

        pnl_engine.manage_positions(symbol, price, signal)

        # skip weak signals

        if signal == "WAIT":

            continue

        # volatility check

        prices = signal_engine.price_history.get(symbol, [])

        volatility = signal_engine.volatility(prices)

        decision = risk_engine.evaluate_trade(
            signal,
            volatility
        )

        print(f"{symbol} | Risk: {decision}")

        # open trades

        if decision == "ALLOW":

            pnl_engine.open_position(
                symbol,
                price,
                signal
            )

    stats = pnl_engine.get_stats()

    print("\n📊 TOTAL PnL:", stats["total_pnl"])

    print("📈 WIN RATE:", stats["win_rate"])

    print("🔁 TRADES:", stats["total_trades"])

    print("===================")

    time.sleep(10)
