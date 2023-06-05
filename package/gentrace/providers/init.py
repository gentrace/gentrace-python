from typing import Optional
from urllib.parse import urlparse

from gentrace.apis.tags.core_api import CoreApi
from gentrace.configuration import Configuration

GENTRACE_API_KEY: str = ""
GENTRACE_BASE_PATH: str = ""
GENTRACE_BRANCH: str = ""
GENTRACE_COMMIT: str = ""
global_gentrace_config: Optional[Configuration] = None
global_gentrace_api: Optional[CoreApi] = None


def init(
    api_key: str,
    host: Optional[str] = None,
    branch: Optional[str] = None,
    commit: Optional[str] = None,
):
    global GENTRACE_API_KEY, GENTRACE_BASE_PATH, global_gentrace_config, global_gentrace_api, GENTRACE_BRANCH, GENTRACE_COMMIT

    if not api_key:
        raise ValueError("Gentrace API key not provided.")

    GENTRACE_API_KEY = api_key

    if host:
        try:
            url = urlparse(host)
            if not url.path.startswith("/api/v1"):
                raise ValueError('Gentrace base path must end in "/api/v1".')
        except Exception as e:
            raise ValueError(f"Invalid Gentrace base path: {str(e)}")

        GENTRACE_BASE_PATH = host

    resolved_host = host if host else "https://gentrace.ai/api/v1"

    global_gentrace_config = Configuration(host=resolved_host)
    global_gentrace_config.access_token = api_key

    global_gentrace_api = CoreApi(global_gentrace_config)

    if branch:
        GENTRACE_BRANCH = branch

    if commit:
        GENTRACE_COMMIT = commit


def deinit():
    global GENTRACE_API_KEY, GENTRACE_BASE_PATH, global_gentrace_config, global_gentrace_api, GENTRACE_BRANCH, GENTRACE_COMMIT

    GENTRACE_API_KEY = ""
    GENTRACE_BASE_PATH = ""
    GENTRACE_BRANCH = ""
    GENTRACE_COMMIT = ""
    global_gentrace_config = None
    global_gentrace_api = None


__all__ = [
    "init",
    "deinit",
    "global_gentrace_api",
    "global_gentrace_config",
    "GENTRACE_API_KEY",
    "GENTRACE_BASE_PATH",
    "GENTRACE_BRANCH",
    "GENTRACE_COMMIT",
]
