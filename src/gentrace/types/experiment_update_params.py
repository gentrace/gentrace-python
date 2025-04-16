# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict
from typing_extensions import Literal, TypedDict

__all__ = ["ExperimentUpdateParams"]


class ExperimentUpdateParams(TypedDict, total=False):
    metadata: Dict[str, object]
    """Updated metadata for the experiment"""

    name: str
    """Updated name for the experiment"""

    status: Literal["GENERATING", "EVALUATING"]
    """Updated status of the experiment"""
