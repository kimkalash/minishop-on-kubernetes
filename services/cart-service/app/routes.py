# app/routes.py

from fastapi import APIRouter, Depends, HTTPException, status
from aioredis import Redis
from typing import List

from app.schemas import CartItemCreate, CartItemResponse, CartResponse
from app.crud import get_cart, add_item, remove_item, clear_cart
from app.db import get_redis

router = APIRouter()


@router.post("/cart/items", status_code=status.HTTP_201_CREATED)
async def add_item_to_cart(
    item: CartItemCreate,
    redis: Redis = Depends(get_redis),
    user_id: int = 1  # Placeholder user ID, replace with auth later
):
    """
    Add an item to the user's cart.
    """
    await add_item(redis, user_id, item)
    return {"message": "Item added to cart"}


@router.get("/cart", response_model=CartResponse)
async def get_user_cart(
    redis: Redis = Depends(get_redis),
    user_id: int = 1  # Placeholder user ID
):
    """
    Retrieve the user's cart with all items.
    """
    items = await get_cart(redis, user_id)
    total_items = sum(item.quantity for item in items)
    total_price = sum((item.price or 0) * item.quantity for item in items)
    return CartResponse(items=items, total_items=total_items, total_price=total_price)


@router.delete("/cart/items/{product_id}")
async def remove_item_from_cart(
    product_id: int,
    redis: Redis = Depends(get_redis),
    user_id: int = 1  # Placeholder user ID
):
    """
    Remove a specific item from the user's cart.
    """
    removed = await remove_item(redis, user_id, product_id)
    if not removed:
        raise HTTPException(status_code=404, detail="Item not found in cart")
    return {"message": "Item removed from cart"}


@router.delete("/cart")
async def clear_user_cart(
    redis: Redis = Depends(get_redis),
    user_id: int = 1  # Placeholder user ID
):
    """
    Clear all items from the user's cart.
    """
    await clear_cart(redis, user_id)
    return {"message": "Cart cleared"}
