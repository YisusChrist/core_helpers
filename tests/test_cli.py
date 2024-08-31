from argparse import ArgumentParser, Namespace
from typing import Any

import pytest

from core_helpers.cli import setup_parser


@pytest.fixture
def parser_data() -> tuple[ArgumentParser, Any]:
    package = "MyApp"
    description = "MyApp description"
    version = "1.0.0"

    parser, _ = setup_parser(package, description, version)
    return parser, _


def test_get_parser(parser_data: tuple[ArgumentParser, Any]) -> None:
    parser, g_main = parser_data

    # Check if the parser is created and main group exists
    assert parser is not None

    # Add argument to the main group and test parsing
    g_main.add_argument(
        "-f",
        "--file",
        dest="file",
        type=str,
        required=True,
        help="The file to process.",
    )

    # Test parsing command-line arguments
    args: Namespace = parser.parse_args(["-f", "testfile.txt"])
    assert args.file == "testfile.txt"

    # Test that the help argument works
    help_message: str = parser.format_help()
    assert "--help" in help_message


def test_add_argument_group_valid(parser_data: tuple[ArgumentParser, Any]) -> None:
    """Test adding a valid argument group."""
    parser, _ = parser_data
    group_name = "example_group"
    group = parser.add_argument_group(group_name)
    assert group.title == group_name


@pytest.mark.parametrize("argument_name", [None, "", 123, []])
def test_add_argument_invalid(
    parser_data: tuple[ArgumentParser, Any], argument_name: Any
) -> None:
    """Test adding an invalid argument group."""
    parser, _ = parser_data
    with pytest.raises((TypeError, IndexError)):
        parser.add_argument(argument_name)
