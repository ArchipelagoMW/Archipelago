from ..generic.Rules import set_rule, add_rule
from BaseClasses import MultiWorld
from ..AutoWorld import LogicMixin
import math


class UndertaleLogic(LogicMixin):
    def _undertale_prev_area(self, player: int, area: int):
        if area == 1:
            return self.world.get_region("Snowdin Forest", player).entrances[0].parent_region.name
        elif area == 2:
            return self.world.get_region("Waterfall", player).entrances[0].parent_region.name
        elif area == 3:
            return self.world.get_region("Hotland", player).entrances[0].parent_region.name
        elif area == 4:
            return self.world.get_region("Core", player).entrances[0].parent_region.name

    def _undertale_is_route(self, player: int, route: int):
        if route == 3:
            return (self.world.route_required[player].current_key == "all_routes")
        if self.world.route_required[player].current_key == "all_routes":
            return True
        if route == 0:
            return (self.world.route_required[player].current_key == "neutral")
        if route == 1:
            return (self.world.route_required[player].current_key == "pacifist")
        if route == 2:
            return (self.world.route_required[player].current_key == "genocide")
        return False

    def _undertale_has_plot(self, player: int, item: str):
        if item == "Goat Plush":
            return (self.has("Goat Plush", player) or self.has("Progressive Plot",player,1))
        elif item == "Complete Skeleton":
            return (self.has("Complete Skeleton", player) or (self.has("Progressive Plot",player,2) and self._undertale_is_route(player,1)))
        elif item == "Snow Shovel":
            return (self.has("Snow Shovel", player) or (self.has("Progressive Plot",player,2) and not self._undertale_is_route(player,1)) or
                    (self.has("Progressive Plot",player,3) and self._undertale_is_route(player,1)))
        elif item == "Fish":
            return (self.has("Fish", player) or (self.has("Progressive Plot",player,4) and self._undertale_is_route(player,1)))
        elif item == "Heat Suit":
            return (self.has("Heat Suit", player) or (self.has("Progressive Plot",player,3) and not self._undertale_is_route(player,1)) or
                    (self.has("Progressive Plot",player,5) and self._undertale_is_route(player,1)))
        elif item == "Cooking Set":
            return ((self.has("Cooking Set", player) or self._undertale_is_route(player,2)) or (self.has("Progressive Plot",player,3) and self._undertale_is_route(player,2)) or
                    (self.has("Progressive Plot",player,4) and self._undertale_is_route(player,0)) or (self.has("Progressive Plot",player,6) and self._undertale_is_route(player,1)))
        elif item == "Microphone":
            return ((self.has("Microphone", player) or self._undertale_is_route(player,2)) or (self.has("Progressive Plot",player,3) and self._undertale_is_route(player,2)) or
                    (self.has("Progressive Plot",player,5) and self._undertale_is_route(player,0)) or (self.has("Progressive Plot",player,7) and self._undertale_is_route(player,1)))
        elif item == "Bridge Tools":
            return ((self.has("Bridge Tools", player)) or (self.has("Progressive Plot",player,4) and self._undertale_is_route(player,2)) or
                    (self.has("Progressive Plot",player,6) and self._undertale_is_route(player,0)) or (self.has("Progressive Plot",player,8) and self._undertale_is_route(player,1)))
        elif item == "Mettaton Plush":
            return (self.has("Mettaton Plush", player) or (self.has("Progressive Plot",player,5) and self._undertale_is_route(player,2)) or
                    (self.has("Progressive Plot",player,7) and self._undertale_is_route(player,0)) or (self.has("Progressive Plot",player,9) and self._undertale_is_route(player,1)))
        elif item == "DT Extractor":
            return ((self.has('DT Extractor', player) or self.has("Progressive Plot",player,10)) and self._undertale_is_route(player,1))

    def _undertale_can_level(self, exp: int, lvl: int):
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
    set_rule(world.get_entrance("Old Home Exit", player), lambda state: state._undertale_has_plot(player, "Goat Plush"))
    set_rule(world.get_entrance("Snowdin Town Exit", player), lambda state: state._undertale_has_plot(player, "Snow Shovel"))
    set_rule(world.get_entrance("Waterfall Exit", player), lambda state: state._undertale_has_plot(player, "Heat Suit"))
    set_rule(world.get_entrance("Cooking Show Entrance", player), lambda state: state._undertale_has_plot(player, "Cooking Set"))
    set_rule(world.get_entrance("News Show Entrance", player), lambda state: state._undertale_has_plot(player, "Microphone"))
    set_rule(world.get_entrance("Hotland Exit", player), lambda state: state._undertale_has_plot(player, "Bridge Tools"))
    set_rule(world.get_entrance("Core Exit", player), lambda state: state._undertale_has_plot(player, "Mettaton Plush"))
    set_rule(world.get_entrance("New Home Exit", player), lambda state: state.has("Determination", player) or state.has("Soul Piece", player, state.world.soul_pieces[player]))
    if world.state._undertale_is_route(player, 1):
        set_rule(world.get_entrance("Papyrus\' Home Entrance", player), lambda state: state._undertale_has_plot(player, "Complete Skeleton"))
        set_rule(world.get_entrance("Undyne\'s Home Entrance", player), lambda state: state._undertale_has_plot(player, "Fish") and state.has('Papyrus Date', player))
        set_rule(world.get_entrance("Lab Elevator", player), lambda state: state.has('Undyne Letter EX', player) and state.has('Undyne Date', player) and state.has('Alphys Date', player) and state._undertale_has_plot(player, "DT Extractor"))
    if world.state._undertale_is_route(player,1):
        set_rule(world.get_location(("Papyrus Plot"), player), lambda state: state.can_reach('Snowdin Town', 'Region', player))
        set_rule(world.get_location(("Undyne Plot"), player), lambda state: state.can_reach('Waterfall', 'Region', player))
        set_rule(world.get_location(("True Lab Plot"), player), lambda state: state.can_reach('New Home', 'Region', player) and state.can_reach('Letter Quest', 'Location', player))
        set_rule(world.get_location(("Chisps Machine"), player), lambda state: state.can_reach('True Lab', 'Region', player))
        set_rule(world.get_location(("Dog Sale 1"), player), lambda state: state.can_reach('Cooking Show', 'Region', player))
        set_rule(world.get_location(("Cat Sale"), player), lambda state: state.can_reach('Cooking Show', 'Region', player))
        set_rule(world.get_location(("Dog Sale 2"), player), lambda state: state.can_reach('Cooking Show', 'Region', player))
        set_rule(world.get_location(("Dog Sale 3"), player), lambda state: state.can_reach('Cooking Show', 'Region', player))
        set_rule(world.get_location(("Dog Sale 4"), player), lambda state: state.can_reach('Cooking Show', 'Region', player))
        set_rule(world.get_location(("Hush Trade"), player), lambda state: state.can_reach('News Show', 'Region', player) and state.has('Hot Dog...?', player, 1))
        set_rule(world.get_location(("Letter Quest"), player), lambda state: state.can_reach('New Home Exit', 'Entrance', player))
    if (not world.state._undertale_is_route(player,2)) or world.state._undertale_is_route(player,3):
        set_rule(world.get_location(("Nicecream Punch Card"), player), lambda state: state.has('Punch Card', player, 3) and state.can_reach('Waterfall', 'Region', player))
        set_rule(world.get_location(("Nicecream Snowdin"), player), lambda state: state.can_reach('Snowdin Town', 'Region', player))
        set_rule(world.get_location(("Nicecream Waterfall"), player), lambda state: state.can_reach('Waterfall', 'Region', player))
        set_rule(world.get_location(("Card Reward"), player), lambda state: state.can_reach('Waterfall', 'Region', player))
        set_rule(world.get_location(("Apron Hidden"), player), lambda state: state.can_reach('Cooking Show', 'Region', player))
        set_rule(world.get_location(("Cooking Show Plot"), player), lambda state: state.can_reach('Cooking Show', 'Region', player))
        set_rule(world.get_location(("TV Show Plot"), player), lambda state: state.can_reach('News Show', 'Region', player))
    if world.state._undertale_is_route(player,2) and (world.rando_love[player] or world.rando_stats[player]):
        maxlv = 5
        exp = 190
        curarea = "Old Home"
        while maxlv < 20:
            if world.state._undertale_prev_area(player, 1) == curarea:
                curarea = "Snowdin Town"
                exp += 407
            elif world.state._undertale_prev_area(player, 2) == curarea:
                curarea = "Waterfall"
                exp += 1643
            elif world.state._undertale_prev_area(player, 3) == curarea:
                curarea = "News Show"
                exp += 3320
            elif world.state._undertale_prev_area(player, 4) == curarea:
                curarea = "Core"
                exp = 50000
            elif curarea == "Core":
                curarea = "Sans"
                exp = 99999
            while world.state._undertale_can_level(exp, maxlv):
                maxlv += 1
                if world.rando_stats[player]:
                    if curarea == "Snowdin Town":
                        set_rule(world.get_location(("ATK "+str(maxlv)), player), lambda state: state.can_reach('Snowdin Town', 'Region', player))
                        set_rule(world.get_location(("HP "+str(maxlv)), player), lambda state: state.can_reach('Snowdin Town', 'Region', player))
                        if maxlv == 9 or maxlv == 13 or maxlv == 17:
                            set_rule(world.get_location(("DEF "+str(maxlv)), player), lambda state: state.can_reach('Snowdin Town', 'Region', player))
                    elif curarea == "Waterfall":
                        set_rule(world.get_location(("ATK "+str(maxlv)), player), lambda state: state.can_reach('Waterfall', 'Region', player))
                        set_rule(world.get_location(("HP "+str(maxlv)), player), lambda state: state.can_reach('Waterfall', 'Region', player))
                        if maxlv == 9 or maxlv == 13 or maxlv == 17:
                            set_rule(world.get_location(("DEF "+str(maxlv)), player), lambda state: state.can_reach('Waterfall', 'Region', player))
                    elif curarea == "News Show":
                        set_rule(world.get_location(("ATK "+str(maxlv)), player), lambda state: state.can_reach('News Show', 'Region', player))
                        set_rule(world.get_location(("HP "+str(maxlv)), player), lambda state: state.can_reach('News Show', 'Region', player))
                        if maxlv == 9 or maxlv == 13 or maxlv == 17:
                            set_rule(world.get_location(("DEF "+str(maxlv)), player), lambda state: state.can_reach('News Show', 'Region', player))
                    elif curarea == "Core":
                        set_rule(world.get_location(("ATK "+str(maxlv)), player), lambda state: state.can_reach('Core Exit', 'Entrance', player))
                        set_rule(world.get_location(("HP "+str(maxlv)), player), lambda state: state.can_reach('Core Exit', 'Entrance', player))
                        if maxlv == 9 or maxlv == 13 or maxlv == 17:
                            set_rule(world.get_location(("DEF "+str(maxlv)), player), lambda state: state.can_reach('Core Exit', 'Entrance', player))
                    elif curarea == "Sans":
                        set_rule(world.get_location(("ATK "+str(maxlv)), player), lambda state: state.can_reach('New Home Exit', 'Entrance', player))
                        set_rule(world.get_location(("HP "+str(maxlv)), player), lambda state: state.can_reach('New Home Exit', 'Entrance', player))
                        if maxlv == 9 or maxlv == 13 or maxlv == 17:
                            set_rule(world.get_location(("DEF "+str(maxlv)), player), lambda state: state.can_reach('New Home Exit', 'Entrance', player))
                if world.rando_love[player]:
                    if curarea == "Snowdin Town":
                        set_rule(world.get_location(("LOVE "+str(maxlv)), player), lambda state: state.can_reach('Snowdin Town', 'Region', player))
                    elif curarea == "Waterfall":
                        set_rule(world.get_location(("LOVE "+str(maxlv)), player), lambda state: state.can_reach('Waterfall', 'Region', player))
                    elif curarea == "News Show":
                        set_rule(world.get_location(("LOVE "+str(maxlv)), player), lambda state: state.can_reach('News Show', 'Region', player))
                    elif curarea == "Core":
                        set_rule(world.get_location(("LOVE "+str(maxlv)), player), lambda state: state.can_reach('Core Exit', 'Entrance', player))
                    elif curarea == "Sans":
                        set_rule(world.get_location(("LOVE "+str(maxlv)), player), lambda state: state.can_reach('New Home Exit', 'Entrance', player))
    set_rule(world.get_location(("Snowman"), player), lambda state: state.can_reach('Snowdin Town', 'Region', player))
    set_rule(world.get_location(("Waterfall Plot"), player), lambda state: state.can_reach('Snowdin Town', 'Region', player))
    set_rule(world.get_location(("Hotland Plot"), player), lambda state: state.can_reach('Waterfall', 'Region', player))
    set_rule(world.get_location(("Core Plot"), player), lambda state: state.can_reach('News Show', 'Region', player))
    set_rule(world.get_location(("Mettaton Plot"), player), lambda state: state.can_reach('Core Exit', 'Entrance', player))
    set_rule(world.get_location(("Bunny 1"), player), lambda state: state.can_reach('Snowdin Town', 'Region', player))
    set_rule(world.get_location(("Bunny 2"), player), lambda state: state.can_reach('Snowdin Town', 'Region', player))
    set_rule(world.get_location(("Bunny 3"), player), lambda state: state.can_reach('Snowdin Town', 'Region', player))
    set_rule(world.get_location(("Bunny 4"), player), lambda state: state.can_reach('Snowdin Town', 'Region', player))
    set_rule(world.get_location(("Astro 1"), player), lambda state: state.can_reach('Waterfall', 'Region', player))
    set_rule(world.get_location(("Astro 2"), player), lambda state: state.can_reach('Waterfall', 'Region', player))
    set_rule(world.get_location(("Gerson 1"), player), lambda state: state.can_reach('Waterfall', 'Region', player))
    set_rule(world.get_location(("Gerson 2"), player), lambda state: state.can_reach('Waterfall', 'Region', player))
    set_rule(world.get_location(("Gerson 3"), player), lambda state: state.can_reach('Waterfall', 'Region', player))
    set_rule(world.get_location(("Gerson 4"), player), lambda state: state.can_reach('Waterfall', 'Region', player))
    set_rule(world.get_location(("Present Knife"), player), lambda state: state.can_reach('New Home', 'Region', player))
    set_rule(world.get_location(("Present Locket"), player), lambda state: state.can_reach('New Home', 'Region', player))
    set_rule(world.get_location(("Trash Burger"), player), lambda state: state.can_reach('Core', 'Region', player))
    set_rule(world.get_location(("Quiche Bench"), player), lambda state: state.can_reach('Waterfall', 'Region', player))
    set_rule(world.get_location(("Tutu Hidden"), player), lambda state: state.can_reach('Waterfall', 'Region', player))
    set_rule(world.get_location(("Grass Shoes"), player), lambda state: state.can_reach('Waterfall', 'Region', player))
    set_rule(world.get_location(("TemmieShop 1"), player), lambda state: state.can_reach('Waterfall', 'Region', player))
    set_rule(world.get_location(("TemmieShop 2"), player), lambda state: state.can_reach('Waterfall', 'Region', player))
    set_rule(world.get_location(("TemmieShop 3"), player), lambda state: state.can_reach('Waterfall', 'Region', player))
    set_rule(world.get_location(("TemmieShop 4"), player), lambda state: state.can_reach('Waterfall', 'Region', player))
    set_rule(world.get_location(("Noodles Fridge"), player), lambda state: state.can_reach('Hotland', 'Region', player))
    set_rule(world.get_location(("Pan Hidden"), player), lambda state: state.can_reach('Hotland', 'Region', player))
    set_rule(world.get_location(("Bratty Catty 1"), player), lambda state: state.can_reach('News Show', 'Region', player))
    set_rule(world.get_location(("Bratty Catty 2"), player), lambda state: state.can_reach('News Show', 'Region', player))
    set_rule(world.get_location(("Bratty Catty 3"), player), lambda state: state.can_reach('News Show', 'Region', player))
    set_rule(world.get_location(("Bratty Catty 4"), player), lambda state: state.can_reach('News Show', 'Region', player))
    set_rule(world.get_location(("Burgerpants 1"), player), lambda state: state.can_reach('News Show', 'Region', player))
    set_rule(world.get_location(("Burgerpants 2"), player), lambda state: state.can_reach('News Show', 'Region', player))
    set_rule(world.get_location(("Burgerpants 3"), player), lambda state: state.can_reach('News Show', 'Region', player))
    set_rule(world.get_location(("Burgerpants 4"), player), lambda state: state.can_reach('News Show', 'Region', player))


# Sets rules on completion condition
def set_completion_rules(world: MultiWorld, player: int):
    completion_requirements = lambda state: True
    if not world.state._undertale_is_route(player, 1):
        completion_requirements = lambda state: state.can_reach('New Home Exit', 'Entrance', player)
    if world.state._undertale_is_route(player, 1):
        completion_requirements = lambda state: state.can_reach('True Lab', 'Region', player)

    world.completion_condition[player] = lambda state: completion_requirements(state)
