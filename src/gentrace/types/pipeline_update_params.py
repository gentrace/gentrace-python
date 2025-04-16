# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Optional
from typing_extensions import Literal, Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = [
    "PipelineUpdateParams",
    "SavedRunsDisplay",
    "SavedRunsDisplayEvaluators",
    "SavedRunsDisplayFeedback",
    "SavedRunsDisplayInputs",
    "SavedRunsDisplayMetadata",
    "SavedRunsDisplayOutputs",
]


class PipelineUpdateParams(TypedDict, total=False):
    branch: Optional[str]
    """The branch of the pipeline"""

    display_name: Annotated[Optional[str], PropertyInfo(alias="displayName")]
    """The display name of the pipeline"""

    folder_id: Annotated[Optional[str], PropertyInfo(alias="folderId")]
    """The ID of the folder containing the pipeline.

    If not provided, the pipeline will be created at root level
    """

    is_archived: Annotated[bool, PropertyInfo(alias="isArchived")]
    """Whether the pipeline is archived"""

    labels: List[str]
    """Labels for the pipeline"""

    saved_runs_display: Annotated[Optional[SavedRunsDisplay], PropertyInfo(alias="savedRunsDisplay")]
    """Saved runs display configuration"""


class SavedRunsDisplayEvaluators(TypedDict, total=False):
    hide: List[str]


class SavedRunsDisplayFeedback(TypedDict, total=False):
    show: bool


_SavedRunsDisplayInputsReservedKeywords = TypedDict(
    "_SavedRunsDisplayInputsReservedKeywords",
    {
        "as": Literal["tabular", "json"],
    },
    total=False,
)


class SavedRunsDisplayInputs(_SavedRunsDisplayInputsReservedKeywords, total=False):
    hide: List[str]

    pretty: bool

    show_compact: Annotated[List[str], PropertyInfo(alias="showCompact")]


_SavedRunsDisplayMetadataReservedKeywords = TypedDict(
    "_SavedRunsDisplayMetadataReservedKeywords",
    {
        "as": Literal["tabular", "json"],
    },
    total=False,
)


class SavedRunsDisplayMetadata(_SavedRunsDisplayMetadataReservedKeywords, total=False):
    show: List[str]


_SavedRunsDisplayOutputsReservedKeywords = TypedDict(
    "_SavedRunsDisplayOutputsReservedKeywords",
    {
        "as": Literal["tabular", "json"],
    },
    total=False,
)


class SavedRunsDisplayOutputs(_SavedRunsDisplayOutputsReservedKeywords, total=False):
    hide: List[str]

    pretty: bool


class SavedRunsDisplay(TypedDict, total=False):
    evaluators: SavedRunsDisplayEvaluators

    feedback: SavedRunsDisplayFeedback

    inputs: SavedRunsDisplayInputs

    metadata: SavedRunsDisplayMetadata

    outputs: SavedRunsDisplayOutputs

    size: Literal["compact", "medium", "large", "full"]
