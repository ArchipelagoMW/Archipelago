from collections.abc import Callable

from worlds.generic.Rules import set_rule


def has_item(state, player: int, item_name: str) -> bool:
    return state.has(item_name, player)


def has_all_items(state, player: int, required_items: tuple[str, ...]) -> bool:
    return all(
        has_item(state, player, item_name)
        for item_name in required_items
    )


# -------------------------
# HM logic
# -------------------------

def can_cut(state, player: int) -> bool:
    return has_all_items(
        state,
        player,
        (
            "HM01 Cut",
            "Hive Badge",
        ),
    )


def can_surf(state, player: int) -> bool:
    return has_all_items(
        state,
        player,
        (
            "HM03 Surf",
            "Fog Badge",
        ),
    )


def can_strength(state, player: int) -> bool:
    return has_all_items(
        state,
        player,
        (
            "HM04 Strength",
            "Plain Badge",
        ),
    )


def can_whirlpool(state, player: int) -> bool:
    return has_all_items(
        state,
        player,
        (
            "HM05 Whirlpool",
            "Glacier Badge",
        ),
    )


def can_waterfall(state, player: int) -> bool:
    return has_all_items(
        state,
        player,
        (
            "HM07 Waterfall",
            "Rising Badge",
        ),
    )


# -------------------------
# Region access logic
# -------------------------

def can_reach_azalea(state, player: int) -> bool:
    return has_item(state, player, "Zephyr Badge")


def can_reach_ilex_forest(state, player: int) -> bool:
    return has_item(state, player, "Hive Badge")


def can_reach_goldenrod(state, player: int) -> bool:
    return can_reach_ilex_forest(state, player)


def can_reach_ecruteak(state, player: int) -> bool:
    return has_all_items(
        state,
        player,
        (
            "Plain Badge",
            "SquirtBottle",
        ),
    )


def can_reach_olivine(state, player: int) -> bool:
    return can_reach_ecruteak(state, player)


def can_reach_cianwood(state, player: int) -> bool:
    return can_surf(state, player)


def can_reach_mahogany(state, player: int) -> bool:
    return can_reach_ecruteak(state, player)


def can_reach_goldenrod_underground(state, player: int) -> bool:
    return has_all_items(
        state,
        player,
        (
            "Glacier Badge",
            "Radio Card",
        ),
    )


def can_reach_blackthorn(state, player: int) -> bool:
    return (
        has_item(state, player, "Glacier Badge")
        and can_strength(state, player)
    )


def can_reach_pokemon_league(state, player: int) -> bool:
    return can_waterfall(state, player)


# -------------------------
# Story logic
# -------------------------

def can_heal_amphy(state, player: int) -> bool:
    return has_item(state, player, "SecretPotion")


def can_clear_radio_tower(state, player: int) -> bool:
    return has_all_items(
        state,
        player,
        (
            "Radio Card",
            "Basement Key",
            "Card Key",
        ),
    )


def can_defeat_clair(state, player: int) -> bool:
    return can_whirlpool(state, player)


# -------------------------
# Entrance rules
# -------------------------

EntranceRule = Callable[[object, int], bool]


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

LocationRule = Callable[[object, int], bool]


LOCATION_RULES: dict[str, LocationRule] = {
    # Early game checks:
    # New Bark Town - Receive Starter is available from the start.
    # Route 30 - Visit Mr. Pokemon is available from the start.
    # Violet City - Defeat Falkner is available from the start.

    "Violet City - Receive Togepi Egg":
        lambda state, player: has_item(state, player, "Zephyr Badge"),

    "Ecruteak City - Defeat Kimono Girls":
        lambda state, player: has_item(state, player, "Fog Badge"),

    "Olivine City - Defeat Jasmine":
        can_heal_amphy,

    "Goldenrod Radio Tower - Receive Card Key":
        lambda state, player: has_item(state, player, "Basement Key"),

    "Goldenrod Radio Tower - Clear Radio Tower":
        can_clear_radio_tower,

    "Blackthorn City - Defeat Clair":
        can_defeat_clair,

    "Pokemon League - Defeat Lance":
        lambda state, player: has_item(state, player, "Rising Badge"),
}


def set_hgss_rules(world) -> None:
    player = world.player
    multiworld = world.multiworld

    for entrance_name, access_rule in ENTRANCE_RULES.items():
        set_rule(
            multiworld.get_entrance(entrance_name, player),
            lambda state, access_rule=access_rule: access_rule(
                state,
                player,
            ),
        )

    for location_name, access_rule in LOCATION_RULES.items():
        set_rule(
            multiworld.get_location(location_name, player),
            lambda state, access_rule=access_rule: access_rule(
                state,
                player,
            ),
        )

    multiworld.completion_condition[player] = (
        lambda state: state.has("Victory", player)
    )