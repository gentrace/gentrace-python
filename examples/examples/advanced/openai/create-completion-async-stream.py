import asyncio
import os

import gentrace
from dotenv import load_dotenv

load_dotenv()

gentrace.init(
    api_key=os.getenv("GENTRACE_API_KEY"),
    host="http://localhost:3000/api",
)


async def main():
    pipeline = gentrace.Pipeline(
        "testing-pipeline-id",
        openai_config={
            "api_key": os.getenv("OPENAI_KEY"),
        },
    )

    pipeline.setup()

    runner = pipeline.start()

    openai = runner.get_openai(asynchronous=True)

    result = await openai.completions.create(
        model="text-davinci-003",
        prompt_template="Hello world {{ name }}",
        prompt_inputs={"name": "Vivek"},
        stream=True,
    )

    async for completion in result:
        print("Completion: ", completion)

    info = await runner.asubmit()

    print("Response: ", info["pipelineRunId"])


asyncio.run(main())
