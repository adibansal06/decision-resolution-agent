
# Declarative tool contracts for the Groq LLM.
# These follow the OpenAI-compatible function-calling format.

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "lookup_order",
            "description": (
                "Look up a customer order using its order ID. "
                "Returns customer details, purchased item, amount, "
                "order status, and exchange eligibility. "
                "Use this first when investigating a customer complaint."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "order_id": {
                        "type": "string",
                        "description": "The customer's unique order ID."
                    }
                },
                "required": ["order_id"],
                "additionalProperties": False
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "check_inventory",
            "description": (
                "Inspect warehouse stock for a product. "
                "Use the item ID obtained from order lookup "
                "to determine whether a replacement is available."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "item_id": {
                        "type": "string",
                        "description": "Unique product identifier."
                    }
                },
                "required": ["item_id"],
                "additionalProperties": False
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "process_refund",
            "description": (
                "Record a mock refund to the original payment method "
                "when an order is ineligible for exchange or replacement "
                "stock is unavailable. Only use after investigating "
                "the order and its eligibility or inventory."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "order_id": {
                        "type": "string",
                        "description": "Order to refund."
                    },
                    "reason": {
                        "type": "string",
                        "description": "Reason why the refund is required."
                    }
                },
                "required": ["order_id", "reason"],
                "additionalProperties": False
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "process_exchange",
            "description": (
                "Confirm an exchange and reserve one replacement unit. "
                "Use only when the order is eligible and inventory is available. "
                "The function rechecks eligibility and stock before reserving."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "order_id": {
                        "type": "string",
                        "description": "Order to exchange."
                    }
                },
                "required": ["order_id"],
                "additionalProperties": False
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "notify_customer",
            "description": (
                "Record a simulated email notification for a customer "
                "after their order has been successfully refunded or exchanged. "
                "The email must match the registered order email."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "email": {
                        "type": "string",
                        "description": "Customer's registered email address."
                    },
                    "message": {
                        "type": "string",
                        "description": "Confirmation message to send."
                    },
                    "order_id": {
                        "type": "string",
                        "description": "Resolved order associated with the message."
                    }
                },
                "required": ["email", "message", "order_id"],
                "additionalProperties": False
            }
        }
    }
]
