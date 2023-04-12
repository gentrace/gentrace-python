# gentrace.model.feedback_request.FeedbackRequest

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  |  | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**pipelineRunId** | str, uuid.UUID,  | str,  |  | value must be a uuid
**rating** | str,  | str,  |  | must be one of ["positive", "negative", "neutral", ] 
**recordedTime** | str, datetime,  | str,  |  | value must conform to RFC-3339 date-time
**details** | None, str,  | NoneClass, str,  |  | [optional] 

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

