import os

import gentrace
from dotenv import load_dotenv

load_dotenv()

PIPELINE_SLUG = "guess-the-year"

gentrace.init(
    api_key=os.getenv("GENTRACE_API_KEY"),
    run_name="vivek python run 2",
    host="http://localhost:3000/api",
)

pipeline = gentrace.Pipeline(
    PIPELINE_SLUG,
    openai_config={
        "api_key": os.getenv("OPENAI_KEY"),
    },
)

pipeline.setup()

pipeline = gentrace.Pipeline(
    "main",
    openai_config={
        "api_key": os.getenv("OPENAI_KEY"),
    },
)

pipeline.setup()


def create_callback(test_case):
    runner = pipeline.start()
    client = runner.get_openai()
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "contentTemplate": "Say this is a {{ value }}",
                "contentInputs": {
                    "value": "test"
                }
            }
        ],
        model="gpt-3.5-turbo",
    )
    return [chat_completion, runner]


result = gentrace.run_test(PIPELINE_SLUG, create_callback)

print("Result: ", result.get('resultId'))
