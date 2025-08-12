"""
Progress reporting for evaluation runs.

This module provides different progress reporting strategies for displaying
the progress of test case execution during evaluations.
"""

import logging
from abc import ABC, abstractmethod
from typing import Optional
from typing_extensions import override

from rich.live import Live
from rich.text import Text
from rich.table import Table
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
    def start(self, pipeline_id: str, total: int, experiment_url: Optional[str] = None) -> None:
        """
        Initialize the progress reporter for a new evaluation run.

        Args:
            pipeline_id: The ID of the pipeline being evaluated.
            total: The total number of test cases to be executed.
            experiment_url: Optional URL to view the experiment in the Gentrace UI.
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
    def start(self, pipeline_id: str, total: int, experiment_url: Optional[str] = None) -> None:
        """Initialize a new evaluation run with line-by-line output."""
        self.pipeline_id = pipeline_id
        self.total = total
        self.current = 0

        message = f"\nRunning experiment with {total} test {'case' if total == 1 else 'cases'}..."
        self.logger.info(message)
        
        # Display the experiment URL if available
        if experiment_url:
            self.logger.info(f"Experiment URL: {experiment_url}")

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
        message = f'[{self.current}/{self.total}] Running test case: "{test_name}"'
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

    The test case name is displayed above the progress bar in a clean,
    non-overlapping way using Rich's Live display.

    Example output:
        Currently running: Test Case Name
        ━━━━━━━━━━━━━━━━━━━━ 80% • 40/50 • 0:01:23
    """

    def __init__(self) -> None:
        """Initialize the rich progress reporter."""
        self.console = Console(stderr=True)
        self.progress: Optional[Progress] = None
        self.task_id: Optional[TaskID] = None
        self.live: Optional[Live] = None
        self.current_test_name = ""
        self.completed_count = 0
        self.total_count = 0
        self.last_completed_test = ""
        self.experiment_url: Optional[str] = None

    def _create_display(self) -> Table:
        """Create the display table with current test info and progress bar."""
        table = Table.grid(padding=0)
        table.add_column(style="bold")
        
        # Add status line
        if self.current_test_name:
            table.add_row(Text(f"Currently running: {self.current_test_name}", style="bold blue"))
        elif self.last_completed_test:
            table.add_row(Text(f"Last completed: {self.last_completed_test}", style="green"))
        else:
            table.add_row(Text("Starting evaluation...", style="bold blue"))
        
        # Add empty row for spacing
        table.add_row()
        
        # Add progress bar
        if self.progress:
            table.add_row(self.progress)
        
        return table

    @override
    def start(self, pipeline_id: str, total: int, experiment_url: Optional[str] = None) -> None:
        """Initialize a new progress bar for the evaluation run."""
        self.total_count = total
        self.completed_count = 0
        self.current_test_name = ""
        self.last_completed_test = ""
        self.experiment_url = experiment_url
        
        # Print the experiment URL separately before starting the Live display
        # Using Rich's hyperlink markup for clickable links in supported terminals
        if experiment_url:
            # Use Rich's link markup to make the URL clickable in supported terminals
            self.console.print(f"[bold cyan]Experiment:[/bold cyan] [link={experiment_url}]{experiment_url}[/link]", crop=False, overflow="ignore")
            self.console.print()  # Add spacing

        # Create progress bar without description in the bar itself
        self.progress = Progress(
            SpinnerColumn(),
            BarColumn(bar_width=None),  # Use full terminal width
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            TextColumn("•"),
            MofNCompleteColumn(),
            TextColumn("•"),
            TimeElapsedColumn(),
            console=None,  # Don't use console directly, we'll use Live
            transient=False,
            refresh_per_second=10,
        )

        self.task_id = self.progress.add_task(
            description="",
            total=total,
        )

        # Start the live display
        self.live = Live(
            self._create_display(),
            console=self.console,
            refresh_per_second=10,
            transient=False,
        )
        self.live.start()

    def update_current_test(self, test_name: str) -> None:
        """Update the display to show the current test case being processed."""
        if self.live:
            self.current_test_name = test_name
            self.live.update(self._create_display())

    @override
    def increment(self, test_name: str) -> None:
        """Report the completion of a test case and increment the progress bar."""
        if self.progress and self.task_id is not None and self.live:
            self.completed_count += 1
            self.last_completed_test = test_name
            self.current_test_name = ""  # Clear current since it's completed
            self.progress.update(self.task_id, advance=1)
            self.live.update(self._create_display())

    @override
    def stop(self) -> None:
        """Finalize the progress bar and cleanup."""
        if self.live:
            # Update final display
            self.current_test_name = ""
            self.last_completed_test = "Evaluation complete"
            self.live.update(self._create_display())
            self.live.stop()
            
            # Print final message after stopping live display
            self.console.print("[bold green]✓ Evaluation complete[/bold green]")
            
            # Cleanup
            self.live = None
            self.progress = None
            self.task_id = None


__all__ = [
    "ProgressReporter",
    "SimpleProgressReporter",
    "RichProgressReporter",
]
