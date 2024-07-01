import asyncio
import os
import time

import gentrace
from dotenv import load_dotenv

load_dotenv()


def example_response(inputs):
    time.sleep(1)
    return "This is a generated response from the AI"


gentrace.init(
    api_key=os.getenv("GENTRACE_API_KEY"),
    host="http://localhost:3000/api",
)

# example existing pipelines

PIPELINE_SLUG = "guess-the-year"
pipeline_by_slug = gentrace.Pipeline(PIPELINE_SLUG)

PIPELINE_ID = "c10408c7-abde-5c19-b339-e8b1087c9b64"
pipeline_by_id = gentrace.Pipeline(id=PIPELINE_ID)

pipeline = pipeline_by_slug


async def measure_func(inputs):
    return example_response(inputs)


async def example_handler(pipeline_run_test_case):
    (runner, test_case) = pipeline_run_test_case
    await runner.ameasure(
        measure_func,
        inputs=test_case.get("inputs")
    )


async def main():
    pipeline_run_test_cases = gentrace.get_test_runners(pipeline)

    for pipeline_run_test_case in pipeline_run_test_cases:
        await example_handler(pipeline_run_test_case)

    result = gentrace.submit_test_runners(pipeline, pipeline_run_test_cases)
    print("Result: ", result)


asyncio.run(main())
