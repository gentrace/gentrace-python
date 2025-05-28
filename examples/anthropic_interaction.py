"""
This example script showcases the use of the Gentrace Python SDK to trace
and monitor interactions within an application using Anthropic's Claude API. It demonstrates:
- Setting up OpenTelemetry for distributed tracing.
- Tracing synchronous and asynchronous calls to Anthropic's API.
- Utilizing Gentrace's @traced and @interaction decorators for enhanced observability.
- Handling both successful operations and simulated errors.
- Following genAI semantic conventions for AI observability.

To run this example, ensure the following environment variables are set:
    GENTRACE_API_KEY: Your Gentrace API token for authentication.
    ANTHROPIC_API_KEY: Your Anthropic API key.
    GENTRACE_BASE_URL: The base URL for your Gentrace instance (e.g., http://localhost:3000).
"""

import os
import atexit
import asyncio
from typing import Dict

from anthropic import Anthropic, AsyncAnthropic
from opentelemetry import trace
from anthropic.types import Message, MessageParam
from opentelemetry.trace import Span, Status, StatusCode
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.util.types import AttributeValue
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace.export import SimpleSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter

from gentrace import GentraceSampler, GentraceSpanProcessor, traced, interaction

resource = Resource(attributes={"service.name": "my-otel-anthropic-interaction-example-app"})
tracer_provider = TracerProvider(resource=resource, sampler=GentraceSampler())

api_key = os.getenv("GENTRACE_API_KEY", "")
anthropic_api_key = os.getenv("ANTHROPIC_API_KEY", "")
gentrace_base_url = os.getenv("GENTRACE_BASE_URL", "")
pipeline_id = os.getenv("GENTRACE_PIPELINE_ID", "")

if not api_key:
    raise ValueError("GENTRACE_API_KEY environment variable not set.")
if not anthropic_api_key:
    raise ValueError("ANTHROPIC_API_KEY environment variable not set.")
if not gentrace_base_url:
    raise ValueError("GENTRACE_BASE_URL environment variable not set.")

otlp_headers: Dict[str, str] = {}
if api_key:
    otlp_headers["Authorization"] = f"Bearer {api_key}"

span_exporter = OTLPSpanExporter(
    endpoint=f"{gentrace_base_url}/otel/v1/traces",
    headers=otlp_headers,
)

client = Anthropic(api_key=anthropic_api_key)
async_client = AsyncAnthropic(api_key=anthropic_api_key)

# Instantiate and add GentraceSpanProcessor to enrich spans with `gentrace.sample`
gentrace_baggage_processor = GentraceSpanProcessor()
tracer_provider.add_span_processor(gentrace_baggage_processor)

simple_export_processor = SimpleSpanProcessor(span_exporter)
tracer_provider.add_span_processor(simple_export_processor)
trace.set_tracer_provider(tracer_provider)


@traced(name="sync_anthropic_llm_call", attributes={"llm_vendor": "Anthropic", "llm_model": "claude-3-5-sonnet-20241022"})
def sync_anthropic_llm_call(prompt: str) -> Message:
    current_span: Span = trace.get_current_span()
    
    model = "claude-3-5-sonnet-20241022"
    max_tokens = 1000
    messages: list[MessageParam] = [{"role": "user", "content": prompt}]
    
    # Set genAI semantic convention attributes for the request
    request_attributes: Dict[str, AttributeValue] = {}
    request_attributes["gen_ai.system"] = "anthropic"
    request_attributes["gen_ai.request.model"] = model
    request_attributes["gen_ai.request.max_tokens"] = max_tokens
    request_attributes["server.address"] = "api.anthropic.com"
    request_attributes["server.port"] = 443
    
    for index, msg_param in enumerate(messages):
        request_attributes[f"gen_ai.prompt.{index}.role"] = str(msg_param["role"])
        request_attributes[f"gen_ai.prompt.{index}.content"] = str(msg_param["content"])
    current_span.set_attributes(request_attributes)
    
    # Add events for request messages
    for index, msg in enumerate(messages):
        current_span.add_event(
            f"gen_ai.{msg['role']}.message",
            attributes={
                "gen_ai.message.index": index,
                "gen_ai.message.role": str(msg["role"]),
                "gen_ai.message.content": str(msg["content"]),
            }
        )
    
    try:
        response = client.messages.create(
            model=model,
            max_tokens=max_tokens,
            messages=messages
        )
        
        # Set response attributes
        response_attributes: Dict[str, AttributeValue] = {}
        response_attributes["gen_ai.response.id"] = response.id
        response_attributes["gen_ai.response.model"] = response.model
        response_attributes["gen_ai.response.finish_reason"] = response.stop_reason or ""
        response_attributes["gen_ai.usage.input_tokens"] = response.usage.input_tokens
        response_attributes["gen_ai.usage.output_tokens"] = response.usage.output_tokens
        
        completion_idx = 0
        for content_block in response.content:
            if content_block.type == "text":
                response_attributes[f"gen_ai.completion.{completion_idx}.role"] = response.role
                response_attributes[f"gen_ai.completion.{completion_idx}.content"] = content_block.text
                completion_idx += 1
        current_span.set_attributes(response_attributes)
        
        # Add events for response content
        for index, content in enumerate(response.content):
            if content.type == "text":
                current_span.add_event(
                    "gen_ai.content",
                    attributes={
                        "gen_ai.content.index": index,
                        "gen_ai.content.type": content.type,
                        "gen_ai.content.text": content.text,
                    }
                )
        
        current_span.set_status(Status(StatusCode.OK))
        return response
    except Exception as e:
        current_span.record_exception(e)
        current_span.set_status(Status(StatusCode.ERROR, str(e)))
        current_span.set_attribute("error.type", type(e).__name__)
        raise


@traced(name="async_anthropic_llm_call", attributes={"llm_vendor": "Anthropic", "llm_model": "claude-3-5-sonnet-20241022"})
async def async_anthropic_llm_call(prompt: str) -> Message:
    current_span: Span = trace.get_current_span()
    
    model = "claude-3-5-sonnet-20241022"
    max_tokens = 1000
    messages: list[MessageParam] = [{"role": "user", "content": prompt}]
    
    # Set genAI semantic convention attributes for the request
    request_attributes: Dict[str, AttributeValue] = {}
    request_attributes["gen_ai.system"] = "anthropic"
    request_attributes["gen_ai.request.model"] = model
    request_attributes["gen_ai.request.max_tokens"] = max_tokens
    request_attributes["server.address"] = "api.anthropic.com"
    request_attributes["server.port"] = 443

    for index, msg_param in enumerate(messages):
        request_attributes[f"gen_ai.prompt.{index}.role"] = str(msg_param["role"])
        request_attributes[f"gen_ai.prompt.{index}.content"] = str(msg_param["content"])
    current_span.set_attributes(request_attributes)
    
    # Add events for request messages
    for index, msg in enumerate(messages):
        current_span.add_event(
            f"gen_ai.{msg['role']}.message",
            attributes={
                "gen_ai.message.index": index,
                "gen_ai.message.role": str(msg["role"]),
                "gen_ai.message.content": str(msg["content"]),
            }
        )
    
    try:
        response = await async_client.messages.create(
            model=model,
            max_tokens=max_tokens,
            messages=messages
        )
        
        # Set response attributes
        response_attributes: Dict[str, AttributeValue] = {}
        response_attributes["gen_ai.response.id"] = response.id
        response_attributes["gen_ai.response.model"] = response.model
        response_attributes["gen_ai.response.finish_reason"] = response.stop_reason or ""
        response_attributes["gen_ai.usage.input_tokens"] = response.usage.input_tokens
        response_attributes["gen_ai.usage.output_tokens"] = response.usage.output_tokens

        completion_idx = 0
        for content_block in response.content:
            if content_block.type == "text":
                response_attributes[f"gen_ai.completion.{completion_idx}.role"] = response.role
                response_attributes[f"gen_ai.completion.{completion_idx}.content"] = content_block.text
                completion_idx += 1
        current_span.set_attributes(response_attributes)
        
        # Add events for response content
        for index, content in enumerate(response.content):
            if content.type == "text":
                current_span.add_event(
                    "gen_ai.content",
                    attributes={
                        "gen_ai.content.index": index,
                        "gen_ai.content.type": content.type,
                        "gen_ai.content.text": content.text,
                    }
                )
        
        current_span.set_status(Status(StatusCode.OK))
        return response
    except Exception as e:
        current_span.record_exception(e)
        current_span.set_status(Status(StatusCode.ERROR, str(e)))
        current_span.set_attribute("error.type", type(e).__name__)
        raise


@interaction(pipeline_id=pipeline_id, name="my_sync_anthropic_interaction_example", attributes={"custom_attr": "sync_value"})
def my_synchronous_interaction(x: int, y: int) -> int:
    result = x * y
    llm_prompt = f"Summarize the result of a synchronous operation: {x} * {y} = {result}"
    llm_response = sync_anthropic_llm_call(llm_prompt)
    print("Final result:", llm_response)
    if result < 0:
        raise ValueError("Synchronous interaction result cannot be negative in this example")
    return result


@interaction(pipeline_id=pipeline_id, name="my_async_anthropic_interaction_example", attributes={"custom_attr": "async_value"})
async def my_asynchronous_interaction(name: str, delay: float = 0.1) -> str:
    await asyncio.sleep(delay)
    llm_prompt = (
        f"Describe an asynchronous interaction with user '{name}' after a delay. Super concise, 10 words or less."
    )
    await async_anthropic_llm_call(llm_prompt)

    result = f"Interacted with {name}!"
    if name == "error":
        raise RuntimeError("Asynchronous interaction encountered a simulated error")
    return result


async def main() -> None:
    async_result_success = await my_asynchronous_interaction("GentraceUser")
    print("Final result:", async_result_success)
    try:
        await my_asynchronous_interaction("error")
    except RuntimeError as e:
        print(f"Caught expected error from asynchronous interaction: {e}\n")

    print("\nCheck the Gentrace dashboard to see all interactions and traces!")


if __name__ == "__main__":
    atexit.register(tracer_provider.shutdown)
    asyncio.run(main())

