import asyncio
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

from gentrace.apis.tags.ingestion_api import IngestionApi
from gentrace.models import PipelineRunRequest

__all__ = ["to_date_string"]


def to_date_string(time_value):
    utc_time = datetime.utcfromtimestamp(time_value)
    utc_time_str = utc_time.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    return utc_time_str[:-4] + "Z"


async def pipeline_run_post_background(
    api_instance: IngestionApi, pipeline_run_data: PipelineRunRequest
):
    with ThreadPoolExecutor() as executor:
        result = await asyncio.get_event_loop().run_in_executor(
            executor, api_instance.pipeline_run_post, pipeline_run_data
        )
    return result
