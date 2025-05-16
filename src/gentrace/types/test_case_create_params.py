# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict
from typing_extensions import Required, Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["TestCaseCreateParams"]


class TestCaseCreateParams(TypedDict, total=False):
    dataset_id: Required[Annotated[str, PropertyInfo(alias="datasetId")]]
    """Dataset UUID"""

    inputs: Required[Dict[str, object]]
    """Test case inputs as a JSON object"""

    name: Required[str]
    """Test case name"""

    expected_outputs: Annotated[Dict[str, object], PropertyInfo(alias="expectedOutputs")]
    """Optional expected outputs as a JSON object"""
