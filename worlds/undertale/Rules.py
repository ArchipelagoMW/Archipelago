from ..generic.Rules import set_rule, add_rule
from BaseClasses import MultiWorld
from ..AutoWorld import LogicMixin


class UndertaleLogic(LogicMixin):
    def _prev_area(self, player: int, world: MultiWorld, area: int):
        if area == 1:
            return world.get_region("Snowdin Forest", player).entrances[0].parent_region.name
        elif area == 2:
            return world.get_region("Waterfall", player).entrances[0].parent_region.name
        elif area == 3:
            return world.get_region("Hotland", player).entrances[0].parent_region.name
        elif area == 4:
            return world.get_region("Core", player).entrances[0].parent_region.name

    def _is_route(self, world: MultiWorld, player: int, route: int):
        if route == 3:
            return (world.route_required[player].current_key == "all_routes")
        if world.route_required[player].current_key == "all_routes":
            return True
        if route == 0:
            return (world.route_required[player].current_key == "neutral")
        if route == 1:
            return (world.route_required[player].current_key == "pacifist")
        if route == 2:
            return (world.route_required[player].current_key == "genocide")
        return False

    def _has_plot(self, player: int, world: MultiWorld, item: str):
        if item == "Goat Plush":
            return (self.has("Goat Plush", player) or self.has("Progressive Plot",player,1))
        elif item == "Complete Skeleton":
            return (self.has("Complete Skeleton", player) or (self.has("Progressive Plot",player,2) and self._is_route(world,player,1)))
        elif item == "Snow Shovel":
            return (self.has("Snow Shovel", player) or (self.has("Progressive Plot",player,2) and not self._is_route(world,player,1)) or
                    (self.has("Progressive Plot",player,3) and self._is_route(world,player,1)))
        elif item == "Fish":
            return (self.has("Fish", player) or (self.has("Progressive Plot",player,4) and self._is_route(world,player,1)))
        elif item == "Heat Suit":
            return (self.has("Heat Suit", player) or (self.has("Progressive Plot",player,3) and not self._is_route(world,player,1)) or
                    (self.has("Progressive Plot",player,5) and self._is_route(world,player,1)))
        elif item == "Cooking Set":
            return ((self.has("Cooking Set", player) or self._is_route(world,player,2)) or (self.has("Progressive Plot",player,3) and self._is_route(world,player,2)) or
                    (self.has("Progressive Plot",player,4) and self._is_route(world,player,0)) or (self.has("Progressive Plot",player,6) and self._is_route(world,player,1)))
        elif item == "Microphone":
            return ((self.has("Microphone", player) or self._is_route(world,player,2)) or (self.has("Progressive Plot",player,3) and self._is_route(world,player,2)) or
                    (self.has("Progressive Plot",player,5) and self._is_route(world,player,0)) or (self.has("Progressive Plot",player,7) and self._is_route(world,player,1)))
        elif item == "Bridge Tools":
            return ((self.has("Bridge Tools", player)) or (self.has("Progressive Plot",player,4) and self._is_route(world,player,2)) or
                    (self.has("Progressive Plot",player,6) and self._is_route(world,player,0)) or (self.has("Progressive Plot",player,8) and self._is_route(world,player,1)))
        elif item == "Mettaton Plush":
            return (self.has("Mettaton Plush", player) or (self.has("Progressive Plot",player,5) and self._is_route(world,player,2)) or
                    (self.has("Progressive Plot",player,7) and self._is_route(world,player,0)) or (self.has("Progressive Plot",player,9) and self._is_route(world,player,1)))
        elif item == "DT Extractor":
            return ((self.has('DT Extractor', player) or self.has("Progressive Plot",player,10)) and self._is_route(world,player,1))

    def _reach_snowdin(self, player: int, world: MultiWorld):
        if self._prev_area(player,world,1) == "Old Home":
            return (self._has_plot(player, world, "Goat Plush"))
        elif self._prev_area(player,world,1) == "Waterfall":
            return (self._reach_waterfall(player, world) and self._has_plot(player, world, "Heat Suit"))
        elif self._prev_area(player,world,1) == "Hotland":
            return (self._reach_news_show(player, world) and self._has_plot(player, world, "Bridge Tools"))

    def _reach_papyrus_date(self, player: int, world: MultiWorld):
        return (self._reach_snowdin(player, world) and self._has_plot(player, world, "Complete Skeleton"))

    def _reach_waterfall(self, player: int, world: MultiWorld):
        if self._prev_area(player,world,2) == "Old Home":
            return (self._has_plot(player, world, "Goat Plush"))
        elif self._prev_area(player,world,2) == "Snowdin Town":
            return (self._reach_snowdin(player, world) and self._has_plot(player, world, "Snow Shovel"))
        elif self._prev_area(player,world,2) == "Hotland":
            return (self._reach_news_show(player, world) and self._has_plot(player, world, "Bridge Tools"))

    def _reach_undyne_hangout(self, player: int, world: MultiWorld):
        return (self._reach_papyrus_date(player, world) and self._reach_waterfall(player, world) and self._has_plot(player, world, "Fish"))

    def _reach_hotland(self, player: int, world: MultiWorld):
        if self._prev_area(player,world,3) == "Old Home":
            return (self._has_plot(player, world, "Goat Plush"))
        elif self._prev_area(player,world,3) == "Snowdin Town":
            return (self._reach_snowdin(player, world) and self._has_plot(player, world, "Snow Shovel"))
        elif self._prev_area(player,world,3) == "Waterfall":
            return (self._reach_waterfall(player, world) and self._has_plot(player, world, "Heat Suit"))

    def _reach_cooking_show(self, player: int, world: MultiWorld):
        return (self._reach_hotland(player, world) and self._has_plot(player, world, "Cooking Set"))

    def _reach_news_show(self, player: int, world: MultiWorld):
        return (self._reach_cooking_show(player, world) and self._has_plot(player, world, "Microphone"))

    def _reach_core(self, player: int, world: MultiWorld):
        if self._prev_area(player,world,4) == "Hotland":
            return (self._reach_news_show(player, world) and self._has_plot(player, world, "Bridge Tools"))
        elif self._prev_area(player,world,4) == "Snowdin Town":
            return (self._reach_snowdin(player, world) and self._has_plot(player, world, "Snow Shovel"))
        elif self._prev_area(player,world,4) == "Waterfall":
            return (self._reach_waterfall(player, world) and self._has_plot(player, world, "Heat Suit"))

    def _reach_core_mettaton(self, player: int, world: MultiWorld):
        return (self._reach_core(player, world) and self._has_plot(player, world, "Mettaton Plush"))

    def _reach_new_home(self, player: int, world: MultiWorld):
        return (self._reach_core_mettaton(player, world))

    def _reach_sans(self, player: int, world: MultiWorld):
        return (self._reach_new_home(player, world) and (self.has("Determination", player) or self.has("Soul Piece", player, self.world.soul_pieces[player])))

    def _reach_true_lab(self, player: int, world: MultiWorld):
        return (self._reach_undyne_hangout(player, world) and self._reach_sans(player, world) and self.has('Undyne Letter EX', player) and self._has_plot(player, world, "DT Extractor"))


def can_level(exp: int, lvl: int):
    if (exp >= 10 and lvl == 1):
        return True
    elif (exp >= 30 and lvl == 2):
        return True
    elif (exp >= 70 and lvl == 3):
        return True
    elif (exp >= 120 and lvl == 4):
        return True
    elif (exp >= 200 and lvl == 5):
        return True
    elif (exp >= 300 and lvl == 6):
        return True
    elif (exp >= 500 and lvl == 7):
        return True
    elif (exp >= 800 and lvl == 8):
        return True
    elif (exp >= 1200 and lvl == 9):
        return True
    elif (exp >= 1700 and lvl == 10):
        return True
    elif (exp >= 2500 and lvl == 11):
        return True
    elif (exp >= 3500 and lvl == 12):
        return True
    elif (exp >= 5000 and lvl == 13):
        return True
    elif (exp >= 7000 and lvl == 14):
        return True
    elif (exp >= 10000 and lvl == 15):
        return True
    elif (exp >= 15000 and lvl == 16):
        return True
    elif (exp >= 25000 and lvl == 17):
        return True
    elif (exp >= 50000 and lvl == 18):
        return True
    elif (exp >= 99999 and lvl == 19):
        return True
    return False


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
    if (not world.state._is_route(world, player,2)) or world.state._is_route(world,player,3):
        set_rule(world.get_location(("Nicecream Punch Card"), player), lambda state: state.has('Punch Card', player, 3) and state._reach_waterfall(player, world))
        set_rule(world.get_location(("Nicecream Snowdin"), player), lambda state: state._reach_snowdin(player, world))
        set_rule(world.get_location(("Nicecream Waterfall"), player), lambda state: state._reach_waterfall(player, world))
        set_rule(world.get_location(("Card Reward"), player), lambda state: state._reach_waterfall(player, world))
        set_rule(world.get_location(("Apron Hidden"), player), lambda state: state._reach_cooking_show(player, world))
        set_rule(world.get_location(("Cooking Show Plot"), player), lambda state: state._reach_cooking_show(player, world))
        set_rule(world.get_location(("TV Show Plot"), player), lambda state: state._reach_news_show(player, world))
    if world.state._is_route(world,player,2) and world.rando_love[player]:
        maxlv = 5
        exp = 190
        curarea = "Old Home"
        while curarea != "Core":
            if UndertaleLogic._prev_area(UndertaleLogic(), player, world, 1) == curarea:
                curarea = "Snowdin Town"
                exp += 412
                while can_level(exp, maxlv):
                    maxlv += 1
                    set_rule(world.get_location(("LOVE "+str(maxlv)), player), lambda state: state._reach_snowdin(player, world))
            if UndertaleLogic._prev_area(UndertaleLogic(), player, world, 2) == curarea:
                curarea = "Waterfall"
                exp += 1643
                while can_level(exp, maxlv):
                    maxlv += 1
                    set_rule(world.get_location(("LOVE "+str(maxlv)), player), lambda state: state._reach_waterfall(player, world))
            if UndertaleLogic._prev_area(UndertaleLogic(), player, world, 3) == curarea:
                curarea = "Hotland"
                exp += 3320
                while can_level(exp, maxlv):
                    maxlv += 1
                    set_rule(world.get_location(("LOVE "+str(maxlv)), player), lambda state: state._reach_hotland(player, world))
            if UndertaleLogic._prev_area(UndertaleLogic(), player, world, 4) == curarea:
                curarea = "Core"
                exp = 50000
                while can_level(exp, maxlv):
                    maxlv += 1
                    set_rule(world.get_location(("LOVE "+str(maxlv)), player), lambda state: state._reach_core_mettaton(player, world))
        exp = 99999
        while can_level(exp, maxlv):
            maxlv += 1
            set_rule(world.get_location(("LOVE "+str(maxlv)), player), lambda state: state._reach_sans(player, world))
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
