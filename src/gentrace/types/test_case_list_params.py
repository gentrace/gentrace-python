# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Annotated, TypedDict

from .._utils import PropertyInfo
from .dataset_list import DatasetList

__all__ = ["TestCaseListParams"]


class TestCaseListParams(TypedDict, total=False):
    dataset_id: Annotated[str, PropertyInfo(alias="datasetId")]
    """Dataset ID"""

    pipeline_id: Annotated[str, PropertyInfo(alias="pipelineId")]
    """Filter to the datasets for a specific pipeline by UUID"""

    pipeline_slug: Annotated[DatasetList, PropertyInfo(alias="pipelineSlug")]
    """Pipeline slug"""
