# coding: utf-8

"""
    Gentrace API

    These API routes are designed to ingest events from clients.  # noqa: E501

    The version of the OpenAPI document: 0.14.0
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


class FullRun(
    schemas.DictSchema
):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """


    class MetaOapg:
        required = {
            "organizationId",
            "pipelineRunId",
            "startTime",
            "endTime",
            "pipelineId",
        }
        
        class properties:
            pipelineRunId = schemas.UUIDSchema
            pipelineId = schemas.UUIDSchema
            organizationId = schemas.UUIDSchema
            startTime = schemas.StrSchema
            endTime = schemas.StrSchema
            
            
            class cost(
                schemas.NumberBase,
                schemas.NoneBase,
                schemas.Schema,
                schemas.NoneDecimalMixin
            ):
            
            
                class MetaOapg:
                    inclusive_minimum = 0
            
            
                def __new__(
                    cls,
                    *_args: typing.Union[None, decimal.Decimal, int, float, ],
                    _configuration: typing.Optional[schemas.Configuration] = None,
                ) -> 'cost':
                    return super().__new__(
                        cls,
                        *_args,
                        _configuration=_configuration,
                    )
            
            
            class elapsed(
                schemas.NumberBase,
                schemas.NoneBase,
                schemas.Schema,
                schemas.NoneDecimalMixin
            ):
            
            
                class MetaOapg:
                    inclusive_minimum = 0
            
            
                def __new__(
                    cls,
                    *_args: typing.Union[None, decimal.Decimal, int, float, ],
                    _configuration: typing.Optional[schemas.Configuration] = None,
                ) -> 'elapsed':
                    return super().__new__(
                        cls,
                        *_args,
                        _configuration=_configuration,
                    )
            
            
            class feedback(
                schemas.NumberBase,
                schemas.NoneBase,
                schemas.Schema,
                schemas.NoneDecimalMixin
            ):
            
            
                class MetaOapg:
                    inclusive_maximum = 1
                    inclusive_minimum = 0
            
            
                def __new__(
                    cls,
                    *_args: typing.Union[None, decimal.Decimal, int, float, ],
                    _configuration: typing.Optional[schemas.Configuration] = None,
                ) -> 'feedback':
                    return super().__new__(
                        cls,
                        *_args,
                        _configuration=_configuration,
                    )
            
            
            class lastInvocation(
                schemas.StrBase,
                schemas.NoneBase,
                schemas.Schema,
                schemas.NoneStrMixin
            ):
            
            
                def __new__(
                    cls,
                    *_args: typing.Union[None, str, ],
                    _configuration: typing.Optional[schemas.Configuration] = None,
                ) -> 'lastInvocation':
                    return super().__new__(
                        cls,
                        *_args,
                        _configuration=_configuration,
                    )
            
            
            class inputs(
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
                ) -> 'inputs':
                    return super().__new__(
                        cls,
                        *_args,
                        _configuration=_configuration,
                        **kwargs,
                    )
            
            
            class outputs(
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
                ) -> 'outputs':
                    return super().__new__(
                        cls,
                        *_args,
                        _configuration=_configuration,
                        **kwargs,
                    )
            
            
            class renderHTMLKey(
                schemas.StrBase,
                schemas.NoneBase,
                schemas.Schema,
                schemas.NoneStrMixin
            ):
            
            
                def __new__(
                    cls,
                    *_args: typing.Union[None, str, ],
                    _configuration: typing.Optional[schemas.Configuration] = None,
                ) -> 'renderHTMLKey':
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
                "pipelineRunId": pipelineRunId,
                "pipelineId": pipelineId,
                "organizationId": organizationId,
                "startTime": startTime,
                "endTime": endTime,
                "cost": cost,
                "elapsed": elapsed,
                "feedback": feedback,
                "lastInvocation": lastInvocation,
                "inputs": inputs,
                "outputs": outputs,
                "renderHTMLKey": renderHTMLKey,
                "metadata": metadata,
            }
    
    organizationId: MetaOapg.properties.organizationId
    pipelineRunId: MetaOapg.properties.pipelineRunId
    startTime: MetaOapg.properties.startTime
    endTime: MetaOapg.properties.endTime
    pipelineId: MetaOapg.properties.pipelineId
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["pipelineRunId"]) -> MetaOapg.properties.pipelineRunId: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["pipelineId"]) -> MetaOapg.properties.pipelineId: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["organizationId"]) -> MetaOapg.properties.organizationId: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["startTime"]) -> MetaOapg.properties.startTime: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["endTime"]) -> MetaOapg.properties.endTime: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["cost"]) -> MetaOapg.properties.cost: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["elapsed"]) -> MetaOapg.properties.elapsed: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["feedback"]) -> MetaOapg.properties.feedback: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["lastInvocation"]) -> MetaOapg.properties.lastInvocation: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["inputs"]) -> MetaOapg.properties.inputs: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["outputs"]) -> MetaOapg.properties.outputs: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["renderHTMLKey"]) -> MetaOapg.properties.renderHTMLKey: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["metadata"]) -> MetaOapg.properties.metadata: ...
    
    @typing.overload
    def __getitem__(self, name: str) -> schemas.UnsetAnyTypeSchema: ...
    
    def __getitem__(self, name: typing.Union[typing_extensions.Literal["pipelineRunId", "pipelineId", "organizationId", "startTime", "endTime", "cost", "elapsed", "feedback", "lastInvocation", "inputs", "outputs", "renderHTMLKey", "metadata", ], str]):
        # dict_instance[name] accessor
        return super().__getitem__(name)
    
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["pipelineRunId"]) -> MetaOapg.properties.pipelineRunId: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["pipelineId"]) -> MetaOapg.properties.pipelineId: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["organizationId"]) -> MetaOapg.properties.organizationId: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["startTime"]) -> MetaOapg.properties.startTime: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["endTime"]) -> MetaOapg.properties.endTime: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["cost"]) -> typing.Union[MetaOapg.properties.cost, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["elapsed"]) -> typing.Union[MetaOapg.properties.elapsed, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["feedback"]) -> typing.Union[MetaOapg.properties.feedback, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["lastInvocation"]) -> typing.Union[MetaOapg.properties.lastInvocation, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["inputs"]) -> typing.Union[MetaOapg.properties.inputs, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["outputs"]) -> typing.Union[MetaOapg.properties.outputs, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["renderHTMLKey"]) -> typing.Union[MetaOapg.properties.renderHTMLKey, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["metadata"]) -> typing.Union[MetaOapg.properties.metadata, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: str) -> typing.Union[schemas.UnsetAnyTypeSchema, schemas.Unset]: ...
    
    def get_item_oapg(self, name: typing.Union[typing_extensions.Literal["pipelineRunId", "pipelineId", "organizationId", "startTime", "endTime", "cost", "elapsed", "feedback", "lastInvocation", "inputs", "outputs", "renderHTMLKey", "metadata", ], str]):
        return super().get_item_oapg(name)
    

    def __new__(
        cls,
        *_args: typing.Union[dict, frozendict.frozendict, ],
        organizationId: typing.Union[MetaOapg.properties.organizationId, str, uuid.UUID, ],
        pipelineRunId: typing.Union[MetaOapg.properties.pipelineRunId, str, uuid.UUID, ],
        startTime: typing.Union[MetaOapg.properties.startTime, str, ],
        endTime: typing.Union[MetaOapg.properties.endTime, str, ],
        pipelineId: typing.Union[MetaOapg.properties.pipelineId, str, uuid.UUID, ],
        cost: typing.Union[MetaOapg.properties.cost, None, decimal.Decimal, int, float, schemas.Unset] = schemas.unset,
        elapsed: typing.Union[MetaOapg.properties.elapsed, None, decimal.Decimal, int, float, schemas.Unset] = schemas.unset,
        feedback: typing.Union[MetaOapg.properties.feedback, None, decimal.Decimal, int, float, schemas.Unset] = schemas.unset,
        lastInvocation: typing.Union[MetaOapg.properties.lastInvocation, None, str, schemas.Unset] = schemas.unset,
        inputs: typing.Union[MetaOapg.properties.inputs, dict, frozendict.frozendict, None, schemas.Unset] = schemas.unset,
        outputs: typing.Union[MetaOapg.properties.outputs, dict, frozendict.frozendict, None, schemas.Unset] = schemas.unset,
        renderHTMLKey: typing.Union[MetaOapg.properties.renderHTMLKey, None, str, schemas.Unset] = schemas.unset,
        metadata: typing.Union[MetaOapg.properties.metadata, dict, frozendict.frozendict, None, schemas.Unset] = schemas.unset,
        _configuration: typing.Optional[schemas.Configuration] = None,
        **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
    ) -> 'FullRun':
        return super().__new__(
            cls,
            *_args,
            organizationId=organizationId,
            pipelineRunId=pipelineRunId,
            startTime=startTime,
            endTime=endTime,
            pipelineId=pipelineId,
            cost=cost,
            elapsed=elapsed,
            feedback=feedback,
            lastInvocation=lastInvocation,
            inputs=inputs,
            outputs=outputs,
            renderHTMLKey=renderHTMLKey,
            metadata=metadata,
            _configuration=_configuration,
            **kwargs,
        )

from gentrace.model.metadata_value_object import MetadataValueObject
