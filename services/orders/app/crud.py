from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models import Order

async def create_order(db: AsyncSession, user_id: int, total_price: float, status: str = "pending"):
    new_order = Order(user_id=user_id, total_price=total_price, status=status)
    db.add(new_order)
    await db.commit()
    await db.refresh(new_order)
    return new_order

async def get_order(db: AsyncSession, order_id: int):
    result = await db.execute(select(Order).where(Order.id == order_id))
    return result.scalar_one_or_none()

async def get_all_orders(db: AsyncSession):
    result = await db.execute(select(Order))
    return result.scalars().all()

async def update_order(db: AsyncSession, order: Order, status: str, total_price: float):
    if status:
        order.status = status
    if total_price:
        order.total_price = total_price
    await db.commit()
    await db.refresh(order)
    return order

async def delete_order(db: AsyncSession, order: Order):
    await db.delete(order)
    await db.commit()
    return order
