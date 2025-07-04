"""Generic background event loop management for async tasks."""

import atexit
import asyncio
import threading
from typing import Any, Set, TypeVar, Optional, Coroutine

# Track pending tasks
_pending_tasks: Set[asyncio.Task[Any]] = set()
_background_loop: Optional[asyncio.AbstractEventLoop] = None
_background_thread: Optional[threading.Thread] = None
_loop_lock = threading.Lock()

T = TypeVar('T')


def _ensure_background_loop() -> asyncio.AbstractEventLoop:
    """Ensure we have a running event loop for background tasks."""
    global _background_loop, _background_thread
    
    with _loop_lock:
        if _background_loop is None or not _background_loop.is_running():
            # Create a new event loop in a background thread
            _background_loop = asyncio.new_event_loop()
            
            def run_loop() -> None:
                asyncio.set_event_loop(_background_loop)
                if _background_loop:
                    _background_loop.run_forever()
            
            _background_thread = threading.Thread(target=run_loop, daemon=True)
            _background_thread.start()
            
            # Register cleanup on exit
            atexit.register(_cleanup_background_loop)
    
    return _background_loop


def _cleanup_background_loop() -> None:
    """Clean up any pending tasks on script exit."""
    global _background_loop, _background_thread
    
    if not _background_loop:
        return
        
    # First, wait for pending tasks
    if _pending_tasks and _background_loop.is_running():
        # Copy the set to avoid modification during iteration
        pending_tasks = list(_pending_tasks)
        if pending_tasks:
            # Create a coroutine to wait for all tasks
            async def wait_for_tasks() -> None:
                await asyncio.gather(*pending_tasks, return_exceptions=True)
            
            # Wait for all pending tasks to complete
            future = asyncio.run_coroutine_threadsafe(
                wait_for_tasks(), 
                _background_loop
            )
            try:
                # Wait up to 5 seconds for tasks to complete
                future.result(timeout=5.0)
            except Exception:
                # Cancel remaining tasks
                def cancel_tasks() -> None:
                    for task in pending_tasks:
                        if not task.done():
                            task.cancel()
                
                _background_loop.call_soon_threadsafe(cancel_tasks)
    
    # Stop the background loop
    if _background_loop.is_running():
        _background_loop.call_soon_threadsafe(_background_loop.stop)
        
    if _background_thread and _background_thread.is_alive():
        _background_thread.join(timeout=1.0)


def schedule_background_task(coro: Coroutine[Any, Any, T]) -> None:
    """
    Schedule a coroutine to run in the background (fire-and-forget).
    
    Args:
        coro: The coroutine to run in the background
    """
    # Get or create the background event loop
    loop = _ensure_background_loop()
    
    # Create task wrapper
    async def task_wrapper() -> T:
        try:
            return await coro
        except Exception:
            # Errors are handled by the coroutine itself
            raise
    
    # Create the task in the background loop
    def schedule_task() -> None:
        task = loop.create_task(task_wrapper())
        _pending_tasks.add(task)
        
        # Remove from pending when done
        def remove_from_pending(_fut: "asyncio.Future[T]") -> None:
            _pending_tasks.discard(task)
        
        task.add_done_callback(remove_from_pending)
    
    # Schedule the task
    loop.call_soon_threadsafe(schedule_task)


__all__ = [
    "schedule_background_task",
]