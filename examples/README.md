# Gentrace Python SDK Examples

This directory contains simplified examples demonstrating key features of the Gentrace Python SDK.

## Examples Overview

### Basic Initialization
- `init_simple.py` - Basic Gentrace initialization with default OpenTelemetry setup
- `init_manual_otel.py` - Manual OpenTelemetry configuration when you need custom control
- `init_with_instrumentation.py` - Adding automatic HTTP instrumentation

### LLM Integrations
- `openai_simple.py` - Simple OpenAI integration with Gentrace tracing
- `openai_instrumentation.py` - OpenAI with automatic OpenInference instrumentation
- `openai_agents_instrumentation.py` - OpenAI Agents (Swarm) with OpenInference instrumentation
- `anthropic_simple.py` - Anthropic Claude integration example
- `pydantic_ai_simple.py` - Simple Pydantic AI framework integration

### Evaluation
- `eval_simple.py` - Basic evaluation example using @eval decorator

## Running Examples

1. Install dependencies:
```bash
pip install -e ..
pip install openai anthropic pydantic-ai openai-agents  # For LLM examples
pip install openinference-instrumentation-openai-agents  # For OpenAI Agents instrumentation
```

2. Set environment variables:
```bash
export GENTRACE_API_KEY="your-api-key"
export GENTRACE_BASE_URL="https://gentrace.ai/api"  # or http://localhost:3000/api
export GENTRACE_PIPELINE_ID="your-pipeline-id"
export OPENAI_API_KEY="your-openai-key"  # For OpenAI examples
export ANTHROPIC_API_KEY="your-anthropic-key"  # For Anthropic examples
```

3. Run an example:
```bash
python init_simple.py
```

## Example Patterns

Each example focuses on one specific use case:
- Basic init examples show different ways to initialize Gentrace
- LLM examples demonstrate tracing AI model calls
- Evaluation examples show how to run experiments and evaluations

For more comprehensive documentation, see the [Gentrace docs](https://docs.gentrace.ai).