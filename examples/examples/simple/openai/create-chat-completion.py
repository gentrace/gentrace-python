import os

import gentrace
from dotenv import load_dotenv

load_dotenv()

gentrace.init(
    api_key=os.getenv("GENTRACE_API_KEY"),
    host="http://localhost:3000/api",
)

openai = gentrace.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

result = openai.chat.completions.create(
    pipeline_slug="testing-vivek-5",
    messages=[
        {
            "role": "user",
            "contentTemplate": "Hello {{ name }}! What's your name?",
            "contentInputs": {"name": "John"},
        }
    ],
    model="gpt-3.5-turbo",
    gentrace={
        "metadata": {
            "booleanPythonTest": {
                "type": "boolean",
                "value": True
            }
        }
    }
)

print(result.pipelineRunId)

gentrace.flush()
