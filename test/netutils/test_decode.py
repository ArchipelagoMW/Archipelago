import unittest
from typing import Any

from NetUtils import decode, encode


class DecodeDepthLimitTest(unittest.TestCase):
    LIMIT = 16

    @staticmethod
    def make_data(depth: int) -> list[dict[str, Any]]:
        arg: Any = [1]
        for _ in range(depth - 4):
            arg = [arg]
        cmd = {"command": "} A command [{", "arg": arg}
        # [{"arg": [[...[1]...]]}]
        # ^1             ^depth
        return [cmd]

    @classmethod
    def make_message(cls, depth: int) -> str:
        return encode(cls.make_data(depth))

    def test_below_limit(self) -> None:
        data = self.make_data(depth=self.LIMIT - 1)
        message = encode(data)
        self.assertEqual(data, decode(message))

    def test_at_limit(self) -> None:
        data = self.make_data(depth=self.LIMIT)
        message = encode(data)
        self.assertEqual(data, decode(message))

    def test_above_limit(self) -> None:
        with self.assertRaises(ValueError):
            decode(self.make_message(depth=self.LIMIT + 1))

    def test_incomplete(self) -> None:
        with self.assertRaises(ValueError):
            decode(self.make_message(depth=self.LIMIT)[:-1])

    def test_invalid(self) -> None:
        with self.assertRaises(ValueError):
            decode(self.make_message(depth=self.LIMIT).replace(":", ","))
