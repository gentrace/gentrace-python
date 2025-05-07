# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List

from .._models import BaseModel
from .test_case import TestCase

__all__ = ["TestCaseList"]


class TestCaseList(BaseModel):
    __test__ = False
    data: List[TestCase]
