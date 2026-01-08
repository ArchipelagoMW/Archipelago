from .bases import SohTestBase
from ..Enums import Items, Locations


class TestTime(SohTestBase):
    options = {"starting_age": "adult", "shuffle_grass": "all"}

    # test that you cannot cut the market grass if you do not have a grass cutter for child Link
    def test_wrong_age_grass(self):
        self.collect_all_but([Items.GORONS_BRACELET, Items.STRENGTH_UPGRADE, Items.BOOMERANG, Items.KOKIRI_SWORD,
                              Items.BOMB_BAG, Items.PROGRESSIVE_BOMB_BAG, Items.PROGRESSIVE_BOMBCHU])
        self.assertFalse(self.can_reach_location(Locations.MARKET_MARKET_GRASS1),
                         "Can access child-exclusive grass without an item that child can use to break it.")
        self.collect_by_name([Items.STRENGTH_UPGRADE])
        self.assertTrue(self.can_reach_location(Locations.MARKET_MARKET_GRASS1))
