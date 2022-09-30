from argparse import Namespace

from BaseClasses import MultiWorld
from worlds.alttp.Dungeons import create_dungeons, get_dungeon_item_pool
from worlds.alttp.EntranceShuffle import link_entrances
from worlds.alttp.InvertedRegions import mark_dark_world_regions
from worlds.alttp.ItemPool import difficulties, generate_itempool
from worlds.alttp.Items import ItemFactory
from worlds.alttp.Regions import create_regions
from worlds.alttp.Shops import create_shops
from test.TestBase import TestBase
from worlds.alttp.Options import Logic, MireMedallion, TurtleMedallion

from worlds import AutoWorld


class TestVanillaOWG(TestBase):
    def setUp(self):
        self.world = MultiWorld(1)
        args = Namespace()
        for name, option in AutoWorld.AutoWorldRegister.world_types["A Link to the Past"].option_definitions.items():
            setattr(args, name, {1: option.from_any(option.default)})
        self.world.set_options(args)
        self.world.set_default_common_options()
        self.world.difficulty_requirements[1] = difficulties['normal']
        setattr(self.world, "glitches_required", {1: Logic(Logic.alias_owg)})
        setattr(self.world, "misery_mire_medallion", {1: MireMedallion(MireMedallion.option_ether)})
        setattr(self.world, "turtle_rock_medallion", {1: TurtleMedallion(TurtleMedallion.option_quake)})
        self.world.worlds[1].er_seed = 0
        self.world.worlds[1].create_regions()
        self.world.worlds[1].create_items()
        self.world.itempool.extend(get_dungeon_item_pool(self.world))
        self.world.itempool.extend(ItemFactory(['Green Pendant', 'Red Pendant', 'Blue Pendant', 'Beat Agahnim 1', 'Beat Agahnim 2', 'Crystal 1', 'Crystal 2', 'Crystal 3', 'Crystal 4', 'Crystal 5', 'Crystal 6', 'Crystal 7'], 1))
        self.world.get_location('Agahnim 1', 1).item = None
        self.world.get_location('Agahnim 2', 1).item = None
        self.world.precollected_items[1].clear()
        self.world.itempool.append(ItemFactory('Pegasus Boots', 1))
        mark_dark_world_regions(self.world, 1)
        self.world.worlds[1].set_rules()