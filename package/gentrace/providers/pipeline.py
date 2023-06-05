import inspect
from typing import Any, Optional

from gentrace.providers.init import GENTRACE_CONFIG_STATE


class Pipeline:
    def __init__(
        self,
        id: str,
        # @deprecated: use gentrace.providers.init.init() instead to set the Gentrace
        # API key
        api_key: Optional[str] = None,
        # @deprecated: use gentrace.providers.init.init() instead to set the Gentrace
        # base URL
        host: Optional[str] = None,
        openai_config: Any = None,
        pinecone_config: Optional[dict] = None,
    ):
        self.id = id

        if api_key:
            self.config = {"api_key": api_key, "host": host}
        else:
            if not GENTRACE_CONFIG_STATE["GENTRACE_API_KEY"]:
                raise ValueError(
                    "No Gentrace API key available. Please use init() to set the API key."
                )
            self.config = {
                "api_key": GENTRACE_CONFIG_STATE["GENTRACE_API_KEY"],
                "host": GENTRACE_CONFIG_STATE["GENTRACE_BASE_PATH"],
            }

        if openai_config:
            try:
                import openai
            except ImportError:
                raise ValueError(
                    "Could not import OpenAI python package. "
                    "Please install it with `pip install openai`."
                )

            for key in openai_config:
                if key not in openai.__all__:
                    raise ValueError(
                        f"Invalid key ({key}) in supplied OpenAI configuration."
                    )

            self.openai_config = openai_config
        else:
            self.openai_config = None

        if pinecone_config:
            try:
                import pinecone
            except ImportError:
                raise ValueError(
                    "Could not import Pinecone python package. "
                    "Please install it with `pip install pinecone-client`."
                )

            pinecone_init_args = inspect.signature(pinecone.init).parameters.keys()

            for key in pinecone_config:
                if key not in pinecone_init_args:
                    raise ValueError(
                        f"Invalid key ({key}) in supplied Pinecone configuration."
                    )
            self.pinecone_config = pinecone_config
        else:
            self.pinecone_config = None

        self.pipeline_handlers = {}

    def setup(self):
        if self.pinecone_config:
            try:
                from gentrace.providers.vectorstores.pinecone import (
                    PineconePipelineHandler,
                )

                pineconeHandler = PineconePipelineHandler(pipeline=self)
                pineconeHandler.init(api_key=self.pinecone_config["api_key"])
                self.pipeline_handlers["pinecone"] = pineconeHandler
            except ImportError:
                raise ImportError(
                    "Please install Pinecone as a dependency with, e.g. `pip install pinecone-client`"
                )

        if self.openai_config:
            try:
                from gentrace.providers.llms.openai import OpenAIPipelineHandler

                OpenAIPipelineHandler.setup(self.openai_config)
                openai_handler = OpenAIPipelineHandler(
                    self.config, self.openai_config, pipeline=self
                )
                self.pipeline_handlers["openai"] = openai_handler
            except ImportError:
                raise ImportError(
                    "Please install OpenAI as a dependency with, e.g. `pip install openai`"
                )

    def start(self):
        from gentrace.providers.pipeline_run import PipelineRun

        return PipelineRun(pipeline=self)
