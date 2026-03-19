"""Integration tests for client polling and delivery logic."""
import pytest
import logging
from unittest.mock import AsyncMock, Mock, patch

from ..data import data
from ..client import KirbyAmClient


@pytest.mark.asyncio
async def test_poll_locations_empty_bitfield(mock_bizhawk_context):
    """Test _poll_locations with no shards collected."""
    client = KirbyAmClient()
    client.initialize_client()
    
    # Mock empty shard bitfield (0x0202C000 = 0x00)
    with patch('worlds.kirbyam.client.bizhawk.read', new_callable=AsyncMock) as mock_read:
        mock_read.return_value = [(0).to_bytes(4, 'little')]
        
        await client._poll_locations(mock_bizhawk_context)
        
        # No new locations should be checked
        assert len(client._checked_location_bits) == 0


@pytest.mark.asyncio
async def test_poll_locations_single_shard(mock_bizhawk_context):
    """Test _poll_locations when one shard is collected."""
    client = KirbyAmClient()
    client.initialize_client()
    
    # Mock shard bitfield with bit 0 set (first shard)
    with patch('worlds.kirbyam.client.bizhawk.read', new_callable=AsyncMock) as mock_read:
        mock_read.return_value = [(0x01).to_bytes(4, 'little')]
        
        await client._poll_locations(mock_bizhawk_context)
        
        # Bit 0 should be marked as checked
        assert 0 in client._checked_location_bits


@pytest.mark.asyncio
async def test_poll_locations_prefers_native_shard_address(mock_bizhawk_context):
    """Test _poll_locations reads the native shard bitfield when available."""
    client = KirbyAmClient()
    client.initialize_client()

    with patch.dict(data.native_ram_addresses, {"shard_bitfield_native": 0x02038970}, clear=False), \
         patch.dict(data.transport_ram_addresses, {"shard_bitfield": 0x0202C000}, clear=False), \
         patch('worlds.kirbyam.client.bizhawk.read', new_callable=AsyncMock) as mock_read:
        mock_read.return_value = [(0x01).to_bytes(1, 'little')]

        await client._poll_locations(mock_bizhawk_context)

        mock_read.assert_awaited_once_with(
            mock_bizhawk_context.bizhawk_ctx,
            [(0x02038970, 1, 'System Bus')]
        )


@pytest.mark.asyncio
async def test_poll_locations_falls_back_to_transport_shard_address(mock_bizhawk_context):
    """Test _poll_locations falls back to transport shard bitfield when native key is missing."""
    client = KirbyAmClient()
    client.initialize_client()

    with patch.dict(data.native_ram_addresses, {}, clear=True), \
         patch.dict(data.transport_ram_addresses, {"shard_bitfield": 0x0202C000}, clear=False), \
         patch('worlds.kirbyam.client.bizhawk.read', new_callable=AsyncMock) as mock_read:
        mock_read.return_value = [(0x01).to_bytes(4, 'little')]

        await client._poll_locations(mock_bizhawk_context)

        mock_read.assert_awaited_once_with(
            mock_bizhawk_context.bizhawk_ctx,
            [(0x0202C000, 4, 'System Bus')]
        )


@pytest.mark.asyncio
async def test_poll_locations_multiple_shards(mock_bizhawk_context, shard_bitfield_fixtures):
    """Test _poll_locations with multiple shards."""
    client = KirbyAmClient()
    client.initialize_client()
    
    # Test with shard_1_2_3 pattern (bits 0, 1, 2 set)
    with patch('worlds.kirbyam.client.bizhawk.read', new_callable=AsyncMock) as mock_read:
        mock_read.return_value = [shard_bitfield_fixtures["shard_1_2_3"].to_bytes(4, 'little')]
        
        await client._poll_locations(mock_bizhawk_context)
        
        # Bits 0, 1, 2 should be marked as checked
        assert 0 in client._checked_location_bits
        assert 1 in client._checked_location_bits
        assert 2 in client._checked_location_bits


@pytest.mark.asyncio
async def test_poll_locations_ignores_unmapped_reserved_bits(mock_bizhawk_context):
    """Test reserved/high bits are ignored when they do not map to any location."""
    client = KirbyAmClient()
    client.initialize_client()

    with patch.dict(data.native_ram_addresses, {}, clear=True), \
         patch.dict(data.transport_ram_addresses, {"shard_bitfield": 0x0202C000}, clear=False), \
         patch('worlds.kirbyam.client.bizhawk.read', new_callable=AsyncMock) as mock_read:
        # Bits 0 and 31 set; only bit 0 maps to current shard locations.
        mock_read.return_value = [(0x80000001).to_bytes(4, 'little')]

        await client._poll_locations(mock_bizhawk_context)

        assert 0 in client._checked_location_bits
        assert 31 not in client._checked_location_bits


@pytest.mark.asyncio
async def test_location_check_sent_on_new_shard(mock_bizhawk_context):
    """Test that LocationChecks is sent when a new shard is detected."""
    client = KirbyAmClient()
    client.initialize_client()
    
    # Pre-populate bizhawk context checked locations
    mock_bizhawk_context.checked_locations = set()
    
    # Mock read returning bit 0 set (first new shard)
    with patch('worlds.kirbyam.client.bizhawk.read', new_callable=AsyncMock) as mock_read, \
         patch.object(mock_bizhawk_context, 'send_msgs', new_callable=AsyncMock) as mock_send:
        
        mock_read.return_value = [(0x01).to_bytes(4, 'little')]
        
        await client._poll_locations(mock_bizhawk_context)

        mock_send.assert_awaited_once_with([
            {"cmd": "LocationChecks", "locations": [data.locations["SHARD_1"].location_id]}
        ])


@pytest.mark.asyncio
async def test_location_check_resent_when_server_missing_location(mock_bizhawk_context):
    """RAM-derived checks should be resent if server checked_locations is missing them."""
    client = KirbyAmClient()
    client.initialize_client()

    first_loc = data.locations["SHARD_1"].location_id
    second_loc = data.locations["SHARD_2"].location_id
    # Simulate server knowing only shard 1 while RAM reports shards 1+2.
    mock_bizhawk_context.checked_locations = {first_loc}

    with patch('worlds.kirbyam.client.bizhawk.read', new_callable=AsyncMock) as mock_read, \
         patch.object(mock_bizhawk_context, 'send_msgs', new_callable=AsyncMock) as mock_send:

        mock_read.return_value = [(0x03).to_bytes(4, 'little')]

        await client._poll_locations(mock_bizhawk_context)

        mock_send.assert_awaited_once_with([
            {"cmd": "LocationChecks", "locations": [second_loc]}
        ])


def test_client_initialization():
    """Test client state is properly initialized."""
    client = KirbyAmClient()
    client.initialize_client()
    
    assert client._checked_location_bits == set()
    assert client._delivered_item_index == 0
    assert client._delivery_pending is False
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
async def test_deliver_items_resyncs_forward_after_reconnect(mock_bizhawk_context):
    """If ROM counter is ahead, client should fast-forward and deliver next missing item."""
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
        # mailbox empty, ROM says first two items were already applied
        mock_read.return_value = [
            (0).to_bytes(4, 'little'),
            (2).to_bytes(4, 'little'),
        ]

        await client._deliver_items(mock_bizhawk_context)

        assert client._delivered_item_index == 2
        assert client._delivery_pending is True
        written = mock_write.await_args.args[1]
        assert written[0][1] == int(3860003).to_bytes(4, 'little')


@pytest.mark.asyncio
async def test_deliver_items_waits_when_rom_counter_ahead_but_items_partial(mock_bizhawk_context):
    """Do not write items while ReceivedItems list is still behind ROM counter."""
    client = KirbyAmClient()
    client.initialize_client()
    client._delivered_item_index = 0
    client._delivery_pending = False

    mock_bizhawk_context.items_received = [
        Mock(item=3860001, player=1),
    ]

    with patch('worlds.kirbyam.client.bizhawk.read', new_callable=AsyncMock) as mock_read, \
         patch('worlds.kirbyam.client.bizhawk.write', new_callable=AsyncMock) as mock_write:
        mock_read.return_value = [
            (0).to_bytes(4, 'little'),
            (2).to_bytes(4, 'little'),
        ]

        await client._deliver_items(mock_bizhawk_context)

        assert client._delivered_item_index == len(mock_bizhawk_context.items_received)
        assert client._delivery_pending is False
        mock_write.assert_awaited_once()
        persisted = mock_write.await_args.args[1]
        assert persisted == [
            (data.transport_ram_addresses["delivered_item_index"], (1).to_bytes(4, 'little'), "System Bus")
        ]


@pytest.mark.asyncio
async def test_deliver_items_skips_malformed_entries_and_logs_warning(mock_bizhawk_context, caplog):
    """Malformed ReceivedItems entries should be skipped, logged, and not crash delivery."""
    client = KirbyAmClient()
    client.initialize_client()

    mock_bizhawk_context.items_received = [
        Mock(item="bad", player=1),
        Mock(item=3860001, player=1),
    ]

    caplog.set_level(logging.WARNING, logger="Archipelago")

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
