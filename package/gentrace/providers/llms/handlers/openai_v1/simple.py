from typing import Optional, Type, cast

from openai import OpenAI

from gentrace.providers.init import GENTRACE_CONFIG_STATE


class LazyLoader:
    _module: Optional[Type] = None

    @classmethod
    def _load_module(cls) -> Type:
        if cls._module is None:
            from gentrace.providers.llms.openai_v1 import (
                GentraceAsyncOpenAI as _GentraceAsyncOpenAI,
            )
            from gentrace.providers.llms.openai_v1 import (
                GentraceSyncOpenAI as _GentraceSyncOpenAI,
            )
            cls._module = {
                "GentraceSyncOpenAI": _GentraceSyncOpenAI,
                "GentraceAsyncOpenAI": _GentraceAsyncOpenAI,
            }
        return cls._module


class SimpleGentraceSyncOpenAI:
    def __init__(self, *args, **kwargs):
        if not GENTRACE_CONFIG_STATE["GENTRACE_API_KEY"]:
            raise ValueError(
                "No Gentrace API key available. Please use init() to set the API key."
            )

        gentrace_config = {
            "api_key": GENTRACE_CONFIG_STATE["GENTRACE_API_KEY"],
            "host": GENTRACE_CONFIG_STATE["GENTRACE_BASE_PATH"],
        }


        GentraceSyncOpenAI = LazyLoader._load_module()["GentraceSyncOpenAI"]
        self._instance = GentraceSyncOpenAI(*args, **kwargs, gentrace_config=gentrace_config)

    def __getattr__(self, name):
        return getattr(self._instance, name)

SimpleGentraceSyncOpenAITyped = cast(OpenAI, SimpleGentraceSyncOpenAI)


class SimpleGentraceAsyncOpenAI:

    def __init__(self, *args, **kwargs):
        if not GENTRACE_CONFIG_STATE["GENTRACE_API_KEY"]:
            raise ValueError(
                "No Gentrace API key available. Please use init() to set the API key."
            )

        gentrace_config = {
            "api_key": GENTRACE_CONFIG_STATE["GENTRACE_API_KEY"],
            "host": GENTRACE_CONFIG_STATE["GENTRACE_BASE_PATH"],
        }

        GentraceAsyncOpenAI = LazyLoader._load_module()["GentraceAsyncOpenAI"]
        self._instance = GentraceAsyncOpenAI(*args, **kwargs, gentrace_config=gentrace_config)

    def __getattr__(self, name):
        return getattr(self._instance, name)


SimpleGentraceAsyncOpenAITyped = cast(OpenAI, SimpleGentraceAsyncOpenAI)

__all__ = [
    "SimpleGentraceSyncOpenAITyped",
    "SimpleGentraceAsyncOpenAITyped"
]
