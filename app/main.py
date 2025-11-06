from fastapi import FastAPI, Depends, HTTPException
from app.config import settings, logging_settings
import logging
from app.middleware.cors import add_cors_middleware
from app.routers.incoming_orders.incoming_orders import router as incoming_orders_router
from app.routers.outgoing_orders.outgoing_orders import router as outgoing_orders_router
from app.routers.stock.stock import router as stock_router
from app.routers.category.category import router as category_router
from app.routers.products.products import router as products_router
from app.auth.auth_route import router as auth_router
from app.db.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text


setup_logging = logging_settings.setup_logging

try:
    setup_logging() #I initialised the logging configuration in config.py here. This ensures that all loggers in the app follow the pattern
    logger = logging.getLogger(__name__)
    logger.info("FastAPI application is starting...")
except Exception as e:
    print(f"Failed to set up logging: {e}")
    logger.error(f"Failed to set up logging: {e}")
    raise

app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION, description=settings.PROJECT_DESCRIPTION)

app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(category_router, prefix="/categories", tags=["Category"])
app.include_router(products_router, prefix="/products",tags=["Product"])
app.include_router(stock_router, prefix="/stocks", tags=["Stock"])
app.include_router(incoming_orders_router, prefix="/incoming",tags=["Incoming Orders"])
app.include_router(outgoing_orders_router, prefix="/outgoing",tags=["Outgoing Orders"])


add_cors_middleware(app)

@app.get("/")
async def root(db: AsyncSession = Depends(get_db)):
    try:

        logger.info("Root endpoint accessed")
        await db.execute(text("SELECT 1"))  # Simple query to check DB connection
        logger.info("Database health check successful")
        return {"message": "This is the root endpoint of the InventoryFlow API",
                "status": "healthy",
                "database": "connected"}
    except Exception as e:
        logger.error(f"Database health check failed: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Database health check failed: {str(e)}"
        )