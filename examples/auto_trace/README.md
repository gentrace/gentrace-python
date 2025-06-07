# Gentrace Auto-Tracing Example

This example demonstrates Gentrace's automatic AST-based tracing feature with pipeline ID support, which instruments all functions in specified modules without requiring manual decoration.

## Prerequisites

Before running the example, ensure you have the following environment variables set:

```bash
export GENTRACE_API_KEY="your-gentrace-api-key"
export GENTRACE_PIPELINE_ID="your-pipeline-uuid"
export OPENAI_API_KEY="your-openai-api-key"
```

## Overview

The example simulates a data processing pipeline with multiple layers of function calls, creating a deep tree of spans to showcase the automatic tracing capabilities with pipeline association.

## Structure

```
auto_trace/
├── README.md                         # This file
├── auto_trace_pipeline_example.py    # Main example script
└── pipeline_example_app/             # Example application package
    ├── __init__.py
    └── workflow.py                   # Pipeline workflow functions
```

## Features Demonstrated

1. **Automatic Function Tracing**: All functions in the `pipeline_example_app` module are automatically traced without decorators
2. **Pipeline ID Support**: All traces are associated with a specific Gentrace pipeline
3. **Deep Span Trees**: The pipeline creates a multi-level hierarchy of spans showing the call flow
4. **OpenTelemetry Integration**: Proper span context propagation with parent-child relationships
5. **Root Span Attribution**: Only the root span includes the `gentrace.pipeline_id` attribute
6. **Decorator Compatibility**: The `@interaction` decorator can be used alongside auto-tracing, with decorator settings taking precedence

## Running the Example

```bash
cd examples/auto_trace
python auto_trace_pipeline_example.py
```

## Expected Output

The example will:

1. Initialize OpenTelemetry with Gentrace configuration
2. Install auto-tracing for the `pipeline_example_app` module
3. Execute a multi-step data processing pipeline
4. Export spans to the Gentrace backend via OTLP

## Span Tree Structure

The automatic tracing creates a span tree like this:

```
run_data_processing_pipeline [root - has pipeline_id from auto-tracing]
├── extract_data
│   └── process_record (multiple calls)
├── transform_data
│   ├── apply_transformation (multiple calls)
│   └── validate_transformation (multiple calls)
└── load_results
    ├── generate_summary [auto-traced]
    └── Manual Summary Enrichment [@traced decorator - custom attributes]
```

## Key Concepts

### Installing Auto-Tracing with Pipeline ID

```python
gentrace.install_auto_tracing(
    ['pipeline_example_app'],
    min_duration=0,
    pipeline_id=pipeline_id
)
```

This must be called BEFORE importing the modules you want to trace.

### How Pipeline ID Works

When a pipeline_id is provided:

- The root span (first span in the trace) includes the `gentrace.pipeline_id` attribute
- Child spans do NOT include the pipeline_id attribute
- This allows the Gentrace backend to associate the entire trace tree with the pipeline
- All spans in the trace are connected via the same `traceId`

### Mixing Auto-Tracing with Manual Tracing

The example demonstrates that manual tracing decorators can be used within auto-traced code:

- Functions marked with `@no_auto_trace` are excluded from automatic tracing
- The `@traced` decorator can be used within auto-traced code for fine-grained control
- Manual traces can add custom attributes and names
- Both auto-traced and manually traced spans maintain proper parent-child relationships
- This allows selective manual instrumentation while maintaining automatic tracing for the rest of the code

### OpenTelemetry Configuration

The example shows proper OpenTelemetry setup with:

- Resource configuration with service name
- Gentrace sampler for sampling decisions
- Gentrace span processor for baggage propagation
- OTLP exporter configured for the Gentrace backend

### Minimum Duration

The `min_duration` parameter (in seconds) can be used to only trace functions that take longer than the specified duration. This helps reduce noise from very fast functions.

## Troubleshooting

If spans don't appear in the Gentrace UI:

1. Check that all environment variables are set correctly
2. Verify the Gentrace backend is running and accessible
3. Ensure the ClickHouse replication task is running
4. Check the console output for any error messages
5. Verify the pipeline ID exists in your Gentrace instance
