import time
from datetime import datetime
from typing import Optional

import openai
import pystache

from gentrace.providers.step_run import StepRun
from gentrace.providers.utils import to_date_string


class OpenAIPipelineHandler:
    def __init__(self, pipeline=None):
        self.pipeline = pipeline

    @classmethod
    def setup(cls, config):
        if config:
            for key, value in config.items():
                setattr(openai, key, value)

    def set_pipeline_run(self, pipeline_run):
        self.pipeline_run = pipeline_run


def create_step_run(
    cls,
    start_time,
    end_time,
    base_completion_options,
    prompt_template,
    prompt_inputs,
    completion,
):
    elapsed_time = int(end_time - start_time)

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

    cls.pipeline_run.add_step_run(
        OpenAICreateCompletionStepRun(
            elapsed_time,
            to_date_string(start_time),
            to_date_string(end_time),
            inputs_dict,
            {**partial_model_params, "promptTemplate": prompt_template},
            completion,
        )
    )


def intercept_completion(original_fn):
    @classmethod
    def wrapper(cls, *args, **kwargs):
        prompt_template = kwargs.get("promptTemplate")
        prompt_inputs = kwargs.get("promptInputs")
        base_completion_options = {
            k: v
            for k, v in kwargs.items()
            if k not in ["promptTemplate", "promptInputs"]
        }

        if "prompt" in base_completion_options:
            raise ValueError(
                "The prompt attribute cannot be provided when using the Gentrace SDK. Use promptTemplate and promptInputs instead."
            )

        if not prompt_template:
            raise ValueError(
                "The promptTemplate attribute must be provided when using the Gentrace SDK."
            )

        rendered_prompt = pystache.render(prompt_template, prompt_inputs)

        new_completion_options = {**base_completion_options, "prompt": rendered_prompt}

        start_time = time.time()
        completion = original_fn(**new_completion_options)
        end_time = time.time()

        create_step_run(
            cls,
            start_time,
            end_time,
            base_completion_options,
            prompt_template,
            prompt_inputs,
            completion,
        )

    return wrapper


def intercept_completion_async(original_fn):
    @classmethod
    async def wrapper(cls, *args, **kwargs):
        prompt_template = kwargs.get("promptTemplate")
        prompt_inputs = kwargs.get("promptInputs")
        stream = kwargs.get("stream")
        base_completion_options = {
            k: v
            for k, v in kwargs.items()
            if k not in ["promptTemplate", "promptInputs"]
        }

        if "prompt" in base_completion_options:
            raise ValueError(
                "The prompt attribute cannot be provided when using the Gentrace SDK. Use promptTemplate and promptInputs instead."
            )

        if not prompt_template:
            raise ValueError(
                "The promptTemplate attribute must be provided when using the Gentrace SDK."
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
            start_time,
            end_time,
            base_completion_options,
            prompt_template,
            prompt_inputs,
            completion,
        )
        return completion

    return wrapper


def intercept_chat_completion(original_fn):
    @classmethod
    def wrapper(cls, *args, **kwargs):
        messages = kwargs.get("messages")
        user = kwargs.get("user")
        model_params = {
            k: v for k, v in kwargs.items() if k not in ["messages", "user"]
        }

        start_time = time.time()
        completion = original_fn(**kwargs)
        end_time = time.time()

        elapsed_time = int(end_time - start_time)

        cls.pipeline_run.add_step_run(
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


def intercept_chat_completion_async(original_fn):
    @classmethod
    async def wrapper(cls, *args, **kwargs):
        messages = kwargs.get("messages")
        user = kwargs.get("user")
        stream = kwargs.get("stream")
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

                elapsed_time = int(end_time - start_time)

                cls.pipeline_run.add_step_run(
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

        elapsed_time = int(end_time - start_time)

        cls.pipeline_run.add_step_run(
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


def intercept_embedding(original_fn):
    @classmethod
    def wrapper(cls, *args, **kwargs):
        model = kwargs.get("model")
        input_params = {k: v for k, v in kwargs.items() if k not in ["model"]}

        start_time = time.time()
        completion = original_fn(**kwargs)
        end_time = time.time()

        elapsed_time = int(end_time - start_time)

        cls.pipeline_run.add_step_run(
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


def intercept_embedding_async(original_fn):
    @classmethod
    async def wrapper(cls, *args, **kwargs):
        model = kwargs.get("model")
        input_params = {k: v for k, v in kwargs.items() if k not in ["model"]}

        start_time = time.time()
        completion = await original_fn(**kwargs)
        end_time = time.time()

        elapsed_time = int(end_time - start_time)

        cls.pipeline_run.add_step_run(
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
