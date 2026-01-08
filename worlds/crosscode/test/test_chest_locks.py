import typing
from BaseClasses import CollectionState
from . import CrossCodeTestBase

class TestChestLocks(CrossCodeTestBase):
    options = { "chest_lock_rando": True }

    def get_no_keys_state(self) -> CollectionState:
        all_state = self.multiworld.get_all_state(use_cache=False)

        # get the key items
        items = self.get_items_by_name(("Thief's Key", "White Key", "Radiant Key"))
        for item in items:
            all_state.remove(item)

        return all_state

    def check_chest_accessibility(self, state: CollectionState, clearances: typing.Iterable[str]):
        """
        Utility function that verifies that all chests with a clearance in `clearances` is accessible and that all
        other chests are not.
        """
        for id, clearance in self.world.logic_dict["chest_clearance_levels"].items():
            if clearance in clearances:
                self.assertIn(
                    self.world.create_location(self.world.location_id_to_name[id]),
                    state.locations_checked
                )
            else:
                self.assertNotIn(
                    self.world.create_location(self.world.location_id_to_name[id]),
                    state.locations_checked
                )

    def test_only_default_chests_accessible(self):
        no_keys_state = self.get_no_keys_state()
        self.check_chest_accessibility(no_keys_state, ("Default"))

    def test_default_and_bronze_chests_accessible_with_thief(self):
        no_keys_state = self.get_no_keys_state()
        no_keys_state.collect(self.get_item_by_name("Thief's Key"))
        self.check_chest_accessibility(no_keys_state, ("Default", "Bronze"))

    def test_default_and_silver_chests_accessible_with_white(self):
        no_keys_state = self.get_no_keys_state()
        no_keys_state.collect(self.get_item_by_name("White Key"))
        self.check_chest_accessibility(no_keys_state, ("Default", "Silver"))

    def test_default_and_gold_chests_accessible_with_radiant(self):
        no_keys_state = self.get_no_keys_state()
        no_keys_state.collect(self.get_item_by_name("Radiant Key"))
        self.check_chest_accessibility(no_keys_state, ("Default", "Gold"))
