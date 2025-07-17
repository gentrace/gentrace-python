# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, Optional

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = ["Experiment"]


class Experiment(BaseModel):
    id: str
    """Experiment UUID"""

    created_at: str = FieldInfo(alias="createdAt")
    """Creation timestamp (ISO 8601)"""

    metadata: Optional[Dict[str, object]] = None
    """Metadata"""

    name: Optional[str] = None
    """Friendly experiment name"""

    pipeline_id: str = FieldInfo(alias="pipelineId")
    """Pipeline UUID"""

    resource_path: Optional[str] = FieldInfo(alias="resourcePath", default=None)
    """Resource path to navigate to the experiment"""

    updated_at: str = FieldInfo(alias="updatedAt")
    """Last update timestamp (ISO 8601)"""
