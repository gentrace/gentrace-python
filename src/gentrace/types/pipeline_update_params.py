# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["PipelineUpdateParams"]


class PipelineUpdateParams(TypedDict, total=False):
    display_name: Annotated[Optional[str], PropertyInfo(alias="displayName")]
    """Pipeline display name"""

    folder_id: Annotated[Optional[str], PropertyInfo(alias="folderId")]
    """Folder UUID"""

    is_archived: Annotated[bool, PropertyInfo(alias="isArchived")]
    """Whether the pipeline is archived"""
