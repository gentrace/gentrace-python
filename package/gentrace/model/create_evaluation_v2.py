# coding: utf-8

"""
    Gentrace API

    These API routes are designed to ingest events from clients.  # noqa: E501

    The version of the OpenAPI document: 0.24.2
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


class CreateEvaluationV2(
    schemas.DictSchema
):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """


    class MetaOapg:
        required = {
            "runId",
            "evaluatorId",
        }
        
        class properties:
            evaluatorId = schemas.UUIDSchema
            runId = schemas.UUIDSchema
            note = schemas.StrSchema
            evalLabel = schemas.StrSchema
            evalValue = schemas.NumberSchema
            __annotations__ = {
                "evaluatorId": evaluatorId,
                "runId": runId,
                "note": note,
                "evalLabel": evalLabel,
                "evalValue": evalValue,
            }
    
    runId: MetaOapg.properties.runId
    evaluatorId: MetaOapg.properties.evaluatorId
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["evaluatorId"]) -> MetaOapg.properties.evaluatorId: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["runId"]) -> MetaOapg.properties.runId: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["note"]) -> MetaOapg.properties.note: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["evalLabel"]) -> MetaOapg.properties.evalLabel: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["evalValue"]) -> MetaOapg.properties.evalValue: ...
    
    @typing.overload
    def __getitem__(self, name: str) -> schemas.UnsetAnyTypeSchema: ...
    
    def __getitem__(self, name: typing.Union[typing_extensions.Literal["evaluatorId", "runId", "note", "evalLabel", "evalValue", ], str]):
        # dict_instance[name] accessor
        return super().__getitem__(name)
    
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["evaluatorId"]) -> MetaOapg.properties.evaluatorId: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["runId"]) -> MetaOapg.properties.runId: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["note"]) -> typing.Union[MetaOapg.properties.note, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["evalLabel"]) -> typing.Union[MetaOapg.properties.evalLabel, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["evalValue"]) -> typing.Union[MetaOapg.properties.evalValue, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: str) -> typing.Union[schemas.UnsetAnyTypeSchema, schemas.Unset]: ...
    
    def get_item_oapg(self, name: typing.Union[typing_extensions.Literal["evaluatorId", "runId", "note", "evalLabel", "evalValue", ], str]):
        return super().get_item_oapg(name)
    

    def __new__(
        cls,
        *_args: typing.Union[dict, frozendict.frozendict, ],
        runId: typing.Union[MetaOapg.properties.runId, str, uuid.UUID, ],
        evaluatorId: typing.Union[MetaOapg.properties.evaluatorId, str, uuid.UUID, ],
        note: typing.Union[MetaOapg.properties.note, str, schemas.Unset] = schemas.unset,
        evalLabel: typing.Union[MetaOapg.properties.evalLabel, str, schemas.Unset] = schemas.unset,
        evalValue: typing.Union[MetaOapg.properties.evalValue, decimal.Decimal, int, float, schemas.Unset] = schemas.unset,
        _configuration: typing.Optional[schemas.Configuration] = None,
        **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
    ) -> 'CreateEvaluationV2':
        return super().__new__(
            cls,
            *_args,
            runId=runId,
            evaluatorId=evaluatorId,
            note=note,
            evalLabel=evalLabel,
            evalValue=evalValue,
            _configuration=_configuration,
            **kwargs,
        )
