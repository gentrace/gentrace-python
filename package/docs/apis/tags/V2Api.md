<a name="__pageTop"></a>
# gentrace.apis.tags.v2_api.V2Api

All URIs are relative to *https://gentrace.ai/api*

Method | HTTP request | Description
------------- | ------------- | -------------
[**v2_evaluations_bulk_post**](#v2_evaluations_bulk_post) | **post** /v2/evaluations/bulk | Bulk create evaluations
[**v2_feedback_id_get**](#v2_feedback_id_get) | **get** /v2/feedback/{id} | Get feedback
[**v2_feedback_id_patch**](#v2_feedback_id_patch) | **patch** /v2/feedback/{id} | Update feedback
[**v2_feedback_post**](#v2_feedback_post) | **post** /v2/feedback | Create feedback
[**v2_folders_get**](#v2_folders_get) | **get** /v2/folders | Get folders
[**v2_folders_id_get**](#v2_folders_id_get) | **get** /v2/folders/{id} | Get a folder
[**v2_pipelines_get**](#v2_pipelines_get) | **get** /v2/pipelines | Get pipelines
[**v2_test_cases_get**](#v2_test_cases_get) | **get** /v2/test-cases | Get test cases
[**v2_test_cases_id_get**](#v2_test_cases_id_get) | **get** /v2/test-cases/{id} | Get a test case
[**v2_test_results_get**](#v2_test_results_get) | **get** /v2/test-results | Get test results

# **v2_evaluations_bulk_post**
<a name="v2_evaluations_bulk_post"></a>
> {str: (bool, date, datetime, dict, float, int, list, str, none_type)} v2_evaluations_bulk_post(any_type)

Bulk create evaluations

### Example

* Bearer Authentication (bearerAuth):
```python
import gentrace
from gentrace.apis.tags import v2_api
from gentrace.model.create_evaluation_v2 import CreateEvaluationV2
from pprint import pprint
# Defining the host is optional and defaults to https://gentrace.ai/api
# See configuration.py for a list of all supported configuration parameters.
configuration = gentrace.Configuration(
    host = "https://gentrace.ai/api"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization: bearerAuth
configuration = gentrace.Configuration(
    access_token = 'YOUR_BEARER_TOKEN'
)
# Enter a context with an instance of the API client
with gentrace.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = v2_api.V2Api(api_client)

    # example passing only required values which don't have defaults set
    body = dict(
        data=[
            CreateEvaluationV2(
                note="note_example",
                evaluator_id="evaluator_id_example",
                run_id="run_id_example",
                eval_label="eval_label_example",
                eval_value=3.14,
            )
        ],
    )
    try:
        # Bulk create evaluations
        api_response = api_instance.v2_evaluations_bulk_post(
            body=body,
        )
        pprint(api_response)
    except gentrace.ApiException as e:
        print("Exception when calling V2Api->v2_evaluations_bulk_post: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
body | typing.Union[SchemaForRequestBodyApplicationJson] | required |
content_type | str | optional, default is 'application/json' | Selects the schema and serialization of the request body
accept_content_types | typing.Tuple[str] | default is ('application/json', 'application/json; charset&#x3D;utf-8', ) | Tells the server the content type(s) that are accepted by the client
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### body

# SchemaForRequestBodyApplicationJson

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  |  | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**[data](#data)** | list, tuple,  | tuple,  |  | 
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

# data

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  |  | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
[**CreateEvaluationV2**]({{complexTypePrefix}}CreateEvaluationV2.md) | [**CreateEvaluationV2**]({{complexTypePrefix}}CreateEvaluationV2.md) | [**CreateEvaluationV2**]({{complexTypePrefix}}CreateEvaluationV2.md) |  | 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#v2_evaluations_bulk_post.ApiResponseFor200) | Evaluations created successfully
400 | [ApiResponseFor400](#v2_evaluations_bulk_post.ApiResponseFor400) | Bad request
500 | [ApiResponseFor500](#v2_evaluations_bulk_post.ApiResponseFor500) | Server error

#### v2_evaluations_bulk_post.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, SchemaFor200ResponseBodyApplicationJsonCharsetutf8, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJson

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  |  | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**count** | decimal.Decimal, int, float,  | decimal.Decimal,  |  | 
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

# SchemaFor200ResponseBodyApplicationJsonCharsetutf8

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  |  | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**count** | decimal.Decimal, int, float,  | decimal.Decimal,  |  | 
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

#### v2_evaluations_bulk_post.ApiResponseFor400
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | Unset | body was not defined |
headers | Unset | headers were not defined |

#### v2_evaluations_bulk_post.ApiResponseFor500
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | Unset | body was not defined |
headers | Unset | headers were not defined |

### Authorization

[bearerAuth](../../../README.md#bearerAuth)

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **v2_feedback_id_get**
<a name="v2_feedback_id_get"></a>
> FeedbackV2 v2_feedback_id_get(id)

Get feedback

### Example

* Bearer Authentication (bearerAuth):
```python
import gentrace
from gentrace.apis.tags import v2_api
from gentrace.model.feedback_v2 import FeedbackV2
from pprint import pprint
# Defining the host is optional and defaults to https://gentrace.ai/api
# See configuration.py for a list of all supported configuration parameters.
configuration = gentrace.Configuration(
    host = "https://gentrace.ai/api"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization: bearerAuth
configuration = gentrace.Configuration(
    access_token = 'YOUR_BEARER_TOKEN'
)
# Enter a context with an instance of the API client
with gentrace.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = v2_api.V2Api(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'id': "id_example",
    }
    try:
        # Get feedback
        api_response = api_instance.v2_feedback_id_get(
            path_params=path_params,
        )
        pprint(api_response)
    except gentrace.ApiException as e:
        print("Exception when calling V2Api->v2_feedback_id_get: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
path_params | RequestPathParams | |
accept_content_types | typing.Tuple[str] | default is ('application/json', 'application/json; charset&#x3D;utf-8', ) | Tells the server the content type(s) that are accepted by the client
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### path_params
#### RequestPathParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
id | IdSchema | | 

# IdSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str, uuid.UUID,  | str,  |  | value must be a uuid

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#v2_feedback_id_get.ApiResponseFor200) | Feedback retrieved successfully
404 | [ApiResponseFor404](#v2_feedback_id_get.ApiResponseFor404) | Feedback not found

#### v2_feedback_id_get.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, SchemaFor200ResponseBodyApplicationJsonCharsetutf8, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**FeedbackV2**](../../models/FeedbackV2.md) |  | 


# SchemaFor200ResponseBodyApplicationJsonCharsetutf8
Type | Description  | Notes
------------- | ------------- | -------------
[**FeedbackV2**](../../models/FeedbackV2.md) |  | 


#### v2_feedback_id_get.ApiResponseFor404
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | Unset | body was not defined |
headers | Unset | headers were not defined |

### Authorization

[bearerAuth](../../../README.md#bearerAuth)

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **v2_feedback_id_patch**
<a name="v2_feedback_id_patch"></a>
> FeedbackV2 v2_feedback_id_patch(idupdate_feedback_v2)

Update feedback

### Example

* Bearer Authentication (bearerAuth):
```python
import gentrace
from gentrace.apis.tags import v2_api
from gentrace.model.update_feedback_v2 import UpdateFeedbackV2
from gentrace.model.feedback_v2 import FeedbackV2
from pprint import pprint
# Defining the host is optional and defaults to https://gentrace.ai/api
# See configuration.py for a list of all supported configuration parameters.
configuration = gentrace.Configuration(
    host = "https://gentrace.ai/api"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization: bearerAuth
configuration = gentrace.Configuration(
    access_token = 'YOUR_BEARER_TOKEN'
)
# Enter a context with an instance of the API client
with gentrace.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = v2_api.V2Api(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'id': "id_example",
    }
    body = UpdateFeedbackV2(
        score=0,
        details="details_example",
    )
    try:
        # Update feedback
        api_response = api_instance.v2_feedback_id_patch(
            path_params=path_params,
            body=body,
        )
        pprint(api_response)
    except gentrace.ApiException as e:
        print("Exception when calling V2Api->v2_feedback_id_patch: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
body | typing.Union[SchemaForRequestBodyApplicationJson] | required |
path_params | RequestPathParams | |
content_type | str | optional, default is 'application/json' | Selects the schema and serialization of the request body
accept_content_types | typing.Tuple[str] | default is ('application/json', 'application/json; charset&#x3D;utf-8', ) | Tells the server the content type(s) that are accepted by the client
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### body

# SchemaForRequestBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**UpdateFeedbackV2**](../../models/UpdateFeedbackV2.md) |  | 


### path_params
#### RequestPathParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
id | IdSchema | | 

# IdSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str, uuid.UUID,  | str,  |  | value must be a uuid

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#v2_feedback_id_patch.ApiResponseFor200) | Feedback updated successfully
400 | [ApiResponseFor400](#v2_feedback_id_patch.ApiResponseFor400) | Bad request
500 | [ApiResponseFor500](#v2_feedback_id_patch.ApiResponseFor500) | Server error

#### v2_feedback_id_patch.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, SchemaFor200ResponseBodyApplicationJsonCharsetutf8, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**FeedbackV2**](../../models/FeedbackV2.md) |  | 


# SchemaFor200ResponseBodyApplicationJsonCharsetutf8
Type | Description  | Notes
------------- | ------------- | -------------
[**FeedbackV2**](../../models/FeedbackV2.md) |  | 


#### v2_feedback_id_patch.ApiResponseFor400
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | Unset | body was not defined |
headers | Unset | headers were not defined |

#### v2_feedback_id_patch.ApiResponseFor500
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | Unset | body was not defined |
headers | Unset | headers were not defined |

### Authorization

[bearerAuth](../../../README.md#bearerAuth)

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **v2_feedback_post**
<a name="v2_feedback_post"></a>
> FeedbackV2 v2_feedback_post(create_feedback_v2)

Create feedback

### Example

* Bearer Authentication (bearerAuth):
```python
import gentrace
from gentrace.apis.tags import v2_api
from gentrace.model.create_feedback_v2 import CreateFeedbackV2
from gentrace.model.feedback_v2 import FeedbackV2
from pprint import pprint
# Defining the host is optional and defaults to https://gentrace.ai/api
# See configuration.py for a list of all supported configuration parameters.
configuration = gentrace.Configuration(
    host = "https://gentrace.ai/api"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization: bearerAuth
configuration = gentrace.Configuration(
    access_token = 'YOUR_BEARER_TOKEN'
)
# Enter a context with an instance of the API client
with gentrace.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = v2_api.V2Api(api_client)

    # example passing only required values which don't have defaults set
    body = CreateFeedbackV2(
        pipeline_run_id="pipeline_run_id_example",
        recorded_time=3.14,
        score=0,
        details="details_example",
    )
    try:
        # Create feedback
        api_response = api_instance.v2_feedback_post(
            body=body,
        )
        pprint(api_response)
    except gentrace.ApiException as e:
        print("Exception when calling V2Api->v2_feedback_post: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
body | typing.Union[SchemaForRequestBodyApplicationJson] | required |
content_type | str | optional, default is 'application/json' | Selects the schema and serialization of the request body
accept_content_types | typing.Tuple[str] | default is ('application/json', 'application/json; charset&#x3D;utf-8', ) | Tells the server the content type(s) that are accepted by the client
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### body

# SchemaForRequestBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**CreateFeedbackV2**](../../models/CreateFeedbackV2.md) |  | 


### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#v2_feedback_post.ApiResponseFor200) | Feedback created successfully
400 | [ApiResponseFor400](#v2_feedback_post.ApiResponseFor400) | Bad request
500 | [ApiResponseFor500](#v2_feedback_post.ApiResponseFor500) | Server error

#### v2_feedback_post.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, SchemaFor200ResponseBodyApplicationJsonCharsetutf8, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**FeedbackV2**](../../models/FeedbackV2.md) |  | 


# SchemaFor200ResponseBodyApplicationJsonCharsetutf8
Type | Description  | Notes
------------- | ------------- | -------------
[**FeedbackV2**](../../models/FeedbackV2.md) |  | 


#### v2_feedback_post.ApiResponseFor400
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | Unset | body was not defined |
headers | Unset | headers were not defined |

#### v2_feedback_post.ApiResponseFor500
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | Unset | body was not defined |
headers | Unset | headers were not defined |

### Authorization

[bearerAuth](../../../README.md#bearerAuth)

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **v2_folders_get**
<a name="v2_folders_get"></a>
> {str: (bool, date, datetime, dict, float, int, list, str, none_type)} v2_folders_get()

Get folders

### Example

* Bearer Authentication (bearerAuth):
```python
import gentrace
from gentrace.apis.tags import v2_api
from gentrace.model.folder_v2 import FolderV2
from pprint import pprint
# Defining the host is optional and defaults to https://gentrace.ai/api
# See configuration.py for a list of all supported configuration parameters.
configuration = gentrace.Configuration(
    host = "https://gentrace.ai/api"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization: bearerAuth
configuration = gentrace.Configuration(
    access_token = 'YOUR_BEARER_TOKEN'
)
# Enter a context with an instance of the API client
with gentrace.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = v2_api.V2Api(api_client)

    # example passing only optional values
    query_params = {
        'parentFolderId': "parentFolderId_example",
    }
    try:
        # Get folders
        api_response = api_instance.v2_folders_get(
            query_params=query_params,
        )
        pprint(api_response)
    except gentrace.ApiException as e:
        print("Exception when calling V2Api->v2_folders_get: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
query_params | RequestQueryParams | |
accept_content_types | typing.Tuple[str] | default is ('application/json', 'application/json; charset&#x3D;utf-8', ) | Tells the server the content type(s) that are accepted by the client
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### query_params
#### RequestQueryParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
parentFolderId | ParentFolderIdSchema | | optional


# ParentFolderIdSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
None, str,  | NoneClass, str,  |  | 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#v2_folders_get.ApiResponseFor200) | Folders retrieved successfully

#### v2_folders_get.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, SchemaFor200ResponseBodyApplicationJsonCharsetutf8, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJson

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  |  | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**[data](#data)** | list, tuple,  | tuple,  |  | 
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

# data

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  |  | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
[**FolderV2**]({{complexTypePrefix}}FolderV2.md) | [**FolderV2**]({{complexTypePrefix}}FolderV2.md) | [**FolderV2**]({{complexTypePrefix}}FolderV2.md) |  | 

# SchemaFor200ResponseBodyApplicationJsonCharsetutf8

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  |  | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**[data](#data)** | list, tuple,  | tuple,  |  | 
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

# data

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  |  | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
[**FolderV2**]({{complexTypePrefix}}FolderV2.md) | [**FolderV2**]({{complexTypePrefix}}FolderV2.md) | [**FolderV2**]({{complexTypePrefix}}FolderV2.md) |  | 

### Authorization

[bearerAuth](../../../README.md#bearerAuth)

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **v2_folders_id_get**
<a name="v2_folders_id_get"></a>
> FolderV2 v2_folders_id_get(id)

Get a folder

### Example

* Bearer Authentication (bearerAuth):
```python
import gentrace
from gentrace.apis.tags import v2_api
from gentrace.model.folder_v2 import FolderV2
from pprint import pprint
# Defining the host is optional and defaults to https://gentrace.ai/api
# See configuration.py for a list of all supported configuration parameters.
configuration = gentrace.Configuration(
    host = "https://gentrace.ai/api"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization: bearerAuth
configuration = gentrace.Configuration(
    access_token = 'YOUR_BEARER_TOKEN'
)
# Enter a context with an instance of the API client
with gentrace.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = v2_api.V2Api(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'id': "id_example",
    }
    try:
        # Get a folder
        api_response = api_instance.v2_folders_id_get(
            path_params=path_params,
        )
        pprint(api_response)
    except gentrace.ApiException as e:
        print("Exception when calling V2Api->v2_folders_id_get: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
path_params | RequestPathParams | |
accept_content_types | typing.Tuple[str] | default is ('application/json', 'application/json; charset&#x3D;utf-8', ) | Tells the server the content type(s) that are accepted by the client
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### path_params
#### RequestPathParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
id | IdSchema | | 

# IdSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str, uuid.UUID,  | str,  |  | value must be a uuid

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#v2_folders_id_get.ApiResponseFor200) | Folder retrieved successfully
404 | [ApiResponseFor404](#v2_folders_id_get.ApiResponseFor404) | Folder not found

#### v2_folders_id_get.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, SchemaFor200ResponseBodyApplicationJsonCharsetutf8, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**FolderV2**](../../models/FolderV2.md) |  | 


# SchemaFor200ResponseBodyApplicationJsonCharsetutf8
Type | Description  | Notes
------------- | ------------- | -------------
[**FolderV2**](../../models/FolderV2.md) |  | 


#### v2_folders_id_get.ApiResponseFor404
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | Unset | body was not defined |
headers | Unset | headers were not defined |

### Authorization

[bearerAuth](../../../README.md#bearerAuth)

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **v2_pipelines_get**
<a name="v2_pipelines_get"></a>
> {str: (bool, date, datetime, dict, float, int, list, str, none_type)} v2_pipelines_get()

Get pipelines

### Example

* Bearer Authentication (bearerAuth):
```python
import gentrace
from gentrace.apis.tags import v2_api
from gentrace.model.searchable_string_input import SearchableStringInput
from gentrace.model.pipeline_v2 import PipelineV2
from pprint import pprint
# Defining the host is optional and defaults to https://gentrace.ai/api
# See configuration.py for a list of all supported configuration parameters.
configuration = gentrace.Configuration(
    host = "https://gentrace.ai/api"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization: bearerAuth
configuration = gentrace.Configuration(
    access_token = 'YOUR_BEARER_TOKEN'
)
# Enter a context with an instance of the API client
with gentrace.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = v2_api.V2Api(api_client)

    # example passing only optional values
    query_params = {
        'label': "label_example",
        'slug': SearchableStringInput(None),
        'folderId': "folderId_example",
    }
    try:
        # Get pipelines
        api_response = api_instance.v2_pipelines_get(
            query_params=query_params,
        )
        pprint(api_response)
    except gentrace.ApiException as e:
        print("Exception when calling V2Api->v2_pipelines_get: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
query_params | RequestQueryParams | |
accept_content_types | typing.Tuple[str] | default is ('application/json', 'application/json; charset&#x3D;utf-8', ) | Tells the server the content type(s) that are accepted by the client
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### query_params
#### RequestQueryParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
label | LabelSchema | | optional
slug | SlugSchema | | optional
folderId | FolderIdSchema | | optional


# LabelSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

# SlugSchema
Type | Description  | Notes
------------- | ------------- | -------------
[**SearchableStringInput**](../../models/SearchableStringInput.md) |  | 


# FolderIdSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
None, str,  | NoneClass, str,  |  | 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#v2_pipelines_get.ApiResponseFor200) | Pipelines retrieved successfully

#### v2_pipelines_get.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, SchemaFor200ResponseBodyApplicationJsonCharsetutf8, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJson

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  |  | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**[data](#data)** | list, tuple,  | tuple,  |  | 
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

# data

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  |  | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
[**PipelineV2**]({{complexTypePrefix}}PipelineV2.md) | [**PipelineV2**]({{complexTypePrefix}}PipelineV2.md) | [**PipelineV2**]({{complexTypePrefix}}PipelineV2.md) |  | 

# SchemaFor200ResponseBodyApplicationJsonCharsetutf8

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  |  | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**data** | dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, bool, None, list, tuple, bytes, io.FileIO, io.BufferedReader,  | frozendict.frozendict, str, decimal.Decimal, BoolClass, NoneClass, tuple, bytes, FileIO |  | 
**[pipelines](#pipelines)** | list, tuple,  | tuple,  |  | [optional] 
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

# pipelines

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  |  | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
[**PipelineV2**]({{complexTypePrefix}}PipelineV2.md) | [**PipelineV2**]({{complexTypePrefix}}PipelineV2.md) | [**PipelineV2**]({{complexTypePrefix}}PipelineV2.md) |  | 

### Authorization

[bearerAuth](../../../README.md#bearerAuth)

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **v2_test_cases_get**
<a name="v2_test_cases_get"></a>
> {str: (bool, date, datetime, dict, float, int, list, str, none_type)} v2_test_cases_get()

Get test cases

### Example

* Bearer Authentication (bearerAuth):
```python
import gentrace
from gentrace.apis.tags import v2_api
from gentrace.model.test_case_v2 import TestCaseV2
from pprint import pprint
# Defining the host is optional and defaults to https://gentrace.ai/api
# See configuration.py for a list of all supported configuration parameters.
configuration = gentrace.Configuration(
    host = "https://gentrace.ai/api"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization: bearerAuth
configuration = gentrace.Configuration(
    access_token = 'YOUR_BEARER_TOKEN'
)
# Enter a context with an instance of the API client
with gentrace.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = v2_api.V2Api(api_client)

    # example passing only optional values
    query_params = {
        'pipelineId': "pipelineId_example",
        'pipelineSlug': "pipelineSlug_example",
    }
    try:
        # Get test cases
        api_response = api_instance.v2_test_cases_get(
            query_params=query_params,
        )
        pprint(api_response)
    except gentrace.ApiException as e:
        print("Exception when calling V2Api->v2_test_cases_get: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
query_params | RequestQueryParams | |
accept_content_types | typing.Tuple[str] | default is ('application/json', 'application/json; charset&#x3D;utf-8', ) | Tells the server the content type(s) that are accepted by the client
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### query_params
#### RequestQueryParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
pipelineId | PipelineIdSchema | | optional
pipelineSlug | PipelineSlugSchema | | optional


# PipelineIdSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str, uuid.UUID,  | str,  |  | value must be a uuid

# PipelineSlugSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#v2_test_cases_get.ApiResponseFor200) | Test cases retrieved successfully

#### v2_test_cases_get.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, SchemaFor200ResponseBodyApplicationJsonCharsetutf8, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJson

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  |  | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**[data](#data)** | list, tuple,  | tuple,  |  | 
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

# data

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  |  | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
[**TestCaseV2**]({{complexTypePrefix}}TestCaseV2.md) | [**TestCaseV2**]({{complexTypePrefix}}TestCaseV2.md) | [**TestCaseV2**]({{complexTypePrefix}}TestCaseV2.md) |  | 

# SchemaFor200ResponseBodyApplicationJsonCharsetutf8

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  |  | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**[data](#data)** | list, tuple,  | tuple,  |  | 
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

# data

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  |  | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
[**TestCaseV2**]({{complexTypePrefix}}TestCaseV2.md) | [**TestCaseV2**]({{complexTypePrefix}}TestCaseV2.md) | [**TestCaseV2**]({{complexTypePrefix}}TestCaseV2.md) |  | 

### Authorization

[bearerAuth](../../../README.md#bearerAuth)

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **v2_test_cases_id_get**
<a name="v2_test_cases_id_get"></a>
> TestCaseV2 v2_test_cases_id_get(id)

Get a test case

### Example

* Bearer Authentication (bearerAuth):
```python
import gentrace
from gentrace.apis.tags import v2_api
from gentrace.model.test_case_v2 import TestCaseV2
from pprint import pprint
# Defining the host is optional and defaults to https://gentrace.ai/api
# See configuration.py for a list of all supported configuration parameters.
configuration = gentrace.Configuration(
    host = "https://gentrace.ai/api"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization: bearerAuth
configuration = gentrace.Configuration(
    access_token = 'YOUR_BEARER_TOKEN'
)
# Enter a context with an instance of the API client
with gentrace.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = v2_api.V2Api(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'id': "id_example",
    }
    try:
        # Get a test case
        api_response = api_instance.v2_test_cases_id_get(
            path_params=path_params,
        )
        pprint(api_response)
    except gentrace.ApiException as e:
        print("Exception when calling V2Api->v2_test_cases_id_get: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
path_params | RequestPathParams | |
accept_content_types | typing.Tuple[str] | default is ('application/json', 'application/json; charset&#x3D;utf-8', ) | Tells the server the content type(s) that are accepted by the client
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### path_params
#### RequestPathParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
id | IdSchema | | 

# IdSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str, uuid.UUID,  | str,  |  | value must be a uuid

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#v2_test_cases_id_get.ApiResponseFor200) | Test case retrieved successfully
404 | [ApiResponseFor404](#v2_test_cases_id_get.ApiResponseFor404) | Test case not found

#### v2_test_cases_id_get.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, SchemaFor200ResponseBodyApplicationJsonCharsetutf8, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**TestCaseV2**](../../models/TestCaseV2.md) |  | 


# SchemaFor200ResponseBodyApplicationJsonCharsetutf8
Type | Description  | Notes
------------- | ------------- | -------------
[**TestCaseV2**](../../models/TestCaseV2.md) |  | 


#### v2_test_cases_id_get.ApiResponseFor404
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | Unset | body was not defined |
headers | Unset | headers were not defined |

### Authorization

[bearerAuth](../../../README.md#bearerAuth)

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **v2_test_results_get**
<a name="v2_test_results_get"></a>
> {str: (bool, date, datetime, dict, float, int, list, str, none_type)} v2_test_results_get()

Get test results

### Example

* Bearer Authentication (bearerAuth):
```python
import gentrace
from gentrace.apis.tags import v2_api
from gentrace.model.test_result_v2 import TestResultV2
from gentrace.model.searchable_unix_seconds_input import SearchableUnixSecondsInput
from gentrace.model.filterable_metadata_input import FilterableMetadataInput
from pprint import pprint
# Defining the host is optional and defaults to https://gentrace.ai/api
# See configuration.py for a list of all supported configuration parameters.
configuration = gentrace.Configuration(
    host = "https://gentrace.ai/api"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization: bearerAuth
configuration = gentrace.Configuration(
    access_token = 'YOUR_BEARER_TOKEN'
)
# Enter a context with an instance of the API client
with gentrace.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = v2_api.V2Api(api_client)

    # example passing only optional values
    query_params = {
        'pipelineId': "pipelineId_example",
        'pipelineSlug': "pipelineSlug_example",
        'createdAt': SearchableUnixSecondsInput(None),
        'metadata': FilterableMetadataInput(
        key=dict(
            exists=True,
            contains="contains_example",
            equals=None,
            gt=None,
            gte=None,
            lt=None,
            lte=None,
        ),
    ),
    }
    try:
        # Get test results
        api_response = api_instance.v2_test_results_get(
            query_params=query_params,
        )
        pprint(api_response)
    except gentrace.ApiException as e:
        print("Exception when calling V2Api->v2_test_results_get: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
query_params | RequestQueryParams | |
accept_content_types | typing.Tuple[str] | default is ('application/json', 'application/json; charset&#x3D;utf-8', ) | Tells the server the content type(s) that are accepted by the client
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### query_params
#### RequestQueryParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
pipelineId | PipelineIdSchema | | optional
pipelineSlug | PipelineSlugSchema | | optional
createdAt | CreatedAtSchema | | optional
metadata | MetadataSchema | | optional


# PipelineIdSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

# PipelineSlugSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

# CreatedAtSchema
Type | Description  | Notes
------------- | ------------- | -------------
[**SearchableUnixSecondsInput**](../../models/SearchableUnixSecondsInput.md) |  | 


# MetadataSchema
Type | Description  | Notes
------------- | ------------- | -------------
[**FilterableMetadataInput**](../../models/FilterableMetadataInput.md) |  | 


### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#v2_test_results_get.ApiResponseFor200) | Successful response

#### v2_test_results_get.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, SchemaFor200ResponseBodyApplicationJsonCharsetutf8, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJson

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  |  | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**[data](#data)** | list, tuple,  | tuple,  |  | 
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

# data

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  |  | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
[**TestResultV2**]({{complexTypePrefix}}TestResultV2.md) | [**TestResultV2**]({{complexTypePrefix}}TestResultV2.md) | [**TestResultV2**]({{complexTypePrefix}}TestResultV2.md) |  | 

# SchemaFor200ResponseBodyApplicationJsonCharsetutf8

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  |  | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**[data](#data)** | list, tuple,  | tuple,  |  | 
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

# data

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  |  | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
[**TestResultV2**]({{complexTypePrefix}}TestResultV2.md) | [**TestResultV2**]({{complexTypePrefix}}TestResultV2.md) | [**TestResultV2**]({{complexTypePrefix}}TestResultV2.md) |  | 

### Authorization

[bearerAuth](../../../README.md#bearerAuth)

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

