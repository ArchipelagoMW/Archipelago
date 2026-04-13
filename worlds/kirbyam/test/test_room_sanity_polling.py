"""Room-sanity polling tests for native gVisitedDoors -> LocationChecks mapping."""

from __future__ import annotations

from unittest.mock import AsyncMock, patch

import pytest

from ..client import KirbyAmClient
from ..data import data


def _room_visit_bytes(*visited_doors_idx: int) -> bytes:
    payload = bytearray(0x120 * 2)
    for doors_idx in visited_doors_idx:
        if 0 <= doors_idx < 0x120:
            offset = doors_idx * 2
            payload[offset:offset + 2] = (0x8000).to_bytes(2, "little")
    return bytes(payload)


@pytest.mark.asyncio
async def test_poll_room_sanity_sends_location_checks_for_visited_doors(mock_bizhawk_context):
    client = KirbyAmClient()
    client.initialize_client()

    mock_bizhawk_context.slot_data["room_sanity"] = True
    mock_bizhawk_context.checked_locations = set()

    room_1_central_circle_data = data.locations["ROOM_SANITY_1_CENTRAL_CIRCLE"]
    room_1_27_data = data.locations["ROOM_SANITY_1_27"]
    room_1_central_circle = room_1_central_circle_data.location_id
    room_1_27 = room_1_27_data.location_id
    assert room_1_central_circle_data.bit_index is not None
    assert room_1_27_data.bit_index is not None

    with patch.dict(data.native_ram_addresses, {"room_visit_flags_native": 0x02028CA0}, clear=False), \
         patch("worlds.kirbyam.client.bizhawk.read", new_callable=AsyncMock) as mock_read, \
         patch.object(mock_bizhawk_context, "send_msgs", new_callable=AsyncMock) as mock_send:
        # Derive visited bits from current location metadata instead of hard-coding doorsIdx constants.
        mock_read.return_value = [_room_visit_bytes(room_1_central_circle_data.bit_index, room_1_27_data.bit_index)]

        await client._poll_room_sanity_locations(mock_bizhawk_context)

    mock_send.assert_awaited_once_with([
        {"cmd": "LocationChecks", "locations": [room_1_central_circle, room_1_27]}
    ])


@pytest.mark.asyncio
async def test_poll_room_sanity_is_gated_off_when_option_disabled(mock_bizhawk_context):
    client = KirbyAmClient()
    client.initialize_client()

    mock_bizhawk_context.slot_data["room_sanity"] = False

    with patch.dict(data.native_ram_addresses, {"room_visit_flags_native": 0x02028CA0}, clear=False), \
         patch("worlds.kirbyam.client.bizhawk.read", new_callable=AsyncMock) as mock_read, \
         patch.object(mock_bizhawk_context, "send_msgs", new_callable=AsyncMock) as mock_send:
        await client._poll_room_sanity_locations(mock_bizhawk_context)

    mock_read.assert_not_awaited()
    mock_send.assert_not_awaited()


@pytest.mark.asyncio
async def test_poll_room_sanity_dedupes_already_server_acknowledged(mock_bizhawk_context):
    client = KirbyAmClient()
    client.initialize_client()

    mock_bizhawk_context.slot_data["room_sanity"] = True
    room_1_central_circle_data = data.locations["ROOM_SANITY_1_CENTRAL_CIRCLE"]
    room_1_central_circle = room_1_central_circle_data.location_id
    assert room_1_central_circle_data.bit_index is not None
    mock_bizhawk_context.checked_locations = {room_1_central_circle}

    with patch.dict(data.native_ram_addresses, {"room_visit_flags_native": 0x02028CA0}, clear=False), \
         patch("worlds.kirbyam.client.bizhawk.read", new_callable=AsyncMock) as mock_read, \
         patch.object(mock_bizhawk_context, "send_msgs", new_callable=AsyncMock) as mock_send, \
         patch("CommonClient.logger") as mock_logger:
        mock_read.return_value = [_room_visit_bytes(room_1_central_circle_data.bit_index)]

        await client._poll_room_sanity_locations(mock_bizhawk_context)

    mock_send.assert_not_awaited()
    mock_logger.debug.assert_called_once()
    debug_args = mock_logger.debug.call_args.args
    assert "dedupe suppressed room-sanity LocationChecks" in debug_args[0]
    assert debug_args[1] == [room_1_central_circle]


@pytest.mark.asyncio
async def test_poll_room_sanity_skips_when_address_missing(mock_bizhawk_context):
    client = KirbyAmClient()
    client.initialize_client()

    mock_bizhawk_context.slot_data["room_sanity"] = True

    native_without_room_visits = {
        key: value
        for key, value in data.native_ram_addresses.items()
        if key != "room_visit_flags_native"
    }

    with patch.dict(data.native_ram_addresses, native_without_room_visits, clear=True), \
         patch("worlds.kirbyam.client.bizhawk.read", new_callable=AsyncMock) as mock_read, \
         patch.object(mock_bizhawk_context, "send_msgs", new_callable=AsyncMock) as mock_send:
        await client._poll_room_sanity_locations(mock_bizhawk_context)

    mock_read.assert_not_awaited()
    mock_send.assert_not_awaited()


@pytest.mark.asyncio
async def test_reconnect_room_sanity_resends_once_then_dedupes(mock_bizhawk_context):
    """Reconnect-equivalent room polling should resend once then dedupe after server ack."""
    client = KirbyAmClient()
    client.initialize_client()

    mock_bizhawk_context.slot_data["room_sanity"] = True
    room_1_central_circle_data = data.locations["ROOM_SANITY_1_CENTRAL_CIRCLE"]
    room_1_central_circle = room_1_central_circle_data.location_id
    assert room_1_central_circle_data.bit_index is not None
    mock_bizhawk_context.checked_locations = set()

    with patch.dict(data.native_ram_addresses, {"room_visit_flags_native": 0x02028CA0}, clear=False), \
         patch("worlds.kirbyam.client.bizhawk.read", new_callable=AsyncMock) as mock_read:
        # First poll: visited in RAM but not on server -> send.
        mock_read.return_value = [_room_visit_bytes(room_1_central_circle_data.bit_index)]
        await client._poll_room_sanity_locations(mock_bizhawk_context)

        # Reconnect-equivalent poll: now server has acknowledged -> dedupe.
        mock_bizhawk_context.checked_locations = {room_1_central_circle}
        mock_read.return_value = [_room_visit_bytes(room_1_central_circle_data.bit_index)]
        await client._poll_room_sanity_locations(mock_bizhawk_context)

    mock_bizhawk_context.send_msgs.assert_awaited_once_with([
        {"cmd": "LocationChecks", "locations": [room_1_central_circle]}
    ])
