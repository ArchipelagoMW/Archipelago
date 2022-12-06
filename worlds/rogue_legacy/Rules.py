from BaseClasses import MultiWorld

from ..AutoWorld import LogicMixin
from ..generic.Rules import set_rule


class RLLogic(LogicMixin):
    def _get_upgrade_total(self, player: int) -> int:
        return int(self.multiworld.health_pool[player]) + \
               int(self.multiworld.mana_pool[player]) + \
               int(self.multiworld.attack_pool[player]) + \
               int(self.multiworld.magic_damage_pool[player])

    def _get_upgrade_count(self, player: int) -> int:
        return self.item_count("Health Up", player) + self.item_count("Mana Up", player) + \
               self.item_count("Attack Up", player) + self.item_count("Magic Damage Up", player)

    def has_vendors(self, player: int) -> bool:
        return self.has_all({"Blacksmith", "Enchantress"}, player)

    def has_upgrade_amount(self, player: int, amount: int) -> bool:
        return self._get_upgrade_count(player) >= amount

    def has_upgrades_percentage(self, player: int, percentage: int) -> bool:
        return self.has_upgrade_amount(player, self._get_upgrade_total(player) * (percentage // 100))

    def has_movement_rune(self, player: int) -> bool:
        return self.has("Vault Runes", player) or self.has("Sprint Runes", player) or self.has("Sky Runes", player)

    def has_fairy_progression(self, player: int) -> bool:
        return self.has("Dragons", player) or (self.has("Enchantress", player) and self.has_movement_rune(player))

    def has_defeated_castle(self, player: int) -> bool:
        return self.has("Defeat Khidr", player) or self.has("Defeat Neo Khidr", player)

    def has_defeated_forest(self, player: int) -> bool:
        return self.has("Defeat Alexander", player) or self.has("Defeat Alexander IV", player)

    def has_defeated_tower(self, player: int) -> bool:
        return self.has("Defeat Ponce de Leon", player) or self.has("Defeat Ponce de Freon", player)

    def has_defeated_dungeon(self, player: int) -> bool:
        return self.has("Defeat Herodotus", player) or self.has("Defeat Astrodotus", player)


def set_rules(multiworld: MultiWorld, player: int):
    # If 'vendors' are 'normal', then expect it to show up in the first half(ish) of the spheres.
    if multiworld.vendors[player] == "normal":
        set_rule(multiworld.get_location("Forest Abkhazia Boss Reward", player),
            lambda state: state.has_vendors(player))

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
            set_rule(multiworld.get_location(location, player), lambda state: state.has(event, player))

    # Set rules for fairy chests to decrease headache of expectation to find non-movement fairy chests.
    for fairy_location in [location for location in multiworld.get_locations(player) if "Fairy" in location.name]:
        set_rule(fairy_location, lambda state: state.has_fairy_progression(player))

    # Region rules.
    multiworld.get_entrance("Forest Abkhazia", player).access_rule = \
        lambda state: state.has_upgrades_percentage(player, 12.5) and state.has_defeated_castle(player)

    multiworld.get_entrance("The Maya", player).access_rule = \
        lambda state: state.has_upgrades_percentage(player, 25) and state.has_defeated_forest(player)

    multiworld.get_entrance("Land of Darkness", player).access_rule = \
        lambda state: state.has_upgrades_percentage(player, 37.5) and state.has_defeated_tower(player)

    multiworld.get_entrance("The Fountain Room", player).access_rule = \
        lambda state: state.has_upgrades_percentage(player, 50) and state.has_defeated_dungeon(player)

    # Win condition.
    multiworld.completion_condition[player] = lambda state: state.has("Defeat The Fountain", player)
