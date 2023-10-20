import asyncio
import os

import gentrace
from dotenv import load_dotenv

load_dotenv()


async def main():
    gentrace.init(
        api_key=os.getenv("GENTRACE_API_KEY"),
        host="http://localhost:3000/api",
    )

    openai = gentrace.AsyncOpenAI()

    result = await openai.chat.completions.create(
        pipeline_slug="testing-pipeline-id",
        messages=[
            {
                "role": "user",
                "contentTemplate": "Hello {{ name }}! Tell me a bit about {{ topic }}",
                "contentInputs": {"name": "John", "topic": "Maine"},
            }
        ],
        model="gpt-3.5-turbo",
        stream=True,
    )

    pipeline_run_id = None
    async for value in result:
        if value.get("pipelineRunId"):
            pipeline_run_id = value.get("pipelineRunId")

    gentrace.flush()

    print("Result: ", pipeline_run_id)


asyncio.run(main())
