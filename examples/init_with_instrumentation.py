"""
Example showing Gentrace init with OpenTelemetry instrumentation.

This demonstrates passing instrumentations to automatically trace HTTP calls.
"""

import os

# Optional: Install these with pip install opentelemetry-instrumentation-requests
from typing import Any, Dict, List

import gentrace
from gentrace import interaction

try:
    from opentelemetry.instrumentation.requests import RequestsInstrumentor  # type: ignore

    instrumentations: List[Any] = [RequestsInstrumentor()]
except ImportError:
    instrumentations = []
    print("Install opentelemetry-instrumentation-requests for automatic HTTP tracing")

# Initialize with instrumentation
gentrace.init(
    api_key=os.getenv("GENTRACE_API_KEY"),
    base_url=os.getenv("GENTRACE_BASE_URL", "https://gentrace.ai/api"),
    otel_setup={"instrumentations": instrumentations} if instrumentations else True,
)


@interaction(name="http_example", pipeline_id=os.getenv("GENTRACE_PIPELINE_ID", ""))
def fetch_data() -> Dict[str, int]:
    import requests

    response = requests.get("https://api.github.com")
    return {"status": response.status_code}


if __name__ == "__main__":
    result = fetch_data()
    print(f"GitHub API returned: {result}")
