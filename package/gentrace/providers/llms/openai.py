import copy
import time
import uuid
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
    config: Dict = {}

    def __init__(self, gentrace_config, config=None, pipeline=None, pipeline_run=None):
        self.pipeline = pipeline
        self.pipeline_run = pipeline_run
        self.gentrace_config = gentrace_config
        if config:
            self.config = config

    @classmethod
    def setup(cls, config):
        if config:
            for key, value in config.items():
                setattr(openai, key, value)


def create_completion_step_run(
    cls,
    pipeline_id: str,
    gentrace_config: Configuration,
    start_time,
    end_time,
    base_completion_options,
    prompt_template,
    prompt_inputs,
    completion,
    pipeline_run_id: Optional[str] = None,
    stream=False,
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

    pipeline_run = cls.pipeline_run if hasattr(cls, "pipeline_run") else None

    is_self_contained = not pipeline_run and pipeline_id

    if is_self_contained:
        pipeline = Pipeline(
            id=pipeline_id,
            api_key=gentrace_config.access_token,
            host=gentrace_config.host,
        )

        pipeline_run = PipelineRun(
            pipeline=pipeline,
            id=pipeline_run_id,
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

        if is_self_contained:
            submit_result = pipeline_run.submit()

            if not stream:
                completion["pipelineRunId"] = (
                    submit_result["pipelineRunId"]
                    if "pipelineRunId" in submit_result
                    else None
                )


def create_completion_stream_response(stream_list):
    final_response_string = ""
    for value in stream_list:
        if "choices" in value and value["choices"]:
            first_choice = value["choices"][0]
            if "text" in first_choice:
                final_response_string += first_choice["text"]
            elif (
                "delta" in first_choice
                and first_choice["delta"]
                and "content" in first_choice["delta"]
            ):
                final_response_string += first_choice["delta"]["content"]
            elif (
                "finish_reason" in first_choice
                and first_choice["finish_reason"] == "stop"
            ):
                break

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

    return final_response


def create_chat_completion_stream_response(stream_list):
    final_response_string = ""
    for value in stream_list:
        if "choices" in value and value["choices"]:
            first_choice = value["choices"][0]
            if "text" in first_choice:
                final_response_string += first_choice["text"]
            elif (
                "delta" in first_choice
                and first_choice["delta"]
                and "content" in first_choice["delta"]
            ):
                final_response_string += first_choice["delta"]["content"]
            elif (
                "finish_reason" in first_choice
                and first_choice["finish_reason"] == "stop"
            ):
                break

    final_response = {
        "choices": [
            {
                "finish_reason": None,
                "index": 0,
                "message": {"content": final_response_string, "role": "assistant"},
            }
        ]
    }

    return final_response


def intercept_completion(original_fn, gentrace_config: Configuration):
    @classmethod
    def wrapper(cls, *args, **kwargs):
        prompt_template = kwargs.get("prompt_template")
        prompt_inputs = kwargs.get("prompt_inputs")
        prompt = kwargs.get("prompt")
        pipeline_id = kwargs.pop("pipeline_id", None)
        stream = kwargs.get("stream")
        base_completion_options = {
            k: v
            for k, v in kwargs.items()
            if k not in ["prompt_template", "prompt_inputs"]
        }

        if stream:
            rendered_prompt = prompt

            if prompt_template and prompt_inputs:
                rendered_prompt = pystache.render(prompt_template, prompt_inputs)
            else:
                # If no prompt template or inputs, then specify the prompt as the entire input
                prompt_inputs = prompt

            new_completion_options = {
                **base_completion_options,
                "prompt": rendered_prompt,
            }

            start_time = time.time()
            completion = original_fn(**new_completion_options)

            is_self_contained = not hasattr(cls, "pipeline_run") and pipeline_id
            if is_self_contained:
                pipeline_run_id = str(uuid.uuid4())

            def profiled_completion():
                modified_response = []
                for value in completion:
                    if value and is_self_contained:
                        value["pipelineRunId"] = pipeline_run_id
                    modified_response.append(value)
                    yield value

                end_time = time.time()

                full_response = create_completion_stream_response(modified_response)

                create_completion_step_run(
                    cls,
                    pipeline_id,
                    gentrace_config,
                    start_time,
                    end_time,
                    base_completion_options,
                    prompt_template,
                    prompt_inputs,
                    full_response,
                    pipeline_run_id if is_self_contained else None,
                    stream,
                )

            return profiled_completion()

        rendered_prompt = prompt

        if prompt_template and prompt_inputs:
            rendered_prompt = pystache.render(prompt_template, prompt_inputs)
        else:
            # If no prompt template or inputs, then specify the prompt as the entire input
            prompt_inputs = prompt

        new_completion_options = {
            **base_completion_options,
            "prompt": rendered_prompt,
        }

        start_time = time.time()
        completion = original_fn(**new_completion_options)

        end_time = time.time()

        create_completion_step_run(
            cls,
            pipeline_id,
            gentrace_config,
            start_time,
            end_time,
            base_completion_options,
            prompt_template,
            prompt_inputs,
            completion,
            None,
            stream,
        )

        return completion

    return wrapper


def intercept_completion_async(original_fn, gentrace_config: Configuration):
    @classmethod
    async def wrapper(cls, *args, **kwargs):
        prompt_template = kwargs.get("prompt_template")
        prompt_inputs = kwargs.get("prompt_inputs")
        prompt = kwargs.get("prompt")
        pipeline_id = kwargs.pop("pipeline_id", None)
        stream = kwargs.get("stream")
        base_completion_options = {
            k: v
            for k, v in kwargs.items()
            if k not in ["prompt_template", "prompt_inputs"]
        }

        if stream:
            rendered_prompt = prompt

            if prompt_template and prompt_inputs:
                rendered_prompt = pystache.render(prompt_template, prompt_inputs)
            else:
                # If no prompt template or inputs, then specify the prompt as the entire input
                prompt_inputs = prompt

            new_completion_options = {
                **base_completion_options,
                "prompt": rendered_prompt,
            }

            start_time = time.time()
            completion = await original_fn(**new_completion_options)

            is_self_contained = not hasattr(cls, "pipeline_run") and pipeline_id
            if is_self_contained:
                pipeline_run_id = str(uuid.uuid4())

            async def profiled_completion():
                modified_response = []
                async for value in completion:
                    if value and is_self_contained:
                        value["pipelineRunId"] = pipeline_run_id
                    modified_response.append(value)
                    yield value

                end_time = time.time()

                full_response = create_completion_stream_response(modified_response)

                create_completion_step_run(
                    cls,
                    pipeline_id,
                    gentrace_config,
                    start_time,
                    end_time,
                    base_completion_options,
                    prompt_template,
                    prompt_inputs,
                    full_response,
                    pipeline_run_id if is_self_contained else None,
                    stream,
                )

            return profiled_completion()

        rendered_prompt = prompt

        if prompt_template and prompt_inputs:
            rendered_prompt = pystache.render(prompt_template, prompt_inputs)
        else:
            # If no prompt template or inputs, then specify the prompt as the entire input
            prompt_inputs = prompt

        new_completion_options = {
            **base_completion_options,
            "prompt": rendered_prompt,
        }

        start_time = time.time()
        completion = await original_fn(**new_completion_options)
        end_time = time.time()

        create_completion_step_run(
            cls,
            pipeline_id,
            gentrace_config,
            start_time,
            end_time,
            base_completion_options,
            prompt_template,
            prompt_inputs,
            completion,
            None,
            stream,
        )
        return completion

    return wrapper


def create_rendered_chat_messages(messages):
    new_messages = []
    for message in messages:
        new_message = copy.deepcopy(message)
        if "contentTemplate" in message and "contentInputs" in message:
            new_message["content"] = pystache.render(
                message["contentTemplate"], message["contentInputs"]
            )

        new_message.pop("contentTemplate", None)
        new_message.pop("contentInputs", None)

        new_messages.append(new_message)

    return new_messages


def intercept_chat_completion(original_fn, gentrace_config: Configuration):
    @classmethod
    def wrapper(cls, *args, **kwargs):
        messages = kwargs.get("messages")
        user = kwargs.get("user")
        pipeline_id = kwargs.pop("pipeline_id", None)
        stream = kwargs.get("stream")

        model_params = {
            k: v for k, v in kwargs.items() if k not in ["messages", "user"]
        }

        if stream:
            rendered_messages = create_rendered_chat_messages(messages)
            new_kwargs = dict(kwargs, messages=rendered_messages)
            start_time = time.time()
            completion = original_fn(**new_kwargs)

            is_self_contained = not hasattr(cls, "pipeline_run") and pipeline_id
            if is_self_contained:
                pipeline_run_id = str(uuid.uuid4())

            def profiled_completion():
                modified_response = []
                for value in completion:
                    if value and is_self_contained:
                        value["pipelineRunId"] = pipeline_run_id
                    modified_response.append(value)
                    yield value

                end_time = time.time()

                elapsed_time = int((end_time - start_time) * 1000)

                pipeline_run = (
                    cls.pipeline_run if hasattr(cls, "pipeline_run") else None
                )

                full_response = create_chat_completion_stream_response(
                    modified_response
                )
                if is_self_contained:
                    pipeline = Pipeline(
                        id=pipeline_id,
                        api_key=gentrace_config.access_token,
                        host=gentrace_config.host,
                    )

                    pipeline_run = PipelineRun(pipeline=pipeline, id=pipeline_run_id)

                if pipeline_run:
                    pipeline_run.add_step_run(
                        OpenAICreateChatCompletionStepRun(
                            elapsed_time,
                            to_date_string(start_time),
                            to_date_string(end_time),
                            {"messages": messages, "user": user},
                            model_params,
                            full_response,
                        )
                    )

                    if is_self_contained:
                        pipeline_run.submit()

            return profiled_completion()

        rendered_messages = create_rendered_chat_messages(messages)

        new_kwargs = dict(kwargs, messages=rendered_messages)

        start_time = time.time()
        completion = original_fn(**new_kwargs)
        end_time = time.time()

        elapsed_time = int((end_time - start_time) * 1000)

        pipeline_run = cls.pipeline_run if hasattr(cls, "pipeline_run") else None

        is_self_contained = not pipeline_run and pipeline_id
        if is_self_contained:
            pipeline = Pipeline(
                id=pipeline_id,
                api_key=gentrace_config.access_token,
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

            if is_self_contained:
                submit_result = pipeline_run.submit()
                completion["pipelineRunId"] = (
                    submit_result["pipelineRunId"]
                    if "pipelineRunId" in submit_result
                    else None
                )

        return completion

    return wrapper


def intercept_chat_completion_async(original_fn, gentrace_config: Configuration):
    @classmethod
    async def wrapper(cls, *args, **kwargs):
        messages = kwargs.get("messages")
        user = kwargs.get("user")
        stream = kwargs.get("stream")
        pipeline_id = kwargs.pop("pipeline_id", None)
        model_params = {
            k: v for k, v in kwargs.items() if k not in ["messages", "user"]
        }

        rendered_messages = create_rendered_chat_messages(messages)
        new_kwargs = dict(kwargs, messages=rendered_messages)

        start_time = time.time()
        completion = await original_fn(**new_kwargs)

        if stream:
            is_self_contained = not hasattr(cls, "pipeline_run") and pipeline_id
            if is_self_contained:
                pipeline_run_id = str(uuid.uuid4())

            async def profiled_completion():
                modified_response = []
                async for value in completion:
                    if value and is_self_contained:
                        value["pipelineRunId"] = pipeline_run_id
                    modified_response.append(value)
                    yield value

                end_time = time.time()

                full_response = create_chat_completion_stream_response(
                    modified_response
                )

                elapsed_time = int((end_time - start_time) * 1000)

                pipeline_run = (
                    cls.pipeline_run if hasattr(cls, "pipeline_run") else None
                )

                if is_self_contained:
                    pipeline = Pipeline(
                        id=pipeline_id,
                        api_key=gentrace_config.access_token,
                        host=gentrace_config.host,
                    )

                    pipeline_run = PipelineRun(
                        pipeline=pipeline,
                        id=pipeline_run_id,
                    )

                if pipeline_run:
                    pipeline_run.add_step_run(
                        OpenAICreateChatCompletionStepRun(
                            elapsed_time,
                            to_date_string(start_time),
                            to_date_string(end_time),
                            {"messages": messages, "user": user},
                            model_params,
                            full_response,
                        )
                    )

                    if is_self_contained:
                        pipeline_run.submit()

            return profiled_completion()

        end_time = time.time()

        elapsed_time = int((end_time - start_time) * 1000)

        pipeline_run = cls.pipeline_run if hasattr(cls, "pipeline_run") else None

        is_self_contained = not pipeline_run and pipeline_id

        if is_self_contained:
            pipeline = Pipeline(
                id=pipeline_id,
                api_key=gentrace_config.access_token,
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

            if is_self_contained:
                submit_result = pipeline_run.submit()
                completion["pipelineRunId"] = (
                    submit_result["pipelineRunId"]
                    if "pipelineRunId" in submit_result
                    else None
                )
        return completion

    return wrapper


def intercept_embedding(original_fn, gentrace_config: Configuration):
    @classmethod
    def wrapper(cls, *args, **kwargs):
        model = kwargs.get("model")
        pipeline_id = kwargs.pop("pipeline_id", None)
        input_params = {k: v for k, v in kwargs.items() if k not in ["model"]}

        start_time = time.time()
        completion = original_fn(**kwargs)
        end_time = time.time()

        elapsed_time = int((end_time - start_time) * 1000)

        pipeline_run = cls.pipeline_run if hasattr(cls, "pipeline_run") else None

        is_self_contained = not pipeline_run and pipeline_id

        if is_self_contained:
            pipeline = Pipeline(
                id=pipeline_id,
                api_key=gentrace_config.access_token,
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

            if is_self_contained:
                submit_result = pipeline_run.submit()
                completion["pipelineRunId"] = (
                    submit_result["pipelineRunId"]
                    if "pipelineRunId" in submit_result
                    else None
                )
        return completion

    return wrapper


def intercept_embedding_async(original_fn, gentrace_config: Configuration):
    @classmethod
    async def wrapper(cls, *args, **kwargs):
        model = kwargs.get("model")
        pipeline_id = kwargs.pop("pipeline_id", None)
        input_params = {k: v for k, v in kwargs.items() if k not in ["model"]}

        start_time = time.time()
        completion = await original_fn(**kwargs)
        end_time = time.time()

        elapsed_time = int((end_time - start_time) * 1000)

        pipeline_run = cls.pipeline_run if hasattr(cls, "pipeline_run") else None

        is_self_contained = not pipeline_run and pipeline_id

        if is_self_contained:
            pipeline = Pipeline(
                id=pipeline_id,
                api_key=gentrace_config.access_token,
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

            if is_self_contained:
                submit_result = pipeline_run.submit()
                completion["pipelineRunId"] = (
                    submit_result["pipelineRunId"]
                    if "pipelineRunId" in submit_result
                    else None
                )

        return completion

    return wrapper


def swap_methods(cls, attribute: str, gentrace_config: Configuration, intercept_fn):
    has_old_sync_saved = hasattr(cls, attribute + "_old")
    original_create = getattr(cls, attribute)
    if has_old_sync_saved:
        original_create = getattr(cls, attribute + "_old")
    else:
        setattr(cls, attribute + "_old", getattr(cls, attribute))

    setattr(cls, attribute, intercept_fn(original_create, gentrace_config))


def annotate_openai_module(
    gentrace_config: Configuration,
):
    import openai

    for name, cls in vars(openai.api_resources).items():
        if isinstance(cls, type):
            if name == "Completion":
                swap_methods(cls, "create", gentrace_config, intercept_completion)
                swap_methods(
                    cls, "acreate", gentrace_config, intercept_completion_async
                )
            elif name == "ChatCompletion":
                swap_methods(cls, "create", gentrace_config, intercept_chat_completion)
                swap_methods(
                    cls, "acreate", gentrace_config, intercept_chat_completion_async
                )

            elif name == "Embedding":
                swap_methods(cls, "create", gentrace_config, intercept_embedding)
                swap_methods(cls, "acreate", gentrace_config, intercept_embedding_async)

            setattr(openai.api_resources, name, cls)


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
                original_create = (
                    cls.create_old if hasattr(cls, "create_old") else cls.create
                )
                new_class.create = intercept_completion(
                    original_create, gentrace_config
                )
                original_acreate = (
                    cls.acreate_old if hasattr(cls, "acreate_old") else cls.acreate
                )
                new_class.acreate = intercept_completion_async(
                    original_acreate, gentrace_config
                )
            elif name == "ChatCompletion":
                original_create = (
                    cls.create_old if hasattr(cls, "create_old") else cls.create
                )
                new_class.create = intercept_chat_completion(
                    original_create, gentrace_config
                )
                original_acreate = (
                    cls.acreate_old if hasattr(cls, "acreate_old") else cls.acreate
                )
                new_class.acreate = intercept_chat_completion_async(
                    original_acreate, gentrace_config
                )
            elif name == "Embedding":
                original_create = (
                    cls.create_old if hasattr(cls, "create_old") else cls.create
                )
                new_class.create = intercept_embedding(original_create, gentrace_config)
                original_acreate = (
                    cls.acreate_old if hasattr(cls, "acreate_old") else cls.acreate
                )
                new_class.acreate = intercept_embedding_async(
                    original_acreate, gentrace_config
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
