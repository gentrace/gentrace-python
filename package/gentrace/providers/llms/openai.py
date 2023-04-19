import time
from typing import Dict, Optional

import openai
import pystache

from gentrace.configuration import Configuration
from gentrace.providers.pipeline import Pipeline
from gentrace.providers.pipeline_run import PipelineRun
from gentrace.providers.step_run import StepRun
from gentrace.providers.utils import to_date_string


class OpenAIPipelineHandler:
    pipeline_run: Optional[PipelineRun] = None
    pipeline: Optional[Pipeline] = None
    gentrace_config: Dict
    config: Dict

    def __init__(self, gentrace_config, config, pipeline=None, pipeline_run=None):
        self.pipeline = pipeline
        self.pipeline_run = pipeline_run
        self.gentrace_config = gentrace_config
        self.config = config

    @classmethod
    def setup(cls, config):
        if config:
            for key, value in config.items():
                setattr(openai, key, value)

    def set_pipeline_run(self, pipeline_run):
        self.pipeline_run = pipeline_run


def create_step_run(
    cls,
    pipeline_id: str,
    gentrace_config: Configuration,
    start_time,
    end_time,
    base_completion_options,
    prompt_template,
    prompt_inputs,
    completion,
):
    elapsed_time = int((end_time - start_time) * 1000)

    user = base_completion_options.get("user")
    suffix = base_completion_options.get("suffix")
    partial_model_params = {
        k: v for k, v in base_completion_options.items() if k not in ["user", "suffix"]
    }

    inputs_dict = {"prompt": prompt_inputs}
    if user is not None:
        inputs_dict["user"] = user
    if suffix is not None:
        inputs_dict["suffix"] = suffix

    pipeline_run = cls.pipeline_run

    if not pipeline_run and pipeline_id:
        pipeline = Pipeline(
            id=pipeline_id,
            api_key=gentrace_config.api_key,
            host=gentrace_config.host,
        )

        pipeline_run = PipelineRun(
            pipeline=pipeline,
        )

    if pipeline_run:
        pipeline_run.add_step_run(
            OpenAICreateCompletionStepRun(
                elapsed_time,
                to_date_string(start_time),
                to_date_string(end_time),
                inputs_dict,
                {**partial_model_params, "promptTemplate": prompt_template},
                completion,
            )
        )


def intercept_completion(original_fn, gentrace_config: Configuration):
    @classmethod
    def wrapper(cls, *args, **kwargs):
        prompt_template = kwargs.get("prompt_template")
        prompt_inputs = kwargs.get("prompt_inputs")
        pipeline_id = kwargs.get("pipeline_id")
        base_completion_options = {
            k: v
            for k, v in kwargs.items()
            if k not in ["prompt_template", "prompt_inputs"]
        }

        if "prompt" in base_completion_options:
            raise ValueError(
                "The prompt attribute cannot be provided when using the Gentrace SDK. Use prompt_template and prompt_inputs instead."
            )

        if not prompt_template:
            raise ValueError(
                "The prompt_template attribute must be provided when using the Gentrace SDK."
            )

        rendered_prompt = pystache.render(prompt_template, prompt_inputs)

        new_completion_options = {**base_completion_options, "prompt": rendered_prompt}

        start_time = time.time()
        completion = original_fn(**new_completion_options)
        end_time = time.time()

        create_step_run(
            cls,
            pipeline_id,
            gentrace_config,
            start_time,
            end_time,
            base_completion_options,
            prompt_template,
            prompt_inputs,
            completion,
        )

    return wrapper


def intercept_completion_async(original_fn, gentrace_config: Configuration):
    @classmethod
    async def wrapper(cls, *args, **kwargs):
        prompt_template = kwargs.get("prompt_template")
        prompt_inputs = kwargs.get("prompt_inputs")
        pipeline_id = kwargs.get("pipeline_id")
        stream = kwargs.get("stream")
        base_completion_options = {
            k: v
            for k, v in kwargs.items()
            if k not in ["prompt_template", "prompt_inputs"]
        }

        if "prompt" in base_completion_options:
            raise ValueError(
                "The prompt attribute cannot be provided when using the Gentrace SDK. Use prompt_template and prompt_inputs instead."
            )

        if not prompt_template:
            raise ValueError(
                "The prompt_template attribute must be provided when using the Gentrace SDK."
            )

        if stream:
            rendered_prompt = pystache.render(prompt_template, prompt_inputs)

            new_completion_options = {
                **base_completion_options,
                "prompt": rendered_prompt,
            }

            start_time = time.time()
            completion = await original_fn(**new_completion_options)

            async def profiled_completion():
                modified_response = []
                async for value in completion:
                    modified_response.append(value)
                    yield value

                end_time = time.time()

                text_list = [
                    obj["choices"][0]["text"]
                    for obj in modified_response
                    if "choices" in obj and obj["choices"]
                ]

                # Major hack by creating a resolved version of the streamed result.
                final_response_string = " ".join(text_list)
                final_response = {
                    "choices": [
                        {
                            "finish_reason": None,
                            "index": 0,
                            "logprobs": None,
                            "text": final_response_string,
                        }
                    ]
                }

                create_step_run(
                    cls,
                    pipeline_id,
                    gentrace_config,
                    start_time,
                    end_time,
                    base_completion_options,
                    prompt_template,
                    prompt_inputs,
                    final_response,
                )

            return profiled_completion()

        rendered_prompt = pystache.render(prompt_template, prompt_inputs)

        new_completion_options = {**base_completion_options, "prompt": rendered_prompt}

        start_time = time.time()
        completion = await original_fn(**new_completion_options)
        end_time = time.time()

        create_step_run(
            cls,
            pipeline_id,
            gentrace_config,
            start_time,
            end_time,
            base_completion_options,
            prompt_template,
            prompt_inputs,
            completion,
        )
        return completion

    return wrapper


def intercept_chat_completion(original_fn, gentrace_config: Configuration):
    @classmethod
    def wrapper(cls, *args, **kwargs):
        messages = kwargs.get("messages")
        user = kwargs.get("user")
        pipeline_id = kwargs.get("pipeline_id")
        model_params = {
            k: v for k, v in kwargs.items() if k not in ["messages", "user"]
        }

        start_time = time.time()
        completion = original_fn(**kwargs)
        end_time = time.time()

        elapsed_time = int((end_time - start_time) * 1000)

        pipeline_run = cls.pipeline_run

        if not pipeline_run and pipeline_id:
            pipeline = Pipeline(
                id=pipeline_id,
                api_key=gentrace_config.api_key,
                host=gentrace_config.host,
            )

            pipeline_run = PipelineRun(
                pipeline=pipeline,
            )

        if pipeline_run:
            pipeline_run.add_step_run(
                OpenAICreateChatCompletionStepRun(
                    elapsed_time,
                    to_date_string(start_time),
                    to_date_string(end_time),
                    {"messages": messages, "user": user},
                    model_params,
                    completion,
                )
            )

        return completion

    return wrapper


def intercept_chat_completion_async(original_fn, gentrace_config: Configuration):
    @classmethod
    async def wrapper(cls, *args, **kwargs):
        messages = kwargs.get("messages")
        user = kwargs.get("user")
        stream = kwargs.get("stream")
        pipeline_id = kwargs.get("pipeline_id")
        model_params = {
            k: v for k, v in kwargs.items() if k not in ["messages", "user"]
        }

        start_time = time.time()
        completion = await original_fn(**kwargs)

        if stream:

            async def profiled_completion():
                modified_response = []
                async for value in completion:
                    modified_response.append(value)
                    yield value

                end_time = time.time()

                text_list = []
                for stream_result in modified_response:
                    if (
                        "choices" in stream_result
                        and stream_result["choices"][0].get("text")
                        and stream_result["choices"][0].get("finish_reason") != "stop"
                    ):
                        text_list.append(stream_result["choices"][0]["text"])

                # Major hack by creating a resolved version of the streamed result.
                final_response_string = " ".join(text_list)
                final_response = {
                    "choices": [
                        {
                            "finish_reason": None,
                            "index": 0,
                            "logprobs": None,
                            "text": final_response_string,
                        }
                    ]
                }

                elapsed_time = int((end_time - start_time) * 1000)

                pipeline_run = cls.pipeline_run

                if not pipeline_run and pipeline_id:
                    pipeline = Pipeline(
                        id=pipeline_id,
                        api_key=gentrace_config.api_key,
                        host=gentrace_config.host,
                    )

                    pipeline_run = PipelineRun(
                        pipeline=pipeline,
                    )

                if pipeline_run:
                    pipeline_run.add_step_run(
                        OpenAICreateChatCompletionStepRun(
                            elapsed_time,
                            to_date_string(start_time),
                            to_date_string(end_time),
                            {"messages": messages, "user": user},
                            model_params,
                            final_response,
                        )
                    )

            return profiled_completion()

        end_time = time.time()

        elapsed_time = int((end_time - start_time) * 1000)

        pipeline_run = cls.pipeline_run

        if not pipeline_run and pipeline_id:
            pipeline = Pipeline(
                id=pipeline_id,
                api_key=gentrace_config.api_key,
                host=gentrace_config.host,
            )

            pipeline_run = PipelineRun(
                pipeline=pipeline,
            )

        if pipeline_run:
            pipeline_run.add_step_run(
                OpenAICreateChatCompletionStepRun(
                    elapsed_time,
                    to_date_string(start_time),
                    to_date_string(end_time),
                    {"messages": messages, "user": user},
                    model_params,
                    completion,
                )
            )
        return completion

    return wrapper


def intercept_embedding(original_fn, gentrace_config: Configuration):
    @classmethod
    def wrapper(cls, *args, **kwargs):
        model = kwargs.get("model")
        pipeline_id = kwargs.get("pipeline_id")
        input_params = {k: v for k, v in kwargs.items() if k not in ["model"]}

        start_time = time.time()
        completion = original_fn(**kwargs)
        end_time = time.time()

        elapsed_time = int((end_time - start_time) * 1000)

        pipeline_run = cls.pipeline_run

        if not pipeline_run and pipeline_id:
            pipeline = Pipeline(
                id=pipeline_id,
                api_key=gentrace_config.api_key,
                host=gentrace_config.host,
            )

            pipeline_run = PipelineRun(
                pipeline=pipeline,
            )

        if pipeline_run:
            pipeline_run.add_step_run(
                OpenAICreateEmbeddingStepRun(
                    elapsed_time,
                    to_date_string(start_time),
                    to_date_string(end_time),
                    input_params,
                    {"model": model},
                    completion,
                )
            )
        return completion

    return wrapper


def intercept_embedding_async(original_fn, gentrace_config: Configuration):
    @classmethod
    async def wrapper(cls, *args, **kwargs):
        model = kwargs.get("model")
        pipeline_id = kwargs.get("pipeline_id")
        input_params = {k: v for k, v in kwargs.items() if k not in ["model"]}

        start_time = time.time()
        completion = await original_fn(**kwargs)
        end_time = time.time()

        elapsed_time = int((end_time - start_time) * 1000)

        pipeline_run = cls.pipeline_run if hasattr(cls, "pipeline_run") else None

        print("pipeline_run", pipeline_run)

        if not pipeline_run and pipeline_id:
            pipeline = Pipeline(
                id=pipeline_id,
                api_key=gentrace_config.api_key,
                host=gentrace_config.host,
            )

            pipeline_run = PipelineRun(
                pipeline=pipeline,
            )

        if pipeline_run:
            pipeline_run.add_step_run(
                OpenAICreateEmbeddingStepRun(
                    elapsed_time,
                    to_date_string(start_time),
                    to_date_string(end_time),
                    input_params,
                    {"model": model},
                    completion,
                )
            )
        return completion

    return wrapper


def annotate_pipeline_handler(
    handler: OpenAIPipelineHandler,
    gentrace_config: Configuration,
    pipeline_run: Optional[PipelineRun] = None,
):
    import openai

    for name, cls in vars(openai.api_resources).items():
        if isinstance(cls, type):
            # Create new class that inherits from the original class, don't directly monkey patch
            # the original class
            new_class = type(name, (cls,), {})
            if name == "Completion":
                new_class.create = intercept_completion(
                    new_class.create, gentrace_config
                )
                new_class.acreate = intercept_completion_async(
                    new_class.acreate, gentrace_config
                )
            elif name == "ChatCompletion":
                new_class.create = intercept_chat_completion(
                    new_class.create, gentrace_config
                )
                new_class.acreate = intercept_chat_completion_async(
                    new_class.acreate, gentrace_config
                )
            elif name == "Embedding":
                new_class.create = intercept_embedding(
                    new_class.create, gentrace_config
                )
                new_class.acreate = intercept_embedding_async(
                    new_class.acreate, gentrace_config
                )

            new_class.pipeline_run = pipeline_run
            setattr(handler, name, new_class)

    return handler


class OpenAICreateCompletionStepRun(StepRun):
    def __init__(
        self, elapsed_time, start_time, end_time, inputs, model_params, response
    ):
        super().__init__(
            "openai",
            "openai_createCompletion",
            elapsed_time,
            start_time,
            end_time,
            inputs,
            model_params,
            response,
        )
        self.inputs = inputs
        self.model_params = model_params
        self.response = response


class OpenAICreateChatCompletionStepRun(StepRun):
    def __init__(
        self, elapsed_time, start_time, end_time, inputs, model_params, response
    ):
        super().__init__(
            "openai",
            "openai_createChatCompletion",
            elapsed_time,
            start_time,
            end_time,
            inputs,
            model_params,
            response,
        )
        self.inputs = inputs
        self.model_params = model_params
        self.response = response


class OpenAICreateEmbeddingStepRun(StepRun):
    def __init__(
        self, elapsed_time, start_time, end_time, inputs, model_params, response
    ):
        super().__init__(
            "openai",
            "openai_createEmbedding",
            elapsed_time,
            start_time,
            end_time,
            inputs,
            model_params,
            response,
        )
        self.inputs = inputs
        self.model_params = model_params
        self.response = response
