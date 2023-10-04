import os

import gentrace
from dotenv import load_dotenv
from pipeline import pipeline

load_dotenv()

gentrace.init(os.getenv("GENTRACE_API_KEY"))

PIPELINE_SLUG = "your-pipeline-slug"

def main():
    test_cases = gentrace.get_test_cases(PIPELINE_SLUG)

    outputs = [] 
    for test_case in test_cases:
        inputs = test_case["inputs"]
        result = pipeline(inputs)
        outputs.append(result)

    # This SDK method creates a single run entity on our servers
    response = gentrace.submit_test_result(PIPELINE_SLUG, test_cases, outputs, {
      "metadata": {
        "promptVariantId": {
          "type": "string",
          "value": "SGVsbG8sIFdvcmxkIQ=="
        }
      }
    })
   
    print("Run ID: ", response["runId"])

main()