# gentrace.model.test_case_v2.TestCaseV2

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  |  | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**archivedAt** | decimal.Decimal, int,  | decimal.Decimal,  | Timestamp in seconds since the UNIX epoch. Can be transformed into a Date object. | value must be a 64 bit integer
**createdAt** | decimal.Decimal, int,  | decimal.Decimal,  | Timestamp in seconds since the UNIX epoch. Can be transformed into a Date object. | value must be a 64 bit integer
**[inputs](#inputs)** | dict, frozendict.frozendict,  | frozendict.frozendict,  | The input data for the test case as a JSON object | 
**name** | str,  | str,  | The name of the test case | 
**id** | str, uuid.UUID,  | str,  | The ID of the test case | value must be a uuid
**pipelineId** | str, uuid.UUID,  | str,  | The ID of the pipeline that the test case belongs to | value must be a uuid
**updatedAt** | decimal.Decimal, int,  | decimal.Decimal,  | Timestamp in seconds since the UNIX epoch. Can be transformed into a Date object. | value must be a 64 bit integer
**[expectedOutputs](#expectedOutputs)** | dict, frozendict.frozendict, None,  | frozendict.frozendict, NoneClass,  | The expected outputs for the test case | [optional] 
**setId** | str, uuid.UUID,  | str,  | The ID of the set (now pipeline) that the test case belongs to | [optional] value must be a uuid
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

# inputs

The input data for the test case as a JSON object

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  | The input data for the test case as a JSON object | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, bool, None, list, tuple, bytes, io.FileIO, io.BufferedReader,  | frozendict.frozendict, str, decimal.Decimal, BoolClass, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

# expectedOutputs

The expected outputs for the test case

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict, None,  | frozendict.frozendict, NoneClass,  | The expected outputs for the test case | 

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)
