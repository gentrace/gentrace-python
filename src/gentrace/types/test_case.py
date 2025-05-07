# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, Optional

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = ["TestCase"]


class TestCase(BaseModel):
    __test__ = False
    id: str
    """Test Case UUID"""

    archived_at: Optional[str] = FieldInfo(alias="archivedAt", default=None)
    """Archive timestamp (ISO 8601)"""

    created_at: str = FieldInfo(alias="createdAt")
    """Creation timestamp (ISO 8601)"""

    dataset_id: str = FieldInfo(alias="datasetId")
    """Associated Dataset UUID"""

    deleted_at: Optional[str] = FieldInfo(alias="deletedAt", default=None)
    """Deletion timestamp (ISO 8601)"""

    expected_outputs: Optional[Dict[str, object]] = FieldInfo(alias="expectedOutputs", default=None)
    """Expected output data for the test case"""

    inputs: Dict[str, object]
    """Input data for the test case"""

    name: str
    """Test Case name"""

    pipeline_id: str = FieldInfo(alias="pipelineId")
    """Associated Pipeline UUID"""

    updated_at: str = FieldInfo(alias="updatedAt")
    """Last update timestamp (ISO 8601)"""
