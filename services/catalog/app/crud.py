from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models import Product

# 1️⃣ Create a new product
async def create_product(db: AsyncSession, name: str, description: str, price: float, stock: int):
    product = Product(name=name, description=description, price=price, stock=stock)
    db.add(product)
    await db.commit()
    await db.refresh(product)  # Refresh to get DB-generated fields like id
    return product


# 2️⃣ Get a product by ID
async def get_product(db: AsyncSession, product_id: int):
    result = await db.execute(select(Product).where(Product.id == product_id))
    return result.scalar_one_or_none()


# 3️⃣ Get all products
async def get_all_products(db: AsyncSession):
    result = await db.execute(select(Product))
    return result.scalars().all()


# 4️⃣ Update a product
async def update_product(db: AsyncSession, product: Product, name: str, description: str, price: float, stock: int):
    product.name = name
    product.description = description
    product.price = price
    product.stock = stock
    db.add(product)
    await db.commit()
