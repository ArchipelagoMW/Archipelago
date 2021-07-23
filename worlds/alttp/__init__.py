import random

from BaseClasses import Item, CollectionState
from .SubClasses import ALttPItem
from ..AutoWorld import World
from .Options import alttp_options
from .Items import as_dict_item_table, item_name_groups, item_table
from .Regions import lookup_name_to_id, create_regions, mark_light_world_regions
from .Rules import set_rules
from .ItemPool import generate_itempool
from .Shops import create_shops
from .Dungeons import create_dungeons

from .InvertedRegions import create_inverted_regions, mark_dark_world_regions
from .EntranceShuffle import link_entrances, link_inverted_entrances, plando_connect

class ALTTPWorld(World):
    game: str = "A Link to the Past"
    options = alttp_options
    topology_present = True
    item_name_groups = item_name_groups
    item_names = frozenset(item_table)
    location_names = frozenset(lookup_name_to_id)
    hint_blacklist = {"Triforce"}

    item_name_to_id = {name: data.item_code for name, data in item_table.items() if type(data.item_code) == int}
    location_name_to_id = lookup_name_to_id

    data_version = 7
    remote_items: bool = False

    set_rules = set_rules

    create_items = generate_itempool

    def create_regions(self):
        player = self.player
        world = self.world
        if world.open_pyramid[player] == 'goal':
            world.open_pyramid[player] = world.goal[player] in {'crystals', 'ganontriforcehunt',
                                                                'localganontriforcehunt', 'ganonpedestal'}
        elif world.open_pyramid[player] == 'auto':
            world.open_pyramid[player] = world.goal[player] in {'crystals', 'ganontriforcehunt',
                                                                'localganontriforcehunt', 'ganonpedestal'} and \
                                         (world.shuffle[player] in {'vanilla', 'dungeonssimple', 'dungeonsfull',
                                                                    'dungeonscrossed'} or not world.shuffle_ganon)
        else:
            world.open_pyramid[player] = {'on': True, 'off': False, 'yes': True, 'no': False}.get(
                world.open_pyramid[player], 'auto')

        world.triforce_pieces_available[player] = max(world.triforce_pieces_available[player],
                                                      world.triforce_pieces_required[player])

        if world.mode[player] != 'inverted':
            create_regions(world, player)
        else:
            create_inverted_regions(world, player)
        create_shops(world, player)
        create_dungeons(world, player)


        if world.logic[player] not in ["noglitches", "minorglitches"] and world.shuffle[player] in \
                {"vanilla", "dungeonssimple", "dungeonsfull", "simple", "restricted", "full"}:
            world.fix_fake_world[player] = False

        # seeded entrance shuffle
        old_random = world.random
        world.random = random.Random(world.er_seeds[player])

        if world.mode[player] != 'inverted':
            link_entrances(world, player)
            mark_light_world_regions(world, player)
        else:
            link_inverted_entrances(world, player)
            mark_dark_world_regions(world, player)

        world.random = old_random
        plando_connect(world, player)

    def collect(self, state: CollectionState, item: Item) -> bool:
        if item.name.startswith('Progressive '):
            if 'Sword' in item.name:
                if state.has('Golden Sword', item.player):
                    pass
                elif state.has('Tempered Sword', item.player) and self.world.difficulty_requirements[
                    item.player].progressive_sword_limit >= 4:
                    state.prog_items['Golden Sword', item.player] += 1
                    return True
                elif state.has('Master Sword', item.player) and self.world.difficulty_requirements[
                    item.player].progressive_sword_limit >= 3:
                    state.prog_items['Tempered Sword', item.player] += 1
                    return True
                elif state.has('Fighter Sword', item.player) and self.world.difficulty_requirements[item.player].progressive_sword_limit >= 2:
                    state.prog_items['Master Sword', item.player] += 1
                    return True
                elif self.world.difficulty_requirements[item.player].progressive_sword_limit >= 1:
                    state.prog_items['Fighter Sword', item.player] += 1
                    return True
            elif 'Glove' in item.name:
                if state.has('Titans Mitts', item.player):
                    pass
                elif state.has('Power Glove', item.player):
                    state.prog_items['Titans Mitts', item.player] += 1
                    return True
                else:
                    state.prog_items['Power Glove', item.player] += 1
                    return True
            elif 'Shield' in item.name:
                if state.has('Mirror Shield', item.player):
                    pass
                elif state.has('Red Shield', item.player) and self.world.difficulty_requirements[item.player].progressive_shield_limit >= 3:
                    state.prog_items['Mirror Shield', item.player] += 1
                    return True
                elif state.has('Blue Shield', item.player)  and self.world.difficulty_requirements[item.player].progressive_shield_limit >= 2:
                    state.prog_items['Red Shield', item.player] += 1
                    return True
                elif self.world.difficulty_requirements[item.player].progressive_shield_limit >= 1:
                    state.prog_items['Blue Shield', item.player] += 1
                    return True
            elif 'Bow' in item.name:
                if state.has('Silver', item.player):
                    pass
                elif state.has('Bow', item.player) and self.world.difficulty_requirements[item.player].progressive_bow_limit >= 2:
                    state.prog_items['Silver Bow', item.player] += 1
                    return True
                elif self.world.difficulty_requirements[item.player].progressive_bow_limit >= 1:
                    state.prog_items['Bow', item.player] += 1
                    return True
        elif item.advancement or item.smallkey or item.bigkey:
            state.prog_items[item.name, item.player] += 1
            return True
        return False

    def get_required_client_version(self) -> tuple:
        return max((0, 1, 4), super(ALTTPWorld, self).get_required_client_version())

    def create_item(self, name: str) -> Item:
        return ALttPItem(name, self.player, **as_dict_item_table[name])


