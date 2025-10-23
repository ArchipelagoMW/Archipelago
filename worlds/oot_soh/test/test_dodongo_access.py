from .. import SohWorld
from ..Items import progressive_items, Items, Locations
from .bases import SohTestBase


class TestCanReachKingDodongo(SohTestBase):
    options = {"shuffle_boss_souls": 1}
    world: SohWorld

    def test_king_dodongo_no_soul(self):
        """
        Checking if player can kill king dodongo
        """
        self.collect_by_name(Items.PROGRESSIVE_BOMB_BAG)
        self.collect_by_name(Items.BOMBCHUS_5)
        self.collect_by_name(Items.STICKS)

        self.assertFalse(self.can_reach_location(Locations.KING_DODONGO),
                         f"Was able to Kill King Dodongo, but shouldn't have been able to.")

    def test_king_dodongo_with_soul(self):
        """
        Checking if player can kill king dodongo
        """
        self.collect_by_name(Items.PROGRESSIVE_BOMB_BAG)
        self.collect_by_name(Items.STICKS)
        self.collect_by_name(Items.KING_DODONGOS_SOUL)
        self.collect_by_name(Items.PROGRESSIVE_SLINGSHOT)

        self.assertTrue(self.can_reach_location(Locations.KING_DODONGO),
                        f"Failed to kill King Dodongo")
