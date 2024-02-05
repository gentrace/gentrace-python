import asyncio
import os

import gentrace
from dotenv import load_dotenv
from gentrace import experiment

load_dotenv()

PIPELINE_SLUG = "guessing-year"

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


@experiment(PIPELINE_SLUG, {
    "metadata": {
        "someKey": {
            "type": "url",
            "text": "Google",
            "url": "https://www.google.com"
        }
    }
})
async def create_measure_callback(test_case):
    print("Getting test case", test_case)
    runner = pipeline.start()
    client = runner.get_openai(asynchronous=True)

    output = runner.measure(
        lambda x=5, y=3: x + y,
        x=1,
        y=2,
    )

    output = runner.measure(
        lambda x=5, y=3: x + y,
        x=3,
        y=4,
    )

    output = runner.measure(
        lambda x=5, y=3: x + y,
        x=5,
        y=6,
    )

    output = runner.measure(
        lambda x=5, y=3: x + y,
        x=7,
        y=8,
    )

    output = await client.chat.completions.create(
        pipeline_slug="testing-chat-completion-value",
        messages=[{"role": "user", "content": "Hello! What's my name?"}],
        model="gpt-3.5-turbo",
    )
    return [output, runner]


asyncio.run(create_measure_callback())
