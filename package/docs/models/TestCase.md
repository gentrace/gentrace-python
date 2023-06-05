# gentrace.model.test_case.TestCase

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  |  | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**createdAt** | str, datetime,  | str,  | The date and time when the test case was created | value must conform to RFC-3339 date-time
**inputs** | str,  | str,  | The input data for the test case as a JSON string | 
**name** | str,  | str,  | The name of the test case | 
**setId** | str, uuid.UUID,  | str,  | The ID of the test set that the test case belongs to | value must be a uuid
**id** | str, uuid.UUID,  | str,  | The ID of the test case | value must be a uuid
**updatedAt** | str, datetime,  | str,  | The date and time when the test case was last updated | value must conform to RFC-3339 date-time
**archivedAt** | None, str, datetime,  | NoneClass, str,  | The date and time when the test case was archived, can be null if the test case has not been archived | [optional] value must conform to RFC-3339 date-time
**expected** | None, str,  | NoneClass, str,  | The expected output for the test case | [optional] 
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

