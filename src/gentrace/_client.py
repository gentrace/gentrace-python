# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, Union, Mapping
from typing_extensions import Self, override

import httpx

from . import _exceptions
from ._qs import Querystring
from ._types import (
    NOT_GIVEN,
    Omit,
    Timeout,
    NotGiven,
    Transport,
    ProxiesTypes,
    RequestOptions,
)
from ._utils import is_given, get_async_library
from ._version import __version__
from .resources import datasets, pipelines, test_cases, experiments, organizations
from ._streaming import Stream as Stream, AsyncStream as AsyncStream
from ._exceptions import GentraceError, APIStatusError
from ._base_client import (
    DEFAULT_MAX_RETRIES,
    SyncAPIClient,
    AsyncAPIClient,
)

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
    pipelines: pipelines.PipelinesResource
    experiments: experiments.ExperimentsResource
    organizations: organizations.OrganizationsResource
    datasets: datasets.DatasetsResource
    test_cases: test_cases.TestCasesResource
    with_raw_response: GentraceWithRawResponse
    with_streaming_response: GentraceWithStreamedResponse

    # client options
    api_key: str

    def __init__(
        self,
        *,
        api_key: str | None = None,
        base_url: str | httpx.URL | None = None,
        timeout: Union[float, Timeout, None, NotGiven] = NOT_GIVEN,
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

        self.pipelines = pipelines.PipelinesResource(self)
        self.experiments = experiments.ExperimentsResource(self)
        self.organizations = organizations.OrganizationsResource(self)
        self.datasets = datasets.DatasetsResource(self)
        self.test_cases = test_cases.TestCasesResource(self)
        self.with_raw_response = GentraceWithRawResponse(self)
        self.with_streaming_response = GentraceWithStreamedResponse(self)

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
        timeout: float | Timeout | None | NotGiven = NOT_GIVEN,
        http_client: httpx.Client | None = None,
        max_retries: int | NotGiven = NOT_GIVEN,
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
    pipelines: pipelines.AsyncPipelinesResource
    experiments: experiments.AsyncExperimentsResource
    organizations: organizations.AsyncOrganizationsResource
    datasets: datasets.AsyncDatasetsResource
    test_cases: test_cases.AsyncTestCasesResource
    with_raw_response: AsyncGentraceWithRawResponse
    with_streaming_response: AsyncGentraceWithStreamedResponse

    # client options
    api_key: str

    def __init__(
        self,
        *,
        api_key: str | None = None,
        base_url: str | httpx.URL | None = None,
        timeout: Union[float, Timeout, None, NotGiven] = NOT_GIVEN,
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

        self.pipelines = pipelines.AsyncPipelinesResource(self)
        self.experiments = experiments.AsyncExperimentsResource(self)
        self.organizations = organizations.AsyncOrganizationsResource(self)
        self.datasets = datasets.AsyncDatasetsResource(self)
        self.test_cases = test_cases.AsyncTestCasesResource(self)
        self.with_raw_response = AsyncGentraceWithRawResponse(self)
        self.with_streaming_response = AsyncGentraceWithStreamedResponse(self)

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
        timeout: float | Timeout | None | NotGiven = NOT_GIVEN,
        http_client: httpx.AsyncClient | None = None,
        max_retries: int | NotGiven = NOT_GIVEN,
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
    def __init__(self, client: Gentrace) -> None:
        self.pipelines = pipelines.PipelinesResourceWithRawResponse(client.pipelines)
        self.experiments = experiments.ExperimentsResourceWithRawResponse(client.experiments)
        self.organizations = organizations.OrganizationsResourceWithRawResponse(client.organizations)
        self.datasets = datasets.DatasetsResourceWithRawResponse(client.datasets)
        self.test_cases = test_cases.TestCasesResourceWithRawResponse(client.test_cases)


class AsyncGentraceWithRawResponse:
    def __init__(self, client: AsyncGentrace) -> None:
        self.pipelines = pipelines.AsyncPipelinesResourceWithRawResponse(client.pipelines)
        self.experiments = experiments.AsyncExperimentsResourceWithRawResponse(client.experiments)
        self.organizations = organizations.AsyncOrganizationsResourceWithRawResponse(client.organizations)
        self.datasets = datasets.AsyncDatasetsResourceWithRawResponse(client.datasets)
        self.test_cases = test_cases.AsyncTestCasesResourceWithRawResponse(client.test_cases)


class GentraceWithStreamedResponse:
    def __init__(self, client: Gentrace) -> None:
        self.pipelines = pipelines.PipelinesResourceWithStreamingResponse(client.pipelines)
        self.experiments = experiments.ExperimentsResourceWithStreamingResponse(client.experiments)
        self.organizations = organizations.OrganizationsResourceWithStreamingResponse(client.organizations)
        self.datasets = datasets.DatasetsResourceWithStreamingResponse(client.datasets)
        self.test_cases = test_cases.TestCasesResourceWithStreamingResponse(client.test_cases)


class AsyncGentraceWithStreamedResponse:
    def __init__(self, client: AsyncGentrace) -> None:
        self.pipelines = pipelines.AsyncPipelinesResourceWithStreamingResponse(client.pipelines)
        self.experiments = experiments.AsyncExperimentsResourceWithStreamingResponse(client.experiments)
        self.organizations = organizations.AsyncOrganizationsResourceWithStreamingResponse(client.organizations)
        self.datasets = datasets.AsyncDatasetsResourceWithStreamingResponse(client.datasets)
        self.test_cases = test_cases.AsyncTestCasesResourceWithStreamingResponse(client.test_cases)


Client = Gentrace

AsyncClient = AsyncGentrace
