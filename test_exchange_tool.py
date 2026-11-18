
from tools.exchange_tools import process_exchange
from database import get_connection


# Test 1: Eligible order with available stock
print("\nTEST 1: Successful exchange")
print(process_exchange("ORD101"))


# Test 2: Another order with available stock
print("\nTEST 2: Successful exchange")
print(process_exchange("ORD104"))


# Test 3: Ineligible order
print("\nTEST 3: Ineligible order")
print(process_exchange("ORD103"))


# Test 4: Eligible order but zero stock
print("\nTEST 4: Zero stock")
print(process_exchange("ORD105"))


# Test 5: Invalid order
print("\nTEST 5: Invalid order")
print(process_exchange("ORD999"))


# Test 6: Duplicate exchange attempt
print("\nTEST 6: Duplicate exchange")
print(process_exchange("ORD101"))


# Verify database changes
print("\nTEST 7: Verify inventory and exchanges")

with get_connection() as conn:
    inventory = conn.execute(
        "SELECT * FROM inventory ORDER BY item_id"
    ).fetchall()

    exchanges = conn.execute(
        "SELECT * FROM exchanges ORDER BY exchange_id"
    ).fetchall()

    print("\nInventory:")
    for row in inventory:
        print(dict(row))

    print("\nExchanges:")
    for row in exchanges:
        print(dict(row))
