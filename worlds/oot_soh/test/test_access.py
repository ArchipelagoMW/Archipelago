from .. import SohWorld
from ..Items import Items, Locations
from .bases import SohTestBase


class TestAccessGBK(SohTestBase):
    """
    Checking to see if the Ganons Boss Key Chest is accessible after passing the Rainbow Bridge.
    This was made to test for this issue https://github.com/aMannus/Archipelago/issues/241
    """
    # fill in the options here, formatted like "shuffle_childs_wallet": False,
    options = {"starting_age": 1, "skip_ganons_trials": True, "rainbow_bridge_greg_modifier": "reward",
               "rainbow_bridge": "greg", "ganons_castle_boss_key_greg_modifier": "wildcard"}
    # options not set here will be set to default
    world: SohWorld

    def test_ganon_bk_chest_skip_trials(self):
        self.collect_by_name(Items.GREG_THE_GREEN_RUPEE)
        self.collect_by_name(Items.BIGGORONS_SWORD)

        self.assertTrue(self.can_reach_location(Locations.GANONS_CASTLE_TOWER_BOSS_KEY_CHEST),
                        f"Wasn't able to reach GBK chest")
