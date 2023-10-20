import os

import gentrace
from dotenv import load_dotenv

load_dotenv()

gentrace.init(
    api_key=os.getenv("GENTRACE_API_KEY"),
    host="http://localhost:3000/api/v1",
)

openai = gentrace.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

result = openai.chat.completions.create(
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

print(result.pipelineRunId)

gentrace.flush()
