from contextlib import asynccontextmanager
from fastapi import FastAPI
from config import settings, logging_settings
from dotenv import load_dotenv
from pathlib import Path
import os
import logging
from middleware.cors import add_cors_middleware

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

add_cors_middleware(app)

@app.get("/")
async def root():
    logger.info("Root endpoint accessed")
    return {"message": "This is the root endpoint of the InventoryFlow API"}

