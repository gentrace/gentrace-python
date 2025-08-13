"""
Centralized warning system for Gentrace Python SDK.
Mirrors the pattern from the Node.js SDK with GT_ prefixed warning IDs.
"""

from typing import Any, Set, Dict, List, Union, Optional

from rich.text import Text
from rich.panel import Panel
from rich.console import Group, Console

from .constants import MAX_EVAL_DATASET_CONCURRENCY

# Global tracking of displayed warnings
_displayed_warnings: Set[str] = set()


class GentraceWarningOptions:
    """Options for creating a GentraceWarning."""
    
    def __init__(
        self,
        warning_id: str,
        title: str,
        message: Union[str, List[str]],
        learn_more_url: Optional[str] = None,
        suppression_hint: Optional[str] = None,
        border_color: str = "yellow"
    ):
        self.warning_id = warning_id
        self.title = title
        self.message = message
        self.learn_more_url = learn_more_url
        self.suppression_hint = suppression_hint
        self.border_color = border_color


class GentraceWarning:
    """Base class for Gentrace warning display."""
    
    def __init__(self, options: GentraceWarningOptions):
        self.warning_id = options.warning_id
        self.title = options.title
        self.message = options.message if isinstance(options.message, list) else [options.message]
        self.learn_more_url = options.learn_more_url
        self.suppression_hint = options.suppression_hint
        self.border_color = options.border_color
    
    def get_simple_message(self) -> str:
        """Get the warning message as a simple string."""
        return " ".join(self.message)
    
    def display(self) -> None:
        """Display the warning with rich formatting."""
        # Check if this warning has already been displayed
        if self.warning_id in _displayed_warnings:
            return
        
        # Mark as displayed
        _displayed_warnings.add(self.warning_id)
        
        try:
            # Build content parts
            content_parts: List[Text] = []
            
            # Add main message
            for line in self.message:
                content_parts.append(Text(line))
            
            # Add learn more URL if provided
            if self.learn_more_url:
                content_parts.append(Text(""))  # Empty line
                content_parts.append(Text(f"Learn more: {self.learn_more_url}", style="cyan"))
            
            # Add suppression hint if provided
            if self.suppression_hint:
                content_parts.append(Text(""))  # Empty line
                content_parts.append(Text(self.suppression_hint, style="dim"))
            
            # Create panel with consistent title format
            formatted_title = f"⚠ {self.title} [{self.warning_id}]"
            warning_panel = Panel(
                Group(*content_parts),
                title=f"[bold {self.border_color}]{formatted_title}[/bold {self.border_color}]",
                border_style=self.border_color,
                title_align="center",
                padding=(1, 2),
            )
            
            # Print with padding
            console: Console = Console(stderr=True)
            console.print("")
            console.print(warning_panel)
            console.print("")
            
        except Exception:
            # Fallback to simple console warning if formatting fails
            print(f"\n⚠ {self.title} [{self.warning_id}]\n\n{self.get_simple_message()}\n", file=__import__('sys').stderr)


# Pre-defined warning types (factory functions)
class GentraceWarnings:
    """Factory functions for creating specific warning types."""
    
    @staticmethod
    def PipelineInvalidError(pipeline_id: str) -> GentraceWarning:
        return GentraceWarning(GentraceWarningOptions(
            warning_id="GT_PipelineInvalidError",
            title="Gentrace Invalid Pipeline ID",
            message=[
                f"Pipeline ID '{pipeline_id}' is not a valid UUID.",
                "",
                "Please verify the pipeline ID matches what's shown in the Gentrace UI.",
            ],
            learn_more_url="https://gentrace.ai/docs/reference/sdk-errors#gt-pipelineinvaliderror",
            suppression_hint="To suppress this warning: @interaction(..., suppress_warnings=True)",
            border_color="red"
        ))
    
    @staticmethod
    def PipelineNotFoundError(pipeline_id: str) -> GentraceWarning:
        return GentraceWarning(GentraceWarningOptions(
            warning_id="GT_PipelineNotFoundError",
            title="Gentrace Pipeline Not Found",
            message=[
                f"Pipeline '{pipeline_id}' does not exist or is not accessible.",
                "",
                "Please verify the pipeline ID matches what's shown in the Gentrace UI.",
            ],
            learn_more_url="https://gentrace.ai/docs/reference/sdk-errors#gt-pipelinenotfounderror",
            suppression_hint="To suppress this warning: @interaction(..., suppress_warnings=True)",
            border_color="red"
        ))
    
    @staticmethod
    def PipelineUnauthorizedError(pipeline_id: str) -> GentraceWarning:
        return GentraceWarning(GentraceWarningOptions(
            warning_id="GT_PipelineUnauthorizedError",
            title="Gentrace Pipeline Unauthorized",
            message=[
                f"Access denied to pipeline '{pipeline_id}'.",
                "",
                "Please check your GENTRACE_API_KEY has the correct permissions.",
            ],
            learn_more_url="https://gentrace.ai/docs/reference/sdk-errors#gt-pipelineunauthorizederror",
            suppression_hint="To suppress this warning: @interaction(..., suppress_warnings=True)",
            border_color="red"
        ))
    
    @staticmethod
    def PipelineError(pipeline_id: str, error_message: Optional[str] = None) -> GentraceWarning:
        return GentraceWarning(GentraceWarningOptions(
            warning_id="GT_PipelineError",
            title="Gentrace Pipeline Error",
            message=[
                f"Failed to validate pipeline '{pipeline_id}'.",
                "",
                f"Error: {error_message or 'Unknown error'}",
            ],
            learn_more_url=None,
            suppression_hint="To suppress this warning: @interaction(..., suppress_warnings=True)",
            border_color="red"
        ))
    
    @staticmethod
    def OtelNotConfiguredError() -> GentraceWarning:
        return GentraceWarning(GentraceWarningOptions(
            warning_id="GT_OtelNotConfiguredError",
            title="Gentrace Configuration Warning",
            message=[
                "OpenTelemetry SDK does not appear to be configured. This means that Gentrace features",
                "like @interaction, @eval, @traced, and eval_dataset() will not record any data to the",
                "Gentrace UI.",
                "",
                "You likely disabled automatic OpenTelemetry setup by passing otel_setup=False to init().",
                "If so, you can fix this by either:",
                "",
                "1. Remove the otel_setup=False option from init() to enable automatic setup",
                "2. Or manually configure OpenTelemetry yourself (see documentation)",
            ],
            learn_more_url="https://gentrace.ai/docs/reference/sdk-errors#gt-otelnotconfigurederror",
            suppression_hint="To suppress this warning: @interaction(..., suppress_warnings=True)"
        ))
    
    @staticmethod
    def AutoInitializationWarning() -> GentraceWarning:
        return GentraceWarning(GentraceWarningOptions(
            warning_id="GT_AutoInitializationWarning",
            title="Auto-Initialization",
            message=[
                "Gentrace was automatically initialized from environment variables.",
                "",
                "This likely means your init() call is not being executed, which can cause issues:",
                "• Custom options passed to init() won't be applied (instrumentations, debug, etc.)",
                "• Instrumentations may not work correctly",
                "• OpenTelemetry configuration may be incomplete",
                "",
                "To fix this, ensure init() is called before executing any Gentrace functions.",
                "",
                "Note: Each **distinct** process/service must call init() before using Gentrace functions.",
            ],
            learn_more_url="https://gentrace.ai/docs/reference/sdk-errors#gt-autoinitializationwarning",
            suppression_hint="To suppress this warning: @interaction(..., suppress_warnings=True)"
        ))
    
    @staticmethod
    def OtelGlobalError(error: Exception) -> GentraceWarning:
        error_message = str(error) if error else "Unknown error"
        return GentraceWarning(GentraceWarningOptions(
            warning_id="GT_OtelGlobalError",
            title="OpenTelemetry Global Error",
            message=[
                "An error occurred in the OpenTelemetry instrumentation.",
                "",
                f"Error: {error_message}",
                "",
                "This may affect trace collection and instrumentation functionality.",
                "Common causes include:",
                "• Network connectivity issues with the trace endpoint",
                "• Invalid configuration or credentials",
                "• Resource limits or memory constraints",
            ],
            learn_more_url="https://gentrace.ai/docs/reference/sdk-errors#gt-otelglobalerror",
            suppression_hint="To suppress OpenTelemetry errors: Use a custom error handler in setup()",
            border_color="red"
        ))
    
    @staticmethod
    def MissingApiKeyError() -> GentraceWarning:
        return GentraceWarning(GentraceWarningOptions(
            warning_id="GT_MissingApiKeyError",
            title="Gentrace API Key Missing",
            message=[
                "Gentrace API key is missing or invalid. The SDK cannot connect to Gentrace",
                "without a valid API key.",
                "",
                "To fix this, provide your API key in one of these ways:",
                "",
                "1. Set the GENTRACE_API_KEY environment variable:",
                "   export GENTRACE_API_KEY=\"your-api-key\"",
                "",
                "2. Pass it directly to init():",
                "   init(api_key=\"your-api-key\")",
                "",
                "Get your API key from: https://gentrace.ai/s/api-keys",
            ],
            learn_more_url="https://gentrace.ai/docs/reference/sdk-errors#gt-missingapikeyerror",
            border_color="red"
        ))
    
    @staticmethod
    def HighConcurrencyError(max_concurrency: int) -> GentraceWarning:
        return GentraceWarning(GentraceWarningOptions(
            warning_id="GT_HighConcurrencyError",
            title="High Concurrency Error",
            message=[
                f"max_concurrency of {max_concurrency} exceeds the maximum allowed value of {MAX_EVAL_DATASET_CONCURRENCY}.",
                "",
                "Please use a lower value:",
                f"    eval_dataset(..., max_concurrency={MAX_EVAL_DATASET_CONCURRENCY})",
                "",
                "High concurrency can overwhelm your API providers and may lead to rate limiting.",
            ],
            learn_more_url=None,
            suppression_hint=None,
            border_color="red"
        ))
    
    @staticmethod
    def MultipleInitWarning(call_number: int, diff_lines: List[str], init_history: List[Dict[str, Any]]) -> GentraceWarning:
        from ..lib.utils import format_timestamp
        
        # Build history display
        history_lines: List[str] = []
        for init_call in init_history:
            timestamp = init_call.get('timestamp')
            if timestamp is not None:
                if hasattr(timestamp, 'timestamp'):
                    # It's a datetime object
                    timestamp_str = format_timestamp(timestamp, relative=True)
                elif isinstance(timestamp, (int, float)):
                    timestamp_str = format_timestamp(timestamp, relative=True)
                else:
                    timestamp_str = str(timestamp)
            else:
                timestamp_str = ''
            history_lines.append(f"  - Call #{init_call['callNumber']}: {timestamp_str}")
        
        # Build message
        message_lines = [
            f"Gentrace init() has been called {call_number} times.",
            "",
            "Previous initializations:",
        ] + history_lines + [
            "",
            "Configuration changes detected:",
        ] + diff_lines + [
            "",
            "Note: Multiple init() calls can lead to unexpected behavior.",
            "The most recent configuration will be used.",
        ]
        
        return GentraceWarning(GentraceWarningOptions(
            warning_id="GT_MultipleInitWarning",
            title="Multiple Initialization Detected",
            message=message_lines,
            learn_more_url=None,
            suppression_hint="To suppress this warning, ensure init() is only called once",
            border_color="yellow"
        ))
    
    @staticmethod
    def OtelPartialFailureWarning(rejected_count: int, error_message: Optional[str] = None) -> GentraceWarning:
        return GentraceWarning(GentraceWarningOptions(
            warning_id="GT_OtelPartialFailureWarning",
            title="Some spans were not ingested",
            message=[
                f"Gentrace could not ingest {rejected_count} {'span' if rejected_count == 1 else 'spans'}.",
                "",
                f"Reason: {error_message or ('The server rejected this span' if rejected_count == 1 else 'The server rejected these spans')}",
                "",
                "This may indicate:",
                "• Invalid span data or attributes",
                "• Rate limiting or quota issues",
                "• Server-side validation failures",
            ],
            learn_more_url="https://gentrace.ai/docs/reference/sdk-errors#gt-otelpartialfailurewarning",
            suppression_hint="This warning will only be shown once per session",
            border_color="red"
        ))
    
    @staticmethod
    def OtelAuthenticationError() -> GentraceWarning:
        return GentraceWarning(GentraceWarningOptions(
            warning_id="GT_OtelAuthenticationError",
            title="Trace Export Authentication Failed",
            message=[
                "Failed to export traces to Gentrace due to authentication failure (401).",
                "",
                "Please check your Gentrace API key:",
                "",
                "1. Verify GENTRACE_API_KEY environment variable is set correctly",
                "2. Ensure the API key is valid and not revoked",
                "",
                "Get your API key from: https://gentrace.ai/s/api-keys",
            ],
            learn_more_url="https://gentrace.ai/docs/reference/sdk-errors#gt-otelauthenticationerror",
            suppression_hint="This warning will only be shown once per session",
            border_color="red"
        ))