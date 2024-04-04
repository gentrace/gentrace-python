import typing_extensions

from gentrace.apis.tags import TagValues
from gentrace.apis.tags.v1_api import V1Api
from gentrace.apis.tags.v2_api import V2Api
from gentrace.apis.tags.feedback_api import FeedbackApi

TagToApi = typing_extensions.TypedDict(
    'TagToApi',
    {
        TagValues.V1: V1Api,
        TagValues.V2: V2Api,
        TagValues.FEEDBACK: FeedbackApi,
    }
)

tag_to_api = TagToApi(
    {
        TagValues.V1: V1Api,
        TagValues.V2: V2Api,
        TagValues.FEEDBACK: FeedbackApi,
    }
)
