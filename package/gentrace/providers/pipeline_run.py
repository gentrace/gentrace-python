import copy
import uuid
from typing import Dict, List, cast

from gentrace.api_client import ApiClient
from gentrace.apis.tags.ingestion_api import IngestionApi
from gentrace.configuration import Configuration
from gentrace.providers.pipeline import Pipeline
from gentrace.providers.step_run import StepRun
from gentrace.providers.utils import pipeline_run_post_async


class PipelineRun:
    def __init__(self, pipeline):
        self.pipeline: Pipeline = pipeline
        self.step_runs: List[StepRun] = []

    def get_pipeline(self):
        return self.pipeline

    def get_openai(self):
        if "openai" in self.pipeline.pipeline_handlers:
            handler = self.pipeline.pipeline_handlers.get("openai")
            cloned_handler = copy.deepcopy(handler)

            from .llms.openai import annotate_pipeline_handler

            annotated_handler = annotate_pipeline_handler(
                cloned_handler, self.pipeline.openai_config, self
            )

            return annotated_handler
        else:
            raise ValueError(
                "Did not find OpenAI handler. Did you call setup() on the pipeline?"
            )

    def get_pinecone(self):
        if "pinecone" in self.pipeline.pipeline_handlers:
            handler = self.pipeline.pipeline_handlers.get("pinecone")
            cloned_handler = copy.deepcopy(handler)
            cloned_handler.set_pipeline_run(self)
            import pinecone

            return cast(pinecone, cloned_handler)
        else:
            raise ValueError(
                "Did not find Pinecone handler. Did you call setup() on the pipeline?"
            )

    def add_step_run(self, step_run: StepRun):
        self.step_runs.append(step_run)

    async def asubmit(self) -> Dict:
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

        try:
            pipeline_post_response = await pipeline_run_post_async(
                ingestion_api, {"name": self.pipeline.id, "stepRuns": step_runs_data}
            )
            return {
                "pipelineRunId": pipeline_post_response.body.get_item_oapg(
                    "pipelineRunId"
                )
            }
        except Exception as e:
            print(f"Error submitting to Gentrace: {e}")
            return {"pipelineRunId": None}

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

        try:
            pipeline_post_response = ingestion_api.pipeline_run_post(
                { "id": uuid.uuid4(), "name": self.pipeline.id, "stepRuns": step_runs_data}
            )
            return {
                "pipelineRunId": pipeline_post_response.body.get_item_oapg(
                    "pipelineRunId"
                )
            }

        except Exception as e:
            print(f"Error submitting to Gentrace: {e}")
            return {"pipelineRunId": None}
