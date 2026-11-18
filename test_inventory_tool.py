
from tools.inventory_tools import check_inventory

# Test 1: Product with available stock
print("\nTEST 1: Available stock")
print(check_inventory("HEADPHONE01"))

# Test 2: Product with zero stock
print("\nTEST 2: Zero stock")
print(check_inventory("MOUSE01"))

# Test 3: Product that does not exist
print("\nTEST 3: Invalid product")
print(check_inventory("UNKNOWN01"))
