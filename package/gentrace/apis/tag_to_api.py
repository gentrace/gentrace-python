import typing_extensions

from gentrace.apis.tags import TagValues
from gentrace.apis.tags.ingestion_api import IngestionApi
from gentrace.apis.tags.feedback_api import FeedbackApi

TagToApi = typing_extensions.TypedDict(
    'TagToApi',
    {
        TagValues.INGESTION: IngestionApi,
        TagValues.FEEDBACK: FeedbackApi,
    }
)

tag_to_api = TagToApi(
    {
        TagValues.INGESTION: IngestionApi,
        TagValues.FEEDBACK: FeedbackApi,
    }
)
