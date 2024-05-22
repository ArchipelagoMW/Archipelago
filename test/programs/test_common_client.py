import unittest

from CommonClient import CommonContext


class TestCommonContext(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.ctx = CommonContext()
        # Using IDs outside the "safe range" for testing purposes only. If this fails unit tests, it's because
        # another world is not following the spec for allowed ID ranges.
        self.ctx.update_data_package({
            "games": {
                "__TestGame1": {
                    "location_name_to_id": {
                        "Test Location 1 - Safe": 2**64 + 1,
                        "Test Location 2 - Duplicate": 2**64 + 2,
                    },
                    "item_name_to_id": {
                        "Test Item 1 - Safe": 2**64 + 1,
                        "Test Item 2 - Duplicate": 2**64 + 2,
                    },
                },
                "__TestGame2": {
                    "location_name_to_id": {
                        "Test Location 3 - Duplicate": 2**64 + 2,
                    },
                    "item_name_to_id": {
                        "Test Item 3 - Duplicate": 2**64 + 2,
                    },
                },
            },
        })

    async def test_archipelago_datapackage_lookups_exist(self):
        assert "Archipelago" in self.ctx.item_names, "Archipelago item names entry does not exist"
        assert "Archipelago" in self.ctx.location_names, "Archipelago location names entry does not exist"

    async def test_implicit_name_lookups(self):
        # Items
        assert self.ctx.item_names[2 ** 64 + 1] == "Test Item 1 - Safe"
        assert self.ctx.item_names[2 ** 64 + 2] == f"Ambiguous item (ID: {2 ** 64 + 2})"
        assert self.ctx.item_names[2 ** 64 + 3] == f"Unknown item (ID: {2 ** 64 + 3})"
        assert self.ctx.item_names[-1] == "Nothing"

        # Locations
        assert self.ctx.location_names[2 ** 64 + 1] == "Test Location 1 - Safe"
        assert self.ctx.location_names[2 ** 64 + 2] == f"Ambiguous location (ID: {2 ** 64 + 2})"
        assert self.ctx.location_names[2 ** 64 + 3] == f"Unknown location (ID: {2 ** 64 + 3})"
        assert self.ctx.location_names[-1] == "Cheat Console"

    async def test_explicit_name_lookups(self):
        # Items
        assert self.ctx.item_names["__TestGame1"][2 ** 64 + 1] == "Test Item 1 - Safe"
        assert self.ctx.item_names["__TestGame1"][2 ** 64 + 2] == "Test Item 2 - Duplicate"
        assert self.ctx.item_names["__TestGame1"][2 ** 64 + 3] == f"Unknown item (ID: {2 ** 64 + 3})"
        assert self.ctx.item_names["__TestGame1"][-1] == "Nothing"
        assert self.ctx.item_names["__TestGame2"][2 ** 64 + 1] == f"Unknown item (ID: {2 ** 64 + 1})"
        assert self.ctx.item_names["__TestGame2"][2 ** 64 + 2] == "Test Item 3 - Duplicate"
        assert self.ctx.item_names["__TestGame2"][2 ** 64 + 3] == f"Unknown item (ID: {2 ** 64 + 3})"
        assert self.ctx.item_names["__TestGame2"][-1] == "Nothing"

        # Locations
        assert self.ctx.location_names["__TestGame1"][2 ** 64 + 1] == "Test Location 1 - Safe"
        assert self.ctx.location_names["__TestGame1"][2 ** 64 + 2] == "Test Location 2 - Duplicate"
        assert self.ctx.location_names["__TestGame1"][2 ** 64 + 3] == f"Unknown location (ID: {2 ** 64 + 3})"
        assert self.ctx.location_names["__TestGame1"][-1] == "Cheat Console"
        assert self.ctx.location_names["__TestGame2"][2 ** 64 + 1] == f"Unknown location (ID: {2 ** 64 + 1})"
        assert self.ctx.location_names["__TestGame2"][2 ** 64 + 2] == "Test Location 3 - Duplicate"
        assert self.ctx.location_names["__TestGame2"][2 ** 64 + 3] == f"Unknown location (ID: {2 ** 64 + 3})"
        assert self.ctx.location_names["__TestGame2"][-1] == "Cheat Console"
