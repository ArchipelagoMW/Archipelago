from .bases import APQuestTestBase


class TestHammerOff(APQuestTestBase):
    options = {
        "hammer": False,
    }

    # Once again, this is just default settings, so running the default tests would be wasteful.
    run_default_tests = False

    # The hammer option adds the Hammer item to the itempool.
    # Since the hammer option is off in this TestCase, we have to verify that the Hammer is *not* in the itempool.
    def test_hammer_doesnt_exist(self) -> None:
        # An easy way to verify that an item is or is not in the itempool is by using WorldTestBase.get_items_by_name().
        # This will return a list of all matching items, which we can check for its length.
        hammers_in_itempool = self.get_items_by_name("Hammer")
        self.assertEqual(len(hammers_in_itempool), 0)

    # If the hammer option is not enabled, the Top Middle Chest should just be accessible with nothing.
    def test_hammer_is_not_required_for_top_middle_chest(self) -> None:
        # To check whether an item is required for a location, we would use self.assertAccessDependency.
        # However, in this case, we want to check that the Hammer *isn't* required for the Top Middle Chest location.
        # The robust way to do this is to collect every item into the state except for the Hammer,
        # then assert that the location is reachable.
        # Luckily, there is a helper for this: "collect_all_but".
        self.collect_all_but("Hammer")

        # Now, we manually check that the location is accessible using location.can_reach(state):
        top_middle_chest_player_one = self.world.get_location("Top Middle Chest")
        self.assertTrue(top_middle_chest_player_one.can_reach(self.multiworld.state))


class TestHammerOn(APQuestTestBase):
    options = {
        "hammer": True,
    }

    # When the hammer option is on, the Hammer should exist in the itempool. Let's verify that.
    def test_hammer_exists(self) -> None:
        # Nothing new to say here, but I do want to take this opportunity to teach you some Python magic. :D
        # In Python, when you check for the truth value of something that isn't a bool,
        # it will be implicitly converted to a bool automatically.
        # Which instances of a class convert to "False" and which convert to "True" is class-specific.
        # In the case of lists (or containers in general), empty means False, and not-empty means True.
        # bool([]) -> False
        # bool([1, 2, 3]) -> True
        # So, after grabbing all instances of the Hammer item from the itempool as a list ...
        hammers_in_itempool = self.get_items_by_name("Hammer")

        # ... instead of checking that the len() is 1, we can run this absolutely beautiful statement instead:
        self.assertTrue(hammers_in_itempool)

        # I love Python <3

    # When the hammer option is on, the Hammer is required for the Top Middle Chest.
    def test_hammer_is_required_for_top_middle_chest(self) -> None:
        # This case is simple again: Just run self.assertAccessDependency()
        self.assertAccessDependency(["Top Middle Chest"], [["Hammer"]])

        # This unit test genuinely found an error in the world code when it was first written!
        # The Hammer logic was not actually being correctly applied even if the hammer option was enabled,
        # and the generator thought Top Middle Chest was considered accessible without the Hammer.
        # This is why testing can be extremely valuable.
