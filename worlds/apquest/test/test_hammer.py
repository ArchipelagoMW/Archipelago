from typing import cast

from test.param import classvar_matrix

from ..items import APQuestItem
from .bases import APQuestTestBase

# This file assumes that you've read test_extra_starting_chest.py first.
# classvar_matrix will not be explained again here, so make sure you've read that first.

# We'll once again use classvar_matrix to test that the world behaves correctly both if "hammer" option is disabled,
# and also that it behaves correctly when the "hammer" option is enabled.
hammer_options = [
    {"hammer": False},
    {"hammer": True},
]


@classvar_matrix(options=hammer_options)
class TestHammer(APQuestTestBase):
    # The hammer option adds the Hammer item to the itempool, so let's verify that it's there (only when it should be).
    # Remember: Each test here will get run twice, once with the "hammer" option disabled, and once with it enabled.
    # We need to check which case we're in, and react appropriately.
    def test_hammer_exists(self) -> None:
        if self.world.options.hammer:
            # To test whether an item exists, we need to find it in the itempool
            # Note: The Item class overrides __eq__, so you could do this using TestCase.assertIn with an Item instance
            # However, the author dislikes this pattern and prefers checking the necessary conditions inside a next().
            with self.subTest("Test that Hammer item exists and is progression if hammer option is enabled"):
                hammer = next((item for item in self.multiworld.itempool if item.name == "Hammer"), None)
                self.assertIsNotNone(hammer)
                self.assertTrue(cast(APQuestItem, hammer).advancement)
        else:
            with self.subTest("Test that Hammer doesn't exist if hammer option is not enabled"):
                # Finding a specific item for a specific player can be done by iterating the multiworld itempool,
                # comparing item.player and item.name to the desired values.
                hammer = next((item for item in self.multiworld.itempool if item.name == "Hammer"), None)
                self.assertIsNone(hammer)

    # If the hammer option is enabled, a breakable wall is placed in front of the top middle chest.
    # Let's test that this requirement is correctly added in the logic.
    def test_hammer_is_required_for_top_middle_chest(self) -> None:
        if self.world.options.hammer:
            with self.subTest("Test that hammer is required for Top Middle Chest if hammer option is enabled"):
                self.assertAccessDependency(["Top Middle Chest"], [["Hammer"]])
        else:
            with self.subTest("Test that hammer isn't required for Top Middle Chest if hammer option is disabled"):
                # In this case, we want to check that the Hammer *isn't* required for the Top Middle Chest location.
                # The robust way to do this is to collect every item into the state except for the Hammer,
                # then assert that the location is reachable.
                # Luckily, there is a helper for this: "collect_all_but".
                self.collect_all_but("Hammer")

                # Now, we manually check that the location is accessible using location.can_reach(state):
                top_middle_chest_player_one = self.world.get_location("Top Middle Chest")
                self.assertTrue(top_middle_chest_player_one.can_reach(self.multiworld.state))

        # This unit test genuinely found an error in the world code when it was first written!
        # This is why testing can be extremely valuable.
