import unittest
from unittest.mock import AsyncMock, MagicMock

from MultiServer import Client, Context, ServerCommandProcessor, process_client_cmd
from NetUtils import LocationStore
from Utils import Version


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


ACCEPTED_CONNECT = {
    "cmd": "Connect",
    "password": "password",
    "game": "TestGame",
    "name": "Player1",
    "uuid": "uuid1",
    "version": Version(0, 6, 7),
    "items_handling": 0b111,
    "tags": [],
    "slot_data": True,
}

# differs from ACCEPTED_CONNECT in every field a client may change, but is refused for the password
REFUSED_CONNECT = {
    "cmd": "Connect",
    "password": "wrong",
    "game": "TestGame 2",
    "name": "Player2",
    "uuid": "uuid2",
    "version": Version(0, 5, 0),
    "items_handling": 0b001,
    "tags": ["Tracker", "NoText"],
    "slot_data": False,
}


class TestConnect(unittest.IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        self.ctx = Context("", 0, "", "password", 0, 0, False)
        self.ctx.connect_names = {"Player1": (0, 1), "Player2": (0, 2)}
        self.ctx.player_names = {(0, 1): "Player1", (0, 2): "Player2"}
        self.ctx.games = {1: "TestGame", 2: "TestGame 2"}
        self.ctx.minimum_client_versions = {1: Version(0, 5, 0), 2: Version(0, 5, 0)}
        self.ctx.locations = LocationStore({1: {}, 2: {}})
        self.ctx.slot_data = {1: {}, 2: {}}
        self.ctx.clients = {0: {1: [], 2: []}}
        self.ctx.send_msgs = AsyncMock()
        self.ctx.send_encoded_msgs = AsyncMock()
        self.client = Client(MagicMock(), self.ctx)

    async def asyncSetUp(self) -> None:
        await process_client_cmd(self.ctx, self.client, ACCEPTED_CONNECT)
        self.before = self.client_state()

    def client_state(self) -> dict:
        return {name: getattr(self.client, name) for name in Client.__slots__ if name != "__weakref__"}

    async def test_refused_connect_leaves_connection_unchanged(self) -> None:
        await process_client_cmd(self.ctx, self.client, REFUSED_CONNECT)

        self.ctx.send_msgs.assert_awaited_with(
            self.client, [{"cmd": "ConnectionRefused", "errors": ["InvalidPassword"]}]
        )
        self.assertEqual(self.client_state(), self.before)
        self.assertEqual(self.ctx.clients, {0: {1: [self.client], 2: []}})
        self.assertEqual(self.ctx.client_ids, {(0, 1): "uuid1"})

    async def test_accepted_connect_updates_connection(self) -> None:
        await process_client_cmd(self.ctx, self.client, {**REFUSED_CONNECT, "password": "password"})

        connected = self.ctx.send_msgs.await_args.args[1][0]
        self.assertEqual(connected["cmd"], "Connected")
        self.assertEqual(connected["slot"], 2)
        self.assertNotIn("slot_data", connected)
        expected = {
            **self.before,
            "slot": 2,
            "version": REFUSED_CONNECT["version"],
            "tags": REFUSED_CONNECT["tags"],
            "remote_items": False,
            "remote_start_inventory": False,
            "no_locations": True,
            "no_text": True,
        }
        self.assertEqual(self.client_state(), expected)
        self.assertEqual(self.ctx.clients, {0: {1: [], 2: [self.client]}})
        self.assertEqual(self.ctx.client_ids, {(0, 1): "uuid1", (0, 2): "uuid2"})
