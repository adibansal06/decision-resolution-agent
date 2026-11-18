
from database import get_connection


def check_inventory(item_id: str) -> dict:
    """
    Check the available stock quantity for a product.

    Args:
        item_id: Unique product identifier.

    Returns:
        Stock information and availability status.
    """

    if not isinstance(item_id, str) or not item_id.strip():
        return {
            "success": False,
            "error": "A valid item ID is required."
        }

    try:
        with get_connection() as conn:
            record = conn.execute(
                """
                SELECT item_id, item_name, stock_quantity
                FROM inventory
                WHERE item_id = ?
                """,
                (item_id.strip().upper(),)
            ).fetchone()

        if record is None:
            return {
                "success": False,
                "error": f"Product {item_id} was not found."
            }

        stock = record["stock_quantity"]

        return {
            "success": True,
            "item_id": record["item_id"],
            "item_name": record["item_name"],
            "stock_quantity": stock,
            "available": stock > 0
        }

    except Exception as error:
        return {
            "success": False,
            "error": f"Inventory inspection failed: {str(error)}"
        }
