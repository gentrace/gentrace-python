import os

import gentrace
from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()

gentrace.init(
    api_key=os.getenv("GENTRACE_API_KEY"),
    host="http://localhost:3000/api",
)

pipeline = gentrace.Pipeline(
    "math-reasoning-pipeline",
    openai_config={
        "api_key": os.getenv("OPENAI_KEY"),
    },
)

pipeline.setup()

runner = pipeline.start()

openai = runner.get_openai()

class Step(BaseModel):
    explanation: str
    output: str

class MathReasoning(BaseModel):
    steps: list[Step]
    final_answer: str

completion = openai.beta.chat.completions.parse(
    model="gpt-4o-2024-08-06",
    messages=[
        {
            "role": "system",
            "content": "You are a helpful math tutor. " \
                       "Guide the user through the solution step by step.",
        },
        {"role": "user", "content": "how can I solve 8x + 7 = -23"},
    ],
    response_format=MathReasoning,
    gentrace={
        "metadata": {"problem_type": {"type": "string", "value": "algebra"}},
    },
)

math_reasoning = completion.choices[0].message.parsed

print(math_reasoning)

info = runner.submit()

print("Response: ", info["pipelineRunId"])

gentrace.flush()
