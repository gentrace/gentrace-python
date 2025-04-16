# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import Required, Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["DatasetCreateParams"]


class DatasetCreateParams(TypedDict, total=False):
    name: Required[str]
    """The name of the dataset"""

    description: Optional[str]
    """The description of the dataset"""

    is_golden: Annotated[bool, PropertyInfo(alias="isGolden")]
    """Toggle to set the dataset as the golden dataset for the pipeline"""

    pipeline_id: Annotated[str, PropertyInfo(alias="pipelineId")]
    """The ID of the pipeline to create the dataset for"""

    pipeline_slug: Annotated[str, PropertyInfo(alias="pipelineSlug")]
    """The slug of the pipeline to create the dataset for"""
