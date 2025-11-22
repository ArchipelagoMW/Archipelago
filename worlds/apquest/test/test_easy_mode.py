from .bases import APQuestTestBase


# When writing a test, you'll first need to subclass unittest.TestCase.
# In our case, we'll subclass the APQuestTestBase we defined in bases.py.
class TestEasyModeLogic(APQuestTestBase):
    # Our test base is a subclass of WorldTestBase.
    # WorldTestBase takes a dict of options and sets up a multiworld for you with a single world of your game.
    # The world will have the options you specified.
    options = {
        "hard_mode": False,
        # Options you don't specify will use their default values.
        # It is good practice to specify every option that has an impact on your test, even when it's the default value.
        # As such, we'll spell out that hard_mode is meant to be False.
        # All other options in APQuest are cosmetic, so we don't need to list them.
    }

    # At this point, we could stop, and a few default tests would be run on our world.
    # At the time of writing (2025-09-04), this includes the following tests:
    # - If you have every item, every location can be reached
    # - If you have no items, you can still reach something ("Sphere 1" is not empty)
    # - The world successfully generates (Fill does not crash)

    # This is already useful, but we also want to do our own tests.
    # A test is a function whose name starts with "test".
    def test_easy_mode_access(self) -> None:
        # Inside a test, we can manually collect items, check access rules, etc.
        # For example, we could check that the two early chests are already accessible despite us having no items.
        # For the sake of structure, let's have every test item in its own subtest.
        with self.subTest("Test checks accessible with nothing"):
            bottom_left_chest = self.world.get_location("Bottom Left Chest")
            top_middle_chest = self.world.get_location("Top Middle Chest")

            # Since access rules have a "state" argument, we must pass our current CollectionState.
            # Helpfully, since we're in a WorldTestBase, we can just use "self.multiworld.state".
            self.assertTrue(bottom_left_chest.can_reach(self.multiworld.state))
            self.assertTrue(top_middle_chest.can_reach(self.multiworld.state))

        # Next, let's test that the top left room location requires the key to unlock the door.
        with self.subTest("Test key is required to get top left chest"):
            top_left_room_chest = self.world.get_location("Top Left Room Chest")

            # Right now, this location should *not* be accessible, as we don't have the key yet.
            self.assertFalse(top_left_room_chest.can_reach(self.multiworld.state))

            # Now, let's collect the Key.
            # For this, there is a handy helper function to collect items from the itempool.
            # Keep in mind that while test functions are sectioned off from one another, subtests are not.
            # Collecting this here means that the state will have the Key for all future subtests in this function.
            self.collect_by_name("Key")

            # The top left room chest should now be accessible.
            self.assertTrue(top_left_room_chest.can_reach(self.multiworld.state))

        # Next, let's test that you need the sword to access locations that require it (bush room and enemies).
        with self.subTest("Test sword is required for enemy and bush locations"):
            # Manually checking the dependency in the previous function was a bit of a hassle, wasn't it?
            # Now we are checking four locations. It would be even longer as a result.
            # Well, there is another option. It's the assertAccessDependency function of WorldTestBase.
            self.assertAccessDependency(
                [
                    "Bottom Right Room Right Chest",
                    "Bottom Right Room Left Chest",
                    "Right Room Enemy Drop",
                    "Final Boss Defeated",  # Reminder: APQuest's victory condition uses this event location
                ],
                [["Sword"]],
            )

            # The assertAccessDependency function is a bit complicated, so let's discuss what it does.
            # By default, the locations argument must contain *every* location that *hard-depends* on the items.
            # So, in our case: If every item except Sword is collected, *exactly* these four locations are unreachable.

            # The possible_items argument is initially more intuitive, but has some complexity as well.
            # In our case, we only care about one item. But sometimes, we care about multiple items at once.
            # This is why we pass a list of lists. We'll discuss this more when we test hard mode logic.

        # Let's do one more test: That the key is required for the Button.
        with self.subTest("Test that the Key is required to activate the Button"):
            # The Button is not the only thing that depends on the Key.
            # As explained above, the locations list must be exhaustive.
            # Thus, we would have to add the "Top Left Room Chest" as well.
            # However, we can set "only_check_listed" if we only want the Top Left Room Button location to be checked.
            self.assertAccessDependency(
                ["Top Left Room Button"],
                [["Key"]],
                only_check_listed=True,
            )

    def test_easy_mode_health_upgrades(self) -> None:
        # For our second test, let's make sure that we have two Health Upgrades with the correct classification.

        # We can find the Health Upgrades in the itempool like this:
        health_upgrades = self.get_items_by_name("Health Upgrade")

        # First, let's verify there's two of them.
        with self.subTest("Test that there are two Health Upgrades in the pool"):
            self.assertEqual(len(health_upgrades), 2)

        # Then, let's verify that they have the useful classification and NOT the progression classification.
        with self.subTest("Test that the Health Upgrades in the pool are useful, but not progression."):
            # To check whether an item has a certain classification, you can use the following helper properties:
            # item.filler, item.trap, item.useful and... item.advancement. No, not item.progression...
            # (Just go with it, AP is old and has had many name changes over the years :D)
            self.assertTrue(all(health_upgrade.useful for health_upgrade in health_upgrades))
            self.assertFalse(any(health_upgrade.advancement for health_upgrade in health_upgrades))
