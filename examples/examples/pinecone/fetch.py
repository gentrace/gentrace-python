import os

import gentrace
from dotenv import load_dotenv

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

index = pinecone.index("openai-trec")

print("Index: ", index)

# result = openai.Embedding.create(
#     input="sample text", model="text-similarity-davinci-001"
# )

# print("Result: ", result)

info = runner.submit()

print("Response: ", info["pipelineRunId"])
