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

    result = openai.ChatCompletion.create(
        messages=[{"role": "user", "content": "Hello!"}], model="gpt-3.5-turbo"
    )

    print("Result: ", result)

    info = await runner.asubmit()

    print("Response: ", info["pipelineRunId"])


asyncio.run(main())
