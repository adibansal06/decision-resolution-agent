
import sqlite3
from pathlib import Path

# Database file will be created in the project directory
DB_PATH = Path(__file__).parent / "resolution.db"


def get_connection():
    """Create and return a database connection."""

    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row

    # Enable foreign key validation
    connection.execute("PRAGMA foreign_keys = ON")

    return connection


def initialize_database():
    """Create tables and insert sample records."""

    with get_connection() as conn:

        # 1. Inventory table
        conn.execute("""
            CREATE TABLE IF NOT EXISTS inventory (
                item_id TEXT PRIMARY KEY,
                item_name TEXT NOT NULL,
                stock_quantity INTEGER NOT NULL
                    CHECK(stock_quantity >= 0)
            )
        """)

        # 2. Orders table
        conn.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                order_id TEXT PRIMARY KEY,
                customer_name TEXT NOT NULL,
                email TEXT NOT NULL,
                item_id TEXT NOT NULL,
                amount REAL NOT NULL CHECK(amount > 0),
                exchange_eligible INTEGER NOT NULL
                    CHECK(exchange_eligible IN (0, 1)),
                status TEXT NOT NULL DEFAULT 'PLACED',
                FOREIGN KEY (item_id)
                    REFERENCES inventory(item_id)
            )
        """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS refunds (
                refund_id INTEGER PRIMARY KEY AUTOINCREMENT,
                order_id TEXT NOT NULL UNIQUE,
                amount REAL NOT NULL,
                payment_method TEXT NOT NULL
                    DEFAULT 'ORIGINAL_PAYMENT_METHOD',
                status TEXT NOT NULL DEFAULT 'PROCESSED',
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (order_id)
                    REFERENCES orders(order_id)
            )
        """)

        # Add the reason column to existing databases if needed.
        refund_columns = {
            row["name"]
            for row in conn.execute(
                "PRAGMA table_info(refunds)"
            ).fetchall()
        }

        if "reason" not in refund_columns:
            conn.execute("""
                ALTER TABLE refunds
                ADD COLUMN reason TEXT NOT NULL
                DEFAULT 'Not specified'
            """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS exchanges (
                exchange_id INTEGER PRIMARY KEY AUTOINCREMENT,
                order_id TEXT NOT NULL UNIQUE,
                item_id TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'CONFIRMED',
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (order_id)
                    REFERENCES orders(order_id),
                FOREIGN KEY (item_id)
                    REFERENCES inventory(item_id)
            )
        """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS notifications (
                notification_id INTEGER PRIMARY KEY AUTOINCREMENT,
                order_id TEXT NOT NULL,
                recipient_email TEXT NOT NULL,
                subject TEXT NOT NULL,
                message TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'SENT',
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (order_id)
                    REFERENCES orders(order_id)
            )
        """)

        # 3. Insert sample inventory
        inventory_records = [
            ("HEADPHONE01", "Wireless Headphones", 5),
            ("MOUSE01", "Wireless Mouse", 0),
            ("KEYBOARD01", "Mechanical Keyboard", 10),
            ("MONITOR01", "LED Monitor", 2),
        ]

        conn.executemany("""
            INSERT OR IGNORE INTO inventory
            (item_id, item_name, stock_quantity)
            VALUES (?, ?, ?)
        """, inventory_records)

        # 4. Insert sample orders
        order_records = [
            ("ORD101", "Rahul", "rahul@example.com",
             "HEADPHONE01", 2000, 1, "PLACED"),

            ("ORD102", "Priya", "priya@example.com",
             "MOUSE01", 1000, 1, "PLACED"),

            ("ORD103", "Aman", "aman@example.com",
             "KEYBOARD01", 3500, 0, "PLACED"),

            ("ORD104", "Neha", "neha@example.com",
             "MONITOR01", 12000, 1, "PLACED"),

            ("ORD105", "Karan", "karan@example.com",
             "MOUSE01", 1000, 1, "PLACED"),
        ]

        conn.executemany("""
            INSERT OR IGNORE INTO orders
            (order_id, customer_name, email, item_id,
             amount, exchange_eligible, status)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, order_records)

    print("Database initialized successfully!")


def display_database():
    """Display orders along with their inventory information."""

    with get_connection() as conn:

        records = conn.execute("""
            SELECT
                o.order_id,
                o.customer_name,
                o.item_id,
                i.item_name,
                o.amount,
                o.exchange_eligible,
                i.stock_quantity
            FROM orders o
            JOIN inventory i
                ON o.item_id = i.item_id
            ORDER BY o.order_id
        """).fetchall()

        print("\n========= ORDER RECORDS =========")

        for row in records:
            print(dict(row))


if __name__ == "__main__":
    initialize_database()
    display_database()
