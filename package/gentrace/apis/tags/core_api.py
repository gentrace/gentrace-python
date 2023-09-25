# coding: utf-8

"""
    Gentrace API

    These API routes are designed to ingest events from clients.  # noqa: E501

    The version of the OpenAPI document: 0.13.0
    Generated by: https://openapi-generator.tech
"""

from gentrace.paths.pipelines.get import PipelinesGet
from gentrace.paths.run.post import RunPost
from gentrace.paths.test_case.get import TestCaseGet
from gentrace.paths.test_case.patch import TestCasePatch
from gentrace.paths.test_case.post import TestCasePost
from gentrace.paths.test_result.get import TestResultGet
from gentrace.paths.test_result.post import TestResultPost
from gentrace.paths.test_result_id.get import TestResultIdGet
from gentrace.paths.test_result_simple.post import TestResultSimplePost
from gentrace.paths.test_result_status.get import TestResultStatusGet


class CoreApi(
    PipelinesGet,
    RunPost,
    TestCaseGet,
    TestCasePatch,
    TestCasePost,
    TestResultGet,
    TestResultIdGet,
    TestResultPost,
    TestResultSimplePost,
    TestResultStatusGet,
):
    """NOTE: This class is auto generated by OpenAPI Generator
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """
    pass
