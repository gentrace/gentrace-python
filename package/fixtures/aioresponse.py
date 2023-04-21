import pytest
from aioresponses import aioresponses


@pytest.fixture
def mockaio():
    with aioresponses() as m:
        yield m
