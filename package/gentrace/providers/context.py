from typing import Literal, Optional, TypedDict


class Render(TypedDict):
    type: Literal["html"]
    key: str


class Context(TypedDict):
    userId: str
    render: Optional[Render]
