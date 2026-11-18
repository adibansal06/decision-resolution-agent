
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
        "ORD107",
        "Test Customer",
        "test.customer@example.com",
        "KEYBOARD01",
        3500,
        0,
        "PLACED"
    ))

print("Ineligible test order created successfully!")
