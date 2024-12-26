import os
import random
import json
import hmac
import hashlib
from typing import Dict, Any

from fastapi import FastAPI, Request, HTTPException
from openai import OpenAI
import gentrace
from dotenv import load_dotenv
from gentrace.providers.test_job_runner import (
    define_interaction,
    handle_webhook,
    template_parameter,
    numeric_parameter,
    enum_parameter,
)
from pydantic import BaseModel, EmailStr

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI()

# Initialize Gentrace
gentrace.init(
    api_key=os.getenv("GENTRACE_API_KEY"),
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
    # TODO: Actually interpolate the inputs
    rendered_email = write_email_prompt_parameter.render({
        "fromName": "John Smith",
        "fromEmail": "john.smith@example.com", 
        "toEmail": "jane.doe@example.com",
        "instructions": "Please write a friendly introduction email",
    })
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

async def verify_signature(request: Request):
    """Verify the webhook signature."""
    webhook_secret = os.getenv("GENTRACE_WEBHOOK_SECRET")
    if not webhook_secret:
        raise HTTPException(status_code=500, detail="Webhook secret not configured")
        
    signature = request.headers.get("x-gentrace-signature")
    if not signature:
        raise HTTPException(status_code=401, detail="No signature provided")
    
    body = await request.body()
    calculated_signature = f"sha256={hmac.new(webhook_secret.encode(), body, hashlib.sha256).hexdigest()}"
    
    if not hmac.compare_digest(signature, calculated_signature):
        raise HTTPException(status_code=401, detail="Invalid signature")

@app.post("/")
async def webhook_handler(request: Request):
    """Handle incoming webhook requests."""
    # Verify the signature
    await verify_signature(request)
    
    # Get request body
    body = await request.json()
    
    # Handle the webhook and return response
    response = await handle_webhook(body)
    return response

def start_server():
    """Start the FastAPI server."""
    import uvicorn
    port = int(os.getenv("PORT", "3500"))
    uvicorn.run(app, host="0.0.0.0", port=port)
    

if __name__ == "__main__":
    start_server()
