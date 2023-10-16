# coding: utf-8

"""
    Gentrace API

    These API routes are designed to ingest events from clients.  # noqa: E501

    The version of the OpenAPI document: 0.17.0
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

class TestEvaluation(
    schemas.DictSchema
):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """


    class MetaOapg:
        required = {
            "billingGpt4OutputTokens",
            "createdAt",
            "billingGpt4InputTokens",
            "billingGpt35InputTokens",
            "billingGpt35OutputTokens",
            "id",
            "runId",
            "isPending",
            "evaluatorId",
            "updatedAt",
        }
        
        class properties:
            id = schemas.UUIDSchema
            createdAt = schemas.StrSchema
            updatedAt = schemas.StrSchema
            isPending = schemas.BoolSchema
            evaluatorId = schemas.UUIDSchema
            runId = schemas.UUIDSchema
            billingGpt4InputTokens = schemas.IntSchema
            billingGpt4OutputTokens = schemas.IntSchema
            billingGpt35InputTokens = schemas.IntSchema
            billingGpt35OutputTokens = schemas.IntSchema
            
            
            class debug(
                schemas.DictBase,
                schemas.NoneBase,
                schemas.Schema,
                schemas.NoneFrozenDictMixin
            ):
            
            
                def __new__(
                    cls,
                    *_args: typing.Union[dict, frozendict.frozendict, None, ],
                    _configuration: typing.Optional[schemas.Configuration] = None,
                    **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
                ) -> 'debug':
                    return super().__new__(
                        cls,
                        *_args,
                        _configuration=_configuration,
                        **kwargs,
                    )
            
            
            class evalLabel(
                schemas.StrBase,
                schemas.NoneBase,
                schemas.Schema,
                schemas.NoneStrMixin
            ):
            
            
                def __new__(
                    cls,
                    *_args: typing.Union[None, str, ],
                    _configuration: typing.Optional[schemas.Configuration] = None,
                ) -> 'evalLabel':
                    return super().__new__(
                        cls,
                        *_args,
                        _configuration=_configuration,
                    )
            
            
            class evalValue(
                schemas.NumberBase,
                schemas.NoneBase,
                schemas.Schema,
                schemas.NoneDecimalMixin
            ):
            
            
                def __new__(
                    cls,
                    *_args: typing.Union[None, decimal.Decimal, int, float, ],
                    _configuration: typing.Optional[schemas.Configuration] = None,
                ) -> 'evalValue':
                    return super().__new__(
                        cls,
                        *_args,
                        _configuration=_configuration,
                    )
            
            
            class manualCreatedByEmail(
                schemas.StrBase,
                schemas.NoneBase,
                schemas.Schema,
                schemas.NoneStrMixin
            ):
            
            
                def __new__(
                    cls,
                    *_args: typing.Union[None, str, ],
                    _configuration: typing.Optional[schemas.Configuration] = None,
                ) -> 'manualCreatedByEmail':
                    return super().__new__(
                        cls,
                        *_args,
                        _configuration=_configuration,
                    )
            __annotations__ = {
                "id": id,
                "createdAt": createdAt,
                "updatedAt": updatedAt,
                "isPending": isPending,
                "evaluatorId": evaluatorId,
                "runId": runId,
                "billingGpt4InputTokens": billingGpt4InputTokens,
                "billingGpt4OutputTokens": billingGpt4OutputTokens,
                "billingGpt35InputTokens": billingGpt35InputTokens,
                "billingGpt35OutputTokens": billingGpt35OutputTokens,
                "debug": debug,
                "evalLabel": evalLabel,
                "evalValue": evalValue,
                "manualCreatedByEmail": manualCreatedByEmail,
            }
    
    billingGpt4OutputTokens: MetaOapg.properties.billingGpt4OutputTokens
    createdAt: MetaOapg.properties.createdAt
    billingGpt4InputTokens: MetaOapg.properties.billingGpt4InputTokens
    billingGpt35InputTokens: MetaOapg.properties.billingGpt35InputTokens
    billingGpt35OutputTokens: MetaOapg.properties.billingGpt35OutputTokens
    id: MetaOapg.properties.id
    runId: MetaOapg.properties.runId
    isPending: MetaOapg.properties.isPending
    evaluatorId: MetaOapg.properties.evaluatorId
    updatedAt: MetaOapg.properties.updatedAt
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["id"]) -> MetaOapg.properties.id: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["createdAt"]) -> MetaOapg.properties.createdAt: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["updatedAt"]) -> MetaOapg.properties.updatedAt: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["isPending"]) -> MetaOapg.properties.isPending: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["evaluatorId"]) -> MetaOapg.properties.evaluatorId: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["runId"]) -> MetaOapg.properties.runId: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["billingGpt4InputTokens"]) -> MetaOapg.properties.billingGpt4InputTokens: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["billingGpt4OutputTokens"]) -> MetaOapg.properties.billingGpt4OutputTokens: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["billingGpt35InputTokens"]) -> MetaOapg.properties.billingGpt35InputTokens: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["billingGpt35OutputTokens"]) -> MetaOapg.properties.billingGpt35OutputTokens: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["debug"]) -> MetaOapg.properties.debug: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["evalLabel"]) -> MetaOapg.properties.evalLabel: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["evalValue"]) -> MetaOapg.properties.evalValue: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["manualCreatedByEmail"]) -> MetaOapg.properties.manualCreatedByEmail: ...
    
    @typing.overload
    def __getitem__(self, name: str) -> schemas.UnsetAnyTypeSchema: ...
    
    def __getitem__(self, name: typing.Union[typing_extensions.Literal["id", "createdAt", "updatedAt", "isPending", "evaluatorId", "runId", "billingGpt4InputTokens", "billingGpt4OutputTokens", "billingGpt35InputTokens", "billingGpt35OutputTokens", "debug", "evalLabel", "evalValue", "manualCreatedByEmail", ], str]):
        # dict_instance[name] accessor
        return super().__getitem__(name)
    
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["id"]) -> MetaOapg.properties.id: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["createdAt"]) -> MetaOapg.properties.createdAt: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["updatedAt"]) -> MetaOapg.properties.updatedAt: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["isPending"]) -> MetaOapg.properties.isPending: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["evaluatorId"]) -> MetaOapg.properties.evaluatorId: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["runId"]) -> MetaOapg.properties.runId: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["billingGpt4InputTokens"]) -> MetaOapg.properties.billingGpt4InputTokens: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["billingGpt4OutputTokens"]) -> MetaOapg.properties.billingGpt4OutputTokens: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["billingGpt35InputTokens"]) -> MetaOapg.properties.billingGpt35InputTokens: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["billingGpt35OutputTokens"]) -> MetaOapg.properties.billingGpt35OutputTokens: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["debug"]) -> typing.Union[MetaOapg.properties.debug, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["evalLabel"]) -> typing.Union[MetaOapg.properties.evalLabel, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["evalValue"]) -> typing.Union[MetaOapg.properties.evalValue, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["manualCreatedByEmail"]) -> typing.Union[MetaOapg.properties.manualCreatedByEmail, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: str) -> typing.Union[schemas.UnsetAnyTypeSchema, schemas.Unset]: ...
    
    def get_item_oapg(self, name: typing.Union[typing_extensions.Literal["id", "createdAt", "updatedAt", "isPending", "evaluatorId", "runId", "billingGpt4InputTokens", "billingGpt4OutputTokens", "billingGpt35InputTokens", "billingGpt35OutputTokens", "debug", "evalLabel", "evalValue", "manualCreatedByEmail", ], str]):
        return super().get_item_oapg(name)
    

    def __new__(
        cls,
        *_args: typing.Union[dict, frozendict.frozendict, ],
        billingGpt4OutputTokens: typing.Union[MetaOapg.properties.billingGpt4OutputTokens, decimal.Decimal, int, ],
        createdAt: typing.Union[MetaOapg.properties.createdAt, str, ],
        billingGpt4InputTokens: typing.Union[MetaOapg.properties.billingGpt4InputTokens, decimal.Decimal, int, ],
        billingGpt35InputTokens: typing.Union[MetaOapg.properties.billingGpt35InputTokens, decimal.Decimal, int, ],
        billingGpt35OutputTokens: typing.Union[MetaOapg.properties.billingGpt35OutputTokens, decimal.Decimal, int, ],
        id: typing.Union[MetaOapg.properties.id, str, uuid.UUID, ],
        runId: typing.Union[MetaOapg.properties.runId, str, uuid.UUID, ],
        isPending: typing.Union[MetaOapg.properties.isPending, bool, ],
        evaluatorId: typing.Union[MetaOapg.properties.evaluatorId, str, uuid.UUID, ],
        updatedAt: typing.Union[MetaOapg.properties.updatedAt, str, ],
        debug: typing.Union[MetaOapg.properties.debug, dict, frozendict.frozendict, None, schemas.Unset] = schemas.unset,
        evalLabel: typing.Union[MetaOapg.properties.evalLabel, None, str, schemas.Unset] = schemas.unset,
        evalValue: typing.Union[MetaOapg.properties.evalValue, None, decimal.Decimal, int, float, schemas.Unset] = schemas.unset,
        manualCreatedByEmail: typing.Union[MetaOapg.properties.manualCreatedByEmail, None, str, schemas.Unset] = schemas.unset,
        _configuration: typing.Optional[schemas.Configuration] = None,
        **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
    ) -> 'TestEvaluation':
        return super().__new__(
            cls,
            *_args,
            billingGpt4OutputTokens=billingGpt4OutputTokens,
            createdAt=createdAt,
            billingGpt4InputTokens=billingGpt4InputTokens,
            billingGpt35InputTokens=billingGpt35InputTokens,
            billingGpt35OutputTokens=billingGpt35OutputTokens,
            id=id,
            runId=runId,
            isPending=isPending,
            evaluatorId=evaluatorId,
            updatedAt=updatedAt,
            debug=debug,
            evalLabel=evalLabel,
            evalValue=evalValue,
            manualCreatedByEmail=manualCreatedByEmail,
            _configuration=_configuration,
            **kwargs,
        )
