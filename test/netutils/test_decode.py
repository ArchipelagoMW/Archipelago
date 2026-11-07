import unittest
from typing import Any

from NetUtils import decode, encode


class DecodeDepthLimitTest(unittest.TestCase):
    LIMIT = 16

    @staticmethod
    def make_data(depth: int = LIMIT, cmd: str = "Cmd") -> list[dict[str, Any]]:
        arg: Any = [1]
        for _ in range(depth - 4):
            arg = [arg]
        res = {"cmd": cmd, "arg": arg}
        # [{"arg": [[...[1]...]]}]
        # ^1             ^depth
        return [res]

    @classmethod
    def make_message(cls, depth: int = LIMIT, cmd: str = "Cmd") -> str:
        return encode(cls.make_data(depth, cmd=cmd))

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
            decode(self.make_message()[:-1])

    def test_invalid(self) -> None:
        with self.assertRaises(ValueError):
            decode(self.make_message().replace(":", ","))

    def test_braces_in_str(self) -> None:
        # should not raise
        decode(self.make_message(cmd="["))
        decode(self.make_message(cmd="{"))
        decode(self.make_message(cmd="}"))
        decode(self.make_message(cmd="]"))

    def test_quote_in_str(self) -> None:
        # should not raise
        decode(self.make_message(cmd='"'))

    def test_bs_quote_in_str(self) -> None:
        # should not raise
        decode(self.make_message(cmd=r'\"'))

    def test_quoted_braces_in_str(self) -> None:
        # should not raise
        decode(self.make_message(cmd='"{["'))

    def test_escape(self) -> None:
        # should not raise
        decode(r"""["\"\\\/\b\f\n\r\t{"]""")
        self.assertEqual("new\nline", decode(r'"new\u000Aline"'))
