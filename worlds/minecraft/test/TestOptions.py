from . import MCTestBase
from ..Constants import region_info
from .. import Options

from BaseClasses import ItemClassification

class AdvancementTestBase(MCTestBase):
    options = {
        "advancement_goal": Options.AdvancementGoal.range_end
    }
    # beatability test implicit

class ShardTestBase(MCTestBase):
    options = {
        "egg_shards_required": Options.EggShardsRequired.range_end,
        "egg_shards_available": Options.EggShardsAvailable.range_end
    }

    # check that itempool is not overfilled with shards
    def test_itempool(self):
        assert len(self.multiworld.get_unfilled_locations()) == len(self.multiworld.itempool)

class CompassTestBase(MCTestBase):
    def test_compasses_in_pool(self):
        structures = [x[1] for x in region_info["default_connections"]]
        itempool_str = {item.name for item in self.multiworld.itempool}
        for struct in structures:
            assert f"Structure Compass ({struct})" in itempool_str

class NoBeeTestBase(MCTestBase):
    options = {
        "bee_traps": Options.BeeTraps.range_start
    }

    # With no bees, there are no traps in the pool
    def test_bees(self):
        for item in self.multiworld.itempool:
            assert item.classification != ItemClassification.trap


class AllBeeTestBase(MCTestBase):
    options = {
        "bee_traps": Options.BeeTraps.range_end
    }

    # With max bees, there are no filler items, only bee traps
    def test_bees(self):
        for item in self.multiworld.itempool:
            assert item.classification != ItemClassification.filler
