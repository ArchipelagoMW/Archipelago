"""Integration tests for client polling and delivery logic."""
import pytest
from unittest.mock import AsyncMock, patch

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
        mock_read.return_value = [(0x01).to_bytes(4, 'little')]

        await client._poll_locations(mock_bizhawk_context)

        mock_read.assert_awaited_once_with(
            mock_bizhawk_context.bizhawk_ctx,
            [(0x02038970, 4, 'System Bus')]
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


def test_client_initialization():
    """Test client state is properly initialized."""
    client = KirbyAmClient()
    client.initialize_client()
    
    assert client._checked_location_bits == set()
    assert client._delivered_item_index == 0
    assert client._delivery_pending is False
    assert client._goal_reported is False
