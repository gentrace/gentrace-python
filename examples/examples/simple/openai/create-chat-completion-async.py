import asyncio
import os

import gentrace
import openai
from dotenv import load_dotenv

load_dotenv()


async def main():
    gentrace.init(
        api_key=os.getenv("GENTRACE_API_KEY"),
        host="http://localhost:3000/api/v1",
    )

    gentrace.configure_openai()

    openai.api_key = os.getenv("OPENAI_KEY")

    result = await openai.ChatCompletion.acreate(
        pipeline_slug="testing-chat-completion-value",
        messages=[
            {
                "role": "user",
                "contentTemplate": "Hello {{ name }}! Tell me a bit about {{ topic }}",
                "contentInputs": {"name": "John", "topic": "Maine"},
            }
        ],
        model="gpt-3.5-turbo",
    )

    gentrace.flush()

    print("Result: ", result["pipelineRunId"])


asyncio.run(main())
