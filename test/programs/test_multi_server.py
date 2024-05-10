import unittest
from MultiServer import Context, ServerCommandProcessor


class TestResolvePlayerName(unittest.TestCase):
    def test_resolve(self) -> None:
        p = ServerCommandProcessor(Context("", 0, "", "", 0, 0, False))
        p.ctx.player_names = {
            (1, 1): "AAA",
            (1, 2): "aBc",
            (1, 3): "a bc",
        }

        self.assertEqual(p.resolve_player("aBc"), (1, 2, "aBc"), "matching case resolve")
        self.assertEqual(p.resolve_player("a_Bc"), (1, 3, "a bc"), "underscore should resolve to space")

        self.assertFalse(p.resolve_player("aB"), "partial name shouldn't resolve to player")
        self.assertFalse(p.resolve_player("abCD"), "incorrect name shouldn't resolve to player")

        p = ServerCommandProcessor(Context("", 0, "", "", 0, 0, False))
        p.ctx.player_names = {
            (1, 1): "AbcdE",
            (1, 2): "abc",
            (1, 3): "abCD",
        }
        self.assertEqual(p.resolve_player("abc"), (1, 2, "abc"), "matching case resolve")
        self.assertEqual(p.resolve_player("abC"), (1, 2, "abc"), "case insensitive resolves when 1 match")
        self.assertEqual(p.resolve_player("Abc"), (1, 2, "abc"), "case insensitive resolves when 1 match")
        self.assertEqual(p.resolve_player("ABC"), (1, 2, "abc"), "case insensitive resolves when 1 match")
        self.assertEqual(p.resolve_player("abcd"), (1, 3, "abCD"), "case insensitive resolves when 1 match")

        self.assertFalse(p.resolve_player("aB"), "partial name shouldn't resolve to player")

