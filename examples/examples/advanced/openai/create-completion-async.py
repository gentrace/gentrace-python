import asyncio
import os

import gentrace
from dotenv import load_dotenv

load_dotenv()

gentrace.init(
    api_key=os.getenv("GENTRACE_API_KEY"),
    host="http://localhost:3000/api/v1",
)


async def main():
    pipeline = gentrace.Pipeline(
        "test-gentrace-python-pipeline",
        openai_config={
            "api_key": os.getenv("OPENAI_KEY"),
        },
    )

    pipeline.setup()

    runner = pipeline.start()

    openai = runner.get_openai()

    await openai.Completion.acreate(
        model="text-davinci-003",
        prompt_template="Hello world {{ name }}",
        prompt_inputs={"name": "Vivek"},
    )

    info = runner.submit()

    print("Response: ", info["pipelineRunId"])


asyncio.run(main())
