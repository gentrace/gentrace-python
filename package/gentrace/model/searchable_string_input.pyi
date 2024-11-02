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

class SearchableStringInput(
    schemas.ComposedSchema,
):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """


    class MetaOapg:
        one_of_0 = schemas.StrSchema
        
        
        class one_of_1(
            schemas.DictSchema
        ):
        
        
            class MetaOapg:
                
                class properties:
                    contains = schemas.StrSchema
                    search = schemas.StrSchema
                    startsWith = schemas.StrSchema
                    endsWith = schemas.StrSchema
                    
                    
                    class _in(
                        schemas.ListSchema
                    ):
                    
                    
                        class MetaOapg:
                            items = schemas.StrSchema
                    
                        def __new__(
                            cls,
                            _arg: typing.Union[typing.Tuple[typing.Union[MetaOapg.items, str, ]], typing.List[typing.Union[MetaOapg.items, str, ]]],
                            _configuration: typing.Optional[schemas.Configuration] = None,
                        ) -> '_in':
                            return super().__new__(
                                cls,
                                _arg,
                                _configuration=_configuration,
                            )
                    
                        def __getitem__(self, i: int) -> MetaOapg.items:
                            return super().__getitem__(i)
                    
                    
                    class notIn(
                        schemas.ListSchema
                    ):
                    
                    
                        class MetaOapg:
                            items = schemas.StrSchema
                    
                        def __new__(
                            cls,
                            _arg: typing.Union[typing.Tuple[typing.Union[MetaOapg.items, str, ]], typing.List[typing.Union[MetaOapg.items, str, ]]],
                            _configuration: typing.Optional[schemas.Configuration] = None,
                        ) -> 'notIn':
                            return super().__new__(
                                cls,
                                _arg,
                                _configuration=_configuration,
                            )
                    
                        def __getitem__(self, i: int) -> MetaOapg.items:
                            return super().__getitem__(i)
                    
                    
                    class mode(
                        schemas.EnumBase,
                        schemas.StrSchema
                    ):
                        
                        @schemas.classproperty
                        def INSENSITIVE(cls):
                            return cls("insensitive")
                        
                        @schemas.classproperty
                        def DEFAULT(cls):
                            return cls("default")
                    __annotations__ = {
                        "contains": contains,
                        "search": search,
                        "startsWith": startsWith,
                        "endsWith": endsWith,
                        "in": _in,
                        "notIn": notIn,
                        "mode": mode,
                    }
            
            @typing.overload
            def __getitem__(self, name: typing_extensions.Literal["contains"]) -> MetaOapg.properties.contains: ...
            
            @typing.overload
            def __getitem__(self, name: typing_extensions.Literal["search"]) -> MetaOapg.properties.search: ...
            
            @typing.overload
            def __getitem__(self, name: typing_extensions.Literal["startsWith"]) -> MetaOapg.properties.startsWith: ...
            
            @typing.overload
            def __getitem__(self, name: typing_extensions.Literal["endsWith"]) -> MetaOapg.properties.endsWith: ...
            
            @typing.overload
            def __getitem__(self, name: typing_extensions.Literal["in"]) -> MetaOapg.properties._in: ...
            
            @typing.overload
            def __getitem__(self, name: typing_extensions.Literal["notIn"]) -> MetaOapg.properties.notIn: ...
            
            @typing.overload
            def __getitem__(self, name: typing_extensions.Literal["mode"]) -> MetaOapg.properties.mode: ...
            
            @typing.overload
            def __getitem__(self, name: str) -> schemas.UnsetAnyTypeSchema: ...
            
            def __getitem__(self, name: typing.Union[typing_extensions.Literal["contains", "search", "startsWith", "endsWith", "in", "notIn", "mode", ], str]):
                # dict_instance[name] accessor
                return super().__getitem__(name)
            
            
            @typing.overload
            def get_item_oapg(self, name: typing_extensions.Literal["contains"]) -> typing.Union[MetaOapg.properties.contains, schemas.Unset]: ...
            
            @typing.overload
            def get_item_oapg(self, name: typing_extensions.Literal["search"]) -> typing.Union[MetaOapg.properties.search, schemas.Unset]: ...
            
            @typing.overload
            def get_item_oapg(self, name: typing_extensions.Literal["startsWith"]) -> typing.Union[MetaOapg.properties.startsWith, schemas.Unset]: ...
            
            @typing.overload
            def get_item_oapg(self, name: typing_extensions.Literal["endsWith"]) -> typing.Union[MetaOapg.properties.endsWith, schemas.Unset]: ...
            
            @typing.overload
            def get_item_oapg(self, name: typing_extensions.Literal["in"]) -> typing.Union[MetaOapg.properties._in, schemas.Unset]: ...
            
            @typing.overload
            def get_item_oapg(self, name: typing_extensions.Literal["notIn"]) -> typing.Union[MetaOapg.properties.notIn, schemas.Unset]: ...
            
            @typing.overload
            def get_item_oapg(self, name: typing_extensions.Literal["mode"]) -> typing.Union[MetaOapg.properties.mode, schemas.Unset]: ...
            
            @typing.overload
            def get_item_oapg(self, name: str) -> typing.Union[schemas.UnsetAnyTypeSchema, schemas.Unset]: ...
            
            def get_item_oapg(self, name: typing.Union[typing_extensions.Literal["contains", "search", "startsWith", "endsWith", "in", "notIn", "mode", ], str]):
                return super().get_item_oapg(name)
            
        
            def __new__(
                cls,
                *_args: typing.Union[dict, frozendict.frozendict, ],
                contains: typing.Union[MetaOapg.properties.contains, str, schemas.Unset] = schemas.unset,
                search: typing.Union[MetaOapg.properties.search, str, schemas.Unset] = schemas.unset,
                startsWith: typing.Union[MetaOapg.properties.startsWith, str, schemas.Unset] = schemas.unset,
                endsWith: typing.Union[MetaOapg.properties.endsWith, str, schemas.Unset] = schemas.unset,
                notIn: typing.Union[MetaOapg.properties.notIn, list, tuple, schemas.Unset] = schemas.unset,
                mode: typing.Union[MetaOapg.properties.mode, str, schemas.Unset] = schemas.unset,
                _configuration: typing.Optional[schemas.Configuration] = None,
                **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
            ) -> 'one_of_1':
                return super().__new__(
                    cls,
                    *_args,
                    contains=contains,
                    search=search,
                    startsWith=startsWith,
                    endsWith=endsWith,
                    notIn=notIn,
                    mode=mode,
                    _configuration=_configuration,
                    **kwargs,
                )
        
        @classmethod
        @functools.lru_cache()
        def one_of(cls):
            # we need this here to make our import statements work
            # we must store _composed_schemas in here so the code is only run
            # when we invoke this method. If we kept this at the class
            # level we would get an error because the class level
            # code would be run when this module is imported, and these composed
            # classes don't exist yet because their module has not finished
            # loading
            return [
                cls.one_of_0,
                cls.one_of_1,
            ]


    def __new__(
        cls,
        *_args: typing.Union[dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, bool, None, list, tuple, bytes, io.FileIO, io.BufferedReader, ],
        _configuration: typing.Optional[schemas.Configuration] = None,
        **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
    ) -> 'SearchableStringInput':
        return super().__new__(
            cls,
            *_args,
            _configuration=_configuration,
            **kwargs,
        )
