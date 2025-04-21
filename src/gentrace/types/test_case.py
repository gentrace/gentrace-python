# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, Optional
from datetime import datetime

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = ["TestCase"]


class TestCase(BaseModel):
    __test__ = False
    id: str
    """Test Case UUID"""

    archived_at: Optional[datetime] = FieldInfo(alias="archivedAt", default=None)
    """Archive timestamp (ISO 8601)"""

    created_at: datetime = FieldInfo(alias="createdAt")
    """Creation timestamp (ISO 8601)"""

    dataset_id: str = FieldInfo(alias="datasetId")
    """Associated Dataset UUID"""

    deleted_at: Optional[datetime] = FieldInfo(alias="deletedAt", default=None)
    """Deletion timestamp (ISO 8601)"""

    expected_outputs: Optional[Dict[str, object]] = FieldInfo(alias="expectedOutputs", default=None)
    """Expected output data for the test case"""

    inputs: Dict[str, object]
    """Input data for the test case"""

    name: str
    """Test Case name"""

    originating_run_id: Optional[str] = FieldInfo(alias="originatingRunId", default=None)
    """Originating Run UUID"""

    pipeline_id: str = FieldInfo(alias="pipelineId")
    """Associated Pipeline UUID"""

    updated_at: datetime = FieldInfo(alias="updatedAt")
    """Last update timestamp (ISO 8601)"""
