from .bases import APQuestTestBase


# Sometimes, you might want to test something with a specific option disabled, then with it enabled.
# For this purpose, we'll just have two different TestCase classes.
class TestExtraStartingChestOff(APQuestTestBase):
    options = {
        "extra_starting_chest": False,
    }

    # Hmm... This is just default options again.
    # This would run all the default WorldTestBase tests a second time on default options. That's a bit wasteful.
    # Luckily, there is a way to turn off the default tests for a WorldTestBase subclass:
    run_default_tests = False

    # Since the extra_starting_chest option is False, we'll verify that the Extra Starting Chest location doesn't exist.
    def test_extra_starting_chest_doesnt_exit(self) -> None:
        # Currently, the best way to check for the existence of a location is to try using get_location,
        # then watch for the KeyError that is raised if the location doesn't exist.
        # In a testing context, we can do this with TestCase.assertRaises.
        self.assertRaises(KeyError, self.world.get_location, "Bottom Left Extra Chest")


class TestExtraStartingChestOn(APQuestTestBase):
    options = {
        "extra_starting_chest": True,
    }

    # In this case, running the default tests is acceptable, since this is a unique options combination.

    # Since the extra_starting_chest option is True, we'll verify that the Extra Starting Chest location exists.
    def test_extra_starting_chest_exists(self) -> None:
        # In this case, the location *should* exist, so world.get_location() should *not* KeyError.
        # This is a bit awkward, because unittest.TestCase doesn't have an "assertNotRaises".
        # So, we'll catch the KeyError ourselves, and then fail in the catch block with a custom message.
        try:
            self.world.get_location("Bottom Left Extra Chest")
        except KeyError:
            self.fail("Bottom Left Extra Chest should exist, but it doesn't.")
