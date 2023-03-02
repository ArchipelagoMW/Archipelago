from . import MCTestBase
from ..Options import minecraft_options

from BaseClasses import ItemClassification

class AdvancementTestBase(MCTestBase):
    options = {
        "advancement_goal": minecraft_options["advancement_goal"].range_end
    }

    def test_beatable(self):
        self.multiworld.state = self.multiworld.get_all_state(False)
        self.assertBeatable(True)

class ShardTestBase(MCTestBase):
    options = {
        "egg_shards_required": minecraft_options["egg_shards_required"].range_end,
        "egg_shards_available": minecraft_options["egg_shards_available"].range_end
    }

    def test_beatable(self):
        assert len(self.multiworld.get_unfilled_locations()) == len(self.multiworld.itempool)
        self.multiworld.state = self.multiworld.get_all_state(False)
        self.assertBeatable(True)

class CompassTestBase(MCTestBase):
    def test_compasses_in_pool(self):
        state = self.multiworld.get_all_state(False)
        assert state.has("Structure Compass (Village)", 1)
        assert state.has("Structure Compass (Pillager Outpost)", 1)
        assert state.has("Structure Compass (Nether Fortress)", 1)
        assert state.has("Structure Compass (Bastion Remnant)", 1)
        assert state.has("Structure Compass (End City)", 1)

class NoBeeTestBase(MCTestBase):
    options = {
        "bee_traps": 0
    }

    # With no bees, there are no traps in the pool
    def test_bees(self):
        for item in self.multiworld.itempool:
            assert item.classification != ItemClassification.trap


class AllBeeTestBase(MCTestBase):
    options = {
        "bee_traps": 100
    }

    # With max bees, there are no filler items, only bee traps
    def test_bees(self):
        for item in self.multiworld.itempool:
            assert item.classification != ItemClassification.filler
