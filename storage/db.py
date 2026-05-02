import sqlite3
import os


class StorageEngine:

    def __init__(self, db_name="quant.db"):

        os.makedirs("storage", exist_ok=True)

        self.db_path = f"storage/{db_name}"

        self.conn = sqlite3.connect(self.db_path)

        self.cursor = self.conn.cursor()

        self.create_tables()

    # =========================
    # TABLES
    # =========================

    def create_tables(self):

        # CANDLES TABLE
        self.cursor.execute("""

        CREATE TABLE IF NOT EXISTS candles (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            symbol TEXT NOT NULL,

            timestamp INTEGER NOT NULL,

            open REAL,

            high REAL,

            low REAL,

            close REAL,

            volume REAL

        )

        """)

        # TRADES TABLE
        self.cursor.execute("""

        CREATE TABLE IF NOT EXISTS trades (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            symbol TEXT NOT NULL,

            direction TEXT NOT NULL,

            entry_price REAL,

            exit_price REAL,

            pnl REAL,

            timestamp INTEGER

        )

        """)

        self.conn.commit()

    # =========================
    # INSERT CANDLES
    # =========================

    def insert_candles(self, symbol, candles):

        for c in candles:

            self.cursor.execute("""

                INSERT INTO candles (

                    symbol,

                    timestamp,

                    open,

                    high,

                    low,

                    close,

                    volume

                ) VALUES (?, ?, ?, ?, ?, ?, ?)

            """, (

                symbol,

                int(c[0]),

                float(c[1]),

                float(c[2]),

                float(c[3]),

                float(c[4]),

                float(c[5])

            ))

        self.conn.commit()

    # =========================
    # INSERT TRADE
    # =========================

    def insert_trade(self, symbol, direction, entry, exit, pnl, timestamp):

        self.cursor.execute("""

            INSERT INTO trades (

                symbol,

                direction,

                entry_price,

                exit_price,

                pnl,

                timestamp

            ) VALUES (?, ?, ?, ?, ?, ?)

        """, (

            symbol,

            direction,

            entry,

            exit,

            pnl,

            timestamp

        ))

        self.conn.commit()

    # =========================
    # READ DATA
    # =========================

    def get_candles(self, symbol, limit=100):

        self.cursor.execute("""

            SELECT * FROM candles

            WHERE symbol = ?

            ORDER BY timestamp DESC

            LIMIT ?

        """, (symbol, limit))

        return self.cursor.fetchall()

    def get_trades(self, symbol=None):

        if symbol:

            self.cursor.execute("""

                SELECT * FROM trades

                WHERE symbol = ?

            """, (symbol,))

        else:

            self.cursor.execute("""

                SELECT * FROM trades

            """)

        return self.cursor.fetchall()
