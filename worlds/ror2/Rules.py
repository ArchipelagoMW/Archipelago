from BaseClasses import MultiWorld
from ..AutoWorld import LogicMixin
from ..generic.Rules import set_rule


class RiskOfRainLogic(LogicMixin):
    def _ror_has_items(self, player: int, amount: int) -> bool:
        count: int = self.item_count("Common Item", player) + self.item_count("Uncommon Item", player) + \
                     self.item_count("Legendary Item", player) + self.item_count("Boss Item", player) + \
                     self.item_count("Lunar Item", player) + self.item_count("Equipment", player) + \
                     self.item_count("Dio's Best Friend", player) + self.item_count("Item Scrap, White", player) + \
                     self.item_count("Item Scrap, Green", player) + self.item_count("Item Scrap, Red", player) + \
                     self.item_count("Item Scrap, Yellow", player)
        return count >= amount


def set_rules(world: MultiWorld, player: int):
    # divide by 5 since 5 levels (then commencement)
    items_per_level = max(int(world.total_locations[player] / 5 / (world.item_pickup_step[player]+1)), 1)

    # lock item pickup access based on level completion
    for i in range(1, items_per_level):
        set_rule(world.get_location(f"ItemPickup{i}", player), lambda state: True)
    for i in range(items_per_level, 2*items_per_level):
        set_rule(world.get_location(f"ItemPickup{i}", player), lambda state: state.has("Beat Level One", player))
    for i in range(2*items_per_level, 3*items_per_level):
        set_rule(world.get_location(f"ItemPickup{i}", player), lambda state: state.has("Beat Level Two", player))
    for i in range(3*items_per_level, 4*items_per_level):
        set_rule(world.get_location(f"ItemPickup{i}", player), lambda state: state.has("Beat Level Three", player))
    for i in range(4*items_per_level, world.total_locations[player] + 1):
        set_rule(world.get_location(f"ItemPickup{i}", player), lambda state: state.has("Beat Level Four", player))

    # require items to beat each stage
    set_rule(world.get_location("Level Two", player),
             lambda state: state.has("Beat Level One", player) and state._ror_has_items(player, items_per_level))
    set_rule(world.get_location("Level Three", player),
             lambda state: state._ror_has_items(player, 2 * items_per_level) and state.has("Beat Level Two", player))
    set_rule(world.get_location("Level Four", player),
             lambda state: state._ror_has_items(player, 3 * items_per_level) and state.has("Beat Level Three", player))
    set_rule(world.get_location("Level Five", player),
             lambda state: state._ror_has_items(player, 4 * items_per_level) and state.has("Beat Level Four", player))
    set_rule(world.get_location("Victory", player),
             lambda state: state._ror_has_items(player, 5 * items_per_level) and state.has("Beat Level Five", player))

    world.completion_condition[player] = lambda state: state.has("Victory", player)
