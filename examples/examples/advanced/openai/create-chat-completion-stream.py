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

result = openai.chat.completions.create(
    messages=[{"role": "user", "content": "Hello! What's the capital of Maine?"}],
    model="gpt-3.5-turbo",
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
    stream=True
)

print("Result: ", result)

for event in result:
    print("Event: ", event)

info = runner.submit()

print("Response: ", info["pipelineRunId"])

gentrace.flush()
