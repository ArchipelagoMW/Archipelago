from worlds.generic.Rules import set_rule


def set_hgss_rules(world) -> None:
    player = world.player
    multiworld = world.multiworld

    # Falkner is available from the start.
    # This gives the player an initial check.

    set_rule(
        multiworld.get_location("Azalea Town - Defeat Bugsy", player),
        lambda state: state.has("Zephyr Badge", player),
    )

    set_rule(
        multiworld.get_location("Goldenrod City - Defeat Whitney", player),
        lambda state: state.has("Hive Badge", player),
    )

    set_rule(
        multiworld.get_location("Ecruteak City - Defeat Morty", player),
        lambda state: state.has("Plain Badge", player),
    )

    set_rule(
        multiworld.get_location("Cianwood City - Defeat Chuck", player),
        lambda state: state.has("Fog Badge", player),
    )

    set_rule(
        multiworld.get_location("Olivine City - Defeat Jasmine", player),
        lambda state: state.has("Storm Badge", player),
    )

    set_rule(
        multiworld.get_location("Mahogany Town - Defeat Pryce", player),
        lambda state: state.has("Mineral Badge", player),
    )

    set_rule(
        multiworld.get_location("Blackthorn City - Defeat Clair", player),
        lambda state: state.has("Glacier Badge", player),
    )

    set_rule(
        multiworld.get_location("Pokemon League - Defeat Lance", player),
        lambda state: state.has("Rising Badge", player),
    )

    multiworld.completion_condition[player] = (
        lambda state: state.has("Victory", player)
    )