import json
import unittest
from typing import Any

from NetUtils import decode, encode, _object_hook, NetworkItem, NetworkPlayer, NetworkSlot, SlotType
from Utils import Version


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
        decode(self.make_message(cmd=r"\""))

    def test_quoted_braces_in_str(self) -> None:
        # should not raise
        decode(self.make_message(cmd='"{["'))


class DecodeTest(unittest.TestCase):
    def test_escape(self) -> None:
        self.assertEqual(["\"\\/\b\f\n\r\t{"], decode(r'["\"\\\/\b\f\n\r\t{"]'))  # fmt: skip
        self.assertEqual("new\nline", decode(r'"new\u000Aline"'))

    def test_bad_escape(self) -> None:
        with self.assertRaises(ValueError):
            decode("\\{")

    def test_non_ascii(self) -> None:
        self.assertEqual("ä", decode('"ä"'))

    def test_bigint(self) -> None:
        n = 2**64
        decoded = decode(str(2**64))
        self.assertEqual(n, decoded)
        self.assertIsInstance(decoded, int)

    def test_tab(self) -> None:
        self.assertEqual([1, 2], decode("[1,\t2]"))

    def test_space(self) -> None:
        self.assertEqual([1, 2], decode("  [  1  ,  2  ]  "))

    def test_lf(self) -> None:
        self.assertEqual([1, 2], decode("[1\n,2]"))

    def test_cr(self) -> None:
        self.assertEqual([1, 2], decode("[1\r,2]"))


class HookTest(unittest.TestCase):
    @staticmethod
    def original_loads(s: str) -> Any:
        return json.loads(s, object_hook=_object_hook)

    def test_lower_case_version(self) -> None:
        s = """{"class": "Version", "major": 1, "minor": 2, "build": 3}"""
        expected = Version(1, 2, 3)
        self.assertEqual(expected, decode(s))
        self.assertEqual(expected, self.original_loads(s))  # compare to original implementation

    def test_upper_case_version(self) -> None:
        s = """{"class": "Version", "Major": 1, "Minor": 2, "Build": 3}"""
        expected = Version(1, 2, 3)
        self.assertEqual(expected, decode(s))
        self.assertEqual(expected, self.original_loads(s))  # compare to original implementation

    def test_partial_version(self) -> None:
        s = """{"class": "Version", "Major": 1}"""
        expected = KeyError  # missing key
        with self.assertRaises(expected):
            decode(s)
        with self.assertRaises(expected):
            self.original_loads(s)  # compare to original implementation

    def test_network_player(self) -> None:
        expected = NetworkPlayer(team=1, slot=2, alias="Alias", name="Name")
        s = encode(expected)
        self.assertEqual(expected, decode(s))

    def test_incomplete_network_player(self) -> None:
        s = """{"class": "NetworkPlayer", "team": 1, "slot": 2, "name": "Name"}"""
        expected = TypeError  # bad call to __init__
        with self.assertRaises(expected):
            decode(s)
        with self.assertRaises(expected):
            self.original_loads(s)  # compare to original implementation

    def test_network_item(self) -> None:
        expected = NetworkItem(item=1, location=2, player=3, flags=4)
        s = encode(expected)
        self.assertEqual(expected, decode(s))

    def test_incomplete_network_item(self) -> None:
        s = """{"class": "NetworkItem", "item": 1, "location": 2}"""
        expected = TypeError  # bad call to __init__
        with self.assertRaises(expected):
            decode(s)
        with self.assertRaises(expected):
            self.original_loads(s)  # compare to original implementation

    def test_partial_network_item(self) -> None:
        # flags are optional
        s = """{"class": "NetworkItem", "item": 1, "location": 2, "player": 3}"""
        expected = NetworkItem(item=1, location=2, player=3)
        self.assertEqual(expected, decode(s))

    def test_network_slot(self) -> None:
        expected = NetworkSlot(name="Name", game="Game", type=SlotType.group, group_members=[1, 2, 3])
        s = encode(expected)
        self.assertEqual(expected, decode(s))

    def test_partial_network_slot(self) -> None:
        # group_members are optional
        s = """{"class": "NetworkSlot", "name": "Name", "game": "Game", "type": 0}"""
        expected = NetworkSlot(name="Name", game="Game", type=SlotType.spectator)
        self.assertEqual(expected, decode(s))

    def test_incomplete_network_slot(self) -> None:
        s = """{"class": "NetworkSlot", "name": "Name", "game": "Game"}"""
        expected = TypeError  # bad call to __init__
        with self.assertRaises(expected):
            decode(s)
        with self.assertRaises(expected):
            self.original_loads(s)  # compare to original implementation

    def test_tests_complete(self) -> None:
        from NetUtils import allowlist, custom_hooks

        tested = {"NetworkPlayer", "NetworkItem", "NetworkSlot", "Version"}
        hooked = set(allowlist.keys()) | set(custom_hooks.keys())
        self.assertEqual(hooked, tested, f"Missing tests for {', '.join(sorted(hooked - tested))}")
