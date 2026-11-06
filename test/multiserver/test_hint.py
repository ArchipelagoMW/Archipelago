import unittest
from types import SimpleNamespace
from unittest.mock import AsyncMock, Mock

from MultiServer import (
    ClientMessageProcessor, Context, collect_hints,
    collect_hint_location_id, format_hint, process_client_cmd,
)
from NetUtils import HintStatus, NetworkSlot, SlotType, _LocationStore
from Utils import restricted_dumps, restricted_loads


class TestHintMode(unittest.TestCase):
    def setUp(self):
        self.ctx = Context("", 0, "", "", 1, 50, False, hint_mode="all")
        self.ctx.locations = _LocationStore({
            1: {100: (200, 1, 1), 101: (201, 2, 2)},
            2: {102: (200, 1, 1)},
        })
        self.ctx.games = {1: "Test Game", 2: "Test Game"}
        self.ctx.slot_info = {
            slot: NetworkSlot(f"Player {slot}", "Test Game", SlotType.player) for slot in (1, 2)
        }
        self.ctx.player_names = {(0, slot): f"Player {slot}" for slot in (1, 2)}
        self.ctx.item_names["Test Game"].update({200: "Progression Item", 201: "Useful Item"})
        self.ctx.location_names["Test Game"].update({100: "Local Check", 101: "Remote Check", 102: "Other Check"})
        self.ctx.er_hint_data = {1: {100: "Secret Entrance"}}

    def make_processor(self):
        self.ctx.clients = {0: {1: [], 2: []}}
        self.ctx.broadcast = Mock()
        processor = ClientMessageProcessor(self.ctx, SimpleNamespace(team=0, slot=1))
        processor.output = Mock()
        return processor

    def test_item_and_location_modes(self):
        for mode, local_hidden, remote_hidden in (
            ("default", False, False), ("own", True, False), ("all", True, True),
        ):
            with self.subTest(mode=mode):
                self.ctx.hint_mode = mode
                hints = collect_hints(self.ctx, 0, 1, 200)
                self.assertEqual([hint.hidden for hint in hints], [local_hidden, remote_hidden])
                self.assertTrue(all(not hint.item_hidden for hint in hints))
                local = collect_hint_location_id(self.ctx, 0, 1, 100)[0]
                remote = collect_hint_location_id(self.ctx, 0, 1, 101)[0]
                self.assertEqual((local.item_hidden, remote.item_hidden), (local_hidden, remote_hidden))
                self.assertFalse(local.hidden or remote.hidden)

    def test_own_mode_conceals_item_link_placements(self):
        self.ctx.hint_mode = "own"
        self.ctx.groups = {3: {1, 2}}
        self.ctx.locations[1][100] = (200, 3, 1)
        self.assertTrue(collect_hints(self.ctx, 0, 1, 200)[0].hidden)
        self.assertTrue(collect_hint_location_id(self.ctx, 0, 1, 100)[0].item_hidden)

    def test_checked_hints_are_visible(self):
        self.ctx.location_checks[0, 1].add(100)
        item_hint = collect_hints(self.ctx, 0, 1, 200)[0]
        location_hint = collect_hint_location_id(self.ctx, 0, 1, 100)[0]
        for hint in (item_hint, location_hint):
            self.assertFalse(hint.hidden or hint.item_hidden)
            self.assertEqual(hint.status, HintStatus.HINT_FOUND)

    def test_cannot_afford_reveal_keeps_hint(self):
        processor = self.make_processor()
        hint = collect_hint_location_id(self.ctx, 0, 1, 101)[0]
        self.ctx.notify_hints(0, [hint])
        processor.get_hints("101", for_location=True)
        self.assertEqual(self.ctx.hints[0, 1], {hint})
        self.assertEqual(self.ctx.hints[0, 2], {hint})
        self.assertEqual(self.ctx.hints_used[0, 1], 0)

    def test_paid_reveal_updates_both_players(self):
        processor = self.make_processor()
        hint = collect_hint_location_id(self.ctx, 0, 1, 101)[0]
        self.ctx.notify_hints(0, [hint])
        self.ctx.location_checks[0, 1].add(100)
        processor.get_hints("101", for_location=True)
        revealed = hint._replace(hidden=False, item_hidden=False)
        self.assertEqual(self.ctx.hints[0, 1], {revealed})
        self.assertEqual(self.ctx.hints[0, 2], {revealed})
        self.assertEqual(self.ctx.hints_used[0, 1], 1)
        processor.get_hints("101", for_location=True)
        self.assertEqual(self.ctx.hints_used[0, 1], 1)

    def test_free_reveal(self):
        processor = self.make_processor()
        self.ctx.hint_cost = 0
        hint = collect_hint_location_id(self.ctx, 0, 1, 100)[0]
        self.ctx.notify_hints(0, [hint])
        processor.get_hints("100", for_location=True)
        self.assertFalse(next(iter(self.ctx.hints[0, 1])).item_hidden)

    def test_group_reveal_updates_all_members(self):
        processor = self.make_processor()
        self.ctx.groups = {3: {1, 2}}
        self.ctx.slot_info[3] = NetworkSlot("Linked Players", "Test Game", SlotType.group, (1, 2))
        self.ctx.player_names[0, 3] = "Linked Players"
        self.ctx.locations[1][101] = (201, 3, 2)
        hint = collect_hint_location_id(self.ctx, 0, 1, 101)[0]
        self.ctx.notify_hints(0, [hint])
        self.ctx.location_checks[0, 1].add(100)
        processor.get_hints("101", for_location=True)
        for slot in (1, 2):
            self.assertEqual(self.ctx.hints[0, slot], {hint._replace(item_hidden=False)})

    def test_save_mode_and_legacy_save(self):
        saved = restricted_loads(restricted_dumps(self.ctx.get_save()))
        restored = Context("", 0, "", "", 1, 50, False)
        restored.set_save(saved)
        self.assertEqual(restored.hint_mode, "all")
        del saved["game_options"]["hint_mode"]
        restored.hint_mode = "own"
        restored.set_save(saved)
        self.assertEqual(restored.hint_mode, "own")

    def test_console_format_conceals_details(self):
        item_hint = collect_hints(self.ctx, 0, 1, 200)[0]
        text = format_hint(self.ctx, 0, item_hint)
        self.assertNotIn("Local Check", text)
        self.assertNotIn("Secret Entrance", text)
        location_hint = collect_hint_location_id(self.ctx, 0, 1, 100)[0]
        text = format_hint(self.ctx, 0, location_hint)
        self.assertIn("Local Check", text)
        self.assertIn("progression", text)
        self.assertNotIn("Progression Item", text)


class TestGameCreatedHints(unittest.IsolatedAsyncioTestCase):
    async def test_game_created_hints_remain_visible(self):
        for command in ("LocationScouts", "CreateHints"):
            with self.subTest(command=command):
                ctx = Context("", 0, "", "", 1, 50, False, hint_mode="all")
                ctx.locations = _LocationStore({1: {100: (200, 1, 1)}})
                ctx.clients = {0: {1: []}}
                ctx.slot_info = {1: NetworkSlot("Player", "Test Game", SlotType.player)}
                ctx.player_names = {(0, 1): "Player"}
                ctx.send_msgs = AsyncMock()
                ctx.broadcast = Mock()
                client = SimpleNamespace(team=0, slot=1, auth=True)
                await process_client_cmd(ctx, client, {
                    "cmd": command, "locations": [100], "create_as_hint": 1,
                })
                hint = next(iter(ctx.hints[0, 1]))
                self.assertFalse(hint.hidden or hint.item_hidden)
