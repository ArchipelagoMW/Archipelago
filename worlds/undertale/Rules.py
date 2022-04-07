from ..generic.Rules import set_rule, add_rule
from BaseClasses import MultiWorld
from ..AutoWorld import LogicMixin


class UndertaleLogic(LogicMixin):
    def _is_route(self, player: int, route: int):
        if route == 0:
            return (self.world.route_required[player].current_key == "neutral")
        if route == 1:
            return (self.world.route_required[player].current_key == "pacifist")
        if route == 2:
            return (self.world.route_required[player].current_key == "genocide")
        return False

    def _reached_true_lab(self, player: int):
        return (self.has('Undyne Letter EX', player) and self._is_route(player,1))

    def _has_amount(self, player: int, item: str, total: int):
        return self.item_count(item, player) >= total


# Sets rules on entrances and advancements that are always applied
def set_rules(world: MultiWorld, player: int):
    set_rule(world.get_location(("Dog Sale 1"), player), lambda state: state._is_route(player, 1))
    set_rule(world.get_location(("Cat Sale"), player), lambda state: state._is_route(player, 1))
    set_rule(world.get_location(("Dog Sale 2"), player), lambda state: state._is_route(player, 1))
    set_rule(world.get_location(("Dog Sale 3"), player), lambda state: state._is_route(player, 1))
    set_rule(world.get_location(("Dog Sale 4"), player), lambda state: state._is_route(player, 1))
    set_rule(world.get_location(("Chisps Machine"), player), lambda state: state._reached_true_lab(player))
    set_rule(world.get_location(("Nicecream Snowdin"), player), lambda state: not state._is_route(player, 2))
    set_rule(world.get_location(("Nicecream Waterfall"), player), lambda state: not state._is_route(player, 2))
    set_rule(world.get_location(("Nicecream Punch Card"), player), lambda state: not state._is_route(player, 2))
    set_rule(world.get_location(("Card Reward"), player), lambda state: (not state._is_route(player, 2)) and state._has_amount(player, 'Punch Card', 3))
    set_rule(world.get_location(("Apron Hidden"), player), lambda state: not state._is_route(player, 2))
    set_rule(world.get_location(("Hush Trade"), player), lambda state: not state._is_route(player, 2))
    set_rule(world.get_location(("Letter Quest"), player), lambda state: state._is_route(player, 1))


# Sets rules on completion condition
def set_completion_rules(world: MultiWorld, player: int):
    completion_requirements = lambda state: \
        (state.has('Heart Locket', player) and state.has('Undyne Letter EX', player) and state._is_route(player,1)) or \
        (state.has('Worn Dagger', player) and state._is_route(player,0)) or \
        (state.has('Worn Dagger', player) and state._is_route(player,2))
    world.completion_condition[player] = lambda state: completion_requirements(state)
