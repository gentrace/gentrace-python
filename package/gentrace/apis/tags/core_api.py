# coding: utf-8

"""
    Gentrace API

    These API routes are designed to ingest events from clients.  # noqa: E501

    The version of the OpenAPI document: 0.8.0
    Generated by: https://openapi-generator.tech
"""

from gentrace.paths.pipeline_run.post import PipelineRunPost
from gentrace.paths.test_case.get import TestCaseGet
from gentrace.paths.test_run.get import TestRunGet
from gentrace.paths.test_run.post import TestRunPost


class CoreApi(
    PipelineRunPost,
    TestCaseGet,
    TestRunGet,
    TestRunPost,
):
    """NOTE: This class is auto generated by OpenAPI Generator
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    pass
