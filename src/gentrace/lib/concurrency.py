"""Concurrency utilities for managing async and sync task execution."""

import atexit
import threading
from typing import Optional
from multiprocessing import cpu_count
from concurrent.futures import ThreadPoolExecutor

class ThreadPoolSingleton:
    """
    A singleton thread pool manager for running synchronous functions in parallel.
    """
    
    _instance: Optional["ThreadPoolSingleton"] = None
    _lock = threading.Lock()
    
    def __new__(cls) -> "ThreadPoolSingleton":
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self) -> None:
        if not hasattr(self, "_initialized"):
            self._thread_pool: Optional[ThreadPoolExecutor] = None
            self._max_workers: int = cpu_count()
            self._lock = threading.Lock()
            self._initialized = True
    
    def get_thread_pool(self) -> ThreadPoolExecutor:
        """Get or create the thread pool executor."""
        if self._thread_pool is None:
            with self._lock:
                if self._thread_pool is None:
                    self._thread_pool = ThreadPoolExecutor(
                        max_workers=self._max_workers,
                        thread_name_prefix="gentrace-worker-"
                    )
        return self._thread_pool
    
    def set_max_workers(self, max_workers: int) -> None:
        """Set the maximum number of worker threads."""
        with self._lock:
            self._max_workers = max_workers
            # If thread pool already exists, we need to recreate it
            if self._thread_pool is not None:
                old_pool = self._thread_pool
                self._thread_pool = ThreadPoolExecutor(
                    max_workers=self._max_workers,
                    thread_name_prefix="gentrace-worker-"
                )
                # Shutdown the old pool gracefully
                old_pool.shutdown(wait=False)
    
    def shutdown(self, wait: bool = True) -> None:
        """Shutdown the thread pool."""
        with self._lock:
            if self._thread_pool is not None:
                self._thread_pool.shutdown(wait=wait)
                self._thread_pool = None


# Global thread pool singleton
_THREAD_POOL = ThreadPoolSingleton()


def _cleanup_thread_pool() -> None:
    """Clean up the thread pool on exit."""
    try:
        _THREAD_POOL.shutdown(wait=False)  # Don't wait on exit, let Python clean up
    except Exception:
        pass  # Ignore errors during cleanup


# Register cleanup on exit
atexit.register(_cleanup_thread_pool)


def get_thread_pool() -> ThreadPoolExecutor:
    """Get the global thread pool executor."""
    return _THREAD_POOL.get_thread_pool()


def set_thread_pool_max_workers(max_workers: int) -> None:
    """Set the maximum number of worker threads in the global thread pool."""
    _THREAD_POOL.set_max_workers(max_workers)






__all__ = [
    "ThreadPoolSingleton",
    "get_thread_pool",
    "set_thread_pool_max_workers",
]