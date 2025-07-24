# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = ["Organization"]


class Organization(BaseModel):
    id: str
    """Organization UUID"""

    created_at: str = FieldInfo(alias="createdAt")
    """Creation timestamp (ISO 8601)"""

    default_pipeline_id: Optional[str] = FieldInfo(alias="defaultPipelineId", default=None)
    """Default pipeline ID for the organization"""

    name: str
    """Organization name"""

    slug: str
    """Organization slug"""

    updated_at: str = FieldInfo(alias="updatedAt")
    """Last update timestamp (ISO 8601)"""
