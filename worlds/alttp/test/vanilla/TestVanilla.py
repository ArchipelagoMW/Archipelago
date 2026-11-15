from ...Dungeons import get_dungeon_item_pool
from ...InvertedRegions import mark_dark_world_regions
from ...ItemPool import difficulties
from ...Items import item_factory
from ...Options import GlitchesRequired

from ..bases import LTTPTestBase, TestBase


class TestVanilla(TestBase, LTTPTestBase):
    def setUp(self):
        self.world_setup()
        self.multiworld.worlds[1].options.glitches_required = GlitchesRequired.from_any("no_glitches")
        self.multiworld.worlds[1].difficulty_requirements = difficulties['normal']
        self.multiworld.worlds[1].options.bombless_start.value = True
        self.multiworld.worlds[1].options.shuffle_capacity_upgrades.value = 2
        self.multiworld.worlds[1].er_seed = 0
        self.multiworld.worlds[1].create_regions()
        self.multiworld.worlds[1].create_items()
        self.multiworld.itempool.extend(get_dungeon_item_pool(self.multiworld))
        self.multiworld.itempool.extend(item_factory(['Green Pendant', 'Red Pendant', 'Blue Pendant', 'Beat Agahnim 1', 'Beat Agahnim 2', 'Crystal 1', 'Crystal 2', 'Crystal 3', 'Crystal 4', 'Crystal 5', 'Crystal 6', 'Crystal 7'], self.world))
        self.multiworld.get_location('Agahnim 1', 1).item = None
        self.multiworld.get_location('Agahnim 2', 1).item = None
        mark_dark_world_regions(self.multiworld, 1)
        self.world.set_rules()
