import openai
import openai.api_resources as api

from openai import ChatCompletion

import inspect
import pinecone

init_args = inspect.signature(pinecone.init).parameters.keys()

print("init args", init_args)

a = "api_key"
b = "value"

setattr(openai, a, b)

print('testing', openai.api_key)

print("audio", getattr(openai, "Audio"))

print('audio 2', getattr(api, "Audio"))

