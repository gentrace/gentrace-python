# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from gentrace import Gentrace, AsyncGentrace
from tests.utils import assert_matches_type
from gentrace.types import Dataset, DatasetList

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestDatasets:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    def test_method_create(self, client: Gentrace) -> None:
        dataset = client.datasets.create(
            description="Negative user feedback collected from our production environment",
            name="Dataset - negative user feedback - 2025-04-01",
        )
        assert_matches_type(Dataset, dataset, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_create_with_all_params(self, client: Gentrace) -> None:
        dataset = client.datasets.create(
            description="Negative user feedback collected from our production environment",
            name="Dataset - negative user feedback - 2025-04-01",
            is_golden=False,
            pipeline_id="123e4567-e89b-12d3-a456-426614174000",
            pipeline_slug="email-summarizer",
        )
        assert_matches_type(Dataset, dataset, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_create(self, client: Gentrace) -> None:
        response = client.datasets.with_raw_response.create(
            description="Negative user feedback collected from our production environment",
            name="Dataset - negative user feedback - 2025-04-01",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        dataset = response.parse()
        assert_matches_type(Dataset, dataset, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_create(self, client: Gentrace) -> None:
        with client.datasets.with_streaming_response.create(
            description="Negative user feedback collected from our production environment",
            name="Dataset - negative user feedback - 2025-04-01",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            dataset = response.parse()
            assert_matches_type(Dataset, dataset, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_method_retrieve(self, client: Gentrace) -> None:
        dataset = client.datasets.retrieve(
            "123e4567-e89b-12d3-a456-426614174000",
        )
        assert_matches_type(Dataset, dataset, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_retrieve(self, client: Gentrace) -> None:
        response = client.datasets.with_raw_response.retrieve(
            "123e4567-e89b-12d3-a456-426614174000",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        dataset = response.parse()
        assert_matches_type(Dataset, dataset, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_retrieve(self, client: Gentrace) -> None:
        with client.datasets.with_streaming_response.retrieve(
            "123e4567-e89b-12d3-a456-426614174000",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            dataset = response.parse()
            assert_matches_type(Dataset, dataset, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_retrieve(self, client: Gentrace) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.datasets.with_raw_response.retrieve(
                "",
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_update(self, client: Gentrace) -> None:
        dataset = client.datasets.update(
            id="123e4567-e89b-12d3-a456-426614174000",
        )
        assert_matches_type(Dataset, dataset, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_update_with_all_params(self, client: Gentrace) -> None:
        dataset = client.datasets.update(
            id="123e4567-e89b-12d3-a456-426614174000",
            description="Negative user feedback collected from our production environment",
            is_archived=True,
            is_golden=True,
            name="Dataset - negative user feedback - 2025-04-01",
        )
        assert_matches_type(Dataset, dataset, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_update(self, client: Gentrace) -> None:
        response = client.datasets.with_raw_response.update(
            id="123e4567-e89b-12d3-a456-426614174000",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        dataset = response.parse()
        assert_matches_type(Dataset, dataset, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_update(self, client: Gentrace) -> None:
        with client.datasets.with_streaming_response.update(
            id="123e4567-e89b-12d3-a456-426614174000",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            dataset = response.parse()
            assert_matches_type(Dataset, dataset, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_update(self, client: Gentrace) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.datasets.with_raw_response.update(
                id="",
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_list(self, client: Gentrace) -> None:
        dataset = client.datasets.list()
        assert_matches_type(DatasetList, dataset, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_list_with_all_params(self, client: Gentrace) -> None:
        dataset = client.datasets.list(
            archived=False,
            pipeline_id="123e4567-e89b-12d3-a456-426614174000",
            pipeline_slug="email-summarizer",
        )
        assert_matches_type(DatasetList, dataset, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_list(self, client: Gentrace) -> None:
        response = client.datasets.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        dataset = response.parse()
        assert_matches_type(DatasetList, dataset, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_list(self, client: Gentrace) -> None:
        with client.datasets.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            dataset = response.parse()
            assert_matches_type(DatasetList, dataset, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncDatasets:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_create(self, async_client: AsyncGentrace) -> None:
        dataset = await async_client.datasets.create(
            description="Negative user feedback collected from our production environment",
            name="Dataset - negative user feedback - 2025-04-01",
        )
        assert_matches_type(Dataset, dataset, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncGentrace) -> None:
        dataset = await async_client.datasets.create(
            description="Negative user feedback collected from our production environment",
            name="Dataset - negative user feedback - 2025-04-01",
            is_golden=False,
            pipeline_id="123e4567-e89b-12d3-a456-426614174000",
            pipeline_slug="email-summarizer",
        )
        assert_matches_type(Dataset, dataset, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_create(self, async_client: AsyncGentrace) -> None:
        response = await async_client.datasets.with_raw_response.create(
            description="Negative user feedback collected from our production environment",
            name="Dataset - negative user feedback - 2025-04-01",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        dataset = await response.parse()
        assert_matches_type(Dataset, dataset, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncGentrace) -> None:
        async with async_client.datasets.with_streaming_response.create(
            description="Negative user feedback collected from our production environment",
            name="Dataset - negative user feedback - 2025-04-01",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            dataset = await response.parse()
            assert_matches_type(Dataset, dataset, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_method_retrieve(self, async_client: AsyncGentrace) -> None:
        dataset = await async_client.datasets.retrieve(
            "123e4567-e89b-12d3-a456-426614174000",
        )
        assert_matches_type(Dataset, dataset, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncGentrace) -> None:
        response = await async_client.datasets.with_raw_response.retrieve(
            "123e4567-e89b-12d3-a456-426614174000",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        dataset = await response.parse()
        assert_matches_type(Dataset, dataset, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncGentrace) -> None:
        async with async_client.datasets.with_streaming_response.retrieve(
            "123e4567-e89b-12d3-a456-426614174000",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            dataset = await response.parse()
            assert_matches_type(Dataset, dataset, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncGentrace) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.datasets.with_raw_response.retrieve(
                "",
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_update(self, async_client: AsyncGentrace) -> None:
        dataset = await async_client.datasets.update(
            id="123e4567-e89b-12d3-a456-426614174000",
        )
        assert_matches_type(Dataset, dataset, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_update_with_all_params(self, async_client: AsyncGentrace) -> None:
        dataset = await async_client.datasets.update(
            id="123e4567-e89b-12d3-a456-426614174000",
            description="Negative user feedback collected from our production environment",
            is_archived=True,
            is_golden=True,
            name="Dataset - negative user feedback - 2025-04-01",
        )
        assert_matches_type(Dataset, dataset, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_update(self, async_client: AsyncGentrace) -> None:
        response = await async_client.datasets.with_raw_response.update(
            id="123e4567-e89b-12d3-a456-426614174000",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        dataset = await response.parse()
        assert_matches_type(Dataset, dataset, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_update(self, async_client: AsyncGentrace) -> None:
        async with async_client.datasets.with_streaming_response.update(
            id="123e4567-e89b-12d3-a456-426614174000",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            dataset = await response.parse()
            assert_matches_type(Dataset, dataset, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_update(self, async_client: AsyncGentrace) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.datasets.with_raw_response.update(
                id="",
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_list(self, async_client: AsyncGentrace) -> None:
        dataset = await async_client.datasets.list()
        assert_matches_type(DatasetList, dataset, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncGentrace) -> None:
        dataset = await async_client.datasets.list(
            archived=False,
            pipeline_id="123e4567-e89b-12d3-a456-426614174000",
            pipeline_slug="email-summarizer",
        )
        assert_matches_type(DatasetList, dataset, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_list(self, async_client: AsyncGentrace) -> None:
        response = await async_client.datasets.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        dataset = await response.parse()
        assert_matches_type(DatasetList, dataset, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncGentrace) -> None:
        async with async_client.datasets.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            dataset = await response.parse()
            assert_matches_type(DatasetList, dataset, path=["response"])

        assert cast(Any, response.is_closed) is True
