from app.db.database import metadata
from sqlalchemy import Table, Column, Integer, String, Numeric

products = Table(
    'products',
    metadata,
    Column("id", Integer, primary_key=True),
    Column("sku", String(50), unique=True, nullable=False, index=True),
    Column("name", String(200), nullable=False),
    Column("price", Numeric(10, 2), nullable=False),
    Column("stock", Integer, nullable=False) 
)
