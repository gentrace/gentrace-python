# gentrace.model.evaluation_v3.EvaluationV3

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  |  | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**createdAt** | decimal.Decimal, int, float,  | decimal.Decimal,  | Timestamp in seconds since the UNIX epoch. Can be transformed into a Date object. | value must be a 32 bit float
**note** | str,  | str,  | Additional notes for the evaluation | 
**evalLabel** | None, str,  | NoneClass, str,  | The label of the evaluation | 
**name** | None, str,  | NoneClass, str,  | The name of the evaluation | 
**isFiltered** | bool,  | BoolClass,  | Indicates if the evaluation is filtered | 
**id** | str, uuid.UUID,  | str,  | The ID of the evaluation | value must be a uuid
**runId** | str, uuid.UUID,  | str,  | The ID of the run | value must be a uuid
**isPending** | bool,  | BoolClass,  | Indicates if the evaluation is pending | 
**evaluatorId** | None, str, uuid.UUID,  | NoneClass, str,  | The ID of the evaluator | value must be a uuid
**evalValue** | None, decimal.Decimal, int, float,  | NoneClass, decimal.Decimal,  | The value of the evaluation | 
**updatedAt** | decimal.Decimal, int, float,  | decimal.Decimal,  | Timestamp in seconds since the UNIX epoch. Can be transformed into a Date object. | value must be a 32 bit float
**[debug](#debug)** | dict, frozendict.frozendict, None,  | frozendict.frozendict, NoneClass,  | Debug information for the evaluation | [optional] 
**comparisonRunId** | None, str, uuid.UUID,  | NoneClass, str,  | The ID of the comparison run, if applicable | [optional] value must be a uuid
**manualCreatedByEmail** | None, str,  | NoneClass, str,  | The email of the user who manually created the evaluation, if applicable | [optional] 
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

# debug

Debug information for the evaluation

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict, None,  | frozendict.frozendict, NoneClass,  | Debug information for the evaluation | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, bool, None, list, tuple, bytes, io.FileIO, io.BufferedReader,  | frozendict.frozendict, str, decimal.Decimal, BoolClass, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

