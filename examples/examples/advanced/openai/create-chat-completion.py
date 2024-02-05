import os

import gentrace
from dotenv import load_dotenv

load_dotenv()

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

openai = runner.get_openai()

messages = [
    {"role": "user", "content": "Hello! What's the capital of Maine?"},
]

result = openai.chat.completions.create(
    messages=messages,
    model="gpt-3.5-turbo",
    gentrace={
        "metadata": {"anotherKey": {"type": "string", "value": "promptTesting"}},
    },
)

messages.append(
    {
        "role": "assistant",
        "content": result.choices[0].message.content
    }
)

result = openai.chat.completions.create(
    messages=messages,
    model="gpt-3.5-turbo",
    gentrace={
        "metadata": {"anotherKey": {"type": "string", "value": "promptTesting"}},
    },
)

print("Result: ", result)

info = runner.submit()

print("Response: ", info["pipelineRunId"])

gentrace.flush()
