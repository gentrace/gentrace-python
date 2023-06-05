from typing import Optional
from urllib.parse import urlparse

from gentrace.apis.tags.core_api import CoreApi
from gentrace.configuration import Configuration

GENTRACE_CONFIG_STATE = {
    "GENTRACE_API_KEY": "",
    "GENTRACE_BASE_PATH": "",
    "GENTRACE_BRANCH": "",
    "GENTRACE_COMMIT": "",
    "global_gentrace_config": None,
    "global_gentrace_api": None,
}


def init(
    api_key: str,
    host: Optional[str] = None,
    branch: Optional[str] = None,
    commit: Optional[str] = None,
):
    global GENTRACE_CONFIG_STATE

    if not api_key:
        raise ValueError("Gentrace API key not provided.")

    GENTRACE_CONFIG_STATE["GENTRACE_API_KEY"] = api_key

    if host:
        try:
            url = urlparse(host)
            if url.path != "/api/v1" and url.path != "/api/v1/":
                raise ValueError('Gentrace URL path must end in "/api/v1".')
        except Exception as e:
            raise ValueError(f"Invalid Gentrace base path: {str(e)}")

        GENTRACE_CONFIG_STATE["GENTRACE_BASE_PATH"] = host

    resolved_host = host if host else "https://gentrace.ai/api/v1"

    config = Configuration(host=resolved_host)
    config.access_token = api_key

    GENTRACE_CONFIG_STATE["global_gentrace_config"] = config
    GENTRACE_CONFIG_STATE["global_gentrace_api"] = CoreApi(config)

    if branch:
        GENTRACE_CONFIG_STATE["GENTRACE_BRANCH"] = branch

    if commit:
        GENTRACE_CONFIG_STATE["GENTRACE_COMMIT"] = commit


def deinit():
    global GENTRACE_CONFIG_STATE

    GENTRACE_CONFIG_STATE["GENTRACE_API_KEY"] = ""
    GENTRACE_CONFIG_STATE["GENTRACE_BASE_PATH"] = ""
    GENTRACE_CONFIG_STATE["GENTRACE_BRANCH"] = ""
    GENTRACE_CONFIG_STATE["GENTRACE_COMMIT"] = ""
    GENTRACE_CONFIG_STATE["global_gentrace_config"] = None
    GENTRACE_CONFIG_STATE["global_gentrace_api"] = None


__all__ = [
    "init",
    "deinit",
    "GENTRACE_CONFIG_STATE",
]
