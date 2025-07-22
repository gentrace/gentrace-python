"""Pipeline-specific validation logic for Gentrace."""

import os
from typing import Set

import anyio

from .utils import display_pipeline_error

# Cache for validated pipeline IDs
_validated_pipelines: Set[str] = set()
# Cache for pipelines that failed validation
_invalid_pipelines: Set[str] = set()
# Flag to track if pipeline validation warning has been issued for a pipeline
_pipeline_warning_issued: Set[str] = set()


def validate_pipeline_access_sync(pipeline_id: str) -> None:
    """
    Synchronously validates that a pipeline ID is accessible with the current API key.
    Only checks once per pipeline ID to avoid redundant API calls.
    
    Args:
        pipeline_id: The pipeline ID to validate
    """
    # Skip if already validated or invalid
    if pipeline_id in _validated_pipelines or pipeline_id in _invalid_pipelines:
        return
    
    try:
        from .client_instance import _get_sync_client_instance
        client = _get_sync_client_instance()
        
        # Attempt to retrieve the pipeline to verify access
        client.pipelines.retrieve(pipeline_id)
        _validated_pipelines.add(pipeline_id)
    except Exception as error:
        _invalid_pipelines.add(pipeline_id)
        
        # Only show warning once per pipeline
        if pipeline_id not in _pipeline_warning_issued:
            _pipeline_warning_issued.add(pipeline_id)
            
            # Check error status code if available
            status_code = getattr(error, 'status_code', None)
            # Also check for status attribute (different client libraries)
            if status_code is None:
                status_code = getattr(error, 'status', None)
            
            if status_code == 404:
                display_pipeline_error(pipeline_id, 'not-found')
            elif status_code in (401, 403):
                display_pipeline_error(pipeline_id, 'unauthorized')
            else:
                display_pipeline_error(pipeline_id, 'unknown', error)


async def validate_pipeline_access(pipeline_id: str) -> None:
    """
    Validates that a pipeline ID is accessible with the current API key.
    Only checks once per pipeline ID to avoid redundant API calls.
    
    Args:
        pipeline_id: The pipeline ID to validate
    """
    # Skip if already validated or invalid
    if pipeline_id in _validated_pipelines or pipeline_id in _invalid_pipelines:
        return
    
    try:
        from .client_instance import _get_async_client_instance
        client = _get_async_client_instance()
        
        # Attempt to retrieve the pipeline to verify access
        await client.pipelines.retrieve(pipeline_id)
        _validated_pipelines.add(pipeline_id)
    except Exception as error:
        _invalid_pipelines.add(pipeline_id)
        
        # Only show warning once per pipeline
        if pipeline_id not in _pipeline_warning_issued:
            _pipeline_warning_issued.add(pipeline_id)
            
            # Check error status code if available
            status_code = getattr(error, 'status_code', None)
            # Also check for status attribute (different client libraries)
            if status_code is None:
                status_code = getattr(error, 'status', None)
            
            if status_code == 404:
                display_pipeline_error(pipeline_id, 'not-found')
            elif status_code in (401, 403):
                display_pipeline_error(pipeline_id, 'unauthorized')
            else:
                display_pipeline_error(pipeline_id, 'unknown', error)


def start_pipeline_validation(pipeline_id: str) -> None:
    """
    Start pipeline validation in the background (fire-and-forget).
    
    Args:
        pipeline_id: The pipeline ID to validate
    """
    # Skip validation in test environments
    # Check multiple indicators that we're in a test environment
    if (os.environ.get("TEST_API_BASE_URL") or 
        os.environ.get("PYTEST_CURRENT_TEST") or
        os.environ.get("CI") or
        os.environ.get("GITHUB_ACTIONS")):
        return
    
    # Skip if already validated or invalid
    if pipeline_id in _validated_pipelines or pipeline_id in _invalid_pipelines:
        return
    
    # Run the async validation with proper timeout
    async def run_validation_with_timeout() -> None:
        try:
            # Use anyio's timeout to ensure validation doesn't hang
            # 5 second timeout should be plenty for a simple API check
            with anyio.fail_after(5):
                await validate_pipeline_access(pipeline_id)
        except Exception:
            # All exceptions are handled, including timeouts
            pass
    
    # Try to use the current event loop's executor
    import asyncio
    try:
        loop = asyncio.get_running_loop()
        # We're in an async context, schedule the task
        loop.create_task(run_validation_with_timeout())
    except RuntimeError:
        # No running event loop, use the default executor
        loop = asyncio.new_event_loop()
        # Use run_in_executor with None to use the default ThreadPoolExecutor
        loop.run_in_executor(
            None,
            lambda: anyio.run(run_validation_with_timeout)
        )


__all__ = [
    "validate_pipeline_access",
    "validate_pipeline_access_sync", 
    "start_pipeline_validation",
]