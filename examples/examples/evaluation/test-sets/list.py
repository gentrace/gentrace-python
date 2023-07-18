import os

import gentrace
from dotenv import load_dotenv

load_dotenv()

gentrace.init(
    api_key=os.getenv("GENTRACE_API_KEY"),
    host="http://localhost:3000/api/v1",
)

LABEL_NAME = "Monkies"

test_sets = gentrace.get_test_sets(LABEL_NAME)

for test_set in test_sets:
    print(test_set["id"])
