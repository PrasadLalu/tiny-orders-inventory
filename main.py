from fastapi import FastAPI, APIRouter
from app.db.database import engine, database, metadata
from app.api.product import router as product_router

# Create tables
metadata.create_all(engine)

# Initialize app
app = FastAPI()

@app.on_event("startup")
async def startup():
    await database.connect()
    
@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

# API router prifix
api_router = APIRouter(prefix="/api/v1")

@api_router.get("/health-check")
def health_check():
    return {"message": "Healthy..."}

# Include routes
api_router.include_router(product_router, tags=["Products"])

app.include_router(api_router)
