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


class ExpandedTestRun(
    schemas.ComposedSchema,
):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """


    class MetaOapg:
        
        
        class all_of_1(
            schemas.DictSchema
        ):
        
        
            class MetaOapg:
                
                class properties:
                
                    @staticmethod
                    def full() -> typing.Type['FullRun']:
                        return FullRun
                    
                    
                    class steps(
                        schemas.ListSchema
                    ):
                    
                    
                        class MetaOapg:
                            
                            @staticmethod
                            def items() -> typing.Type['ResolvedStepRun']:
                                return ResolvedStepRun
                    
                        def __new__(
                            cls,
                            _arg: typing.Union[typing.Tuple['ResolvedStepRun'], typing.List['ResolvedStepRun']],
                            _configuration: typing.Optional[schemas.Configuration] = None,
                        ) -> 'steps':
                            return super().__new__(
                                cls,
                                _arg,
                                _configuration=_configuration,
                            )
                    
                        def __getitem__(self, i: int) -> 'ResolvedStepRun':
                            return super().__getitem__(i)
                
                    @staticmethod
                    def case() -> typing.Type['TestCase']:
                        return TestCase
                    
                    
                    class evaluations(
                        schemas.ListSchema
                    ):
                    
                    
                        class MetaOapg:
                            
                            @staticmethod
                            def items() -> typing.Type['TestEvaluation']:
                                return TestEvaluation
                    
                        def __new__(
                            cls,
                            _arg: typing.Union[typing.Tuple['TestEvaluation'], typing.List['TestEvaluation']],
                            _configuration: typing.Optional[schemas.Configuration] = None,
                        ) -> 'evaluations':
                            return super().__new__(
                                cls,
                                _arg,
                                _configuration=_configuration,
                            )
                    
                        def __getitem__(self, i: int) -> 'TestEvaluation':
                            return super().__getitem__(i)
                    __annotations__ = {
                        "full": full,
                        "steps": steps,
                        "case": case,
                        "evaluations": evaluations,
                    }
            
            @typing.overload
            def __getitem__(self, name: typing_extensions.Literal["full"]) -> 'FullRun': ...
            
            @typing.overload
            def __getitem__(self, name: typing_extensions.Literal["steps"]) -> MetaOapg.properties.steps: ...
            
            @typing.overload
            def __getitem__(self, name: typing_extensions.Literal["case"]) -> 'TestCase': ...
            
            @typing.overload
            def __getitem__(self, name: typing_extensions.Literal["evaluations"]) -> MetaOapg.properties.evaluations: ...
            
            @typing.overload
            def __getitem__(self, name: str) -> schemas.UnsetAnyTypeSchema: ...
            
            def __getitem__(self, name: typing.Union[typing_extensions.Literal["full", "steps", "case", "evaluations", ], str]):
                # dict_instance[name] accessor
                return super().__getitem__(name)
            
            
            @typing.overload
            def get_item_oapg(self, name: typing_extensions.Literal["full"]) -> typing.Union['FullRun', schemas.Unset]: ...
            
            @typing.overload
            def get_item_oapg(self, name: typing_extensions.Literal["steps"]) -> typing.Union[MetaOapg.properties.steps, schemas.Unset]: ...
            
            @typing.overload
            def get_item_oapg(self, name: typing_extensions.Literal["case"]) -> typing.Union['TestCase', schemas.Unset]: ...
            
            @typing.overload
            def get_item_oapg(self, name: typing_extensions.Literal["evaluations"]) -> typing.Union[MetaOapg.properties.evaluations, schemas.Unset]: ...
            
            @typing.overload
            def get_item_oapg(self, name: str) -> typing.Union[schemas.UnsetAnyTypeSchema, schemas.Unset]: ...
            
            def get_item_oapg(self, name: typing.Union[typing_extensions.Literal["full", "steps", "case", "evaluations", ], str]):
                return super().get_item_oapg(name)
            
        
            def __new__(
                cls,
                *_args: typing.Union[dict, frozendict.frozendict, ],
                full: typing.Union['FullRun', schemas.Unset] = schemas.unset,
                steps: typing.Union[MetaOapg.properties.steps, list, tuple, schemas.Unset] = schemas.unset,
                case: typing.Union['TestCase', schemas.Unset] = schemas.unset,
                evaluations: typing.Union[MetaOapg.properties.evaluations, list, tuple, schemas.Unset] = schemas.unset,
                _configuration: typing.Optional[schemas.Configuration] = None,
                **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
            ) -> 'all_of_1':
                return super().__new__(
                    cls,
                    *_args,
                    full=full,
                    steps=steps,
                    case=case,
                    evaluations=evaluations,
                    _configuration=_configuration,
                    **kwargs,
                )
        
        @classmethod
        @functools.lru_cache()
        def all_of(cls):
            # we need this here to make our import statements work
            # we must store _composed_schemas in here so the code is only run
            # when we invoke this method. If we kept this at the class
            # level we would get an error because the class level
            # code would be run when this module is imported, and these composed
            # classes don't exist yet because their module has not finished
            # loading
            return [
                TestRun,
                cls.all_of_1,
            ]


    def __new__(
        cls,
        *_args: typing.Union[dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, bool, None, list, tuple, bytes, io.FileIO, io.BufferedReader, ],
        _configuration: typing.Optional[schemas.Configuration] = None,
        **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
    ) -> 'ExpandedTestRun':
        return super().__new__(
            cls,
            *_args,
            _configuration=_configuration,
            **kwargs,
        )

from gentrace.model.full_run import FullRun
from gentrace.model.resolved_step_run import ResolvedStepRun
from gentrace.model.test_case import TestCase
from gentrace.model.test_evaluation import TestEvaluation
from gentrace.model.test_run import TestRun
