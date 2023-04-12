import copy
import json
from typing import Dict, List

from gentrace.api_client import ApiClient
from gentrace.apis.tags.ingestion_api import IngestionApi
from gentrace.configuration import Configuration
from gentrace.providers.step_run import StepRun


class PipelineRun:
    def __init__(self, pipeline):
        self.pipeline = pipeline
        self.step_runs: List[StepRun] = []

    def get_pipeline(self):
        return self.pipeline

    def get_openai(self):
        if "openai" in self.pipeline.pipeline_handlers:
            handler = self.pipeline.pipeline_handlers.get("openai")
            cloned_handler = copy.deepcopy(handler)
            import openai.api_resources as api

            from .llms.openai import (
                intercept_chat_completion,
                intercept_completion,
                intercept_embedding,
            )

            for name, cls in vars(api).items():
                if isinstance(cls, type):
                    # Create new class that inherits from the original class, don't directly monkey patch
                    # the original class
                    new_class = type(name, (cls,), {})
                    if name == "Completion":
                        new_class.create = intercept_completion(new_class.create)
                    elif name == "ChatCompletion":
                        new_class.create = intercept_chat_completion(new_class.create)
                    elif name == "Embedding":
                        new_class.create = intercept_embedding(new_class.create)

                    new_class.pipeline_run = self

                    setattr(cloned_handler, name, new_class)
                    # TODO: get the typing from the underlying model
                    # TODO: must work on a acreate() method, check that streaming works

            cloned_handler.set_pipeline_run(self)
            return cloned_handler
        else:
            raise ValueError(
                "Did not find OpenAI handler. Did you call setup() on the pipeline?"
            )

    def get_pinecone(self):
        if "pinecone" in self.pipeline.pipeline_handlers:
            handler = self.pipeline.pipeline_handlers.get("pinecone")
            cloned_handler = copy.deepcopy(handler)
            cloned_handler.set_pipeline_run(self)
            return cloned_handler
        else:
            raise ValueError(
                "Did not find Pinecone handler. Did you call setup() on the pipeline?"
            )

    def add_step_run(self, step_run: StepRun):
        self.step_runs.append(step_run)

    def submit(self) -> Dict:
        configuration = Configuration(host=self.pipeline.config.get("host"))
        configuration.access_token = self.pipeline.config.get("api_key")
        api_client = ApiClient(configuration=configuration)
        ingestion_api = IngestionApi(api_client=api_client)

        step_runs_data = [
            {
                "provider": {
                    "name": step_run.provider,
                    "invocation": step_run.invocation,
                    "modelParams": step_run.model_params,
                    "inputs": step_run.inputs,
                    "outputs": step_run.outputs,
                },
                "elapsedTime": step_run.elapsed_time,
                "startTime": step_run.start_time,
                "endTime": step_run.end_time,
            }
            for step_run in self.step_runs
        ]

        print("Step run: ", json.dumps(step_runs_data, indent=2))

        pipeline_post_response = ingestion_api.pipeline_run_post(
            {"name": self.pipeline.id, "stepRuns": step_runs_data}
        )

        return {
            "pipelineRunId": pipeline_post_response.body.get_item_oapg("pipelineRunId")
        }
