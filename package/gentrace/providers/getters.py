import os
import re

import openai
from urllib3.util import parse_url

from gentrace.configuration import Configuration as GentraceConfiguration

openai.api_key = os.getenv("OPENAI_KEY")


def test_validity():
    from gentrace import api_key, host

    if not api_key:
        raise ValueError("Gentrace API key not set")

    # Totally fine (and expected) to not have a host set
    if not host:
        return

    path = parse_url(host).path

    if host and path != "/api/v1" and path != "/api/v1/":
        raise ValueError("Gentrace host is invalid")


def configure_openai():
    from gentrace import api_key, host

    from .llms.openai import annotate_openai_module

    test_validity()

    resolved_host = host if host else "https://gentrace.ai/api/v1"

    gentrace_config = GentraceConfiguration(host=resolved_host)
    gentrace_config.access_token = api_key

    annotate_openai_module(gentrace_config=gentrace_config)


def configure_pinecone():
    from .vectorstores.pinecone import annotate_pinecone_module

    test_validity()

    annotate_pinecone_module()


__all__ = ["configure_openai", "configure_pinecone"]
