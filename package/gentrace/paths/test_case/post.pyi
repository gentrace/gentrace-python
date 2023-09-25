# coding: utf-8

"""


    Generated by: https://openapi-generator.tech
"""

import decimal  # noqa: F401
import functools  # noqa: F401
import io  # noqa: F401
import re  # noqa: F401
import typing  # noqa: F401
import uuid  # noqa: F401
from dataclasses import dataclass
from datetime import date, datetime  # noqa: F401

import frozendict  # noqa: F401
import typing_extensions  # noqa: F401
import urllib3
from urllib3._collections import HTTPHeaderDict

from gentrace import (
    api_client,
    exceptions,
    schemas,  # noqa: F401
)
from gentrace.model.create_multiple_test_cases import CreateMultipleTestCases
from gentrace.model.create_single_test_case import CreateSingleTestCase

# body param

class SchemaForRequestBodyApplicationJson(
    schemas.ComposedSchema,
):
    class MetaOapg:
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
                CreateSingleTestCase,
                CreateMultipleTestCases,
            ]
    def __new__(
        cls,
        *_args: typing.Union[
            dict,
            frozendict.frozendict,
            str,
            date,
            datetime,
            uuid.UUID,
            int,
            float,
            decimal.Decimal,
            bool,
            None,
            list,
            tuple,
            bytes,
            io.FileIO,
            io.BufferedReader,
        ],
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
    ) -> "SchemaForRequestBodyApplicationJson":
        return super().__new__(
            cls,
            *_args,
            _configuration=_configuration,
            **kwargs,
        )

request_body_any_type = api_client.RequestBody(
    content={
        "application/json": api_client.MediaType(
            schema=SchemaForRequestBodyApplicationJson
        ),
    },
    required=True,
)

class SchemaFor200ResponseBodyApplicationJson(
    schemas.ComposedSchema,
):
    class MetaOapg:
        class one_of_0(schemas.DictSchema):
            class MetaOapg:
                class properties:
                    caseId = schemas.StrSchema
                    __annotations__ = {
                        "caseId": caseId,
                    }
            @typing.overload
            def __getitem__(
                self, name: typing_extensions.Literal["caseId"]
            ) -> MetaOapg.properties.caseId: ...
            @typing.overload
            def __getitem__(self, name: str) -> schemas.UnsetAnyTypeSchema: ...
            def __getitem__(
                self, name: typing.Union[typing_extensions.Literal["caseId",], str]
            ):
                # dict_instance[name] accessor
                return super().__getitem__(name)
            @typing.overload
            def get_item_oapg(
                self, name: typing_extensions.Literal["caseId"]
            ) -> typing.Union[MetaOapg.properties.caseId, schemas.Unset]: ...
            @typing.overload
            def get_item_oapg(
                self, name: str
            ) -> typing.Union[schemas.UnsetAnyTypeSchema, schemas.Unset]: ...
            def get_item_oapg(
                self, name: typing.Union[typing_extensions.Literal["caseId",], str]
            ):
                return super().get_item_oapg(name)
            def __new__(
                cls,
                *_args: typing.Union[
                    dict,
                    frozendict.frozendict,
                ],
                caseId: typing.Union[
                    MetaOapg.properties.caseId, str, schemas.Unset
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
            ) -> "one_of_0":
                return super().__new__(
                    cls,
                    *_args,
                    caseId=caseId,
                    _configuration=_configuration,
                    **kwargs,
                )

        class one_of_1(schemas.DictSchema):
            class MetaOapg:
                class properties:
                    creationCount = schemas.IntSchema
                    __annotations__ = {
                        "creationCount": creationCount,
                    }
            @typing.overload
            def __getitem__(
                self, name: typing_extensions.Literal["creationCount"]
            ) -> MetaOapg.properties.creationCount: ...
            @typing.overload
            def __getitem__(self, name: str) -> schemas.UnsetAnyTypeSchema: ...
            def __getitem__(
                self,
                name: typing.Union[typing_extensions.Literal["creationCount",], str],
            ):
                # dict_instance[name] accessor
                return super().__getitem__(name)
            @typing.overload
            def get_item_oapg(
                self, name: typing_extensions.Literal["creationCount"]
            ) -> typing.Union[MetaOapg.properties.creationCount, schemas.Unset]: ...
            @typing.overload
            def get_item_oapg(
                self, name: str
            ) -> typing.Union[schemas.UnsetAnyTypeSchema, schemas.Unset]: ...
            def get_item_oapg(
                self,
                name: typing.Union[typing_extensions.Literal["creationCount",], str],
            ):
                return super().get_item_oapg(name)
            def __new__(
                cls,
                *_args: typing.Union[
                    dict,
                    frozendict.frozendict,
                ],
                creationCount: typing.Union[
                    MetaOapg.properties.creationCount,
                    decimal.Decimal,
                    int,
                    schemas.Unset,
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
            ) -> "one_of_1":
                return super().__new__(
                    cls,
                    *_args,
                    creationCount=creationCount,
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
        *_args: typing.Union[
            dict,
            frozendict.frozendict,
            str,
            date,
            datetime,
            uuid.UUID,
            int,
            float,
            decimal.Decimal,
            bool,
            None,
            list,
            tuple,
            bytes,
            io.FileIO,
            io.BufferedReader,
        ],
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
    ) -> "SchemaFor200ResponseBodyApplicationJson":
        return super().__new__(
            cls,
            *_args,
            _configuration=_configuration,
            **kwargs,
        )

class SchemaFor200ResponseBodyApplicationJsonCharsetutf8(
    schemas.ComposedSchema,
):
    class MetaOapg:
        class one_of_0(schemas.DictSchema):
            class MetaOapg:
                class properties:
                    caseId = schemas.StrSchema
                    __annotations__ = {
                        "caseId": caseId,
                    }
            @typing.overload
            def __getitem__(
                self, name: typing_extensions.Literal["caseId"]
            ) -> MetaOapg.properties.caseId: ...
            @typing.overload
            def __getitem__(self, name: str) -> schemas.UnsetAnyTypeSchema: ...
            def __getitem__(
                self, name: typing.Union[typing_extensions.Literal["caseId",], str]
            ):
                # dict_instance[name] accessor
                return super().__getitem__(name)
            @typing.overload
            def get_item_oapg(
                self, name: typing_extensions.Literal["caseId"]
            ) -> typing.Union[MetaOapg.properties.caseId, schemas.Unset]: ...
            @typing.overload
            def get_item_oapg(
                self, name: str
            ) -> typing.Union[schemas.UnsetAnyTypeSchema, schemas.Unset]: ...
            def get_item_oapg(
                self, name: typing.Union[typing_extensions.Literal["caseId",], str]
            ):
                return super().get_item_oapg(name)
            def __new__(
                cls,
                *_args: typing.Union[
                    dict,
                    frozendict.frozendict,
                ],
                caseId: typing.Union[
                    MetaOapg.properties.caseId, str, schemas.Unset
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
            ) -> "one_of_0":
                return super().__new__(
                    cls,
                    *_args,
                    caseId=caseId,
                    _configuration=_configuration,
                    **kwargs,
                )

        class one_of_1(schemas.DictSchema):
            class MetaOapg:
                class properties:
                    creationCount = schemas.IntSchema
                    __annotations__ = {
                        "creationCount": creationCount,
                    }
            @typing.overload
            def __getitem__(
                self, name: typing_extensions.Literal["creationCount"]
            ) -> MetaOapg.properties.creationCount: ...
            @typing.overload
            def __getitem__(self, name: str) -> schemas.UnsetAnyTypeSchema: ...
            def __getitem__(
                self,
                name: typing.Union[typing_extensions.Literal["creationCount",], str],
            ):
                # dict_instance[name] accessor
                return super().__getitem__(name)
            @typing.overload
            def get_item_oapg(
                self, name: typing_extensions.Literal["creationCount"]
            ) -> typing.Union[MetaOapg.properties.creationCount, schemas.Unset]: ...
            @typing.overload
            def get_item_oapg(
                self, name: str
            ) -> typing.Union[schemas.UnsetAnyTypeSchema, schemas.Unset]: ...
            def get_item_oapg(
                self,
                name: typing.Union[typing_extensions.Literal["creationCount",], str],
            ):
                return super().get_item_oapg(name)
            def __new__(
                cls,
                *_args: typing.Union[
                    dict,
                    frozendict.frozendict,
                ],
                creationCount: typing.Union[
                    MetaOapg.properties.creationCount,
                    decimal.Decimal,
                    int,
                    schemas.Unset,
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
            ) -> "one_of_1":
                return super().__new__(
                    cls,
                    *_args,
                    creationCount=creationCount,
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
        *_args: typing.Union[
            dict,
            frozendict.frozendict,
            str,
            date,
            datetime,
            uuid.UUID,
            int,
            float,
            decimal.Decimal,
            bool,
            None,
            list,
            tuple,
            bytes,
            io.FileIO,
            io.BufferedReader,
        ],
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
    ) -> "SchemaFor200ResponseBodyApplicationJsonCharsetutf8":
        return super().__new__(
            cls,
            *_args,
            _configuration=_configuration,
            **kwargs,
        )

@dataclass
class ApiResponseFor200(api_client.ApiResponse):
    response: urllib3.HTTPResponse
    body: typing.Union[
        SchemaFor200ResponseBodyApplicationJson,
        SchemaFor200ResponseBodyApplicationJsonCharsetutf8,
    ]
    headers: schemas.Unset = schemas.unset

_response_for_200 = api_client.OpenApiResponse(
    response_cls=ApiResponseFor200,
    content={
        "application/json": api_client.MediaType(
            schema=SchemaFor200ResponseBodyApplicationJson
        ),
        "application/json; charset=utf-8": api_client.MediaType(
            schema=SchemaFor200ResponseBodyApplicationJsonCharsetutf8
        ),
    },
)

@dataclass
class ApiResponseFor400(api_client.ApiResponse):
    response: urllib3.HTTPResponse
    body: schemas.Unset = schemas.unset
    headers: schemas.Unset = schemas.unset

_response_for_400 = api_client.OpenApiResponse(
    response_cls=ApiResponseFor400,
)

@dataclass
class ApiResponseFor500(api_client.ApiResponse):
    response: urllib3.HTTPResponse
    body: schemas.Unset = schemas.unset
    headers: schemas.Unset = schemas.unset

_response_for_500 = api_client.OpenApiResponse(
    response_cls=ApiResponseFor500,
)
_all_accept_content_types = (
    "application/json",
    "application/json; charset=utf-8",
)

class BaseApi(api_client.Api):
    @typing.overload
    def _test_case_post_oapg(
        self,
        body: typing.Union[
            SchemaForRequestBodyApplicationJson,
            dict,
            frozendict.frozendict,
            str,
            date,
            datetime,
            uuid.UUID,
            int,
            float,
            decimal.Decimal,
            bool,
            None,
            list,
            tuple,
            bytes,
            io.FileIO,
            io.BufferedReader,
        ],
        content_type: typing_extensions.Literal["application/json"] = ...,
        accept_content_types: typing.Tuple[str] = _all_accept_content_types,
        stream: bool = False,
        timeout: typing.Optional[typing.Union[int, typing.Tuple]] = None,
        skip_deserialization: typing_extensions.Literal[False] = ...,
    ) -> typing.Union[ApiResponseFor200,]: ...
    @typing.overload
    def _test_case_post_oapg(
        self,
        body: typing.Union[
            SchemaForRequestBodyApplicationJson,
            dict,
            frozendict.frozendict,
            str,
            date,
            datetime,
            uuid.UUID,
            int,
            float,
            decimal.Decimal,
            bool,
            None,
            list,
            tuple,
            bytes,
            io.FileIO,
            io.BufferedReader,
        ],
        content_type: str = ...,
        accept_content_types: typing.Tuple[str] = _all_accept_content_types,
        stream: bool = False,
        timeout: typing.Optional[typing.Union[int, typing.Tuple]] = None,
        skip_deserialization: typing_extensions.Literal[False] = ...,
    ) -> typing.Union[ApiResponseFor200,]: ...
    @typing.overload
    def _test_case_post_oapg(
        self,
        body: typing.Union[
            SchemaForRequestBodyApplicationJson,
            dict,
            frozendict.frozendict,
            str,
            date,
            datetime,
            uuid.UUID,
            int,
            float,
            decimal.Decimal,
            bool,
            None,
            list,
            tuple,
            bytes,
            io.FileIO,
            io.BufferedReader,
        ],
        skip_deserialization: typing_extensions.Literal[True],
        content_type: str = ...,
        accept_content_types: typing.Tuple[str] = _all_accept_content_types,
        stream: bool = False,
        timeout: typing.Optional[typing.Union[int, typing.Tuple]] = None,
    ) -> api_client.ApiResponseWithoutDeserialization: ...
    @typing.overload
    def _test_case_post_oapg(
        self,
        body: typing.Union[
            SchemaForRequestBodyApplicationJson,
            dict,
            frozendict.frozendict,
            str,
            date,
            datetime,
            uuid.UUID,
            int,
            float,
            decimal.Decimal,
            bool,
            None,
            list,
            tuple,
            bytes,
            io.FileIO,
            io.BufferedReader,
        ],
        content_type: str = ...,
        accept_content_types: typing.Tuple[str] = _all_accept_content_types,
        stream: bool = False,
        timeout: typing.Optional[typing.Union[int, typing.Tuple]] = None,
        skip_deserialization: bool = ...,
    ) -> typing.Union[
        ApiResponseFor200,
        api_client.ApiResponseWithoutDeserialization,
    ]: ...
    def _test_case_post_oapg(
        self,
        body: typing.Union[
            SchemaForRequestBodyApplicationJson,
            dict,
            frozendict.frozendict,
            str,
            date,
            datetime,
            uuid.UUID,
            int,
            float,
            decimal.Decimal,
            bool,
            None,
            list,
            tuple,
            bytes,
            io.FileIO,
            io.BufferedReader,
        ],
        content_type: str = "application/json",
        accept_content_types: typing.Tuple[str] = _all_accept_content_types,
        stream: bool = False,
        timeout: typing.Optional[typing.Union[int, typing.Tuple]] = None,
        skip_deserialization: bool = False,
    ):
        """
        Create a new test case
        :param skip_deserialization: If true then api_response.response will be set but
            api_response.body and api_response.headers will not be deserialized into schema
            class instances
        """
        used_path = path.value

        _headers = HTTPHeaderDict()
        # TODO add cookie handling
        if accept_content_types:
            for accept_content_type in accept_content_types:
                _headers.add("Accept", accept_content_type)

        if body is schemas.unset:
            raise exceptions.ApiValueError(
                "The required body parameter has an invalid value of: unset. Set a valid value instead"
            )
        _fields = None
        _body = None
        serialized_data = request_body_any_type.serialize(body, content_type)
        _headers.add("Content-Type", content_type)
        if "fields" in serialized_data:
            _fields = serialized_data["fields"]
        elif "body" in serialized_data:
            _body = serialized_data["body"]
        response = self.api_client.call_api(
            resource_path=used_path,
            method="post".upper(),
            headers=_headers,
            fields=_fields,
            body=_body,
            auth_settings=_auth,
            stream=stream,
            timeout=timeout,
        )

        if skip_deserialization:
            api_response = api_client.ApiResponseWithoutDeserialization(
                response=response
            )
        else:
            response_for_status = _status_code_to_response.get(str(response.status))
            if response_for_status:
                api_response = response_for_status.deserialize(
                    response, self.api_client.configuration
                )
            else:
                api_response = api_client.ApiResponseWithoutDeserialization(
                    response=response
                )

        if not 200 <= response.status <= 299:
            raise exceptions.ApiException(
                status=response.status,
                reason=response.reason,
                api_response=api_response,
            )

        return api_response

class TestCasePost(BaseApi):
    # this class is used by api classes that refer to endpoints with operationId fn names

    @typing.overload
    def test_case_post(
        self,
        body: typing.Union[
            SchemaForRequestBodyApplicationJson,
            dict,
            frozendict.frozendict,
            str,
            date,
            datetime,
            uuid.UUID,
            int,
            float,
            decimal.Decimal,
            bool,
            None,
            list,
            tuple,
            bytes,
            io.FileIO,
            io.BufferedReader,
        ],
        content_type: typing_extensions.Literal["application/json"] = ...,
        accept_content_types: typing.Tuple[str] = _all_accept_content_types,
        stream: bool = False,
        timeout: typing.Optional[typing.Union[int, typing.Tuple]] = None,
        skip_deserialization: typing_extensions.Literal[False] = ...,
    ) -> typing.Union[ApiResponseFor200,]: ...
    @typing.overload
    def test_case_post(
        self,
        body: typing.Union[
            SchemaForRequestBodyApplicationJson,
            dict,
            frozendict.frozendict,
            str,
            date,
            datetime,
            uuid.UUID,
            int,
            float,
            decimal.Decimal,
            bool,
            None,
            list,
            tuple,
            bytes,
            io.FileIO,
            io.BufferedReader,
        ],
        content_type: str = ...,
        accept_content_types: typing.Tuple[str] = _all_accept_content_types,
        stream: bool = False,
        timeout: typing.Optional[typing.Union[int, typing.Tuple]] = None,
        skip_deserialization: typing_extensions.Literal[False] = ...,
    ) -> typing.Union[ApiResponseFor200,]: ...
    @typing.overload
    def test_case_post(
        self,
        body: typing.Union[
            SchemaForRequestBodyApplicationJson,
            dict,
            frozendict.frozendict,
            str,
            date,
            datetime,
            uuid.UUID,
            int,
            float,
            decimal.Decimal,
            bool,
            None,
            list,
            tuple,
            bytes,
            io.FileIO,
            io.BufferedReader,
        ],
        skip_deserialization: typing_extensions.Literal[True],
        content_type: str = ...,
        accept_content_types: typing.Tuple[str] = _all_accept_content_types,
        stream: bool = False,
        timeout: typing.Optional[typing.Union[int, typing.Tuple]] = None,
    ) -> api_client.ApiResponseWithoutDeserialization: ...
    @typing.overload
    def test_case_post(
        self,
        body: typing.Union[
            SchemaForRequestBodyApplicationJson,
            dict,
            frozendict.frozendict,
            str,
            date,
            datetime,
            uuid.UUID,
            int,
            float,
            decimal.Decimal,
            bool,
            None,
            list,
            tuple,
            bytes,
            io.FileIO,
            io.BufferedReader,
        ],
        content_type: str = ...,
        accept_content_types: typing.Tuple[str] = _all_accept_content_types,
        stream: bool = False,
        timeout: typing.Optional[typing.Union[int, typing.Tuple]] = None,
        skip_deserialization: bool = ...,
    ) -> typing.Union[
        ApiResponseFor200,
        api_client.ApiResponseWithoutDeserialization,
    ]: ...
    def test_case_post(
        self,
        body: typing.Union[
            SchemaForRequestBodyApplicationJson,
            dict,
            frozendict.frozendict,
            str,
            date,
            datetime,
            uuid.UUID,
            int,
            float,
            decimal.Decimal,
            bool,
            None,
            list,
            tuple,
            bytes,
            io.FileIO,
            io.BufferedReader,
        ],
        content_type: str = "application/json",
        accept_content_types: typing.Tuple[str] = _all_accept_content_types,
        stream: bool = False,
        timeout: typing.Optional[typing.Union[int, typing.Tuple]] = None,
        skip_deserialization: bool = False,
    ):
        return self._test_case_post_oapg(
            body=body,
            content_type=content_type,
            accept_content_types=accept_content_types,
            stream=stream,
            timeout=timeout,
            skip_deserialization=skip_deserialization,
        )

class ApiForpost(BaseApi):
    # this class is used by api classes that refer to endpoints by path and http method names

    @typing.overload
    def post(
        self,
        body: typing.Union[
            SchemaForRequestBodyApplicationJson,
            dict,
            frozendict.frozendict,
            str,
            date,
            datetime,
            uuid.UUID,
            int,
            float,
            decimal.Decimal,
            bool,
            None,
            list,
            tuple,
            bytes,
            io.FileIO,
            io.BufferedReader,
        ],
        content_type: typing_extensions.Literal["application/json"] = ...,
        accept_content_types: typing.Tuple[str] = _all_accept_content_types,
        stream: bool = False,
        timeout: typing.Optional[typing.Union[int, typing.Tuple]] = None,
        skip_deserialization: typing_extensions.Literal[False] = ...,
    ) -> typing.Union[ApiResponseFor200,]: ...
    @typing.overload
    def post(
        self,
        body: typing.Union[
            SchemaForRequestBodyApplicationJson,
            dict,
            frozendict.frozendict,
            str,
            date,
            datetime,
            uuid.UUID,
            int,
            float,
            decimal.Decimal,
            bool,
            None,
            list,
            tuple,
            bytes,
            io.FileIO,
            io.BufferedReader,
        ],
        content_type: str = ...,
        accept_content_types: typing.Tuple[str] = _all_accept_content_types,
        stream: bool = False,
        timeout: typing.Optional[typing.Union[int, typing.Tuple]] = None,
        skip_deserialization: typing_extensions.Literal[False] = ...,
    ) -> typing.Union[ApiResponseFor200,]: ...
    @typing.overload
    def post(
        self,
        body: typing.Union[
            SchemaForRequestBodyApplicationJson,
            dict,
            frozendict.frozendict,
            str,
            date,
            datetime,
            uuid.UUID,
            int,
            float,
            decimal.Decimal,
            bool,
            None,
            list,
            tuple,
            bytes,
            io.FileIO,
            io.BufferedReader,
        ],
        skip_deserialization: typing_extensions.Literal[True],
        content_type: str = ...,
        accept_content_types: typing.Tuple[str] = _all_accept_content_types,
        stream: bool = False,
        timeout: typing.Optional[typing.Union[int, typing.Tuple]] = None,
    ) -> api_client.ApiResponseWithoutDeserialization: ...
    @typing.overload
    def post(
        self,
        body: typing.Union[
            SchemaForRequestBodyApplicationJson,
            dict,
            frozendict.frozendict,
            str,
            date,
            datetime,
            uuid.UUID,
            int,
            float,
            decimal.Decimal,
            bool,
            None,
            list,
            tuple,
            bytes,
            io.FileIO,
            io.BufferedReader,
        ],
        content_type: str = ...,
        accept_content_types: typing.Tuple[str] = _all_accept_content_types,
        stream: bool = False,
        timeout: typing.Optional[typing.Union[int, typing.Tuple]] = None,
        skip_deserialization: bool = ...,
    ) -> typing.Union[
        ApiResponseFor200,
        api_client.ApiResponseWithoutDeserialization,
    ]: ...
    def post(
        self,
        body: typing.Union[
            SchemaForRequestBodyApplicationJson,
            dict,
            frozendict.frozendict,
            str,
            date,
            datetime,
            uuid.UUID,
            int,
            float,
            decimal.Decimal,
            bool,
            None,
            list,
            tuple,
            bytes,
            io.FileIO,
            io.BufferedReader,
        ],
        content_type: str = "application/json",
        accept_content_types: typing.Tuple[str] = _all_accept_content_types,
        stream: bool = False,
        timeout: typing.Optional[typing.Union[int, typing.Tuple]] = None,
        skip_deserialization: bool = False,
    ):
        return self._test_case_post_oapg(
            body=body,
            content_type=content_type,
            accept_content_types=accept_content_types,
            stream=stream,
            timeout=timeout,
            skip_deserialization=skip_deserialization,
        )
