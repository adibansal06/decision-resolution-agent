
from tools.notification_tools import notify_customer
from database import get_connection


# Test 1: Notify customer after refund
print("\nTEST 1: Refund notification")

print(notify_customer(
    "rahul@example.com",
    "Your exchange has been confirmed.",
    "ORD101"
))


# Test 2: Notify customer after exchange
print("\nTEST 2: Exchange notification")

print(notify_customer(
    "rahul@example.com",
    "Your exchange has been confirmed.",
    "ORD101"
))


# Test 3: Invalid order
print("\nTEST 3: Invalid order")

print(notify_customer(
    "rahul@example.com",
    "Your exchange has been confirmed.",
    "ORD101"
))


# Test 4: Unresolved order
print("\nTEST 4: Unresolved order")

print(notify_customer(
    "rahul@example.com",
    "Your exchange has been confirmed.",
    "ORD105"
))


# Test 5: Duplicate notification
print("\nTEST 5: Duplicate notification")

print(notify_customer(
    "rahul@example.com",
    "Your refund has been processed.",
    "ORD102"
))


# Verify notification records
print("\nTEST 6: Database verification")

with get_connection() as conn:
    records = conn.execute(
        "SELECT * FROM notifications ORDER BY notification_id"
    ).fetchall()

    for record in records:
        print(dict(record))
