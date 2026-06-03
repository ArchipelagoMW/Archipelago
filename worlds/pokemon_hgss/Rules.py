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
# Johto route/story logic
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
    return (
        can_reach_olivine(state, player)
        and can_surf(state, player)
    )


def can_reach_mahogany(state, player: int) -> bool:
    return can_reach_ecruteak(state, player)


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


def can_reach_blackthorn(state, player: int) -> bool:
    return (
        has_item(state, player, "Glacier Badge")
        and can_strength(state, player)
    )


def can_defeat_clair(state, player: int) -> bool:
    return (
        can_reach_blackthorn(state, player)
        and can_whirlpool(state, player)
    )


def can_reach_pokemon_league(state, player: int) -> bool:
    return (
        has_item(state, player, "Rising Badge")
        and can_waterfall(state, player)
    )


# -------------------------
# Location logic
# -------------------------

LocationRule = Callable[[object, int], bool]


LOCATION_RULES: dict[str, LocationRule] = {
    # Early game checks:
    # New Bark Town - Receive Starter is available from the start.
    # Route 30 - Visit Mr. Pokemon is available from the start.
    # Violet City - Defeat Falkner is available from the start.

    "Violet City - Receive Togepi Egg":
        lambda state, player: has_item(state, player, "Zephyr Badge"),

    "Azalea Town - Clear Slowpoke Well":
        can_reach_azalea,

    "Azalea Town - Defeat Bugsy":
        can_reach_azalea,

    "Ilex Forest - Clear Farfetch'd Puzzle":
        can_reach_ilex_forest,

    "Goldenrod City - Defeat Whitney":
        can_reach_goldenrod,

    "Goldenrod Radio Tower - Receive Radio Card":
        can_reach_goldenrod,

    "Ecruteak City - Defeat Rival in Burned Tower":
        can_reach_ecruteak,

    "Ecruteak City - Defeat Morty":
        can_reach_ecruteak,

    "Ecruteak City - Defeat Kimono Girls":
        lambda state, player: (
            can_reach_ecruteak(state, player)
            and has_item(state, player, "Fog Badge")
        ),

    "Olivine Lighthouse - Reach Amphy":
        can_reach_olivine,

    "Cianwood City - Receive SecretPotion":
        can_reach_cianwood,

    "Cianwood City - Defeat Chuck":
        can_reach_cianwood,

    "Olivine City - Defeat Jasmine":
        lambda state, player: (
            can_reach_olivine(state, player)
            and can_heal_amphy(state, player)
        ),

    "Mahogany Town - Clear Team Rocket HQ":
        can_reach_mahogany,

    "Mahogany Town - Defeat Pryce":
        can_reach_mahogany,

    "Goldenrod Underground - Receive Basement Key":
        lambda state, player: (
            has_item(state, player, "Glacier Badge")
            and has_item(state, player, "Radio Card")
        ),

    "Goldenrod Radio Tower - Receive Card Key":
        lambda state, player: has_item(state, player, "Basement Key"),

    "Goldenrod Radio Tower - Clear Radio Tower":
        can_clear_radio_tower,

    "Blackthorn City - Defeat Clair":
        can_defeat_clair,

    "Pokemon League - Defeat Lance":
        can_reach_pokemon_league,
}


def set_hgss_rules(world) -> None:
    player = world.player
    multiworld = world.multiworld

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