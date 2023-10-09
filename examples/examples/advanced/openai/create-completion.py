import os

import gentrace
from dotenv import load_dotenv

load_dotenv()

gentrace.init(
    api_key=os.getenv("GENTRACE_API_KEY"),
    host="http://localhost:3000/api/v1",
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

result = openai.completions.create(
    model="text-davinci-003",
    prompt_template="Hello world {{ name }}. What's the capital of Maine?",
    prompt_inputs={"name": "OpenAI"},
)

print("Response: ", result)

info = runner.submit()

print("Response: ", info["pipelineRunId"])

gentrace.flush()
