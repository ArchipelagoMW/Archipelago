from ..generic.Rules import set_rule, add_rule
from BaseClasses import MultiWorld, CollectionState

# Sets rules on entrances and advancements that are always applied
def set_rules(world: MultiWorld, player: int):
    world.completion_condition[player] = lambda state: \
        state.has("Victory", player)

    # Change the state to something else later to check game progression
    set_rule(world.get_entrance("Defeat Meiling", player), lambda state: True)
    set_rule(world.get_entrance("Defeat Marisa", player), lambda state: True)
    set_rule(world.get_entrance("Defeat Patchouli", player), lambda state: True)
    set_rule(world.get_entrance("Defeat Remilia", player), lambda state: True)
    set_rule(world.get_entrance("Defeat Nitori", player), lambda state: True)
    set_rule(world.get_entrance("Defeat Flandre", player), lambda state: True)