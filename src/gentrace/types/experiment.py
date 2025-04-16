# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, Optional
from datetime import datetime
from typing_extensions import Literal

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = ["Experiment"]


class Experiment(BaseModel):
    id: str
    """Experiment UUID"""

    branch: Optional[str] = None
    """Git branch"""

    commit: Optional[str] = None
    """Git commit hash"""

    created_at: datetime = FieldInfo(alias="createdAt")
    """Creation timestamp (ISO 8601)"""

    metadata: Optional[Dict[str, object]] = None
    """Metadata"""

    name: Optional[str] = None
    """Friendly experiment name"""

    pipeline_id: str = FieldInfo(alias="pipelineId")
    """Pipeline UUID"""

    status: Literal["GENERATING", "EVALUATING"]
    """Status"""

    updated_at: datetime = FieldInfo(alias="updatedAt")
    """Last update timestamp (ISO 8601)"""
