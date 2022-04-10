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

    def _reach_snowdin(self, player: int, plots: int):
        return (self.has('Plot', player, plots+1))

    def _reach_papyrus_date(self, player: int, plots: int):
        return (self._reach_snowdin(player, plots+1))

    def _reach_waterfall(self, player: int, plots: int):
        return (self._reach_snowdin(player, plots+1))

    def _reach_undyne_hangout(self, player: int, plots: int):
        return (self._reach_papyrus_date(player, plots+2) and self._reach_waterfall(player, plots+2))

    def _reach_hotland(self, player: int, plots: int):
        return (self._reach_waterfall(player, plots+1))

    def _reach_cooking_show(self, player: int, plots: int):
        return (self._reach_hotland(player, plots+1))

    def _reach_news_show(self, player: int, plots: int):
        return (self._reach_cooking_show(player, plots+1))

    def _reach_core(self, player: int, plots: int):
        return (self._reach_news_show(player, plots+1))

    def _reach_core_mettaton(self, player: int, plots: int):
        return (self._reach_core(player, plots+1))

    def _reach_new_home(self, player: int, plots: int):
        return (self._reach_core_mettaton(player, plots))

    def _reach_sans(self, player: int, plots: int):
        return (self._reach_new_home(player, plots+1))

    def _reach_true_lab(self, player: int, plots: int):
        return (self._reach_sans(player, plots+3) and self.has('Undyne Letter EX', player))



# Sets rules on entrances and advancements that are always applied
def set_rules(world: MultiWorld, player: int):
    if world.state._is_route(world, player,1):
        set_rule(world.get_location(("Chisps Machine"), player), lambda state: state._reach_true_lab(player, 0))
        set_rule(world.get_location(("Dog Sale 1"), player), lambda state: state._reach_hotland(player, 0))
        set_rule(world.get_location(("Cat Sale"), player), lambda state: state._reach_hotland(player, 0))
        set_rule(world.get_location(("Dog Sale 2"), player), lambda state: state._reach_hotland(player, 0))
        set_rule(world.get_location(("Dog Sale 3"), player), lambda state: state._reach_hotland(player, 0))
        set_rule(world.get_location(("Dog Sale 4"), player), lambda state: state._reach_hotland(player, 0))
        set_rule(world.get_location(("Hush Trade"), player), lambda state: state._reach_hotland(player, 0) and state.has('Hot Dog...?', player, 1))
        set_rule(world.get_location(("Letter Quest"), player), lambda state: state._reach_sans(player, 0))
    if not world.state._is_route(world, player,2):
        set_rule(world.get_location(("Card Reward"), player), lambda state: state.has('Punch Card', player, 3) and state._reach_waterfall(player, 0))
        set_rule(world.get_location(("Nicecream Snowdin"), player), lambda state: state._reach_snowdin(player, 0))
        set_rule(world.get_location(("Nicecream Waterfall"), player), lambda state: state._reach_waterfall(player, 0))
        set_rule(world.get_location(("Nicecream Punch Card"), player), lambda state: state._reach_waterfall(player, 0))
        set_rule(world.get_location(("Apron Hidden"), player), lambda state: state._reach_cooking_show(player, 0))
    set_rule(world.get_location(("Snowman"), player), lambda state: state._reach_snowdin(player, 0))
    set_rule(world.get_location(("Bunny 1"), player), lambda state: state._reach_snowdin(player, 0))
    set_rule(world.get_location(("Bunny 2"), player), lambda state: state._reach_snowdin(player, 0))
    set_rule(world.get_location(("Bunny 3"), player), lambda state: state._reach_snowdin(player, 0))
    set_rule(world.get_location(("Bunny 4"), player), lambda state: state._reach_snowdin(player, 0))
    set_rule(world.get_location(("Astro 1"), player), lambda state: state._reach_waterfall(player, 0))
    set_rule(world.get_location(("Astro 2"), player), lambda state: state._reach_waterfall(player, 0))
    set_rule(world.get_location(("Gerson 1"), player), lambda state: state._reach_waterfall(player, 0))
    set_rule(world.get_location(("Gerson 2"), player), lambda state: state._reach_waterfall(player, 0))
    set_rule(world.get_location(("Gerson 3"), player), lambda state: state._reach_waterfall(player, 0))
    set_rule(world.get_location(("Gerson 4"), player), lambda state: state._reach_waterfall(player, 0))
    set_rule(world.get_location(("Present Knife"), player), lambda state: state._reach_new_home(player, 0))
    set_rule(world.get_location(("Present Locket"), player), lambda state: state._reach_new_home(player, 0))
    set_rule(world.get_location(("Trash Burger"), player), lambda state: state._reach_waterfall(player, 0))
    set_rule(world.get_location(("Quiche Bench"), player), lambda state: state._reach_waterfall(player, 0))
    set_rule(world.get_location(("Tutu Hidden"), player), lambda state: state._reach_waterfall(player, 0))
    set_rule(world.get_location(("Grass Shoes"), player), lambda state: state._reach_waterfall(player, 0))
    set_rule(world.get_location(("TemmieShop 1"), player), lambda state: state._reach_waterfall(player, 0))
    set_rule(world.get_location(("TemmieShop 2"), player), lambda state: state._reach_waterfall(player, 0))
    set_rule(world.get_location(("TemmieShop 3"), player), lambda state: state._reach_waterfall(player, 0))
    set_rule(world.get_location(("TemmieShop 4"), player), lambda state: state._reach_waterfall(player, 0))
    set_rule(world.get_location(("Noodles Fridge"), player), lambda state: state._reach_hotland(player, 0))
    set_rule(world.get_location(("Pan Hidden"), player), lambda state: state._reach_hotland(player, 0))
    set_rule(world.get_location(("Bratty Catty 1"), player), lambda state: state._reach_hotland(player, 0))
    set_rule(world.get_location(("Bratty Catty 2"), player), lambda state: state._reach_hotland(player, 0))
    set_rule(world.get_location(("Bratty Catty 3"), player), lambda state: state._reach_hotland(player, 0))
    set_rule(world.get_location(("Bratty Catty 4"), player), lambda state: state._reach_hotland(player, 0))
    set_rule(world.get_location(("Burgerpants 1"), player), lambda state: state._reach_hotland(player, 0))
    set_rule(world.get_location(("Burgerpants 2"), player), lambda state: state._reach_hotland(player, 0))
    set_rule(world.get_location(("Burgerpants 3"), player), lambda state: state._reach_hotland(player, 0))
    set_rule(world.get_location(("Burgerpants 4"), player), lambda state: state._reach_hotland(player, 0))


# Sets rules on completion condition
def set_completion_rules(world: MultiWorld, player: int):
    completion_requirements = lambda state: True
    if not world.state._is_route(world, player, 1):
        completion_requirements = lambda state: state._reach_sans(player, 0)
    if world.state._is_route(world, player, 1):
        completion_requirements = lambda state: state._reach_true_lab(player, 0)

    world.completion_condition[player] = lambda state: completion_requirements(state)
