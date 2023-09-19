# gentrace.model.update_test_case.UpdateTestCase

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  |  | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**id** | str, uuid.UUID,  | str,  | ID of the test case to update | value must be a uuid
**name** | None, str,  | NoneClass, str,  | Name of the test case | [optional] 
**[inputs](#inputs)** | dict, frozendict.frozendict, None,  | frozendict.frozendict, NoneClass,  | Inputs for the test case | [optional] 
**[expectedOutputs](#expectedOutputs)** | dict, frozendict.frozendict, None,  | frozendict.frozendict, NoneClass,  | Expected outputs for the test case | [optional] 
**archived** | None, bool,  | NoneClass, BoolClass,  | Archive status for the test case | [optional] 
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

# inputs

Inputs for the test case

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict, None,  | frozendict.frozendict, NoneClass,  | Inputs for the test case | 

# expectedOutputs

Expected outputs for the test case

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict, None,  | frozendict.frozendict, NoneClass,  | Expected outputs for the test case | 

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

