"""Generic background event loop management for async tasks."""

import atexit
import asyncio
import threading
from typing import Any, Set, TypeVar, Optional, Coroutine

# Track pending tasks and futures
_pending_tasks: Set[asyncio.Task[Any]] = set()
_pending_futures: Set[Any] = set()  # concurrent.futures.Future objects
_background_loop: Optional[asyncio.AbstractEventLoop] = None
_background_thread: Optional[threading.Thread] = None
_loop_lock = threading.Lock()
_cleanup_registered = False

T = TypeVar("T")


def _ensure_background_loop() -> asyncio.AbstractEventLoop:
    """Ensure we have a running event loop for background tasks."""
    global _background_loop, _background_thread, _cleanup_registered

    with _loop_lock:
        if _background_loop is None or not _background_loop.is_running():
            # Create a new event loop in a background thread
            _background_loop = asyncio.new_event_loop()

            def run_loop() -> None:
                asyncio.set_event_loop(_background_loop)
                if _background_loop:
                    try:
                        _background_loop.run_forever()
                    finally:
                        # Clean up the loop when it stops
                        try:
                            _background_loop.close()
                        except Exception:
                            pass

            _background_thread = threading.Thread(target=run_loop, daemon=True, name="gentrace-background")
            _background_thread.start()

            # Wait for the loop to be running
            import time

            max_wait = 1.0  # Maximum 1 second wait
            start_time = time.time()
            while not _background_loop.is_running() and (time.time() - start_time) < max_wait:
                time.sleep(0.001)  # Check every millisecond

            # Register cleanup on exit only once
            if not _cleanup_registered:
                atexit.register(_cleanup_background_loop)
                _cleanup_registered = True

    return _background_loop


def _cleanup_background_loop() -> None:
    """Clean up any pending tasks on script exit."""
    global _background_loop, _background_thread, _cleanup_registered

    # Prevent re-entry
    _cleanup_registered = False

    if not _background_loop:
        return
    
    # First wait for all pending futures (from run_coroutine_threadsafe)
    if _pending_futures:
        for future in list(_pending_futures):
            if not future.done():
                try:
                    # Wait for the future to complete
                    future.result(timeout=2.0)
                except Exception:
                    # Ignore exceptions, we just want to ensure completion
                    pass

    # Wait for all pending tasks to complete
    if _pending_tasks:
        # Copy the set to avoid modification during iteration
        pending_tasks = list(_pending_tasks)

        # Wait for all tasks to complete
        if _background_loop.is_running() and pending_tasks:
            # Create a coroutine to wait for all tasks
            async def wait_for_tasks() -> None:
                # Filter out done tasks
                active_tasks = [task for task in pending_tasks if not task.done()]
                if active_tasks:
                    # Wait for all tasks with a reasonable timeout
                    try:
                        await asyncio.wait_for(
                            asyncio.gather(*active_tasks, return_exceptions=True),
                            timeout=2.0  # Give tasks 2 seconds to complete
                        )
                    except asyncio.TimeoutError:
                        # If tasks don't complete in time, cancel them
                        for task in active_tasks:
                            if not task.done():
                                task.cancel()

            try:
                future = asyncio.run_coroutine_threadsafe(wait_for_tasks(), _background_loop)
                future.result(timeout=3.0)  # Wait up to 3 seconds total
            except Exception:
                pass

    # Stop the background loop
    if _background_loop and _background_loop.is_running():
        _background_loop.call_soon_threadsafe(_background_loop.stop)

    if _background_thread and _background_thread.is_alive():
        _background_thread.join(timeout=0.5)

    # Close the loop to release resources
    if _background_loop:
        try:
            if not _background_loop.is_closed():
                _background_loop.close()
        except Exception:
            pass

    # Clear global references
    _background_loop = None
    _background_thread = None
    _pending_tasks.clear()
    _pending_futures.clear()


def schedule_background_task(coro: Coroutine[Any, Any, T]) -> None:
    """
    Schedule a coroutine to run in the background (fire-and-forget).

    Args:
        coro: The coroutine to run in the background
    """
    try:
        # Get or create the background event loop
        loop = _ensure_background_loop()

        # Wrap the coroutine with exception handling
        async def safe_wrapper() -> None:
            try:
                await coro
            except asyncio.CancelledError:
                pass
            except Exception:
                # Silently ignore exceptions in background tasks
                pass

        # Use run_coroutine_threadsafe to properly schedule the coroutine
        # This returns a concurrent.futures.Future, not an asyncio.Task
        future = asyncio.run_coroutine_threadsafe(safe_wrapper(), loop)
        
        # Track the future so we can wait for it on cleanup
        _pending_futures.add(future)

        # Add callback to handle completion
        def cleanup_future(fut: Any) -> None:
            _pending_futures.discard(fut)
            try:
                # Try to get the result to clear any exceptions
                fut.result()
            except Exception:
                pass

        future.add_done_callback(cleanup_future)

    except Exception:
        # If anything fails, close the coroutine to prevent warnings
        try:
            coro.close()
        except Exception:
            pass


__all__ = [
    "schedule_background_task",
]

