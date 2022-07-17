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

    def _reach_snowdin(self, player: int, world: MultiWorld):
        return (self.has("Goat Plush", player) or
                self.has("Progressive Plot",player,1))

    def _reach_papyrus_date(self, player: int, world: MultiWorld):
        return (self._reach_snowdin(player, world) and (self.has("Complete Skeleton", player) or
                                                                                (self.has("Progressive Plot",player,2) and self._is_route(world,player,1))))

    def _reach_waterfall(self, player: int, world: MultiWorld):
        return (self._reach_snowdin(player, world) and (self.has("Snow Shovel", player) or
                                                        (self.has("Progressive Plot",player,2) and not self._is_route(world,player,1)) or
                                                        (self.has("Progressive Plot",player,3) and self._is_route(world,player,1))))

    def _reach_undyne_hangout(self, player: int, world: MultiWorld):
        return (self._reach_papyrus_date(player, world) and self._reach_waterfall(player, world) and (self.has("Fish", player) or
                                                                                               (self.has("Progressive Plot",player,4) and self._is_route(world,player,1))))

    def _reach_hotland(self, player: int, world: MultiWorld):
        return (self._reach_waterfall(player, world) and (self.has("Heat Suit", player) or
                                                          (self.has("Progressive Plot",player,3) and not self._is_route(world,player,1)) or
                                                          (self.has("Progressive Plot",player,5) and self._is_route(world,player,1))))

    def _reach_cooking_show(self, player: int, world: MultiWorld):
        return (self._reach_hotland(player, world) and (self.has("Cooking Set", player) or
                                                        (self.has("Progressive Plot",player,3) and self._is_route(world,player,2)) or
                                                        (self.has("Progressive Plot",player,4) and self._is_route(world,player,0)) or
                                                        (self.has("Progressive Plot",player,6) and self._is_route(world,player,1))))

    def _reach_news_show(self, player: int, world: MultiWorld):
        return (self._reach_cooking_show(player, world) and (self.has("Microphone", player) or
                                                             (self.has("Progressive Plot",player,3) and self._is_route(world,player,2)) or
                                                             (self.has("Progressive Plot",player,5) and self._is_route(world,player,0)) or
                                                             (self.has("Progressive Plot",player,7) and self._is_route(world,player,1))))

    def _reach_core(self, player: int, world: MultiWorld):
        return (self._reach_news_show(player, world) and (self.has("Bridge Tools", player) or
                                                          (self.has("Progressive Plot",player,4) and self._is_route(world,player,2)) or
                                                          (self.has("Progressive Plot",player,6) and self._is_route(world,player,0)) or
                                                          (self.has("Progressive Plot",player,8) and self._is_route(world,player,1))))

    def _reach_core_mettaton(self, player: int, world: MultiWorld):
        return (self._reach_core(player, world) and (self.has("Mettaton Plush", player) or
                                                          (self.has("Progressive Plot",player,5) and self._is_route(world,player,2)) or
                                                          (self.has("Progressive Plot",player,7) and self._is_route(world,player,0)) or
                                                          (self.has("Progressive Plot",player,9) and self._is_route(world,player,1))))

    def _reach_new_home(self, player: int, world: MultiWorld):
        return (self._reach_core_mettaton(player, world))

    def _reach_sans(self, player: int, world: MultiWorld):
        return (self._reach_new_home(player, world) and (self.has("Determination", player) or self.has("Soul Piece", player, self.world.soul_pieces[player])))

    def _reach_true_lab(self, player: int, world: MultiWorld):
        return (self._reach_undyne_hangout(player, world) and self._reach_sans(player, world) and self.has('Undyne Letter EX', player) and (self.has("DT Extractor", player) or
                                                                                               (self.has("Progressive Plot",player,10) and self._is_route(world,player,1))))



# Sets rules on entrances and advancements that are always applied
def set_rules(world: MultiWorld, player: int):
    if world.state._is_route(world, player,1):
        set_rule(world.get_location(("Papyrus Plot"), player), lambda state: state._reach_snowdin(player, world))
        set_rule(world.get_location(("Undyne Plot"), player), lambda state: state._reach_waterfall(player, world))
        set_rule(world.get_location(("True Lab Plot"), player), lambda state: state._reach_new_home(player, world))
        set_rule(world.get_location(("Chisps Machine"), player), lambda state: state._reach_true_lab(player, world))
        set_rule(world.get_location(("Dog Sale 1"), player), lambda state: state._reach_cooking_show(player, world))
        set_rule(world.get_location(("Cat Sale"), player), lambda state: state._reach_cooking_show(player, world))
        set_rule(world.get_location(("Dog Sale 2"), player), lambda state: state._reach_cooking_show(player, world))
        set_rule(world.get_location(("Dog Sale 3"), player), lambda state: state._reach_cooking_show(player, world))
        set_rule(world.get_location(("Dog Sale 4"), player), lambda state: state._reach_cooking_show(player, world))
        set_rule(world.get_location(("Hush Trade"), player), lambda state: state._reach_news_show(player, world) and state.has('Hot Dog...?', player, 1))
        set_rule(world.get_location(("Letter Quest"), player), lambda state: state._reach_sans(player, world))
    if not world.state._is_route(world, player,2):
        set_rule(world.get_location(("Card Reward"), player), lambda state: state.has('Punch Card', player, 3) and state._reach_waterfall(player, world))
        set_rule(world.get_location(("Nicecream Snowdin"), player), lambda state: state._reach_snowdin(player, world))
        set_rule(world.get_location(("Nicecream Waterfall"), player), lambda state: state._reach_waterfall(player, world))
        set_rule(world.get_location(("Nicecream Punch Card"), player), lambda state: state._reach_waterfall(player, world))
        set_rule(world.get_location(("Apron Hidden"), player), lambda state: state._reach_cooking_show(player, world))
        set_rule(world.get_location(("Cooking Show Plot"), player), lambda state: state._reach_cooking_show(player, world))
        set_rule(world.get_location(("TV Show Plot"), player), lambda state: state._reach_news_show(player, world))
    if world.state._is_route(world,player,2) and world.rando_love[player]:
        set_rule(world.get_location(("LOVE 6"), player), lambda state: state._reach_snowdin(player, world))
        set_rule(world.get_location(("LOVE 7"), player), lambda state: state._reach_snowdin(player, world))
        set_rule(world.get_location(("LOVE 8"), player), lambda state: state._reach_snowdin(player, world))
        set_rule(world.get_location(("LOVE 9"), player), lambda state: state._reach_waterfall(player, world))
        set_rule(world.get_location(("LOVE 10"), player), lambda state: state._reach_waterfall(player, world))
        set_rule(world.get_location(("LOVE 11"), player), lambda state: state._reach_waterfall(player, world))
        set_rule(world.get_location(("LOVE 12"), player), lambda state: state._reach_hotland(player, world))
        set_rule(world.get_location(("LOVE 13"), player), lambda state: state._reach_hotland(player, world))
        set_rule(world.get_location(("LOVE 14"), player), lambda state: state._reach_hotland(player, world))
        set_rule(world.get_location(("LOVE 15"), player), lambda state: state._reach_core_mettaton(player, world))
        set_rule(world.get_location(("LOVE 16"), player), lambda state: state._reach_core_mettaton(player, world))
        set_rule(world.get_location(("LOVE 17"), player), lambda state: state._reach_core_mettaton(player, world))
        set_rule(world.get_location(("LOVE 18"), player), lambda state: state._reach_core_mettaton(player, world))
        set_rule(world.get_location(("LOVE 19"), player), lambda state: state._reach_core_mettaton(player, world))
        set_rule(world.get_location(("LOVE 20"), player), lambda state: state._reach_sans(player, world))
    set_rule(world.get_location(("Snowman"), player), lambda state: state._reach_snowdin(player, world))
    set_rule(world.get_location(("Waterfall Plot"), player), lambda state: state._reach_snowdin(player, world))
    set_rule(world.get_location(("Hotland Plot"), player), lambda state: state._reach_waterfall(player, world))
    set_rule(world.get_location(("Core Plot"), player), lambda state: state._reach_news_show(player, world))
    set_rule(world.get_location(("Mettaton Plot"), player), lambda state: state._reach_core_mettaton(player, world))
    set_rule(world.get_location(("Bunny 1"), player), lambda state: state._reach_snowdin(player, world))
    set_rule(world.get_location(("Bunny 2"), player), lambda state: state._reach_snowdin(player, world))
    set_rule(world.get_location(("Bunny 3"), player), lambda state: state._reach_snowdin(player, world))
    set_rule(world.get_location(("Bunny 4"), player), lambda state: state._reach_snowdin(player, world))
    set_rule(world.get_location(("Astro 1"), player), lambda state: state._reach_waterfall(player, world))
    set_rule(world.get_location(("Astro 2"), player), lambda state: state._reach_waterfall(player, world))
    set_rule(world.get_location(("Gerson 1"), player), lambda state: state._reach_waterfall(player, world))
    set_rule(world.get_location(("Gerson 2"), player), lambda state: state._reach_waterfall(player, world))
    set_rule(world.get_location(("Gerson 3"), player), lambda state: state._reach_waterfall(player, world))
    set_rule(world.get_location(("Gerson 4"), player), lambda state: state._reach_waterfall(player, world))
    set_rule(world.get_location(("Present Knife"), player), lambda state: state._reach_new_home(player, world))
    set_rule(world.get_location(("Present Locket"), player), lambda state: state._reach_new_home(player, world))
    set_rule(world.get_location(("Trash Burger"), player), lambda state: state._reach_core(player, world))
    set_rule(world.get_location(("Quiche Bench"), player), lambda state: state._reach_waterfall(player, world))
    set_rule(world.get_location(("Tutu Hidden"), player), lambda state: state._reach_waterfall(player, world))
    set_rule(world.get_location(("Grass Shoes"), player), lambda state: state._reach_waterfall(player, world))
    set_rule(world.get_location(("TemmieShop 1"), player), lambda state: state._reach_waterfall(player, world))
    set_rule(world.get_location(("TemmieShop 2"), player), lambda state: state._reach_waterfall(player, world))
    set_rule(world.get_location(("TemmieShop 3"), player), lambda state: state._reach_waterfall(player, world))
    set_rule(world.get_location(("TemmieShop 4"), player), lambda state: state._reach_waterfall(player, world))
    set_rule(world.get_location(("Noodles Fridge"), player), lambda state: state._reach_hotland(player, world))
    set_rule(world.get_location(("Pan Hidden"), player), lambda state: state._reach_hotland(player, world))
    set_rule(world.get_location(("Bratty Catty 1"), player), lambda state: state._reach_news_show(player, world))
    set_rule(world.get_location(("Bratty Catty 2"), player), lambda state: state._reach_news_show(player, world))
    set_rule(world.get_location(("Bratty Catty 3"), player), lambda state: state._reach_news_show(player, world))
    set_rule(world.get_location(("Bratty Catty 4"), player), lambda state: state._reach_news_show(player, world))
    set_rule(world.get_location(("Burgerpants 1"), player), lambda state: state._reach_news_show(player, world))
    set_rule(world.get_location(("Burgerpants 2"), player), lambda state: state._reach_news_show(player, world))
    set_rule(world.get_location(("Burgerpants 3"), player), lambda state: state._reach_news_show(player, world))
    set_rule(world.get_location(("Burgerpants 4"), player), lambda state: state._reach_news_show(player, world))


# Sets rules on completion condition
def set_completion_rules(world: MultiWorld, player: int):
    completion_requirements = lambda state: True
    if not world.state._is_route(world, player, 1):
        completion_requirements = lambda state: state._reach_sans(player, world)
    if world.state._is_route(world, player, 1):
        completion_requirements = lambda state: state._reach_true_lab(player, world)

    world.completion_condition[player] = lambda state: completion_requirements(state)
