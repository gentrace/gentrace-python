import os

import gentrace
import pinecone
from dotenv import load_dotenv

load_dotenv()

gentrace.api_key = os.getenv("GENTRACE_API_KEY")
gentrace.host = "http://localhost:3000/api/v1"

gentrace.configure_pinecone()

pinecone.init(
    api_key=os.getenv("PINECONE_API_KEY"),
)

result = pinecone.Index("openai-trec").fetch(
    ids=["3980"], pipeline_id="self-contained-pinecone-fetch"
)

gentrace.flush()

print("Result: ", result["pipelineRunId"])
