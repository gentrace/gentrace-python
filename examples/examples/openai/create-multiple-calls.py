import os

import gentrace
from dotenv import load_dotenv

load_dotenv()

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

embedding_result = openai.Embedding.create(
    input="sample text", model="text-similarity-davinci-001"
)

print("Embedding result: ", embedding_result)

completion_result = openai.Completion.create(
    model="text-davinci-003",
    promptTemplate="Hello world {{ name }}",
    promptInputs={"name": "test"},
)

print("Completion result: ", completion_result)

info = runner.submit()

print("Response: ", info["pipelineRunId"])
