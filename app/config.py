import os
from dotenv import load_dotenv
from pathlib import Path
from logging.config import dictConfig

load_dotenv()

class Settings:
    PROJECT_NAME: str = "InventoryFlow API"
    PROJECT_VERSION: str = "0.0.1"
    PROJECT_DESCRIPTION: str = "InventoryFlow is a blazing-fast, API-first inventory management system that helps you organize stock, manage orders, and automate communication across your supply chain — all with clean code and a modular design."

    DATABASE_URL= os.getenv("DATABASE_URL")
    JWT_SECRET_KEY= os.getenv("JWT_SECRET_KEY", "def_jwt_secret_key_!(#)")
    JWT_ALGORITHM= os.getenv("JWT_ALGORITHM", "HS256")

class LoggingSettings:
    @staticmethod
    def setup_logging():
        logging_config = {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "default": {
                    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                },
            },
            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                    "formatter": "default",
                },
                "file": {
                    "class": "logging.handlers.RotatingFileHandler",
                    "formatter": "default",
                    "filename": "app.log",
                    "maxBytes": 10485760,  # 10 MB
                    "backupCount": 5,     # Keep 5 backup files
                },
            },
            "root": {
                "level": "INFO",
                "handlers": ["console", "file"],
            },
        }
        dictConfig(logging_config)

settings = Settings()
logging_settings = LoggingSettings()