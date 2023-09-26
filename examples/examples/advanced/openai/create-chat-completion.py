import os

import gentrace
from dotenv import load_dotenv

load_dotenv()

gentrace.init(
    api_key=os.getenv("GENTRACE_API_KEY"),
    host="http://localhost:3000/api/v1",
)

pipeline = gentrace.Pipeline(
    "testing-pipeline-id",
    openai_config={
        "api_key": os.getenv("OPENAI_KEY"),
    },
)

pipeline.setup()

runner = pipeline.start(
    {
        "userId": "123",
        "metadata": {"test": {"type": "string", "value": "https://google.com"}},
    }
)

openai = runner.get_openai()

result = openai.ChatCompletion.create(
    messages=[{"role": "user", "content": "Hello!"}],
    model="gpt-3.5-turbo",
    gentrace={
        "metadata": {"anotherKey": {"type": "string", "value": "promptTesting"}},
    },
)

result = openai.ChatCompletion.create(
    messages=[{"role": "user", "content": "Hello!"}],
    model="gpt-3.5-turbo",
    gentrace={
        "metadata": {"anotherKey2": {"type": "string", "value": "promptTesting"}},
    },
)


print("Result: ", result)

info = runner.submit()

print("Response: ", info["pipelineRunId"])


gentrace.flush()
