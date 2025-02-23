from . import MessengerTestBase


class StartIventoryTest(MessengerTestBase):
    options = {
        "start_inventory": {
            "Wingsuit": 1,
            "Rope Dart": 1,
        }
    }

    def test_items_removed_from_pool(self):
        """Tests that the start inventory items don't exist in the itempool."""
        for item in self.multiworld.itempool:
            self.assertFalse(item in self.options["start_inventory"])
