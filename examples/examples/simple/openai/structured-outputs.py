import os

import gentrace
from dotenv import load_dotenv
from gentrace import OpenAI
from pydantic import BaseModel

load_dotenv()

gentrace.init(
    api_key=os.getenv("GENTRACE_API_KEY"),
    host="http://localhost:3000/api",
    log_level="info",
)

openai = OpenAI(api_key=os.getenv("OPENAI_KEY"))

class Step(BaseModel):
    explanation: str
    output: str

class MathReasoning(BaseModel):
    steps: list[Step]
    final_answer: str

result = openai.beta.chat.completions.parse(
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
    pipeline_slug="math-reasoning-pipeline",
    gentrace={
        "metadata": {"problem_type": {"type": "string", "value": "algebra"}},
    },
)

math_reasoning = result.choices[0].message.parsed

print("Math Reasoning: ", math_reasoning)
print("Result: ", result.pipelineRunId)

gentrace.flush()
