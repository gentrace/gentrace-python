import copy
from typing import Optional

from gentrace.providers.context import Context


class StepRun:
    def __init__(
            self,
            provider: str,
            invocation: str,
            elapsed_time: float,
            start_time: str,
            end_time: str,
            inputs: any,
            model_params: any,
            outputs: any,
            context: Optional[Context] = None,
    ):
        self.provider = provider
        self.invocation = invocation
        self.elapsed_time = elapsed_time
        self.start_time = start_time
        self.end_time = end_time
        self.inputs = copy.deepcopy(inputs)
        self.model_params = model_params
        self.outputs = copy.deepcopy(outputs)
        self.context = copy.deepcopy(context or {})
