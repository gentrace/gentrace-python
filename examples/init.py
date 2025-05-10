import os
import logging

from gentrace.lib.init import init

logger = logging.getLogger(__name__)

"""
This example script demonstrates how to initialize the Gentrace SDK.
It shows the basic setup required to use Gentrace for tracing and monitoring
Python applications.

Ensure the following environment variables are set:
    GENTRACE_API_KEY: Your Gentrace API token for authentication.
    GENTRACE_BASE_URL: The base URL for your Gentrace instance (e.g., http://localhost:3000).
"""

init(
    bearer_token=os.getenv("GENTRACE_API_KEY"),
    base_url=os.getenv("GENTRACE_BASE_URL"),
)

logger.info("Gentrace initialized")
