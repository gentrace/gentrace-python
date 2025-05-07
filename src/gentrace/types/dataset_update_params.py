# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["DatasetUpdateParams"]


class DatasetUpdateParams(TypedDict, total=False):
    description: Optional[str]
    """Dataset description"""

    is_archived: Annotated[bool, PropertyInfo(alias="isArchived")]
    """Archive the dataset"""

    is_golden: Annotated[bool, PropertyInfo(alias="isGolden")]
    """Set the dataset as the golden dataset"""

    name: str
    """Dataset name"""
