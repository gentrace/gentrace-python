import os
import time
from multiprocessing.pool import ThreadPool

import gentrace
from dotenv import load_dotenv

load_dotenv()


def example_response(inputs):
    return "This is a generated response from the AI"


def enable_parallelism(function, inputs, parallel_threads):
    # modify this parallelization approach as needed
    pool = ThreadPool(processes=parallel_threads)
    outputs = pool.map(function, inputs)
    return outputs


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


def measure_func(inputs):
    time.sleep(0.3)  # Simulate some work
    return {"example": example_response(inputs)}


def example_handler(pipeline_run_test_case):
    (runner, test_case) = pipeline_run_test_case
    runner.measure(
        measure_func,
        inputs=test_case.get("inputs")
    )


# Get all test runners
pipeline_run_test_cases = gentrace.get_test_runners(
    pipeline,
    dataset_id="70a96925-db53-5c59-82b4-f42e988950a9"
)

# Process first test case to get initial result
first_test_case = [pipeline_run_test_cases[0]]
example_handler(first_test_case[0])

# Submit first test case to get result ID
result = gentrace.submit_test_runners(pipeline, first_test_case)
print("Initial submission result:", result)

# Process remaining test cases in parallel
remaining_test_cases = pipeline_run_test_cases[2:]  # Skip first two like in TypeScript example
enable_parallelism(example_handler, remaining_test_cases, 5)

# Update the test result with the remaining processed test cases
update_response = gentrace.update_test_result_with_runners(
    result["resultId"],
    remaining_test_cases
)
print("Update response:", update_response)
