# coding: utf-8

"""
    Gentrace API

    These API routes are designed to ingest events from clients.  # noqa: E501

    The version of the OpenAPI document: 0.27.0
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


class EvaluationV2(
    schemas.DictSchema
):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """


    class MetaOapg:
        required = {
            "createdAt",
            "note",
            "evalLabel",
            "name",
            "isFiltered",
            "id",
            "runId",
            "isPending",
            "evaluatorId",
            "evalValue",
            "updatedAt",
        }
        
        class properties:
            id = schemas.UUIDSchema
            createdAt = schemas.Float32Schema
            updatedAt = schemas.Float32Schema
            isPending = schemas.BoolSchema
            isFiltered = schemas.BoolSchema
            evaluatorId = schemas.UUIDSchema
            runId = schemas.UUIDSchema
            
            
            class name(
                schemas.StrBase,
                schemas.NoneBase,
                schemas.Schema,
                schemas.NoneStrMixin
            ):
            
            
                def __new__(
                    cls,
                    *_args: typing.Union[None, str, ],
                    _configuration: typing.Optional[schemas.Configuration] = None,
                ) -> 'name':
                    return super().__new__(
                        cls,
                        *_args,
                        _configuration=_configuration,
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
            note = schemas.StrSchema
            
            
            class debug(
                schemas.DictBase,
                schemas.NoneBase,
                schemas.Schema,
                schemas.NoneFrozenDictMixin
            ):
            
            
                class MetaOapg:
                    additional_properties = schemas.AnyTypeSchema
            
                
                def __getitem__(self, name: typing.Union[str, ]) -> MetaOapg.additional_properties:
                    # dict_instance[name] accessor
                    return super().__getitem__(name)
                
                def get_item_oapg(self, name: typing.Union[str, ]) -> MetaOapg.additional_properties:
                    return super().get_item_oapg(name)
            
                def __new__(
                    cls,
                    *_args: typing.Union[dict, frozendict.frozendict, None, ],
                    _configuration: typing.Optional[schemas.Configuration] = None,
                    **kwargs: typing.Union[MetaOapg.additional_properties, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, bool, None, list, tuple, bytes, io.FileIO, io.BufferedReader, ],
                ) -> 'debug':
                    return super().__new__(
                        cls,
                        *_args,
                        _configuration=_configuration,
                        **kwargs,
                    )
            
            
            class comparisonRunId(
                schemas.UUIDBase,
                schemas.StrBase,
                schemas.NoneBase,
                schemas.Schema,
                schemas.NoneStrMixin
            ):
            
            
                class MetaOapg:
                    format = 'uuid'
            
            
                def __new__(
                    cls,
                    *_args: typing.Union[None, str, uuid.UUID, ],
                    _configuration: typing.Optional[schemas.Configuration] = None,
                ) -> 'comparisonRunId':
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
                "isFiltered": isFiltered,
                "evaluatorId": evaluatorId,
                "runId": runId,
                "name": name,
                "evalLabel": evalLabel,
                "evalValue": evalValue,
                "note": note,
                "debug": debug,
                "comparisonRunId": comparisonRunId,
                "manualCreatedByEmail": manualCreatedByEmail,
            }
    
    createdAt: MetaOapg.properties.createdAt
    note: MetaOapg.properties.note
    evalLabel: MetaOapg.properties.evalLabel
    name: MetaOapg.properties.name
    isFiltered: MetaOapg.properties.isFiltered
    id: MetaOapg.properties.id
    runId: MetaOapg.properties.runId
    isPending: MetaOapg.properties.isPending
    evaluatorId: MetaOapg.properties.evaluatorId
    evalValue: MetaOapg.properties.evalValue
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
    def __getitem__(self, name: typing_extensions.Literal["isFiltered"]) -> MetaOapg.properties.isFiltered: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["evaluatorId"]) -> MetaOapg.properties.evaluatorId: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["runId"]) -> MetaOapg.properties.runId: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["name"]) -> MetaOapg.properties.name: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["evalLabel"]) -> MetaOapg.properties.evalLabel: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["evalValue"]) -> MetaOapg.properties.evalValue: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["note"]) -> MetaOapg.properties.note: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["debug"]) -> MetaOapg.properties.debug: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["comparisonRunId"]) -> MetaOapg.properties.comparisonRunId: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["manualCreatedByEmail"]) -> MetaOapg.properties.manualCreatedByEmail: ...
    
    @typing.overload
    def __getitem__(self, name: str) -> schemas.UnsetAnyTypeSchema: ...
    
    def __getitem__(self, name: typing.Union[typing_extensions.Literal["id", "createdAt", "updatedAt", "isPending", "isFiltered", "evaluatorId", "runId", "name", "evalLabel", "evalValue", "note", "debug", "comparisonRunId", "manualCreatedByEmail", ], str]):
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
    def get_item_oapg(self, name: typing_extensions.Literal["isFiltered"]) -> MetaOapg.properties.isFiltered: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["evaluatorId"]) -> MetaOapg.properties.evaluatorId: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["runId"]) -> MetaOapg.properties.runId: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["name"]) -> MetaOapg.properties.name: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["evalLabel"]) -> MetaOapg.properties.evalLabel: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["evalValue"]) -> MetaOapg.properties.evalValue: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["note"]) -> MetaOapg.properties.note: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["debug"]) -> typing.Union[MetaOapg.properties.debug, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["comparisonRunId"]) -> typing.Union[MetaOapg.properties.comparisonRunId, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["manualCreatedByEmail"]) -> typing.Union[MetaOapg.properties.manualCreatedByEmail, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: str) -> typing.Union[schemas.UnsetAnyTypeSchema, schemas.Unset]: ...
    
    def get_item_oapg(self, name: typing.Union[typing_extensions.Literal["id", "createdAt", "updatedAt", "isPending", "isFiltered", "evaluatorId", "runId", "name", "evalLabel", "evalValue", "note", "debug", "comparisonRunId", "manualCreatedByEmail", ], str]):
        return super().get_item_oapg(name)
    

    def __new__(
        cls,
        *_args: typing.Union[dict, frozendict.frozendict, ],
        createdAt: typing.Union[MetaOapg.properties.createdAt, decimal.Decimal, int, float, ],
        note: typing.Union[MetaOapg.properties.note, str, ],
        evalLabel: typing.Union[MetaOapg.properties.evalLabel, None, str, ],
        name: typing.Union[MetaOapg.properties.name, None, str, ],
        isFiltered: typing.Union[MetaOapg.properties.isFiltered, bool, ],
        id: typing.Union[MetaOapg.properties.id, str, uuid.UUID, ],
        runId: typing.Union[MetaOapg.properties.runId, str, uuid.UUID, ],
        isPending: typing.Union[MetaOapg.properties.isPending, bool, ],
        evaluatorId: typing.Union[MetaOapg.properties.evaluatorId, str, uuid.UUID, ],
        evalValue: typing.Union[MetaOapg.properties.evalValue, None, decimal.Decimal, int, float, ],
        updatedAt: typing.Union[MetaOapg.properties.updatedAt, decimal.Decimal, int, float, ],
        debug: typing.Union[MetaOapg.properties.debug, dict, frozendict.frozendict, None, schemas.Unset] = schemas.unset,
        comparisonRunId: typing.Union[MetaOapg.properties.comparisonRunId, None, str, uuid.UUID, schemas.Unset] = schemas.unset,
        manualCreatedByEmail: typing.Union[MetaOapg.properties.manualCreatedByEmail, None, str, schemas.Unset] = schemas.unset,
        _configuration: typing.Optional[schemas.Configuration] = None,
        **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
    ) -> 'EvaluationV2':
        return super().__new__(
            cls,
            *_args,
            createdAt=createdAt,
            note=note,
            evalLabel=evalLabel,
            name=name,
            isFiltered=isFiltered,
            id=id,
            runId=runId,
            isPending=isPending,
            evaluatorId=evaluatorId,
            evalValue=evalValue,
            updatedAt=updatedAt,
            debug=debug,
            comparisonRunId=comparisonRunId,
            manualCreatedByEmail=manualCreatedByEmail,
            _configuration=_configuration,
            **kwargs,
        )
