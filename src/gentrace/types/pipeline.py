# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, List, Optional
from datetime import datetime

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = ["Pipeline"]


class Pipeline(BaseModel):
    id: str
    """Pipeline UUID"""

    archived_at: Optional[datetime] = FieldInfo(alias="archivedAt", default=None)
    """Archive timestamp (ISO 8601)"""

    branch: Optional[str] = None
    """Branch name"""

    created_at: datetime = FieldInfo(alias="createdAt")
    """Creation timestamp (ISO 8601)"""

    display_name: Optional[str] = FieldInfo(alias="displayName", default=None)
    """Pipeline display name"""

    folder_id: Optional[str] = FieldInfo(alias="folderId", default=None)
    """Folder UUID"""

    golden_dataset_id: Optional[str] = FieldInfo(alias="goldenDatasetId", default=None)
    """Golden dataset UUID"""

    labels: List[str]
    """Labels"""

    organization_id: str = FieldInfo(alias="organizationId")
    """Organization UUID"""

    private_member_id: Optional[str] = FieldInfo(alias="privateMemberId", default=None)
    """Private member UUID"""

    saved_result_display: Optional[Dict[str, object]] = FieldInfo(alias="savedResultDisplay", default=None)
    """Saved result display configuration"""

    saved_runs_display: Optional[Dict[str, object]] = FieldInfo(alias="savedRunsDisplay", default=None)
    """Saved runs display configuration"""

    slug: str
    """Pipeline slug"""

    updated_at: datetime = FieldInfo(alias="updatedAt")
    """Last update timestamp (ISO 8601)"""

    version: int
    """Pipeline version (version 2 and beyond have tracing support)"""
