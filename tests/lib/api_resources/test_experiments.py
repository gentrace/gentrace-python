# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from gentrace import Gentrace, AsyncGentrace
from tests.utils import assert_matches_type
from gentrace.types import (
    Experiment,
    ExperimentList,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestExperiments:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    def test_method_create(self, client: Gentrace) -> None:
        experiment = client.experiments.create(
            pipeline_id="123e4567-e89b-12d3-a456-426614174000",
        )
        assert_matches_type(Experiment, experiment, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_create_with_all_params(self, client: Gentrace) -> None:
        experiment = client.experiments.create(
            pipeline_id="123e4567-e89b-12d3-a456-426614174000",
            metadata={"promptTemplate": "bar"},
            name="OpenAI o3-mini prompt",
        )
        assert_matches_type(Experiment, experiment, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_create(self, client: Gentrace) -> None:
        response = client.experiments.with_raw_response.create(
            pipeline_id="123e4567-e89b-12d3-a456-426614174000",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        experiment = response.parse()
        assert_matches_type(Experiment, experiment, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_create(self, client: Gentrace) -> None:
        with client.experiments.with_streaming_response.create(
            pipeline_id="123e4567-e89b-12d3-a456-426614174000",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            experiment = response.parse()
            assert_matches_type(Experiment, experiment, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_method_retrieve(self, client: Gentrace) -> None:
        experiment = client.experiments.retrieve(
            "123e4567-e89b-12d3-a456-426614174000",
        )
        assert_matches_type(Experiment, experiment, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_retrieve(self, client: Gentrace) -> None:
        response = client.experiments.with_raw_response.retrieve(
            "123e4567-e89b-12d3-a456-426614174000",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        experiment = response.parse()
        assert_matches_type(Experiment, experiment, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_retrieve(self, client: Gentrace) -> None:
        with client.experiments.with_streaming_response.retrieve(
            "123e4567-e89b-12d3-a456-426614174000",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            experiment = response.parse()
            assert_matches_type(Experiment, experiment, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_retrieve(self, client: Gentrace) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.experiments.with_raw_response.retrieve(
                "",
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_update(self, client: Gentrace) -> None:
        experiment = client.experiments.update(
            id="123e4567-e89b-12d3-a456-426614174000",
        )
        assert_matches_type(Experiment, experiment, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_update_with_all_params(self, client: Gentrace) -> None:
        experiment = client.experiments.update(
            id="123e4567-e89b-12d3-a456-426614174000",
            metadata={"key": "bar"},
            name="OpenAI o3-mini prompt",
            status="GENERATING",
        )
        assert_matches_type(Experiment, experiment, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_update(self, client: Gentrace) -> None:
        response = client.experiments.with_raw_response.update(
            id="123e4567-e89b-12d3-a456-426614174000",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        experiment = response.parse()
        assert_matches_type(Experiment, experiment, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_update(self, client: Gentrace) -> None:
        with client.experiments.with_streaming_response.update(
            id="123e4567-e89b-12d3-a456-426614174000",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            experiment = response.parse()
            assert_matches_type(Experiment, experiment, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_update(self, client: Gentrace) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.experiments.with_raw_response.update(
                id="",
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_list(self, client: Gentrace) -> None:
        experiment = client.experiments.list()
        assert_matches_type(ExperimentList, experiment, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_list_with_all_params(self, client: Gentrace) -> None:
        experiment = client.experiments.list(
            pipeline_id="123e4567-e89b-12d3-a456-426614174000",
        )
        assert_matches_type(ExperimentList, experiment, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_list(self, client: Gentrace) -> None:
        response = client.experiments.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        experiment = response.parse()
        assert_matches_type(ExperimentList, experiment, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_list(self, client: Gentrace) -> None:
        with client.experiments.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            experiment = response.parse()
            assert_matches_type(ExperimentList, experiment, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncExperiments:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.skip()
    @parametrize
    async def test_method_create(self, async_client: AsyncGentrace) -> None:
        experiment = await async_client.experiments.create(
            pipeline_id="123e4567-e89b-12d3-a456-426614174000",
        )
        assert_matches_type(Experiment, experiment, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncGentrace) -> None:
        experiment = await async_client.experiments.create(
            pipeline_id="123e4567-e89b-12d3-a456-426614174000",
            metadata={"promptTemplate": "bar"},
            name="OpenAI o3-mini prompt",
        )
        assert_matches_type(Experiment, experiment, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_create(self, async_client: AsyncGentrace) -> None:
        response = await async_client.experiments.with_raw_response.create(
            pipeline_id="123e4567-e89b-12d3-a456-426614174000",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        experiment = await response.parse()
        assert_matches_type(Experiment, experiment, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncGentrace) -> None:
        async with async_client.experiments.with_streaming_response.create(
            pipeline_id="123e4567-e89b-12d3-a456-426614174000",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            experiment = await response.parse()
            assert_matches_type(Experiment, experiment, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_method_retrieve(self, async_client: AsyncGentrace) -> None:
        experiment = await async_client.experiments.retrieve(
            "123e4567-e89b-12d3-a456-426614174000",
        )
        assert_matches_type(Experiment, experiment, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncGentrace) -> None:
        response = await async_client.experiments.with_raw_response.retrieve(
            "123e4567-e89b-12d3-a456-426614174000",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        experiment = await response.parse()
        assert_matches_type(Experiment, experiment, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncGentrace) -> None:
        async with async_client.experiments.with_streaming_response.retrieve(
            "123e4567-e89b-12d3-a456-426614174000",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            experiment = await response.parse()
            assert_matches_type(Experiment, experiment, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncGentrace) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.experiments.with_raw_response.retrieve(
                "",
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_update(self, async_client: AsyncGentrace) -> None:
        experiment = await async_client.experiments.update(
            id="123e4567-e89b-12d3-a456-426614174000",
        )
        assert_matches_type(Experiment, experiment, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_update_with_all_params(self, async_client: AsyncGentrace) -> None:
        experiment = await async_client.experiments.update(
            id="123e4567-e89b-12d3-a456-426614174000",
            metadata={"key": "bar"},
            name="OpenAI o3-mini prompt",
            status="GENERATING",
        )
        assert_matches_type(Experiment, experiment, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_update(self, async_client: AsyncGentrace) -> None:
        response = await async_client.experiments.with_raw_response.update(
            id="123e4567-e89b-12d3-a456-426614174000",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        experiment = await response.parse()
        assert_matches_type(Experiment, experiment, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_update(self, async_client: AsyncGentrace) -> None:
        async with async_client.experiments.with_streaming_response.update(
            id="123e4567-e89b-12d3-a456-426614174000",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            experiment = await response.parse()
            assert_matches_type(Experiment, experiment, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_update(self, async_client: AsyncGentrace) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.experiments.with_raw_response.update(
                id="",
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_list(self, async_client: AsyncGentrace) -> None:
        experiment = await async_client.experiments.list()
        assert_matches_type(ExperimentList, experiment, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncGentrace) -> None:
        experiment = await async_client.experiments.list(
            pipeline_id="123e4567-e89b-12d3-a456-426614174000",
        )
        assert_matches_type(ExperimentList, experiment, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_list(self, async_client: AsyncGentrace) -> None:
        response = await async_client.experiments.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        experiment = await response.parse()
        assert_matches_type(ExperimentList, experiment, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncGentrace) -> None:
        async with async_client.experiments.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            experiment = await response.parse()
            assert_matches_type(ExperimentList, experiment, path=["response"])

        assert cast(Any, response.is_closed) is True
