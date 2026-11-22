from .bases import Dota2TestBase

class BasicTestLogic(Dota2TestBase):
    options = {
        "goal_type": "standard",
        "total_wins_to_win": 3,
        "primordial_fragments_to_win": 10,
        # Options you don't specify will use their default values.
        # It is good practice to specify every option that has an impact on your test, even when it's the default value.
    }

    def test_basic_access(self) -> None:
        with self.subTest("Test checks accessible with nothing"):
            tango = self.world.get_location("Tango")
            iron_branch = self.world.get_location("Iron Branch")

            # Since access rules have a "state" argument, we must pass our current CollectionState.
            # Helpfully, since we're in a WorldTestBase, we can just use "self.multiworld.state".
            self.assertTrue(tango.can_reach(self.multiworld.state))  # consumables need no unlock
            # Iron Branch needs its shop unlock
            self.assertFalse(iron_branch.can_reach(self.multiworld.state))
            self.collect_by_name("Unlock branches")
            self.assertTrue(iron_branch.can_reach(self.multiworld.state))
