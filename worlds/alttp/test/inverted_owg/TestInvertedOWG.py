from worlds.alttp.Dungeons import get_dungeon_item_pool
from worlds.alttp.EntranceShuffle import link_inverted_entrances
from worlds.alttp.InvertedRegions import create_inverted_regions
from worlds.alttp.ItemPool import difficulties
from worlds.alttp.Items import item_factory
from worlds.alttp.Options import GlitchesRequired
from worlds.alttp.Regions import mark_light_world_regions
from worlds.alttp.Shops import create_shops
from test.bases import TestBase

from worlds.alttp.test import LTTPTestBase


class TestInvertedOWG(TestBase, LTTPTestBase):
    def setUp(self):
        self.world_setup()
        self.multiworld.glitches_required[1] = GlitchesRequired.from_any("overworld_glitches")
        self.multiworld.mode[1].value = 2
        self.multiworld.bombless_start[1].value = True
        self.multiworld.shuffle_capacity_upgrades[1].value = 2
        self.multiworld.worlds[1].difficulty_requirements = difficulties['normal']
        create_inverted_regions(self.multiworld, 1)
        self.world.create_dungeons()
        create_shops(self.multiworld, 1)
        link_inverted_entrances(self.multiworld, 1)
        self.world.create_items()
        self.multiworld.itempool.extend(get_dungeon_item_pool(self.multiworld))
        self.multiworld.itempool.extend(item_factory(['Green Pendant', 'Red Pendant', 'Blue Pendant', 'Beat Agahnim 1', 'Beat Agahnim 2', 'Crystal 1', 'Crystal 2', 'Crystal 3', 'Crystal 4', 'Crystal 5', 'Crystal 6', 'Crystal 7'], self.world))
        self.multiworld.get_location('Agahnim 1', 1).item = None
        self.multiworld.get_location('Agahnim 2', 1).item = None
        self.multiworld.precollected_items[1].clear()
        self.multiworld.itempool.append(item_factory('Pegasus Boots', self.world))
        mark_light_world_regions(self.multiworld, 1)
        self.world.set_rules()
