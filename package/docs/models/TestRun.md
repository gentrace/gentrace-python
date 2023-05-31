# gentrace.model.test_run.TestRun

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  |  | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**id** | str, uuid.UUID,  | str,  | The unique identifier for the test run. | [optional] value must be a uuid
**createdAt** | str, datetime,  | str,  | The date and time the test run was created. | [optional] value must conform to RFC-3339 date-time
**updatedAt** | str, datetime,  | str,  | The date and time the test run was last updated. | [optional] value must conform to RFC-3339 date-time
**setId** | str, uuid.UUID,  | str,  | The unique identifier for the test set associated with the test run. | [optional] value must be a uuid
**source** | str,  | str,  | The source of the test run. | [optional] 
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

