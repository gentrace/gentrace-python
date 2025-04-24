# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from .._models import BaseModel

__all__ = ["TestCaseDeleteResponse"]


class TestCaseDeleteResponse(BaseModel):
    __test__ = False
    success: bool
    """A boolean indicating the deletion was successful"""
