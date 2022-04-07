from ..generic.Rules import set_rule, add_rule
from BaseClasses import MultiWorld
from ..AutoWorld import LogicMixin


class UndertaleLogic(LogicMixin):
    def _is_route(self, world: MultiWorld, player: int, route: int):
        if route == 0:
            return (world.route_required[player].current_key == "neutral")
        if route == 1:
            return (world.route_required[player].current_key == "pacifist")
        if route == 2:
            return (world.route_required[player].current_key == "genocide")
        return False

    def _reached_true_lab(self, player: int):
        return (self.has('Undyne Letter EX', player))


# Sets rules on entrances and advancements that are always applied
def set_rules(world: MultiWorld, player: int):
    if world.state._is_route(world, player,1):
        set_rule(world.get_location(("Chisps Machine"), player), lambda state: state._reached_true_lab(world, player))
    if not world.state._is_route(world, player,2):
        set_rule(world.get_location(("Card Reward"), player), lambda state: state.has('Punch Card', player, 3))


# Sets rules on completion condition
def set_completion_rules(world: MultiWorld, player: int):
    completion_requirements = lambda state: True
    if not world.state._is_route(world, player, 1):
        completion_requirements = lambda state: state.has('Worn Dagger', player)
    if world.state._is_route(world, player, 1):
        completion_requirements = lambda state: state.has('Heart Locket', player) and state.has('Undyne Letter EX', player)

    world.completion_condition[player] = lambda state: completion_requirements(state)
