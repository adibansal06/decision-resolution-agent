
from tools.order_tools import lookup_order

# Test 1: Existing order
print("\nTEST 1: Existing order")
print(lookup_order("ORD101"))

# Test 2: Ineligible order
print("\nTEST 2: Ineligible order")
print(lookup_order("ORD103"))

# Test 3: Invalid order
print("\nTEST 3: Non-existing order")
print(lookup_order("ORD999"))
