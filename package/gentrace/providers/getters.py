from typing import Any, Dict

from gentrace.configuration import Configuration as GentraceConfiguration


class OpenAIGetter:
    annotated: bool = False
    openai_config: Dict = {}
    openai_handle: Any = None

    def __getattr__(self, name):
        print("Getting", name)
        if not self.annotated:
            from gentrace import api_key, host

            gentrace_config = GentraceConfiguration(host=host)
            gentrace_config.access_token = api_key

            from .llms.openai import annotate_pipeline_handler

            self.annotated = True
            annotate_pipeline_handler(self, gentrace_config)

        return getattr(self, name)

    def __setattr__(self, __name: str, __value: Any) -> None:
        print("Setting", __name, __value)
        pass

    @property
    def api_key(self):
        import openai

        return openai.api_key

    @api_key.setter
    def api_key(self, value):
        import openai

        openai.api_key = value


openai = OpenAIGetter()

__all__ = ["openai"]

# def pinecone(
#     config: Dict,
#     gentrace_api_key: str,
#     gentrace_base_path: Optional[str] = None,
# ) -> Any:
#     try:
#         from .vectorstores.pinecone import PineconePipelineHandler

#         pinecone_handler = PineconePipelineHandler(
#             gentrace_config=GentraceConfiguration(
#                 api_key=gentrace_api_key, base_path=gentrace_base_path
#             ),
#             config=config,
#         )
#         return pinecone_handler
#     except Exception as e:
#         raise ImportError(
#             "Please install Pinecone as a dependency with, e.g. `pip install pinecone`"
#         )
