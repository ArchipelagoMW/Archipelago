from BaseClasses import CollectionState
from worlds.rac3.test import RAC3TestBase


class TestBiobliterator(RAC3TestBase):

    def test_logic(self):
        state = self.multiworld.state
        self.assertTrue(self.can_reach_region("Veldin"), "Can't start on Veldin")
        self.assertFalse(self.can_reach_region("Florana"), "Florana reachable without coordinates")
        self.assertFalse(self.can_reach_region("Starship Phoenix"), "Starship Phoenix reachable without coordinates")
        self.assertFalse(self.can_reach_region("Command Center"), "Command Center reachable from Veldin")
        self.assertFalse(self.can_reach_location("Command Center: Biobliterator Defeated!"),
                         "Goal reachable from Veldin")

        state.sweep_for_advancements()
        self.assertTrue(self.can_reach_region("Florana"), "Can't reach Florana from Veldin")
        self.assertTrue(self.can_reach_region("Starship Phoenix"), "Can't reach Starship Phoenix from Veldin")
        self.assertFalse(self.can_reach_region("Command Center"), "Command Center reachable from Florana")
        self.assertFalse(self.can_reach_location("Command Center: Biobliterator Defeated!"),
                         "Goal reachable from Florana")

        self.collect_by_name("Infobot: Command Center")
        self.assertTrue(self.can_reach_region("Command Center"), "Can't reach Command Center with coordinates")
        self.assertFalse(self.can_reach_location("Command Center: Biobliterator Defeated!"),
                         "Goal reachable with no items")

        self.collect_by_name(["Hypershot", "Gravity-Boots", "Tyhrra-Guise", "Hacker", "Refractor"])
        self.assertTrue(self.can_reach_location("Command Center: Biobliterator Defeated!"),
                        "Goal not reachable with items")
