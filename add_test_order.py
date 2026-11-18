
from database import get_connection

with get_connection() as conn:
    conn.execute("""
        INSERT INTO orders (
            order_id,
            customer_name,
            email,
            item_id,
            amount,
            exchange_eligible,
            status
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        "ORD106",
        "Aditya Test",
        "aditya.test@example.com",
        "HEADPHONE01",
        2000,
        1,
        "PLACED"
    ))

print("Fresh exchange test order created!")
