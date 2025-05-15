# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = ["Dataset"]


class Dataset(BaseModel):
    id: str
    """Dataset UUID"""

    archived_at: Optional[str] = FieldInfo(alias="archivedAt", default=None)
    """Archive timestamp (ISO 8601)"""

    created_at: str = FieldInfo(alias="createdAt")
    """Creation timestamp (ISO 8601)"""

    description: Optional[str] = None
    """Dataset description"""

    name: str
    """Dataset name"""

    pipeline_id: str = FieldInfo(alias="pipelineId")
    """Pipeline UUID"""

    updated_at: str = FieldInfo(alias="updatedAt")
    """Last update timestamp (ISO 8601)"""
