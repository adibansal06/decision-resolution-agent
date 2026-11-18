
from database import get_connection


def notify_customer(
    email: str,
    message: str,
    order_id: str
) -> dict:
    """
    Record a simulated email notification.

    Args:
        email: Customer's registered email address.
        message: Notification message body.
        order_id: Resolved order associated with the notification.
    """

    if not isinstance(email, str) or not email.strip():
        return {"success": False, "error": "Valid email is required."}

    if not isinstance(message, str) or not message.strip():
        return {"success": False, "error": "Message body is required."}

    if not isinstance(order_id, str) or not order_id.strip():
        return {"success": False, "error": "Valid order ID is required."}

    email = email.strip()
    message = message.strip()
    order_id = order_id.strip().upper()

    try:
        with get_connection() as conn:
            conn.execute("BEGIN IMMEDIATE")

            order = conn.execute(
                """
                SELECT order_id, customer_name, email, status
                FROM orders
                WHERE order_id = ?
                """,
                (order_id,)
            ).fetchone()

            if order is None:
                return {"success": False, "error": "Order not found."}

            if order["email"].lower() != email.lower():
                return {
                    "success": False,
                    "error": "Email does not match the registered customer."
                }

            if order["status"] not in ("REFUNDED", "EXCHANGED"):
                return {
                    "success": False,
                    "error": "Order has not been resolved yet."
                }

            existing = conn.execute(
                """
                SELECT notification_id FROM notifications
                WHERE order_id = ?
                """,
                (order_id,)
            ).fetchone()

            if existing:
                return {
                    "success": False,
                    "error": "Notification already recorded for this order."
                }

            subject = f"Update regarding your order {order_id}"

            cursor = conn.execute(
                """
                INSERT INTO notifications
                (order_id, recipient_email, subject, message, status)
                VALUES (?, ?, ?, ?, 'SIMULATED')
                """,
                (order_id, email, subject, message)
            )

            return {
                "success": True,
                "notification_id": cursor.lastrowid,
                "order_id": order_id,
                "recipient_email": email,
                "subject": subject,
                "status": "SIMULATED"
            }

    except Exception as error:
        return {
            "success": False,
            "error": f"Notification failed: {str(error)}"
        }
