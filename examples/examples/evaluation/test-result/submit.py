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


def create_embedding_callback(test_case):
    runner = pipeline.start()

    openai_handle = runner.get_openai()

    output = openai_handle.embeddings.create(
        input="sample text", model="text-embedding-3-small"
    )

    return [output, runner]


result = gentrace.run_test(PIPELINE_SLUG, create_embedding_callback, context={
    "metadata": {
        "promptString": {
            "type": "string",
            "value": "testing"
        }
    }
}, result_name="Testing")

print("Result: ", result)
