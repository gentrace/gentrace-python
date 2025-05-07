# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import Required, Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["DatasetCreateParams"]


class DatasetCreateParams(TypedDict, total=False):
    description: Required[Optional[str]]
    """Dataset description"""

    name: Required[str]
    """Dataset name"""

    is_golden: Annotated[bool, PropertyInfo(alias="isGolden")]
    """Whether the dataset is golden"""

    pipeline_id: Annotated[str, PropertyInfo(alias="pipelineId")]
    """Pipeline ID (mutually exclusive with pipelineSlug)"""

    pipeline_slug: Annotated[str, PropertyInfo(alias="pipelineSlug")]
    """Pipeline slug (mutually exclusive with pipelineId)"""
