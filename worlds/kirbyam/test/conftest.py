"""Pytest fixtures for Kirby AM client and world testing."""
import pytest
from typing import Dict, Generator
from unittest.mock import AsyncMock, Mock


@pytest.fixture
def mock_bizhawk_context() -> Mock:
    """
    Create a mock BizHawkClientContext with typical properties.
    
    Provides:
    - bizhawk_ctx: mock connection context
    - server: mock AP server connection
    - address: mock client address
    - state: mock game state
    - slot_data: mock slot-specific world data
    - checked_locations: set of checked location IDs
    - items_received: list of items received from server
    - send_msgs: async method mock for sending AP commands
    """
    ctx = Mock()
    ctx.bizhawk_ctx = Mock()
    ctx.server = Mock()
    ctx.server.socket = Mock()
    ctx.server.socket.closed = False
    ctx.address = ("127.0.0.1", 12345)
    ctx.state = Mock()
    ctx.slot_data = {
        "goal": "defeat_dark_mind",
        "randomize_shard_locations": True,
    }
    ctx.checked_locations = set()
    ctx.items_received = []  # List of NetworkItem objects delivered to player
    ctx.slot = 1
    ctx.team = 0
    ctx.auth = "test_auth_token"
    ctx.send_msgs = AsyncMock()  # Mock the async send_msgs method
    return ctx


@pytest.fixture
def mock_ram_read_write() -> Generator[Dict[str, bytes], None, None]:
    """
    Create a mock RAM state for reads/writes during tests.
    
    Simulates EWRAM layout with AP mailbox and game state addresses.
    Returns dict mapping address (int) -> bytes value.
    """
    ram_state: Dict[int, bytes] = {}
    
    # AP Mailbox region (0x0202C000-0x0202C028)
    ram_state[0x0202C000] = (0).to_bytes(4, 'little')  # shard_bitfield
    ram_state[0x0202C004] = (0).to_bytes(4, 'little')  # incoming_item_flag
    ram_state[0x0202C008] = (0).to_bytes(4, 'little')  # incoming_item_id
    ram_state[0x0202C00C] = (0).to_bytes(4, 'little')  # incoming_item_player
    ram_state[0x0202C010] = (0).to_bytes(4, 'little')  # debug_item_counter
    ram_state[0x0202C014] = (0).to_bytes(4, 'little')  # debug_last_item_id
    ram_state[0x0202C018] = (0).to_bytes(4, 'little')  # debug_last_from
    ram_state[0x0202C01C] = (0).to_bytes(4, 'little')  # frame_counter
    ram_state[0x0202C020] = (0).to_bytes(4, 'little')  # delivered_item_index
    
    yield ram_state


@pytest.fixture
def mock_bizhawk_read(mock_ram_read_write: Dict[int, bytes]):
    """
    Create an async mock for bizhawk.read() that returns RAM values.
    
    Usage:
        with patch('worlds.kirbyam.client.bizhawk.read', mock_bizhawk_read):
            result = await bizhawk.read(ctx, reads)
    """
    async def read_func(bizhawk_ctx, reads):
        """Mock BizHawk read: takes list of (addr, size, bus) tuples."""
        results = []
        for addr, size, bus in reads:
            # Return stored value or zeros if not set
            value = mock_ram_read_write.get(addr, b'\x00' * size)
            results.append(value[:size].ljust(size, b'\x00'))
        return results
    
    return read_func


@pytest.fixture
def mock_bizhawk_write(mock_ram_read_write: Dict[int, bytes]):
    """
    Create an async mock for bizhawk.write() that updates RAM state.
    
    Simulates writing to RAM addresses and stores values for later reads.
    """
    async def write_func(bizhawk_ctx, writes):
        """Mock BizHawk write: takes list of (addr, value, bus) tuples."""
        for addr, value, bus in writes:
            mock_ram_read_write[addr] = value
        return None
    
    return write_func


@pytest.fixture
def shard_bitfield_fixtures() -> Dict[str, int]:
    """
    Pre-generated shard bitfield values for testing location polling.
    
    Each fixture represents a different game state:
    - empty: no shards collected (0x00)
    - shard_1: first shard only (0x01)
    - shard_2_3: shards 1 and 2 (0x03)
    - all_8_shards: all 8 mirror shards (0xFF)
    """
    return {
        "empty": 0x00,
        "shard_1": 0x01,
        "shard_1_2": 0x03,
        "shard_1_2_3": 0x07,
        "shard_1_to_4": 0x0F,
        "all_8_shards": 0xFF,
    }


@pytest.fixture
def item_delivery_fixtures() -> Dict[str, Dict[str, int]]:
    """
    Pre-generated item delivery sequences for testing item handling.
    
    Each fixture contains:
    - item_id: AP item ID to deliver
    - player_id: slot ID to credit
    - expected_state_change: what should happen in client
    """
    base_offset = 3860000
    return {
        "1_up": {
            "item_id": base_offset + 1,
            "player_id": 1,
            "description": "1-Up item",
        },
        "shard_1": {
            "item_id": base_offset + 2,
            "player_id": 1,
            "description": "Mirror Shard 1",
        },
        "shard_8": {
            "item_id": base_offset + 9,
            "player_id": 1,
            "description": "Mirror Shard 8",
        },
    }


@pytest.fixture
def location_check_fixtures() -> Dict[str, int]:
    """
    Pre-generated location ID mappings for testing.
    
    Maps friendly names to location IDs used in LocationChecks commands.
    """
    base_offset = 3860100  # Base offset for Kirby AM locations
    return {
        "shard_1": base_offset + 1,
        "shard_2": base_offset + 2,
        "shard_3": base_offset + 3,
        "shard_4": base_offset + 4,
        "shard_5": base_offset + 5,
        "shard_6": base_offset + 6,
        "shard_7": base_offset + 7,
        "shard_8": base_offset + 8,
    }
