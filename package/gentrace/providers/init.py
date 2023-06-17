import os
from typing import Optional
from urllib.parse import urlparse

from gentrace.api_client import ApiClient
from gentrace.apis.tags.core_api import CoreApi
from gentrace.configuration import Configuration

GENTRACE_CONFIG_STATE = {
    "GENTRACE_API_KEY": "",
    "GENTRACE_BASE_PATH": "",
    "GENTRACE_BRANCH": "",
    "GENTRACE_COMMIT": "",
    "GENTRACE_LOG_LEVEL": "warn",
    "global_gentrace_config": None,
    "global_gentrace_api": None,
}


def init(
    api_key: Optional[str] = None,
    host: Optional[str] = None,
    branch: Optional[str] = None,
    commit: Optional[str] = None,
    log_level: Optional[str] = None,
    run_name: Optional[str] = None,
):
    global GENTRACE_CONFIG_STATE

    if not api_key and not os.getenv("GENTRACE_API_KEY"):
        raise ValueError(
            "Gentrace API key was provided neither by the `apiKey` param in the constructor nor by the `GENTRACE_API_KEY` env variable."
        )

    GENTRACE_CONFIG_STATE["GENTRACE_API_KEY"] = api_key or os.getenv("GENTRACE_API_KEY")
    GENTRACE_CONFIG_STATE["GENTRACE_RUN_NAME"] = run_name or os.getenv(
        "GENTRACE_RUN_NAME"
    )

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
    api_client = ApiClient(configuration=config)
    GENTRACE_CONFIG_STATE["global_gentrace_api"] = CoreApi(api_client=api_client)

    if branch:
        GENTRACE_CONFIG_STATE["GENTRACE_BRANCH"] = branch

    if commit:
        GENTRACE_CONFIG_STATE["GENTRACE_COMMIT"] = commit

    if log_level:
        if log_level not in ["info", "warn"]:
            raise ValueError("Invalid log level: {}".format(log_level))
        GENTRACE_CONFIG_STATE["GENTRACE_LOG_LEVEL"] = log_level


def deinit():
    global GENTRACE_CONFIG_STATE

    GENTRACE_CONFIG_STATE["GENTRACE_API_KEY"] = ""
    GENTRACE_CONFIG_STATE["GENTRACE_BASE_PATH"] = ""
    GENTRACE_CONFIG_STATE["GENTRACE_BRANCH"] = ""
    GENTRACE_CONFIG_STATE["GENTRACE_COMMIT"] = ""
    GENTRACE_CONFIG_STATE["GENTRACE_LOG_LEVEL"] = "warn"
    GENTRACE_CONFIG_STATE["global_gentrace_config"] = None
    GENTRACE_CONFIG_STATE["global_gentrace_api"] = None


__all__ = [
    "init",
    "deinit",
    "GENTRACE_CONFIG_STATE",
]
