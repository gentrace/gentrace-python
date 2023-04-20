import os

import gentrace
from dotenv import load_dotenv
from gentrace import providers

load_dotenv()

gentrace.api_key = os.getenv("GENTRACE_API_KEY")
gentrace.host = "http://localhost:3000/api/v1"

providers.openai_api_key = os.getenv("OPENAI_KEY")
openai = providers.openai

result = openai.Completion.create(
    pipeline_id="text-generation",
    model="text-davinci-003",
    prompt_template="Hello world {{ name }}",
    prompt_inputs={"name": "test"},
)

gentrace.flush()

print("Result: ", result.pipeline_run_id)
