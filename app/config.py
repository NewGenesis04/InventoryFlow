import os
import logging
import json
from datetime import datetime, timezone
from dotenv import load_dotenv
from logging.config import dictConfig

load_dotenv()


class JsonFormatter(logging.Formatter):
    """Custom JSON formatter for structured logging."""
    
    def format(self, record: logging.LogRecord) -> str:
        
        log_data = {
            "timestamp": datetime.fromtimestamp(record.created, tz=timezone.utc).isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.name,
            "line": record.lineno,
        }
        
        # Add exception info if present
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)
        
        # Add extra fields if present
        if hasattr(record, "extra_fields"):
            log_data.update(record.extra_fields)
        
        return json.dumps(log_data)


class Settings:
    PROJECT_NAME: str = "InventoryFlow API"
    PROJECT_VERSION: str = "0.0.1"
    PROJECT_DESCRIPTION: str = "InventoryFlow is a blazing-fast, API-first inventory management system that helps you organize stock, manage orders, and automate communication across your supply chain — all with clean code and a modular design."

    DATABASE_URL= os.getenv("DB_URL")
    JWT_SECRET_KEY= os.getenv("JWT_SECRET_KEY")
    JWT_ALGORITHM= os.getenv("JWT_ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES= os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 5)

class LoggingSettings:
    @staticmethod
    def setup_logging():
        logging_config = {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "json": {
                    "()": "app.config.JsonFormatter",
                },
            },
            "handlers": {
                "console": {
                    "class": "rich.logging.RichHandler",
                    "rich_tracebacks": True,
                    "show_time": True,
                    "show_path": False,
                    "markup": True,
                },
                "file": {
                    "class": "logging.handlers.RotatingFileHandler",
                    "formatter": "json",
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