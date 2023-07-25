import os

import gentrace
from dotenv import load_dotenv

load_dotenv()

PIPELINE_SLUG = "guess-the-year"

gentrace.init(
    api_key=os.getenv("GENTRACE_API_KEY"),
    run_name="vivek python run 2",
    host="http://localhost:3000/api/v1",
)

pipeline = gentrace.Pipeline(
    PIPELINE_SLUG,
    openai_config={
        "api_key": os.getenv("OPENAI_KEY"),
    },
)

pipeline.setup()


def create_embedding(test_case):
    runner = pipeline.start()

    openai_handle = runner.get_openai()

    output = openai_handle.Embedding.create(
        input="sample text", model="text-similarity-davinci-001"
    )

    return [output, runner]


result = gentrace.run_test(PIPELINE_SLUG, create_embedding)

print("Result: ", result)
