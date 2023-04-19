from typing import Any, Dict, Optional, cast

from gentrace.configuration import Configuration as GentraceConfiguration


class ProvidersGetter:
    openai_config: Dict = {}

    openai_handle: Any = None

    def get_openai(self):
        if self.openai_handle:
            return self.openai_handle

        try:
            from gentrace import api_key, host

            from .llms.openai import OpenAIPipelineHandler

            gentrace_config = GentraceConfiguration(host=host)
            gentrace_config.access_token = api_key

            OpenAIPipelineHandler.setup(self.openai_config)
            openai_handler = OpenAIPipelineHandler(
                gentrace_config=gentrace_config,
                config=self.openai_config,
            )

            from .llms.openai import annotate_pipeline_handler

            annotated_handler = annotate_pipeline_handler(
                openai_handler, gentrace_config
            )

            import openai

            # TODO: Could not find an easy way to create a union type with openai and
            # OpenAIPipelineHandler, so we just use openai.
            typed_cloned_handler = cast(openai, annotated_handler)
            self.openai_handle = typed_cloned_handler
            return typed_cloned_handler
        except Exception as e:
            raise ImportError(
                "Please install OpenAI as a dependency with, e.g. `pip install openai`"
            )

    def __getattr__(self, name):
        if name == "openai":
            return self.get_openai()

    def __setattr__(self, name, value):
        if name.startswith("openai_"):
            self.openai_config[name[7:]] = value
        else:
            raise AttributeError("Invalid attribute")


providers = ProvidersGetter()

__all__ = ["providers"]

# def openai(
#     gentrace_api_key: str,
#     gentrace_base_path: Optional[str] = None,
#     config: Dict = None,
# ) -> Any:
#     try:
#         from .llms.openai import OpenAIPipelineHandler

#         gentrace_config = GentraceConfiguration(
#             api_key=gentrace_api_key, base_path=gentrace_base_path
#         )

#         OpenAIPipelineHandler.setup(config)
#         openai_handler = OpenAIPipelineHandler(
#             gentrace_config=gentrace_config,
#             config=config,
#         )

#         # TODO: problem is that this needs to be annotated every time a method
#         # is invoked.
#         from .llms.openai import annotate_pipeline_handler

#         return annotate_pipeline_handler(openai_handler, gentrace_config)
#     except Exception as e:
#         raise ImportError(
#             "Please install OpenAI as a dependency with, e.g. `pip install openai`"
#         )


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
