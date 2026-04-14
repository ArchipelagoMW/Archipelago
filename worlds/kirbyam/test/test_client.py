"""Integration tests for client polling and delivery logic."""
import asyncio
import pytest
import logging
from unittest.mock import AsyncMock, Mock, patch

import worlds._bizhawk as bizhawk
from worlds._bizhawk.context import _game_watcher, AuthStatus

from ..data import LocationCategory, data
from ..client import (
    KirbyAmClient,
    _MAP_ITEM_ID_TO_AREA_ID,
    _ROOM_PROPS_DOORS_IDX_OFFSET,
    _ROOM_PROPS_ROM_BASE,
    _ROOM_PROPS_STRIDE,
    _ROOM_UPDATE_BOUNCE_TYPE,
)
from ..options import OneHitMode
from ..rom import KirbyAmProcedurePatch


@pytest.mark.asyncio
async def test_validate_rom_accepts_patched_kirby_header(mock_bizhawk_context):
    client = KirbyAmClient()

    with patch('worlds.kirbyam.client.bizhawk.read', new_callable=AsyncMock) as mock_read:
        mock_read.side_effect = [
            [b'AGB KIRBY AM', b'B8KE', b'01'],
            [b'\x01' + (b'\x00' * 15)],
        ]

        assert await client.validate_rom(mock_bizhawk_context) is True
        assert mock_bizhawk_context.game == client.game
        assert mock_bizhawk_context.want_slot_data is True


@pytest.mark.asyncio
async def test_validate_rom_reads_auth_from_rom_domain_offset(mock_bizhawk_context):
    client = KirbyAmClient()

    original_auth_addr = data.rom_addresses.get("gArchipelagoInfo")
    data.rom_addresses["gArchipelagoInfo"] = 0x08F00000
    try:
        with patch('worlds.kirbyam.client.bizhawk.read', new_callable=AsyncMock) as mock_read:
            mock_read.side_effect = [
                [b'AGB KIRBY AM', b'B8KE', b'01'],
                [b'\x01' + (b'\x00' * 15)],
            ]

            assert await client.validate_rom(mock_bizhawk_context) is True

        mock_read.assert_any_await(
            mock_bizhawk_context.bizhawk_ctx,
            [(0x00F00000, 16, "ROM")],
        )
    finally:
        if original_auth_addr is None:
            data.rom_addresses.pop("gArchipelagoInfo", None)
        else:
            data.rom_addresses["gArchipelagoInfo"] = original_auth_addr


@pytest.mark.asyncio
async def test_validate_rom_rejects_missing_auth_address(mock_bizhawk_context, caplog):
    client = KirbyAmClient()

    original_auth_addr = data.rom_addresses.pop("gArchipelagoInfo", None)
    try:
        with patch('worlds.kirbyam.client.bizhawk.display_message', new_callable=AsyncMock) as mock_display:
            with caplog.at_level(logging.ERROR):
                assert await client.validate_rom(mock_bizhawk_context) is False

        mock_display.assert_awaited_once_with(
            mock_bizhawk_context.bizhawk_ctx,
            "Unable to load ROM: patch metadata address is missing.",
        )
        assert "missing rom address 'gArchipelagoInfo'" in caplog.text
    finally:
        if original_auth_addr is not None:
            data.rom_addresses["gArchipelagoInfo"] = original_auth_addr


@pytest.mark.asyncio
async def test_validate_rom_rejects_unpatched_kirby_rom(mock_bizhawk_context, caplog):
    client = KirbyAmClient()
    mock_bizhawk_context.rom_hash = KirbyAmProcedurePatch.hash

    with patch('worlds.kirbyam.client.bizhawk.read', new_callable=AsyncMock) as mock_read, \
         patch('worlds.kirbyam.client.bizhawk.display_message', new_callable=AsyncMock) as mock_display:
        with caplog.at_level(logging.INFO):
            assert await client.validate_rom(mock_bizhawk_context) is False

    mock_read.assert_not_awaited()
    mock_display.assert_awaited_once_with(
        mock_bizhawk_context.bizhawk_ctx,
        "Unable to load ROM: base ROM detected. Please use a patched ROM.",
    )
    assert "unpatched Kirby & The Amazing Mirror ROM" in caplog.text


@pytest.mark.asyncio
async def test_validate_rom_rejects_missing_auth_block_read(mock_bizhawk_context, caplog):
    client = KirbyAmClient()

    with patch('worlds.kirbyam.client.bizhawk.read', new_callable=AsyncMock) as mock_read, \
         patch('worlds.kirbyam.client.bizhawk.display_message', new_callable=AsyncMock) as mock_display:
        mock_read.side_effect = [
            [b'AGB KIRBY AM', b'B8KE', b'01'],
            bizhawk.RequestFailedError("Connection closed"),
        ]

        with caplog.at_level(logging.INFO):
            assert await client.validate_rom(mock_bizhawk_context) is False

    mock_display.assert_awaited_once_with(
        mock_bizhawk_context.bizhawk_ctx,
        "Unable to load ROM: could not read patch metadata.",
    )
    assert "unpatched Kirby & The Amazing Mirror ROM" not in caplog.text
    assert "ROM auth read failed during validation" in caplog.text


@pytest.mark.asyncio
async def test_validate_rom_rejects_non_kirby_header(mock_bizhawk_context, caplog):
    client = KirbyAmClient()

    with patch('worlds.kirbyam.client.bizhawk.read', new_callable=AsyncMock) as mock_read, \
         patch('worlds.kirbyam.client.bizhawk.display_message', new_callable=AsyncMock) as mock_display:
        mock_read.side_effect = [
            [b'POKEMON EMER', b'BPEE', b'01'],
        ]

        with caplog.at_level(logging.INFO):
            assert await client.validate_rom(mock_bizhawk_context) is False

    mock_display.assert_awaited_once_with(
        mock_bizhawk_context.bizhawk_ctx,
        "Unable to load ROM: invalid Kirby and the Amazing Mirror ROM.",
    )
    assert "ROM validation failed" in caplog.text


@pytest.mark.asyncio
async def test_validate_rom_rejects_empty_patch_metadata(mock_bizhawk_context, caplog):
    client = KirbyAmClient()

    with patch('worlds.kirbyam.client.bizhawk.read', new_callable=AsyncMock) as mock_read, \
         patch('worlds.kirbyam.client.bizhawk.display_message', new_callable=AsyncMock) as mock_display:
        mock_read.side_effect = [
            [b'AGB KIRBY AM', b'B8KE', b'01'],
            [b'\x00' * 16],
        ]

        with caplog.at_level(logging.INFO):
            assert await client.validate_rom(mock_bizhawk_context) is False

    mock_display.assert_awaited_once_with(
        mock_bizhawk_context.bizhawk_ctx,
        "Unable to load ROM: missing patch metadata. Rebuild your patched ROM.",
    )
    assert "KirbyAM patch metadata was missing" in caplog.text


@pytest.mark.asyncio
async def test_validate_rom_rejects_empty_patch_metadata_logs_once(mock_bizhawk_context, caplog):
    client = KirbyAmClient()

    with patch('worlds.kirbyam.client.bizhawk.read', new_callable=AsyncMock) as mock_read, \
         patch('worlds.kirbyam.client.bizhawk.display_message', new_callable=AsyncMock) as mock_display:
        mock_read.side_effect = [
            [b'AGB KIRBY AM', b'B8KE', b'01'],
            [b'\x00' * 16],
            [b'AGB KIRBY AM', b'B8KE', b'01'],
            [b'\x00' * 16],
        ]

        with caplog.at_level(logging.INFO):
            assert await client.validate_rom(mock_bizhawk_context) is False
            assert await client.validate_rom(mock_bizhawk_context) is False

    mock_display.assert_awaited_once_with(
        mock_bizhawk_context.bizhawk_ctx,
        "Unable to load ROM: missing patch metadata. Rebuild your patched ROM.",
    )
    assert caplog.text.count("KirbyAM patch metadata was missing") == 1


@pytest.mark.asyncio
async def test_poll_locations_is_noop_and_does_not_read_ram(mock_bizhawk_context):
    """Shard polling is disabled for AP checks and should no-op without RAM reads."""
    client = KirbyAmClient()
    client.initialize_client()

    with patch('worlds.kirbyam.client.bizhawk.read', new_callable=AsyncMock) as mock_read:
        await client._poll_locations(mock_bizhawk_context)
        mock_read.assert_not_awaited()


@pytest.mark.asyncio
async def test_poll_locations_does_not_send_location_checks(mock_bizhawk_context):
    """No LocationChecks should ever be emitted by shard polling."""
    client = KirbyAmClient()
    client.initialize_client()
    mock_bizhawk_context.checked_locations = set()

    with patch.object(mock_bizhawk_context, 'send_msgs', new_callable=AsyncMock) as mock_send:
        await client._poll_locations(mock_bizhawk_context)
    mock_send.assert_not_awaited()


@pytest.mark.asyncio
async def test_reconcile_native_map_ownership_sets_all_map_bits_for_starting_option(mock_bizhawk_context):
    client = KirbyAmClient()
    client.initialize_client()
    mock_bizhawk_context.slot_data["start_with_all_maps"] = True

    with patch('worlds.kirbyam.client.bizhawk.read', new_callable=AsyncMock) as mock_read, \
         patch('worlds.kirbyam.client.bizhawk.write', new_callable=AsyncMock) as mock_write:
        mock_read.return_value = [(1).to_bytes(4, 'little')]

        await client._reconcile_native_map_ownership(mock_bizhawk_context)

    expected_bits = 1
    for area_id in range(1, 10):
        expected_bits |= 1 << area_id
    mock_write.assert_awaited_once_with(
        mock_bizhawk_context.bizhawk_ctx,
        [(
            data.native_ram_addresses["big_chest_bitfield_native"],
            expected_bits.to_bytes(4, 'little'),
            "System Bus",
        )],
    )


@pytest.mark.asyncio
async def test_reconcile_native_map_ownership_uses_only_delivered_map_items(mock_bizhawk_context):
    client = KirbyAmClient()
    client.initialize_client()
    client._delivered_item_index = 2
    mock_bizhawk_context.items_received = [
        Mock(item=3860010, player=1),
        Mock(item=3860024, player=1),
        Mock(item=3860017, player=1),
    ]

    with patch('worlds.kirbyam.client.bizhawk.read', new_callable=AsyncMock) as mock_read, \
         patch('worlds.kirbyam.client.bizhawk.write', new_callable=AsyncMock) as mock_write:
        mock_read.return_value = [(0).to_bytes(4, 'little')]

        await client._reconcile_native_map_ownership(mock_bizhawk_context)

    expected_bits = (1 << 1) | (1 << 4)
    mock_write.assert_awaited_once_with(
        mock_bizhawk_context.bizhawk_ctx,
        [(
            data.native_ram_addresses["big_chest_bitfield_native"],
            expected_bits.to_bytes(4, 'little'),
            "System Bus",
        )],
    )


@pytest.mark.asyncio
async def test_reconcile_native_map_ownership_skips_write_when_native_bits_match(mock_bizhawk_context):
    client = KirbyAmClient()
    client.initialize_client()
    client._delivered_item_index = 1
    mock_bizhawk_context.items_received = [Mock(item=3860013, player=1)]

    with patch('worlds.kirbyam.client.bizhawk.read', new_callable=AsyncMock) as mock_read, \
         patch('worlds.kirbyam.client.bizhawk.write', new_callable=AsyncMock) as mock_write:
        mock_read.return_value = [((1 << 6)).to_bytes(4, 'little')]

        await client._reconcile_native_map_ownership(mock_bizhawk_context)

    mock_write.assert_not_awaited()


def test_ap_owned_native_map_bits_updates_cache_incrementally(mock_bizhawk_context):
    client = KirbyAmClient()
    client.initialize_client()
    mock_bizhawk_context.items_received = [
        Mock(item=3860010, player=1),
        Mock(item=3860024, player=1),
        Mock(item=3860017, player=1),
    ]
    client._delivered_item_index = 2

    with patch.object(client, '_extract_delivery_item_fields', wraps=client._extract_delivery_item_fields) as wrapped_extract:
        first_bits = client._ap_owned_native_map_bits(mock_bizhawk_context)
        first_call_count = wrapped_extract.call_count

        second_bits = client._ap_owned_native_map_bits(mock_bizhawk_context)

        client._delivered_item_index = 3
        third_bits = client._ap_owned_native_map_bits(mock_bizhawk_context)

    first_expected = (
        (1 << _MAP_ITEM_ID_TO_AREA_ID[3860010])
        | (1 << _MAP_ITEM_ID_TO_AREA_ID[3860024])
    )
    third_expected = first_expected | (1 << _MAP_ITEM_ID_TO_AREA_ID[3860017])
    assert first_bits == first_expected
    assert second_bits == first_bits
    assert third_bits == third_expected
    assert first_call_count == 2
    assert wrapped_extract.call_count == 3


def test_ap_owned_native_map_bits_rebuilds_after_delivered_index_rewind(mock_bizhawk_context):
    client = KirbyAmClient()
    client.initialize_client()
    mock_bizhawk_context.items_received = [
        Mock(item=3860010, player=1),
        Mock(item=3860024, player=1),
        Mock(item=3860017, player=1),
    ]

    client._delivered_item_index = 3
    _ = client._ap_owned_native_map_bits(mock_bizhawk_context)

    client._delivered_item_index = 1
    rewound_bits = client._ap_owned_native_map_bits(mock_bizhawk_context)

    assert rewound_bits == (1 << _MAP_ITEM_ID_TO_AREA_ID[3860010])


@pytest.mark.asyncio
async def test_poll_major_chest_sends_location_checks_for_set_bits(mock_bizhawk_context):
    """Set transport major-chest bits should map to major-chest LocationChecks."""
    client = KirbyAmClient()
    client.initialize_client()

    cabbage = data.locations["MAJOR_CHEST_CABBAGE_CAVERN"].location_id
    olive = data.locations["MAJOR_CHEST_OLIVE_OCEAN"].location_id
    peppermint = data.locations["MAJOR_CHEST_PEPPERMINT_PALACE"].location_id
    mock_bizhawk_context.checked_locations = set()

    with patch.dict(data.transport_ram_addresses, {"major_chest_flags": 0x0203B028}, clear=False), \
         patch('worlds.kirbyam.client.bizhawk.read', new_callable=AsyncMock) as mock_read, \
         patch.object(mock_bizhawk_context, 'send_msgs', new_callable=AsyncMock) as mock_send:
        # Bits 3, 6, 7 set => Cabbage, Olive, Peppermint major chests.
        mock_read.return_value = [((1 << 3) | (1 << 6) | (1 << 7)).to_bytes(4, 'little')]

        await client._poll_major_chest_locations(mock_bizhawk_context)

    mock_send.assert_awaited_once_with([
        {"cmd": "LocationChecks", "locations": [cabbage, olive, peppermint]}
    ])


@pytest.mark.asyncio
async def test_poll_major_chest_skips_already_server_acknowledged(mock_bizhawk_context):
    """No major-chest resend when server already acknowledges all mapped transport checks."""
    client = KirbyAmClient()
    client.initialize_client()
    client._debug_logging_enabled = True

    olive = data.locations["MAJOR_CHEST_OLIVE_OCEAN"].location_id
    mock_bizhawk_context.checked_locations = {olive}

    with patch.dict(data.transport_ram_addresses, {"major_chest_flags": 0x0203B028}, clear=False), \
         patch('worlds.kirbyam.client.bizhawk.read', new_callable=AsyncMock) as mock_read, \
         patch.object(mock_bizhawk_context, 'send_msgs', new_callable=AsyncMock) as mock_send, \
         patch('CommonClient.logger') as mock_logger:
        mock_read.return_value = [((1 << 6)).to_bytes(4, 'little')]

        await client._poll_major_chest_locations(mock_bizhawk_context)

    mock_send.assert_not_awaited()
    assert mock_logger.debug.called
    assert "dedupe suppressed major-chest LocationChecks" in mock_logger.debug.call_args.args[0]
    assert mock_logger.debug.call_args.args[1] == [olive]


@pytest.mark.asyncio
async def test_poll_major_chest_skips_when_address_missing(mock_bizhawk_context):
    """Missing transport major chest address should no-op safely."""
    client = KirbyAmClient()
    client.initialize_client()

    transport_without_chests = {k: v for k, v in data.transport_ram_addresses.items() if k != "major_chest_flags"}
    ram_without_chests = {k: v for k, v in data.ram_addresses.items() if k != "major_chest_flags"}

    with patch.dict(data.transport_ram_addresses, transport_without_chests, clear=True), \
         patch.dict(data.ram_addresses, ram_without_chests, clear=True), \
         patch('worlds.kirbyam.client.bizhawk.read', new_callable=AsyncMock) as mock_read, \
         patch.object(mock_bizhawk_context, 'send_msgs', new_callable=AsyncMock) as mock_send:
        await client._poll_major_chest_locations(mock_bizhawk_context)

    mock_read.assert_not_awaited()
    mock_send.assert_not_awaited()


@pytest.mark.asyncio
async def test_shard_poll_does_not_trigger_major_chest_locations(mock_bizhawk_context):
    """Shard polling should not emit major-chest location IDs."""
    client = KirbyAmClient()
    client.initialize_client()

    mock_bizhawk_context.checked_locations = set()

    with patch.object(mock_bizhawk_context, 'send_msgs', new_callable=AsyncMock) as mock_send:
        await client._poll_locations(mock_bizhawk_context)

    mock_send.assert_not_awaited()


@pytest.mark.asyncio
async def test_poll_minor_chest_sends_location_checks_for_set_bits(mock_bizhawk_context):
    """Set native minor-chest bits should map to MINOR_CHEST LocationChecks."""
    client = KirbyAmClient()
    client.initialize_client()

    room_1_20 = data.locations["MINOR_CHEST_RAINBOW_ROUTE_1_20"].location_id
    room_1_22 = data.locations["MINOR_CHEST_RAINBOW_ROUTE_1_22"].location_id
    room_1_38 = data.locations["MINOR_CHEST_RAINBOW_ROUTE_1_38"].location_id
    mock_bizhawk_context.checked_locations = set()

    bits = (1 << 1) | (1 << 23) | (1 << 41)

    with patch.dict(data.native_ram_addresses, {"small_chest_flags_native": 0x02038960}, clear=False), \
         patch('worlds.kirbyam.client.bizhawk.read', new_callable=AsyncMock) as mock_read, \
         patch.object(mock_bizhawk_context, 'send_msgs', new_callable=AsyncMock) as mock_send:
        mock_read.return_value = [bits.to_bytes(10, 'little')]

        await client._poll_minor_chest_locations(mock_bizhawk_context)

    mock_send.assert_awaited_once_with([
        {"cmd": "LocationChecks", "locations": [room_1_20, room_1_22, room_1_38]}
    ])


@pytest.mark.asyncio
async def test_poll_minor_chest_skips_when_address_missing(mock_bizhawk_context):
    """Missing native minor chest address should no-op safely."""
    client = KirbyAmClient()
    client.initialize_client()

    native_without_minor = {k: v for k, v in data.native_ram_addresses.items() if k != "small_chest_flags_native"}

    with patch.dict(data.native_ram_addresses, native_without_minor, clear=True), \
         patch('worlds.kirbyam.client.bizhawk.read', new_callable=AsyncMock) as mock_read, \
         patch.object(mock_bizhawk_context, 'send_msgs', new_callable=AsyncMock) as mock_send:
        await client._poll_minor_chest_locations(mock_bizhawk_context)

    mock_read.assert_not_awaited()
    mock_send.assert_not_awaited()


@pytest.mark.asyncio
async def test_poll_minor_chest_skips_already_server_acknowledged(mock_bizhawk_context):
    """No minor-chest resend when server already acknowledges all mapped checks."""
    client = KirbyAmClient()
    client.initialize_client()
    client._debug_logging_enabled = True

    room_1_20 = data.locations["MINOR_CHEST_RAINBOW_ROUTE_1_20"].location_id
    mock_bizhawk_context.checked_locations = {room_1_20}

    with patch.dict(data.native_ram_addresses, {"small_chest_flags_native": 0x02038960}, clear=False), \
         patch('worlds.kirbyam.client.bizhawk.read', new_callable=AsyncMock) as mock_read, \
         patch.object(mock_bizhawk_context, 'send_msgs', new_callable=AsyncMock) as mock_send, \
         patch('CommonClient.logger') as mock_logger:
        mock_read.return_value = [((1 << 1)).to_bytes(10, 'little')]

        await client._poll_minor_chest_locations(mock_bizhawk_context)

    mock_send.assert_not_awaited()
    assert mock_logger.debug.called
    assert "dedupe suppressed minor-chest LocationChecks" in mock_logger.debug.call_args.args[0]
    assert mock_logger.debug.call_args.args[1] == [room_1_20]


@pytest.mark.asyncio
async def test_poll_vitality_chest_sends_location_checks_for_set_bits(mock_bizhawk_context):
    """Set transport vitality-chest bits should map to vitality-chest LocationChecks."""
    client = KirbyAmClient()
    client.initialize_client()

    carrot = data.locations["VITALITY_CHEST_CARROT_CASTLE"].location_id
    olive = data.locations["VITALITY_CHEST_OLIVE_OCEAN"].location_id
    mock_bizhawk_context.checked_locations = set()

    with patch.dict(data.transport_ram_addresses, {"vitality_chest_flags": 0x0203B02C}, clear=False), \
         patch('worlds.kirbyam.client.bizhawk.read', new_callable=AsyncMock) as mock_read, \
         patch.object(mock_bizhawk_context, 'send_msgs', new_callable=AsyncMock) as mock_send:
        # Bits 0 and 1 set => Carrot Castle and Olive Ocean vitality chests.
        mock_read.return_value = [((1 << 0) | (1 << 1)).to_bytes(4, 'little')]

        await client._poll_vitality_chest_locations(mock_bizhawk_context)

    mock_send.assert_awaited_once_with([
        {"cmd": "LocationChecks", "locations": [carrot, olive]}
    ])


@pytest.mark.asyncio
async def test_poll_vitality_chest_skips_already_server_acknowledged(mock_bizhawk_context):
    """No vitality-chest resend when server already acknowledges all mapped transport checks."""
    client = KirbyAmClient()
    client.initialize_client()
    client._debug_logging_enabled = True

    carrot = data.locations["VITALITY_CHEST_CARROT_CASTLE"].location_id
    mock_bizhawk_context.checked_locations = {carrot}

    with patch.dict(data.transport_ram_addresses, {"vitality_chest_flags": 0x0203B02C}, clear=False), \
         patch('worlds.kirbyam.client.bizhawk.read', new_callable=AsyncMock) as mock_read, \
         patch.object(mock_bizhawk_context, 'send_msgs', new_callable=AsyncMock) as mock_send, \
         patch('CommonClient.logger') as mock_logger:
        mock_read.return_value = [((1 << 0)).to_bytes(4, 'little')]

        await client._poll_vitality_chest_locations(mock_bizhawk_context)

    mock_send.assert_not_awaited()
    assert mock_logger.debug.called
    assert "dedupe suppressed vitality-chest LocationChecks" in mock_logger.debug.call_args.args[0]
    assert mock_logger.debug.call_args.args[1] == [carrot]


@pytest.mark.asyncio
async def test_poll_vitality_chest_skips_when_address_missing(mock_bizhawk_context):
    """Missing transport vitality chest address should no-op safely."""
    client = KirbyAmClient()
    client.initialize_client()

    transport_without_chests = {k: v for k, v in data.transport_ram_addresses.items() if k != "vitality_chest_flags"}
    ram_without_chests = {k: v for k, v in data.ram_addresses.items() if k != "vitality_chest_flags"}

    with patch.dict(data.transport_ram_addresses, transport_without_chests, clear=True), \
         patch.dict(data.ram_addresses, ram_without_chests, clear=True), \
         patch('worlds.kirbyam.client.bizhawk.read', new_callable=AsyncMock) as mock_read, \
         patch.object(mock_bizhawk_context, 'send_msgs', new_callable=AsyncMock) as mock_send:
        await client._poll_vitality_chest_locations(mock_bizhawk_context)

    mock_read.assert_not_awaited()
    mock_send.assert_not_awaited()


@pytest.mark.asyncio
async def test_poll_sound_player_chest_sends_location_checks_for_set_bits(mock_bizhawk_context):
    """Set transport sound-player bit should map to Sound Player chest LocationChecks."""
    client = KirbyAmClient()
    client.initialize_client()

    sound_player = data.locations["SOUND_PLAYER_CHEST"].location_id
    mock_bizhawk_context.checked_locations = set()

    with patch.dict(data.transport_ram_addresses, {"sound_player_chest_flags": 0x0203B030}, clear=False), \
         patch('worlds.kirbyam.client.bizhawk.read', new_callable=AsyncMock) as mock_read, \
         patch.object(mock_bizhawk_context, 'send_msgs', new_callable=AsyncMock) as mock_send:
        mock_read.return_value = [((1 << 0)).to_bytes(4, 'little')]

        await client._poll_sound_player_chest_locations(mock_bizhawk_context)

    mock_send.assert_awaited_once_with([
        {"cmd": "LocationChecks", "locations": [sound_player]}
    ])


@pytest.mark.asyncio
async def test_poll_sound_player_chest_skips_when_address_missing(mock_bizhawk_context):
    """Missing transport Sound Player chest address should no-op safely."""
    client = KirbyAmClient()
    client.initialize_client()

    transport_without_chests = {
        k: v for k, v in data.transport_ram_addresses.items() if k != "sound_player_chest_flags"
    }
    ram_without_chests = {k: v for k, v in data.ram_addresses.items() if k != "sound_player_chest_flags"}

    with patch.dict(data.transport_ram_addresses, transport_without_chests, clear=True), \
         patch.dict(data.ram_addresses, ram_without_chests, clear=True), \
         patch('worlds.kirbyam.client.bizhawk.read', new_callable=AsyncMock) as mock_read, \
         patch.object(mock_bizhawk_context, 'send_msgs', new_callable=AsyncMock) as mock_send:
        await client._poll_sound_player_chest_locations(mock_bizhawk_context)

    mock_read.assert_not_awaited()
    mock_send.assert_not_awaited()


@pytest.mark.asyncio
async def test_poll_hub_switch_sends_location_checks_for_set_bits(mock_bizhawk_context):
    """Set transport hub-switch bits after baseline should map to LocationChecks."""
    client = KirbyAmClient()
    client.initialize_client()

    moonlight = data.locations["HUB_SWITCH_MOONLIGHT"].location_id
    moonlight_bit = data.locations["HUB_SWITCH_MOONLIGHT"].bit_index
    assert moonlight_bit is not None
    rainbow_east = data.locations["HUB_SWITCH_RAINBOW_ROUTE_EAST"].location_id
    mock_bizhawk_context.checked_locations = set()

    with patch.dict(data.transport_ram_addresses, {"hub_switch_flags": 0x0203B04C}, clear=False), \
         patch('worlds.kirbyam.client.bizhawk.read', new_callable=AsyncMock) as mock_read, \
         patch.object(mock_bizhawk_context, 'send_msgs', new_callable=AsyncMock) as mock_send:
        mock_read.side_effect = [
            [(0).to_bytes(4, 'little')],
            [((1 << moonlight_bit) | (1 << 1)).to_bytes(4, 'little')],
        ]

        await client._poll_hub_switch_locations(mock_bizhawk_context)
        await client._poll_hub_switch_locations(mock_bizhawk_context)

    mock_send.assert_awaited_once_with([
        {"cmd": "LocationChecks", "locations": [rainbow_east, moonlight]}
    ])


@pytest.mark.asyncio
async def test_poll_hub_switch_suppresses_pre_session_stale_bits(mock_bizhawk_context):
    """First hub-switch poll with empty checked_locations should baseline and suppress stale bits."""
    client = KirbyAmClient()
    client.initialize_client()
    client._debug_logging_enabled = True

    mock_bizhawk_context.checked_locations = set()

    with patch.dict(data.transport_ram_addresses, {"hub_switch_flags": 0x0203B04C}, clear=False), \
         patch('worlds.kirbyam.client.bizhawk.read', new_callable=AsyncMock) as mock_read, \
         patch.object(mock_bizhawk_context, 'send_msgs', new_callable=AsyncMock) as mock_send, \
         patch('CommonClient.logger') as mock_logger:
        mock_read.return_value = [((1 << 0)).to_bytes(4, 'little')]

        await client._poll_hub_switch_locations(mock_bizhawk_context)
        await client._poll_hub_switch_locations(mock_bizhawk_context)

    mock_send.assert_not_awaited()
    assert mock_logger.info.called
    assert "hub-switch baseline initialized" in mock_logger.info.call_args.args[0]


@pytest.mark.asyncio
async def test_poll_hub_switch_skips_already_server_acknowledged(mock_bizhawk_context):
    """No hub-switch resend when server already acknowledges all mapped transport checks."""
    client = KirbyAmClient()
    client.initialize_client()
    client._debug_logging_enabled = True

    moonlight = data.locations["HUB_SWITCH_MOONLIGHT"].location_id
    moonlight_bit = data.locations["HUB_SWITCH_MOONLIGHT"].bit_index
    assert moonlight_bit is not None
    mock_bizhawk_context.checked_locations = {moonlight}

    with patch.dict(data.transport_ram_addresses, {"hub_switch_flags": 0x0203B04C}, clear=False), \
         patch('worlds.kirbyam.client.bizhawk.read', new_callable=AsyncMock) as mock_read, \
         patch.object(mock_bizhawk_context, 'send_msgs', new_callable=AsyncMock) as mock_send, \
         patch('CommonClient.logger') as mock_logger:
        mock_read.return_value = [((1 << moonlight_bit)).to_bytes(4, 'little')]

        await client._poll_hub_switch_locations(mock_bizhawk_context)

    mock_send.assert_not_awaited()
    assert mock_logger.debug.called
    assert "dedupe suppressed hub-switch LocationChecks" in mock_logger.debug.call_args.args[0]
    assert mock_logger.debug.call_args.args[1] == [moonlight]


@pytest.mark.asyncio
async def test_poll_hub_switch_skips_when_address_missing(mock_bizhawk_context):
    """Missing transport hub-switch address should no-op safely."""
    client = KirbyAmClient()
    client.initialize_client()

    transport_without_hub_switch = {k: v for k, v in data.transport_ram_addresses.items() if k != "hub_switch_flags"}
    ram_without_hub_switch = {k: v for k, v in data.ram_addresses.items() if k != "hub_switch_flags"}

    with patch.dict(data.transport_ram_addresses, transport_without_hub_switch, clear=True), \
         patch.dict(data.ram_addresses, ram_without_hub_switch, clear=True), \
         patch('worlds.kirbyam.client.bizhawk.read', new_callable=AsyncMock) as mock_read, \
         patch.object(mock_bizhawk_context, 'send_msgs', new_callable=AsyncMock) as mock_send:
        await client._poll_hub_switch_locations(mock_bizhawk_context)

    mock_read.assert_not_awaited()
    mock_send.assert_not_awaited()


@pytest.mark.asyncio
async def test_poll_hub_switch_rebaselines_on_stream_marker_change(mock_bizhawk_context):
    """Hub-switch baseline persists across AP reconnect, but stream change forces re-baseline."""
    client = KirbyAmClient()
    client.initialize_client()

    rainbow_east = data.locations["HUB_SWITCH_RAINBOW_ROUTE_EAST"].location_id
    mock_bizhawk_context.checked_locations = set()
    mock_bizhawk_context.bizhawk_ctx.streams = object()

    with patch.dict(data.transport_ram_addresses, {"hub_switch_flags": 0x0203B04C}, clear=False), \
         patch('worlds.kirbyam.client.bizhawk.read', new_callable=AsyncMock) as mock_read, \
         patch.object(mock_bizhawk_context, 'send_msgs', new_callable=AsyncMock) as mock_send:
        mock_read.side_effect = [
            [((1 << 10)).to_bytes(4, 'little')],
            [((1 << 10)).to_bytes(4, 'little')],
            [((1 << 10) | (1 << 1)).to_bytes(4, 'little')],
        ]

        await client._poll_hub_switch_locations(mock_bizhawk_context)

        # Simulate BizHawk stream identity change (ROM resync / reconnect).
        mock_bizhawk_context.bizhawk_ctx.streams = object()
        await client._poll_hub_switch_locations(mock_bizhawk_context)
        await client._poll_hub_switch_locations(mock_bizhawk_context)

    mock_send.assert_awaited_once_with([
        {"cmd": "LocationChecks", "locations": [rainbow_east]}
    ])


@pytest.mark.asyncio
async def test_poll_room_entry_logging_logs_only_on_room_change(mock_bizhawk_context):
    client = KirbyAmClient()
    client.initialize_client()
    client._room_label_by_doors_idx = {42: "REGION_TEST_ROOM"}
    client._room_region_key_by_doors_idx = {42: "ROOM_SANITY_1_20"}

    with patch('worlds.kirbyam.client.bizhawk.read', new_callable=AsyncMock) as mock_read, \
         patch('CommonClient.logger') as mock_logger:
        mock_read.side_effect = [
            [(0x0010).to_bytes(2, 'little')],
            [(42).to_bytes(2, 'little')],
            [(0x0010).to_bytes(2, 'little')],
        ]

        await client._poll_room_entry_logging(mock_bizhawk_context)
        await client._poll_room_entry_logging(mock_bizhawk_context)

    assert mock_read.await_count == 3
    mock_bizhawk_context.send_msgs.assert_awaited_once_with([{
        "cmd": "Bounce",
        "slots": [mock_bizhawk_context.slot],
        "data": {
            "type": _ROOM_UPDATE_BOUNCE_TYPE,
            "nativeRoomId": 0x0010,
            "doorsIdx": 42,
            "roomRegionKey": "ROOM_SANITY_1_20",
            "roomLabel": "REGION_TEST_ROOM",
        },
    }])
    mock_logger.info.assert_called_once_with(
        "KirbyAM: entered room %s (native=0x%04x, doorsIdx=%d)",
        "REGION_TEST_ROOM",
        0x0010,
        42,
        extra={"NoStream": True},
    )


@pytest.mark.asyncio
async def test_poll_room_entry_logging_reads_doors_idx_from_rom_lookup(mock_bizhawk_context):
    client = KirbyAmClient()
    client.initialize_client()
    client._debug_logging_enabled = True
    client._room_label_by_doors_idx = {7: "REGION_LOOKUP_ROOM"}
    client._room_region_key_by_doors_idx = {7: "ROOM_SANITY_2_01"}

    native_room_id = 0x0021
    expected_rom_addr = _ROOM_PROPS_ROM_BASE + native_room_id * _ROOM_PROPS_STRIDE + _ROOM_PROPS_DOORS_IDX_OFFSET

    with patch('worlds.kirbyam.client.bizhawk.read', new_callable=AsyncMock) as mock_read, \
         patch('CommonClient.logger') as mock_logger:
        mock_read.side_effect = [
            [native_room_id.to_bytes(2, 'little')],
            [(7).to_bytes(2, 'little')],
        ]

        await client._poll_room_entry_logging(mock_bizhawk_context)

    mock_read.assert_any_await(
        mock_bizhawk_context.bizhawk_ctx,
        [(expected_rom_addr, 2, "ROM")],
    )
    mock_bizhawk_context.send_msgs.assert_awaited_once_with([{
        "cmd": "Bounce",
        "slots": [mock_bizhawk_context.slot],
        "data": {
            "type": _ROOM_UPDATE_BOUNCE_TYPE,
            "nativeRoomId": native_room_id,
            "doorsIdx": 7,
            "roomRegionKey": "ROOM_SANITY_2_01",
            "roomLabel": "REGION_LOOKUP_ROOM",
        },
    }])
    mock_logger.info.assert_called_once_with(
        "KirbyAM: entered room %s (native=0x%04x, doorsIdx=%d)",
        "REGION_LOOKUP_ROOM",
        native_room_id,
        7,
        extra={"NoStream": False},
    )


@pytest.mark.asyncio
async def test_poll_room_entry_logging_handles_rom_lookup_failure(mock_bizhawk_context):
    client = KirbyAmClient()
    client.initialize_client()

    with patch('worlds.kirbyam.client.bizhawk.read', new_callable=AsyncMock) as mock_read, \
         patch('CommonClient.logger') as mock_logger:
        mock_read.side_effect = [
            [(0x0003).to_bytes(2, 'little')],
            bizhawk.SyncError("lookup failed"),
        ]

        await client._poll_room_entry_logging(mock_bizhawk_context)

    mock_logger.info.assert_called_once_with(
        "KirbyAM: room entry — native=0x%04x (doorsIdx lookup failed)",
        0x0003,
        extra={"NoStream": True},
    )


@pytest.mark.asyncio
async def test_poll_room_entry_logging_retries_after_short_rom_read(mock_bizhawk_context):
    client = KirbyAmClient()
    client.initialize_client()
    client._room_label_by_doors_idx = {11: "REGION_RETRY_ROOM"}
    client._room_region_key_by_doors_idx = {11: "ROOM_SANITY_3_02"}

    with patch('worlds.kirbyam.client.bizhawk.read', new_callable=AsyncMock) as mock_read, \
         patch('CommonClient.logger') as mock_logger:
        mock_read.side_effect = [
            [(0x0008).to_bytes(2, 'little')],
            [b'\x0b'],
            [(0x0008).to_bytes(2, 'little')],
            [(11).to_bytes(2, 'little')],
        ]

        await client._poll_room_entry_logging(mock_bizhawk_context)
        await client._poll_room_entry_logging(mock_bizhawk_context)

    assert client._last_native_room_id == 0x0008
    mock_bizhawk_context.send_msgs.assert_awaited_once_with([{
        "cmd": "Bounce",
        "slots": [mock_bizhawk_context.slot],
        "data": {
            "type": _ROOM_UPDATE_BOUNCE_TYPE,
            "nativeRoomId": 0x0008,
            "doorsIdx": 11,
            "roomRegionKey": "ROOM_SANITY_3_02",
            "roomLabel": "REGION_RETRY_ROOM",
        },
    }])
    mock_logger.info.assert_called_once_with(
        "KirbyAM: entered room %s (native=0x%04x, doorsIdx=%d)",
        "REGION_RETRY_ROOM",
        0x0008,
        11,
        extra={"NoStream": True},
    )


@pytest.mark.asyncio
async def test_poll_room_entry_logging_re_emits_on_reconnect_state_reset(mock_bizhawk_context):
    client = KirbyAmClient()
    client.initialize_client()
    client._room_label_by_doors_idx = {9: "REGION_RECONNECT_ROOM"}
    client._room_region_key_by_doors_idx = {9: "ROOM_SANITY_4_01"}

    with patch('worlds.kirbyam.client.bizhawk.read', new_callable=AsyncMock) as mock_read:
        mock_read.side_effect = [
            [(0x0015).to_bytes(2, 'little')],
            [(9).to_bytes(2, 'little')],
            [(0x0015).to_bytes(2, 'little')],
            [(9).to_bytes(2, 'little')],
        ]

        await client._poll_room_entry_logging(mock_bizhawk_context)
        client._reset_reconnect_transient_state()
        await client._poll_room_entry_logging(mock_bizhawk_context)

    assert mock_bizhawk_context.send_msgs.await_count == 2
    first_payload = mock_bizhawk_context.send_msgs.await_args_list[0].args[0][0]
    second_payload = mock_bizhawk_context.send_msgs.await_args_list[1].args[0][0]
    assert first_payload["cmd"] == "Bounce"
    assert second_payload["cmd"] == "Bounce"
    assert first_payload["data"]["type"] == _ROOM_UPDATE_BOUNCE_TYPE
    assert second_payload["data"]["type"] == _ROOM_UPDATE_BOUNCE_TYPE
    assert first_payload["data"]["nativeRoomId"] == 0x0015
    assert second_payload["data"]["nativeRoomId"] == 0x0015


@pytest.mark.asyncio
async def test_poll_room_entry_logging_retries_after_bounce_send_failure(mock_bizhawk_context):
    client = KirbyAmClient()
    client.initialize_client()
    client._room_label_by_doors_idx = {12: "REGION_SEND_RETRY_ROOM"}
    client._room_region_key_by_doors_idx = {12: "ROOM_SANITY_5_10"}

    with patch('worlds.kirbyam.client.bizhawk.read', new_callable=AsyncMock) as mock_read, \
         patch.object(mock_bizhawk_context, 'send_msgs', new_callable=AsyncMock) as mock_send, \
         patch('CommonClient.logger') as mock_logger:
        mock_read.side_effect = [
            [(0x0020).to_bytes(2, 'little')],
            [(12).to_bytes(2, 'little')],
            [(0x0020).to_bytes(2, 'little')],
            [(12).to_bytes(2, 'little')],
        ]
        mock_send.side_effect = [RuntimeError("socket down"), None]

        await client._poll_room_entry_logging(mock_bizhawk_context)
        assert client._last_native_room_id == 0x0020
        assert client._last_sent_room_update_native_room_id is None

        await client._poll_room_entry_logging(mock_bizhawk_context)

    assert client._last_native_room_id == 0x0020
    assert client._last_sent_room_update_native_room_id == 0x0020
    assert mock_send.await_count == 2
    mock_logger.info.assert_called_once_with(
        "KirbyAM: entered room %s (native=0x%04x, doorsIdx=%d)",
        "REGION_SEND_RETRY_ROOM",
        0x0020,
        12,
        extra={"NoStream": True},
    )


@pytest.mark.asyncio
async def test_poll_room_entry_logging_nostream_gating_respects_debug_flag(mock_bizhawk_context):
    client = KirbyAmClient()
    client.initialize_client()
    client._room_label_by_doors_idx = {9: "REGION_NOSTREAM_ROOM"}

    with patch('worlds.kirbyam.client.bizhawk.read', new_callable=AsyncMock) as mock_read, \
         patch('CommonClient.logger') as mock_logger:
        mock_read.side_effect = [
            [(0x0012).to_bytes(2, 'little')],
            [(9).to_bytes(2, 'little')],
        ]
        await client._poll_room_entry_logging(mock_bizhawk_context)

    mock_logger.info.assert_called_once()
    assert mock_logger.info.call_args.kwargs.get("extra", {}).get("NoStream") is True

    client._last_native_room_id = None
    client._debug_logging_enabled = True

    with patch('worlds.kirbyam.client.bizhawk.read', new_callable=AsyncMock) as mock_read, \
         patch('CommonClient.logger') as mock_logger:
        mock_read.side_effect = [
            [(0x0013).to_bytes(2, 'little')],
            [(9).to_bytes(2, 'little')],
        ]
        await client._poll_room_entry_logging(mock_bizhawk_context)

    mock_logger.info.assert_called_once()
    assert mock_logger.info.call_args.kwargs.get("extra", {}).get("NoStream") is False


def test_major_chest_data_sanity():
    """Major-chest entries should have explicit unique IDs and unique mapped bits."""
    major_chests = [
        loc for loc in data.locations.values()
        if loc.category.name == "MAJOR_CHEST"
    ]

    assert major_chests

    ids = [loc.location_id for loc in major_chests]
    assert all(loc_id is not None for loc_id in ids)
    assert len(ids) == len(set(ids))

    bits = [loc.bit_index for loc in major_chests]
    assert all(bit is not None for bit in bits)
    assert len(bits) == len(set(bits))


def test_vitality_chest_data_sanity():
    """Vitality-chest entries should have explicit unique IDs and unique mapped bits."""
    vitality_chests = [
        loc for loc in data.locations.values()
        if loc.category.name == "VITALITY_CHEST"
    ]

    assert len(vitality_chests) == 4

    ids = [loc.location_id for loc in vitality_chests]
    assert all(loc_id is not None for loc_id in ids)
    assert len(ids) == len(set(ids))

    bits = [loc.bit_index for loc in vitality_chests]
    assert all(bit is not None for bit in bits)
    assert len(bits) == len(set(bits))


def test_sound_player_chest_data_sanity():
    """Sound Player chest entry should have explicit unique ID and mapped transport bit."""
    sound_player_chests = [
        loc for loc in data.locations.values()
        if loc.category.name == "SOUND_PLAYER_CHEST"
    ]

    assert len(sound_player_chests) == 1

    sound_player = sound_player_chests[0]
    assert sound_player.location_id is not None
    assert sound_player.bit_index == 0


def test_hub_switch_data_sanity():
    """Hub-switch entries should have explicit unique IDs and unique mapped bits."""
    hub_switches = [
        loc for loc in data.locations.values()
        if loc.category.name == "HUB_SWITCH"
    ]

    assert len(hub_switches) == 15

    ids = [loc.location_id for loc in hub_switches]
    assert all(loc_id is not None for loc_id in ids)
    assert len(ids) == len(set(ids))

    bits = [loc.bit_index for loc in hub_switches]
    assert all(bit is not None for bit in bits)
    assert len(bits) == len(set(bits))


def test_client_initialization():
    """Test client state is properly initialized."""
    client = KirbyAmClient()
    client.initialize_client()
    
    assert client._checked_location_bits == set()
    assert client._delivered_item_index == 0
    assert client._delivery_pending is False
    assert client._delivery_pending_frame is None
    assert client._goal_reported is False


@pytest.mark.asyncio
async def test_deliver_items_resyncs_after_save_loss(mock_bizhawk_context):
    """If ROM counter regresses, client should rewind delivery cursor and resend."""
    client = KirbyAmClient()
    client.initialize_client()
    client._delivered_item_index = 3
    client._delivery_pending = False

    mock_bizhawk_context.items_received = [
        Mock(item=3860001, player=1),
        Mock(item=3860002, player=1),
        Mock(item=3860003, player=1),
        Mock(item=3860004, player=1),
    ]

    with patch('worlds.kirbyam.client.bizhawk.read', new_callable=AsyncMock) as mock_read, \
         patch('worlds.kirbyam.client.bizhawk.write', new_callable=AsyncMock) as mock_write:
        # mailbox empty, ROM says only one item was actually applied
        mock_read.return_value = [
            (0).to_bytes(4, 'little'),
            (1).to_bytes(4, 'little'),
        ]

        await client._deliver_items(mock_bizhawk_context)

        assert client._delivered_item_index == 1
        assert client._delivery_pending is True
        written = mock_write.await_args.args[1]
        assert written[0][1] == int(3860002).to_bytes(4, 'little')


@pytest.mark.asyncio
async def test_deliver_items_does_not_fast_forward_when_not_pending(mock_bizhawk_context):
    """In-range forward ROM counters are advisory unless a pending mailbox ACK is in flight."""
    client = KirbyAmClient()
    client.initialize_client()
    client._delivered_item_index = 0
    client._delivery_pending = False

    mock_bizhawk_context.items_received = [
        Mock(item=3860001, player=1),
        Mock(item=3860002, player=1),
        Mock(item=3860003, player=1),
    ]

    with patch('worlds.kirbyam.client.bizhawk.read', new_callable=AsyncMock) as mock_read, \
         patch('worlds.kirbyam.client.bizhawk.write', new_callable=AsyncMock) as mock_write:
        # mailbox empty, ROM counter is ahead but no pending ACK exists
        mock_read.return_value = [
            (0).to_bytes(4, 'little'),
            (2).to_bytes(4, 'little'),
        ]

        await client._deliver_items(mock_bizhawk_context)

        assert client._delivered_item_index == 0
        assert client._delivery_pending is True
        written = mock_write.await_args.args[1]
        assert written[0][1] == int(3860001).to_bytes(4, 'little')


@pytest.mark.asyncio
async def test_deliver_items_continues_when_rom_counter_ahead_of_received_items(mock_bizhawk_context, caplog):
    """A stale/high ROM counter should not permanently suppress mailbox writes."""
    client = KirbyAmClient()
    client.initialize_client()
    client._debug_logging_enabled = True
    client._delivered_item_index = 0
    client._delivery_pending = False

    mock_bizhawk_context.items_received = [
        Mock(item=3860001, player=1),
    ]

    caplog.set_level(logging.INFO, logger="Client")

    with patch('worlds.kirbyam.client.bizhawk.read', new_callable=AsyncMock) as mock_read, \
         patch('worlds.kirbyam.client.bizhawk.write', new_callable=AsyncMock) as mock_write:
        mock_read.return_value = [
            (0).to_bytes(4, 'little'),
            (2).to_bytes(4, 'little'),
            (333).to_bytes(4, 'little'),
        ]

        await client._deliver_items(mock_bizhawk_context)

        assert client._delivered_item_index == 0
        assert client._delivery_pending is True
        assert client._delivery_pending_frame == 333
        mock_write.assert_awaited_once()
        written = mock_write.await_args.args[1]
        assert written == [
            (data.transport_ram_addresses["incoming_item_id"], int(3860001).to_bytes(4, 'little'), "System Bus"),
            (data.transport_ram_addresses["incoming_item_player"], (1).to_bytes(4, 'little'), "System Bus"),
            (data.transport_ram_addresses["incoming_item_flag"], (1).to_bytes(4, 'little'), "System Bus"),
        ]

    assert "ROM delivery counter is ahead of received items" in caplog.text
    assert "ROM counter fallback active; continuing mailbox delivery" in caplog.text


@pytest.mark.asyncio
async def test_deliver_items_logs_when_rom_counter_returns_in_range(mock_bizhawk_context, caplog):
    """Ahead-counter fallback should clear once ROM and server state are plausibly aligned again."""
    client = KirbyAmClient()
    client.initialize_client()
    client._debug_logging_enabled = True
    client._delivered_item_index = 0
    client._delivery_counter_ahead_fallback_active = True
    client._delivery_counter_ahead_resume_logged = True

    caplog.set_level(logging.INFO, logger="Client")

    with patch('worlds.kirbyam.client.bizhawk.read', new_callable=AsyncMock) as mock_read:
        mock_read.return_value = [
            (0).to_bytes(4, 'little'),
            (0).to_bytes(4, 'little'),
            (500).to_bytes(4, 'little'),
        ]

        await client._deliver_items(mock_bizhawk_context, allow_new_writes=False)

    assert client._delivery_counter_ahead_fallback_active is False
    assert client._delivery_counter_ahead_resume_logged is False
    assert "ROM delivery counter is back in range" in caplog.text


@pytest.mark.asyncio
async def test_deliver_items_rom_counter_logs_hidden_from_stream_when_debug_disabled(mock_bizhawk_context):
    client = KirbyAmClient()
    client.initialize_client()
    client._delivered_item_index = 0
    client._delivery_pending = False

    mock_bizhawk_context.items_received = [
        Mock(item=3860001, player=1),
    ]

    with patch('worlds.kirbyam.client.bizhawk.read', new_callable=AsyncMock) as mock_read, \
         patch('worlds.kirbyam.client.bizhawk.write', new_callable=AsyncMock), \
         patch('CommonClient.logger') as mock_logger:
        mock_read.return_value = [
            (0).to_bytes(4, 'little'),
            (2).to_bytes(4, 'little'),
            (333).to_bytes(4, 'little'),
        ]

        await client._deliver_items(mock_bizhawk_context)

    assert any(
        call.args and isinstance(call.args[0], str) and "ROM delivery counter" in call.args[0]
        for call in mock_logger.info.call_args_list
    )
    assert any(
        call.args and isinstance(call.args[0], str) and "ROM counter fallback active" in call.args[0]
        for call in mock_logger.info.call_args_list
    )
    assert all(
        call.kwargs.get("extra", {}).get("NoStream") is True
        for call in mock_logger.info.call_args_list
        if call.args and isinstance(call.args[0], str) and (
            "ROM delivery counter" in call.args[0] or "ROM counter fallback active" in call.args[0]
        )
    )


@pytest.mark.asyncio
async def test_deliver_items_skips_malformed_entries_and_logs_warning(mock_bizhawk_context, caplog):
    """Malformed ReceivedItems entries should be skipped, logged, and not crash delivery."""
    client = KirbyAmClient()
    client.initialize_client()

    mock_bizhawk_context.items_received = [
        Mock(item="bad", player=1),
        Mock(item=3860001, player=1),
    ]

    caplog.set_level(logging.WARNING, logger="Client")

    with patch('worlds.kirbyam.client.bizhawk.read', new_callable=AsyncMock) as mock_read, \
         patch('worlds.kirbyam.client.bizhawk.write', new_callable=AsyncMock) as mock_write:
        mock_read.return_value = [
            (0).to_bytes(4, 'little'),
            (0).to_bytes(4, 'little'),
        ]

        await client._deliver_items(mock_bizhawk_context)

        assert client._delivery_pending is True
        assert client._delivered_item_index == 1
        written = mock_write.await_args.args[1]
        assert written[0][1] == int(3860001).to_bytes(4, 'little')

    assert "Skipping malformed ReceivedItems entry" in caplog.text


@pytest.mark.asyncio
async def test_deliver_items_clears_stuck_mailbox_after_timeout(mock_bizhawk_context, caplog):
    """A stuck mailbox flag should time out, clear, and keep the same item index for retry."""
    client = KirbyAmClient()
    client.initialize_client()
    client._delivery_pending = True
    client._delivery_pending_frame = 100
    client._delivered_item_index = 0

    mock_bizhawk_context.items_received = [
        Mock(item=3860001, player=1),
    ]

    caplog.set_level(logging.WARNING, logger="Client")

    with patch('worlds.kirbyam.client.bizhawk.read', new_callable=AsyncMock) as mock_read, \
         patch('worlds.kirbyam.client.bizhawk.write', new_callable=AsyncMock) as mock_write:
        mock_read.return_value = [
            (1).to_bytes(4, 'little'),
            (0).to_bytes(4, 'little'),
            (131).to_bytes(4, 'little'),
        ]

        await client._deliver_items(mock_bizhawk_context)

        mock_write.assert_awaited_once_with(
            mock_bizhawk_context.bizhawk_ctx,
            [(data.transport_ram_addresses["incoming_item_flag"], (0).to_bytes(4, 'little'), 'System Bus')]
        )
        assert client._delivery_pending is False
        assert client._delivery_pending_frame is None
        assert client._delivered_item_index == 0

    assert "Mailbox ACK timeout" in caplog.text


@pytest.mark.asyncio
async def test_deliver_items_clears_stuck_mailbox_after_wall_clock_timeout(mock_bizhawk_context, caplog):
    """A stuck mailbox flag should time out via wall-clock fallback when frame_counter is stuck."""
    client = KirbyAmClient()
    client.initialize_client()
    client._delivery_pending = True
    client._delivery_pending_frame = 0
    client._delivery_pending_time = 100.0
    client._delivered_item_index = 0

    mock_bizhawk_context.items_received = [
        Mock(item=3860001, player=1),
    ]

    caplog.set_level(logging.WARNING, logger="Client")

    with patch('worlds.kirbyam.client.bizhawk.read', new_callable=AsyncMock) as mock_read, \
         patch('worlds.kirbyam.client.bizhawk.write', new_callable=AsyncMock) as mock_write, \
         patch('worlds.kirbyam.client.time.monotonic', return_value=101.1):
        mock_read.return_value = [
            (1).to_bytes(4, 'little'),
            (0).to_bytes(4, 'little'),
            (0).to_bytes(4, 'little'),
            (1).to_bytes(4, 'little'),
        ]

        await client._deliver_items(mock_bizhawk_context)

        mock_write.assert_awaited_once_with(
            mock_bizhawk_context.bizhawk_ctx,
            [(data.transport_ram_addresses["incoming_item_flag"], (0).to_bytes(4, 'little'), 'System Bus')]
        )
        assert client._delivery_pending is False
        assert client._delivery_pending_frame is None
        assert client._delivery_pending_time is None
        assert client._delivery_pending_item_index is None
        assert client._delivered_item_index == 0
        assert client._delivery_retry_not_before == pytest.approx(101.6)

    assert "Mailbox ACK timeout" in caplog.text
    assert "time timeout (1.1s >= 1.0s)" in caplog.text


@pytest.mark.asyncio
async def test_deliver_items_does_not_use_time_fallback_when_frame_advances(mock_bizhawk_context):
    """Monotonic timeout fallback should not trigger while frame_counter advances."""
    client = KirbyAmClient()
    client.initialize_client()
    client._delivery_pending = True
    client._delivery_pending_frame = 100
    client._delivery_pending_time = 100.0
    client._delivered_item_index = 0

    mock_bizhawk_context.items_received = [
        Mock(item=3860001, player=1),
    ]

    with patch('worlds.kirbyam.client.bizhawk.read', new_callable=AsyncMock) as mock_read, \
         patch('worlds.kirbyam.client.bizhawk.write', new_callable=AsyncMock) as mock_write, \
         patch('worlds.kirbyam.client.time.monotonic', return_value=101.5):
        mock_read.return_value = [
            (1).to_bytes(4, 'little'),
            (0).to_bytes(4, 'little'),
            (101).to_bytes(4, 'little'),
            (1).to_bytes(4, 'little'),
        ]

        await client._deliver_items(mock_bizhawk_context)

        mock_write.assert_not_awaited()
        assert client._delivery_pending is True
        assert client._delivery_pending_frame == 100
        assert client._delivery_pending_time == 100.0


@pytest.mark.asyncio
async def test_deliver_items_records_pending_frame_when_writing(mock_bizhawk_context):
    """Writing a mailbox item should capture the current frame for timeout tracking."""
    client = KirbyAmClient()
    client.initialize_client()

    mock_bizhawk_context.items_received = [
        Mock(item=3860001, player=1),
    ]

    with patch('worlds.kirbyam.client.bizhawk.read', new_callable=AsyncMock) as mock_read, \
         patch('worlds.kirbyam.client.bizhawk.write', new_callable=AsyncMock) as mock_write:
        mock_read.return_value = [
            (0).to_bytes(4, 'little'),
            (0).to_bytes(4, 'little'),
            (1234).to_bytes(4, 'little'),
        ]

        await client._deliver_items(mock_bizhawk_context)

        mock_write.assert_awaited_once()
        assert client._delivery_pending is True
        assert client._delivery_pending_frame == 1234


@pytest.mark.asyncio
async def test_deliver_items_ack_clears_pending_and_advances_cursor(mock_bizhawk_context):
    """ROM ACK should clear pending state, persist cursor, and emit receive notification once."""
    client = KirbyAmClient()
    client.initialize_client()
    client._delivery_pending = True
    client._delivery_pending_item_index = 0
    client._delivered_item_index = 0

    mock_bizhawk_context.items_received = [
        Mock(item=3860001, player=1),
    ]

    with patch.dict(data.transport_ram_addresses, {"debug_item_counter": None}, clear=False), \
         patch('worlds.kirbyam.client.bizhawk.read', new_callable=AsyncMock) as mock_read, \
         patch('worlds.kirbyam.client.bizhawk.write', new_callable=AsyncMock) as mock_write, \
         patch.object(client, '_emit_receive_notification', new_callable=AsyncMock) as mock_emit:
        mock_read.return_value = [
            (0).to_bytes(4, 'little'),
            (250).to_bytes(4, 'little'),
        ]

        await client._deliver_items(mock_bizhawk_context)

    assert client._delivery_pending is False
    assert client._delivery_pending_frame is None
    assert client._delivery_pending_item_index is None
    assert client._delivered_item_index == 1
    mock_write.assert_awaited_once_with(
        mock_bizhawk_context.bizhawk_ctx,
        [(data.transport_ram_addresses["delivered_item_index"], (1).to_bytes(4, 'little'), 'System Bus')]
    )
    mock_emit.assert_awaited_once_with(mock_bizhawk_context, 0)


@pytest.mark.asyncio
async def test_deliver_items_fast_forward_on_pending_ack(mock_bizhawk_context):
    """Pending-ACK fast-forward reconciliation should advance cursor and can queue the next mailbox write."""
    client = KirbyAmClient()
    client.initialize_client()
    client._delivered_item_index = 0
    client._delivery_pending = True
    client._delivery_pending_item_index = 0

    mock_bizhawk_context.items_received = [
        Mock(item=3860001, player=1),
        Mock(item=3860002, player=1),
        Mock(item=3860003, player=1),
    ]

    with patch('worlds.kirbyam.client.bizhawk.read', new_callable=AsyncMock) as mock_read, \
         patch('worlds.kirbyam.client.bizhawk.write', new_callable=AsyncMock) as mock_write:
        mock_read.return_value = [
            (0).to_bytes(4, 'little'),
            (2).to_bytes(4, 'little'),
            (900).to_bytes(4, 'little'),
        ]

        await client._deliver_items(mock_bizhawk_context)

    assert client._delivered_item_index == 2
    assert client._delivery_pending is True
    assert client._delivery_pending_item_index == 2
    assert client._delivery_pending_frame == 900

    written_batches = [call.args[1] for call in mock_write.await_args_list]
    assert [
        (data.transport_ram_addresses["delivered_item_index"], (2).to_bytes(4, 'little'), 'System Bus')
    ] in written_batches
    assert [
        (data.transport_ram_addresses["incoming_item_id"], int(3860003).to_bytes(4, 'little'), 'System Bus'),
        (data.transport_ram_addresses["incoming_item_player"], (1).to_bytes(4, 'little'), 'System Bus'),
        (data.transport_ram_addresses["incoming_item_flag"], (1).to_bytes(4, 'little'), 'System Bus'),
    ] in written_batches
    assert [
        (data.transport_ram_addresses["incoming_item_flag"], (0).to_bytes(4, 'little'), 'System Bus')
    ] not in written_batches


@pytest.mark.asyncio
async def test_deliver_items_fast_forward_log_gated_by_debug(mock_bizhawk_context):
    client = KirbyAmClient()
    client.initialize_client()
    client._delivered_item_index = 0
    client._delivery_pending = True
    client._delivery_pending_item_index = 0

    mock_bizhawk_context.items_received = [
        Mock(item=3860001, player=1),
        Mock(item=3860002, player=1),
        Mock(item=3860003, player=1),
    ]

    with patch('worlds.kirbyam.client.bizhawk.read', new_callable=AsyncMock) as mock_read, \
         patch('worlds.kirbyam.client.bizhawk.write', new_callable=AsyncMock), \
         patch('CommonClient.logger') as mock_logger:
        mock_read.return_value = [
            (0).to_bytes(4, 'little'),
            (2).to_bytes(4, 'little'),
        ]

        await client._deliver_items(mock_bizhawk_context)

    matching_disabled = [
        call
        for call in mock_logger.info.call_args_list
        if call.args and isinstance(call.args[0], str) and "ROM delivery counter moved forward" in call.args[0]
    ]
    assert matching_disabled
    assert all(call.kwargs.get("extra", {}).get("NoStream") is True for call in matching_disabled)

    client = KirbyAmClient()
    client.initialize_client()
    client._debug_logging_enabled = True
    client._delivered_item_index = 0
    client._delivery_pending = True
    client._delivery_pending_item_index = 0

    with patch('worlds.kirbyam.client.bizhawk.read', new_callable=AsyncMock) as mock_read, \
         patch('worlds.kirbyam.client.bizhawk.write', new_callable=AsyncMock), \
         patch('CommonClient.logger') as mock_logger:
        mock_read.return_value = [
            (0).to_bytes(4, 'little'),
            (2).to_bytes(4, 'little'),
        ]

        await client._deliver_items(mock_bizhawk_context)

    mock_logger.info.assert_any_call(
        "KirbyAM: ROM delivery counter moved forward from %s to %s on pending ACK; fast-forwarding client delivery cursor",
        0,
        2,
        extra={"NoStream": False},
    )


@pytest.mark.asyncio
async def test_deliver_items_mailbox_write_log_gated_by_debug(mock_bizhawk_context):
    client = KirbyAmClient()
    client.initialize_client()

    mock_bizhawk_context.items_received = [
        Mock(item=3860001, player=1),
    ]

    with patch('worlds.kirbyam.client.bizhawk.read', new_callable=AsyncMock) as mock_read, \
         patch('worlds.kirbyam.client.bizhawk.write', new_callable=AsyncMock), \
         patch('CommonClient.logger') as mock_logger:
        mock_read.return_value = [
            (0).to_bytes(4, 'little'),
            (0).to_bytes(4, 'little'),
            (1234).to_bytes(4, 'little'),
        ]

        await client._deliver_items(mock_bizhawk_context)

    matching_disabled = [
        call
        for call in mock_logger.info.call_args_list
        if call.args and isinstance(call.args[0], str) and "Delivering mailbox item index" in call.args[0]
    ]
    assert matching_disabled
    assert all(call.kwargs.get("extra", {}).get("NoStream") is True for call in matching_disabled)

    client = KirbyAmClient()
    client.initialize_client()
    client._debug_logging_enabled = True
    mock_bizhawk_context.items_received = [
        Mock(item=3860001, player=1),
    ]

    with patch('worlds.kirbyam.client.bizhawk.read', new_callable=AsyncMock) as mock_read, \
         patch('worlds.kirbyam.client.bizhawk.write', new_callable=AsyncMock), \
         patch('CommonClient.logger') as mock_logger:
        mock_read.return_value = [
            (0).to_bytes(4, 'little'),
            (0).to_bytes(4, 'little'),
            (1234).to_bytes(4, 'little'),
        ]

        await client._deliver_items(mock_bizhawk_context)

    mock_logger.info.assert_any_call(
        "KirbyAM: Delivering mailbox item index %s (%s from %s)",
        0,
        "1 Up",
        "Player 1",
        extra={"NoStream": False},
    )


@pytest.mark.asyncio
async def test_deliver_items_skips_entry_missing_player_and_continues(mock_bizhawk_context, caplog):
    """Entries missing required fields should be skipped and delivery should continue."""
    client = KirbyAmClient()
    client.initialize_client()

    mock_bizhawk_context.items_received = [
        Mock(item=3860001),
        Mock(item=3860002, player=1),
    ]

    caplog.set_level(logging.WARNING, logger="Client")

    with patch('worlds.kirbyam.client.bizhawk.read', new_callable=AsyncMock) as mock_read, \
         patch('worlds.kirbyam.client.bizhawk.write', new_callable=AsyncMock) as mock_write:
        mock_read.return_value = [
            (0).to_bytes(4, 'little'),
            (0).to_bytes(4, 'little'),
            (777).to_bytes(4, 'little'),
        ]

        await client._deliver_items(mock_bizhawk_context)

    assert client._delivered_item_index == 1
    assert client._delivery_pending is True
    written = mock_write.await_args.args[1]
    assert written[0][1] == int(3860002).to_bytes(4, 'little')
    assert "Skipping malformed ReceivedItems entry" in caplog.text


@pytest.mark.asyncio
async def test_goal_dark_mind_native_signal_reports_client_goal_for_addressless_event(mock_bizhawk_context):
    """Dark Mind goal should send CLIENT_GOAL directly when the goal is an addressless runtime event."""
    from NetUtils import ClientStatus

    client = KirbyAmClient()
    client.initialize_client()

    mock_bizhawk_context.slot_data["goal"] = 0
    mock_bizhawk_context.checked_locations = set()
    mock_bizhawk_context.server_locations = set()
    mock_bizhawk_context.finished_game = False

    with patch.dict(data.native_ram_addresses, {"ai_kirby_state_native": 0x0203AD2C}, clear=False), \
         patch('worlds.kirbyam.client.bizhawk.read', new_callable=AsyncMock) as mock_read:
        mock_read.return_value = [(9999).to_bytes(4, 'little')]

        await client._maybe_report_goal(mock_bizhawk_context)

    mock_bizhawk_context.send_msgs.assert_awaited_once_with([
        {"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}
    ])
    assert mock_bizhawk_context.finished_game is True
    assert client._goal_reported is True


@pytest.mark.asyncio
async def test_goal_dark_mind_server_exposed_goal_reports_location_then_goal_status(mock_bizhawk_context):
    """Dark Mind goal should preserve legacy location-check flow when the server exposes a numeric goal location."""
    from NetUtils import ClientStatus

    client = KirbyAmClient()
    client.initialize_client()

    dark_mind_goal_id = data.locations["GOAL_DARK_MIND"].location_id
    mock_bizhawk_context.slot_data["goal"] = 0
    mock_bizhawk_context.checked_locations = set()
    mock_bizhawk_context.server_locations = {dark_mind_goal_id}

    with patch.dict(data.native_ram_addresses, {"ai_kirby_state_native": 0x0203AD2C}, clear=False), \
         patch('worlds.kirbyam.client.bizhawk.read', new_callable=AsyncMock) as mock_read:
        mock_read.return_value = [(9999).to_bytes(4, 'little')]

        await client._maybe_report_goal(mock_bizhawk_context)

        mock_bizhawk_context.send_msgs.assert_awaited_once_with([
            {"cmd": "LocationChecks", "locations": [dark_mind_goal_id]}
        ])

    mock_bizhawk_context.send_msgs.reset_mock()
    mock_bizhawk_context.checked_locations.add(dark_mind_goal_id)

    with patch.dict(data.native_ram_addresses, {"ai_kirby_state_native": 0x0203AD2C}, clear=False), \
         patch('worlds.kirbyam.client.bizhawk.read', new_callable=AsyncMock) as mock_read:
        mock_read.return_value = [(9999).to_bytes(4, 'little')]

        await client._maybe_report_goal(mock_bizhawk_context)

    mock_bizhawk_context.send_msgs.assert_awaited_once_with([
        {"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}
    ])
    assert mock_bizhawk_context.finished_game is True
    assert client._goal_reported is True


@pytest.mark.asyncio
async def test_goal_dark_mind_falls_back_to_10000_when_9999_was_missed(mock_bizhawk_context):
    """Dark Mind goal mode should accept 10000 as a fallback post-clear goal signal."""
    from NetUtils import ClientStatus

    client = KirbyAmClient()
    client.initialize_client()

    mock_bizhawk_context.slot_data["goal"] = 0
    mock_bizhawk_context.checked_locations = set()
    mock_bizhawk_context.server_locations = set()
    mock_bizhawk_context.finished_game = False

    with patch.dict(data.native_ram_addresses, {"ai_kirby_state_native": 0x0203AD2C}, clear=False), \
         patch('worlds.kirbyam.client.bizhawk.read', new_callable=AsyncMock) as mock_read:
        mock_read.return_value = [(10000).to_bytes(4, 'little')]

        await client._maybe_report_goal(mock_bizhawk_context)

    mock_bizhawk_context.send_msgs.assert_awaited_once_with([
        {"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}
    ])
    assert mock_bizhawk_context.finished_game is True


@pytest.mark.asyncio
async def test_goal_dark_mind_reports_client_goal_after_10000_fallback_ack(mock_bizhawk_context):
    """Dark Mind goal mode should still send CLIENT_GOAL after a 10000 fallback goal check is acknowledged."""
    from NetUtils import ClientStatus

    client = KirbyAmClient()
    client.initialize_client()

    goal_id = data.locations["GOAL_DARK_MIND"].location_id
    mock_bizhawk_context.slot_data["goal"] = 0
    mock_bizhawk_context.checked_locations = {goal_id}
    mock_bizhawk_context.server_locations = {goal_id}

    with patch.dict(data.native_ram_addresses, {"ai_kirby_state_native": 0x0203AD2C}, clear=False), \
         patch('worlds.kirbyam.client.bizhawk.read', new_callable=AsyncMock) as mock_read:
        mock_read.return_value = [(10000).to_bytes(4, 'little')]

        await client._maybe_report_goal(mock_bizhawk_context)

    mock_bizhawk_context.send_msgs.assert_awaited_once_with([
        {"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}
    ])
    assert mock_bizhawk_context.finished_game is True
    assert client._goal_reported is True


@pytest.mark.asyncio
async def test_goal_native_signal_missing_falls_back_to_noop(mock_bizhawk_context):
    """If native goal signal address is unavailable, goal reporting should no-op safely."""
    client = KirbyAmClient()
    client.initialize_client()

    with patch.dict(data.native_ram_addresses, {}, clear=True), \
         patch('worlds.kirbyam.client.bizhawk.read', new_callable=AsyncMock) as mock_read:
        await client._maybe_report_goal(mock_bizhawk_context)

    mock_read.assert_not_awaited()
    mock_bizhawk_context.send_msgs.assert_not_awaited()


@pytest.mark.asyncio
async def test_goal_location_check_sent_once_before_ack(mock_bizhawk_context):
    """Native signal should not spam duplicate goal location checks before server acknowledgement."""
    client = KirbyAmClient()
    client.initialize_client()

    goal_id = data.locations["GOAL_DARK_MIND"].location_id
    mock_bizhawk_context.slot_data["goal"] = 0
    mock_bizhawk_context.server_locations = {goal_id}

    with patch.dict(data.native_ram_addresses, {"ai_kirby_state_native": 0x0203AD2C}, clear=False), \
         patch('worlds.kirbyam.client.bizhawk.read', new_callable=AsyncMock) as mock_read:
        mock_read.return_value = [(9999).to_bytes(4, 'little')]
        await client._maybe_report_goal(mock_bizhawk_context)
        await client._maybe_report_goal(mock_bizhawk_context)

    mock_bizhawk_context.send_msgs.assert_awaited_once_with([
        {"cmd": "LocationChecks", "locations": [goal_id]}
    ])


@pytest.mark.asyncio
async def test_goal_location_uses_locations_checked_for_reconnect_safe_dedup(mock_bizhawk_context):
    """Goal location checks should dedupe via ctx.locations_checked when available."""
    client = KirbyAmClient()
    client.initialize_client()

    goal_id = data.locations["GOAL_DARK_MIND"].location_id
    mock_bizhawk_context.slot_data["goal"] = 0
    mock_bizhawk_context.locations_checked = set()
    mock_bizhawk_context.server_locations = {goal_id}

    with patch.dict(data.native_ram_addresses, {"ai_kirby_state_native": 0x0203AD2C}, clear=False), \
         patch('worlds.kirbyam.client.bizhawk.read', new_callable=AsyncMock) as mock_read:
        mock_read.return_value = [(9999).to_bytes(4, 'little')]

        await client._maybe_report_goal(mock_bizhawk_context)
        await client._maybe_report_goal(mock_bizhawk_context)

    assert goal_id in mock_bizhawk_context.locations_checked
    mock_bizhawk_context.send_msgs.assert_awaited_once_with([
        {"cmd": "LocationChecks", "locations": [goal_id]}
    ])


@pytest.mark.asyncio
async def test_probe_boss_candidates_no_address_no_read(mock_bizhawk_context):
    """Boss probe should no-op when native candidate address is not configured."""
    client = KirbyAmClient()
    client.initialize_client()

    with patch.dict(data.native_ram_addresses, {}, clear=True), \
         patch('worlds.kirbyam.client.bizhawk.read', new_callable=AsyncMock) as mock_read:
        await client._probe_boss_defeat_candidates(mock_bizhawk_context)

        mock_read.assert_not_awaited()


@pytest.mark.asyncio
async def test_goal_reporting_logs_native_signal_seen(mock_bizhawk_context):
    """Info log should fire exactly once when native goal signal is first observed."""
    client = KirbyAmClient()
    client.initialize_client()

    mock_bizhawk_context.slot_data["goal"] = 0
    mock_bizhawk_context.checked_locations = set()
    mock_bizhawk_context.server_locations = set()
    mock_bizhawk_context.finished_game = False

    with patch.dict(data.native_ram_addresses, {"ai_kirby_state_native": 0x0203AD2C}, clear=False), \
         patch('worlds.kirbyam.client.bizhawk.read', new_callable=AsyncMock) as mock_read, \
         patch('CommonClient.logger') as mock_logger:
        mock_read.return_value = [(9999).to_bytes(4, 'little')]
        await client._maybe_report_goal(mock_bizhawk_context)

    signal_calls = [
        c for c in mock_logger.info.call_args_list
        if "native goal signal seen" in c.args[0]
    ]
    assert len(signal_calls) == 1
    assert signal_calls[0].args[1:] == (0,)  # goal_option=0


@pytest.mark.asyncio
async def test_goal_reporting_logs_location_check_sent(mock_bizhawk_context):
    """Info log should fire when goal location check is sent to server."""
    client = KirbyAmClient()
    client.initialize_client()

    goal_id = data.locations["GOAL_DARK_MIND"].location_id
    mock_bizhawk_context.slot_data["goal"] = 0
    mock_bizhawk_context.checked_locations = set()
    mock_bizhawk_context.server_locations = {goal_id}

    with patch.dict(data.native_ram_addresses, {"ai_kirby_state_native": 0x0203AD2C}, clear=False), \
         patch('worlds.kirbyam.client.bizhawk.read', new_callable=AsyncMock) as mock_read, \
         patch('CommonClient.logger') as mock_logger:
        mock_read.return_value = [(9999).to_bytes(4, 'little')]
        await client._maybe_report_goal(mock_bizhawk_context)

    check_calls = [
        c for c in mock_logger.info.call_args_list
        if "sending goal location check" in c.args[0]
    ]
    assert len(check_calls) == 1
    assert check_calls[0].args[1:] == (goal_id,)


@pytest.mark.asyncio
async def test_goal_reporting_logs_client_goal_status(mock_bizhawk_context):
    """Info log should fire when CLIENT_GOAL status is sent."""
    client = KirbyAmClient()
    client.initialize_client()

    goal_id = data.locations["GOAL_DARK_MIND"].location_id
    mock_bizhawk_context.slot_data["goal"] = 0
    mock_bizhawk_context.checked_locations = {goal_id}
    mock_bizhawk_context.server_locations = {goal_id}

    with patch.dict(data.native_ram_addresses, {"ai_kirby_state_native": 0x0203AD2C}, clear=False), \
         patch('worlds.kirbyam.client.bizhawk.read', new_callable=AsyncMock) as mock_read, \
         patch('CommonClient.logger') as mock_logger:
        mock_read.return_value = [(9999).to_bytes(4, 'little')]
        # Prime the native signal so it was "seen" before this call.
        client._native_goal_signal_seen = True
        await client._maybe_report_goal(mock_bizhawk_context)

    complete_calls = [
        c for c in mock_logger.info.call_args_list
        if "goal complete" in c.args[0]
    ]
    assert len(complete_calls) == 1
    assert complete_calls[0].args[1:] == (0,)  # goal_option=0


@pytest.mark.asyncio
async def test_goal_reporting_logs_direct_client_goal_for_addressless_event(mock_bizhawk_context):
    """Info log should explain direct CLIENT_GOAL reporting when the goal is addressless."""
    from NetUtils import ClientStatus

    client = KirbyAmClient()
    client.initialize_client()

    mock_bizhawk_context.slot_data["goal"] = 0
    mock_bizhawk_context.checked_locations = set()
    mock_bizhawk_context.server_locations = set()
    mock_bizhawk_context.finished_game = False

    with patch.dict(data.native_ram_addresses, {"ai_kirby_state_native": 0x0203AD2C}, clear=False), \
         patch('worlds.kirbyam.client.bizhawk.read', new_callable=AsyncMock) as mock_read, \
         patch('CommonClient.logger') as mock_logger:
        mock_read.return_value = [(9999).to_bytes(4, 'little')]
        await client._maybe_report_goal(mock_bizhawk_context)

    mock_bizhawk_context.send_msgs.assert_awaited_once_with([
        {"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}
    ])
    direct_calls = [
        c for c in mock_logger.info.call_args_list
        if "goal location is addressless in this world" in c.args[0]
    ]
    assert len(direct_calls) == 1
    assert direct_calls[0].args[1:] == (0,)


@pytest.mark.asyncio
async def test_goal_reporting_emits_goal_complete_popup(mock_bizhawk_context):
    """CLIENT_GOAL status send should also emit a concise player popup."""
    client = KirbyAmClient()
    client.initialize_client()

    mock_bizhawk_context.slot_data["goal"] = 0
    mock_bizhawk_context.checked_locations = set()

    with patch.dict(data.native_ram_addresses, {"ai_kirby_state_native": 0x0203AD2C}, clear=False), \
         patch('worlds.kirbyam.client.bizhawk.read', new_callable=AsyncMock) as mock_read, \
         patch('worlds.kirbyam.client.bizhawk.display_message', new_callable=AsyncMock) as mock_display:
        mock_read.return_value = [(9999).to_bytes(4, 'little')]

        await client._maybe_report_goal(mock_bizhawk_context)

    mock_display.assert_awaited_once_with(mock_bizhawk_context.bizhawk_ctx, "Goal complete")


@pytest.mark.asyncio
async def test_receive_notification_emits_once_per_delivery_index(mock_bizhawk_context):
    """Receive notification should fire on ACK once per delivered item index."""
    client = KirbyAmClient()
    client.initialize_client()

    mock_bizhawk_context.items_received = [Mock(item=3860001, player=2)]
    mock_bizhawk_context.player_names = {2: "PlayerTwo"}
    mock_bizhawk_context.item_names = Mock()
    mock_bizhawk_context.item_names.lookup_in_slot.return_value = "Mirror Shard"

    client._delivery_pending = True
    client._delivery_pending_item_index = 0
    client._delivered_item_index = 0

    with patch('worlds.kirbyam.client.bizhawk.read', new_callable=AsyncMock) as mock_read, \
         patch('worlds.kirbyam.client.bizhawk.write', new_callable=AsyncMock), \
         patch('worlds.kirbyam.client.bizhawk.display_message', new_callable=AsyncMock) as mock_display:
        mock_read.return_value = [
            (0).to_bytes(4, 'little'),
            (0).to_bytes(4, 'little'),
        ]

        await client._deliver_items(mock_bizhawk_context)

        # Simulate an ACK replay for the same pending index; should dedupe.
        client._delivery_pending = True
        client._delivery_pending_item_index = 0
        client._delivered_item_index = 0
        await client._deliver_items(mock_bizhawk_context)

    mock_display.assert_awaited_once_with(
        mock_bizhawk_context.bizhawk_ctx,
        "Received Mirror Shard from PlayerTwo",
    )


@pytest.mark.asyncio
async def test_receive_notification_honors_slot_data_toggle(mock_bizhawk_context):
    """Receive notifications should be suppressible by slot-data toggle."""
    client = KirbyAmClient()
    client.initialize_client()

    mock_bizhawk_context.slot_data["enable_receive_notifications"] = False
    mock_bizhawk_context.items_received = [Mock(item=3860001, player=2)]
    mock_bizhawk_context.player_names = {2: "PlayerTwo"}
    mock_bizhawk_context.item_names = Mock()
    mock_bizhawk_context.item_names.lookup_in_slot.return_value = "Mirror Shard"

    client._load_notification_settings(mock_bizhawk_context)

    with patch('worlds.kirbyam.client.bizhawk.display_message', new_callable=AsyncMock) as mock_display:
        await client._emit_receive_notification(mock_bizhawk_context, 0)

    mock_display.assert_not_awaited()


@pytest.mark.asyncio
async def test_receive_notification_uses_local_slot_for_item_name_lookup(mock_bizhawk_context):
    """Receive item-name lookup should use the local slot context, not sender slot."""
    client = KirbyAmClient()
    client.initialize_client()

    if not data.items:
        pytest.skip("KirbyAM dataset has no items; skipping receive-notification item-name lookup test.")

    first_item_id = next(iter(data.items.keys()))
    mock_bizhawk_context.slot = 1
    mock_bizhawk_context.items_received = [Mock(item=first_item_id, player=2)]
    mock_bizhawk_context.player_names = {2: "PlayerTwo"}
    mock_bizhawk_context.item_names = Mock()
    mock_bizhawk_context.item_names.lookup_in_slot.return_value = "Mirror Shard"

    with patch('worlds.kirbyam.client.bizhawk.display_message', new_callable=AsyncMock) as mock_display:
        await client._emit_receive_notification(mock_bizhawk_context, 0)

    mock_bizhawk_context.item_names.lookup_in_slot.assert_called_once_with(first_item_id, 1)
    mock_display.assert_awaited_once_with(
        mock_bizhawk_context.bizhawk_ctx,
        "Received Mirror Shard from PlayerTwo",
    )


@pytest.mark.asyncio
async def test_receive_notification_queue_log_gated_by_debug(mock_bizhawk_context):
    client = KirbyAmClient()
    client.initialize_client()

    mock_bizhawk_context.slot = 1
    mock_bizhawk_context.items_received = [Mock(item=3860001, player=2)]
    mock_bizhawk_context.player_names = {2: "PlayerTwo"}
    mock_bizhawk_context.item_names = Mock()
    mock_bizhawk_context.item_names.lookup_in_slot.return_value = "Mirror Shard"

    with patch('worlds.kirbyam.client.bizhawk.display_message', new_callable=AsyncMock), \
         patch('CommonClient.logger') as mock_logger:
        await client._emit_receive_notification(mock_bizhawk_context, 0)

    assert not any(
        call.args and isinstance(call.args[0], str) and "receive notification queued" in call.args[0]
        for call in mock_logger.info.call_args_list
    )

    client = KirbyAmClient()
    client.initialize_client()
    client._debug_logging_enabled = True
    mock_bizhawk_context.items_received = [Mock(item=3860001, player=2)]

    with patch('worlds.kirbyam.client.bizhawk.display_message', new_callable=AsyncMock), \
         patch('CommonClient.logger') as mock_logger:
        await client._emit_receive_notification(mock_bizhawk_context, 0)

    mock_logger.info.assert_any_call(
        "KirbyAM: receive notification queued (index=%s, item=%s, sender=%s, lookup_slot=%s)",
        0,
        "Mirror Shard",
        "PlayerTwo",
        1,
    )


@pytest.mark.asyncio
async def test_receive_notification_not_emitted_for_malformed_skipped_item(mock_bizhawk_context):
    """Malformed ReceivedItems entries should be skipped without receive notification output."""
    client = KirbyAmClient()
    client.initialize_client()

    mock_bizhawk_context.items_received = [Mock(item="bad", player=2)]

    with patch('worlds.kirbyam.client.bizhawk.read', new_callable=AsyncMock) as mock_read, \
         patch('worlds.kirbyam.client.bizhawk.write', new_callable=AsyncMock), \
         patch('worlds.kirbyam.client.bizhawk.display_message', new_callable=AsyncMock) as mock_display:
        mock_read.return_value = [
            (0).to_bytes(4, 'little'),
            (0).to_bytes(4, 'little'),
        ]

        await client._deliver_items(mock_bizhawk_context)

    mock_display.assert_not_awaited()


@pytest.mark.asyncio
async def test_receive_notification_reconnect_replay_dedupes_on_rewind(mock_bizhawk_context):
    """Replayed ACK for an already-notified index should not emit another receive notification."""
    client = KirbyAmClient()
    client.initialize_client()

    mock_bizhawk_context.items_received = [
        Mock(item=3860001, player=2),
        Mock(item=3860002, player=2),
    ]
    mock_bizhawk_context.player_names = {2: "PlayerTwo"}
    mock_bizhawk_context.item_names = Mock()
    mock_bizhawk_context.item_names.lookup_in_slot.return_value = "Mirror Shard"

    client._notified_receive_indices.add(1)
    client._delivery_pending = True
    client._delivery_pending_item_index = 1
    client._delivered_item_index = 1

    with patch('worlds.kirbyam.client.bizhawk.read', new_callable=AsyncMock) as mock_read, \
         patch('worlds.kirbyam.client.bizhawk.write', new_callable=AsyncMock), \
         patch('worlds.kirbyam.client.bizhawk.display_message', new_callable=AsyncMock) as mock_display:
        mock_read.return_value = [
            (0).to_bytes(4, 'little'),
            (1).to_bytes(4, 'little'),
        ]

        await client._deliver_items(mock_bizhawk_context)

    mock_display.assert_not_awaited()


@pytest.mark.asyncio
async def test_receive_notification_not_emitted_on_fast_forward_only(mock_bizhawk_context):
    """Fast-forward cursor reconciliation without ACK should not emit receive notifications."""
    client = KirbyAmClient()
    client.initialize_client()

    client._delivered_item_index = 0
    mock_bizhawk_context.items_received = [
        Mock(item=3860001, player=2),
        Mock(item=3860002, player=2),
    ]

    with patch('worlds.kirbyam.client.bizhawk.read', new_callable=AsyncMock) as mock_read, \
         patch('worlds.kirbyam.client.bizhawk.write', new_callable=AsyncMock), \
         patch('worlds.kirbyam.client.bizhawk.display_message', new_callable=AsyncMock) as mock_display:
        mock_read.return_value = [
            (0).to_bytes(4, 'little'),
            (2).to_bytes(4, 'little'),
        ]

        await client._deliver_items(mock_bizhawk_context)

    mock_display.assert_not_awaited()


@pytest.mark.asyncio
async def test_receive_notification_emits_via_counter_advance_ack(mock_bizhawk_context):
    # Realistic ACK path: ROM clears flag AND advances counter in the same frame.
    # The fast-forward branch runs before the delivery_pending check, so without the
    # fix the notification was silently dropped.  Captures _ff_was_pending before
    # clearing and emits notification when _ff_was_pending and flag == 0.
    client = KirbyAmClient()
    client.initialize_client()

    mock_bizhawk_context.items_received = [Mock(item=3860001, player=2)]
    mock_bizhawk_context.player_names = {2: 'PlayerTwo'}
    mock_bizhawk_context.item_names = Mock()
    mock_bizhawk_context.item_names.lookup_in_slot.return_value = 'Mirror Shard'

    client._delivery_pending = True
    client._delivery_pending_item_index = 0
    client._delivered_item_index = 0

    with patch('worlds.kirbyam.client.bizhawk.read', new_callable=AsyncMock) as mock_read, \
         patch('worlds.kirbyam.client.bizhawk.write', new_callable=AsyncMock), \
         patch('worlds.kirbyam.client.bizhawk.display_message', new_callable=AsyncMock) as mock_display:
        # flag == 0 (cleared by ROM), counter == 1 (incremented by ROM - ACK signal)
        mock_read.return_value = [
            (0).to_bytes(4, 'little'),   # incoming_item_flag = 0
            (1).to_bytes(4, 'little'),   # debug_item_counter = 1
        ]
        await client._deliver_items(mock_bizhawk_context)

    mock_display.assert_awaited_once_with(
        mock_bizhawk_context.bizhawk_ctx,
        'Received Mirror Shard from PlayerTwo',
    )


@pytest.mark.asyncio
async def test_receive_notification_not_emitted_on_fast_forward_stale_flag(mock_bizhawk_context):
    # Abnormal fast-forward: counter advanced but flag is still set (save-state
    # interference).  Client clears the stale flag but must not emit a notification
    # because the normal flag-clear ACK was not observed.
    client = KirbyAmClient()
    client.initialize_client()

    mock_bizhawk_context.items_received = [Mock(item=3860001, player=2)]
    mock_bizhawk_context.player_names = {2: 'PlayerTwo'}
    mock_bizhawk_context.item_names = Mock()
    mock_bizhawk_context.item_names.lookup_in_slot.return_value = 'Mirror Shard'

    client._delivery_pending = True
    client._delivery_pending_item_index = 0
    client._delivered_item_index = 0

    with patch('worlds.kirbyam.client.bizhawk.read', new_callable=AsyncMock) as mock_read, \
         patch('worlds.kirbyam.client.bizhawk.write', new_callable=AsyncMock), \
         patch('worlds.kirbyam.client.bizhawk.display_message', new_callable=AsyncMock) as mock_display:
        # flag = 1 (stale, not cleared), counter = 1 (advanced - abnormal state)
        mock_read.return_value = [
            (1).to_bytes(4, 'little'),   # incoming_item_flag = 1 (stale)
            (1).to_bytes(4, 'little'),   # debug_item_counter = 1
        ]
        await client._deliver_items(mock_bizhawk_context)

    mock_display.assert_not_awaited()


def test_send_notification_dedupes_outgoing_printjson_events(mock_bizhawk_context):
    """Outgoing ItemSend PrintJSON should notify once and dedupe reconnect echoes."""
    client = KirbyAmClient()
    client.initialize_client()

    mock_bizhawk_context.slot = 1
    mock_bizhawk_context.player_names = {2: "PlayerTwo"}
    mock_bizhawk_context.item_names = Mock()
    mock_bizhawk_context.item_names.lookup_in_slot.return_value = "Mirror Shard"

    item_payload = Mock(item=3860001, player=1, location=123)
    printjson_payload = {
        "type": "ItemSend",
        "item": item_payload,
        "receiving": 2,
    }

    with patch('worlds.kirbyam.client.bizhawk.display_message', new_callable=AsyncMock) as mock_display, \
         patch('worlds.kirbyam.client.Utils.async_start') as mock_async_start:
        mock_async_start.side_effect = lambda coro: coro.close()

        client.on_package(mock_bizhawk_context, "PrintJSON", printjson_payload)
        client.on_package(mock_bizhawk_context, "PrintJSON", printjson_payload)

    assert mock_async_start.call_count == 1
    assert mock_display.call_count == 1
    display_args = mock_display.call_args.args
    # Format: "You sent <item> to <receiver> at <location>"
    message = display_args[1]
    assert "You sent" in message and "Mirror Shard" in message and "PlayerTwo" in message and "Location 123" in message, \
        f"Expected message to contain item, receiver, and location: {message}"
    # Ensure ItemSend item-name lookup uses the receiving slot context.
    mock_bizhawk_context.item_names.lookup_in_slot.assert_called_once_with(
        item_payload.item,
        printjson_payload["receiving"],
    )


def test_send_notification_ignores_unrelated_itemsend_traffic(mock_bizhawk_context):
    """ItemSend traffic not sent by local slot should not emit local send notifications."""
    client = KirbyAmClient()
    client.initialize_client()

    mock_bizhawk_context.slot = 1
    mock_bizhawk_context.player_names = {2: "PlayerTwo"}
    mock_bizhawk_context.item_names = Mock()
    mock_bizhawk_context.item_names.lookup_in_slot.return_value = "Mirror Shard"

    unrelated_payload = {
        "type": "ItemSend",
        "item": Mock(item=3860001, player=3, location=123),
        "receiving": 2,
    }

    with patch('worlds.kirbyam.client.bizhawk.display_message', new_callable=AsyncMock) as mock_display, \
         patch('worlds.kirbyam.client.Utils.async_start') as mock_async_start:
        mock_async_start.side_effect = lambda coro: coro.close()
        client.on_package(mock_bizhawk_context, "PrintJSON", unrelated_payload)

    assert mock_async_start.call_count == 0
    assert mock_display.call_count == 0


def test_self_send_printjson_queues_fallback_received_item(mock_bizhawk_context):
    client = KirbyAmClient()
    client.initialize_client()

    mock_bizhawk_context.slot = 1
    mock_bizhawk_context.items_received = []

    payload = {
        "type": "ItemSend",
        "item": Mock(item=3860001, player=1, location=3961000, flags=0),
        "receiving": 1,
    }

    with patch('worlds.kirbyam.client.bizhawk.display_message', new_callable=AsyncMock), \
         patch('worlds.kirbyam.client.Utils.async_start') as mock_async_start:
        mock_async_start.side_effect = lambda coro: coro.close()
        client.on_package(mock_bizhawk_context, "PrintJSON", payload)

    assert len(mock_bizhawk_context.items_received) == 1
    queued = mock_bizhawk_context.items_received[0]
    assert queued.item == 3860001
    assert queued.location == 3961000
    assert queued.player == 1
    assert queued.flags == 0


def test_self_send_printjson_fallback_dedupes_identical_packet(mock_bizhawk_context):
    client = KirbyAmClient()
    client.initialize_client()

    mock_bizhawk_context.slot = 1
    mock_bizhawk_context.items_received = []

    payload = {
        "type": "ItemSend",
        "item": Mock(item=3860001, player=1, location=3961000, flags=0),
        "receiving": 1,
    }

    with patch('worlds.kirbyam.client.bizhawk.display_message', new_callable=AsyncMock), \
         patch('worlds.kirbyam.client.Utils.async_start') as mock_async_start:
        mock_async_start.side_effect = lambda coro: coro.close()
        client.on_package(mock_bizhawk_context, "PrintJSON", payload)
        client.on_package(mock_bizhawk_context, "PrintJSON", payload)

    assert len(mock_bizhawk_context.items_received) == 1


def test_send_notification_rate_limit_suppresses_burst(mock_bizhawk_context):
    """Burst sends should be rate-limited with summary notification when window rolls over."""
    client = KirbyAmClient()
    client.initialize_client()

    mock_bizhawk_context.slot = 1
    mock_bizhawk_context.player_names = {2: "PlayerTwo"}
    mock_bizhawk_context.item_names = Mock()
    mock_bizhawk_context.item_names.lookup_in_slot.return_value = "Mirror Shard"

    with patch('worlds.kirbyam.client.bizhawk.display_message', new_callable=AsyncMock) as mock_display, \
         patch('worlds.kirbyam.client.Utils.async_start') as mock_async_start, \
         patch('worlds.kirbyam.client.time.monotonic') as mock_monotonic:
        mock_async_start.side_effect = lambda coro: coro.close()

        # First 6 sends inside same 2s window: 5 visible + 1 suppressed.
        mock_monotonic.return_value = 100.0
        for idx in range(6):
            payload = {
                "type": "ItemSend",
                "item": Mock(item=3860000 + idx, player=1, location=200 + idx),
                "receiving": 2,
            }
            client.on_package(mock_bizhawk_context, "PrintJSON", payload)

        # Advance time to roll window and flush suppression summary.
        mock_monotonic.return_value = 103.0
        payload = {
            "type": "ItemSend",
            "item": Mock(item=3860999, player=1, location=999),
            "receiving": 2,
        }
        client.on_package(mock_bizhawk_context, "PrintJSON", payload)

    # 5 visible in first window, 1 summary on rollover, 1 visible after rollover.
    assert mock_async_start.call_count == 7


def test_send_notification_queue_log_gated_by_debug(mock_bizhawk_context):
    client = KirbyAmClient()
    client.initialize_client()

    mock_bizhawk_context.slot = 1
    mock_bizhawk_context.player_names = {2: "PlayerTwo"}
    mock_bizhawk_context.item_names = Mock()
    mock_bizhawk_context.item_names.lookup_in_slot.return_value = "Mirror Shard"
    payload = {
        "type": "ItemSend",
        "item": Mock(item=3860001, player=1, location=123),
        "receiving": 2,
    }

    with patch('worlds.kirbyam.client.bizhawk.display_message', new_callable=AsyncMock), \
         patch('worlds.kirbyam.client.Utils.async_start') as mock_async_start, \
         patch('CommonClient.logger') as mock_logger:
        mock_async_start.side_effect = lambda coro: coro.close()
        client.on_package(mock_bizhawk_context, "PrintJSON", payload)

    assert not any(
        call.args and isinstance(call.args[0], str) and "send notification queued" in call.args[0]
        for call in mock_logger.info.call_args_list
    )

    client = KirbyAmClient()
    client.initialize_client()
    client._debug_logging_enabled = True
    with patch('worlds.kirbyam.client.bizhawk.display_message', new_callable=AsyncMock), \
         patch('worlds.kirbyam.client.Utils.async_start') as mock_async_start, \
         patch('CommonClient.logger') as mock_logger:
        mock_async_start.side_effect = lambda coro: coro.close()
        client.on_package(mock_bizhawk_context, "PrintJSON", payload)

    mock_logger.info.assert_any_call(
        "KirbyAM: send notification queued (item=%s, sender=%s, receiver=%s, location=%s)",
        "Mirror Shard",
        "Player 1",
        "PlayerTwo",
        "Location 123",
    )


@pytest.mark.asyncio
async def test_room_sanity_resend_log_gated_by_debug(mock_bizhawk_context):
    client = KirbyAmClient()
    client.initialize_client()
    mock_bizhawk_context.slot_data["room_sanity"] = True
    client._room_sanity_location_ids_by_bit = {0: [3961000]}
    client._room_sanity_bits_sorted = [0]

    raw = bytearray(0x120 * 2)
    raw[0:2] = (0x8000).to_bytes(2, 'little')

    with patch.dict(data.native_ram_addresses, {"room_visit_flags_native": 0x02028CA0}, clear=False), \
         patch('worlds.kirbyam.client.bizhawk.read', new_callable=AsyncMock) as mock_read, \
         patch.object(mock_bizhawk_context, 'send_msgs', new_callable=AsyncMock) as mock_send, \
         patch('CommonClient.logger') as mock_logger:
        mock_read.return_value = [bytes(raw)]

        await client._poll_room_sanity_locations(mock_bizhawk_context)

    mock_send.assert_awaited_once_with([{"cmd": "LocationChecks", "locations": [3961000]}])
    matching_disabled = [
        call
        for call in mock_logger.info.call_args_list
        if call.args and isinstance(call.args[0], str) and "resending room-sanity LocationChecks missing on server" in call.args[0]
    ]
    assert matching_disabled
    assert all(call.kwargs.get("extra", {}).get("NoStream") is True for call in matching_disabled)

    client = KirbyAmClient()
    client.initialize_client()
    client._debug_logging_enabled = True
    mock_bizhawk_context.slot_data["room_sanity"] = True
    client._room_sanity_location_ids_by_bit = {0: [3961000]}
    client._room_sanity_bits_sorted = [0]
    mock_bizhawk_context.checked_locations = set()

    with patch.dict(data.native_ram_addresses, {"room_visit_flags_native": 0x02028CA0}, clear=False), \
         patch('worlds.kirbyam.client.bizhawk.read', new_callable=AsyncMock) as mock_read, \
         patch.object(mock_bizhawk_context, 'send_msgs', new_callable=AsyncMock), \
         patch('CommonClient.logger') as mock_logger:
        mock_read.return_value = [bytes(raw)]

        await client._poll_room_sanity_locations(mock_bizhawk_context)

    matching_enabled = [
        call
        for call in mock_logger.info.call_args_list
        if call.args and isinstance(call.args[0], str) and "resending room-sanity LocationChecks missing on server" in call.args[0]
    ]
    assert matching_enabled
    assert all(call.kwargs.get("extra", {}).get("NoStream") is False for call in matching_enabled)


@pytest.mark.asyncio
async def test_probe_boss_candidates_logs_rising_edges(mock_bizhawk_context):
    """Boss probe should log rising bit transitions for candidate mapping."""
    client = KirbyAmClient()
    client.initialize_client()

    with patch.dict(data.native_ram_addresses, {"boss_mirror_table_native": 0x02028C14}, clear=False), \
         patch('worlds.kirbyam.client.bizhawk.read', new_callable=AsyncMock) as mock_read, \
         patch('CommonClient.logger') as mock_logger:
        # First probe establishes baseline with all zeros.
        mock_read.return_value = [bytes(32)]
        await client._probe_boss_defeat_candidates(mock_bizhawk_context)

        # Second probe sets one bit at first byte (bit 3).
        payload = bytearray(32)
        payload[0] = 0x08
        mock_read.return_value = [bytes(payload)]
        await client._probe_boss_defeat_candidates(mock_bizhawk_context)

        assert mock_logger.debug.called
        logged_args = mock_logger.debug.call_args.args
        assert "KirbyAM: boss candidate probe rising bits" in logged_args[0]
        assert "0x02028C14[bit3]" in logged_args[1]


@pytest.mark.asyncio
async def test_probe_boss_candidates_resets_baseline_on_stream_change(mock_bizhawk_context):
    """Changing BizHawk stream identity should re-baseline probe snapshots."""
    client = KirbyAmClient()
    client.initialize_client()

    first_stream = object()
    second_stream = object()
    mock_bizhawk_context.bizhawk_ctx.streams = first_stream

    with patch.dict(data.native_ram_addresses, {"boss_mirror_table_native": 0x02028C14}, clear=False), \
         patch('worlds.kirbyam.client.bizhawk.read', new_callable=AsyncMock) as mock_read, \
         patch('CommonClient.logger') as mock_logger:
        # Baseline with first stream.
        mock_read.return_value = [bytes(32)]
        await client._probe_boss_defeat_candidates(mock_bizhawk_context)

        # Switch stream identity and present non-zero state; should be treated as new baseline.
        mock_bizhawk_context.bizhawk_ctx.streams = second_stream
        payload = bytearray(32)
        payload[0] = 0x08
        mock_read.return_value = [bytes(payload)]
        await client._probe_boss_defeat_candidates(mock_bizhawk_context)

        mock_logger.info.assert_not_called()


@pytest.mark.asyncio
async def test_probe_unsafe_delivery_candidates_no_addresses_no_read(mock_bizhawk_context):
    """Unsafe-delivery candidate probe should no-op when no optional addresses are configured."""
    client = KirbyAmClient()
    client.initialize_client()

    with patch.dict(data.native_ram_addresses, {}, clear=True), \
         patch('worlds.kirbyam.client.bizhawk.read', new_callable=AsyncMock) as mock_read:
        await client._probe_unsafe_delivery_candidates(mock_bizhawk_context)

    mock_read.assert_not_awaited()


@pytest.mark.asyncio
async def test_probe_unsafe_delivery_candidates_logs_counter_changes(mock_bizhawk_context):
    """Configured unsafe-delivery candidate counters should log when values change."""
    client = KirbyAmClient()
    client.initialize_client()

    with patch.dict(
        data.native_ram_addresses,
        {
            "shadow_kirby_encounters_native": 0x020229D0,
            "mirra_encounters_native": 0x020229D8,
        },
        clear=False,
    ), patch('worlds.kirbyam.client.bizhawk.read', new_callable=AsyncMock) as mock_read, \
         patch('CommonClient.logger') as mock_logger:
        mock_read.return_value = [
            (0).to_bytes(4, 'little'),
            (0).to_bytes(4, 'little'),
        ]
        await client._probe_unsafe_delivery_candidates(mock_bizhawk_context)

        mock_read.return_value = [
            (1).to_bytes(4, 'little'),
            (2).to_bytes(4, 'little'),
        ]
        await client._probe_unsafe_delivery_candidates(mock_bizhawk_context)

    assert mock_logger.debug.call_count == 2
    first_args = mock_logger.debug.call_args_list[0].args
    second_args = mock_logger.debug.call_args_list[1].args
    assert "unsafe-delivery candidate probe" in first_args[0]
    assert first_args[1:] == ("shadow_kirby_encounters", 0, 1)
    assert second_args[1:] == ("mirra_encounters", 0, 2)


@pytest.mark.asyncio
async def test_probe_unsafe_delivery_candidates_rebaseline_on_stream_change(mock_bizhawk_context):
    """Unsafe-delivery candidate probe should re-baseline on BizHawk reconnect."""
    client = KirbyAmClient()
    client.initialize_client()

    first_stream = object()
    second_stream = object()
    mock_bizhawk_context.bizhawk_ctx.streams = first_stream

    with patch.dict(
        data.native_ram_addresses,
        {"shadow_kirby_encounters_native": 0x020229D0},
        clear=False,
    ), patch('worlds.kirbyam.client.bizhawk.read', new_callable=AsyncMock) as mock_read, \
         patch('CommonClient.logger') as mock_logger:
        mock_read.return_value = [(0).to_bytes(4, 'little')]
        await client._probe_unsafe_delivery_candidates(mock_bizhawk_context)

        mock_bizhawk_context.bizhawk_ctx.streams = second_stream
        mock_read.return_value = [(3).to_bytes(4, 'little')]
        await client._probe_unsafe_delivery_candidates(mock_bizhawk_context)

    mock_logger.info.assert_not_called()


def test_load_debug_settings_defaults_to_disabled(mock_bizhawk_context):
    client = KirbyAmClient()
    client.initialize_client()

    client._load_debug_settings(mock_bizhawk_context)

    assert client._debug_logging_enabled is False


def test_load_debug_settings_honors_slot_data_toggle_true(mock_bizhawk_context):
    client = KirbyAmClient()
    client.initialize_client()
    mock_bizhawk_context.slot_data["debug"] = {"logging": True}

    client._load_debug_settings(mock_bizhawk_context)

    assert client._debug_logging_enabled is True


def test_load_debug_settings_ignores_removed_gameplay_state_key(mock_bizhawk_context):
    client = KirbyAmClient()
    client.initialize_client()
    mock_bizhawk_context.slot_data["debug"] = {"gameplay_state_logging": True}

    client._load_debug_settings(mock_bizhawk_context)

    assert client._debug_logging_enabled is False


def test_no_extra_lives_enabled_defaults_to_false(mock_bizhawk_context):
    client = KirbyAmClient()
    client.initialize_client()

    assert client._no_extra_lives_enabled(mock_bizhawk_context) is False


def test_no_extra_lives_enabled_honors_slot_data_toggle(mock_bizhawk_context):
    client = KirbyAmClient()
    client.initialize_client()
    mock_bizhawk_context.slot_data["no_extra_lives"] = True

    assert client._no_extra_lives_enabled(mock_bizhawk_context) is True


@pytest.mark.asyncio
async def test_enforce_no_extra_lives_writes_zero_to_life_counter(mock_bizhawk_context):
    client = KirbyAmClient()
    client.initialize_client()
    mock_bizhawk_context.slot_data["no_extra_lives"] = True

    with patch.dict(data.native_ram_addresses, {"kirby_lives_native": 0x02020FE2}, clear=False), \
         patch('worlds.kirbyam.client.bizhawk.read', new_callable=AsyncMock) as mock_read, \
         patch('worlds.kirbyam.client.bizhawk.write', new_callable=AsyncMock) as mock_write:
        mock_read.return_value = [(2).to_bytes(1, 'little')]

        await client._enforce_no_extra_lives(mock_bizhawk_context)

    mock_write.assert_awaited_once_with(
        mock_bizhawk_context.bizhawk_ctx,
        [(0x02020FE2, (0).to_bytes(1, 'little'), 'System Bus')]
    )


@pytest.mark.asyncio
async def test_enforce_no_extra_lives_skips_write_when_already_zero(mock_bizhawk_context):
    client = KirbyAmClient()
    client.initialize_client()
    mock_bizhawk_context.slot_data["no_extra_lives"] = True

    with patch.dict(data.native_ram_addresses, {"kirby_lives_native": 0x02020FE2}, clear=False), \
         patch('worlds.kirbyam.client.bizhawk.read', new_callable=AsyncMock) as mock_read, \
         patch('worlds.kirbyam.client.bizhawk.write', new_callable=AsyncMock) as mock_write:
        mock_read.return_value = [(0).to_bytes(1, 'little')]

        await client._enforce_no_extra_lives(mock_bizhawk_context)

    mock_write.assert_not_awaited()


@pytest.mark.asyncio
async def test_enforce_no_extra_lives_logs_only_when_debug_enabled(mock_bizhawk_context):
    client = KirbyAmClient()
    client.initialize_client()
    client._debug_logging_enabled = True
    mock_bizhawk_context.slot_data["no_extra_lives"] = True

    with patch.dict(data.native_ram_addresses, {"kirby_lives_native": 0x02020FE2}, clear=False), \
         patch('worlds.kirbyam.client.bizhawk.read', new_callable=AsyncMock) as mock_read, \
         patch('worlds.kirbyam.client.bizhawk.write', new_callable=AsyncMock) as mock_write, \
         patch('CommonClient.logger') as mock_logger:
        mock_read.return_value = [(1).to_bytes(1, 'little')]

        await client._enforce_no_extra_lives(mock_bizhawk_context)

    mock_write.assert_awaited_once()
    mock_logger.info.assert_any_call(
        "KirbyAM debug: no-extra-lives clamped native lives from %s to 0",
        1,
    )


@pytest.mark.asyncio
async def test_enforce_one_hit_mode_clamps_max_hp_and_current_hp(mock_bizhawk_context):
    client = KirbyAmClient()
    client.initialize_client()
    mock_bizhawk_context.slot_data["one_hit_mode"] = OneHitMode.option_exclude_vitality_counters

    with patch.dict(
        data.native_ram_addresses,
        {
            "kirby_vitality_counter_native": 0x02038980,
            "kirby_hp_native": 0x02020FE0,
            "kirby_max_hp_native": 0x02020FE1,
        },
        clear=False,
    ), patch('worlds.kirbyam.client.bizhawk.read', new_callable=AsyncMock) as mock_read, \
         patch('worlds.kirbyam.client.bizhawk.write', new_callable=AsyncMock) as mock_write:
        mock_read.return_value = [
            (0).to_bytes(2, 'little'),
            (4).to_bytes(1, 'little', signed=True),
            (6).to_bytes(1, 'little', signed=True),
        ]

        await client._enforce_one_hit_mode(mock_bizhawk_context)

    mock_write.assert_awaited_once_with(
        mock_bizhawk_context.bizhawk_ctx,
        [
            (0x02020FE1, bytes([1]), 'System Bus'),
            (0x02020FE0, bytes([1]), 'System Bus'),
        ],
    )


@pytest.mark.asyncio
async def test_enforce_one_hit_mode_exclude_scrubs_native_vitality_counter(mock_bizhawk_context):
    client = KirbyAmClient()
    client.initialize_client()
    mock_bizhawk_context.slot_data["one_hit_mode"] = OneHitMode.option_exclude_vitality_counters

    with patch.dict(
        data.native_ram_addresses,
        {
            "kirby_vitality_counter_native": 0x02038980,
            "kirby_hp_native": 0x02020FE0,
            "kirby_max_hp_native": 0x02020FE1,
        },
        clear=False,
    ), patch('worlds.kirbyam.client.bizhawk.read', new_callable=AsyncMock) as mock_read, \
         patch('worlds.kirbyam.client.bizhawk.write', new_callable=AsyncMock) as mock_write:
        mock_read.return_value = [
            (3).to_bytes(2, 'little'),
            (1).to_bytes(1, 'little', signed=True),
            (1).to_bytes(1, 'little', signed=True),
        ]

        await client._enforce_one_hit_mode(mock_bizhawk_context)

    mock_write.assert_awaited_once_with(
        mock_bizhawk_context.bizhawk_ctx,
        [
            (0x02038980, (0).to_bytes(2, 'little'), 'System Bus'),
        ],
    )


@pytest.mark.asyncio
async def test_enforce_one_hit_mode_preserves_dead_hp_state(mock_bizhawk_context):
    client = KirbyAmClient()
    client.initialize_client()
    mock_bizhawk_context.slot_data["one_hit_mode"] = OneHitMode.option_include_vitality_counters

    with patch.dict(
        data.native_ram_addresses,
        {
            "kirby_vitality_counter_native": 0x02038980,
            "kirby_hp_native": 0x02020FE0,
            "kirby_max_hp_native": 0x02020FE1,
        },
        clear=False,
    ), patch('worlds.kirbyam.client.bizhawk.read', new_callable=AsyncMock) as mock_read, \
         patch('worlds.kirbyam.client.bizhawk.write', new_callable=AsyncMock) as mock_write:
        mock_read.return_value = [
            (1).to_bytes(2, 'little'),
            (-1).to_bytes(1, 'little', signed=True),
            (6).to_bytes(1, 'little', signed=True),
        ]

        await client._enforce_one_hit_mode(mock_bizhawk_context)

    mock_write.assert_awaited_once_with(
        mock_bizhawk_context.bizhawk_ctx,
        [
            (0x02020FE1, bytes([2]), 'System Bus'),
        ],
    )


@pytest.mark.asyncio
async def test_enforce_one_hit_mode_skips_writes_when_already_within_cap(mock_bizhawk_context):
    client = KirbyAmClient()
    client.initialize_client()
    mock_bizhawk_context.slot_data["one_hit_mode"] = OneHitMode.option_include_vitality_counters

    with patch.dict(
        data.native_ram_addresses,
        {
            "kirby_vitality_counter_native": 0x02038980,
            "kirby_hp_native": 0x02020FE0,
            "kirby_max_hp_native": 0x02020FE1,
        },
        clear=False,
    ), patch('worlds.kirbyam.client.bizhawk.read', new_callable=AsyncMock) as mock_read, \
         patch('worlds.kirbyam.client.bizhawk.write', new_callable=AsyncMock) as mock_write:
        mock_read.return_value = [
            (2).to_bytes(2, 'little'),
            (2).to_bytes(1, 'little', signed=True),
            (3).to_bytes(1, 'little', signed=True),
        ]

        await client._enforce_one_hit_mode(mock_bizhawk_context)

    mock_write.assert_not_awaited()


@pytest.mark.asyncio
async def test_runtime_gameplay_state_logs_ai_and_demo_changes_with_heartbeat(mock_bizhawk_context):
    client = KirbyAmClient()
    client.initialize_client()
    mock_bizhawk_context.slot_data["debug"] = {"logging": True}
    client._load_debug_settings(mock_bizhawk_context)

    with patch.dict(
        data.native_ram_addresses,
        {
            "ai_kirby_state_native": 0x0203AD2C,
            "demo_playback_flags_native": 0x0203AD10,
        },
        clear=False,
    ), patch.dict(
        data.transport_ram_addresses,
        {"hook_heartbeat": 0x0203B034},
        clear=False,
    ), patch('worlds.kirbyam.client.bizhawk.read', new_callable=AsyncMock) as mock_read, \
         patch('CommonClient.logger') as mock_logger:
        mock_read.side_effect = [
            [
                (100).to_bytes(4, 'little'),
                (0).to_bytes(4, 'little'),
                (7).to_bytes(4, 'little'),
            ],
            [
                (300).to_bytes(4, 'little'),
                (0).to_bytes(4, 'little'),
                (8).to_bytes(4, 'little'),
            ],
            [
                (300).to_bytes(4, 'little'),
                (0x10).to_bytes(4, 'little'),
                (9).to_bytes(4, 'little'),
            ],
        ]

        await client._runtime_gameplay_state(mock_bizhawk_context)
        await client._runtime_gameplay_state(mock_bizhawk_context)
        await client._runtime_gameplay_state(mock_bizhawk_context)

    ai_logs = [
        c for c in mock_logger.info.call_args_list
        if c.args and isinstance(c.args[0], str) and "ai_kirby_state_native changed" in c.args[0]
    ]
    demo_logs = [
        c for c in mock_logger.info.call_args_list
        if c.args and isinstance(c.args[0], str) and "demo_playback_flags_native changed" in c.args[0]
    ]

    assert len(ai_logs) == 2
    assert len(demo_logs) == 2

    assert ai_logs[0].args[1] == 100
    assert ai_logs[0].args[4] == 7
    assert ai_logs[1].args[1] == 300
    assert ai_logs[1].args[4] == 8

    assert demo_logs[0].args[1] == 0
    assert demo_logs[0].args[3] == 7
    assert demo_logs[1].args[1] == 0x10
    assert demo_logs[1].args[3] == 9


@pytest.mark.asyncio
async def test_log_boss_shard_debug_window_emits_per_frame_while_active(mock_bizhawk_context):
    client = KirbyAmClient()
    client.initialize_client()
    client._debug_logging_enabled = True

    with patch.dict(
        data.transport_ram_addresses,
        {
            "boss_defeat_flags": 0x0203B024,
            "shard_scrub_delay_frames": 0x0203B03C,
            "delivered_shard_bitfield": 0x0203B038,
            "shard_bitfield": 0x0203B000,
            "hook_heartbeat": 0x0203B034,
            "boss_temp_shard_bitfield": 0x0203B044,
        },
        clear=False,
    ), patch.dict(
        data.native_ram_addresses,
        {"shard_bitfield_native": 0x02038970},
        clear=False,
    ), patch('worlds.kirbyam.client.bizhawk.read', new_callable=AsyncMock) as mock_read, \
         patch('CommonClient.logger') as mock_logger:
        mock_read.side_effect = [
            [
                (5).to_bytes(4, 'little'),
                (0x02).to_bytes(4, 'little'),
            ],
            [
                (1).to_bytes(4, 'little'),
                (0).to_bytes(4, 'little'),
                (0x02).to_bytes(4, 'little'),
                (100).to_bytes(4, 'little'),
                (0x02).to_bytes(1, 'little'),
            ],
            [
                (4).to_bytes(4, 'little'),
                (0x02).to_bytes(4, 'little'),
            ],
            [
                (1).to_bytes(4, 'little'),
                (0).to_bytes(4, 'little'),
                (0x02).to_bytes(4, 'little'),
                (101).to_bytes(4, 'little'),
                (0x02).to_bytes(1, 'little'),
            ],
        ]

        await client._log_boss_shard_debug_window(
            mock_bizhawk_context,
            gameplay_active=False,
            defer_reason="non_gameplay_cutscene",
            ai_state=200,
        )
        await client._log_boss_shard_debug_window(
            mock_bizhawk_context,
            gameplay_active=False,
            defer_reason="non_gameplay_cutscene",
            ai_state=200,
        )

    frame_logs = [
        c for c in mock_logger.info.call_args_list
        if c.args and isinstance(c.args[0], str) and "boss-shard window frame" in c.args[0]
    ]
    assert len(frame_logs) == 2


@pytest.mark.asyncio
async def test_log_boss_shard_debug_window_logs_completion_on_resume(mock_bizhawk_context):
    client = KirbyAmClient()
    client.initialize_client()
    client._debug_logging_enabled = True

    with patch.dict(
        data.transport_ram_addresses,
        {
            "boss_defeat_flags": 0x0203B024,
            "shard_scrub_delay_frames": 0x0203B03C,
            "delivered_shard_bitfield": 0x0203B038,
            "shard_bitfield": 0x0203B000,
            "hook_heartbeat": 0x0203B034,
            "boss_temp_shard_bitfield": 0x0203B044,
        },
        clear=False,
    ), patch.dict(
        data.native_ram_addresses,
        {"shard_bitfield_native": 0x02038970},
        clear=False,
    ), patch('worlds.kirbyam.client.bizhawk.read', new_callable=AsyncMock) as mock_read, \
         patch('CommonClient.logger') as mock_logger:
        mock_read.side_effect = [
            [
                (1).to_bytes(4, 'little'),
                (0x02).to_bytes(4, 'little'),
            ],
            [
                (1).to_bytes(4, 'little'),
                (0).to_bytes(4, 'little'),
                (0x02).to_bytes(4, 'little'),
                (200).to_bytes(4, 'little'),
                (0x02).to_bytes(1, 'little'),
            ],
            [
                (0).to_bytes(4, 'little'),
                (0x00).to_bytes(4, 'little'),
            ],
            [
                (1).to_bytes(4, 'little'),
                (0).to_bytes(4, 'little'),
                (0x00).to_bytes(4, 'little'),
                (201).to_bytes(4, 'little'),
                (0x00).to_bytes(1, 'little'),
            ],
        ]

        await client._log_boss_shard_debug_window(
            mock_bizhawk_context,
            gameplay_active=False,
            defer_reason="non_gameplay_cutscene",
            ai_state=200,
        )
        await client._log_boss_shard_debug_window(
            mock_bizhawk_context,
            gameplay_active=True,
            defer_reason="gameplay_active",
            ai_state=300,
        )

    completion_logs = [
        c for c in mock_logger.info.call_args_list
        if c.args and isinstance(c.args[0], str) and "boss-shard window complete" in c.args[0]
    ]
    assert len(completion_logs) == 1


@pytest.mark.asyncio
async def test_game_watcher_skips_when_server_is_none(mock_bizhawk_context):
    """game_watcher should do nothing when ctx.server is None (AP not connected)."""
    client = KirbyAmClient()
    client.initialize_client()
    mock_bizhawk_context.server = None

    with patch('worlds.kirbyam.client.bizhawk.read', new_callable=AsyncMock) as mock_read:
        await client.game_watcher(mock_bizhawk_context)
        mock_read.assert_not_awaited()


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("raised_exception", "expected_log_call", "expected_log_kwargs"),
    [
        (
            bizhawk.RequestFailedError("Connection timed out"),
            (
                "KirbyAM: BizHawk request failed during watcher tick; waiting for reconnect (%s)",
                "Connection timed out",
            ),
            {"extra": {"NoStream": True}},
        ),
        (
            bizhawk.NotConnectedError(),
            ("KirbyAM: BizHawk disconnected during watcher tick; waiting for reconnect",),
            {"extra": {"NoStream": True}},
        ),
    ],
)
async def test_game_watcher_recovers_locally_from_transport_errors(
    mock_bizhawk_context,
    raised_exception,
    expected_log_call,
    expected_log_kwargs,
):
    """KirbyAM's shipped handler should absorb transient BizHawk disconnects without crashing the watcher."""
    client = KirbyAmClient()
    client.initialize_client()
    client._watcher_server_ready = True
    client._ram_state_loaded = True
    client._delivery_pending = True
    client._delivery_pending_frame = 17
    client._delivery_pending_item_index = 3

    with patch('CommonClient.logger') as mock_logger, \
         patch.object(client, '_sync_death_link_setting', new_callable=AsyncMock), \
         patch.object(client, '_runtime_gameplay_state', new_callable=AsyncMock) as mock_gate:
        mock_gate.side_effect = raised_exception

        await client.game_watcher(mock_bizhawk_context)

    assert client._watcher_requires_bizhawk_resync is True
    assert client._ram_state_loaded is False
    assert client._delivery_pending is False
    assert client._delivery_pending_frame is None
    assert client._delivery_pending_item_index is None
    mock_logger.info.assert_any_call(*expected_log_call, **expected_log_kwargs)


@pytest.mark.asyncio
async def test_game_watcher_reloads_state_after_transport_recovery(mock_bizhawk_context):
    """After a transport error, the next successful tick should reload RAM-backed state and clear recovery flags."""
    client = KirbyAmClient()
    client.initialize_client()
    client._watcher_server_ready = True
    client._watcher_requires_bizhawk_resync = True
    client._last_watcher_transport_error = "Connection timed out"

    with patch.object(client, '_reset_reconnect_transient_state') as mock_reset, \
         patch.object(client, '_load_persistent_state', new_callable=AsyncMock) as mock_load, \
         patch.object(client, '_reconcile_native_map_ownership', new_callable=AsyncMock) as mock_reconcile_maps, \
         patch.object(client, '_runtime_gameplay_state', new_callable=AsyncMock) as mock_gate, \
         patch.object(client, '_apply_pending_death_link', new_callable=AsyncMock) as mock_apply_death_link, \
         patch.object(client, '_poll_and_send_local_death_link', new_callable=AsyncMock) as mock_send_death_link, \
         patch.object(client, '_poll_boss_defeat_locations', new_callable=AsyncMock) as mock_poll_boss, \
         patch.object(client, '_poll_major_chest_locations', new_callable=AsyncMock) as mock_poll_major, \
         patch.object(client, '_poll_minor_chest_locations', new_callable=AsyncMock) as mock_poll_minor, \
         patch.object(client, '_poll_vitality_chest_locations', new_callable=AsyncMock) as mock_poll_vitality, \
         patch.object(client, '_poll_sound_player_chest_locations', new_callable=AsyncMock) as mock_poll_sound_player, \
         patch.object(client, '_poll_hub_switch_locations', new_callable=AsyncMock) as mock_poll_hub_switch, \
         patch.object(client, '_probe_boss_defeat_candidates', new_callable=AsyncMock) as mock_probe_boss, \
         patch.object(client, '_probe_unsafe_delivery_candidates', new_callable=AsyncMock) as mock_probe_unsafe, \
         patch.object(client, '_deliver_items', new_callable=AsyncMock) as mock_deliver, \
         patch.object(client, '_maybe_report_goal', new_callable=AsyncMock) as mock_goal:
        mock_gate.return_value = (True, "gameplay_active", 300)

        await client.game_watcher(mock_bizhawk_context)

    mock_reset.assert_called_once_with()
    mock_load.assert_awaited_once_with(mock_bizhawk_context)
    mock_reconcile_maps.assert_awaited_once_with(mock_bizhawk_context)
    mock_apply_death_link.assert_awaited_once_with(mock_bizhawk_context)
    mock_send_death_link.assert_awaited_once_with(mock_bizhawk_context)
    mock_poll_boss.assert_awaited_once_with(mock_bizhawk_context)
    mock_poll_major.assert_awaited_once_with(mock_bizhawk_context)
    mock_poll_minor.assert_awaited_once_with(mock_bizhawk_context)
    mock_poll_vitality.assert_awaited_once_with(mock_bizhawk_context)
    mock_poll_sound_player.assert_awaited_once_with(mock_bizhawk_context)
    mock_poll_hub_switch.assert_awaited_once_with(mock_bizhawk_context)
    mock_probe_boss.assert_awaited_once_with(mock_bizhawk_context)
    mock_probe_unsafe.assert_awaited_once_with(mock_bizhawk_context)
    mock_deliver.assert_awaited_once_with(mock_bizhawk_context)
    mock_goal.assert_awaited_once_with(mock_bizhawk_context, ai_state_override=300)
    assert client._watcher_requires_bizhawk_resync is False
    assert client._ram_state_loaded is True
    assert client._last_watcher_transport_error is None


@pytest.mark.asyncio
async def test_global_game_watcher_recovers_when_handler_tick_times_out():
    """A RequestFailedError in handler game_watcher should not crash the global watcher loop."""
    ctx = Mock()
    ctx.watcher_timeout = 0.01
    ctx.watcher_event = asyncio.Event()
    ctx.watcher_event.set()
    ctx.exit_event = asyncio.Event()
    ctx.bizhawk_ctx = Mock()
    ctx.bizhawk_ctx.connection_status = bizhawk.ConnectionStatus.CONNECTED
    ctx.client_handler = Mock()
    ctx.server = None
    ctx.auth_status = AuthStatus.NOT_AUTHENTICATED
    ctx.rom_hash = "test_rom_hash"

    async def raise_timeout(*_args, **_kwargs):
        ctx.exit_event.set()
        raise bizhawk.RequestFailedError("Connection timed out")

    ctx.client_handler.game_watcher = AsyncMock(side_effect=raise_timeout)

    with patch('worlds._bizhawk.context.ping', new_callable=AsyncMock) as mock_ping, \
         patch('worlds._bizhawk.context.get_hash', new_callable=AsyncMock) as mock_get_hash, \
         patch('worlds._bizhawk.context.logger') as mock_logger:
        mock_get_hash.return_value = "test_rom_hash"

        await asyncio.wait_for(_game_watcher(ctx), timeout=0.2)

    mock_ping.assert_awaited_once_with(ctx.bizhawk_ctx)
    ctx.client_handler.game_watcher.assert_awaited_once_with(ctx)
    mock_logger.info.assert_any_call("Lost connection to BizHawk: Connection timed out")


@pytest.mark.asyncio
async def test_game_watcher_skips_when_slot_data_is_none(mock_bizhawk_context):
    """game_watcher should do nothing when ctx.slot_data is None (handshake not complete)."""
    client = KirbyAmClient()
    client.initialize_client()
    mock_bizhawk_context.slot_data = None

    with patch('worlds.kirbyam.client.bizhawk.read', new_callable=AsyncMock) as mock_read:
        await client.game_watcher(mock_bizhawk_context)
        mock_read.assert_not_awaited()


@pytest.mark.asyncio
async def test_game_watcher_skips_when_server_socket_is_missing(mock_bizhawk_context):
    """game_watcher should do nothing when ctx.server.socket is temporarily unavailable."""
    client = KirbyAmClient()
    client.initialize_client()
    mock_bizhawk_context.server.socket = None

    with patch('worlds.kirbyam.client.bizhawk.read', new_callable=AsyncMock) as mock_read:
        await client.game_watcher(mock_bizhawk_context)
        mock_read.assert_not_awaited()


@pytest.mark.asyncio
async def test_game_watcher_skips_when_server_socket_is_closed(mock_bizhawk_context):
    """game_watcher should do nothing when AP socket is closed."""
    client = KirbyAmClient()
    client.initialize_client()
    mock_bizhawk_context.server.socket.closed = True

    with patch('worlds.kirbyam.client.bizhawk.read', new_callable=AsyncMock) as mock_read:
        await client.game_watcher(mock_bizhawk_context)
        mock_read.assert_not_awaited()



@pytest.mark.asyncio
async def test_game_watcher_reconnect_entry_resets_transient_state_once(mock_bizhawk_context):
    """First watcher tick after AP session readiness should reset transient reconnect state and log once."""
    client = KirbyAmClient()
    client.initialize_client()
    mock_bizhawk_context.slot_data["debug"] = {"logging": True}

    client._last_runtime_gate_reason = "non_gameplay_cutscene"
    client._last_shard_poll_log = ("resend", (1,), ())
    client._last_boss_poll_log = ("resend", (2,), ())
    client._last_major_chest_poll_log = ("resend", (3,), ())
    client._last_vitality_chest_poll_log = ("resend", (4,), ())
    client._last_sound_player_chest_poll_log = ("resend", (5,), ())
    client._last_hub_switch_poll_log = ("resend", (6,), ())
    client._hub_switch_baseline_mask = 0x00000400
    client._hub_switch_session_initialized = True
    hub_stream_marker = object()
    client._hub_switch_stream_marker = hub_stream_marker
    client._last_boss_probe_snapshot = bytes(32)
    client._boss_probe_stream_marker = object()
    client._unsafe_delivery_probe_stream_marker = object()
    client._last_unsafe_delivery_counter_values = {"shadow_kirby_encounters": 2}

    with patch('CommonClient.logger') as mock_logger, \
         patch.object(client, '_runtime_gameplay_state', new_callable=AsyncMock) as mock_gate, \
         patch.object(client, '_load_persistent_state', new_callable=AsyncMock) as mock_load, \
         patch.object(client, '_reconcile_native_map_ownership', new_callable=AsyncMock) as mock_reconcile_maps, \
            patch.object(client, '_log_boss_shard_debug_window', new_callable=AsyncMock), \
         patch.object(client, '_poll_locations', new_callable=AsyncMock) as mock_poll_locations, \
         patch.object(client, '_poll_boss_defeat_locations', new_callable=AsyncMock) as mock_poll_boss, \
            patch.object(client, '_poll_major_chest_locations', new_callable=AsyncMock) as mock_poll_major_chests, \
                patch.object(client, '_poll_minor_chest_locations', new_callable=AsyncMock) as mock_poll_minor_chests, \
            patch.object(client, '_poll_vitality_chest_locations', new_callable=AsyncMock) as mock_poll_vitality_chests, \
            patch.object(client, '_poll_sound_player_chest_locations', new_callable=AsyncMock) as mock_poll_sound_player_chests, \
                patch.object(client, '_poll_hub_switch_locations', new_callable=AsyncMock) as mock_poll_hub_switches, \
         patch.object(client, '_probe_boss_defeat_candidates', new_callable=AsyncMock) as mock_probe, \
         patch.object(client, '_probe_unsafe_delivery_candidates', new_callable=AsyncMock) as mock_probe_unsafe, \
         patch.object(client, '_deliver_items', new_callable=AsyncMock) as mock_deliver, \
         patch.object(client, '_maybe_report_goal', new_callable=AsyncMock) as mock_goal:
        mock_gate.return_value = (True, "gameplay_active", 300)

        await client.game_watcher(mock_bizhawk_context)

        assert client._watcher_server_ready is True
        assert client._last_runtime_gate_reason is None
        assert client._last_shard_poll_log is None
        assert client._last_boss_poll_log is None
        assert client._last_major_chest_poll_log is None
        assert client._last_vitality_chest_poll_log is None
        assert client._last_sound_player_chest_poll_log is None
        assert client._last_hub_switch_poll_log is None
        assert client._hub_switch_baseline_mask == 0x00000400
        assert client._hub_switch_session_initialized is True
        assert client._hub_switch_stream_marker is hub_stream_marker
        assert client._last_boss_probe_snapshot is None
        assert client._boss_probe_stream_marker is None
        assert client._unsafe_delivery_probe_stream_marker is None
        assert client._last_unsafe_delivery_counter_values == {}
        mock_logger.info.assert_any_call("KirbyAM: AP session ready; reconnect-safe reconciliation active")
        mock_load.assert_awaited_once()
        mock_reconcile_maps.assert_awaited()
        mock_poll_locations.assert_not_awaited()
        mock_poll_boss.assert_awaited_once()
        mock_poll_major_chests.assert_awaited_once()
        mock_poll_minor_chests.assert_awaited_once()
        mock_poll_vitality_chests.assert_awaited_once()
        mock_poll_sound_player_chests.assert_awaited_once()
        mock_poll_hub_switches.assert_awaited_once()
        mock_probe.assert_awaited_once()
        mock_probe_unsafe.assert_awaited_once()
        mock_deliver.assert_awaited_once_with(mock_bizhawk_context)
        mock_goal.assert_awaited_once_with(mock_bizhawk_context, ai_state_override=300)

        mock_logger.info.reset_mock()
        await client.game_watcher(mock_bizhawk_context)
        assert not mock_logger.info.called


@pytest.mark.asyncio
async def test_game_watcher_reconnect_entry_suppresses_session_ready_log_when_debug_disabled(mock_bizhawk_context):
    client = KirbyAmClient()
    client.initialize_client()

    with patch('CommonClient.logger') as mock_logger, \
         patch.object(client, '_runtime_gameplay_state', new_callable=AsyncMock) as mock_gate, \
         patch.object(client, '_load_persistent_state', new_callable=AsyncMock), \
         patch.object(client, '_reconcile_native_map_ownership', new_callable=AsyncMock), \
         patch.object(client, '_log_boss_shard_debug_window', new_callable=AsyncMock), \
         patch.object(client, '_apply_pending_death_link', new_callable=AsyncMock), \
         patch.object(client, '_poll_and_send_local_death_link', new_callable=AsyncMock), \
         patch.object(client, '_poll_boss_defeat_locations', new_callable=AsyncMock), \
         patch.object(client, '_poll_major_chest_locations', new_callable=AsyncMock), \
         patch.object(client, '_poll_minor_chest_locations', new_callable=AsyncMock), \
         patch.object(client, '_poll_vitality_chest_locations', new_callable=AsyncMock), \
         patch.object(client, '_poll_sound_player_chest_locations', new_callable=AsyncMock), \
         patch.object(client, '_poll_hub_switch_locations', new_callable=AsyncMock), \
         patch.object(client, '_poll_room_sanity_locations', new_callable=AsyncMock), \
         patch.object(client, '_probe_boss_defeat_candidates', new_callable=AsyncMock), \
         patch.object(client, '_probe_unsafe_delivery_candidates', new_callable=AsyncMock), \
         patch.object(client, '_deliver_items', new_callable=AsyncMock), \
         patch.object(client, '_maybe_report_goal', new_callable=AsyncMock):
        mock_gate.return_value = (True, "gameplay_active", 300)

        await client.game_watcher(mock_bizhawk_context)

    assert not any(
        call.args and call.args[0] == "KirbyAM: AP session ready; reconnect-safe reconciliation active"
        for call in mock_logger.info.call_args_list
    )


@pytest.mark.asyncio
async def test_runtime_gameplay_state_active_on_normal_state(mock_bizhawk_context):
    """AI state 300 should be treated as gameplay-active."""
    client = KirbyAmClient()
    client.initialize_client()

    with patch.dict(data.native_ram_addresses, {"ai_kirby_state_native": 0x0203AD2C}, clear=False), \
         patch('worlds.kirbyam.client.bizhawk.read', new_callable=AsyncMock) as mock_read:
        mock_read.return_value = [
            (300).to_bytes(4, 'little'),
            (0).to_bytes(4, 'little'),
        ]

        active, reason, ai_state = await client._runtime_gameplay_state(mock_bizhawk_context)

    assert active is True
    assert reason == "gameplay_active"
    assert ai_state == 300


@pytest.mark.asyncio
async def test_runtime_gameplay_state_non_gameplay_on_title_demo_state(mock_bizhawk_context):
    """AI state 300 should defer polling when the title-demo playback flag is active."""
    client = KirbyAmClient()
    client.initialize_client()

    with patch.dict(data.native_ram_addresses, {"ai_kirby_state_native": 0x0203AD2C}, clear=False), \
         patch('worlds.kirbyam.client.bizhawk.read', new_callable=AsyncMock) as mock_read:
        mock_read.return_value = [
            (300).to_bytes(4, 'little'),
            (0x10).to_bytes(4, 'little'),
        ]

        active, reason, ai_state = await client._runtime_gameplay_state(mock_bizhawk_context)

    assert active is False
    assert reason == "non_gameplay_title_demo"
    assert ai_state == 300


@pytest.mark.asyncio
async def test_runtime_gameplay_state_fail_open_when_demo_signal_unavailable(mock_bizhawk_context):
    """Missing demo_playback_flags_native should fail open for state 300."""
    client = KirbyAmClient()
    client.initialize_client()

    with patch.dict(
        data.native_ram_addresses,
        {
            "ai_kirby_state_native": 0x0203AD2C,
            "demo_playback_flags_native": None,
        },
        clear=False,
    ), patch('worlds.kirbyam.client.bizhawk.read', new_callable=AsyncMock) as mock_read:
        mock_read.return_value = [(300).to_bytes(4, 'little')]

        active, reason, ai_state = await client._runtime_gameplay_state(mock_bizhawk_context)

    assert active is True
    assert reason == "gameplay_active"
    assert ai_state == 300


@pytest.mark.asyncio
async def test_runtime_gameplay_state_non_gameplay_on_cutscene_state(mock_bizhawk_context):
    """AI state 200 should defer gameplay polling/delivery as non-gameplay."""
    client = KirbyAmClient()
    client.initialize_client()

    with patch.dict(data.native_ram_addresses, {"ai_kirby_state_native": 0x0203AD2C}, clear=False), \
         patch('worlds.kirbyam.client.bizhawk.read', new_callable=AsyncMock) as mock_read:
        mock_read.return_value = [(200).to_bytes(4, 'little')]

        active, reason, ai_state = await client._runtime_gameplay_state(mock_bizhawk_context)

    assert active is False
    assert reason == "non_gameplay_cutscene"
    assert ai_state == 200


@pytest.mark.asyncio
async def test_runtime_gameplay_state_non_gameplay_on_tutorial_or_menu_state(mock_bizhawk_context):
    """AI state below cutscene threshold should be classified as tutorial/menu non-gameplay."""
    client = KirbyAmClient()
    client.initialize_client()

    with patch.dict(data.native_ram_addresses, {"ai_kirby_state_native": 0x0203AD2C}, clear=False), \
         patch('worlds.kirbyam.client.bizhawk.read', new_callable=AsyncMock) as mock_read:
        mock_read.return_value = [(100).to_bytes(4, 'little')]

        active, reason, ai_state = await client._runtime_gameplay_state(mock_bizhawk_context)

    assert active is False
    assert reason == "non_gameplay_tutorial_or_menu"
    assert ai_state == 100


@pytest.mark.asyncio
@pytest.mark.parametrize("goal_clear_state", [9999, 10000])
async def test_runtime_gameplay_state_non_gameplay_on_goal_clear_state(mock_bizhawk_context, goal_clear_state):
    """Goal-clear AI states should remain classified as non-gameplay."""
    client = KirbyAmClient()
    client.initialize_client()

    with patch.dict(data.native_ram_addresses, {"ai_kirby_state_native": 0x0203AD2C}, clear=False), \
         patch('worlds.kirbyam.client.bizhawk.read', new_callable=AsyncMock) as mock_read:
        mock_read.return_value = [(goal_clear_state).to_bytes(4, 'little')]

        active, reason, ai_state = await client._runtime_gameplay_state(mock_bizhawk_context)

    assert active is False
    assert reason == "non_gameplay_goal_clear"
    assert ai_state == goal_clear_state


@pytest.mark.asyncio
async def test_runtime_gameplay_state_fail_open_on_unknown_post_normal_state(mock_bizhawk_context):
    """Unknown post-300 AI states should fail open so item delivery is not blocked."""
    client = KirbyAmClient()
    client.initialize_client()

    with patch.dict(data.native_ram_addresses, {"ai_kirby_state_native": 0x0203AD2C}, clear=False), \
         patch('worlds.kirbyam.client.bizhawk.read', new_callable=AsyncMock) as mock_read:
        mock_read.return_value = [(301).to_bytes(4, 'little')]

        active, reason, ai_state = await client._runtime_gameplay_state(mock_bizhawk_context)

    assert active is True
    assert reason == "gameplay_active"
    assert ai_state == 301


@pytest.mark.asyncio
async def test_runtime_gameplay_state_fail_open_when_signal_unavailable(mock_bizhawk_context):
    """Missing ai_kirby_state_native should fail open for compatibility."""
    client = KirbyAmClient()
    client.initialize_client()

    with patch.dict(data.native_ram_addresses, {}, clear=True), \
         patch('worlds.kirbyam.client.bizhawk.read', new_callable=AsyncMock) as mock_read:
        active, reason, ai_state = await client._runtime_gameplay_state(mock_bizhawk_context)

    assert active is True
    assert reason == "gate_signal_unavailable"
    assert ai_state is None
    mock_read.assert_not_awaited()


@pytest.mark.asyncio
async def test_game_watcher_defers_polling_and_new_writes_when_non_gameplay(mock_bizhawk_context):
    """In non-gameplay state, watcher defers location/boss polling and new mailbox writes."""
    client = KirbyAmClient()
    client.initialize_client()

    with patch.object(client, '_runtime_gameplay_state', new_callable=AsyncMock) as mock_gate, \
         patch.object(client, '_load_persistent_state', new_callable=AsyncMock) as mock_load, \
         patch.object(client, '_poll_locations', new_callable=AsyncMock) as mock_poll_locations, \
         patch.object(client, '_poll_boss_defeat_locations', new_callable=AsyncMock) as mock_poll_boss, \
         patch.object(client, '_probe_boss_defeat_candidates', new_callable=AsyncMock) as mock_probe, \
            patch.object(client, '_probe_unsafe_delivery_candidates', new_callable=AsyncMock) as mock_probe_unsafe, \
         patch.object(client, '_deliver_items', new_callable=AsyncMock) as mock_deliver, \
            patch.object(client, '_maybe_report_goal', new_callable=AsyncMock) as mock_goal, \
            patch('worlds.kirbyam.client.bizhawk.display_message', new_callable=AsyncMock) as mock_display:
        mock_gate.return_value = (False, "non_gameplay_cutscene", 200)

        await client.game_watcher(mock_bizhawk_context)

    mock_load.assert_awaited_once()
    mock_poll_locations.assert_not_awaited()
    mock_poll_boss.assert_not_awaited()
    mock_probe.assert_not_awaited()
    mock_probe_unsafe.assert_not_awaited()
    mock_deliver.assert_awaited_once_with(mock_bizhawk_context, allow_new_writes=False)
    mock_goal.assert_awaited_once_with(mock_bizhawk_context, ai_state_override=200)
    mock_display.assert_awaited_once_with(mock_bizhawk_context.bizhawk_ctx, "Item sending paused by game state")


@pytest.mark.asyncio
async def test_game_watcher_emits_pause_then_resume_popups_on_transition(mock_bizhawk_context):
    """Watcher should emit one pause and one resume popup across gameplay gate transitions."""
    client = KirbyAmClient()
    client.initialize_client()

    with patch.object(client, '_runtime_gameplay_state', new_callable=AsyncMock) as mock_gate, \
         patch.object(client, '_load_persistent_state', new_callable=AsyncMock), \
         patch.object(client, '_reconcile_native_map_ownership', new_callable=AsyncMock), \
         patch.object(client, '_apply_pending_death_link', new_callable=AsyncMock), \
         patch.object(client, '_poll_and_send_local_death_link', new_callable=AsyncMock), \
         patch.object(client, '_poll_locations', new_callable=AsyncMock), \
         patch.object(client, '_poll_boss_defeat_locations', new_callable=AsyncMock), \
         patch.object(client, '_poll_major_chest_locations', new_callable=AsyncMock), \
         patch.object(client, '_poll_minor_chest_locations', new_callable=AsyncMock), \
         patch.object(client, '_poll_vitality_chest_locations', new_callable=AsyncMock), \
         patch.object(client, '_poll_sound_player_chest_locations', new_callable=AsyncMock), \
         patch.object(client, '_poll_hub_switch_locations', new_callable=AsyncMock), \
         patch.object(client, '_probe_boss_defeat_candidates', new_callable=AsyncMock), \
         patch.object(client, '_probe_unsafe_delivery_candidates', new_callable=AsyncMock), \
         patch.object(client, '_deliver_items', new_callable=AsyncMock), \
         patch.object(client, '_maybe_report_goal', new_callable=AsyncMock), \
         patch('worlds.kirbyam.client.bizhawk.display_message', new_callable=AsyncMock) as mock_display:
        mock_gate.side_effect = [
            (False, "non_gameplay_cutscene", 200),
            (True, "gameplay_active", 300),
        ]

        await client.game_watcher(mock_bizhawk_context)
        await client.game_watcher(mock_bizhawk_context)

    mock_display.assert_any_await(mock_bizhawk_context.bizhawk_ctx, "Item sending paused by game state")
    mock_display.assert_any_await(mock_bizhawk_context.bizhawk_ctx, "Item sending resumed")


@pytest.mark.asyncio
async def test_game_watcher_suppresses_runtime_gate_logs_when_debug_disabled(mock_bizhawk_context):
    client = KirbyAmClient()
    client.initialize_client()

    with patch.object(client, '_runtime_gameplay_state', new_callable=AsyncMock) as mock_gate, \
         patch.object(client, '_load_persistent_state', new_callable=AsyncMock), \
         patch.object(client, '_deliver_items', new_callable=AsyncMock), \
         patch.object(client, '_maybe_report_goal', new_callable=AsyncMock), \
         patch('worlds.kirbyam.client.bizhawk.display_message', new_callable=AsyncMock), \
         patch('CommonClient.logger') as mock_logger:
        mock_gate.return_value = (False, "non_gameplay_tutorial_or_menu", 0)

        await client.game_watcher(mock_bizhawk_context)

    defer_logs = [
        call for call in mock_logger.info.call_args_list
        if call.args and isinstance(call.args[0], str)
        and "deferring location polling/new item writes" in call.args[0]
    ]
    assert defer_logs == []


@pytest.mark.asyncio
async def test_game_watcher_emits_runtime_gate_logs_when_debug_enabled(mock_bizhawk_context):
    client = KirbyAmClient()
    client.initialize_client()
    mock_bizhawk_context.slot_data["debug"] = {"logging": True}

    with patch.object(client, '_runtime_gameplay_state', new_callable=AsyncMock) as mock_gate, \
         patch.object(client, '_load_persistent_state', new_callable=AsyncMock), \
         patch.object(client, '_reconcile_native_map_ownership', new_callable=AsyncMock), \
            patch.object(client, '_log_boss_shard_debug_window', new_callable=AsyncMock), \
         patch.object(client, '_apply_pending_death_link', new_callable=AsyncMock), \
         patch.object(client, '_poll_and_send_local_death_link', new_callable=AsyncMock), \
         patch.object(client, '_poll_boss_defeat_locations', new_callable=AsyncMock), \
         patch.object(client, '_poll_major_chest_locations', new_callable=AsyncMock), \
         patch.object(client, '_poll_minor_chest_locations', new_callable=AsyncMock), \
         patch.object(client, '_poll_vitality_chest_locations', new_callable=AsyncMock), \
         patch.object(client, '_poll_sound_player_chest_locations', new_callable=AsyncMock), \
         patch.object(client, '_poll_hub_switch_locations', new_callable=AsyncMock), \
         patch.object(client, '_poll_room_sanity_locations', new_callable=AsyncMock), \
         patch.object(client, '_probe_boss_defeat_candidates', new_callable=AsyncMock), \
         patch.object(client, '_probe_unsafe_delivery_candidates', new_callable=AsyncMock), \
         patch.object(client, '_deliver_items', new_callable=AsyncMock), \
         patch.object(client, '_maybe_report_goal', new_callable=AsyncMock), \
         patch('worlds.kirbyam.client.bizhawk.display_message', new_callable=AsyncMock), \
         patch('CommonClient.logger') as mock_logger:
        mock_gate.side_effect = [
            (False, "non_gameplay_tutorial_or_menu", 0),
            (True, "gameplay_active", 300),
        ]

        await client.game_watcher(mock_bizhawk_context)
        await client.game_watcher(mock_bizhawk_context)

    mock_logger.info.assert_any_call(
        "KirbyAM: deferring location polling/new item writes (%s, ai_state=%s)",
        "non_gameplay_tutorial_or_menu",
        0,
    )
    mock_logger.info.assert_any_call(
        "KirbyAM: gameplay-active state restored; resuming normal watcher flow"
    )


@pytest.mark.asyncio
async def test_game_watcher_syncs_death_link_enabled_from_slot_data(mock_bizhawk_context):
    """DeathLink tag state should be enabled when slot_data.death_link is true."""
    client = KirbyAmClient()
    client.initialize_client()
    mock_bizhawk_context.slot_data["death_link"] = 1

    with patch.object(client, '_runtime_gameplay_state', new_callable=AsyncMock) as mock_gate, \
         patch.object(client, '_load_persistent_state', new_callable=AsyncMock), \
         patch.object(client, '_reconcile_native_map_ownership', new_callable=AsyncMock), \
            patch.object(client, '_apply_pending_death_link', new_callable=AsyncMock), \
            patch.object(client, '_poll_and_send_local_death_link', new_callable=AsyncMock), \
         patch.object(client, '_poll_locations', new_callable=AsyncMock), \
         patch.object(client, '_poll_boss_defeat_locations', new_callable=AsyncMock), \
         patch.object(client, '_poll_major_chest_locations', new_callable=AsyncMock), \
         patch.object(client, '_poll_minor_chest_locations', new_callable=AsyncMock), \
         patch.object(client, '_poll_vitality_chest_locations', new_callable=AsyncMock), \
         patch.object(client, '_poll_sound_player_chest_locations', new_callable=AsyncMock), \
         patch.object(client, '_poll_hub_switch_locations', new_callable=AsyncMock), \
         patch.object(client, '_probe_boss_defeat_candidates', new_callable=AsyncMock), \
         patch.object(client, '_probe_unsafe_delivery_candidates', new_callable=AsyncMock), \
         patch.object(client, '_deliver_items', new_callable=AsyncMock), \
         patch.object(client, '_maybe_report_goal', new_callable=AsyncMock):
        mock_gate.return_value = (True, "gameplay_active", 300)
        await client.game_watcher(mock_bizhawk_context)

    mock_bizhawk_context.update_death_link.assert_awaited_once_with(True)


@pytest.mark.asyncio
async def test_game_watcher_death_link_sync_is_deduped_until_value_changes(mock_bizhawk_context):
    """DeathLink tag update should not repeat every frame when slot_data value is unchanged."""
    client = KirbyAmClient()
    client.initialize_client()
    mock_bizhawk_context.slot_data["death_link"] = False

    with patch.object(client, '_runtime_gameplay_state', new_callable=AsyncMock) as mock_gate, \
         patch.object(client, '_load_persistent_state', new_callable=AsyncMock), \
         patch.object(client, '_reconcile_native_map_ownership', new_callable=AsyncMock), \
            patch.object(client, '_apply_pending_death_link', new_callable=AsyncMock), \
            patch.object(client, '_poll_and_send_local_death_link', new_callable=AsyncMock), \
         patch.object(client, '_poll_locations', new_callable=AsyncMock), \
         patch.object(client, '_poll_boss_defeat_locations', new_callable=AsyncMock), \
         patch.object(client, '_poll_major_chest_locations', new_callable=AsyncMock), \
         patch.object(client, '_poll_minor_chest_locations', new_callable=AsyncMock), \
         patch.object(client, '_poll_vitality_chest_locations', new_callable=AsyncMock), \
         patch.object(client, '_poll_sound_player_chest_locations', new_callable=AsyncMock), \
         patch.object(client, '_poll_hub_switch_locations', new_callable=AsyncMock), \
         patch.object(client, '_probe_boss_defeat_candidates', new_callable=AsyncMock), \
         patch.object(client, '_probe_unsafe_delivery_candidates', new_callable=AsyncMock), \
         patch.object(client, '_deliver_items', new_callable=AsyncMock), \
         patch.object(client, '_maybe_report_goal', new_callable=AsyncMock):
        mock_gate.return_value = (True, "gameplay_active", 300)
        await client.game_watcher(mock_bizhawk_context)
        await client.game_watcher(mock_bizhawk_context)

        # Change slot_data runtime value and ensure one additional sync call.
        mock_bizhawk_context.slot_data["death_link"] = True
        await client.game_watcher(mock_bizhawk_context)

    assert mock_bizhawk_context.update_death_link.await_count == 2
    mock_bizhawk_context.update_death_link.assert_any_await(False)
    mock_bizhawk_context.update_death_link.assert_any_await(True)


def test_on_package_queues_incoming_death_link_when_enabled(mock_bizhawk_context):
    """DeathLink Bounced packets should queue one pending incoming kill event."""
    client = KirbyAmClient()
    client.initialize_client()
    client._death_link_enabled = True

    client.on_package(
        mock_bizhawk_context,
        "Bounced",
        {"tags": ["DeathLink"], "data": {"time": 123.0, "source": "Other Player"}},
    )

    assert client._incoming_death_link_pending is True
    assert client._last_incoming_death_link_time == 123.0


def test_death_link_flavor_templates_loaded_from_data_file():
    """DeathLink flavor text templates should be loaded through the JSON data loader."""
    sentinel_templates = [
        "{player} was defeated by a mysterious force.",
        "{player} found the wrong kind of shortcut.",
    ]

    with patch("worlds.kirbyam.client.load_json_data", return_value=sentinel_templates) as mock_loader:
        client = KirbyAmClient()
        client.initialize_client()

    mock_loader.assert_any_call("deathlink_flavor_text.json")
    assert client._death_link_flavor_templates == sentinel_templates


@pytest.mark.asyncio
async def test_apply_pending_death_link_writes_zero_hp(mock_bizhawk_context):
    """Incoming DeathLink should write Kirby HP to zero when gameplay is active."""
    client = KirbyAmClient()
    client.initialize_client()
    client._death_link_enabled = True
    client._incoming_death_link_pending = True

    with patch.dict(data.native_ram_addresses, {"kirby_hp_native": 0x02020FE0}, clear=False), \
         patch('worlds.kirbyam.client.bizhawk.read', new_callable=AsyncMock) as mock_read, \
         patch('worlds.kirbyam.client.bizhawk.write', new_callable=AsyncMock) as mock_write:
        mock_read.return_value = [(5).to_bytes(1, 'little')]

        await client._apply_pending_death_link(mock_bizhawk_context)

    mock_write.assert_awaited_once_with(
        mock_bizhawk_context.bizhawk_ctx,
        [(0x02020FE0, (0).to_bytes(1, 'little'), 'System Bus')]
    )
    assert client._incoming_death_link_pending is False
    assert client._suppress_next_local_death_send is True


@pytest.mark.asyncio
async def test_local_death_transition_sends_death_link_once(mock_bizhawk_context):
    """Outgoing DeathLink should send once on an alive->dead transition."""
    client = KirbyAmClient()
    client.initialize_client()
    client._death_link_enabled = True
    client._death_link_flavor_templates = ["{player} got lost in the mirror world."]
    mock_bizhawk_context.player_names = {1: "hasherwi"}

    with patch.dict(data.native_ram_addresses, {"kirby_hp_native": 0x02020FE0}, clear=False), \
         patch('worlds.kirbyam.client.bizhawk.read', new_callable=AsyncMock) as mock_read:
        mock_read.side_effect = [
            [(5).to_bytes(1, 'little')],
            [(0).to_bytes(1, 'little')],
            [(0).to_bytes(1, 'little')],
        ]

        await client._poll_and_send_local_death_link(mock_bizhawk_context)
        await client._poll_and_send_local_death_link(mock_bizhawk_context)
        await client._poll_and_send_local_death_link(mock_bizhawk_context)

    mock_bizhawk_context.send_death.assert_awaited_once_with("hasherwi got lost in the mirror world.")


@pytest.mark.asyncio
async def test_incoming_death_link_suppresses_echo_send(mock_bizhawk_context):
    """Applying incoming DeathLink should not immediately re-send an outgoing DeathLink."""
    client = KirbyAmClient()
    client.initialize_client()
    client._death_link_enabled = True
    client._incoming_death_link_pending = True
    client._last_local_alive_state = True

    with patch.dict(data.native_ram_addresses, {"kirby_hp_native": 0x02020FE0}, clear=False), \
         patch('worlds.kirbyam.client.bizhawk.read', new_callable=AsyncMock) as mock_read, \
         patch('worlds.kirbyam.client.bizhawk.write', new_callable=AsyncMock) as mock_write:
        mock_read.side_effect = [
            [(5).to_bytes(1, 'little')],
            [(0).to_bytes(1, 'little')],
        ]

        await client._apply_pending_death_link(mock_bizhawk_context)
        await client._poll_and_send_local_death_link(mock_bizhawk_context)

    mock_write.assert_awaited_once()
    mock_bizhawk_context.send_death.assert_not_awaited()
    assert client._suppress_next_local_death_send is False


@pytest.mark.asyncio
async def test_apply_pending_death_link_already_dead_does_not_suppress(mock_bizhawk_context):
    """Receiving DeathLink while already dead should not suppress the next real local death."""
    client = KirbyAmClient()
    client.initialize_client()
    client._death_link_enabled = True
    client._incoming_death_link_pending = True

    with patch.dict(data.native_ram_addresses, {"kirby_hp_native": 0x02020FE0}, clear=False), \
         patch('worlds.kirbyam.client.bizhawk.read', new_callable=AsyncMock) as mock_read, \
         patch('worlds.kirbyam.client.bizhawk.write', new_callable=AsyncMock) as mock_write:
        mock_read.return_value = [(0).to_bytes(1, 'little')]

        await client._apply_pending_death_link(mock_bizhawk_context)

    mock_write.assert_not_awaited()
    assert client._incoming_death_link_pending is False
    assert client._suppress_next_local_death_send is False


@pytest.mark.asyncio
async def test_deliver_items_defers_new_write_when_gated(mock_bizhawk_context):
    """Delivery gating should preserve state and avoid writing a new mailbox item."""
    client = KirbyAmClient()
    client.initialize_client()

    mock_bizhawk_context.items_received = [
        Mock(item=3860001, player=1),
    ]

    with patch('worlds.kirbyam.client.bizhawk.read', new_callable=AsyncMock) as mock_read, \
         patch('worlds.kirbyam.client.bizhawk.write', new_callable=AsyncMock) as mock_write:
        mock_read.return_value = [
            (0).to_bytes(4, 'little'),
            (0).to_bytes(4, 'little'),
            (100).to_bytes(4, 'little'),
        ]

        await client._deliver_items(mock_bizhawk_context, allow_new_writes=False)

    assert client._delivery_pending is False
    assert client._delivered_item_index == 0
    mock_write.assert_not_awaited()


@pytest.mark.asyncio
async def test_poll_boss_defeat_sends_location_checks_for_set_bits(mock_bizhawk_context):
    """Boss defeat transport register with a set bit should produce a LocationChecks send."""
    client = KirbyAmClient()
    client.initialize_client()

    boss1_loc = data.locations["BOSS_DEFEAT_1"].location_id
    mock_bizhawk_context.checked_locations = set()

    with patch.dict(data.transport_ram_addresses, {"boss_defeat_flags": 0x0203B024}, clear=False), \
         patch('worlds.kirbyam.client.bizhawk.read', new_callable=AsyncMock) as mock_read, \
         patch.object(mock_bizhawk_context, 'send_msgs', new_callable=AsyncMock) as mock_send, \
         patch('CommonClient.logger') as mock_logger:
        # Bit 0 set — Mustard Mountain boss defeated
        mock_read.return_value = [(0x01).to_bytes(4, 'little')]

        await client._poll_boss_defeat_locations(mock_bizhawk_context)

        mock_send.assert_awaited_once_with([
            {"cmd": "LocationChecks", "locations": [boss1_loc]}
        ])
        assert mock_logger.info.called
        assert "resending boss-defeat LocationChecks missing on server" in mock_logger.info.call_args.args[0]
        assert mock_logger.info.call_args.args[1] == [boss1_loc]


@pytest.mark.asyncio
async def test_poll_boss_defeat_skips_already_server_acknowledged(mock_bizhawk_context):
    """No LocationChecks sent when boss defeat bit is set but server already acknowledged it."""
    client = KirbyAmClient()
    client.initialize_client()
    client._debug_logging_enabled = True

    boss1_loc = data.locations["BOSS_DEFEAT_1"].location_id
    mock_bizhawk_context.checked_locations = {boss1_loc}

    with patch.dict(data.transport_ram_addresses, {"boss_defeat_flags": 0x0203B024}, clear=False), \
         patch('worlds.kirbyam.client.bizhawk.read', new_callable=AsyncMock) as mock_read, \
         patch.object(mock_bizhawk_context, 'send_msgs', new_callable=AsyncMock) as mock_send, \
         patch('CommonClient.logger') as mock_logger:
        mock_read.return_value = [(0x01).to_bytes(4, 'little')]

        await client._poll_boss_defeat_locations(mock_bizhawk_context)

        mock_send.assert_not_awaited()
        assert mock_logger.debug.called
        assert "dedupe suppressed boss-defeat LocationChecks" in mock_logger.debug.call_args.args[0]
        assert mock_logger.debug.call_args.args[1] == [boss1_loc]


@pytest.mark.asyncio
async def test_poll_boss_defeat_uses_probe_fallback_when_transport_bit_missing(mock_bizhawk_context):
    """Issue #573: probe-observed native boss bit should backfill missing transport signal."""
    client = KirbyAmClient()
    client.initialize_client()

    boss1_loc = data.locations["BOSS_DEFEAT_1"].location_id
    mock_bizhawk_context.checked_locations = set()

    with patch.dict(
        data.transport_ram_addresses,
        {"boss_defeat_flags": 0x0203B024},
        clear=False,
    ), patch.dict(
        data.native_ram_addresses,
        {"boss_mirror_table_native": 0x02028C14},
        clear=False,
    ), patch('worlds.kirbyam.client.bizhawk.read', new_callable=AsyncMock) as mock_read, \
         patch.object(mock_bizhawk_context, 'send_msgs', new_callable=AsyncMock) as mock_send:
        # Probe baseline then rising edge for bit 0 (boss 1), then poll transport=0.
        mock_read.side_effect = [
            [bytes(32)],
            [bytes([0x01]) + bytes(31)],
            [(0x00).to_bytes(4, 'little')],
        ]

        await client._probe_boss_defeat_candidates(mock_bizhawk_context)
        await client._probe_boss_defeat_candidates(mock_bizhawk_context)
        await client._poll_boss_defeat_locations(mock_bizhawk_context)

    mock_send.assert_awaited_once_with([
        {"cmd": "LocationChecks", "locations": [boss1_loc]}
    ])


@pytest.mark.asyncio
async def test_poll_boss_defeat_skips_when_address_missing(mock_bizhawk_context):
    """When boss_defeat_flags address is not in addresses.json the method should no-op."""
    client = KirbyAmClient()
    client.initialize_client()

    transport_without_boss = {k: v for k, v in data.transport_ram_addresses.items() if k != "boss_defeat_flags"}

    with patch.dict(data.transport_ram_addresses, transport_without_boss, clear=True), \
         patch('worlds.kirbyam.client.bizhawk.read', new_callable=AsyncMock) as mock_read:
        await client._poll_boss_defeat_locations(mock_bizhawk_context)
        mock_read.assert_not_awaited()


@pytest.mark.asyncio
async def test_shard_poll_does_not_trigger_boss_defeat_locations(mock_bizhawk_context):
    """Shard bitfield polling must not send boss-defeat location checks."""
    client = KirbyAmClient()
    client.initialize_client()

    mock_bizhawk_context.checked_locations = set()

    with patch.object(mock_bizhawk_context, 'send_msgs', new_callable=AsyncMock) as mock_send:
        await client._poll_locations(mock_bizhawk_context)
        mock_send.assert_not_awaited()


@pytest.mark.asyncio
async def test_poll_enemy_ability_reroll_events_treats_counter_rollback_as_reset(mock_bizhawk_context):
    """Counter rollback after mailbox reset must not produce a false missed-events log."""
    client = KirbyAmClient()
    client.initialize_client()
    client._debug_logging_enabled = True
    mock_bizhawk_context.slot_data = {"ability_randomization_mode": 2}

    counter_addr = data.transport_ram_addresses["ability_reroll_event_counter_runtime"]
    source_addr_addr = data.transport_ram_addresses["ability_reroll_source_addr_runtime"]
    ability_id_addr = data.transport_ram_addresses["ability_reroll_ability_id_runtime"]

    with patch('worlds.kirbyam.client.bizhawk.read', new_callable=AsyncMock) as mock_read, \
         patch('CommonClient.logger') as mock_logger:
        mock_read.side_effect = [
            [(5).to_bytes(4, 'little')],
            [(0).to_bytes(4, 'little')],
            [(1).to_bytes(4, 'little')],
            [(0x00123456).to_bytes(4, 'little'), (3).to_bytes(4, 'little')],
        ]

        await client._poll_enemy_ability_reroll_events(mock_bizhawk_context)
        await client._poll_enemy_ability_reroll_events(mock_bizhawk_context)
        await client._poll_enemy_ability_reroll_events(mock_bizhawk_context)

    assert client._last_ability_reroll_event_counter == 1
    assert len(mock_read.await_args_list) == 4
    assert mock_read.await_args_list[0].args == (
        mock_bizhawk_context.bizhawk_ctx,
        [(counter_addr, 4, "System Bus")],
    )
    assert mock_read.await_args_list[1].args == (
        mock_bizhawk_context.bizhawk_ctx,
        [(counter_addr, 4, "System Bus")],
    )
    assert mock_read.await_args_list[2].args == (
        mock_bizhawk_context.bizhawk_ctx,
        [(counter_addr, 4, "System Bus")],
    )
    assert mock_read.await_args_list[3].args == (
        mock_bizhawk_context.bizhawk_ctx,
        [
            (source_addr_addr, 4, "System Bus"),
            (ability_id_addr, 4, "System Bus"),
        ],
    )

    unexpected_missed_event_logs = [
        call
        for call in mock_logger.info.call_args_list
        if call.args and isinstance(call.args[0], str) and "occurred between polls" in call.args[0]
    ]
    assert unexpected_missed_event_logs == []
    mock_logger.info.assert_any_call(
        "Kirby swallowed a %s. Ability was rerolled to %s.",
        "UNKNOWN_0x123456",
        "Burning",
        extra={"NoStream": False},
    )


@pytest.mark.asyncio
async def test_sync_enemy_copy_ability_runtime_config_rewrites_when_revalidation_detects_mailbox_drift(mock_bizhawk_context):
    """When signature is unchanged, periodic read-back should still rewrite drifted mailbox state."""
    client = KirbyAmClient()
    client.initialize_client()

    policy = {
        "mode": 2,
        "seed": 0x0000000100000002,
        "ability_randomization_no_ability_weight": 55,
        "allowed_abilities": [],
    }
    mock_bizhawk_context.slot_data = {"enemy_copy_ability_policy": policy}

    mode = 2
    seed_lo = 2
    seed_hi = 1
    no_ability_weight = 55
    allowed_mask = 0
    client._last_ability_runtime_config_signature = (mode, seed_lo, seed_hi, no_ability_weight, allowed_mask)
    client._ability_runtime_config_revalidate_counter = 999

    with patch('worlds.kirbyam.client.bizhawk.read', new_callable=AsyncMock) as mock_read, \
         patch('worlds.kirbyam.client.bizhawk.write', new_callable=AsyncMock) as mock_write:
        mock_read.return_value = [
            (0).to_bytes(4, 'little'),
            (0).to_bytes(4, 'little'),
            (0).to_bytes(4, 'little'),
            (0).to_bytes(4, 'little'),
            (0).to_bytes(4, 'little'),
        ]

        await client._sync_enemy_copy_ability_runtime_config(mock_bizhawk_context)

    mode_addr = data.transport_ram_addresses["ability_randomization_mode_runtime"]
    seed_lo_addr = data.transport_ram_addresses["ability_randomization_seed_lo_runtime"]
    seed_hi_addr = data.transport_ram_addresses["ability_randomization_seed_hi_runtime"]
    weight_addr = data.transport_ram_addresses["ability_randomization_no_ability_weight_runtime"]
    mask_addr = data.transport_ram_addresses["ability_randomization_allowed_mask_runtime"]
    rng_state_addr = data.transport_ram_addresses["ability_randomization_rng_state_runtime"]

    mock_read.assert_awaited_once_with(
        mock_bizhawk_context.bizhawk_ctx,
        [
            (mode_addr, 4, "System Bus"),
            (seed_lo_addr, 4, "System Bus"),
            (seed_hi_addr, 4, "System Bus"),
            (weight_addr, 4, "System Bus"),
            (mask_addr, 4, "System Bus"),
        ],
    )
    mock_write.assert_awaited_once_with(
        mock_bizhawk_context.bizhawk_ctx,
        [
            (mode_addr, (mode).to_bytes(4, "little"), "System Bus"),
            (seed_lo_addr, (seed_lo).to_bytes(4, "little"), "System Bus"),
            (seed_hi_addr, (seed_hi).to_bytes(4, "little"), "System Bus"),
            (weight_addr, (no_ability_weight).to_bytes(4, "little"), "System Bus"),
            (mask_addr, (allowed_mask).to_bytes(4, "little"), "System Bus"),
            (rng_state_addr, (0).to_bytes(4, "little"), "System Bus"),
        ],
    )


def test_vitality_chest_locations_defined_in_regions():
    """Regression test: all VITALITY_CHEST locations must be registered in their regions.

    Issue #428 occurred because vitality chest locations were defined in locations.json
    but not referenced in areas.json. This test prevents that regression from silently
    recurring during future region edits.
    """
    # Derive vitality chest keys from locations data to keep this test future-proof.
    location_category_enum = getattr(data, "LocationCategory", None)
    vitality_category = getattr(location_category_enum, "VITALITY_CHEST", None) if location_category_enum else None
    vitality_chest_keys = {
        key
        for key, loc in data.locations.items()
        if key.startswith("VITALITY_CHEST_")
        or (vitality_category is not None and getattr(loc, "category", None) == vitality_category)
    }

    # Verify vitality chests were found (derivation logic sanity check).
    assert vitality_chest_keys, "No VITALITY_CHEST locations found in locations.json"

    # Verify each vitality chest is registered in a region.
    all_region_locations = set()
    for region_data in data.regions.values():
        all_region_locations.update(region_data.locations)

    for key in vitality_chest_keys:
        assert key in all_region_locations, \
            f"VITALITY_CHEST location '{key}' defined in locations.json but not registered in any region in areas.json"


def test_hub_switch_locations_defined_in_regions():
    """Regression test: all HUB_SWITCH locations must be registered in their regions."""
    location_category_enum = getattr(data, "LocationCategory", None)
    hub_switch_category = getattr(location_category_enum, "HUB_SWITCH", None) if location_category_enum else None
    hub_switch_keys = {
        key
        for key, loc in data.locations.items()
        if key.startswith("HUB_SWITCH_")
        or (hub_switch_category is not None and getattr(loc, "category", None) == hub_switch_category)
    }

    assert hub_switch_keys, "No HUB_SWITCH locations found in locations.json"

    all_region_locations = set()
    for region_data in data.regions.values():
        all_region_locations.update(region_data.locations)

    for key in hub_switch_keys:
        assert key in all_region_locations, \
            f"HUB_SWITCH location '{key}' defined in locations.json but not registered in any region in areas.json"


def test_minor_chest_locations_defined_in_regions_when_present():
    """All MINOR_CHEST locations (when enabled) must be registered in some data/regions entry."""
    minor_chest_keys = {
        key
        for key, loc in data.locations.items()
        if key.startswith("MINOR_CHEST_")
        or (getattr(loc, "category", None) == LocationCategory.MINOR_CHEST)
    }

    if not minor_chest_keys:
        return

    all_region_locations = set()
    for region_data in data.regions.values():
        all_region_locations.update(region_data.locations)

    for key in minor_chest_keys:
        assert key in all_region_locations, \
            f"MINOR_CHEST location '{key}' defined in locations.json but not registered in any data/regions/*.json entry"


def test_minor_chest_locations_have_unique_bit_indices_when_present():
    """Enabled MINOR_CHEST locations must not reuse native bit indices."""
    minor_chest_with_bits = [
        loc for loc in data.locations.values()
        if getattr(loc, "category", None) == LocationCategory.MINOR_CHEST
        and getattr(loc, "bit_index", None) is not None
    ]
    if not minor_chest_with_bits:
        return

    bit_indices = [loc.bit_index for loc in minor_chest_with_bits if loc.bit_index is not None]
    assert len(bit_indices) == len(set(bit_indices)), (
        "MINOR_CHEST locations must use unique bit_index values to avoid duplicate AP checks: "
        f"{bit_indices}"
    )
