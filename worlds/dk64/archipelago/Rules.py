"""Rules for Archipelago."""

from BaseClasses import MultiWorld
from worlds.AutoWorld import LogicMixin
from worlds.generic.Rules import add_rule, set_rule


def set_rules(world: MultiWorld, player: int):
    """Set the rules for the given player's world."""
    # DK64_TODO: Get location access rules from DK64R

    world.completion_condition[player] = lambda state: state.has("Banana Hoard", player)
