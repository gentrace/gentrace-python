# gentrace.model.test_run.TestRun

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  |  | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**createdAt** | str,  | str,  |  | 
**resultId** | str, uuid.UUID,  | str,  |  | value must be a uuid
**caseId** | str, uuid.UUID,  | str,  |  | value must be a uuid
**id** | str, uuid.UUID,  | str,  |  | value must be a uuid
**updatedAt** | str,  | str,  |  | 
**[path](#path)** | list, tuple, None,  | tuple, NoneClass,  |  | [optional] 
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

# path

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple, None,  | tuple, NoneClass,  |  | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
[**RunPathSection**](RunPathSection.md) | [**RunPathSection**](RunPathSection.md) | [**RunPathSection**](RunPathSection.md) |  | 

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

