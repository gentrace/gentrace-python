import copy
from typing import Any, Optional

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
        self.inputs = self._convert_to_dict(copy.deepcopy(inputs))
        self.model_params = model_params
        self.outputs = self._convert_to_dict(copy.deepcopy(outputs))
        self.context = copy.deepcopy(context or {})

    def _convert_to_dict(self, obj: Any) -> Any:
        if hasattr(obj, '__dict__'):
            # Check for model_dump first (works for both v1 and v2)
            if hasattr(obj, 'model_dump'):
                return obj.model_dump()
            # Fallback to dict() if model_dump is not available
            elif hasattr(obj, 'dict'):
                return obj.dict()
            # If neither method is available, use vars() to extrace the object's attributes
            else:
                return vars(obj)
        elif isinstance(obj, dict):
            return {k: self._convert_to_dict(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [self._convert_to_dict(item) for item in obj]
        return obj
