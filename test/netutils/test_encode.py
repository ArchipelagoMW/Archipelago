import json
import unittest
from typing import Any, NamedTuple

from NetUtils import encode, _scan_for_TypedTuples


class EncodeTest(unittest.TestCase):
    def test_circular_array(self) -> None:
        arg: list[Any] = []
        arg.append(arg)
        with self.assertRaises(RecursionError):
            encode(arg)

    def test_named_tuple(self) -> None:
        class Obj(NamedTuple):
            a: int = 1
            z: int = 2

        obj = Obj()
        expected = """{"a":1,"z":2,"class":"Obj"}"""
        self.assertEqual(expected, encode(obj))
        # compare to legacy json
        self.assertEqual(expected, json.dumps(_scan_for_TypedTuples(obj), separators=(",", ":")))
