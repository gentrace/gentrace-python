import os

import gentrace
from dotenv import load_dotenv

load_dotenv()

gentrace.init(
    api_key=os.getenv("GENTRACE_API_KEY"),
    host="http://localhost:3000/api",
)

pipeline = gentrace.Pipeline(
    "testing-pipeline-id",
    openai_config={
        "api_key": os.getenv("OPENAI_KEY"),
    },
)

pipeline.setup()

runner = pipeline.start()

openai = runner.get_openai()

embedding_result = openai.embeddings.create(
    input="sample text", model="text-similarity-davinci-001"
)

print("Embedding result: ", embedding_result)

completion_result = openai.completions.create(
    model="text-davinci-003",
    prompt_template="Hello world {{ name }}",
    prompt_inputs={"name": "test"},
)

print("Completion result: ", completion_result)

info = runner.submit()

print("Response: ", info["pipelineRunId"])

gentrace.flush()
