# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from gentrace import Gentrace, AsyncGentrace
from tests.utils import assert_matches_type
from gentrace.types import (
    Pipeline,
    PipelineListResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestPipelines:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    def test_method_create(self, client: Gentrace) -> None:
        pipeline = client.pipelines.create(
            slug="email-summarizer",
        )
        assert_matches_type(Pipeline, pipeline, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_create_with_all_params(self, client: Gentrace) -> None:
        pipeline = client.pipelines.create(
            slug="email-summarizer",
            branch="main",
            display_name="My Pipeline",
            folder_id="98461244-7a78-4042-a7b5-7634dd2cfeb7",
            is_private=False,
            labels=["label1", "label2"],
            version=1,
        )
        assert_matches_type(Pipeline, pipeline, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_create(self, client: Gentrace) -> None:
        response = client.pipelines.with_raw_response.create(
            slug="email-summarizer",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        pipeline = response.parse()
        assert_matches_type(Pipeline, pipeline, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_create(self, client: Gentrace) -> None:
        with client.pipelines.with_streaming_response.create(
            slug="email-summarizer",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            pipeline = response.parse()
            assert_matches_type(Pipeline, pipeline, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_method_retrieve(self, client: Gentrace) -> None:
        pipeline = client.pipelines.retrieve(
            "123e4567-e89b-12d3-a456-426614174000",
        )
        assert_matches_type(Pipeline, pipeline, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_retrieve(self, client: Gentrace) -> None:
        response = client.pipelines.with_raw_response.retrieve(
            "123e4567-e89b-12d3-a456-426614174000",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        pipeline = response.parse()
        assert_matches_type(Pipeline, pipeline, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_retrieve(self, client: Gentrace) -> None:
        with client.pipelines.with_streaming_response.retrieve(
            "123e4567-e89b-12d3-a456-426614174000",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            pipeline = response.parse()
            assert_matches_type(Pipeline, pipeline, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_retrieve(self, client: Gentrace) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.pipelines.with_raw_response.retrieve(
                "",
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_update(self, client: Gentrace) -> None:
        pipeline = client.pipelines.update(
            id="123e4567-e89b-12d3-a456-426614174000",
        )
        assert_matches_type(Pipeline, pipeline, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_update_with_all_params(self, client: Gentrace) -> None:
        pipeline = client.pipelines.update(
            id="123e4567-e89b-12d3-a456-426614174000",
            branch="main",
            display_name="My Pipeline",
            folder_id="98461244-7a78-4042-a7b5-7634dd2cfeb7",
            is_archived=False,
            labels=["label1", "label2"],
            saved_runs_display={
                "evaluators": {"hide": ["b7d21c49-3a5e-4a6f-9d8b-f8c4e2d6a3b1"]},
                "feedback": {"show": False},
                "inputs": {
                    "as": "json",
                    "hide": ["internal_id"],
                    "pretty": True,
                    "show_compact": ["query"],
                },
                "metadata": {
                    "as": "tabular",
                    "show": ["timestamp", "latency"],
                },
                "outputs": {
                    "as": "json",
                    "hide": ["raw_response"],
                    "pretty": True,
                },
                "size": "full",
            },
        )
        assert_matches_type(Pipeline, pipeline, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_update(self, client: Gentrace) -> None:
        response = client.pipelines.with_raw_response.update(
            id="123e4567-e89b-12d3-a456-426614174000",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        pipeline = response.parse()
        assert_matches_type(Pipeline, pipeline, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_update(self, client: Gentrace) -> None:
        with client.pipelines.with_streaming_response.update(
            id="123e4567-e89b-12d3-a456-426614174000",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            pipeline = response.parse()
            assert_matches_type(Pipeline, pipeline, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_update(self, client: Gentrace) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.pipelines.with_raw_response.update(
                id="",
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_list(self, client: Gentrace) -> None:
        pipeline = client.pipelines.list()
        assert_matches_type(PipelineListResponse, pipeline, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_list_with_all_params(self, client: Gentrace) -> None:
        pipeline = client.pipelines.list(
            folder_id="123e4567-e89b-12d3-a456-426614174000",
            label="production",
            slug="my-pipeline",
        )
        assert_matches_type(PipelineListResponse, pipeline, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_list(self, client: Gentrace) -> None:
        response = client.pipelines.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        pipeline = response.parse()
        assert_matches_type(PipelineListResponse, pipeline, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_list(self, client: Gentrace) -> None:
        with client.pipelines.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            pipeline = response.parse()
            assert_matches_type(PipelineListResponse, pipeline, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncPipelines:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_create(self, async_client: AsyncGentrace) -> None:
        pipeline = await async_client.pipelines.create(
            slug="email-summarizer",
        )
        assert_matches_type(Pipeline, pipeline, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncGentrace) -> None:
        pipeline = await async_client.pipelines.create(
            slug="email-summarizer",
            branch="main",
            display_name="My Pipeline",
            folder_id="98461244-7a78-4042-a7b5-7634dd2cfeb7",
            is_private=False,
            labels=["label1", "label2"],
            version=1,
        )
        assert_matches_type(Pipeline, pipeline, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_create(self, async_client: AsyncGentrace) -> None:
        response = await async_client.pipelines.with_raw_response.create(
            slug="email-summarizer",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        pipeline = await response.parse()
        assert_matches_type(Pipeline, pipeline, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncGentrace) -> None:
        async with async_client.pipelines.with_streaming_response.create(
            slug="email-summarizer",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            pipeline = await response.parse()
            assert_matches_type(Pipeline, pipeline, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_method_retrieve(self, async_client: AsyncGentrace) -> None:
        pipeline = await async_client.pipelines.retrieve(
            "123e4567-e89b-12d3-a456-426614174000",
        )
        assert_matches_type(Pipeline, pipeline, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncGentrace) -> None:
        response = await async_client.pipelines.with_raw_response.retrieve(
            "123e4567-e89b-12d3-a456-426614174000",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        pipeline = await response.parse()
        assert_matches_type(Pipeline, pipeline, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncGentrace) -> None:
        async with async_client.pipelines.with_streaming_response.retrieve(
            "123e4567-e89b-12d3-a456-426614174000",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            pipeline = await response.parse()
            assert_matches_type(Pipeline, pipeline, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncGentrace) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.pipelines.with_raw_response.retrieve(
                "",
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_update(self, async_client: AsyncGentrace) -> None:
        pipeline = await async_client.pipelines.update(
            id="123e4567-e89b-12d3-a456-426614174000",
        )
        assert_matches_type(Pipeline, pipeline, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_update_with_all_params(self, async_client: AsyncGentrace) -> None:
        pipeline = await async_client.pipelines.update(
            id="123e4567-e89b-12d3-a456-426614174000",
            branch="main",
            display_name="My Pipeline",
            folder_id="98461244-7a78-4042-a7b5-7634dd2cfeb7",
            is_archived=False,
            labels=["label1", "label2"],
            saved_runs_display={
                "evaluators": {"hide": ["b7d21c49-3a5e-4a6f-9d8b-f8c4e2d6a3b1"]},
                "feedback": {"show": False},
                "inputs": {
                    "as": "json",
                    "hide": ["internal_id"],
                    "pretty": True,
                    "show_compact": ["query"],
                },
                "metadata": {
                    "as": "tabular",
                    "show": ["timestamp", "latency"],
                },
                "outputs": {
                    "as": "json",
                    "hide": ["raw_response"],
                    "pretty": True,
                },
                "size": "full",
            },
        )
        assert_matches_type(Pipeline, pipeline, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_update(self, async_client: AsyncGentrace) -> None:
        response = await async_client.pipelines.with_raw_response.update(
            id="123e4567-e89b-12d3-a456-426614174000",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        pipeline = await response.parse()
        assert_matches_type(Pipeline, pipeline, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_update(self, async_client: AsyncGentrace) -> None:
        async with async_client.pipelines.with_streaming_response.update(
            id="123e4567-e89b-12d3-a456-426614174000",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            pipeline = await response.parse()
            assert_matches_type(Pipeline, pipeline, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_update(self, async_client: AsyncGentrace) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.pipelines.with_raw_response.update(
                id="",
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_list(self, async_client: AsyncGentrace) -> None:
        pipeline = await async_client.pipelines.list()
        assert_matches_type(PipelineListResponse, pipeline, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncGentrace) -> None:
        pipeline = await async_client.pipelines.list(
            folder_id="123e4567-e89b-12d3-a456-426614174000",
            label="production",
            slug="my-pipeline",
        )
        assert_matches_type(PipelineListResponse, pipeline, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_list(self, async_client: AsyncGentrace) -> None:
        response = await async_client.pipelines.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        pipeline = await response.parse()
        assert_matches_type(PipelineListResponse, pipeline, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncGentrace) -> None:
        async with async_client.pipelines.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            pipeline = await response.parse()
            assert_matches_type(PipelineListResponse, pipeline, path=["response"])

        assert cast(Any, response.is_closed) is True
