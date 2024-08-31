import logging
from pathlib import Path
from typing import Generator

import loguru
import pytest
from typeguard import TypeCheckError

from core_helpers.logs import setup_logger

PACKAGE = "MyApp"


@pytest.fixture
def temp_log_file() -> Generator[Path, None, None]:
    # Create a temporary log file
    log_file = Path("temp_test_log.log")
    yield log_file
    # if log_file.exists():
    #    log_file.unlink()  # This safely removes the file after the test


def test_setup_logger_standard(temp_log_file: Path) -> None:
    logger = setup_logger(
        PACKAGE, temp_log_file, debug=True, use_loguru=False, no_cache=True
    )
    assert isinstance(logger, logging.Logger)

    logger.info("Testing standard logger")
    assert temp_log_file.exists()


def test_setup_logger_loguru(temp_log_file: Path) -> None:
    logger = setup_logger(
        PACKAGE, temp_log_file, debug=True, use_loguru=True, no_cache=True
    )
    assert isinstance(logger, loguru._Logger)  # type: ignore

    logger.info("Testing Loguru logger")
    assert temp_log_file.exists()


def test_setup_logger_cached_instance(temp_log_file: Path) -> None:
    # First logger instance
    logger1 = setup_logger(
        PACKAGE, temp_log_file, debug=True, use_loguru=False, no_cache=False
    )
    # Cached instance should be returned
    logger2 = setup_logger(
        PACKAGE, temp_log_file, debug=True, use_loguru=False, no_cache=False
    )

    assert logger1 is logger2  # Check if the cached instance is reused


def test_setup_logger_no_cache(temp_log_file: Path) -> None:
    logger1 = setup_logger(
        PACKAGE, temp_log_file, debug=True, use_loguru=False, no_cache=True
    )
    logger2 = setup_logger(
        PACKAGE, temp_log_file, debug=True, use_loguru=False, no_cache=True
    )

    assert logger1 is not logger2  # Ensure no_cache=True forces a new instance


def test_setup_logger_invalid_PACKAGE_name(temp_log_file: Path) -> None:
    with pytest.raises(TypeCheckError):
        setup_logger(
            None,  # type: ignore
            temp_log_file,
            debug=True,
            use_loguru=False,
            no_cache=True,
        )


def test_setup_logger_invalid_log_file_type() -> None:
    with pytest.raises(TypeCheckError):
        setup_logger(
            PACKAGE,
            12345,  # type: ignore
            debug=True,
            use_loguru=False,
            no_cache=True,
        )


def test_setup_logger_invalid_debug_type(temp_log_file: Path) -> None:
    with pytest.raises(TypeCheckError):
        setup_logger(
            PACKAGE,
            temp_log_file,
            debug="not_a_bool",  # type: ignore
            use_loguru=False,
            no_cache=True,
        )


def test_setup_logger_invalid_use_loguru_type(temp_log_file: Path) -> None:
    with pytest.raises(TypeCheckError):
        setup_logger(
            PACKAGE,
            temp_log_file,
            debug=True,
            use_loguru=[],  # type: ignore
            no_cache=True,
        )


def test_setup_logger_invalid_no_cache_type(temp_log_file: Path) -> None:
    with pytest.raises(TypeCheckError):
        setup_logger(
            PACKAGE,
            temp_log_file,
            debug=True,
            use_loguru=False,
            no_cache="invalid",  # type: ignore
        )


def test_setup_logger_no_handlers(temp_log_file: Path) -> None:
    logger = setup_logger(
        PACKAGE, temp_log_file, debug=False, use_loguru=False, no_cache=True
    )
    assert isinstance(logger, logging.Logger)

    # logger.handlers.clear()  # Manually clear handlers

    logger = setup_logger(
        PACKAGE, temp_log_file, debug=False, use_loguru=False, no_cache=True
    )
    assert len(logger.handlers) == 1  # Ensure handler is re-added


def test_setup_logger_loguru_reconfiguration(temp_log_file: Path) -> None:
    logger = setup_logger(
        PACKAGE, temp_log_file, debug=True, use_loguru=True, no_cache=True
    )
    logger.info("First configuration")

    # Reconfigure Loguru logger with a different setting
    logger = setup_logger(
        PACKAGE, temp_log_file, debug=False, use_loguru=True, no_cache=True
    )
    logger.info("Second configuration")

    assert temp_log_file.exists()

    with temp_log_file.open("r") as f:
        log_content: str = f.read()
        assert "First configuration" in log_content
        assert "Second configuration" in log_content
