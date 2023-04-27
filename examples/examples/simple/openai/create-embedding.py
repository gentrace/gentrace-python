import os

import gentrace
import openai
from dotenv import load_dotenv

load_dotenv()

gentrace.api_key = os.getenv("GENTRACE_API_KEY")
gentrace.host = "http://localhost:3000/api/v1"

gentrace.configure_openai()

openai.log = "debug"
openai.api_key = os.getenv("OPENAI_KEY")

result = openai.Embedding.create(
    input="sample text",
    model="text-similarity-davinci-001",
    pipeline_id="testing-value",
)

gentrace.flush()

print("Result: ", result["pipelineRunId"])
