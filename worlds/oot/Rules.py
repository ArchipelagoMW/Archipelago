from collections import deque
import logging
from .Location import DisableType
from .SaveContext import SaveContext
# from Search import Search
from BaseClasses import CollectionState
from worlds.generic.Rules import set_rule, add_rule, add_item_rule, forbid_item, item_in_locations
from ..AutoWorld import LogicMixin


class OOTLogic(LogicMixin):

    def _oot_has_stones(self, count, player): 
        return self.has_group("stones", player, count)

    def _oot_has_medallions(self, count, player): 
        return self.has_group("medallions", player, count)

    def _oot_has_dungeon_rewards(self, count, player): 
        return self.has_group("rewards", player, count)

    def _oot_has_bottle(self, player): 
        return self.has_group("bottles", player)

    # This function operates by assuming different behavior based on the "level of recursion", handled manually. 
    # If it's called while self.age[player] is None, then it will set the age variable and then attempt to reach the region. 
    # If self.age[player] is not None, then it will compare it to the 'age' parameter, and return True iff they are equal. 
    #   This lets us fake the OOT accessibility check that cares about age. Unfortunately it's still tied to the ground region. 
    def _oot_reach_as_age(self, regionname, age, player): 
        if self.age[player] is None: 
            self.age[player] = age
            can_reach = self.world.get_region(regionname, player).can_reach(self)
            self.age[player] = None
            return can_reach
        return self.age[player] == age

    # Store the age before calling this!
    def _oot_update_age_reachable_regions(self, player): 
        self.stale[player] = False
        for age in ['child', 'adult']: 
            self.age[player] = age
            rrp = getattr(self, f'{age}_reachable_regions')[player]
            bc = getattr(self, f'{age}_blocked_connections')[player]
            queue = deque(getattr(self, f'{age}_blocked_connections')[player])
            start = self.world.get_region('Menu', player)

            # init on first call - this can't be done on construction since the regions don't exist yet
            if not start in rrp:
                rrp.add(start)
                bc.update(start.exits)
                queue.extend(start.exits)

            # run BFS on all connections, and keep track of those blocked by missing items
            while queue:
                connection = queue.popleft()
                new_region = connection.connected_region
                if new_region in rrp:
                    bc.remove(connection)
                elif connection.can_reach(self):
                    rrp.add(new_region)
                    bc.remove(connection)
                    bc.update(new_region.exits)
                    queue.extend(new_region.exits)
                    self.path[new_region] = (new_region.name, self.path.get(connection, None))


def set_rules(ootworld):
    logger = logging.getLogger('')

    world = ootworld.world
    player = ootworld.player

    if ootworld.logic_rules != 'no_logic': 
        if ootworld.triforce_hunt: 
            world.completion_condition[player] = lambda state: state.has('Triforce Piece', player, ootworld.triforce_goal)
        else: 
            world.completion_condition[player] = lambda state: state.has('Triforce', player)

    # ganon can only carry triforce
    world.get_location('Ganon', player).item_rule = lambda item: item.name == 'Triforce'

    # is_child = ootworld.parser.parse_rule('is_child')
    # guarantee_hint = ootworld.parser.parse_rule('guarantee_hint')

    for location in ootworld.get_locations():
        if ootworld.shuffle_song_items == 'song':
            if location.type == 'Song':
                # must be a song, or there are songs in starting items; then it can be anything
                add_item_rule(location, lambda item: 
                    (ootworld.starting_songs and item.type != 'Song')
                    or (item.type == 'Song' and item.player == location.player))
            else:
                add_item_rule(location, lambda item: item.type != 'Song')

        if location.type == 'Shop':
            if location.name in ootworld.shop_prices:
                add_item_rule(location, lambda item: item.type != 'Shop')
                location.price = ootworld.shop_prices[location.name]
                # If price was specified in plando, use it here so access rule is set correctly.
                # if location.name in world.distribution.locations and world.distribution.locations[location.name].price is not None:
                #     price = world.distribution.locations[location.name].price
                #     if price > 999: # Cap positive values above 999 so that they're not impossible.
                #         world.distribution.locations[location.name].price = 999
                #         price = 999
                #     elif price < -32768: # Prices below this will error on patching.
                #         world.distribution.locations[location.name].price = -32768
                #         price = -32768
                #     location.price = price
                #     world.shop_prices[location.name] = price
                add_rule(location, create_shop_rule(location, ootworld.parser))
            else:
                add_item_rule(location, lambda item: item.type == 'Shop' and item.player == location.player)
        elif 'Deku Scrub' in location.name:
            add_rule(location, create_shop_rule(location, ootworld.parser))
        else:
            add_item_rule(location, lambda item: item.type != 'Shop')

        if ootworld.skip_child_zelda and location.name == 'Song from Impa':
            limit_to_itemset(location, SaveContext.giveable_items)
            add_item_rule(location, lambda item: item.player == location.player)

        if location.name == 'Forest Temple MQ First Room Chest' and ootworld.shuffle_bosskeys == 'dungeon' and ootworld.shuffle_smallkeys == 'dungeon' and ootworld.tokensanity == 'off':
            # This location needs to be a small key. Make sure the boss key isn't placed here.
            forbid_item(location, 'Boss Key (Forest Temple)', ootworld.player)

        # TODO: re-add hints once they are working
        # if location.type == 'HintStone' and ootworld.hints == 'mask':
        #     location.add_rule(is_child)

        # if location.name in ootworld.always_hints:
            # location.add_rule(guarantee_hint)

    # Handle this properly in the AP fill
    # for location in world.disabled_locations:
    #     try:
    #         world.get_location(location).disabled = DisableType.PENDING
    #     except:
    #         logger.debug('Tried to disable location that does not exist: %s' % location)


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


def limit_to_itemset(location, itemset):
    old_rule = location.item_rule
    location.item_rule = lambda item: item.name in itemset and old_rule(item)


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
    for location in ootworld.world.get_filled_locations():
        if location.player == ootworld.player and location.item.type == 'Shop':
            # Add wallet requirements
            if location.item.name in ['Buy Arrows (50)', 'Buy Fish', 'Buy Goron Tunic', 'Buy Bombchu (20)', 'Buy Bombs (30)']:
                add_rule(location, wallet)
            elif location.item.name in ['Buy Zora Tunic', 'Buy Blue Fire']:
                add_rule(location, wallet2)

            # Add adult only checks
            if location.item.name in ['Buy Goron Tunic', 'Buy Zora Tunic']:
                is_adult = ootworld.parser.parse_rule('is_adult', location)
                add_rule(location, is_adult)

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

    if ootworld.world.accessibility == 'beatable': 
        return

    all_state = ootworld.state_with_items(ootworld.itempool)

    for location in ootworld.get_locations():
        # If a shop is not reachable as adult, it can't have Goron Tunic or Zora Tunic as child can't buy these
        if location.type == 'Shop' and not all_state._oot_reach_as_age(location.parent_region.name, 'adult', ootworld.player):
            forbid_item(location, 'Buy Goron Tunic', ootworld.player)
            forbid_item(location, 'Buy Zora Tunic', ootworld.player)

