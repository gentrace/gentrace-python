import io  # noqa: F401
import typing

from gentrace.api_client import ApiClient
from gentrace.apis.tags.core_api import CoreApi
from gentrace.paths.files_upload.post import SchemaForRequestBodyMultipartFormData
from gentrace.schemas import BinarySchema
from gentrace.providers.init import (
    GENTRACE_CONFIG_STATE,
)


def upload_file(
    file: typing.Union[BinarySchema, bytes, io.FileIO, io.BufferedReader]
) -> str:
    """Creates multiple test cases for a specified pipeline using the Gentrace API.

    Parameters:
    - pipeline_slug (str): The unique identifier of the pipeline to which the test cases should be added.
    - payload (List[TestCaseDict]): The array payload containing the test cases to be created.

    Returns:
    - int: Count of test cases created.

    Raises:
    - ValueError: If the Gentrace API key is not initialized or if the pipeline_slug is not passed.

    Note:
    Ensure that the Gentrace API is initialized by calling init() before using this function.
    """
    config = GENTRACE_CONFIG_STATE["global_gentrace_config"]
    if not config:
        raise ValueError("Gentrace API key not initialized. Call init() first.")

    api_client = ApiClient(configuration=config)
    api = CoreApi(api_client=api_client)

    body = SchemaForRequestBodyMultipartFormData(file=file)
    response = api.files_upload_post(body=body)
    url = response.body.get("url", None)
    return url
