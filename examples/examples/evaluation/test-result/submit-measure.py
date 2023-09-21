import os

import gentrace
from dotenv import load_dotenv

load_dotenv()

PIPELINE_SLUG = "main"

gentrace.init(
    api_key=os.getenv("GENTRACE_API_KEY"),
    run_name="vivek python run 2",
    host="http://localhost:3000/api/v1",
)

pipeline = gentrace.Pipeline(
    PIPELINE_SLUG,
    openai_config={
        "api_key": os.getenv("OPENAI_KEY"),
    },
)

pipeline.setup()

pipeline = gentrace.Pipeline(
    "main",
    openai_config={
        "api_key": os.getenv("OPENAI_KEY"),
    },
)

pipeline.setup()


def create_measure_callback(test_case):
    runner = pipeline.start()
    output = runner.measure(
        lambda x=5, y=3: x + y,
        x=100,
        y=1000,
        step_info={
            "context": {"userId": "123", "render": {"type": "html", "key": "test_key"}}
        },
    )
    return [output, runner]


result = gentrace.run_test("main", create_measure_callback)
