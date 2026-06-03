from worlds.generic.Rules import set_rule


def set_hgss_rules(world) -> None:
    player = world.player
    multiworld = world.multiworld

    set_rule(
        multiworld.get_location("Azalea Town - Defeat Bugsy", player),
        lambda state: state.has("Zephyr Badge", player),
    )

    set_rule(
        multiworld.get_location("Goldenrod City - Defeat Whitney", player),
        lambda state: state.has("Hive Badge", player),
    )

    set_rule(
        multiworld.get_location("Pokemon League - Defeat Lance", player),
        lambda state: (
            state.has("Plain Badge", player)
            and state.has("Rising Badge", player)
        ),
    )

    multiworld.completion_condition[player] = (
        lambda state: state.has("Victory", player)
    )