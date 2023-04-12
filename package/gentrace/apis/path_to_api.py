import typing_extensions

from gentrace.apis.paths.pipeline_run import PipelineRun
from gentrace.paths import PathValues

PathToApi = typing_extensions.TypedDict(
    "PathToApi",
    {
        PathValues.PIPELINERUN: PipelineRun,
    },
)

path_to_api = PathToApi(
    {
        PathValues.PIPELINERUN: PipelineRun,
    }
)
