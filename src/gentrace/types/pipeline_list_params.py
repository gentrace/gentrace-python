# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Union, Optional
from typing_extensions import Literal, Annotated, TypeAlias, TypedDict

from .._utils import PropertyInfo

__all__ = ["PipelineListParams", "Slug", "SlugUnionMember1"]


class PipelineListParams(TypedDict, total=False):
    folder_id: Annotated[Optional[str], PropertyInfo(alias="folderId")]
    """The ID of the folder to filter pipelines by"""

    slug: Slug
    """Filter pipelines by slug"""


_SlugUnionMember1ReservedKeywords = TypedDict(
    "_SlugUnionMember1ReservedKeywords",
    {
        "in": List[str],
    },
    total=False,
)


class SlugUnionMember1(_SlugUnionMember1ReservedKeywords, total=False):
    contains: str

    ends_with: Annotated[str, PropertyInfo(alias="endsWith")]

    mode: Literal["insensitive", "default"]

    not_in: Annotated[List[str], PropertyInfo(alias="notIn")]

    search: str

    starts_with: Annotated[str, PropertyInfo(alias="startsWith")]


Slug: TypeAlias = Union[str, SlugUnionMember1]
