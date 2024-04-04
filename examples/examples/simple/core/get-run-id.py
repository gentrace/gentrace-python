import asyncio
import os

import gentrace
from dotenv import load_dotenv

load_dotenv()


async def main():
    gentrace.init(
        api_key=os.getenv("GENTRACE_API_KEY"),
        host="http://localhost:3000/api",
    )

    # example runID
    run_id = "5615b021-03cd-4cd9-9bc8-6a2f7bf4240e"
    run_data = await gentrace.get_run(run_id)

    print(run_data)

asyncio.run(main())
