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


class EvaluatorV2(
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
            "id",
            "runCondition",
            "updatedAt",
            "who",
        }
        
        class properties:
            id = schemas.UUIDSchema
            createdAt = schemas.Float32Schema
            updatedAt = schemas.Float32Schema
            name = schemas.StrSchema
            who = schemas.StrSchema
            valueType = schemas.StrSchema
            runCondition = schemas.StrSchema
        
            @staticmethod
            def archivedAt() -> typing.Type['UnixSecondsNullable']:
                return UnixSecondsNullable
            
            
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
            
            
            class options(
                schemas.ListBase,
                schemas.NoneBase,
                schemas.Schema,
                schemas.NoneTupleMixin
            ):
            
            
                class MetaOapg:
                    items = schemas.AnyTypeSchema
            
            
                def __new__(
                    cls,
                    *_args: typing.Union[list, tuple, None, ],
                    _configuration: typing.Optional[schemas.Configuration] = None,
                ) -> 'options':
                    return super().__new__(
                        cls,
                        *_args,
                        _configuration=_configuration,
                    )
            aiModel = schemas.StrSchema
            
            
            class pipelineId(
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
                ) -> 'pipelineId':
                    return super().__new__(
                        cls,
                        *_args,
                        _configuration=_configuration,
                    )
            
            
            class processorId(
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
                ) -> 'processorId':
                    return super().__new__(
                        cls,
                        *_args,
                        _configuration=_configuration,
                    )
            organizationId = schemas.UUIDSchema
            templateDescription = schemas.StrSchema
            
            
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
            heuristicFnLanguage = schemas.StrSchema
            
            
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
            
            
            class aiImageUrls(
                schemas.ListSchema
            ):
            
            
                class MetaOapg:
                    items = schemas.StrSchema
            
                def __new__(
                    cls,
                    _arg: typing.Union[typing.Tuple[typing.Union[MetaOapg.items, str, ]], typing.List[typing.Union[MetaOapg.items, str, ]]],
                    _configuration: typing.Optional[schemas.Configuration] = None,
                ) -> 'aiImageUrls':
                    return super().__new__(
                        cls,
                        _arg,
                        _configuration=_configuration,
                    )
            
                def __getitem__(self, i: int) -> MetaOapg.items:
                    return super().__getitem__(i)
            
            
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
            
            
            class classifierValuePath(
                schemas.StrBase,
                schemas.NoneBase,
                schemas.Schema,
                schemas.NoneStrMixin
            ):
            
            
                def __new__(
                    cls,
                    *_args: typing.Union[None, str, ],
                    _configuration: typing.Optional[schemas.Configuration] = None,
                ) -> 'classifierValuePath':
                    return super().__new__(
                        cls,
                        *_args,
                        _configuration=_configuration,
                    )
            
            
            class classifierExpectedValuePath(
                schemas.StrBase,
                schemas.NoneBase,
                schemas.Schema,
                schemas.NoneStrMixin
            ):
            
            
                def __new__(
                    cls,
                    *_args: typing.Union[None, str, ],
                    _configuration: typing.Optional[schemas.Configuration] = None,
                ) -> 'classifierExpectedValuePath':
                    return super().__new__(
                        cls,
                        *_args,
                        _configuration=_configuration,
                    )
            
            
            class multiClassOptions(
                schemas.ListSchema
            ):
            
            
                class MetaOapg:
                    items = schemas.StrSchema
            
                def __new__(
                    cls,
                    _arg: typing.Union[typing.Tuple[typing.Union[MetaOapg.items, str, ]], typing.List[typing.Union[MetaOapg.items, str, ]]],
                    _configuration: typing.Optional[schemas.Configuration] = None,
                ) -> 'multiClassOptions':
                    return super().__new__(
                        cls,
                        _arg,
                        _configuration=_configuration,
                    )
            
                def __getitem__(self, i: int) -> MetaOapg.items:
                    return super().__getitem__(i)
            prodEvalActive = schemas.BoolSchema
            
            
            class samplingProbability(
                schemas.NumberBase,
                schemas.NoneBase,
                schemas.Schema,
                schemas.NoneDecimalMixin
            ):
            
            
                def __new__(
                    cls,
                    *_args: typing.Union[None, decimal.Decimal, int, float, ],
                    _configuration: typing.Optional[schemas.Configuration] = None,
                ) -> 'samplingProbability':
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
                "who": who,
                "valueType": valueType,
                "runCondition": runCondition,
                "archivedAt": archivedAt,
                "icon": icon,
                "options": options,
                "aiModel": aiModel,
                "pipelineId": pipelineId,
                "processorId": processorId,
                "organizationId": organizationId,
                "templateDescription": templateDescription,
                "heuristicFn": heuristicFn,
                "heuristicFnLanguage": heuristicFnLanguage,
                "aiPromptFormat": aiPromptFormat,
                "aiImageUrls": aiImageUrls,
                "humanPrompt": humanPrompt,
                "classifierValuePath": classifierValuePath,
                "classifierExpectedValuePath": classifierExpectedValuePath,
                "multiClassOptions": multiClassOptions,
                "prodEvalActive": prodEvalActive,
                "samplingProbability": samplingProbability,
            }
    
    createdAt: MetaOapg.properties.createdAt
    valueType: MetaOapg.properties.valueType
    name: MetaOapg.properties.name
    id: MetaOapg.properties.id
    runCondition: MetaOapg.properties.runCondition
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
    def __getitem__(self, name: typing_extensions.Literal["who"]) -> MetaOapg.properties.who: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["valueType"]) -> MetaOapg.properties.valueType: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["runCondition"]) -> MetaOapg.properties.runCondition: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["archivedAt"]) -> 'UnixSecondsNullable': ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["icon"]) -> MetaOapg.properties.icon: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["options"]) -> MetaOapg.properties.options: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["aiModel"]) -> MetaOapg.properties.aiModel: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["pipelineId"]) -> MetaOapg.properties.pipelineId: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["processorId"]) -> MetaOapg.properties.processorId: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["organizationId"]) -> MetaOapg.properties.organizationId: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["templateDescription"]) -> MetaOapg.properties.templateDescription: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["heuristicFn"]) -> MetaOapg.properties.heuristicFn: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["heuristicFnLanguage"]) -> MetaOapg.properties.heuristicFnLanguage: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["aiPromptFormat"]) -> MetaOapg.properties.aiPromptFormat: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["aiImageUrls"]) -> MetaOapg.properties.aiImageUrls: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["humanPrompt"]) -> MetaOapg.properties.humanPrompt: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["classifierValuePath"]) -> MetaOapg.properties.classifierValuePath: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["classifierExpectedValuePath"]) -> MetaOapg.properties.classifierExpectedValuePath: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["multiClassOptions"]) -> MetaOapg.properties.multiClassOptions: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["prodEvalActive"]) -> MetaOapg.properties.prodEvalActive: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["samplingProbability"]) -> MetaOapg.properties.samplingProbability: ...
    
    @typing.overload
    def __getitem__(self, name: str) -> schemas.UnsetAnyTypeSchema: ...
    
    def __getitem__(self, name: typing.Union[typing_extensions.Literal["id", "createdAt", "updatedAt", "name", "who", "valueType", "runCondition", "archivedAt", "icon", "options", "aiModel", "pipelineId", "processorId", "organizationId", "templateDescription", "heuristicFn", "heuristicFnLanguage", "aiPromptFormat", "aiImageUrls", "humanPrompt", "classifierValuePath", "classifierExpectedValuePath", "multiClassOptions", "prodEvalActive", "samplingProbability", ], str]):
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
    def get_item_oapg(self, name: typing_extensions.Literal["who"]) -> MetaOapg.properties.who: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["valueType"]) -> MetaOapg.properties.valueType: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["runCondition"]) -> MetaOapg.properties.runCondition: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["archivedAt"]) -> typing.Union['UnixSecondsNullable', schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["icon"]) -> typing.Union[MetaOapg.properties.icon, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["options"]) -> typing.Union[MetaOapg.properties.options, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["aiModel"]) -> typing.Union[MetaOapg.properties.aiModel, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["pipelineId"]) -> typing.Union[MetaOapg.properties.pipelineId, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["processorId"]) -> typing.Union[MetaOapg.properties.processorId, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["organizationId"]) -> typing.Union[MetaOapg.properties.organizationId, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["templateDescription"]) -> typing.Union[MetaOapg.properties.templateDescription, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["heuristicFn"]) -> typing.Union[MetaOapg.properties.heuristicFn, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["heuristicFnLanguage"]) -> typing.Union[MetaOapg.properties.heuristicFnLanguage, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["aiPromptFormat"]) -> typing.Union[MetaOapg.properties.aiPromptFormat, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["aiImageUrls"]) -> typing.Union[MetaOapg.properties.aiImageUrls, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["humanPrompt"]) -> typing.Union[MetaOapg.properties.humanPrompt, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["classifierValuePath"]) -> typing.Union[MetaOapg.properties.classifierValuePath, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["classifierExpectedValuePath"]) -> typing.Union[MetaOapg.properties.classifierExpectedValuePath, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["multiClassOptions"]) -> typing.Union[MetaOapg.properties.multiClassOptions, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["prodEvalActive"]) -> typing.Union[MetaOapg.properties.prodEvalActive, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["samplingProbability"]) -> typing.Union[MetaOapg.properties.samplingProbability, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: str) -> typing.Union[schemas.UnsetAnyTypeSchema, schemas.Unset]: ...
    
    def get_item_oapg(self, name: typing.Union[typing_extensions.Literal["id", "createdAt", "updatedAt", "name", "who", "valueType", "runCondition", "archivedAt", "icon", "options", "aiModel", "pipelineId", "processorId", "organizationId", "templateDescription", "heuristicFn", "heuristicFnLanguage", "aiPromptFormat", "aiImageUrls", "humanPrompt", "classifierValuePath", "classifierExpectedValuePath", "multiClassOptions", "prodEvalActive", "samplingProbability", ], str]):
        return super().get_item_oapg(name)
    

    def __new__(
        cls,
        *_args: typing.Union[dict, frozendict.frozendict, ],
        createdAt: typing.Union[MetaOapg.properties.createdAt, decimal.Decimal, int, float, ],
        valueType: typing.Union[MetaOapg.properties.valueType, str, ],
        name: typing.Union[MetaOapg.properties.name, str, ],
        id: typing.Union[MetaOapg.properties.id, str, uuid.UUID, ],
        runCondition: typing.Union[MetaOapg.properties.runCondition, str, ],
        updatedAt: typing.Union[MetaOapg.properties.updatedAt, decimal.Decimal, int, float, ],
        who: typing.Union[MetaOapg.properties.who, str, ],
        archivedAt: typing.Union['UnixSecondsNullable', schemas.Unset] = schemas.unset,
        icon: typing.Union[MetaOapg.properties.icon, None, str, schemas.Unset] = schemas.unset,
        options: typing.Union[MetaOapg.properties.options, list, tuple, None, schemas.Unset] = schemas.unset,
        aiModel: typing.Union[MetaOapg.properties.aiModel, str, schemas.Unset] = schemas.unset,
        pipelineId: typing.Union[MetaOapg.properties.pipelineId, None, str, uuid.UUID, schemas.Unset] = schemas.unset,
        processorId: typing.Union[MetaOapg.properties.processorId, None, str, uuid.UUID, schemas.Unset] = schemas.unset,
        organizationId: typing.Union[MetaOapg.properties.organizationId, str, uuid.UUID, schemas.Unset] = schemas.unset,
        templateDescription: typing.Union[MetaOapg.properties.templateDescription, str, schemas.Unset] = schemas.unset,
        heuristicFn: typing.Union[MetaOapg.properties.heuristicFn, None, str, schemas.Unset] = schemas.unset,
        heuristicFnLanguage: typing.Union[MetaOapg.properties.heuristicFnLanguage, str, schemas.Unset] = schemas.unset,
        aiPromptFormat: typing.Union[MetaOapg.properties.aiPromptFormat, None, str, schemas.Unset] = schemas.unset,
        aiImageUrls: typing.Union[MetaOapg.properties.aiImageUrls, list, tuple, schemas.Unset] = schemas.unset,
        humanPrompt: typing.Union[MetaOapg.properties.humanPrompt, None, str, schemas.Unset] = schemas.unset,
        classifierValuePath: typing.Union[MetaOapg.properties.classifierValuePath, None, str, schemas.Unset] = schemas.unset,
        classifierExpectedValuePath: typing.Union[MetaOapg.properties.classifierExpectedValuePath, None, str, schemas.Unset] = schemas.unset,
        multiClassOptions: typing.Union[MetaOapg.properties.multiClassOptions, list, tuple, schemas.Unset] = schemas.unset,
        prodEvalActive: typing.Union[MetaOapg.properties.prodEvalActive, bool, schemas.Unset] = schemas.unset,
        samplingProbability: typing.Union[MetaOapg.properties.samplingProbability, None, decimal.Decimal, int, float, schemas.Unset] = schemas.unset,
        _configuration: typing.Optional[schemas.Configuration] = None,
        **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
    ) -> 'EvaluatorV2':
        return super().__new__(
            cls,
            *_args,
            createdAt=createdAt,
            valueType=valueType,
            name=name,
            id=id,
            runCondition=runCondition,
            updatedAt=updatedAt,
            who=who,
            archivedAt=archivedAt,
            icon=icon,
            options=options,
            aiModel=aiModel,
            pipelineId=pipelineId,
            processorId=processorId,
            organizationId=organizationId,
            templateDescription=templateDescription,
            heuristicFn=heuristicFn,
            heuristicFnLanguage=heuristicFnLanguage,
            aiPromptFormat=aiPromptFormat,
            aiImageUrls=aiImageUrls,
            humanPrompt=humanPrompt,
            classifierValuePath=classifierValuePath,
            classifierExpectedValuePath=classifierExpectedValuePath,
            multiClassOptions=multiClassOptions,
            prodEvalActive=prodEvalActive,
            samplingProbability=samplingProbability,
            _configuration=_configuration,
            **kwargs,
        )

from gentrace.model.unix_seconds_nullable import UnixSecondsNullable
