from typing import Any

import pytest

import gentrace.lib.experiment as exp_mod
import gentrace.lib.experiment_control as exp_ctrl


# Automatically stub out experiment API calls to avoid real network interactions
@pytest.fixture(autouse=True)
def _stub_experiment_api(monkeypatch: Any) -> None:  # type: ignore
    async def fake_start_experiment_api(*_: Any, **__: Any) -> str:
        return "dummy-experiment-id"

    async def fake_finish_experiment_api(*_: Any, **__: Any) -> None:
        return None

    monkeypatch.setattr(exp_ctrl, "start_experiment_api", fake_start_experiment_api)
    monkeypatch.setattr(exp_mod, "start_experiment_api", fake_start_experiment_api)
    monkeypatch.setattr(exp_ctrl, "finish_experiment_api", fake_finish_experiment_api)
    monkeypatch.setattr(exp_mod, "finish_experiment_api", fake_finish_experiment_api)


import asyncio
from typing import Any, Dict, Union, Sequence

from pytest import LogCaptureFixture
from pydantic import BaseModel

from gentrace import TestInput as GentraceTestInput, experiment
from gentrace.types import TestCase as GentraceTestCase
from gentrace.lib.utils import is_pydantic_v1
from gentrace.lib.eval_dataset import eval_dataset

PIPELINE_ID = "76ecc73d-3419-431f-aafc-93a9d1af1b83"


# Setup - Helper Models, Functions, Data Providers


class InputModel(BaseModel):
    a: str
    b: int


class SimpleTestCase(GentraceTestCase):
    pass


class SimpleTestInputDict(GentraceTestInput[Dict[str, Any]]):
    pass


# Helper to convert Pydantic model based on version
def model_to_dict(model: BaseModel) -> Dict[str, Any]:
    if is_pydantic_v1():
        return model.dict()  # type: ignore
    else:
        return model.model_dump()


# Interaction Functions
def sync_interaction(inputs: Dict[str, Any]) -> Dict[str, Any]:
    return {"result": f"{inputs.get('a', '')}-{inputs.get('b', 0)}"}


async def async_interaction(inputs: Dict[str, Any]) -> Dict[str, Any]:
    await asyncio.sleep(0.01)
    return {"result": f"async-{inputs.get('a', '')}-{inputs.get('b', 0)}"}


# Data Providers
def sync_data_provider_dict() -> Sequence[SimpleTestInputDict]:
    return [
        SimpleTestInputDict(name="case1", inputs={"a": "hello", "b": 1}),
        SimpleTestInputDict(name="case2", inputs={"a": "world", "b": 2}),
    ]


async def async_data_provider_dict() -> Sequence[SimpleTestInputDict]:
    await asyncio.sleep(0.01)
    return [
        SimpleTestInputDict(name="async_case1", inputs={"a": "hello_async", "b": 10}),
        SimpleTestInputDict(name="async_case2", inputs={"a": "world_async", "b": 20}),
    ]


# Provide dummy required fields for TestCase initialization
DUMMY_PIPELINE_ID = "test-pipeline-id"
DUMMY_DATASET_ID = "test-dataset-id"
DUMMY_CREATED_AT = "2023-01-01T00:00:00Z"
DUMMY_UPDATED_AT = "2023-01-01T00:00:00Z"


def sync_data_provider_testcase() -> Sequence[SimpleTestCase]:
    input1_dict = model_to_dict(InputModel(a="tc_hello", b=100))
    input2_dict = model_to_dict(InputModel(a="tc_world", b=200))
    return [
        SimpleTestCase(
            id="tc1",
            name="case_tc1",
            inputs=input1_dict,
            pipelineId=DUMMY_PIPELINE_ID,
            datasetId=DUMMY_DATASET_ID,
            createdAt=DUMMY_CREATED_AT,
            updatedAt=DUMMY_UPDATED_AT,
        ),
        SimpleTestCase(
            id="tc2",
            name="case_tc2",
            inputs=input2_dict,
            pipelineId=DUMMY_PIPELINE_ID,
            datasetId=DUMMY_DATASET_ID,
            createdAt=DUMMY_CREATED_AT,
            updatedAt=DUMMY_UPDATED_AT,
        ),
    ]


def sync_data_provider_mixed() -> Sequence[Union[SimpleTestCase, SimpleTestInputDict]]:
    input1_dict = model_to_dict(InputModel(a="tc_hello", b=100))
    input4_dict = model_to_dict(InputModel(a="tc_noname", b=4))
    return [
        SimpleTestCase(
            id="tc1",
            name="case_tc1",
            inputs=input1_dict,
            pipelineId=DUMMY_PIPELINE_ID,
            datasetId=DUMMY_DATASET_ID,
            createdAt=DUMMY_CREATED_AT,
            updatedAt=DUMMY_UPDATED_AT,
        ),
        SimpleTestInputDict(name="dict_case2", inputs={"a": "dict_world", "b": 2}),
        SimpleTestInputDict(inputs={"a": "nameless_dict", "b": 3}),
        SimpleTestCase(
            id="tc4_noid",
            name="tc4_noname_case",
            inputs=input4_dict,
            pipelineId=DUMMY_PIPELINE_ID,
            datasetId=DUMMY_DATASET_ID,
            createdAt=DUMMY_CREATED_AT,
            updatedAt=DUMMY_UPDATED_AT,
        ),
    ]


def sync_data_provider_invalid_for_schema() -> Sequence[SimpleTestInputDict]:
    return [
        SimpleTestInputDict(name="valid_case", inputs={"a": "ok", "b": 1}),
        SimpleTestInputDict(name="invalid_case_missing_b", inputs={"a": "bad"}),
        SimpleTestInputDict(name="invalid_case_wrong_type", inputs={"a": "bad2", "b": "not_an_int"}),
    ]


# Tests


@pytest.mark.asyncio
async def test_eval_dataset_outside_experiment() -> None:
    """Verify eval_dataset raises RuntimeError when called outside @experiment."""
    with pytest.raises(RuntimeError) as excinfo:
        await eval_dataset(
            data=sync_data_provider_dict,
            interaction=sync_interaction,
        )
    assert "eval_dataset must be called within the context" in str(excinfo.value)


@experiment(pipeline_id=PIPELINE_ID)
@pytest.mark.asyncio
async def test_eval_dataset_sync_interaction_sync_data() -> None:
    """Test eval_dataset with sync interaction and sync data provider (dicts)."""
    results = await eval_dataset(
        data=sync_data_provider_dict,
        interaction=sync_interaction,
    )
    assert len(results) == 2
    assert results[0] == {"result": "hello-1"}
    assert results[1] == {"result": "world-2"}


@experiment(pipeline_id=PIPELINE_ID)
@pytest.mark.asyncio
async def test_eval_dataset_async_interaction_sync_data() -> None:
    """Test eval_dataset with async interaction and sync data provider (dicts)."""
    results = await eval_dataset(
        data=sync_data_provider_dict,
        interaction=async_interaction,
    )
    assert len(results) == 2
    assert results[0] == {"result": "async-hello-1"}
    assert results[1] == {"result": "async-world-2"}


@experiment(pipeline_id=PIPELINE_ID)
@pytest.mark.asyncio
async def test_eval_dataset_sync_interaction_async_data() -> None:
    """Test eval_dataset with sync interaction and async data provider (dicts)."""
    results = await eval_dataset(
        data=async_data_provider_dict,
        interaction=sync_interaction,
    )
    assert len(results) == 2
    assert results[0] == {"result": "hello_async-10"}
    assert results[1] == {"result": "world_async-20"}


@experiment(pipeline_id=PIPELINE_ID)
@pytest.mark.asyncio
async def test_eval_dataset_async_interaction_async_data() -> None:
    """Test eval_dataset with async interaction and async data provider (dicts)."""
    results = await eval_dataset(
        data=async_data_provider_dict,
        interaction=async_interaction,
    )
    assert len(results) == 2
    assert results[0] == {"result": "async-hello_async-10"}
    assert results[1] == {"result": "async-world_async-20"}


@experiment(pipeline_id=PIPELINE_ID)
@pytest.mark.asyncio
async def test_eval_dataset_with_testcase_objects() -> None:
    """Test eval_dataset using TestCase objects as input."""
    results = await eval_dataset(
        data=sync_data_provider_testcase,
        interaction=sync_interaction,
    )
    assert len(results) == 2
    assert results[0] == {"result": "tc_hello-100"}
    assert results[1] == {"result": "tc_world-200"}


@experiment(pipeline_id=PIPELINE_ID)
@pytest.mark.asyncio
async def test_eval_dataset_with_mixed_inputs() -> None:
    """Test eval_dataset using a mix of TestCase objects and dicts, and check naming."""
    results = await eval_dataset(
        data=sync_data_provider_mixed,
        interaction=sync_interaction,
    )
    assert len(results) == 4
    assert results[0] == {"result": "tc_hello-100"}
    assert results[1] == {"result": "dict_world-2"}
    assert results[2] == {"result": "nameless_dict-3"}
    assert results[3] == {"result": "tc_noname-4"}


@experiment(pipeline_id=PIPELINE_ID)
@pytest.mark.asyncio
async def test_eval_dataset_with_schema_success() -> None:
    """Test eval_dataset with a Pydantic schema and valid data."""
    results = await eval_dataset(
        data=sync_data_provider_dict,
        schema=InputModel,
        interaction=sync_interaction,
    )
    assert len(results) == 2
    assert results[0] == {"result": "hello-1"}
    assert results[1] == {"result": "world-2"}


@experiment(pipeline_id=PIPELINE_ID)
@pytest.mark.asyncio
async def test_eval_dataset_with_schema_failure(caplog: LogCaptureFixture) -> None:
    """Test eval_dataset with a Pydantic schema and invalid data. Expect None for failed cases."""
    results = await eval_dataset(
        data=sync_data_provider_invalid_for_schema,
        schema=InputModel,
        interaction=sync_interaction,
    )

    assert len(results) == 3
    assert results[0] == {"result": "ok-1"}
    assert results[1] is None
    assert results[2] is None

    assert "Pydantic validation failed for test case invalid_case_missing_b" in caplog.text
    assert "Pydantic validation failed for test case invalid_case_wrong_type" in caplog.text
    assert '{"result": "bad-0"}' not in caplog.text
    assert '{"result": "bad2-0"}' not in caplog.text
