import os

import gentrace
import pinecone
from dotenv import load_dotenv

load_dotenv()

gentrace.init(
    api_key=os.getenv("GENTRACE_API_KEY"),
    host="http://localhost:3000/api/v1",
    log_level="info",
)

gentrace.configure_pinecone()

pinecone.init(
    api_key=os.getenv("PINECONE_API_KEY"),
)

result = pinecone.Index("openai-trec").fetch(
    ids=["3980"], pipeline_slug="self-contained-pinecone-fetch"
)

gentrace.flush()

print("Result: ", result["pipelineRunId"])
