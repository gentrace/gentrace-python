import asyncio
import logging
import re
import sys
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

from gentrace.apis.tags.core_api import CoreApi
from gentrace.models import PipelineRunRequest
from gentrace.providers.init import GENTRACE_CONFIG_STATE

__all__ = [
    "to_date_string",
    "pipeline_run_post_background",
    "log_debug",
    "log_info",
    "log_warn",
]

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Create a stream handler that writes to stderr
stdout_handler = logging.StreamHandler()
logger.setLevel(logging.INFO)

formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
stdout_handler.setFormatter(formatter)

# Add the handlers to the logger
logger.addHandler(stdout_handler)


def to_date_string(time_value):
    utc_time = datetime.utcfromtimestamp(time_value)
    utc_time_str = utc_time.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    return utc_time_str[:-4] + "Z"


def log_debug(message, **params):
    log_level = GENTRACE_CONFIG_STATE["GENTRACE_LOG_LEVEL"]
    if not log_level:
        return

    library_log_level = logging.INFO if log_level == "info" else logging.WARN
    logger.setLevel(library_log_level)

    msg = logfmt(dict(message=message, **params))
    logger.debug(msg)


def log_info(message, **params):
    log_level = GENTRACE_CONFIG_STATE["GENTRACE_LOG_LEVEL"]
    if not log_level:
        return

    library_log_level = logging.INFO if log_level == "info" else logging.WARN
    logger.setLevel(library_log_level)

    msg = logfmt(dict(message=message, **params))
    logger.info(msg)


def log_warn(message, **params):
    log_level = GENTRACE_CONFIG_STATE["GENTRACE_LOG_LEVEL"]
    if not log_level:
        return

    library_log_level = logging.INFO if log_level == "info" else logging.WARN
    logger.setLevel(library_log_level)

    msg = logfmt(dict(message=message, **params))
    logger.warn(msg)


# Logger exception automatically logs the stack trace
def log_exception(message, **params):
    log_level = GENTRACE_CONFIG_STATE["GENTRACE_LOG_LEVEL"]
    if not log_level:
        return

    library_log_level = logging.INFO if log_level == "info" else logging.WARN
    logger.setLevel(library_log_level)

    logger.exception(message)


def logfmt(props):
    def fmt(key, val):
        # Handle case where val is a bytes or bytesarray
        if hasattr(val, "decode"):
            val = val.decode("utf-8")
        # Check if val is already a string to avoid re-encoding into ascii.
        if not isinstance(val, str):
            val = str(val)
        if re.search(r"\s", val):
            val = repr(val)
        # key should already be a string
        if re.search(r"\s", key):
            key = repr(key)
        return "{key}={val}".format(key=key, val=val)

    return " ".join([fmt(key, val) for key, val in sorted(props.items())])


async def pipeline_run_post_background(
    api_instance: CoreApi, pipeline_run_data: PipelineRunRequest
):
    def wrapped_api_invocation():
        try:
            log_info("Submitting PipelineRun to Gentrace")
            result = api_instance.pipeline_run_post(pipeline_run_data)
            log_info("Successfully submitted PipelineRun to Gentrace")
            return result
        except Exception as e:
            log_exception("Error submitting to Gentrace: ")
            return None

    with ThreadPoolExecutor() as executor:
        result = await asyncio.get_event_loop().run_in_executor(
            executor, wrapped_api_invocation
        )
    return result
