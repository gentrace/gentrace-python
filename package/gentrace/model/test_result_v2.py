# coding: utf-8

"""
    Gentrace API

    These API routes are designed to ingest events from clients.  # noqa: E501

    The version of the OpenAPI document: 0.23.0
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


class TestResultV2(
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
            "id",
            "pipelineId",
            "updatedAt",
        }
        
        class properties:
            id = schemas.UUIDSchema
            createdAt = schemas.Float32Schema
            updatedAt = schemas.Float32Schema
            
            
            class archivedAt(
                schemas.Float32Base,
                schemas.NumberBase,
                schemas.NoneBase,
                schemas.Schema,
                schemas.NoneDecimalMixin
            ):
            
            
                class MetaOapg:
                    format = 'float'
            
            
                def __new__(
                    cls,
                    *_args: typing.Union[None, decimal.Decimal, int, float, ],
                    _configuration: typing.Optional[schemas.Configuration] = None,
                ) -> 'archivedAt':
                    return super().__new__(
                        cls,
                        *_args,
                        _configuration=_configuration,
                    )
            pipelineId = schemas.UUIDSchema
            
            
            class branch(
                schemas.StrBase,
                schemas.NoneBase,
                schemas.Schema,
                schemas.NoneStrMixin
            ):
            
            
                def __new__(
                    cls,
                    *_args: typing.Union[None, str, ],
                    _configuration: typing.Optional[schemas.Configuration] = None,
                ) -> 'branch':
                    return super().__new__(
                        cls,
                        *_args,
                        _configuration=_configuration,
                    )
            
            
            class commit(
                schemas.StrBase,
                schemas.NoneBase,
                schemas.Schema,
                schemas.NoneStrMixin
            ):
            
            
                def __new__(
                    cls,
                    *_args: typing.Union[None, str, ],
                    _configuration: typing.Optional[schemas.Configuration] = None,
                ) -> 'commit':
                    return super().__new__(
                        cls,
                        *_args,
                        _configuration=_configuration,
                    )
            
            
            class metadata(
                schemas.DictBase,
                schemas.NoneBase,
                schemas.Schema,
                schemas.NoneFrozenDictMixin
            ):
            
            
                class MetaOapg:
                    
                    @staticmethod
                    def additional_properties() -> typing.Type['MetadataValueObject']:
                        return MetadataValueObject
            
                
                def __getitem__(self, name: typing.Union[str, ]) -> 'MetadataValueObject':
                    # dict_instance[name] accessor
                    return super().__getitem__(name)
                
                def get_item_oapg(self, name: typing.Union[str, ]) -> 'MetadataValueObject':
                    return super().get_item_oapg(name)
            
                def __new__(
                    cls,
                    *_args: typing.Union[dict, frozendict.frozendict, None, ],
                    _configuration: typing.Optional[schemas.Configuration] = None,
                    **kwargs: 'MetadataValueObject',
                ) -> 'metadata':
                    return super().__new__(
                        cls,
                        *_args,
                        _configuration=_configuration,
                        **kwargs,
                    )
            
            
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
            __annotations__ = {
                "id": id,
                "createdAt": createdAt,
                "updatedAt": updatedAt,
                "archivedAt": archivedAt,
                "pipelineId": pipelineId,
                "branch": branch,
                "commit": commit,
                "metadata": metadata,
                "name": name,
            }
    
    archivedAt: MetaOapg.properties.archivedAt
    createdAt: MetaOapg.properties.createdAt
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
    def __getitem__(self, name: typing_extensions.Literal["archivedAt"]) -> MetaOapg.properties.archivedAt: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["pipelineId"]) -> MetaOapg.properties.pipelineId: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["branch"]) -> MetaOapg.properties.branch: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["commit"]) -> MetaOapg.properties.commit: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["metadata"]) -> MetaOapg.properties.metadata: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["name"]) -> MetaOapg.properties.name: ...
    
    @typing.overload
    def __getitem__(self, name: str) -> schemas.UnsetAnyTypeSchema: ...
    
    def __getitem__(self, name: typing.Union[typing_extensions.Literal["id", "createdAt", "updatedAt", "archivedAt", "pipelineId", "branch", "commit", "metadata", "name", ], str]):
        # dict_instance[name] accessor
        return super().__getitem__(name)
    
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["id"]) -> MetaOapg.properties.id: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["createdAt"]) -> MetaOapg.properties.createdAt: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["updatedAt"]) -> MetaOapg.properties.updatedAt: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["archivedAt"]) -> MetaOapg.properties.archivedAt: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["pipelineId"]) -> MetaOapg.properties.pipelineId: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["branch"]) -> typing.Union[MetaOapg.properties.branch, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["commit"]) -> typing.Union[MetaOapg.properties.commit, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["metadata"]) -> typing.Union[MetaOapg.properties.metadata, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["name"]) -> typing.Union[MetaOapg.properties.name, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: str) -> typing.Union[schemas.UnsetAnyTypeSchema, schemas.Unset]: ...
    
    def get_item_oapg(self, name: typing.Union[typing_extensions.Literal["id", "createdAt", "updatedAt", "archivedAt", "pipelineId", "branch", "commit", "metadata", "name", ], str]):
        return super().get_item_oapg(name)
    

    def __new__(
        cls,
        *_args: typing.Union[dict, frozendict.frozendict, ],
        archivedAt: typing.Union[MetaOapg.properties.archivedAt, None, decimal.Decimal, int, float, ],
        createdAt: typing.Union[MetaOapg.properties.createdAt, decimal.Decimal, int, float, ],
        id: typing.Union[MetaOapg.properties.id, str, uuid.UUID, ],
        pipelineId: typing.Union[MetaOapg.properties.pipelineId, str, uuid.UUID, ],
        updatedAt: typing.Union[MetaOapg.properties.updatedAt, decimal.Decimal, int, float, ],
        branch: typing.Union[MetaOapg.properties.branch, None, str, schemas.Unset] = schemas.unset,
        commit: typing.Union[MetaOapg.properties.commit, None, str, schemas.Unset] = schemas.unset,
        metadata: typing.Union[MetaOapg.properties.metadata, dict, frozendict.frozendict, None, schemas.Unset] = schemas.unset,
        name: typing.Union[MetaOapg.properties.name, None, str, schemas.Unset] = schemas.unset,
        _configuration: typing.Optional[schemas.Configuration] = None,
        **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
    ) -> 'TestResultV2':
        return super().__new__(
            cls,
            *_args,
            archivedAt=archivedAt,
            createdAt=createdAt,
            id=id,
            pipelineId=pipelineId,
            updatedAt=updatedAt,
            branch=branch,
            commit=commit,
            metadata=metadata,
            name=name,
            _configuration=_configuration,
            **kwargs,
        )

from gentrace.model.metadata_value_object import MetadataValueObject
