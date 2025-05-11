from contextlib import asynccontextmanager
from fastapi import FastAPI
from config import settings, logging_settings
from dotenv import load_dotenv
from pathlib import Path
import os
import logging
from db.database import init_db
from middleware.cors import add_cors_middleware

@asynccontextmanager
async def life_span(app: FastAPI):
    """
    Lifecycle event handler for the FastAPI application.

    This asynchronous function is called when the FastAPI application starts up
    and shuts down. It initializes the database on startup and performs cleanup
    on shutdown.

    Args:
        app (FastAPI): The FastAPI application instance.

    Yields:
        None: This function yields control back to the application after startup.
    """
    # Startup: Initialize the database
    print(f"server is starting")
    await init_db()
    
    yield  # Yield control back to FastAPI
    
    # Shutdown: Perform any necessary cleanup
    print(f"server is ending")


setup_logging = logging_settings.setup_logging
try:
    setup_logging()
    logger = logging.getLogger(__name__)
    logger.info("FastAPI application is starting...")
except Exception as e:
    print(f"Failed to set up logging: {e}")
    logger.error(f"Failed to set up logging: {e}")
    raise

app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION, description=settings.PROJECT_DESCRIPTION, lifespan=life_span)

add_cors_middleware(app)

@app.get("/")
async def root():
    logger.info("Root endpoint accessed")
    return {"message": "This is the root endpoint of the InventoryFlow API"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)