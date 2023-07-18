import typing_extensions

from gentrace.apis.paths.pipeline_run import PipelineRun
from gentrace.apis.paths.test_case import TestCase
from gentrace.apis.paths.test_run import TestRun
from gentrace.apis.paths.test_sets import TestSets
from gentrace.paths import PathValues

PathToApi = typing_extensions.TypedDict(
    "PathToApi",
    {
        PathValues.PIPELINERUN: PipelineRun,
        PathValues.TESTCASE: TestCase,
        PathValues.TESTRUN: TestRun,
        PathValues.TESTSETS: TestSets,
    },
)

path_to_api = PathToApi(
    {
        PathValues.PIPELINERUN: PipelineRun,
        PathValues.TESTCASE: TestCase,
        PathValues.TESTRUN: TestRun,
        PathValues.TESTSETS: TestSets,
    }
)
