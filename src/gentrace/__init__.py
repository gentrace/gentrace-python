# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Any, Union, Callable, cast

from . import types
from ._types import NOT_GIVEN, Omit, NoneType, NotGiven, Transport, ProxiesTypes
from ._utils import file_from_path
from ._client import (
    Client,
    Stream,
    Timeout,
    Gentrace,
    Transport,
    AsyncClient,
    AsyncStream,
    AsyncGentrace,
    RequestOptions,
)
from ._models import BaseModel
from ._version import __title__, __version__
from ._response import APIResponse as APIResponse, AsyncAPIResponse as AsyncAPIResponse
from .resources import (
    DatasetsResource,
    PipelinesResource,
    TestCasesResource,
    ExperimentsResource,
    AsyncDatasetsResource,
    AsyncPipelinesResource,
    AsyncTestCasesResource,
    AsyncExperimentsResource,
)
from ._constants import DEFAULT_TIMEOUT, DEFAULT_MAX_RETRIES, DEFAULT_CONNECTION_LIMITS
from ._exceptions import (
    APIError,
    ConflictError,
    GentraceError,
    NotFoundError,
    APIStatusError,
    RateLimitError,
    APITimeoutError,
    BadRequestError,
    APIConnectionError,
    AuthenticationError,
    InternalServerError,
    PermissionDeniedError,
    UnprocessableEntityError,
    APIResponseValidationError,
)
from ._base_client import DefaultHttpxClient, DefaultAsyncHttpxClient
from ._utils._logs import setup_logging as _setup_logging
from .lib.client_instance import _get_sync_client_instance, _get_async_client_instance


class _ResourceWrapper:
    def __init__(self, client_accessor_func: Callable[[], Union[Gentrace, AsyncGentrace]], resource_name: str):
        """Initializes the resource wrapper."""
        self._client_accessor_func = client_accessor_func
        self._resource_name = resource_name

    def __getattr__(self, name: str) -> Any:
        """Gets an attribute from the underlying resource."""
        client = self._client_accessor_func()
        resource_obj = getattr(client, self._resource_name)
        return getattr(resource_obj, name)


pipelines = cast(PipelinesResource, _ResourceWrapper(_get_sync_client_instance, "pipelines"))
experiments = cast(ExperimentsResource, _ResourceWrapper(_get_sync_client_instance, "experiments"))
datasets = cast(DatasetsResource, _ResourceWrapper(_get_sync_client_instance, "datasets"))
test_cases = cast(TestCasesResource, _ResourceWrapper(_get_sync_client_instance, "test_cases"))

pipelines_async = cast(AsyncPipelinesResource, _ResourceWrapper(_get_async_client_instance, "pipelines"))
experiments_async = cast(AsyncExperimentsResource, _ResourceWrapper(_get_async_client_instance, "experiments"))
datasets_async = cast(AsyncDatasetsResource, _ResourceWrapper(_get_async_client_instance, "datasets"))
test_cases_async = cast(AsyncTestCasesResource, _ResourceWrapper(_get_async_client_instance, "test_cases"))

from .lib.init import init
from .lib.traced import traced
from .lib.interaction import interaction

__all__ = [
    "types",
    "__version__",
    "__title__",
    "NoneType",
    "Transport",
    "ProxiesTypes",
    "NotGiven",
    "NOT_GIVEN",
    "Omit",
    "GentraceError",
    "APIError",
    "APIStatusError",
    "APITimeoutError",
    "APIConnectionError",
    "APIResponseValidationError",
    "BadRequestError",
    "AuthenticationError",
    "PermissionDeniedError",
    "NotFoundError",
    "ConflictError",
    "UnprocessableEntityError",
    "RateLimitError",
    "InternalServerError",
    "Timeout",
    "RequestOptions",
    "Client",
    "AsyncClient",
    "Stream",
    "AsyncStream",
    "Gentrace",
    "AsyncGentrace",
    "file_from_path",
    "BaseModel",
    "DEFAULT_TIMEOUT",
    "DEFAULT_MAX_RETRIES",
    "DEFAULT_CONNECTION_LIMITS",
    "DefaultHttpxClient",
    "DefaultAsyncHttpxClient",

    # Custom library functions
    "init",
    "traced",
    "interaction",
]

_setup_logging()

# Update the __module__ attribute for exported symbols so that
# error messages point to this module instead of the module
# it was originally defined in, e.g.
# gentrace._exceptions.NotFoundError -> gentrace.NotFoundError
__locals = locals()
for __name in __all__:
    if not __name.startswith("__"):
        try:
            __locals[__name].__module__ = "gentrace"
        except (TypeError, AttributeError):
            # Some of our exported symbols are builtins which we can't set attributes for.
            pass
