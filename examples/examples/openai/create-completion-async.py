import asyncio
import os

import gentrace
from dotenv import load_dotenv

load_dotenv()


async def main():
    pipeline = gentrace.Pipeline(
        "test-gentrace-python-pipeline",
        os.getenv("GENTRACE_API_KEY"),
        host="http://localhost:3000/api/v1",
        openai_config={
            "api_key": os.getenv("OPENAI_KEY"),
        },
    )

    pipeline.setup()

    runner = pipeline.start()

    openai = runner.get_openai()

    asyncio.get_event_loop()

    result = await openai.Completion.acreate(
        model="text-davinci-003",
        promptTemplate="Hello world {{ name }}",
        promptInputs={"name": "Vivek"},
    )

    # TODO: Can we figure out a way to profile how long it takes to pull all values from
    # the result?
    # async for chunk in result:
    #     print("Chunk: ", chunk)

    print("Result: ", result)

    info = runner.submit()

    print("Response: ", info["pipelineRunId"])


asyncio.run(main())
