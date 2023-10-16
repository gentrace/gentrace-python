import typing_extensions

from gentrace.apis.paths.files_upload import FilesUpload
from gentrace.apis.paths.pipelines import Pipelines
from gentrace.apis.paths.run import Run
from gentrace.apis.paths.test_case import TestCase
from gentrace.apis.paths.test_result import TestResult
from gentrace.apis.paths.test_result_id import TestResultId
from gentrace.apis.paths.test_result_simple import TestResultSimple
from gentrace.apis.paths.test_result_status import TestResultStatus
from gentrace.paths import PathValues

PathToApi = typing_extensions.TypedDict(
    'PathToApi',
    {
        PathValues.RUN: Run,
        PathValues.TESTCASE: TestCase,
        PathValues.TESTRESULT: TestResult,
        PathValues.TESTRESULT_ID: TestResultId,
        PathValues.TESTRESULT_STATUS: TestResultStatus,
        PathValues.TESTRESULTSIMPLE: TestResultSimple,
        PathValues.PIPELINES: Pipelines,
        PathValues.FILES_UPLOAD: FilesUpload,
    }
)

path_to_api = PathToApi(
    {
        PathValues.RUN: Run,
        PathValues.TESTCASE: TestCase,
        PathValues.TESTRESULT: TestResult,
        PathValues.TESTRESULT_ID: TestResultId,
        PathValues.TESTRESULT_STATUS: TestResultStatus,
        PathValues.TESTRESULTSIMPLE: TestResultSimple,
        PathValues.PIPELINES: Pipelines,
        PathValues.FILES_UPLOAD: FilesUpload,
    }
)
