import io  # noqa: F401
import os
import tempfile
import typing

from gentrace.api_client import ApiClient
from gentrace.apis.tags.v1_api import V1Api
from gentrace.paths.v1_files_upload.post import SchemaForRequestBodyMultipartFormData
from gentrace.providers.init import (
    GENTRACE_CONFIG_STATE,
)
from gentrace.schemas import BinarySchema


def upload_file(
        file: typing.Union[BinarySchema, bytes, io.FileIO, io.BufferedReader]
) -> str:
    """Uploads a file to the Gentrace API.

    Parameters:
    - file (typing.Union[BinarySchema, bytes, io.FileIO, io.BufferedReader]): The file to be uploaded.

    Returns:
    - str: URL of the uploaded file.

    Raises:
    - ValueError: If the Gentrace API key is not initialized

    Note:
    Ensure that the Gentrace API is initialized by calling init() before using this function.
    """
    config = GENTRACE_CONFIG_STATE["global_gentrace_config"]
    if not config:
        raise ValueError("Gentrace API key not initialized. Call init() first.")

    api_client = ApiClient(configuration=config)
    api = V1Api(api_client=api_client)

    body = SchemaForRequestBodyMultipartFormData(file=file)
    response = api.v1_files_upload_post(body=body)
    url = response.body.get("url", None)
    return url


def upload_bytes(file_name: str, content: bytes):
    """Uploads a file as bytes to the Gentrace API.

    Parameters:
    - file_name (str): The name of the file to be uploaded.
    - content (bytes): The content of the file to be uploaded.

    Returns:
    - str: URL of the uploaded file.

    Raises:
    - ValueError: If the Gentrace API key is not initialized

    Note:
    Ensure that the Gentrace API is initialized by calling init() before using this function.
    """
    config = GENTRACE_CONFIG_STATE["global_gentrace_config"]
    if not config:
        raise ValueError("Gentrace API key not initialized. Call init() first.")

    temp_dir = tempfile.gettempdir()
    temp_file_path = os.path.join(temp_dir, file_name)

    with open(temp_file_path, "wb") as temp:
        temp.write(content)

    file = io.FileIO(temp_file_path, mode="rb")

    url = upload_file(file)

    file.close()
    os.remove(temp_file_path)

    return url
