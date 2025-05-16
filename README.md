# Gentrace Python SDK

[![PyPI version](https://img.shields.io/pypi/v/gentrace.svg)](https://pypi.org/project/gentrace-py/)

This library provides tools to instrument and evaluate your AI applications using Gentrace.

The full API documentation can be found in [api.md](api.md).

## Installation

```sh
# install from PyPI
pip install --pre gentrace-py
```

## Core Concepts

The Gentrace SDK exposes several key functions to help you instrument and evaluate your AI pipelines:

- **`init`** – Initialise the SDK with your API key and optional base URL.
- **`interaction`** – Decorator to trace a single function that performs your core AI logic.
- **`experiment`** – Context decorator that groups related evaluation runs.
- **`eval`** – Decorator that defines a single evaluation (test case) to run inside an experiment.
- **`eval_dataset`** – Helper that runs an interaction against every test-case in a dataset.

All of these utilities rely on OpenTelemetry to capture and export spans, which represent units of work or operations within your application. These spans are then sent to Gentrace for visualization and analysis. Make sure you have an OTel SDK running (see [OpenTelemetry Integration](#opentelemetry-integration)).

## Basic Usage

### 1. Initialisation

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
        model="gpt-4o",
        messages=[{"role": "user", "content": query}]
    )
    return response.choices[0].message.content
```

Each call to a function decorated with `@interaction` (like `query_ai` above) creates a span, capturing its execution details and any associated metadata, inputs, and outputs. This span is then sent to Gentrace.

### 3. Testing and Evaluation

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
        schema=QueryInputsSchema, # Extra validation with Pydantic of the test case structure
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

## OpenTelemetry Integration

OpenTelemetry **must** be running for spans created by `interaction`, `experiment`, `eval`, and `eval_dataset` to be exported. The OpenTelemetry SDK is included as a dependency of this package.

Example setup:

```python
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry import trace
import os

# In virtually all cases, you should use https://gentrace.ai/api as the base URL
GENTRACE_BASE_URL = os.environ.get('GENTRACE_BASE_URL', 'https://gentrace.ai/api')
GENTRACE_API_KEY = os.environ['GENTRACE_API_KEY']

resource = Resource.create({
    "service.name": "my-gentrace-app"
})

provider = TracerProvider(resource=resource)
trace.set_tracer_provider(provider)

exporter = OTLPSpanExporter(
    endpoint=f"{GENTRACE_BASE_URL}/otel/v1/traces",
    headers={
        "Authorization": f"Bearer {GENTRACE_API_KEY}"
    },
)
processor = SimpleSpanProcessor(exporter)
provider.add_span_processor(processor)

print("OpenTelemetry SDK started – spans will be sent to Gentrace.")
```

## Examples

## Setup
Create a virtual environment with [`uv`](https://docs.astral.sh/uv/getting-started/installation/#standalone-installer) and install dependencies:

```bash
uv venv
source venv/bin/activate # May differ for your shell (e.g. fish → venv/bin/activate.fish)
uv pip install .[openai]
```

Check the [`examples/`](examples) directory for runnable scripts that demonstrate the patterns above.

Each example script requires specific environment variables to be set. Check the documentation at the top of each script for details on the required variables.

```bash
GENTRACE_API_KEY=api-key \
OPENAI_API_KEY=openai-api-key \
GENTRACE_BASE_URL=https://gentrace.ai/api \
GENTRACE_PIPELINE_ID=pipeline-id \
python examples/interaction.py
```

## Requirements

Python 3.8 or newer.

## Contributing

See the [contributing guide](./CONTRIBUTING.md).

## Support

Questions or feedback? [support@gentrace.ai](mailto:support@gentrace.ai)

