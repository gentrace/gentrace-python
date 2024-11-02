# gentrace.model.run_v2.RunV2

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  |  | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**[stepRuns](#stepRuns)** | list, tuple,  | tuple,  |  | 
**id** | str, uuid.UUID,  | str,  | The ID of the run | value must be a uuid
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

# stepRuns

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  |  | 

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
**[outputs](#outputs)** | dict, frozendict.frozendict,  | frozendict.frozendict,  | The outputs of the run | 
**invocation** | str,  | str,  | The name of the method being invoked | 
**cost** | decimal.Decimal, int, float,  | decimal.Decimal,  | The cost of the run in USD | 
**[modelParams](#modelParams)** | dict, frozendict.frozendict,  | frozendict.frozendict,  | The parameters used by the model | 
**[inputs](#inputs)** | dict, frozendict.frozendict,  | frozendict.frozendict,  | The inputs of the run | 
**stepId** | str, uuid.UUID,  | str,  | The ID of the step | value must be a uuid
**startTime** | decimal.Decimal, int, float,  | decimal.Decimal,  | Timestamp in seconds since the UNIX epoch. Can be transformed into a Date object. | value must be a 32 bit float
**endTime** | decimal.Decimal, int, float,  | decimal.Decimal,  | Timestamp in seconds since the UNIX epoch. Can be transformed into a Date object. | value must be a 32 bit float
**providerName** | str,  | str,  | The name of the provider | 
**stepRunId** | str, uuid.UUID,  | str,  | The ID of the step run | value must be a uuid
**elapsedTime** | decimal.Decimal, int,  | decimal.Decimal,  | The milliseconds to complete the run | 
**order** | decimal.Decimal, int,  | decimal.Decimal,  | The order of the step run. The last step has the highest \&quot;order\&quot; number. | 
**[metadata](#metadata)** | dict, frozendict.frozendict, None,  | frozendict.frozendict, NoneClass,  |  | [optional] 
**error** | None, str,  | NoneClass, str,  |  | [optional] 
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

# modelParams

The parameters used by the model

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  | The parameters used by the model | 

# inputs

The inputs of the run

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  | The inputs of the run | 

# outputs

The outputs of the run

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  | The outputs of the run | 

# metadata

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict, None,  | frozendict.frozendict, NoneClass,  |  | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**any_string_name** | [**MetadataValueObject**](MetadataValueObject.md) | [**MetadataValueObject**](MetadataValueObject.md) | any string name can be used but the value must be the correct type | [optional] 

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

