import typing_extensions

from gentrace.paths import PathValues
from gentrace.apis.paths.v1_run import V1Run
from gentrace.apis.paths.v1_feedback import V1Feedback
from gentrace.apis.paths.v1_test_case import V1TestCase
from gentrace.apis.paths.v1_test_result import V1TestResult
from gentrace.apis.paths.v1_test_result_id import V1TestResultId
from gentrace.apis.paths.v1_test_result_status import V1TestResultStatus
from gentrace.apis.paths.v1_test_result_simple import V1TestResultSimple
from gentrace.apis.paths.v1_pipelines import V1Pipelines
from gentrace.apis.paths.v1_files_upload import V1FilesUpload
from gentrace.apis.paths.v2_feedback import V2Feedback
from gentrace.apis.paths.v2_feedback_id import V2FeedbackId
from gentrace.apis.paths.v2_runs_id import V2RunsId
from gentrace.apis.paths.v2_test_results import V2TestResults
from gentrace.apis.paths.v2_test_cases import V2TestCases
from gentrace.apis.paths.v2_test_cases_id import V2TestCasesId
from gentrace.apis.paths.v2_pipelines import V2Pipelines
from gentrace.apis.paths.v2_folders import V2Folders
from gentrace.apis.paths.v2_folders_id import V2FoldersId
from gentrace.apis.paths.v2_evaluators import V2Evaluators
from gentrace.apis.paths.v2_evaluations_bulk import V2EvaluationsBulk

PathToApi = typing_extensions.TypedDict(
    'PathToApi',
    {
        PathValues.V1_RUN: V1Run,
        PathValues.V1_FEEDBACK: V1Feedback,
        PathValues.V1_TESTCASE: V1TestCase,
        PathValues.V1_TESTRESULT: V1TestResult,
        PathValues.V1_TESTRESULT_ID: V1TestResultId,
        PathValues.V1_TESTRESULT_STATUS: V1TestResultStatus,
        PathValues.V1_TESTRESULTSIMPLE: V1TestResultSimple,
        PathValues.V1_PIPELINES: V1Pipelines,
        PathValues.V1_FILES_UPLOAD: V1FilesUpload,
        PathValues.V2_FEEDBACK: V2Feedback,
        PathValues.V2_FEEDBACK_ID: V2FeedbackId,
        PathValues.V2_RUNS_ID: V2RunsId,
        PathValues.V2_TESTRESULTS: V2TestResults,
        PathValues.V2_TESTCASES: V2TestCases,
        PathValues.V2_TESTCASES_ID: V2TestCasesId,
        PathValues.V2_PIPELINES: V2Pipelines,
        PathValues.V2_FOLDERS: V2Folders,
        PathValues.V2_FOLDERS_ID: V2FoldersId,
        PathValues.V2_EVALUATORS: V2Evaluators,
        PathValues.V2_EVALUATIONS_BULK: V2EvaluationsBulk,
    }
)

path_to_api = PathToApi(
    {
        PathValues.V1_RUN: V1Run,
        PathValues.V1_FEEDBACK: V1Feedback,
        PathValues.V1_TESTCASE: V1TestCase,
        PathValues.V1_TESTRESULT: V1TestResult,
        PathValues.V1_TESTRESULT_ID: V1TestResultId,
        PathValues.V1_TESTRESULT_STATUS: V1TestResultStatus,
        PathValues.V1_TESTRESULTSIMPLE: V1TestResultSimple,
        PathValues.V1_PIPELINES: V1Pipelines,
        PathValues.V1_FILES_UPLOAD: V1FilesUpload,
        PathValues.V2_FEEDBACK: V2Feedback,
        PathValues.V2_FEEDBACK_ID: V2FeedbackId,
        PathValues.V2_RUNS_ID: V2RunsId,
        PathValues.V2_TESTRESULTS: V2TestResults,
        PathValues.V2_TESTCASES: V2TestCases,
        PathValues.V2_TESTCASES_ID: V2TestCasesId,
        PathValues.V2_PIPELINES: V2Pipelines,
        PathValues.V2_FOLDERS: V2Folders,
        PathValues.V2_FOLDERS_ID: V2FoldersId,
        PathValues.V2_EVALUATORS: V2Evaluators,
        PathValues.V2_EVALUATIONS_BULK: V2EvaluationsBulk,
    }
)
