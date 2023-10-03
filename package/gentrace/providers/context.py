from typing import Any, Dict, Literal, Optional, TypedDict, Union


class Render(TypedDict):
    type: Literal["html"]
    key: str


class MetadataValueRequired(TypedDict):
    type: str


MetadataValue = Union[MetadataValueRequired, Dict[str, Any]]


class Context(TypedDict):
    userId: Optional[str]
    render: Optional[Render]
    metadata: Optional[Dict[str, MetadataValue]]
    previousRunId: Optional[str]


class ResultContext(TypedDict):
    metadata: Optional[Dict[str, MetadataValue]]