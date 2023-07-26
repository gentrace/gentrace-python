# coding: utf-8

"""
    Gentrace API

    These API routes are designed to ingest events from clients.  # noqa: E501

    The version of the OpenAPI document: 0.11.0
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


class TestResult(schemas.DictSchema):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    class MetaOapg:
        class properties:
            id = schemas.UUIDSchema
            createdAt = schemas.DateTimeSchema
            updatedAt = schemas.DateTimeSchema
            pipelineId = schemas.UUIDSchema
            branch = schemas.StrSchema
            commit = schemas.StrSchema
            name = schemas.StrSchema
            __annotations__ = {
                "id": id,
                "createdAt": createdAt,
                "updatedAt": updatedAt,
                "pipelineId": pipelineId,
                "branch": branch,
                "commit": commit,
                "name": name,
            }

    @typing.overload
    def __getitem__(
        self, name: typing_extensions.Literal["id"]
    ) -> MetaOapg.properties.id:
        ...

    @typing.overload
    def __getitem__(
        self, name: typing_extensions.Literal["createdAt"]
    ) -> MetaOapg.properties.createdAt:
        ...

    @typing.overload
    def __getitem__(
        self, name: typing_extensions.Literal["updatedAt"]
    ) -> MetaOapg.properties.updatedAt:
        ...

    @typing.overload
    def __getitem__(
        self, name: typing_extensions.Literal["pipelineId"]
    ) -> MetaOapg.properties.pipelineId:
        ...

    @typing.overload
    def __getitem__(
        self, name: typing_extensions.Literal["branch"]
    ) -> MetaOapg.properties.branch:
        ...

    @typing.overload
    def __getitem__(
        self, name: typing_extensions.Literal["commit"]
    ) -> MetaOapg.properties.commit:
        ...

    @typing.overload
    def __getitem__(
        self, name: typing_extensions.Literal["name"]
    ) -> MetaOapg.properties.name:
        ...

    @typing.overload
    def __getitem__(self, name: str) -> schemas.UnsetAnyTypeSchema:
        ...

    def __getitem__(
        self,
        name: typing.Union[
            typing_extensions.Literal[
                "id",
                "createdAt",
                "updatedAt",
                "pipelineId",
                "branch",
                "commit",
                "name",
            ],
            str,
        ],
    ):
        # dict_instance[name] accessor
        return super().__getitem__(name)

    @typing.overload
    def get_item_oapg(
        self, name: typing_extensions.Literal["id"]
    ) -> typing.Union[MetaOapg.properties.id, schemas.Unset]:
        ...

    @typing.overload
    def get_item_oapg(
        self, name: typing_extensions.Literal["createdAt"]
    ) -> typing.Union[MetaOapg.properties.createdAt, schemas.Unset]:
        ...

    @typing.overload
    def get_item_oapg(
        self, name: typing_extensions.Literal["updatedAt"]
    ) -> typing.Union[MetaOapg.properties.updatedAt, schemas.Unset]:
        ...

    @typing.overload
    def get_item_oapg(
        self, name: typing_extensions.Literal["pipelineId"]
    ) -> typing.Union[MetaOapg.properties.pipelineId, schemas.Unset]:
        ...

    @typing.overload
    def get_item_oapg(
        self, name: typing_extensions.Literal["branch"]
    ) -> typing.Union[MetaOapg.properties.branch, schemas.Unset]:
        ...

    @typing.overload
    def get_item_oapg(
        self, name: typing_extensions.Literal["commit"]
    ) -> typing.Union[MetaOapg.properties.commit, schemas.Unset]:
        ...

    @typing.overload
    def get_item_oapg(
        self, name: typing_extensions.Literal["name"]
    ) -> typing.Union[MetaOapg.properties.name, schemas.Unset]:
        ...

    @typing.overload
    def get_item_oapg(
        self, name: str
    ) -> typing.Union[schemas.UnsetAnyTypeSchema, schemas.Unset]:
        ...

    def get_item_oapg(
        self,
        name: typing.Union[
            typing_extensions.Literal[
                "id",
                "createdAt",
                "updatedAt",
                "pipelineId",
                "branch",
                "commit",
                "name",
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
        id: typing.Union[
            MetaOapg.properties.id, str, uuid.UUID, schemas.Unset
        ] = schemas.unset,
        createdAt: typing.Union[
            MetaOapg.properties.createdAt, str, datetime, schemas.Unset
        ] = schemas.unset,
        updatedAt: typing.Union[
            MetaOapg.properties.updatedAt, str, datetime, schemas.Unset
        ] = schemas.unset,
        pipelineId: typing.Union[
            MetaOapg.properties.pipelineId, str, uuid.UUID, schemas.Unset
        ] = schemas.unset,
        branch: typing.Union[
            MetaOapg.properties.branch, str, schemas.Unset
        ] = schemas.unset,
        commit: typing.Union[
            MetaOapg.properties.commit, str, schemas.Unset
        ] = schemas.unset,
        name: typing.Union[
            MetaOapg.properties.name, str, schemas.Unset
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
    ) -> "TestResult":
        return super().__new__(
            cls,
            *_args,
            id=id,
            createdAt=createdAt,
            updatedAt=updatedAt,
            pipelineId=pipelineId,
            branch=branch,
            commit=commit,
            name=name,
            _configuration=_configuration,
            **kwargs,
        )
