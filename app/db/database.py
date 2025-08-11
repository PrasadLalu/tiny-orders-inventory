from databases import Database
from sqlalchemy import MetaData
from sqlalchemy import create_engine

DATABASE_URL = "sqlite:///./inventory.db"

database = Database(DATABASE_URL)
metadata = MetaData()
engine = create_engine(DATABASE_URL)
