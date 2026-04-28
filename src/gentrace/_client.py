# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import TYPE_CHECKING, Any, Mapping
from typing_extensions import Self, override

import httpx

from . import _exceptions
from ._qs import Querystring
from ._types import (
    Omit,
    Timeout,
    NotGiven,
    Transport,
    ProxiesTypes,
    RequestOptions,
    not_given,
)
from ._utils import (
    is_given,
    is_mapping_t,
    get_async_library,
)
from ._compat import cached_property
from ._version import __version__
from ._streaming import Stream as Stream, AsyncStream as AsyncStream
from ._exceptions import GentraceError, APIStatusError
from ._base_client import (
    DEFAULT_MAX_RETRIES,
    SyncAPIClient,
    AsyncAPIClient,
)

if TYPE_CHECKING:
    from .resources import datasets, pipelines, test_cases, experiments, organizations
    from .resources.datasets import DatasetsResource, AsyncDatasetsResource
    from .resources.pipelines import PipelinesResource, AsyncPipelinesResource
    from .resources.test_cases import TestCasesResource, AsyncTestCasesResource
    from .resources.experiments import ExperimentsResource, AsyncExperimentsResource
    from .resources.organizations import OrganizationsResource, AsyncOrganizationsResource

__all__ = [
    "Timeout",
    "Transport",
    "ProxiesTypes",
    "RequestOptions",
    "Gentrace",
    "AsyncGentrace",
    "Client",
    "AsyncClient",
]


class Gentrace(SyncAPIClient):
    # client options
    api_key: str

    def __init__(
        self,
        *,
        api_key: str | None = None,
        base_url: str | httpx.URL | None = None,
        timeout: float | Timeout | None | NotGiven = not_given,
        max_retries: int = DEFAULT_MAX_RETRIES,
        default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        # Configure a custom httpx client.
        # We provide a `DefaultHttpxClient` class that you can pass to retain the default values we use for `limits`, `timeout` & `follow_redirects`.
        # See the [httpx documentation](https://www.python-httpx.org/api/#client) for more details.
        http_client: httpx.Client | None = None,
        # Enable or disable schema validation for data returned by the API.
        # When enabled an error APIResponseValidationError is raised
        # if the API responds with invalid data for the expected schema.
        #
        # This parameter may be removed or changed in the future.
        # If you rely on this feature, please open a GitHub issue
        # outlining your use-case to help us decide if it should be
        # part of our public interface in the future.
        _strict_response_validation: bool = False,
    ) -> None:
        """Construct a new synchronous Gentrace client instance.

        This automatically infers the `api_key` argument from the `GENTRACE_API_KEY` environment variable if it is not provided.
        """
        if api_key is None:
            api_key = os.environ.get("GENTRACE_API_KEY")
        if api_key is None:
            raise GentraceError(
                "The api_key client option must be set either by passing api_key to the client or by setting the GENTRACE_API_KEY environment variable"
            )
        self.api_key = api_key

        if base_url is None:
            base_url = os.environ.get("GENTRACE_BASE_URL")
        if base_url is None:
            base_url = f"https://gentrace.ai/api"

        custom_headers_env = os.environ.get("GENTRACE_CUSTOM_HEADERS")
        if custom_headers_env is not None:
            parsed: dict[str, str] = {}
            for line in custom_headers_env.split("\n"):
                colon = line.find(":")
                if colon >= 0:
                    parsed[line[:colon].strip()] = line[colon + 1 :].strip()
            default_headers = {**parsed, **(default_headers if is_mapping_t(default_headers) else {})}

        super().__init__(
            version=__version__,
            base_url=base_url,
            max_retries=max_retries,
            timeout=timeout,
            http_client=http_client,
            custom_headers=default_headers,
            custom_query=default_query,
            _strict_response_validation=_strict_response_validation,
        )

    @cached_property
    def pipelines(self) -> PipelinesResource:
        from .resources.pipelines import PipelinesResource

        return PipelinesResource(self)

    @cached_property
    def experiments(self) -> ExperimentsResource:
        from .resources.experiments import ExperimentsResource

        return ExperimentsResource(self)

    @cached_property
    def organizations(self) -> OrganizationsResource:
        from .resources.organizations import OrganizationsResource

        return OrganizationsResource(self)

    @cached_property
    def datasets(self) -> DatasetsResource:
        from .resources.datasets import DatasetsResource

        return DatasetsResource(self)

    @cached_property
    def test_cases(self) -> TestCasesResource:
        from .resources.test_cases import TestCasesResource

        return TestCasesResource(self)

    @cached_property
    def with_raw_response(self) -> GentraceWithRawResponse:
        return GentraceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> GentraceWithStreamedResponse:
        return GentraceWithStreamedResponse(self)

    @property
    @override
    def qs(self) -> Querystring:
        return Querystring(array_format="comma")

    @property
    @override
    def auth_headers(self) -> dict[str, str]:
        api_key = self.api_key
        return {"Authorization": f"Bearer {api_key}"}

    @property
    @override
    def default_headers(self) -> dict[str, str | Omit]:
        return {
            **super().default_headers,
            "X-Stainless-Async": "false",
            **self._custom_headers,
        }

    def copy(
        self,
        *,
        api_key: str | None = None,
        base_url: str | httpx.URL | None = None,
        timeout: float | Timeout | None | NotGiven = not_given,
        http_client: httpx.Client | None = None,
        max_retries: int | NotGiven = not_given,
        default_headers: Mapping[str, str] | None = None,
        set_default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        set_default_query: Mapping[str, object] | None = None,
        _extra_kwargs: Mapping[str, Any] = {},
    ) -> Self:
        """
        Create a new client instance re-using the same options given to the current client with optional overriding.
        """
        if default_headers is not None and set_default_headers is not None:
            raise ValueError("The `default_headers` and `set_default_headers` arguments are mutually exclusive")

        if default_query is not None and set_default_query is not None:
            raise ValueError("The `default_query` and `set_default_query` arguments are mutually exclusive")

        headers = self._custom_headers
        if default_headers is not None:
            headers = {**headers, **default_headers}
        elif set_default_headers is not None:
            headers = set_default_headers

        params = self._custom_query
        if default_query is not None:
            params = {**params, **default_query}
        elif set_default_query is not None:
            params = set_default_query

        http_client = http_client or self._client
        return self.__class__(
            api_key=api_key or self.api_key,
            base_url=base_url or self.base_url,
            timeout=self.timeout if isinstance(timeout, NotGiven) else timeout,
            http_client=http_client,
            max_retries=max_retries if is_given(max_retries) else self.max_retries,
            default_headers=headers,
            default_query=params,
            **_extra_kwargs,
        )

    # Alias for `copy` for nicer inline usage, e.g.
    # client.with_options(timeout=10).foo.create(...)
    with_options = copy

    @override
    def _make_status_error(
        self,
        err_msg: str,
        *,
        body: object,
        response: httpx.Response,
    ) -> APIStatusError:
        if response.status_code == 400:
            return _exceptions.BadRequestError(err_msg, response=response, body=body)

        if response.status_code == 401:
            return _exceptions.AuthenticationError(err_msg, response=response, body=body)

        if response.status_code == 403:
            return _exceptions.PermissionDeniedError(err_msg, response=response, body=body)

        if response.status_code == 404:
            return _exceptions.NotFoundError(err_msg, response=response, body=body)

        if response.status_code == 409:
            return _exceptions.ConflictError(err_msg, response=response, body=body)

        if response.status_code == 422:
            return _exceptions.UnprocessableEntityError(err_msg, response=response, body=body)

        if response.status_code == 429:
            return _exceptions.RateLimitError(err_msg, response=response, body=body)

        if response.status_code >= 500:
            return _exceptions.InternalServerError(err_msg, response=response, body=body)
        return APIStatusError(err_msg, response=response, body=body)


class AsyncGentrace(AsyncAPIClient):
    # client options
    api_key: str

    def __init__(
        self,
        *,
        api_key: str | None = None,
        base_url: str | httpx.URL | None = None,
        timeout: float | Timeout | None | NotGiven = not_given,
        max_retries: int = DEFAULT_MAX_RETRIES,
        default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        # Configure a custom httpx client.
        # We provide a `DefaultAsyncHttpxClient` class that you can pass to retain the default values we use for `limits`, `timeout` & `follow_redirects`.
        # See the [httpx documentation](https://www.python-httpx.org/api/#asyncclient) for more details.
        http_client: httpx.AsyncClient | None = None,
        # Enable or disable schema validation for data returned by the API.
        # When enabled an error APIResponseValidationError is raised
        # if the API responds with invalid data for the expected schema.
        #
        # This parameter may be removed or changed in the future.
        # If you rely on this feature, please open a GitHub issue
        # outlining your use-case to help us decide if it should be
        # part of our public interface in the future.
        _strict_response_validation: bool = False,
    ) -> None:
        """Construct a new async AsyncGentrace client instance.

        This automatically infers the `api_key` argument from the `GENTRACE_API_KEY` environment variable if it is not provided.
        """
        if api_key is None:
            api_key = os.environ.get("GENTRACE_API_KEY")
        if api_key is None:
            raise GentraceError(
                "The api_key client option must be set either by passing api_key to the client or by setting the GENTRACE_API_KEY environment variable"
            )
        self.api_key = api_key

        if base_url is None:
            base_url = os.environ.get("GENTRACE_BASE_URL")
        if base_url is None:
            base_url = f"https://gentrace.ai/api"

        custom_headers_env = os.environ.get("GENTRACE_CUSTOM_HEADERS")
        if custom_headers_env is not None:
            parsed: dict[str, str] = {}
            for line in custom_headers_env.split("\n"):
                colon = line.find(":")
                if colon >= 0:
                    parsed[line[:colon].strip()] = line[colon + 1 :].strip()
            default_headers = {**parsed, **(default_headers if is_mapping_t(default_headers) else {})}

        super().__init__(
            version=__version__,
            base_url=base_url,
            max_retries=max_retries,
            timeout=timeout,
            http_client=http_client,
            custom_headers=default_headers,
            custom_query=default_query,
            _strict_response_validation=_strict_response_validation,
        )

    @cached_property
    def pipelines(self) -> AsyncPipelinesResource:
        from .resources.pipelines import AsyncPipelinesResource

        return AsyncPipelinesResource(self)

    @cached_property
    def experiments(self) -> AsyncExperimentsResource:
        from .resources.experiments import AsyncExperimentsResource

        return AsyncExperimentsResource(self)

    @cached_property
    def organizations(self) -> AsyncOrganizationsResource:
        from .resources.organizations import AsyncOrganizationsResource

        return AsyncOrganizationsResource(self)

    @cached_property
    def datasets(self) -> AsyncDatasetsResource:
        from .resources.datasets import AsyncDatasetsResource

        return AsyncDatasetsResource(self)

    @cached_property
    def test_cases(self) -> AsyncTestCasesResource:
        from .resources.test_cases import AsyncTestCasesResource

        return AsyncTestCasesResource(self)

    @cached_property
    def with_raw_response(self) -> AsyncGentraceWithRawResponse:
        return AsyncGentraceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncGentraceWithStreamedResponse:
        return AsyncGentraceWithStreamedResponse(self)

    @property
    @override
    def qs(self) -> Querystring:
        return Querystring(array_format="comma")

    @property
    @override
    def auth_headers(self) -> dict[str, str]:
        api_key = self.api_key
        return {"Authorization": f"Bearer {api_key}"}

    @property
    @override
    def default_headers(self) -> dict[str, str | Omit]:
        return {
            **super().default_headers,
            "X-Stainless-Async": f"async:{get_async_library()}",
            **self._custom_headers,
        }

    def copy(
        self,
        *,
        api_key: str | None = None,
        base_url: str | httpx.URL | None = None,
        timeout: float | Timeout | None | NotGiven = not_given,
        http_client: httpx.AsyncClient | None = None,
        max_retries: int | NotGiven = not_given,
        default_headers: Mapping[str, str] | None = None,
        set_default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        set_default_query: Mapping[str, object] | None = None,
        _extra_kwargs: Mapping[str, Any] = {},
    ) -> Self:
        """
        Create a new client instance re-using the same options given to the current client with optional overriding.
        """
        if default_headers is not None and set_default_headers is not None:
            raise ValueError("The `default_headers` and `set_default_headers` arguments are mutually exclusive")

        if default_query is not None and set_default_query is not None:
            raise ValueError("The `default_query` and `set_default_query` arguments are mutually exclusive")

        headers = self._custom_headers
        if default_headers is not None:
            headers = {**headers, **default_headers}
        elif set_default_headers is not None:
            headers = set_default_headers

        params = self._custom_query
        if default_query is not None:
            params = {**params, **default_query}
        elif set_default_query is not None:
            params = set_default_query

        http_client = http_client or self._client
        return self.__class__(
            api_key=api_key or self.api_key,
            base_url=base_url or self.base_url,
            timeout=self.timeout if isinstance(timeout, NotGiven) else timeout,
            http_client=http_client,
            max_retries=max_retries if is_given(max_retries) else self.max_retries,
            default_headers=headers,
            default_query=params,
            **_extra_kwargs,
        )

    # Alias for `copy` for nicer inline usage, e.g.
    # client.with_options(timeout=10).foo.create(...)
    with_options = copy

    @override
    def _make_status_error(
        self,
        err_msg: str,
        *,
        body: object,
        response: httpx.Response,
    ) -> APIStatusError:
        if response.status_code == 400:
            return _exceptions.BadRequestError(err_msg, response=response, body=body)

        if response.status_code == 401:
            return _exceptions.AuthenticationError(err_msg, response=response, body=body)

        if response.status_code == 403:
            return _exceptions.PermissionDeniedError(err_msg, response=response, body=body)

        if response.status_code == 404:
            return _exceptions.NotFoundError(err_msg, response=response, body=body)

        if response.status_code == 409:
            return _exceptions.ConflictError(err_msg, response=response, body=body)

        if response.status_code == 422:
            return _exceptions.UnprocessableEntityError(err_msg, response=response, body=body)

        if response.status_code == 429:
            return _exceptions.RateLimitError(err_msg, response=response, body=body)

        if response.status_code >= 500:
            return _exceptions.InternalServerError(err_msg, response=response, body=body)
        return APIStatusError(err_msg, response=response, body=body)


class GentraceWithRawResponse:
    _client: Gentrace

    def __init__(self, client: Gentrace) -> None:
        self._client = client

    @cached_property
    def pipelines(self) -> pipelines.PipelinesResourceWithRawResponse:
        from .resources.pipelines import PipelinesResourceWithRawResponse

        return PipelinesResourceWithRawResponse(self._client.pipelines)

    @cached_property
    def experiments(self) -> experiments.ExperimentsResourceWithRawResponse:
        from .resources.experiments import ExperimentsResourceWithRawResponse

        return ExperimentsResourceWithRawResponse(self._client.experiments)

    @cached_property
    def organizations(self) -> organizations.OrganizationsResourceWithRawResponse:
        from .resources.organizations import OrganizationsResourceWithRawResponse

        return OrganizationsResourceWithRawResponse(self._client.organizations)

    @cached_property
    def datasets(self) -> datasets.DatasetsResourceWithRawResponse:
        from .resources.datasets import DatasetsResourceWithRawResponse

        return DatasetsResourceWithRawResponse(self._client.datasets)

    @cached_property
    def test_cases(self) -> test_cases.TestCasesResourceWithRawResponse:
        from .resources.test_cases import TestCasesResourceWithRawResponse

        return TestCasesResourceWithRawResponse(self._client.test_cases)


class AsyncGentraceWithRawResponse:
    _client: AsyncGentrace

    def __init__(self, client: AsyncGentrace) -> None:
        self._client = client

    @cached_property
    def pipelines(self) -> pipelines.AsyncPipelinesResourceWithRawResponse:
        from .resources.pipelines import AsyncPipelinesResourceWithRawResponse

        return AsyncPipelinesResourceWithRawResponse(self._client.pipelines)

    @cached_property
    def experiments(self) -> experiments.AsyncExperimentsResourceWithRawResponse:
        from .resources.experiments import AsyncExperimentsResourceWithRawResponse

        return AsyncExperimentsResourceWithRawResponse(self._client.experiments)

    @cached_property
    def organizations(self) -> organizations.AsyncOrganizationsResourceWithRawResponse:
        from .resources.organizations import AsyncOrganizationsResourceWithRawResponse

        return AsyncOrganizationsResourceWithRawResponse(self._client.organizations)

    @cached_property
    def datasets(self) -> datasets.AsyncDatasetsResourceWithRawResponse:
        from .resources.datasets import AsyncDatasetsResourceWithRawResponse

        return AsyncDatasetsResourceWithRawResponse(self._client.datasets)

    @cached_property
    def test_cases(self) -> test_cases.AsyncTestCasesResourceWithRawResponse:
        from .resources.test_cases import AsyncTestCasesResourceWithRawResponse

        return AsyncTestCasesResourceWithRawResponse(self._client.test_cases)


class GentraceWithStreamedResponse:
    _client: Gentrace

    def __init__(self, client: Gentrace) -> None:
        self._client = client

    @cached_property
    def pipelines(self) -> pipelines.PipelinesResourceWithStreamingResponse:
        from .resources.pipelines import PipelinesResourceWithStreamingResponse

        return PipelinesResourceWithStreamingResponse(self._client.pipelines)

    @cached_property
    def experiments(self) -> experiments.ExperimentsResourceWithStreamingResponse:
        from .resources.experiments import ExperimentsResourceWithStreamingResponse

        return ExperimentsResourceWithStreamingResponse(self._client.experiments)

    @cached_property
    def organizations(self) -> organizations.OrganizationsResourceWithStreamingResponse:
        from .resources.organizations import OrganizationsResourceWithStreamingResponse

        return OrganizationsResourceWithStreamingResponse(self._client.organizations)

    @cached_property
    def datasets(self) -> datasets.DatasetsResourceWithStreamingResponse:
        from .resources.datasets import DatasetsResourceWithStreamingResponse

        return DatasetsResourceWithStreamingResponse(self._client.datasets)

    @cached_property
    def test_cases(self) -> test_cases.TestCasesResourceWithStreamingResponse:
        from .resources.test_cases import TestCasesResourceWithStreamingResponse

        return TestCasesResourceWithStreamingResponse(self._client.test_cases)


class AsyncGentraceWithStreamedResponse:
    _client: AsyncGentrace

    def __init__(self, client: AsyncGentrace) -> None:
        self._client = client

    @cached_property
    def pipelines(self) -> pipelines.AsyncPipelinesResourceWithStreamingResponse:
        from .resources.pipelines import AsyncPipelinesResourceWithStreamingResponse

        return AsyncPipelinesResourceWithStreamingResponse(self._client.pipelines)

    @cached_property
    def experiments(self) -> experiments.AsyncExperimentsResourceWithStreamingResponse:
        from .resources.experiments import AsyncExperimentsResourceWithStreamingResponse

        return AsyncExperimentsResourceWithStreamingResponse(self._client.experiments)

    @cached_property
    def organizations(self) -> organizations.AsyncOrganizationsResourceWithStreamingResponse:
        from .resources.organizations import AsyncOrganizationsResourceWithStreamingResponse

        return AsyncOrganizationsResourceWithStreamingResponse(self._client.organizations)

    @cached_property
    def datasets(self) -> datasets.AsyncDatasetsResourceWithStreamingResponse:
        from .resources.datasets import AsyncDatasetsResourceWithStreamingResponse

        return AsyncDatasetsResourceWithStreamingResponse(self._client.datasets)

    @cached_property
    def test_cases(self) -> test_cases.AsyncTestCasesResourceWithStreamingResponse:
        from .resources.test_cases import AsyncTestCasesResourceWithStreamingResponse

        return AsyncTestCasesResourceWithStreamingResponse(self._client.test_cases)


Client = Gentrace

AsyncClient = AsyncGentrace
