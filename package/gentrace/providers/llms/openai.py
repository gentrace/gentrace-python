from typing import Optional
import time
import mustache
import openai
import openai.api_resources as api

class OpenAIPipelineHandler:
    def __init__(self, pipeline = None):
        self.pipeline = pipeline

    @classmethod
    def setup(config):
        if config:
            for key, value in config.items():
                setattr(openai, key, value)

    def set_pipeline_run(self, pipeline_run):
        self.pipeline_run = pipeline_run
        
def intercept_completion(original_completion):
    def wrapper(*args, **kwargs):
        prompt_template = kwargs.get("promptTemplate")
        prompt_inputs = kwargs.get("promptInputs")
        base_completion_options = {k: v for k, v in kwargs.items() if k not in ["promptTemplate", "promptInputs"]}

        if "prompt" in base_completion_options:
            raise ValueError("The prompt attribute cannot be provided when using the GENTRACE SDK. Use promptTemplate and promptInputs instead.")

        if not prompt_template:
            raise ValueError("The promptTemplate attribute must be provided when using the GENTRACE SDK.")

        rendered_prompt = mustache.render(prompt_template, prompt_inputs)

        new_completion_options = {**base_completion_options, "prompt": rendered_prompt}

        start_time = time.time()
        completion = original_completion(**new_completion_options)
        end_time = time.time()

        elapsed_time = int(end_time - start_time)

        user = base_completion_options.get("user")
        suffix = base_completion_options.get("suffix")
        partial_model_params = {k: v for k, v in base_completion_options.items() if k not in ["user", "suffix"]}

        self.pipeline_run.add_step_run(
            OpenAICreateCompletionStepRun(
                elapsed_time,
                start_time,
                end_time,
                {"prompt": prompt_inputs, "user": user, "suffix": suffix},
                {**partial_model_params, "promptTemplate": prompt_template},
                completion
            )
        )
    return wrapper


for name, cls in vars(api).items():
    if isinstance(cls, type):
        # Create new class that inherits from the original class, don't directly monkey patch 
        # the original class
        new_class = type(name, (cls,), {})
        if name == 'Completion':
          new_class.create = intercept_completion(new_class.create)
          # TODO: Must work on a acreate() method and check that streaming works

        setattr(OpenAIPipelineHandler, name, new_class)
