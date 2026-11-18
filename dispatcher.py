
import json

from tools.order_tools import lookup_order
from tools.inventory_tools import check_inventory
from tools.refund_tools import process_refund
from tools.exchange_tools import process_exchange
from tools.notification_tools import notify_customer


# Centralized whitelist: only these functions may be executed.
TOOL_REGISTRY = {
    "lookup_order": lookup_order,
    "check_inventory": check_inventory,
    "process_refund": process_refund,
    "process_exchange": process_exchange,
    "notify_customer": notify_customer
}


# Define the accepted arguments for every registered tool.
TOOL_ARGUMENTS = {
    "lookup_order": {
        "required": {"order_id"}
    },
    "check_inventory": {
        "required": {"item_id"}
    },
    "process_refund": {
        "required": {"order_id", "reason"}
    },
    "process_exchange": {
        "required": {"order_id"}
    },
    "notify_customer": {
        "required": {"email", "message", "order_id"}
    }
}


def dispatch_tool(tool_name: str, arguments) -> dict:
    """
    Safely validate and execute a registered tool.

    Args:
        tool_name: Name requested by the LLM.
        arguments: Dictionary or JSON string of arguments.

    Returns:
        Structured tool execution result.
    """

    # 1. Authorization: reject unknown tools.
    if tool_name not in TOOL_REGISTRY:
        return {
            "success": False,
            "error": f"Tool '{tool_name}' is not authorized."
        }

    # 2. Parse arguments.
    if isinstance(arguments, str):
        try:
            arguments = json.loads(arguments)
        except json.JSONDecodeError:
            return {
                "success": False,
                "error": "Malformed JSON arguments."
            }

    # 3. Ensure arguments are a JSON object.
    if not isinstance(arguments, dict):
        return {
            "success": False,
            "error": "Tool arguments must be a JSON object."
        }

    required = TOOL_ARGUMENTS[tool_name]["required"]
    received = set(arguments.keys())

    # 4. Check missing arguments.
    missing = required - received

    if missing:
        return {
            "success": False,
            "error": f"Missing required arguments: {sorted(missing)}"
        }

    # 5. Reject unexpected arguments.
    unexpected = received - required

    if unexpected:
        return {
            "success": False,
            "error": f"Unexpected arguments: {sorted(unexpected)}"
        }

    # 6. Validate argument values.
    for key, value in arguments.items():
        if not isinstance(value, str) or not value.strip():
            return {
                "success": False,
                "error": f"Argument '{key}' must be a non-empty string."
            }

    # 7. Execute only the whitelisted function.
    try:
        function = TOOL_REGISTRY[tool_name]
        return function(**arguments)

    except Exception as error:
        return {
            "success": False,
            "error": f"Tool execution failed: {str(error)}"
        }
