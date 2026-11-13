import unittest
from unittest.mock import AsyncMock, MagicMock

from MultiServer import (
    Client, Context, ServerCommandProcessor, max_say_length,
    process_client_cmd,  # pyright: ignore[reportUnknownVariableType]
)


class TestResolvePlayerName(unittest.TestCase):
    def test_resolve(self) -> None:
        p = ServerCommandProcessor(Context("", 0, "", "", 0, 0, False))
        p.ctx.player_names = {
            (1, 1): "AAA",
            (1, 2): "aBc",
            (1, 3): "abC",
        }
        assert not p.resolve_player("abc"), "ambiguous name entry shouldn't resolve to player"
        assert not p.resolve_player("Abc"), "ambiguous name entry shouldn't resolve to player"
        assert p.resolve_player("aBc") == (1, 2, "aBc"), "matching case resolve"
        assert p.resolve_player("abC") == (1, 3, "abC"), "matching case resolve"
        assert not p.resolve_player("aB"), "partial name shouldn't resolve to player"
        assert not p.resolve_player("abCD"), "incorrect name shouldn't resolve to player"

        p.ctx.player_names = {
            (1, 1): "aaa",
            (1, 2): "abc",
            (1, 3): "abC",
        }
        assert p.resolve_player("abc") == (1, 2, "abc"), "matching case resolve"
        assert not p.resolve_player("Abc"), "ambiguous name entry shouldn't resolve to player"
        assert not p.resolve_player("aBc"), "ambiguous name entry shouldn't resolve to player"
        assert p.resolve_player("abC") == (1, 3, "abC"), "matching case resolve"

        p.ctx.player_names = {
            (1, 1): "AbcdE",
            (1, 2): "abc",
            (1, 3): "abCD",
        }
        assert p.resolve_player("abc") == (1, 2, "abc"), "matching case resolve"
        assert p.resolve_player("abC") == (1, 2, "abc"), "case insensitive resolves when 1 match"
        assert p.resolve_player("Abc") == (1, 2, "abc"), "case insensitive resolves when 1 match"
        assert p.resolve_player("ABC") == (1, 2, "abc"), "case insensitive resolves when 1 match"
        assert p.resolve_player("abcd") == (1, 3, "abCD"), "case insensitive resolves when 1 match"
        assert not p.resolve_player("aB"), "partial name shouldn't resolve to player"


class TestSayLength(unittest.IsolatedAsyncioTestCase):
    async def say(self, text: str) -> tuple[AsyncMock, MagicMock]:
        ctx = Context("", 0, "", "", 0, 0, False)
        ctx.send_msgs = send_msgs = AsyncMock()
        client = Client(MagicMock(), ctx)
        client.auth = True
        client.messageprocessor = messageprocessor = MagicMock()
        await process_client_cmd(ctx, client, {"cmd": "Say", "text": text})
        return send_msgs, messageprocessor

    async def test_say_at_limit(self) -> None:
        send_msgs, messageprocessor = await self.say("a" * max_say_length)
        messageprocessor.assert_called_once()
        send_msgs.assert_not_called()

    async def test_say_over_limit(self) -> None:
        send_msgs, messageprocessor = await self.say("a" * (max_say_length + 1))
        messageprocessor.assert_not_called()
        self.assertEqual(send_msgs.call_args.args[1][0]["cmd"], "InvalidPacket")
