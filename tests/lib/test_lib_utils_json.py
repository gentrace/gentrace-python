import json
import warnings
from typing import Any, Dict, List
from dataclasses import dataclass
from typing_extensions import override

import pytest

from gentrace.lib.utils import (
    OTLP_MAX_INT_SIZE,
    OTLP_MIN_INT_SIZE,
    CIRCULAR_REFERENCE_PLACEHOLDER,
    _gentrace_json_dumps,
    gentrace_format_otel_value,
)


class UnserializableObj:
    @override
    def __str__(self) -> str:
        raise TypeError("Cannot be stringified")

    @override
    def __repr__(self) -> str:
        return "UnserializableObjRepr"


@dataclass
class MyDataClass:
    x: int
    s: str


def test_json_dumps_basic_types() -> None:
    assert _gentrace_json_dumps(None) == "null"
    assert _gentrace_json_dumps(True) == "true"
    assert _gentrace_json_dumps(False) == "false"
    assert _gentrace_json_dumps(123) == "123"
    assert _gentrace_json_dumps(123.45) == "123.45"
    assert _gentrace_json_dumps("hello world") == '"hello world"'


def test_json_dumps_collections() -> None:
    assert _gentrace_json_dumps([1, "a", True]) == '[1, "a", true]'
    assert _gentrace_json_dumps((1, "a", True)) == '[1, "a", true]'
    assert _gentrace_json_dumps({"key1": "value1", "key2": 123}) == '{"key1": "value1", "key2": 123}'
    assert _gentrace_json_dumps([]) == "[]"
    assert _gentrace_json_dumps({}) == "{}"


def test_json_dumps_nested_collections() -> None:
    nested_list = [1, ["a", "b"], {"key": [2, 3]}]
    expected_json_list = '[1, ["a", "b"], {"key": [2, 3]}]'
    assert _gentrace_json_dumps(nested_list) == expected_json_list

    nested_dict = {"outer_key": [1, {"inner_key": "value"}]}
    expected_json_dict = '{"outer_key": [1, {"inner_key": "value"}]}'
    assert _gentrace_json_dumps(nested_dict) == expected_json_dict


def test_json_dumps_custom_objects() -> None:
    my_instance = MyDataClass(x=1, s="test")
    assert _gentrace_json_dumps(my_instance) == f'"{str(my_instance)}"'
    assert _gentrace_json_dumps(UnserializableObj()) == f'"[UnserializableType: UnserializableObj]"'


def test_json_dumps_circular_list() -> None:
    a: List[Any] = [1, 2]
    a.append(a)
    with pytest.warns(UserWarning, match="Fallback to placeholder for entire value due to complex circular reference"):
        assert _gentrace_json_dumps(a) == json.dumps(CIRCULAR_REFERENCE_PLACEHOLDER)


def test_json_dumps_circular_dict() -> None:
    a: Dict[str, Any] = {"key1": "value1"}
    a["self"] = a
    with pytest.warns(UserWarning, match="Fallback to placeholder for entire value due to complex circular reference"):
        assert _gentrace_json_dumps(a) == json.dumps(CIRCULAR_REFERENCE_PLACEHOLDER)


def test_json_dumps_mutual_circular_references() -> None:
    obj1: Dict[str, Any] = {"name": "obj1"}
    obj2: Dict[str, Any] = {"name": "obj2"}
    obj1["ref_to_obj2"] = obj2
    obj2["ref_to_obj1"] = obj1

    with pytest.warns(UserWarning, match="Fallback to placeholder for entire value due to complex circular reference"):
        assert _gentrace_json_dumps(obj1) == json.dumps(CIRCULAR_REFERENCE_PLACEHOLDER)

    with pytest.warns(UserWarning, match="Fallback to placeholder for entire value due to complex circular reference"):
        assert _gentrace_json_dumps(obj2) == json.dumps(CIRCULAR_REFERENCE_PLACEHOLDER)


def test_gentrace_format_otel_value_int_range() -> None:
    assert gentrace_format_otel_value(OTLP_MAX_INT_SIZE) == OTLP_MAX_INT_SIZE
    assert gentrace_format_otel_value(OTLP_MIN_INT_SIZE) == OTLP_MIN_INT_SIZE

    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        assert gentrace_format_otel_value(OTLP_MAX_INT_SIZE + 1) == str(OTLP_MAX_INT_SIZE + 1)
        assert len(w) == 1
        assert issubclass(w[-1].category, UserWarning)
        assert "outside the OTLP 64-bit signed integer range" in str(w[-1].message)

    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        assert gentrace_format_otel_value(OTLP_MIN_INT_SIZE - 1) == str(OTLP_MIN_INT_SIZE - 1)
        assert len(w) == 1
        assert issubclass(w[-1].category, UserWarning)
        assert "outside the OTLP 64-bit signed integer range" in str(w[-1].message)


def test_gentrace_format_otel_value_complex_object_uses_safe_dumper() -> None:
    circular_list: List[Any] = [1]
    circular_list.append(circular_list)
    with pytest.warns(UserWarning, match="Fallback to placeholder for entire value due to complex circular reference"):
        assert gentrace_format_otel_value(circular_list) == json.dumps(CIRCULAR_REFERENCE_PLACEHOLDER)


def test_shared_object_not_circular() -> None:
    shared_obj = {"shared": "data"}
    container = [shared_obj, shared_obj]
    assert _gentrace_json_dumps(container) == '[{"shared": "data"}, {"shared": "data"}]'


def test_complex_object_within_list() -> None:
    my_item1 = MyDataClass(x=1, s="a")
    my_item2 = MyDataClass(x=2, s="b")
    data = [my_item1, my_item2]
    expected_json = f'["{str(my_item1)}", "{str(my_item2)}"]'
    assert _gentrace_json_dumps(data) == expected_json


def test_list_of_unserializable() -> None:
    data = [1, UnserializableObj(), 3]
    expected = f'[1, "[UnserializableType: UnserializableObj]", 3]'
    assert _gentrace_json_dumps(data) == expected


def test_dict_with_unserializable_value() -> None:
    data = {"a": 1, "b": UnserializableObj(), "c": 3}
    expected = f'{{"a": 1, "b": "[UnserializableType: UnserializableObj]", "c": 3}}'
    assert _gentrace_json_dumps(data) == expected
