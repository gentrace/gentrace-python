import inspect
from typing import Any, Optional


class Pipeline:
    def __init__(
        self,
        id: str,
        api_key: str,
        host: Optional[str] = None,
        openai_config: Any = None,
        pinecone_config: Optional[dict] = None,
    ):
        self.id = id
        self.config = {"api_key": api_key, "host": host}

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
