# gentrace.model.evaluator_v2.EvaluatorV2

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  |  | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**createdAt** | decimal.Decimal, int, float,  | decimal.Decimal,  | Timestamp in seconds since the UNIX epoch. Can be transformed into a Date object. | value must be a 32 bit float
**valueType** | str,  | str,  | The scoring method used by the evaluator (such as \&quot;ENUM\&quot;, \&quot;PERCENTAGE\&quot;) | 
**name** | str,  | str,  | The name of the evaluator | 
**id** | str, uuid.UUID,  | str,  | The ID of the evaluator | value must be a uuid
**runCondition** | str,  | str,  | The run condition of the evaluator (such as \&quot;TEST_PROD\&quot;, \&quot;TEST\&quot;, \&quot;PROD\&quot;, \&quot;COMPARISON_2\&quot;) | 
**updatedAt** | decimal.Decimal, int, float,  | decimal.Decimal,  | Timestamp in seconds since the UNIX epoch. Can be transformed into a Date object. | value must be a 32 bit float
**who** | str,  | str,  | The type of evaluator (such as \&quot;AI\&quot;, \&quot;HEURISTIC\&quot;, \&quot;HUMAN\&quot;, \&quot;CLASSIFIER\&quot;) | 
**archivedAt** | [**UnixSecondsNullable**](UnixSecondsNullable.md) | [**UnixSecondsNullable**](UnixSecondsNullable.md) |  | [optional] 
**icon** | None, str,  | NoneClass, str,  |  | [optional] 
**[options](#options)** | list, tuple, None,  | tuple, NoneClass,  | For evaluators with options scoring, the available options to choose from | [optional] 
**aiModel** | str,  | str,  | For AI evaluators, the AI model to use | [optional] 
**pipelineId** | None, str, uuid.UUID,  | NoneClass, str,  | The ID of the pipeline that the evaluator belongs to | [optional] value must be a uuid
**processorId** | None, str, uuid.UUID,  | NoneClass, str,  | The ID of the processor associated with the evaluator | [optional] value must be a uuid
**organizationId** | str, uuid.UUID,  | str,  | The ID of the organization that the evaluator belongs to | [optional] value must be a uuid
**templateDescription** | str,  | str,  | For evaluator templates, the description of the template | [optional] 
**heuristicFn** | None, str,  | NoneClass, str,  | For heuristic evaluators, the heuristic function to use | [optional] 
**aiPromptFormat** | None, str,  | NoneClass, str,  | For AI evaluators, the prompt template that should be sent to the AI model | [optional] 
**[aiImageUrls](#aiImageUrls)** | list, tuple,  | tuple,  | For AI image evaluators, the paths to the image URLs | [optional] 
**humanPrompt** | None, str,  | NoneClass, str,  | For human evaluators, the instructions for the human to follow | [optional] 
**classifierValuePath** | None, str,  | NoneClass, str,  | For classification evaluators, the path to the predicted classification | [optional] 
**classifierExpectedValuePath** | None, str,  | NoneClass, str,  | For classification evaluators, the path to the expected classification | [optional] 
**[multiClassOptions](#multiClassOptions)** | list, tuple,  | tuple,  | For classification evaluators using multi-class evaluation, the available options to match with | [optional] 
**prodEvalActive** | bool,  | BoolClass,  | Use \&quot;samplingProbability\&quot; instead | [optional] 
**samplingProbability** | None, decimal.Decimal, int, float,  | NoneClass, decimal.Decimal,  | When optionally running on production data, the associated sampling probability of this evaluator (from 0 to 100) | [optional] 
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

# options

For evaluators with options scoring, the available options to choose from

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple, None,  | tuple, NoneClass,  | For evaluators with options scoring, the available options to choose from | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
items | dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, bool, None, list, tuple, bytes, io.FileIO, io.BufferedReader,  | frozendict.frozendict, str, decimal.Decimal, BoolClass, NoneClass, tuple, bytes, FileIO |  | 

# aiImageUrls

For AI image evaluators, the paths to the image URLs

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  | For AI image evaluators, the paths to the image URLs | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
items | str,  | str,  |  | 

# multiClassOptions

For classification evaluators using multi-class evaluation, the available options to match with

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  | For classification evaluators using multi-class evaluation, the available options to match with | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
items | str,  | str,  |  | 

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

