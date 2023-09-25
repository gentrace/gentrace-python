# gentrace.model.test_evaluator.TestEvaluator

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  |  | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**createdAt** | str,  | str,  |  | 
**valueType** | str,  | str,  |  | must be one of ["ENUM", "PERCENTAGE", ] 
**name** | str,  | str,  |  | 
**[options](#options)** | dict, frozendict.frozendict, None,  | frozendict.frozendict, NoneClass,  |  | 
**id** | str, uuid.UUID,  | str,  |  | value must be a uuid
**pipelineId** | str,  | str,  |  | 
**updatedAt** | str,  | str,  |  | 
**who** | str,  | str,  |  | must be one of ["AI", "HEURISTIC", "HUMAN", ] 
**archivedAt** | None, str,  | NoneClass, str,  |  | [optional] 
**icon** | None, str,  | NoneClass, str,  |  | [optional] 
**aiModel** | None, str,  | NoneClass, str,  |  | [optional] must be one of ["OPENAI_3_5", "OPENAI_4", ] 
**processorId** | None, str,  | NoneClass, str,  |  | [optional] 
**heuristicFn** | None, str,  | NoneClass, str,  |  | [optional] 
**aiPromptFormat** | None, str,  | NoneClass, str,  |  | [optional] 
**humanPrompt** | None, str,  | NoneClass, str,  |  | [optional] 
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

# options

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict, None,  | frozendict.frozendict, NoneClass,  |  | 

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

