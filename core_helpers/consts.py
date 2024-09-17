"""Constants for the core_helpers package."""

from pathlib import Path

from core_helpers.xdg_paths import get_user_path

try:
    from importlib import metadata
except ImportError:  # for Python < 3.8
    import importlib_metadata as metadata  # type: ignore


class BaseConfig:
    PACKAGE = "default_package"  # Can be overridden by subclasses

    CONFIG_PATH: Path = get_user_path(PACKAGE, "config")
    LOG_PATH: Path = get_user_path(PACKAGE, "log")

    EXIT_SUCCESS = 0
    EXIT_FAILURE = 1

    DEBUG = False
    PROFILE = False

    @classmethod
    def log_file(cls) -> Path:
        return cls.LOG_PATH / f"{cls.PACKAGE}.log"

    @classmethod
    def version(cls) -> str:
        return metadata.version(cls.PACKAGE or __name__)

    @classmethod
    def author(cls) -> str:
        return metadata.metadata(cls.PACKAGE or __name__)["Author"]

    @classmethod
    def desc(cls) -> str:
        return metadata.metadata(cls.PACKAGE or __name__)["Summary"]

    @classmethod
    def repo(cls) -> str:
        return metadata.metadata(cls.PACKAGE or __name__)["Home-page"]
