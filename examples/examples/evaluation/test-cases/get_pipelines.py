import os

import gentrace
from dotenv import load_dotenv

load_dotenv()

gentrace.init(
    api_key=os.getenv("GENTRACE_API_KEY"), host="http://localhost:3000/api"
)

all_pipelines = gentrace.get_pipelines()

pipelines = [pipeline["createdAt"] for pipeline in all_pipelines]

print("All pipelines: ", pipelines)
