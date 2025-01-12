import itertools
import logging
from argparse import Namespace
from pathlib import Path

from rich import print
from rich.traceback import install

from core_helpers.cli import ArgparseColorThemes, setup_parser
from core_helpers.logs import setup_logger
from core_helpers.rich_print import print_error_message
from core_helpers.updates import check_updates
from core_helpers.utils import print_welcome
from core_helpers.xdg_paths import APP_DIRS, HOME_DIRS, get_user_path

from app.config import AppConfig  # type: ignore
from app.custom_logs import logger  # type: ignore

try:
    from importlib import metadata
except ImportError:  # for Python < 3.8
    import importlib_metadata as metadata  # type: ignore


def create_logger(package, log_file, debug, use_loguru) -> None:
    print(
        f"Creating logger with package={package}, log_file={log_file}, debug={debug}, use_loguru={use_loguru}..."
    )
    logger = setup_logger(
        package=package,
        log_file=log_file,
        debug=debug,
        use_loguru=use_loguru,
        no_cache=True,
    )

    logger_level = logger.level if isinstance(logger, logging.Logger) else None
    print("Logger level:", logger_level)
    logger_handlers = logger.handlers if hasattr(logger, "handlers") else None
    print("Logger handlers:", logger_handlers)

    # Now you can use the logger
    logger.info("Hello, world!")
    logger.debug("This is a debug message.")
    logger.error("This is an error message.")
    logger.warning("This is a warning message.")

    del logger

    print()


def test_logger() -> None:
    package = "MyApp"
    log_file = "myapp.log"

    for bool1, bool2 in itertools.product([True, False], repeat=2):
        create_logger(package, log_file, bool1, bool2)


def test_parser() -> None:
    parser, g_main = setup_parser(
        "MyApp",
        "MyApp description",
        "1.0.0",
        theme=ArgparseColorThemes.LILAC,
    )

    g_main.add_argument(
        "-f",
        "--file",
        dest="file",
        type=str,
        required=True,
        help="The file to process.",
    )

    args: Namespace = parser.parse_args()

    parser.print_help()


def test_updates() -> None:
    urls: list[str] = [
        "https://github.com/vuejs/vue",
        "https://github.com/Jules-WinnfieldX/CyberDropDownloader",
        "https://gitlab.com/TheEvilSkeleton/Upscaler",
        "https://codeberg.org/forgejo/forgejo",
        "https://gitea.com//docker/metadata-action",
        "https://gitea.angry.im/PeterCxy/OpenEUICC",
        "https://git.cryto.net/joepie91/box",
        "https://gitee.com/LongbowEnterprise/BootstrapBlazor",
        "https://gitee.com/cxasm/notepad--",
    ]

    for url in urls:
        print(f"Checking updates for {url}...")
        check_updates(url, "0.0.1")
        print()


def test_xdg_paths() -> None:
    for path_type in APP_DIRS:
        path: Path = get_user_path(__package__, path_type)
        print(f"{path_type}: {path}")
    for path_type in HOME_DIRS:
        path = get_user_path(__package__, path_type)
        print(f"{path_type}: {path}")


def main() -> None:
    install(show_locals=False)

    __package__: str = "core_helpers"

    version: str = metadata.version(__package__)
    desc: str = metadata.metadata(__package__)["Summary"]
    repo: str = metadata.metadata(__package__)["Home-page"]

    print_welcome(__package__, version, desc, repo, random_font=True)

    LOG_PATH = (
        "C:\\Users\\yisus_christ\\AppData\\Local\\iltransfer\\iltransfer\\iltransfer.ini"
    )

    msg = (
        "There were errors during the execution of the script. "
        f"Check the logs at '{LOG_PATH}' for more information."
    )

    print(f"[red]ERROR[/]: {msg}")
    print()
    print_error_message(msg)

    return

    test_parser()
    test_logger()
    test_updates()
    test_xdg_paths()


def test_app() -> None:
    # Step 1: Setup the parser
    parser, _ = setup_parser(
        AppConfig.PACKAGE,
        "test description",  # AppConfig.desc(),
        "0.0.1",  # AppConfig.version(),
    )

    # Step 2: Parse the arguments
    args: Namespace = parser.parse_args()

    # Step 3: Update AppConfig.DEBUG based on parsed arguments
    if args.debug:
        AppConfig.DEBUG = True

    # Step 4: Proceed with the rest of the program (e.g., setting up logging)
    # Now the AppConfig.DEBUG has been updated before setting up the logger
    logger.info("Logger is set up.")


if __name__ == "__main__":
    test_app()
