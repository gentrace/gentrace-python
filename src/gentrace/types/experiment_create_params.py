# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict
from typing_extensions import Required, Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["ExperimentCreateParams"]


class ExperimentCreateParams(TypedDict, total=False):
    pipeline_id: Required[Annotated[str, PropertyInfo(alias="pipelineId")]]
    """The ID of the pipeline to create the experiment for"""

    metadata: Dict[str, object]
    """Optional metadata for the experiment"""

    name: str
    """Friendly experiment name"""
