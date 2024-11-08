import os
import uuid
from datetime import datetime, timezone

import requests
from dotenv import load_dotenv

load_dotenv()

# Get API key from environment
api_key = os.getenv("GENTRACE_API_KEY")
base_url = "https://gentrace.ai/api"

# Headers for authentication
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

# Create a run with required fields
run = {
    "id": str(uuid.uuid4()),
    "collectionMethod": "manual",
    "stepRuns": [
        {
            "providerName": "test-provider",
            "invocation": "test-invocation",
            "modelParams": {},
            "inputs": {
                "prompt": "Hello world"
            },
            "outputs": {
                "completion": "Hi there!"
            },
            "context": {
                "userId": "string",
                "metadata": None
            },
            "elapsedTime": 1000,

            # Modify with your desired dates in ISO 8601 format
            "startTime": datetime.now(timezone.utc).isoformat(),
            "endTime": datetime.now(timezone.utc).isoformat()
        }
    ]
}

# Optional fields
run["slug"] = "your-pipeline-slug"

# Make the POST request to create run
response = requests.post(
    f"{base_url}/v1/run",
    headers=headers,
    json=run
)

# Check if request was successful
if response.status_code == 200:
    result = response.json()
    print(result)
else:
    print(f"Error creating run: {response.status_code}")
    print(response.text)
