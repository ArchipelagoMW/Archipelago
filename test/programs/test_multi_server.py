import unittest
from MultiServer import Context, ServerCommandProcessor


class TestResolvePlayerName(unittest.TestCase):
    def test_resolve(self) -> None:
        p = ServerCommandProcessor(Context("", 0, "", "", 1, 0, 0, False))
        p.ctx.player_names = {
            (0, 1): "AAA",
            (0, 2): "aBc",
            (0, 3): "abC",
        }
        assert not p.resolve_player("abc"), "ambiguous name entry shouldn't resolve to player"
        assert not p.resolve_player("Abc"), "ambiguous name entry shouldn't resolve to player"
        assert p.resolve_player("aBc") == (0, 2, "aBc"), "matching case resolve"
        assert p.resolve_player("abC") == (0, 3, "abC"), "matching case resolve"
        assert not p.resolve_player("aB"), "partial name shouldn't resolve to player"
        assert not p.resolve_player("abCD"), "incorrect name shouldn't resolve to player"

        p.ctx.player_names = {
            (0, 1): "aaa",
            (0, 2): "abc",
            (0, 3): "abC",
        }
        assert p.resolve_player("abc") == (0, 2, "abc"), "matching case resolve"
        assert not p.resolve_player("Abc"), "ambiguous name entry shouldn't resolve to player"
        assert not p.resolve_player("aBc"), "ambiguous name entry shouldn't resolve to player"
        assert p.resolve_player("abC") == (0, 3, "abC"), "matching case resolve"

        p.ctx.player_names = {
            (0, 1): "AbcdE",
            (0, 2): "abc",
            (0, 3): "abCD",
        }
        assert p.resolve_player("abc") == (0, 2, "abc"), "matching case resolve"
        assert p.resolve_player("abC") == (0, 2, "abc"), "case insensitive resolves when 1 match"
        assert p.resolve_player("Abc") == (0, 2, "abc"), "case insensitive resolves when 1 match"
        assert p.resolve_player("ABC") == (0, 2, "abc"), "case insensitive resolves when 1 match"
        assert p.resolve_player("abcd") == (0, 3, "abCD"), "case insensitive resolves when 1 match"
        assert not p.resolve_player("aB"), "partial name shouldn't resolve to player"

        # teams
        p.ctx.teams = 2
        p.ctx._update_teams()
        p.ctx.player_names = {
            (0, 1): "AAA",
            (0, 2): "aBc",
            (0, 3): "abC",
            (1, 1): "AAA",
            (1, 2): "aBc",
            (1, 3): "abC",
        }
        assert not p.resolve_player("AAA"), "missing team entry"
        assert p.resolve_player("aBc@Team1") == (0, 2, "aBc"), "matching case resolve with explicit team"
        assert not p.resolve_player("ABC@Team1"), "ambiguous name entry shouldn't resolve to player"
        assert p.resolve_player("abC@Team2") == (1, 3, "abC"), "incorrect team entry"
        assert not p.resolve_player("AAA@Team3"), "invalid team"
