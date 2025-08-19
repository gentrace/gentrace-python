from typing import Optional
from typing_extensions import override

from opentelemetry import baggage
from opentelemetry.trace import Span
from opentelemetry.context import Context
from opentelemetry.sdk.trace import ReadableSpan, SpanProcessor

from gentrace.lib.constants import ATTR_GENTRACE_SAMPLE_KEY, ATTR_GENTRACE_IN_EXPERIMENT


class GentraceSpanProcessor(SpanProcessor):
    """
    A span processor that extracts Gentrace-specific baggage from the context
    and adds it as span attributes. This processor is used to propagate
    Gentrace-specific context across service boundaries.
    """

    @override
    def force_flush(self, timeout_millis: int = 30000) -> bool:
        """
        Forces to export all finished spans.
        """
        # no-op
        return True

    @override
    def on_start(self, span: Span, parent_context: Optional[Context] = None) -> None:
        """
        Called when a Span is started, if the span.is_recording()
        returns true.
        """
        for key in [ATTR_GENTRACE_SAMPLE_KEY, ATTR_GENTRACE_IN_EXPERIMENT]:
            value = baggage.get_baggage(key, context=parent_context)
            if isinstance(value, str):
                span.set_attribute(key, value)

    @override
    def on_end(self, span: ReadableSpan) -> None:
        """
        Called when a ReadableSpan is ended, if the span.is_recording()
        returns true.
        """
        # no-op
        pass

    @override
    def shutdown(self) -> None:
        """
        Shuts down the processor. Called when SDK is shut down. This is an
        opportunity for processor to do any cleanup required.
        """
        # no-op
        pass
