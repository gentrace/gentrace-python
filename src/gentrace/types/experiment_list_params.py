# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["ExperimentListParams"]


class ExperimentListParams(TypedDict, total=False):
    pipeline_id: Annotated[str, PropertyInfo(alias="pipelineId")]
    """Filter to the datasets for a specific pipeline by UUID"""
