from BaseClasses import MultiWorld
from ..AutoWorld import LogicMixin
from ..generic.Rules import set_rule


class LegacyLogic(LogicMixin):
    def _legacy_has_any_vendors(self, player: int) -> bool:
        return self.item_count("Blacksmith", player) > 0 or self.item_count("Enchantress", player) > 0

    def _legacy_has_all_vendors(self, player: int) -> bool:
        return self.item_count("Blacksmith", player) > 0 and self.item_count("Enchantress", player) > 0

    def _legacy_has_stat_upgrades(self, player: int, amount: int) -> bool:
        count: int = self.item_count("Health Up", player) + self.item_count("Mana Up", player) + \
                     self.item_count("Attack Up", player) + self.item_count("Magic Damage Up", player) + \
                     self.item_count("Armor Up", player) + self.item_count("Equip Up", player)
        return count >= amount


def set_rules(world: MultiWorld, player: int):
    # Chests
    for i in range(0, world.chests_per_zone[player]):
        set_rule(world.get_location(f"Castle Hamson Chest {i + 1}", player),
                 lambda state: True)

        set_rule(world.get_location(f"Forest Abkhazia Chest {i + 1}", player),
                 lambda state: state.has("Defeated Khindr", player))

        set_rule(world.get_location(f"The Maya Chest {i + 1}", player),
                 lambda state: state.has("Defeated Alexander", player))

        set_rule(world.get_location(f"The Land of Darkness Chest {i + 1}", player),
                 lambda state: state.has("Defeated Ponce de Leon", player))

    # Fairy Chests
    for i in range(0, world.fairy_chests_per_zone[player]):
        set_rule(world.get_location(f"Castle Hamson Fairy Chest {i + 1}", player),
                 lambda state: True)

        set_rule(world.get_location(f"Forest Abkhazia Fairy Chest {i + 1}", player),
                 lambda state: state.has("Defeated Khindr", player))

        set_rule(world.get_location(f"The Maya Fairy Chest {i + 1}", player),
                 lambda state: state.has("Defeated Alexander", player))

        set_rule(world.get_location(f"The Land of Darkness Fairy Chest {i + 1}", player),
                 lambda state: state.has("Defeated Ponce de Leon", player))

    # Vendors
    if world.vendors[player] == "early":
        set_rule(world.get_location("Castle Hamson", player), lambda state: state._legacy_has_all_vendors(player))
    elif world.vendors[player] == "normal":
        set_rule(world.get_location("Forest Abkhazia", player), lambda state: state._legacy_has_any_vendors(player))
    elif world.vendors[player] == "anywhere":
        pass  # it can be anywhere, so no rule for this!

    # Scale Diary Entries
    for i in range(0, 5):
        set_rule(world.get_location(f"Diary {i + 1}", player), lambda state: True)
        set_rule(world.get_location(f"Diary {i + 6}", player), lambda state: state.has("Defeated Khindr", player))
        set_rule(world.get_location(f"Diary {i + 11}", player), lambda state: state.has("Defeated Alexander", player))
        set_rule(world.get_location(f"Diary {i + 16}", player), lambda state: state.has("Defeated Ponce de Leon", player))
        set_rule(world.get_location(f"Diary {i + 21}", player), lambda state: state.has("Defeated Herodotus", player))

    # Scale each manor location.
        set_rule(world.get_location(f"Manor Ground Road", player), lambda state: True)
        set_rule(world.get_location(f"Manor Main Base", player), lambda state: True)
        set_rule(world.get_location(f"Manor Main Bottom Window", player), lambda state: True)
        set_rule(world.get_location(f"Manor Main Top Window", player), lambda state: True)
        set_rule(world.get_location(f"Manor Main Roof", player), lambda state: True)
        set_rule(world.get_location(f"Manor Left Wing Base", player), lambda state: True)
        set_rule(world.get_location(f"Manor Right Wing Base", player), lambda state: True)

        set_rule(world.get_location(f"Manor Left Wing Window", player), lambda state: state.has("Defeated Khindr", player))
        set_rule(world.get_location(f"Manor Left Wing Roof", player), lambda state: state.has("Defeated Khindr", player))
        set_rule(world.get_location(f"Manor Right Wing Window", player), lambda state: state.has("Defeated Khindr", player))
        set_rule(world.get_location(f"Manor Right Wing Roof", player), lambda state: state.has("Defeated Khindr", player))
        set_rule(world.get_location(f"Manor Left Big Base", player), lambda state: state.has("Defeated Khindr", player))
        set_rule(world.get_location(f"Manor Right Big Base", player), lambda state: state.has("Defeated Khindr", player))
        set_rule(world.get_location(f"Manor Left Tree 1", player), lambda state: state.has("Defeated Khindr", player))
        set_rule(world.get_location(f"Manor Left Tree 2", player), lambda state: state.has("Defeated Khindr", player))
        set_rule(world.get_location(f"Manor Right Tree", player), lambda state: state.has("Defeated Khindr", player))

        set_rule(world.get_location(f"Manor Left Big Upper 1", player), lambda state: state.has("Defeated Alexander", player))
        set_rule(world.get_location(f"Manor Left Big Upper 2", player), lambda state: state.has("Defeated Alexander", player))
        set_rule(world.get_location(f"Manor Left Big Windows", player), lambda state: state.has("Defeated Alexander", player))
        set_rule(world.get_location(f"Manor Left Big Roof", player), lambda state: state.has("Defeated Alexander", player))
        set_rule(world.get_location(f"Manor Left Far Base", player), lambda state: state.has("Defeated Alexander", player))
        set_rule(world.get_location(f"Manor Left Far Roof", player), lambda state: state.has("Defeated Alexander", player))
        set_rule(world.get_location(f"Manor Left Extension", player), lambda state: state.has("Defeated Alexander", player))
        set_rule(world.get_location(f"Manor Right Big Upper", player), lambda state: state.has("Defeated Alexander", player))
        set_rule(world.get_location(f"Manor Right Big Roof", player), lambda state: state.has("Defeated Alexander", player))
        set_rule(world.get_location(f"Manor Right Extension", player), lambda state: state.has("Defeated Alexander", player))

        set_rule(world.get_location(f"Manor Right High Base", player), lambda state: state.has("Defeated Ponce de Leon", player))
        set_rule(world.get_location(f"Manor Right High Upper", player), lambda state: state.has("Defeated Ponce de Leon", player))
        set_rule(world.get_location(f"Manor Right High Tower", player), lambda state: state.has("Defeated Ponce de Leon", player))
        set_rule(world.get_location(f"Manor Observatory Base", player), lambda state: state.has("Defeated Ponce de Leon", player))
        set_rule(world.get_location(f"Manor Observatory Telescope", player), lambda state: state.has("Defeated Ponce de Leon", player))

    # Standard Zone Progression
    set_rule(world.get_location("Khindr's Reward Chest", player), lambda state: state.has("Defeated Khindr", player))
    set_rule(world.get_location("Forest Abkhazia", player), lambda state: state._legacy_has_stat_upgrades(player, 10) and state.has("Defeated Khindr", player))
    set_rule(world.get_location("Alexander's Reward Chest", player), lambda state: state.has("Defeated Alexander", player))
    set_rule(world.get_location("The Maya", player), lambda state: state._legacy_has_stat_upgrades(player, 25) and state.has("Defeated Alexander", player))
    set_rule(world.get_location("Ponce de Leon's Reward Chest", player), lambda state: state.has("Defeated Ponce de Leon", player))
    set_rule(world.get_location("The Land of Darkness", player), lambda state: state._legacy_has_stat_upgrades(player, 40) and state.has("Defeated Ponce de Leon", player))
    set_rule(world.get_location("Herodotus's Reward Chest", player), lambda state: state.has("Defeated Herodotus", player))
    set_rule(world.get_location("Victory", player), lambda state: state._legacy_has_stat_upgrades(player, 55) and state.has("Defeated Herodotus", player))

    world.completion_condition[player] = lambda state: state.has("Victory", player)
