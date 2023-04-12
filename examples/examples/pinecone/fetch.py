import os

import gentrace
from dotenv import load_dotenv

from examples.pinecone.utils import DEFAULT_VECTOR

load_dotenv()

pipeline = gentrace.Pipeline(
    "test-gentrace-python-pipeline",
    os.getenv("GENTRACE_API_KEY"),
    host="http://localhost:3000/api/v1",
    pinecone_config={
        "api_key": os.getenv("PINECONE_API_KEY"),
    },
)

pipeline.setup()

runner = pipeline.start()

pinecone = runner.get_pinecone()

index = pinecone.Index("openai-trec")

print("Index: ", index)

result = index.query(
    top_k=10,
    vector=DEFAULT_VECTOR,
)

print("Result: ", result)

info = runner.submit()

print("Response: ", info["pipelineRunId"])
