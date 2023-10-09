import os

import gentrace
from dotenv import load_dotenv
from gentrace import OpenAI

load_dotenv()

gentrace.init(
    api_key=os.getenv("GENTRACE_API_KEY"),
    host="http://localhost:3000/api/v1",
    log_level="info",
)

openai = OpenAI(api_key=os.getenv("OPENAI_KEY"))

result = openai.embeddings.create(
    input="sample text",
    model="text-embedding-ada-002",
    pipeline_slug="testing-pipeline-id",
)

print("Result: ", result.pipelineRunId)

gentrace.flush()
