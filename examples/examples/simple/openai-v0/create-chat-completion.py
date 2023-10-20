import os

import gentrace
import openai
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENAI_KEY")

gentrace.init(
    api_key=os.getenv("GENTRACE_API_KEY"),
    host="http://localhost:3000/api/v1",
)

gentrace.configure_openai()

result = openai.ChatCompletion.create(
    pipeline_slug="testing-pipeline-id",
    messages=[
        {
            "role": "user",
            "contentTemplate": "Hello {{ name }}! What's your name?",
            "contentInputs": {"name": "John"},
        }
    ],
    model="gpt-3.5-turbo",
)

print(result["pipelineRunId"])

gentrace.flush()
