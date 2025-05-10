import logging
from typing import Any, Dict, Union, Literal, Optional

from .._types import NOT_GIVEN
from .client_handles import experiments_async

logger = logging.getLogger("gentrace")

"""
This module provides the core experiment control functionality for the Gentrace Python SDK.
It includes types and functions for starting and finishing experiments via the Gentrace API.
"""

async def start_experiment_api(
    *,
    pipelineId: str,
    metadata: Optional[Dict[str, Any]] = None,
    name: Optional[str] = None,
) -> str:
    """
    Starts a new experiment run by creating an experiment record via the Gentrace API.
    
    Args:
        pipelineId: The ID of the pipeline to create the experiment for.
        metadata: Optional metadata for the experiment.
        name: Friendly experiment name.
               
    Returns:
        str: The unique ID of the created experiment run.
    """
    logger.debug(f"Attempting to start Gentrace experiment via API for pipeline ID `{pipelineId}` with name `{name}`.")
    experiment = await experiments_async.create(
        pipeline_id=pipelineId,
        metadata=metadata if metadata is not None else NOT_GIVEN,
        name=name if name is not None else NOT_GIVEN,
    )
    
    return experiment.id

async def finish_experiment_api(*, id: str, error: Optional[Union[Exception, str]] = None) -> None:
    """
    Finishes an experiment run by updating its status via the Gentrace API.
    
    Args:
        id: The ID of the experiment to finish.
        error: Optional error information. If provided, it will be logged.
    """
    logger.debug(f"Attempting to finish Gentrace experiment via API for experiment ID `{id}`.")
    
    status_to_set: Literal["EVALUATING"] = "EVALUATING"
    # In the future, if the API supports errorMessage, it would be set here.
    # For now, we will log the error if present.

    if error:
        error_message = str(error) if isinstance(error, Exception) else error
        logger.info(f"Finishing Gentrace experiment `{id}` with a recorded error. Error details: {error_message}")
        # If there was an error, the status on the backend might be handled differently
        # or this might imply a different status if the API allowed. For now, we proceed
        # to set it to EVALUATING as per Node.js SDK's apparent behavior, or this
        # could be a point to set a specific "ERROR" status if available.

    try:
        await experiments_async.update(
            id,
            status=status_to_set,
        )
        logger.info(f"Successfully updated Gentrace experiment `{id}` to status `{status_to_set}` via API.")
    except Exception as e:
        logger.error(f"Failed to update Gentrace experiment `{id}` status via API. Details: {e}")
        # Optionally re-raise or handle as appropriate for the SDK's error handling strategy
        raise

__all__ = [
    "start_experiment_api",
    "finish_experiment_api",
]
