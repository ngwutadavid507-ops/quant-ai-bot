import time
import csv
import os


class PnLEngine:

    def __init__(self):

        self.positions = {}

        self.trades = []

        self.cooldowns = {}

        self.logfile = "storage/trade_journal.csv"

        self.initialize_log()

    def initialize_log(self):

        os.makedirs("storage", exist_ok=True)

        if not os.path.exists(self.logfile):

            with open(self.logfile, "w", newline="") as f:

                writer = csv.writer(f)

                writer.writerow([
                    "timestamp",
                    "symbol",
                    "direction",
                    "entry",
                    "exit",
                    "pnl",
                    "reason"
                ])

    def log_trade(self, trade):

        with open(self.logfile, "a", newline="") as f:

            writer = csv.writer(f)

            writer.writerow([
                time.strftime("%Y-%m-%d %H:%M:%S"),
                trade["symbol"],
                trade["direction"],
                trade["entry"],
                trade["exit"],
                trade["pnl"],
                trade["reason"]
            ])

    def open_position(self, symbol, price, direction):

        if symbol in self.cooldowns:

            cooldown_time = time.time() - self.cooldowns[symbol]

            if cooldown_time < 30:

                print(f"{symbol} cooldown active")

                return

        if symbol in self.positions:

            return

        self.positions[symbol] = {
            "entry": price,
            "direction": direction,
            "open_time": time.time()
        }

        print(f"OPEN {direction} {symbol} @ {price}")

    def close_position(self, symbol, price, reason="manual"):

        if symbol not in self.positions:

            return

        pos = self.positions[symbol]

        entry = pos["entry"]

        direction = pos["direction"]

        pnl = 0

        if direction == "BUY":

            pnl = price - entry

        elif direction == "SELL":

            pnl = entry - price

        trade = {
            "symbol": symbol,
            "entry": entry,
            "exit": price,
            "direction": direction,
            "pnl": pnl,
            "reason": reason
        }

        self.trades.append(trade)

        self.log_trade(trade)

        print(f"CLOSE {symbol} PnL: {pnl} | {reason}")

        self.cooldowns[symbol] = time.time()

        del self.positions[symbol]

    def manage_positions(self, symbol, price, signal):

        if symbol not in self.positions:

            return

        pos = self.positions[symbol]

        entry = pos["entry"]

        direction = pos["direction"]

        open_time = pos["open_time"]

        hold_time = time.time() - open_time

        pnl = price - entry if direction == "BUY" else entry - price

        # minimum hold time

        if hold_time < 20:

            return

        # take profit

        if pnl > entry * 0.003:

            self.close_position(symbol, price, "take_profit")

        # stop loss

        elif pnl < -entry * 0.002:

            self.close_position(symbol, price, "stop_loss")

        # signal flip protection

        elif pnl < 0 and (
            (direction == "BUY" and signal == "SELL") or
            (direction == "SELL" and signal == "BUY")
        ):

            self.close_position(symbol, price, "signal_flip")

    def get_total_pnl(self):

        return sum(t["pnl"] for t in self.trades)

    def get_stats(self):

        wins = len([t for t in self.trades if t["pnl"] > 0])

        losses = len([t for t in self.trades if t["pnl"] <= 0])

        avg_win = (
            sum(t["pnl"] for t in self.trades if t["pnl"] > 0) / wins
            if wins else 0
        )

        avg_loss = (
            sum(t["pnl"] for t in self.trades if t["pnl"] <= 0) / losses
            if losses else 0
        )

        return {
            "total_trades": len(self.trades),
            "wins": wins,
            "losses": losses,
            "win_rate": (
                (wins / len(self.trades)) * 100
                if self.trades else 0
            ),
            "avg_win": avg_win,
            "avg_loss": avg_loss,
            "total_pnl": self.get_total_pnl()
        }
