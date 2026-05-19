from . import OkamiTestBase
from ..Enums.DivineInstruments import DivineInstruments


class TestDivineInstruments(OkamiTestBase):

    def test_regular_instruments(self) -> None:
        self.world_setup()
        # Make sure divine retribution is precollected
        self.assertIs(self.count(DivineInstruments.DIVINE_RETRIBUTION.value.item_name), 1)
        # Collect everything
        self.collect_all_but([""])
        for i in DivineInstruments:
            # We still have 1 of each, and not a 2nd divine retribution.
            self.assertIs(self.count(i.value.item_name), 1)
        # No progressive weapons, they're not enabled.
        self.assertIs(self.count("Progressive Mirror"), 0)
        self.assertIs(self.count("Progressive Sword"), 0)
        self.assertIs(self.count("Progressive Rosary"), 0)

    def test_progressive_instruments(self) -> None:
        self.options = {
            "ProgressiveWeapons": 1
        }

        self.world_setup()
        # Make sure divine retribution is precollected
        self.assertIs(self.count(DivineInstruments.DIVINE_RETRIBUTION.value.item_name), 1)
        self.collect_all_but([""])
        for i in DivineInstruments:
            # Still only 1 divine retribution
            if i.value.item_name == DivineInstruments.DIVINE_RETRIBUTION.value.item_name:
                self.assertIs(self.count(i.value.item_name), 1)
            else:
                # No other regular weapons
                self.assertIs(self.count(i.value.item_name), 0)
        # Check progressive weapons count
        self.assertIs(self.count("Progressive Mirror"), 4)
        self.assertIs(self.count("Progressive Sword"), 5)
        self.assertIs(self.count("Progressive Rosary"), 5)
