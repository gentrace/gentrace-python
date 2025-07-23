# pyright: reportUnknownVariableType=false, reportUnknownArgumentType=false, reportArgumentType=false, reportCallIssue=false, reportTypedDictNotRequiredAccess=false, reportInvalidTypeArguments=false
from typing import Any
from unittest.mock import MagicMock

import pytest

import gentrace.lib.experiment as exp_mod
import gentrace.lib.experiment_control as exp_ctrl
from gentrace.types.experiment import Experiment


# Automatically stub out experiment API calls to avoid real network interactions
@pytest.fixture(autouse=True)
def _stub_experiment_api(monkeypatch: Any) -> None:  # type: ignore
    async def fake_start_experiment_api(*_: Any, **__: Any) -> Experiment:
        return Experiment(
            id="dummy-experiment-id",
            createdAt="2023-01-01T00:00:00Z",
            metadata=None,
            name=None,
            pipelineId="dummy-pipeline-id",
            resourcePath="/experiments/dummy-experiment-id",
            updatedAt="2023-01-01T00:00:00Z",
        )

    async def fake_finish_experiment_api(*_: Any, **__: Any) -> None:
        return None
    
    # Mock the client instance to return a proper base_url
    mock_client = MagicMock()
    mock_client.base_url = "https://gentrace.ai/api"
    
    def fake_get_async_client_instance():
        return mock_client

    monkeypatch.setattr(exp_ctrl, "start_experiment_api", fake_start_experiment_api)
    monkeypatch.setattr(exp_mod, "start_experiment_api", fake_start_experiment_api)
    monkeypatch.setattr(exp_ctrl, "finish_experiment_api", fake_finish_experiment_api)
    monkeypatch.setattr(exp_mod, "finish_experiment_api", fake_finish_experiment_api)
    monkeypatch.setattr(exp_mod, "_get_async_client_instance", fake_get_async_client_instance)


import asyncio
from typing import Any, Dict, Mapping, Sequence

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


# Helper to convert Pydantic model based on version
def model_to_dict(model: BaseModel) -> Dict[str, Any]:
    if is_pydantic_v1():
        return model.dict()  # type: ignore
    else:
        return model.model_dump()


# Interaction Functions
def sync_interaction(test_case: GentraceTestCase) -> Dict[str, Any]:
    inputs = test_case.inputs
    return {"result": f"{inputs.get('a', '')}-{inputs.get('b', 0)}"}


async def async_interaction(test_case: GentraceTestCase) -> Dict[str, Any]:
    await asyncio.sleep(0.01)
    inputs = test_case.inputs
    return {"result": f"async-{inputs.get('a', '')}-{inputs.get('b', 0)}"}


# Data Providers
def sync_data_provider_dict() -> Sequence[GentraceTestInput[Mapping[str, Any]]]:
    return [
        GentraceTestInput(name="case1", inputs={"a": "hello", "b": 1}),
        GentraceTestInput(name="case2", inputs={"a": "world", "b": 2}),
    ]


async def async_data_provider_dict() -> Sequence[GentraceTestInput[Mapping[str, Any]]]:
    await asyncio.sleep(0.01)
    return [
        GentraceTestInput(name="async_case1", inputs={"a": "hello_async", "b": 10}),
        GentraceTestInput(name="async_case2", inputs={"a": "world_async", "b": 20}),
    ]


# Provide dummy required fields for TestCase initialization
DUMMY_PIPELINE_ID = "test-pipeline-id"
DUMMY_DATASET_ID = "test-dataset-id"
DUMMY_CREATED_AT = "2023-01-01T00:00:00Z"
DUMMY_UPDATED_AT = "2023-01-01T00:00:00Z"


def sync_data_provider_testcase() -> Sequence[GentraceTestCase]:
    input1_dict = model_to_dict(InputModel(a="tc_hello", b=100))
    input2_dict = model_to_dict(InputModel(a="tc_world", b=200))
    return [
        GentraceTestCase(
            id="tc1",
            name="case_tc1",
            inputs=input1_dict,
            pipelineId=DUMMY_PIPELINE_ID,
            datasetId=DUMMY_DATASET_ID,
            createdAt=DUMMY_CREATED_AT,
            updatedAt=DUMMY_UPDATED_AT,
        ),
        GentraceTestCase(
            id="tc2",
            name="case_tc2",
            inputs=input2_dict,
            pipelineId=DUMMY_PIPELINE_ID,
            datasetId=DUMMY_DATASET_ID,
            createdAt=DUMMY_CREATED_AT,
            updatedAt=DUMMY_UPDATED_AT,
        ),
    ]


def sync_data_provider_mixed() -> Sequence[GentraceTestCase]:
    input1_dict = model_to_dict(InputModel(a="tc_hello", b=100))
    input4_dict = model_to_dict(InputModel(a="tc_noname", b=4))
    return [
        GentraceTestCase(
            id="tc1",
            name="case_tc1",
            inputs=input1_dict,
            pipelineId=DUMMY_PIPELINE_ID,
            datasetId=DUMMY_DATASET_ID,
            createdAt=DUMMY_CREATED_AT,
            updatedAt=DUMMY_UPDATED_AT,
        ),
        GentraceTestCase(
            id="tc2",
            name="dict_case2",
            inputs={"a": "dict_world", "b": 2},
            pipelineId=DUMMY_PIPELINE_ID,
            datasetId=DUMMY_DATASET_ID,
            createdAt=DUMMY_CREATED_AT,
            updatedAt=DUMMY_UPDATED_AT,
        ),
        GentraceTestCase(
            id="tc3",
            name="nameless_dict",
            inputs={"a": "nameless_dict", "b": 3},
            pipelineId=DUMMY_PIPELINE_ID,
            datasetId=DUMMY_DATASET_ID,
            createdAt=DUMMY_CREATED_AT,
            updatedAt=DUMMY_UPDATED_AT,
        ),
        GentraceTestCase(
            id="tc4_noid",
            name="tc4_noname_case",
            inputs=input4_dict,
            pipelineId=DUMMY_PIPELINE_ID,
            datasetId=DUMMY_DATASET_ID,
            createdAt=DUMMY_CREATED_AT,
            updatedAt=DUMMY_UPDATED_AT,
        ),
    ]


def sync_data_provider_invalid_for_schema() -> Sequence[GentraceTestInput[Mapping[str, Any]]]:
    return [
        GentraceTestInput(name="valid_case", inputs={"a": "ok", "b": 1}),
        GentraceTestInput(name="invalid_case_missing_b", inputs={"a": "bad"}),
        GentraceTestInput(name="invalid_case_wrong_type", inputs={"a": "bad2", "b": "not_an_int"}),
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
    results = await eval_dataset(  # type: ignore
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


# Plain array tests
@experiment(pipeline_id=PIPELINE_ID)
@pytest.mark.asyncio
async def test_eval_dataset_with_plain_array_dict() -> None:
    """Test eval_dataset with a plain array of dictionaries."""
    plain_array = [
        GentraceTestInput(name="plain1", inputs={"a": "plain_hello", "b": 1}),
        GentraceTestInput(name="plain2", inputs={"a": "plain_world", "b": 2}),
    ]
    
    results = await eval_dataset(
        data=plain_array,
        interaction=sync_interaction,
    )
    assert len(results) == 2
    assert results[0] == {"result": "plain_hello-1"}
    assert results[1] == {"result": "plain_world-2"}


@experiment(pipeline_id=PIPELINE_ID)
@pytest.mark.asyncio
async def test_eval_dataset_with_plain_array_testcase() -> None:
    """Test eval_dataset with a plain array of TestCase objects."""
    input1_dict = model_to_dict(InputModel(a="array_hello", b=10))
    input2_dict = model_to_dict(InputModel(a="array_world", b=20))
    
    plain_array = [
        GentraceTestCase(
            id="array1",
            name="array_case1",
            inputs=input1_dict,
            pipelineId=DUMMY_PIPELINE_ID,
            datasetId=DUMMY_DATASET_ID,
            createdAt=DUMMY_CREATED_AT,
            updatedAt=DUMMY_UPDATED_AT,
        ),
        GentraceTestCase(
            id="array2",
            name="array_case2",
            inputs=input2_dict,
            pipelineId=DUMMY_PIPELINE_ID,
            datasetId=DUMMY_DATASET_ID,
            createdAt=DUMMY_CREATED_AT,
            updatedAt=DUMMY_UPDATED_AT,
        ),
    ]
    
    results = await eval_dataset(
        data=plain_array,
        interaction=async_interaction,
    )
    assert len(results) == 2
    assert results[0] == {"result": "async-array_hello-10"}
    assert results[1] == {"result": "async-array_world-20"}


@experiment(pipeline_id=PIPELINE_ID)
@pytest.mark.asyncio
async def test_eval_dataset_with_plain_array_mixed() -> None:
    """Test eval_dataset with a plain array of mixed TestCase objects and dicts."""
    input1_dict = model_to_dict(InputModel(a="mixed_tc", b=5))
    
    plain_array = [
        GentraceTestCase(
            id="mixed1",
            name="mixed_testcase",
            inputs=input1_dict,
            pipelineId=DUMMY_PIPELINE_ID,
            datasetId=DUMMY_DATASET_ID,
            createdAt=DUMMY_CREATED_AT,
            updatedAt=DUMMY_UPDATED_AT,
        ),
        GentraceTestInput(name="mixed_dict", inputs={"a": "mixed_dict_data", "b": 15}),
    ]
    
    results = await eval_dataset(
        data=plain_array,
        interaction=sync_interaction,
    )
    assert len(results) == 2
    assert results[0] == {"result": "mixed_tc-5"}
    assert results[1] == {"result": "mixed_dict_data-15"}


@experiment(pipeline_id=PIPELINE_ID)
@pytest.mark.asyncio
async def test_eval_dataset_with_plain_array_and_schema() -> None:
    """Test eval_dataset with a plain array and Pydantic schema validation."""
    plain_array = [
        GentraceTestInput(name="schema1", inputs={"a": "validated", "b": 42}),
        GentraceTestInput(name="schema2", inputs={"a": "also_validated", "b": 84}),
    ]
    
    results = await eval_dataset(
        data=plain_array,
        schema=InputModel,
        interaction=sync_interaction,
    )
    assert len(results) == 2
    assert results[0] == {"result": "validated-42"}
    assert results[1] == {"result": "also_validated-84"}
