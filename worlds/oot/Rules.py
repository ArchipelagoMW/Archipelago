from collections import deque
import logging
import typing

from .Regions import TimeOfDay
from .DungeonList import dungeon_table
from .Hints import HintArea
from .Items import oot_is_item_of_type
from .LocationList import dungeon_song_locations

from BaseClasses import CollectionState
from worlds.generic.Rules import set_rule, add_rule, add_item_rule, forbid_item
from ..AutoWorld import LogicMixin


class OOTLogic(LogicMixin):

    def _oot_has_stones(self, count, player): 
        return self.has_group("stones", player, count)

    def _oot_has_medallions(self, count, player): 
        return self.has_group("medallions", player, count)

    def _oot_has_dungeon_rewards(self, count, player): 
        return self.has_group("rewards", player, count)

    def _oot_has_hearts(self, count, player):
        containers = self.count("Heart Container", player)
        pieces = self.count("Piece of Heart", player) + self.count("Piece of Heart (Treasure Chest Game)", player)
        total_hearts = 3 + containers + int(pieces / 4)
        return total_hearts >= count

    def _oot_has_bottle(self, player): 
        return self.has_group("logic_bottles", player)

    def _oot_has_beans(self, player):
        return self.has("Magic Bean Pack", player) or self.has("Buy Magic Bean", player) or self.has("Magic Bean", player, 10)

    # Used for fall damage and other situations where damage is unavoidable
    def _oot_can_live_dmg(self, player, hearts):
        mult = self.multiworld.worlds[player].damage_multiplier
        if hearts*4 >= 3:
            return mult != 'ohko' and mult != 'quadruple'
        else:
            return mult != 'ohko'

    # Figure out if the given region's parent dungeon has shortcuts enabled
    def _oot_region_has_shortcuts(self, player, regionname):
        return self.multiworld.worlds[player].region_has_shortcuts(regionname)


    # This function operates by assuming different behavior based on the "level of recursion", handled manually. 
    # If it's called while self.age[player] is None, then it will set the age variable and then attempt to reach the region. 
    # If self.age[player] is not None, then it will compare it to the 'age' parameter, and return True iff they are equal. 
    #   This lets us fake the OOT accessibility check that cares about age. Unfortunately it's still tied to the ground region. 
    def _oot_reach_as_age(self, regionname, age, player): 
        if self.age[player] is None: 
            self.age[player] = age
            can_reach = self.multiworld.get_region(regionname, player).can_reach(self)
            self.age[player] = None
            return can_reach
        return self.age[player] == age

    def _oot_reach_at_time(self, regionname, tod, already_checked, player):
        name_map = {
            TimeOfDay.DAY: self.day_reachable_regions[player],
            TimeOfDay.DAMPE: self.dampe_reachable_regions[player],
            TimeOfDay.ALL: self.day_reachable_regions[player].intersection(self.dampe_reachable_regions[player])
        }
        if regionname in name_map[tod]:
            return True
        region = self.multiworld.get_region(regionname, player)
        if region.provides_time == TimeOfDay.ALL or regionname == 'Root':
            self.day_reachable_regions[player].add(regionname)
            self.dampe_reachable_regions[player].add(regionname)
            return True
        if region.provides_time == TimeOfDay.DAMPE:
            self.dampe_reachable_regions[player].add(regionname)
            return tod == TimeOfDay.DAMPE
        for entrance in region.entrances:
            if entrance.parent_region.name in already_checked:
                continue
            if self._oot_reach_at_time(entrance.parent_region.name, tod, already_checked + [regionname], player):
                if tod == TimeOfDay.DAY:
                    self.day_reachable_regions[player].add(regionname)
                elif tod == TimeOfDay.DAMPE:
                    self.dampe_reachable_regions[player].add(regionname)
                elif tod == TimeOfDay.ALL:
                    self.day_reachable_regions[player].add(regionname)
                    self.dampe_reachable_regions[player].add(regionname)
                return True
        return False

    # Store the age before calling this!
    def _oot_update_age_reachable_regions(self, player): 
        self.stale[player] = False
        for age in ['child', 'adult']: 
            self.age[player] = age
            rrp = getattr(self, f'{age}_reachable_regions')[player]
            bc = getattr(self, f'{age}_blocked_connections')[player]
            queue = deque(getattr(self, f'{age}_blocked_connections')[player])
            start = self.multiworld.get_region('Menu', player)

            # init on first call - this can't be done on construction since the regions don't exist yet
            if not start in rrp:
                rrp.add(start)
                bc.update(start.exits)
                queue.extend(start.exits)

            # run BFS on all connections, and keep track of those blocked by missing items
            while queue:
                connection = queue.popleft()
                new_region = connection.connected_region
                if new_region is None: 
                    continue
                if new_region in rrp:
                    bc.remove(connection)
                elif connection.can_reach(self):
                    rrp.add(new_region)
                    bc.remove(connection)
                    bc.update(new_region.exits)
                    queue.extend(new_region.exits)
                    self.path[new_region] = (new_region.name, self.path.get(connection, None))


# Sets extra rules on various specific locations not handled by the rule parser.
def set_rules(ootworld):
    logger = logging.getLogger('')

    world = ootworld.multiworld
    player = ootworld.player

    if ootworld.logic_rules != 'no_logic': 
        if ootworld.triforce_hunt: 
            world.completion_condition[player] = lambda state: state.has('Triforce Piece', player, ootworld.triforce_goal)
        else: 
            world.completion_condition[player] = lambda state: state.has('Triforce', player)

    # ganon can only carry triforce
    world.get_location('Ganon', player).item_rule = lambda item: item.name == 'Triforce'

    # is_child = ootworld.parser.parse_rule('is_child')
    guarantee_hint = ootworld.parser.parse_rule('guarantee_hint')

    for location in filter(lambda location: location.name in ootworld.shop_prices
        or location.type in {'Scrub', 'GrottoScrub'}, ootworld.get_locations()):
        if location.type == 'Shop':
            location.price = ootworld.shop_prices[location.name]
        add_rule(location, create_shop_rule(location, ootworld.parser))

    if (ootworld.dungeon_mq['Forest Temple'] and ootworld.shuffle_bosskeys == 'dungeon'
        and ootworld.shuffle_smallkeys == 'dungeon' and ootworld.tokensanity == 'off'):
        # First room chest needs to be a small key. Make sure the boss key isn't placed here.
        location = world.get_location('Forest Temple MQ First Room Chest', player)
        forbid_item(location, 'Boss Key (Forest Temple)', ootworld.player)

    if ootworld.shuffle_song_items in {'song', 'dungeon'} and not ootworld.songs_as_items:
        # Sheik in Ice Cavern is the only song location in a dungeon; need to ensure that it cannot be anything else.
        # This is required if map/compass included, or any_dungeon shuffle.
        location = world.get_location('Sheik in Ice Cavern', player)
        add_item_rule(location, lambda item: oot_is_item_of_type(item, 'Song'))

    if ootworld.shuffle_child_trade == 'skip_child_zelda':
        # Song from Impa must be local
        location = world.get_location('Song from Impa', player)
        add_item_rule(location, lambda item: item.player == player)

    for name in ootworld.always_hints:
        add_rule(world.get_location(name, player), guarantee_hint)

    # TODO: re-add hints once they are working
    # if location.type == 'HintStone' and ootworld.hints == 'mask':
    #     location.add_rule(is_child)


def create_shop_rule(location, parser):
    def required_wallets(price):
        if price > 500:
            return 3
        if price > 200:
            return 2
        if price > 99:
            return 1
        return 0
    return parser.parse_rule('(Progressive_Wallet, %d)' % required_wallets(location.price))


# This function should be run once after the shop items are placed in the world.
# It should be run before other items are placed in the world so that logic has
# the correct checks for them. This is safe to do since every shop is still
# accessible when all items are obtained and every shop item is not.
# This function should also be called when a world is copied if the original world
# had called this function because the world.copy does not copy the rules
def set_shop_rules(ootworld):
    found_bombchus = ootworld.parser.parse_rule('found_bombchus')
    wallet = ootworld.parser.parse_rule('Progressive_Wallet')
    wallet2 = ootworld.parser.parse_rule('(Progressive_Wallet, 2)')

    for location in filter(lambda location: location.item and oot_is_item_of_type(location.item, 'Shop'), ootworld.get_locations()):
        # Add wallet requirements
        if location.item.name in ['Buy Arrows (50)', 'Buy Fish', 'Buy Goron Tunic', 'Buy Bombchu (20)', 'Buy Bombs (30)']:
            add_rule(location, wallet)
        elif location.item.name in ['Buy Zora Tunic', 'Buy Blue Fire']:
            add_rule(location, wallet2)

        # Add adult only checks
        if location.item.name in ['Buy Goron Tunic', 'Buy Zora Tunic']:
            add_rule(location, ootworld.parser.parse_rule('is_adult', location))

        # Add item prerequisite checks
        if location.item.name in ['Buy Blue Fire',
                                  'Buy Blue Potion',
                                  'Buy Bottle Bug',
                                  'Buy Fish',
                                  'Buy Green Potion',
                                  'Buy Poe',
                                  'Buy Red Potion [30]',
                                  'Buy Red Potion [40]',
                                  'Buy Red Potion [50]',
                                  'Buy Fairy\'s Spirit']:
            add_rule(location, lambda state: CollectionState._oot_has_bottle(state, ootworld.player))
        if location.item.name in ['Buy Bombchu (10)', 'Buy Bombchu (20)', 'Buy Bombchu (5)']:
            add_rule(location, found_bombchus)


# This function should be ran once after setting up entrances and before placing items
# The goal is to automatically set item rules based on age requirements in case entrances were shuffled
def set_entrances_based_rules(ootworld):

    all_state = ootworld.get_state_with_complete_itempool()
    all_state.sweep_for_events(locations=ootworld.get_locations())

    for location in filter(lambda location: location.type == 'Shop', ootworld.get_locations()):
        # If a shop is not reachable as adult, it can't have Goron Tunic or Zora Tunic as child can't buy these
        if not all_state._oot_reach_as_age(location.parent_region.name, 'adult', ootworld.player):
            forbid_item(location, 'Buy Goron Tunic', ootworld.player)
            forbid_item(location, 'Buy Zora Tunic', ootworld.player)

