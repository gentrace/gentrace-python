"""
Simple Gentrace initialization with OpenTelemetry enabled (default).
"""

import os
from typing import Dict

from dotenv import load_dotenv

from gentrace import init, interaction

load_dotenv()

# Initialize with OpenTelemetry enabled (default behavior)
init(
    api_key=os.getenv("GENTRACE_API_KEY"),
    base_url=os.getenv("GENTRACE_BASE_URL", "https://gentrace.ai/api"),
)


# Now you can use decorators to trace your code
@interaction(name="simple_example", pipeline_id=os.getenv("GENTRACE_PIPELINE_ID", ""))
def main() -> Dict[str, str]:
    print("Hello from Gentrace!")
    return {"message": "This interaction is being traced"}


if __name__ == "__main__":
    result = main()
    print(f"Result: {result}")
