# coding: utf-8

"""
    Gentrace API

    These API routes are designed to ingest events from clients.  # noqa: E501

    The version of the OpenAPI document: 0.13.0
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

class TestEvaluator(
    schemas.DictSchema
):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """


    class MetaOapg:
        required = {
            "createdAt",
            "valueType",
            "name",
            "options",
            "id",
            "pipelineId",
            "updatedAt",
            "who",
        }
        
        class properties:
            id = schemas.UUIDSchema
            createdAt = schemas.StrSchema
            updatedAt = schemas.StrSchema
            name = schemas.StrSchema
            
            
            class options(
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
                ) -> 'options':
                    return super().__new__(
                        cls,
                        *_args,
                        _configuration=_configuration,
                        **kwargs,
                    )
            pipelineId = schemas.StrSchema
            
            
            class who(
                schemas.EnumBase,
                schemas.StrSchema
            ):
                
                @schemas.classproperty
                def AI(cls):
                    return cls("AI")
                
                @schemas.classproperty
                def HEURISTIC(cls):
                    return cls("HEURISTIC")
                
                @schemas.classproperty
                def HUMAN(cls):
                    return cls("HUMAN")
            
            
            class valueType(
                schemas.EnumBase,
                schemas.StrSchema
            ):
                
                @schemas.classproperty
                def ENUM(cls):
                    return cls("ENUM")
                
                @schemas.classproperty
                def PERCENTAGE(cls):
                    return cls("PERCENTAGE")
            
            
            class archivedAt(
                schemas.StrBase,
                schemas.NoneBase,
                schemas.Schema,
                schemas.NoneStrMixin
            ):
            
            
                class MetaOapg:
                    format = 'datetime'
            
            
                def __new__(
                    cls,
                    *_args: typing.Union[None, str, ],
                    _configuration: typing.Optional[schemas.Configuration] = None,
                ) -> 'archivedAt':
                    return super().__new__(
                        cls,
                        *_args,
                        _configuration=_configuration,
                    )
            
            
            class icon(
                schemas.StrBase,
                schemas.NoneBase,
                schemas.Schema,
                schemas.NoneStrMixin
            ):
            
            
                def __new__(
                    cls,
                    *_args: typing.Union[None, str, ],
                    _configuration: typing.Optional[schemas.Configuration] = None,
                ) -> 'icon':
                    return super().__new__(
                        cls,
                        *_args,
                        _configuration=_configuration,
                    )
            
            
            class aiModel(
                schemas.EnumBase,
                schemas.StrBase,
                schemas.NoneBase,
                schemas.Schema,
                schemas.NoneStrMixin
            ):
            
            
                class MetaOapg:
                    enum_value_to_name = {
                        "OPENAI_3_5": "_5",
                        "OPENAI_4": "POSITIVE_4",
                    }
                
                @schemas.classproperty
                def _5(cls):
                    return cls("OPENAI_3_5")
                
                @schemas.classproperty
                def POSITIVE_4(cls):
                    return cls("OPENAI_4")
            
            
                def __new__(
                    cls,
                    *_args: typing.Union[None, str, ],
                    _configuration: typing.Optional[schemas.Configuration] = None,
                ) -> 'aiModel':
                    return super().__new__(
                        cls,
                        *_args,
                        _configuration=_configuration,
                    )
            
            
            class processorId(
                schemas.StrBase,
                schemas.NoneBase,
                schemas.Schema,
                schemas.NoneStrMixin
            ):
            
            
                def __new__(
                    cls,
                    *_args: typing.Union[None, str, ],
                    _configuration: typing.Optional[schemas.Configuration] = None,
                ) -> 'processorId':
                    return super().__new__(
                        cls,
                        *_args,
                        _configuration=_configuration,
                    )
            
            
            class heuristicFn(
                schemas.StrBase,
                schemas.NoneBase,
                schemas.Schema,
                schemas.NoneStrMixin
            ):
            
            
                def __new__(
                    cls,
                    *_args: typing.Union[None, str, ],
                    _configuration: typing.Optional[schemas.Configuration] = None,
                ) -> 'heuristicFn':
                    return super().__new__(
                        cls,
                        *_args,
                        _configuration=_configuration,
                    )
            
            
            class aiPromptFormat(
                schemas.StrBase,
                schemas.NoneBase,
                schemas.Schema,
                schemas.NoneStrMixin
            ):
            
            
                def __new__(
                    cls,
                    *_args: typing.Union[None, str, ],
                    _configuration: typing.Optional[schemas.Configuration] = None,
                ) -> 'aiPromptFormat':
                    return super().__new__(
                        cls,
                        *_args,
                        _configuration=_configuration,
                    )
            
            
            class humanPrompt(
                schemas.StrBase,
                schemas.NoneBase,
                schemas.Schema,
                schemas.NoneStrMixin
            ):
            
            
                def __new__(
                    cls,
                    *_args: typing.Union[None, str, ],
                    _configuration: typing.Optional[schemas.Configuration] = None,
                ) -> 'humanPrompt':
                    return super().__new__(
                        cls,
                        *_args,
                        _configuration=_configuration,
                    )
            __annotations__ = {
                "id": id,
                "createdAt": createdAt,
                "updatedAt": updatedAt,
                "name": name,
                "options": options,
                "pipelineId": pipelineId,
                "who": who,
                "valueType": valueType,
                "archivedAt": archivedAt,
                "icon": icon,
                "aiModel": aiModel,
                "processorId": processorId,
                "heuristicFn": heuristicFn,
                "aiPromptFormat": aiPromptFormat,
                "humanPrompt": humanPrompt,
            }
    
    createdAt: MetaOapg.properties.createdAt
    valueType: MetaOapg.properties.valueType
    name: MetaOapg.properties.name
    options: MetaOapg.properties.options
    id: MetaOapg.properties.id
    pipelineId: MetaOapg.properties.pipelineId
    updatedAt: MetaOapg.properties.updatedAt
    who: MetaOapg.properties.who
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["id"]) -> MetaOapg.properties.id: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["createdAt"]) -> MetaOapg.properties.createdAt: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["updatedAt"]) -> MetaOapg.properties.updatedAt: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["name"]) -> MetaOapg.properties.name: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["options"]) -> MetaOapg.properties.options: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["pipelineId"]) -> MetaOapg.properties.pipelineId: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["who"]) -> MetaOapg.properties.who: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["valueType"]) -> MetaOapg.properties.valueType: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["archivedAt"]) -> MetaOapg.properties.archivedAt: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["icon"]) -> MetaOapg.properties.icon: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["aiModel"]) -> MetaOapg.properties.aiModel: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["processorId"]) -> MetaOapg.properties.processorId: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["heuristicFn"]) -> MetaOapg.properties.heuristicFn: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["aiPromptFormat"]) -> MetaOapg.properties.aiPromptFormat: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["humanPrompt"]) -> MetaOapg.properties.humanPrompt: ...
    
    @typing.overload
    def __getitem__(self, name: str) -> schemas.UnsetAnyTypeSchema: ...
    
    def __getitem__(self, name: typing.Union[typing_extensions.Literal["id", "createdAt", "updatedAt", "name", "options", "pipelineId", "who", "valueType", "archivedAt", "icon", "aiModel", "processorId", "heuristicFn", "aiPromptFormat", "humanPrompt", ], str]):
        # dict_instance[name] accessor
        return super().__getitem__(name)
    
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["id"]) -> MetaOapg.properties.id: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["createdAt"]) -> MetaOapg.properties.createdAt: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["updatedAt"]) -> MetaOapg.properties.updatedAt: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["name"]) -> MetaOapg.properties.name: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["options"]) -> MetaOapg.properties.options: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["pipelineId"]) -> MetaOapg.properties.pipelineId: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["who"]) -> MetaOapg.properties.who: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["valueType"]) -> MetaOapg.properties.valueType: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["archivedAt"]) -> typing.Union[MetaOapg.properties.archivedAt, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["icon"]) -> typing.Union[MetaOapg.properties.icon, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["aiModel"]) -> typing.Union[MetaOapg.properties.aiModel, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["processorId"]) -> typing.Union[MetaOapg.properties.processorId, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["heuristicFn"]) -> typing.Union[MetaOapg.properties.heuristicFn, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["aiPromptFormat"]) -> typing.Union[MetaOapg.properties.aiPromptFormat, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["humanPrompt"]) -> typing.Union[MetaOapg.properties.humanPrompt, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: str) -> typing.Union[schemas.UnsetAnyTypeSchema, schemas.Unset]: ...
    
    def get_item_oapg(self, name: typing.Union[typing_extensions.Literal["id", "createdAt", "updatedAt", "name", "options", "pipelineId", "who", "valueType", "archivedAt", "icon", "aiModel", "processorId", "heuristicFn", "aiPromptFormat", "humanPrompt", ], str]):
        return super().get_item_oapg(name)
    

    def __new__(
        cls,
        *_args: typing.Union[dict, frozendict.frozendict, ],
        createdAt: typing.Union[MetaOapg.properties.createdAt, str, ],
        valueType: typing.Union[MetaOapg.properties.valueType, str, ],
        name: typing.Union[MetaOapg.properties.name, str, ],
        options: typing.Union[MetaOapg.properties.options, dict, frozendict.frozendict, None, ],
        id: typing.Union[MetaOapg.properties.id, str, uuid.UUID, ],
        pipelineId: typing.Union[MetaOapg.properties.pipelineId, str, ],
        updatedAt: typing.Union[MetaOapg.properties.updatedAt, str, ],
        who: typing.Union[MetaOapg.properties.who, str, ],
        archivedAt: typing.Union[MetaOapg.properties.archivedAt, None, str, schemas.Unset] = schemas.unset,
        icon: typing.Union[MetaOapg.properties.icon, None, str, schemas.Unset] = schemas.unset,
        aiModel: typing.Union[MetaOapg.properties.aiModel, None, str, schemas.Unset] = schemas.unset,
        processorId: typing.Union[MetaOapg.properties.processorId, None, str, schemas.Unset] = schemas.unset,
        heuristicFn: typing.Union[MetaOapg.properties.heuristicFn, None, str, schemas.Unset] = schemas.unset,
        aiPromptFormat: typing.Union[MetaOapg.properties.aiPromptFormat, None, str, schemas.Unset] = schemas.unset,
        humanPrompt: typing.Union[MetaOapg.properties.humanPrompt, None, str, schemas.Unset] = schemas.unset,
        _configuration: typing.Optional[schemas.Configuration] = None,
        **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
    ) -> 'TestEvaluator':
        return super().__new__(
            cls,
            *_args,
            createdAt=createdAt,
            valueType=valueType,
            name=name,
            options=options,
            id=id,
            pipelineId=pipelineId,
            updatedAt=updatedAt,
            who=who,
            archivedAt=archivedAt,
            icon=icon,
            aiModel=aiModel,
            processorId=processorId,
            heuristicFn=heuristicFn,
            aiPromptFormat=aiPromptFormat,
            humanPrompt=humanPrompt,
            _configuration=_configuration,
            **kwargs,
        )
