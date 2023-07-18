# coding: utf-8

"""
    Gentrace API

    These API routes are designed to ingest events from clients.  # noqa: E501

    The version of the OpenAPI document: 0.9.0
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

class TestCase(schemas.DictSchema):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    class MetaOapg:
        required = {
            "createdAt",
            "inputs",
            "name",
            "setId",
            "id",
            "updatedAt",
        }

        class properties:
            id = schemas.UUIDSchema
            createdAt = schemas.DateTimeSchema
            updatedAt = schemas.DateTimeSchema
            inputs = schemas.DictSchema
            name = schemas.StrSchema
            setId = schemas.UUIDSchema

            class archivedAt(
                schemas.DateTimeBase,
                schemas.StrBase,
                schemas.NoneBase,
                schemas.Schema,
                schemas.NoneStrMixin,
            ):
                class MetaOapg:
                    format = "date-time"
                def __new__(
                    cls,
                    *_args: typing.Union[
                        None,
                        str,
                        datetime,
                    ],
                    _configuration: typing.Optional[schemas.Configuration] = None,
                ) -> "archivedAt":
                    return super().__new__(
                        cls,
                        *_args,
                        _configuration=_configuration,
                    )

            class expected(
                schemas.StrBase, schemas.NoneBase, schemas.Schema, schemas.NoneStrMixin
            ):
                def __new__(
                    cls,
                    *_args: typing.Union[
                        None,
                        str,
                    ],
                    _configuration: typing.Optional[schemas.Configuration] = None,
                ) -> "expected":
                    return super().__new__(
                        cls,
                        *_args,
                        _configuration=_configuration,
                    )

            class expectedSteps(
                schemas.ListBase,
                schemas.NoneBase,
                schemas.Schema,
                schemas.NoneTupleMixin,
            ):
                class MetaOapg:
                    class items(schemas.DictSchema):
                        class MetaOapg:
                            required = {
                                "output",
                                "key",
                            }

                            class properties:
                                class key(schemas.StrSchema):
                                    pass
                                output = schemas.StrSchema

                                class inputs(
                                    schemas.DictBase,
                                    schemas.NoneBase,
                                    schemas.Schema,
                                    schemas.NoneFrozenDictMixin,
                                ):
                                    class MetaOapg:
                                        additional_properties = schemas.StrSchema
                                    def __getitem__(
                                        self, name: typing.Union[str,]
                                    ) -> MetaOapg.additional_properties:
                                        # dict_instance[name] accessor
                                        return super().__getitem__(name)
                                    def get_item_oapg(
                                        self, name: typing.Union[str,]
                                    ) -> MetaOapg.additional_properties:
                                        return super().get_item_oapg(name)
                                    def __new__(
                                        cls,
                                        *_args: typing.Union[
                                            dict,
                                            frozendict.frozendict,
                                            None,
                                        ],
                                        _configuration: typing.Optional[
                                            schemas.Configuration
                                        ] = None,
                                        **kwargs: typing.Union[
                                            MetaOapg.additional_properties,
                                            str,
                                        ],
                                    ) -> "inputs":
                                        return super().__new__(
                                            cls,
                                            *_args,
                                            _configuration=_configuration,
                                            **kwargs,
                                        )
                                __annotations__ = {
                                    "key": key,
                                    "output": output,
                                    "inputs": inputs,
                                }
                        output: MetaOapg.properties.output
                        key: MetaOapg.properties.key

                        @typing.overload
                        def __getitem__(
                            self, name: typing_extensions.Literal["key"]
                        ) -> MetaOapg.properties.key: ...
                        @typing.overload
                        def __getitem__(
                            self, name: typing_extensions.Literal["output"]
                        ) -> MetaOapg.properties.output: ...
                        @typing.overload
                        def __getitem__(
                            self, name: typing_extensions.Literal["inputs"]
                        ) -> MetaOapg.properties.inputs: ...
                        @typing.overload
                        def __getitem__(
                            self, name: str
                        ) -> schemas.UnsetAnyTypeSchema: ...
                        def __getitem__(
                            self,
                            name: typing.Union[
                                typing_extensions.Literal[
                                    "key",
                                    "output",
                                    "inputs",
                                ],
                                str,
                            ],
                        ):
                            # dict_instance[name] accessor
                            return super().__getitem__(name)
                        @typing.overload
                        def get_item_oapg(
                            self, name: typing_extensions.Literal["key"]
                        ) -> MetaOapg.properties.key: ...
                        @typing.overload
                        def get_item_oapg(
                            self, name: typing_extensions.Literal["output"]
                        ) -> MetaOapg.properties.output: ...
                        @typing.overload
                        def get_item_oapg(
                            self, name: typing_extensions.Literal["inputs"]
                        ) -> typing.Union[
                            MetaOapg.properties.inputs, schemas.Unset
                        ]: ...
                        @typing.overload
                        def get_item_oapg(
                            self, name: str
                        ) -> typing.Union[
                            schemas.UnsetAnyTypeSchema, schemas.Unset
                        ]: ...
                        def get_item_oapg(
                            self,
                            name: typing.Union[
                                typing_extensions.Literal[
                                    "key",
                                    "output",
                                    "inputs",
                                ],
                                str,
                            ],
                        ):
                            return super().get_item_oapg(name)
                        def __new__(
                            cls,
                            *_args: typing.Union[
                                dict,
                                frozendict.frozendict,
                            ],
                            output: typing.Union[
                                MetaOapg.properties.output,
                                str,
                            ],
                            key: typing.Union[
                                MetaOapg.properties.key,
                                str,
                            ],
                            inputs: typing.Union[
                                MetaOapg.properties.inputs,
                                dict,
                                frozendict.frozendict,
                                None,
                                schemas.Unset,
                            ] = schemas.unset,
                            _configuration: typing.Optional[
                                schemas.Configuration
                            ] = None,
                            **kwargs: typing.Union[
                                schemas.AnyTypeSchema,
                                dict,
                                frozendict.frozendict,
                                str,
                                date,
                                datetime,
                                uuid.UUID,
                                int,
                                float,
                                decimal.Decimal,
                                None,
                                list,
                                tuple,
                                bytes,
                            ],
                        ) -> "items":
                            return super().__new__(
                                cls,
                                *_args,
                                output=output,
                                key=key,
                                inputs=inputs,
                                _configuration=_configuration,
                                **kwargs,
                            )
                def __new__(
                    cls,
                    *_args: typing.Union[
                        list,
                        tuple,
                        None,
                    ],
                    _configuration: typing.Optional[schemas.Configuration] = None,
                ) -> "expectedSteps":
                    return super().__new__(
                        cls,
                        *_args,
                        _configuration=_configuration,
                    )
            __annotations__ = {
                "id": id,
                "createdAt": createdAt,
                "updatedAt": updatedAt,
                "inputs": inputs,
                "name": name,
                "setId": setId,
                "archivedAt": archivedAt,
                "expected": expected,
                "expectedSteps": expectedSteps,
            }
    createdAt: MetaOapg.properties.createdAt
    inputs: MetaOapg.properties.inputs
    name: MetaOapg.properties.name
    setId: MetaOapg.properties.setId
    id: MetaOapg.properties.id
    updatedAt: MetaOapg.properties.updatedAt

    @typing.overload
    def __getitem__(
        self, name: typing_extensions.Literal["id"]
    ) -> MetaOapg.properties.id: ...
    @typing.overload
    def __getitem__(
        self, name: typing_extensions.Literal["createdAt"]
    ) -> MetaOapg.properties.createdAt: ...
    @typing.overload
    def __getitem__(
        self, name: typing_extensions.Literal["updatedAt"]
    ) -> MetaOapg.properties.updatedAt: ...
    @typing.overload
    def __getitem__(
        self, name: typing_extensions.Literal["inputs"]
    ) -> MetaOapg.properties.inputs: ...
    @typing.overload
    def __getitem__(
        self, name: typing_extensions.Literal["name"]
    ) -> MetaOapg.properties.name: ...
    @typing.overload
    def __getitem__(
        self, name: typing_extensions.Literal["setId"]
    ) -> MetaOapg.properties.setId: ...
    @typing.overload
    def __getitem__(
        self, name: typing_extensions.Literal["archivedAt"]
    ) -> MetaOapg.properties.archivedAt: ...
    @typing.overload
    def __getitem__(
        self, name: typing_extensions.Literal["expected"]
    ) -> MetaOapg.properties.expected: ...
    @typing.overload
    def __getitem__(
        self, name: typing_extensions.Literal["expectedSteps"]
    ) -> MetaOapg.properties.expectedSteps: ...
    @typing.overload
    def __getitem__(self, name: str) -> schemas.UnsetAnyTypeSchema: ...
    def __getitem__(
        self,
        name: typing.Union[
            typing_extensions.Literal[
                "id",
                "createdAt",
                "updatedAt",
                "inputs",
                "name",
                "setId",
                "archivedAt",
                "expected",
                "expectedSteps",
            ],
            str,
        ],
    ):
        # dict_instance[name] accessor
        return super().__getitem__(name)
    @typing.overload
    def get_item_oapg(
        self, name: typing_extensions.Literal["id"]
    ) -> MetaOapg.properties.id: ...
    @typing.overload
    def get_item_oapg(
        self, name: typing_extensions.Literal["createdAt"]
    ) -> MetaOapg.properties.createdAt: ...
    @typing.overload
    def get_item_oapg(
        self, name: typing_extensions.Literal["updatedAt"]
    ) -> MetaOapg.properties.updatedAt: ...
    @typing.overload
    def get_item_oapg(
        self, name: typing_extensions.Literal["inputs"]
    ) -> MetaOapg.properties.inputs: ...
    @typing.overload
    def get_item_oapg(
        self, name: typing_extensions.Literal["name"]
    ) -> MetaOapg.properties.name: ...
    @typing.overload
    def get_item_oapg(
        self, name: typing_extensions.Literal["setId"]
    ) -> MetaOapg.properties.setId: ...
    @typing.overload
    def get_item_oapg(
        self, name: typing_extensions.Literal["archivedAt"]
    ) -> typing.Union[MetaOapg.properties.archivedAt, schemas.Unset]: ...
    @typing.overload
    def get_item_oapg(
        self, name: typing_extensions.Literal["expected"]
    ) -> typing.Union[MetaOapg.properties.expected, schemas.Unset]: ...
    @typing.overload
    def get_item_oapg(
        self, name: typing_extensions.Literal["expectedSteps"]
    ) -> typing.Union[MetaOapg.properties.expectedSteps, schemas.Unset]: ...
    @typing.overload
    def get_item_oapg(
        self, name: str
    ) -> typing.Union[schemas.UnsetAnyTypeSchema, schemas.Unset]: ...
    def get_item_oapg(
        self,
        name: typing.Union[
            typing_extensions.Literal[
                "id",
                "createdAt",
                "updatedAt",
                "inputs",
                "name",
                "setId",
                "archivedAt",
                "expected",
                "expectedSteps",
            ],
            str,
        ],
    ):
        return super().get_item_oapg(name)
    def __new__(
        cls,
        *_args: typing.Union[
            dict,
            frozendict.frozendict,
        ],
        createdAt: typing.Union[
            MetaOapg.properties.createdAt,
            str,
            datetime,
        ],
        inputs: typing.Union[
            MetaOapg.properties.inputs,
            dict,
            frozendict.frozendict,
        ],
        name: typing.Union[
            MetaOapg.properties.name,
            str,
        ],
        setId: typing.Union[
            MetaOapg.properties.setId,
            str,
            uuid.UUID,
        ],
        id: typing.Union[
            MetaOapg.properties.id,
            str,
            uuid.UUID,
        ],
        updatedAt: typing.Union[
            MetaOapg.properties.updatedAt,
            str,
            datetime,
        ],
        archivedAt: typing.Union[
            MetaOapg.properties.archivedAt, None, str, datetime, schemas.Unset
        ] = schemas.unset,
        expected: typing.Union[
            MetaOapg.properties.expected, None, str, schemas.Unset
        ] = schemas.unset,
        expectedSteps: typing.Union[
            MetaOapg.properties.expectedSteps, list, tuple, None, schemas.Unset
        ] = schemas.unset,
        _configuration: typing.Optional[schemas.Configuration] = None,
        **kwargs: typing.Union[
            schemas.AnyTypeSchema,
            dict,
            frozendict.frozendict,
            str,
            date,
            datetime,
            uuid.UUID,
            int,
            float,
            decimal.Decimal,
            None,
            list,
            tuple,
            bytes,
        ],
    ) -> "TestCase":
        return super().__new__(
            cls,
            *_args,
            createdAt=createdAt,
            inputs=inputs,
            name=name,
            setId=setId,
            id=id,
            updatedAt=updatedAt,
            archivedAt=archivedAt,
            expected=expected,
            expectedSteps=expectedSteps,
            _configuration=_configuration,
            **kwargs,
        )
