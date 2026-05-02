class RiskEngine:

    def __init__(self):

        self.max_loss_streak = 3

        self.loss_streak = 0

        self.cooldown = False

    def evaluate_trade(self, signal, volatility):

        # block trading if cooldown active

        if self.cooldown:

            return "BLOCKED"

        # skip high volatility

        if volatility > 50:

            return "BLOCKED"

        # only allow strong signals

        if signal not in ["BUY", "SELL"]:

            return "NO_TRADE"

        return "ALLOW"

    def record_result(self, win):

        if win:

            self.loss_streak = 0

        else:

            self.loss_streak += 1

        if self.loss_streak >= self.max_loss_streak:

            self.cooldown = True
