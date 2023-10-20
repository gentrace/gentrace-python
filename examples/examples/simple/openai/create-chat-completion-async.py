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

    openai.api_key = os.getenv("OPENAI_KEY")

    result = await openai.chat.completions.create(
        pipeline_slug="testing-pipeline-id",
        messages=[
            {
                "role": "user",
                "contentTemplate": "Hello {{ name }}!",
                "contentInputs": {"name": "John"},
            }
        ],
        model="gpt-3.5-turbo",
    )

    gentrace.flush()

    print("Result: ", result.pipelineRunId)


asyncio.run(main())
