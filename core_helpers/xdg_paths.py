"""XDG Base Directory Specification paths."""

from pathlib import Path
from typing import Callable

from platformdirs import (site_cache_path, site_config_path, site_data_path,
                          site_runtime_path, user_cache_path, user_config_path,
                          user_data_path, user_desktop_path,
                          user_documents_path, user_downloads_path,
                          user_log_path, user_music_path, user_pictures_path,
                          user_runtime_path, user_state_path, user_videos_path)

# Mapping app directories
APP_DIRS: dict[str, Callable] = {
    "cache": user_cache_path,
    "config": user_config_path,
    "data": user_data_path,
    "log": user_log_path,
    "runtime": user_runtime_path,
    "state": user_state_path,
    "site_cache": site_cache_path,
    "site_config": site_config_path,
    "site_data": site_data_path,
    "site_runtime": site_runtime_path,
}
# Mapping home directories
HOME_DIRS: dict[str, Callable] = {
    "desktop": user_desktop_path,
    "documents": user_documents_path,
    "downloads": user_downloads_path,
    "music": user_music_path,
    "pictures": user_pictures_path,
    "videos": user_videos_path,
}


def get_user_path(package: str, path_type: str) -> Path:
    """
    Return the requested path for the specified path type (e.g., 'cache', 'config', 'data', 'log').

    Args:
        package (str): The name of the package or project.
        path_type (str): The type of path requested ('cache', 'config', 'data', 'log').

    Returns:
        Path: The path to the requested directory.
    """
    path_func = APP_DIRS.get(path_type)
    if path_func:
        return path_func(appname=package, ensure_exists=True).resolve()
    path_func = HOME_DIRS.get(path_type)
    if path_func:
        return path_func().resolve()
    raise ValueError(f"Unsupported path type: {path_type}")
