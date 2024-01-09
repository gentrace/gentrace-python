# gentrace.model.create_evaluation_v2.CreateEvaluationV2

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  |  | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**runId** | str, uuid.UUID,  | str,  | The ID of the run. The evaluator and run must be in the same pipeline. | value must be a uuid
**evaluatorId** | str, uuid.UUID,  | str,  | The ID of the evaluator. The evaluator and run must be in the same pipeline. | value must be a uuid
**note** | str,  | str,  | Optionally add a note to the evaluation | [optional] 
**evalLabel** | str,  | str,  | If the evaluator output type is an enum, the label of the enum value. | [optional] 
**evalValue** | decimal.Decimal, int, float,  | decimal.Decimal,  | If the evaluator output type is a percentage, a number between 0 and 1 representing the percentage. | [optional] 
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

