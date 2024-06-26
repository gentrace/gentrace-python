# coding: utf-8

"""
    Gentrace API

    These API routes are designed to ingest events from clients.  # noqa: E501

    The version of the OpenAPI document: 0.26.0
    Generated by: https://openapi-generator.tech
"""

import decimal  # noqa: F401
import functools  # noqa: F401
import io  # noqa: F401
import re  # noqa: F401
import typing  # noqa: F401
import uuid  # noqa: F401
from datetime import date, datetime  # noqa: F401

import frozendict  # noqa: F401
import typing_extensions  # noqa: F401

from gentrace import schemas  # noqa: F401


class CreateFeedbackV2(
    schemas.DictSchema
):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """


    class MetaOapg:
        required = {
            "score",
            "pipelineRunId",
            "recordedTime",
        }
        
        class properties:
            pipelineRunId = schemas.UUIDSchema
            recordedTime = schemas.Float32Schema
            
            
            class score(
                schemas.Float64Schema
            ):
            
            
                class MetaOapg:
                    format = 'double'
                    inclusive_maximum = 1
                    inclusive_minimum = 0
            
            
            class details(
                schemas.StrBase,
                schemas.NoneBase,
                schemas.Schema,
                schemas.NoneStrMixin
            ):
            
            
                def __new__(
                    cls,
                    *_args: typing.Union[None, str, ],
                    _configuration: typing.Optional[schemas.Configuration] = None,
                ) -> 'details':
                    return super().__new__(
                        cls,
                        *_args,
                        _configuration=_configuration,
                    )
            __annotations__ = {
                "pipelineRunId": pipelineRunId,
                "recordedTime": recordedTime,
                "score": score,
                "details": details,
            }
    
    score: MetaOapg.properties.score
    pipelineRunId: MetaOapg.properties.pipelineRunId
    recordedTime: MetaOapg.properties.recordedTime
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["pipelineRunId"]) -> MetaOapg.properties.pipelineRunId: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["recordedTime"]) -> MetaOapg.properties.recordedTime: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["score"]) -> MetaOapg.properties.score: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["details"]) -> MetaOapg.properties.details: ...
    
    @typing.overload
    def __getitem__(self, name: str) -> schemas.UnsetAnyTypeSchema: ...
    
    def __getitem__(self, name: typing.Union[typing_extensions.Literal["pipelineRunId", "recordedTime", "score", "details", ], str]):
        # dict_instance[name] accessor
        return super().__getitem__(name)
    
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["pipelineRunId"]) -> MetaOapg.properties.pipelineRunId: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["recordedTime"]) -> MetaOapg.properties.recordedTime: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["score"]) -> MetaOapg.properties.score: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["details"]) -> typing.Union[MetaOapg.properties.details, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: str) -> typing.Union[schemas.UnsetAnyTypeSchema, schemas.Unset]: ...
    
    def get_item_oapg(self, name: typing.Union[typing_extensions.Literal["pipelineRunId", "recordedTime", "score", "details", ], str]):
        return super().get_item_oapg(name)
    

    def __new__(
        cls,
        *_args: typing.Union[dict, frozendict.frozendict, ],
        score: typing.Union[MetaOapg.properties.score, decimal.Decimal, int, float, ],
        pipelineRunId: typing.Union[MetaOapg.properties.pipelineRunId, str, uuid.UUID, ],
        recordedTime: typing.Union[MetaOapg.properties.recordedTime, decimal.Decimal, int, float, ],
        details: typing.Union[MetaOapg.properties.details, None, str, schemas.Unset] = schemas.unset,
        _configuration: typing.Optional[schemas.Configuration] = None,
        **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
    ) -> 'CreateFeedbackV2':
        return super().__new__(
            cls,
            *_args,
            score=score,
            pipelineRunId=pipelineRunId,
            recordedTime=recordedTime,
            details=details,
            _configuration=_configuration,
            **kwargs,
        )
