# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List

from .._models import BaseModel
from .pipeline import Pipeline

__all__ = ["PipelineListResponse"]


class PipelineListResponse(BaseModel):
    data: List[Pipeline]
