from typing import Any, Dict, Optional

from gentrace.configuration import Configuration as GentraceConfiguration


def openai(
    gentrace_api_key: str,
    gentrace_base_path: Optional[str] = None,
    config: Dict = None,
) -> Any:
    try:
        from .llms.openai import OpenAIPipelineHandler

        gentrace_config = GentraceConfiguration(
            api_key=gentrace_api_key, base_path=gentrace_base_path
        )

        OpenAIPipelineHandler.setup(config)
        openai_handler = OpenAIPipelineHandler(
            gentrace_config=gentrace_config,
            config=config,
        )

        # TODO: problem is that this needs to be annotated every time a method
        # is invoked.
        from .llms.openai import annotate_pipeline_handler

        return annotate_pipeline_handler(openai_handler, gentrace_config)
    except Exception as e:
        raise ImportError(
            "Please install OpenAI as a dependency with, e.g. `pip install openai`"
        )


def pinecone(
    config: Dict,
    gentrace_api_key: str,
    gentrace_base_path: Optional[str] = None,
) -> Any:
    try:
        from .vectorstores.pinecone import PineconePipelineHandler

        pinecone_handler = PineconePipelineHandler(
            gentrace_config=GentraceConfiguration(
                api_key=gentrace_api_key, base_path=gentrace_base_path
            ),
            config=config,
        )
        return pinecone_handler
    except Exception as e:
        raise ImportError(
            "Please install Pinecone as a dependency with, e.g. `pip install pinecone`"
        )
