"""
This example script demonstrates how to use the Gentrace Python SDK
to define and run experiments with evaluations. It showcases:

- Setting up Gentrace and OpenTelemetry for tracing.
- Defining an experiment using the @experiment decorator.
- Defining evaluation test cases within the experiment using the @eval decorator.
- Dynamically invoking these evaluation test cases.

To run this example, ensure the following environment variables are set:
    GENTRACE_API_KEY: Your Gentrace API token for authentication.
    GENTRACE_BASE_URL: The base URL for your Gentrace instance (e.g., http://localhost:3000 or https://gentrace.ai/api).
"""

import os
import asyncio
import logging
from typing import Any, Dict, List

from gentrace import eval, init, experiment

gentrace_api_key = os.getenv("GENTRACE_API_KEY")
gentrace_base_url = os.getenv("GENTRACE_BASE_URL")

if not gentrace_api_key:
    raise ValueError("GENTRACE_API_KEY environment variable not set.")
if not gentrace_base_url:
    raise ValueError("GENTRACE_BASE_URL environment variable not set.")

init(
    base_url=gentrace_base_url,
    api_key=gentrace_api_key,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

PIPELINE_ID = "26d64c23-e38c-56fd-9b45-9adc87de797b"


def compose_email(subject: str, body: str, to: str, from_: str) -> str:
    """Formats an email string with given subject, body, recipient, and sender.

    This is a placeholder function for demonstration purposes within the experiment.

    Args:
        subject: The subject line of the email.
        body: The main content of the email.
        to: The recipient's email address.
        from_: The sender's email address.

    Returns:
        A string representing the formatted email.
    """
    return f"To: {to}\\nFrom: {from_}\\nSubject: {subject}\\n\\n{body}"


@experiment(
    pipeline_id=PIPELINE_ID,
    options={
        "name": "Dynamic Eval Experiment",
        "metadata": {"environment": "example", "version": "2.0"},
    },
)
async def run_evals_experiment() -> None:
    logger.info(f"Running experiment with options")

    @eval(name="Email Content Test 1", metadata={"variant": "A"})
    async def check_email_variant_A(subject: str, body: str, expected_keywords: List[str]) -> Dict[str, Any]:
        email_content = compose_email(subject=subject, body=body, to="test@example.com", from_="sender@example.com")
        for keyword in expected_keywords:
            assert keyword in email_content, f"Keyword '{keyword}' not found in email variant A"
        logger.info(f"    [{check_email_variant_A.__name__}] PASSED.")
        return {"email_length": len(email_content), "subject": subject, "body": body}

    await check_email_variant_A(
        subject="Welcome Email A",
        body="This is variant A of our welcome email.",
        expected_keywords=["Welcome Email A", "variant A"],
    )

    @eval(name="Email Content Test 2 (Sync)", metadata={"variant": "B"})
    async def check_email_variant_B_sync(subject: str, body: str, disallowed_phrases: List[str]) -> Dict[str, Any]:
        email_content = compose_email(subject=subject, body=body, to="user@example.net", from_="marketing@example.com")
        for phrase in disallowed_phrases:
            assert phrase not in email_content, f"Disallowed phrase '{phrase}' found in email variant B"
        logger.info(f"    [{check_email_variant_B_sync.__name__}] PASSED.")
        return {"email_length": len(email_content), "subject": subject, "body": body, "outcome": "sync success"}

    await check_email_variant_B_sync(
        subject="Special Offer B",
        body="Variant B: Get your special discount now!",
        disallowed_phrases=["spam", "free money"],
    )

    @eval(name="Error Case Test", metadata={"test_type": "failure_simulation"})
    async def check_email_potentially_failing(subject: str) -> Dict[str, str]:
        if not subject:
            raise ValueError("Subject cannot be empty for this test.")
        logger.info(f"    [{check_email_potentially_failing.__name__}] Processed (expected to fail or be caught).")
        return {"status": "ran_before_potential_error", "subject_used": subject}

    try:
        await check_email_potentially_failing(subject="")
    except ValueError as e:
        logger.warning(f"Caught expected error in '{check_email_potentially_failing.__name__}': {e}")

    @eval(name="Simple Log Test")
    def simple_log_test() -> Dict[str, str]:
        log_output = "This is a simple log test within an experiment."
        logger.info(f"    [{simple_log_test.__name__}] {log_output}")
        return {"log_message": log_output}

    await simple_log_test()

    logger.info("Finished all test cases in run_evals_experiment.")


async def run_example() -> None:
    print("--- Example: Experiment with Dynamically Defined and Called Evals ---")
    try:
        experiment_result = await run_evals_experiment()
        print(f"--- Experiment Result from main function: {experiment_result} ---")
    except Exception as e:
        print(f"--- Experiment Execution FAILED: {type(e).__name__}: {e} ---")


if __name__ == "__main__":
    import atexit

    from opentelemetry import trace
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import ConsoleSpanExporter, SimpleSpanProcessor
    from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter

    trace_provider = TracerProvider()
    trace.set_tracer_provider(trace_provider)

    console_exporter = ConsoleSpanExporter()
    span_processor = SimpleSpanProcessor(console_exporter)
    trace_provider.add_span_processor(span_processor)

    otlp_headers = {"Authorization": f"Bearer {gentrace_api_key}"}

    span_exporter = OTLPSpanExporter(
        endpoint=f"{gentrace_base_url}/otel/v1/traces",
        headers=otlp_headers,
    )

    span_processor = SimpleSpanProcessor(span_exporter)
    trace_provider.add_span_processor(span_processor)

    atexit.register(trace_provider.shutdown)

    print("OpenTelemetry ConsoleSpanExporter initialized for basic span output.")

    print("Running example...")

    asyncio.run(run_example())

    print("--- Example Run Finished ---")
