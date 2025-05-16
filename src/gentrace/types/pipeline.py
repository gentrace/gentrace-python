# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = ["Pipeline"]


class Pipeline(BaseModel):
    id: str
    """Pipeline UUID"""

    archived_at: Optional[str] = FieldInfo(alias="archivedAt", default=None)
    """Archive timestamp (ISO 8601)"""

    created_at: str = FieldInfo(alias="createdAt")
    """Creation timestamp (ISO 8601)"""

    display_name: Optional[str] = FieldInfo(alias="displayName", default=None)
    """Pipeline display name"""

    folder_id: Optional[str] = FieldInfo(alias="folderId", default=None)
    """Folder UUID"""

    golden_dataset_id: Optional[str] = FieldInfo(alias="goldenDatasetId", default=None)
    """Golden dataset UUID"""

    slug: str
    """Pipeline slug"""

    updated_at: str = FieldInfo(alias="updatedAt")
    """Last update timestamp (ISO 8601)"""
