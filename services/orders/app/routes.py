from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db import get_db
from app.crud import create_order, get_order, get_all_orders, update_order, delete_order
from app.schemas.orders import OrderCreate, OrderUpdate, OrderResponse

router = APIRouter()

@router.post("/orders", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
async def create_order_route(request: OrderCreate, db: AsyncSession = Depends(get_db)):
    return await create_order(db, request.user_id, request.total_price, request.status)

@router.get("/orders/{order_id}", response_model=OrderResponse)
async def get_order_route(order_id: int, db: AsyncSession = Depends(get_db)):
    order = await get_order(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@router.get("/orders", response_model=list[OrderResponse])
async def get_all_orders_route(db: AsyncSession = Depends(get_db)):
    return await get_all_orders(db)

@router.put("/orders/{order_id}", response_model=OrderResponse)
async def update_order_route(order_id: int, request: OrderUpdate, db: AsyncSession = Depends(get_db)):
    order = await get_order(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return await update_order(db, order, request.status or order.status, request.total_price or order.total_price)

@router.delete("/orders/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_order_route(order_id: int, db: AsyncSession = Depends(get_db)):
    order = await get_order(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    await delete_order(db, order)
    return None
