"""
Progress reporting for evaluation runs.

This module provides different progress reporting strategies for displaying
the progress of test case execution during evaluations.
"""

import logging
from abc import ABC, abstractmethod
from typing import Optional
from typing_extensions import override

from rich.console import Console
from rich.progress import (
    TaskID,
    Progress,
    BarColumn,
    TextColumn,
    SpinnerColumn,
    TimeElapsedColumn,
    MofNCompleteColumn,
)


class ProgressReporter(ABC):
    """
    Abstract base class for progress reporting during evaluation runs.
    
    Implementations can provide different visualization strategies
    for tracking the progress of test case execution.
    """
    
    @abstractmethod
    def start(self, pipeline_id: str, total: int) -> None:
        """
        Initialize the progress reporter for a new evaluation run.
        
        Args:
            pipeline_id: The ID of the pipeline being evaluated.
            total: The total number of test cases to be executed.
        """
        pass
    
    
    @abstractmethod
    def increment(self, test_name: str) -> None:
        """
        Report that a single test case has been completed.
        
        Args:
            test_name: The name or identifier of the completed test case.
        """
        pass
    
    @abstractmethod
    def stop(self) -> None:
        """
        Finalize the progress reporter after all test cases have been executed.
        
        This should be called whether the evaluation completed successfully or not.
        """
        pass


class SimpleProgressReporter(ProgressReporter):
    """
    Simple progress reporter that outputs line-by-line progress.
    
    Ideal for CI/CD environments where interactive terminals are not available
    or when you want persistent, searchable logs of each test case execution.
    
    Example output:
        Running experiment with 50 test cases...
        [1/50] Running test case: "Login test"
        [2/50] Running test case: "Signup test"
        ...
        [50/50] Running test case: "Logout test"
        Evaluation complete.
    """
    
    def __init__(self, logger: Optional[logging.Logger] = None) -> None:
        """
        Initialize the simple progress reporter.
        
        Args:
            logger: Optional logger instance. If not provided, uses the module logger.
        """
        self.total = 0
        self.current = 0
        self.pipeline_id = ""
        self.logger = logger if logger is not None else logging.getLogger("gentrace")
    
    @override
    def start(self, pipeline_id: str, total: int) -> None:
        """Initialize a new evaluation run with line-by-line output."""
        self.pipeline_id = pipeline_id
        self.total = total
        self.current = 0
        
        message = f"\nRunning experiment with {total} test {'case' if total == 1 else 'cases'}..."
        self.logger.info(message)
    
    def update_current_test(self, test_name: str) -> None:
        """
        Update the current test case being processed.
        
        Note: SimpleProgressReporter doesn't display the current test separately,
        so this method is a no-op.
        
        Args:
            test_name: The name of the test case currently being processed.
        """
        # SimpleProgressReporter shows progress line-by-line and doesn't
        # need to update the current test display
        pass
    
    @override
    def increment(self, test_name: str) -> None:
        """Report the completion of a test case."""
        self.current += 1
        message = f"[{self.current}/{self.total}] Running test case: \"{test_name}\""
        self.logger.info(message)
    
    @override
    def stop(self) -> None:
        """Report the completion of the evaluation run."""
        self.logger.info("Evaluation complete.")


class RichProgressReporter(ProgressReporter):
    """
    Interactive progress bar reporter using the rich library.
    
    Creates a visual progress bar that updates in place, ideal for
    local development and interactive terminal sessions.
    
    Example output:
        ████████████████░░░░ | Test Case Name        | 80% | 40/50
    """
    
    def __init__(self) -> None:
        """Initialize the rich progress reporter."""
        self.console = Console(stderr=True)
        self.progress: Optional[Progress] = None
        self.task_id: Optional[TaskID] = None
        self.current_test_name = ""
        self.completed_count = 0
    
    @override
    def start(self, pipeline_id: str, total: int) -> None:
        """Initialize a new progress bar for the evaluation run."""
        # Create progress bar with custom format
        self.progress = Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            MofNCompleteColumn(),
            TimeElapsedColumn(),
            console=self.console,
            transient=False,  # Keep the bar visible after completion
        )
        
        self.progress.start()
        self.task_id = self.progress.add_task(
            description=self._format_test_name("Starting..."),
            total=total
        )
        self.completed_count = 0
    
    def update_current_test(self, test_name: str) -> None:
        """Update the display to show the current test case being processed."""
        if self.progress and self.task_id is not None:
            self.current_test_name = test_name
            self.progress.update(
                self.task_id,
                description=self._format_test_name(f"Running: {test_name}")
            )
    
    @override
    def increment(self, test_name: str) -> None:
        """Report the completion of a test case and increment the progress bar."""
        if self.progress and self.task_id is not None:
            self.completed_count += 1
            self.progress.update(
                self.task_id,
                advance=1,
                description=self._format_test_name(f"Completed: {test_name}")
            )
    
    @override
    def stop(self) -> None:
        """Finalize the progress bar and cleanup."""
        if self.progress and self.task_id is not None:
            # Update final message
            self.progress.update(
                self.task_id,
                description=self._format_test_name("Evaluation complete")
            )
            # Stop the progress bar
            self.progress.stop()
            self.progress = None
            self.task_id = None
    
    def _format_test_name(self, name: str, max_length: int = 40) -> str:
        """
        Format a test name to fit within a fixed width.
        
        Args:
            name: The test name to format.
            max_length: Maximum length for the name display.
            
        Returns:
            The formatted name, truncated with ellipsis if necessary.
        """
        if len(name) <= max_length:
            return name.ljust(max_length)
        return name[:max_length - 3] + "..."


__all__ = [
    "ProgressReporter",
    "SimpleProgressReporter", 
    "RichProgressReporter",
]