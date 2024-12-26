import os
import random
import json
from typing import Dict, Any

from openai import OpenAI
import gentrace
from dotenv import load_dotenv
from gentrace.providers.test_job_runner import (
    define_interaction,
    listen,
    template_parameter,
    numeric_parameter,
    enum_parameter,
)
from pydantic import BaseModel, EmailStr

load_dotenv()

# Initialize Gentrace
gentrace.init(
    api_key=os.getenv("GENTRACE_API_KEY"),
    # host="http://localhost:3000/api",
)

# # Initialize OpenAI client
# client = OpenAI(
#     api_key=os.getenv("OPENAI_KEY"),
# )

# Define parameters
write_email_prompt_parameter = template_parameter({
    "name": "Write email prompt",
    "defaultValue": "Write an email to {{toEmail}} from ({{fromName}}) {{fromEmail}} according to these instructions: {{instructions}}",
    "variables": [
        {"name": "fromName", "example": "John Doe"},
        {"name": "fromEmail", "example": "john.doe@gmail.com"},
        {"name": "toEmail", "example": "blah@gmail.com"},
        {
            "name": "instructions",
            "example": {"subject": "Hello", "body": "Write a short email"}
        }
    ]
})

# Input validation models using Pydantic
class WriteEmailInput(BaseModel):
    fromName: str
    fromEmail: EmailStr
    toEmail: EmailStr
    instructions: str

async def write_email(inputs: Dict[str, Any]) -> Dict[str, Any]:
    result = {
        "from": inputs.get('fromName'),
        "fromEmail": inputs.get('fromEmail'),
        "to": inputs.get('toEmail'),
        "instructions": inputs.get('instructions')
    }
    raise Exception("Failed to process email inputs")

    return json.dumps({k: v for k, v in result.items() if v is not None})
    # completion = await client.chat.completions.create(
    #     model="gpt-4o-mini",
    #     messages=[
    #         {
    #             "role": "user",
    #             "content": write_email_prompt_parameter["render"]({
    #                 "fromName": inputs["fromName"],
    #                 "fromEmail": inputs["fromEmail"],
    #                 "toEmail": inputs["toEmail"],
    #                 "instructions": inputs["instructions"],
    #             }),
    #         }
    #     ],
    # )
    # return {
    #     "body": completion.choices[0].message.content,
    # }

# Define write_email interaction
write_email_interaction = define_interaction({
    "name": "Write email",
    "fn": write_email,
    "parameters": [write_email_prompt_parameter],
    "inputType": WriteEmailInput
})

# Draft reply interaction
async def draft_reply(inputs: Dict[str, Any]) -> Dict[str, Any]:
    """Draft reply interaction function."""
    return {
        "reply": "blah"
    }

draft_reply_interaction = define_interaction({
    "name": "Draft reply",
    "fn": draft_reply
})

# Random year parameter
random_year_parameter = numeric_parameter({
    "name": "Random component of year",
    "defaultValue": 3
})

class GuessYearInput(BaseModel):
    query: str

async def guess_the_year(inputs: Dict[str, Any]) -> int:
    """Guess the year interaction function."""
    return int(2022 + (random_year_parameter["getValue"]() * random.random()))

guess_year_interaction = define_interaction({
    "name": "Guess the year",
    "fn": guess_the_year,
    "inputType": GuessYearInput,
    "parameters": [random_year_parameter]
})

# Model parameter
model_parameter = enum_parameter({
    "name": "AI Model",
    "defaultValue": "GPT-4o",
    "options": ["GPT-4o", "GPT-4o-mini", "claude-3.5-sonnet", "gemini-1.5-pro-002"]
})

class ChooseModelInput(BaseModel):
    query: str

async def choose_model(inputs: Dict[str, Any]) -> str:
    """Choose model interaction function."""
    return f"I will use the model {model_parameter['getValue']()}."

choose_model_interaction = define_interaction({
    "name": "Choose model",
    "fn": choose_model,
    "inputType": ChooseModelInput,
    "parameters": [model_parameter]
})


if __name__ == "__main__":
    # Start listening for test jobs
    listen()
