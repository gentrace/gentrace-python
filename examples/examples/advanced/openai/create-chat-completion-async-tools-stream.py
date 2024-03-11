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
        model="gpt-4-1106-preview",
        stream=True,
        messages=[
            {
                "role": "user",
                "content": "Convert this sentence to JSON: John is 10 years old.",
            },
        ],
        gentrace={
            "metadata": {
                # We support multiple metadata keys within the metadata object
                "externalServiceUrl": {
                    # Every metadata object must have a "type" key
                    "type": "url",
                    "url": "https://external-service.example.com",
                    "text": "External service"
                },
                "gitSha": {
                    "type": "string",
                    "value": "testing"
                }
            }
        },
        tools=[
            {
                "type": "function",
                "function": {
                    "name": "person",
                    "description": "pn_info",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "age": {
                                "type": "integer",
                                "description": "Age",
                            },
                        },
                        "required": ["age"],
                    },
                },
            },
        ],
    )

    async for completion in result:
        print('Completion: ', completion)
        pass

    info = await runner.asubmit()

    print("Response: ", info["pipelineRunId"])


asyncio.run(main())
