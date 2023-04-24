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

active_indexes = pinecone.list_indexes()

print("Active indexes: ", active_indexes)


info = runner.submit()

print("Response: ", info["pipelineRunId"])
