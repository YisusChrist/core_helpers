import os
import random
import re
from typing import Optional

import pyfiglet  # type: ignore
from rich import print


def _strip_rich_tags(text: str) -> str:
    """
    Remove rich text tags from a string.

    Args:
        text (str): The text to remove tags from.

    Returns:
        str: The text with tags removed.
    """
    return re.sub(r"\[\/?[\w=#]*\]", "", text)


def _get_random_font() -> str:
    """
    Get a random font from pyfiglet.

    Returns:
        str: A random font name.
    """
    fonts: list[str] = pyfiglet.FigletFont.getFonts()
    return random.choice(fonts)


def print_welcome(
    package: str,
    version: str,
    desc: str,
    repo: str,
    font: Optional[str] = "slant",
    random_font: Optional[bool] = False,
) -> None:
    """
    Print a welcome message in the terminal.

    Args:
        package (str): The package name.
        version (str): The package version.
        desc (str): The package description.
        repo (str): The package repository.
        font (str, optional): The font to use. Defaults to "slant".
        random_font (bool, optional): Whether to use a random font. Defaults to False.
    """
    # Get terminal width
    width: int = os.get_terminal_size().columns

    if random_font:
        font = _get_random_font()

    # Create and format title, repository, and description
    title: str = package.replace("_", " ").capitalize()
    version = f"[i][red]Version: {version}[/]"
    repo = f"[cyan]{repo}[/]"
    desc = f"[blue]{desc}[/] - {version}"

    # Render and print title using pyfiglet
    figlet = pyfiglet.Figlet(font=font, justify="center", width=width)
    print(f"""[green]{figlet.renderText(title)}[/]""")

    # Calculate visible lengths and center accordingly
    visible_desc: str = _strip_rich_tags(desc)
    visible_repo: str = _strip_rich_tags(repo)

    # Print description and repository info with rich formatting
    print(desc.center(width + len(desc) - len(visible_desc)))
    print(repo.center(width + len(repo) - len(visible_repo)))
    print()