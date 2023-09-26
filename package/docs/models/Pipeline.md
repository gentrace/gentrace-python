# gentrace.model.pipeline.Pipeline

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  |  | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**organizationId** | str,  | str,  | The ID of the organization that owns the pipeline | 
**createdAt** | str, datetime,  | str,  | The date and time when the pipeline was created | value must conform to RFC-3339 date-time
**id** | str, uuid.UUID,  | str,  | The ID of the pipeline | value must be a uuid
**slug** | str,  | str,  | The slug of the pipeline | 
**[labels](#labels)** | list, tuple,  | tuple,  | The labels attached to the pipeline | 
**updatedAt** | str, datetime,  | str,  | The date and time when the pipeline was last updated | value must conform to RFC-3339 date-time
**archivedAt** | None, str, datetime,  | NoneClass, str,  | The date and time when the pipeline was archived, can be null if the pipeline has not been archived | [optional] value must conform to RFC-3339 date-time
**displayName** | None, str,  | NoneClass, str,  | The name of the pipeline | [optional] 
**branch** | None, str,  | NoneClass, str,  | The branch that the pipeline is associated with | [optional] 
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

# labels

The labels attached to the pipeline

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  | The labels attached to the pipeline | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
items | str,  | str,  |  | 

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

