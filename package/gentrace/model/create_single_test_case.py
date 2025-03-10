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


class CreateSingleTestCase(
    schemas.DictSchema
):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """


    class MetaOapg:
        required = {
            "inputs",
            "name",
        }
        
        class properties:
            name = schemas.StrSchema
            
            
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
            
            
            class pipelineSlug(
                schemas.StrSchema
            ):
            
            
                class MetaOapg:
                    min_length = 1
            
            
            class datasetId(
                schemas.StrSchema
            ):
            
            
                class MetaOapg:
                    min_length = 1
            
            
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
                "name": name,
                "inputs": inputs,
                "pipelineSlug": pipelineSlug,
                "datasetId": datasetId,
                "expectedOutputs": expectedOutputs,
            }
    
    inputs: MetaOapg.properties.inputs
    name: MetaOapg.properties.name
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["name"]) -> MetaOapg.properties.name: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["inputs"]) -> MetaOapg.properties.inputs: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["pipelineSlug"]) -> MetaOapg.properties.pipelineSlug: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["datasetId"]) -> MetaOapg.properties.datasetId: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["expectedOutputs"]) -> MetaOapg.properties.expectedOutputs: ...
    
    @typing.overload
    def __getitem__(self, name: str) -> schemas.UnsetAnyTypeSchema: ...
    
    def __getitem__(self, name: typing.Union[typing_extensions.Literal["name", "inputs", "pipelineSlug", "datasetId", "expectedOutputs", ], str]):
        # dict_instance[name] accessor
        return super().__getitem__(name)
    
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["name"]) -> MetaOapg.properties.name: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["inputs"]) -> MetaOapg.properties.inputs: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["pipelineSlug"]) -> typing.Union[MetaOapg.properties.pipelineSlug, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["datasetId"]) -> typing.Union[MetaOapg.properties.datasetId, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["expectedOutputs"]) -> typing.Union[MetaOapg.properties.expectedOutputs, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: str) -> typing.Union[schemas.UnsetAnyTypeSchema, schemas.Unset]: ...
    
    def get_item_oapg(self, name: typing.Union[typing_extensions.Literal["name", "inputs", "pipelineSlug", "datasetId", "expectedOutputs", ], str]):
        return super().get_item_oapg(name)
    

    def __new__(
        cls,
        *_args: typing.Union[dict, frozendict.frozendict, ],
        inputs: typing.Union[MetaOapg.properties.inputs, dict, frozendict.frozendict, ],
        name: typing.Union[MetaOapg.properties.name, str, ],
        pipelineSlug: typing.Union[MetaOapg.properties.pipelineSlug, str, schemas.Unset] = schemas.unset,
        datasetId: typing.Union[MetaOapg.properties.datasetId, str, schemas.Unset] = schemas.unset,
        expectedOutputs: typing.Union[MetaOapg.properties.expectedOutputs, dict, frozendict.frozendict, None, schemas.Unset] = schemas.unset,
        _configuration: typing.Optional[schemas.Configuration] = None,
        **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
    ) -> 'CreateSingleTestCase':
        return super().__new__(
            cls,
            *_args,
            inputs=inputs,
            name=name,
            pipelineSlug=pipelineSlug,
            datasetId=datasetId,
            expectedOutputs=expectedOutputs,
            _configuration=_configuration,
            **kwargs,
        )
