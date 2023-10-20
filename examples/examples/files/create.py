import os

import gentrace
from dotenv import load_dotenv

load_dotenv()

gentrace.init(
    api_key=os.getenv("GENTRACE_API_KEY"), host="http://localhost:3000/api"
)

with open("examples/files/gentrace-icon.png", "rb") as f:
    url = gentrace.upload_file(f)

    print("Gentrace URL: ", url)

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
