import os

import gentrace
from dotenv import load_dotenv

load_dotenv()

gentrace.init(
    api_key=os.getenv("GENTRACE_API_KEY"), host="http://localhost:3000/api"
)

with open("examples/files/gentrace-icon.png", "rb") as f:
    # Remember to specify the file extension! The Gentrace UI relies on the file
    # extension to render file contents correctly.
    url = gentrace.upload_bytes("gentrace-icon.png", f.read())

print(url)

gentrace.create_test_case(
    "main",
    {
        "name": 'Gentrace Icon',
        'inputs': {
            'imageUrl': url,
        },
        "expectedOutputs": {
            "value": "Gentrace logo"
        }
    }
)
