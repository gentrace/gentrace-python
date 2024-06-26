import os

import gentrace
from dotenv import load_dotenv

load_dotenv()

PIPELINE_SLUG = "testing-pipeline-id"

gentrace.init(
    api_key=os.getenv("GENTRACE_API_KEY"),
    run_name="vivek python run 2",
)

pipeline = gentrace.Pipeline(
    PIPELINE_SLUG,
    openai_config={
        "api_key": os.getenv("OPENAI_KEY"),
    },
)

pipeline.setup()

pipeline = gentrace.Pipeline(
    PIPELINE_SLUG,
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

result = gentrace.run_test(PIPELINE_SLUG, create_measure_callback)


