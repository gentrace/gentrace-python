import os

import gentrace
import openai
from dotenv import load_dotenv

load_dotenv()

gentrace.api_key = os.getenv("GENTRACE_API_KEY")
gentrace.host = "http://localhost:3000/api/v1"

gentrace.configure()

openai.api_key = os.getenv("OPENAI_KEY")

result = openai.ChatCompletion.create(
    pipeline_id="testing-chat-completion-value",
    messages=[{"role": "user", "content": "Hello!"}],
    model="gpt-3.5-turbo",
    stream=True,
)

pipeline_run_id = None

for value in result:
    if value.get("pipeline_run_id"):
        pipeline_run_id = value.get("pipeline_run_id")

print("Result: ", pipeline_run_id)

gentrace.flush()
