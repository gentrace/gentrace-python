import asyncio
import os

import gentrace
from dotenv import load_dotenv
from gentrace import experiment

load_dotenv()

PIPELINE_SLUG = "main"

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
    "main",
    openai_config={
        "api_key": os.getenv("OPENAI_KEY"),
    },
)

pipeline.setup()


@experiment("guess-the-year")
async def create_measure_callback(test_case):
    print("Running with test case", test_case)
    runner = pipeline.start()
    output = runner.measure(
        lambda x=5, y=3: x + y,
        x=100,
        y=1000,
    )
    return [output, runner]


asyncio.run(create_measure_callback())
