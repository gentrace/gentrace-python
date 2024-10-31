# coding: utf-8

"""
    Gentrace API

    These API routes are designed to ingest events from clients.  # noqa: E501

    The version of the OpenAPI document: 0.27.0
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


class TestCaseV2(
    schemas.DictSchema
):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """


    class MetaOapg:
        required = {
            "archivedAt",
            "createdAt",
            "deletedAt",
            "inputs",
            "name",
            "datasetId",
            "id",
            "pipelineId",
            "updatedAt",
        }
        
        class properties:
            id = schemas.UUIDSchema
            createdAt = schemas.Float32Schema
            updatedAt = schemas.Float32Schema
        
            @staticmethod
            def archivedAt() -> typing.Type['UnixSecondsNullable']:
                return UnixSecondsNullable
        
            @staticmethod
            def deletedAt() -> typing.Type['UnixSecondsNullable']:
                return UnixSecondsNullable
            
            
            class inputs(
                schemas.DictSchema
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
                    *_args: typing.Union[dict, frozendict.frozendict, ],
                    _configuration: typing.Optional[schemas.Configuration] = None,
                    **kwargs: typing.Union[MetaOapg.additional_properties, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, bool, None, list, tuple, bytes, io.FileIO, io.BufferedReader, ],
                ) -> 'inputs':
                    return super().__new__(
                        cls,
                        *_args,
                        _configuration=_configuration,
                        **kwargs,
                    )
            name = schemas.StrSchema
            pipelineId = schemas.UUIDSchema
            datasetId = schemas.UUIDSchema
            
            
            class expectedOutputs(
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
                ) -> 'expectedOutputs':
                    return super().__new__(
                        cls,
                        *_args,
                        _configuration=_configuration,
                        **kwargs,
                    )
            __annotations__ = {
                "id": id,
                "createdAt": createdAt,
                "updatedAt": updatedAt,
                "archivedAt": archivedAt,
                "deletedAt": deletedAt,
                "inputs": inputs,
                "name": name,
                "pipelineId": pipelineId,
                "datasetId": datasetId,
                "expectedOutputs": expectedOutputs,
            }
    
    archivedAt: 'UnixSecondsNullable'
    createdAt: MetaOapg.properties.createdAt
    deletedAt: 'UnixSecondsNullable'
    inputs: MetaOapg.properties.inputs
    name: MetaOapg.properties.name
    datasetId: MetaOapg.properties.datasetId
    id: MetaOapg.properties.id
    pipelineId: MetaOapg.properties.pipelineId
    updatedAt: MetaOapg.properties.updatedAt
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["id"]) -> MetaOapg.properties.id: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["createdAt"]) -> MetaOapg.properties.createdAt: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["updatedAt"]) -> MetaOapg.properties.updatedAt: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["archivedAt"]) -> 'UnixSecondsNullable': ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["deletedAt"]) -> 'UnixSecondsNullable': ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["inputs"]) -> MetaOapg.properties.inputs: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["name"]) -> MetaOapg.properties.name: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["pipelineId"]) -> MetaOapg.properties.pipelineId: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["datasetId"]) -> MetaOapg.properties.datasetId: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["expectedOutputs"]) -> MetaOapg.properties.expectedOutputs: ...
    
    @typing.overload
    def __getitem__(self, name: str) -> schemas.UnsetAnyTypeSchema: ...
    
    def __getitem__(self, name: typing.Union[typing_extensions.Literal["id", "createdAt", "updatedAt", "archivedAt", "deletedAt", "inputs", "name", "pipelineId", "datasetId", "expectedOutputs", ], str]):
        # dict_instance[name] accessor
        return super().__getitem__(name)
    
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["id"]) -> MetaOapg.properties.id: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["createdAt"]) -> MetaOapg.properties.createdAt: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["updatedAt"]) -> MetaOapg.properties.updatedAt: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["archivedAt"]) -> 'UnixSecondsNullable': ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["deletedAt"]) -> 'UnixSecondsNullable': ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["inputs"]) -> MetaOapg.properties.inputs: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["name"]) -> MetaOapg.properties.name: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["pipelineId"]) -> MetaOapg.properties.pipelineId: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["datasetId"]) -> MetaOapg.properties.datasetId: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["expectedOutputs"]) -> typing.Union[MetaOapg.properties.expectedOutputs, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: str) -> typing.Union[schemas.UnsetAnyTypeSchema, schemas.Unset]: ...
    
    def get_item_oapg(self, name: typing.Union[typing_extensions.Literal["id", "createdAt", "updatedAt", "archivedAt", "deletedAt", "inputs", "name", "pipelineId", "datasetId", "expectedOutputs", ], str]):
        return super().get_item_oapg(name)
    

    def __new__(
        cls,
        *_args: typing.Union[dict, frozendict.frozendict, ],
        archivedAt: 'UnixSecondsNullable',
        createdAt: typing.Union[MetaOapg.properties.createdAt, decimal.Decimal, int, float, ],
        deletedAt: 'UnixSecondsNullable',
        inputs: typing.Union[MetaOapg.properties.inputs, dict, frozendict.frozendict, ],
        name: typing.Union[MetaOapg.properties.name, str, ],
        datasetId: typing.Union[MetaOapg.properties.datasetId, str, uuid.UUID, ],
        id: typing.Union[MetaOapg.properties.id, str, uuid.UUID, ],
        pipelineId: typing.Union[MetaOapg.properties.pipelineId, str, uuid.UUID, ],
        updatedAt: typing.Union[MetaOapg.properties.updatedAt, decimal.Decimal, int, float, ],
        expectedOutputs: typing.Union[MetaOapg.properties.expectedOutputs, dict, frozendict.frozendict, None, schemas.Unset] = schemas.unset,
        _configuration: typing.Optional[schemas.Configuration] = None,
        **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
    ) -> 'TestCaseV2':
        return super().__new__(
            cls,
            *_args,
            archivedAt=archivedAt,
            createdAt=createdAt,
            deletedAt=deletedAt,
            inputs=inputs,
            name=name,
            datasetId=datasetId,
            id=id,
            pipelineId=pipelineId,
            updatedAt=updatedAt,
            expectedOutputs=expectedOutputs,
            _configuration=_configuration,
            **kwargs,
        )

from gentrace.model.unix_seconds_nullable import UnixSecondsNullable
