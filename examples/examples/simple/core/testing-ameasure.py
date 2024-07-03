import asyncio
import os
import time
from datetime import datetime
from typing import Optional

import gentrace
from dotenv import load_dotenv
from pydantic import BaseModel, Field

load_dotenv()


class User(BaseModel):
    id: int
    name: str
    email: str
    age: int = Field(..., ge=0)
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.now)
    notes: Optional[str] = None


def example_response(user):
    time.sleep(1)
    print("User: ", user.name)
    return user


gentrace.init(
    api_key=os.getenv("GENTRACE_API_KEY"),
    host="http://localhost:3000/api",
)

# example existing pipelines

PIPELINE_SLUG = "guess-the-year"
pipeline_by_slug = gentrace.Pipeline(PIPELINE_SLUG)

PIPELINE_ID = "c10408c7-abde-5c19-b339-e8b1087c9b64"
pipeline_by_id = gentrace.Pipeline(id=PIPELINE_ID)

pipeline = pipeline_by_slug


async def measure_func(user):
    return example_response(user)


async def example_handler(pipeline_run_test_case):
    (runner, test_case) = pipeline_run_test_case
    user = User(
        id=1,
        name="John Doe",
        email="john@example.com",
        age=30,
    )
    await runner.ameasure(
        measure_func,
        user=user
    )


async def main():
    pipeline_run_test_cases = gentrace.get_test_runners(pipeline)

    for pipeline_run_test_case in pipeline_run_test_cases:
        await example_handler(pipeline_run_test_case)

    result = gentrace.submit_test_runners(pipeline, pipeline_run_test_cases)
    print("Result: ", result)


asyncio.run(main())
