from BaseClasses import MultiWorld
from ..AutoWorld import LogicMixin
from ..generic.Rules import set_rule


class RiskOfRainLogic(LogicMixin):
    def _ror_has_items(self, player: int, amount: int) -> bool:
        count: int = self.item_count("Common Item", player) + self.item_count("Uncommon Item", player) + \
                     self.item_count("Legendary Item", player) + self.item_count("Boss Item", player) + \
                     self.item_count("Lunar Item", player) + self.item_count("Equipment", player)
        return count >= amount


def set_rules(world: MultiWorld, player: int):
    total_checks = world.total_locations[player]
    # divide by 5 since 5 levels (then commencement)
    items_per_level = total_checks / 5
    leftover = total_checks % 5

    set_rule(world.get_location("Level One", player),
             lambda state: state._ror_has_items(player, items_per_level + leftover))
    set_rule(world.get_location("Level Two", player),
             lambda state: state._ror_has_items(player, items_per_level) and state.has("Beat Level One", player))
    set_rule(world.get_location("Level Three", player),
             lambda state: state._ror_has_items(player, items_per_level) and state.has("Beat Level Two", player))
    set_rule(world.get_location("Level Four", player),
             lambda state: state._ror_has_items(player, items_per_level) and state.has("Beat Level Three", player))
    set_rule(world.get_location("Level Five", player),
             lambda state: state._ror_has_items(player, items_per_level) and state.has("Beat Level Four", player))
    set_rule(world.get_location("Victory", player),
             lambda state: state._ror_has_items(player, items_per_level) and state.has("Beat Level Five", player))

    world.completion_condition[player] = lambda state: state.has("Victory", player)