"""Command-line interface helper functions."""

from argparse import ArgumentParser, _ArgumentGroup

from rich_argparse_plus import RichHelpFormatterPlus  # type: ignore


def setup_parser(
    package: str, description: str, version: str
) -> tuple[ArgumentParser, _ArgumentGroup]:
    """
    Create a parser with the default command-line arguments.

    Returns:
        tuple[ArgumentParser, _ArgumentGroup]: The parser and the main group.
    """
    parser = ArgumentParser(
        description=description,  # Program description
        formatter_class=RichHelpFormatterPlus,  # Disable line wrapping
        allow_abbrev=False,  # Disable abbreviations
        add_help=False,  # Disable default help
    )

    main_group: _ArgumentGroup = parser.add_argument_group("Main Options")
    # Add arguments in the main group later

    misc_group: _ArgumentGroup = parser.add_argument_group("Miscellaneous Options")
    # Help
    misc_group.add_argument(
        "-h", "--help", action="help", help="Show this help message and exit."
    )
    # Verbose
    misc_group.add_argument(
        "-v",
        "--verbose",
        dest="verbose",
        action="store_true",
        default=False,
        help="Show log messages on screen. Default is False.",
    )
    # Debug
    misc_group.add_argument(
        "-d",
        "--debug",
        dest="debug",
        action="store_true",
        default=False,
        help="Activate debug logs. Default is False.",
    )
    # Version
    misc_group.add_argument(
        "-V",
        "--version",
        action="version",
        help="Show version number and exit.",
        version=f"[argparse.prog]{package}[/] version [i]{version}[/]",
    )

    return parser, main_group
