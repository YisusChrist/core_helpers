import re
from typing import Optional

import requests
from packaging.version import InvalidVersion, Version
from rich import print

MAX_TIMEOUT = 10


def _get_latest_release_version(repo_url: str, is_gitlab: bool = False) -> str | None:
    """
    Retrieve the latest release version from the repository.

    Args:
        repo_url (str): The URL of the repository releases.
        is_gitlab (bool): Whether the repository is hosted on GitLab.

    Returns:
        str | None: The name of the latest release version if found, else None.
    """
    try:
        if is_gitlab:
            # Adjust the URL for GitLab's permalink for the latest release
            repo_url = repo_url.replace(
                "/releases/latest", "/releases/permalink/latest"
            )

        response: requests.Response = requests.get(repo_url, timeout=MAX_TIMEOUT)
        response.raise_for_status()

        tag_name = response.json().get("tag_name")
        name = response.json().get("name")
        # Check if the tag_name is a valid version
        if tag_name and re.match(r".*v?\d+\.\d+\.\d+", tag_name):
            return tag_name
        elif name and re.match(r".*v?\d+\.\d+\.\d+", name):
            return name
        return None
    except requests.exceptions.RequestException:
        return None


def _parse_version_tag(tag_name: str) -> Version:
    """
    Parse a version tag, stripping any leading non-numeric characters like 'v'.

    Args:
        tag_name (str): The name of the tag (e.g., 'v5.5.1').

    Returns:
        Version: Parsed Version object.
    """
    if not tag_name:
        return Version("0.0.0")
    # Remove any prefix like 'v' or 'release-'
    version_str = re.sub(r"^[^\d]*", "", tag_name)
    try:
        return Version(version_str)
    except InvalidVersion:
        return Version("0.0.0")


def _get_latest_tag(tags: list[dict[str, str]]) -> str:
    """
    Get the latest version tag from a list of tags.

    Args:
        tags (list[dict[str, str]]): List of tags retrieved from the repository.

    Returns:
        str: The name of the latest version tag.
    """
    # Parse all version tags and sort them
    parsed_tags = [(_parse_version_tag(tag["name"]), tag["name"]) for tag in tags]
    sorted_tags = sorted(parsed_tags, key=lambda x: x[0])

    # Return the name of the latest tag
    return sorted_tags[-1][1]  # The last tag in the sorted list is the latest


def _get_latest_tag_version(repo_url: str) -> str | None:
    """
    Retrieve the latest tag from the repository.

    Args:
        repo_url (str): The URL of the repository tags.

    Returns:
        str | None: The name of the latest tag if found, else None.
    """
    try:
        response: requests.Response = requests.get(repo_url, timeout=MAX_TIMEOUT)
        response.raise_for_status()
        tags = response.json()
        if tags:
            return _get_latest_tag(tags)
        return None
    except requests.exceptions.RequestException:
        return None


def _get_gitlab_project_id(gitlab_url: str) -> int | None:
    """
    Retrieve the GitLab project ID based on the given URL.

    Args:
        gitlab_url (str): The URL of the GitLab project.

    Returns:
        int | None: The project ID if found, else None.
    """
    api_url = f"https://gitlab.com/api/v4/projects/{gitlab_url}"
    try:
        response: requests.Response = requests.get(api_url, timeout=MAX_TIMEOUT)
        response.raise_for_status()
        return response.json().get("id")
    except requests.exceptions.RequestException:
        return None


def _is_newer_version(local_version: str, remote_version: str) -> bool:
    """
    Compare two versions to determine if the remote version is newer than the local version.

    Args:
        local_version (str): The current local version of the software.
        remote_version (str): The version retrieved from the remote repository.

    Returns:
        bool: True if the remote version is newer, False otherwise.
    """
    try:
        local_ver = Version(local_version)
        remote_ver = Version(remote_version)
        return remote_ver > local_ver
    except InvalidVersion as e:
        # The project version is not PEP 440 compliant
        # Compare the versions lexicographically
        return remote_version > local_version


def check_updates(git_url: str, current_version: str) -> None:
    """
    Check if there is a newer version of the script available in the Git repository.

    Supported platforms:
    - GitHub
    - GitLab
    - Codeberg
    - Gitea
    - Gitea Angry
    - Git Cryto
    - Gitee

    Args:
        git_url (str): The URL of the Git repository.
        current_version (str): The current version of the script.
    """
    if git_url.endswith(".git"):
        git_url = git_url[:-4]
    if git_url.endswith("/"):
        git_url = git_url[:-1]

    project_id: str = ""
    is_gitlab = False

    if "github.com" in git_url:
        api_base = "https://api.github.com/repos"
        project_id = git_url.split("https://github.com/")[1]
    elif "gitlab.com" in git_url:
        is_gitlab = True
        api_base = "https://gitlab.com/api/v4/projects"
        gitlab_project_path: str = git_url.split("https://gitlab.com/")[1].replace(
            "/", "%2F"
        )
        gitlab_project_id: int | None = _get_gitlab_project_id(gitlab_project_path)
        if not gitlab_project_id:
            print("[red]ERROR[/]: Could not retrieve the GitLab project ID.")
            return

        project_id = str(gitlab_project_id)
    elif "codeberg.org" in git_url:
        api_base = "https://codeberg.org/api/v1/repos"
        project_id = git_url.split("https://codeberg.org/")[1]
    elif "gitea.com" in git_url:
        api_base = "https://gitea.com/api/v1/repos"
        project_id = git_url.split("https://gitea.com/")[1]
    elif "gitea.angry.im" in git_url:
        api_base = "https://gitea.angry.im/api/v1/repos"
        project_id = git_url.split("https://gitea.angry.im/")[1]
    elif "git.cryto.net" in git_url:
        api_base = "https://git.cryto.net/api/v1/repos"
        project_id = git_url.split("https://git.cryto.net/")[1]
    elif "gitee.com" in git_url:
        api_base = "https://gitee.com/api/v5/repos"
        project_id = git_url.split("https://gitee.com/")[1]
    else:
        print("[red]ERROR[/]: Unsupported platform.")
        return

    release_url: str = f"{api_base}/{project_id}/releases/latest"
    tag_url: str = f"{api_base}/{project_id}/tags"

    latest_version: Optional[str] = _get_latest_release_version(release_url, is_gitlab)
    if latest_version is None:  # Try to get the latest tag if no release found
        latest_version = _get_latest_tag_version(tag_url)

    if latest_version and _is_newer_version(current_version, latest_version):
        print(
            "\n[yellow]Newer version of the script available: "
            f"{latest_version}.\nPlease consider updating your version.[/]"
        )
    elif latest_version is None:
        print("[red]ERROR[/]: Could not check for updates. No releases or tags found.")
