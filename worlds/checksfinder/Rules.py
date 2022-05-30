from ..generic.Rules import set_rule, add_rule
from BaseClasses import MultiWorld
from ..AutoWorld import LogicMixin


class ChecksFinderLogic(LogicMixin):

    def _has_total(self, player: int, total: int):
        return (self.item_count('Map Width', player)+self.item_count('Map Height', player)+
                self.item_count('Map Bombs', player)) >= total


# Sets rules on entrances and advancements that are always applied
def set_rules(world: MultiWorld, player: int):
    set_rule(world.get_location(("Tile 6"), player), lambda state: state._has_total(player, 1))
    set_rule(world.get_location(("Tile 7"), player), lambda state: state._has_total(player, 2))
    set_rule(world.get_location(("Tile 8"), player), lambda state: state._has_total(player, 3))
    set_rule(world.get_location(("Tile 9"), player), lambda state: state._has_total(player, 4))
    set_rule(world.get_location(("Tile 10"), player), lambda state: state._has_total(player, 5))
    set_rule(world.get_location(("Tile 11"), player), lambda state: state._has_total(player, 6))
    set_rule(world.get_location(("Tile 12"), player), lambda state: state._has_total(player, 7))
    set_rule(world.get_location(("Tile 13"), player), lambda state: state._has_total(player, 8))
    set_rule(world.get_location(("Tile 14"), player), lambda state: state._has_total(player, 9))
    set_rule(world.get_location(("Tile 15"), player), lambda state: state._has_total(player, 10))
    set_rule(world.get_location(("Tile 16"), player), lambda state: state._has_total(player, 11))
    set_rule(world.get_location(("Tile 17"), player), lambda state: state._has_total(player, 12))
    set_rule(world.get_location(("Tile 18"), player), lambda state: state._has_total(player, 13))
    set_rule(world.get_location(("Tile 19"), player), lambda state: state._has_total(player, 14))
    set_rule(world.get_location(("Tile 20"), player), lambda state: state._has_total(player, 15))
    set_rule(world.get_location(("Tile 21"), player), lambda state: state._has_total(player, 16))
    set_rule(world.get_location(("Tile 22"), player), lambda state: state._has_total(player, 17))
    set_rule(world.get_location(("Tile 23"), player), lambda state: state._has_total(player, 18))
    set_rule(world.get_location(("Tile 24"), player), lambda state: state._has_total(player, 19))
    set_rule(world.get_location(("Tile 25"), player), lambda state: state._has_total(player, 20))


# Sets rules on completion condition
def set_completion_rules(world: MultiWorld, player: int):

    width_req = 10-5
    height_req = 10-5
    bomb_req = 20-5
    completion_requirements = lambda state: \
        state.has("Map Width", player, width_req) and \
        state.has("Map Height", player, height_req) and \
        state.has("Map Bombs", player, bomb_req)
    world.completion_condition[player] = lambda state: completion_requirements(state)
