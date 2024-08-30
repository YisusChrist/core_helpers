"""Logging configuration."""

import logging

import loguru
from loguru import logger as loguru_logger

# Cache the logger instance
_cached_logger: logging.Logger | loguru._Logger = None  # type: ignore


def setup_logger(
    package: str, log_file: str, debug: bool = False, use_loguru: bool = False
) -> logging.Logger | loguru._Logger:  # type: ignore
    """
    Set up and return a configured logger instance using either `logging` or `loguru`.

    Args:
        package (str): The name of the package or project.
        log_file (str): The path to the log file.
        debug (bool): Whether to enable debug-level logging.
        use_loguru (bool): Whether to use `loguru` instead of the standard `logging` module.

    Returns:
        Optional[logging.Logger]: The configured logger instance (only if using `logging`).
    """
    global _cached_logger

    if _cached_logger is not None:
        return _cached_logger

    if use_loguru:
        # Loguru configuration
        loguru_logger.remove()  # Remove default configuration
        loguru_log_level: str = "DEBUG" if debug else "INFO"

        # Configure Loguru to log to file
        loguru_logger.add(
            log_file, level=loguru_log_level, format="{time} {level} {message}"
        )

        # Configure Loguru to log to console
        loguru_logger.add(
            lambda msg: print(msg, end=""), level=loguru_log_level, colorize=True
        )

        _cached_logger = loguru_logger
        return loguru_logger

    else:
        # Standard logging configuration
        logger: logging.Logger = logging.getLogger(name=package)

        if not logger.hasHandlers():  # Prevent adding handlers multiple times
            # Define log handlers
            log_handlers: list[logging.FileHandler] = [
                logging.FileHandler(filename=log_file)
            ]

            # Set the log level and message format
            log_level: int = logging.DEBUG if debug else logging.INFO
            log_format = "[%(asctime)s] %(levelname)s: %(message)s"

            # If in debug mode, include additional information
            if debug:
                log_format += ": %(pathname)s:%(lineno)d in %(funcName)s"

            # Configure the logging system
            logging.basicConfig(
                level=log_level,
                format=log_format,
                handlers=log_handlers,
            )

        _cached_logger = logger
        return logger
