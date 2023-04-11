import time
from typing import Optional
import pystache
import openai
import openai.api_resources as api
from gentrace.providers.step_run import StepRun


class OpenAIPipelineHandler:
    def __init__(self, pipeline = None):
        self.pipeline = pipeline

    @classmethod
    def setup(cls, config):
        if config:
            for key, value in config.items():
                print(f"Setting OpenAI config : {key} = {value}")
                setattr(openai, key, value)

    def set_pipeline_run(self, pipeline_run):
        self.pipeline_run = pipeline_run
        
def intercept_completion(original_completion):
    def wrapper(*args, **kwargs):
        prompt_template = kwargs.get("promptTemplate")
        prompt_inputs = kwargs.get("promptInputs")
        base_completion_options = {k: v for k, v in kwargs.items() if k not in ["promptTemplate", "promptInputs"]}

        if "prompt" in base_completion_options:
            raise ValueError("The prompt attribute cannot be provided when using the Gentrace SDK. Use promptTemplate and promptInputs instead.")

        if not prompt_template:
            raise ValueError("The promptTemplate attribute must be provided when using the Gentrace SDK.")

        rendered_prompt = pystache.render(prompt_template, prompt_inputs)

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

def intercept_chat_completion(original_completion):
    def wrapper(*args, **kwargs):
        messages = kwargs.get("messages")
        user = kwargs.get("user")
        model_params = {k: v for k, v in kwargs.items() if k not in ["messages", "user"]}

        start_time = time.time()
        completion = original_completion(**kwargs)
        end_time = time.time()

        elapsed_time = int(end_time - start_time)

        self.pipeline_run.add_step_run(
            OpenAICreateChatCompletionStepRun(
                elapsed_time,
                start_time,
                end_time,
                {"messages": messages, "user": user},
                model_params,
                completion
            )
        )
    return wrapper

def intercept_embedding(original_completion):
    def wrapper(*args, **kwargs):
        model = kwargs.get("model")
        input_params = {k: v for k, v in kwargs.items() if k not in ["model"]}

        start_time = time.time()
        completion = original_completion(**kwargs)
        end_time = time.time()

        elapsed_time = int(end_time - start_time)

        self.pipeline_run.add_step_run(
            OpenAICreateEmbeddingStepRun(
                elapsed_time,
                start_time,
                end_time,
                input_params,
                { "model": model },
                completion
            )
        )
    return wrapper


class OpenAICreateCompletionStepRun(StepRun):
    def __init__(self, elapsed_time, start_time, end_time, inputs, model_params, response):
        super().__init__(
            "openai",
            "openai_createCompletion",
            elapsed_time,
            start_time,
            end_time,
            inputs,
            model_params,
            response
        )
        self.inputs = inputs
        self.model_params = model_params
        self.response = response

class OpenAICreateChatCompletionStepRun(StepRun):
    def __init__(self, elapsed_time, start_time, end_time, inputs, model_params, response):
        super().__init__(
            "openai",
            "openai_createChatCompletion",
            elapsed_time,
            start_time,
            end_time,
            inputs,
            model_params,
            response
        )
        self.inputs = inputs
        self.model_params = model_params
        self.response = response

class OpenAICreateEmbeddingStepRun(StepRun):
    def __init__(self, elapsed_time, start_time, end_time, inputs, model_params, response):
        super().__init__(
            "openai",
            "openai_createEmbedding",
            elapsed_time,
            start_time,
            end_time,
            inputs,
            model_params,
            response
        )
        self.inputs = inputs
        self.model_params = model_params
        self.response = response

for name, cls in vars(api).items():
    if isinstance(cls, type):
        # Create new class that inherits from the original class, don't directly monkey patch 
        # the original class
        new_class = type(name, (cls,), {})
        if name == 'Completion':
          new_class.create = intercept_completion(new_class.create)
        elif name == 'ChatCompletion':
          new_class.create = intercept_chat_completion(new_class.create)
        elif name == 'Embedding':
          new_class.create = intercept_embedding(new_class.create)

         # TODO: Must work on a acreate() method and check that streaming works
        setattr(OpenAIPipelineHandler, name, new_class)
