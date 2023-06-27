# gentrace.model.test_case.TestCase

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  |  | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**createdAt** | str, datetime,  | str,  | The date and time when the test case was created | value must conform to RFC-3339 date-time
**[inputs](#inputs)** | dict, frozendict.frozendict,  | frozendict.frozendict,  | The input data for the test case as a JSON object | 
**name** | str,  | str,  | The name of the test case | 
**setId** | str, uuid.UUID,  | str,  | The ID of the test set that the test case belongs to | value must be a uuid
**id** | str, uuid.UUID,  | str,  | The ID of the test case | value must be a uuid
**updatedAt** | str, datetime,  | str,  | The date and time when the test case was last updated | value must conform to RFC-3339 date-time
**archivedAt** | None, str, datetime,  | NoneClass, str,  | The date and time when the test case was archived, can be null if the test case has not been archived | [optional] value must conform to RFC-3339 date-time
**expected** | None, str,  | NoneClass, str,  | The expected output for the test case | [optional] 
**[expectedSteps](#expectedSteps)** | list, tuple, None,  | tuple, NoneClass,  |  | [optional] 
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

# inputs

The input data for the test case as a JSON object

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  | The input data for the test case as a JSON object | 

# expectedSteps

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple, None,  | tuple, NoneClass,  |  | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
[items](#items) | dict, frozendict.frozendict,  | frozendict.frozendict,  |  | 

# items

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  |  | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**output** | str,  | str,  | The output of the step | 
**key** | str,  | str,  | The key of the step | 
**[inputs](#inputs)** | dict, frozendict.frozendict, None,  | frozendict.frozendict, NoneClass,  | The inputs of the step | [optional] 
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

# inputs

The inputs of the step

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict, None,  | frozendict.frozendict, NoneClass,  | The inputs of the step | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**any_string_name** | str,  | str,  | any string name can be used but the value must be the correct type | [optional] 

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

