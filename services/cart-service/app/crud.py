# app/crud.py
from typing import List, Optional
import json
from redis.asyncio import Redis
from app.schemas import CartItemCreate, CartItemResponse

CART_PREFIX = "cart:"  # Redis key prefix for carts


def _cart_key(user_id: int) -> str:
    """Helper to build Redis key for a user's cart."""
    return f"{CART_PREFIX}{user_id}"


async def get_cart(redis: Redis, user_id: int) -> List[CartItemResponse]:
    """
    Retrieve the cart items for a user from Redis.
    Returns a list of CartItemResponse objects.
    """
    key = _cart_key(user_id)
    cart_data = await redis.get(key)
    if not cart_data:
        return []
    # cart_data stored as JSON string, parse it
    items_dict = json.loads(cart_data)
    return [CartItemResponse(**item) for item in items_dict]


async def add_item(redis: Redis, user_id: int, item: CartItemCreate) -> None:
    """
    Add or update an item in the user's cart.
    If item exists, increments quantity.
    """
    key = _cart_key(user_id)
    cart_data = await redis.get(key)
    items = []
    if cart_data:
        items = json.loads(cart_data)

    # Check if product already in cart
    for existing_item in items:
        if existing_item["product_id"] == item.product_id:
            existing_item["quantity"] += item.quantity
            break
    else:
        # Item not found, add new
        items.append(item.dict())

    await redis.set(key, json.dumps(items))


async def remove_item(redis: Redis, user_id: int, product_id: int) -> bool:
    """
    Remove an item from the cart.
    Returns True if item was removed, False if not found.
    """
    key = _cart_key(user_id)
    cart_data = await redis.get(key)
    if not cart_data:
        return False

    items = json.loads(cart_data)
    new_items = [item for item in items if item["product_id"] != product_id]

    if len(new_items) == len(items):
        return False  # item not found

    await redis.set(key, json.dumps(new_items))
    return True


async def clear_cart(redis: Redis, user_id: int) -> None:
    """Remove all items from user's cart."""
    key = _cart_key(user_id)
    await redis.delete(key)
