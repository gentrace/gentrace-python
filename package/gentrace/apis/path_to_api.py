import typing_extensions

from gentrace.apis.paths.pipelines import Pipelines
from gentrace.apis.paths.run import Run
from gentrace.apis.paths.test_case import TestCase
from gentrace.apis.paths.test_result import TestResult
from gentrace.apis.paths.test_run import TestRun
from gentrace.paths import PathValues

PathToApi = typing_extensions.TypedDict(
    'PathToApi',
    {
        PathValues.RUN: Run,
        PathValues.TESTCASE: TestCase,
        PathValues.TESTRESULT: TestResult,
        PathValues.TESTRUN: TestRun,
        PathValues.PIPELINES: Pipelines,
    }
)

path_to_api = PathToApi(
    {
        PathValues.RUN: Run,
        PathValues.TESTCASE: TestCase,
        PathValues.TESTRESULT: TestResult,
        PathValues.TESTRUN: TestRun,
        PathValues.PIPELINES: Pipelines,
    }
)
