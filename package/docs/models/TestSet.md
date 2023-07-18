# gentrace.model.test_set.TestSet

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  |  | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**organizationId** | str,  | str,  | The ID of the organization that owns the test set | 
**createdAt** | str, datetime,  | str,  | The date and time when the test set was created | value must conform to RFC-3339 date-time
**[cases](#cases)** | list, tuple,  | tuple,  | The array of test cases that belong to the test set | 
**name** | str,  | str,  | The name of the test set | 
**id** | str, uuid.UUID,  | str,  | The ID of the test set | value must be a uuid
**[labels](#labels)** | list, tuple,  | tuple,  | The labels attached to the test set | 
**updatedAt** | str, datetime,  | str,  | The date and time when the test set was last updated | value must conform to RFC-3339 date-time
**archivedAt** | None, str, datetime,  | NoneClass, str,  | The date and time when the test set was archived, can be null if the test set has not been archived | [optional] value must conform to RFC-3339 date-time
**branch** | None, str,  | NoneClass, str,  | The branch that the test set is associated with | [optional] 
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

# cases

The array of test cases that belong to the test set

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  | The array of test cases that belong to the test set | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
[**TestCase**](TestCase.md) | [**TestCase**](TestCase.md) | [**TestCase**](TestCase.md) |  | 

# labels

The labels attached to the test set

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  | The labels attached to the test set | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
items | str,  | str,  |  | 

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

