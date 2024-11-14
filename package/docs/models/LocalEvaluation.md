# gentrace.model.local_evaluation.LocalEvaluation

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  |  | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**name** | str,  | str,  | The name of the local evaluation | 
**value** | decimal.Decimal, int, float,  | decimal.Decimal,  | The numeric value of the evaluation | 
**label** | None, str,  | NoneClass, str,  | Optional label for the evaluation | [optional] 
**debug** | [**LocalEvaluationDebug**](LocalEvaluationDebug.md) | [**LocalEvaluationDebug**](LocalEvaluationDebug.md) |  | [optional] 
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)
