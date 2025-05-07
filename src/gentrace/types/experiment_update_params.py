# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Optional
from typing_extensions import Literal, TypedDict

__all__ = ["ExperimentUpdateParams"]


class ExperimentUpdateParams(TypedDict, total=False):
    metadata: Optional[Dict[str, object]]
    """Metadata"""

    name: Optional[str]
    """Friendly experiment name"""

    status: Literal["GENERATING", "EVALUATING"]
    """Status"""
