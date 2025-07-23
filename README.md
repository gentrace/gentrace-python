# Gentrace Python SDK

<!-- prettier-ignore -->
[![PyPI version](https://img.shields.io/pypi/v/gentrace-py.svg?label=pypi%20(stable))](https://pypi.org/project/gentrace-py/)

This library provides tools to instrument and evaluate your AI applications using Gentrace.

The full API documentation can be found in [api.md](api.md).

## Installation

```sh
# install from PyPI
pip install gentrace-py
```

## Core Concepts

The Gentrace SDK exposes several key functions to help you instrument and evaluate your AI pipelines:

- **`init`** – Initialise the SDK with your API key and optional base URL.
- **`interaction`** – Decorator to trace a single function that performs your core AI logic. ([Requires OpenTelemetry](#opentelemetry-integration))
- **`experiment`** – Context decorator that groups related evaluation runs. ([Requires OpenTelemetry](#opentelemetry-integration))
- **`eval`** – Decorator that defines a single evaluation (test case) to run inside an experiment. ([Requires OpenTelemetry](#opentelemetry-integration))
- **`eval_dataset`** – Helper that runs an interaction against every test-case in a dataset. ([Requires OpenTelemetry](#opentelemetry-integration))

All of these utilities rely on OpenTelemetry to capture and export spans, which represent units of work or operations within your application. These spans are then sent to Gentrace for visualization and analysis. Make sure you have an OTel SDK running (see [OpenTelemetry Integration](#opentelemetry-integration)).

## Basic Usage

### 1. Initialisation (`init`)

> **TIP**
> You can get your Gentrace API key at [https://gentrace.ai/s/api-keys](https://gentrace.ai/s/api-keys)

```python
import os
from gentrace import init

GENTRACE_API_KEY = os.environ["GENTRACE_API_KEY"]

init(
    api_key=GENTRACE_API_KEY,
    # Optional for self-hosted deployments: base_url=os.environ.get("GENTRACE_BASE_URL", "https://gentrace.ai/api")
)

print("Gentrace initialised!")
```

### 2. Instrumenting Your Code (`interaction`)

Wrap the function that contains your AI logic so each call is traced.

```python
import openai

from gentrace import interaction, init

OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]

GENTRACE_API_KEY = os.environ["GENTRACE_API_KEY"]
GENTRACE_PIPELINE_ID = os.environ["GENTRACE_PIPELINE_ID"]

init(
    api_key=GENTRACE_API_KEY,
    # Optional for self-hosted deployments: base_url=os.environ.get("GENTRACE_BASE_URL", "https://gentrace.ai/api")
)

client = OpenAI(api_key=OPENAI_API_KEY)


@interaction(pipeline_id=GENTRACE_PIPELINE_ID)
async def query_ai(query: str) -> str | None:
    response = client.chat.completions.create(
        model="gpt-4o", messages=[{"role": "user", "content": query}]
    )
    return response.choices[0].message.content
```

Each call to a function decorated with `@interaction` (like `query_ai` above) creates a span, capturing its execution details and any associated metadata, inputs, and outputs. This span is then sent to Gentrace.

#### Simplified Usage (Default Pipeline)

If your organization has a default pipeline configured, you can use `@interaction` without specifying a pipeline ID:

```python
from gentrace import interaction, init

init(api_key=GENTRACE_API_KEY)

# Simplest usage - no pipeline ID required
@interaction()
def process_data(data: str) -> str:
    return f"Processed: {data}"

# With custom attributes but no pipeline ID
@interaction(attributes={"model": "gpt-4", "temperature": 0.7})
def analyze_data(data: str) -> dict:
    return {"analysis": data.upper(), "length": len(data)}

# Async function with custom name
@interaction(name="Custom Analysis")
async def async_process(data: str) -> str:
    await asyncio.sleep(0.1)
    return f"Async processed: {data}"
```

When no `pipeline_id` is provided, the SDK automatically uses your organization's default pipeline.

### 3. Lower-Level Tracing (`traced`)

Use the `traced` decorator to wrap any function with OpenTelemetry tracing, creating a span for its execution. This is useful for instrumenting helper functions or specific blocks of code within a larger system. ([Requires OpenTelemetry](#opentelemetry-integration))

```python
import asyncio

from gentrace import traced, interaction
from openai import OpenAI

client = OpenAI()

USER_ID = "<user_id>"
PIPELINE_ID = "<pipeline_id>"


@traced(name="OpenAI Call")
async def summarize_user(user_info: str) -> str:
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": f"Summarize the following user info: {user_info}"}],
    )
    return response.choices[0].message.content


@traced(name="Get User Info DB Call")
async def get_user_info(user_id: str) -> str:
    # This would be a database call in a real application
    return f"User {user_id}: Sample information"


@interaction(pipeline_id=GENTRACE_PIPELINE_ID)
async def main_task(input: str) -> str:
    user_info = await get_user_info(input)
    return await summarize_user(user_info)


asyncio.run(main_task(USER_ID))
```

You can also provide additional `attributes` to the `@traced` decorator to add to the span. Like `interaction`, this also requires OpenTelemetry to be set up properly.

### 4. Testing and Evaluation

#### Running Single Evaluations (`eval`)

Use `experiment` to create a testing context and `eval` for individual test cases.

```python
import asyncio
from gentrace import experiment, eval
import os

GENTRACE_API_KEY = os.environ["GENTRACE_API_KEY"]
GENTRACE_PIPELINE_ID = os.environ["GENTRACE_PIPELINE_ID"]

init(
    api_key=GENTRACE_API_KEY,
    # Optional for self-hosted deployments: base_url=os.environ.get("GENTRACE_BASE_URL", "https://gentrace.ai/api")
)


@interaction(pipeline_id=GENTRACE_PIPELINE_ID)
async def query_ai(query: str) -> str | None:
    # Implementation from previous example
    pass


@experiment(pipeline_id=GENTRACE_PIPELINE_ID)
async def simple_evals() -> None:
    @eval(name="capital-of-france")
    async def paris_test() -> None:
        result = await query_ai("What is the capital of France?")
        assert result and "Paris" in result

    # Immediately invoke the eval
    await paris_test()


asyncio.run(simple_evals())
```

The `@eval` decorator creates a 'test' span for `paris_test`. When `query_ai` (an `@interaction`-decorated function) is called within `paris_test`, its own interaction span is also created. This interaction span is nested under the 'test' span, creating a trace of the evaluation. Both spans are sent to Gentrace.

#### Running Dataset Evaluations (`eval_dataset`)

```python
import asyncio, os
from gentrace import TestCase, TestInput, init, experiment, eval_dataset, test_cases_async
from typing_extensions import TypedDict
from pydantic import BaseModel

GENTRACE_API_KEY = os.environ["GENTRACE_API_KEY"]
GENTRACE_PIPELINE_ID = os.environ["GENTRACE_PIPELINE_ID"]
GENTRACE_DATASET_ID = os.environ["GENTRACE_DATASET_ID"]

init(
    api_key=GENTRACE_API_KEY,
    # Optional for self-hosted deployments: base_url=os.environ.get("GENTRACE_BASE_URL", "https://gentrace.ai/api")
)


# Option 1️⃣: Fetch test cases from Gentrace
async def fetch_test_cases() -> list[TestCase]:
    cases = await test_cases_async.list(dataset_id=GENTRACE_DATASET_ID)

    # Each test case within cases.data has an attribute "inputs" with the structure: { query: str }
    return cases.data


# Option 2️⃣: Provide locally defined test cases by using TestInput and a typed dict
# (in this case QueryInputs)
class QueryInputs(TypedDict):
    query: str


def custom_test_cases() -> list[TestInput[QueryInputs]]:
    return [
        TestInput[QueryInputs](name="Test Case 1", inputs={"query": "Hello, World!"}),
        TestInput[QueryInputs](name="Test Case 2", inputs={"query": "How does this work?"}),
    ]


# Optionally, validate the structure of your inputs with Pydantic
class QueryInputsSchema(BaseModel):
    query: str


@experiment(pipeline_id=GENTRACE_PIPELINE_ID)
async def dataset_evals() -> None:
    # Option 1️⃣: Use test cases from Gentrace
    await eval_dataset(
        data=fetch_test_cases,
        interaction=query_ai,
        schema=QueryInputsSchema,  # Extra validation with Pydantic of the test case structure
    )

    # Option 2️⃣: Use locally defined test cases
    await eval_dataset(
        data=custom_test_cases,
        interaction=query_ai,
    )


asyncio.run(dataset_evals())
```

The `eval_dataset` utility creates a 'test' span for each test case processed from the dataset. If the `interaction` argument (e.g., `query_ai`) is an `@interaction`-decorated function, then for each test case, an additional interaction span is created.

This interaction span is nested within its corresponding 'test' span. All these spans are sent to Gentrace, allowing detailed analysis of how the interaction performs across the entire dataset.

### Span Hierarchy Visualization

```
[SPAN] Test Case 1
├─── [SPAN] @interaction Function
│    ├─── [SPAN] @traced (LLM call)
│    │    ├─── Model: gpt-4
│    │    ├─── Input: "What is the capital of France?"
│    │    └─── Output: "The capital of France is Paris."
│    │
│    └─── [SPAN] @traced (Tool call)
│         ├─── Tool: search_wikipedia
│         ├─── Input: "Paris"
│         └─── Output: "Paris is the capital and most populous city of France..."
```

This hierarchical structure allows Gentrace to provide detailed analysis of performance and behavior at different levels of granularity.

## OpenTelemetry Integration

OpenTelemetry **must** be running for spans created by `interaction`, `experiment`, `eval`, and `eval_dataset` to be exported. The OpenTelemetry SDK is included as a dependency of this package.

Example setup:

```python
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry import trace
from gentrace import GentraceSampler, GentraceSpanProcessor
import os

# In virtually all cases, you should use https://gentrace.ai/api as the base URL
GENTRACE_BASE_URL = os.environ.get("GENTRACE_BASE_URL", "https://gentrace.ai/api")
GENTRACE_API_KEY = os.environ["GENTRACE_API_KEY"]

resource = Resource.create({"service.name": "my-gentrace-app"})

provider = TracerProvider(
    resource=resource,
    sampler=GentraceSampler(),  # Use GentraceSampler for selective tracing
)
trace.set_tracer_provider(provider)

exporter = OTLPSpanExporter(
    endpoint=f"{GENTRACE_BASE_URL}/otel/v1/traces",
    headers={"Authorization": f"Bearer {GENTRACE_API_KEY}"},
)

# Add GentraceSpanProcessor to propagate gentrace.sample attribute
provider.add_span_processor(GentraceSpanProcessor())
provider.add_span_processor(SimpleSpanProcessor(exporter))

processor = SimpleSpanProcessor(exporter)
provider.add_span_processor(processor)

print("OpenTelemetry SDK started – spans will be sent to Gentrace.")
```

### GentraceSampler and GentraceSpanProcessor

Gentrace provides two specialized OpenTelemetry components to help control which spans are sent to Gentrace:

#### GentraceSampler

The `GentraceSampler` is a custom OpenTelemetry sampler that selectively samples spans based on the presence of a `gentrace.sample` attribute. This helps reduce the volume of telemetry data by only sending relevant spans to Gentrace.

```python
from gentrace import GentraceSampler
from opentelemetry.sdk.trace import TracerProvider

# Create a tracer provider with the GentraceSampler
provider = TracerProvider(resource=resource, sampler=GentraceSampler())
```

How it works:
- The sampler checks for the `gentrace.sample` key in the OpenTelemetry Baggage or as a span attribute
- If `gentrace.sample` is set to `"true"`, the span will be sampled and exported to Gentrace
- Otherwise, the span will be dropped and not exported

This is particularly useful for filtering out spans that are not relevant to Gentrace tracing, reducing noise and data volume.

#### GentraceSpanProcessor

The `GentraceSpanProcessor` is a specialized span processor that ensures the `gentrace.sample` attribute is properly propagated from the OpenTelemetry Baggage to span attributes.

```python
from gentrace import GentraceSpanProcessor

# Add the GentraceSpanProcessor to your tracer provider
provider.add_span_processor(GentraceSpanProcessor())
```

How it works:
- When a span starts, the processor checks for the `gentrace.sample` key in the current OpenTelemetry Baggage
- If found, it extracts this value and adds it as an attribute to the span
- This ensures that the sampling attribute is propagated correctly to all spans that need to be tracked by Gentrace

Using both components together provides optimal control over which spans are sent to Gentrace:

```python
# Complete example
provider = TracerProvider(resource=resource, sampler=GentraceSampler())
trace.set_tracer_provider(provider)

# Add GentraceSpanProcessor first to ensure proper attribute propagation
provider.add_span_processor(GentraceSpanProcessor())

# Then add your exporter processor
provider.add_span_processor(SimpleSpanProcessor(exporter))
```

## Examples

See the [examples guide](./examples/README.md) for instructions on how to run the examples.


## Requirements

Python 3.8 or newer.

## Contributing

See the [contributing guide](./CONTRIBUTING.md).

## Support

Questions or feedback? [support@gentrace.ai](mailto:support@gentrace.ai)
