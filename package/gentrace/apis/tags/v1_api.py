# coding: utf-8

"""
    Gentrace API

    These API routes are designed to ingest events from clients.  # noqa: E501

    The version of the OpenAPI document: 0.23.0
    Generated by: https://openapi-generator.tech
"""

from gentrace.paths.v1_feedback.post import V1FeedbackPost
from gentrace.paths.v1_files_upload.post import V1FilesUploadPost
from gentrace.paths.v1_pipelines.get import V1PipelinesGet
from gentrace.paths.v1_run.post import V1RunPost
from gentrace.paths.v1_test_case.get import V1TestCaseGet
from gentrace.paths.v1_test_case.patch import V1TestCasePatch
from gentrace.paths.v1_test_case.post import V1TestCasePost
from gentrace.paths.v1_test_result.get import V1TestResultGet
from gentrace.paths.v1_test_result.post import V1TestResultPost
from gentrace.paths.v1_test_result_id.get import V1TestResultIdGet
from gentrace.paths.v1_test_result_simple.post import V1TestResultSimplePost
from gentrace.paths.v1_test_result_status.get import V1TestResultStatusGet


class V1Api(
    V1FeedbackPost,
    V1FilesUploadPost,
    V1PipelinesGet,
    V1RunPost,
    V1TestCaseGet,
    V1TestCasePatch,
    V1TestCasePost,
    V1TestResultGet,
    V1TestResultIdGet,
    V1TestResultPost,
    V1TestResultSimplePost,
    V1TestResultStatusGet,
):
    """NOTE: This class is auto generated by OpenAPI Generator
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """
    pass
