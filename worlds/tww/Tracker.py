"""
Universal Tracker support for The Wind Waker randomizer.

This module contains all Universal Tracker-specific logic including:
- Deferred entrance tracking and reconnection
- UT generation detection and handling
- Option restoration from UT slot_data
"""

from typing import Any, NamedTuple

# Universal Tracker multiworld attribute names
UT_RE_GEN_PASSTHROUGH_ATTR = "re_gen_passthrough"
UT_GENERATION_IS_FAKE_ATTR = "generation_is_fake"
UT_ENFORCE_DEFERRED_CONNECTIONS_ATTR = "enforce_deferred_connections"

# Wind Waker game name for UT identification
WIND_WAKER_GAME_NAME = "The Wind Waker"

class DatastorageParsed(NamedTuple):
    """Parsed datastorage key for deferred entrance tracking."""
    team: int
    player: int
    stage_name: str

def is_ut_generation(multiworld: Any) -> bool:
    """
    Check if the current generation is a Universal Tracker generation.

    :param multiworld: The MultiWorld object.
    :return: True if UT is active, False otherwise.
    """
    return hasattr(multiworld, UT_GENERATION_IS_FAKE_ATTR) and getattr(multiworld, UT_GENERATION_IS_FAKE_ATTR)

def get_ut_slot_data(multiworld: Any, game_name: str = WIND_WAKER_GAME_NAME) -> dict[str, Any] | None:
    """
    Get the slot_data from re_gen_passthrough for the given game.

    :param multiworld: The MultiWorld object.
    :param game_name: The game name to look up (defaults to "The Wind Waker").
    :return: The slot_data dict if available, None otherwise.
    """
    re_gen_passthrough = getattr(multiworld, UT_RE_GEN_PASSTHROUGH_ATTR, {})
    if not re_gen_passthrough or game_name not in re_gen_passthrough:
        return None
    return re_gen_passthrough[game_name]

def should_defer_entrances(multiworld: Any, has_randomized_entrances: bool) -> bool:
    """
    Check if entrances should be deferred based on UT and server settings.

    :param multiworld: The MultiWorld object.
    :param has_randomized_entrances: Whether the world has randomized entrances.
    :return: True if entrances should be deferred, False otherwise.
    """
    # Only defer entrances during UT regeneration
    if not is_ut_generation(multiworld):
        return False

    # Check if server has deferred connections enabled
    deferred_enabled = getattr(
        multiworld,
        UT_ENFORCE_DEFERRED_CONNECTIONS_ATTR,
        None
    ) in ("on", "default")

    # Only defer if entrances are actually randomized
    return deferred_enabled and has_randomized_entrances


def parse_datastorage_key(key: str) -> DatastorageParsed | None:
    """
    Parse a datastorage key and return parsed components or None if invalid.

    Expected format: tww_<team>_<player>_<stagename>

    :param key: The datastorage key to parse.
    :return: DatastorageParsed with team, player, stage_name, or None if invalid.
    """
    parts = key.split("_")
    min_parts = 4
    if len(parts) < min_parts or parts[0] != "tww":
        return None
    try:
        team = int(parts[1])
        player = int(parts[2])
        stage_name = "_".join(parts[3:])
        return DatastorageParsed(team=team, player=player, stage_name=stage_name)
    except (ValueError, IndexError):
        return None
