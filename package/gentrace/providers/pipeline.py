import inspect
from typing import Optional, Any

from gentrace.configuration import Configuration as GentraceConfiguration
from gentrace.providers.pipeline_run import PipelineRun


class Pipeline:
    def __init__(
        self,
        id: str,
        api_key: str,
        base_path: Optional[str] = None,
        openai_config: Any = None,
        pinecone_config: Optional[dict] = None,
    ):
        self.id = id
        self.config = GentraceConfiguration(api_key=api_key, base_path=base_path)
        
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
                  raise ValueError(f"Invalid key ({key}) in supplied OpenAI configuration.")

          self.openAIConfig = openai_config

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
                    raise ValueError(f"Invalid key ({key}) in supplied Pinecone configuration.")
            self.pineconeConfig = pinecone_config

        self.pipelineHandlers = {}

    def setup(self):
        if self.pineconeConfig:
            try:
                from gentrace.providers.vectorstores.pinecone import PineconePipelineHandler

                pineconeHandler = PineconePipelineHandler(pipeline=self)
                pineconeHandler.init(**self.pineconeConfig)
                self.pipelineHandlers["pinecone"] = pineconeHandler
            except ImportError:
                raise ImportError(
                    "Please install Pinecone as a dependency with, e.g. `pip install pinecone-client`"
                )

        if self.openAIConfig:
            try:
                from gentrace.providers.llms.openai import OpenAIPipelineHandler
                OpenAIPipelineHandler.setup(self.openAIConfig)
                openAIHandler = OpenAIPipelineHandler(pipeline=self)
                self.pipelineHandlers["openai"] = openAIHandler
            except ImportError:
                raise ImportError(
                    "Please install OpenAI as a dependency with, e.g. `pip install openai`"
                )

    def start(self):
        return PipelineRun(pipeline=self)

