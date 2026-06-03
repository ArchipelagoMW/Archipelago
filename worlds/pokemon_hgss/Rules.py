from collections.abc import Callable
from typing import Any

from worlds.generic.Rules import set_rule


def has_item(state, world: Any, item_name: str) -> bool:
    return state.has(item_name, world.player)


def has_all_items(state, world: Any, required_items: tuple[str, ...]) -> bool:
    return all(
        has_item(state, world, item_name)
        for item_name in required_items
    )


def hm_badge_requirements_enabled(world: Any) -> bool:
    return bool(world.options.hm_badge_requirements.value)


# -------------------------
# HM logic
# -------------------------

def can_cut(state, world: Any) -> bool:
    if not has_item(state, world, "HM01 Cut"):
        return False

    if not hm_badge_requirements_enabled(world):
        return True

    return has_item(state, world, "Hive Badge")


def can_surf(state, world: Any) -> bool:
    if not has_item(state, world, "HM03 Surf"):
        return False

    if not hm_badge_requirements_enabled(world):
        return True

    return has_item(state, world, "Fog Badge")


def can_strength(state, world: Any) -> bool:
    if not has_item(state, world, "HM04 Strength"):
        return False

    if not hm_badge_requirements_enabled(world):
        return True

    return has_item(state, world, "Plain Badge")


def can_whirlpool(state, world: Any) -> bool:
    if not has_item(state, world, "HM05 Whirlpool"):
        return False

    if not hm_badge_requirements_enabled(world):
        return True

    return has_item(state, world, "Glacier Badge")


def can_waterfall(state, world: Any) -> bool:
    if not has_item(state, world, "HM07 Waterfall"):
        return False

    if not hm_badge_requirements_enabled(world):
        return True

    return has_item(state, world, "Rising Badge")


# -------------------------
# Region access logic
# -------------------------

def can_reach_azalea(state, world: Any) -> bool:
    return has_item(state, world, "Zephyr Badge")


def can_reach_ilex_forest(state, world: Any) -> bool:
    return has_item(state, world, "Hive Badge")


def can_reach_goldenrod(state, world: Any) -> bool:
    return can_reach_ilex_forest(state, world)


def can_reach_ecruteak(state, world: Any) -> bool:
    return has_all_items(
        state,
        world,
        (
            "Plain Badge",
            "SquirtBottle",
        ),
    )


def can_reach_olivine(state, world: Any) -> bool:
    return can_reach_ecruteak(state, world)


def can_reach_cianwood(state, world: Any) -> bool:
    return can_surf(state, world)


def can_reach_mahogany(state, world: Any) -> bool:
    return can_reach_ecruteak(state, world)


def can_reach_goldenrod_underground(state, world: Any) -> bool:
    return has_all_items(
        state,
        world,
        (
            "Glacier Badge",
            "Radio Card",
        ),
    )


def can_reach_blackthorn(state, world: Any) -> bool:
    return (
        has_item(state, world, "Glacier Badge")
        and can_strength(state, world)
    )


def can_reach_pokemon_league(state, world: Any) -> bool:
    return can_waterfall(state, world)


# -------------------------
# Story logic
# -------------------------

def can_heal_amphy(state, world: Any) -> bool:
    return has_item(state, world, "SecretPotion")


def can_clear_radio_tower(state, world: Any) -> bool:
    return has_all_items(
        state,
        world,
        (
            "Radio Card",
            "Basement Key",
            "Card Key",
        ),
    )


def can_defeat_clair(state, world: Any) -> bool:
    return can_whirlpool(state, world)


# -------------------------
# Entrance rules
# -------------------------

EntranceRule = Callable[[object, Any], bool]


ENTRANCE_RULES: dict[str, EntranceRule] = {
    # Early route connections are open by default:
    # Menu to New Bark Town
    # New Bark Town to Route 30
    # Route 30 to Violet City

    "Violet City to Azalea Town":
        can_reach_azalea,

    "Azalea Town to Ilex Forest":
        can_reach_ilex_forest,

    "Ilex Forest to Goldenrod City":
        can_reach_goldenrod,

    "Goldenrod City to Goldenrod Radio Tower":
        can_reach_goldenrod,

    "Goldenrod City to Ecruteak City":
        can_reach_ecruteak,

    "Ecruteak City to Olivine City":
        can_reach_olivine,

    "Olivine City to Cianwood City":
        can_reach_cianwood,

    "Ecruteak City to Mahogany Town":
        can_reach_mahogany,

    "Goldenrod City to Goldenrod Underground":
        can_reach_goldenrod_underground,

    "Mahogany Town to Blackthorn City":
        can_reach_blackthorn,

    "Blackthorn City to Pokemon League":
        can_reach_pokemon_league,
}


# -------------------------
# Location rules
# -------------------------

LocationRule = Callable[[object, Any], bool]


LOCATION_RULES: dict[str, LocationRule] = {
    # Early game checks:
    # New Bark Town - Receive Starter is available from the start.
    # Route 30 - Visit Mr. Pokemon is available from the start.
    # Violet City - Defeat Falkner is available from the start.

    "Violet City - Receive Togepi Egg":
        lambda state, world: has_item(state, world, "Zephyr Badge"),

    "Ecruteak City - Defeat Kimono Girls":
        lambda state, world: has_item(state, world, "Fog Badge"),

    "Olivine City - Defeat Jasmine":
        can_heal_amphy,

    "Goldenrod Radio Tower - Receive Card Key":
        lambda state, world: has_item(state, world, "Basement Key"),

    "Goldenrod Radio Tower - Clear Radio Tower":
        can_clear_radio_tower,

    "Blackthorn City - Defeat Clair":
        can_defeat_clair,

    "Pokemon League - Defeat Lance":
        lambda state, world: has_item(state, world, "Rising Badge"),
}


def set_hgss_rules(world) -> None:
    multiworld = world.multiworld
    player = world.player

    for entrance_name, access_rule in ENTRANCE_RULES.items():
        set_rule(
            multiworld.get_entrance(entrance_name, player),
            lambda state, access_rule=access_rule: access_rule(
                state,
                world,
            ),
        )

    for location_name, access_rule in LOCATION_RULES.items():
        set_rule(
            multiworld.get_location(location_name, player),
            lambda state, access_rule=access_rule: access_rule(
                state,
                world,
            ),
        )

    multiworld.completion_condition[player] = (
        lambda state: state.has("Victory", player)
    )