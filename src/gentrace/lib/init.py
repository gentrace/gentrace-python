from typing import Any, Dict, Optional

from gentrace import Gentrace, AsyncGentrace

from .client_instance import _set_client_instances


def init(*, api_key: Optional[str] = None, base_url: Optional[str] = None, **kwargs: Any) -> None:
    """
    Initializes the Gentrace SDK, configuring global client instances.

    This function sets up both synchronous and asynchronous Gentrace clients.
    If `api_key` is not provided, the underlying clients will attempt to use the
    GENTRACE_API_KEY environment variable. If `base_url` is not provided, they will
    attempt to use the GENTRACE_BASE_URL environment variable or a default URL.

    All arguments must be passed as keyword arguments.

    Args:
        api_key (Optional[str]): The Gentrace API key
            If None, GENTRACE_API_KEY environment variable is used by clients.
        base_url (Optional[str]): The base URL for the Gentrace API. If not provided,
            it's determined by the client (env variable or default).
        **kwargs (Any): Additional keyword arguments passed to the underlying
            `Gentrace` (synchronous) and `AsyncGentrace` (asynchronous)
            client constructors. This allows for advanced configuration.
            Common options include `timeout`, `max_retries`, `default_headers`,
            `default_query`, and `http_client`.
            If `http_client` is provided, it will be passed to both the synchronous
            and asynchronous client constructors. Ensure its type is compatible.

            Refer to the constructor signatures of `gentrace.Gentrace` and
            `gentrace.AsyncGentrace` for a full list of available options.

    Side Effects:
        Sets the internal singleton client instances used by the SDK, making them
        available for subsequent API calls through the gentrace library.
    """
    constructor_args: Dict[str, Any] = {}
    if api_key is not None:
        constructor_args["api_key"] = api_key

    if base_url is not None:
        constructor_args["base_url"] = base_url

    constructor_args.update(kwargs)

    sync_g_client = Gentrace(**constructor_args)
    async_g_client = AsyncGentrace(**constructor_args)

    _set_client_instances(sync_g_client, async_g_client)


__all__ = ["init"]
