
from test.param import classvar_matrix

from .bases import APQuestTestBase

# Sometimes, you might want to test something with a specific option disabled, and then with it enabled.
# To do this efficiently, we can use param.classvar_matrix.
# First, we prepare a list of every option(s combination) we want to test:
extra_starting_chest_options = [
    {"extra_starting_chest": False},
    {"extra_starting_chest": True},
]


# Then, we decorate our TestCase with @classvar_matrix, passing our options into it.
# Our TestCase will then be run once with the extra_starting_chest option disabled, and once with it enabled.
# Remember: The WorldTestBase class has a ClassVar called "options", which is what we're setting here.
# CAREFUL: Passing multiple ClassVars to classvar_matrix will run *all combinations*, not perform a "zip" operation.
@classvar_matrix(options=extra_starting_chest_options)
class TestExtraStartingChest(APQuestTestBase):
    # Our extra starting chest only exists if the extra_starting_chest option is enabled, so let's verify that.
    def test_extra_starting_chest_exists(self) -> None:
        # Remember: Each test here will get run twice:
        # Once with the "extra_starting_chest" option disabled, and once with it enabled.
        # We need to check which case we're in, and run the appropriate test.
        if self.world.options.extra_starting_chest:
            with self.subTest("Test that Bottom Left Extra Chest exists when extra_starting_chest option is enabled"):
                # Currently, the best way to check for the existence of a location is to try using get_location,
                # then catch the KeyError that is raised if the location doesn't exist.
                # This makes this test a bit awkward, because TestCase has an assertRaises, but not an assertNotRaises.
                try:
                    self.world.get_location("Bottom Left Extra Chest")
                except KeyError:
                    self.fail("Bottom Left Extra Chest should exist, but it doesn't.")
        else:
            with self.subTest(
                "Test that Bottom Left Extra Chest does not exist when extra_starting_chest option is disabled"
            ):
                self.assertRaises(KeyError, self.world.get_location, "Bottom Left Extra Chest")
