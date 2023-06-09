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

    pipeline = gentrace.Pipeline(
        "test-gentrace-python-pipeline",
        openai_config={
            "api_key": os.getenv("OPENAI_KEY"),
        },
    )

    pipeline.setup()

    runner = pipeline.start()

    openai = runner.get_openai()

    result = await openai.Embedding.acreate(
        input="sample text", model="text-similarity-davinci-001"
    )

    print("Result: ", result)

    info = runner.submit()

    print("Response: ", info["pipelineRunId"])


asyncio.run(main())
