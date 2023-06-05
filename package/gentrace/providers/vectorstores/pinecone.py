import time
import uuid
from typing import Any, Dict, List, Optional, Tuple, Union

import pinecone
from pinecone import (
    FetchResponse,
    QueryResponse,
    QueryVector,
    SparseValues,
    UpsertResponse,
    Vector,
)
from pinecone.config import init

from gentrace.configuration import Configuration as GentraceConfiguration
from gentrace.providers.init import GENTRACE_CONFIG_STATE
from gentrace.providers.pipeline import Pipeline
from gentrace.providers.pipeline_run import PipelineRun
from gentrace.providers.step_run import StepRun
from gentrace.providers.utils import to_date_string


class ModifiedIndex(pinecone.Index):
    def __init__(
        self,
        index_name: str,
        pool_threads=1,
        *args,
        **kwargs,
    ):
        super().__init__(index_name, pool_threads, *args, **kwargs)

    def manage_step_run(
        self,
        step_run,
        pipeline_id,
    ):
        pipeline_run_id = None
        is_self_contained = not hasattr(self, "pipeline_run") and pipeline_id
        if is_self_contained:
            pipeline_run_id = str(uuid.uuid4())

        pipeline_run = self.pipeline_run if hasattr(self, "pipeline_run") else None

        if is_self_contained:
            from gentrace import api_key, host

            if api_key:
                gentrace_config = GentraceConfiguration(host=host)
                gentrace_config.access_token = api_key
            else:
                gentrace_config = GENTRACE_CONFIG_STATE["global_gentrace_config"]

            pipeline = Pipeline(
                id=pipeline_id,
                api_key=gentrace_config.access_token,
                host=gentrace_config.host,
            )

            pipeline_run = PipelineRun(pipeline=pipeline, id=pipeline_run_id)

        if pipeline_run:
            pipeline_run.add_step_run(step_run)

            if is_self_contained:
                pipeline_run.submit()

        return pipeline_run_id

    def fetch(
        self, ids: List[str], namespace: Optional[str] = None, **kwargs
    ) -> FetchResponse:
        start_time = time.time()
        pipeline_id = kwargs.pop("pipeline_id", None)

        response = super().fetch(ids, namespace, **kwargs)
        end_time = time.time()
        elapsed_time = int((end_time - start_time) * 1000)

        pipeline_run_id = self.manage_step_run(
            PineconeFetchStepRun(
                elapsed_time,
                to_date_string(start_time),
                to_date_string(end_time),
                {"ids": ids, "namespace": namespace},
                response.to_dict(),
            ),
            pipeline_id,
        )

        if pipeline_run_id:
            response["pipelineRunId"] = pipeline_run_id

        return response

    def update(
        self,
        id: str,
        values: Optional[List[float]] = None,
        set_metadata: Optional[
            Dict[str, Union[str, float, int, bool, List[int], List[float], List[str]]]
        ] = None,
        namespace: Optional[str] = None,
        sparse_values: Optional[
            Union[SparseValues, Dict[str, Union[List[float], List[int]]]]
        ] = None,
        **kwargs,
    ) -> Dict[str, any]:
        start_time = time.time()
        pipeline_id = kwargs.pop("pipeline_id", None)
        response = super().update(
            values, set_metadata, namespace, sparse_values, **kwargs
        )
        end_time = time.time()
        elapsed_time = int((end_time - start_time) * 1000)

        pipeline_run_id = self.manage_step_run(
            PineconeUpdateStepRun(
                elapsed_time,
                to_date_string(start_time),
                to_date_string(end_time),
                {
                    "id": id,
                    "values": values,
                    "set_metadata": set_metadata,
                    "namespace": namespace,
                    "sparse_values": sparse_values,
                },
                response,
            ),
            pipeline_id,
        )

        if pipeline_run_id:
            response["pipelineRunId"] = pipeline_run_id

        return response

    def query(
        self,
        vector: Optional[List[float]] = None,
        id: Optional[str] = None,
        queries: Optional[Union[List[QueryVector], List[Tuple]]] = None,
        top_k: Optional[int] = None,
        namespace: Optional[str] = None,
        filter: Optional[Dict[str, Union[str, float, int, bool, List, dict]]] = None,
        include_values: Optional[bool] = None,
        include_metadata: Optional[bool] = None,
        sparse_vector: Optional[
            Union[SparseValues, Dict[str, Union[List[float], List[int]]]]
        ] = None,
        **kwargs,
    ) -> QueryResponse:
        pipeline_id = kwargs.pop("pipeline_id", None)
        bound_query = super().query
        start_time = time.time()
        response = bound_query(
            vector,
            id,
            queries,
            top_k,
            namespace,
            filter,
            include_values,
            include_metadata,
            sparse_vector,
            **kwargs,
        )
        end_time = time.time()
        elapsed_time = int((end_time - start_time) * 1000)
        inputs = {
            "vector": vector,
            "id": id,
            "queries": queries,
            "namespace": namespace,
            "include_values": include_values,
            "include_metadata": include_metadata,
            "sparse_vector": sparse_vector,
        }
        model_params = {"top_k": top_k, "filter": filter}

        pipeline_run_id = self.manage_step_run(
            PineconeQueryStepRun(
                elapsed_time,
                to_date_string(start_time),
                to_date_string(end_time),
                {**inputs},
                {**model_params},
                response.to_dict(),
            ),
            pipeline_id,
        )

        if pipeline_run_id:
            response["pipelineRunId"] = pipeline_run_id

        return response

    def upsert(
        self,
        vectors: Union[List[Vector], List[tuple], List[dict]],
        namespace: Optional[str] = None,
        batch_size: Optional[int] = None,
        show_progress: bool = True,
        **kwargs,
    ) -> UpsertResponse:
        pipeline_id = kwargs.pop("pipeline_id", None)
        start_time = time.time()
        response = super().upsert(
            vectors, namespace, batch_size, show_progress, **kwargs
        )
        end_time = time.time()
        elapsed_time = int((end_time - start_time) * 1000)

        pipeline_run_id = self.manage_step_run(
            PineconeUpsertStepRun(
                elapsed_time,
                to_date_string(start_time),
                to_date_string(end_time),
                {
                    "vectors": vectors,
                    "namespace": namespace,
                    "batch_size": batch_size,
                    "show_progress": show_progress,
                },
                response.to_dict(),
            ),
            pipeline_id,
        )

        if pipeline_run_id:
            response["pipelineRunId"] = pipeline_run_id

        return response

    def delete(
        self,
        ids: Optional[List[str]] = None,
        delete_all: Optional[bool] = None,
        namespace: Optional[str] = None,
        filter: Optional[Dict[str, Union[str, float, int, bool, List, dict]]] = None,
        **kwargs,
    ) -> Dict[str, Any]:
        start_time = time.time()
        response = super().delete(ids, delete_all, namespace, filter, **kwargs)
        end_time = time.time()
        elapsed_time = int((end_time - start_time) * 1000)

        pipeline_id = kwargs.pop("pipeline_id", None)

        pipeline_run_id = self.manage_step_run(
            PineconeDeleteStepRun(
                elapsed_time,
                to_date_string(start_time),
                to_date_string(end_time),
                {
                    "ids": ids,
                    "delete_all": delete_all,
                    "namespace": namespace,
                    "filter": filter,
                },
                response,
            ),
            pipeline_id,
        )

        if pipeline_run_id:
            response["pipelineRunId"] = pipeline_run_id

        return response


def Index(index_name: str, pool_threads=1, *args, **kwargs):
    modified_index = ModifiedIndex(index_name, pool_threads, *args, **kwargs)
    return modified_index


class PineconePipelineHandler:
    pipeline: Optional[Pipeline] = None
    pipeline_run: Optional[PipelineRun] = None

    def __init__(self, pipeline=None):
        self.pipeline: Optional[Pipeline] = pipeline

    def __getattr__(self, name):
        import pinecone

        return getattr(pinecone, name)

    def set_pipeline_run(self, pipeline_run):
        self.pipeline_run: Optional[PipelineRun] = pipeline_run

    def init(self, *args, **kwargs):
        init(*args, **kwargs)

    def Index(self, *args, **kwargs):
        modified_index = self.ModifiedIndexContained(self.pipeline_run, *args, **kwargs)
        return modified_index

    class ModifiedIndexContained(ModifiedIndex):
        def __init__(self, pipeline_run, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.pipeline_run = pipeline_run


# Assign exported member function to PineconePipelineHandler
for exported_member in dir(pinecone):
    if (
        not exported_member.startswith("__")
        and exported_member != "Index"
        and exported_member != "init"
    ):
        retrieved_member = getattr(pinecone, exported_member)
        setattr(
            PineconePipelineHandler,
            exported_member,
            staticmethod(retrieved_member)
            if callable(retrieved_member)
            else retrieved_member,
        )


def annotate_pinecone_module():
    # Directly modify the pinecone module by changing the Index class that's used.
    pinecone.Index = Index
    pass


class PineconeFetchStepRun(StepRun):
    def __init__(
        self,
        elapsed_time: int,
        start_time: str,
        end_time: str,
        inputs: dict,
        response: dict,
    ):
        super().__init__(
            "pinecone",
            "pinecone_indexFetch",
            elapsed_time,
            start_time,
            end_time,
            inputs,
            {},
            response,
        )
        self.inputs = inputs
        self.response = response


class PineconeQueryStepRun(StepRun):
    def __init__(
        self,
        elapsed_time: int,
        start_time: str,
        end_time: str,
        inputs: dict,
        model_params: dict,
        response: dict,
    ):
        super().__init__(
            "pinecone",
            "pinecone_indexQuery",
            elapsed_time,
            start_time,
            end_time,
            inputs,
            model_params,
            response,
        )
        self.inputs = inputs
        self.response = response


class PineconeUpdateStepRun(StepRun):
    def __init__(
        self,
        elapsed_time: int,
        start_time: str,
        end_time: str,
        inputs: dict,
        response: dict,
    ):
        super().__init__(
            "pinecone",
            "pinecone_indexUpdate",
            elapsed_time,
            start_time,
            end_time,
            inputs,
            {},
            response,
        )
        self.inputs = inputs
        self.response = response


class PineconeUpsertStepRun(StepRun):
    def __init__(
        self,
        elapsed_time: int,
        start_time: str,
        end_time: str,
        inputs: dict,
        response: dict,
    ):
        super().__init__(
            "pinecone",
            "pinecone_indexUpsert",
            elapsed_time,
            start_time,
            end_time,
            inputs,
            {},
            response,
        )
        self.inputs = inputs
        self.response = response


class PineconeDeleteStepRun(StepRun):
    def __init__(
        self,
        elapsed_time: int,
        start_time: str,
        end_time: str,
        inputs: dict,
        response: dict,
    ):
        super().__init__(
            "pinecone",
            "pinecone_indexDelete1",
            elapsed_time,
            start_time,
            end_time,
            inputs,
            {},
            response,
        )
        self.inputs = inputs
        self.response = response
