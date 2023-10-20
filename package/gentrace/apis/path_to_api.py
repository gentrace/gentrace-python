import typing_extensions

from gentrace.apis.paths.v1_files_upload import V1FilesUpload
from gentrace.apis.paths.v1_pipelines import V1Pipelines
from gentrace.apis.paths.v1_run import V1Run
from gentrace.apis.paths.v1_test_case import V1TestCase
from gentrace.apis.paths.v1_test_result import V1TestResult
from gentrace.apis.paths.v1_test_result_id import V1TestResultId
from gentrace.apis.paths.v1_test_result_simple import V1TestResultSimple
from gentrace.apis.paths.v1_test_result_status import V1TestResultStatus
from gentrace.apis.paths.v2_pipelines import V2Pipelines
from gentrace.apis.paths.v2_test_cases import V2TestCases
from gentrace.apis.paths.v2_test_results import V2TestResults
from gentrace.paths import PathValues

PathToApi = typing_extensions.TypedDict(
    'PathToApi',
    {
        PathValues.V1_RUN: V1Run,
        PathValues.V1_TESTCASE: V1TestCase,
        PathValues.V1_TESTRESULT: V1TestResult,
        PathValues.V1_TESTRESULT_ID: V1TestResultId,
        PathValues.V1_TESTRESULT_STATUS: V1TestResultStatus,
        PathValues.V1_TESTRESULTSIMPLE: V1TestResultSimple,
        PathValues.V1_PIPELINES: V1Pipelines,
        PathValues.V1_FILES_UPLOAD: V1FilesUpload,
        PathValues.V2_TESTRESULTS: V2TestResults,
        PathValues.V2_TESTCASES: V2TestCases,
        PathValues.V2_PIPELINES: V2Pipelines,
    }
)

path_to_api = PathToApi(
    {
        PathValues.V1_RUN: V1Run,
        PathValues.V1_TESTCASE: V1TestCase,
        PathValues.V1_TESTRESULT: V1TestResult,
        PathValues.V1_TESTRESULT_ID: V1TestResultId,
        PathValues.V1_TESTRESULT_STATUS: V1TestResultStatus,
        PathValues.V1_TESTRESULTSIMPLE: V1TestResultSimple,
        PathValues.V1_PIPELINES: V1Pipelines,
        PathValues.V1_FILES_UPLOAD: V1FilesUpload,
        PathValues.V2_TESTRESULTS: V2TestResults,
        PathValues.V2_TESTCASES: V2TestCases,
        PathValues.V2_PIPELINES: V2Pipelines,
    }
)
