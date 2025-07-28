from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db import get_db
from app.crud import (
    create_product,
    get_product,
    get_all_products,
    update_product,
    delete_product
)
from app.schemas.catalog import ProductCreate, ProductUpdate, ProductResponse

router = APIRouter()

# 1️⃣ Create a product
@router.post("/products", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
async def create_product_route(request: ProductCreate, db: AsyncSession = Depends(get_db)):
    return await create_product(db, request.name, request.description, request.price, request.stock)


# 2️⃣ Get a product by ID
@router.get("/products/{product_id}", response_model=ProductResponse)
async def get_product_route(product_id: int, db: AsyncSession = Depends(get_db)):
    product = await get_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


# 3️⃣ Get all products
@router.get("/products", response_model=list[ProductResponse])
async def get_all_products_route(db: AsyncSession = Depends(get_db)):
    return await get_all_products(db)


# 4️⃣ Update a product
@router.put("/products/{product_id}", response_model=ProductResponse)
async def update_product_route(product_id: int, request: ProductUpdate, db: AsyncSession = Depends(get_db)):
    product = await get_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    # Update fields, use existing values if not provided
    updated_product = await update_product(
        db,
        product,
        name=request.name or product.name,
        description=request.description or product.description,
        price=request.price or product.price,
        stock=request.stock if request.stock is not None else product.stock
    )
    return updated_product


# 5️⃣ Delete a product
@router.delete("/products/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product_route(product_id: int, db: AsyncSession = Depends(get_db)):
    product = await get_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    await delete_product(db, product)
    return None

