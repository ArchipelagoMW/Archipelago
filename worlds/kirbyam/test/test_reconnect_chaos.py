"""Reconnect chaos tests for KirbyAM BizHawk client idempotency (Issue #302)."""

from __future__ import annotations

from unittest.mock import AsyncMock, Mock, patch

import pytest

from ..client import KirbyAmClient
from ..data import data


@pytest.mark.asyncio
async def test_reconnect_chaos_boss_defeat_polling_resends_once_then_dedupes(mock_bizhawk_context):
    """Reconnect cycles should not duplicate boss-defeat LocationChecks after server acknowledgement."""
    client = KirbyAmClient()
    client.initialize_client()

    boss1_id = data.locations["BOSS_DEFEAT_1"].location_id
    mock_bizhawk_context.checked_locations = set()

    with patch.dict(data.transport_ram_addresses, {"boss_defeat_flags": 0x0202C024}, clear=False), \
         patch('worlds.kirbyam.client.bizhawk.read', new_callable=AsyncMock) as mock_read:
        # First poll: boss bit set and not acknowledged by server -> send once.
        mock_read.return_value = [(0x01).to_bytes(4, 'little')]
        await client._poll_boss_defeat_locations(mock_bizhawk_context)

        # Reconnect-equivalent poll: same RAM bit, now acknowledged by server -> dedupe.
        mock_bizhawk_context.checked_locations = {boss1_id}
        mock_read.return_value = [(0x01).to_bytes(4, 'little')]
        await client._poll_boss_defeat_locations(mock_bizhawk_context)

    # Exactly one LocationChecks send across connect/disconnect/reconnect.
    mock_bizhawk_context.send_msgs.assert_awaited_once_with([
        {"cmd": "LocationChecks", "locations": [boss1_id]}
    ])


@pytest.mark.asyncio
async def test_reconnect_chaos_item_delivery_resumes_without_duplicate_first_item(mock_bizhawk_context):
    """Delivery should resume after reconnect without replaying already-pending first item."""
    client = KirbyAmClient()
    client.initialize_client()

    item1 = 3860001
    item2 = 3860002
    mock_bizhawk_context.items_received = [
        Mock(item=item1, player=1),
        Mock(item=item2, player=1),
    ]

    id_addr = data.transport_ram_addresses["incoming_item_id"]

    with patch('worlds.kirbyam.client.bizhawk.read', new_callable=AsyncMock) as mock_read, \
         patch('worlds.kirbyam.client.bizhawk.write', new_callable=AsyncMock) as mock_write, \
         patch.object(client, '_runtime_gameplay_state', new_callable=AsyncMock) as mock_gate, \
         patch.object(client, '_load_persistent_state', new_callable=AsyncMock), \
         patch.object(client, '_apply_pending_death_link', new_callable=AsyncMock), \
         patch.object(client, '_poll_and_send_local_death_link', new_callable=AsyncMock), \
         patch.object(client, '_poll_locations', new_callable=AsyncMock), \
         patch.object(client, '_poll_boss_defeat_locations', new_callable=AsyncMock), \
         patch.object(client, '_poll_major_chest_locations', new_callable=AsyncMock), \
         patch.object(client, '_poll_vitality_chest_locations', new_callable=AsyncMock), \
         patch.object(client, '_probe_boss_defeat_candidates', new_callable=AsyncMock), \
         patch.object(client, '_probe_unsafe_delivery_candidates', new_callable=AsyncMock), \
         patch.object(client, '_maybe_report_goal', new_callable=AsyncMock):
        mock_gate.return_value = (True, "gameplay_active", 300)

        # Cycle 1 (connected): write first item, pending ACK.
        mock_read.return_value = [
            (0).to_bytes(4, 'little'),
            (0).to_bytes(4, 'little'),
            (10).to_bytes(4, 'little'),
        ]
        await client.game_watcher(mock_bizhawk_context)

        # Cycle 2 (disconnected): no watcher delivery work.
        mock_bizhawk_context.server.socket.closed = True
        await client.game_watcher(mock_bizhawk_context)

        # Cycle 3 (reconnected): ACK first item.
        mock_bizhawk_context.server.socket.closed = False
        mock_read.return_value = [
            (0).to_bytes(4, 'little'),
            (1).to_bytes(4, 'little'),
            (20).to_bytes(4, 'little'),
        ]
        await client.game_watcher(mock_bizhawk_context)

        # Cycle 4 (connected): write second item.
        mock_read.return_value = [
            (0).to_bytes(4, 'little'),
            (1).to_bytes(4, 'little'),
            (21).to_bytes(4, 'little'),
        ]
        await client.game_watcher(mock_bizhawk_context)

    # Ensure first item write occurred once and second item write occurred once.
    mailbox_writes = [
        batch
        for batch in (call.args[1] for call in mock_write.await_args_list)
        if any(addr == id_addr for addr, *_ in batch)
    ]
    item_ids_written = [
        int.from_bytes(next(payload for addr, payload, _ in batch if addr == id_addr), 'little')
        for batch in mailbox_writes
    ]
    assert item_ids_written.count(item1) == 1
    assert item_ids_written.count(item2) == 1
    assert item_ids_written == [item1, item2]
    assert client._delivered_item_index >= 1


@pytest.mark.asyncio
async def test_reconnect_chaos_goal_reporting_is_idempotent_across_cycles(mock_bizhawk_context):
    """Goal flow should send location then status once, with no duplicate status on later reconnects."""
    client = KirbyAmClient()
    client.initialize_client()

    goal_id = data.locations["GOAL_DARK_MIND"].location_id
    mock_bizhawk_context.slot_data["goal"] = 0
    mock_bizhawk_context.checked_locations = set()
    mock_bizhawk_context.locations_checked = set()

    with patch.object(client, '_runtime_gameplay_state', new_callable=AsyncMock) as mock_gate, \
         patch.object(client, '_load_persistent_state', new_callable=AsyncMock), \
         patch.object(client, '_apply_pending_death_link', new_callable=AsyncMock), \
         patch.object(client, '_poll_and_send_local_death_link', new_callable=AsyncMock), \
         patch.object(client, '_poll_locations', new_callable=AsyncMock), \
         patch.object(client, '_poll_boss_defeat_locations', new_callable=AsyncMock), \
         patch.object(client, '_poll_major_chest_locations', new_callable=AsyncMock), \
         patch.object(client, '_poll_vitality_chest_locations', new_callable=AsyncMock), \
         patch.object(client, '_probe_boss_defeat_candidates', new_callable=AsyncMock), \
         patch.object(client, '_probe_unsafe_delivery_candidates', new_callable=AsyncMock), \
         patch.object(client, '_deliver_items', new_callable=AsyncMock):
        # Use ai_state override for deterministic goal signal without RAM reads.
        mock_gate.return_value = (True, "gameplay_active", 9999)

        # Cycle 1: send goal location check.
        await client.game_watcher(mock_bizhawk_context)

        # Cycle 2: disconnected no-op.
        mock_bizhawk_context.server.socket.closed = True
        await client.game_watcher(mock_bizhawk_context)

        # Cycle 3: reconnected with goal location acknowledged by server; send CLIENT_GOAL.
        mock_bizhawk_context.server.socket.closed = False
        mock_bizhawk_context.checked_locations.add(goal_id)
        await client.game_watcher(mock_bizhawk_context)

        # Cycle 4: another reconnect-safe watcher run should not send duplicate status.
        await client.game_watcher(mock_bizhawk_context)

    payloads = [call.args[0][0] for call in mock_bizhawk_context.send_msgs.await_args_list]
    location_msgs = [p for p in payloads if p.get("cmd") == "LocationChecks"]
    status_msgs = [p for p in payloads if p.get("cmd") == "StatusUpdate"]

    assert len(location_msgs) == 1
    assert location_msgs[0]["locations"] == [goal_id]
    assert len(status_msgs) == 1
