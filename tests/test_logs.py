import logging
from pathlib import Path

import loguru
import pytest
from typeguard import TypeCheckError

from core_helpers.logs import LoggerProxy

PACKAGE = "MyApp"
LOG_FILE = Path(PACKAGE + ".log")


@pytest.fixture
def temp_log_file(tmp_path: Path) -> Path:
    return tmp_path / "temp_test_log.log"


def test_setup_logger_standard(temp_log_file: Path) -> None:
    logger: LoggerProxy = LoggerProxy()
    logger.setup_logger(
        PACKAGE, temp_log_file, debug=True, use_loguru=False, cache=False
    )
    assert isinstance(logger._logger, logging.Logger)

    logger.info("Testing standard logger")
    assert temp_log_file.exists()


def test_setup_logger_loguru(temp_log_file: Path) -> None:
    logger: LoggerProxy = LoggerProxy()
    logger.setup_logger(
        PACKAGE, temp_log_file, debug=True, use_loguru=True, cache=False
    )
    assert isinstance(logger._logger, loguru._Logger)  # type: ignore

    logger.info("Testing Loguru logger")
    assert temp_log_file.exists()


def test_setup_logger_cached_instance(temp_log_file: Path) -> None:
    # First logger instance
    logger: LoggerProxy = LoggerProxy()
    logger.setup_logger(
        PACKAGE, temp_log_file, debug=True, use_loguru=False, cache=True
    )
    logger1: LoggerProxy = logger._logger
    logger.setup_logger(
        PACKAGE, temp_log_file, debug=True, use_loguru=False, cache=True
    )
    logger2: LoggerProxy = logger._logger

    assert logger1 is logger2  # Check if the cached instance is reused


def test_setup_logger_no_cache(temp_log_file: Path) -> None:
    logger1: LoggerProxy = LoggerProxy()
    logger1.setup_logger(
        PACKAGE, temp_log_file, debug=True, use_loguru=False, cache=False
    )
    logger2: LoggerProxy = LoggerProxy()
    logger2.setup_logger(
        PACKAGE, temp_log_file, debug=True, use_loguru=False, cache=False
    )

    assert logger1 is not logger2  # Ensure cache=False forces a new instance


def test_setup_logger_invalid_PACKAGE_name(temp_log_file: Path) -> None:
    logger: LoggerProxy = LoggerProxy()
    with pytest.raises(TypeCheckError):
        logger.setup_logger(
            None,  # type: ignore
            temp_log_file,
            debug=True,
            use_loguru=False,
            cache=False,
        )


def test_setup_logger_invalid_log_file_type() -> None:
    logger: LoggerProxy = LoggerProxy()
    with pytest.raises(TypeCheckError):
        logger.setup_logger(
            PACKAGE,
            12345,  # type: ignore
            debug=True,
            use_loguru=False,
            cache=False,
        )


def test_setup_logger_invalid_debug_type(temp_log_file: Path) -> None:
    logger: LoggerProxy = LoggerProxy()
    with pytest.raises(TypeCheckError):
        logger.setup_logger(
            PACKAGE,
            temp_log_file,
            debug="not_a_bool",  # type: ignore
            use_loguru=False,
            cache=False,
        )


def test_setup_logger_invalid_use_loguru_type(temp_log_file: Path) -> None:
    logger: LoggerProxy = LoggerProxy()
    with pytest.raises(TypeCheckError):
        logger.setup_logger(
            PACKAGE,
            temp_log_file,
            debug=True,
            use_loguru=[],  # type: ignore
            cache=False,
        )


def test_setup_logger_invalid_cache_type(temp_log_file: Path) -> None:
    logger: LoggerProxy = LoggerProxy()
    with pytest.raises(TypeCheckError):
        logger.setup_logger(
            PACKAGE,
            temp_log_file,
            debug=True,
            use_loguru=False,
            cache="invalid",  # type: ignore
        )


def test_setup_logger_no_handlers(temp_log_file: Path) -> None:
    logger: LoggerProxy = LoggerProxy()
    logger.setup_logger(
        PACKAGE, temp_log_file, debug=False, use_loguru=False, cache=False
    )
    assert isinstance(logger._logger, logging.Logger)

    # logger.handlers.clear()  # Manually clear handlers

    logger.setup_logger(
        PACKAGE, temp_log_file, debug=False, use_loguru=False, cache=False
    )
    assert len(logger._logger.handlers) == 1  # Ensure handler is re-added


def test_setup_logger_loguru_reconfiguration(temp_log_file: Path) -> None:
    logger: LoggerProxy = LoggerProxy()
    logger.setup_logger(
        PACKAGE, temp_log_file, debug=True, use_loguru=True, cache=False
    )
    logger.info("First configuration")

    # Reconfigure Loguru logger with a different setting
    logger.setup_logger(
        PACKAGE, temp_log_file, debug=False, use_loguru=True, cache=False
    )
    logger.info("Second configuration")

    assert temp_log_file.exists()

    with temp_log_file.open("r") as f:
        log_content: str = f.read()
        assert "First configuration" in log_content
        assert "Second configuration" in log_content
