"""Pytest fixtures for Kirby AM client and world testing."""
import json
import logging
import pytest
from itertools import count
from pathlib import Path
from typing import Any, Dict, Generator
from unittest.mock import AsyncMock, Mock

from ..data import data


FIXTURE_DATA_DIR = Path(__file__).resolve().parent / "data"
REPO_ROOT = Path(__file__).resolve().parents[3]
TEST_OUTPUT_DIR = REPO_ROOT / "test-output" / "kirbyam"
TEST_LOG_FILE = TEST_OUTPUT_DIR / "pytest-kirbyam.log"
TEST_LOGGER = logging.getLogger("worlds.kirbyam.test")
_IO_SEQUENCE = count(1)


def _load_fixture_json(filename: str) -> dict[str, Any]:
    with (FIXTURE_DATA_DIR / filename).open("r", encoding="utf-8") as fixture_file:
        loaded = json.load(fixture_file)
    if not isinstance(loaded, dict):
        raise TypeError(f"Fixture file {filename} must contain a JSON object")
    return loaded


def _format_payload(payload: Any) -> Any:
    if isinstance(payload, bytes):
        return payload.hex()
    if isinstance(payload, list):
        return [_format_payload(value) for value in payload]
    if isinstance(payload, tuple):
        return tuple(_format_payload(value) for value in payload)
    if isinstance(payload, dict):
        return {key: _format_payload(value) for key, value in payload.items()}
    return payload


def pytest_configure(config: pytest.Config) -> None:
    TEST_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    handler = logging.FileHandler(TEST_LOG_FILE, mode="w", encoding="utf-8")
    handler.setFormatter(logging.Formatter(
        "%(asctime)s %(levelname)s [%(name)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    ))
    handler.setLevel(logging.DEBUG)

    root_logger = logging.getLogger()
    root_logger.addHandler(handler)
    root_logger.setLevel(logging.DEBUG)

    config._kirbyam_test_log_handler = handler  # type: ignore[attr-defined]
    TEST_LOGGER.info("KirbyAM pytest logging initialized. output=%s", TEST_LOG_FILE)


def pytest_unconfigure(config: pytest.Config) -> None:
    handler = getattr(config, "_kirbyam_test_log_handler", None)
    if handler is None:
        return
    logging.getLogger().removeHandler(handler)
    handler.close()


def pytest_runtest_setup(item: pytest.Item) -> None:
    TEST_LOGGER.info("START test=%s", item.nodeid)


def pytest_runtest_teardown(item: pytest.Item, nextitem: pytest.Item | None) -> None:
    del nextitem
    TEST_LOGGER.info("END test=%s", item.nodeid)


@pytest.fixture(scope="session")
def kirbyam_test_log_dir() -> Path:
    return TEST_OUTPUT_DIR


@pytest.fixture(scope="session")
def kirbyam_test_log_file(kirbyam_test_log_dir: Path) -> Path:
    del kirbyam_test_log_dir
    return TEST_LOG_FILE


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

    async def send_msgs_side_effect(messages):
        request_id = next(_IO_SEQUENCE)
        TEST_LOGGER.debug("ap.send_msgs[%s] request=%s", request_id, _format_payload(messages))
        TEST_LOGGER.debug("ap.send_msgs[%s] response=accepted", request_id)
        return None

    ctx.send_msgs = AsyncMock(side_effect=send_msgs_side_effect)  # Mock the async send_msgs method
    ctx.update_death_link = AsyncMock(return_value=None)
    TEST_LOGGER.debug(
        "client.context created slot=%s team=%s address=%s checked_locations=%s items_received=%s",
        ctx.slot,
        ctx.team,
        ctx.address,
        sorted(ctx.checked_locations),
        ctx.items_received,
    )
    return ctx


@pytest.fixture
def mock_ram_read_write() -> Generator[Dict[int, bytes], None, None]:
    """
    Create a mock RAM state for reads/writes during tests.
    
    Simulates EWRAM layout with AP mailbox and game state addresses.
    Returns dict mapping address (int) -> bytes value.
    """
    ram_state: Dict[int, bytes] = {}
    baseline = _load_fixture_json("ram_mailbox_baseline.json")
    baseline_u32 = baseline.get("ram_u32", {})
    if not isinstance(baseline_u32, dict):
        raise TypeError("ram_mailbox_baseline.json ram_u32 must be an object")
    for addr_text, value in baseline_u32.items():
        if not isinstance(addr_text, str):
            continue
        if not isinstance(value, int):
            continue
        ram_state[int(addr_text, 16)] = int(value).to_bytes(4, "little", signed=False)
    
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
        request_id = next(_IO_SEQUENCE)
        TEST_LOGGER.debug("bizhawk.read[%s] request=%s", request_id, _format_payload(reads))
        results = []
        for addr, size, bus in reads:
            # Return stored value or zeros if not set
            value = mock_ram_read_write.get(addr, b'\x00' * size)
            results.append(value[:size].ljust(size, b'\x00'))
        TEST_LOGGER.debug("bizhawk.read[%s] response=%s", request_id, _format_payload(results))
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
        request_id = next(_IO_SEQUENCE)
        TEST_LOGGER.debug("bizhawk.write[%s] request=%s", request_id, _format_payload(writes))
        for addr, value, bus in writes:
            mock_ram_read_write[addr] = value
        TEST_LOGGER.debug("bizhawk.write[%s] response=stored", request_id)
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
    payload = _load_fixture_json("shard_bitfields.json")
    scenarios = payload.get("scenarios", {})
    if not isinstance(scenarios, dict):
        raise TypeError("shard_bitfields.json scenarios must be an object")
    result: Dict[str, int] = {}
    for scenario_name, scenario_data in scenarios.items():
        if not isinstance(scenario_name, str) or not isinstance(scenario_data, dict):
            continue
        bitfield = scenario_data.get("bitfield")
        if isinstance(bitfield, int):
            result[scenario_name] = bitfield
    return result


@pytest.fixture
def item_delivery_fixtures() -> Dict[str, Dict[str, Any]]:
    """
    Pre-generated item delivery sequences for testing item handling.
    
    Each fixture contains:
    - item_id: AP item ID to deliver
    - player_id: slot ID to credit
    - expected_state_change: what should happen in client
    """
    payload = _load_fixture_json("item_delivery_sequences.json")
    scenarios = payload.get("scenarios", {})
    if not isinstance(scenarios, dict):
        raise TypeError("item_delivery_sequences.json scenarios must be an object")
    result: Dict[str, Dict[str, int]] = {}
    for scenario_name, scenario_data in scenarios.items():
        if not isinstance(scenario_name, str) or not isinstance(scenario_data, dict):
            continue
        item_id = scenario_data.get("item_id")
        player_id = scenario_data.get("player_id")
        if isinstance(item_id, int) and isinstance(player_id, int):
            result[scenario_name] = {
                "item_id": item_id,
                "player_id": player_id,
                "description": str(scenario_data.get("description", scenario_name)),
            }
    return result


@pytest.fixture
def location_check_fixtures() -> Dict[str, int]:
    """
    Pre-generated location ID mappings for testing.
    
    Maps friendly names to location IDs used in LocationChecks commands.
    """
    payload = _load_fixture_json("location_check_transitions.json")
    location_keys = payload.get("location_keys", [])
    if not isinstance(location_keys, list):
        raise TypeError("location_check_transitions.json location_keys must be a list")
    result: Dict[str, int] = {}
    for loc_key in location_keys:
        if not isinstance(loc_key, str):
            continue
        loc_data = data.locations.get(loc_key)
        if loc_data is None:
            continue
        result[loc_key.lower()] = loc_data.location_id
    return result
