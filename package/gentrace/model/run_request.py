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


class RunRequest(
    schemas.DictSchema
):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """


    class MetaOapg:
        required = {
            "stepRuns",
            "id",
        }
        
        class properties:
            id = schemas.UUIDSchema
            
            
            class stepRuns(
                schemas.ListSchema
            ):
            
            
                class MetaOapg:
                    
                    @staticmethod
                    def items() -> typing.Type['StepRun']:
                        return StepRun
            
                def __new__(
                    cls,
                    _arg: typing.Union[typing.Tuple['StepRun'], typing.List['StepRun']],
                    _configuration: typing.Optional[schemas.Configuration] = None,
                ) -> 'stepRuns':
                    return super().__new__(
                        cls,
                        _arg,
                        _configuration=_configuration,
                    )
            
                def __getitem__(self, i: int) -> 'StepRun':
                    return super().__getitem__(i)
            
            
            class collectionMethod(
                schemas.EnumBase,
                schemas.StrSchema
            ):
            
            
                class MetaOapg:
                    enum_value_to_name = {
                        "manual": "MANUAL",
                        "runner": "RUNNER",
                    }
                
                @schemas.classproperty
                def MANUAL(cls):
                    return cls("manual")
                
                @schemas.classproperty
                def RUNNER(cls):
                    return cls("runner")
            slug = schemas.StrSchema
            
            
            class previousRunId(
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
                ) -> 'previousRunId':
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
            __annotations__ = {
                "id": id,
                "stepRuns": stepRuns,
                "collectionMethod": collectionMethod,
                "slug": slug,
                "previousRunId": previousRunId,
                "metadata": metadata,
            }
    
    stepRuns: MetaOapg.properties.stepRuns
    id: MetaOapg.properties.id
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["id"]) -> MetaOapg.properties.id: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["stepRuns"]) -> MetaOapg.properties.stepRuns: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["collectionMethod"]) -> MetaOapg.properties.collectionMethod: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["slug"]) -> MetaOapg.properties.slug: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["previousRunId"]) -> MetaOapg.properties.previousRunId: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["metadata"]) -> MetaOapg.properties.metadata: ...
    
    @typing.overload
    def __getitem__(self, name: str) -> schemas.UnsetAnyTypeSchema: ...
    
    def __getitem__(self, name: typing.Union[typing_extensions.Literal["id", "stepRuns", "collectionMethod", "slug", "previousRunId", "metadata", ], str]):
        # dict_instance[name] accessor
        return super().__getitem__(name)
    
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["id"]) -> MetaOapg.properties.id: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["stepRuns"]) -> MetaOapg.properties.stepRuns: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["collectionMethod"]) -> typing.Union[MetaOapg.properties.collectionMethod, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["slug"]) -> typing.Union[MetaOapg.properties.slug, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["previousRunId"]) -> typing.Union[MetaOapg.properties.previousRunId, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["metadata"]) -> typing.Union[MetaOapg.properties.metadata, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: str) -> typing.Union[schemas.UnsetAnyTypeSchema, schemas.Unset]: ...
    
    def get_item_oapg(self, name: typing.Union[typing_extensions.Literal["id", "stepRuns", "collectionMethod", "slug", "previousRunId", "metadata", ], str]):
        return super().get_item_oapg(name)
    

    def __new__(
        cls,
        *_args: typing.Union[dict, frozendict.frozendict, ],
        stepRuns: typing.Union[MetaOapg.properties.stepRuns, list, tuple, ],
        id: typing.Union[MetaOapg.properties.id, str, uuid.UUID, ],
        collectionMethod: typing.Union[MetaOapg.properties.collectionMethod, str, schemas.Unset] = schemas.unset,
        slug: typing.Union[MetaOapg.properties.slug, str, schemas.Unset] = schemas.unset,
        previousRunId: typing.Union[MetaOapg.properties.previousRunId, None, str, uuid.UUID, schemas.Unset] = schemas.unset,
        metadata: typing.Union[MetaOapg.properties.metadata, dict, frozendict.frozendict, None, schemas.Unset] = schemas.unset,
        _configuration: typing.Optional[schemas.Configuration] = None,
        **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
    ) -> 'RunRequest':
        return super().__new__(
            cls,
            *_args,
            stepRuns=stepRuns,
            id=id,
            collectionMethod=collectionMethod,
            slug=slug,
            previousRunId=previousRunId,
            metadata=metadata,
            _configuration=_configuration,
            **kwargs,
        )

from gentrace.model.metadata_value_object import MetadataValueObject
from gentrace.model.step_run import StepRun
