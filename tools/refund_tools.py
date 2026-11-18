
from database import get_connection


def process_refund(order_id: str, reason: str) -> dict:
    """
    Record a mock refund against the original payment method.

    Args:
        order_id: Order identifier.
        reason: Reason for initiating the refund.
    """

    if not isinstance(order_id, str) or not order_id.strip():
        return {"success": False, "error": "Valid order ID required."}

    if not isinstance(reason, str) or not reason.strip():
        return {"success": False, "error": "Refund reason is required."}

    order_id = order_id.strip().upper()
    reason = reason.strip()

    try:
        with get_connection() as conn:
            conn.execute("BEGIN IMMEDIATE")

            order = conn.execute(
                """
                SELECT order_id, amount, status
                FROM orders WHERE order_id = ?
                """,
                (order_id,)
            ).fetchone()

            if order is None:
                return {"success": False, "error": "Order not found."}

            if order["status"] != "PLACED":
                return {
                    "success": False,
                    "error": f"Order already resolved or unavailable: {order['status']}"
                }

            cursor = conn.execute(
                """
                INSERT INTO refunds
                (order_id, amount, payment_method, status, reason)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    order_id,
                    order["amount"],
                    "ORIGINAL_PAYMENT_METHOD",
                    "PROCESSED",
                    reason
                )
            )

            conn.execute(
                "UPDATE orders SET status = 'REFUNDED' WHERE order_id = ?",
                (order_id,)
            )

            return {
                "success": True,
                "refund_id": cursor.lastrowid,
                "order_id": order_id,
                "refund_amount": order["amount"],
                "reason": reason,
                "payment_method": "ORIGINAL_PAYMENT_METHOD",
                "status": "PROCESSED"
            }

    except Exception as error:
        return {
            "success": False,
            "error": f"Refund processing failed: {str(error)}"
        }
