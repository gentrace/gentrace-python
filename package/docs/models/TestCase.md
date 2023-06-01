# gentrace.model.test_case.TestCase

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  |  | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**createdAt** | str, datetime,  | str,  | The date and time when the test case was created | value must conform to RFC-3339 date-time
**[inputs](#inputs)** | dict, frozendict.frozendict,  | frozendict.frozendict,  | The input data for the test case | 
**name** | str,  | str,  | The name of the test case | 
**setId** | str, uuid.UUID,  | str,  | The ID of the test set that the test case belongs to | value must be a uuid
**id** | str, uuid.UUID,  | str,  | The ID of the test case | value must be a uuid
**updatedAt** | str, datetime,  | str,  | The date and time when the test case was last updated | value must conform to RFC-3339 date-time
**archivedAt** | str, datetime,  | str,  | The date and time when the test case was archived | [optional] value must conform to RFC-3339 date-time
**expected** | str,  | str,  | The expected output for the test case | [optional] 
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

# inputs

The input data for the test case

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  | The input data for the test case | 

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

