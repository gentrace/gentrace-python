# gentrace.model.pipeline_v2.PipelineV2

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  |  | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**organizationId** | str,  | str,  | The ID of the organization that owns the pipeline | 
**archivedAt** | decimal.Decimal, int,  | decimal.Decimal,  | Timestamp in seconds since the UNIX epoch. Can be transformed into a Date object. | value must be a 64 bit integer
**createdAt** | decimal.Decimal, int,  | decimal.Decimal,  | Timestamp in seconds since the UNIX epoch. Can be transformed into a Date object. | value must be a 64 bit integer
**privateUserEmail** | None, str,  | NoneClass, str,  | If null, this is a team pipeline. If not null, this is a private pipeline for the specified email. | 
**id** | str, uuid.UUID,  | str,  | The ID of the pipeline | value must be a uuid
**branch** | None, str,  | NoneClass, str,  | The branch that the pipeline is associated with | 
**privateMemberId** | None, str,  | NoneClass, str,  | If null, this is a team pipeline. If not null, this is a private pipeline for the specified member ID. | 
**slug** | str,  | str,  | The slug of the pipeline | 
**[labels](#labels)** | list, tuple,  | tuple,  | The labels attached to the pipeline | 
**updatedAt** | decimal.Decimal, int,  | decimal.Decimal,  | Timestamp in seconds since the UNIX epoch. Can be transformed into a Date object. | value must be a 64 bit integer
**displayName** | None, str,  | NoneClass, str,  | The name of the pipeline | [optional] 
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

