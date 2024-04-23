import os
import gentrace
from multiprocessing.pool import ThreadPool
from dotenv import load_dotenv

load_dotenv()

def example_response(inputs):
  return "This is a generated response from the AI";

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

def example_handler(pipeline_run_test_case):
    (runner, test_case) = pipeline_run_test_case 
    runner.measure(
        lambda inputs: example_response(inputs),
        inputs=test_case.get("inputs")
    )

pipeline_run_test_cases = gentrace.get_test_runners(pipeline)

enable_parallelism(example_handler, pipeline_run_test_cases, 4)

result = gentrace.submit_test_runners(pipeline, pipeline_run_test_cases)
print("Result: ", result)
