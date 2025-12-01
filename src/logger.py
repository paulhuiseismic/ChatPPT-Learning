from loguru import logger
import sys
import logging


log_format = "{time:YYYY-MM-DD HH:mm:ss} | {level} | {module}:{function}:{line} - {message}"

logger.remove()

logger.add(sys.stdout, level="DEBUG", format=log_format, colorize=True)
logger.add(sys.stderr, level="ERROR", format=log_format, colorize=True)

logger.add("logs/app.log", rotation="1 MB", level="DEBUG", format=log_format)

LOG = logger

__all__ = ["LOG"]