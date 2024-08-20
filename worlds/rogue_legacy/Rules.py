from BaseClasses import CollectionState, MultiWorld


def get_upgrade_total(multiworld: MultiWorld, player: int) -> int:
    return int(multiworld.health_pool[player]) + int(multiworld.mana_pool[player]) + \
           int(multiworld.attack_pool[player]) + int(multiworld.magic_damage_pool[player])


def get_upgrade_count(state: CollectionState, player: int) -> int:
    return state.count("Health Up", player) + state.count("Mana Up", player) + \
        state.count("Attack Up", player) + state.count("Magic Damage Up", player)


def has_vendors(state: CollectionState, player: int) -> bool:
    return state.has_all({"Blacksmith", "Enchantress"}, player)


def has_upgrade_amount(state: CollectionState, player: int, amount: int) -> bool:
    return get_upgrade_count(state, player) >= amount


def has_upgrades_percentage(state: CollectionState, player: int, percentage: float) -> bool:
    return has_upgrade_amount(state, player, round(get_upgrade_total(state.multiworld, player) * (percentage / 100)))


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


def set_rules(multiworld: MultiWorld, player: int):
    # If 'vendors' are 'normal', then expect it to show up in the first half(ish) of the spheres.
    if multiworld.vendors[player] == "normal":
        multiworld.get_location("Forest Abkhazia Boss Reward", player).access_rule = \
            lambda state: has_vendors(state, player)

    # Gate each manor location so everything isn't dumped into sphere 1.
    manor_rules = {
        "Defeat Khidr" if multiworld.khidr[player] == "vanilla" else "Defeat Neo Khidr": [
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
        "Defeat Alexander" if multiworld.alexander[player] == "vanilla" else "Defeat Alexander IV": [
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
        "Defeat Ponce de Leon" if multiworld.leon[player] == "vanilla" else "Defeat Ponce de Freon": [
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
            multiworld.get_location(location, player).access_rule = lambda state: state.has(event, player)

    # Set rules for fairy chests to decrease headache of expectation to find non-movement fairy chests.
    for fairy_location in [location for location in multiworld.get_locations(player) if "Fairy" in location.name]:
        fairy_location.access_rule = lambda state: has_fairy_progression(state, player)

    # Region rules.
    multiworld.get_entrance("Forest Abkhazia", player).access_rule = \
        lambda state: has_upgrades_percentage(state, player, 12.5) and has_defeated_castle(state, player)

    multiworld.get_entrance("The Maya", player).access_rule = \
        lambda state: has_upgrades_percentage(state, player, 25) and has_defeated_forest(state, player)

    multiworld.get_entrance("Land of Darkness", player).access_rule = \
        lambda state: has_upgrades_percentage(state, player, 37.5) and has_defeated_tower(state, player)

    multiworld.get_entrance("The Fountain Room", player).access_rule = \
        lambda state: has_upgrades_percentage(state, player, 50) and has_defeated_dungeon(state, player)

    # Win condition.
    multiworld.completion_condition[player] = lambda state: state.has("Defeat The Fountain", player)
