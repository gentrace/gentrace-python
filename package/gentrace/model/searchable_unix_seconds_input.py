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


class SearchableUnixSecondsInput(
    schemas.ComposedSchema,
):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """


    class MetaOapg:
        one_of_0 = schemas.Float32Schema
        
        
        class one_of_1(
            schemas.DictSchema
        ):
        
        
            class MetaOapg:
                
                class properties:
                    gt = schemas.Float32Schema
                    gte = schemas.Float32Schema
                    lt = schemas.Float32Schema
                    lte = schemas.Float32Schema
                    __annotations__ = {
                        "gt": gt,
                        "gte": gte,
                        "lt": lt,
                        "lte": lte,
                    }
            
            @typing.overload
            def __getitem__(self, name: typing_extensions.Literal["gt"]) -> MetaOapg.properties.gt: ...
            
            @typing.overload
            def __getitem__(self, name: typing_extensions.Literal["gte"]) -> MetaOapg.properties.gte: ...
            
            @typing.overload
            def __getitem__(self, name: typing_extensions.Literal["lt"]) -> MetaOapg.properties.lt: ...
            
            @typing.overload
            def __getitem__(self, name: typing_extensions.Literal["lte"]) -> MetaOapg.properties.lte: ...
            
            @typing.overload
            def __getitem__(self, name: str) -> schemas.UnsetAnyTypeSchema: ...
            
            def __getitem__(self, name: typing.Union[typing_extensions.Literal["gt", "gte", "lt", "lte", ], str]):
                # dict_instance[name] accessor
                return super().__getitem__(name)
            
            
            @typing.overload
            def get_item_oapg(self, name: typing_extensions.Literal["gt"]) -> typing.Union[MetaOapg.properties.gt, schemas.Unset]: ...
            
            @typing.overload
            def get_item_oapg(self, name: typing_extensions.Literal["gte"]) -> typing.Union[MetaOapg.properties.gte, schemas.Unset]: ...
            
            @typing.overload
            def get_item_oapg(self, name: typing_extensions.Literal["lt"]) -> typing.Union[MetaOapg.properties.lt, schemas.Unset]: ...
            
            @typing.overload
            def get_item_oapg(self, name: typing_extensions.Literal["lte"]) -> typing.Union[MetaOapg.properties.lte, schemas.Unset]: ...
            
            @typing.overload
            def get_item_oapg(self, name: str) -> typing.Union[schemas.UnsetAnyTypeSchema, schemas.Unset]: ...
            
            def get_item_oapg(self, name: typing.Union[typing_extensions.Literal["gt", "gte", "lt", "lte", ], str]):
                return super().get_item_oapg(name)
            
        
            def __new__(
                cls,
                *_args: typing.Union[dict, frozendict.frozendict, ],
                gt: typing.Union[MetaOapg.properties.gt, decimal.Decimal, int, float, schemas.Unset] = schemas.unset,
                gte: typing.Union[MetaOapg.properties.gte, decimal.Decimal, int, float, schemas.Unset] = schemas.unset,
                lt: typing.Union[MetaOapg.properties.lt, decimal.Decimal, int, float, schemas.Unset] = schemas.unset,
                lte: typing.Union[MetaOapg.properties.lte, decimal.Decimal, int, float, schemas.Unset] = schemas.unset,
                _configuration: typing.Optional[schemas.Configuration] = None,
                **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
            ) -> 'one_of_1':
                return super().__new__(
                    cls,
                    *_args,
                    gt=gt,
                    gte=gte,
                    lt=lt,
                    lte=lte,
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
    ) -> 'SearchableUnixSecondsInput':
        return super().__new__(
            cls,
            *_args,
            _configuration=_configuration,
            **kwargs,
        )
