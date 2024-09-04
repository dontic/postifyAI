import logging
import os
import sys

# Get the LOGGING_DEBUG from the .env file
from dotenv import load_dotenv

load_dotenv()


def setup_logger(name: str) -> logging.Logger:
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(
        logging.DEBUG if os.getenv("LOGGING_DEBUG") == "True" else logging.INFO
    )

    # Create console handler and set level to debug
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.DEBUG)

    # Create formatter
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    # Add formatter to console handler
    console_handler.setFormatter(formatter)

    # Add console handler to logger
    logger.addHandler(console_handler)

    # Prevent the log messages from being duplicated in the root logger
    logger.propagate = False

    return logger


# Usage examples:
# logger = setup_logger(__name__)
# logger.debug("This is a debug message")
# logger.info("This is an info message")
# logger.warning("This is a warning message")
# logger.error("This is an error message")
# logger.critical("This is a critical message")
