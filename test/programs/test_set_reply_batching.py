"""Tests for server-side SetReply batching (pending_set_replies buffer and flush)."""
import asyncio
import unittest
from unittest.mock import AsyncMock, MagicMock, patch

from MultiServer import Context, Client, process_client_cmd


def make_mock_socket():
    sock = MagicMock()
    sock.open = True
    sock.send = AsyncMock(return_value=None)
    return sock


def make_client(ctx: Context, team: int = 0, slot: int = 1):
    sock = make_mock_socket()
    client = Client(sock, ctx)
    client.auth = True
    client.team = team
    client.slot = slot
    ctx.player_names[team, slot] = f"Player{slot}"
    return client


@patch("MultiServer.Context._load_game_data")
class TestSetReplyBatching(unittest.IsolatedAsyncioTestCase):
    async def test_set_buffers_reply_in_pending_set_replies(self, mock_load_game_data):
        ctx = Context("", 0, "", "", 0, 0, False)
        ctx.save = MagicMock()
        client = make_client(ctx)
        ctx.clients[0] = {1: [client]}
        ctx.stored_data_notification_clients["test_key"].add(client)

        await process_client_cmd(ctx, client, {
            "cmd": "Set",
            "key": "test_key",
            "operations": [{"operation": "replace", "value": 42}],
        })

        self.assertIn(client, ctx.pending_set_replies)
        self.assertEqual(len(ctx.pending_set_replies[client]), 1)
        reply = ctx.pending_set_replies[client][0]
        self.assertEqual(reply["cmd"], "SetReply")
        self.assertEqual(reply["key"], "test_key")
        self.assertEqual(reply["value"], 42)
        self.assertEqual(reply["original_value"], 0)

    async def test_multiple_sets_batch_per_client(self, mock_load_game_data):
        ctx = Context("", 0, "", "", 0, 0, False)
        ctx.save = MagicMock()
        client = make_client(ctx)
        ctx.clients[0] = {1: [client]}
        ctx.stored_data_notification_clients["k1"].add(client)
        ctx.stored_data_notification_clients["k2"].add(client)

        await process_client_cmd(ctx, client, {
            "cmd": "Set", "key": "k1", "operations": [{"operation": "replace", "value": 1}],
        })
        await process_client_cmd(ctx, client, {
            "cmd": "Set", "key": "k2", "operations": [{"operation": "replace", "value": 2}],
        })

        self.assertEqual(len(ctx.pending_set_replies[client]), 2)
        self.assertEqual(ctx.pending_set_replies[client][0]["key"], "k1")
        self.assertEqual(ctx.pending_set_replies[client][0]["value"], 1)
        self.assertEqual(ctx.pending_set_replies[client][1]["key"], "k2")
        self.assertEqual(ctx.pending_set_replies[client][1]["value"], 2)

    async def test_flush_sends_one_message_per_client_with_all_pending_replies(self, mock_load_game_data):
        ctx = Context("", 0, "", "", 0, 0, False)
        ctx.save = MagicMock()
        send_msgs = AsyncMock(return_value=True)
        ctx.send_msgs = send_msgs

        client_a = make_client(ctx, team=0, slot=1)
        client_b = make_client(ctx, team=0, slot=2)
        ctx.clients[0] = {1: [client_a], 2: [client_b]}
        ctx.stored_data_notification_clients["key"].add(client_a)
        ctx.stored_data_notification_clients["key"].add(client_b)

        await process_client_cmd(ctx, client_a, {
            "cmd": "Set", "key": "key", "operations": [{"operation": "replace", "value": 10}],
        })

        self.assertEqual(send_msgs.call_count, 0, "no immediate send before flush")
        self.assertEqual(len(ctx.pending_set_replies[client_a]), 1)
        self.assertEqual(len(ctx.pending_set_replies[client_b]), 1)

        await ctx._flush_pending_set_replies()

        self.assertEqual(send_msgs.call_count, 2, "one send per client")
        calls = {call.args[0]: call.args[1] for call in send_msgs.call_args_list}
        self.assertIn(client_a, calls)
        self.assertIn(client_b, calls)
        self.assertEqual(len(calls[client_a]), 1)
        self.assertEqual(len(calls[client_b]), 1)
        self.assertEqual(calls[client_a][0]["cmd"], "SetReply")
        self.assertEqual(calls[client_a][0]["value"], 10)
        self.assertFalse(ctx.pending_set_replies, "buffer cleared after flush")

    async def test_flush_clears_buffer(self, mock_load_game_data):
        ctx = Context("", 0, "", "", 0, 0, False)
        ctx.save = MagicMock()
        ctx.send_msgs = AsyncMock(return_value=True)
        client = make_client(ctx)
        ctx.clients[0] = {1: [client]}
        ctx.stored_data_notification_clients["x"].add(client)

        await process_client_cmd(ctx, client, {
            "cmd": "Set", "key": "x", "operations": [{"operation": "replace", "value": 99}],
        })
        self.assertTrue(ctx.pending_set_replies)

        await ctx._flush_pending_set_replies()
        self.assertFalse(ctx.pending_set_replies)

    async def test_disconnect_clears_pending_set_replies_for_client(self, mock_load_game_data):
        ctx = Context("", 0, "", "", 0, 0, False)
        ctx.save = MagicMock()
        client = make_client(ctx)
        ctx.clients[0] = {1: [client]}
        ctx.endpoints.append(client)
        ctx.stored_data_notification_clients["key"].add(client)

        await process_client_cmd(ctx, client, {
            "cmd": "Set", "key": "key", "operations": [{"operation": "replace", "value": 1}],
        })
        self.assertIn(client, ctx.pending_set_replies)

        with patch("MultiServer.on_client_disconnected", new_callable=AsyncMock):
            await ctx.disconnect(client)

        self.assertNotIn(client, ctx.pending_set_replies)

    async def test_want_reply_includes_sender_in_targets(self, mock_load_game_data):
        ctx = Context("", 0, "", "", 0, 0, False)
        ctx.save = MagicMock()
        client = make_client(ctx)
        ctx.clients[0] = {1: [client]}
        # no SetNotify: only targets are from want_reply (sender)
        await process_client_cmd(ctx, client, {
            "cmd": "Set",
            "key": "solo_key",
            "operations": [{"operation": "replace", "value": 7}],
            "want_reply": True,
        })
        self.assertIn(client, ctx.pending_set_replies)
        self.assertEqual(len(ctx.pending_set_replies[client]), 1)
        self.assertEqual(ctx.pending_set_replies[client][0]["value"], 7)

    async def test_schedule_flush_sets_flag_and_clears_after_scheduled_flush(self, mock_load_game_data):
        ctx = Context("", 0, "", "", 0, 0, False)
        ctx.save = MagicMock()
        ctx.send_msgs = AsyncMock(return_value=True)
        client = make_client(ctx)
        ctx.clients[0] = {1: [client]}
        ctx.stored_data_notification_clients["k"].add(client)

        self.assertFalse(ctx._pending_set_reply_flush_scheduled)
        await process_client_cmd(ctx, client, {
            "cmd": "Set", "key": "k", "operations": [{"operation": "replace", "value": 0}],
        })
        self.assertTrue(ctx._pending_set_reply_flush_scheduled)
        self.assertTrue(ctx.pending_set_replies)

        await asyncio.sleep(0.06)
        self.assertFalse(ctx._pending_set_reply_flush_scheduled)
        self.assertFalse(ctx.pending_set_replies)
        self.assertEqual(ctx.send_msgs.call_count, 1)
