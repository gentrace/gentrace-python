"""
GenAI Semantic Conventions Example

This example demonstrates using OpenTelemetry GenAI semantic conventions
with native OTEL handles while still using Gentrace init() for setup.
It shows a simple LLM span wrapped by an outer interaction span.

How to run:
1. Set environment variables:
   export GENTRACE_API_KEY="your-api-key"
   export OPENAI_API_KEY="your-openai-key"
   export GENTRACE_BASE_URL="https://gentrace.ai/api"  # optional
   export GENTRACE_PIPELINE_ID="your-pipeline-id"  # optional

2. Run the example:
   python examples/genai-semantic-conventions.py
"""

import os
import json
import asyncio
from typing import Any, Dict, List, cast

from dotenv import load_dotenv
from openai import AsyncOpenAI
from opentelemetry import trace
from opentelemetry.trace import Status, StatusCode

from gentrace import init, interaction

# Load environment variables
load_dotenv()

# Initialize Gentrace with OpenTelemetry setup enabled
init(
    api_key=os.getenv("GENTRACE_API_KEY", ""),
    base_url=os.getenv("GENTRACE_BASE_URL", "https://gentrace.ai/api"),
    otel_setup=True,
)


async def main() -> None:
    # Get the tracer
    tracer = trace.get_tracer("genai-example", "1.0.0")
    
    # Create OpenAI client
    client = AsyncOpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
    )

    # Example 1: Simple chat completion with system message
    @interaction(
        name="ask-question",
        pipeline_id=os.getenv("GENTRACE_PIPELINE_ID", "genai-example-pipeline"),
    )
    async def ask_question(question: str) -> str:
        # Create a child span with GenAI semantic conventions
        with tracer.start_as_current_span("openai-chat-completion") as span:
            try:
                # Set GenAI attributes according to semantic conventions
                span.set_attributes({
                    "gen_ai.system": "openai",
                    "gen_ai.request.model": "gpt-4.1-nano",
                    "gen_ai.operation.name": "chat",
                    "service.name": "genai-semantic-example",
                })

                system_message = "You are a helpful assistant that explains complex topics simply."

                # Add system message as event
                span.add_event("gen_ai.system.message", {
                    "role": "system",
                    "content": system_message,
                })

                # Add user message as event
                span.add_event("gen_ai.user.message", {
                    "role": "user",
                    "content": question,
                })

                print("Sending chat completion request...")

                completion = await client.chat.completions.create(
                    model="gpt-4.1-nano",
                    messages=[
                        {"role": "system", "content": system_message},
                        {"role": "user", "content": question},
                    ],
                    temperature=0.7,
                )

                assistant_message = completion.choices[0].message.content or ""

                # Add choice event for the completion
                span.add_event("gen_ai.choice", {
                    "index": 0,
                    "content": assistant_message,
                    "role": "assistant",
                    "finish_reason": completion.choices[0].finish_reason,
                })

                span.set_status(Status(StatusCode.OK))

                return assistant_message
            except Exception as error:
                span.record_exception(error)
                span.set_status(Status(StatusCode.ERROR, str(error)))
                raise

    # Example 2: Function calling with real API invocation
    @interaction(
        name="function-calling-with-api",
        pipeline_id=os.getenv("GENTRACE_PIPELINE_ID", "genai-tools-pipeline"),
    )
    async def simulate_tool_call() -> str:
        with tracer.start_as_current_span("openai-function-calling-simulation") as span:
            try:
                span.set_attributes({
                    "gen_ai.system": "openai",
                    "gen_ai.request.model": "gpt-4.1-nano",
                    "gen_ai.operation.name": "chat",
                    "service.name": "genai-semantic-example",
                })

                # Simulate a conversation that's already in progress with tool usage
                user_question = "What's the weather like in San Francisco?"

                # Previous assistant response that decided to use a tool
                assistant_tool_call_message: Dict[str, Any] = {
                    "content": "",
                    "tool_calls": [
                        {
                            "id": "call_abc123",
                            "type": "function",
                            "function": {
                                "name": "get_weather",
                                "arguments": '{"location": "San Francisco, CA", "unit": "fahrenheit"}',
                            },
                        },
                    ],
                }

                # Tool execution result
                tool_response = {"temperature": 72, "unit": "fahrenheit", "conditions": "sunny"}
                tool_response_string = json.dumps(tool_response)

                # Add all input messages to represent the conversation history
                span.add_event("gen_ai.user.message", {
                    "role": "user",
                    "content": user_question,
                })

                span.add_event("gen_ai.assistant.message", {
                    "role": "assistant",
                    "content": assistant_tool_call_message["content"],
                    "tool_calls": json.dumps(assistant_tool_call_message["tool_calls"]),
                })

                span.add_event("gen_ai.tool.message", {
                    "role": "tool",
                    "content": tool_response_string,
                    "name": "get_weather",
                })

                # Make the actual OpenAI API call with the full conversation
                print("Making OpenAI API call with tool context (requesting 2 choices)...")

                # Convert tool_calls to proper format for OpenAI API
                from openai.types.chat import (
                    ChatCompletionToolMessageParam,
                    ChatCompletionUserMessageParam,
                    ChatCompletionAssistantMessageParam,
                )
                from openai.types.chat.chat_completion_message_tool_call_param import ChatCompletionMessageToolCallParam

                tool_calls = [
                    ChatCompletionMessageToolCallParam(
                        id=cast(str, tc["id"]),
                        type="function",
                        function={
                            "name": cast(str, tc["function"]["name"]),
                            "arguments": cast(str, tc["function"]["arguments"])
                        }
                    )
                    for tc in cast(List[Dict[str, Any]], assistant_tool_call_message["tool_calls"])
                ]

                completion = await client.chat.completions.create(
                    model="gpt-4.1-nano",
                    messages=[
                        ChatCompletionUserMessageParam(role="user", content=user_question),
                        ChatCompletionAssistantMessageParam(
                            role="assistant",
                            content=assistant_tool_call_message["content"],
                            tool_calls=tool_calls,
                        ),
                        ChatCompletionToolMessageParam(
                            role="tool",
                            content=tool_response_string,
                            tool_call_id="call_abc123",
                        ),
                    ],
                    n=2,  # Request 2 different choices
                    temperature=1,  # Add some variation between choices
                )

                # Dynamically add choice events based on the API response
                for index, choice in enumerate(completion.choices):
                    span.add_event("gen_ai.choice", {
                        "index": index,
                        "content": choice.message.content or "",
                        "role": "assistant",
                        "finish_reason": choice.finish_reason,
                    })

                span.set_status(Status(StatusCode.OK))

                # Return the first choice as the primary response
                return completion.choices[0].message.content or ""
            except Exception as error:
                span.record_exception(error)
                span.set_status(Status(StatusCode.ERROR, str(error)))
                raise

    # Example 1: Simple question
    print("=== Example 1: Simple Chat Completion ===")
    question = "Explain quantum computing in one sentence."
    print(f"Question: {question}")

    answer = await ask_question(question)
    print(f"Answer: {answer}")

    # Example 2: Simulated function calling
    print("\n=== Example 2: Simulated Function Calling ===")
    print("Simulating a conversation with tool usage...")

    weather_answer = await simulate_tool_call()
    print(f"Answer: {weather_answer}")

    # Wait for spans to flush
    print("\nWaiting for spans to flush...")
    await asyncio.sleep(2)


if __name__ == "__main__":
    asyncio.run(main())