import asyncio
import concurrent
import copy
import inspect
import threading
import uuid
from typing import Dict, List, Optional, cast

from gentrace.api_client import ApiClient
from gentrace.apis.tags.core_api import CoreApi
from gentrace.configuration import Configuration
from gentrace.providers.pipeline import Pipeline
from gentrace.providers.step_run import StepRun
from gentrace.providers.utils import pipeline_run_post_background

_pipeline_run_loop = None
_pipeline_tasks = []


# https://stackoverflow.com/a/63110035/1057411
def fire_and_forget(coro):
    global _pipeline_run_loop, _pipeline_tasks
    if _pipeline_run_loop is None:
        _pipeline_run_loop = asyncio.new_event_loop()
        threading.Thread(target=_pipeline_run_loop.run_forever, daemon=True).start()
    if inspect.iscoroutine(coro):
        task = asyncio.run_coroutine_threadsafe(coro, _pipeline_run_loop)
        _pipeline_tasks.append(task)


def flush():
    global _pipeline_tasks
    if _pipeline_tasks:
        # Wait for all tasks to complete
        concurrent.futures.wait(_pipeline_tasks)
        _pipeline_tasks.clear()


class PipelineRun:
    def __init__(self, pipeline, id: Optional[str] = None):
        self.pipeline: Pipeline = pipeline
        self.pipeline_run_id: str = id or str(uuid.uuid4())
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

            import openai

            # TODO: Could not find an easy way to create a union type with openai and
            # OpenAIPipelineHandler, so we just use openai.
            typed_cloned_handler = cast(openai, annotated_handler)

            return typed_cloned_handler
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
        core_api = CoreApi(api_client=api_client)

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

        pipeline_run_id = str(uuid.uuid4())

        try:
            pipeline_post_response = await pipeline_run_post_background(
                core_api,
                {
                    "id": pipeline_run_id,
                    "name": self.pipeline.id,
                    "stepRuns": step_runs_data,
                },
            )
            return {
                "pipelineRunId": pipeline_post_response.body.get_item_oapg(
                    "pipelineRunId"
                )
            }
        except Exception as e:
            print(f"Error submitting to Gentrace: {e}")
            return {"pipelineRunId": None}

    def submit(self, wait_for_server=False) -> Dict:
        configuration = Configuration(host=self.pipeline.config.get("host"))
        configuration.access_token = self.pipeline.config.get("api_key")

        api_client = ApiClient(configuration=configuration)
        core_api = CoreApi(api_client=api_client)

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

        if len(step_runs_data) == 0:
            return {"pipelineRunId": None}

        if not wait_for_server:
            fire_and_forget(
                pipeline_run_post_background(
                    core_api,
                    {
                        "id": self.pipeline_run_id,
                        "name": self.pipeline.id,
                        "stepRuns": step_runs_data,
                    },
                )
            )

            return {"pipelineRunId": self.pipeline_run_id}

        if wait_for_server:
            try:
                pipeline_post_response = core_api.pipeline_run_post(
                    {
                        "id": self.pipeline_run_id,
                        "name": self.pipeline.id,
                        "stepRuns": step_runs_data,
                    }
                )
                return {
                    "pipelineRunId": pipeline_post_response.body.get_item_oapg(
                        "pipelineRunId"
                    )
                }

            except Exception as e:
                print(f"Error submitting to Gentrace: {e}")
                return {"pipelineRunId": None}
