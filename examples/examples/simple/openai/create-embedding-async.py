import asyncio
import os

import gentrace
from dotenv import load_dotenv
from gentrace import AsyncOpenAI

load_dotenv()

gentrace.init(
    api_key=os.getenv("GENTRACE_API_KEY"),
    host="http://localhost:3000/api/v1",
    log_level="info",
)

openai = AsyncOpenAI(api_key=os.getenv("OPENAI_KEY"))


async def main():
    result = await openai.embeddings.create(
        input="sample text",
        model="text-embedding-ada-002",
        pipeline_slug="testing-pipeline-id",
    )

    print("Result: ", result.pipelineRunId)

    gentrace.flush()


asyncio.run(main())
