# coding: utf-8

"""
    Gentrace API

    These API routes are designed to ingest events from clients.  # noqa: E501

    The version of the OpenAPI document: 0.15.1
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


class CreateMultipleTestCases(
    schemas.DictSchema
):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """


    class MetaOapg:
        
        class properties:
            pipelineSlug = schemas.StrSchema
            
            
            class testCases(
                schemas.ListSchema
            ):
            
            
                class MetaOapg:
                    
                    
                    class items(
                        schemas.DictSchema
                    ):
                    
                    
                        class MetaOapg:
                            required = {
                                "expectedOutputs",
                                "inputs",
                                "name",
                            }
                            
                            class properties:
                                
                                
                                class name(
                                    schemas.StrSchema
                                ):
                                
                                
                                    class MetaOapg:
                                        min_length = 1
                                
                                
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
                                expectedOutputs = schemas.DictSchema
                                __annotations__ = {
                                    "name": name,
                                    "inputs": inputs,
                                    "expectedOutputs": expectedOutputs,
                                }
                        
                        expectedOutputs: MetaOapg.properties.expectedOutputs
                        inputs: MetaOapg.properties.inputs
                        name: MetaOapg.properties.name
                        
                        @typing.overload
                        def __getitem__(self, name: typing_extensions.Literal["name"]) -> MetaOapg.properties.name: ...
                        
                        @typing.overload
                        def __getitem__(self, name: typing_extensions.Literal["inputs"]) -> MetaOapg.properties.inputs: ...
                        
                        @typing.overload
                        def __getitem__(self, name: typing_extensions.Literal["expectedOutputs"]) -> MetaOapg.properties.expectedOutputs: ...
                        
                        @typing.overload
                        def __getitem__(self, name: str) -> schemas.UnsetAnyTypeSchema: ...
                        
                        def __getitem__(self, name: typing.Union[typing_extensions.Literal["name", "inputs", "expectedOutputs", ], str]):
                            # dict_instance[name] accessor
                            return super().__getitem__(name)
                        
                        
                        @typing.overload
                        def get_item_oapg(self, name: typing_extensions.Literal["name"]) -> MetaOapg.properties.name: ...
                        
                        @typing.overload
                        def get_item_oapg(self, name: typing_extensions.Literal["inputs"]) -> MetaOapg.properties.inputs: ...
                        
                        @typing.overload
                        def get_item_oapg(self, name: typing_extensions.Literal["expectedOutputs"]) -> MetaOapg.properties.expectedOutputs: ...
                        
                        @typing.overload
                        def get_item_oapg(self, name: str) -> typing.Union[schemas.UnsetAnyTypeSchema, schemas.Unset]: ...
                        
                        def get_item_oapg(self, name: typing.Union[typing_extensions.Literal["name", "inputs", "expectedOutputs", ], str]):
                            return super().get_item_oapg(name)
                        
                    
                        def __new__(
                            cls,
                            *_args: typing.Union[dict, frozendict.frozendict, ],
                            expectedOutputs: typing.Union[MetaOapg.properties.expectedOutputs, dict, frozendict.frozendict, ],
                            inputs: typing.Union[MetaOapg.properties.inputs, dict, frozendict.frozendict, ],
                            name: typing.Union[MetaOapg.properties.name, str, ],
                            _configuration: typing.Optional[schemas.Configuration] = None,
                            **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
                        ) -> 'items':
                            return super().__new__(
                                cls,
                                *_args,
                                expectedOutputs=expectedOutputs,
                                inputs=inputs,
                                name=name,
                                _configuration=_configuration,
                                **kwargs,
                            )
            
                def __new__(
                    cls,
                    _arg: typing.Union[typing.Tuple[typing.Union[MetaOapg.items, dict, frozendict.frozendict, ]], typing.List[typing.Union[MetaOapg.items, dict, frozendict.frozendict, ]]],
                    _configuration: typing.Optional[schemas.Configuration] = None,
                ) -> 'testCases':
                    return super().__new__(
                        cls,
                        _arg,
                        _configuration=_configuration,
                    )
            
                def __getitem__(self, i: int) -> MetaOapg.items:
                    return super().__getitem__(i)
            __annotations__ = {
                "pipelineSlug": pipelineSlug,
                "testCases": testCases,
            }
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["pipelineSlug"]) -> MetaOapg.properties.pipelineSlug: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["testCases"]) -> MetaOapg.properties.testCases: ...
    
    @typing.overload
    def __getitem__(self, name: str) -> schemas.UnsetAnyTypeSchema: ...
    
    def __getitem__(self, name: typing.Union[typing_extensions.Literal["pipelineSlug", "testCases", ], str]):
        # dict_instance[name] accessor
        return super().__getitem__(name)
    
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["pipelineSlug"]) -> typing.Union[MetaOapg.properties.pipelineSlug, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["testCases"]) -> typing.Union[MetaOapg.properties.testCases, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: str) -> typing.Union[schemas.UnsetAnyTypeSchema, schemas.Unset]: ...
    
    def get_item_oapg(self, name: typing.Union[typing_extensions.Literal["pipelineSlug", "testCases", ], str]):
        return super().get_item_oapg(name)
    

    def __new__(
        cls,
        *_args: typing.Union[dict, frozendict.frozendict, ],
        pipelineSlug: typing.Union[MetaOapg.properties.pipelineSlug, str, schemas.Unset] = schemas.unset,
        testCases: typing.Union[MetaOapg.properties.testCases, list, tuple, schemas.Unset] = schemas.unset,
        _configuration: typing.Optional[schemas.Configuration] = None,
        **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
    ) -> 'CreateMultipleTestCases':
        return super().__new__(
            cls,
            *_args,
            pipelineSlug=pipelineSlug,
            testCases=testCases,
            _configuration=_configuration,
            **kwargs,
        )
