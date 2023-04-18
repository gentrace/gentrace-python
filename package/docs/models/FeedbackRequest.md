# gentrace.model.feedback_request.FeedbackRequest

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  |  | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**score** | decimal.Decimal, int, float,  | decimal.Decimal,  |  | value must be a 32 bit float
**pipelineRunId** | str, uuid.UUID,  | str,  |  | value must be a uuid
**recordedTime** | str, datetime,  | str,  |  | value must conform to RFC-3339 date-time
**details** | None, str,  | NoneClass, str,  |  | [optional] 

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

