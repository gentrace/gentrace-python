# gentrace.model.feedback_v2.FeedbackV2

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  |  | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**score** | decimal.Decimal, int, float,  | decimal.Decimal,  | The score of the feedback, ranging from 0 to 1 | value must be a 64 bit float
**pipelineRunId** | str, uuid.UUID,  | str,  | The unique identifier for the pipeline run | value must be a uuid
**id** | str, uuid.UUID,  | str,  | The unique identifier for the feedback | value must be a uuid
**recordedTime** | decimal.Decimal, int, float,  | decimal.Decimal,  | Timestamp in seconds since the UNIX epoch. Can be transformed into a Date object. | value must be a 32 bit float
**details** | None, str,  | NoneClass, str,  | Optional details about the feedback | [optional] 
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

