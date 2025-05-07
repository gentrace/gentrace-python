# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List

from .._models import BaseModel
from .experiment import Experiment

__all__ = ["ExperimentList"]


class ExperimentList(BaseModel):
    data: List[Experiment]
