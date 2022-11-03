from argparse import Namespace

from BaseClasses import MultiWorld
from worlds.alttp.Dungeons import create_dungeons, get_dungeon_item_pool
from worlds.alttp.EntranceShuffle import link_entrances
from worlds.alttp.InvertedRegions import mark_dark_world_regions
from worlds.alttp.ItemPool import difficulties, generate_itempool
from worlds.alttp.Items import ItemFactory
from worlds.alttp.Regions import create_regions
from worlds.alttp.Shops import create_shops
from worlds.alttp.Rules import set_rules
from test.TestBase import TestBase

from worlds import AutoWorld


class TestVanillaOWG(TestBase):
    def setUp(self):
        self.multiworld = MultiWorld(1)
        args = Namespace()
        for name, option in AutoWorld.AutoWorldRegister.world_types["A Link to the Past"].option_definitions.items():
            setattr(args, name, {1: option.from_any(option.default)})
        self.multiworld.set_options(args)
        self.multiworld.set_default_common_options()
        self.multiworld.difficulty_requirements[1] = difficulties['normal']
        self.multiworld.logic[1] = "owglitches"
        self.multiworld.worlds[1].er_seed = 0
        self.multiworld.worlds[1].create_regions()
        self.multiworld.worlds[1].create_items()
        self.multiworld.required_medallions[1] = ['Ether', 'Quake']
        self.multiworld.itempool.extend(get_dungeon_item_pool(self.multiworld))
        self.multiworld.itempool.extend(ItemFactory(['Green Pendant', 'Red Pendant', 'Blue Pendant', 'Beat Agahnim 1', 'Beat Agahnim 2', 'Crystal 1', 'Crystal 2', 'Crystal 3', 'Crystal 4', 'Crystal 5', 'Crystal 6', 'Crystal 7'], 1))
        self.multiworld.get_location('Agahnim 1', 1).item = None
        self.multiworld.get_location('Agahnim 2', 1).item = None
        self.multiworld.precollected_items[1].clear()
        self.multiworld.itempool.append(ItemFactory('Pegasus Boots', 1))
        mark_dark_world_regions(self.multiworld, 1)
        self.multiworld.worlds[1].set_rules()