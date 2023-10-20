import os

import gentrace
from dotenv import load_dotenv

load_dotenv()

gentrace.init(
    api_key=os.getenv("GENTRACE_API_KEY"),
    host="http://localhost:3000/api",
    log_level="info",
)

openai = gentrace.OpenAI(api_key=os.getenv("OPENAI_KEY"))

result = openai.completions.create(
    pipeline_slug="testing-pipeline-id",
    model="text-davinci-003",
    prompt_template="Hello world {{ name }}. What's the capital of Maine?",
    prompt_inputs={"name": "OpenAI"},
)

print("Response: ", result)

gentrace.flush()

print("Result: ", result.pipelineRunId)
