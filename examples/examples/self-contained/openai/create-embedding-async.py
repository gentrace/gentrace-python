import asyncio
import os

import gentrace
from dotenv import load_dotenv
from gentrace import providers

load_dotenv()


async def main():
    gentrace.api_key = os.getenv("GENTRACE_API_KEY")
    gentrace.host = "http://localhost:3000/api/v1"

    providers.openai_api_key = os.getenv("OPENAI_KEY")
    openai = providers.openai

    result = await openai.Embedding.acreate(
        input="sample text",
        model="text-similarity-davinci-001",
        pipeline_id="testing-value",
    )

    gentrace.flush()

    print("Result: ", result.pipeline_run_id)


asyncio.run(main())
