"""Tests for serializers module."""

import json
from datetime import datetime

import pytest

from apiforge.serializers import JSONSerializer, BaseSerializer


class TestJSONSerializer:
    def test_dumps_string(self):
        s = JSONSerializer()
        result = s.dumps({"key": "value"})
        assert result == '{"key": "value"}'

    def test_dumps_integer(self):
        s = JSONSerializer()
        result = s.dumps(42)
        assert result == "42"

    def test_dumps_list(self):
        s = JSONSerializer()
        result = s.dumps([1, 2, 3])
        assert result == "[1, 2, 3]"

    def test_dumps_none(self):
        s = JSONSerializer()
        result = s.dumps(None)
        assert result == "null"

    def test_dumps_nested(self):
        s = JSONSerializer()
        data = {"a": [1, 2], "b": {"c": True}}
        result = s.dumps(data)
        parsed = json.loads(result)
        assert parsed == data

    def test_loads_string(self):
        s = JSONSerializer()
        result = s.loads('{"key": "value"}')
        assert result == {"key": "value"}

    def test_loads_bytes(self):
        s = JSONSerializer()
        result = s.loads(b'{"key": "value"}')
        assert result == {"key": "value"}

    def test_loads_list(self):
        s = JSONSerializer()
        result = s.loads("[1, 2, 3]")
        assert result == [1, 2, 3]

    def test_roundtrip(self):
        s = JSONSerializer()
        data = {"name": "test", "values": [1, 2, 3], "nested": {"a": True}}
        result = s.loads(s.dumps(data))
        assert result == data

    def test_dumps_invalid_object_raises(self):
        s = JSONSerializer()
        with pytest.raises(TypeError):
            s.dumps(datetime.now())

    def test_loads_invalid_json_raises(self):
        s = JSONSerializer()
        with pytest.raises(json.JSONDecodeError):
            s.loads("not valid json {{{")

    def test_loads_empty_string_raises(self):
        s = JSONSerializer()
        with pytest.raises(json.JSONDecodeError):
            s.loads("")

    def test_dumps_with_indent(self):
        s = JSONSerializer(indent=2)
        result = s.dumps({"key": "value"})
        assert "\n" in result
        assert "  " in result

    def test_dumps_with_sort_keys(self):
        s = JSONSerializer(sort_keys=True)
        result = s.dumps({"b": 2, "a": 1})
        assert '"a": 1' in result
        assert '"b": 2' in result

    def test_dumps_with_ensure_ascii_false(self):
        s = JSONSerializer(ensure_ascii=False)
        result = s.dumps({"text": "привет"})
        assert "привет" in result

    def test_dumps_with_ensure_ascii_true(self):
        s = JSONSerializer(ensure_ascii=True)
        result = s.dumps({"text": "привет"})
        assert "\\u043f" in result

    def test_loads_bool(self):
        s = JSONSerializer()
        assert s.loads("true") is True
        assert s.loads("false") is False

    def test_loads_number(self):
        s = JSONSerializer()
        assert s.loads("42") == 42
        assert s.loads("3.14") == 3.14


class TestBaseSerializer:
    def test_cannot_instantiate_base(self):
        with pytest.raises(TypeError):
            BaseSerializer()
