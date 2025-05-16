# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

import typing as _t

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
    """A wrapper class that provides lazy access to Gentrace API resources.

    This class acts as a proxy to access resources (like pipelines, experiments, etc.) from
    either a synchronous or asynchronous Gentrace client. It lazily initializes the client
    only when a resource method is actually accessed.

    Args:
        client_accessor_func: A callable that returns either a Gentrace or AsyncGentrace client instance
        resource_name: The name of the resource to wrap (e.g. "pipelines", "experiments")
    """

    def __init__(self, client_accessor_func: _t.Callable[[], _t.Union[Gentrace, AsyncGentrace]], resource_name: str):
        """Initializes the resource wrapper."""
        self._client_accessor_func = client_accessor_func
        self._resource_name = resource_name

    def __getattr__(self, name: str) -> _t.Any:
        """Gets an attribute from the underlying resource.

        Args:
            name: The name of the attribute to access on the resource

        Returns:
            The requested attribute from the underlying resource
        """
        client = self._client_accessor_func()
        resource_obj = getattr(client, self._resource_name)
        return getattr(resource_obj, name)


pipelines = _t.cast(PipelinesResource, _ResourceWrapper(_get_sync_client_instance, "pipelines"))
experiments = _t.cast(ExperimentsResource, _ResourceWrapper(_get_sync_client_instance, "experiments"))
datasets = _t.cast(DatasetsResource, _ResourceWrapper(_get_sync_client_instance, "datasets"))
test_cases = _t.cast(TestCasesResource, _ResourceWrapper(_get_sync_client_instance, "test_cases"))

pipelines_async = _t.cast(AsyncPipelinesResource, _ResourceWrapper(_get_async_client_instance, "pipelines"))
experiments_async = _t.cast(AsyncExperimentsResource, _ResourceWrapper(_get_async_client_instance, "experiments"))
datasets_async = _t.cast(AsyncDatasetsResource, _ResourceWrapper(_get_async_client_instance, "datasets"))
test_cases_async = _t.cast(AsyncTestCasesResource, _ResourceWrapper(_get_async_client_instance, "test_cases"))

from .types import Dataset, Pipeline, TestCase, Experiment
from .lib.eval import eval
from .lib.init import init
from .lib.traced import traced
from .lib.sampler import GentraceSampler
from .lib.constants import (
    ATTR_GENTRACE_SAMPLE_KEY,
    ATTR_GENTRACE_PIPELINE_ID,
    ATTR_GENTRACE_TEST_CASE_ID,
    ATTR_GENTRACE_EXPERIMENT_ID,
    ATTR_GENTRACE_TEST_CASE_NAME,
    ATTR_GENTRACE_FN_ARGS_EVENT_NAME,
    ATTR_GENTRACE_FN_OUTPUT_EVENT_NAME,
)
from .lib.experiment import experiment
from .lib.interaction import interaction
from .lib.eval_dataset import TestInput, eval_dataset
from .lib.span_processor import GentraceSpanProcessor

### End custom Gentrace imports

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
    # Start custom Gentrace exports
    "init",
    "traced",
    "interaction",
    "experiment",
    "eval",
    "eval_dataset",
    "TestInput",
    "ATTR_GENTRACE_PIPELINE_ID",
    "ATTR_GENTRACE_TEST_CASE_ID",
    "ATTR_GENTRACE_EXPERIMENT_ID",
    "ATTR_GENTRACE_FN_ARGS_EVENT_NAME",
    "ATTR_GENTRACE_FN_OUTPUT_EVENT_NAME",
    "ATTR_GENTRACE_TEST_CASE_NAME",
    "ATTR_GENTRACE_SAMPLE_KEY",
    "GentraceSampler",
    "GentraceSpanProcessor",
    "TestCase",
    "Experiment",
    "Dataset",
    "Pipeline",
    # End custom Gentrace exports
]

if not _t.TYPE_CHECKING:
    from ._utils._resources_proxy import resources as resources

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
