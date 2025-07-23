"""Simplified background task scheduling using run_in_executor."""

import asyncio
from typing import Any, TypeVar, Coroutine

T = TypeVar("T")


def schedule_background_task(coro: Coroutine[Any, Any, T]) -> None:
    """
    Schedule a coroutine to run in the background (fire-and-forget).
    
    Uses the default thread pool executor to run the task without blocking.
    
    Args:
        coro: The coroutine to run in the background
    """
    try:
        # Get the current event loop, or create one if needed
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            # No event loop in current thread, create a new one
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        
        # Define a sync function that runs the coroutine
        def run_coro() -> None:
            """Run the coroutine in its own event loop."""
            try:
                # Create a new event loop for this thread
                new_loop = asyncio.new_event_loop()
                asyncio.set_event_loop(new_loop)
                try:
                    # Run the coroutine to completion
                    new_loop.run_until_complete(coro)
                except Exception:
                    # Silently ignore exceptions in background tasks
                    pass
                finally:
                    # Clean up the loop
                    new_loop.close()
                    asyncio.set_event_loop(None)
            except Exception:
                # Silently ignore exceptions in event loop setup/teardown
                pass
            finally:
                # Always ensure coroutine is closed regardless of where an exception occurs
                try:
                    coro.close()
                except Exception:
                    pass
        
        # Schedule the sync function to run in the default thread pool
        # Using None as the executor argument makes Python use its default
        # ThreadPoolExecutor, which is lazily created and managed by asyncio
        loop.run_in_executor(None, run_coro)
        
    except Exception:
        # If scheduling fails, close the coroutine to prevent warnings
        try:
            coro.close()
        except Exception:
            pass


__all__ = [
    "schedule_background_task",
]