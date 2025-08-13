# pyright: reportUnknownVariableType=false, reportUnknownArgumentType=false, reportArgumentType=false, reportCallIssue=false, reportTypedDictNotRequiredAccess=false
"""Tests for eval_dataset concurrency control."""

import time
import asyncio
import threading
from typing import Any, Dict, List, Mapping
from unittest.mock import MagicMock

import pytest

import gentrace.lib.experiment as exp_mod
import gentrace.lib.experiment_control as exp_ctrl
from gentrace import TestInput as GentraceTestInput, init, experiment, eval_dataset
from gentrace.types import TestCase as GentraceTestCase
from gentrace.lib.constants import MAX_EVAL_DATASET_CONCURRENCY
from gentrace.types.experiment import Experiment

# Use same pipeline ID as other tests
PIPELINE_ID = "76ecc73d-3419-431f-aafc-93a9d1af1b83"


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


class ConcurrencyTracker:
    """Helper class to track concurrent executions."""
    
    def __init__(self):
        self.concurrent_count = 0
        self.max_concurrent = 0
        self.execution_log: List[Dict[str, Any]] = []
        self._lock = asyncio.Lock()
    
    async def increment(self, task_id: str) -> int:
        """Increment and track concurrent count."""
        async with self._lock:
            self.concurrent_count += 1
            current = self.concurrent_count
            self.max_concurrent = max(self.max_concurrent, current)
            self.execution_log.append({
                "task_id": task_id,
                "event": "start",
                "time": time.time(),
                "concurrent": current
            })
            return current
    
    async def decrement(self, task_id: str) -> None:
        """Decrement concurrent count."""
        async with self._lock:
            self.concurrent_count -= 1
            self.execution_log.append({
                "task_id": task_id,
                "event": "end",
                "time": time.time(),
                "concurrent": self.concurrent_count
            })


@pytest.fixture
def tracker():
    """Create a fresh concurrency tracker."""
    return ConcurrencyTracker()


@pytest.fixture(autouse=True)
def init_gentrace():
    """Initialize Gentrace for tests."""
    init(api_key="test-key", base_url="https://gentrace.ai/api")


def create_test_data(num_items: int) -> List[GentraceTestInput[Mapping[str, Any]]]:
    """Create test data."""
    return [
        GentraceTestInput(inputs={"id": f"test-{i}"})
        for i in range(num_items)
    ]


@experiment(pipeline_id=PIPELINE_ID)
@pytest.mark.asyncio
async def test_async_function_with_max_concurrency(tracker: ConcurrencyTracker) -> None:
    """Test that async functions respect max_concurrency using semaphore."""
    
    async def async_task(test_case: GentraceTestCase) -> Dict[str, Any]:
        """Async task that tracks concurrency."""
        inputs = test_case.inputs
        task_id = str(inputs.get("id", "unknown"))
        current = await tracker.increment(task_id)
        
        # Simulate async work
        await asyncio.sleep(0.1)
        
        await tracker.decrement(task_id)
        return {"result": f"Processed {task_id}", "max_concurrent_seen": current}
    
    results = await eval_dataset(
        data=lambda: create_test_data(10),
        interaction=async_task,
        max_concurrency=3,
    )
    
    assert len(results) == 10
    assert tracker.max_concurrent <= 3, f"Expected max 3 concurrent, but got {tracker.max_concurrent}"


@experiment(pipeline_id=PIPELINE_ID)
@pytest.mark.asyncio
async def test_sync_function_with_max_concurrency(tracker: ConcurrencyTracker) -> None:
    """Test that sync functions respect max_concurrency using thread pool."""
    
    # Use a thread-safe counter for sync functions
    sync_lock = threading.Lock()
    
    def sync_task(test_case: GentraceTestCase) -> Dict[str, Any]:
        """Sync task that tracks concurrency."""
        inputs = test_case.inputs
        task_id = str(inputs.get("id", "unknown"))
        
        # Manually track concurrency for sync functions
        with sync_lock:
            tracker.concurrent_count += 1
            current = tracker.concurrent_count
            tracker.max_concurrent = max(tracker.max_concurrent, current)
        
        # Simulate sync work
        time.sleep(0.1)
        
        with sync_lock:
            tracker.concurrent_count -= 1
        
        return {"result": f"Processed {task_id}", "max_concurrent_seen": current}
    
    results = await eval_dataset(
        data=lambda: create_test_data(10),
        interaction=sync_task,
        max_concurrency=3,
    )
    
    assert len(results) == 10
    assert tracker.max_concurrent <= 3, f"Expected max 3 concurrent, but got {tracker.max_concurrent}"


@experiment(pipeline_id=PIPELINE_ID)
@pytest.mark.asyncio
async def test_no_max_concurrency(tracker: ConcurrencyTracker) -> None:
    """Test that without max_concurrency, all tasks run concurrently."""
    
    async def async_task(test_case: GentraceTestCase) -> Dict[str, Any]:
        """Async task that tracks concurrency."""
        inputs = test_case.inputs
        task_id = str(inputs.get("id", "unknown"))
        current = await tracker.increment(task_id)
        
        # Simulate async work
        await asyncio.sleep(0.1)
        
        await tracker.decrement(task_id)
        return {"result": f"Processed {task_id}", "max_concurrent_seen": current}
    
    results = await eval_dataset(
        data=lambda: create_test_data(10),
        interaction=async_task,
        # No max_concurrency - should run all at once
    )
    
    assert len(results) == 10
    # All 10 should run concurrently
    assert tracker.max_concurrent == 10, f"Expected all 10 concurrent, but got {tracker.max_concurrent}"


@experiment(pipeline_id=PIPELINE_ID)
@pytest.mark.asyncio
async def test_max_concurrency_zero() -> None:
    """Test that max_concurrency=0 is treated as no limit."""
    
    tracker = ConcurrencyTracker()
    
    async def async_task(test_case: GentraceTestCase) -> Dict[str, Any]:
        """Async task that tracks concurrency."""
        inputs = test_case.inputs
        task_id = str(inputs.get("id", "unknown"))
        current = await tracker.increment(task_id)
        
        # Simulate async work
        await asyncio.sleep(0.1)
        
        await tracker.decrement(task_id)
        return {"result": f"Processed {task_id}", "max_concurrent_seen": current}
    
    results = await eval_dataset(
        data=lambda: create_test_data(5),
        interaction=async_task,
        max_concurrency=0,  # Should be treated as no limit
    )
    
    assert len(results) == 5
    # All 5 should run concurrently
    assert tracker.max_concurrent == 5, f"Expected all 5 concurrent, but got {tracker.max_concurrent}"


@experiment(pipeline_id=PIPELINE_ID)
@pytest.mark.asyncio
async def test_max_concurrency_one() -> None:
    """Test that max_concurrency=1 runs tasks sequentially."""
    
    tracker = ConcurrencyTracker()
    
    async def async_task(test_case: GentraceTestCase) -> Dict[str, Any]:
        """Async task that tracks concurrency."""
        inputs = test_case.inputs
        task_id = str(inputs.get("id", "unknown"))
        current = await tracker.increment(task_id)
        
        # Simulate async work
        await asyncio.sleep(0.05)
        
        await tracker.decrement(task_id)
        return {"result": f"Processed {task_id}", "max_concurrent_seen": current}
    
    results = await eval_dataset(
        data=lambda: create_test_data(5),
        interaction=async_task,
        max_concurrency=1,
    )
    
    assert len(results) == 5
    assert tracker.max_concurrent == 1, f"Expected max 1 concurrent, but got {tracker.max_concurrent}"


@experiment(pipeline_id=PIPELINE_ID)
@pytest.mark.asyncio
@pytest.mark.filterwarnings("ignore:max_concurrency")
async def test_max_concurrency_exceeds_limit() -> None:
    """Test that max_concurrency > MAX_EVAL_DATASET_CONCURRENCY raises ValueError."""
    
    async def async_task(_: GentraceTestCase) -> Dict[str, Any]:
        """Simple async task."""
        return {"result": "ok"}
    
    # Should raise ValueError when max_concurrency exceeds the limit
    with pytest.raises(ValueError) as exc_info:
        await eval_dataset(
            data=lambda: create_test_data(5),
            interaction=async_task,
            max_concurrency=MAX_EVAL_DATASET_CONCURRENCY + 1,
        )
    
    assert f"exceeds maximum allowed value of {MAX_EVAL_DATASET_CONCURRENCY}" in str(exc_info.value)
    
    # Test with a much higher value
    with pytest.raises(ValueError) as exc_info:
        await eval_dataset(
            data=lambda: create_test_data(5),
            interaction=async_task,
            max_concurrency=MAX_EVAL_DATASET_CONCURRENCY + 50,
        )
    
    assert f"exceeds maximum allowed value of {MAX_EVAL_DATASET_CONCURRENCY}" in str(exc_info.value)
    
    # Verify that max_concurrency=MAX_EVAL_DATASET_CONCURRENCY is still allowed (boundary test)
    results = await eval_dataset(
        data=lambda: create_test_data(5),
        interaction=async_task,
        max_concurrency=MAX_EVAL_DATASET_CONCURRENCY,
    )
    
    assert len(results) == 5