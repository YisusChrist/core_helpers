import itertools
import logging
from argparse import Namespace

from rich import print
from rich.traceback import install

from core_helpers.cli import ArgparseColorThemes, setup_parser
from core_helpers.logs import setup_logger
from core_helpers.updates import check_updates
from core_helpers.utils import print_welcome

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

    create_logger(package, log_file, True, False)
    create_logger(package, log_file, False, False)

    return

    for bool1, bool2 in itertools.product([True, False], repeat=2):
        create_logger(package, log_file, bool1, bool2)


def test_parser() -> Namespace:
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

    return args


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


def main() -> None:
    install(show_locals=False)

    __package__: str = "core_helpers"

    version: str = metadata.version(__package__)
    desc: str = metadata.metadata(__package__)["Summary"]
    repo: str = metadata.metadata(__package__)["Home-page"]

    print_welcome(__package__, version, desc, repo, random_font=True)

    args: Namespace = test_parser()

    test_logger()
    test_updates()


if __name__ == "__main__":
    main()