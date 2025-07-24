import sys
import json
import logging
import warnings
from typing import Any, Set, Dict, List, Tuple, Union, Optional, cast
from datetime import datetime
from collections.abc import Sequence

from pydantic import BaseModel
from rich.live import Live
from rich.text import Text
from rich.tree import Tree
from rich.panel import Panel
from rich.table import Table, Column
from rich.syntax import Syntax
from rich.console import Group, Console, RenderableType
from rich.spinner import Spinner
from opentelemetry import trace as trace_api
from rich.markdown import Markdown
from rich.progress import (
    TaskID,
    Progress,
    BarColumn,
    TextColumn,
    SpinnerColumn,
    TimeElapsedColumn,
    MofNCompleteColumn,
    TimeRemainingColumn,
)
from opentelemetry.util import types as otel_types
from opentelemetry.sdk.trace import TracerProvider as SDKTracerProvider

logger = logging.getLogger("gentrace")

OTLP_MAX_INT_SIZE = (2**63) - 1  # Max 64-bit signed integer
OTLP_MIN_INT_SIZE = -(2**63)  # Min 64-bit signed integer

CIRCULAR_REFERENCE_PLACEHOLDER = "[CircularReference]"

# Global flag to ensure the OpenTelemetry configuration warning is issued only once per session
_otel_config_warning_issued = False

# Default spinner style for Gentrace operations
DEFAULT_SPINNER = "dots"



class GentraceConsole:
    """Centralized console management for Gentrace with rich formatting capabilities."""

    _instance: Optional["GentraceConsole"] = None
    _console: Console

    def __new__(cls) -> "GentraceConsole":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._console = Console(stderr=True, highlight=True)
        return cls._instance

    @property
    def console(self) -> Console:
        return self._console

    def print(self, *args: Any, **kwargs: Any) -> None:
        """Print with rich formatting."""
        self._console.print(*args, **kwargs)

    def log(self, message: str, style: Optional[str] = None) -> None:
        """Print a log message with optional styling."""
        if style:
            self._console.print(f"[{style}]{message}[/{style}]")
        else:
            self._console.print(message)

    def success(self, message: str) -> None:
        """Print a success message."""
        self._console.print(f"[green]✓[/green] {message}")

    def error(self, message: str) -> None:
        """Print an error message."""
        self._console.print(f"[red]✗[/red] {message}")

    def warning(self, message: str) -> None:
        """Print a warning message."""
        self._console.print(f"[yellow]⚠[/yellow] {message}")

    def info(self, message: str) -> None:
        """Print an info message."""
        self._console.print(f"[blue]ℹ[/blue] {message}")

    def step_progress(self, text: str = "") -> Spinner:
        """Create a spinner for step progress."""
        return Spinner(DEFAULT_SPINNER, text, style="blue")

    def step_completed(self, message: str) -> RenderableType:
        """Return a renderable for completed step."""
        return f"[green]✓[/green] {message}"

    def create_panel(
        self, content: Union[str, RenderableType], title: Optional[str] = None, border_style: str = "blue"
    ) -> Panel:
        """Create a styled panel."""
        return Panel(content, title=title, border_style=border_style, title_align="left")

    def create_table(self, title: Optional[str] = None, **kwargs: Any) -> Table:
        """Create a styled table."""
        return Table(title=title, show_header=True, header_style="bold magenta", **kwargs)

    def create_progress_bar(self) -> Progress:
        """Create a styled progress bar."""
        return Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            MofNCompleteColumn(),
            TimeRemainingColumn(),
            console=self._console,
            transient=True,
        )

    def create_tree(self, label: RenderableType, guide_style: str = "gray50") -> Tree:
        """Create a tree structure for hierarchical display."""
        return Tree(label, guide_style=guide_style)

    def display_dict(self, data: Dict[str, Any], title: Optional[str] = None) -> None:
        """Display a dictionary in a formatted table."""
        table = self.create_table(title=title)
        table.add_column("Key", style="cyan", no_wrap=True)
        table.add_column("Value", style="white")

        for key, value in data.items():
            table.add_row(str(key), str(value))

        self._console.print(table)

    def display_list(self, items: List[Any], title: Optional[str] = None, columns: Optional[List[str]] = None) -> None:
        """Display a list in a formatted table."""
        if not items:
            self.info("No items to display")
            return

        table = self.create_table(title=title)

        if columns:
            for col in columns:
                table.add_column(col)
        else:
            table.add_column("Item")

        for item in items:
            if isinstance(item, (list, tuple)) and columns:
                # Cast item to sequence to help type checker
                elem_list = cast(Union[List[Any], Tuple[Any, ...]], item)
                table.add_row(*[str(elem) for elem in elem_list])
            else:
                # Cast to help type checker with the str() call
                table.add_row(str(cast(Any, item)))

        self._console.print(table)

    def code_block(self, code: str, language: str = "python", title: Optional[str] = None) -> None:
        """Display a syntax-highlighted code block."""
        syntax = Syntax(code, language, theme="monokai", line_numbers=True)
        if title:
            self._console.print(self.create_panel(syntax, title=title))
        else:
            self._console.print(syntax)

    def markdown(self, text: str) -> None:
        """Display markdown formatted text."""
        md = Markdown(text)
        self._console.print(md)


def get_console() -> GentraceConsole:
    """Get the singleton GentraceConsole instance."""
    return GentraceConsole()


def pretty_print_json(data: Any, title: Optional[str] = None) -> None:
    """Pretty print JSON data with syntax highlighting."""
    console = get_console()
    json_str = json.dumps(data, indent=2)
    console.code_block(json_str, language="json", title=title)


def pretty_print_error(error: Exception, show_traceback: bool = True) -> None:
    """Pretty print an error with optional traceback."""
    console = get_console()

    error_panel = Panel(
        str(error),
        title=f"[red]{type(error).__name__}[/red]",
        border_style="red",
        title_align="left",
    )
    console.console.print(error_panel)

    if show_traceback:
        import traceback

        tb = traceback.format_exc()
        console.code_block(tb, language="python", title="Traceback")


class ProgressHandler:
    """Handler for progress tracking with rich output."""

    def __init__(self, total: Optional[int] = None, description: str = "Processing..."):
        self.console = get_console()
        self.progress = Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            MofNCompleteColumn() if total else TextColumn(""),
            TimeElapsedColumn(),
            console=self.console.console,
            transient=True,
        )
        self.task_id: Optional[TaskID] = None
        self.total = total
        self.description = description
        self._started = False

    def __enter__(self) -> "ProgressHandler":
        self.start()
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        self.stop()

    def start(self) -> None:
        """Start the progress display."""
        if not self._started:
            self.progress.start()
            self.task_id = self.progress.add_task(self.description, total=self.total)
            self._started = True

    def update(self, advance: int = 1, description: Optional[str] = None) -> None:
        """Update progress."""
        if self.task_id is not None:
            if description:
                self.progress.update(self.task_id, description=description)
            self.progress.update(self.task_id, advance=advance)

    def stop(self) -> None:
        """Stop the progress display."""
        if self._started:
            self.progress.stop()
            self._started = False


def display_table(
    columns: Sequence[Union[Column, str]],
    rows: Sequence[Sequence[Union[Text, str]]],
    title: Optional[str] = None,
    caption: Optional[str] = None,
    show_lines: bool = False,
    show_edge: bool = True,
) -> None:
    """Display data in a beautifully formatted table."""
    console = get_console()

    table = Table(
        title=title,
        caption=caption,
        show_lines=show_lines,
        show_edge=show_edge,
        show_header=True,
        header_style="bold magenta",
    )

    # Add columns
    for col in columns:
        if isinstance(col, str):
            table.add_column(col)
        else:
            # Assume it's a Column object
            table.add_column(str(col))

    # Add rows
    for row in rows:
        table.add_row(*[str(cell) for cell in row])

    console.console.print(table)


def format_timestamp(timestamp: Union[int, float, datetime], relative: bool = False) -> str:
    """Format a timestamp for display."""
    if isinstance(timestamp, (int, float)):
        dt = datetime.fromtimestamp(timestamp)
    else:
        dt = timestamp

    if relative:
        # Calculate relative time
        now = datetime.now()
        delta = now - dt

        if delta.days > 0:
            return f"{delta.days}d ago"
        elif delta.seconds > 3600:
            return f"{delta.seconds // 3600}h ago"
        elif delta.seconds > 60:
            return f"{delta.seconds // 60}m ago"
        else:
            return "just now"
    else:
        return dt.strftime("%Y-%m-%d %H:%M:%S")


def _is_gentrace_initialized() -> bool:
    """Check if Gentrace has been initialized via init()."""
    gentrace_module = sys.modules.get("gentrace")
    return bool(gentrace_module and getattr(gentrace_module, "__gentrace_initialized", False))


def _is_otel_configured() -> bool:
    """Check if OpenTelemetry SDK TracerProvider is configured."""
    provider = trace_api.get_tracer_provider()
    return isinstance(provider, SDKTracerProvider)


def ensure_initialized(suppress_warnings: bool = False) -> None:
    """
    Ensures Gentrace is properly initialized with OpenTelemetry configured.
    
    This function:
    1. First attempts auto-initialization if environment variables are set
    2. Then checks if OpenTelemetry is configured
    3. Shows a warning if otel_setup was explicitly set to False but OTEL is not configured
    
    Args:
        suppress_warnings: If True, suppresses auto-initialization warnings.
    """
    import os
    
    # First, try auto-initialization if needed
    if not _is_otel_configured() and not _is_gentrace_initialized():
        api_key = os.environ.get("GENTRACE_API_KEY")
        if api_key:
            # Show warning about auto-initialization unless suppressed
            if not suppress_warnings:
                _show_auto_init_warning()
            
            from .init import init
            init_kwargs: Dict[str, Any] = {"api_key": api_key}
            base_url = os.environ.get("GENTRACE_BASE_URL")
            if base_url:
                init_kwargs["base_url"] = base_url
            init(**init_kwargs)
            # After auto-init, OTEL should be configured, so we can return
            return
    
    # If we reach here, either:
    # 1. OTEL is already configured (good)
    # 2. Gentrace was initialized but with otel_setup=False
    # 3. No environment variables for auto-init
    
    # Only warn if otel_setup was explicitly set to False
    otel_setup_config = getattr(sys.modules.get('gentrace'), '__gentrace_otel_setup_config', None)
    if otel_setup_config is False and not _is_otel_configured():
        # Show the warning (using the existing warning logic)
        if not suppress_warnings:
            _show_otel_warning()


def _show_auto_init_warning() -> None:
    """
    Shows a warning when Gentrace is automatically initialized from environment variables.
    """
    # Check if warnings would be suppressed for our message
    with warnings.catch_warnings(record=True) as caught_warnings:
        # Don't override filters - use whatever the user has set
        warnings.warn(
            "Gentrace was automatically initialized from environment variables",
            UserWarning,
            stacklevel=2
        )
        
    # If no warning was caught, it means it's being filtered - don't show rich display
    if not caught_warnings:
        return
    
    console = get_console()
    
    warning_content = Group(
        Text("Gentrace was automatically initialized from environment variables.", style="bold white"),
        Text(),
        Text("This likely means your init() call is not being executed, which can cause issues:", style="yellow"),
        Text("• Custom options passed to init() won't be applied (instrumentations, debug, etc.)", style="white"),
        Text("• Instrumentations may not work correctly", style="white"),
        Text("• OpenTelemetry configuration may be incomplete", style="white"),
        Text(),
        Text("Learn more: https://next.gentrace.ai/docs/sdk-reference/errors#gt-autoinitializationwarning", style="cyan"),
        Text(),
        Text("To fix this, ensure init() is called before executing decorators.", style="yellow"),
        Text(),
        Text("Note: Each distinct process/service must call init() before using @interaction decorators.", style="cyan"),
        Text(),
        Text("To suppress this warning:", style="dim"),
        Text("• Use: @interaction(pipeline_id=\"...\", suppress_warnings=True)", style="dim"),
        Text("• Or: warnings.filterwarnings('ignore', message='Gentrace was automatically initialized')", style="dim"),
    )
    
    # Create red bordered panel
    warning_panel = Panel(
        warning_content,
        title="[bold red]⚠ Warning: Auto-Initialization [GT_AutoInitializationWarning][/bold red]",
        border_style="red",
        title_align="left",
        padding=(1, 2),
    )
    
    # Code example for proper initialization
    init_code = """  from gentrace import init, interaction

  # Call this at the very beginning of your application
  init(api_key="your-api-key")

  # Then use decorators
  @interaction(pipeline_id="my-pipeline-id")
  def my_function():
      return "Hello, world!"""
    
    console.console.print(warning_panel)
    console.console.print()
    
    console.console.print(Text("Recommended initialization pattern:", style="bold cyan"))
    console.console.print()
    
    syntax = Syntax(
        init_code,
        "python",
        theme="monokai",
        line_numbers=False,
        word_wrap=True,
        background_color="default",
    )
    console.console.print(syntax)
    console.console.print()


def _show_otel_warning() -> None:
    """
    Internal function to show the OpenTelemetry configuration warning.
    This is called by ensure_initialized() when needed.
    """
    global _otel_config_warning_issued
    if _otel_config_warning_issued:
        return

    provider = trace_api.get_tracer_provider()

    if not isinstance(provider, SDKTracerProvider):
        # Check if warnings would be suppressed for our message
        with warnings.catch_warnings(record=True) as caught_warnings:
            warnings.simplefilter("always")
            warnings.warn(
                "OpenTelemetry SDK does not appear to be configured",
                UserWarning,
                stacklevel=2
            )
            
        # If no warning was caught, it means it's being filtered - don't show rich display
        if not caught_warnings:
            _otel_config_warning_issued = True
            return
        
        console = get_console()

        # Create a warning panel with rich formatting
        warning_content = Group(
            Text("OpenTelemetry SDK does not appear to be configured. This means that Gentrace features"),
            Text("like @interaction, @eval, @traced, and eval_dataset() will not record any data to the"),
            Text("Gentrace UI."),
            Text(),
            Text("Learn more: https://next.gentrace.ai/docs/sdk-reference/errors#gt-otelnotconfigurederror", style="cyan"),
            Text(),
            Text("You have two options to fix this:"),
        )

        warning_panel = Panel(
            warning_content,
            title="[bold red]⚠ Gentrace Configuration Warning [GT_OtelNotConfiguredError][/bold red]",
            border_style="red",
            title_align="left",
            padding=(1, 2),
        )

        # Init example code (recommended)
        # Add indentation to each line for visual padding
        init_example_code = """  from gentrace import init

  init(
      api_key="your-api-key",
      # otel_setup=True is the default, can be omitted
  )"""

        # Manual setup code
        # Add indentation to each line for visual padding
        manual_setup_code = """  import os
  import atexit
  from gentrace import init
  from opentelemetry import trace
  from opentelemetry.sdk.trace import TracerProvider
  from opentelemetry.sdk.resources import Resource
  from opentelemetry.sdk.trace.export import SimpleSpanProcessor
  from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter

  # Initialize Gentrace without OpenTelemetry setup
  init(
      api_key="your-api-key",
      base_url="https://gentrace.ai/api",  # or your custom endpoint
      otel_setup=False
  )

  # Set up the resource with service name
  resource = Resource(attributes={"service.name": "your-service-name"})

  # Create and set the tracer provider
  trace.set_tracer_provider(TracerProvider(resource=resource))

  # Configure the OTLP exporter for Gentrace
  otlp_headers = {"Authorization": f"Bearer {os.getenv('GENTRACE_API_KEY')}"}
  span_exporter = OTLPSpanExporter(
      endpoint=f"{os.getenv('GENTRACE_BASE_URL', 'https://gentrace.ai/api')}/otel/v1/traces",
      headers=otlp_headers
  )

  # Add the span processor
  trace.get_tracer_provider().add_span_processor(SimpleSpanProcessor(span_exporter))

  # Ensure graceful shutdown
  def shutdown_handler():
      provider = trace.get_tracer_provider()
      if hasattr(provider, 'shutdown'):
          provider.shutdown()
          print("OpenTelemetry SDK shut down successfully")

  # Register shutdown handler
  atexit.register(shutdown_handler)

  print("OpenTelemetry SDK started – spans will be sent to Gentrace.")"""

        try:
            console.console.print(warning_panel)
            console.console.print()  # Add spacing

            # Display the recommended init() approach with star emoji
            console.console.print(Text("⭐ Option 1: Use Gentrace's automatic OpenTelemetry setup (recommended):", style="bold green"))
            console.console.print()

            syntax_init = Syntax(
                init_example_code,
                "python",
                theme="monokai",
                line_numbers=False,
                word_wrap=True,
                background_color="default",
                indent_guides=True,
                code_width=100,
            )
            console.console.print(syntax_init)
            console.console.print()

            # Display the manual setup option
            console.console.print(Text("Option 2: If you have otel_setup=False, manually configure OpenTelemetry:", style="gray"))
            console.console.print()

            syntax_manual = Syntax(
                manual_setup_code,
                "python",
                theme="monokai",
                line_numbers=False,
                word_wrap=True,
                background_color="default",
                indent_guides=True,
                code_width=100,
            )
            console.console.print(syntax_manual)
            console.console.print()

            console.console.print(
                Text("Tip: Copy the code above and add it to your application setup.", style="gray")
            )
            console.console.print()
            
            console.console.print(
                Text("To suppress this warning:", style="dim")
            )
            console.console.print(
                Text("• Use: @interaction(pipeline_id=\"...\", suppress_warnings=True)", style="dim")
            )
            console.console.print(
                Text("• Or: warnings.filterwarnings('ignore', message='OpenTelemetry SDK does not appear')", style="dim")
            )
            console.console.print()  # Extra line break after suppression info

        except Exception:  # Fallback if rich formatting/printing fails
            fallback_message = """Gentrace: OpenTelemetry SDK does not appear to be configured. This means that Gentrace features like @interaction, @eval, @traced, and eval_dataset() will not record any data to the Gentrace UI.

Learn more: https://next.gentrace.ai/docs/sdk-reference/errors#gt-otelnotconfigurederror

You have two options:

⭐ Option 1: Use Gentrace's automatic OpenTelemetry setup (recommended):

    from gentrace import init
    
    init(
        api_key="your-api-key",
        # otel_setup=True is the default, can be omitted
    )

Option 2: If you have otel_setup=False, manually configure OpenTelemetry with the Gentrace endpoint.

See the documentation for the complete setup code.
"""
            warnings.warn(fallback_message, UserWarning, stacklevel=2)

        _otel_config_warning_issued = True


def display_pipeline_error(
    pipeline_id: str,
    error_type: str,
    error: Optional[Exception] = None
) -> None:
    """
    Displays a beautifully formatted pipeline error message.
    
    Args:
        pipeline_id: The pipeline ID that caused the error
        error_type: One of 'invalid-format', 'not-found', 'unauthorized', 'unknown'
        error: Optional exception object for additional context
    """
    # Check if warnings would be suppressed for our message
    warning_messages = {
        'invalid-format': f"Pipeline ID '{pipeline_id}' is not a valid UUID",
        'not-found': f"Pipeline '{pipeline_id}' does not exist",
        'unauthorized': f"Access denied to pipeline '{pipeline_id}'",
        'unknown': f"Failed to validate pipeline '{pipeline_id}'"
    }
    
    warning_message = warning_messages.get(error_type, warning_messages['unknown'])
    
    # Check if the warning would be suppressed
    with warnings.catch_warnings(record=True) as caught_warnings:
        # Use current warning filters
        warnings.warn(
            warning_message,
            UserWarning,
            stacklevel=3
        )
        
    # If no warning was caught, it's being filtered - don't show anything
    if not caught_warnings:
        return
    
    # Warning would be shown, so show rich display instead
    
    console = get_console()
    
    # Common suppression note
    suppression_note = Text(
        "To suppress this warning: warnings.filterwarnings('ignore', message='Pipeline')",
        style="dim"
    )
    
    if error_type == 'invalid-format':
        error_title = "⚠ Warning: Gentrace Invalid Pipeline ID [GT_PipelineInvalidError]"
        error_content = Group(
            Text(f"Pipeline ID '{pipeline_id}' is not a valid UUID.", style="yellow"),
            Text(),
            Text("Please verify the pipeline ID matches what's shown in the Gentrace UI.", style="white"),
            Text(),
            Text("Learn more: https://next.gentrace.ai/docs/sdk-reference/errors#gt-pipelineinvaliderror", style="cyan"),
            Text(),
            suppression_note,
        )
        border_style = "red"
    
    elif error_type == 'not-found':
        error_title = "⚠ Warning: Gentrace Pipeline Not Found [GT_PipelineNotFoundError]"
        error_content = Group(
            Text(f"Pipeline '{pipeline_id}' does not exist or is not accessible.", style="yellow"),
            Text(),
            Text("Please verify the pipeline ID matches what's shown in the Gentrace UI.", style="white"),
            Text(),
            Text("Learn more: https://next.gentrace.ai/docs/sdk-reference/errors#gt-pipelinenotfounderror", style="cyan"),
            Text(),
            suppression_note,
        )
        border_style = "red"
    
    elif error_type == 'unauthorized':
        error_title = "⚠ Warning: Gentrace Pipeline Unauthorized [GT_PipelineUnauthorizedError]"
        error_content = Group(
            Text(f"Access denied to pipeline '{pipeline_id}'.", style="yellow"),
            Text(),
            Text("Please check your GENTRACE_API_KEY has the correct permissions.", style="white"),
            Text(),
            Text("Learn more: https://next.gentrace.ai/docs/sdk-reference/errors#gt-pipelineunauthorizederror", style="cyan"),
            Text(),
            suppression_note,
        )
        border_style = "red"
    
    else:  # unknown
        error_title = "⚠ Warning: Gentrace Pipeline Error"
        error_message = error.args[0] if error and error.args else "Unknown error"
        error_content = Group(
            Text(f"Failed to validate pipeline '{pipeline_id}'.", style="yellow"),
            Text(),
            Text(f"Error: {error_message}", style="gray"),
            Text(),
            suppression_note,
        )
        border_style = "red"
    
    error_panel = Panel(
        error_content,
        title=f"[bold red]{error_title}[/bold red]",
        border_style=border_style,
        title_align="left",
        padding=(1, 2),
    )
    
    try:
        console.console.print(error_panel)
        console.console.print()
    except Exception:
        # Fallback to simple logging if rich formatting fails
        logger.error(f"Gentrace Pipeline Error: {error_type} for pipeline '{pipeline_id}'")




def _convert_pydantic_model_to_dict_if_applicable(obj: Any) -> Any:
    """Checks if an object is a Pydantic model and converts it to a dict.
    Returns the original object if it's not a Pydantic model or conversion fails.
    """
    if isinstance(obj, BaseModel):
        try:
            # Pydantic V2
            return obj.model_dump()
        except AttributeError:
            # Pydantic V1
            try:
                return obj.dict()  # type: ignore
            except AttributeError:
                # Should not happen if isinstance check passed and it's a Pydantic model
                pass  # Fall through, returning original obj
    return obj


def _gentrace_json_dumps(value: Any) -> str:
    """Helper to dump objects to JSON string, handling circular references and non-serializable types.

    This is a serialization function designed to help properly convert Open Telemetry span attributes
    or convert the function arguments and outputs to a serializable format.
    """

    # Attempt to convert top-level value if it's a Pydantic model
    value = _convert_pydantic_model_to_dict_if_applicable(value)

    seen_objects_for_this_dump: Set[int] = set()

    def default_handler(obj: Any) -> Any:
        obj_id = id(obj)
        if obj_id in seen_objects_for_this_dump:
            return CIRCULAR_REFERENCE_PLACEHOLDER

        seen_objects_for_this_dump.add(obj_id)

        # Attempt to convert Pydantic models to dict
        # Must be done before trying str(obj) as Pydantic models might have custom __str__
        processed_obj = _convert_pydantic_model_to_dict_if_applicable(obj)

        # If the object was a Pydantic model and successfully converted,
        # processed_obj will be a dict. Otherwise, it's the original obj.
        # We only proceed to str(obj) if it wasn't a Pydantic model or conversion failed.
        if processed_obj is not obj:  # Check if conversion happened
            # If it was converted (e.g. to a dict), it's ready for json.dumps
            return processed_obj

        try:
            return str(obj)
        except Exception:
            return f"[UnserializableType: {type(obj).__name__}]"

    try:
        return json.dumps(value, default=default_handler)
    except ValueError as e:
        if "Circular reference detected" in str(e):
            # This case should ideally be caught by the default_handler.
            # If it still occurs, it means a very complex or deep cycle was not fully handled before json.dumps itself gave up.
            # We return a simple placeholder for the entire problematic value.
            # To be more granular, the default_handler would need to be even more sophisticated
            # or we'd need a pre-processing step to replace cycles before calling json.dumps.
            warnings.warn(
                f"Fallback to placeholder for entire value due to complex circular reference: {e}",
                UserWarning,
                stacklevel=2,
            )
            return json.dumps(CIRCULAR_REFERENCE_PLACEHOLDER)
        raise  # Re-raise other ValueErrors
    except TypeError as e:
        # Fallback if default_handler somehow returns a type json.dumps still can't handle,
        # or if the initial `value` itself is problematic in a way that bypasses the default logic early.
        warnings.warn(
            f"Fallback JSON serialization due to TypeError: {e}. Result may be lossy.", UserWarning, stacklevel=2
        )
        # Final fallback to simple str conversion for the whole object if custom logic fails.
        return json.dumps(str(value), default=str)


def gentrace_format_otel_value(value: Any) -> otel_types.AttributeValue:
    """Convert a user attribute value to an OpenTelemetry compatible type.

    Simple types (str, bool, float) are passed through.
    Integers are checked against OTel's 64-bit range and converted to string if outside.
    All other types (lists, dicts, complex objects) are JSON stringified using a safe dumper.
    """
    if isinstance(value, (str, bool, float)):
        return value
    elif isinstance(value, int):
        if not (OTLP_MIN_INT_SIZE <= value <= OTLP_MAX_INT_SIZE):
            warnings.warn(
                f"Integer value {value} is outside the OTLP 64-bit signed integer range "
                f"({OTLP_MIN_INT_SIZE} to {OTLP_MAX_INT_SIZE}), it will be converted to a string.",
                UserWarning,
                stacklevel=2,
            )
            return str(value)
        return value
    else:
        # For lists, dicts, complex objects, etc., JSON stringify safely.
        return _gentrace_json_dumps(value)


def gentrace_format_otel_attributes(attributes: Dict[str, Any]) -> Dict[str, otel_types.AttributeValue]:
    """Prepare an attributes dictionary for OpenTelemetry by formatting each value."""
    return {key: gentrace_format_otel_value(value) for key, value in attributes.items()}


def is_pydantic_v1() -> bool:
    """Checks if the installed Pydantic version is V1."""
    try:
        from pydantic import VERSION

        return VERSION.startswith("1.")
    except ImportError:
        return False


# Additional pretty printing utilities


def create_status_spinner(text: str = "Processing...", spinner_style: str = DEFAULT_SPINNER) -> Live:
    """Create a live status spinner that can be updated."""
    console = get_console()
    spinner = Spinner(spinner_style, text, style="blue")
    return Live(spinner, console=console.console, transient=True)


def print_trace_info(trace_id: str, span_id: str, parent_span_id: Optional[str] = None) -> None:
    """Pretty print trace information."""
    console = get_console()

    trace_info = {
        "Trace ID": trace_id,
        "Span ID": span_id,
        "Parent Span ID": parent_span_id or "None",
    }

    console.display_dict(trace_info, title="Trace Information")


def print_evaluation_results(results: Dict[str, Any], title: str = "Evaluation Results") -> None:
    """Pretty print evaluation results with formatting."""
    console = get_console()

    # Create a tree for hierarchical display
    tree = console.create_tree(f"[bold blue]{title}[/bold blue]")

    for key, value in results.items():
        if isinstance(value, dict):
            subtree = tree.add(f"[cyan]{key}[/cyan]")
            value_dict = cast(Dict[str, Any], value)
            for sub_k, sub_v in value_dict.items():
                subtree.add(f"[green]{sub_k}[/green]: {sub_v}")
        else:
            tree.add(f"[green]{key}[/green]: {value}")

    console.console.print(tree)


def print_function_call_summary(
    function_name: str,
    args: "tuple[Any, ...]",
    kwargs: "dict[str, Any]",
    result: Any = None,
    duration: Optional[float] = None,
    error: Optional[Exception] = None,
) -> None:
    """Pretty print a function call summary."""
    console = get_console()

    # Create panel content
    content_lines = [
        f"[bold cyan]Function:[/bold cyan] {function_name}",
        f"[bold cyan]Arguments:[/bold cyan] {args}",
        f"[bold cyan]Keyword Arguments:[/bold cyan] {kwargs}",
    ]

    if duration is not None:
        content_lines.append(f"[bold cyan]Duration:[/bold cyan] {duration:.3f}s")

    if error is not None:
        content_lines.append(f"[bold red]Error:[/bold red] {type(error).__name__}: {str(error)}")
        border_style = "red"
        title = "[red]Function Call Failed[/red]"
    else:
        content_lines.append(f"[bold green]Result:[/bold green] {result}")
        border_style = "green"
        title = "[green]Function Call Completed[/green]"

    content = "\n".join(content_lines)
    panel = console.create_panel(content, title=title, border_style=border_style)
    console.console.print(panel)


__all__ = [
    "gentrace_format_otel_attributes",
    "gentrace_format_otel_value",
    "_gentrace_json_dumps",
    "is_pydantic_v1",
    "ensure_initialized",
    "GentraceConsole",
    "get_console",
    "pretty_print_json",
    "pretty_print_error",
    "ProgressHandler",
    "display_table",
    "format_timestamp",
    "create_status_spinner",
    "print_trace_info",
    "print_evaluation_results",
    "print_function_call_summary",
]
