import os
import re

import openai

from gentrace.configuration import Configuration as GentraceConfiguration

openai.api_key = os.getenv("OPENAI_KEY")


VALID_GENTRACE_HOST = r"^https?://[\w.-]+:\d{1,5}/api/v1/?$"


def test_validity():
    from gentrace import api_key, host

    if not api_key:
        raise ValueError("Gentrace API key not set")

    if host and not re.match(VALID_GENTRACE_HOST, host):
        raise ValueError("Gentrace host is invalid")


def configure_openai():
    from gentrace import api_key, host

    from .llms.openai import annotate_openai_module

    test_validity()

    if host and not re.match(VALID_GENTRACE_HOST, host):
        raise ValueError("Gentrace host is invalid")

    gentrace_config = GentraceConfiguration(host=host)
    gentrace_config.access_token = api_key

    annotate_openai_module(gentrace_config=gentrace_config)


def configure_pinecone():
    from .vectorstores.pinecone import annotate_pinecone_module

    test_validity()

    annotate_pinecone_module()


__all__ = ["configure_openai", "configure_pinecone"]
