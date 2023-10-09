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
        pipeline_slug="testing-pipeline-id",
        model="text-davinci-003",
        prompt_template="Hello world {{ name }}",
        prompt_inputs={"name": "test"},
    )

    gentrace.flush()

    print("Result: ", result.pipelineRunId)


asyncio.run(main())
