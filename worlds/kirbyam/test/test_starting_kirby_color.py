from __future__ import annotations

from random import Random
from types import SimpleNamespace
from unittest.mock import AsyncMock, patch

import pytest

from .. import KirbyAmWorld
from ..client import KirbyAmClient
from ..colors import STARTING_KIRBY_COLOR_RANDOM_OPTION, load_kirby_colors
from ..data import data


def test_world_helper_resolves_starting_kirby_color_random_choice() -> None:
    world = KirbyAmWorld.__new__(KirbyAmWorld)
    world.random = Random(0)
    world.options = SimpleNamespace(
        starting_kirby_color=SimpleNamespace(
            current_key="random_color",
            value=STARTING_KIRBY_COLOR_RANDOM_OPTION,
        ),
    )
    resolved_color_id, resolved_color_name = KirbyAmWorld._get_resolved_starting_kirby_color(world)

    supported = {color.color_id: color.display_name for color in load_kirby_colors()}
    assert resolved_color_id in supported
    assert resolved_color_name == supported[resolved_color_id]


def test_world_helper_caches_resolved_starting_kirby_color_random_choice() -> None:
    world = KirbyAmWorld.__new__(KirbyAmWorld)
    world.random = Random(0)
    world.options = SimpleNamespace(
        starting_kirby_color=SimpleNamespace(
            current_key="random_color",
            value=STARTING_KIRBY_COLOR_RANDOM_OPTION,
        ),
    )

    first = KirbyAmWorld._get_resolved_starting_kirby_color(world)
    second = KirbyAmWorld._get_resolved_starting_kirby_color(world)

    assert first == second


@pytest.mark.asyncio
async def test_client_syncs_starting_kirby_color_runtime_config_once(mock_bizhawk_context) -> None:
    client = KirbyAmClient()
    client.initialize_client()
    mock_bizhawk_context.slot_data = {
        "debug": {"logging": False},
        "starting_kirby_color": 7,
        "starting_kirby_color_name": "Sapphire",
    }

    with (
        patch.dict(
            data.transport_ram_addresses,
            {"starting_kirby_color_id": 0x0203B050},
            clear=False,
        ),
        patch(
            "worlds.kirbyam.client.bizhawk.read",
            new_callable=AsyncMock,
            # First call: mailbox holds sentinel (unsynced).
            side_effect=[
                [(0xFFFFFFFF).to_bytes(4, "little")],
            ],
        ) as mock_read,
        patch(
            "worlds.kirbyam.client.bizhawk.write",
            new_callable=AsyncMock,
        ) as mock_write,
    ):
        client._load_debug_settings(mock_bizhawk_context)
        await client._sync_starting_kirby_color_runtime_config(mock_bizhawk_context)
        await client._sync_starting_kirby_color_runtime_config(mock_bizhawk_context)

    assert mock_read.await_count == 1
    assert mock_write.await_count == 1
    write_payload = mock_write.await_args_list[0].args[1]
    assert write_payload == [(0x0203B050, (7).to_bytes(4, "little"), "System Bus")]


@pytest.mark.asyncio
async def test_client_starting_color_sync_short_circuits_after_initial_sync(mock_bizhawk_context) -> None:
    client = KirbyAmClient()
    client.initialize_client()
    mock_bizhawk_context.slot_data = {
        "debug": {"logging": False},
        "starting_kirby_color": 7,
        "starting_kirby_color_name": "Sapphire",
    }

    with (
        patch.dict(
            data.transport_ram_addresses,
            {"starting_kirby_color_id": 0x0203B050},
            clear=False,
        ),
        patch(
            "worlds.kirbyam.client.bizhawk.read",
            new_callable=AsyncMock,
            side_effect=[[(0xFFFFFFFF).to_bytes(4, "little")]],
        ) as mock_read,
        patch(
            "worlds.kirbyam.client.bizhawk.write",
            new_callable=AsyncMock,
        ) as mock_write,
    ):
        client._load_debug_settings(mock_bizhawk_context)
        await client._sync_starting_kirby_color_runtime_config(mock_bizhawk_context)
        await client._sync_starting_kirby_color_runtime_config(mock_bizhawk_context)

    assert mock_read.await_count == 1
    assert mock_write.await_count == 1


def test_load_kirby_colors_rejects_invalid_key_format() -> None:
    from .. import colors as colors_module

    load_kirby_colors.cache_clear()
    with patch.object(
        colors_module,
        "load_json_data",
        return_value={"colors": [{"key": "bad-key", "id": 1, "name": "Bad"}, {"key": "pink", "id": 0, "name": "Pink"}]},
    ):
        with pytest.raises(ValueError, match="invalid key format"):
            load_kirby_colors()
    load_kirby_colors.cache_clear()


def test_load_kirby_colors_rejects_non_string_key() -> None:
    from .. import colors as colors_module

    load_kirby_colors.cache_clear()
    with patch.object(
        colors_module,
        "load_json_data",
        return_value={"colors": [{"key": None, "id": 0, "name": "Pink"}]},
    ):
        with pytest.raises(ValueError, match="non-string key"):
            load_kirby_colors()
    load_kirby_colors.cache_clear()


def test_load_kirby_colors_rejects_non_string_name() -> None:
    from .. import colors as colors_module

    load_kirby_colors.cache_clear()
    with patch.object(
        colors_module,
        "load_json_data",
        return_value={"colors": [{"key": "pink", "id": 0, "name": None}]},
    ):
        with pytest.raises(ValueError, match="non-string display name"):
            load_kirby_colors()
    load_kirby_colors.cache_clear()


def test_load_kirby_colors_rejects_out_of_range_id() -> None:
    from .. import colors as colors_module

    load_kirby_colors.cache_clear()
    with patch.object(
        colors_module,
        "load_json_data",
        return_value={"colors": [{"key": "pink", "id": 0, "name": "Pink"}, {"key": "ultra", "id": 14, "name": "Ultra"}]},
    ):
        with pytest.raises(ValueError, match="out of supported range"):
            load_kirby_colors()
    load_kirby_colors.cache_clear()


def test_reset_reconnect_transient_state_clears_starting_color_log_signature() -> None:
    client = KirbyAmClient()
    client.initialize_client()
    client._starting_kirby_color_logged_signature = (7, "Sapphire")

    client._reset_reconnect_transient_state()

    assert client._starting_kirby_color_logged_signature is None
