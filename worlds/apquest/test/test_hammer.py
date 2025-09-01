from typing import cast

from test.general import gen_steps, setup_multiworld
from test.multiworld.test_multiworlds import MultiworldTestBase
from ..items import APQuestItem

from ..world import APQuestWorld


# Sometimes, you might want to perform tests on a multiworld game with two or more of your worlds.
# In our case, we'll make a multiworld where one world has the hammer option enabled, and the other doesn't.
# This allows us to efficiently test both scenarios in one.
# However, the MultiworldTestBase is a little less fleshed out, so we have to do some of the work ourselves.
class TestHammer(MultiworldTestBase):
    # WorldTestBase has a default setUp method that uses ClassVars that you define in your subclass.
    # MultiworldTestBase doesn't have this, so we have to write our own.
    # Luckily, we can still make use of several helper functions.
    def setUp(self) -> None:
        # test.general.setup_multiworld allows us to easily create a multiworld.
        # All we have to provide is a list of world classes that the worlds should be created from.
        # In our case, we want two APQuestWorlds
        self.multiworld = setup_multiworld([APQuestWorld, APQuestWorld], ())

        # We'll set the "hammer" option to False for world 1, and True for world 2.
        # The "cast" is here because otherwise, type checkers would not be able to resolve the "hammer" option.
        # Also worth noting is that multiworld.worlds is 1-indexed in that the index represents the actual world number.
        cast(APQuestWorld, self.multiworld.worlds[1]).options.hammer.value = False
        cast(APQuestWorld, self.multiworld.worlds[2]).options.hammer.value = True

        # Finally, we need to run the generation steps (create_regions, create_items etc.)
        # We can do this using a helper method on MultiworldTestBase and a helper constant in test.general:
        self.assertSteps(gen_steps)

    # The hammer option adds the Hammer item to the itempool, so let's verify that it's there (only when it should be).
    def test_hammer_exists(self) -> None:
        # To test whether an item exists, we need to find it in the itempool
        # Note: The Item class overrides __eq__, so you could do this using TestCase.assertIn with an Item instance
        # However, the author dislikes this pattern and would rather check for the necessary conditions inside a next()
        with self.subTest("Test that Hammer doesn't exist if hammer option is not enabled"):
            # Finding a specific item for a specific player can be done by iterating the multiworld itempool,
            # comparing item.player and item.name to the desired values.
            hammer = next(
                (item for item in self.multiworld.itempool if item.player == 1 and item.name == "Hammer"), None
            )
            self.assertIsNone(hammer)

        with self.subTest("Test that Hammer item exists and is progression if hammer option is enabled"):
            hammer = next(
                (item for item in self.multiworld.itempool if item.player == 2 and item.name == "Hammer"), None
            )
            self.assertIsNotNone(hammer)
            self.assertTrue(cast(APQuestItem, hammer).advancement)

    # If the hammer option is enabled, a breakable wall is placed in front of the top middle chest.
    # Let's test that this requirement is correctly added in the logic.
    def test_hammer_is_required_for_top_middle_chest(self) -> None:
        with self.subTest("Test that hammer isn't required for Top Middle Chest if hammer option is disabled"):
            # The multiworld class has functions for get_location, get_entrance etc. as well.
            # When using these versions of the functions, you need to provide the name and the player number.
            top_middle_chest_player_one = self.multiworld.get_location("Top Middle Chest", 1)
            self.assertTrue(top_middle_chest_player_one.can_reach(self.multiworld.state))

        with self.subTest("Test that hammer is required for Top Middle Chest if hammer option is enabled"):
            top_middle_chest_player_two = self.multiworld.get_location("Top Middle Chest", 2)
            self.assertFalse(top_middle_chest_player_two.can_reach(self.multiworld.state))

            # We'll create an instance of the Hammer item, then collect it into the state.
            # For this, we can use our world's create_item method.
            # You could also use the same strategy as above and grab the instance of the item from the itempool instead.
            hammer = self.multiworld.worlds[2].create_item("Hammer")
            self.multiworld.state.collect(hammer)

            self.assertTrue(top_middle_chest_player_two.can_reach(self.multiworld.state))

        # This unit test genuinely found an error in the world code when it was first written!
        # This is why testing can be extremely valuable.
