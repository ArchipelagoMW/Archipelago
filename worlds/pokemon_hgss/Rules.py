from worlds.generic.Rules import set_rule


LOCATION_RULES = {
    # Early checks:
    # New Bark Town - Receive Starter is available from the start.
    # Route 30 - Visit Mr. Pokemon is available from the start.
    # Violet City - Defeat Falkner is available from the start.

    "Violet City - Receive Togepi Egg": (
        "Zephyr Badge",
    ),

    "Azalea Town - Clear Slowpoke Well": (
        "Zephyr Badge",
    ),
    "Azalea Town - Defeat Bugsy": (
        "Zephyr Badge",
    ),

    "Ilex Forest - Clear Farfetch'd Puzzle": (
        "Hive Badge",
    ),

    "Goldenrod City - Defeat Whitney": (
        "Hive Badge",
    ),
    "Goldenrod Radio Tower - Receive Radio Card": (
        "Hive Badge",
    ),

    "Ecruteak City - Defeat Rival in Burned Tower": (
        "Plain Badge",
        "SquirtBottle",
    ),
    "Ecruteak City - Defeat Morty": (
        "Plain Badge",
        "SquirtBottle",
    ),

    "Ecruteak City - Defeat Kimono Girls": (
        "Fog Badge",
        "SquirtBottle",
    ),

    "Olivine Lighthouse - Reach Amphy": (
        "Plain Badge",
        "SquirtBottle",
    ),

    "Cianwood City - Receive SecretPotion": (
        "HM03 Surf",
        "Fog Badge",
    ),
    "Cianwood City - Defeat Chuck": (
        "HM03 Surf",
        "Fog Badge",
    ),

    "Olivine City - Defeat Jasmine": (
        "SecretPotion",
    ),

    "Mahogany Town - Clear Team Rocket HQ": (
        "Fog Badge",
        "SquirtBottle",
    ),
    "Mahogany Town - Defeat Pryce": (
        "Fog Badge",
        "SquirtBottle",
    ),

    "Goldenrod Underground - Receive Basement Key": (
        "Glacier Badge",
        "Radio Card",
    ),
    "Goldenrod Radio Tower - Receive Card Key": (
        "Basement Key",
    ),
    "Goldenrod Radio Tower - Clear Radio Tower": (
        "Card Key",
    ),

    "Blackthorn City - Defeat Clair": (
        "Glacier Badge",
        "HM04 Strength",
    ),

    "Pokemon League - Defeat Lance": (
        "Rising Badge",
        "HM07 Waterfall",
    ),
}


def has_all_items(state, player: int, required_items: tuple[str, ...]) -> bool:
    return all(
        state.has(item_name, player)
        for item_name in required_items
    )


def set_hgss_rules(world) -> None:
    player = world.player
    multiworld = world.multiworld

    for location_name, required_items in LOCATION_RULES.items():
        set_rule(
            multiworld.get_location(location_name, player),
            lambda state, required_items=required_items: has_all_items(
                state,
                player,
                required_items,
            ),
        )

    multiworld.completion_condition[player] = (
        lambda state: state.has("Victory", player)
    )