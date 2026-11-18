
from dispatcher import dispatch_tool
from tool_schemas import TOOLS


# Test 1: Valid order lookup
print("\nTEST 1: Valid tool call")

print(dispatch_tool(
    "lookup_order",
    {"order_id": "ORD101"}
))


# Test 2: Valid inventory inspection
print("\nTEST 2: Inventory inspection")

print(dispatch_tool(
    "check_inventory",
    {"item_id": "HEADPHONE01"}
))


# Test 3: Unknown tool
print("\nTEST 3: Unauthorized tool")

print(dispatch_tool(
    "delete_database",
    {}
))


# Test 4: Missing required argument
print("\nTEST 4: Missing argument")

print(dispatch_tool(
    "lookup_order",
    {}
))


# Test 5: Malformed JSON
print("\nTEST 5: Malformed JSON")

print(dispatch_tool(
    "lookup_order",
    '{"order_id": '
))


# Test 6: Unexpected argument
print("\nTEST 6: Unexpected argument")

print(dispatch_tool(
    "lookup_order",
    {
        "order_id": "ORD101",
        "password": "anything"
    }
))


# Test 7: Verify tool schemas
print("\nTEST 7: Registered tool schemas")

for tool in TOOLS:
    print(tool["function"]["name"])
