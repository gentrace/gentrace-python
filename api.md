# Pipelines

Types:

```python
from gentrace.types import CreatePipelineBody, Pipeline, PipelineList
```

Methods:

- <code title="post /v4/pipelines">client.pipelines.<a href="./src/gentrace/resources/pipelines.py">create</a>(\*\*<a href="src/gentrace/types/pipeline_create_params.py">params</a>) -> <a href="./src/gentrace/types/pipeline.py">Pipeline</a></code>
- <code title="get /v4/pipelines/{id}">client.pipelines.<a href="./src/gentrace/resources/pipelines.py">retrieve</a>(id) -> <a href="./src/gentrace/types/pipeline.py">Pipeline</a></code>
- <code title="post /v4/pipelines/{id}">client.pipelines.<a href="./src/gentrace/resources/pipelines.py">update</a>(id, \*\*<a href="src/gentrace/types/pipeline_update_params.py">params</a>) -> <a href="./src/gentrace/types/pipeline.py">Pipeline</a></code>
- <code title="get /v4/pipelines">client.pipelines.<a href="./src/gentrace/resources/pipelines.py">list</a>(\*\*<a href="src/gentrace/types/pipeline_list_params.py">params</a>) -> <a href="./src/gentrace/types/pipeline_list.py">PipelineList</a></code>

# Experiments

Types:

```python
from gentrace.types import Experiment, ExperimentList
```

Methods:

- <code title="post /v4/experiments">client.experiments.<a href="./src/gentrace/resources/experiments.py">create</a>(\*\*<a href="src/gentrace/types/experiment_create_params.py">params</a>) -> <a href="./src/gentrace/types/experiment.py">Experiment</a></code>
- <code title="get /v4/experiments/{id}">client.experiments.<a href="./src/gentrace/resources/experiments.py">retrieve</a>(id) -> <a href="./src/gentrace/types/experiment.py">Experiment</a></code>
- <code title="post /v4/experiments/{id}">client.experiments.<a href="./src/gentrace/resources/experiments.py">update</a>(id, \*\*<a href="src/gentrace/types/experiment_update_params.py">params</a>) -> <a href="./src/gentrace/types/experiment.py">Experiment</a></code>
- <code title="get /v4/experiments">client.experiments.<a href="./src/gentrace/resources/experiments.py">list</a>(\*\*<a href="src/gentrace/types/experiment_list_params.py">params</a>) -> <a href="./src/gentrace/types/experiment_list.py">ExperimentList</a></code>

# Organizations

Types:

```python
from gentrace.types import Organization
```

Methods:

- <code title="get /v4/organizations/{id}">client.organizations.<a href="./src/gentrace/resources/organizations.py">retrieve</a>(id) -> <a href="./src/gentrace/types/organization.py">Organization</a></code>

# Datasets

Types:

```python
from gentrace.types import Dataset, DatasetList
```

Methods:

- <code title="post /v4/datasets">client.datasets.<a href="./src/gentrace/resources/datasets.py">create</a>(\*\*<a href="src/gentrace/types/dataset_create_params.py">params</a>) -> <a href="./src/gentrace/types/dataset.py">Dataset</a></code>
- <code title="get /v4/datasets/{id}">client.datasets.<a href="./src/gentrace/resources/datasets.py">retrieve</a>(id) -> <a href="./src/gentrace/types/dataset.py">Dataset</a></code>
- <code title="post /v4/datasets/{id}">client.datasets.<a href="./src/gentrace/resources/datasets.py">update</a>(id, \*\*<a href="src/gentrace/types/dataset_update_params.py">params</a>) -> <a href="./src/gentrace/types/dataset.py">Dataset</a></code>
- <code title="get /v4/datasets">client.datasets.<a href="./src/gentrace/resources/datasets.py">list</a>(\*\*<a href="src/gentrace/types/dataset_list_params.py">params</a>) -> <a href="./src/gentrace/types/dataset_list.py">DatasetList</a></code>

# TestCases

Types:

```python
from gentrace.types import TestCase, TestCaseList
```

Methods:

- <code title="post /v4/test-cases">client.test_cases.<a href="./src/gentrace/resources/test_cases.py">create</a>(\*\*<a href="src/gentrace/types/test_case_create_params.py">params</a>) -> <a href="./src/gentrace/types/test_case.py">TestCase</a></code>
- <code title="get /v4/test-cases/{id}">client.test_cases.<a href="./src/gentrace/resources/test_cases.py">retrieve</a>(id) -> <a href="./src/gentrace/types/test_case.py">TestCase</a></code>
- <code title="get /v4/test-cases">client.test_cases.<a href="./src/gentrace/resources/test_cases.py">list</a>(\*\*<a href="src/gentrace/types/test_case_list_params.py">params</a>) -> <a href="./src/gentrace/types/test_case_list.py">TestCaseList</a></code>
- <code title="delete /v4/test-cases/{id}">client.test_cases.<a href="./src/gentrace/resources/test_cases.py">delete</a>(id) -> None</code>
