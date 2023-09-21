import os

import gentrace
import openai
from dotenv import load_dotenv

load_dotenv()

gentrace.init(
    api_key=os.getenv("GENTRACE_API_KEY"),
    host="http://localhost:3000/api/v1",
)

gentrace.configure_openai()

openai.api_key = os.getenv("OPENAI_KEY")

result = openai.ChatCompletion.create(
    pipeline_slug="testing-chat-completion-value",
    messages=[
        {
            "role": "user",
            "contentTemplate": "Hello {{ name }}! What's your name?",
            "contentInputs": {"name": "John"},
        }
    ],
    model="gpt-3.5-turbo",
    context={
        "userId": "123",
    },
)

print(result)

gentrace.flush()
