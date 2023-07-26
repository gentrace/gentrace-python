import typing_extensions

from gentrace.apis.tags import TagValues
from gentrace.apis.tags.core_api import CoreApi
from gentrace.apis.tags.feedback_api import FeedbackApi

TagToApi = typing_extensions.TypedDict(
    "TagToApi",
    {
        TagValues.CORE: CoreApi,
        TagValues.FEEDBACK: FeedbackApi,
    },
)

tag_to_api = TagToApi(
    {
        TagValues.CORE: CoreApi,
        TagValues.FEEDBACK: FeedbackApi,
    }
)
