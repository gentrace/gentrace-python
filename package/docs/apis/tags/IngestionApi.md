<a name="__pageTop"></a>
# gentrace.apis.tags.ingestion_api.IngestionApi

All URIs are relative to *https://gentrace.ai/api/v1*

Method | HTTP request | Description
------------- | ------------- | -------------
[**pipeline_run_post**](#pipeline_run_post) | **post** /pipeline-run | Create a pipeline run

# **pipeline_run_post**
<a name="pipeline_run_post"></a>
> PipelineRunResponse pipeline_run_post(pipeline_run_request)

Create a pipeline run

### Example

* Bearer Authentication (bearerAuth):
```python
import gentrace
from gentrace.apis.tags import ingestion_api
from gentrace.model.pipeline_run_response import PipelineRunResponse
from gentrace.model.pipeline_run_request import PipelineRunRequest
from pprint import pprint
# Defining the host is optional and defaults to https://gentrace.ai/api/v1
# See configuration.py for a list of all supported configuration parameters.
configuration = gentrace.Configuration(
    host = "https://gentrace.ai/api/v1"
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
    api_instance = ingestion_api.IngestionApi(api_client)

    # example passing only required values which don't have defaults set
    body = PipelineRunRequest(
        name="name_example",
        step_runs=[
            dict(
                provider=dict(
                    name="name_example",
                    invocation="invocation_example",
                    model_params=dict(),
                    inputs=dict(),
                    outputs=dict(),
                ),
                elapsed_time=1,
                start_time="1970-01-01T00:00:00.00Z",
                end_time="1970-01-01T00:00:00.00Z",
            )
        ],
    )
    try:
        # Create a pipeline run
        api_response = api_instance.pipeline_run_post(
            body=body,
        )
        pprint(api_response)
    except gentrace.ApiException as e:
        print("Exception when calling IngestionApi->pipeline_run_post: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
body | typing.Union[SchemaForRequestBodyApplicationJson] | required |
content_type | str | optional, default is 'application/json' | Selects the schema and serialization of the request body
accept_content_types | typing.Tuple[str] | default is ('application/json; charset&#x3D;utf-8', 'application/json', ) | Tells the server the content type(s) that are accepted by the client
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### body

# SchemaForRequestBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**PipelineRunRequest**](../../models/PipelineRunRequest.md) |  | 


### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#pipeline_run_post.ApiResponseFor200) | Stored pipeline run
400 | [ApiResponseFor400](#pipeline_run_post.ApiResponseFor400) | Bad request
500 | [ApiResponseFor500](#pipeline_run_post.ApiResponseFor500) | Internal server error

#### pipeline_run_post.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJsonCharsetutf8, SchemaFor200ResponseBodyApplicationJson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJsonCharsetutf8
Type | Description  | Notes
------------- | ------------- | -------------
[**PipelineRunResponse**](../../models/PipelineRunResponse.md) |  | 


# SchemaFor200ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**PipelineRunResponse**](../../models/PipelineRunResponse.md) |  | 


#### pipeline_run_post.ApiResponseFor400
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | Unset | body was not defined |
headers | Unset | headers were not defined |

#### pipeline_run_post.ApiResponseFor500
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | Unset | body was not defined |
headers | Unset | headers were not defined |

### Authorization

[bearerAuth](../../../README.md#bearerAuth)

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

