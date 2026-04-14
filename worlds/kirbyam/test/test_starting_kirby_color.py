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


def test_client_starting_color_config_log_hidden_when_debug_disabled(mock_bizhawk_context) -> None:
    client = KirbyAmClient()
    client.initialize_client()
    client._debug_logging_enabled = False
    mock_bizhawk_context.slot_data = {
        "starting_kirby_color": 0,
        "starting_kirby_color_name": "Pink",
    }

    with patch("CommonClient.logger.info") as mock_info:
        client._log_starting_kirby_color_config_once(mock_bizhawk_context)
        client._log_starting_kirby_color_config_once(mock_bizhawk_context)

    assert mock_info.call_count == 0


def test_client_starting_color_config_log_emits_once_when_debug_enabled(mock_bizhawk_context) -> None:
    client = KirbyAmClient()
    client.initialize_client()
    client._debug_logging_enabled = True
    mock_bizhawk_context.slot_data = {
        "starting_kirby_color": 0,
        "starting_kirby_color_name": "Pink",
    }

    with patch("CommonClient.logger.info") as mock_info:
        client._log_starting_kirby_color_config_once(mock_bizhawk_context)
        client._log_starting_kirby_color_config_once(mock_bizhawk_context)

    assert mock_info.call_count == 1
    assert mock_info.call_args.args[0] == "KirbyAM: configured starting Kirby color is %s (%s)"


def test_client_starting_color_config_log_emits_after_debug_toggle_on(mock_bizhawk_context) -> None:
    client = KirbyAmClient()
    client.initialize_client()
    client._debug_logging_enabled = False
    mock_bizhawk_context.slot_data = {
        "starting_kirby_color": 0,
        "starting_kirby_color_name": "Pink",
    }

    with patch("CommonClient.logger.info") as mock_info:
        client._log_starting_kirby_color_config_once(mock_bizhawk_context)

        client._debug_logging_enabled = True
        client._log_starting_kirby_color_config_once(mock_bizhawk_context)

    assert mock_info.call_count == 1
    assert client._starting_kirby_color_logged_signature == (0, "Pink")


@pytest.mark.asyncio
async def test_client_starting_color_sync_log_hidden_when_debug_disabled(mock_bizhawk_context) -> None:
    client = KirbyAmClient()
    client.initialize_client()
    client._debug_logging_enabled = False
    mock_bizhawk_context.slot_data = {
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
        ),
        patch(
            "worlds.kirbyam.client.bizhawk.write",
            new_callable=AsyncMock,
        ),
        patch("CommonClient.logger.info") as mock_info,
    ):
        await client._sync_starting_kirby_color_runtime_config(mock_bizhawk_context)

    assert mock_info.call_count == 0


@pytest.mark.asyncio
async def test_client_game_watcher_logs_starting_color_once_after_initial_ready_transition(
    mock_bizhawk_context,
) -> None:
    client = KirbyAmClient()
    client.initialize_client()
    client._ram_state_loaded = True
    mock_bizhawk_context.slot_data = {
        "starting_kirby_color": 0,
        "starting_kirby_color_name": "Pink",
    }
    mock_bizhawk_context.server = SimpleNamespace(socket=SimpleNamespace(closed=False))
    mock_bizhawk_context.items_received = []
    mock_bizhawk_context.bizhawk_ctx = object()

    with (
        patch.object(client, "_sync_death_link_setting", new=AsyncMock()),
        patch.object(client, "_sync_enemy_copy_ability_runtime_config", new=AsyncMock()),
        patch.object(
            client,
            "_load_debug_settings",
            side_effect=lambda _ctx: setattr(client, "_debug_logging_enabled", True),
        ),
        patch.object(client, "_sync_starting_kirby_color_runtime_config", new=AsyncMock()),
        patch.object(client, "_runtime_gameplay_state", new=AsyncMock(return_value=(False, "menu", None))),
        patch.object(client, "_log_boss_shard_debug_window", new=AsyncMock()),
        patch.object(client, "_display_client_message", new=AsyncMock()),
        patch.object(client, "_deliver_items", new=AsyncMock()),
        patch.object(client, "_maybe_report_goal", new=AsyncMock()),
        patch("CommonClient.logger.info") as mock_info,
    ):
        await client.game_watcher(mock_bizhawk_context)
        await client.game_watcher(mock_bizhawk_context)

    matching = [
        call for call in mock_info.call_args_list
        if call.args and call.args[0] == "KirbyAM: configured starting Kirby color is %s (%s)"
    ]
    assert len(matching) == 1
