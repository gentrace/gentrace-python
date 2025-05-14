# The ATTR_ prefix follows OpenTelemetry semantic convention naming
# from their packages.
ANONYMOUS_SPAN_NAME = "anonymous_function"

ATTR_GENTRACE_PIPELINE_ID = "gentrace.pipeline_id"

ATTR_GENTRACE_FN_ARGS_EVENT_NAME = "gentrace.fn.args"
ATTR_GENTRACE_FN_OUTPUT_EVENT_NAME = "gentrace.fn.output"

ATTR_GENTRACE_EXPERIMENT_ID = "gentrace.experiment_id"
ATTR_GENTRACE_TEST_CASE_NAME = "gentrace.test_case_name"
ATTR_GENTRACE_TEST_CASE_ID = "gentrace.test_case_id"

ATTR_GENTRACE_SAMPLE_KEY = "gentrace.sample"

__all__ = [
    "ANONYMOUS_SPAN_NAME",
    "ATTR_GENTRACE_FN_ARGS_EVENT_NAME",
    "ATTR_GENTRACE_FN_OUTPUT_EVENT_NAME",
    "ATTR_GENTRACE_EXPERIMENT_ID",
    "ATTR_GENTRACE_TEST_CASE_NAME",
    "ATTR_GENTRACE_TEST_CASE_ID",
    "ATTR_GENTRACE_PIPELINE_ID",
    "ATTR_GENTRACE_SAMPLE_KEY",
]
