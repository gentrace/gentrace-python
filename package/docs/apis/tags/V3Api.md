<a name="__pageTop"></a>
# gentrace.apis.tags.v3_api.V3Api

All URIs are relative to *https://gentrace.ai/api*

Method | HTTP request | Description
------------- | ------------- | -------------
[**v3_evaluations_get**](#v3_evaluations_get) | **get** /v3/evaluations | Get evaluations

# **v3_evaluations_get**
<a name="v3_evaluations_get"></a>
> {str: (bool, date, datetime, dict, float, int, list, str, none_type)} v3_evaluations_get(result_id)

Get evaluations

### Example

* Bearer Authentication (bearerAuth):
```python
import gentrace
from gentrace.apis.tags import v3_api
from gentrace.model.evaluation_v3 import EvaluationV3
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
    api_instance = v3_api.V3Api(api_client)

    # example passing only required values which don't have defaults set
    query_params = {
        'resultId': "resultId_example",
    }
    try:
        # Get evaluations
        api_response = api_instance.v3_evaluations_get(
            query_params=query_params,
        )
        pprint(api_response)
    except gentrace.ApiException as e:
        print("Exception when calling V3Api->v3_evaluations_get: %s\n" % e)
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
resultId | ResultIdSchema | | 


# ResultIdSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str, uuid.UUID,  | str,  |  | value must be a uuid

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#v3_evaluations_get.ApiResponseFor200) | Evaluations retrieved successfully
400 | [ApiResponseFor400](#v3_evaluations_get.ApiResponseFor400) | Bad request
404 | [ApiResponseFor404](#v3_evaluations_get.ApiResponseFor404) | Result not found
500 | [ApiResponseFor500](#v3_evaluations_get.ApiResponseFor500) | Server error

#### v3_evaluations_get.ApiResponseFor200
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
**[data](#data)** | list, tuple,  | tuple,  |  | [optional] 
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

# data

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  |  | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
[**EvaluationV3**]({{complexTypePrefix}}EvaluationV3.md) | [**EvaluationV3**]({{complexTypePrefix}}EvaluationV3.md) | [**EvaluationV3**]({{complexTypePrefix}}EvaluationV3.md) |  | 

# SchemaFor200ResponseBodyApplicationJsonCharsetutf8

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  |  | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**[data](#data)** | list, tuple,  | tuple,  |  | [optional] 
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

# data

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  |  | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
[**EvaluationV3**]({{complexTypePrefix}}EvaluationV3.md) | [**EvaluationV3**]({{complexTypePrefix}}EvaluationV3.md) | [**EvaluationV3**]({{complexTypePrefix}}EvaluationV3.md) |  | 

#### v3_evaluations_get.ApiResponseFor400
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | Unset | body was not defined |
headers | Unset | headers were not defined |

#### v3_evaluations_get.ApiResponseFor404
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | Unset | body was not defined |
headers | Unset | headers were not defined |

#### v3_evaluations_get.ApiResponseFor500
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | Unset | body was not defined |
headers | Unset | headers were not defined |

### Authorization

[bearerAuth](../../../README.md#bearerAuth)

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

