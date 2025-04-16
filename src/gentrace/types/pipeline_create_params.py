# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Optional
from typing_extensions import Literal, Required, Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["PipelineCreateParams"]


class PipelineCreateParams(TypedDict, total=False):
    slug: Required[str]
    """A URL-friendly identifier (lowercase alphanumeric with dashes)"""

    branch: Optional[str]
    """The branch of the pipeline"""

    display_name: Annotated[Optional[str], PropertyInfo(alias="displayName")]
    """The display name of the pipeline"""

    folder_id: Annotated[Optional[str], PropertyInfo(alias="folderId")]
    """The ID of the folder containing the pipeline.

    If not provided, the pipeline will be created at root level
    """

    is_private: Annotated[Optional[bool], PropertyInfo(alias="isPrivate")]
    """Whether the pipeline is private"""

    labels: List[str]
    """Labels for the pipeline"""

    version: Literal[1, 2]
    """The version of the pipeline"""
