
from database import get_connection


def process_exchange(order_id: str) -> dict:
    """
    Confirm an exchange and reserve one replacement item.

    Rechecks eligibility and stock inside a database
    transaction to prevent invalid or duplicate exchanges.
    """

    if not isinstance(order_id, str) or not order_id.strip():
        return {
            "success": False,
            "error": "A valid order ID is required."
        }

    order_id = order_id.strip().upper()

    try:
        with get_connection() as conn:
            # Start an immediate transaction to safely
            # coordinate stock reservation.
            conn.execute("BEGIN IMMEDIATE")

            order = conn.execute(
                """
                SELECT order_id, item_id, exchange_eligible, status
                FROM orders
                WHERE order_id = ?
                """,
                (order_id,)
            ).fetchone()

            if order is None:
                return {
                    "success": False,
                    "error": f"Order {order_id} was not found."
                }

            if order["status"] != "PLACED":
                return {
                    "success": False,
                    "error": (
                        f"Order cannot be exchanged. "
                        f"Current status: {order['status']}."
                    )
                }

            if not order["exchange_eligible"]:
                return {
                    "success": False,
                    "error": "This order is not eligible for exchange."
                }

            item_id = order["item_id"]

            inventory = conn.execute(
                """
                SELECT item_name, stock_quantity
                FROM inventory
                WHERE item_id = ?
                """,
                (item_id,)
            ).fetchone()

            if inventory is None or inventory["stock_quantity"] <= 0:
                return {
                    "success": False,
                    "error": "Replacement item is out of stock."
                }

            # Reserve one unit of stock.
            conn.execute(
                """
                UPDATE inventory
                SET stock_quantity = stock_quantity - 1
                WHERE item_id = ? AND stock_quantity > 0
                """,
                (item_id,)
            )

            # Record the exchange.
            cursor = conn.execute(
                """
                INSERT INTO exchanges (order_id, item_id, status)
                VALUES (?, ?, 'CONFIRMED')
                """,
                (order_id, item_id)
            )

            exchange_id = cursor.lastrowid

            # Update order status.
            conn.execute(
                """
                UPDATE orders
                SET status = 'EXCHANGED'
                WHERE order_id = ?
                """,
                (order_id,)
            )

            return {
                "success": True,
                "exchange_id": exchange_id,
                "order_id": order_id,
                "item_id": item_id,
                "item_name": inventory["item_name"],
                "status": "CONFIRMED",
                "message": "Exchange successfully confirmed."
            }

    except Exception as error:
        return {
            "success": False,
            "error": f"Exchange processing failed: {str(error)}"
        }
