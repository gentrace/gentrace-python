from typing import Optional, Sequence
from typing_extensions import override

from opentelemetry.trace import Link, SpanKind, TraceState
from opentelemetry.baggage import get_baggage
from opentelemetry.util.types import Attributes
from opentelemetry.context.context import Context
from opentelemetry.sdk.trace.sampling import (
    Sampler,
    Decision,
    SamplingResult,
)

from .constants import ATTR_GENTRACE_SAMPLE_KEY


class GentraceSampler(Sampler):
    """
    A sampler that samples spans based on the presence of a 'gentrace.sample' baggage entry
    or span attribute. If either is set to 'true', the span will be sampled.
    """

    @override
    def should_sample(
        self,
        parent_context: Optional[Context],
        trace_id: int,
        name: str,
        kind: Optional[SpanKind] = None,
        attributes: Attributes = None,
        links: Optional[Sequence[Link]] = None,
        trace_state: Optional[TraceState] = None,
    ) -> SamplingResult:
        """
        Determines whether a span should be sampled based on the presence of a 'gentrace.sample'
        (ATTR_GENTRACE_SAMPLE_KEY) baggage entry or span attribute.

        Args:
            parent_context: The parent context.
            trace_id: The trace ID of the span.
            name: The name of the span.
            kind: The kind of the span.
            attributes: The attributes of the span.
            links: The links of the span.
            trace_state: The trace state of the span.

        Returns:
            A sampling result indicating whether the span should be sampled.
        """
        sample_baggage_value = get_baggage(ATTR_GENTRACE_SAMPLE_KEY, context=parent_context)
        if sample_baggage_value == "true":
            return SamplingResult(Decision.RECORD_AND_SAMPLE, attributes, trace_state)

        if attributes and attributes.get(ATTR_GENTRACE_SAMPLE_KEY) == "true":
            return SamplingResult(Decision.RECORD_AND_SAMPLE, attributes, trace_state)

        return SamplingResult(Decision.DROP, attributes, trace_state)

    @override
    def __str__(self) -> str:
        return "GentraceSampler"

    @override
    def get_description(self) -> str:
        return "GentraceSampler"
