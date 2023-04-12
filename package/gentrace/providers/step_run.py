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
    ):
        self.provider = provider
        self.invocation = invocation
        self.elapsed_time = elapsed_time
        self.start_time = start_time
        self.end_time = end_time
        self.inputs = inputs
        self.model_params = model_params
        self.outputs = outputs
