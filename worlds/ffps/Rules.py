from ..generic.Rules import set_rule, add_rule
from BaseClasses import MultiWorld
from ..AutoWorld import LogicMixin


# Sets rules on entrances and advancements that are always applied
def set_rules(world: MultiWorld, player: int):
    set_rule(world.get_location(("Salvage ScrapTrap"), player), lambda state: True)
    set_rule(world.get_location(("Salvage Scrap Baby"), player), lambda state: True)
    set_rule(world.get_location(("Salvage Lefty"), player), lambda state: True)
    set_rule(world.get_location(("Salvage Molten Freddy"), player), lambda state: True)


# Sets rules on completion condition
def set_completion_rules(world: MultiWorld, player: int):
    completion_requirements = lambda state: \
        state.has("ScrapTrap", player) and \
        state.has("Scrap Baby", player) and \
        state.has("Lefty", player) and \
        state.has("Molten Freddy", player)
    world.completion_condition[player] = lambda state: completion_requirements(state)
