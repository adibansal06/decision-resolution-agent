
from tools.refund_tools import process_refund
from database import get_connection


# Test 1: Refund an eligible order with zero stock
print("\nTEST 1: Refund for unavailable stock")
print(process_refund("ORD102",
    "Replacement item was unavailable."))


# Test 2: Refund an ineligible order
print("\nTEST 2: Refund for ineligible item")
print(process_refund("ORD103",
    "Replacement item was unavailable."))


# Test 3: Invalid order
print("\nTEST 3: Invalid order")
print(process_refund("ORD999",
    "Replacement item was unavailable."))


# Test 4: Attempt duplicate refund
print("\nTEST 4: Duplicate refund")
print(process_refund("ORD102",
    "Replacement item was unavailable."))


# Verify the database records
print("\nTEST 5: Verify refund records")

with get_connection() as conn:
    records = conn.execute(
        "SELECT * FROM refunds ORDER BY refund_id"
    ).fetchall()

    for record in records:
        print(dict(record))
