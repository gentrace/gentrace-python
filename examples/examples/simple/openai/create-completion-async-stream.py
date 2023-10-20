import asyncio
import os

import gentrace
from dotenv import load_dotenv

load_dotenv()


async def main():
    gentrace.init(
        api_key=os.getenv("GENTRACE_API_KEY"),
        host="http://localhost:3000/api/v1",
    )

    openai = gentrace.AsyncOpenAI()

    result = await openai.completions.create(
        pipeline_slug="text-generation",
        model="text-davinci-003",
        prompt_template="Hello world {{ name }}",
        prompt_inputs={"name": "test"},
        stream=True,
    )

    async for value in result:
        print("Value", value.pipelineRunId)

    gentrace.flush()


asyncio.run(main())
