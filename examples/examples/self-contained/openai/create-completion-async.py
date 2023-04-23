import asyncio
import os

import gentrace
import openai
from dotenv import load_dotenv

load_dotenv()


async def main():
    gentrace.api_key = os.getenv("GENTRACE_API_KEY")
    gentrace.host = "http://localhost:3000/api/v1"

    gentrace.configure_openai()

    openai.api_key = os.getenv("OPENAI_KEY")

    result = await openai.Completion.acreate(
        pipeline_id="text-generation",
        model="text-davinci-003",
        prompt_template="Hello world {{ name }}",
        prompt_inputs={"name": "test"},
    )

    gentrace.flush()

    print("Result: ", result.pipeline_run_id)


asyncio.run(main())
