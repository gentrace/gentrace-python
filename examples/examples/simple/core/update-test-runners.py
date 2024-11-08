import asyncio
import os
from typing import Any

import gentrace
from dotenv import load_dotenv

load_dotenv()

def example_response(inputs: Any) -> str:
    return "This is a generated response from the AI"

async def main():
    gentrace.init(
        api_key=os.getenv("GENTRACE_API_KEY"),
        host="http://localhost:3000/api",
    )

    PIPELINE_SLUG = "guess-the-year"

    # Get the existing pipeline (if already exists)
    pipeline_by_slug = gentrace.Pipeline(PIPELINE_SLUG)

    # Example pipeline by ID
    PIPELINE_ID = "c10408c7-abde-5c19-b339-e8b1087c9b64"
    gentrace.Pipeline(id=PIPELINE_ID)

    pipeline = pipeline_by_slug

    pipeline_run_test_cases = gentrace.get_test_runners(pipeline)
    
    response = gentrace.submit_test_runners(pipeline, [pipeline_run_test_cases[0]])

    # Update the test result with the remaining runners
    update_response = gentrace.update_test_result_with_runners(
        response["resultId"],
        pipeline_run_test_cases[1:]
    )
    print("Update response:", update_response)

if __name__ == "__main__":
    asyncio.run(main())
