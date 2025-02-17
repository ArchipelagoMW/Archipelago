from worlds.banjo_tooie.Names import itemName, locationName
from ..Options import KingJingalingHasJiggy, RandomizeJinjos
from . import BanjoTooieTestBase

#This file contains tests of options that barely do anything.

class TestVanillaJingalingJiggy(BanjoTooieTestBase):
    options = {
        "jingaling_jiggy": KingJingalingHasJiggy.option_true,
        "randomize_jinjos": RandomizeJinjos.option_true # Just so that jinjo jiggies are also in the pool.
    }
    def test_item_pool(self) -> None:
        item_pool_names = [item.name for item in self.multiworld.itempool]
        assert item_pool_names.count(itemName.JIGGY) == 89

    def test_prefill(self) -> None:
        assert [location for location in self.world.get_locations()\
                if location.name == locationName.JIGGYIH10][0].item.name == itemName.JIGGY

class TestRandomizedJingalingJiggy(BanjoTooieTestBase):
    options = {
        "jingaling_jiggy": KingJingalingHasJiggy.option_false,
        "randomize_jinjos": RandomizeJinjos.option_true
    }
    def test_item_pool(self) -> None:
        item_pool_names = [item.name for item in self.multiworld.itempool]
        assert item_pool_names.count(itemName.JIGGY) == 90
