# coding: utf-8

"""
    Gentrace API

    These API routes are designed to ingest events from clients.  # noqa: E501

    The version of the OpenAPI document: 0.11.4
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

class FeedbackResponse(
    schemas.DictSchema
):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """


    class MetaOapg:
        required = {
            "message",
        }
        
        class properties:
            message = schemas.StrSchema
            __annotations__ = {
                "message": message,
            }
        additional_properties = schemas.NotAnyTypeSchema
    
    message: MetaOapg.properties.message
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["message"]) -> MetaOapg.properties.message: ...
    
    def __getitem__(self, name: typing.Union[typing_extensions.Literal["message"], ]):
        # dict_instance[name] accessor
        return super().__getitem__(name)
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["message"]) -> MetaOapg.properties.message: ...
    
    def get_item_oapg(self, name: typing.Union[typing_extensions.Literal["message"], ]):
        return super().get_item_oapg(name)

    def __new__(
        cls,
        *_args: typing.Union[dict, frozendict.frozendict, ],
        message: typing.Union[MetaOapg.properties.message, str, ],
        _configuration: typing.Optional[schemas.Configuration] = None,
    ) -> 'FeedbackResponse':
        return super().__new__(
            cls,
            *_args,
            message=message,
            _configuration=_configuration,
        )
