from worlds.banjo_tooie.Names import itemName, locationName
from ..Options import KingJingalingHasJiggy, RandomizeJinjos, WorldRequirements
from . import BanjoTooieTestBase

#This file contains tests of options that barely do anything.

class TestVanillaJingalingJiggy(BanjoTooieTestBase):
    options = {
        "jingaling_jiggy": KingJingalingHasJiggy.option_true,
        "randomize_jinjos": RandomizeJinjos.option_true, # Just so that jinjo jiggies are also in the pool.
        "world_requirements": WorldRequirements.option_custom,
        "custom_worlds": "1,1,1,1,1,1,1,1,61"
    }
    def test_item_pool(self) -> None:
        progression_jiggies = sum(1 for item in self.multiworld.itempool if item.advancement and item.name == itemName.JIGGY)
        useful_jiggies = sum(1 for item in self.multiworld.itempool if item.useful and item.name == itemName.JIGGY)
        assert progression_jiggies == 60
        assert useful_jiggies == 15

    def test_prefill(self) -> None:
        assert [location for location in self.world.get_locations()\
                if location.name == locationName.JIGGYIH10][0].item.name == itemName.JIGGY

class TestRandomizedJingalingJiggy(BanjoTooieTestBase):
    options = {
        "jingaling_jiggy": KingJingalingHasJiggy.option_false,
        "randomize_jinjos": RandomizeJinjos.option_true,
        "world_requirements": WorldRequirements.option_custom,
        "custom_worlds": "1,1,1,1,1,1,1,1,61",
    }
    def test_item_pool(self) -> None:
        progression_jiggies = sum(1 for item in self.multiworld.itempool if item.advancement and item.name == itemName.JIGGY)
        useful_jiggies = sum(1 for item in self.multiworld.itempool if item.useful and item.name == itemName.JIGGY)
        assert progression_jiggies == 61
        assert useful_jiggies == 15
