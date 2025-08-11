from fastapi import APIRouter, HTTPException, status
from app.models.products import products
from app.schemas.product import Product
from app.db.database import database

router = APIRouter()
params = {"id": None, "sku": None}

async def find_product(params: dict):
    if params["id"]:
        query = products.select().where(products.c.id == params["id"])
        return await database.fetch_one(query)
    if params["sku"]:
        query = products.select().where(products.c.sku == params["sku"])
        return await database.fetch_one(query)

@router.get("/products")
async def list_products():
    data = await database.fetch_all(products.select())
    return {"products": data}

@router.post("/products", status_code=status.HTTP_201_CREATED)
async def create_product(product: Product):
    # Check existing product
    params["sku"] = product.sku
    existing_product = await find_product(params)
    if existing_product:
        raise HTTPException(status_code=409, detail="Product already created.")
    
    # Create new product
    query = products.insert().values(sku=product.sku, name=product.name, price=product.price, stock=product.stock)
    id = await database.execute(query)
    
    # Find newly created product
    params["id"] = id
    data = await find_product(params)
    return {"message": "Product created", "product": data}

@router.get("/products/{product_id}")
async def find_product_by_id(product_id: int):
    params["id"] = product_id
    # Find product
    product = await find_product(params)
    if not product:
        raise HTTPException(status_code=404, detail=f"Product not found with id:{product_id}.")
    return {"product": product}

@router.put("/products/{product_id}")
async def update_product(product_id: int, payload: Product):
    # Find product
    params["id"] = product_id
    product = await find_product()
    if not product:
        raise HTTPException(status_code=404, detail=f"Product not found with id:{product_id}.")
    
    query = (
        products.update()
        .where(products.c.id == product_id)
        .values(
            sku=payload.sku,
            name=payload.name,
            price=payload.price,
            stock=payload.stock
        )
    )
    await database.execute(query)
    
    # Fetch updated product details
    params["id"] = product_id
    updated_product = await find_product(params)
    return {"message": "Product details update successfully", "product": updated_product}

@router.delete("/products/{product_id}")
async def delete_product(product_id: int):
    # Find product
    query = products.select().where(products.c.id == product_id)
    product = await database.fetch_one(query)
    if not product:
        raise HTTPException(status_code=404, detail=f"Product not found with id:{product_id}.")
    
    # Delete product
    query = products.delete().where(products.c.id == product_id)
    await database.execute(query)
    return {"message": "Product deleted successfully"}
