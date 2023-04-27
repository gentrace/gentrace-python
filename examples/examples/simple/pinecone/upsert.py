import os
import random

import gentrace
import pinecone
from dotenv import load_dotenv

from examples.utils import DEFAULT_VECTOR

load_dotenv()

gentrace.api_key = os.getenv("GENTRACE_API_KEY")
gentrace.host = "http://localhost:3000/api/v1"

gentrace.configure_pinecone()

pinecone.init(
    api_key=os.getenv("PINECONE_API_KEY"),
)

result = pinecone.Index("openai-trec").upsert(
    [
        {
            "id": str(random.randint(0, 9999)),
            "values": DEFAULT_VECTOR,
        },
    ],
    pipeline_id="self-contained-pinecone-upsert",
)

gentrace.flush()

print("Result: ", result["pipelineRunId"])
