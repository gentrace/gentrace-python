import os
from typing import Dict

import gentrace
from dotenv import load_dotenv

load_dotenv()

gentrace.init(
    api_key=os.getenv("GENTRACE_API_KEY"), host="http://localhost:3000/api"
)

DATASET_ID = "70a96925-db53-5c59-82b4-f42e988950a9"
PIPELINE_ID = "c10408c7-abde-5c19-b339-e8b1087c9b64"

dataset_cases = gentrace.get_test_cases(dataset_id=DATASET_ID)
pipeline_cases = gentrace.get_test_cases(pipeline_id=PIPELINE_ID)

def case_to_dict(case: Dict) -> Dict:
    return {
        "id": case.get("id"),
        "createdAt": case.get("createdAt")
    }

dataset_case_dict = {c["id"]: c for c in map(case_to_dict, dataset_cases)}
pipeline_case_dict = {c["id"]: c for c in map(case_to_dict, pipeline_cases)}
diff_cases = []

for case_id in set(dataset_case_dict.keys()) | set(pipeline_case_dict.keys()):
    if case_id not in dataset_case_dict:
        diff_cases.append(("Only in Pipeline", pipeline_case_dict[case_id]))
    elif case_id not in pipeline_case_dict:
        diff_cases.append(("Only in Dataset", dataset_case_dict[case_id]))
    elif dataset_case_dict[case_id] != pipeline_case_dict[case_id]:
        diff_cases.append(("Different", {
            "Dataset": dataset_case_dict[case_id],
            "Pipeline": pipeline_case_dict[case_id]
        }))

print(f"Differences between Dataset {DATASET_ID} and Pipeline {PIPELINE_ID}:")
for diff_type, case in diff_cases:
    print(f"{diff_type}:", end=" ")
    print(f"  {case}")