from BaseClasses import CollectionState
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from . import RLWorld


def get_upgrade_total(world: "RLWorld") -> int:
    return int(world.options.health_pool) + int(world.options.mana_pool) + \
           int(world.options.attack_pool) + int(world.options.magic_damage_pool)


def get_upgrade_count(state: CollectionState, player: int) -> int:
    return state.count("Health Up", player) + state.count("Mana Up", player) + \
        state.count("Attack Up", player) + state.count("Magic Damage Up", player)


def has_vendors(state: CollectionState, player: int) -> bool:
    return state.has_all({"Blacksmith", "Enchantress"}, player)


def has_upgrade_amount(state: CollectionState, player: int, amount: int) -> bool:
    return get_upgrade_count(state, player) >= amount


def has_upgrades_percentage(state: CollectionState, world: "RLWorld", percentage: float) -> bool:
    return has_upgrade_amount(state, world.player, round(get_upgrade_total(world) * (percentage / 100)))


def has_movement_rune(state: CollectionState, player: int) -> bool:
    return state.has("Vault Runes", player) or state.has("Sprint Runes", player) or state.has("Sky Runes", player)


def has_fairy_progression(state: CollectionState, player: int) -> bool:
    return state.has("Dragons", player) or (state.has("Enchantress", player) and has_movement_rune(state, player))


def has_defeated_castle(state: CollectionState, player: int) -> bool:
    return state.has("Defeat Khidr", player) or state.has("Defeat Neo Khidr", player)


def has_defeated_forest(state: CollectionState, player: int) -> bool:
    return state.has("Defeat Alexander", player) or state.has("Defeat Alexander IV", player)


def has_defeated_tower(state: CollectionState, player: int) -> bool:
    return state.has("Defeat Ponce de Leon", player) or state.has("Defeat Ponce de Freon", player)


def has_defeated_dungeon(state: CollectionState, player: int) -> bool:
    return state.has("Defeat Herodotus", player) or state.has("Defeat Astrodotus", player)


def set_rules(world: "RLWorld", player: int):
    # If 'vendors' are 'normal', then expect it to show up in the first half(ish) of the spheres.
    if world.options.vendors == "normal":
        world.get_location("Forest Abkhazia Boss Reward").access_rule = \
            lambda state: has_vendors(state, player)

    # Gate each manor location so everything isn't dumped into sphere 1.
    manor_rules = {
        "Defeat Khidr" if world.options.khidr == "vanilla" else "Defeat Neo Khidr": [
            "Manor - Left Wing Window",
            "Manor - Left Wing Rooftop",
            "Manor - Right Wing Window",
            "Manor - Right Wing Rooftop",
            "Manor - Left Big Base",
            "Manor - Right Big Base",
            "Manor - Left Tree 1",
            "Manor - Left Tree 2",
            "Manor - Right Tree",
        ],
        "Defeat Alexander" if world.options.alexander == "vanilla" else "Defeat Alexander IV": [
            "Manor - Left Big Upper 1",
            "Manor - Left Big Upper 2",
            "Manor - Left Big Windows",
            "Manor - Left Big Rooftop",
            "Manor - Left Far Base",
            "Manor - Left Far Roof",
            "Manor - Left Extension",
            "Manor - Right Big Upper",
            "Manor - Right Big Rooftop",
            "Manor - Right Extension",
        ],
        "Defeat Ponce de Leon" if world.options.leon == "vanilla" else "Defeat Ponce de Freon": [
            "Manor - Right High Base",
            "Manor - Right High Upper",
            "Manor - Right High Tower",
            "Manor - Observatory Base",
            "Manor - Observatory Telescope",
        ]
    }

    # Set rules for manor locations.
    for event, locations in manor_rules.items():
        for location in locations:
            world.get_location(location).access_rule = lambda state: state.has(event, player)

    # Set rules for fairy chests to decrease headache of expectation to find non-movement fairy chests.
    for fairy_location in [location for location in world.multiworld.get_locations(player) if "Fairy" in location.name]:
        fairy_location.access_rule = lambda state: has_fairy_progression(state, player)

    # Region rules.
    world.get_entrance("Forest Abkhazia").access_rule = \
        lambda state: has_upgrades_percentage(state, world, 12.5) and has_defeated_castle(state, player)

    world.get_entrance("The Maya").access_rule = \
        lambda state: has_upgrades_percentage(state, world, 25) and has_defeated_forest(state, player)

    world.get_entrance("Land of Darkness").access_rule = \
        lambda state: has_upgrades_percentage(state, world, 37.5) and has_defeated_tower(state, player)

    world.get_entrance("The Fountain Room").access_rule = \
        lambda state: has_upgrades_percentage(state, world, 50) and has_defeated_dungeon(state, player)

    # Win condition.
    world.multiworld.completion_condition[player] = lambda state: state.has("Defeat The Fountain", player)
