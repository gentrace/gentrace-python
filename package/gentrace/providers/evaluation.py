from typing import Dict, Optional, TypedDict

from gentrace.api_client import ApiClient
from gentrace.apis.tags.core_api import CoreApi
from gentrace.configuration import Configuration


class Run(TypedDict):
    runId: str


class Evaluation:
    def __init__(
        self,
        api_key: str,
        host: Optional[str] = None,
    ):
        self.api_key = api_key
        self.host = host

        configuration = Configuration(host=self.host)
        configuration.access_token = self.api_key

        api_client = ApiClient(configuration=configuration)
        self.core_api = CoreApi(api_client=api_client)

    def get_test_cases(self, set_id: str):
        response = self.core_api.test_case_get({"setId": set_id})
        data = response.body
        return data["testCases"]

    def submit_test_results(
        self, set_id: str, source: str, test_results: list[Dict]
    ) -> Run:
        response = self.core_api.test_run_post(
            {
                "setId": set_id,
                "source": source,
                "testResults": test_results,
            }
        )
        data = response.body
        return data
