"""Pipeline validation utilities for Gentrace."""

import atexit
import asyncio
import threading
from typing import Set, Optional

from .utils import display_pipeline_error

# Track pending validation tasks
_pending_validations: Set[asyncio.Task[None]] = set()
_validation_loop: Optional[asyncio.AbstractEventLoop] = None
_validation_thread: Optional[threading.Thread] = None
_validation_lock = threading.Lock()

# Cache for validated pipeline IDs
_validated_pipelines: Set[str] = set()
# Cache for pipelines that failed validation
_invalid_pipelines: Set[str] = set()
# Flag to track if pipeline validation warning has been issued for a pipeline
_pipeline_warning_issued: Set[str] = set()


def _ensure_validation_loop() -> asyncio.AbstractEventLoop:
    """Ensure we have a running event loop for validation tasks."""
    global _validation_loop, _validation_thread
    
    with _validation_lock:
        if _validation_loop is None or not _validation_loop.is_running():
            # Create a new event loop in a background thread
            _validation_loop = asyncio.new_event_loop()
            
            def run_loop() -> None:
                asyncio.set_event_loop(_validation_loop)
                if _validation_loop:
                    _validation_loop.run_forever()
            
            _validation_thread = threading.Thread(target=run_loop, daemon=True)
            _validation_thread.start()
            
            # Register cleanup on exit
            atexit.register(_cleanup_validations)
    
    return _validation_loop


def _cleanup_validations() -> None:
    """Clean up any pending validation tasks on script exit."""
    global _validation_loop, _validation_thread
    
    if not _validation_loop:
        return
        
    # First, wait for pending validations
    if _pending_validations and _validation_loop.is_running():
        # Copy the set to avoid modification during iteration
        pending_tasks = list(_pending_validations)
        if pending_tasks:
            # Create a coroutine to wait for all tasks
            async def wait_for_tasks() -> None:
                await asyncio.gather(*pending_tasks, return_exceptions=True)
            
            # Wait for all pending validations to complete
            future = asyncio.run_coroutine_threadsafe(
                wait_for_tasks(), 
                _validation_loop
            )
            try:
                # Wait up to 5 seconds for validations to complete
                future.result(timeout=5.0)
            except Exception:
                # Cancel remaining tasks
                def cancel_tasks() -> None:
                    for task in pending_tasks:
                        if not task.done():
                            task.cancel()
                
                _validation_loop.call_soon_threadsafe(cancel_tasks)
    
    # Stop the validation loop
    if _validation_loop.is_running():
        _validation_loop.call_soon_threadsafe(_validation_loop.stop)
        
    if _validation_thread and _validation_thread.is_alive():
        _validation_thread.join(timeout=1.0)


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
    # Get or create the validation event loop
    loop = _ensure_validation_loop()
    
    # Create validation task
    async def validate_task() -> None:
        try:
            await validate_pipeline_access(pipeline_id)
        except Exception:
            # Error is already logged in validate_pipeline_access
            pass
    
    # Create the task in the validation loop
    def schedule_validation() -> None:
        task = loop.create_task(validate_task())
        _pending_validations.add(task)
        
        # Remove from pending when done
        def remove_from_pending(_fut: "asyncio.Future[None]") -> None:
            _pending_validations.discard(task)
        
        task.add_done_callback(remove_from_pending)
    
    # Schedule the validation task
    loop.call_soon_threadsafe(schedule_validation)


__all__ = [
    "validate_pipeline_access",
    "validate_pipeline_access_sync", 
    "start_pipeline_validation",
]