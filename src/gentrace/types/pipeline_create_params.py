# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import Required, Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["PipelineCreateParams"]


class PipelineCreateParams(TypedDict, total=False):
    slug: Required[str]
    """Pipeline slug"""

    display_name: Annotated[Optional[str], PropertyInfo(alias="displayName")]
    """Pipeline display name"""

    folder_id: Annotated[Optional[str], PropertyInfo(alias="folderId")]
    """Folder UUID"""
