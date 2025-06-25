from typing import Any, Union, Callable, cast

from gentrace import Gentrace, AsyncGentrace
from gentrace.resources import (
    DatasetsResource,
    PipelinesResource,
    TestCasesResource,
    ExperimentsResource,
    AsyncDatasetsResource,
    AsyncPipelinesResource,
    AsyncTestCasesResource,
    AsyncExperimentsResource,
)

from .client_instance import _get_sync_client_instance, _get_async_client_instance


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

__all__ = [
    "pipelines",
    "experiments",
    "datasets",
    "test_cases",
    "pipelines_async",
    "experiments_async",
    "datasets_async",
    "test_cases_async",
]
