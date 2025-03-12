import logging
import logging.config
import os

# Configure logging with dynamic settings
def configure_logging(log_level=None):
    os.makedirs("logs", exist_ok=True)  # Ensure the logs directory exists

    # Load environment variables for logging configuration if not explicitly passed
    log_level = log_level or os.getenv("LOG_LEVEL", "INFO").upper()  # Default to INFO if not set
    log_file = os.getenv("LOG_FILE", "logs/application.log")  # Default log file location
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    # Configure logging settings
    logging_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "standard": {
                "format": log_format
            }
        },
        "handlers": {
            "console": {
                "level": log_level,
                "class": "logging.StreamHandler",
                "formatter": "standard",
                "stream": "ext://sys.stdout"
            },
            "file": {
                "level": log_level,
                "class": "logging.FileHandler",
                "formatter": "standard",
                "filename": log_file,
                "mode": "a"
            }
        },
        "root": {
            "level": log_level,
            "handlers": ["console", "file"]
        }
    }

    # Apply logging configuration
    logging.config.dictConfig(logging_config)