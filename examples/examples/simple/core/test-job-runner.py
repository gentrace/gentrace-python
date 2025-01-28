import os
import random
import json
from typing import Dict, Any

import gentrace
from dotenv import load_dotenv
from gentrace.providers.test_job_runner import (
    define_interaction,
    listen,
    template_parameter,
    numeric_parameter,
    enum_parameter,
    string_parameter,
)
from pydantic import BaseModel, EmailStr

load_dotenv()

# Initialize Gentrace
gentrace.init(
    api_key=os.getenv("GENTRACE_API_KEY"),
    host="http://localhost:3000/api",
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
    print(f"✅ WRITE_EMAIL | Parameter: {write_email_prompt_parameter}")
    print(f"✅ WRITE_EMAIL | Received inputs: {inputs}")
    
    # Extract values from inputs or use defaults
    render_values = {
        "fromName": inputs.get("fromName", "John Smith"),
        "fromEmail": inputs.get("fromEmail", "john.smith@example.com"),
        "toEmail": inputs.get("toEmail", "jane.doe@example.com"),
        "instructions": inputs.get("instructions", "Please write a friendly introduction email"),
    }
    print(f"✅ WRITE_EMAIL | Using render values: {render_values}")
    
    rendered_email = write_email_prompt_parameter.render(render_values)
    print(f"✅ WRITE_EMAIL | Rendered email: {rendered_email}")
    return rendered_email

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
    return int(2022 + (random_year_parameter.get_value() * random.random()))

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
    return f"I will use the model {model_parameter.get_value()}."

choose_model_interaction = define_interaction({
    "name": "Choose model",
    "fn": choose_model,
    "inputType": ChooseModelInput,
    "parameters": [model_parameter]
})

# User greeting parameter
greeting_parameter = string_parameter({
    "name": "User greeting",
    "defaultValue": "Hello there!"
})

class GreetUserInput(BaseModel):
    name: str

async def greet_user(inputs: Dict[str, Any]) -> str:
    """Greet user interaction function."""
    return f"{greeting_parameter.get_value()} {inputs.get('name', 'User')}"

greet_user_interaction = define_interaction({
    "name": "Greet user",
    "fn": greet_user,
    "inputType": GreetUserInput,
    "parameters": [greeting_parameter]
})

if __name__ == "__main__":
    # Start listening for test jobs
    listen()
