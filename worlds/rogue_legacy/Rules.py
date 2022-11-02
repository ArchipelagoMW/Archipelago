from BaseClasses import MultiWorld, CollectionState

from ..AutoWorld import LogicMixin
from ..generic.Rules import set_rule


class LegacyLogic(LogicMixin):
    def has_any_vendors(self: CollectionState, player: int) -> bool:
        return self.has_any({"Blacksmith", "Enchantress"}, player)

    def has_all_vendors(self: CollectionState, player: int) -> bool:
        return self.has_all({"Blacksmith", "Enchantress"}, player)

    def has_stat_upgrades(self, player: int, amount: int) -> bool:
        return self.stat_upgrade_count(player) >= amount

    def total_stat_upgrades_count(self, player: int) -> int:
        return int(self.multiworld.health_pool[player]) + \
               int(self.multiworld.mana_pool[player]) + \
               int(self.multiworld.attack_pool[player]) + \
               int(self.multiworld.magic_damage_pool[player])

    def stat_upgrade_count(self: CollectionState, player: int) -> int:
        return self.item_count("Health Up", player) + self.item_count("Mana Up", player) + \
               self.item_count("Attack Up", player) + self.item_count("Magic Damage Up", player)


def set_rules(multiworld: MultiWorld, player: int):
    # Vendors
    if multiworld.vendors[player] == "normal":
        set_rule(multiworld.get_location("Forest Abkhazia Boss Reward", player),
                 lambda state: state.has_all_vendors(player))

    # Scale each manor location.
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

    for event, locations in manor_rules.items():
        for location in locations:
            set_rule(multiworld.get_location(location, player), lambda state: state.has(event, player))

    # Standard Zone Progression
    multiworld.get_entrance("Forest Abkhazia", player).access_rule = \
        (lambda state: state.has_stat_upgrades(player, 0.125 * state.total_stat_upgrades_count(player)) and
                       (state.has("Defeat Khidr", player) or state.has("Defeat Neo Khidr", player)))
    multiworld.get_entrance("The Maya", player).access_rule = \
        (lambda state: state.has_stat_upgrades(player, 0.25 * state.total_stat_upgrades_count(player)) and
                           (state.has("Defeat Alexander", player) or state.has("Defeat Alexander IV", player)))
    multiworld.get_entrance("Land of Darkness", player).access_rule = \
        (lambda state: state.has_stat_upgrades(player, 0.375 * state.total_stat_upgrades_count(player)) and
                           (state.has("Defeat Ponce de Leon", player) or state.has("Defeat Ponce de Freon", player)))
    multiworld.get_entrance("The Fountain Room", player).access_rule = \
        (lambda state: state.has_stat_upgrades(player, 0.5 * state.total_stat_upgrades_count(player)) and
                           (state.has("Defeat Herodotus", player) or state.has("Defeat Astrodotus", player)))

    multiworld.completion_condition[player] = lambda state: state.has("Defeat The Fountain", player)
