import typing_extensions

from gentrace.apis.paths.pipeline_run import PipelineRun
from gentrace.apis.paths.test_case import TestCase
from gentrace.apis.paths.test_run import TestRun
from gentrace.paths import PathValues

PathToApi = typing_extensions.TypedDict(
    "PathToApi",
    {
        PathValues.PIPELINERUN: PipelineRun,
        PathValues.TESTCASE: TestCase,
        PathValues.TESTRUN: TestRun,
    },
)

path_to_api = PathToApi(
    {
        PathValues.PIPELINERUN: PipelineRun,
        PathValues.TESTCASE: TestCase,
        PathValues.TESTRUN: TestRun,
    }
)
