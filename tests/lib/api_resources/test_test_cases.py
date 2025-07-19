# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from gentrace import Gentrace, AsyncGentrace
from tests.utils import assert_matches_type
from gentrace.types import TestCase, TestCaseList

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestTestCases:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    def test_method_create(self, client: Gentrace) -> None:
        test_case = client.test_cases.create(
            dataset_id="b2c3d4e5-f6a7-8901-2345-67890abcdef1",
            inputs={"query": "bar"},
            name="Prompting with a SQL query that does not return any results",
        )
        assert_matches_type(TestCase, test_case, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_create_with_all_params(self, client: Gentrace) -> None:
        test_case = client.test_cases.create(
            dataset_id="b2c3d4e5-f6a7-8901-2345-67890abcdef1",
            inputs={"query": "bar"},
            name="Prompting with a SQL query that does not return any results",
            expected_outputs={"result": "bar"},
        )
        assert_matches_type(TestCase, test_case, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_create(self, client: Gentrace) -> None:
        response = client.test_cases.with_raw_response.create(
            dataset_id="b2c3d4e5-f6a7-8901-2345-67890abcdef1",
            inputs={"query": "bar"},
            name="Prompting with a SQL query that does not return any results",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        test_case = response.parse()
        assert_matches_type(TestCase, test_case, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_create(self, client: Gentrace) -> None:
        with client.test_cases.with_streaming_response.create(
            dataset_id="b2c3d4e5-f6a7-8901-2345-67890abcdef1",
            inputs={"query": "bar"},
            name="Prompting with a SQL query that does not return any results",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            test_case = response.parse()
            assert_matches_type(TestCase, test_case, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_method_retrieve(self, client: Gentrace) -> None:
        test_case = client.test_cases.retrieve(
            "123e4567-e89b-12d3-a456-426614174000",
        )
        assert_matches_type(TestCase, test_case, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_retrieve(self, client: Gentrace) -> None:
        response = client.test_cases.with_raw_response.retrieve(
            "123e4567-e89b-12d3-a456-426614174000",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        test_case = response.parse()
        assert_matches_type(TestCase, test_case, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_retrieve(self, client: Gentrace) -> None:
        with client.test_cases.with_streaming_response.retrieve(
            "123e4567-e89b-12d3-a456-426614174000",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            test_case = response.parse()
            assert_matches_type(TestCase, test_case, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_retrieve(self, client: Gentrace) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.test_cases.with_raw_response.retrieve(
                "",
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_list(self, client: Gentrace) -> None:
        test_case = client.test_cases.list()
        assert_matches_type(TestCaseList, test_case, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_list_with_all_params(self, client: Gentrace) -> None:
        test_case = client.test_cases.list(
            dataset_id="123e4567-e89b-12d3-a456-426614174000",
            pipeline_id="123e4567-e89b-12d3-a456-426614174000",
            pipeline_slug="email-summarizer",
        )
        assert_matches_type(TestCaseList, test_case, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_list(self, client: Gentrace) -> None:
        response = client.test_cases.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        test_case = response.parse()
        assert_matches_type(TestCaseList, test_case, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_list(self, client: Gentrace) -> None:
        with client.test_cases.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            test_case = response.parse()
            assert_matches_type(TestCaseList, test_case, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_method_delete(self, client: Gentrace) -> None:
        test_case = client.test_cases.delete(
            "123e4567-e89b-12d3-a456-426614174000",
        )
        assert test_case is None

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_delete(self, client: Gentrace) -> None:
        response = client.test_cases.with_raw_response.delete(
            "123e4567-e89b-12d3-a456-426614174000",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        test_case = response.parse()
        assert test_case is None

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_delete(self, client: Gentrace) -> None:
        with client.test_cases.with_streaming_response.delete(
            "123e4567-e89b-12d3-a456-426614174000",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            test_case = response.parse()
            assert test_case is None

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_delete(self, client: Gentrace) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.test_cases.with_raw_response.delete(
                "",
            )


class TestAsyncTestCases:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.skip()
    @parametrize
    async def test_method_create(self, async_client: AsyncGentrace) -> None:
        test_case = await async_client.test_cases.create(
            dataset_id="b2c3d4e5-f6a7-8901-2345-67890abcdef1",
            inputs={"query": "bar"},
            name="Prompting with a SQL query that does not return any results",
        )
        assert_matches_type(TestCase, test_case, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncGentrace) -> None:
        test_case = await async_client.test_cases.create(
            dataset_id="b2c3d4e5-f6a7-8901-2345-67890abcdef1",
            inputs={"query": "bar"},
            name="Prompting with a SQL query that does not return any results",
            expected_outputs={"result": "bar"},
        )
        assert_matches_type(TestCase, test_case, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_create(self, async_client: AsyncGentrace) -> None:
        response = await async_client.test_cases.with_raw_response.create(
            dataset_id="b2c3d4e5-f6a7-8901-2345-67890abcdef1",
            inputs={"query": "bar"},
            name="Prompting with a SQL query that does not return any results",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        test_case = await response.parse()
        assert_matches_type(TestCase, test_case, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncGentrace) -> None:
        async with async_client.test_cases.with_streaming_response.create(
            dataset_id="b2c3d4e5-f6a7-8901-2345-67890abcdef1",
            inputs={"query": "bar"},
            name="Prompting with a SQL query that does not return any results",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            test_case = await response.parse()
            assert_matches_type(TestCase, test_case, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_method_retrieve(self, async_client: AsyncGentrace) -> None:
        test_case = await async_client.test_cases.retrieve(
            "123e4567-e89b-12d3-a456-426614174000",
        )
        assert_matches_type(TestCase, test_case, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncGentrace) -> None:
        response = await async_client.test_cases.with_raw_response.retrieve(
            "123e4567-e89b-12d3-a456-426614174000",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        test_case = await response.parse()
        assert_matches_type(TestCase, test_case, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncGentrace) -> None:
        async with async_client.test_cases.with_streaming_response.retrieve(
            "123e4567-e89b-12d3-a456-426614174000",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            test_case = await response.parse()
            assert_matches_type(TestCase, test_case, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncGentrace) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.test_cases.with_raw_response.retrieve(
                "",
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_list(self, async_client: AsyncGentrace) -> None:
        test_case = await async_client.test_cases.list()
        assert_matches_type(TestCaseList, test_case, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncGentrace) -> None:
        test_case = await async_client.test_cases.list(
            dataset_id="123e4567-e89b-12d3-a456-426614174000",
            pipeline_id="123e4567-e89b-12d3-a456-426614174000",
            pipeline_slug="email-summarizer",
        )
        assert_matches_type(TestCaseList, test_case, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_list(self, async_client: AsyncGentrace) -> None:
        response = await async_client.test_cases.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        test_case = await response.parse()
        assert_matches_type(TestCaseList, test_case, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncGentrace) -> None:
        async with async_client.test_cases.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            test_case = await response.parse()
            assert_matches_type(TestCaseList, test_case, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_method_delete(self, async_client: AsyncGentrace) -> None:
        test_case = await async_client.test_cases.delete(
            "123e4567-e89b-12d3-a456-426614174000",
        )
        assert test_case is None

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncGentrace) -> None:
        response = await async_client.test_cases.with_raw_response.delete(
            "123e4567-e89b-12d3-a456-426614174000",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        test_case = await response.parse()
        assert test_case is None

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncGentrace) -> None:
        async with async_client.test_cases.with_streaming_response.delete(
            "123e4567-e89b-12d3-a456-426614174000",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            test_case = await response.parse()
            assert test_case is None

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_delete(self, async_client: AsyncGentrace) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.test_cases.with_raw_response.delete(
                "",
            )
