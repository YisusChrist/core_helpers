"""Logging configuration."""

from logging import Logger

from core_helpers.logs import setup_logger
from .config import AppConfig  # type: ignore

# Automatically sets up and returns the cached logger instance
logger: Logger = setup_logger(
    AppConfig.PACKAGE,
    AppConfig.log_file(),
    AppConfig.DEBUG,
)
