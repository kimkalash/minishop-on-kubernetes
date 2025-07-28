from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models import Product

# ✅ Create
async def create_product(db: AsyncSession, name: str, description: str, price: float, stock: int):
    new_product = Product(name=name, description=description, price=price, stock=stock)
    db.add(new_product)
    await db.commit()
    await db.refresh(new_product)
    return new_product

# ✅ Read (Single Product)
async def get_product(db: AsyncSession, product_id: int):
    result = await db.execute(select(Product).where(Product.id == product_id))
    return result.scalar_one_or_none()

# ✅ Read (All Products)
async def get_all_products(db: AsyncSession):
    result = await db.execute(select(Product))
    return result.scalars().all()

# ✅ Update
async def update_product(db: AsyncSession, product: Product, name: str, description: str, price: float, stock: int):
    product.name = name
    product.description = description
    product.price = price
    product.stock = stock
    await db.commit()
    await db.refresh(product)
    return product

# ✅ Delete
async def delete_product(db: AsyncSession, product: Product):
    await db.delete(product)
    await db.commit()
    return product

