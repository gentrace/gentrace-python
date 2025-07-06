import os
from typing import Dict, Optional

from .._types import NOT_GIVEN
from .._client import Gentrace, AsyncGentrace
from .._exceptions import GentraceError

_sync_client: Optional[Gentrace] = None
_async_client: Optional[AsyncGentrace] = None


def _get_default_options() -> Dict[str, str]:
    """
    Fetches default Gentrace options from environment variables.

    Returns:
        A dictionary containing "api_key" and "base_url" if the
        corresponding GENTRACE_API_KEY and GENTRACE_BASE_URL environment
        variables are set. Returns an empty dictionary otherwise.
    """
    options: Dict[str, str] = {}
    api_key = os.environ.get("GENTRACE_API_KEY")
    base_url = os.environ.get("GENTRACE_BASE_URL")

    if api_key:
        options["api_key"] = api_key
    if base_url:
        options["base_url"] = base_url
    return options


def _get_default_sync_client() -> Optional[Gentrace]:
    """
    Creates a default synchronous Gentrace client using environment variables.

    Returns:
        A Gentrace client instance if GENTRACE_API_KEY is set, None otherwise.
    """
    options = _get_default_options()
    if "api_key" in options:
        return Gentrace(
            api_key=options["api_key"],
            base_url=options.get("base_url"),  # Can be None
            timeout=NOT_GIVEN,
            default_headers=None,
            default_query=None,
        )
    return None


def _get_default_async_client() -> Optional[AsyncGentrace]:
    """
    Creates a default asynchronous Gentrace client using environment variables.

    Returns:
        An AsyncGentrace client instance if GENTRACE_API_KEY is set, None otherwise.
    """
    options = _get_default_options()
    if "api_key" in options:
        return AsyncGentrace(
            api_key=options["api_key"],
            base_url=options.get("base_url"),  # Can be None
            timeout=NOT_GIVEN,
            default_headers=None,
            default_query=None,
        )
    return None


def _get_sync_client_instance() -> Gentrace:
    """
    Retrieves the singleton synchronous Gentrace client instance.

    Initializes a default client from environment variables if no client has been
    explicitly set via init().

    Returns:
        The Gentrace client instance.

    Raises:
        GentraceError: If the SDK has not been initialized and GENTRACE_API_KEY
                       is not found in environment variables.
    """
    global _sync_client
    if _sync_client is None:
        _sync_client = _get_default_sync_client()
        if _sync_client is None:
            raise GentraceError("Gentrace SDK not initialized. Please call init() or set GENTRACE_API_KEY.")
    return _sync_client


def _get_async_client_instance() -> AsyncGentrace:
    """
    Retrieves the singleton asynchronous Gentrace client instance.

    Initializes a default client from environment variables if no client has been
    explicitly set via init().

    Returns:
        The AsyncGentrace client instance.

    Raises:
        GentraceError: If the SDK has not been initialized and GENTRACE_API_KEY
                       is not found in environment variables.
    """
    global _async_client
    if _async_client is None:
        _async_client = _get_default_async_client()
        if _async_client is None:
            raise GentraceError("Gentrace SDK not initialized. Please call init() or set GENTRACE_API_KEY.")
    return _async_client


def _set_client_instances(sync_client: Optional[Gentrace], async_client: Optional[AsyncGentrace]) -> None:
    """
    Sets the global synchronous and asynchronous Gentrace client instances.
    Can be used to reset clients by passing None.

    Args:
        sync_client: The synchronous Gentrace client instance or None.
        async_client: The asynchronous Gentrace client instance or None.
    """
    global _sync_client, _async_client
    _sync_client = sync_client
    _async_client = async_client


__all__ = [
    "_get_sync_client_instance",
    "_set_client_instances",
    "_get_async_client_instance",
]
