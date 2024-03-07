import copy
import os
import time
import uuid
from typing import Any, Dict, List, Optional

import pystache
from openai import AsyncOpenAI, OpenAI, chat, completions, embeddings

from gentrace.providers.pipeline import Pipeline
from gentrace.providers.pipeline_run import PipelineRun
from gentrace.providers.step_run import StepRun
from gentrace.providers.utils import to_date_string

# Mega hack: somehow __class__ is actually invoking the OpenAI constructor
prior_value = os.environ.get("OPENAI_API_KEY", None)

os.environ["OPENAI_API_KEY"] = "DUMMY_VALUE"

# Extract classes as you mentioned
ExtractedCompletions = completions.__class__
ExtractedChat = chat.__class__
ExtractedChatCompletions = chat.completions.__class__
ExtractedEmbeddings = embeddings.__class__

if prior_value is not None:
    os.environ["OPENAI_API_KEY"] = prior_value
else:
    del os.environ["OPENAI_API_KEY"]

# Hack: dummy async OpenAI client to get async classes
dummy_client = AsyncOpenAI(api_key="DUMMY_VALUE")

ExtractedAsyncCompletions = dummy_client.completions.__class__
ExtractedAsyncChat = dummy_client.chat.__class__
ExtractedAsyncChatCompletions = dummy_client.chat.completions.__class__
ExtractedAsyncEmbeddings = dummy_client.embeddings.__class__


class GentraceAsyncOpenAI(AsyncOpenAI):
    pipeline_run: Optional[PipelineRun] = None

    def __init__(self, *args, **kwargs):
        # print all kwargs
        self.pipeline_run = kwargs.pop("pipeline_run", None)
        self.pipeline = kwargs.pop("pipeline", None)
        self.config = kwargs.pop("gentrace_config")

        super().__init__(*args, **kwargs)

        self.completions = GentraceAsyncCompletions(client=self, gentrace_config=self.config,
                                                    pipeline=self.pipeline,
                                                    pipeline_run=self.pipeline_run)
        self.chat = ExtractedAsyncChat(self)
        self.chat.completions = GentraceAsyncChatCompletions(client=self, gentrace_config=self.config,
                                                             pipeline=self.pipeline,
                                                             pipeline_run=self.pipeline_run)
        self.embeddings = GentraceAsyncEmbeddings(client=self, gentrace_config=self.config,
                                                  pipeline=self.pipeline,
                                                  pipeline_run=self.pipeline_run)


class GentraceAsyncEmbeddings(ExtractedAsyncEmbeddings):

    def __init__(self, *, gentrace_config: Dict[str, Any], client: AsyncOpenAI, pipeline: Optional[Pipeline] = None,
                 pipeline_run: Optional[PipelineRun] = None):
        super().__init__(client)

        self.pipeline = pipeline
        self.pipeline_run = pipeline_run
        self.gentrace_config = gentrace_config

    async def create(self, *args, **kwargs):
        model = kwargs.get("model")
        pipeline_slug = kwargs.pop("pipeline_slug", None)

        context = kwargs.pop("gentrace", {})
        input_params = {k: v for k, v in kwargs.items() if k not in ["model"]}

        start_time = time.time()
        completion = await super().create(*args, **kwargs)
        end_time = time.time()

        elapsed_time = int((end_time - start_time) * 1000)

        pipeline_run = self.pipeline_run

        is_self_contained = not pipeline_run and pipeline_slug

        if is_self_contained:
            pipeline = Pipeline(
                slug=pipeline_slug,
                **self.gentrace_config,
            )

            pipeline_run = PipelineRun(pipeline=pipeline, context=context)

        if pipeline_run:
            pipeline_run.add_step_run(
                OpenAICreateEmbeddingStepRun(
                    elapsed_time,
                    to_date_string(start_time),
                    to_date_string(end_time),
                    input_params,
                    {"model": model},
                    completion.dict(),
                    context,
                )
            )

            if is_self_contained:
                submit_result = pipeline_run.submit()
                setattr(completion, "pipelineRunId",
                        submit_result["pipelineRunId"] if "pipelineRunId" in submit_result else None)

        return completion


class GentraceAsyncCompletions(ExtractedAsyncCompletions):
    def __init__(self, *, gentrace_config: Dict[str, Any], client: AsyncOpenAI, pipeline: Optional[Pipeline] = None,
                 pipeline_run: Optional[PipelineRun] = None):
        super().__init__(client)

        self.pipeline = pipeline
        self.pipeline_run = pipeline_run
        self.gentrace_config = gentrace_config

    async def create(self, *args, **kwargs):
        prompt_template = kwargs.get("prompt_template")
        prompt_inputs = kwargs.get("prompt_inputs")
        prompt = kwargs.get("prompt")
        pipeline_slug = kwargs.pop("pipeline_slug", None)

        context = kwargs.pop("gentrace", {})
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
            completion = await super().create(**new_completion_options)

            is_self_contained = (
                    not self.pipeline_run and pipeline_slug
            )
            if is_self_contained:
                pipeline_run_id = str(uuid.uuid4())

            async def profiled_completion():
                modified_response = []
                async for value in completion:
                    if value and is_self_contained:
                        setattr(value, "pipelineRunId", pipeline_run_id)
                    modified_response.append(value)
                    yield value

                end_time = time.time()

                full_response = create_completion_stream_response(modified_response)

                create_completion_step_run(
                    self.pipeline_run,
                    pipeline_slug,
                    self.gentrace_config,
                    start_time,
                    end_time,
                    base_completion_options,
                    prompt_template,
                    prompt_inputs,
                    completion,
                    full_response,
                    pipeline_run_id if is_self_contained else None,
                    stream,
                    context,
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
        completion = await super().create(**new_completion_options)
        end_time = time.time()

        create_completion_step_run(
            self.pipeline_run,
            pipeline_slug,
            self.gentrace_config,
            start_time,
            end_time,
            base_completion_options,
            prompt_template,
            prompt_inputs,
            completion,
            completion.dict(),
            None,
            stream,
            context,
        )
        return completion


class GentraceAsyncChatCompletions(ExtractedAsyncChatCompletions):
    def __init__(self, *, gentrace_config: Dict[str, Any], client: AsyncOpenAI, pipeline: Optional[Pipeline] = None,
                 pipeline_run: Optional[PipelineRun] = None):
        super().__init__(client)

        self.pipeline = pipeline
        self.pipeline_run = pipeline_run
        self.gentrace_config = gentrace_config

    async def create(self, *args, **kwargs):
        messages = kwargs.get("messages")
        user = kwargs.get("user")
        stream = kwargs.get("stream")
        pipeline_slug = kwargs.pop("pipeline_slug", None)
        context = kwargs.pop("gentrace", {})
        model_params = {
            k: v for k, v in kwargs.items() if k not in ["messages", "user"]
        }

        content_templates_array = [
            message["contentTemplate"] if "contentTemplate" in message else None
            for message in messages
        ]

        content_inputs_array = [
            message["contentInputs"] if "contentInputs" in message else None
            for message in messages
        ]

        rendered_messages = create_rendered_chat_messages(messages)
        new_kwargs = dict(kwargs, messages=rendered_messages)

        start_time = time.time()
        completion = await super().create(**new_kwargs)

        if stream:
            is_self_contained = (
                    not self.pipeline_run and pipeline_slug
            )
            if is_self_contained:
                pipeline_run_id = str(uuid.uuid4())

            async def profiled_completion():
                modified_response = []
                async for value in completion:
                    if value and is_self_contained:
                        setattr(value, "pipelineRunId", pipeline_run_id)
                    modified_response.append(value)
                    yield value

                end_time = time.time()

                full_response = create_chat_completion_stream_response(
                    modified_response
                )

                elapsed_time = int((end_time - start_time) * 1000)

                pipeline_run = self.pipeline_run

                if is_self_contained:
                    pipeline = Pipeline(
                        slug=pipeline_slug,
                        **self.gentrace_config,
                    )

                    pipeline_run = PipelineRun(
                        pipeline=pipeline,
                        id=pipeline_run_id,
                        context=context,
                    )

                if pipeline_run:
                    pipeline_run.add_step_run(
                        OpenAICreateChatCompletionStepRun(
                            elapsed_time,
                            to_date_string(start_time),
                            to_date_string(end_time),
                            {
                                "messages": messages,
                                "user": user,
                                "contentInputs": content_inputs_array,
                            },
                            {
                                **model_params,
                                "contentTemplates": content_templates_array,
                            },
                            full_response,
                            context,
                        )
                    )

                    if is_self_contained:
                        pipeline_run.submit()

            return profiled_completion()

        end_time = time.time()

        elapsed_time = int((end_time - start_time) * 1000)

        pipeline_run = self.pipeline_run

        is_self_contained = not pipeline_run and pipeline_slug

        if is_self_contained:
            pipeline = Pipeline(
                slug=pipeline_slug,
                **self.gentrace_config
            )

            pipeline_run = PipelineRun(
                pipeline=pipeline,
                context=context,
            )

        if pipeline_run:
            pipeline_run.add_step_run(
                OpenAICreateChatCompletionStepRun(
                    elapsed_time,
                    to_date_string(start_time),
                    to_date_string(end_time),
                    {
                        "messages": messages,
                        "user": user,
                        "contentInputs": content_inputs_array,
                    },
                    {
                        **model_params,
                        "contentTemplates": content_templates_array,
                    },
                    completion.dict(),
                    context,
                )
            )

            if is_self_contained:
                submit_result = pipeline_run.submit()
                setattr(completion, "pipelineRunId",
                        submit_result["pipelineRunId"] if "pipelineRunId" in submit_result else None)

        return completion


class GentraceSyncOpenAI(OpenAI):
    pipeline_run: Optional[PipelineRun] = None

    def __init__(self, *args, **kwargs):
        # print all kwargs
        self.pipeline_run = kwargs.pop("pipeline_run", None)
        self.pipeline = kwargs.pop("pipeline", None)
        self.config = kwargs.pop("gentrace_config")

        super().__init__(*args, **kwargs)

        self.completions = GentraceSyncCompletions(client=self, gentrace_config=self.config,
                                                   pipeline=self.pipeline,
                                                   pipeline_run=self.pipeline_run)
        self.chat = ExtractedChat(self)
        self.chat.completions = GentraceSyncChatCompletions(client=self, gentrace_config=self.config,
                                                            pipeline=self.pipeline,
                                                            pipeline_run=self.pipeline_run)
        self.embeddings = GentraceSyncEmbeddings(client=self, gentrace_config=self.config,
                                                 pipeline=self.pipeline,
                                                 pipeline_run=self.pipeline_run)


class GentraceSyncEmbeddings(ExtractedEmbeddings):

    def __init__(self, *, gentrace_config: Dict[str, Any], client: OpenAI, pipeline: Optional[Pipeline] = None,
                 pipeline_run: Optional[PipelineRun] = None):
        super().__init__(client)

        self.pipeline = pipeline
        self.pipeline_run = pipeline_run
        self.gentrace_config = gentrace_config

    def create(self, *args, **kwargs):
        model = kwargs.get("model")
        pipeline_slug = kwargs.pop("pipeline_slug", None)
        context = kwargs.pop("gentrace", {})
        input_params = {k: v for k, v in kwargs.items() if k not in ["model"]}

        start_time = time.time()
        completion = super().create(**kwargs)
        end_time = time.time()

        elapsed_time = int((end_time - start_time) * 1000)

        pipeline_run = self.pipeline_run

        is_self_contained = not pipeline_run and pipeline_slug

        if is_self_contained:
            pipeline = Pipeline(
                slug=pipeline_slug,
                **self.gentrace_config,
            )

            pipeline_run = PipelineRun(
                pipeline=pipeline,
                context=context,
            )

        if pipeline_run:
            pipeline_run.add_step_run(
                OpenAICreateEmbeddingStepRun(
                    elapsed_time,
                    to_date_string(start_time),
                    to_date_string(end_time),
                    input_params,
                    {"model": model},
                    completion.dict(),
                    context,
                )
            )

            if is_self_contained:
                submit_result = pipeline_run.submit()
                setattr(completion, "pipelineRunId",
                        submit_result["pipelineRunId"] if "pipelineRunId" in submit_result else None)

        return completion


def create_chat_completion_stream_response(stream_list):
    final_response_string = ""
    tool_id_to_info_map = {}
    model = ""
    id_ = ""  # `id` is a built-in function in Python, so we use `id_` instead.
    created = 0

    for value in stream_list:
        model = getattr(value, "model", "")
        id_ = getattr(value, "id", "")
        created = getattr(value, "created", 0)

        if hasattr(value, "choices") and value.choices:
            first_choice = value.choices[0]

            if hasattr(first_choice, "delta") and first_choice.delta:
                if hasattr(first_choice.delta, "tool_calls") and first_choice.delta.tool_calls:
                    for tool_call in first_choice.delta.tool_calls:
                        if tool_call.id:
                            existing_tool_info = tool_id_to_info_map.get(tool_call.id)
                            if not existing_tool_info:
                                tool_id_to_info_map[tool_call.id] = tool_call
                            else:
                                if getattr(existing_tool_info.function, "arguments", None) is not None and \
                                        getattr(tool_call.function, "arguments", None) is not None:
                                    existing_tool_info.function.arguments += tool_call.function.arguments
                        else:
                            if tool_id_to_info_map:
                                tool_id = next(iter(tool_id_to_info_map))
                                existing_tool_info = tool_id_to_info_map[tool_id]
                                if getattr(existing_tool_info.function, "arguments", None) is not None and \
                                        getattr(tool_call.function, "arguments", None) is not None:
                                    existing_tool_info.function.arguments += tool_call.function.arguments

                if hasattr(first_choice.delta, "content") and first_choice.delta.content:
                    final_response_string += first_choice.delta.content
            elif hasattr(first_choice, "finish_reason") and first_choice.finish_reason:
                break

    final_response = {
        "id": id_,
        "object": "chat.completion",
        "created": created,
        "model": model,
        "choices": [
            {
                "finish_reason": None,
                "index": 0,
                "message": {
                    "content": final_response_string,
                    "role": "assistant",
                    "tool_calls": [tool_call.dict() for tool_call in list(tool_id_to_info_map.values())],
                },
            },
        ],
    }

    return final_response


class GentraceSyncChatCompletions(ExtractedChatCompletions):

    def __init__(self, *, gentrace_config: Dict[str, Any], client: OpenAI, pipeline: Optional[Pipeline] = None,
                 pipeline_run: Optional[PipelineRun] = None):
        super().__init__(client)

        self.pipeline = pipeline
        self.pipeline_run = pipeline_run
        self.gentrace_config = gentrace_config

    def create(self, *args, **kwargs):
        messages = kwargs.get("messages")
        user = kwargs.get("user")
        pipeline_slug = kwargs.pop("pipeline_slug", None)
        stream = kwargs.get("stream")
        context = kwargs.pop("gentrace", {})

        model_params = {
            k: v for k, v in kwargs.items() if k not in ["messages", "user"]
        }

        content_templates_array = [
            message["contentTemplate"] if "contentTemplate" in message else None
            for message in messages
        ]

        content_inputs_array = [
            message["contentInputs"] if "contentInputs" in message else None
            for message in messages
        ]

        if stream:
            rendered_messages = create_rendered_chat_messages(messages)
            new_kwargs = dict(kwargs, messages=rendered_messages)
            start_time = time.time()
            completion = super().create(*args, **new_kwargs)

            is_self_contained = (
                    not self.pipeline_run and pipeline_slug
            )
            if is_self_contained:
                pipeline_run_id = str(uuid.uuid4())

            def profiled_completion():
                modified_response = []
                for value in completion:
                    if value and is_self_contained:
                        setattr(value, "pipelineRunId", pipeline_run_id)
                    modified_response.append(value)
                    yield value

                end_time = time.time()

                elapsed_time = int((end_time - start_time) * 1000)

                pipeline_run = self.pipeline_run

                full_response = create_chat_completion_stream_response(
                    modified_response
                )
                if is_self_contained:
                    pipeline = Pipeline(
                        slug=pipeline_slug,
                        **self.gentrace_config,
                    )

                    pipeline_run = PipelineRun(
                        pipeline=pipeline, id=pipeline_run_id, context=context
                    )

                if pipeline_run:
                    pipeline_run.add_step_run(
                        OpenAICreateChatCompletionStepRun(
                            elapsed_time,
                            to_date_string(start_time),
                            to_date_string(end_time),
                            {
                                "messages": messages,
                                "user": user,
                                "contentInputs": content_inputs_array,
                            },
                            {
                                **model_params,
                                "contentTemplates": content_templates_array,
                            },
                            full_response,
                            context,
                        )
                    )

                    if is_self_contained:
                        pipeline_run.submit()

            return profiled_completion()

        rendered_messages = create_rendered_chat_messages(messages)

        new_kwargs = dict(kwargs, messages=rendered_messages)

        start_time = time.time()
        completion = super().create(*args, **new_kwargs)
        end_time = time.time()

        elapsed_time = int((end_time - start_time) * 1000)

        pipeline_run = self.pipeline_run

        is_self_contained = not pipeline_run and pipeline_slug
        if is_self_contained:
            pipeline = Pipeline(
                slug=pipeline_slug,
                **self.gentrace_config,
            )

            pipeline_run = PipelineRun(
                pipeline=pipeline,
                context=context,
            )

        if pipeline_run:
            pipeline_run.add_step_run(
                OpenAICreateChatCompletionStepRun(
                    elapsed_time,
                    to_date_string(start_time),
                    to_date_string(end_time),
                    {
                        "messages": messages,
                        "user": user,
                        "contentInputs": content_inputs_array,
                    },
                    {**model_params, "contentTemplates": content_templates_array},
                    completion.dict(),
                    context,
                )
            )

            if is_self_contained:
                submit_result = pipeline_run.submit()
                setattr(completion, "pipelineRunId",
                        submit_result["pipelineRunId"] if "pipelineRunId" in submit_result else None)

        return completion


def create_rendered_chat_messages(messages):
    new_messages = []
    for message in messages:
        new_message = copy.deepcopy(message)
        if "contentTemplate" in message and "contentInputs" in message:
            new_message["content"] = pystache.render(
                message["contentTemplate"], message["contentInputs"]
            )

            if "contentTemplate" in new_message:
                new_message.pop("contentTemplate", None)

            if "contentInputs" in new_message:
                new_message.pop("contentInputs", None)

        new_messages.append(new_message)

    return new_messages


class GentraceSyncCompletions(ExtractedCompletions):

    def __init__(self, *, gentrace_config: Dict[str, Any], client: OpenAI, pipeline: Optional[Pipeline] = None,
                 pipeline_run: Optional[PipelineRun] = None):
        super().__init__(client)

        self.pipeline = pipeline
        self.pipeline_run = pipeline_run
        self.gentrace_config = gentrace_config

    def create(self, *args, **kwargs):
        prompt_template = kwargs.get("prompt_template")
        prompt_inputs = kwargs.get("prompt_inputs")
        prompt = kwargs.get("prompt")
        pipeline_slug = kwargs.pop("pipeline_slug", None)
        context = kwargs.pop("gentrace", {})
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
            completion = super().create(*args, **new_completion_options)

            is_self_contained = (
                    not self.pipeline_run and pipeline_slug
            )
            if is_self_contained:
                pipeline_run_id = str(uuid.uuid4())

            def profiled_completion():
                modified_response = []
                for value in completion:
                    if value and is_self_contained:
                        setattr(value, "pipelineRunId", pipeline_run_id)
                    modified_response.append(value)
                    yield value

                end_time = time.time()

                full_response = create_completion_stream_response(modified_response)

                create_completion_step_run(
                    self.pipeline_run,
                    pipeline_slug,
                    self.gentrace_config,
                    start_time,
                    end_time,
                    base_completion_options,
                    prompt_template,
                    prompt_inputs,
                    completion,
                    full_response,
                    pipeline_run_id if is_self_contained else None,
                    stream,
                    context,
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
        completion = super().create(*args, **new_completion_options)

        end_time = time.time()

        create_completion_step_run(
            self.pipeline_run,
            pipeline_slug,
            self.gentrace_config,
            start_time,
            end_time,
            base_completion_options,
            prompt_template,
            prompt_inputs,
            completion,
            # Models need to converted from Pydantic to dict
            completion.dict(),
            None,
            stream,
            context,
        )

        return completion


def create_completion_step_run(
        pipeline_run: Optional[PipelineRun],
        pipeline_slug: str,
        gentrace_config: Dict[str, Any],
        start_time,
        end_time,
        base_completion_options,
        prompt_template,
        prompt_inputs,
        completion,
        completion_dict,
        pipeline_run_id: Optional[str] = None,
        stream=False,
        context={},
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

    is_self_contained = not pipeline_run and pipeline_slug

    if is_self_contained:
        pipeline = Pipeline(
            slug=pipeline_slug,
            **gentrace_config,
        )

        pipeline_run = PipelineRun(
            pipeline=pipeline, id=pipeline_run_id, context=context
        )

    if pipeline_run:
        pipeline_run.add_step_run(
            OpenAICreateCompletionStepRun(
                elapsed_time,
                to_date_string(start_time),
                to_date_string(end_time),
                inputs_dict,
                {**partial_model_params, "promptTemplate": prompt_template},
                completion_dict,
                context,
            )
        )

        if is_self_contained:
            submit_result = pipeline_run.submit()

            if not stream:
                setattr(completion, "pipelineRunId",
                        submit_result["pipelineRunId"] if "pipelineRunId" in submit_result else None)


def create_completion_stream_response(stream_list):
    final_response_string = ""
    for value in stream_list:
        if hasattr(value, "choices") and value.choices:
            first_choice = value.choices[0]
            if hasattr(first_choice, "text"):
                final_response_string += first_choice.text
            elif (
                    hasattr(first_choice, "delta")
                    and first_choice.delta
                    and hasattr(first_choice.delta, "content")
            ):
                final_response_string += first_choice.delta.content
            elif (
                    hasattr(first_choice, "finish_reason")
                    and first_choice.finish_reason == "stop"
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


class OpenAICreateCompletionStepRun(StepRun):
    def __init__(
            self,
            elapsed_time,
            start_time,
            end_time,
            inputs,
            model_params,
            response,
            context,
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
            context,
        )
        self.response = response


class OpenAICreateChatCompletionStepRun(StepRun):
    def __init__(
            self,
            elapsed_time,
            start_time,
            end_time,
            inputs,
            model_params,
            response,
            context,
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
            context,
        )
        self.response = response


class OpenAICreateEmbeddingStepRun(StepRun):
    def __init__(
            self,
            elapsed_time,
            start_time,
            end_time,
            inputs,
            model_params,
            response,
            context,
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
            context,
        )
        self.response = response
