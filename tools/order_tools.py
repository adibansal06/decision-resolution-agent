
from database import get_connection


def lookup_order(order_id: str) -> dict:
    """
    Retrieve customer, order, product and exchange eligibility details.

    Args:
        order_id: Unique order identifier.

    Returns:
        Dictionary containing order details or an error.
    """

    if not isinstance(order_id, str) or not order_id.strip():
        return {
            "success": False,
            "error": "A valid order ID is required."
        }

    try:
        with get_connection() as conn:
            record = conn.execute(
                """
                SELECT
                    o.order_id,
                    o.customer_name,
                    o.email,
                    o.item_id,
                    i.item_name,
                    o.amount,
                    o.exchange_eligible,
                    o.status
                FROM orders o
                JOIN inventory i
                    ON o.item_id = i.item_id
                WHERE o.order_id = ?
                """,
                (order_id.strip().upper(),)
            ).fetchone()

        if record is None:
            return {
                "success": False,
                "error": f"Order {order_id} was not found."
            }

        return {
            "success": True,
            "order": {
                "order_id": record["order_id"],
                "customer_name": record["customer_name"],
                "email": record["email"],
                "item_id": record["item_id"],
                "item_name": record["item_name"],
                "amount": record["amount"],
                "exchange_eligible": bool(
                    record["exchange_eligible"]
                ),
                "status": record["status"]
            }
        }

    except Exception as error:
        return {
            "success": False,
            "error": f"Order lookup failed: {str(error)}"
        }
