from typing import cast

from test.general import gen_steps, setup_multiworld
from test.multiworld.test_multiworlds import MultiworldTestBase

from ..world import APQuestWorld


# This file assumes that you've read test_hammer.py first.
# MultiworldTestBase and the custom setUp function will not be explained again here.
# (Author's note: Sorry, I know it would have been more convenient if the tests could be read in alphabetical order...)
class TestExtraStartingChest(MultiworldTestBase):
    def setUp(self) -> None:
        self.multiworld = setup_multiworld([APQuestWorld, APQuestWorld], ())

        cast(APQuestWorld, self.multiworld.worlds[1]).options.extra_starting_chest.value = False
        cast(APQuestWorld, self.multiworld.worlds[2]).options.extra_starting_chest.value = True

        self.assertSteps(gen_steps)

    # Our extra starting chest only exists if the extra_starting_chest option is enabled, so let's verify that.
    def test_extra_starting_chest_exists(self) -> None:
        with self.subTest(
            "Test that Bottom Left Extra Chest does not exist when extra_starting_chest option is disabled"
        ):
            # Currently, the best way to check for the existence of a location is to try getting it using get_location,
            # then catch the KeyError that is raised if it doesn't exist.
            # This makes this test a bit awkward, because TestCase has an assertRaises, but not an assertNotRaises.
            self.assertRaises(KeyError, self.multiworld.get_location, "Bottom Left Extra Chest", 1)

        with self.subTest("Test that Bottom Left Extra Chest exists when extra_starting_chest option is enabled"):
            try:
                self.multiworld.get_location("Bottom Left Extra Chest", 2)
            except KeyError:
                self.fail("Bottom Left Extra Chest should exist, but it doesn't.")
