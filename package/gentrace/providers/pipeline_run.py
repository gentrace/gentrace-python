from typing import Dict, List
from gentrace.api import IngestionApi
from gentrace.providers.pipeline import Pipeline
from gentrace.providers.step_run import StepRun

class PipelineRun:
    def __init__(self, pipeline: Pipeline):
        self.pipeline = pipeline
        self.step_runs = []

    def get_pipeline(self) -> Pipeline:
        return self.pipeline

    async def get_openai(self):
        if "openai" in self.pipeline.pipeline_handlers:
            handler = self.pipeline.pipeline_handlers.get("openai")
            cloned_handler = handler.clone()
            cloned_handler.set_pipeline_run(self)
            return cloned_handler
        else:
            raise ValueError("Did not find OpenAI handler. Did you call setup() on the pipeline?")

    async def get_pinecone(self):
        if "pinecone" in self.pipeline.pipeline_handlers:
            handler = self.pipeline.pipeline_handlers.get("pinecone")
            cloned_handler = handler.clone()
            cloned_handler.set_pipeline_run(self)
            return cloned_handler
        else:
            raise ValueError("Did not find Pinecone handler. Did you call setup() on the pipeline?")

    def add_step_run(self, step_run: StepRun):
        self.step_runs.append(step_run)

    async def submit(self) -> Dict:
        ingestion_api = IngestionApi(self.pipeline.config)

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

        pipeline_post_response = await ingestion_api.pipeline_run_post(
            {
                "name": self.pipeline.id,
                "stepRuns": step_runs_data
            }
        )

        return pipeline_post_response.data
