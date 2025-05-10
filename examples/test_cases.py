import asyncio

from gentrace.lib import init, test_cases_async

DATASET_ID = "a4eb18dc-8738-4056-a363-ab57845c5ec9"


async def main() -> None:
    init()

    response = await test_cases_async.list(dataset_id=DATASET_ID)
    for test_case in response.data:
        print(f"ID: {test_case.id}, Name: {test_case.name}")


if __name__ == "__main__":
    asyncio.run(main())
