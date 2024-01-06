from BaseClasses import MultiWorld
from ..generic.Rules import set_rule


def set_rules(world: MultiWorld, player: int):
    for i in range(16, 31):
        set_rule(
            world.get_location(f"IDLE item number {i}", player),
            lambda state: state.prog_items[player].total() >= 4
        )

    for i in range(31, 51):
        set_rule(
            world.get_location(f"IDLE item number {i}", player),
            lambda state: state.prog_items[player].total() >= 10
        )

    for i in range(51, 101):
        set_rule(
            world.get_location(f"IDLE item number {i}", player),
            lambda state: state.prog_items[player].total() >= 20
        )

    for i in range(101, 201):
        set_rule(
            world.get_location(f"IDLE item number {i}", player),
            lambda state: state.prog_items[player].total() >= 40
        )

    world.completion_condition[player] =\
        lambda state:\
        state.can_reach(world.get_location("IDLE item number 200", player), "Location", player)
