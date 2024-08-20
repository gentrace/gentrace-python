import os

import gentrace
from dotenv import load_dotenv

load_dotenv()

PIPELINE_SLUG = "copilot"

gentrace.init(
    api_key=os.getenv("GENTRACE_API_KEY"),
    run_name="vivek python run 2",
    host="http://localhost:3000/api",
)

pipeline = gentrace.Pipeline(
    PIPELINE_SLUG,
    openai_config={
        "api_key": os.getenv("OPENAI_KEY"),
    },
)

pipeline.setup()

pipeline = gentrace.Pipeline(
    "copilot",
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

result = gentrace.run_test(
    "copilot",
    create_measure_callback,
    dataset_id="0c36c737-d6e1-4913-b506-212459d7e2ea",
)


