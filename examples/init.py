"""
This example script showcases the basic initialization of the Gentrace Python SDK.
It demonstrates:
- Setting up the Gentrace SDK with API key and base URL
- Basic configuration for tracing and monitoring
- Environment variable handling for secure credential management

To run this example, ensure the following environment variables are set:
    GENTRACE_API_KEY: Your Gentrace API token for authentication.
    GENTRACE_BASE_URL: The base URL for your Gentrace instance (e.g., http://localhost:3000).
"""

import os

from gentrace import init

init(
    api_key=os.getenv("GENTRACE_API_KEY"),
    # Optional for self-hosted deployments: base_url=os.getenv("GENTRACE_BASE_URL", "https://gentrace.ai/api"),
)

print("Gentrace initialized! ✅")
