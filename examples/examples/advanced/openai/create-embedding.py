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

result = openai.embeddings.create(
    input="sample text", model="text-embedding-ada-002"
)

print("Result: ", result)

info = runner.submit()

print("Info: ", info)

gentrace.flush()
