import asyncio
import struct
import unittest
from unittest.mock import AsyncMock, Mock, patch

from NetUtils import NetworkItem

from .. import TWWClient
from ..Memory import APBridgeError, APBridgeRemoteError, DolphinMemory, WiiMemory
from .test_memory import FakeAPBridge, FakeWRTXCache


class FakeTWW:
    """Small memory image with a game-consumed item queue and identity chart map."""

    def __init__(self):
        self.data = {}
        self.put(0x80000000, b"GZLE99")
        self.put(TWWClient.CURR_STAGE_NAME_ADDR, b"sea\0\0\0\0\0")
        self.put(TWWClient.CURR_STAGE_ID_ADDR, b"\x01")
        self.put(TWWClient.SLOT_NAME_ADDR, b"Wii Test Slot\0")
        self.put(TWWClient.CURR_HEALTH_ADDR, b"\x00\x0C")
        self.put(TWWClient.GIVE_ITEM_ARRAY_ADDR, b"\xFF" * 16)
        self.put(TWWClient.CHARTS_MAPPING_ADDR, b"".join(i.to_bytes(2, "big") for i in range(1, 50)))
        self.delivered = []
        self.write_cache = FakeWRTXCache(self.apply_write)
        self.drop_ack = None
        self.drop_ack_counts = {}
        self.reject_write = None

    def put(self, address, data):
        self.data.update((address + offset, value) for offset, value in enumerate(data))

    def read(self, address, length):
        return bytes(self.data.get(address + offset, 0) for offset in range(length))

    def apply_write(self, address, payload):
        self.put(address, payload)
        if TWWClient.GIVE_ITEM_ARRAY_ADDR <= address < TWWClient.GIVE_ITEM_ARRAY_ADDR + 16:
            self.delivered.extend(payload)
            self.put(address, b"\xFF" * len(payload))

    def reply(self, request):
        if request == b"HELLO":
            return b"NIN-AP"
        address, length = struct.unpack(">IH", request[4:10])
        if request[:4] == b"READ":
            return b"DATA" + request[4:12] + self.read(address, length)
        if request[:4] != b"WRTX":
            raise ValueError(f"Unexpected write magic: {request[:4]!r}")
        if address == self.reject_write:
            return b"ERR!" + request[4:10] + b"\x02\x00" + request[12:20]
        reply = self.write_cache.reply(request)
        if reply[:4] == b"ERR!":
            return reply
        if address == self.drop_ack:
            return None
        if self.drop_ack_counts.get(address, 0):
            self.drop_ack_counts[address] -= 1
            return None
        return reply


class TestTWWClient(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.ctx = TWWClient.TWWContext(None, None)
        self.processor = TWWClient.TWWCommandProcessor(self.ctx)
        self.processor.output = Mock()

    async def asyncTearDown(self):
        self.ctx.memory.un_hook()
        await self.ctx.shutdown()

    def use_wii(self, peer):
        self.ctx.memory = WiiMemory("127.0.0.1", peer.port, timeout=0.15)
        self.ctx.memory.hook()
        self.ctx.console_status = self.ctx.connected_status

    def give_test_item(self):
        item_id = next(apid for apid, name in TWWClient.LOOKUP_ID_TO_NAME.items() if name == "Grappling Hook")
        self.ctx.items_received = [NetworkItem(item_id, 1, 1)]

    async def test_default_and_status_commands(self):
        self.assertIsInstance(self.ctx.memory, DolphinMemory)
        self.assertTrue(self.processor._cmd_console())
        self.assertIn("Dolphin", self.processor.output.call_args.args[0])
        with self.assertLogs("Client", level="INFO") as logs:
            self.processor._cmd_dolphin()
        self.assertIn("Dolphin Status: Dolphin connection has not been initiated.", logs.output[0])

    async def test_console_selection_and_off_clear_session_state(self):
        old_memory = self.ctx.memory
        self.ctx.auth = "Old Slot"
        self.ctx.slot = 1
        self.give_test_item()
        self.ctx.awaiting_rom = True
        self.ctx.finished_game = True
        self.ctx.received_magic_idx = 5
        self.ctx.salvage_locations_map = {"old": 1}
        self.ctx.item_delivery_uncertain = True
        self.assertTrue(self.processor._cmd_console("192.0.2.10"))
        self.assertIs(self.ctx.memory, old_memory)
        self.assertIsInstance(self.ctx.pending_memory, WiiMemory)
        self.assertTrue(self.ctx.watcher_event.is_set())
        with patch.object(old_memory, "un_hook") as unhook:
            await self.ctx.switch_memory()
            unhook.assert_called_once_with()
        self.assertIsInstance(self.ctx.memory, WiiMemory)
        self.assertFalse(self.ctx.memory.is_hooked())
        self.assertIsNone(self.ctx.auth)
        self.assertIsNone(self.ctx.slot)
        self.assertFalse(self.ctx.awaiting_rom)
        self.assertFalse(self.ctx.finished_game)
        self.assertEqual(self.ctx.items_received, [])
        self.assertEqual(self.ctx.salvage_locations_map, {})
        self.assertEqual(self.ctx.received_magic_idx, -1)
        self.assertTrue(self.ctx.item_delivery_uncertain)
        with self.assertLogs("Client", level="INFO") as logs:
            self.processor._cmd_dolphin()
        self.assertIn("Dolphin is inactive", logs.output[0])
        self.assertTrue(self.processor._cmd_console())
        self.assertEqual(self.processor.output.call_args.args[0], TWWClient.ITEM_DELIVERY_UNCERTAIN_STATUS)
        wii = self.ctx.memory
        self.assertTrue(self.processor._cmd_console("off"))
        with patch.object(wii, "un_hook") as unhook:
            await self.ctx.switch_memory()
            unhook.assert_called_once_with()
        self.assertIsInstance(self.ctx.memory, DolphinMemory)
        self.assertTrue(self.ctx.item_delivery_uncertain)

    async def test_invalid_console_does_not_switch(self):
        for address in ("bad-ip", "192.0.2.999", "::1", "192.0.2.10:55000"):
            with self.subTest(address=address):
                self.assertFalse(self.processor._cmd_console(address))
                self.assertIsNone(self.ctx.pending_memory)
        self.assertIsInstance(self.ctx.memory, DolphinMemory)

    async def test_dolphin_default_loop_authenticates_and_cleans_up(self):
        game = FakeTWW()
        engine = Mock()
        engine.is_hooked.return_value = False
        engine.hook.side_effect = lambda: setattr(engine.is_hooked, "return_value", True)
        engine.read_bytes.side_effect = game.read
        self.ctx.awaiting_rom = True
        self.ctx.server_auth = AsyncMock(side_effect=self.ctx.exit_event.set)
        with patch.dict("sys.modules", {"dolphin_memory_engine": engine}):
            await asyncio.wait_for(TWWClient.dolphin_sync_task(self.ctx), 2)
        self.assertEqual(self.ctx.auth, "Wii Test Slot")
        self.assertEqual(self.ctx.console_status, "Dolphin connected successfully.")
        engine.hook.assert_called_once_with()
        engine.un_hook.assert_called_once_with()
        self.ctx.server_auth.assert_awaited_once_with()

    async def test_wii_loop_recovers_after_bad_probe_without_touching_dolphin(self):
        game = FakeTWW()
        first_hello = True

        def responder(request):
            nonlocal first_hello
            if request == b"HELLO" and first_hello:
                first_hello = False
                return b"BAD"
            return game.reply(request)

        with FakeAPBridge(responder) as peer:
            self.ctx.memory = WiiMemory("127.0.0.1", peer.port)
            self.ctx.awaiting_rom = True
            self.ctx.disconnect = AsyncMock()
            self.ctx.server_auth = AsyncMock(side_effect=self.ctx.exit_event.set)
            # Advance the reconnect wait without spending five seconds in this test.
            self.ctx.watcher_event.wait = AsyncMock(return_value=True)
            with patch.object(DolphinMemory, "hook") as hook, patch.object(DolphinMemory, "un_hook") as unhook:
                await asyncio.wait_for(TWWClient.dolphin_sync_task(self.ctx), 2)
                hook.assert_not_called()
                unhook.assert_not_called()
            self.ctx.disconnect.assert_awaited_once_with()
            self.assertEqual(peer.requests.count(b"HELLO"), 2)
            self.assertEqual(self.ctx.auth, "Wii Test Slot")
            self.assertEqual(self.ctx.console_status, "Wii AP Bridge connected successfully.")
            self.assertFalse(self.ctx.memory.is_hooked())

    async def test_connected_package_defers_memory_reads(self):
        self.ctx.slot = 1
        with patch.object(self.ctx.memory, "read_bytes") as read:
            self.ctx.on_package("Connected", {"slot_data": {}})
            await asyncio.sleep(0)
            read.assert_not_called()

    async def test_wii_gameplay_paths_use_selected_memory(self):
        game = FakeTWW()
        with FakeAPBridge(game.reply) as peer:
            self.use_wii(peer)
            self.ctx.slot = 1
            self.ctx.send_msgs = AsyncMock()
            self.ctx.check_locations = AsyncMock()
            self.ctx.visited_stage_names = set()
            self.ctx.update_salvage_locations_map()
            self.assertEqual(len(self.ctx.salvage_locations_map), 49)
            self.give_test_item()
            await TWWClient.give_items(self.ctx)
            self.assertEqual(game.delivered, [TWWClient.ITEM_TABLE["Grappling Hook"].item_id])
            self.assertEqual(game.read(TWWClient.EXPECTED_INDEX_ADDR, 2), b"\x00\x01")
            await TWWClient.check_locations(self.ctx)
            self.ctx.check_locations.assert_awaited_once()
            await TWWClient.check_current_stage_changed(self.ctx)
            self.assertEqual(self.ctx.current_stage_name, "sea")
            self.assertEqual(self.ctx.visited_stage_names, {"sea"})
            self.assertTrue(await TWWClient.check_alive(self.ctx))
            self.ctx.on_deathlink({"time": 1, "source": "Test"})
            self.assertEqual(game.read(TWWClient.CURR_HEALTH_ADDR, 2), b"\x00\x00")
            self.assertFalse(await TWWClient.check_alive(self.ctx))

    async def test_uncertain_queue_or_index_write_is_not_replayed_after_reconnect(self):
        for address in (TWWClient.GIVE_ITEM_ARRAY_ADDR, TWWClient.EXPECTED_INDEX_ADDR):
            with self.subTest(address=address):
                self.ctx.item_delivery_uncertain = False
                game = FakeTWW()
                game.drop_ack = address
                with FakeAPBridge(game.reply) as peer:
                    self.use_wii(peer)
                    self.give_test_item()
                    with self.assertRaises(APBridgeError):
                        await TWWClient.give_items(self.ctx)
                    self.assertTrue(self.ctx.item_delivery_uncertain)
                    self.assertEqual(len(game.delivered), 1)
                    self.assertFalse(self.ctx.memory.is_hooked())
                    attempts = [request for request in peer.requests
                                if request[:4] == b"WRTX" and int.from_bytes(request[4:8], "big") == address]
                    self.assertEqual(len(attempts), 3)
                    self.assertEqual(attempts, [attempts[0]] * 3)
                    await self.ctx.disconnect()
                    self.assertTrue(self.ctx.item_delivery_uncertain)
                    self.ctx.memory.hook()
                    count = len(peer.requests)
                    await TWWClient.give_items(self.ctx)
                    self.assertEqual(len(peer.requests), count)
                    self.assertEqual(len(game.delivered), 1)
                    self.ctx.memory.un_hook()

    async def test_lost_queue_or_index_ack_recovers_without_duplicate_item(self):
        for address in (TWWClient.GIVE_ITEM_ARRAY_ADDR, TWWClient.EXPECTED_INDEX_ADDR):
            with self.subTest(address=address):
                game = FakeTWW()
                game.drop_ack_counts[address] = 1
                with FakeAPBridge(game.reply) as peer:
                    self.use_wii(peer)
                    self.give_test_item()
                    await TWWClient.give_items(self.ctx)
                    item_id = TWWClient.ITEM_TABLE["Grappling Hook"].item_id
                    self.assertEqual(game.delivered, [item_id])
                    self.assertEqual(game.read(TWWClient.EXPECTED_INDEX_ADDR, 2), b"\x00\x01")
                    self.assertEqual(game.write_cache.writes, [
                        (TWWClient.GIVE_ITEM_ARRAY_ADDR, bytes([item_id])),
                        (TWWClient.EXPECTED_INDEX_ADDR, b"\x00\x01"),
                    ])
                    self.assertFalse(self.ctx.item_delivery_uncertain)
                    self.assertTrue(self.ctx.memory.is_hooked())
                    attempts = [request for request in peer.requests
                                if request[:4] == b"WRTX" and int.from_bytes(request[4:8], "big") == address]
                    self.assertEqual(len(attempts), 2)
                    self.assertEqual(attempts[0], attempts[1])
                    self.assertEqual(len(peer.peers), 2)
                    write_count = sum(request[:4] == b"WRTX" for request in peer.requests)
                    await TWWClient.give_items(self.ctx)
                    self.assertEqual(sum(request[:4] == b"WRTX" for request in peer.requests), write_count)
                    self.assertEqual(game.delivered, [item_id])
                    self.ctx.memory.un_hook()

    async def test_rejected_queue_write_does_not_pause_delivery(self):
        game = FakeTWW()
        game.reject_write = TWWClient.GIVE_ITEM_ARRAY_ADDR
        with FakeAPBridge(game.reply) as peer:
            self.use_wii(peer)
            self.give_test_item()
            with self.assertRaises(APBridgeRemoteError):
                await TWWClient.give_items(self.ctx)
            self.assertFalse(self.ctx.item_delivery_uncertain)
            self.assertEqual(game.delivered, [])
            self.assertEqual(game.write_cache.writes, [])
            self.assertEqual(sum(request[:4] == b"WRTX" for request in peer.requests), 1)

    async def test_rejected_index_write_also_pauses_delivery(self):
        game = FakeTWW()
        game.reject_write = TWWClient.EXPECTED_INDEX_ADDR
        with FakeAPBridge(game.reply) as peer:
            self.use_wii(peer)
            self.give_test_item()
            with self.assertRaises(APBridgeRemoteError):
                await TWWClient.give_items(self.ctx)
            self.assertTrue(self.ctx.item_delivery_uncertain)
            self.assertEqual(len(game.delivered), 1)
            self.assertEqual(game.read(TWWClient.EXPECTED_INDEX_ADDR, 2), b"\x00\x00")

    async def test_read_failure_does_not_pause_item_delivery(self):
        game = FakeTWW()
        with FakeAPBridge(game.reply) as peer:
            self.use_wii(peer)
            self.give_test_item()
            peer.responder = lambda request: b"BAD"
            with self.assertRaises(APBridgeError):
                await TWWClient.give_items(self.ctx)
            self.assertFalse(self.ctx.item_delivery_uncertain)
            self.assertEqual(game.delivered, [])
            peer.responder = game.reply
            self.ctx.memory.hook()
            await TWWClient.give_items(self.ctx)
            self.assertEqual(len(game.delivered), 1)

    async def test_full_item_queue_can_be_interrupted_by_switch_or_exit(self):
        for action in ("switch", "exit"):
            with self.subTest(action=action):
                self.ctx.pending_memory = None
                self.ctx.exit_event.clear()
                game = FakeTWW()
                game.put(TWWClient.GIVE_ITEM_ARRAY_ADDR, bytes(16))
                with FakeAPBridge(game.reply) as peer:
                    self.use_wii(peer)
                    self.give_test_item()
                    task = asyncio.create_task(TWWClient.give_items(self.ctx))
                    await asyncio.sleep(0)
                    if action == "switch":
                        self.processor._cmd_console("off")
                    else:
                        self.ctx.exit_event.set()
                    await asyncio.wait_for(task, 1)
                    self.assertEqual(game.delivered, [])
                    self.ctx.memory.un_hook()

    async def test_deathlink_failure_marks_lost_without_escaping_callback(self):
        game = FakeTWW()
        game.drop_ack = TWWClient.CURR_HEALTH_ADDR
        with FakeAPBridge(game.reply) as peer:
            self.use_wii(peer)
            self.ctx.slot = 1
            self.ctx.on_deathlink({"time": 1, "source": "Test"})
            self.assertFalse(self.ctx.memory.is_hooked())
            self.assertIn("Wii AP Bridge connection was lost", self.ctx.console_status)
            self.assertTrue(self.ctx.watcher_event.is_set())
            self.assertFalse(self.ctx.item_delivery_uncertain)
