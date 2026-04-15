"""Area-first-visit polling tests for native gVisitedDoors -> LocationChecks mapping."""

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
async def test_poll_area_visit_sends_one_check_per_visited_area(mock_bizhawk_context):
    client = KirbyAmClient()
    client.initialize_client()

    mock_bizhawk_context.checked_locations = set()

    area_1_location_id = data.locations["AREA_VISIT_1_RAINBOW_ROUTE"].location_id
    area_2_location_id = data.locations["AREA_VISIT_2_MOONLIGHT_MANSION"].location_id

    room_1_data = data.locations["ROOM_SANITY_1_01"]
    room_1_alt_data = data.locations["ROOM_SANITY_1_02"]
    room_2_data = data.locations["ROOM_SANITY_2_01"]
    assert room_1_data.bit_index is not None
    assert room_1_alt_data.bit_index is not None
    assert room_2_data.bit_index is not None

    with patch.dict(data.native_ram_addresses, {"room_visit_flags_native": 0x02028CA0}, clear=False), \
         patch("worlds.kirbyam.client.bizhawk.read", new_callable=AsyncMock) as mock_read, \
         patch.object(mock_bizhawk_context, "send_msgs", new_callable=AsyncMock) as mock_send:
        # Visiting multiple rooms in one area still yields only one area check.
        mock_read.return_value = [
            _room_visit_bytes(room_1_data.bit_index, room_1_alt_data.bit_index, room_2_data.bit_index)
        ]

        await client._poll_area_visit_locations(mock_bizhawk_context)

    mock_send.assert_awaited_once_with([
        {"cmd": "LocationChecks", "locations": [area_1_location_id, area_2_location_id]}
    ])


@pytest.mark.asyncio
async def test_poll_area_visit_dedupes_already_acknowledged(mock_bizhawk_context):
    client = KirbyAmClient()
    client.initialize_client()

    area_1_location_id = data.locations["AREA_VISIT_1_RAINBOW_ROUTE"].location_id
    room_1_data = data.locations["ROOM_SANITY_1_01"]
    assert room_1_data.bit_index is not None

    mock_bizhawk_context.checked_locations = {area_1_location_id}

    with patch.dict(data.native_ram_addresses, {"room_visit_flags_native": 0x02028CA0}, clear=False), \
         patch("worlds.kirbyam.client.bizhawk.read", new_callable=AsyncMock) as mock_read, \
         patch.object(mock_bizhawk_context, "send_msgs", new_callable=AsyncMock) as mock_send, \
         patch("CommonClient.logger") as mock_logger:
        mock_read.return_value = [_room_visit_bytes(room_1_data.bit_index)]

        await client._poll_area_visit_locations(mock_bizhawk_context)

    mock_send.assert_not_awaited()
    mock_logger.debug.assert_called_once()
    debug_args = mock_logger.debug.call_args.args
    assert "dedupe suppressed area-first-visit LocationChecks" in debug_args[0]
    assert debug_args[1] == [area_1_location_id]


@pytest.mark.asyncio
async def test_reconnect_area_visit_resends_once_then_dedupes(mock_bizhawk_context):
    client = KirbyAmClient()
    client.initialize_client()

    area_1_location_id = data.locations["AREA_VISIT_1_RAINBOW_ROUTE"].location_id
    room_1_data = data.locations["ROOM_SANITY_1_01"]
    assert room_1_data.bit_index is not None

    mock_bizhawk_context.checked_locations = set()

    with patch.dict(data.native_ram_addresses, {"room_visit_flags_native": 0x02028CA0}, clear=False), \
         patch("worlds.kirbyam.client.bizhawk.read", new_callable=AsyncMock) as mock_read:
        mock_read.return_value = [_room_visit_bytes(room_1_data.bit_index)]
        await client._poll_area_visit_locations(mock_bizhawk_context)

        mock_bizhawk_context.checked_locations = {area_1_location_id}
        mock_read.return_value = [_room_visit_bytes(room_1_data.bit_index)]
        await client._poll_area_visit_locations(mock_bizhawk_context)

    mock_bizhawk_context.send_msgs.assert_awaited_once_with([
        {"cmd": "LocationChecks", "locations": [area_1_location_id]}
    ])
