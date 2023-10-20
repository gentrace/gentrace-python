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

    pipeline = gentrace.Pipeline(
        "testing-pipeline-id",
        openai_config={
            "api_key": os.getenv("OPENAI_KEY"),
        },
    )

    pipeline.setup()

    runner = pipeline.start()

    openai = runner.get_openai(asynchronous=True)

    result = await openai.chat.completions.create(
        messages=[{"role": "user", "content": "Hello!"}],
        model="gpt-3.5-turbo",
    )

    print("Result: ", result)

    info = runner.submit()

    print("Response: ", info["pipelineRunId"])


asyncio.run(main())
