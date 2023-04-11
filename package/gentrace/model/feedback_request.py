# coding: utf-8

"""
    Gentrace API

    These API routes are designed to ingest events from clients.  # noqa: E501

    The version of the OpenAPI document: 0.2.2
    Generated by: https://openapi-generator.tech
"""

from datetime import date, datetime  # noqa: F401
import decimal  # noqa: F401
import functools  # noqa: F401
import io  # noqa: F401
import re  # noqa: F401
import typing  # noqa: F401
import typing_extensions  # noqa: F401
import uuid  # noqa: F401

import frozendict  # noqa: F401

from gentrace import schemas  # noqa: F401


class FeedbackRequest(
    schemas.DictSchema
):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """


    class MetaOapg:
        required = {
            "pipelineRunId",
            "rating",
            "recordedTime",
        }
        
        class properties:
            pipelineRunId = schemas.UUIDSchema
            
            
            class rating(
                schemas.EnumBase,
                schemas.StrSchema
            ):
            
            
                class MetaOapg:
                    enum_value_to_name = {
                        "positive": "POSITIVE",
                        "negative": "NEGATIVE",
                        "neutral": "NEUTRAL",
                    }
                
                @schemas.classproperty
                def POSITIVE(cls):
                    return cls("positive")
                
                @schemas.classproperty
                def NEGATIVE(cls):
                    return cls("negative")
                
                @schemas.classproperty
                def NEUTRAL(cls):
                    return cls("neutral")
            recordedTime = schemas.DateTimeSchema
            
            
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
                "rating": rating,
                "recordedTime": recordedTime,
                "details": details,
            }
        additional_properties = schemas.NotAnyTypeSchema
    
    pipelineRunId: MetaOapg.properties.pipelineRunId
    rating: MetaOapg.properties.rating
    recordedTime: MetaOapg.properties.recordedTime
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["pipelineRunId"]) -> MetaOapg.properties.pipelineRunId: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["rating"]) -> MetaOapg.properties.rating: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["recordedTime"]) -> MetaOapg.properties.recordedTime: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["details"]) -> MetaOapg.properties.details: ...
    
    def __getitem__(self, name: typing.Union[typing_extensions.Literal["pipelineRunId"], typing_extensions.Literal["rating"], typing_extensions.Literal["recordedTime"], typing_extensions.Literal["details"], ]):
        # dict_instance[name] accessor
        return super().__getitem__(name)
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["pipelineRunId"]) -> MetaOapg.properties.pipelineRunId: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["rating"]) -> MetaOapg.properties.rating: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["recordedTime"]) -> MetaOapg.properties.recordedTime: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["details"]) -> typing.Union[MetaOapg.properties.details, schemas.Unset]: ...
    
    def get_item_oapg(self, name: typing.Union[typing_extensions.Literal["pipelineRunId"], typing_extensions.Literal["rating"], typing_extensions.Literal["recordedTime"], typing_extensions.Literal["details"], ]):
        return super().get_item_oapg(name)

    def __new__(
        cls,
        *_args: typing.Union[dict, frozendict.frozendict, ],
        pipelineRunId: typing.Union[MetaOapg.properties.pipelineRunId, str, uuid.UUID, ],
        rating: typing.Union[MetaOapg.properties.rating, str, ],
        recordedTime: typing.Union[MetaOapg.properties.recordedTime, str, datetime, ],
        details: typing.Union[MetaOapg.properties.details, None, str, schemas.Unset] = schemas.unset,
        _configuration: typing.Optional[schemas.Configuration] = None,
    ) -> 'FeedbackRequest':
        return super().__new__(
            cls,
            *_args,
            pipelineRunId=pipelineRunId,
            rating=rating,
            recordedTime=recordedTime,
            details=details,
            _configuration=_configuration,
        )
