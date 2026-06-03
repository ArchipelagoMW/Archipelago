from worlds.generic.Rules import set_rule


LOCATION_RULES = {
    # Falkner is available from the start.

    "Azalea Town - Defeat Bugsy": (
        "Zephyr Badge",
    ),
    "Goldenrod City - Defeat Whitney": (
        "Hive Badge",
    ),
    "Ecruteak City - Defeat Morty": (
        "Plain Badge",
    ),
    "Cianwood City - Defeat Chuck": (
        "Fog Badge",
    ),
    "Olivine City - Defeat Jasmine": (
        "Storm Badge",
    ),
    "Mahogany Town - Defeat Pryce": (
        "Mineral Badge",
    ),
    "Blackthorn City - Defeat Clair": (
        "Glacier Badge",
    ),
    "Pokemon League - Defeat Lance": (
        "Rising Badge",
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